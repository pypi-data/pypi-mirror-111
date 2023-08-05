import atexit
from contextlib import ExitStack, contextmanager
from pathlib import PurePath
from typing import List, Union, Generator, Iterable

import importlib_resources
from deprecated.classic import deprecated
from pkg_resources import resource_listdir


def _get_file_manager_cleanup_on_exit():
    file_manager = ExitStack()
    # Cleanup context managed files, at program shutdown
    atexit.register(file_manager.close)
    return file_manager


@deprecated(
    version="0.5.13",
    reason="Folder possibly extracted in a tmp dir is not cleanup until the program exit.",
)
def get_folder(root_pkg_name: str = __package__, directory: str = "data") -> Union[PurePath, str]:
    """
    Retrieve folder in module: root_pkg_name.directory
    @params:
    - root_pk_name: Typically my_module.__package__
    @returns: Absolute path
    """
    file_manager = _get_file_manager_cleanup_on_exit()
    ref = importlib_resources.files(root_pkg_name) / directory
    path = file_manager.enter_context(importlib_resources.as_file(ref))
    return path


@deprecated(
    version="0.5.13",
    reason="Files/Folder possibly extracted in a tmp dir are not cleanup until the program exit. Use importlib.files(...) instead",
)
def get_files(
    root_pkg_name: str = __package__, directory: str = "data", ignore_init_file: bool = True
) -> List[Union[PurePath, str]]:
    """
    Retrieve list of files in module: root_pkg_name.directory
    @params:
    - root_pk_name: Typically my_module.__package__
    @returns: List of absolute paths
    """
    paths = [
        filename for filename in importlib_resources.files(f"{root_pkg_name}.{directory}").iterdir()
    ]

    paths = [
        p
        for p in paths
        if not str(p).endswith("__init__.py") and not str(p).endswith("__pycache__")
    ]
    return paths


# FUTURE: Migrating to python std lib:
# https://importlib-resources.readthedocs.io/en/latest/migration.html#pkg-resources-resource-listdir
