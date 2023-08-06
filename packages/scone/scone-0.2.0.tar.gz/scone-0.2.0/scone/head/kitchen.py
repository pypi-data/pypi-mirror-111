#  Copyright 2020, Olivier 'reivilibre'.
#
#  This file is part of Scone.
#
#  Scone is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Scone is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Scone.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import os
import signal
import time
import traceback
from asyncio import Future, Queue
from collections import deque
from contextvars import ContextVar
from pathlib import Path
from typing import Any, Deque, Dict, Optional, Tuple, Type, TypeVar

import cattr
from frozendict import frozendict

from scone.common.chanpro import Channel, ChanProHead
from scone.common.misc import eprint
from scone.head import sshconn
from scone.head.dag import RecipeMeta, RecipeState, Resource, Vertex
from scone.head.dependency_tracking import (
    DependencyBook,
    DependencyCache,
    DependencyTracker,
    hash_dict,
)
from scone.head.head import Head
from scone.head.recipe import Recipe
from scone.sous import utensil_namer
from scone.sous.utensils import Utensil

logger = logging.getLogger(__name__)

current_recipe: ContextVar[Recipe] = ContextVar("current_recipe")

A = TypeVar("A")


class Preparation:
    def __init__(self, head: Head):
        self.dag = head.dag
        self.head = head
        self._queue: Deque[Tuple[Recipe, RecipeMeta]] = deque()
        self._current_recipe: Optional[Recipe] = None

    def needs(
        self,
        requirement: str,
        identifier: str,
        hard: bool = True,
        sous: Optional[str] = "(self)",
        **extra_identifiers: Any,
    ) -> None:
        assert self._current_recipe is not None

        if sous == "(self)":
            sous = self._current_recipe.recipe_context.sous

        resource = Resource.new_lenient(
            requirement, identifier, sous, frozendict(extra_identifiers)
        )

        self.dag.needs(self._current_recipe, resource, not hard)

    def wants(self, requirement: str, identifier: str, **extra_identifiers: Any):
        return self.needs(requirement, identifier, hard=False, **extra_identifiers)

    def provides(
        self,
        requirement: str,
        identifier: str,
        sous: Optional[str] = "(self)",
        **extra_identifiers: Any,
    ) -> None:
        assert self._current_recipe is not None

        if sous == "(self)":
            sous = self._current_recipe.recipe_context.sous

        resource = Resource.new_lenient(
            requirement, identifier, sous, frozendict(extra_identifiers)
        )

        self.dag.provides(self._current_recipe, resource)

    def after(self, other_recipe: "Recipe"):
        assert self._current_recipe is not None
        self.dag.add_ordering(other_recipe, self._current_recipe)

    def before(self, other_recipe: "Recipe"):
        assert self._current_recipe is not None
        self.dag.add_ordering(self._current_recipe, other_recipe)

    def subrecipe(self, sub: "Recipe"):
        self.dag.add(sub)
        self._queue.append((sub, self.dag.recipe_meta[sub]))

    def prepare_all(self) -> None:
        for recipe in self.dag.vertices:
            if not isinstance(recipe, Recipe):
                continue
            meta = self.dag.recipe_meta[recipe]
            if meta.state != RecipeState.LOADED:
                continue
            self._queue.append((recipe, meta))

        while self._queue:
            recipe, meta = self._queue.popleft()
            self._current_recipe = recipe
            recipe.prepare(self, self.head)
            self._current_recipe = None
            meta.state = RecipeState.PREPARED


class Kitchen:
    def __init__(
        self,
        head: "Head",
        dependency_store: DependencyCache,
    ):
        self._chanproheads: Dict[Tuple[str, str], Future[ChanProHead]] = dict()
        self._dependency_store = dependency_store
        self._dependency_trackers: Dict[Recipe, DependencyTracker] = dict()
        self.head = head
        self.last_updated_ats: Dict[Resource, int] = dict()
        self._cookable: Queue[Optional[Vertex]] = Queue()
        self._sleeper_slots: int = 0
        self._kitchen_time: int = int(1000 * time.time())

    def get_dependency_tracker(self):
        return self._dependency_trackers[current_recipe.get()]

    async def get_chanprohead(self, host: str, user: str) -> ChanProHead:
        async def new_conn():
            connection_details = self.head.souss[host]
            # XXX opt ckey =
            #  os.path.join(self.head.directory, connection_details["clientkey"])

            try:
                cp, root = await sshconn.open_ssh_sous(
                    connection_details["host"],
                    connection_details["user"],
                    None,
                    user,
                    connection_details["souscmd"],
                    connection_details.get("dangerous_debug_logging", False),
                )
            except Exception:
                logger.error("Failed to open SSH connection", exc_info=True)
                raise

            return ChanProHead(cp, root)

        hostuser = (host, user)
        if hostuser not in self._chanproheads:
            self._chanproheads[hostuser] = asyncio.create_task(new_conn())

        return await self._chanproheads[hostuser]

    async def prepare_to_cook(self):
        await self._emit_fridge_resources()

        for vertex in self.head.dag.vertices:
            if isinstance(vertex, Recipe):
                rec_meta = self.head.dag.recipe_meta[vertex]
                if rec_meta.incoming_uncompleted == 0:
                    rec_meta.state = RecipeState.COOKABLE
                    self._cookable.put_nowait(vertex)
                else:
                    rec_meta.state = RecipeState.PENDING
            elif isinstance(vertex, Resource):
                res_meta = self.head.dag.resource_meta[vertex]
                if res_meta.incoming_uncompleted == 0:
                    res_meta.completed = True
                    if res_meta.hard_need:
                        needers = self.head.dag.edges[vertex]
                        needers_str = "".join(f" - {n}\n" for n in needers)
                        raise RuntimeError(
                            f"Hard need 「{vertex}」 not satisfiable."
                            f" Needed by:\n{needers_str}"
                        )
                    self._cookable.put_nowait(vertex)

    async def cook_all(self):
        num_workers = 8
        self._sleeper_slots = num_workers - 1

        workers = []
        workers_routines = []
        for _ in range(num_workers):
            worker = CookingWorker(self)
            workers.append(worker)
            workers_routines.append(worker.start())

        # register handler
        def signal_handler_progress(_1, _2):
            eprint("----- SIGUSR1 Progress Report -----")
            for i, worker in enumerate(workers):
                eprint(f"Worker {i} ({worker.state}):")
                eprint(f"  recipe: {worker.current_recipe}")
            eprint("-----------------------------------")

        signal.signal(signal.SIGUSR1, signal_handler_progress)

        await asyncio.gather(*workers_routines, return_exceptions=False)

        # unregister handler
        signal.signal(signal.SIGUSR1, signal.SIG_IGN)

    async def close_all_ssh_connections(self):
        connections = self._chanproheads
        self._chanproheads = dict()

        for _key_tuple, connection_future in connections.items():
            try:
                connection = await connection_future
                await connection.close()
            except Exception:
                traceback.print_exc()

    async def _should_skip(
        self, recipe: Recipe
    ) -> Tuple[Optional[DependencyBook], bool]:
        """
        :param recipe: recipe to inquire about
        :return: dep book, or None if there wasn't one needed to compute this
            and true if the recipe should be skipped, false otherwise.
        """

        only_when_flag_set = False

        if recipe in self.head.dag.watching:
            for watching, only_when in self.head.dag.watching[recipe].items():
                if isinstance(watching, Resource):
                    # only recipe watches are accepted here.
                    # resource watches are handled by adding them to the watchlist
                    # in the dependency book
                    continue
                assert isinstance(watching, Recipe)
                only_when_flag_set |= only_when
                watch_rmeta = self.head.dag.recipe_meta[watching]
                if watch_rmeta.state == RecipeState.COOKED:
                    # underlying recipe changed. Ideally want a new changed state.
                    # TODO(design): have a 'changed' state for recipes?
                    return None, False

        if only_when_flag_set:
            # TODO(design) is it sensible to skip this here? What if we need to
            #  provide something? I suppose it's not guaranteed to be provided.
            return None, True

        inquiry = await self._dependency_store.inquire(recipe)
        if inquiry is None:
            return None, False
        _id, prev_book = inquiry

        # ignored books are not valid...
        if prev_book.ignored:
            return prev_book, False

        # compute and compare the var hash...
        sous_vars = recipe.recipe_context.variables
        vars_to_hash = {}
        for var in prev_book.var_list:
            try:
                vars_to_hash[var] = sous_vars.get_dotted(var)
            except KeyError:
                # variable missing
                return prev_book, False
        my_varhash = hash_dict(vars_to_hash)
        if prev_book.varhash != my_varhash:
            return prev_book, False

        # compare watched resources...
        for resource, last_update_time in prev_book.watching.items():
            res_time = self.head.dag.resource_time.get(resource)
            if res_time is None:
                # suggests something has changed in a significant way...
                return prev_book, False

            if res_time != last_update_time:
                # recipe is out of date
                return prev_book, False

        return prev_book, True

    # async def run_epoch(
    #     self,
    #     epoch: List[DepEle],
    #     depchecks: Dict[Recipe, DepCheckOutcome],
    #     concurrency_limit_per_host: int = 5,
    # ):
    #     per_host_lists: Dict[str, List[Recipe]] = defaultdict(lambda: [])
    #
    #     # sort into per-host lists
    #     for recipe in epoch:
    #         if isinstance(recipe, Recipe):
    #             if depchecks[recipe].label != CheckOutcomeLabel.SAFE_TO_SKIP:
    #                 per_host_lists[recipe.get_host()].append(recipe)
    #
    #     coros: List[Coroutine] = []
    #
    #     for host, recipes in per_host_lists.items():
    #         host_work_pool = HostWorkPool(recipes, depchecks)
    #         coros.append(host_work_pool.cook_all(self, concurrency_limit_per_host))
    #
    #     await asyncio.gather(*coros, return_exceptions=False)

    async def start(self, utensil: Utensil) -> Channel:
        utensil_name = utensil_namer(utensil.__class__)
        recipe = current_recipe.get()
        context = recipe.recipe_context
        cph = await self.get_chanprohead(context.sous, context.user)

        # noinspection PyDataclass
        payload = cattr.unstructure(utensil)

        return await cph.start_command_channel(utensil_name, payload)

    ut = start

    async def start_and_consume(self, utensil: Utensil) -> Any:
        channel = await self.start(utensil)
        return await channel.consume()

    ut1 = start_and_consume

    async def start_and_consume_attrs_optional(
        self, utensil: Utensil, attr_class: Type[A]
    ) -> Optional[A]:
        value = await self.start_and_consume(utensil)
        if value is None:
            return None
        return cattr.structure(value, attr_class)

    ut1a = start_and_consume_attrs_optional

    async def start_and_consume_attrs(self, utensil: Utensil, attr_class: Type[A]) -> A:
        value = await self.start_and_consume_attrs_optional(utensil, attr_class)
        if value is None:
            raise ValueError("Received None")
        return value

    ut1areq = start_and_consume_attrs

    async def start_and_wait_close(self, utensil: Utensil) -> Any:
        channel = await self.start(utensil)
        return await channel.wait_close()

    ut0 = start_and_wait_close

    async def _store_dependency(self, recipe: Recipe):
        dependency_tracker = self._dependency_trackers.pop(recipe, None)
        if not dependency_tracker:
            raise KeyError(f"Recipe {recipe} has not been tracked.")
        depbook = dependency_tracker.build_book()
        if depbook:
            await self._dependency_store.register(recipe, depbook)

    @staticmethod
    def resource_on_sous(
        kind: str, id: str, extra_params: Optional[frozendict] = None
    ) -> Resource:
        recipe = current_recipe.get()
        context = recipe.recipe_context
        return Resource(kind, id, context.sous, extra_params)

    async def _emit_fridge_resources(self):
        from scone.default.steps.fridge_steps import get_fridge_dirs

        for fridge_dir in get_fridge_dirs(self.head):
            num_prefix_parts = len(fridge_dir.parts)
            for root, _dirs, files in os.walk(fridge_dir):
                for file in files:
                    full_path = Path(root, file)
                    parts = full_path.parts
                    if parts[0:num_prefix_parts] != fridge_dir.parts:
                        raise RuntimeError(
                            f"{parts[0:num_prefix_parts]!r} != {fridge_dir.parts!r}"
                        )
                    fridge_relative_path = "/".join(parts[num_prefix_parts:])
                    fridge_res = Resource("fridge", fridge_relative_path, None)
                    stat = os.stat(full_path)
                    mtime = int(stat.st_mtime_ns // 1e6)
                    self.head.dag.resource_time[fridge_res] = mtime


#
# @attr.s(auto_attribs=True)
# class HostWorkPool:
#     jobs: List[Recipe]
#     depchecks: Dict[Recipe, DepCheckOutcome]
#     next_job: int = 0
#
#     async def cook_all(self, kitchen: Kitchen, concurrency_limit: int):
#         num_jobs = len(self.jobs)
#         concurrency_limit = min(num_jobs, concurrency_limit)
#
#         async def cooker():
#             while self.next_job < num_jobs:
#                 recipe = self.jobs[self.next_job]
#                 self.next_job += 1
#
#                 current_recipe.set(recipe)
#                 depcheck = self.depchecks.get(recipe)
#                 if (
#                     depcheck is not None
#                     and depcheck.label == CheckOutcomeLabel.CHECK_DYNAMIC
#                 ):
#                     book = depcheck.book
#                     assert book is not None
#                     can_skip = await kitchen.ut1(
#                         CanSkipDynamic(book.dyn_sous_file_hashes)
#                     )
#                     if can_skip:
#                         continue
#
#                 await recipe.cook(kitchen)
#                 # if successful, store dependencies
#                 await kitchen._store_dependency(recipe)
#                 nps = kitchen._notifying_provides.get(recipe, None)
#                 if nps:
#                     for depspec in nps:
#                         if depspec not in kitchen.notifications:
#                             # default to changed if not told otherwise
#                             kitchen.notifications[depspec] = True
#
#         await asyncio.gather(
#             *[asyncio.create_task(cooker()) for _ in range(concurrency_limit)]
#         )


class CookingWorker:
    def __init__(self, kitchen):
        self.kitchen = kitchen
        self.state = "not started"
        self.current_recipe = None

    async def start(self):
        self.state = "started"
        dag = self.kitchen.head.dag
        while True:
            if self.kitchen._sleeper_slots <= 0 and self.kitchen._cookable.empty():
                self.kitchen._sleeper_slots -= 1
                self.kitchen._cookable.put_nowait(None)
                self.state = "ended"
                break

            self.kitchen._sleeper_slots -= 1
            try:
                self.state = "polling"
                next_job = await self.kitchen._cookable.get()
            finally:
                self.state = "after polling"
                self.kitchen._sleeper_slots += 1

            if next_job is None:
                continue

            if isinstance(next_job, Recipe):
                meta = dag.recipe_meta[next_job]

                last_book, should_skip = await self.kitchen._should_skip(next_job)
                if should_skip and last_book:
                    # logger.debug("skipping %s", next_job)
                    meta.state = RecipeState.SKIPPED
                    # provide stuff that it provided last time
                    for res, last_update_time in last_book.provided.items():
                        # logger.debug("skip-providing %s", res)
                        dag.resource_time[res] = max(
                            last_update_time, dag.resource_time.get(res, -1)
                        )
                else:
                    meta.state = RecipeState.BEING_COOKED
                    current_recipe.set(next_job)
                    eprint(f"cooking {next_job}")
                    tracker = DependencyTracker(DependencyBook(), dag, next_job)
                    self.kitchen._dependency_trackers[next_job] = tracker
                    try:
                        self.state = "cooking"
                        self.current_recipe = next_job
                        await next_job.cook(self.kitchen)
                        self.state = "cooked"

                        # provide stuff
                        for outgoing in dag.edges[next_job]:
                            if not isinstance(outgoing, Resource):
                                continue
                            # logger.debug("providing %s", outgoing)
                            tracker.provide(outgoing)
                    except Exception as e:
                        meta.state = RecipeState.FAILED
                        raise RuntimeError(f"Recipe {next_job} failed!") from e
                    eprint(f"cooked {next_job}")

                    if next_job in self.kitchen.head.dag.watching:
                        for watching, only_when in self.kitchen.head.dag.watching[
                            next_job
                        ].items():
                            if isinstance(watching, Resource):
                                # recipe watches are handled when loading the
                                # dependency book.
                                tracker.watch(watching)

                    await self.kitchen._store_dependency(next_job)
                    meta.state = RecipeState.COOKED
            elif isinstance(next_job, Resource):
                eprint(f"have {next_job}")
                pass

            for edge in dag.edges[next_job]:
                # logger.debug("updating edge: %s → %s", next_job, edge)
                if isinstance(edge, Recipe):
                    rec_meta = dag.recipe_meta[edge]
                    rec_meta.incoming_uncompleted -= 1
                    if (
                        rec_meta.incoming_uncompleted == 0
                        and rec_meta.state == RecipeState.PENDING
                    ):
                        rec_meta.state = RecipeState.COOKABLE
                        self.kitchen._cookable.put_nowait(edge)
                elif isinstance(edge, Resource):
                    res_meta = dag.resource_meta[edge]
                    res_meta.incoming_uncompleted -= 1
                    if res_meta.incoming_uncompleted == 0 and not res_meta.completed:
                        res_meta.completed = True
                        self.kitchen._cookable.put_nowait(edge)
