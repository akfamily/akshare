# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Numba-compiled functions.

Provides an arsenal of Numba-compiled functions that are used by indicator
classes. These only accept NumPy arrays and other Numba-compatible types.

!!! note
    Set `wait` to 1 to exclude the current value from calculation of future values.

!!! warning
    Do not attempt to use these functions for building features as they
    may introduce look-ahead bias to your model."""

import numpy as np
from numba import njit

from vectorbt import _typing as tp
from vectorbt.base.reshape_fns import flex_select_auto_nb
from vectorbt.generic import nb as generic_nb
from vectorbt.labels.enums import TrendMode


@njit(cache=True)
def future_mean_apply_nb(close: tp.Array2d,
                         window: int,
                         ewm: bool,
                         wait: int = 1,
                         adjust: bool = False) -> tp.Array2d:
    """Get the mean of the next period."""
    if ewm:
        out = generic_nb.ewm_mean_nb(close[::-1], window, minp=window, adjust=adjust)[::-1]
    else:
        out = generic_nb.rolling_mean_nb(close[::-1], window, minp=window)[::-1]
    if wait > 0:
        return generic_nb.bshift_nb(out, wait)
    return out


@njit(cache=True)
def future_std_apply_nb(close: tp.Array2d,
                        window: int,
                        ewm: bool,
                        wait: int = 1,
                        adjust: bool = False,
                        ddof: int = 0) -> tp.Array2d:
    """Get the standard deviation of the next period."""
    if ewm:
        out = generic_nb.ewm_std_nb(close[::-1], window, minp=window, adjust=adjust, ddof=ddof)[::-1]
    else:
        out = generic_nb.rolling_std_nb(close[::-1], window, minp=window, ddof=ddof)[::-1]
    if wait > 0:
        return generic_nb.bshift_nb(out, wait)
    return out


@njit(cache=True)
def future_min_apply_nb(close: tp.Array2d, window: int, wait: int = 1) -> tp.Array2d:
    """Get the minimum of the next period."""
    out = generic_nb.rolling_min_nb(close[::-1], window, minp=window)[::-1]
    if wait > 0:
        return generic_nb.bshift_nb(out, wait)
    return out


@njit(cache=True)
def future_max_apply_nb(close: tp.Array2d, window: int, wait: int = 1) -> tp.Array2d:
    """Get the maximum of the next period."""
    out = generic_nb.rolling_max_nb(close[::-1], window, minp=window)[::-1]
    if wait > 0:
        return generic_nb.bshift_nb(out, wait)
    return out


@njit(cache=True)
def fixed_labels_apply_nb(close: tp.Array2d, n: int) -> tp.Array2d:
    """Get percentage change from the current value to a future value."""
    return (generic_nb.bshift_nb(close, n) - close) / close


@njit(cache=True)
def mean_labels_apply_nb(close: tp.Array2d,
                         window: int,
                         ewm: bool,
                         wait: int = 1,
                         adjust: bool = False) -> tp.Array2d:
    """Get the percentage change from the current value to the average of the next period."""
    return (future_mean_apply_nb(close, window, ewm, wait, adjust) - close) / close


@njit(cache=True)
def get_symmetric_pos_th_nb(neg_th: tp.MaybeArray[float]) -> tp.MaybeArray[float]:
    """Compute the positive return that is symmetric to a negative one.

    For example, 50% down requires 100% to go up to the initial level."""
    return neg_th / (1 - neg_th)


@njit(cache=True)
def get_symmetric_neg_th_nb(pos_th: tp.MaybeArray[float]) -> tp.MaybeArray[float]:
    """Compute the negative return that is symmetric to a positive one."""
    return pos_th / (1 + pos_th)


@njit(cache=True)
def local_extrema_apply_nb(close: tp.Array2d,
                           pos_th: tp.MaybeArray[float],
                           neg_th: tp.MaybeArray[float],
                           flex_2d: bool = True) -> tp.Array2d:
    """Get array of local extrema denoted by 1 (peak) or -1 (trough), otherwise 0.

    Two adjacent peak and trough points should exceed the given threshold parameters.

    If any threshold is given element-wise, it will be applied per new/updated extremum.

    Inspired by https://www.mdpi.com/1099-4300/22/10/1162/pdf"""
    pos_th = np.asarray(pos_th)
    neg_th = np.asarray(neg_th)
    out = np.full(close.shape, 0, dtype=np.int64)

    for col in range(close.shape[1]):
        prev_i = 0
        direction = 0

        for i in range(1, close.shape[0]):
            _pos_th = abs(flex_select_auto_nb(pos_th, prev_i, col, flex_2d))
            _neg_th = abs(flex_select_auto_nb(neg_th, prev_i, col, flex_2d))
            if _pos_th == 0:
                raise ValueError("Positive threshold cannot be 0")
            if _neg_th == 0:
                raise ValueError("Negative threshold cannot be 0")

            if direction == 1:
                # Find next high while updating current lows
                if close[i, col] < close[prev_i, col]:
                    prev_i = i
                elif close[i, col] >= close[prev_i, col] * (1 + _pos_th):
                    out[prev_i, col] = -1
                    prev_i = i
                    direction = -1
            elif direction == -1:
                # Find next low while updating current highs
                if close[i, col] > close[prev_i, col]:
                    prev_i = i
                elif close[i, col] <= close[prev_i, col] * (1 - _neg_th):
                    out[prev_i, col] = 1
                    prev_i = i
                    direction = 1
            else:
                # Find first high/low
                if close[i, col] >= close[prev_i, col] * (1 + _pos_th):
                    out[prev_i, col] = -1
                    prev_i = i
                    direction = -1
                elif close[i, col] <= close[prev_i, col] * (1 - _neg_th):
                    out[prev_i, col] = 1
                    prev_i = i
                    direction = 1

            if i == close.shape[0] - 1:
                # Find last high/low
                if direction != 0:
                    out[prev_i, col] = -direction
    return out


@njit(cache=True)
def bn_trend_labels_nb(close: tp.Array2d, local_extrema: tp.Array2d) -> tp.Array2d:
    """Return 0 for H-L and 1 for L-H."""
    out = np.full_like(close, np.nan, dtype=np.float64)

    for col in range(close.shape[1]):
        idxs = np.flatnonzero(local_extrema[:, col])
        if idxs.shape[0] == 0:
            continue

        for k in range(1, idxs.shape[0]):
            prev_i = idxs[k - 1]
            next_i = idxs[k]

            if close[next_i, col] > close[prev_i, col]:
                out[prev_i:next_i, col] = 1
            else:
                out[prev_i:next_i, col] = 0

    return out


@njit(cache=True)
def bn_cont_trend_labels_nb(close: tp.Array2d, local_extrema: tp.Array2d) -> tp.Array2d:
    """Normalize each range between two extrema between 0 (will go up) and 1 (will go down)."""
    out = np.full_like(close, np.nan, dtype=np.float64)

    for col in range(close.shape[1]):
        idxs = np.flatnonzero(local_extrema[:, col])
        if idxs.shape[0] == 0:
            continue

        for k in range(1, idxs.shape[0]):
            prev_i = idxs[k - 1]
            next_i = idxs[k]

            _min = np.min(close[prev_i:next_i + 1, col])
            _max = np.max(close[prev_i:next_i + 1, col])
            out[prev_i:next_i, col] = 1 - (close[prev_i:next_i, col] - _min) / (_max - _min)

    return out


@njit(cache=True)
def bn_cont_sat_trend_labels_nb(close: tp.Array2d,
                                local_extrema: tp.Array2d,
                                pos_th: tp.MaybeArray[float],
                                neg_th: tp.MaybeArray[float],
                                flex_2d: bool = True) -> tp.Array2d:
    """Similar to `bn_cont_trend_labels_nb` but sets each close value to 0 or 1
    if the percentage change to the next extremum exceeds the threshold set for this range.
    """
    pos_th = np.asarray(pos_th)
    neg_th = np.asarray(neg_th)
    out = np.full_like(close, np.nan, dtype=np.float64)

    for col in range(close.shape[1]):
        idxs = np.flatnonzero(local_extrema[:, col])
        if idxs.shape[0] == 0:
            continue

        for k in range(1, idxs.shape[0]):
            prev_i = idxs[k - 1]
            next_i = idxs[k]

            _pos_th = abs(flex_select_auto_nb(pos_th, prev_i, col, flex_2d))
            _neg_th = abs(flex_select_auto_nb(neg_th, prev_i, col, flex_2d))
            if _pos_th == 0:
                raise ValueError("Positive threshold cannot be 0")
            if _neg_th == 0:
                raise ValueError("Negative threshold cannot be 0")
            _min = np.min(close[prev_i:next_i + 1, col])
            _max = np.max(close[prev_i:next_i + 1, col])

            for i in range(prev_i, next_i):
                if close[next_i, col] > close[prev_i, col]:
                    _start = _max / (1 + _pos_th)
                    _end = _min * (1 + _pos_th)
                    if _max >= _end and close[i, col] <= _start:
                        out[i, col] = 1
                    else:
                        out[i, col] = 1 - (close[i, col] - _start) / (_max - _start)
                else:
                    _start = _min / (1 - _neg_th)
                    _end = _max * (1 - _neg_th)
                    if _min <= _end and close[i, col] >= _start:
                        out[i, col] = 0
                    else:
                        out[i, col] = 1 - (close[i, col] - _min) / (_start - _min)

    return out


@njit(cache=True)
def pct_trend_labels_nb(close: tp.Array2d, local_extrema: tp.Array2d, normalize: bool) -> tp.Array2d:
    """Compute the percentage change of the current value to the next extremum."""
    out = np.full_like(close, np.nan, dtype=np.float64)

    for col in range(close.shape[1]):
        idxs = np.flatnonzero(local_extrema[:, col])
        if idxs.shape[0] == 0:
            continue

        for k in range(1, idxs.shape[0]):
            prev_i = idxs[k - 1]
            next_i = idxs[k]

            for i in range(prev_i, next_i):
                if close[next_i, col] > close[prev_i, col] and normalize:
                    out[i, col] = (close[next_i, col] - close[i, col]) / close[next_i, col]
                else:
                    out[i, col] = (close[next_i, col] - close[i, col]) / close[i, col]

    return out


@njit(cache=True)
def trend_labels_apply_nb(close: tp.Array2d,
                          pos_th: tp.MaybeArray[float],
                          neg_th: tp.MaybeArray[float],
                          mode: int,
                          flex_2d: bool = True) -> tp.Array2d:
    """Apply a trend labeling function based on `TrendMode`."""
    local_extrema = local_extrema_apply_nb(close, pos_th, neg_th, flex_2d)
    if mode == TrendMode.Binary:
        return bn_trend_labels_nb(close, local_extrema)
    if mode == TrendMode.BinaryCont:
        return bn_cont_trend_labels_nb(close, local_extrema)
    if mode == TrendMode.BinaryContSat:
        return bn_cont_sat_trend_labels_nb(close, local_extrema, pos_th, neg_th, flex_2d)
    if mode == TrendMode.PctChange:
        return pct_trend_labels_nb(close, local_extrema, False)
    if mode == TrendMode.PctChangeNorm:
        return pct_trend_labels_nb(close, local_extrema, True)
    raise ValueError("Trend mode is not recognized")


@njit(cache=True)
def breakout_labels_nb(close: tp.Array2d,
                       window: int,
                       pos_th: tp.MaybeArray[float],
                       neg_th: tp.MaybeArray[float],
                       wait: int = 1,
                       flex_2d: bool = True) -> tp.Array2d:
    """For each value, return 1 if any value in the next period is greater than the
    positive threshold (in %), -1 if less than the negative threshold, and 0 otherwise.

    First hit wins."""
    pos_th = np.asarray(pos_th)
    neg_th = np.asarray(neg_th)
    out = np.full_like(close, 0, dtype=np.float64)

    for col in range(close.shape[1]):
        for i in range(close.shape[0]):
            _pos_th = abs(flex_select_auto_nb(pos_th, i, col, flex_2d))
            _neg_th = abs(flex_select_auto_nb(neg_th, i, col, flex_2d))

            for j in range(i + wait, min(i + window + wait, close.shape[0])):
                if _pos_th > 0 and close[j, col] >= close[i, col] * (1 + _pos_th):
                    out[i, col] = 1
                    break
                if _neg_th > 0 and close[j, col] <= close[i, col] * (1 - _neg_th):
                    out[i, col] = -1
                    break

    return out
