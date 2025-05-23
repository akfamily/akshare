# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Custom pandas accessors for signals data.

Methods can be accessed as follows:

* `SignalsSRAccessor` -> `pd.Series.vbt.signals.*`
* `SignalsDFAccessor` -> `pd.DataFrame.vbt.signals.*`

```pycon
>>> import pandas as pd
>>> import vectorbt as vbt

>>> # vectorbt.signals.accessors.SignalsAccessor.pos_rank
>>> pd.Series([False, True, True, True, False]).vbt.signals.pos_rank()
0    0
1    1
2    2
3    3
4    0
dtype: int64
```

The accessors extend `vectorbt.generic.accessors`.

!!! note
    The underlying Series/DataFrame should already be a signal series.

    Input arrays should be `np.bool_`.

    Grouping is only supported by the methods that accept the `group_by` argument.

    Accessors do not utilize caching.

Run for the examples below:
    
```pycon
>>> import vectorbt as vbt
>>> import numpy as np
>>> import pandas as pd
>>> from numba import njit
>>> from datetime import datetime

>>> mask = pd.DataFrame({
...     'a': [True, False, False, False, False],
...     'b': [True, False, True, False, True],
...     'c': [True, True, True, False, False]
... }, index=pd.Index([
...     datetime(2020, 1, 1),
...     datetime(2020, 1, 2),
...     datetime(2020, 1, 3),
...     datetime(2020, 1, 4),
...     datetime(2020, 1, 5)
... ]))
>>> mask
                a      b      c
2020-01-01   True   True   True
2020-01-02  False  False   True
2020-01-03  False   True   True
2020-01-04  False  False  False
2020-01-05  False   True  False
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `SignalsAccessor.metrics`.

```pycon
>>> mask.vbt.signals.stats(column='a')
Start                       2020-01-01 00:00:00
End                         2020-01-05 00:00:00
Period                          5 days 00:00:00
Total                                         1
Rate [%]                                     20
First Index                 2020-01-01 00:00:00
Last Index                  2020-01-01 00:00:00
Norm Avg Index [-1, 1]                       -1
Distance: Min                               NaT
Distance: Max                               NaT
Distance: Mean                              NaT
Distance: Std                               NaT
Total Partitions                              1
Partition Rate [%]                          100
Partition Length: Min           1 days 00:00:00
Partition Length: Max           1 days 00:00:00
Partition Length: Mean          1 days 00:00:00
Partition Length: Std                       NaT
Partition Distance: Min                     NaT
Partition Distance: Max                     NaT
Partition Distance: Mean                    NaT
Partition Distance: Std                     NaT
Name: a, dtype: object
```

We can pass another signal array to compare this array with:

```pycon
>>> mask.vbt.signals.stats(column='a', settings=dict(other=mask['b']))
Start                       2020-01-01 00:00:00
End                         2020-01-05 00:00:00
Period                          5 days 00:00:00
Total                                         1
Rate [%]                                     20
Total Overlapping                             1
Overlapping Rate [%]                    33.3333
First Index                 2020-01-01 00:00:00
Last Index                  2020-01-01 00:00:00
Norm Avg Index [-1, 1]                       -1
Distance -> Other: Min          0 days 00:00:00
Distance -> Other: Max          0 days 00:00:00
Distance -> Other: Mean         0 days 00:00:00
Distance -> Other: Std                      NaT
Total Partitions                              1
Partition Rate [%]                          100
Partition Length: Min           1 days 00:00:00
Partition Length: Max           1 days 00:00:00
Partition Length: Mean          1 days 00:00:00
Partition Length: Std                       NaT
Partition Distance: Min                     NaT
Partition Distance: Max                     NaT
Partition Distance: Mean                    NaT
Partition Distance: Std                     NaT
Name: a, dtype: object
```

We can also return duration as a floating number rather than a timedelta:

```pycon
>>> mask.vbt.signals.stats(column='a', settings=dict(to_timedelta=False))
Start                       2020-01-01 00:00:00
End                         2020-01-05 00:00:00
Period                                        5
Total                                         1
Rate [%]                                     20
First Index                 2020-01-01 00:00:00
Last Index                  2020-01-01 00:00:00
Norm Avg Index [-1, 1]                       -1
Distance: Min                               NaN
Distance: Max                               NaN
Distance: Mean                              NaN
Distance: Std                               NaN
Total Partitions                              1
Partition Rate [%]                          100
Partition Length: Min                         1
Partition Length: Max                         1
Partition Length: Mean                        1
Partition Length: Std                       NaN
Partition Distance: Min                     NaN
Partition Distance: Max                     NaN
Partition Distance: Mean                    NaN
Partition Distance: Std                     NaN
Name: a, dtype: object
```

`SignalsAccessor.stats` also supports (re-)grouping:

```pycon
>>> mask.vbt.signals.stats(column=0, group_by=[0, 0, 1])
Start                       2020-01-01 00:00:00
End                         2020-01-05 00:00:00
Period                          5 days 00:00:00
Total                                         4
Rate [%]                                     40
First Index                 2020-01-01 00:00:00
Last Index                  2020-01-05 00:00:00
Norm Avg Index [-1, 1]                    -0.25
Distance: Min                   2 days 00:00:00
Distance: Max                   2 days 00:00:00
Distance: Mean                  2 days 00:00:00
Distance: Std                   0 days 00:00:00
Total Partitions                              4
Partition Rate [%]                          100
Partition Length: Min           1 days 00:00:00
Partition Length: Max           1 days 00:00:00
Partition Length: Mean          1 days 00:00:00
Partition Length: Std           0 days 00:00:00
Partition Distance: Min         2 days 00:00:00
Partition Distance: Max         2 days 00:00:00
Partition Distance: Mean        2 days 00:00:00
Partition Distance: Std         0 days 00:00:00
Name: 0, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `SignalsAccessor.subplots`.

This class inherits subplots from `vectorbt.generic.accessors.GenericAccessor`.
"""

import warnings

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base import reshape_fns
from vectorbt.base.array_wrapper import ArrayWrapper
from vectorbt.generic import nb as generic_nb
from vectorbt.generic import plotting
from vectorbt.generic.accessors import GenericAccessor, GenericSRAccessor, GenericDFAccessor
from vectorbt.generic.ranges import Ranges
from vectorbt.records.mapped_array import MappedArray
from vectorbt.root_accessors import register_dataframe_vbt_accessor, register_series_vbt_accessor
from vectorbt.signals import nb
from vectorbt.utils import checks
from vectorbt.utils.colors import adjust_lightness
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.decorators import class_or_instancemethod
from vectorbt.utils.template import RepEval

__pdoc__ = {}


class SignalsAccessor(GenericAccessor):
    """Accessor on top of signal series. For both, Series and DataFrames.

    Accessible through `pd.Series.vbt.signals` and `pd.DataFrame.vbt.signals`."""

    def __init__(self, obj: tp.SeriesFrame, **kwargs) -> None:
        checks.assert_dtype(obj, np.bool_)

        GenericAccessor.__init__(self, obj, **kwargs)

    @property
    def sr_accessor_cls(self) -> tp.Type["SignalsSRAccessor"]:
        """Accessor class for `pd.Series`."""
        return SignalsSRAccessor

    @property
    def df_accessor_cls(self) -> tp.Type["SignalsDFAccessor"]:
        """Accessor class for `pd.DataFrame`."""
        return SignalsDFAccessor

    # ############# Overriding ############# #

    def bshift(self, *args, fill_value: bool = False, **kwargs) -> tp.SeriesFrame:
        """`vectorbt.generic.accessors.GenericAccessor.bshift` with `fill_value=False`."""
        return GenericAccessor.bshift(self, *args, fill_value=fill_value, **kwargs)

    def fshift(self, *args, fill_value: bool = False, **kwargs) -> tp.SeriesFrame:
        """`vectorbt.generic.accessors.GenericAccessor.fshift` with `fill_value=False`."""
        return GenericAccessor.fshift(self, *args, fill_value=fill_value, **kwargs)

    @classmethod
    def empty(cls, *args, fill_value: bool = False, **kwargs) -> tp.SeriesFrame:
        """`vectorbt.base.accessors.BaseAccessor.empty` with `fill_value=False`."""
        return GenericAccessor.empty(*args, fill_value=fill_value, dtype=np.bool_, **kwargs)

    @classmethod
    def empty_like(cls, *args, fill_value: bool = False, **kwargs) -> tp.SeriesFrame:
        """`vectorbt.base.accessors.BaseAccessor.empty_like` with `fill_value=False`."""
        return GenericAccessor.empty_like(*args, fill_value=fill_value, dtype=np.bool_, **kwargs)

    # ############# Generation ############# #

    @classmethod
    def generate(cls,
                 shape: tp.RelaxedShape,
                 choice_func_nb: tp.ChoiceFunc, *args,
                 pick_first: bool = False,
                 **kwargs) -> tp.SeriesFrame:
        """See `vectorbt.signals.nb.generate_nb`.

        `**kwargs` will be passed to pandas constructor.

        Usage:
            * Generate random signals manually:

            ```pycon
            >>> @njit
            ... def choice_func_nb(from_i, to_i, col):
            ...     return col + from_i

            >>> pd.DataFrame.vbt.signals.generate((5, 3),
            ...     choice_func_nb, index=mask.index, columns=mask.columns)
                            a      b      c
            2020-01-01   True  False  False
            2020-01-02  False   True  False
            2020-01-03  False  False   True
            2020-01-04  False  False  False
            2020-01-05  False  False  False
            ```
        """
        checks.assert_numba_func(choice_func_nb)

        if not isinstance(shape, tuple):
            shape = (shape, 1)
        elif isinstance(shape, tuple) and len(shape) == 1:
            shape = (shape[0], 1)

        result = nb.generate_nb(shape, pick_first, choice_func_nb, *args)

        if cls.is_series():
            if shape[1] > 1:
                raise ValueError("Use DataFrame accessor")
            return pd.Series(result[:, 0], **kwargs)
        return pd.DataFrame(result, **kwargs)

    @classmethod
    def generate_both(cls,
                      shape: tp.RelaxedShape,
                      entry_choice_func_nb: tp.Optional[tp.ChoiceFunc] = None,
                      entry_args: tp.ArgsLike = None,
                      exit_choice_func_nb: tp.Optional[tp.ChoiceFunc] = None,
                      exit_args: tp.ArgsLike = None,
                      entry_wait: int = 1,
                      exit_wait: int = 1,
                      entry_pick_first: bool = True,
                      exit_pick_first: bool = True,
                      **kwargs) -> tp.Tuple[tp.SeriesFrame, tp.SeriesFrame]:
        """See `vectorbt.signals.nb.generate_enex_nb`.

        `**kwargs` will be passed to pandas constructor.

        Usage:
            * Generate entry and exit signals one after another. Each column increment
            the number of ticks to wait before placing the exit signal.

            ```pycon
            >>> @njit
            ... def entry_choice_func_nb(from_i, to_i, col, temp_idx_arr):
            ...     temp_idx_arr[0] = from_i
            ...     return temp_idx_arr[:1]  # array with one signal

            >>> @njit
            ... def exit_choice_func_nb(from_i, to_i, col, temp_idx_arr):
            ...     wait = col
            ...     temp_idx_arr[0] = from_i + wait
            ...     if temp_idx_arr[0] < to_i:
            ...         return temp_idx_arr[:1]  # array with one signal
            ...     return temp_idx_arr[:0]  # empty array

            >>> temp_idx_arr = np.empty((1,), dtype=np.int64)  # reuse memory
            >>> en, ex = pd.DataFrame.vbt.signals.generate_both(
            ...     (5, 3),
            ...     entry_choice_func_nb, (temp_idx_arr,),
            ...     exit_choice_func_nb, (temp_idx_arr,),
            ...     index=mask.index, columns=mask.columns)
            >>> en
                            a      b      c
            2020-01-01   True   True   True
            2020-01-02  False  False  False
            2020-01-03   True  False  False
            2020-01-04  False   True  False
            2020-01-05   True  False   True
            >>> ex
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True  False  False
            2020-01-03  False   True  False
            2020-01-04   True  False   True
            2020-01-05  False  False  False
            ```
        """
        checks.assert_not_none(entry_choice_func_nb)
        checks.assert_not_none(exit_choice_func_nb)
        checks.assert_numba_func(entry_choice_func_nb)
        checks.assert_numba_func(exit_choice_func_nb)
        if entry_args is None:
            entry_args = ()
        if exit_args is None:
            exit_args = ()

        if not isinstance(shape, tuple):
            shape = (shape, 1)
        elif isinstance(shape, tuple) and len(shape) == 1:
            shape = (shape[0], 1)

        result1, result2 = nb.generate_enex_nb(
            shape,
            entry_wait,
            exit_wait,
            entry_pick_first,
            exit_pick_first,
            entry_choice_func_nb, entry_args,
            exit_choice_func_nb, exit_args
        )
        if cls.is_series():
            if shape[1] > 1:
                raise ValueError("Use DataFrame accessor")
            return pd.Series(result1[:, 0], **kwargs), pd.Series(result2[:, 0], **kwargs)
        return pd.DataFrame(result1, **kwargs), pd.DataFrame(result2, **kwargs)

    def generate_exits(self,
                       exit_choice_func_nb: tp.ChoiceFunc, *args,
                       wait: int = 1,
                       until_next: bool = True,
                       skip_until_exit: bool = False,
                       pick_first: bool = False,
                       wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.signals.nb.generate_ex_nb`.

        Usage:
            * Fill all space after signals in `mask`:

            ```pycon
            >>> @njit
            ... def exit_choice_func_nb(from_i, to_i, col, temp_range):
            ...     return temp_range[from_i:to_i]

            >>> temp_range = np.arange(mask.shape[0])  # reuse memory
            >>> mask.vbt.signals.generate_exits(exit_choice_func_nb, temp_range)
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True   True  False
            2020-01-03   True  False  False
            2020-01-04   True   True   True
            2020-01-05   True  False   True
            ```
        """
        checks.assert_numba_func(exit_choice_func_nb)

        exits = nb.generate_ex_nb(
            self.to_2d_array(),
            wait,
            until_next,
            skip_until_exit,
            pick_first,
            exit_choice_func_nb,
            *args
        )
        return self.wrapper.wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))

    # ############# Filtering ############# #

    @class_or_instancemethod
    def clean(cls_or_self,
              *args,
              entry_first: bool = True,
              broadcast_kwargs: tp.KwargsLike = None,
              wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeTuple[tp.SeriesFrame]:
        """Clean signals.

        If one array passed, see `SignalsAccessor.first`.
        If two arrays passed, entries and exits, see `vectorbt.signals.nb.clean_enex_nb`."""
        if not isinstance(cls_or_self, type):
            args = (cls_or_self.obj, *args)
        if len(args) == 1:
            obj = args[0]
            if not isinstance(obj, (pd.Series, pd.DataFrame)):
                wrapper = ArrayWrapper.from_shape(np.asarray(obj).shape)
                obj = wrapper.wrap(obj)
            return obj.vbt.signals.first(wrap_kwargs=wrap_kwargs)
        elif len(args) == 2:
            if broadcast_kwargs is None:
                broadcast_kwargs = {}
            entries, exits = reshape_fns.broadcast(*args, **broadcast_kwargs)
            entries_out, exits_out = nb.clean_enex_nb(
                reshape_fns.to_2d_array(entries),
                reshape_fns.to_2d_array(exits),
                entry_first
            )
            return (
                ArrayWrapper.from_obj(entries).wrap(entries_out, group_by=False, **merge_dicts({}, wrap_kwargs)),
                ArrayWrapper.from_obj(exits).wrap(exits_out, group_by=False, **merge_dicts({}, wrap_kwargs))
            )
        else:
            raise ValueError("Either one or two arrays must be passed")

    # ############# Random ############# #

    @classmethod
    def generate_random(cls,
                        shape: tp.RelaxedShape,
                        n: tp.Optional[tp.ArrayLike] = None,
                        prob: tp.Optional[tp.ArrayLike] = None,
                        pick_first: bool = False,
                        seed: tp.Optional[int] = None,
                        **kwargs) -> tp.SeriesFrame:
        """Generate signals randomly.

        If `n` is set, see `vectorbt.signals.nb.generate_rand_nb`.
        If `prob` is set, see `vectorbt.signals.nb.generate_rand_by_prob_nb`.

        `n` should be either a scalar or an array that will broadcast to the number of columns.
        `prob` should be either a single number or an array that will broadcast to match `shape`.
        `**kwargs` will be passed to pandas constructor.

        Usage:
            * For each column, generate a variable number of signals:

            ```pycon
            >>> pd.DataFrame.vbt.signals.generate_random((5, 3), n=[0, 1, 2],
            ...     seed=42, index=mask.index, columns=mask.columns)
                            a      b      c
            2020-01-01  False  False   True
            2020-01-02  False  False   True
            2020-01-03  False  False  False
            2020-01-04  False   True  False
            2020-01-05  False  False  False
            ```

            * For each column and time step, pick a signal with 50% probability:

            ```pycon
            >>> pd.DataFrame.vbt.signals.generate_random((5, 3), prob=0.5,
            ...     seed=42, index=mask.index, columns=mask.columns)
                            a      b      c
            2020-01-01   True   True   True
            2020-01-02  False   True  False
            2020-01-03  False  False  False
            2020-01-04  False  False   True
            2020-01-05   True  False   True
            ```
        """
        flex_2d = True
        if not isinstance(shape, tuple):
            flex_2d = False
            shape = (shape, 1)
        elif isinstance(shape, tuple) and len(shape) == 1:
            flex_2d = False
            shape = (shape[0], 1)

        if n is not None and prob is not None:
            raise ValueError("Either n or prob should be set, not both")
        if n is not None:
            n = np.broadcast_to(n, shape[1])
            result = nb.generate_rand_nb(shape, n, seed=seed)
        elif prob is not None:
            prob = np.broadcast_to(prob, shape)
            result = nb.generate_rand_by_prob_nb(shape, prob, pick_first, flex_2d, seed=seed)
        else:
            raise ValueError("At least n or prob should be set")

        if cls.is_series():
            if shape[1] > 1:
                raise ValueError("Use DataFrame accessor")
            return pd.Series(result[:, 0], **kwargs)
        return pd.DataFrame(result, **kwargs)

    # ############# Exits ############# #

    @classmethod
    def generate_random_both(cls,
                             shape: tp.RelaxedShape,
                             n: tp.Optional[tp.ArrayLike] = None,
                             entry_prob: tp.Optional[tp.ArrayLike] = None,
                             exit_prob: tp.Optional[tp.ArrayLike] = None,
                             seed: tp.Optional[int] = None,
                             entry_wait: int = 1,
                             exit_wait: int = 1,
                             entry_pick_first: bool = True,
                             exit_pick_first: bool = True,
                             **kwargs) -> tp.Tuple[tp.SeriesFrame, tp.SeriesFrame]:
        """Generate chain of entry and exit signals randomly.

        If `n` is set, see `vectorbt.signals.nb.generate_rand_enex_nb`.
        If `entry_prob` and `exit_prob` are set, see `vectorbt.signals.nb.generate_rand_enex_by_prob_nb`.

        For arguments, see `SignalsAccessor.generate_random`.

        Usage:
            * For each column, generate two entries and exits randomly:

            ```pycon
            >>> en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            ...     (5, 3), n=2, seed=42, index=mask.index, columns=mask.columns)
            >>> en
                            a      b      c
            2020-01-01   True   True   True
            2020-01-02  False  False  False
            2020-01-03   True   True  False
            2020-01-04  False  False   True
            2020-01-05  False  False  False
            >>> ex
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True   True   True
            2020-01-03  False  False  False
            2020-01-04  False   True  False
            2020-01-05   True  False   True
            ```

            * For each column and time step, pick entry with 50% probability and exit right after:

            ```pycon
            >>> en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            ...     (5, 3), entry_prob=0.5, exit_prob=1.,
            ...     seed=42, index=mask.index, columns=mask.columns)
            >>> en
                            a      b      c
            2020-01-01   True   True   True
            2020-01-02  False  False  False
            2020-01-03  False  False  False
            2020-01-04  False  False   True
            2020-01-05   True  False  False
            >>> ex
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True   True  False
            2020-01-03  False  False   True
            2020-01-04  False   True  False
            2020-01-05   True  False   True
            ```
        """
        flex_2d = True
        if not isinstance(shape, tuple):
            flex_2d = False
            shape = (shape, 1)
        elif isinstance(shape, tuple) and len(shape) == 1:
            flex_2d = False
            shape = (shape[0], 1)

        if n is not None and (entry_prob is not None or exit_prob is not None):
            raise ValueError("Either n or any of the entry_prob and exit_prob should be set, not both")
        if n is not None:
            n = np.broadcast_to(n, shape[1])
            entries, exits = nb.generate_rand_enex_nb(shape, n, entry_wait, exit_wait, seed=seed)
        elif entry_prob is not None and exit_prob is not None:
            entry_prob = np.broadcast_to(entry_prob, shape)
            exit_prob = np.broadcast_to(exit_prob, shape)
            entries, exits = nb.generate_rand_enex_by_prob_nb(
                shape,
                entry_prob,
                exit_prob,
                entry_wait,
                exit_wait,
                entry_pick_first,
                exit_pick_first,
                flex_2d,
                seed=seed
            )
        else:
            raise ValueError("At least n, or entry_prob and exit_prob should be set")

        if cls.is_series():
            if shape[1] > 1:
                raise ValueError("Use DataFrame accessor")
            return pd.Series(entries[:, 0], **kwargs), pd.Series(exits[:, 0], **kwargs)
        return pd.DataFrame(entries, **kwargs), pd.DataFrame(exits, **kwargs)

    def generate_random_exits(self,
                              prob: tp.Optional[tp.ArrayLike] = None,
                              seed: tp.Optional[int] = None,
                              wait: int = 1,
                              until_next: bool = True,
                              skip_until_exit: bool = False,
                              wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Generate exit signals randomly.

        If `prob` is None, see `vectorbt.signals.nb.generate_rand_ex_nb`.
        Otherwise, see `vectorbt.signals.nb.generate_rand_ex_by_prob_nb`.

        Usage:
            * After each entry in `mask`, generate exactly one exit:

            ```pycon
            >>> mask.vbt.signals.generate_random_exits(seed=42)
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02  False   True  False
            2020-01-03   True  False  False
            2020-01-04  False   True  False
            2020-01-05  False  False   True
            ```

            * After each entry in `mask` and at each time step, generate exit with 50% probability:

            ```pycon
            >>> mask.vbt.signals.generate_random_exits(prob=0.5, seed=42)
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True  False  False
            2020-01-03  False  False  False
            2020-01-04  False  False  False
            2020-01-05  False  False   True
            ```
        """
        if prob is not None:
            obj, prob = reshape_fns.broadcast(self.obj, prob, keep_raw=[False, True])
            exits = nb.generate_rand_ex_by_prob_nb(
                reshape_fns.to_2d_array(obj),
                prob,
                wait,
                until_next,
                skip_until_exit,
                obj.ndim == 2,
                seed=seed
            )
            return ArrayWrapper.from_obj(obj).wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))
        exits = nb.generate_rand_ex_nb(
            self.to_2d_array(),
            wait,
            until_next,
            skip_until_exit,
            seed=seed
        )
        return self.wrapper.wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))

    def generate_stop_exits(self,
                            ts: tp.ArrayLike,
                            stop: tp.ArrayLike,
                            trailing: tp.ArrayLike = False,
                            entry_wait: int = 1,
                            exit_wait: int = 1,
                            until_next: bool = True,
                            skip_until_exit: bool = False,
                            pick_first: bool = True,
                            chain: bool = False,
                            broadcast_kwargs: tp.KwargsLike = None,
                            wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeTuple[tp.SeriesFrame]:
        """Generate exits based on when `ts` hits the stop.

        For arguments, see `vectorbt.signals.nb.stop_choice_nb`.
        If `chain` is True, see `vectorbt.signals.nb.generate_stop_enex_nb`.
        Otherwise, see `vectorbt.signals.nb.generate_stop_ex_nb`.

        Arguments `entries`, `ts` and `stop` will broadcast using `vectorbt.base.reshape_fns.broadcast`
        and `broadcast_kwargs`.

        For arguments, see `vectorbt.signals.nb.stop_choice_nb`.

        !!! hint
            Default arguments will generate an exit signal strictly between two entry signals.
            If both entry signals are too close to each other, no exit will be generated.

            To ignore all entries that come between an entry and its exit,
            set `until_next` to False and `skip_until_exit` to True.

            To remove all entries that come between an entry and its exit,
            set `chain` to True. This will return two arrays: new entries and exits.

        Usage:
            ```pycon
            >>> ts = pd.Series([1, 2, 3, 2, 1])

            >>> # stop loss
            >>> mask.vbt.signals.generate_stop_exits(ts, -0.1)
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02  False  False  False
            2020-01-03  False  False  False
            2020-01-04  False   True   True
            2020-01-05  False  False  False

            >>> # trailing stop loss
            >>> mask.vbt.signals.generate_stop_exits(ts, -0.1, trailing=True)
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02  False  False  False
            2020-01-03  False  False  False
            2020-01-04   True   True   True
            2020-01-05  False  False  False
            ```
        """
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        entries = self.obj

        keep_raw = (False, True, True, True)
        broadcast_kwargs = merge_dicts(dict(require_kwargs=dict(requirements='W')), broadcast_kwargs)
        entries, ts, stop, trailing = reshape_fns.broadcast(
            entries, ts, stop, trailing, **broadcast_kwargs, keep_raw=keep_raw)

        # Perform generation
        if chain:
            new_entries, exits = nb.generate_stop_enex_nb(
                reshape_fns.to_2d_array(entries),
                ts,
                stop,
                trailing,
                entry_wait,
                exit_wait,
                pick_first,
                entries.ndim == 2
            )
            return ArrayWrapper.from_obj(entries).wrap(new_entries, group_by=False, **merge_dicts({}, wrap_kwargs)), \
                   ArrayWrapper.from_obj(entries).wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))
        else:
            if skip_until_exit and until_next:
                warnings.warn("skip_until_exit=True has only effect when until_next=False", stacklevel=2)
            exits = nb.generate_stop_ex_nb(
                reshape_fns.to_2d_array(entries),
                ts,
                stop,
                trailing,
                exit_wait,
                until_next,
                skip_until_exit,
                pick_first,
                entries.ndim == 2
            )
            return ArrayWrapper.from_obj(entries).wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))

    def generate_ohlc_stop_exits(self,
                                 open: tp.ArrayLike,
                                 high: tp.Optional[tp.ArrayLike] = None,
                                 low: tp.Optional[tp.ArrayLike] = None,
                                 close: tp.Optional[tp.ArrayLike] = None,
                                 is_open_safe: bool = True,
                                 out_dict: tp.Optional[tp.Dict[str, tp.ArrayLike]] = None,
                                 sl_stop: tp.ArrayLike = np.nan,
                                 sl_trail: tp.ArrayLike = False,
                                 tp_stop: tp.ArrayLike = np.nan,
                                 reverse: tp.ArrayLike = False,
                                 entry_wait: int = 1,
                                 exit_wait: int = 1,
                                 until_next: bool = True,
                                 skip_until_exit: bool = False,
                                 pick_first: bool = True,
                                 chain: bool = False,
                                 broadcast_kwargs: tp.KwargsLike = None,
                                 wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeTuple[tp.SeriesFrame]:
        """Generate exits based on when the price hits (trailing) stop loss or take profit.

        !!! hint
            This function is meant for signal analysis. For backtesting, consider using
            the stop logic integrated into `vectorbt.portfolio.base.Portfolio.from_signals`.

        If any of `high`, `low` or `close` is None, it will be set to `open`.

        Use `out_dict` as a dict to pass `stop_price` and `stop_type` arrays. You can also
        set `out_dict` to {} to produce these arrays automatically and still have access to them.

        For arguments, see `vectorbt.signals.nb.ohlc_stop_choice_nb`.
        If `chain` is True, see `vectorbt.signals.nb.generate_ohlc_stop_enex_nb`.
        Otherwise, see `vectorbt.signals.nb.generate_ohlc_stop_ex_nb`.

        All array-like arguments including stops and `out_dict` will broadcast using
        `vectorbt.base.reshape_fns.broadcast` and `broadcast_kwargs`.

        For arguments, see `vectorbt.signals.nb.ohlc_stop_choice_nb`.

        !!! note
            `open` isn't necessarily open price, but can be any entry price (even previous close).
            Stop price is calculated based solely on the entry price.

        !!! hint
            Default arguments will generate an exit signal strictly between two entry signals.
            If both entry signals are too close to each other, no exit will be generated.

            To ignore all entries that come between an entry and its exit,
            set `until_next` to False and `skip_until_exit` to True.

            To remove all entries that come between an entry and its exit,
            set `chain` to True. This will return two arrays: new entries and exits.

        Usage:
            * The same example as under `vectorbt.signals.nb.generate_ohlc_stop_ex_nb`:

            ```pycon
            >>> from vectorbt.signals.enums import StopType

            >>> price = pd.DataFrame({
            ...     'open': [10, 11, 12, 11, 10],
            ...     'high': [11, 12, 13, 12, 11],
            ...     'low': [9, 10, 11, 10, 9],
            ...     'close': [10, 11, 12, 11, 10]
            ... })
            >>> out_dict = {}
            >>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
            ...     price['open'], price['high'], price['low'], price['close'],
            ...     sl_stop=0.1, sl_trail=True, tp_stop=0.1, out_dict=out_dict)
            >>> exits
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True   True  False
            2020-01-03  False  False  False
            2020-01-04  False   True   True
            2020-01-05  False  False  False

            >>> out_dict['stop_price']
                           a     b     c
            2020-01-01   NaN   NaN   NaN
            2020-01-02  11.0  11.0   NaN
            2020-01-03   NaN   NaN   NaN
            2020-01-04   NaN  10.8  10.8
            2020-01-05   NaN   NaN   NaN

            >>> out_dict['stop_type'].vbt(mapping=StopType).apply_mapping()
                                 a           b          c
            2020-01-01        None        None       None
            2020-01-02  TakeProfit  TakeProfit       None
            2020-01-03        None        None       None
            2020-01-04        None   TrailStop  TrailStop
            2020-01-05        None        None       None
            ```

            Notice how the first two entry signals in the third column have no exit signal - there is
            no room between them for an exit signal.

            * To find an exit for the first entry and ignore all entries that are in-between them,
            we can pass `until_next=False` and `skip_until_exit=True`:

            ```pycon
            >>> out_dict = {}
            >>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
            ...     price['open'], price['high'], price['low'], price['close'],
            ...     sl_stop=0.1, sl_trail=True, tp_stop=0.1, out_dict=out_dict,
            ...     until_next=False, skip_until_exit=True)
            >>> exits
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True   True   True
            2020-01-03  False  False  False
            2020-01-04  False   True   True
            2020-01-05  False  False  False

            >>> out_dict['stop_price']
            2020-01-01   NaN   NaN   NaN
            2020-01-02  11.0  11.0  11.0
            2020-01-03   NaN   NaN   NaN
            2020-01-04   NaN  10.8  10.8
            2020-01-05   NaN   NaN   NaN

            >>> out_dict['stop_type'].vbt(mapping=StopType).apply_mapping()
                                 a           b           c
            2020-01-01        None        None        None
            2020-01-02  TakeProfit  TakeProfit  TakeProfit
            2020-01-03        None        None        None
            2020-01-04        None   TrailStop   TrailStop
            2020-01-05        None        None        None
            ```

            Now, the first signal in the third column gets executed regardless of the entries that come next,
            which is very similar to the logic that is implemented in `vectorbt.portfolio.base.Portfolio.from_signals`.

            * To automatically remove all ignored entry signals, pass `chain=True`.
            This will return a new entries array:

            ```pycon
            >>> out_dict = {}
            >>> new_entries, exits = mask.vbt.signals.generate_ohlc_stop_exits(
            ...     price['open'], price['high'], price['low'], price['close'],
            ...     sl_stop=0.1, sl_trail=True, tp_stop=0.1, out_dict=out_dict,
            ...     chain=True)
            >>> new_entries
                            a      b      c
            2020-01-01   True   True   True
            2020-01-02  False  False  False  << removed entry in the third column
            2020-01-03  False   True   True
            2020-01-04  False  False  False
            2020-01-05  False   True  False
            >>> exits
                            a      b      c
            2020-01-01  False  False  False
            2020-01-02   True   True   True
            2020-01-03  False  False  False
            2020-01-04  False   True   True
            2020-01-05  False  False  False
            ```

            !!! warning
                The last two examples above make entries dependent upon exits - this makes only sense
                if you have no other exit arrays to combine this stop exit array with.
        """
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        entries = self.obj
        if high is None:
            high = open
        if low is None:
            low = open
        if close is None:
            close = open
        if out_dict is None:
            out_dict_passed = False
            out_dict = {}
        else:
            out_dict_passed = True
        stop_price_out = out_dict.get('stop_price', np.nan if out_dict_passed else None)
        stop_type_out = out_dict.get('stop_type', -1 if out_dict_passed else None)
        out_args = ()
        if stop_price_out is not None:
            out_args += (stop_price_out,)
        if stop_type_out is not None:
            out_args += (stop_type_out,)

        keep_raw = (False, True, True, True, True, True, True, True, True) + (False,) * len(out_args)
        broadcast_kwargs = merge_dicts(dict(require_kwargs=dict(requirements='W')), broadcast_kwargs)
        entries, open, high, low, close, sl_stop, sl_trail, tp_stop, reverse, *out_args = reshape_fns.broadcast(
            entries, open, high, low, close, sl_stop, sl_trail, tp_stop, reverse, *out_args,
            **broadcast_kwargs, keep_raw=keep_raw)
        if stop_price_out is None:
            stop_price_out = np.empty_like(entries, dtype=np.float64)
        else:
            stop_price_out = out_args[0]
            out_args = out_args[1:]
        if stop_type_out is None:
            stop_type_out = np.empty_like(entries, dtype=np.int64)
        else:
            stop_type_out = out_args[0]
        stop_price_out = reshape_fns.to_2d_array(stop_price_out)
        stop_type_out = reshape_fns.to_2d_array(stop_type_out)

        # Perform generation
        if chain:
            new_entries, exits = nb.generate_ohlc_stop_enex_nb(
                reshape_fns.to_2d_array(entries),
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
                entry_wait,
                exit_wait,
                pick_first,
                entries.ndim == 2
            )
            out_dict['stop_price'] = ArrayWrapper.from_obj(entries).wrap(
                stop_price_out, group_by=False, **merge_dicts({}, wrap_kwargs))
            out_dict['stop_type'] = ArrayWrapper.from_obj(entries).wrap(
                stop_type_out, group_by=False, **merge_dicts({}, wrap_kwargs))
            return ArrayWrapper.from_obj(entries).wrap(new_entries, group_by=False, **merge_dicts({}, wrap_kwargs)), \
                   ArrayWrapper.from_obj(entries).wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))
        else:
            if skip_until_exit and until_next:
                warnings.warn("skip_until_exit=True has only effect when until_next=False", stacklevel=2)
            exits = nb.generate_ohlc_stop_ex_nb(
                reshape_fns.to_2d_array(entries),
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
                until_next,
                skip_until_exit,
                pick_first,
                entries.ndim == 2
            )
            out_dict['stop_price'] = ArrayWrapper.from_obj(entries).wrap(
                stop_price_out, group_by=False, **merge_dicts({}, wrap_kwargs))
            out_dict['stop_type'] = ArrayWrapper.from_obj(entries).wrap(
                stop_type_out, group_by=False, **merge_dicts({}, wrap_kwargs))
            return ArrayWrapper.from_obj(entries).wrap(exits, group_by=False, **merge_dicts({}, wrap_kwargs))

    # ############# Ranges ############# #

    def between_ranges(self,
                       other: tp.Optional[tp.ArrayLike] = None,
                       from_other: bool = False,
                       broadcast_kwargs: tp.KwargsLike = None,
                       group_by: tp.GroupByLike = None,
                       attach_ts: bool = True,
                       attach_other: bool = False,
                       **kwargs) -> Ranges:
        """Wrap the result of `vectorbt.signals.nb.between_ranges_nb`
        with `vectorbt.generic.ranges.Ranges`.

        If `other` specified, see `vectorbt.signals.nb.between_two_ranges_nb`.
        Both will broadcast using `vectorbt.base.reshape_fns.broadcast` and `broadcast_kwargs`.

        Usage:
            * One array:

            ```pycon
            >>> mask_sr = pd.Series([True, False, False, True, False, True, True])
            >>> ranges = mask_sr.vbt.signals.between_ranges()
            >>> ranges
            <vectorbt.generic.ranges.Ranges at 0x7ff29ea7c7b8>

            >>> ranges.records_readable
               Range Id  Column  Start Timestamp  End Timestamp  Status
            0         0       0                0              3  Closed
            1         1       0                3              5  Closed
            2         2       0                5              6  Closed

            >>> ranges.duration.values
            array([3, 2, 1])
            ```

            * Two arrays, traversing the signals of the first array:

            ```pycon
            >>> mask_sr = pd.Series([True, True, True, False, False])
            >>> mask_sr2 = pd.Series([False, False, True, False, True])
            >>> ranges = mask_sr.vbt.signals.between_ranges(other=mask_sr2)
            >>> ranges
            <vectorbt.generic.ranges.Ranges at 0x7ff29e3b80f0>

            >>> ranges.records_readable
               Range Id  Column  Start Timestamp  End Timestamp  Status
            0         0       0                0              2  Closed
            1         1       0                1              2  Closed
            2         2       0                2              2  Closed

            >>> ranges.duration.values
            array([2, 1, 0])
            ```

            * Two arrays, traversing the signals of the second array:

            ```pycon
            >>> ranges = mask_sr.vbt.signals.between_ranges(other=mask_sr2, from_other=True)
            >>> ranges
            <vectorbt.generic.ranges.Ranges at 0x7ff29eccbd68>

            >>> ranges.records_readable
               Range Id  Column  Start Timestamp  End Timestamp  Status
            0         0       0                2              2  Closed
            1         1       0                2              4  Closed

            >>> ranges.duration.values
            array([0, 2])
            ```
        """
        if broadcast_kwargs is None:
            broadcast_kwargs = {}

        if other is None:
            # One input array
            range_records = nb.between_ranges_nb(self.to_2d_array())
            wrapper = self.wrapper
            to_attach = self.obj
        else:
            # Two input arrays
            obj, other = reshape_fns.broadcast(self.obj, other, **broadcast_kwargs)
            range_records = nb.between_two_ranges_nb(
                reshape_fns.to_2d_array(obj),
                reshape_fns.to_2d_array(other),
                from_other=from_other
            )
            wrapper = ArrayWrapper.from_obj(obj)
            to_attach = other if attach_other else obj
        return Ranges(
            wrapper,
            range_records,
            ts=to_attach if attach_ts else None,
            **kwargs
        ).regroup(group_by)

    def partition_ranges(self, group_by: tp.GroupByLike = None, attach_ts: bool = True, **kwargs) -> Ranges:
        """Wrap the result of `vectorbt.signals.nb.partition_ranges_nb`
        with `vectorbt.generic.ranges.Ranges`.

        If `use_end_idxs` is True, uses the index of the last signal in each partition as `idx_arr`.
        Otherwise, uses the index of the first signal.

        Usage:
            ```pycon
            >>> mask_sr = pd.Series([True, True, True, False, True, True])
            >>> mask_sr.vbt.signals.partition_ranges().records_readable
               Range Id  Column  Start Timestamp  End Timestamp  Status
            0         0       0                0              3  Closed
            1         1       0                4              5    Open
            ```
        """
        range_records = nb.partition_ranges_nb(self.to_2d_array())
        return Ranges(
            self.wrapper,
            range_records,
            ts=self.obj if attach_ts else None,
            **kwargs
        ).regroup(group_by)

    def between_partition_ranges(self, group_by: tp.GroupByLike = None, attach_ts: bool = True, **kwargs) -> Ranges:
        """Wrap the result of `vectorbt.signals.nb.between_partition_ranges_nb`
        with `vectorbt.generic.ranges.Ranges`.

        Usage:
            ```pycon
            >>> mask_sr = pd.Series([True, False, False, True, False, True, True])
            >>> mask_sr.vbt.signals.between_partition_ranges().records_readable
               Range Id  Column  Start Timestamp  End Timestamp  Status
            0         0       0                0              3  Closed
            1         1       0                3              5  Closed
            ```
        """
        range_records = nb.between_partition_ranges_nb(self.to_2d_array())
        return Ranges(
            self.wrapper,
            range_records,
            ts=self.obj if attach_ts else None,
            **kwargs
        ).regroup(group_by)

    # ############# Ranking ############# #

    def rank(self,
             rank_func_nb: tp.RankFunc, *args,
             prepare_func: tp.Optional[tp.Callable] = None,
             reset_by: tp.Optional[tp.ArrayLike] = None,
             after_false: bool = False,
             broadcast_kwargs: tp.KwargsLike = None,
             wrap_kwargs: tp.KwargsLike = None,
             as_mapped: bool = False,
             **kwargs) -> tp.Union[tp.SeriesFrame, MappedArray]:
        """See `vectorbt.signals.nb.rank_nb`.

        Will broadcast with `reset_by` using `vectorbt.base.reshape_fns.broadcast` and `broadcast_kwargs`.

        Use `prepare_func` to prepare further arguments to be passed before `*args`, such as temporary arrays.
        It should take both broadcasted arrays (`reset_by` can be None) and return a tuple.

        Set `as_mapped` to True to return an instance of `vectorbt.records.mapped_array.MappedArray`."""
        checks.assert_not_none(rank_func_nb)
        checks.assert_numba_func(rank_func_nb)
        if broadcast_kwargs is None:
            broadcast_kwargs = {}

        if reset_by is not None:
            obj, reset_by = reshape_fns.broadcast(self.obj, reset_by, **broadcast_kwargs)
            reset_by = reshape_fns.to_2d_array(reset_by)
        else:
            obj = self.obj
        obj_arr = reshape_fns.to_2d_array(obj)
        if prepare_func is not None:
            temp_arrs = prepare_func(obj_arr, reset_by)
        else:
            temp_arrs = ()
        rank = nb.rank_nb(
            obj_arr,
            reset_by,
            after_false,
            rank_func_nb,
            *temp_arrs,
            *args
        )
        rank_wrapped = ArrayWrapper.from_obj(obj).wrap(rank, group_by=False, **merge_dicts({}, wrap_kwargs))
        if as_mapped:
            rank_wrapped = rank_wrapped.replace(-1, np.nan)
            return rank_wrapped.vbt.to_mapped(
                dropna=True,
                dtype=np.int64,
                **kwargs
            )
        return rank_wrapped

    def pos_rank(self, allow_gaps: bool = False, **kwargs) -> tp.Union[tp.SeriesFrame, MappedArray]:
        """Get signal position ranks.

        Uses `SignalsAccessor.rank` with `vectorbt.signals.nb.sig_pos_rank_nb`.

        Usage:
            * Rank each True value in each partition in `mask`:

            ```pycon
            >>> mask.vbt.signals.pos_rank()
                        a  b  c
            2020-01-01  0  0  0
            2020-01-02 -1 -1  1
            2020-01-03 -1  0  2
            2020-01-04 -1 -1 -1
            2020-01-05 -1  0 -1

            >>> mask.vbt.signals.pos_rank(after_false=True)
                        a  b  c
            2020-01-01 -1 -1 -1
            2020-01-02 -1 -1 -1
            2020-01-03 -1  0 -1
            2020-01-04 -1 -1 -1
            2020-01-05 -1  0 -1

            >>> mask.vbt.signals.pos_rank(allow_gaps=True)
                        a  b  c
            2020-01-01  0  0  0
            2020-01-02 -1 -1  1
            2020-01-03 -1  1  2
            2020-01-04 -1 -1 -1
            2020-01-05 -1  2 -1

            >>> mask.vbt.signals.pos_rank(reset_by=~mask, allow_gaps=True)
                        a  b  c
            2020-01-01  0  0  0
            2020-01-02 -1 -1  1
            2020-01-03 -1  0  2
            2020-01-04 -1 -1 -1
            2020-01-05 -1  0 -1
            ```
        """
        prepare_func = lambda obj, reset_by: (np.full(obj.shape[1], -1, dtype=np.int64),)
        return self.rank(
            nb.sig_pos_rank_nb,
            allow_gaps,
            prepare_func=prepare_func,
            **kwargs
        )

    def partition_pos_rank(self, **kwargs) -> tp.Union[tp.SeriesFrame, MappedArray]:
        """Get partition position ranks.

        Uses `SignalsAccessor.rank` with `vectorbt.signals.nb.part_pos_rank_nb`.

        Usage:
            * Rank each partition of True values in `mask`:

            ```pycon
            >>> mask.vbt.signals.partition_pos_rank()
                        a  b  c
            2020-01-01  0  0  0
            2020-01-02 -1 -1  0
            2020-01-03 -1  1  0
            2020-01-04 -1 -1 -1
            2020-01-05 -1  2 -1

            >>> mask.vbt.signals.partition_pos_rank(after_false=True)
                        a  b  c
            2020-01-01 -1 -1 -1
            2020-01-02 -1 -1 -1
            2020-01-03 -1  0 -1
            2020-01-04 -1 -1 -1
            2020-01-05 -1  1 -1

            >>> mask.vbt.signals.partition_pos_rank(reset_by=mask)
                        a  b  c
            2020-01-01  0  0  0
            2020-01-02 -1 -1  0
            2020-01-03 -1  0  0
            2020-01-04 -1 -1 -1
            2020-01-05 -1  0 -1
            ```
        """
        prepare_func = lambda obj, reset_by: (np.full(obj.shape[1], -1, dtype=np.int64),)
        return self.rank(
            nb.part_pos_rank_nb,
            prepare_func=prepare_func,
            **kwargs
        )

    def first(self, wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.SeriesFrame:
        """Select signals that satisfy the condition `pos_rank == 0`."""
        pos_rank = self.pos_rank(**kwargs).values
        return self.wrapper.wrap(pos_rank == 0, group_by=False, **merge_dicts({}, wrap_kwargs))

    def nth(self, n: int, wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.SeriesFrame:
        """Select signals that satisfy the condition `pos_rank == n`."""
        pos_rank = self.pos_rank(**kwargs).values
        return self.wrapper.wrap(pos_rank == n, group_by=False, **merge_dicts({}, wrap_kwargs))

    def from_nth(self, n: int, wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.SeriesFrame:
        """Select signals that satisfy the condition `pos_rank >= n`."""
        pos_rank = self.pos_rank(**kwargs).values
        return self.wrapper.wrap(pos_rank >= n, group_by=False, **merge_dicts({}, wrap_kwargs))

    def pos_rank_mapped(self, group_by: tp.GroupByLike = None, **kwargs) -> MappedArray:
        """Get a mapped array of signal position ranks.

        See `SignalsAccessor.pos_rank`."""
        return self.pos_rank(as_mapped=True, group_by=group_by, **kwargs)

    def partition_pos_rank_mapped(self, group_by: tp.GroupByLike = None, **kwargs) -> MappedArray:
        """Get a mapped array of partition position ranks.

        See `SignalsAccessor.partition_pos_rank`."""
        return self.partition_pos_rank(as_mapped=True, group_by=group_by, **kwargs)

    # ############# Index ############# #

    def nth_index(self, n: int, return_labels: bool = True, group_by: tp.GroupByLike = None,
                  wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """See `vectorbt.signals.nb.nth_index_nb`.

        Usage:
            ```pycon
            >>> mask.vbt.signals.nth_index(0)
            a   2020-01-01
            b   2020-01-01
            c   2020-01-01
            Name: nth_index, dtype: datetime64[ns]

            >>> mask.vbt.signals.nth_index(2)
            a          NaT
            b   2020-01-05
            c   2020-01-03
            Name: nth_index, dtype: datetime64[ns]

            >>> mask.vbt.signals.nth_index(-1)
            a   2020-01-01
            b   2020-01-05
            c   2020-01-03
            Name: nth_index, dtype: datetime64[ns]

            >>> mask.vbt.signals.nth_index(-1, group_by=True)
            Timestamp('2020-01-05 00:00:00')
            ```
        """
        if self.is_frame() and self.wrapper.grouper.is_grouped(group_by=group_by):
            squeezed = self.squeeze_grouped(generic_nb.any_squeeze_nb, group_by=group_by)
            arr = reshape_fns.to_2d_array(squeezed)
        else:
            arr = self.to_2d_array()
        nth_index = nb.nth_index_nb(arr, n)
        if return_labels:
            minus_one_mask = nth_index == -1
            nth_index = nth_index.astype(object)
            nth_index[minus_one_mask] = np.nan
            nth_index[~minus_one_mask] = self.wrapper.index[nth_index[~minus_one_mask].astype(np.int64)]
        wrap_kwargs = merge_dicts(dict(name_or_index='nth_index'), wrap_kwargs)
        return self.wrapper.wrap_reduced(nth_index, group_by=group_by, **wrap_kwargs)

    def norm_avg_index(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """See `vectorbt.signals.nb.norm_avg_index_nb`.

        Normalized average index measures the average signal location relative to the middle of the column.
        This way, we can quickly see where the majority of signals are located.

        Common values are:

        * -1.0: only the first signal is set
        * 1.0: only the last signal is set
        * 0.0: symmetric distribution around the middle
        * [-1.0, 0.0): average signal is on the left
        * (0.0, 1.0]: average signal is on the right

        Usage:
            ```pycon
            >>> pd.Series([True, False, False, False]).vbt.signals.norm_avg_index()
            -1.0

            >>> pd.Series([False, False, False, True]).vbt.signals.norm_avg_index()
            1.0

            >>> pd.Series([True, False, False, True]).vbt.signals.norm_avg_index()
            0.0
            ```
        """
        norm_avg_index = nb.norm_avg_index_nb(self.to_2d_array())
        wrap_kwargs = merge_dicts(dict(name_or_index='norm_avg_index'), wrap_kwargs)
        norm_avg_index = self.wrapper.wrap_reduced(norm_avg_index, group_by=False, **wrap_kwargs)
        if self.is_frame() and self.wrapper.grouper.is_grouped(group_by=group_by):
            # Group index is a weighted average of column indexes in the group
            if group_by is None:
                group_by = self.wrapper.grouper.group_by
            col_total = self.total(group_by=False)
            norm_avg_index *= col_total
            norm_avg_index = norm_avg_index.vbt.squeeze_grouped(
                generic_nb.sum_squeeze_nb, group_by=group_by)
            group_total = col_total.vbt.squeeze_grouped(
                generic_nb.sum_squeeze_nb, group_by=group_by)
            norm_avg_index /= group_total
        return norm_avg_index

    def index_mapped(self, group_by: tp.GroupByLike = None, **kwargs) -> MappedArray:
        """Get a mapped array of indices.

        See `vectorbt.generic.accessors.GenericAccessor.to_mapped`.

        Only True values will be considered."""
        indices = np.arange(len(self.wrapper.index), dtype=np.float64)[:, None]
        indices = np.tile(indices, (1, len(self.wrapper.columns)))
        indices = reshape_fns.soft_to_ndim(indices, self.wrapper.ndim)
        indices[~self.obj.values] = np.nan
        return self.wrapper.wrap(indices).vbt.to_mapped(
            dropna=True,
            dtype=np.int64,
            group_by=group_by,
            **kwargs
        )

    def total(self, wrap_kwargs: tp.KwargsLike = None,
              group_by: tp.GroupByLike = None) -> tp.MaybeSeries:
        """Total number of True values in each column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='total'), wrap_kwargs)
        return self.sum(group_by=group_by, wrap_kwargs=wrap_kwargs)

    def rate(self, wrap_kwargs: tp.KwargsLike = None,
             group_by: tp.GroupByLike = None, **kwargs) -> tp.MaybeSeries:
        """`SignalsAccessor.total` divided by the total index length in each column/group."""
        total = reshape_fns.to_1d_array(self.total(group_by=group_by, **kwargs))
        wrap_kwargs = merge_dicts(dict(name_or_index='rate'), wrap_kwargs)
        total_steps = self.wrapper.grouper.get_group_lens(group_by=group_by) * self.wrapper.shape[0]
        return self.wrapper.wrap_reduced(total / total_steps, group_by=group_by, **wrap_kwargs)

    def total_partitions(self, wrap_kwargs: tp.KwargsLike = None,
                         group_by: tp.GroupByLike = None, **kwargs) -> tp.MaybeSeries:
        """Total number of partitions of True values in each column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='total_partitions'), wrap_kwargs)
        return self.partition_ranges(**kwargs).count(group_by=group_by, wrap_kwargs=wrap_kwargs)

    def partition_rate(self, wrap_kwargs: tp.KwargsLike = None,
                       group_by: tp.GroupByLike = None, **kwargs) -> tp.MaybeSeries:
        """`SignalsAccessor.total_partitions` divided by `SignalsAccessor.total` in each column/group."""
        total_partitions = reshape_fns.to_1d_array(self.total_partitions(group_by=group_by, *kwargs))
        total = reshape_fns.to_1d_array(self.total(group_by=group_by, *kwargs))
        wrap_kwargs = merge_dicts(dict(name_or_index='partition_rate'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_partitions / total, group_by=group_by, **wrap_kwargs)

    # ############# Logical operations ############# #

    def AND(self, other: tp.ArrayLike, **kwargs) -> tp.SeriesFrame:
        """Combine with `other` using logical AND.

        See `vectorbt.base.accessors.BaseAccessor.combine`.

        """
        return self.combine(other, combine_func=np.logical_and, **kwargs)

    def OR(self, other: tp.ArrayLike, **kwargs) -> tp.SeriesFrame:
        """Combine with `other` using logical OR.

        See `vectorbt.base.accessors.BaseAccessor.combine`.

        Usage:
            * Perform two OR operations and concatenate them:

            ```pycon
            >>> ts = pd.Series([1, 2, 3, 2, 1])
            >>> mask.vbt.signals.OR([ts > 1, ts > 2], concat=True, keys=['>1', '>2'])
                                        >1                   >2
                            a     b      c      a      b      c
            2020-01-01   True  True   True   True   True   True
            2020-01-02   True  True   True  False  False   True
            2020-01-03   True  True   True   True   True   True
            2020-01-04   True  True   True  False  False  False
            2020-01-05  False  True  False  False   True  False
            ```
        """
        return self.combine(other, combine_func=np.logical_or, **kwargs)

    def XOR(self, other: tp.ArrayLike, **kwargs) -> tp.SeriesFrame:
        """Combine with `other` using logical XOR.

        See `vectorbt.base.accessors.BaseAccessor.combine`."""
        return self.combine(other, combine_func=np.logical_xor, **kwargs)

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `SignalsAccessor.stats`.

        Merges `vectorbt.generic.accessors.GenericAccessor.stats_defaults` and
        `signals.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        signals_stats_cfg = settings['signals']['stats']

        return merge_dicts(
            GenericAccessor.stats_defaults.__get__(self),
            signals_stats_cfg
        )

    _metrics: tp.ClassVar[Config] = Config(
        dict(
            start=dict(
                title='Start',
                calc_func=lambda self: self.wrapper.index[0],
                agg_func=None,
                tags='wrapper'
            ),
            end=dict(
                title='End',
                calc_func=lambda self: self.wrapper.index[-1],
                agg_func=None,
                tags='wrapper'
            ),
            period=dict(
                title='Period',
                calc_func=lambda self: len(self.wrapper.index),
                apply_to_timedelta=True,
                agg_func=None,
                tags='wrapper'
            ),
            total=dict(
                title='Total',
                calc_func='total',
                tags='signals'
            ),
            rate=dict(
                title='Rate [%]',
                calc_func='rate',
                post_calc_func=lambda self, out, settings: out * 100,
                tags='signals'
            ),
            total_overlapping=dict(
                title='Total Overlapping',
                calc_func=lambda self, other, group_by:
                (self & other).vbt.signals.total(group_by=group_by),
                check_silent_has_other=True,
                tags=['signals', 'other']
            ),
            overlapping_rate=dict(
                title='Overlapping Rate [%]',
                calc_func=lambda self, other, group_by:
                (self & other).vbt.signals.total(group_by=group_by) /
                (self | other).vbt.signals.total(group_by=group_by),
                post_calc_func=lambda self, out, settings: out * 100,
                check_silent_has_other=True,
                tags=['signals', 'other']
            ),
            first_index=dict(
                title='First Index',
                calc_func='nth_index',
                n=0,
                return_labels=True,
                tags=['signals', 'index']
            ),
            last_index=dict(
                title='Last Index',
                calc_func='nth_index',
                n=-1,
                return_labels=True,
                tags=['signals', 'index']
            ),
            norm_avg_index=dict(
                title='Norm Avg Index [-1, 1]',
                calc_func='norm_avg_index',
                tags=['signals', 'index']
            ),
            distance=dict(
                title=RepEval("f'Distance {\"<-\" if from_other else \"->\"} {other_name}' "
                              "if other is not None else 'Distance'"),
                calc_func='between_ranges.duration',
                post_calc_func=lambda self, out, settings: {
                    'Min': out.min(),
                    'Max': out.max(),
                    'Mean': out.mean(),
                    'Std': out.std(ddof=settings.get('ddof', 1))
                },
                apply_to_timedelta=True,
                tags=RepEval("['signals', 'distance', 'other'] if other is not None else ['signals', 'distance']")
            ),
            total_partitions=dict(
                title='Total Partitions',
                calc_func='total_partitions',
                tags=['signals', 'partitions']
            ),
            partition_rate=dict(
                title='Partition Rate [%]',
                calc_func='partition_rate',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=['signals', 'partitions']
            ),
            partition_len=dict(
                title='Partition Length',
                calc_func='partition_ranges.duration',
                post_calc_func=lambda self, out, settings: {
                    'Min': out.min(),
                    'Max': out.max(),
                    'Mean': out.mean(),
                    'Std': out.std(ddof=settings.get('ddof', 1))
                },
                apply_to_timedelta=True,
                tags=['signals', 'partitions', 'distance']
            ),
            partition_distance=dict(
                title='Partition Distance',
                calc_func='between_partition_ranges.duration',
                post_calc_func=lambda self, out, settings: {
                    'Min': out.min(),
                    'Max': out.max(),
                    'Mean': out.mean(),
                    'Std': out.std(ddof=settings.get('ddof', 1))
                },
                apply_to_timedelta=True,
                tags=['signals', 'partitions', 'distance']
            ),
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def plot(self, yref: str = 'y', **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """Plot signals.

        Args:
            yref (str): Y coordinate axis.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericAccessor.lineplot`.

        Usage:
            ```pycon
            >>> mask[['a', 'c']].vbt.signals.plot()
            ```

            ![](/assets/images/signals_df_plot.svg)
        """
        default_layout = dict()
        default_layout['yaxis' + yref[1:]] = dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['false', 'true']
        )
        return self.obj.vbt.lineplot(**merge_dicts(default_layout, kwargs))

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `SignalsAccessor.plots`.

        Merges `vectorbt.generic.accessors.GenericAccessor.plots_defaults` and
        `signals.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        signals_plots_cfg = settings['signals']['plots']

        return merge_dicts(
            GenericAccessor.plots_defaults.__get__(self),
            signals_plots_cfg
        )

    @property
    def subplots(self) -> Config:
        return self._subplots


SignalsAccessor.override_metrics_doc(__pdoc__)
SignalsAccessor.override_subplots_doc(__pdoc__)


@register_series_vbt_accessor('signals')
class SignalsSRAccessor(SignalsAccessor, GenericSRAccessor):
    """Accessor on top of signal series. For Series only.

    Accessible through `pd.Series.vbt.signals`."""

    def __init__(self, obj: tp.Series, **kwargs) -> None:
        GenericSRAccessor.__init__(self, obj, **kwargs)
        SignalsAccessor.__init__(self, obj, **kwargs)

    def plot_as_markers(self, y: tp.Optional[tp.ArrayLike] = None,
                        **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """Plot Series as markers.

        Args:
            y (array_like): Y-axis values to plot markers on.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericAccessor.scatterplot`.

        Usage:
            ```pycon
            >>> ts = pd.Series([1, 2, 3, 2, 1], index=mask.index)
            >>> fig = ts.vbt.lineplot()
            >>> mask['b'].vbt.signals.plot_as_entry_markers(y=ts, fig=fig)
            >>> (~mask['b']).vbt.signals.plot_as_exit_markers(y=ts, fig=fig)
            ```

            ![](/assets/images/signals_plot_as_markers.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        if y is None:
            y = pd.Series.vbt.empty_like(self.obj, 1)
        else:
            y = reshape_fns.to_pd_array(y)

        return y[self.obj].vbt.scatterplot(**merge_dicts(dict(
            trace_kwargs=dict(
                marker=dict(
                    symbol='circle',
                    color=plotting_cfg['contrast_color_schema']['blue'],
                    size=7,
                    line=dict(
                        width=1,
                        color=adjust_lightness(plotting_cfg['contrast_color_schema']['blue'])
                    )
                )
            )
        ), kwargs))

    def plot_as_entry_markers(self, y: tp.Optional[tp.ArrayLike] = None,
                              **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """Plot signals as entry markers.

        See `SignalsSRAccessor.plot_as_markers`."""
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        return self.plot_as_markers(y=y, **merge_dicts(dict(
            trace_kwargs=dict(
                marker=dict(
                    symbol='triangle-up',
                    color=plotting_cfg['contrast_color_schema']['green'],
                    size=8,
                    line=dict(
                        width=1,
                        color=adjust_lightness(plotting_cfg['contrast_color_schema']['green'])
                    )
                ),
                name='Entry'
            )
        ), kwargs))

    def plot_as_exit_markers(self, y: tp.Optional[tp.ArrayLike] = None,
                             **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """Plot signals as exit markers.

        See `SignalsSRAccessor.plot_as_markers`."""
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        return self.plot_as_markers(y=y, **merge_dicts(dict(
            trace_kwargs=dict(
                marker=dict(
                    symbol='triangle-down',
                    color=plotting_cfg['contrast_color_schema']['red'],
                    size=8,
                    line=dict(
                        width=1,
                        color=adjust_lightness(plotting_cfg['contrast_color_schema']['red'])
                    )
                ),
                name='Exit'
            )
        ), kwargs))


@register_dataframe_vbt_accessor('signals')
class SignalsDFAccessor(SignalsAccessor, GenericDFAccessor):
    """Accessor on top of signal series. For DataFrames only.

    Accessible through `pd.DataFrame.vbt.signals`."""

    def __init__(self, obj: tp.Frame, **kwargs) -> None:
        GenericDFAccessor.__init__(self, obj, **kwargs)
        SignalsAccessor.__init__(self, obj, **kwargs)
