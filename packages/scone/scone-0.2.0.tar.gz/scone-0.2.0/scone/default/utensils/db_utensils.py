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

import logging

import attr

try:
    import asyncpg
except ImportError:
    asyncpg = None

try:
    from mysql import connector as mysql_connector
except ImportError:
    mysql_connector = None

from scone.common.chanpro import Channel
from scone.sous import Utensil
from scone.sous.utensils import Worktop

logger = logging.getLogger(__name__)

if not asyncpg:
    logger.info("asyncpg not found, install if you need Postgres support")


@attr.s(auto_attribs=True)
class PostgresTransaction(Utensil):
    database: str

    # statements like CREATE DATABASE are not permitted in transactions.
    use_transaction_block: bool = True

    async def execute(self, channel: Channel, worktop: Worktop) -> None:
        if not asyncpg:
            raise RuntimeError("asyncpg is not installed.")

        async def queryloop():
            while True:
                next_input = await channel.recv()
                if next_input is None:
                    return
                query, *args = next_input
                if query is None:
                    break
                try:
                    results = [
                        dict(record) for record in await conn.fetch(query, *args)
                    ]
                except asyncpg.PostgresError:
                    logger.error(
                        "Failed query %s with args %r", query, args, exc_info=True
                    )
                    await channel.close("Query error")
                    raise

                await channel.send(results)

        conn = await asyncpg.connect(database=self.database)
        try:
            if self.use_transaction_block:
                async with conn.transaction():
                    await queryloop()
            else:
                await queryloop()
        finally:
            await conn.close()


@attr.s(auto_attribs=True)
class MysqlTransaction(Utensil):
    database: str
    user: str
    unix_socket: bool = False

    async def execute(self, channel: Channel, worktop: Worktop) -> None:
        if not mysql_connector:
            raise RuntimeError("mysql-connector-python is not installed.")

        async def queryloop():
            while True:
                next_input = await channel.recv()
                if next_input is None:
                    return
                query, *args = next_input
                if query is None:
                    break
                try:
                    cur.execute(query, tuple(args))

                    if conn.unread_result:
                        names = cur.column_names
                        results = [
                            dict(zip(names, rectuple)) for rectuple in cur.fetchall()
                        ]
                    else:
                        results = []
                except mysql_connector.errors.Error:
                    logger.error(
                        "Failed query %s with args %r", query, args, exc_info=True
                    )
                    await channel.close("Query error")
                    raise

                await channel.send(results)

        # TODO(perf): make async

        unix_socket = "/var/run/mysqld/mysqld.sock" if self.unix_socket else None

        conn = mysql_connector.connect(
            database=self.database, user=self.user, unix_socket=unix_socket
        )
        cur = conn.cursor()
        try:
            await queryloop()
            # autocommit disabled in this mode by default
            conn.commit()
        finally:
            conn.close()
