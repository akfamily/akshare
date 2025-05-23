# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Numba-compiled functions.

Provides an arsenal of Numba-compiled functions for records and mapped arrays.
These only accept NumPy arrays and other Numba-compatible types.

!!! note
    vectorbt treats matrices as first-class citizens and expects input arrays to be
    2-dim, unless function has suffix `_1d` or is meant to be input to another function.
    Data is processed along index (axis 0).

    All functions passed as argument should be Numba-compiled.

    Records should retain the order they were created in."""

import numpy as np
from numba import njit
from numba.extending import overload
from numba.np.numpy_support import as_dtype

from vectorbt import _typing as tp


# ############# Indexing ############# #


@njit(cache=True)
def col_range_nb(col_arr: tp.Array1d, n_cols: int) -> tp.ColRange:
    """Build column range for sorted column array.

    Creates a 2-dim array with first column being start indices (inclusive) and
    second column being end indices (exclusive).

    !!! note
        Requires `col_arr` to be in ascending order. This can be done by sorting."""
    col_range = np.full((n_cols, 2), -1, dtype=np.int64)
    last_col = -1

    for r in range(col_arr.shape[0]):
        col = col_arr[r]
        if col < last_col:
            raise ValueError("col_arr must be in ascending order")
        if col != last_col:
            if last_col != -1:
                col_range[last_col, 1] = r
            col_range[col, 0] = r
            last_col = col
        if r == col_arr.shape[0] - 1:
            col_range[col, 1] = r + 1
    return col_range


@njit(cache=True)
def col_range_select_nb(col_range: tp.ColRange, new_cols: tp.Array1d) -> tp.Tuple[tp.Array1d, tp.Array1d]:
    """Perform indexing on a sorted array using column range `col_range`.

    Returns indices of elements corresponding to columns in `new_cols` and a new column array."""
    col_range = col_range[new_cols]
    new_n = np.sum(col_range[:, 1] - col_range[:, 0])
    indices_out = np.empty(new_n, dtype=np.int64)
    col_arr_out = np.empty(new_n, dtype=np.int64)
    j = 0

    for c in range(new_cols.shape[0]):
        from_r = col_range[c, 0]
        to_r = col_range[c, 1]
        if from_r == -1 or to_r == -1:
            continue
        rang = np.arange(from_r, to_r)
        indices_out[j:j + rang.shape[0]] = rang
        col_arr_out[j:j + rang.shape[0]] = c
        j += rang.shape[0]
    return indices_out, col_arr_out


@njit(cache=True)
def record_col_range_select_nb(records: tp.RecordArray, col_range: tp.ColRange,
                               new_cols: tp.Array1d) -> tp.RecordArray:
    """Perform indexing on sorted records using column range `col_range`.

    Returns new records."""
    col_range = col_range[new_cols]
    new_n = np.sum(col_range[:, 1] - col_range[:, 0])
    out = np.empty(new_n, dtype=records.dtype)
    j = 0

    for c in range(new_cols.shape[0]):
        from_r = col_range[c, 0]
        to_r = col_range[c, 1]
        if from_r == -1 or to_r == -1:
            continue
        col_records = np.copy(records[from_r:to_r])
        col_records['col'][:] = c  # don't forget to assign new column indices
        out[j:j + col_records.shape[0]] = col_records
        j += col_records.shape[0]
    return out


@njit(cache=True)
def col_map_nb(col_arr: tp.Array1d, n_cols: int) -> tp.ColMap:
    """Build a map between columns and their indices.

    Returns an array with indices segmented by column, and an array with count per segment.

    Works well for unsorted column arrays."""
    col_lens_out = np.full(n_cols, 0, dtype=np.int64)
    for r in range(col_arr.shape[0]):
        col = col_arr[r]
        col_lens_out[col] += 1

    col_start_idxs = np.cumsum(col_lens_out) - col_lens_out
    col_idxs_out = np.empty((col_arr.shape[0],), dtype=np.int64)
    col_i = np.full(n_cols, 0, dtype=np.int64)
    for r in range(col_arr.shape[0]):
        col = col_arr[r]
        col_idxs_out[col_start_idxs[col] + col_i[col]] = r
        col_i[col] += 1

    return col_idxs_out, col_lens_out


@njit(cache=True)
def col_map_select_nb(col_map: tp.ColMap, new_cols: tp.Array1d) -> tp.Tuple[tp.Array1d, tp.Array1d]:
    """Same as `mapped_col_range_select_nb` but using column map `col_map`."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    total_count = np.sum(col_lens[new_cols])
    idxs_out = np.empty(total_count, dtype=np.int64)
    col_arr_out = np.empty(total_count, dtype=np.int64)
    j = 0

    for new_col_i in range(len(new_cols)):
        new_col = new_cols[new_col_i]
        col_len = col_lens[new_col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[new_col]
        idxs = col_idxs[col_start_idx:col_start_idx + col_len]
        idxs_out[j:j + col_len] = idxs
        col_arr_out[j:j + col_len] = new_col_i
        j += col_len
    return idxs_out, col_arr_out


@njit(cache=True)
def record_col_map_select_nb(records: tp.RecordArray, col_map: tp.ColMap, new_cols: tp.Array1d) -> tp.RecordArray:
    """Same as `record_col_range_select_nb` but using column map `col_map`."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.empty(np.sum(col_lens[new_cols]), dtype=records.dtype)
    j = 0

    for new_col_i in range(len(new_cols)):
        new_col = new_cols[new_col_i]
        col_len = col_lens[new_col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[new_col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        col_records = np.copy(records[ridxs])
        col_records['col'][:] = new_col_i
        out[j:j + col_len] = col_records
        j += col_len
    return out


# ############# Sorting ############# #


@njit(cache=True)
def is_col_sorted_nb(col_arr: tp.Array1d) -> bool:
    """Check whether the column array is sorted."""
    for i in range(len(col_arr) - 1):
        if col_arr[i + 1] < col_arr[i]:
            return False
    return True


@njit(cache=True)
def is_col_idx_sorted_nb(col_arr: tp.Array1d, id_arr: tp.Array1d) -> bool:
    """Check whether the column and index arrays are sorted."""
    for i in range(len(col_arr) - 1):
        if col_arr[i + 1] < col_arr[i]:
            return False
        if col_arr[i + 1] == col_arr[i] and id_arr[i + 1] < id_arr[i]:
            return False
    return True


# ############# Mapping ############# #


@njit
def mapped_to_mask_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap,
                      inout_map_func_nb: tp.MaskInOutMapFunc, *args) -> tp.Array1d:
    """Map mapped array to a mask per column.

    Returns the same shape as `mapped_arr`.

    `inout_map_func_nb` should accept the boolean array that should be written, indices of values,
    index of the column, values of the column, and `*args`, and return nothing."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    inout = np.full(mapped_arr.shape[0], False, dtype=np.bool_)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        inout_map_func_nb(inout, ridxs, col, mapped_arr[ridxs], *args)
    return inout


@njit(cache=True)
def top_n_inout_map_nb(inout: tp.Array1d, idxs: tp.Array1d, col: int, mapped_arr: tp.Array1d, n: int) -> None:
    """`inout_map_func_nb` that returns indices of top N elements."""
    # TODO: np.argpartition
    inout[idxs[np.argsort(mapped_arr)[-n:]]] = True


@njit(cache=True)
def bottom_n_inout_map_nb(inout: tp.Array1d, idxs: tp.Array1d, col: int, mapped_arr: tp.Array1d, n: int) -> None:
    """`inout_map_func_nb` that returns indices of bottom N elements."""
    inout[idxs[np.argsort(mapped_arr)[:n]]] = True


@njit
def apply_on_mapped_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap,
                       apply_func_nb: tp.MappedApplyFunc, *args) -> tp.Array1d:
    """Apply function on mapped array per column.

    Returns the same shape as `mapped_arr`.

    `apply_func_nb` should accept the indices of values, index of the column, values of the column,
    and `*args`, and return an array."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.empty(mapped_arr.shape[0], dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        out[ridxs] = apply_func_nb(ridxs, col, mapped_arr[ridxs], *args)
    return out


@njit
def apply_on_records_nb(records: tp.RecordArray, col_map: tp.ColMap,
                        apply_func_nb: tp.RecordApplyFunc, *args) -> tp.Array1d:
    """Apply function on records per column.

    Returns the same shape as `records`.

    `apply_func_nb` should accept the records of the column and `*args`, and return an array."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.empty(records.shape[0], dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        out[ridxs] = apply_func_nb(records[ridxs], *args)
    return out


@njit
def map_records_nb(records: tp.RecordArray, map_func_nb: tp.RecordMapFunc[float], *args) -> tp.Array1d:
    """Map each record to a single value.

    `map_func_nb` should accept a single record and `*args`, and return a single value."""
    out = np.empty(records.shape[0], dtype=np.float64)

    for r in range(records.shape[0]):
        out[r] = map_func_nb(records[r], *args)
    return out


# ############# Expansion ############# #


@njit(cache=True)
def is_mapped_expandable_nb(col_arr: tp.Array1d, idx_arr: tp.Array1d, target_shape: tp.Shape) -> bool:
    """Check whether mapped array can be expanded without positional conflicts."""
    temp = np.zeros(target_shape)

    for i in range(len(col_arr)):
        if temp[idx_arr[i], col_arr[i]] > 0:
            return False
        temp[idx_arr[i], col_arr[i]] = 1
    return True


def _expand_mapped_nb(
    mapped_arr,
    col_arr,
    idx_arr,
    target_shape,
    fill_value,
):
    nb_enabled = not isinstance(mapped_arr, np.ndarray)
    if nb_enabled:
        mapped_arr_dtype = as_dtype(mapped_arr.dtype)
        fill_value_dtype = as_dtype(fill_value)
    else:
        mapped_arr_dtype = mapped_arr.dtype
        fill_value_dtype = np.array(fill_value).dtype
    dtype = np.promote_types(mapped_arr_dtype, fill_value_dtype)

    def impl(mapped_arr, col_arr, idx_arr, target_shape, fill_value):
        out = np.full(target_shape, fill_value, dtype=dtype)

        for r in range(mapped_arr.shape[0]):
            out[idx_arr[r], col_arr[r]] = mapped_arr[r]
        return out

    if not nb_enabled:
        return impl(mapped_arr, col_arr, idx_arr, target_shape, fill_value)

    return impl


ol_expand_mapped_nb = overload(_expand_mapped_nb)(_expand_mapped_nb)


@njit(cache=True)
def expand_mapped_nb(
    mapped_arr: tp.Array1d,
    col_arr: tp.Array1d,
    idx_arr: tp.Array1d,
    target_shape: tp.Shape,
    fill_value: float,
) -> tp.Array2d:
    """Set each element to a value by boolean mask."""
    return _expand_mapped_nb(mapped_arr, col_arr, idx_arr, target_shape, fill_value)


def _stack_expand_mapped_nb(mapped_arr, col_map, fill_value):
    nb_enabled = not isinstance(mapped_arr, np.ndarray)
    if nb_enabled:
        mapped_arr_dtype = as_dtype(mapped_arr.dtype)
        fill_value_dtype = as_dtype(fill_value)
    else:
        mapped_arr_dtype = mapped_arr.dtype
        fill_value_dtype = np.array(fill_value).dtype
    dtype = np.promote_types(mapped_arr_dtype, fill_value_dtype)

    def impl(mapped_arr, col_map, fill_value):
        col_idxs, col_lens = col_map
        col_start_idxs = np.cumsum(col_lens) - col_lens
        out = np.full((np.max(col_lens), col_lens.shape[0]), fill_value, dtype=dtype)

        for col in range(col_lens.shape[0]):
            col_len = col_lens[col]
            if col_len == 0:
                continue
            col_start_idx = col_start_idxs[col]
            idxs = col_idxs[col_start_idx : col_start_idx + col_len]
            out[:col_len, col] = mapped_arr[idxs]

        return out

    if not nb_enabled:
        return impl(mapped_arr, col_map, fill_value)

    return impl


ol_stack_expand_mapped_nb = overload(_stack_expand_mapped_nb)(_stack_expand_mapped_nb)


@njit(cache=True)
def stack_expand_mapped_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap, fill_value: float) -> tp.Array2d:
    """Expand mapped array by stacking without using index data."""
    return _stack_expand_mapped_nb(mapped_arr, col_map, fill_value)


# ############# Reducing ############# #

@njit
def reduce_mapped_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap, fill_value: float,
                     reduce_func_nb: tp.ReduceFunc, *args) -> tp.Array1d:
    """Reduce mapped array by column to a single value.

    Faster than `expand_mapped_nb` and `vbt.*` used together, and also
    requires less memory. But does not take advantage of caching.

    `reduce_func_nb` should accept index of the column, mapped array and `*args`,
    and return a single value."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full(col_lens.shape[0], fill_value, dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        out[col] = reduce_func_nb(col, mapped_arr[ridxs], *args)
    return out


@njit
def reduce_mapped_to_idx_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap, idx_arr: tp.Array1d,
                            fill_value: float, reduce_func_nb: tp.ReduceFunc, *args) -> tp.Array1d:
    """Reduce mapped array by column to an index.

    Same as `reduce_mapped_nb` except `idx_arr` should be passed.

    !!! note
        Must return integers or raise an exception."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full(col_lens.shape[0], fill_value, dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        col_out = reduce_func_nb(col, mapped_arr[ridxs], *args)
        out[col] = idx_arr[ridxs][col_out]
    return out


@njit
def reduce_mapped_to_array_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap, fill_value: float,
                              reduce_func_nb: tp.ReduceFunc, *args) -> tp.Array2d:
    """Reduce mapped array by column to an array.

    `reduce_func_nb` same as for `reduce_mapped_nb` but should return an array."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len > 0:
            col_start_idx = col_start_idxs[col]
            col0, idxs0 = col, col_idxs[col_start_idx:col_start_idx + col_len]
            break

    col_out = reduce_func_nb(col0, mapped_arr[idxs0], *args)
    out = np.full((col_out.shape[0], col_lens.shape[0]), fill_value, dtype=np.float64)
    out[:, col0] = col_out

    for col in range(col0 + 1, col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        out[:, col] = reduce_func_nb(col, mapped_arr[ridxs], *args)
    return out


@njit
def reduce_mapped_to_idx_array_nb(mapped_arr: tp.Array1d, col_map: tp.ColMap, idx_arr: tp.Array1d,
                                  fill_value: float, reduce_func_nb: tp.ReduceFunc, *args) -> tp.Array2d:
    """Reduce mapped array by column to an index array.

    Same as `reduce_mapped_to_array_nb` except `idx_arr` should be passed.

    !!! note
        Must return integers or raise an exception."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len > 0:
            col_start_idx = col_start_idxs[col]
            col0, idxs0 = col, col_idxs[col_start_idx:col_start_idx + col_len]
            break

    col_out = reduce_func_nb(col0, mapped_arr[idxs0], *args)
    out = np.full((col_out.shape[0], col_lens.shape[0]), fill_value, dtype=np.float64)
    out[:, col0] = idx_arr[idxs0][col_out]

    for col in range(col0 + 1, col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        col_out = reduce_func_nb(col, mapped_arr[ridxs], *args)
        out[:, col] = idx_arr[ridxs][col_out]
    return out


@njit(cache=True)
def mapped_value_counts_nb(codes: tp.Array1d, n_uniques: int, col_map: tp.ColMap) -> tp.Array2d:
    """Get value counts of an already factorized mapped array."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full((n_uniques, col_lens.shape[0]), 0, dtype=np.int64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        for c in range(col_len):
            out[codes[col_idxs[col_start_idx + c]], col] += 1
    return out
