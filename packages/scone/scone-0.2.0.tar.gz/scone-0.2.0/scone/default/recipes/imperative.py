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
from typing import List

from scone.default.utensils.basic_utensils import SimpleExec
from scone.head.head import Head
from scone.head.kitchen import Kitchen, Preparation
from scone.head.recipe import Recipe, RecipeContext
from scone.head.utils import check_type, check_type_opt


class ImperativeShellCommands(Recipe):
    _NAME = "shell-commands"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.working_dir = check_type_opt(args.get("cd"), str)
        self.commands = check_type(args.get("commands"), List[str])

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        if self.working_dir:
            preparation.needs("directory", self.working_dir)

    async def cook(self, kitchen: Kitchen) -> None:
        for command in self.commands:
            result = await kitchen.ut1areq(
                SimpleExec(["sh", "-c", command], self.working_dir or "/tmp"),
                SimpleExec.Result,
            )

            if result.exit_code != 0:
                esc_stderr = result.stderr.decode().replace("\n", "\n    ")
                raise RuntimeError(
                    f"Exit code of {command!r} was {result.exit_code}. stderr:\n"
                    f"    {esc_stderr}\n" + ("-" * 40)
                )
