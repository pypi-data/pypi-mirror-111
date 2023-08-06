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
import grp
import logging
import os
import pwd
import shutil
import stat
from typing import List, Optional

import attr

from scone.common.chanpro import Channel
from scone.common.misc import sha256_file
from scone.sous.utensils import Utensil, Worktop


@attr.s(auto_attribs=True)
class WriteFile(Utensil):
    path: str
    mode: int
    atomic: bool = attr.ib(default=True)

    async def execute(self, channel: Channel, worktop):
        oldumask = os.umask(0)
        temp_path = self.path + "._scone-part"
        write_path = temp_path if self.atomic else self.path
        fdnum = os.open(write_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.mode)
        os.umask(oldumask)

        with open(fdnum, "wb") as file:
            while True:
                next_chunk = await channel.recv()
                if next_chunk is None:
                    break
                assert isinstance(next_chunk, bytes)
                file.write(next_chunk)

        if self.atomic:
            shutil.move(temp_path, self.path)

        await channel.send("OK")


@attr.s(auto_attribs=True)
class WriteBlockInFile(Utensil):
    path: str
    mode: int
    marker_line_prefix: str
    marker_name: str
    data: str

    async def execute(self, channel: Channel, worktop):
        start_marker = self.marker_line_prefix + "BEGIN " + self.marker_name + "\n"
        end_marker = self.marker_line_prefix + "END " + self.marker_name + "\n"

        if os.path.exists(self.path):
            with open(self.path, "r") as fin:
                file_lines = fin.readlines()

            try:
                start_index = file_lines.index(start_marker)
                end_index = file_lines.index(end_marker)
                file_lines = file_lines[:start_index] + file_lines[end_index + 1 :]
            except ValueError:
                pass
        else:
            file_lines = []

        file_lines.append(start_marker + self.data + "\n" + end_marker)

        oldumask = os.umask(0)
        fdnum = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.mode)
        os.umask(oldumask)

        with open(fdnum, "w") as file:
            file.writelines(file_lines)


@attr.s(auto_attribs=True)
class MakeDirectory(Utensil):
    path: str
    mode: int

    async def execute(self, channel: Channel, worktop):
        oldumask = os.umask(0)
        os.mkdir(self.path, self.mode)
        os.umask(oldumask)


@attr.s(auto_attribs=True)
class MakeSymlink(Utensil):
    path: str
    target: str

    async def execute(self, channel: Channel, worktop):
        os.symlink(self.target, self.path)


@attr.s(auto_attribs=True)
class Stat(Utensil):
    path: str

    logger = logging.getLogger(__name__)

    @attr.s(auto_attribs=True)
    class Result:
        uid: int
        gid: int
        dir: bool
        user: str
        group: str
        mode: int

    async def execute(self, channel: Channel, worktop):
        try:
            self.logger.debug("going to stat")
            stat_result = os.stat(self.path, follow_symlinks=False)
        except FileNotFoundError:
            self.logger.debug(":(")
            await channel.send(None)
            return

        self.logger.debug("going to user")
        user = pwd.getpwuid(stat_result.st_uid).pw_name
        self.logger.debug("going to grp")
        group = grp.getgrgid(stat_result.st_gid).gr_name
        self.logger.debug("going to respond")

        await channel.send(
            Stat.Result(
                uid=stat_result.st_uid,
                gid=stat_result.st_gid,
                dir=stat.S_ISDIR(stat_result.st_mode),
                user=user,
                group=group,
                mode=stat_result.st_mode,
            )
        )


@attr.s(auto_attribs=True)
class Chown(Utensil):
    path: str
    user: Optional[str]
    group: Optional[str]

    async def execute(self, channel: Channel, worktop):
        shutil.chown(self.path, self.user, self.group)


@attr.s(auto_attribs=True)
class Chmod(Utensil):
    path: str
    mode: int

    async def execute(self, channel: Channel, worktop):
        os.chmod(self.path, self.mode)


@attr.s(auto_attribs=True)
class SimpleExec(Utensil):
    args: List[str]
    working_dir: str

    @attr.s(auto_attribs=True)
    class Result:
        exit_code: int
        stdout: bytes
        stderr: bytes

    async def execute(self, channel: Channel, worktop: Worktop):
        proc = await asyncio.create_subprocess_exec(
            *self.args,
            stdin=None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.working_dir
        )

        stdout, stderr = await proc.communicate()

        # send the result
        exit_code = proc.returncode
        assert exit_code is not None

        await channel.send(
            SimpleExec.Result(exit_code=exit_code, stdout=stdout, stderr=stderr)
        )


@attr.s(auto_attribs=True)
class HashFile(Utensil):
    path: str

    async def execute(self, channel: Channel, worktop: Worktop):
        try:
            sha256 = await asyncio.get_running_loop().run_in_executor(
                worktop.pools.threaded, sha256_file, self.path
            )
            await channel.send(sha256)
        except FileNotFoundError:
            await channel.send(None)
