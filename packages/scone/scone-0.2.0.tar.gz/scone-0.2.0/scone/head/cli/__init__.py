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
import sys
import time
from argparse import ArgumentParser
from pathlib import Path

from scone.common.misc import eprint
from scone.common.pools import Pools
from scone.head import dot_emitter
from scone.head.dependency_tracking import DependencyCache
from scone.head.head import Head
from scone.head.kitchen import Kitchen, Preparation


def cli() -> None:
    logging.basicConfig()
    logging.getLogger("scone").setLevel(logging.DEBUG)
    code = asyncio.get_event_loop().run_until_complete(cli_async())
    sys.exit(code)


async def cli_async() -> int:
    dep_cache = None
    try:
        args = sys.argv[1:]

        parser = ArgumentParser(description="Cook!")
        parser.add_argument("hostspec", type=str, help="Sous or group name")
        parser.add_argument(
            "--menu",
            "-m",
            type=str,
            help="Specify a comma-separated list of names of menu to cook. "
            "If not specified, all menus will be cooked.",
        )
        parser.add_argument(
            "--yes",
            "-y",
            action="store_true",
            default=False,
            help="Don't prompt for confirmation",
        )
        argp = parser.parse_args(args)

        eprint("Loading head…")

        cdir = Path(os.getcwd())

        while not Path(cdir, "scone.head.toml").exists():
            cdir = cdir.parent
            if len(cdir.parts) <= 1:
                eprint("Don't appear to be in a head. STOP.")
                return 1

        menu_subset = None
        if argp.menu:
            menu_subset = argp.menu.split(",")

        head = Head.open(str(cdir))

        eprint(head.debug_info())

        hosts = set()

        if argp.hostspec in head.souss:
            hosts.add(argp.hostspec)
        elif argp.hostspec in head.groups:
            for sous in head.groups[argp.hostspec]:
                hosts.add(sous)
        else:
            eprint(f"Unrecognised sous or group: '{argp.hostspec}'")
            sys.exit(1)

        eprint(f"Selected the following souss: {', '.join(hosts)}")

        head.load_variables(hosts)
        head.load_menus(menu_subset, hosts)

        eprint("Preparing recipes…")
        prepare = Preparation(head)

        start_ts = time.monotonic()
        prepare.prepare_all()
        del prepare
        end_ts = time.monotonic()
        eprint(f"Preparation completed in {end_ts - start_ts:.3f} s.")
        # eprint(f"{len(order)} courses planned.")

        dot_emitter.emit_dot(head.dag, Path(cdir, "dag.0.dot"))

        dep_cache = await DependencyCache.open(
            os.path.join(head.directory, "depcache.sqlite3")
        )

        kitchen = Kitchen(head, dep_cache)
        await kitchen.prepare_to_cook()

        eprint("Ready to cook? [y/N]: ", end="")
        if argp.yes:
            eprint("y (due to --yes)")
        else:
            if not input().lower().startswith("y"):
                eprint("Stopping.")
                return 101

        try:
            await kitchen.cook_all()
        finally:
            dot_emitter.emit_dot(head.dag, Path(cdir, "dag.9.dot"))
            await kitchen.close_all_ssh_connections()

        return 0
    finally:
        Pools.get().shutdown()
        if dep_cache:
            await dep_cache.db.close()


if __name__ == "__main__":
    cli()
