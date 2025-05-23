# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Numba-compiled functions.

Provides an arsenal of Numba-compiled functions that are used by indicator
classes. These only accept NumPy arrays and other Numba-compatible types.

!!! note
    vectorbt treats matrices as first-class citizens and expects input arrays to be
    2-dim, unless function has suffix `_1d` or is meant to be input to another function.
    Data is processed along index (axis 0).

    All functions passed as argument should be Numba-compiled."""

import numpy as np
from numba import njit

from vectorbt import _typing as tp
from vectorbt.generic import nb as generic_nb


@njit(cache=True)
def ma_nb(a: tp.Array2d, window: int, ewm: bool, adjust: bool = False) -> tp.Array2d:
    """Compute simple or exponential moving average (`ewm=True`)."""
    if ewm:
        return generic_nb.ewm_mean_nb(a, window, minp=window, adjust=adjust)
    return generic_nb.rolling_mean_nb(a, window, minp=window)


@njit(cache=True)
def mstd_nb(a: tp.Array2d, window: int, ewm: int, adjust: bool = False, ddof: int = 0) -> tp.Array2d:
    """Compute simple or exponential moving STD (`ewm=True`)."""
    if ewm:
        return generic_nb.ewm_std_nb(a, window, minp=window, adjust=adjust, ddof=ddof)
    return generic_nb.rolling_std_nb(a, window, minp=window, ddof=ddof)


@njit(cache=True)
def ma_cache_nb(close: tp.Array2d, windows: tp.List[int], ewms: tp.List[bool],
                adjust: bool) -> tp.Dict[int, tp.Array2d]:
    """Caching function for `vectorbt.indicators.basic.MA`."""
    cache_dict = dict()
    for i in range(len(windows)):
        h = hash((windows[i], ewms[i]))
        if h not in cache_dict:
            cache_dict[h] = ma_nb(close, windows[i], ewms[i], adjust=adjust)
    return cache_dict


@njit(cache=True)
def ma_apply_nb(close: tp.Array2d, window: int, ewm: bool, adjust: bool,
                cache_dict: tp.Dict[int, tp.Array2d]) -> tp.Array2d:
    """Apply function for `vectorbt.indicators.basic.MA`."""
    h = hash((window, ewm))
    return cache_dict[h]


@njit(cache=True)
def mstd_cache_nb(close: tp.Array2d, windows: tp.List[int], ewms: tp.List[bool], adjust: bool,
                  ddof: int) -> tp.Dict[int, tp.Array2d]:
    """Caching function for `vectorbt.indicators.basic.MSTD`."""
    cache_dict = dict()
    for i in range(len(windows)):
        h = hash((windows[i], ewms[i]))
        if h not in cache_dict:
            cache_dict[h] = mstd_nb(close, windows[i], ewms[i], adjust=adjust, ddof=ddof)
    return cache_dict


@njit(cache=True)
def mstd_apply_nb(close: tp.Array2d, window: int, ewm: bool, adjust: bool, ddof: int,
                  cache_dict: tp.Dict[int, tp.Array2d]) -> tp.Array2d:
    """Apply function for `vectorbt.indicators.basic.MSTD`."""
    h = hash((window, ewm))
    return cache_dict[h]


@njit(cache=True)
def bb_cache_nb(close: tp.Array2d, windows: tp.List[int], ewms: tp.List[bool], alphas: tp.List[float],
                adjust: bool, ddof: int) -> tp.Tuple[tp.Dict[int, tp.Array2d], tp.Dict[int, tp.Array2d]]:
    """Caching function for `vectorbt.indicators.basic.BBANDS`."""
    ma_cache_dict = ma_cache_nb(close, windows, ewms, adjust)
    mstd_cache_dict = mstd_cache_nb(close, windows, ewms, adjust, ddof)
    return ma_cache_dict, mstd_cache_dict


@njit(cache=True)
def bb_apply_nb(close: tp.Array2d, window: int, ewm: bool, alpha: float,
                adjust: bool, ddof: int, ma_cache_dict: tp.Dict[int, tp.Array2d],
                mstd_cache_dict: tp.Dict[int, tp.Array2d]) -> tp.Tuple[tp.Array2d, tp.Array2d, tp.Array2d]:
    """Apply function for `vectorbt.indicators.basic.BBANDS`."""
    # Calculate lower, middle and upper bands
    h = hash((window, ewm))
    ma = np.copy(ma_cache_dict[h])
    mstd = np.copy(mstd_cache_dict[h])
    # # (MA + Kσ), MA, (MA - Kσ)
    return ma, ma + alpha * mstd, ma - alpha * mstd


@njit(cache=True)
def rsi_cache_nb(close: tp.Array2d, windows: tp.List[int], ewms: tp.List[bool],
                 adjust: bool) -> tp.Dict[int, tp.Tuple[tp.Array2d, tp.Array2d]]:
    """Caching function for `vectorbt.indicators.basic.RSI`."""
    delta = generic_nb.diff_nb(close)
    up, down = delta.copy(), delta.copy()
    up = generic_nb.set_by_mask_nb(up, up < 0, 0)
    down = np.abs(generic_nb.set_by_mask_nb(down, down > 0, 0))

    # Cache
    cache_dict = dict()
    for i in range(len(windows)):
        h = hash((windows[i], ewms[i]))
        if h not in cache_dict:
            roll_up = ma_nb(up, windows[i], ewms[i], adjust=adjust)
            roll_down = ma_nb(down, windows[i], ewms[i], adjust=adjust)
            cache_dict[h] = roll_up, roll_down
    return cache_dict


@njit(cache=True)
def rsi_apply_nb(close: tp.Array2d, window: int, ewm: bool, adjust: bool,
                 cache_dict: tp.Dict[int, tp.Tuple[tp.Array2d, tp.Array2d]]) -> tp.Array2d:
    """Apply function for `vectorbt.indicators.basic.RSI`."""
    h = hash((window, ewm))
    roll_up, roll_down = cache_dict[h]
    rs = roll_up / roll_down
    return 100 - 100 / (1 + rs)


@njit(cache=True)
def stoch_cache_nb(high: tp.Array2d, low: tp.Array2d, close: tp.Array2d,
                   k_windows: tp.List[int], d_windows: tp.List[int], d_ewms: tp.List[bool],
                   adjust: bool) -> tp.Dict[int, tp.Tuple[tp.Array2d, tp.Array2d]]:
    """Caching function for `vectorbt.indicators.basic.STOCH`."""
    cache_dict = dict()
    for i in range(len(k_windows)):
        h = hash(k_windows[i])
        if h not in cache_dict:
            roll_min = generic_nb.rolling_min_nb(low, k_windows[i])
            roll_max = generic_nb.rolling_max_nb(high, k_windows[i])
            cache_dict[h] = roll_min, roll_max
    return cache_dict


@njit(cache=True)
def stoch_apply_nb(high: tp.Array2d, low: tp.Array2d, close: tp.Array2d,
                   k_window: int, d_window: int, d_ewm: bool, adjust: bool,
                   cache_dict: tp.Dict[int, tp.Tuple[tp.Array2d, tp.Array2d]]) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Apply function for `vectorbt.indicators.basic.STOCH`."""
    h = hash(k_window)
    roll_min, roll_max = cache_dict[h]
    percent_k = 100 * (close - roll_min) / (roll_max - roll_min)
    percent_d = ma_nb(percent_k, d_window, d_ewm, adjust=adjust)
    return percent_k, percent_d


@njit(cache=True)
def macd_cache_nb(close: tp.Array2d, fast_windows: tp.List[int], slow_windows: tp.List[int],
                  signal_windows: tp.List[int], macd_ewms: tp.List[bool], signal_ewms: tp.List[bool],
                  adjust: bool) -> tp.Dict[int, tp.Array2d]:
    """Caching function for `vectorbt.indicators.basic.MACD`."""
    windows = fast_windows.copy()
    windows.extend(slow_windows)
    ewms = macd_ewms.copy()
    ewms.extend(macd_ewms)
    return ma_cache_nb(close, windows, ewms, adjust)


@njit(cache=True)
def macd_apply_nb(close: tp.Array2d, fast_window: int, slow_window: int,
                  signal_window: int, macd_ewm: bool, signal_ewm: bool, adjust: bool,
                  cache_dict: tp.Dict[int, tp.Array2d]) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Apply function for `vectorbt.indicators.basic.MACD`."""
    fast_h = hash((fast_window, macd_ewm))
    slow_h = hash((slow_window, macd_ewm))
    fast_ma = cache_dict[fast_h]
    slow_ma = cache_dict[slow_h]
    macd_ts = fast_ma - slow_ma
    signal_ts = ma_nb(macd_ts, signal_window, signal_ewm, adjust=adjust)
    return macd_ts, signal_ts


@njit(cache=True)
def true_range_nb(high: tp.Array2d, low: tp.Array2d, close: tp.Array2d) -> tp.Array2d:
    """Calculate true range."""
    prev_close = generic_nb.fshift_nb(close, 1)
    tr1 = high - low
    tr2 = np.abs(high - prev_close)
    tr3 = np.abs(low - prev_close)
    tr = np.empty(prev_close.shape, dtype=np.float64)
    for col in range(tr.shape[1]):
        for i in range(tr.shape[0]):
            tr[i, col] = max(tr1[i, col], tr2[i, col], tr3[i, col])
    return tr


@njit(cache=True)
def atr_cache_nb(high: tp.Array2d, low: tp.Array2d, close: tp.Array2d, windows: tp.List[int],
                 ewms: tp.List[bool], adjust: bool) -> tp.Tuple[tp.Array2d, tp.Dict[int, tp.Array2d]]:
    """Caching function for `vectorbt.indicators.basic.ATR`."""
    # Calculate TR here instead of re-calculating it for each param in atr_apply_nb
    tr = true_range_nb(high, low, close)
    cache_dict = dict()
    for i in range(len(windows)):
        h = hash((windows[i], ewms[i]))
        if h not in cache_dict:
            cache_dict[h] = ma_nb(tr, windows[i], ewms[i], adjust=adjust)
    return tr, cache_dict


@njit(cache=True)
def atr_apply_nb(high: tp.Array2d, low: tp.Array2d, close: tp.Array2d, window: int, ewm: bool, adjust: bool,
                 tr: tp.Array2d, cache_dict: tp.Dict[int, tp.Array2d]) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Apply function for `vectorbt.indicators.basic.ATR`."""
    h = hash((window, ewm))
    return tr, cache_dict[h]


@njit(cache=True)
def obv_custom_nb(close: tp.Array2d, volume_ts: tp.Array2d) -> tp.Array2d:
    """Custom calculation function for `vectorbt.indicators.basic.OBV`."""
    obv = generic_nb.set_by_mask_mult_nb(volume_ts, close < generic_nb.fshift_nb(close, 1), -volume_ts)
    obv = generic_nb.nancumsum_nb(obv)
    return obv
