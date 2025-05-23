# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Functions for working with index/columns.

Index functions perform operations on index objects, such as stacking, combining,
and cleansing MultiIndex levels. "Index" in pandas context is referred to both index and columns."""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from numba import njit

from vectorbt import _typing as tp
from vectorbt.utils import checks


def to_any_index(index_like: tp.IndexLike) -> tp.Index:
    """Convert any index-like object to an index.

    Index objects are kept as-is."""
    if not isinstance(index_like, pd.Index):
        return pd.Index(index_like)
    return index_like


def get_index(arg: tp.SeriesFrame, axis: int) -> tp.Index:
    """Get index of `arg` by `axis`."""
    checks.assert_instance_of(arg, (pd.Series, pd.DataFrame))
    checks.assert_in(axis, (0, 1))

    if axis == 0:
        return arg.index
    else:
        if checks.is_series(arg):
            if arg.name is not None:
                return pd.Index([arg.name])
            return pd.Index([0])  # same as how pandas does it
        else:
            return arg.columns


def index_from_values(values: tp.ArrayLikeSequence, name: tp.Optional[str] = None) -> tp.Index:
    """Create a new `pd.Index` with `name` by parsing an iterable `values`.

    Each in `values` will correspond to an element in the new index."""
    scalar_types = (int, float, complex, str, bool, datetime, timedelta, np.generic)
    value_names = []
    for i in range(len(values)):
        v = values[i]
        if v is None or isinstance(v, scalar_types):
            value_names.append(v)
        elif isinstance(v, np.ndarray):
            if np.issubdtype(v.dtype, np.floating):
                if np.isclose(v, v.item(0), equal_nan=True).all():
                    value_names.append(v.item(0))
                else:
                    value_names.append('array_%d' % i)
            else:
                if np.equal(v, v.item(0)).all():
                    value_names.append(v.item(0))
                else:
                    value_names.append('array_%d' % i)
        else:
            value_names.append('%s_%d' % (str(type(v).__name__), i))
    return pd.Index(value_names, name=name)


def repeat_index(index: tp.IndexLike, n: int, ignore_default: tp.Optional[bool] = None) -> tp.Index:
    """Repeat each element in `index` `n` times.

    Set `ignore_default` to None to use the default."""
    from vectorbt._settings import settings
    broadcasting_cfg = settings['broadcasting']

    if ignore_default is None:
        ignore_default = broadcasting_cfg['ignore_default']

    index = to_any_index(index)
    if checks.is_default_index(index) and ignore_default:  # ignore simple ranges without name
        return pd.RangeIndex(start=0, stop=len(index) * n, step=1)
    return index.repeat(n)


def tile_index(index: tp.IndexLike, n: int, ignore_default: tp.Optional[bool] = None) -> tp.Index:
    """Tile the whole `index` `n` times.

    Set `ignore_default` to None to use the default."""
    from vectorbt._settings import settings
    broadcasting_cfg = settings['broadcasting']

    if ignore_default is None:
        ignore_default = broadcasting_cfg['ignore_default']

    index = to_any_index(index)
    if checks.is_default_index(index) and ignore_default:  # ignore simple ranges without name
        return pd.RangeIndex(start=0, stop=len(index) * n, step=1)
    if isinstance(index, pd.MultiIndex):
        return pd.MultiIndex.from_tuples(np.tile(index, n), names=index.names)
    return pd.Index(np.tile(index, n), name=index.name)


def stack_indexes(indexes: tp.Sequence[tp.IndexLike], drop_duplicates: tp.Optional[bool] = None,
                  keep: tp.Optional[str] = None, drop_redundant: tp.Optional[bool] = None) -> tp.Index:
    """Stack each index in `indexes` on top of each other, from top to bottom.

    Set `drop_duplicates`, `keep`, or `drop_redundant` to None to use the default."""
    from vectorbt._settings import settings
    broadcasting_cfg = settings['broadcasting']

    if drop_duplicates is None:
        drop_duplicates = broadcasting_cfg['drop_duplicates']
    if keep is None:
        keep = broadcasting_cfg['keep']
    if drop_redundant is None:
        drop_redundant = broadcasting_cfg['drop_redundant']

    levels = []
    for i in range(len(indexes)):
        index = indexes[i]
        if not isinstance(index, pd.MultiIndex):
            levels.append(to_any_index(index))
        else:
            for j in range(index.nlevels):
                levels.append(index.get_level_values(j))

    new_index = pd.MultiIndex.from_arrays(levels)
    if drop_duplicates:
        new_index = drop_duplicate_levels(new_index, keep=keep)
    if drop_redundant:
        new_index = drop_redundant_levels(new_index)
    return new_index


def combine_indexes(indexes: tp.Sequence[tp.IndexLike],
                    ignore_default: tp.Optional[bool] = None, **kwargs) -> tp.Index:
    """Combine each index in `indexes` using Cartesian product.

    Keyword arguments will be passed to `stack_indexes`."""
    new_index = to_any_index(indexes[0])
    for i in range(1, len(indexes)):
        index1, index2 = new_index, to_any_index(indexes[i])
        new_index1 = repeat_index(index1, len(index2), ignore_default=ignore_default)
        new_index2 = tile_index(index2, len(index1), ignore_default=ignore_default)
        new_index = stack_indexes([new_index1, new_index2], **kwargs)
    return new_index


def drop_levels(index: tp.Index, levels: tp.MaybeLevelSequence, strict: bool = True) -> tp.Index:
    """Drop `levels` in `index` by their name/position."""
    if not isinstance(index, pd.MultiIndex):
        return index
    if strict:
        return index.droplevel(levels)

    levels_to_drop = set()
    if isinstance(levels, (int, str)):
        levels = (levels,)
    for level in levels:
        if level in index.names:
            levels_to_drop.add(level)
        elif isinstance(level, int) and 0 <= level < index.nlevels or level == -1:
            levels_to_drop.add(level)
    if len(levels_to_drop) < index.nlevels:
        # Drop only if there will be some indexes left
        return index.droplevel(list(levels_to_drop))
    return index


def rename_levels(index: tp.Index, name_dict: tp.Dict[str, tp.Any], strict: bool = True) -> tp.Index:
    """Rename levels in `index` by `name_dict`."""
    for k, v in name_dict.items():
        if isinstance(index, pd.MultiIndex):
            if k in index.names:
                index = index.rename(v, level=k)
            elif strict:
                raise KeyError(f"Level '{k}' not found")
        else:
            if index.name == k:
                index.name = v
            elif strict:
                raise KeyError(f"Level '{k}' not found")
    return index


def select_levels(index: tp.Index, level_names: tp.MaybeLevelSequence) -> tp.Index:
    """Build a new index by selecting one or multiple `level_names` from `index`."""
    checks.assert_instance_of(index, pd.MultiIndex)

    if isinstance(level_names, (int, str)):
        return index.get_level_values(level_names)
    levels = [index.get_level_values(level_name) for level_name in level_names]
    return pd.MultiIndex.from_arrays(levels)


def drop_redundant_levels(index: tp.Index) -> tp.Index:
    """Drop levels in `index` that either have a single unnamed value or a range from 0 to n."""
    if not isinstance(index, pd.MultiIndex):
        return index

    levels_to_drop = []
    for i in range(index.nlevels):
        if len(index) > 1 and len(index.levels[i]) == 1 and index.levels[i].name is None:
            levels_to_drop.append(i)
        elif checks.is_default_index(index.get_level_values(i)):
            levels_to_drop.append(i)
    # Remove redundant levels only if there are some non-redundant levels left
    if len(levels_to_drop) < index.nlevels:
        return index.droplevel(levels_to_drop)
    return index


def drop_duplicate_levels(index: tp.Index, keep: tp.Optional[str] = None) -> tp.Index:
    """Drop levels in `index` with the same name and values.

    Set `keep` to 'last' to keep last levels, otherwise 'first'.

    Set `keep` to None to use the default."""
    from vectorbt._settings import settings
    broadcasting_cfg = settings['broadcasting']

    if keep is None:
        keep = broadcasting_cfg['keep']
    if not isinstance(index, pd.MultiIndex):
        return index
    checks.assert_in(keep.lower(), ['first', 'last'])

    levels = []
    levels_to_drop = []
    if keep == 'first':
        r = range(0, index.nlevels)
    else:
        r = range(index.nlevels - 1, -1, -1)  # loop backwards
    for i in r:
        level = (index.levels[i].name, tuple(index.get_level_values(i).to_numpy().tolist()))
        if level not in levels:
            levels.append(level)
        else:
            levels_to_drop.append(i)
    return index.droplevel(levels_to_drop)


@njit(cache=True)
def _align_index_to_nb(a: tp.Array1d, b: tp.Array1d) -> tp.Array1d:
    """Return indices required to align `a` to `b`."""
    idxs = np.empty(b.shape[0], dtype=np.int64)
    g = 0
    for i in range(b.shape[0]):
        for j in range(a.shape[0]):
            if b[i] == a[j]:
                idxs[g] = j
                g += 1
                break
    return idxs


def align_index_to(index1: tp.Index, index2: tp.Index) -> pd.IndexSlice:
    """Align `index1` to have the same shape as `index2` if they have any levels in common.

    Returns index slice for the aligning."""
    if not isinstance(index1, pd.MultiIndex):
        index1 = pd.MultiIndex.from_arrays([index1])
    if not isinstance(index2, pd.MultiIndex):
        index2 = pd.MultiIndex.from_arrays([index2])
    if pd.Index.equals(index1, index2):
        return pd.IndexSlice[:]

    # Build map between levels in first and second index
    mapper = {}
    for i in range(index1.nlevels):
        for j in range(index2.nlevels):
            name1 = index1.names[i]
            name2 = index2.names[j]
            if name1 == name2:
                if set(index2.levels[j]).issubset(set(index1.levels[i])):
                    if i in mapper:
                        raise ValueError(f"There are multiple candidate levels with name {name1} in second index")
                    mapper[i] = j
                    continue
                if name1 is not None:
                    raise ValueError(f"Level {name1} in second index contains values not in first index")
    if len(mapper) == 0:
        raise ValueError("Can't find common levels to align both indexes")

    # Factorize first to be accepted by Numba
    factorized = []
    for k, v in mapper.items():
        factorized.append(pd.factorize(pd.concat((
            index1.get_level_values(k).to_series(),
            index2.get_level_values(v).to_series()
        )))[0])
    stacked = np.transpose(np.stack(factorized))
    indices1 = stacked[:len(index1)]
    indices2 = stacked[len(index1):]
    if len(np.unique(indices1, axis=0)) != len(indices1):
        raise ValueError("Duplicated values in first index are not allowed")

    # Try to tile
    if len(index2) % len(index1) == 0:
        tile_times = len(index2) // len(index1)
        index1_tiled = np.tile(indices1, (tile_times, 1))
        if np.array_equal(index1_tiled, indices2):
            return pd.IndexSlice[np.tile(np.arange(len(index1)), tile_times)]

    # Do element-wise comparison
    unique_indices = np.unique(stacked, axis=0, return_inverse=True)[1]
    unique1 = unique_indices[:len(index1)]
    unique2 = unique_indices[len(index1):]
    return pd.IndexSlice[_align_index_to_nb(unique1, unique2)]


def align_indexes(indexes: tp.Sequence[tp.Index]) -> tp.List[tp.Index]:
    """Align multiple indexes to each other."""
    max_len = max(map(len, indexes))
    indices = []
    for i in range(len(indexes)):
        index_i = indexes[i]
        if len(index_i) == max_len:
            indices.append(pd.IndexSlice[:])
        else:
            for j in range(len(indexes)):
                index_j = indexes[j]
                if len(index_j) == max_len:
                    try:
                        indices.append(align_index_to(index_i, index_j))
                        break
                    except ValueError:
                        pass
            if len(indices) < i + 1:
                raise ValueError(f"Index at position {i} could not be aligned")
    return indices


OptionalLevelSequence = tp.Optional[tp.Sequence[tp.Union[None, tp.Level]]]


def pick_levels(index: tp.Index,
                required_levels: OptionalLevelSequence = None,
                optional_levels: OptionalLevelSequence = None) -> tp.Tuple[tp.List[int], tp.List[int]]:
    """Pick optional and required levels and return their indices.

    Raises an exception if index has less or more levels than expected."""
    if required_levels is None:
        required_levels = []
    if optional_levels is None:
        optional_levels = []
    checks.assert_instance_of(index, pd.MultiIndex)

    n_opt_set = len(list(filter(lambda x: x is not None, optional_levels)))
    n_req_set = len(list(filter(lambda x: x is not None, required_levels)))
    n_levels_left = index.nlevels - n_opt_set
    if n_req_set < len(required_levels):
        if n_levels_left != len(required_levels):
            n_expected = len(required_levels) + n_opt_set
            raise ValueError(f"Expected {n_expected} levels, found {index.nlevels}")

    levels_left = list(range(index.nlevels))

    # Pick optional levels
    _optional_levels = []
    for level in optional_levels:
        level_pos = None
        if level is not None:
            checks.assert_instance_of(level, (int, str))
            if isinstance(level, str):
                level_pos = index.names.index(level)
            else:
                level_pos = level
            if level_pos < 0:
                level_pos = index.nlevels + level_pos
            levels_left.remove(level_pos)
        _optional_levels.append(level_pos)

    # Pick required levels
    _required_levels = []
    for level in required_levels:
        level_pos = None
        if level is not None:
            checks.assert_instance_of(level, (int, str))
            if isinstance(level, str):
                level_pos = index.names.index(level)
            else:
                level_pos = level
            if level_pos < 0:
                level_pos = index.nlevels + level_pos
            levels_left.remove(level_pos)
        _required_levels.append(level_pos)
    for i, level in enumerate(_required_levels):
        if level is None:
            _required_levels[i] = levels_left.pop(0)

    return _required_levels, _optional_levels


def find_first_occurrence(index_value: tp.Any, index: tp.Index) -> int:
    """Return index of the first occurrence in `index`."""
    loc = index.get_loc(index_value)
    if isinstance(loc, slice):
        return loc.start
    elif isinstance(loc, list):
        return loc[0]
    elif isinstance(loc, np.ndarray):
        return np.flatnonzero(loc)[0]
    return loc
