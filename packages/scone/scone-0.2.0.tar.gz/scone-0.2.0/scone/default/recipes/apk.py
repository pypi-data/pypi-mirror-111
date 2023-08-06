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
import random
from asyncio import Lock
from collections import defaultdict
from typing import Dict, List, Tuple

from scone.default.utensils.basic_utensils import SimpleExec
from scone.head.head import Head
from scone.head.kitchen import Kitchen, Preparation
from scone.head.recipe import Recipe, RecipeContext
from scone.head.utils import check_type

logger = logging.getLogger(__name__)

# (id of Kitchen, sous name) → Lock
apk_locks: Dict[Tuple[int, str], Lock] = defaultdict(Lock)


class ApkPackage(Recipe):
    _NAME = "apk-install"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)
        self.packages: List[str] = check_type(args["packages"], list)

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)

        for package in self.packages:
            preparation.provides("apk-package", package)

    async def _apk_command(
        self, kitchen: Kitchen, args: List[str]
    ) -> SimpleExec.Result:
        retries = 3

        while retries > 0:
            result = await kitchen.ut1areq(SimpleExec(args, "/"), SimpleExec.Result)

            logger.debug("E %r: %r", args, result.stderr)

            if result.exit_code == 0:
                return result

            sleep = 2.0 + 3.0 * random.random()
            await asyncio.sleep(sleep)

        return result  # noqa

    async def cook(self, kitchen: Kitchen) -> None:
        # this is a one-off task assuming everything works
        kitchen.get_dependency_tracker()

        lock = apk_locks[(id(kitchen), self.recipe_context.sous)]

        if not self.packages:
            return

        # we only let one apk operation run at once on each sous
        async with lock:
            # apk update not needed because it's automatic once the cache timer expires!

            install_args = ["apk", "add", "-q"]
            install_args += list(self.packages)
            install = await self._apk_command(kitchen, install_args)

            if install.exit_code != 0:
                raise RuntimeError(
                    f"apk add failed with err {install.exit_code}:"
                    f" {install.stderr!r}"
                )
