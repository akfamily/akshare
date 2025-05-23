# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Numba-compiled functions.

Provides an arsenal of Numba-compiled functions that are used by accessors
and in many other parts of the backtesting pipeline, such as technical indicators.
These only accept NumPy arrays and other Numba-compatible types.

```pycon
>>> import numpy as np
>>> import vectorbt as vbt

>>> # vectorbt.signals.nb.pos_rank_nb
>>> vbt.signals.nb.pos_rank_nb(np.array([False, True, True, True, False])[:, None])[:, 0]
[-1  0  1  2 -1]
```

!!! note
    vectorbt treats matrices as first-class citizens and expects input arrays to be
    2-dim, unless function has suffix `_1d` or is meant to be input to another function. 
    Data is processed along index (axis 0).
    
    All functions passed as argument should be Numba-compiled.

    Returned indices should be absolute."""

import numpy as np
from numba import njit

from vectorbt import _typing as tp
from vectorbt.base.reshape_fns import flex_select_auto_nb
from vectorbt.generic.enums import range_dt, RangeStatus
from vectorbt.signals.enums import StopType
from vectorbt.utils.array_ import uniform_summing_to_one_nb, rescale_float_to_int_nb, renormalize_nb


# ############# Generation ############# #


@njit
def generate_nb(shape: tp.Shape,
                pick_first: bool,
                choice_func_nb: tp.ChoiceFunc, *args) -> tp.Array2d:
    """Create a boolean matrix of `shape` and pick signals using `choice_func_nb`.

    Args:
        shape (array): Target shape.
        pick_first (bool): Whether to pick the first signal out of all returned by `choice_func_nb`.
        choice_func_nb (callable): Choice function.

            `choice_func_nb` should accept index of the start of the range `from_i`,
            index of the end of the range `to_i`, index of the column `col`, and `*args`.
            It should return an array of indices from `[from_i, to_i)` (can be empty).
        *args: Arguments passed to `choice_func_nb`.

    Usage:
        ```pycon
        >>> from numba import njit
        >>> import numpy as np
        >>> from vectorbt.signals.nb import generate_nb

        >>> @njit
        ... def choice_func_nb(from_i, to_i, col):
        ...     return np.array([from_i + col])

        >>> generate_nb((5, 3), choice_func_nb)
        [[ True False False]
         [False  True False]
         [False False  True]
         [False False False]
         [False False False]]
        ```
    """
    out = np.full(shape, False, dtype=np.bool_)

    for col in range(out.shape[1]):
        idxs = choice_func_nb(0, shape[0], col, *args)
        if len(idxs) == 0:
            continue
        if pick_first:
            first_i = idxs[0]
            if first_i < 0 or first_i >= shape[0]:
                raise ValueError("First returned index is out of bounds")
            out[first_i, col] = True
        else:
            if np.any(idxs < 0) or np.any(idxs >= shape[0]):
                raise ValueError("Returned indices are out of bounds")
            out[idxs, col] = True
    return out


@njit
def generate_ex_nb(entries: tp.Array2d,
                   wait: int,
                   until_next: bool,
                   skip_until_exit: bool,
                   pick_first: bool,
                   exit_choice_func_nb: tp.ChoiceFunc, *args) -> tp.Array2d:
    """Pick exit signals using `exit_choice_func_nb` after each signal in `entries`.

    Args:
        entries (array): Boolean array with entry signals.
        wait (int): Number of ticks to wait before placing exits.

            !!! note
                Setting `wait` to 0 or False may result in two signals at one bar.
        until_next (int): Whether to place signals up to the next entry signal.

            !!! note
                Setting it to False makes it difficult to tell which exit belongs to which entry.
        skip_until_exit (bool): Whether to skip processing entry signals until the next exit.

            Has only effect when `until_next` is disabled.

            !!! note
                Setting it to True makes it difficult to tell which exit belongs to which entry.
        pick_first (bool): Whether to pick the first signal out of all returned by `exit_choice_func_nb`.
        exit_choice_func_nb (callable): Exit choice function.

            See `choice_func_nb` in `generate_nb`.
        *args (callable): Arguments passed to `exit_choice_func_nb`.
    """
    exits = np.full_like(entries, False)

    for col in range(entries.shape[1]):
        entry_idxs = np.flatnonzero(entries[:, col])
        last_exit_i = -1
        for i in range(entry_idxs.shape[0]):
            # Calculate the range to choose from
            if skip_until_exit and entry_idxs[i] <= last_exit_i:
                continue
            from_i = entry_idxs[i] + wait
            if i < entry_idxs.shape[0] - 1 and until_next:
                to_i = entry_idxs[i + 1]
            else:
                to_i = entries.shape[0]
            if to_i > from_i:
                # Run the UDF
                idxs = exit_choice_func_nb(from_i, to_i, col, *args)
                if len(idxs) == 0:
                    continue
                if pick_first:
                    first_i = idxs[0]
                    if first_i < from_i or first_i >= to_i:
                        raise ValueError("First returned index is out of bounds")
                    exits[first_i, col] = True
                    last_exit_i = first_i
                else:
                    if np.any(idxs < from_i) or np.any(idxs >= to_i):
                        raise ValueError("Returned indices are out of bounds")
                    exits[idxs, col] = True
                    last_exit_i = idxs[-1]
    return exits


@njit
def generate_enex_nb(shape: tp.Shape,
                     entry_wait: int,
                     exit_wait: int,
                     entry_pick_first: bool,
                     exit_pick_first: bool,
                     entry_choice_func_nb: tp.ChoiceFunc,
                     entry_args: tp.Args,
                     exit_choice_func_nb: tp.ChoiceFunc,
                     exit_args: tp.Args) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Pick entry signals using `entry_choice_func_nb` and exit signals using 
    `exit_choice_func_nb` one after another.

    Args:
        shape (array): Target shape.
        entry_wait (int): Number of ticks to wait before placing entries.

            !!! note
                Setting `entry_wait` to 0 or False assumes that both entry and exit can be processed
                within the same bar, and exit can be processed before entry.
        exit_wait (int): Number of ticks to wait before placing exits.

            !!! note
                Setting `exit_wait` to 0 or False assumes that both entry and exit can be processed
                within the same bar, and entry can be processed before exit.
        entry_pick_first (bool): Whether to pick the first entry out of all returned by `entry_choice_func_nb`.
        exit_pick_first (bool): Whether to pick the first exit out of all returned by `exit_choice_func_nb`.

            Setting it to False acts similarly to setting `skip_until_exit` to True in `generate_ex_nb`.
        entry_choice_func_nb (callable): Entry choice function.

            See `choice_func_nb` in `generate_nb`.
        entry_args (tuple): Arguments unpacked and passed to `entry_choice_func_nb`.
        exit_choice_func_nb (callable): Exit choice function.

            See `choice_func_nb` in `generate_nb`.
        exit_args (tuple): Arguments unpacked and passed to `exit_choice_func_nb`.
    """
    entries = np.full(shape, False)
    exits = np.full(shape, False)
    if entry_wait == 0 and exit_wait == 0:
        raise ValueError("entry_wait and exit_wait cannot be both 0")

    for col in range(shape[1]):
        prev_prev_i = -2
        prev_i = -1
        i = 0
        while True:
            to_i = shape[0]
            # Cannot assign two functions to a var in numba
            if i % 2 == 0:
                if i == 0:
                    from_i = 0
                else:
                    from_i = prev_i + entry_wait
                if from_i >= to_i:
                    break
                idxs = entry_choice_func_nb(from_i, to_i, col, *entry_args)
                a = entries
                pick_first = entry_pick_first
            else:
                from_i = prev_i + exit_wait
                if from_i >= to_i:
                    break
                idxs = exit_choice_func_nb(from_i, to_i, col, *exit_args)
                a = exits
                pick_first = exit_pick_first
            if len(idxs) == 0:
                break
            first_i = idxs[0]
            if first_i == prev_i == prev_prev_i:
                raise ValueError("Infinite loop detected")
            if first_i < from_i:
                raise ValueError("First index is out of bounds")
            if pick_first:
                # Consider only the first signal
                if first_i >= to_i:
                    raise ValueError("First index is out of bounds")
                a[first_i, col] = True
                prev_prev_i = prev_i
                prev_i = first_i
                i += 1
            else:
                # Consider all signals
                last_i = idxs[-1]
                if last_i >= to_i:
                    raise ValueError("Last index is out of bounds")
                a[idxs, col] = True
                prev_prev_i = prev_i
                prev_i = last_i
                i += 1

    return entries, exits


# ############# Filtering ############# #


@njit(cache=True)
def clean_enex_1d_nb(entries: tp.Array1d,
                     exits: tp.Array1d,
                     entry_first: bool) -> tp.Tuple[tp.Array1d, tp.Array1d]:
    """Clean entry and exit arrays by picking the first signal out of each.

    Entry signal must be picked first. If both signals are present, selects none."""
    entries_out = np.full(entries.shape, False, dtype=np.bool_)
    exits_out = np.full(exits.shape, False, dtype=np.bool_)

    phase = -1
    for i in range(entries.shape[0]):
        if entries[i] and exits[i]:
            continue
        if entries[i]:
            if phase == -1 or phase == 0:
                phase = 1
                entries_out[i] = True
        if exits[i]:
            if (not entry_first and phase == -1) or phase == 1:
                phase = 0
                exits_out[i] = True

    return entries_out, exits_out


@njit(cache=True)
def clean_enex_nb(entries: tp.Array2d,
                  exits: tp.Array2d,
                  entry_first: bool) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """2-dim version of `clean_enex_1d_nb`."""
    entries_out = np.empty(entries.shape, dtype=np.bool_)
    exits_out = np.empty(exits.shape, dtype=np.bool_)

    for col in range(entries.shape[1]):
        entries_out[:, col], exits_out[:, col] = clean_enex_1d_nb(entries[:, col], exits[:, col], entry_first)
    return entries_out, exits_out


# ############# Random ############# #


@njit(cache=True)
def rand_choice_nb(from_i: int, to_i: int, col: int, n: tp.MaybeArray[int]) -> tp.Array1d:
    """`choice_func_nb` to randomly pick `n` values from range `[from_i, to_i)`.

    `n` uses flexible indexing."""
    ns = np.asarray(n)
    size = min(to_i - from_i, flex_select_auto_nb(ns, 0, col, True))
    return from_i + np.random.choice(to_i - from_i, size=size, replace=False)


@njit
def generate_rand_nb(shape: tp.Shape, n: tp.MaybeArray[int], seed: tp.Optional[int] = None) -> tp.Array2d:
    """Create a boolean matrix of `shape` and pick a number of signals randomly.

    Specify `seed` to make output deterministic.

    See `rand_choice_nb`."""
    if seed is not None:
        np.random.seed(seed)
    return generate_nb(
        shape,
        False,
        rand_choice_nb, n
    )


@njit(cache=True)
def rand_by_prob_choice_nb(from_i: int,
                           to_i: int,
                           col: int,
                           prob: tp.MaybeArray[float],
                           pick_first: bool,
                           temp_idx_arr: tp.Array1d,
                           flex_2d: bool) -> tp.Array1d:
    """`choice_func_nb` to randomly pick values from range `[from_i, to_i)` with probability `prob`.

    `prob` uses flexible indexing."""
    probs = np.asarray(prob)
    j = 0
    for i in range(from_i, to_i):
        if np.random.uniform(0, 1) < flex_select_auto_nb(probs, i, col, flex_2d):  # [0, 1)
            temp_idx_arr[j] = i
            j += 1
            if pick_first:
                break
    return temp_idx_arr[:j]


@njit
def generate_rand_by_prob_nb(shape: tp.Shape,
                             prob: tp.MaybeArray[float],
                             pick_first: bool,
                             flex_2d: bool,
                             seed: tp.Optional[int] = None) -> tp.Array2d:
    """Create a boolean matrix of `shape` and pick signals randomly by probability `prob`.

    `prob` should be a 2-dim array of shape `shape`.
    Specify `seed` to make output deterministic.

    See `rand_by_prob_choice_nb`."""
    if seed is not None:
        np.random.seed(seed)
    temp_idx_arr = np.empty((shape[0],), dtype=np.int64)
    return generate_nb(
        shape,
        pick_first,
        rand_by_prob_choice_nb, prob, pick_first, temp_idx_arr, flex_2d
    )


# ############# Random exits ############# #

@njit
def generate_rand_ex_nb(entries: tp.Array2d,
                        wait: int,
                        until_next: bool,
                        skip_until_exit: bool,
                        seed: tp.Optional[int] = None) -> tp.Array2d:
    """Pick an exit after each entry in `entries`.

    Specify `seed` to make output deterministic."""
    if seed is not None:
        np.random.seed(seed)
    return generate_ex_nb(
        entries,
        wait,
        until_next,
        skip_until_exit,
        True,
        rand_choice_nb, 1
    )


@njit
def generate_rand_ex_by_prob_nb(entries: tp.Array2d,
                                prob: tp.MaybeArray[float],
                                wait: int,
                                until_next: bool,
                                skip_until_exit: bool,
                                flex_2d: bool,
                                seed: tp.Optional[int] = None) -> tp.Array2d:
    """Pick an exit after each entry in `entries` by probability `prob`.

    `prob` should be a 2-dim array of shape `shape`.
    Specify `seed` to make output deterministic."""
    if seed is not None:
        np.random.seed(seed)
    temp_idx_arr = np.empty((entries.shape[0],), dtype=np.int64)
    return generate_ex_nb(
        entries,
        wait,
        until_next,
        skip_until_exit,
        True,
        rand_by_prob_choice_nb, prob, True, temp_idx_arr, flex_2d
    )


@njit
def generate_rand_enex_nb(shape: tp.Shape,
                          n: tp.MaybeArray[int],
                          entry_wait: int,
                          exit_wait: int,
                          seed: tp.Optional[int] = None) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Pick a number of entries and the same number of exits one after another.

    Respects `entry_wait` and `exit_wait` constraints through a number of tricks.
    Tries to mimic a uniform distribution as much as possible.

    The idea is the following: with constraints, there is some fixed amount of total
    space required between first entry and last exit. Upscale this space in a way that
    distribution of entries and exit is similar to a uniform distribution. This means
    randomizing the position of first entry, last exit, and all signals between them.

    `n` uses flexible indexing.
    Specify `seed` to make output deterministic."""
    if seed is not None:
        np.random.seed(seed)
    entries = np.full(shape, False)
    exits = np.full(shape, False)
    if entry_wait == 0 and exit_wait == 0:
        raise ValueError("entry_wait and exit_wait cannot be both 0")
    ns = np.asarray(n)

    if entry_wait == 1 and exit_wait == 1:
        # Basic case
        both = generate_rand_nb(shape, ns * 2, seed=None)
        for col in range(both.shape[1]):
            both_idxs = np.flatnonzero(both[:, col])
            entries[both_idxs[0::2], col] = True
            exits[both_idxs[1::2], col] = True
    else:
        for col in range(shape[1]):
            _n = flex_select_auto_nb(ns, 0, col, True)
            if _n == 1:
                entry_idx = np.random.randint(0, shape[0] - exit_wait)
                entries[entry_idx, col] = True
            else:
                # Minimum range between two entries
                min_range = entry_wait + exit_wait

                # Minimum total range between first and last entry
                min_total_range = min_range * (_n - 1)
                if shape[0] < min_total_range + exit_wait + 1:
                    raise ValueError("Cannot take a larger sample than population")

                # We should decide how much space should be allocate before first and after last entry
                # Maximum space outside of min_total_range
                max_free_space = shape[0] - min_total_range - 1

                # If min_total_range is tiny compared to max_free_space, limit it
                # otherwise we would have huge space before first and after last entry
                # Limit it such as distribution of entries mimics uniform
                free_space = min(max_free_space, 3 * shape[0] // (_n + 1))

                # What about last exit? it requires exit_wait space
                free_space -= exit_wait

                # Now we need to distribute free space among three ranges:
                # 1) before first, 2) between first and last added to min_total_range, 3) after last
                # We do 2) such that min_total_range can freely expand to maximum
                # We allocate twice as much for 3) as for 1) because an exit is missing
                rand_floats = uniform_summing_to_one_nb(6)
                chosen_spaces = rescale_float_to_int_nb(rand_floats, (0, free_space), free_space)
                first_idx = chosen_spaces[0]
                last_idx = shape[0] - np.sum(chosen_spaces[-2:]) - exit_wait - 1

                # Selected range between first and last entry
                total_range = last_idx - first_idx

                # Maximum range between two entries within total_range
                max_range = total_range - (_n - 2) * min_range

                # Select random ranges within total_range
                rand_floats = uniform_summing_to_one_nb(_n - 1)
                chosen_ranges = rescale_float_to_int_nb(rand_floats, (min_range, max_range), total_range)

                # Translate them into entries
                entry_idxs = np.empty(_n, dtype=np.int64)
                entry_idxs[0] = first_idx
                entry_idxs[1:] = chosen_ranges
                entry_idxs = np.cumsum(entry_idxs)
                entries[entry_idxs, col] = True

        # Generate exits
        for col in range(shape[1]):
            entry_idxs = np.flatnonzero(entries[:, col])
            for j in range(len(entry_idxs)):
                entry_i = entry_idxs[j] + exit_wait
                if j < len(entry_idxs) - 1:
                    exit_i = entry_idxs[j + 1] - entry_wait
                else:
                    exit_i = entries.shape[0] - 1
                i = np.random.randint(exit_i - entry_i + 1)
                exits[entry_i + i, col] = True
    return entries, exits


def rand_enex_apply_nb(input_shape: tp.Shape,
                       n: tp.MaybeArray[int],
                       entry_wait: int,
                       exit_wait: int) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """`apply_func_nb` that calls `generate_rand_enex_nb`."""
    return generate_rand_enex_nb(input_shape, n, entry_wait, exit_wait)


@njit
def generate_rand_enex_by_prob_nb(shape: tp.Shape,
                                  entry_prob: tp.MaybeArray[float],
                                  exit_prob: tp.MaybeArray[float],
                                  entry_wait: int,
                                  exit_wait: int,
                                  entry_pick_first: bool,
                                  exit_pick_first: bool,
                                  flex_2d: bool,
                                  seed: tp.Optional[int] = None) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Pick entries by probability `entry_prob` and exits by probability `exit_prob` one after another.

    `entry_prob` and `exit_prob` should be 2-dim arrays of shape `shape`.
    Specify `seed` to make output deterministic."""
    if seed is not None:
        np.random.seed(seed)
    temp_idx_arr = np.empty((shape[0],), dtype=np.int64)
    return generate_enex_nb(
        shape,
        entry_wait,
        exit_wait,
        entry_pick_first,
        exit_pick_first,
        rand_by_prob_choice_nb, (entry_prob, entry_pick_first, temp_idx_arr, flex_2d),
        rand_by_prob_choice_nb, (exit_prob, exit_pick_first, temp_idx_arr, flex_2d)
    )


# ############# Stop exits ############# #


@njit(cache=True)
def first_choice_nb(from_i: int, to_i: int, col: int, a: tp.Array2d) -> tp.Array1d:
    """`choice_func_nb` that returns the index of the first signal in `a`."""
    out = np.empty((1,), dtype=np.int64)
    for i in range(from_i, to_i):
        if a[i, col]:
            out[0] = i
            return out
    return out[:0]  # empty


@njit(cache=True)
def stop_choice_nb(from_i: int,
                   to_i: int,
                   col: int,
                   ts: tp.ArrayLike,
                   stop: tp.MaybeArray[float],
                   trailing: tp.MaybeArray[bool],
                   wait: int,
                   pick_first: bool,
                   temp_idx_arr: tp.Array1d,
                   flex_2d: bool) -> tp.Array1d:
    """`choice_func_nb` that returns the indices of the stop being hit.

    Args:
        from_i (int): Index to start generation from (inclusive).
        to_i (int): Index to run generation to (exclusive).
        col (int): Current column.
        ts (array of float): 2-dim time series array such as price.
        stop (float or array_like): Stop value for stop loss.

            Can be per frame, column, row, or element-wise. Set to `np.nan` to disable.
        trailing (bool or array_like): Whether to use trailing stop.

            Can be per frame, column, row, or element-wise. Set to False to disable.
        wait (int): Number of ticks to wait before placing exits.

            Setting False or 0 may result in two signals at one bar.

            !!! note
                If `wait` is greater than 0, trailing stop won't update at bars that come before `from_i`.
        pick_first (bool): Whether to stop as soon as the first exit signal is found.
        temp_idx_arr (array of int): Empty integer array used to temporarily store indices.
        flex_2d (bool): See `vectorbt.base.reshape_fns.flex_select_auto_nb`."""
    j = 0
    init_i = from_i - wait
    init_ts = flex_select_auto_nb(ts, init_i, col, flex_2d)
    init_stop = flex_select_auto_nb(np.asarray(stop), init_i, col, flex_2d)
    init_trailing = flex_select_auto_nb(np.asarray(trailing), init_i, col, flex_2d)
    max_high = min_low = init_ts

    for i in range(from_i, to_i):
        if not np.isnan(init_stop):
            if init_trailing:
                if init_stop >= 0:
                    # Trailing stop buy
                    curr_stop_price = min_low * (1 + abs(init_stop))
                else:
                    # Trailing stop sell
                    curr_stop_price = max_high * (1 - abs(init_stop))
            else:
                curr_stop_price = init_ts * (1 + init_stop)

        # Check if stop price is within bar
        curr_ts = flex_select_auto_nb(ts, i, col, flex_2d)
        if not np.isnan(init_stop):
            if init_stop >= 0:
                exit_signal = curr_ts >= curr_stop_price
            else:
                exit_signal = curr_ts <= curr_stop_price
            if exit_signal:
                temp_idx_arr[j] = i
                j += 1
                if pick_first:
                    return temp_idx_arr[:1]

        # Keep track of lowest low and highest high if trailing
        if init_trailing:
            if curr_ts < min_low:
                min_low = curr_ts
            elif curr_ts > max_high:
                max_high = curr_ts
    return temp_idx_arr[:j]


@njit
def generate_stop_ex_nb(entries: tp.Array2d,
                        ts: tp.ArrayLike,
                        stop: tp.MaybeArray[float],
                        trailing: tp.MaybeArray[bool],
                        wait: int,
                        until_next: bool,
                        skip_until_exit: bool,
                        pick_first: bool,
                        flex_2d: bool) -> tp.Array2d:
    """Generate using `generate_ex_nb` and `stop_choice_nb`.

    Usage:
        * Generate trailing stop loss and take profit signals for 10%.

        ```pycon
        >>> import numpy as np
        >>> from vectorbt.signals.nb import generate_stop_ex_nb

        >>> entries = np.asarray([False, True, False, False, False])[:, None]
        >>> ts = np.asarray([1, 2, 3, 2, 1])[:, None]

        >>> generate_stop_ex_nb(entries, ts, -0.1, True, 1, True, True)
        array([[False],
               [False],
               [False],
               [ True],
               [False]])

        >>> generate_stop_ex_nb(entries, ts, 0.1, False, 1, True, True)
        array([[False],
               [False],
               [ True],
               [False],
               [False]])
        ```
    """
    temp_idx_arr = np.empty((entries.shape[0],), dtype=np.int64)
    return generate_ex_nb(
        entries,
        wait,
        until_next,
        skip_until_exit,
        pick_first,
        stop_choice_nb,
        ts,
        stop,
        trailing,
        wait,
        pick_first,
        temp_idx_arr,
        flex_2d
    )


@njit
def generate_stop_enex_nb(entries: tp.Array2d,
                          ts: tp.Array,
                          stop: tp.MaybeArray[float],
                          trailing: tp.MaybeArray[bool],
                          entry_wait: int,
                          exit_wait: int,
                          pick_first: bool,
                          flex_2d: bool) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Generate one after another using `generate_enex_nb` and `stop_choice_nb`.

    Returns two arrays: new entries and exits.

    !!! note
        Has the same logic as calling `generate_stop_ex_nb` with `skip_until_exit=True`, but
        removes all entries that come before the next exit."""
    temp_idx_arr = np.empty((entries.shape[0],), dtype=np.int64)
    return generate_enex_nb(
        entries.shape,
        entry_wait,
        exit_wait,
        True,
        pick_first,
        first_choice_nb, (entries,),
        stop_choice_nb, (ts, stop, trailing, exit_wait, pick_first, temp_idx_arr, flex_2d)
    )


@njit(cache=True)
def ohlc_stop_choice_nb(from_i: int,
                        to_i: int,
                        col: int,
                        open: tp.ArrayLike,
                        high: tp.ArrayLike,
                        low: tp.ArrayLike,
                        close: tp.ArrayLike,
                        stop_price_out: tp.Array2d,
                        stop_type_out: tp.Array2d,
                        sl_stop: tp.MaybeArray[float],
                        sl_trail: tp.MaybeArray[bool],
                        tp_stop: tp.MaybeArray[float],
                        reverse: tp.MaybeArray[bool],
                        is_open_safe: bool,
                        wait: int,
                        pick_first: bool,
                        temp_idx_arr: tp.Array1d,
                        flex_2d: bool) -> tp.Array1d:
    """`choice_func_nb` that returns the indices of the stop price being hit within OHLC.

    Compared to `stop_choice_nb`, takes into account the whole bar, can check for both
    (trailing) stop loss and take profit simultaneously, and tracks hit price and stop type.

    !!! note
        We don't have intra-candle data. If there was a huge price fluctuation in both directions,
        we can't determine whether SL was triggered before TP and vice versa. So some assumptions
        need to be made: 1) trailing stop can only be based on previous close/high, and
        2) we pessimistically assume that SL comes before TP.
    
    Args:
        col (int): Current column.
        from_i (int): Index to start generation from (inclusive).
        to_i (int): Index to run generation to (exclusive).
        open (array of float): Entry price such as open or previous close.
        high (array of float): High price.
        low (array of float): Low price.
        close (array of float): Close price.
        stop_price_out (array of float): Array where hit price of each exit will be stored.
        stop_type_out (array of int): Array where stop type of each exit will be stored.

            0 for stop loss, 1 for take profit.
        sl_stop (float or array_like): Percentage value for stop loss.

            Can be per frame, column, row, or element-wise. Set to `np.nan` to disable.
        sl_trail (bool or array_like): Whether `sl_stop` is trailing.

            Can be per frame, column, row, or element-wise. Set to False to disable.
        tp_stop (float or array_like): Percentage value for take profit.

            Can be per frame, column, row, or element-wise. Set to `np.nan` to disable.
        reverse (bool or array_like): Whether to do the opposite, i.e.: prices are followed downwards.
        is_open_safe (bool): Whether entry price comes right at or before open.

            If True and wait is 0, can use high/low at entry bar. Otherwise uses only close.
        wait (int): Number of ticks to wait before placing exits.

            Setting False or 0 may result in entry and exit signal at one bar.

            !!! note
                If `wait` is greater than 0, even with `is_open_safe` set to True,
                trailing stop won't update at bars that come before `from_i`.
        pick_first (bool): Whether to stop as soon as the first exit signal is found.
        temp_idx_arr (array of int): Empty integer array used to temporarily store indices.
        flex_2d (bool): See `vectorbt.base.reshape_fns.flex_select_auto_nb`.
    """
    init_i = from_i - wait
    init_open = flex_select_auto_nb(open, init_i, col, flex_2d)
    init_sl_stop = flex_select_auto_nb(np.asarray(sl_stop), init_i, col, flex_2d)
    if init_sl_stop < 0:
        raise ValueError("Stop value must be 0 or greater")
    init_sl_trail = flex_select_auto_nb(np.asarray(sl_trail), init_i, col, flex_2d)
    init_tp_stop = flex_select_auto_nb(np.asarray(tp_stop), init_i, col, flex_2d)
    if init_tp_stop < 0:
        raise ValueError("Stop value must be 0 or greater")
    init_reverse = flex_select_auto_nb(np.asarray(reverse), init_i, col, flex_2d)
    max_p = min_p = init_open
    j = 0

    for i in range(from_i, to_i):
        # Resolve current bar
        _open = flex_select_auto_nb(open, i, col, flex_2d)
        _high = flex_select_auto_nb(high, i, col, flex_2d)
        _low = flex_select_auto_nb(low, i, col, flex_2d)
        _close = flex_select_auto_nb(close, i, col, flex_2d)
        if np.isnan(_open):
            _open = _close
        if np.isnan(_low):
            _low = min(_open, _close)
        if np.isnan(_high):
            _high = max(_open, _close)

        # Calculate stop price
        if not np.isnan(init_sl_stop):
            if init_sl_trail:
                if init_reverse:
                    curr_sl_stop_price = min_p * (1 + init_sl_stop)
                else:
                    curr_sl_stop_price = max_p * (1 - init_sl_stop)
            else:
                if init_reverse:
                    curr_sl_stop_price = init_open * (1 + init_sl_stop)
                else:
                    curr_sl_stop_price = init_open * (1 - init_sl_stop)
        if not np.isnan(init_tp_stop):
            if init_reverse:
                curr_tp_stop_price = init_open * (1 - init_tp_stop)
            else:
                curr_tp_stop_price = init_open * (1 + init_tp_stop)

        # Check if stop price is within bar
        if i > init_i or is_open_safe:
            # is_open_safe means open is either open or any other price before it
            # so it's safe to use high/low at entry bar
            curr_high = _high
            curr_low = _low
        else:
            # Otherwise, we can only use close price at entry bar
            curr_high = curr_low = _close

        exit_signal = False
        if not np.isnan(init_sl_stop):
            if (not init_reverse and curr_low <= curr_sl_stop_price) or \
                    (init_reverse and curr_high >= curr_sl_stop_price):
                exit_signal = True
                stop_price_out[i, col] = curr_sl_stop_price
                if init_sl_trail:
                    stop_type_out[i, col] = StopType.TrailStop
                else:
                    stop_type_out[i, col] = StopType.StopLoss
        if not exit_signal and not np.isnan(init_tp_stop):
            if (not init_reverse and curr_high >= curr_tp_stop_price) or \
                    (init_reverse and curr_low <= curr_tp_stop_price):
                exit_signal = True
                stop_price_out[i, col] = curr_tp_stop_price
                stop_type_out[i, col] = StopType.TakeProfit
        if exit_signal:
            temp_idx_arr[j] = i
            j += 1
            if pick_first:
                return temp_idx_arr[:1]

        # Keep track of highest high if trailing
        if init_sl_trail:
            if curr_low < min_p:
                min_p = curr_low
            if curr_high > max_p:
                max_p = curr_high

    return temp_idx_arr[:j]


@njit
def generate_ohlc_stop_ex_nb(entries: tp.Array2d,
                             open: tp.ArrayLike,
                             high: tp.ArrayLike,
                             low: tp.ArrayLike,
                             close: tp.ArrayLike,
                             stop_price_out: tp.Array2d,
                             stop_type_out: tp.Array2d,
                             sl_stop: tp.MaybeArray[float],
                             sl_trail: tp.MaybeArray[bool],
                             tp_stop: tp.MaybeArray[float],
                             reverse: tp.MaybeArray[bool],
                             is_open_safe: bool,
                             wait: int,
                             until_next: bool,
                             skip_until_exit: bool,
                             pick_first: bool,
                             flex_2d: bool) -> tp.Array2d:
    """Generate using `generate_ex_nb` and `ohlc_stop_choice_nb`.

    Usage:
        * Generate trailing stop loss and take profit signals for 10%.
        Illustrates how exit signal can be generated within the same bar as entry.

        ```pycon
        >>> import numpy as np
        >>> from vectorbt.signals.nb import generate_ohlc_stop_ex_nb

        >>> entries = np.asarray([True, False, True, False, False])[:, None]
        >>> entry_price = np.asarray([10, 11, 12, 11, 10])[:, None]
        >>> high_price = entry_price + 1
        >>> low_price = entry_price - 1
        >>> close_price = entry_price
        >>> stop_price_out = np.full_like(entries, np.nan, dtype=np.float64)
        >>> stop_type_out = np.full_like(entries, -1, dtype=np.int64)

        >>> generate_ohlc_stop_ex_nb(
        ...     entries=entries,
        ...     open=entry_price,
        ...     high=high_price,
        ...     low=low_price,
        ...     close=close_price,
        ...     stop_price_out=stop_price_out,
        ...     stop_type_out=stop_type_out,
        ...     sl_stop=0.1,
        ...     sl_trail=True,
        ...     tp_stop=0.1,
        ...     reverse=False,
        ...     is_open_safe=True,
        ...     wait=1,
        ...     until_next=True,
        ...     skip_until_exit=False,
        ...     pick_first=True,
        ...     flex_2d=True
        ... )
        array([[ True],
               [False],
               [False],
               [ True],
               [False]])

        >>> stop_price_out
        array([[ 9. ],  << trailing SL from 10 (entry_price)
               [ nan],
               [ nan],
               [11.7],  << trailing SL from 13 (high_price)
               [ nan]])

        >>> stop_type_out
        array([[ 1],
               [-1],
               [-1],
               [ 1],
               [-1]])
        ```

        Note that if `is_open_safe` was False, the first exit would be executed at the second bar.
        This is because we don't know whether the entry price comes before the high and low price
        at the first bar, and so the trailing stop isn't triggered for the low price of 9.0.
    """
    temp_idx_arr = np.empty((entries.shape[0],), dtype=np.int64)
    return generate_ex_nb(
        entries,
        wait,
        until_next,
        skip_until_exit,
        pick_first,
        ohlc_stop_choice_nb,
        open,
        high,
        low,
        close,
        stop_price_out,
        stop_type_out,
        sl_stop,
        sl_trail,
        tp_stop,
        reverse,
        is_open_safe,
        wait,
        pick_first,
        temp_idx_arr,
        flex_2d
    )


@njit
def generate_ohlc_stop_enex_nb(entries: tp.Array2d,
                               open: tp.ArrayLike,
                               high: tp.ArrayLike,
                               low: tp.ArrayLike,
                               close: tp.ArrayLike,
                               stop_price_out: tp.Array2d,
                               stop_type_out: tp.Array2d,
                               sl_stop: tp.MaybeArray[float],
                               sl_trail: tp.MaybeArray[bool],
                               tp_stop: tp.MaybeArray[float],
                               reverse: tp.MaybeArray[bool],
                               is_open_safe: bool,
                               entry_wait: int,
                               exit_wait: int,
                               pick_first: bool,
                               flex_2d: bool) -> tp.Tuple[tp.Array2d, tp.Array2d]:
    """Generate one after another using `generate_enex_nb` and `ohlc_stop_choice_nb`.

    Returns two arrays: new entries and exits.

    !!! note
        Has the same logic as calling `generate_ohlc_stop_ex_nb` with `skip_until_exit=True`, but
        removes all entries that come before the next exit."""
    temp_idx_arr = np.empty((entries.shape[0],), dtype=np.int64)
    return generate_enex_nb(
        entries.shape,
        entry_wait,
        exit_wait,
        True,
        pick_first,
        first_choice_nb, (entries,),
        ohlc_stop_choice_nb, (
            open,
            high,
            low,
            close,
            stop_price_out,
            stop_type_out,
            sl_stop,
            sl_trail,
            tp_stop,
            reverse,
            is_open_safe,
            exit_wait,
            pick_first,
            temp_idx_arr,
            flex_2d
        )
    )


# ############# Map and reduce ranges ############# #


@njit(cache=True)
def between_ranges_nb(a: tp.Array2d) -> tp.RecordArray:
    """Create a record of type `vectorbt.generic.enums.range_dt` for each range between two signals in `a`."""
    range_records = np.empty(a.shape[0] * a.shape[1], dtype=range_dt)
    ridx = 0

    for col in range(a.shape[1]):
        a_idxs = np.flatnonzero(a[:, col])
        if a_idxs.shape[0] > 1:
            for j in range(1, a_idxs.shape[0]):
                from_i = a_idxs[j - 1]
                to_i = a_idxs[j]
                range_records[ridx]['id'] = ridx
                range_records[ridx]['col'] = col
                range_records[ridx]['start_idx'] = from_i
                range_records[ridx]['end_idx'] = to_i
                range_records[ridx]['status'] = RangeStatus.Closed
                ridx += 1
    return range_records[:ridx]


@njit(cache=True)
def between_two_ranges_nb(a: tp.Array2d, b: tp.Array2d, from_other: bool = False) -> tp.RecordArray:
    """Create a record of type `vectorbt.generic.enums.range_dt` for each range between two signals in `a` and `b`.

    If `from_other` is False, returns ranges from each in `a` to the succeeding in `b`.
    Otherwise, returns ranges from each in `b` to the preceding in `a`.

    When `a` and `b` overlap (two signals at the same time), the distance between overlapping
    signals is still considered and `from_i` would match `to_i`."""
    range_records = np.empty(a.shape[0] * a.shape[1], dtype=range_dt)
    ridx = 0

    for col in range(a.shape[1]):
        a_idxs = np.flatnonzero(a[:, col])
        if a_idxs.shape[0] > 0:
            b_idxs = np.flatnonzero(b[:, col])
            if b_idxs.shape[0] > 0:
                if from_other:
                    for j, to_i in enumerate(b_idxs):
                        valid_a_idxs = a_idxs[a_idxs <= to_i]
                        if len(valid_a_idxs) > 0:
                            from_i = valid_a_idxs[-1]  # preceding in a
                            range_records[ridx]['id'] = ridx
                            range_records[ridx]['col'] = col
                            range_records[ridx]['start_idx'] = from_i
                            range_records[ridx]['end_idx'] = to_i
                            range_records[ridx]['status'] = RangeStatus.Closed
                            ridx += 1
                else:
                    for j, from_i in enumerate(a_idxs):
                        valid_b_idxs = b_idxs[b_idxs >= from_i]
                        if len(valid_b_idxs) > 0:
                            to_i = valid_b_idxs[0]  # succeeding in b
                            range_records[ridx]['id'] = ridx
                            range_records[ridx]['col'] = col
                            range_records[ridx]['start_idx'] = from_i
                            range_records[ridx]['end_idx'] = to_i
                            range_records[ridx]['status'] = RangeStatus.Closed
                            ridx += 1
    return range_records[:ridx]


@njit(cache=True)
def partition_ranges_nb(a: tp.Array2d) -> tp.RecordArray:
    """Create a record of type `vectorbt.generic.enums.range_dt` for each partition of signals in `a`."""
    range_records = np.empty(a.shape[0] * a.shape[1], dtype=range_dt)
    ridx = 0

    for col in range(a.shape[1]):
        is_partition = False
        from_i = -1
        for i in range(a.shape[0]):
            if a[i, col]:
                if not is_partition:
                    from_i = i
                is_partition = True
            elif is_partition:
                to_i = i
                range_records[ridx]['id'] = ridx
                range_records[ridx]['col'] = col
                range_records[ridx]['start_idx'] = from_i
                range_records[ridx]['end_idx'] = to_i
                range_records[ridx]['status'] = RangeStatus.Closed
                ridx += 1
                is_partition = False
            if i == a.shape[0] - 1:
                if is_partition:
                    to_i = a.shape[0] - 1
                    range_records[ridx]['id'] = ridx
                    range_records[ridx]['col'] = col
                    range_records[ridx]['start_idx'] = from_i
                    range_records[ridx]['end_idx'] = to_i
                    range_records[ridx]['status'] = RangeStatus.Open
                    ridx += 1
    return range_records[:ridx]


@njit(cache=True)
def between_partition_ranges_nb(a: tp.Array2d) -> tp.RecordArray:
    """Create a record of type `vectorbt.generic.enums.range_dt` for each range between two partitions in `a`."""
    range_records = np.empty(a.shape[0] * a.shape[1], dtype=range_dt)
    ridx = 0

    for col in range(a.shape[1]):
        is_partition = False
        from_i = -1
        for i in range(a.shape[0]):
            if a[i, col]:
                if not is_partition and from_i != -1:
                    to_i = i
                    range_records[ridx]['id'] = ridx
                    range_records[ridx]['col'] = col
                    range_records[ridx]['start_idx'] = from_i
                    range_records[ridx]['end_idx'] = to_i
                    range_records[ridx]['status'] = RangeStatus.Closed
                    ridx += 1
                is_partition = True
                from_i = i
            else:
                is_partition = False
    return range_records[:ridx]


# ############# Ranking ############# #

@njit
def rank_nb(a: tp.Array2d,
            reset_by: tp.Optional[tp.Array1d],
            after_false: bool,
            rank_func_nb: tp.RankFunc, *args) -> tp.Array2d:
    """Rank each signal using `rank_func_nb`.

    Applies `rank_func_nb` on each True value. Should accept index of the row, 
    index of the column, index of the last reset signal, index of the end of the previous partition,
    index of the start of the current partition, and `*args`. Should return -1 for no rank, otherwise 0 or greater.

    Setting `after_false` to True will disregard the first partition of True values
    if there is no False value before them."""
    out = np.full(a.shape, -1, dtype=np.int64)

    for col in range(a.shape[1]):
        reset_i = 0
        prev_part_end_i = -1
        part_start_i = -1
        in_partition = False
        false_seen = not after_false
        for i in range(a.shape[0]):
            if reset_by is not None:
                if reset_by[i, col]:
                    reset_i = i
            if a[i, col] and not (after_false and not false_seen):
                if not in_partition:
                    part_start_i = i
                in_partition = True
                out[i, col] = rank_func_nb(i, col, reset_i, prev_part_end_i, part_start_i, *args)
            elif not a[i, col]:
                if in_partition:
                    prev_part_end_i = i - 1
                in_partition = False
                false_seen = True
    return out


@njit(cache=True)
def sig_pos_rank_nb(i: int, col: int, reset_i: int, prev_part_end_i: int, part_start_i: int,
                    sig_pos_temp: tp.Array1d, allow_gaps: bool) -> int:
    """`rank_func_nb` that returns the rank of each signal by its position in the partition."""
    if reset_i > prev_part_end_i and max(reset_i, part_start_i) == i:
        sig_pos_temp[col] = -1
    elif not allow_gaps and part_start_i == i:
        sig_pos_temp[col] = -1
    sig_pos_temp[col] += 1
    return sig_pos_temp[col]


@njit(cache=True)
def part_pos_rank_nb(i: int, col: int, reset_i: int, prev_part_end_i: int, part_start_i: int,
                     part_pos_temp: tp.Array1d) -> int:
    """`rank_func_nb` that returns the rank of each partition by its position in the series."""
    if reset_i > prev_part_end_i and max(reset_i, part_start_i) == i:
        part_pos_temp[col] = 0
    elif part_start_i == i:
        part_pos_temp[col] += 1
    return part_pos_temp[col]


# ############# Index ############# #


@njit(cache=True)
def nth_index_1d_nb(a: tp.Array1d, n: int) -> int:
    """Get the index of the n-th True value.

    !!! note
        `n` starts with 0 and can be negative."""
    if n >= 0:
        found = -1
        for i in range(a.shape[0]):
            if a[i]:
                found += 1
                if found == n:
                    return i
    else:
        found = 0
        for i in range(a.shape[0] - 1, -1, -1):
            if a[i]:
                found -= 1
                if found == n:
                    return i
    return -1


@njit(cache=True)
def nth_index_nb(a: tp.Array2d, n: int) -> tp.Array1d:
    """2-dim version of `nth_index_1d_nb`."""
    out = np.empty(a.shape[1], dtype=np.int64)
    for col in range(a.shape[1]):
        out[col] = nth_index_1d_nb(a[:, col], n)
    return out


@njit(cache=True)
def norm_avg_index_1d_nb(a: tp.Array1d) -> float:
    """Get mean index normalized to (-1, 1)."""
    mean_index = np.mean(np.flatnonzero(a))
    return renormalize_nb(mean_index, (0, len(a) - 1), (-1, 1))


@njit(cache=True)
def norm_avg_index_nb(a: tp.Array2d) -> tp.Array1d:
    """2-dim version of `norm_avg_index_1d_nb`."""
    out = np.empty(a.shape[1], dtype=np.float64)
    for col in range(a.shape[1]):
        out[col] = norm_avg_index_1d_nb(a[:, col])
    return out
