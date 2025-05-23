# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for documentation."""

import json

import numpy as np

from vectorbt import _typing as tp


class Documented:
    """Abstract class for documenting self.

    !!! note
        Won't get converted into a string in `prepare_for_doc`."""

    def to_doc(self, **kwargs) -> str:
        """Convert to a doc."""
        raise NotImplementedError

    def __str__(self):
        """Return string of self."""
        try:
            return self.to_doc()
        except NotImplementedError:
            return repr(self)


class SafeToStr:
    """Class that can be safely converted into a string in `prepare_for_doc`."""


def prepare_for_doc(obj: tp.Any, replace: tp.DictLike = None, path: str = None) -> tp.Any:
    """Prepare object for use in documentation."""
    if isinstance(obj, SafeToStr):
        return str(obj)
    if isinstance(obj, np.dtype) and hasattr(obj, "fields"):
        return dict(zip(
            dict(obj.fields).keys(),
            list(map(lambda x: str(x[0]), dict(obj.fields).values()))
        ))
    if isinstance(obj, tuple) and hasattr(obj, "_asdict"):
        return prepare_for_doc(obj._asdict(), replace, path)
    if isinstance(obj, (tuple, list)):
        return [prepare_for_doc(v, replace, path) for v in obj]
    if isinstance(obj, dict):
        if replace is None:
            replace = {}
        new_obj = dict()
        for k, v in obj.items():
            if path is None:
                new_path = k
            else:
                new_path = path + '.' + k
            if new_path in replace:
                new_obj[k] = replace[new_path]
            else:
                new_obj[k] = prepare_for_doc(v, replace, new_path)
        return new_obj
    if hasattr(obj, 'shape') and isinstance(obj.shape, tuple):
        if len(obj.shape) == 0:
            return obj.item()
        return "{} of shape {}".format(object.__repr__(obj), obj.shape)
    return obj


def to_doc(obj: tp.Any, replace: tp.DictLike = None, path: str = None, **kwargs) -> str:
    """Convert object to a JSON string."""
    kwargs = {**dict(indent=4, default=str), **kwargs}
    return json.dumps(prepare_for_doc(obj, replace, path), **kwargs)
