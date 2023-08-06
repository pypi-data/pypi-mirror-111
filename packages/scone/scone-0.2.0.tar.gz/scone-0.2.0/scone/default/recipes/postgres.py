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

from scone.default.utensils.db_utensils import PostgresTransaction
from scone.head.head import Head
from scone.head.kitchen import Kitchen, Preparation
from scone.head.recipe import Recipe, RecipeContext
from scone.head.utils import check_type


def postgres_dodgy_escape_literal(unescaped: str) -> str:
    python_esc = repr(unescaped)
    if python_esc[0] == '"':
        return "E'" + python_esc[1:-1].replace("'", "\\'") + "'"
    else:
        assert python_esc[0] == "'"
        return "E" + python_esc


class PostgresDatabase(Recipe):
    _NAME = "pg-db"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.database_name = check_type(args.get("name"), str)
        self.owner = check_type(args.get("owner"), str)
        self.encoding = args.get("encoding", "utf8")
        # en_GB.UTF-8 may have perf impact and needs to be installed as a locale
        # with locale-gen on Ubuntu. In short, a pain.
        # C or POSIX is recommended.
        self.collate = args.get("collate", "C")
        self.ctype = args.get("ctype", "C")
        self.template = args.get("template", "template0")

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        preparation.provides("postgres-database", self.database_name)
        preparation.needs("postgres-user", self.owner)

    async def cook(self, kitchen: Kitchen) -> None:
        ch = await kitchen.start(
            PostgresTransaction("postgres", use_transaction_block=False)
        )
        await ch.send(
            (
                "SELECT 1 AS count FROM pg_catalog.pg_database WHERE datname = $1",
                self.database_name,
            )
        )
        dbs = await ch.recv()
        if len(dbs) > 0 and dbs[0]["count"] == 1:
            await ch.send(None)
            await ch.wait_close()
            return

        q = f"""
            CREATE DATABASE {self.database_name}
                WITH OWNER {self.owner}
                ENCODING {self.encoding}
                LC_COLLATE {postgres_dodgy_escape_literal(self.collate)}
                LC_CTYPE {postgres_dodgy_escape_literal(self.ctype)}
                TEMPLATE {postgres_dodgy_escape_literal(self.template)}
        """

        await ch.send((q,))
        res = await ch.recv()
        if len(res) != 0:
            raise RuntimeError("expected empty result set.")
        await ch.send(None)
        await ch.wait_close()


class PostgresUser(Recipe):
    _NAME = "pg-user"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.user_name = check_type(args.get("name"), str)
        self.passwordless = check_type(args.get("passwordless", False), bool)
        if not self.passwordless:
            self.password = check_type(args.get("password"), str)
        elif "password" in args:
            raise ValueError("'password' specified when 'passwordless' also specified.")

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        preparation.provides("postgres-user", self.user_name)

    async def cook(self, kitchen: Kitchen) -> None:
        ch = await kitchen.start(PostgresTransaction("postgres"))
        await ch.send(
            (
                "SELECT 1 AS count FROM pg_catalog.pg_user WHERE usename = $1",
                self.user_name,
            )
        )
        dbs = await ch.recv()
        if len(dbs) > 0 and dbs[0]["count"] == 1:
            await ch.send(None)
            await ch.wait_close()
            return

        if self.passwordless:
            q = f"""
                CREATE ROLE {self.user_name}
                    LOGIN
            """
        else:
            # this is close enough to Postgres escaping I believe.
            escaped_password = postgres_dodgy_escape_literal(str(self.password))

            q = f"""
                CREATE ROLE {self.user_name}
                    WITH PASSWORD {escaped_password}
                    LOGIN
            """

        await ch.send((q,))
        res = await ch.recv()
        if len(res) != 0:
            raise RuntimeError("expected empty result set.")
        await ch.send(None)
        await ch.wait_close()


class PostgresCommands(Recipe):
    _NAME = "pg-commands"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.database = check_type(args.get("database"), str)
        self.commands = check_type(args.get("commands"), list)
        self.skip_database_need = check_type(
            args.get("skip_database_need", False), bool
        )

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        if not self.skip_database_need:
            preparation.needs("postgres-database", self.database)

    async def cook(self, kitchen: Kitchen) -> None:
        ch = await kitchen.start(PostgresTransaction(self.database))

        for command in self.commands:
            await ch.send((command,))

            res = await ch.recv()
            if len(res) != 0:
                raise RuntimeError("expected empty result set.")

        await ch.send(None)
        await ch.wait_close()
