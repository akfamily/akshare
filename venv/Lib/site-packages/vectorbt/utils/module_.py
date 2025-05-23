# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for modules."""

import importlib
import inspect
import pkgutil
import sys
from types import ModuleType

from vectorbt import _typing as tp


def is_from_module(obj: tp.Any, module: ModuleType) -> bool:
    """Return whether `obj` is from module `module`."""
    mod = inspect.getmodule(inspect.unwrap(obj))
    return mod is None or mod.__name__ == module.__name__


def list_module_keys(module_name: str, whitelist: tp.Optional[tp.List[str]] = None,
                     blacklist: tp.Optional[tp.List[str]] = None):
    """List the names of all public functions and classes defined in the module `module_name`.

    Includes the names listed in `whitelist` and excludes the names listed in `blacklist`."""
    if whitelist is None:
        whitelist = []
    if blacklist is None:
        blacklist = []
    module = sys.modules[module_name]
    return [name for name, obj in inspect.getmembers(module)
            if (not name.startswith("_") and is_from_module(obj, module)
                and ((inspect.isroutine(obj) and callable(obj)) or inspect.isclass(obj))
                and name not in blacklist) or name in whitelist]


def import_submodules(package: tp.Union[str, ModuleType]) -> tp.Dict[str, ModuleType]:
    """Import all submodules of a module, recursively, including subpackages.

    If package defines `__blacklist__`, does not import modules that match names from this list."""
    if isinstance(package, str):
        package = importlib.import_module(package)
    blacklist = []
    if hasattr(package, '__blacklist__'):
        blacklist = package.__blacklist__
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        if '.'.join(name.split('.')[:-1]) != package.__name__:
            continue
        if name.split('.')[-1] in blacklist:
            continue
        results[name] = importlib.import_module(name)
        if is_pkg:
            results.update(import_submodules(name))
    return results
