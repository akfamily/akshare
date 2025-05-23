# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Mapping utilities."""

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.utils import checks


def reverse_mapping(mapping: tp.Mapping) -> dict:
    """Reverse a mapping.

    Returns a dict."""
    return {v: k for k, v in mapping.items()}


def to_mapping(mapping_like: tp.MappingLike, reverse: bool = False) -> dict:
    """Convert mapping-like object to a mapping.

    Enable `reverse` to apply `reverse_mapping` on the result dict."""
    if checks.is_namedtuple(mapping_like):
        mapping = {v: k for k, v in mapping_like._asdict().items()}
        if -1 not in mapping_like:
            mapping[-1] = None
    elif not checks.is_mapping(mapping_like):
        if checks.is_index(mapping_like):
            mapping_like = mapping_like.to_series().reset_index(drop=True)
        if checks.is_series(mapping_like):
            mapping = mapping_like.to_dict()
        else:
            mapping = dict(enumerate(mapping_like))
    else:
        mapping = dict(mapping_like)
    if reverse:
        mapping = reverse_mapping(mapping)
    return mapping


def apply_mapping(obj: tp.Any,
                  mapping_like: tp.Optional[tp.MappingLike] = None,
                  reverse: bool = False,
                  ignore_case: bool = True,
                  ignore_underscores: bool = True,
                  ignore_type: tp.MaybeTuple[tp.DTypeLike] = None,
                  ignore_missing: bool = False,
                  na_sentinel: tp.Any = None) -> tp.Any:
    """Apply mapping on object using a mapping-like object.

    Args:
        obj (any): Any object.

            Can take a scalar, tuple, list, set, frozenset, NumPy array, Index, Series, and DataFrame.
        mapping_like (mapping_like): Any mapping-like object.

            See `to_mapping`.
        reverse (bool): See `reverse` in `to_mapping`.
        ignore_case (bool): Whether to ignore the case if the key is a string.
        ignore_underscores (bool): Whether to ignore underscores if the key is a string.
        ignore_type (dtype_like or tuple): One or multiple types or data types to ignore.
        ignore_missing (bool): Whether to ignore missing values.
        na_sentinel (any): Value to mark “not found”.
    """
    if mapping_like is None:
        return obj

    if ignore_case and ignore_underscores:
        key_func = lambda x: x.lower().replace('_', '')
    elif ignore_case:
        key_func = lambda x: x.lower()
    elif ignore_underscores:
        key_func = lambda x: x.replace('_', '')
    else:
        key_func = lambda x: x
    if not isinstance(ignore_type, tuple):
        ignore_type = (ignore_type,)

    mapping = to_mapping(mapping_like, reverse=reverse)

    new_mapping = dict()
    for k, v in mapping.items():
        if pd.isnull(k):
            na_sentinel = v
        else:
            if isinstance(k, str):
                k = key_func(k)
            new_mapping[k] = v

    def _compatible_types(x_type: type, item: tp.Any = None) -> bool:
        if item is not None:
            if np.dtype(x_type) == 'O':
                x_type = type(item)
        for y_type in ignore_type:
            if y_type is None:
                return False
            if x_type is y_type:
                return True
            x_dtype = np.dtype(x_type)
            y_dtype = np.dtype(y_type)
            if x_dtype is y_dtype:
                return True
            if np.issubdtype(x_dtype, np.integer) and np.issubdtype(y_dtype, np.integer):
                return True
            if np.issubdtype(x_dtype, np.floating) and np.issubdtype(y_dtype, np.floating):
                return True
            if np.issubdtype(x_dtype, np.bool_) and np.issubdtype(y_dtype, np.bool_):
                return True
            if np.issubdtype(x_dtype, np.flexible) and np.issubdtype(y_dtype, np.flexible):
                return True
        return False

    def _converter(x: tp.Any) -> tp.Any:
        if pd.isnull(x):
            return na_sentinel
        if isinstance(x, str):
            x = key_func(x)
        if ignore_missing:
            try:
                return new_mapping[x]
            except KeyError:
                return x
        return new_mapping[x]

    if isinstance(obj, (tuple, list, set, frozenset)):
        result = [apply_mapping(
            v,
            mapping_like=mapping_like,
            reverse=reverse,
            ignore_case=ignore_case,
            ignore_underscores=ignore_underscores,
            ignore_type=ignore_type,
            ignore_missing=ignore_missing,
            na_sentinel=na_sentinel
        ) for v in obj]
        return type(obj)(result)
    if isinstance(obj, np.ndarray):
        if obj.size == 0:
            return obj
        if ignore_type is None or not _compatible_types(obj.dtype, obj.item(0)):
            if obj.ndim == 1:
                return pd.Series(obj).map(_converter).values
            return np.vectorize(_converter)(obj)
        return obj
    if isinstance(obj, pd.Series):
        if obj.size == 0:
            return obj
        if ignore_type is None or not _compatible_types(obj.dtype, obj.iloc[0]):
            return obj.map(_converter)
        return obj
    if isinstance(obj, pd.Index):
        if obj.size == 0:
            return obj
        if ignore_type is None or not _compatible_types(obj.dtype, obj[0]):
            return obj.map(_converter)
        return obj
    if isinstance(obj, pd.DataFrame):
        if obj.size == 0:
            return obj
        series = []
        for sr_name, sr in obj.items():
            if ignore_type is None or not _compatible_types(sr.dtype, sr.iloc[0]):
                series.append(sr.map(_converter))
            else:
                series.append(sr)
        return pd.concat(series, axis=1, keys=obj.columns)
    if ignore_type is None or not _compatible_types(type(obj)):
        return _converter(obj)
    return obj
