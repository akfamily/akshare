# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Numba-compiled functions.

Provides an arsenal of Numba-compiled functions that are used by accessors
and in many other parts of the backtesting pipeline, such as technical indicators.
These only accept NumPy arrays and other Numba-compatible types.

The module can be accessed directly via `vbt.nb`.

```pycon
>>> import numpy as np
>>> import vectorbt as vbt

>>> # vectorbt.generic.nb.rolling_mean_1d_nb
>>> vbt.nb.rolling_mean_1d_nb(np.array([1, 2, 3, 4]), 2)
array([nan, 1.5, 2.5, 3.5])
```

!!! note
    vectorbt treats matrices as first-class citizens and expects input arrays to be
    2-dim, unless function has suffix `_1d` or is meant to be input to another function. 
    Data is processed along index (axis 0).
    
    Rolling functions with `minp=None` have `min_periods` set to the window size.
    
    All functions passed as argument should be Numba-compiled."""

import numpy as np
from numba import njit
from numba.extending import overload
from numba.core.types import Type, Omitted
from numba.np.numpy_support import as_dtype
from numba.typed import Dict

from vectorbt import _typing as tp
from vectorbt.generic.enums import RangeStatus, DrawdownStatus, range_dt, drawdown_dt


@njit(cache=True)
def shuffle_1d_nb(a: tp.Array1d, seed: tp.Optional[int] = None) -> tp.Array1d:
    """Shuffle each column in `a`.

    Specify `seed` to make output deterministic."""
    if seed is not None:
        np.random.seed(seed)
    return np.random.permutation(a)


@njit(cache=True)
def shuffle_nb(a: tp.Array2d, seed: tp.Optional[int] = None) -> tp.Array2d:
    """2-dim version of `shuffle_1d_nb`."""
    if seed is not None:
        np.random.seed(seed)
    out = np.empty_like(a, dtype=a.dtype)

    for col in range(a.shape[1]):
        out[:, col] = np.random.permutation(a[:, col])
    return out


def _set_by_mask_1d_nb(arr, mask, value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        value_dtype = as_dtype(value)
    else:
        a_dtype = arr.dtype
        value_dtype = np.array(value).dtype
    dtype = np.promote_types(a_dtype, value_dtype)

    def impl(arr, mask, value):
        out = arr.astype(dtype)
        out[mask] = value
        return out

    if not nb_enabled:
        return impl(arr, mask, value)

    return impl


def _set_by_mask_1d_nb(arr, mask, value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        value_dtype = as_dtype(value)
    else:
        a_dtype = arr.dtype
        value_dtype = np.array(value).dtype
    dtype = np.promote_types(a_dtype, value_dtype)

    def impl(arr, mask, value):
        out = arr.astype(dtype)
        out[mask] = value
        return out

    if not nb_enabled:
        return impl(arr, mask, value)

    return impl


ol_set_by_mask_1d_nb = overload(_set_by_mask_1d_nb)(_set_by_mask_1d_nb)


@njit(cache=True)
def set_by_mask_1d_nb(arr: tp.Array1d, mask: tp.Array1d, value: tp.Scalar) -> tp.Array1d:
    """Set each element to a value by boolean mask."""
    return _set_by_mask_1d_nb(arr, mask, value)


def _set_by_mask_nb(arr, mask, value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        value_dtype = as_dtype(value)
    else:
        a_dtype = arr.dtype
        value_dtype = np.array(value).dtype
    dtype = np.promote_types(a_dtype, value_dtype)

    def impl(arr, mask, value):
        out = arr.astype(dtype)
        for col in range(arr.shape[1]):
            out[mask[:, col], col] = value
        return out

    if not nb_enabled:
        return impl(arr, mask, value)

    return impl


ol_set_by_mask_nb = overload(_set_by_mask_nb)(_set_by_mask_nb)


@njit(cache=True)
def set_by_mask_nb(arr: tp.Array2d, mask: tp.Array2d, value: tp.Scalar) -> tp.Array2d:
    """2-dim version of `set_by_mask_1d_nb`."""
    return _set_by_mask_nb(arr, mask, value)


def _set_by_mask_mult_1d_nb(arr, mask, values):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        value_dtype = as_dtype(values.dtype)
    else:
        a_dtype = arr.dtype
        value_dtype = values.dtype
    dtype = np.promote_types(a_dtype, value_dtype)

    def impl(arr, mask, values):
        out = arr.astype(dtype)
        out[mask] = values[mask]
        return out

    if not nb_enabled:
        return impl(arr, mask, values)

    return impl


ol_set_by_mask_mult_1d_nb = overload(_set_by_mask_mult_1d_nb)(_set_by_mask_mult_1d_nb)


@njit(cache=True)
def set_by_mask_mult_1d_nb(arr: tp.Array1d, mask: tp.Array1d, values: tp.Array1d) -> tp.Array1d:
    """Set each element in one array to the corresponding element in another by boolean mask.

    `values` must be of the same shape as in the array."""
    return _set_by_mask_mult_1d_nb(arr, mask, values)


def _set_by_mask_mult_nb(arr, mask, values):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        value_dtype = as_dtype(values.dtype)
    else:
        a_dtype = arr.dtype
        value_dtype = values.dtype
    dtype = np.promote_types(a_dtype, value_dtype)

    def impl(arr, mask, values):
        out = arr.astype(dtype)
        for col in range(arr.shape[1]):
            out[mask[:, col], col] = values[mask[:, col], col]
        return out

    if not nb_enabled:
        return impl(arr, mask, values)

    return impl


ol_set_by_mask_mult_nb = overload(_set_by_mask_mult_nb)(_set_by_mask_mult_nb)


@njit(cache=True)
def set_by_mask_mult_nb(arr: tp.Array2d, mask: tp.Array2d, values: tp.Array2d) -> tp.Array2d:
    """2-dim version of `set_by_mask_mult_1d_nb`."""
    return _set_by_mask_mult_nb(arr, mask, values)


@njit(cache=True)
def fillna_1d_nb(a: tp.Array1d, value: tp.Scalar) -> tp.Array1d:
    """Replace NaNs with value.

    Numba equivalent to `pd.Series(a).fillna(value)`."""
    return set_by_mask_1d_nb(a, np.isnan(a), value)


@njit(cache=True)
def fillna_nb(a: tp.Array2d, value: tp.Scalar) -> tp.Array2d:
    """2-dim version of `fillna_1d_nb`."""
    return set_by_mask_nb(a, np.isnan(a), value)


def _bshift_1d_nb(arr, n, fill_value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        if isinstance(fill_value, Omitted):
            fill_value_dtype = np.asarray(fill_value.value).dtype
        else:
            fill_value_dtype = as_dtype(fill_value)
    else:
        a_dtype = arr.dtype
        fill_value_dtype = np.array(fill_value).dtype
    dtype = np.promote_types(a_dtype, fill_value_dtype)

    def impl(arr, n, fill_value):
        out = np.empty(arr.shape[0], dtype=dtype)
        for i in range(out.shape[0]):
            if i + n <= out.shape[0] - 1:
                out[i] = arr[i + n]
            else:
                out[i] = fill_value
        return out

    if not nb_enabled:
        return impl(arr, n, fill_value)

    return impl


ol_bshift_1d_nb = overload(_bshift_1d_nb)(_bshift_1d_nb)


@njit(cache=True)
def bshift_1d_nb(arr: tp.Array1d, n: int = 1, fill_value: tp.Scalar = np.nan) -> tp.Array1d:
    """Shift backward by `n` positions.

    Numba equivalent to `pd.Series(arr).shift(-n)`.

    !!! warning
        This operation looks ahead."""
    return _bshift_1d_nb(arr, n, fill_value)


def _bshift_nb(arr, n, fill_value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        if isinstance(fill_value, Omitted):
            fill_value_dtype = np.asarray(fill_value.value).dtype
        else:
            fill_value_dtype = as_dtype(fill_value)
    else:
        a_dtype = arr.dtype
        fill_value_dtype = np.array(fill_value).dtype
    dtype = np.promote_types(a_dtype, fill_value_dtype)

    def impl(arr, n, fill_value):
        out = np.empty_like(arr, dtype=dtype)
        for col in range(arr.shape[1]):
            out[:, col] = bshift_1d_nb(arr[:, col], n=n, fill_value=fill_value)
        return out

    if not nb_enabled:
        return impl(arr, n, fill_value)

    return impl


ol_bshift_nb = overload(_bshift_nb)(_bshift_nb)


@njit(cache=True)
def bshift_nb(arr: tp.Array2d, n: int = 1, fill_value: tp.Scalar = np.nan) -> tp.Array2d:
    """2-dim version of `bshift_1d_nb`."""
    return _bshift_nb(arr, n, fill_value)


def _fshift_1d_nb(arr, n, fill_value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        if isinstance(fill_value, Omitted):
            fill_value_dtype = np.asarray(fill_value.value).dtype
        else:
            fill_value_dtype = as_dtype(fill_value)
    else:
        a_dtype = arr.dtype
        fill_value_dtype = np.array(fill_value).dtype
    dtype = np.promote_types(a_dtype, fill_value_dtype)

    def impl(arr, n, fill_value):
        out = np.empty(arr.shape[0], dtype=dtype)
        for i in range(out.shape[0]):
            if i - n >= 0:
                out[i] = arr[i - n]
            else:
                out[i] = fill_value
        return out

    if not nb_enabled:
        return impl(arr, n, fill_value)

    return impl


ol_fshift_1d_nb = overload(_fshift_1d_nb)(_fshift_1d_nb)


@njit(cache=True)
def fshift_1d_nb(arr: tp.Array1d, n: int = 1, fill_value: tp.Scalar = np.nan) -> tp.Array1d:
    """Shift forward by `n` positions.

    Numba equivalent to `pd.Series(arr).shift(n)`."""
    return _fshift_1d_nb(arr, n, fill_value)


def _fshift_nb(arr, n, fill_value):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
        if isinstance(fill_value, Omitted):
            fill_value_dtype = np.asarray(fill_value.value).dtype
        else:
            fill_value_dtype = as_dtype(fill_value)
    else:
        a_dtype = arr.dtype
        fill_value_dtype = np.array(fill_value).dtype
    dtype = np.promote_types(a_dtype, fill_value_dtype)

    def impl(arr, n, fill_value):
        out = np.empty_like(arr, dtype=dtype)
        for col in range(arr.shape[1]):
            out[:, col] = fshift_1d_nb(arr[:, col], n=n, fill_value=fill_value)
        return out

    if not nb_enabled:
        return impl(arr, n, fill_value)

    return impl


ol_fshift_nb = overload(_fshift_nb)(_fshift_nb)


@njit(cache=True)
def fshift_nb(arr: tp.Array2d, n: int = 1, fill_value: tp.Scalar = np.nan) -> tp.Array2d:
    """2-dim version of `fshift_1d_nb`."""
    return _fshift_nb(arr, n, fill_value)


@njit(cache=True)
def diff_1d_nb(a: tp.Array1d, n: int = 1) -> tp.Array1d:
    """Return the 1-th discrete difference.

    Numba equivalent to `pd.Series(a).diff()`."""
    out = np.empty_like(a, dtype=np.float64)
    out[:n] = np.nan
    out[n:] = a[n:] - a[:-n]
    return out


@njit(cache=True)
def diff_nb(a: tp.Array2d, n: int = 1) -> tp.Array2d:
    """2-dim version of `diff_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = diff_1d_nb(a[:, col], n=n)
    return out


@njit(cache=True)
def pct_change_1d_nb(a: tp.Array1d, n: int = 1) -> tp.Array1d:
    """Return the percentage change.

    Numba equivalent to `pd.Series(a).pct_change()`."""
    out = np.empty_like(a, dtype=np.float64)
    out[:n] = np.nan
    out[n:] = a[n:] / a[:-n] - 1
    return out


@njit(cache=True)
def pct_change_nb(a: tp.Array2d, n: int = 1) -> tp.Array2d:
    """2-dim version of `pct_change_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = pct_change_1d_nb(a[:, col], n=n)
    return out


@njit(cache=True)
def bfill_1d_nb(a: tp.Array1d) -> tp.Array1d:
    """Fill NaNs by propagating first valid observation backward.

    Numba equivalent to `pd.Series(a).fillna(method='bfill')`.

    !!! warning
        This operation looks ahead."""
    out = np.empty_like(a, dtype=a.dtype)
    lastval = a[-1]
    for i in range(a.shape[0] - 1, -1, -1):
        if np.isnan(a[i]):
            out[i] = lastval
        else:
            lastval = out[i] = a[i]
    return out


@njit(cache=True)
def bfill_nb(a: tp.Array2d) -> tp.Array2d:
    """2-dim version of `bfill_1d_nb`."""
    out = np.empty_like(a, dtype=a.dtype)
    for col in range(a.shape[1]):
        out[:, col] = bfill_1d_nb(a[:, col])
    return out


@njit(cache=True)
def ffill_1d_nb(a: tp.Array1d) -> tp.Array1d:
    """Fill NaNs by propagating last valid observation forward.

    Numba equivalent to `pd.Series(a).fillna(method='ffill')`."""
    out = np.empty_like(a, dtype=a.dtype)
    lastval = a[0]
    for i in range(a.shape[0]):
        if np.isnan(a[i]):
            out[i] = lastval
        else:
            lastval = out[i] = a[i]
    return out


@njit(cache=True)
def ffill_nb(a: tp.Array2d) -> tp.Array2d:
    """2-dim version of `ffill_1d_nb`."""
    out = np.empty_like(a, dtype=a.dtype)
    for col in range(a.shape[1]):
        out[:, col] = ffill_1d_nb(a[:, col])
    return out


def _nanprod_nb(arr):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
    else:
        a_dtype = arr.dtype
    dtype = np.promote_types(a_dtype, int)

    def impl(arr):
        out = np.empty(arr.shape[1], dtype=dtype)
        for col in range(arr.shape[1]):
            out[col] = np.nanprod(arr[:, col])
        return out

    if not nb_enabled:
        return impl(arr)

    return impl


ol_nanprod_nb = overload(_nanprod_nb)(_nanprod_nb)


@njit(cache=True)
def nanprod_nb(arr: tp.Array2d) -> tp.Array1d:
    """Numba equivalent of `np.nanprod` along axis 0."""
    return _nanprod_nb(arr)


def _nancumsum_nb(arr):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
    else:
        a_dtype = arr.dtype
    dtype = np.promote_types(a_dtype, int)

    def impl(arr):
        out = np.empty(arr.shape, dtype=dtype)
        for col in range(arr.shape[1]):
            out[:, col] = np.nancumsum(arr[:, col])
        return out

    if not nb_enabled:
        return impl(arr)

    return impl


ol_nancumsum_nb = overload(_nancumsum_nb)(_nancumsum_nb)


@njit(cache=True)
def nancumsum_nb(arr: tp.Array2d) -> tp.Array2d:
    """Numba equivalent of `np.nancumsum` along axis 0."""
    return _nancumsum_nb(arr)


def _nancumprod_nb(arr):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
    else:
        a_dtype = arr.dtype
    dtype = np.promote_types(a_dtype, int)

    def impl(arr):
        out = np.empty(arr.shape, dtype=dtype)
        for col in range(arr.shape[1]):
            out[:, col] = np.nancumprod(arr[:, col])
        return out

    if not nb_enabled:
        return impl(arr)

    return impl


ol_nancumprod_nb = overload(_nancumprod_nb)(_nancumprod_nb)


@njit(cache=True)
def nancumprod_nb(arr: tp.Array2d) -> tp.Array2d:
    """Numba equivalent of `np.nancumprod` along axis 0."""
    return _nancumprod_nb(arr)


def _nansum_nb(arr):
    nb_enabled = isinstance(arr, Type)
    if nb_enabled:
        a_dtype = as_dtype(arr.dtype)
    else:
        a_dtype = arr.dtype
    dtype = np.promote_types(a_dtype, int)

    def impl(arr):
        out = np.empty(arr.shape[1], dtype=dtype)
        for col in range(arr.shape[1]):
            out[col] = np.nansum(arr[:, col])
        return out

    if not nb_enabled:
        return impl(arr)

    return impl


ol_nansum_nb = overload(_nansum_nb)(_nansum_nb)


@njit(cache=True)
def nansum_nb(arr: tp.Array2d) -> tp.Array1d:
    """Numba equivalent of `np.nansum` along axis 0."""
    return _nansum_nb(arr)


@njit(cache=True)
def nancnt_nb(a: tp.Array2d) -> tp.Array1d:
    """Compute count while ignoring NaNs."""
    out = np.empty(a.shape[1], dtype=np.int64)
    for col in range(a.shape[1]):
        out[col] = np.sum(~np.isnan(a[:, col]))
    return out


@njit(cache=True)
def nanmin_nb(a: tp.Array2d) -> tp.Array1d:
    """Numba-equivalent of `np.nanmin` along axis 0."""
    out = np.empty(a.shape[1], dtype=a.dtype)
    for col in range(a.shape[1]):
        out[col] = np.nanmin(a[:, col])
    return out


@njit(cache=True)
def nanmax_nb(a: tp.Array2d) -> tp.Array1d:
    """Numba-equivalent of `np.nanmax` along axis 0."""
    out = np.empty(a.shape[1], dtype=a.dtype)
    for col in range(a.shape[1]):
        out[col] = np.nanmax(a[:, col])
    return out


@njit(cache=True)
def nanmean_nb(a: tp.Array2d) -> tp.Array1d:
    """Numba-equivalent of `np.nanmean` along axis 0."""
    out = np.empty(a.shape[1], dtype=np.float64)
    for col in range(a.shape[1]):
        out[col] = np.nanmean(a[:, col])
    return out


@njit(cache=True)
def nanmedian_nb(a: tp.Array2d) -> tp.Array1d:
    """Numba-equivalent of `np.nanmedian` along axis 0."""
    out = np.empty(a.shape[1], dtype=np.float64)
    for col in range(a.shape[1]):
        out[col] = np.nanmedian(a[:, col])
    return out


@njit(cache=True)
def nanstd_1d_nb(a: tp.Array1d, ddof: int = 0) -> float:
    """Numba-equivalent of `np.nanstd`."""
    cnt = a.shape[0] - np.count_nonzero(np.isnan(a))
    rcount = max(cnt - ddof, 0)
    if rcount == 0:
        return np.nan
    return np.sqrt(np.nanvar(a) * cnt / rcount)


@njit(cache=True)
def nanstd_nb(a: tp.Array2d, ddof: int = 0) -> tp.Array1d:
    """2-dim version of `nanstd_1d_nb`."""
    out = np.empty(a.shape[1], dtype=np.float64)
    for col in range(a.shape[1]):
        out[col] = nanstd_1d_nb(a[:, col], ddof=ddof)
    return out


# ############# Rolling functions ############# #


@njit(cache=True)
def rolling_min_1d_nb(a: tp.Array1d, window: int, minp: tp.Optional[int] = None) -> tp.Array1d:
    """Return rolling min.

    Numba equivalent to `pd.Series(a).rolling(window, min_periods=minp).min()`."""
    if minp is None:
        minp = window
    if minp > window:
        raise ValueError("minp must be <= window")
    out = np.empty_like(a, dtype=np.float64)
    for i in range(a.shape[0]):
        minv = a[i]
        cnt = 0
        for j in range(max(i - window + 1, 0), i + 1):
            if np.isnan(a[j]):
                continue
            if np.isnan(minv) or a[j] < minv:
                minv = a[j]
            cnt += 1
        if cnt < minp:
            out[i] = np.nan
        else:
            out[i] = minv
    return out


@njit(cache=True)
def rolling_min_nb(a: tp.Array2d, window: int, minp: tp.Optional[int] = None) -> tp.Array2d:
    """2-dim version of `rolling_min_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = rolling_min_1d_nb(a[:, col], window, minp=minp)
    return out


@njit(cache=True)
def rolling_max_1d_nb(a: tp.Array1d, window: int, minp: tp.Optional[int] = None) -> tp.Array1d:
    """Return rolling max.

    Numba equivalent to `pd.Series(a).rolling(window, min_periods=minp).max()`."""
    if minp is None:
        minp = window
    if minp > window:
        raise ValueError("minp must be <= window")
    out = np.empty_like(a, dtype=np.float64)
    for i in range(a.shape[0]):
        maxv = a[i]
        cnt = 0
        for j in range(max(i - window + 1, 0), i + 1):
            if np.isnan(a[j]):
                continue
            if np.isnan(maxv) or a[j] > maxv:
                maxv = a[j]
            cnt += 1
        if cnt < minp:
            out[i] = np.nan
        else:
            out[i] = maxv
    return out


@njit(cache=True)
def rolling_max_nb(a: tp.Array2d, window: int, minp: tp.Optional[int] = None) -> tp.Array2d:
    """2-dim version of `rolling_max_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = rolling_max_1d_nb(a[:, col], window, minp=minp)
    return out


@njit(cache=True)
def rolling_mean_1d_nb(a: tp.Array1d, window: int, minp: tp.Optional[int] = None) -> tp.Array1d:
    """Return rolling mean.

    Numba equivalent to `pd.Series(a).rolling(window, min_periods=minp).mean()`."""
    if minp is None:
        minp = window
    if minp > window:
        raise ValueError("minp must be <= window")
    out = np.empty_like(a, dtype=np.float64)
    cumsum_arr = np.zeros_like(a)
    cumsum = 0
    nancnt_arr = np.zeros_like(a)
    nancnt = 0
    for i in range(a.shape[0]):
        if np.isnan(a[i]):
            nancnt = nancnt + 1
        else:
            cumsum = cumsum + a[i]
        nancnt_arr[i] = nancnt
        cumsum_arr[i] = cumsum
        if i < window:
            window_len = i + 1 - nancnt
            window_cumsum = cumsum
        else:
            window_len = window - (nancnt - nancnt_arr[i - window])
            window_cumsum = cumsum - cumsum_arr[i - window]
        if window_len < minp:
            out[i] = np.nan
        else:
            out[i] = window_cumsum / window_len
    return out


@njit(cache=True)
def rolling_mean_nb(a: tp.Array2d, window: int, minp: tp.Optional[int] = None) -> tp.Array2d:
    """2-dim version of `rolling_mean_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = rolling_mean_1d_nb(a[:, col], window, minp=minp)
    return out


@njit(cache=True)
def rolling_std_1d_nb(a: tp.Array1d, window: int, minp: tp.Optional[int] = None, ddof: int = 0) -> tp.Array1d:
    """Return rolling standard deviation.

    Numba equivalent to `pd.Series(a).rolling(window, min_periods=minp).std(ddof=ddof)`."""
    if minp is None:
        minp = window
    if minp > window:
        raise ValueError("minp must be <= window")
    out = np.empty_like(a, dtype=np.float64)
    cumsum_arr = np.zeros_like(a)
    cumsum = 0
    cumsum_sq_arr = np.zeros_like(a)
    cumsum_sq = 0
    nancnt_arr = np.zeros_like(a)
    nancnt = 0
    for i in range(a.shape[0]):
        if np.isnan(a[i]):
            nancnt = nancnt + 1
        else:
            cumsum = cumsum + a[i]
            cumsum_sq = cumsum_sq + a[i] ** 2
        nancnt_arr[i] = nancnt
        cumsum_arr[i] = cumsum
        cumsum_sq_arr[i] = cumsum_sq
        if i < window:
            window_len = i + 1 - nancnt
            window_cumsum = cumsum
            window_cumsum_sq = cumsum_sq
        else:
            window_len = window - (nancnt - nancnt_arr[i - window])
            window_cumsum = cumsum - cumsum_arr[i - window]
            window_cumsum_sq = cumsum_sq - cumsum_sq_arr[i - window]
        if window_len < minp or window_len == ddof:
            out[i] = np.nan
        else:
            mean = window_cumsum / window_len
            out[i] = np.sqrt(np.abs(window_cumsum_sq - 2 * window_cumsum *
                                    mean + window_len * mean ** 2) / (window_len - ddof))
    return out


@njit(cache=True)
def rolling_std_nb(a: tp.Array2d, window: int, minp: tp.Optional[int] = None, ddof: int = 0) -> tp.Array2d:
    """2-dim version of `rolling_std_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = rolling_std_1d_nb(a[:, col], window, minp=minp, ddof=ddof)
    return out


@njit(cache=True)
def ewm_mean_1d_nb(a: tp.Array1d, span: int, minp: int = 0, adjust: bool = False) -> tp.Array1d:
    """Return exponential weighted average.

    Numba equivalent to `pd.Series(a).ewm(span=span, min_periods=minp, adjust=adjust).mean()`.

    Adaptation of `pd._libs.window.aggregations.window_aggregations.ewma` with default arguments."""
    if minp is None:
        minp = span
    if minp > span:
        raise ValueError("minp must be <= span")
    N = len(a)
    out = np.empty(N, dtype=np.float64)
    if N == 0:
        return out
    com = (span - 1) / 2.0
    alpha = 1. / (1. + com)
    old_wt_factor = 1. - alpha
    new_wt = 1. if adjust else alpha
    weighted_avg = a[0]
    is_observation = (weighted_avg == weighted_avg)
    nobs = int(is_observation)
    out[0] = weighted_avg if (nobs >= minp) else np.nan
    old_wt = 1.

    for i in range(1, N):
        cur = a[i]
        is_observation = (cur == cur)
        nobs += is_observation
        if weighted_avg == weighted_avg:
            old_wt *= old_wt_factor
            if is_observation:
                # avoid numerical errors on constant series
                if weighted_avg != cur:
                    weighted_avg = ((old_wt * weighted_avg) + (new_wt * cur)) / (old_wt + new_wt)
                if adjust:
                    old_wt += new_wt
                else:
                    old_wt = 1.
        elif is_observation:
            weighted_avg = cur
        out[i] = weighted_avg if (nobs >= minp) else np.nan
    return out


@njit(cache=True)
def ewm_mean_nb(a: tp.Array2d, span: int, minp: int = 0, adjust: bool = False) -> tp.Array2d:
    """2-dim version of `ewm_mean_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = ewm_mean_1d_nb(a[:, col], span, minp=minp, adjust=adjust)
    return out


@njit(cache=True)
def ewm_std_1d_nb(a: tp.Array1d, span: int, minp: int = 0, adjust: bool = False, ddof: int = 0) -> tp.Array1d:
    """Return exponential weighted standard deviation.

    Numba equivalent to `pd.Series(a).ewm(span=span, min_periods=minp).std(ddof=ddof)`.

    Adaptation of `pd._libs.window.aggregations.window_aggregations.ewmcov` with default arguments."""
    if minp is None:
        minp = span
    if minp > span:
        raise ValueError("minp must be <= span")
    N = len(a)
    out = np.empty(N, dtype=np.float64)
    if N == 0:
        return out
    com = (span - 1) / 2.0
    alpha = 1. / (1. + com)
    old_wt_factor = 1. - alpha
    new_wt = 1. if adjust else alpha
    mean_x = a[0]
    mean_y = a[0]
    is_observation = ((mean_x == mean_x) and (mean_y == mean_y))
    nobs = int(is_observation)
    if not is_observation:
        mean_x = np.nan
        mean_y = np.nan
    out[0] = np.nan
    cov = 0.
    sum_wt = 1.
    sum_wt2 = 1.
    old_wt = 1.

    for i in range(1, N):
        cur_x = a[i]
        cur_y = a[i]
        is_observation = ((cur_x == cur_x) and (cur_y == cur_y))
        nobs += is_observation
        if mean_x == mean_x:
            sum_wt *= old_wt_factor
            sum_wt2 *= (old_wt_factor * old_wt_factor)
            old_wt *= old_wt_factor
            if is_observation:
                old_mean_x = mean_x
                old_mean_y = mean_y

                # avoid numerical errors on constant series
                if mean_x != cur_x:
                    mean_x = ((old_wt * old_mean_x) +
                              (new_wt * cur_x)) / (old_wt + new_wt)

                # avoid numerical errors on constant series
                if mean_y != cur_y:
                    mean_y = ((old_wt * old_mean_y) +
                              (new_wt * cur_y)) / (old_wt + new_wt)
                cov = ((old_wt * (cov + ((old_mean_x - mean_x) *
                                         (old_mean_y - mean_y)))) +
                       (new_wt * ((cur_x - mean_x) *
                                  (cur_y - mean_y)))) / (old_wt + new_wt)
                sum_wt += new_wt
                sum_wt2 += (new_wt * new_wt)
                old_wt += new_wt
                if not adjust:
                    sum_wt /= old_wt
                    sum_wt2 /= (old_wt * old_wt)
                    old_wt = 1.
        elif is_observation:
            mean_x = cur_x
            mean_y = cur_y

        if nobs >= minp:
            numerator = sum_wt * sum_wt
            denominator = numerator - sum_wt2
            if denominator > 0.:
                out[i] = ((numerator / denominator) * cov)
            else:
                out[i] = np.nan
        else:
            out[i] = np.nan
    return np.sqrt(out)


@njit(cache=True)
def ewm_std_nb(a: tp.Array2d, span: int, minp: int = 0, adjust: bool = False, ddof: int = 0) -> tp.Array2d:
    """2-dim version of `ewm_std_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = ewm_std_1d_nb(a[:, col], span, minp=minp, adjust=adjust, ddof=ddof)
    return out


# ############# Expanding functions ############# #


@njit(cache=True)
def expanding_min_1d_nb(a: tp.Array1d, minp: int = 1) -> tp.Array1d:
    """Return expanding min.

    Numba equivalent to `pd.Series(a).expanding(min_periods=minp).min()`."""
    out = np.empty_like(a, dtype=np.float64)
    minv = a[0]
    cnt = 0
    for i in range(a.shape[0]):
        if np.isnan(minv) or a[i] < minv:
            minv = a[i]
        if not np.isnan(a[i]):
            cnt += 1
        if cnt < minp:
            out[i] = np.nan
        else:
            out[i] = minv
    return out


@njit(cache=True)
def expanding_min_nb(a: tp.Array2d, minp: int = 1) -> tp.Array2d:
    """2-dim version of `expanding_min_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = expanding_min_1d_nb(a[:, col], minp=minp)
    return out


@njit(cache=True)
def expanding_max_1d_nb(a: tp.Array1d, minp: int = 1) -> tp.Array1d:
    """Return expanding max.

    Numba equivalent to `pd.Series(a).expanding(min_periods=minp).max()`."""
    out = np.empty_like(a, dtype=np.float64)
    maxv = a[0]
    cnt = 0
    for i in range(a.shape[0]):
        if np.isnan(maxv) or a[i] > maxv:
            maxv = a[i]
        if not np.isnan(a[i]):
            cnt += 1
        if cnt < minp:
            out[i] = np.nan
        else:
            out[i] = maxv
    return out


@njit(cache=True)
def expanding_max_nb(a: tp.Array2d, minp: int = 1) -> tp.Array2d:
    """2-dim version of `expanding_max_1d_nb`."""
    out = np.empty_like(a, dtype=np.float64)
    for col in range(a.shape[1]):
        out[:, col] = expanding_max_1d_nb(a[:, col], minp=minp)
    return out


@njit(cache=True)
def expanding_mean_1d_nb(a: tp.Array1d, minp: int = 1) -> tp.Array1d:
    """Return expanding mean.

    Numba equivalent to `pd.Series(a).expanding(min_periods=minp).mean()`."""
    return rolling_mean_1d_nb(a, a.shape[0], minp=minp)


@njit(cache=True)
def expanding_mean_nb(a: tp.Array2d, minp: int = 1) -> tp.Array2d:
    """2-dim version of `expanding_mean_1d_nb`."""
    return rolling_mean_nb(a, a.shape[0], minp=minp)


@njit(cache=True)
def expanding_std_1d_nb(a: tp.Array1d, minp: int = 1, ddof: int = 0) -> tp.Array1d:
    """Return expanding standard deviation.

    Numba equivalent to `pd.Series(a).expanding(min_periods=minp).std(ddof=ddof)`."""
    return rolling_std_1d_nb(a, a.shape[0], minp=minp, ddof=ddof)


@njit(cache=True)
def expanding_std_nb(a: tp.Array2d, minp: int = 1, ddof: int = 0) -> tp.Array2d:
    """2-dim version of `expanding_std_1d_nb`."""
    return rolling_std_nb(a, a.shape[0], minp=minp, ddof=ddof)


# ############# Apply functions ############# #


@njit
def apply_nb(a: tp.Array2d, apply_func_nb: tp.ApplyFunc, *args) -> tp.Array2d:
    """Apply function on each column.

    `apply_func_nb` should accept index of the column, the array, and `*args`.
    Should return a single value or an array of shape `a.shape[1]`."""
    for col in range(a.shape[1]):
        _out = apply_func_nb(col, a[:, col], *args)
        if col == 0:
            out = np.empty_like(a, dtype=np.asarray(_out).dtype)
        out[:, col] = _out
    return out


@njit
def row_apply_nb(a: tp.Array2d, apply_func_nb: tp.RowApplyFunc, *args) -> tp.Array2d:
    """Apply function on each row.

    `apply_func_nb` should accept index of the row, the array, and `*args`.
    Should return a single value or an array of shape `a.shape[1]`."""
    for i in range(a.shape[0]):
        _out = apply_func_nb(i, a[i, :], *args)
        if i == 0:
            out = np.empty_like(a, dtype=np.asarray(_out).dtype)
        out[i, :] = _out
    return out


@njit
def rolling_apply_nb(a: tp.Array2d, window: int, minp: tp.Optional[int],
                     apply_func_nb: tp.RollApplyFunc, *args) -> tp.Array2d:
    """Provide rolling window calculations.

    `apply_func_nb` should accept index of the row, index of the column,
    the array, and `*args`. Should return a single value."""
    if minp is None:
        minp = window
    out = np.empty_like(a, dtype=np.float64)
    nancnt_arr = np.empty((a.shape[0],), dtype=np.int64)
    for col in range(a.shape[1]):
        nancnt = 0
        for i in range(a.shape[0]):
            if np.isnan(a[i, col]):
                nancnt = nancnt + 1
            nancnt_arr[i] = nancnt
            if i < window:
                valid_cnt = i + 1 - nancnt
            else:
                valid_cnt = window - (nancnt - nancnt_arr[i - window])
            if valid_cnt < minp:
                out[i, col] = np.nan
            else:
                window_a = a[max(0, i + 1 - window):i + 1, col]
                out[i, col] = apply_func_nb(i, col, window_a, *args)
    return out


@njit
def rolling_matrix_apply_nb(a: tp.Array2d, window: int, minp: tp.Optional[int],
                            apply_func_nb: tp.RollMatrixApplyFunc, *args) -> tp.Array2d:
    """`rolling_apply_nb` with `apply_func_nb` being applied on all columns at once.

    `apply_func_nb` should accept index of the row, the 2-dim array, and `*args`.
    Should return a single value or an array of shape `a.shape[1]`."""
    if minp is None:
        minp = window
    out = np.empty_like(a, dtype=np.float64)
    nancnt_arr = np.empty((a.shape[0],), dtype=np.int64)
    for i in range(a.shape[0]):
        nancnt = 0
        for col in range(a.shape[1]):
            if np.isnan(a[i, col]):
                nancnt = nancnt + 1
        nancnt_arr[i] = nancnt
        if i < window:
            valid_cnt = i + 1 - nancnt
        else:
            valid_cnt = window - (nancnt - nancnt_arr[i - window])
        if valid_cnt < minp:
            out[i, :] = np.nan
        else:
            window_a = a[max(0, i + 1 - window):i + 1, :]
            out[i, :] = apply_func_nb(i, window_a, *args)
    return out


@njit
def expanding_apply_nb(a: tp.Array2d, minp: tp.Optional[int],
                       apply_func_nb: tp.RollApplyFunc, *args) -> tp.Array2d:
    """Expanding version of `rolling_apply_nb`."""
    return rolling_apply_nb(a, a.shape[0], minp, apply_func_nb, *args)


@njit
def expanding_matrix_apply_nb(a: tp.Array2d, minp: tp.Optional[int],
                              apply_func_nb: tp.RollMatrixApplyFunc, *args) -> tp.Array2d:
    """Expanding version of `rolling_matrix_apply_nb`."""
    return rolling_matrix_apply_nb(a, a.shape[0], minp, apply_func_nb, *args)


@njit
def groupby_apply_nb(a: tp.Array2d, groups: Dict,
                     apply_func_nb: tp.GroupByApplyFunc, *args) -> tp.Array2d:
    """Provide group-by calculations.

    `groups` should be a dictionary, where each key is an index that points to an element in the new array
    where a group-by result will be stored, while the value should be an array of indices in `a`
    to apply `apply_func_nb` on.

    `apply_func_nb` should accept indices of the group, index of the column,
    the array, and `*args`. Should return a single value."""
    for col in range(a.shape[1]):
        for g, (i, idxs) in enumerate(groups.items()):
            _out = apply_func_nb(idxs, col, a[idxs, col], *args)
            if col == 0 and g == 0:
                out = np.empty((len(groups), a.shape[1]), dtype=np.asarray(_out).dtype)
            out[i, col] = _out
    return out


@njit
def groupby_matrix_apply_nb(a: tp.Array2d, groups: Dict,
                            apply_func_nb: tp.GroupByMatrixApplyFunc, *args) -> tp.Array2d:
    """`groupby_apply_nb` with `apply_func_nb` being applied on all columns at once.

    `apply_func_nb` should accept indices of the group, the 2-dim array, and `*args`.
    Should return a single value or an array of shape `a.shape[1]`."""
    for g, (i, idxs) in enumerate(groups.items()):
        _out = apply_func_nb(idxs, a[idxs, :], *args)
        if g == 0:
            out = np.empty((len(groups), a.shape[1]), dtype=np.asarray(_out).dtype)
        out[i, :] = _out
    return out


# ############# Map, filter and reduce ############# #


@njit
def applymap_nb(a: tp.Array2d, map_func_nb: tp.ApplyMapFunc, *args) -> tp.Array2d:
    """Map non-NA elements element-wise using `map_func_nb`.

    `map_func_nb` should accept index of the row, index of the column,
    the element itself, and `*args`. Should return a single value."""
    out = np.full_like(a, np.nan, dtype=np.float64)

    for col in range(out.shape[1]):
        idxs = np.flatnonzero(~np.isnan(a[:, col]))
        for i in idxs:
            out[i, col] = map_func_nb(i, col, a[i, col], *args)
    return out


@njit
def filter_nb(a: tp.Array2d, filter_func_nb: tp.FilterFunc, *args) -> tp.Array2d:
    """Filter non-NA elements elementwise using `filter_func_nb`. 
    The filtered out elements will become NA.

    `filter_func_nb` should accept index of the row, index of the column,
    the element itself, and `*args`. Should return a bool."""
    out = a.astype(np.float64)

    for col in range(out.shape[1]):
        idxs = np.flatnonzero(~np.isnan(a[:, col]))
        for i in idxs:
            if not filter_func_nb(i, col, a[i, col], *args):
                out[i, col] = np.nan
    return out


@njit
def apply_and_reduce_nb(a: tp.Array2d, apply_func_nb: tp.ApplyFunc, apply_args: tuple,
                        reduce_func_nb: tp.ReduceFunc, reduce_args: tuple) -> tp.Array1d:
    """Apply `apply_func_nb` on each column and reduce into a single value using `reduce_func_nb`.

    `apply_func_nb` should accept index of the column, the column itself, and `*apply_args`.
    Should return an array.

    `reduce_func_nb` should accept index of the column, the array of results from
    `apply_func_nb` for that column, and `*reduce_args`. Should return a single value."""
    for col in range(a.shape[1]):
        mapped = apply_func_nb(col, a[:, col], *apply_args)
        _out = reduce_func_nb(col, mapped, *reduce_args)
        if col == 0:
            out = np.empty(a.shape[1], dtype=np.asarray(_out).dtype)
        out[col] = _out
    return out


@njit
def reduce_nb(a: tp.Array2d, reduce_func_nb: tp.ReduceFunc, *args) -> tp.Array1d:
    """Reduce each column into a single value using `reduce_func_nb`.

    `reduce_func_nb` should accept index of the column, the array, and `*args`.
    Should return a single value."""
    for col in range(a.shape[1]):
        _out = reduce_func_nb(col, a[:, col], *args)
        if col == 0:
            out = np.empty(a.shape[1], dtype=np.asarray(_out).dtype)
        out[col] = _out
    return out


@njit
def reduce_to_array_nb(a: tp.Array2d, reduce_func_nb: tp.ReduceArrayFunc, *args) -> tp.Array2d:
    """Reduce each column into an array of values using `reduce_func_nb`.

    `reduce_func_nb` same as for `reduce_nb` but should return an array.

    !!! note
        Output of `reduce_func_nb` should be strictly homogeneous."""
    for col in range(a.shape[1]):
        _out = reduce_func_nb(col, a[:, col], *args)
        if col == 0:
            out = np.empty((_out.shape[0], a.shape[1]), dtype=_out.dtype)
        out[:, col] = _out
    return out


@njit
def reduce_grouped_nb(a: tp.Array2d, group_lens: tp.Array1d,
                      reduce_func_nb: tp.GroupReduceFunc, *args) -> tp.Array1d:
    """Reduce each group of columns into a single value using `reduce_func_nb`.

    `reduce_func_nb` should accept index of the group, the array of row values, and `*args`.
    Should return a single value."""
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        _out = reduce_func_nb(group, a[:, from_col:to_col], *args)
        if group == 0:
            out = np.empty(len(group_lens), dtype=np.asarray(_out).dtype)
        out[group] = _out
        from_col = to_col
    return out


@njit(cache=True)
def flatten_forder_nb(a: tp.Array2d) -> tp.Array1d:
    """Flatten `a` in F order."""
    out = np.empty(a.shape[0] * a.shape[1], dtype=a.dtype)
    for col in range(a.shape[1]):
        out[col * a.shape[0]:(col + 1) * a.shape[0]] = a[:, col]
    return out


@njit
def flat_reduce_grouped_nb(a: tp.Array2d, group_lens: tp.Array1d, in_c_order: bool,
                           reduce_func_nb: tp.FlatGroupReduceFunc, *args) -> tp.Array1d:
    """Same as `reduce_grouped_nb` but passes flattened array."""
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        if in_c_order:
            _out = reduce_func_nb(group, a[:, from_col:to_col].flatten(), *args)
        else:
            _out = reduce_func_nb(group, flatten_forder_nb(a[:, from_col:to_col]), *args)
        if group == 0:
            out = np.empty(len(group_lens), dtype=np.asarray(_out).dtype)
        out[group] = _out
        from_col = to_col
    return out


@njit
def reduce_grouped_to_array_nb(a: tp.Array2d, group_lens: tp.Array1d,
                               reduce_func_nb: tp.GroupReduceArrayFunc, *args) -> tp.Array2d:
    """Reduce each group of columns into an array of values using `reduce_func_nb`.

    `reduce_func_nb` same as for `reduce_grouped_nb` but should return an array.

    !!! note
        Output of `reduce_func_nb` should be strictly homogeneous."""
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        _out = reduce_func_nb(group, a[:, from_col:to_col], *args)
        if group == 0:
            out = np.empty((_out.shape[0], len(group_lens)), dtype=_out.dtype)
        out[:, group] = _out
        from_col = to_col
    return out


@njit
def flat_reduce_grouped_to_array_nb(a: tp.Array2d, group_lens: tp.Array1d, in_c_order: bool,
                                    reduce_func_nb: tp.FlatGroupReduceArrayFunc, *args) -> tp.Array2d:
    """Same as `reduce_grouped_to_array_nb` but passes flattened 1D array."""
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        if in_c_order:
            _out = reduce_func_nb(group, a[:, from_col:to_col].flatten(), *args)
        else:
            _out = reduce_func_nb(group, flatten_forder_nb(a[:, from_col:to_col]), *args)
        if group == 0:
            out = np.full((_out.shape[0], len(group_lens)), np.nan, dtype=_out.dtype)
        out[:, group] = _out
        from_col = to_col
    return out


@njit
def squeeze_grouped_nb(a: tp.Array2d, group_lens: tp.Array1d,
                       squeeze_func_nb: tp.GroupSqueezeFunc, *args) -> tp.Array2d:
    """Squeeze each group of columns into a single column using `squeeze_func_nb`.

    `squeeze_func_nb` should accept index of the row, index of the group,
    the array, and `*args`. Should return a single value."""
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        for i in range(a.shape[0]):
            _out = squeeze_func_nb(i, group, a[i, from_col:to_col], *args)
            if group == 0 and i == 0:
                out = np.empty((a.shape[0], len(group_lens)), dtype=np.asarray(_out).dtype)
            out[i, group] = _out
        from_col = to_col
    return out


# ############# Reshaping ############# #

@njit(cache=True)
def flatten_grouped_nb(a: tp.Array2d, group_lens: tp.Array1d, in_c_order: bool) -> tp.Array2d:
    """Flatten each group of columns."""
    out = np.full((a.shape[0] * np.max(group_lens), len(group_lens)), np.nan, dtype=np.float64)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        for k in range(group_len):
            if in_c_order:
                out[k::np.max(group_lens), group] = a[:, from_col + k]
            else:
                out[k * a.shape[0]:(k + 1) * a.shape[0], group] = a[:, from_col + k]
        from_col = to_col
    return out


@njit(cache=True)
def flatten_uniform_grouped_nb(a: tp.Array2d, group_lens: tp.Array1d, in_c_order: bool) -> tp.Array2d:
    """Flatten each group of columns of the same length."""
    out = np.empty((a.shape[0] * np.max(group_lens), len(group_lens)), dtype=a.dtype)
    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        group_len = to_col - from_col
        for k in range(group_len):
            if in_c_order:
                out[k::np.max(group_lens), group] = a[:, from_col + k]
            else:
                out[k * a.shape[0]:(k + 1) * a.shape[0], group] = a[:, from_col + k]
        from_col = to_col
    return out


# ############# Reducers ############# #


@njit(cache=True)
def nth_reduce_nb(col: int, a: tp.Array1d, n: int) -> float:
    """Return n-th element."""
    if (n < 0 and abs(n) > a.shape[0]) or n >= a.shape[0]:
        raise ValueError("index is out of bounds")
    return a[n]


@njit(cache=True)
def nth_index_reduce_nb(col: int, a: tp.Array1d, n: int) -> int:
    """Return index of n-th element."""
    if (n < 0 and abs(n) > a.shape[0]) or n >= a.shape[0]:
        raise ValueError("index is out of bounds")
    if n >= 0:
        return n
    return a.shape[0] + n


@njit(cache=True)
def min_reduce_nb(col: int, a: tp.Array1d) -> float:
    """Return min (ignores NaNs)."""
    return np.nanmin(a)


@njit(cache=True)
def max_reduce_nb(col: int, a: tp.Array1d) -> float:
    """Return max (ignores NaNs)."""
    return np.nanmax(a)


@njit(cache=True)
def mean_reduce_nb(col: int, a: tp.Array1d) -> float:
    """Return mean (ignores NaNs)."""
    return np.nanmean(a)


@njit(cache=True)
def median_reduce_nb(col: int, a: tp.Array1d) -> float:
    """Return median (ignores NaNs)."""
    return np.nanmedian(a)


@njit(cache=True)
def std_reduce_nb(col: int, a: tp.Array1d, ddof) -> float:
    """Return std (ignores NaNs)."""
    return nanstd_1d_nb(a, ddof=ddof)


@njit(cache=True)
def sum_reduce_nb(col: int, a: tp.Array1d) -> float:
    """Return sum (ignores NaNs)."""
    return np.nansum(a)


@njit(cache=True)
def count_reduce_nb(col: int, a: tp.Array1d) -> int:
    """Return count (ignores NaNs)."""
    return np.sum(~np.isnan(a))


@njit(cache=True)
def argmin_reduce_nb(col: int, a: tp.Array1d) -> int:
    """Return position of min."""
    a = np.copy(a)
    mask = np.isnan(a)
    if np.all(mask):
        raise ValueError("All-NaN slice encountered")
    a[mask] = np.inf
    return np.argmin(a)


@njit(cache=True)
def argmax_reduce_nb(col: int, a: tp.Array1d) -> int:
    """Return position of max."""
    a = np.copy(a)
    mask = np.isnan(a)
    if np.all(mask):
        raise ValueError("All-NaN slice encountered")
    a[mask] = -np.inf
    return np.argmax(a)


@njit(cache=True)
def describe_reduce_nb(col: int, a: tp.Array1d, perc: tp.Array1d, ddof: int) -> tp.Array1d:
    """Return descriptive statistics (ignores NaNs).

    Numba equivalent to `pd.Series(a).describe(perc)`."""
    a = a[~np.isnan(a)]
    out = np.empty(5 + len(perc), dtype=np.float64)
    out[0] = len(a)
    if len(a) > 0:
        out[1] = np.mean(a)
        out[2] = nanstd_1d_nb(a, ddof=ddof)
        out[3] = np.min(a)
        out[4:-1] = np.percentile(a, perc * 100)
        out[4 + len(perc)] = np.max(a)
    else:
        out[1:] = np.nan
    return out


# ############# Value counts ############# #


@njit(cache=True)
def value_counts_nb(codes: tp.Array2d, n_uniques: int, group_lens: tp.Array1d) -> tp.Array2d:
    """Return value counts per column/group."""
    out = np.full((n_uniques, group_lens.shape[0]), 0, dtype=np.int64)

    from_col = 0
    for group in range(len(group_lens)):
        to_col = from_col + group_lens[group]
        for col in range(from_col, to_col):
            for i in range(codes.shape[0]):
                out[codes[i, col], group] += 1
        from_col = to_col
    return out


# ############# Group squeezers ############# #


@njit(cache=True)
def min_squeeze_nb(col: int, group: int, a: tp.Array1d) -> float:
    """Return min (ignores NaNs) of a group."""
    return np.nanmin(a)


@njit(cache=True)
def max_squeeze_nb(col: int, group: int, a: tp.Array1d) -> float:
    """Return max (ignores NaNs) of a group."""
    return np.nanmax(a)


@njit(cache=True)
def sum_squeeze_nb(col: int, group: int, a: tp.Array1d) -> float:
    """Return sum (ignores NaNs) of a group."""
    return np.nansum(a)


@njit(cache=True)
def any_squeeze_nb(col: int, group: int, a: tp.Array1d) -> bool:
    """Return any (ignores NaNs) of a group."""
    return np.any(a)


# ############# Ranges ############# #

@njit(cache=True)
def find_ranges_nb(ts: tp.Array2d, gap_value: tp.Scalar) -> tp.RecordArray:
    """Find ranges and store their information as records to an array.

    Usage:
        * Find ranges in time series:

        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from vectorbt.generic.nb import find_ranges_nb

        >>> ts = np.asarray([
        ...     [np.nan, np.nan, np.nan, np.nan],
        ...     [     2, np.nan, np.nan, np.nan],
        ...     [     3,      3, np.nan, np.nan],
        ...     [np.nan,      4,      4, np.nan],
        ...     [     5, np.nan,      5,      5],
        ...     [     6,      6, np.nan,      6]
        ... ])
        >>> records = find_ranges_nb(ts, np.nan)

        >>> pd.DataFrame.from_records(records)
           id  col  start_idx  end_idx
        0   0    0          1        3
        1   1    0          4        6
        2   2    1          2        4
        3   3    1          5        6
        4   4    2          3        5
        5   5    3          4        6
        ```
    """
    out = np.empty(ts.shape[0] * ts.shape[1], dtype=range_dt)
    ridx = 0

    for col in range(ts.shape[1]):
        range_started = False
        start_idx = -1
        end_idx = -1
        store_record = False
        status = -1

        for i in range(ts.shape[0]):
            cur_val = ts[i, col]

            if cur_val == gap_value or np.isnan(cur_val) and np.isnan(gap_value):
                if range_started:
                    # If stopped, save the current range
                    end_idx = i
                    range_started = False
                    store_record = True
                    status = RangeStatus.Closed
            else:
                if not range_started:
                    # If started, register a new range
                    start_idx = i
                    range_started = True

            if i == ts.shape[0] - 1 and range_started:
                # If still running, mark for save
                end_idx = ts.shape[0] - 1
                range_started = False
                store_record = True
                status = RangeStatus.Open

            if store_record:
                # Save range to the records
                out[ridx]['id'] = ridx
                out[ridx]['col'] = col
                out[ridx]['start_idx'] = start_idx
                out[ridx]['end_idx'] = end_idx
                out[ridx]['status'] = status
                ridx += 1

                # Reset running vars for a new range
                store_record = False

    return out[:ridx]


@njit(cache=True)
def range_duration_nb(start_idx_arr: tp.Array1d,
                      end_idx_arr: tp.Array1d,
                      status_arr: tp.Array2d) -> tp.Array1d:
    """Get duration of each duration record."""
    out = np.empty(start_idx_arr.shape[0], dtype=np.int64)
    for ridx in range(out.shape[0]):
        if status_arr[ridx] == RangeStatus.Open:
            out[ridx] = end_idx_arr[ridx] - start_idx_arr[ridx] + 1
        else:
            out[ridx] = end_idx_arr[ridx] - start_idx_arr[ridx]
    return out


@njit(cache=True)
def range_coverage_nb(start_idx_arr: tp.Array1d,
                      end_idx_arr: tp.Array1d,
                      status_arr: tp.Array2d,
                      col_map: tp.ColMap,
                      index_lens: tp.Array1d,
                      overlapping: bool = False,
                      normalize: bool = False) -> tp.Array1d:
    """Get coverage of range records.

    Set `overlapping` to True to get the number of overlapping steps.
    Set `normalize` to True to get the number of steps in relation either to the total number of steps
    (when `overlapping=False`) or to the number of covered steps (when `overlapping=True`).
    """
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full(col_lens.shape[0], np.nan, dtype=np.float64)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        temp = np.full(index_lens[col], 0, dtype=np.int64)
        for ridx in ridxs:
            if status_arr[ridx] == RangeStatus.Open:
                temp[start_idx_arr[ridx]:end_idx_arr[ridx] + 1] += 1
            else:
                temp[start_idx_arr[ridx]:end_idx_arr[ridx]] += 1
        if overlapping:
            if normalize:
                out[col] = np.sum(temp > 1) / np.sum(temp > 0)
            else:
                out[col] = np.sum(temp > 1)
        else:
            if normalize:
                out[col] = np.sum(temp > 0) / index_lens[col]
            else:
                out[col] = np.sum(temp > 0)
    return out


@njit(cache=True)
def ranges_to_mask_nb(start_idx_arr: tp.Array1d,
                      end_idx_arr: tp.Array1d,
                      status_arr: tp.Array2d,
                      col_map: tp.ColMap,
                      index_len: int) -> tp.Array2d:
    """Convert ranges to 2-dim mask."""
    col_idxs, col_lens = col_map
    col_start_idxs = np.cumsum(col_lens) - col_lens
    out = np.full((index_len, col_lens.shape[0]), False, dtype=np.bool_)

    for col in range(col_lens.shape[0]):
        col_len = col_lens[col]
        if col_len == 0:
            continue
        col_start_idx = col_start_idxs[col]
        ridxs = col_idxs[col_start_idx:col_start_idx + col_len]
        for ridx in ridxs:
            if status_arr[ridx] == RangeStatus.Open:
                out[start_idx_arr[ridx]:end_idx_arr[ridx] + 1, col] = True
            else:
                out[start_idx_arr[ridx]:end_idx_arr[ridx], col] = True

    return out


# ############# Drawdowns ############# #

@njit(cache=True)
def get_drawdowns_nb(ts: tp.Array2d) -> tp.RecordArray:
    """Fill drawdown records by analyzing a time series.

    Usage:
        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from vectorbt.generic.nb import get_drawdowns_nb

        >>> ts = np.asarray([
        ...     [1, 5, 1, 3],
        ...     [2, 4, 2, 2],
        ...     [3, 3, 3, 1],
        ...     [4, 2, 2, 2],
        ...     [5, 1, 1, 3]
        ... ])
        >>> records = get_drawdowns_nb(ts)

        >>> pd.DataFrame.from_records(records)
           id  col  peak_idx  start_idx  valley_idx  end_idx  peak_val  valley_val  \\
        0   0    1         0          1           4        4       5.0         1.0
        1   1    2         2          3           4        4       3.0         1.0
        2   2    3         0          1           2        4       3.0         1.0

           end_val  status
        0      1.0       0
        1      1.0       0
        2      3.0       1
        ```
    """
    out = np.empty(ts.shape[0] * ts.shape[1], dtype=drawdown_dt)
    ddidx = 0

    for col in range(ts.shape[1]):
        drawdown_started = False
        peak_idx = -1
        valley_idx = -1
        peak_val = ts[0, col]
        valley_val = ts[0, col]
        store_record = False
        status = -1

        for i in range(ts.shape[0]):
            cur_val = ts[i, col]

            if not np.isnan(cur_val):
                if np.isnan(peak_val) or cur_val >= peak_val:
                    # Value increased
                    if not drawdown_started:
                        # If not running, register new peak
                        peak_val = cur_val
                        peak_idx = i
                    else:
                        # If running, potential recovery
                        if cur_val >= peak_val:
                            drawdown_started = False
                            store_record = True
                            status = DrawdownStatus.Recovered
                else:
                    # Value decreased
                    if not drawdown_started:
                        # If not running, start new drawdown
                        drawdown_started = True
                        valley_val = cur_val
                        valley_idx = i
                    else:
                        # If running, potential valley
                        if cur_val < valley_val:
                            valley_val = cur_val
                            valley_idx = i

                if i == ts.shape[0] - 1 and drawdown_started:
                    # If still running, mark for save
                    drawdown_started = False
                    store_record = True
                    status = DrawdownStatus.Active

                if store_record:
                    # Save drawdown to the records
                    out[ddidx]['id'] = ddidx
                    out[ddidx]['col'] = col
                    out[ddidx]['peak_idx'] = peak_idx
                    out[ddidx]['start_idx'] = peak_idx + 1
                    out[ddidx]['valley_idx'] = valley_idx
                    out[ddidx]['end_idx'] = i
                    out[ddidx]['peak_val'] = peak_val
                    out[ddidx]['valley_val'] = valley_val
                    out[ddidx]['end_val'] = cur_val
                    out[ddidx]['status'] = status
                    ddidx += 1

                    # Reset running vars for a new drawdown
                    peak_idx = i
                    valley_idx = i
                    peak_val = cur_val
                    valley_val = cur_val
                    store_record = False
                    status = -1

    return out[:ddidx]


@njit(cache=True)
def dd_drawdown_nb(peak_val_arr: tp.Array1d, valley_val_arr: tp.Array1d) -> tp.Array1d:
    """Return the drawdown of each drawdown record."""
    return (valley_val_arr - peak_val_arr) / peak_val_arr


@njit(cache=True)
def dd_decline_duration_nb(start_idx_arr: tp.Array1d, valley_idx_arr: tp.Array1d) -> tp.Array1d:
    """Return the duration of the peak-to-valley phase of each drawdown record."""
    return valley_idx_arr - start_idx_arr + 1


@njit(cache=True)
def dd_recovery_duration_nb(valley_idx_arr: tp.Array1d,
                            end_idx_arr: tp.Array1d) -> tp.Array1d:
    """Return the duration of the valley-to-recovery phase of each drawdown record."""
    return end_idx_arr - valley_idx_arr


@njit(cache=True)
def dd_recovery_duration_ratio_nb(start_idx_arr: tp.Array1d,
                                  valley_idx_arr: tp.Array1d,
                                  end_idx_arr: tp.Array1d) -> tp.Array1d:
    """Return the ratio of the recovery duration to the decline duration of each drawdown record."""
    recovery_duration = dd_recovery_duration_nb(valley_idx_arr, end_idx_arr)
    decline_duration = dd_decline_duration_nb(start_idx_arr, valley_idx_arr)
    return recovery_duration / decline_duration


@njit(cache=True)
def dd_recovery_return_nb(valley_val_arr: tp.Array1d, end_val_arr: tp.Array1d) -> tp.Array1d:
    """Return the recovery return of each drawdown record."""
    return (end_val_arr - valley_val_arr) / valley_val_arr


# ############# Crossover ############# #

@njit(cache=True)
def crossed_above_1d_nb(arr1: tp.Array1d, arr2: tp.Array1d, wait: int = 0) -> tp.Array1d:
    """Get the crossover of the first array going above the second array."""
    out = np.empty(arr1.shape, dtype=np.bool_)
    was_below = False
    crossed_ago = -1

    for i in range(arr1.shape[0]):
        if np.isnan(arr1[i]) or np.isnan(arr2[i]):
            crossed_ago = -1
            was_below = False
            out[i] = False
        elif arr1[i] > arr2[i]:
            if was_below:
                crossed_ago += 1
                out[i] = crossed_ago == wait
            else:
                out[i] = False
        elif arr1[i] == arr2[i]:
            crossed_ago = -1
            out[i] = False
        else:
            crossed_ago = -1
            was_below = True
            out[i] = False
    return out


@njit(cache=True)
def crossed_above_nb(arr1: tp.Array2d, arr2: tp.Array2d, wait: int = 0) -> tp.Array2d:
    """2-dim version of `crossed_above_1d_nb`."""
    out = np.empty(arr1.shape, dtype=np.bool_)
    for col in range(arr1.shape[1]):
        out[:, col] = crossed_above_1d_nb(arr1[:, col], arr2[:, col], wait=wait)
    return out
