# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for working with arrays."""

import numpy as np
from numba import njit

from vectorbt import _typing as tp


def is_sorted(a: tp.Array1d) -> np.bool_:
    """Checks if array is sorted."""
    return np.all(a[:-1] <= a[1:])


@njit(cache=True)
def is_sorted_nb(a: tp.Array1d) -> bool:
    """Numba-compiled version of `is_sorted`."""
    for i in range(a.size - 1):
        if a[i + 1] < a[i]:
            return False
    return True


@njit(cache=True)
def insert_argsort_nb(A: tp.Array1d, I: tp.Array1d) -> None:
    """Perform argsort using insertion sort.

    In-memory and without recursion -> very fast for smaller arrays."""
    for j in range(1, len(A)):
        A_j = A[j]
        I_j = I[j]
        i = j - 1
        while i >= 0 and (A[i] > A_j or np.isnan(A[i])):
            A[i + 1] = A[i]
            I[i + 1] = I[i]
            i = i - 1
        A[i + 1] = A_j
        I[i + 1] = I_j


def get_ranges_arr(starts: tp.ArrayLike, ends: tp.ArrayLike) -> tp.Array1d:
    """Build array from start and end indices.

    Based on https://stackoverflow.com/a/37626057"""
    starts_arr = np.asarray(starts)
    if starts_arr.ndim == 0:
        starts_arr = np.array([starts_arr])
    ends_arr = np.asarray(ends)
    if ends_arr.ndim == 0:
        ends_arr = np.array([ends_arr])
    starts_arr, end = np.broadcast_arrays(starts_arr, ends_arr)
    counts = ends_arr - starts_arr
    counts_csum = counts.cumsum()
    id_arr = np.ones(counts_csum[-1], dtype=int)
    id_arr[0] = starts_arr[0]
    id_arr[counts_csum[:-1]] = starts_arr[1:] - ends_arr[:-1] + 1
    return id_arr.cumsum()


@njit(cache=True)
def uniform_summing_to_one_nb(n: int) -> tp.Array1d:
    """Generate random floats summing to one.

    See # https://stackoverflow.com/a/2640067/8141780"""
    rand_floats = np.empty(n + 1, dtype=np.float64)
    rand_floats[0] = 0.
    rand_floats[1] = 1.
    rand_floats[2:] = np.random.uniform(0, 1, n - 1)
    rand_floats = np.sort(rand_floats)
    rand_floats = rand_floats[1:] - rand_floats[:-1]
    return rand_floats


def renormalize(a: tp.MaybeArray[float], from_range: tp.Tuple[float, float],
                to_range: tp.Tuple[float, float]) -> tp.MaybeArray[float]:
    """Renormalize `a` from one range to another."""
    from_delta = from_range[1] - from_range[0]
    to_delta = to_range[1] - to_range[0]
    return (to_delta * (a - from_range[0]) / from_delta) + to_range[0]


renormalize_nb = njit(cache=True)(renormalize)
"""Numba-compiled version of `renormalize`."""


def min_rel_rescale(a: tp.Array, to_range: tp.Tuple[float, float]) -> tp.Array:
    """Rescale elements in `a` relatively to minimum."""
    a_min = np.min(a)
    a_max = np.max(a)
    if a_max - a_min == 0:
        return np.full(a.shape, to_range[0])
    from_range = (a_min, a_max)

    from_range_ratio = np.inf
    if a_min != 0:
        from_range_ratio = a_max / a_min

    to_range_ratio = to_range[1] / to_range[0]
    if from_range_ratio < to_range_ratio:
        to_range = (to_range[0], to_range[0] * from_range_ratio)
    return renormalize(a, from_range, to_range)


def max_rel_rescale(a: tp.Array, to_range: tp.Tuple[float, float]) -> tp.Array:
    """Rescale elements in `a` relatively to maximum."""
    a_min = np.min(a)
    a_max = np.max(a)
    if a_max - a_min == 0:
        return np.full(a.shape, to_range[1])
    from_range = (a_min, a_max)

    from_range_ratio = np.inf
    if a_min != 0:
        from_range_ratio = a_max / a_min

    to_range_ratio = to_range[1] / to_range[0]
    if from_range_ratio < to_range_ratio:
        to_range = (to_range[1] / from_range_ratio, to_range[1])
    return renormalize(a, from_range, to_range)


@njit(cache=True)
def rescale_float_to_int_nb(floats: tp.Array, int_range: tp.Tuple[float, float], total: float) -> tp.Array:
    """Rescale a float array into an int array."""
    ints = np.floor(renormalize_nb(floats, [0., 1.], int_range))
    leftover = int(total - ints.sum())
    for i in range(leftover):
        ints[np.random.choice(len(ints))] += 1
    return ints
