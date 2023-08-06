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
import os
from enum import Enum
from pathlib import Path, PurePath
from typing import List, Optional, Tuple, Union

from jinja2 import DictLoader, Environment

from scone.head.head import Head
from scone.head.kitchen import Kitchen
from scone.head.variables import Variables

SUPERMARKET_RELATIVE = ".scone-cache/supermarket"


def get_fridge_dirs(head: Head) -> List[Path]:
    # TODO expand with per-sous/per-group dirs?
    return [Path(head.directory, "fridge")]


def search_in_dirlist(
    dirlist: List[Path], relative: Union[str, PurePath]
) -> Optional[Path]:
    for directory in dirlist:
        potential_path = directory.joinpath(relative)
        if potential_path.exists():
            return potential_path
    return None


def search_in_fridge(
    head: Head, relative: Union[str, PurePath]
) -> Optional[Tuple[str, Path]]:
    """
    :param head: Head
    :param relative: Relative fridge path
    :return: (desugared fridge path, path to file on filesystem)
    """
    fridge_dirs = get_fridge_dirs(head)
    # TODO(feature): try sous and group-prefixed paths, and return the desugared
    #   path alongside.
    final = search_in_dirlist(fridge_dirs, relative)
    if final:
        return str(relative), final
    else:
        return None


class FridgeMetadata(Enum):
    FRIDGE = 0
    FROZEN = 1
    TEMPLATE = 2


def decode_fridge_extension(path: str) -> Tuple[str, FridgeMetadata]:
    exts = {
        ".frozen": FridgeMetadata.FROZEN,
        ".j2": FridgeMetadata.TEMPLATE,
        # don't know if we want to support .j2.frozen, but we could in the future
    }

    for ext, meta in exts.items():
        if path.endswith(ext):
            return path[: -len(ext)], meta

    return path, FridgeMetadata.FRIDGE


async def load_and_transform(
    kitchen: Kitchen, meta: FridgeMetadata, fullpath: Path, variables: Variables
) -> bytes:
    head = kitchen.head
    # TODO(perf) don't do this in async loop
    with fullpath.open("rb") as file:
        data = file.read()
    if meta == FridgeMetadata.FROZEN:
        # decrypt
        if head.secret_access is None:
            raise RuntimeError("Frozen file but no secret access enabled!")
        data = head.secret_access.decrypt_bytes(data)
    elif meta == FridgeMetadata.TEMPLATE:
        # pass through Jinja2
        try:
            env = Environment(
                loader=DictLoader({str(fullpath): data.decode()}), autoescape=False
            )
            template = env.get_template(str(fullpath))
            proxies = kitchen.get_dependency_tracker().get_j2_var_proxies(variables)
            data = template.render(proxies).encode()
        except Exception as e:
            raise RuntimeError(f"Error templating: {fullpath}") from e

        # try:
        #     return jinja2.utils.concat(
        #         template.root_render_func(template.new_context(proxies))
        #     )
        # except Exception:
        #     template.environment.handle_exception()

    return data


def _find_files_in_dir(relative: str, dir: Path) -> List[Tuple[str, str, Path]]:
    """
    :param relative:
    :param dir:
    :return: Tuple of (
        relative path with prefix included,
        relative path with prefix not included,
        path to local file
    )
    """
    result = []
    num_prefix_parts = len(dir.parts)
    for root, dirs, files in os.walk(dir):
        for file in files:
            full_path = Path(root, file)
            parts = full_path.parts
            if parts[0:num_prefix_parts] != dir.parts:
                raise RuntimeError(f"{parts[0:num_prefix_parts]!r} != {dir.parts!r}")
            dir_relative_path = "/".join(parts[num_prefix_parts:])
            result.append(
                (relative + "/" + dir_relative_path, dir_relative_path, full_path)
            )
    return result


def search_children_in_fridge(
    head: Head, relative: Union[str, PurePath]
) -> Optional[List[Tuple[str, str, Path]]]:
    """
    Similar to `search_in_fridge` but finds (recursively) ALL children of a named
    directory. This 'directory' can be split across multiple fridge search paths.
    """
    fridge_dirs = get_fridge_dirs(head)

    results = []
    # only the first file found for a path counts — this allows overrides
    found_filenames = set()

    for directory in fridge_dirs:
        potential_path = directory.joinpath(relative)
        if potential_path.exists():
            # find children
            for rel, rel_unprefixed, file in _find_files_in_dir(
                str(relative), potential_path
            ):
                unextended_name, _transformer = decode_fridge_extension(rel)
                if unextended_name in found_filenames:
                    continue
                results.append((rel, rel_unprefixed, file))
                found_filenames.add(unextended_name)

    return results
