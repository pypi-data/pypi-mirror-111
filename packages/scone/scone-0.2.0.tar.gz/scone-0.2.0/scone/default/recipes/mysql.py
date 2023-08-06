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

from scone.default.utensils.db_utensils import MysqlTransaction
from scone.head.head import Head
from scone.head.kitchen import Kitchen, Preparation
from scone.head.recipe import Recipe, RecipeContext
from scone.head.utils import check_type, check_type_opt


def mysql_dodgy_escape_literal(unescaped: str) -> str:
    python_esc = repr(unescaped)
    if python_esc[0] == '"':
        return "'" + python_esc[1:-1].replace("'", "\\'") + "'"
    else:
        assert python_esc[0] == "'"
        return python_esc


def mysql_dodgy_escape_username(unescaped: str) -> str:
    parts = unescaped.split("@")
    if len(parts) != 2:
        raise ValueError(f"{unescaped!r} is not a valid sconified mysql user name.")
    return (
        mysql_dodgy_escape_literal(parts[0])
        + "@"
        + mysql_dodgy_escape_literal(parts[1])
    )


class MysqlDatabase(Recipe):
    _NAME = "mysql-db"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.database_name = check_type(args.get("name"), str)
        self.charset = args.get("charset", "utf8mb4")
        self.collate = args.get("collate", "utf8mb4_unicode_ci")
        self.grant_all_to = check_type_opt(args.get("grant_all_to"), List[str])

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        preparation.provides("mysql-database", self.database_name)
        if self.grant_all_to:
            for user in self.grant_all_to:
                preparation.needs("mysql-user", user)

    async def cook(self, kitchen: Kitchen) -> None:
        ch = await kitchen.start(MysqlTransaction("mysql", "root", unix_socket=True))
        await ch.send(
            (
                "SHOW DATABASES LIKE %s",
                self.database_name,
            )
        )
        dbs = await ch.recv()
        if len(dbs) > 0:
            await ch.send(None)
            await ch.wait_close()
            return

        q = f"""
            CREATE DATABASE {self.database_name}
                CHARACTER SET = {mysql_dodgy_escape_literal(self.charset)}
                COLLATE = {mysql_dodgy_escape_literal(self.collate)}
        """

        await ch.send((q,))
        res = await ch.recv()
        if len(res) != 0:
            raise RuntimeError("expected empty result set.")

        if self.grant_all_to:
            for user in self.grant_all_to:
                q = f"""
                    GRANT ALL PRIVILEGES ON {self.database_name}.*
                        TO {mysql_dodgy_escape_username(user)}
                """
                await ch.send((q,))
                res = await ch.recv()
                if len(res) != 0:
                    raise RuntimeError("expected empty result set.")

            q = """
                FLUSH PRIVILEGES
            """
            await ch.send((q,))
            res = await ch.recv()
            if len(res) != 0:
                raise RuntimeError("expected empty result set.")

        await ch.send(None)
        await ch.wait_close()


class MysqlUser(Recipe):
    _NAME = "mysql-user"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.user_name = check_type(args.get("name"), str)
        self.password = check_type(args.get("password"), str)

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        preparation.provides("mysql-user", self.user_name)

    async def cook(self, kitchen: Kitchen) -> None:
        ch = await kitchen.start(MysqlTransaction("mysql", "root", unix_socket=True))
        await ch.send(
            (
                "SELECT 1 AS count FROM mysql.user "
                "WHERE CONCAT(user, '@', host) = %s",
                self.user_name,
            )
        )
        dbs = await ch.recv()
        if len(dbs) > 0 and dbs[0]["count"] == 1:
            await ch.send(None)
            await ch.wait_close()
            return

        # this is close enough to MySQL escaping I believe.
        escaped_password = mysql_dodgy_escape_literal(str(self.password))

        q = f"""
            CREATE USER {mysql_dodgy_escape_username(self.user_name)}
                IDENTIFIED BY {escaped_password}
        """

        await ch.send((q,))
        res = await ch.recv()
        if len(res) != 0:
            raise RuntimeError("expected empty result set.")
        await ch.send(None)
        await ch.wait_close()
