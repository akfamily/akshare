# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Custom pandas accessors for generic data.

Methods can be accessed as follows:

* `GenericSRAccessor` -> `pd.Series.vbt.*`
* `GenericDFAccessor` -> `pd.DataFrame.vbt.*`

```pycon
>>> import pandas as pd
>>> import vectorbt as vbt

>>> # vectorbt.generic.accessors.GenericAccessor.rolling_mean
>>> pd.Series([1, 2, 3, 4]).vbt.rolling_mean(2)
0    NaN
1    1.5
2    2.5
3    3.5
dtype: float64
```

The accessors inherit `vectorbt.base.accessors` and are inherited by more
specialized accessors, such as `vectorbt.signals.accessors` and `vectorbt.returns.accessors`.

!!! note
    Grouping is only supported by the methods that accept the `group_by` argument.

    Accessors do not utilize caching.

Run for the examples below:
    
```pycon
>>> import vectorbt as vbt
>>> import numpy as np
>>> import pandas as pd
>>> from numba import njit
>>> from datetime import datetime, timedelta

>>> df = pd.DataFrame({
...     'a': [1, 2, 3, 4, 5],
...     'b': [5, 4, 3, 2, 1],
...     'c': [1, 2, 3, 2, 1]
... }, index=pd.Index([
...     datetime(2020, 1, 1),
...     datetime(2020, 1, 2),
...     datetime(2020, 1, 3),
...     datetime(2020, 1, 4),
...     datetime(2020, 1, 5)
... ]))
>>> df
            a  b  c
2020-01-01  1  5  1
2020-01-02  2  4  2
2020-01-03  3  3  3
2020-01-04  4  2  2
2020-01-05  5  1  1

>>> index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(10)]
>>> sr = pd.Series(np.arange(len(index)), index=index)
>>> sr
2020-01-01    0
2020-01-02    1
2020-01-03    2
2020-01-04    3
2020-01-05    4
2020-01-06    5
2020-01-07    6
2020-01-08    7
2020-01-09    8
2020-01-10    9
dtype: int64
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `GenericAccessor.metrics`.

```pycon
>>> df2 = pd.DataFrame({
...     'a': [np.nan, 2, 3],
...     'b': [4, np.nan, 5],
...     'c': [6, 7, np.nan]
... }, index=['x', 'y', 'z'])

>>> df2.vbt(freq='d').stats(column='a')
Start                      x
End                        z
Period       3 days 00:00:00
Count                      2
Mean                     2.5
Std                 0.707107
Min                      2.0
Median                   2.5
Max                      3.0
Min Index                  y
Max Index                  z
Name: a, dtype: object
```

### Mapping

Mapping can be set both in `GenericAccessor` (preferred) and `GenericAccessor.stats`:

```pycon
>>> mapping = {x: 'test_' + str(x) for x in pd.unique(df2.values.flatten())}
>>> df2.vbt(freq='d', mapping=mapping).stats(column='a')
Start                                   x
End                                     z
Period                    3 days 00:00:00
Count                                   2
Value Counts: test_2.0                  1
Value Counts: test_3.0                  1
Value Counts: test_4.0                  0
Value Counts: test_5.0                  0
Value Counts: test_6.0                  0
Value Counts: test_7.0                  0
Value Counts: test_nan                  1
Name: a, dtype: object

>>> df2.vbt(freq='d').stats(column='a', settings=dict(mapping=mapping))
UserWarning: Changing the mapping will create a copy of this object.
Consider setting it upon object creation to re-use existing cache.

Start                                   x
End                                     z
Period                    3 days 00:00:00
Count                                   2
Value Counts: test_2.0                  1
Value Counts: test_3.0                  1
Value Counts: test_4.0                  0
Value Counts: test_5.0                  0
Value Counts: test_6.0                  0
Value Counts: test_7.0                  0
Value Counts: test_nan                  1
Name: a, dtype: object
```

Selecting a column before calling `stats` will consider uniques from this column only:

```pycon
>>> df2['a'].vbt(freq='d', mapping=mapping).stats()
Start                                   x
End                                     z
Period                    3 days 00:00:00
Count                                   2
Value Counts: test_2.0                  1
Value Counts: test_3.0                  1
Value Counts: test_nan                  1
Name: a, dtype: object
```

To include all keys from `mapping`, pass `incl_all_keys=True`:

>>> df2['a'].vbt(freq='d', mapping=mapping).stats(settings=dict(incl_all_keys=True))
Start                                   x
End                                     z
Period                    3 days 00:00:00
Count                                   2
Value Counts: test_2.0                  1
Value Counts: test_3.0                  1
Value Counts: test_4.0                  0
Value Counts: test_5.0                  0
Value Counts: test_6.0                  0
Value Counts: test_7.0                  0
Value Counts: test_nan                  1
Name: a, dtype: object
```

`GenericAccessor.stats` also supports (re-)grouping:

```pycon
>>> df2.vbt(freq='d').stats(column=0, group_by=[0, 0, 1])
Start                      x
End                        z
Period       3 days 00:00:00
Count                      4
Mean                     3.5
Std                 1.290994
Min                      2.0
Median                   3.5
Max                      5.0
Min Index                  y
Max Index                  z
Name: 0, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `GenericAccessor.subplots`.

`GenericAccessor` class has a single subplot based on `GenericAccessor.plot`:

```pycon
>>> df2.vbt.plots()
```

![](/assets/images/generic_plots.svg)
"""

import warnings

import numpy as np
import pandas as pd
from numba.typed import Dict
from scipy import stats
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import (
    Binarizer,
    MinMaxScaler,
    MaxAbsScaler,
    Normalizer,
    RobustScaler,
    StandardScaler,
    QuantileTransformer,
    PowerTransformer
)
from sklearn.utils.validation import check_is_fitted

from vectorbt import _typing as tp
from vectorbt.base import index_fns, reshape_fns
from vectorbt.base.accessors import BaseAccessor, BaseDFAccessor, BaseSRAccessor
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.generic import plotting, nb
from vectorbt.generic.decorators import attach_nb_methods, attach_transform_methods
from vectorbt.generic.drawdowns import Drawdowns
from vectorbt.generic.plots_builder import PlotsBuilderMixin
from vectorbt.generic.ranges import Ranges
from vectorbt.generic.splitters import SplitterT, RangeSplitter, RollingSplitter, ExpandingSplitter
from vectorbt.generic.stats_builder import StatsBuilderMixin
from vectorbt.records.mapped_array import MappedArray
from vectorbt.utils import checks
from vectorbt.utils.config import Config, merge_dicts, resolve_dict
from vectorbt.utils.figure import make_figure, make_subplots
from vectorbt.utils.mapping import apply_mapping, to_mapping

try:  # pragma: no cover
    import bottleneck as bn

    nanmean = bn.nanmean
    nanstd = bn.nanstd
    nansum = bn.nansum
    nanmax = bn.nanmax
    nanmin = bn.nanmin
    nanmedian = bn.nanmedian
    nanargmax = bn.nanargmax
    nanargmin = bn.nanargmin
except ImportError:
    # slower numpy
    nanmean = np.nanmean
    nanstd = np.nanstd
    nansum = np.nansum
    nanmax = np.nanmax
    nanmin = np.nanmin
    nanmedian = np.nanmedian
    nanargmax = np.nanargmax
    nanargmin = np.nanargmin

__pdoc__ = {}


class MetaGenericAccessor(type(StatsBuilderMixin), type(PlotsBuilderMixin)):
    pass


GenericAccessorT = tp.TypeVar("GenericAccessorT", bound="GenericAccessor")
SplitOutputT = tp.Union[tp.MaybeTuple[tp.Tuple[tp.Frame, tp.Index]], tp.BaseFigure]


class TransformerT(tp.Protocol):
    def __init__(self, **kwargs) -> None:
        ...

    def transform(self, *args, **kwargs) -> tp.Array2d:
        ...

    def fit_transform(self, *args, **kwargs) -> tp.Array2d:
        ...


nb_config = Config(
    {
        'shuffle': dict(func=nb.shuffle_nb, path='vectorbt.generic.nb.shuffle_nb'),
        'fillna': dict(func=nb.fillna_nb, path='vectorbt.generic.nb.fillna_nb'),
        'bshift': dict(func=nb.bshift_nb, path='vectorbt.generic.nb.bshift_nb'),
        'fshift': dict(func=nb.fshift_nb, path='vectorbt.generic.nb.fshift_nb'),
        'diff': dict(func=nb.diff_nb, path='vectorbt.generic.nb.diff_nb'),
        'pct_change': dict(func=nb.pct_change_nb, path='vectorbt.generic.nb.pct_change_nb'),
        'bfill': dict(func=nb.bfill_nb, path='vectorbt.generic.nb.bfill_nb'),
        'ffill': dict(func=nb.ffill_nb, path='vectorbt.generic.nb.ffill_nb'),
        'cumsum': dict(func=nb.nancumsum_nb, path='vectorbt.generic.nb.nancumsum_nb'),
        'cumprod': dict(func=nb.nancumprod_nb, path='vectorbt.generic.nb.nancumprod_nb'),
        'rolling_min': dict(func=nb.rolling_min_nb, path='vectorbt.generic.nb.rolling_min_nb'),
        'rolling_max': dict(func=nb.rolling_max_nb, path='vectorbt.generic.nb.rolling_max_nb'),
        'rolling_mean': dict(func=nb.rolling_mean_nb, path='vectorbt.generic.nb.rolling_mean_nb'),
        'expanding_min': dict(func=nb.expanding_min_nb, path='vectorbt.generic.nb.expanding_min_nb'),
        'expanding_max': dict(func=nb.expanding_max_nb, path='vectorbt.generic.nb.expanding_max_nb'),
        'expanding_mean': dict(func=nb.expanding_mean_nb, path='vectorbt.generic.nb.expanding_mean_nb'),
        'product': dict(func=nb.nanprod_nb, is_reducing=True, path='vectorbt.generic.nb.nanprod_nb')
    },
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['nb_config'] = f"""Config of Numba methods to be added to `GenericAccessor`.

```json
{nb_config.to_doc()}
```
"""

transform_config = Config(
    {
        'binarize': dict(
            transformer=Binarizer,
            docstring="See `sklearn.preprocessing.Binarizer`."
        ),
        'minmax_scale': dict(
            transformer=MinMaxScaler,
            docstring="See `sklearn.preprocessing.MinMaxScaler`."
        ),
        'maxabs_scale': dict(
            transformer=MaxAbsScaler,
            docstring="See `sklearn.preprocessing.MaxAbsScaler`."
        ),
        'normalize': dict(
            transformer=Normalizer,
            docstring="See `sklearn.preprocessing.Normalizer`."
        ),
        'robust_scale': dict(
            transformer=RobustScaler,
            docstring="See `sklearn.preprocessing.RobustScaler`."
        ),
        'scale': dict(
            transformer=StandardScaler,
            docstring="See `sklearn.preprocessing.StandardScaler`."
        ),
        'quantile_transform': dict(
            transformer=QuantileTransformer,
            docstring="See `sklearn.preprocessing.QuantileTransformer`."
        ),
        'power_transform': dict(
            transformer=PowerTransformer,
            docstring="See `sklearn.preprocessing.PowerTransformer`."
        )
    },
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['transform_config'] = f"""Config of transform methods to be added to `GenericAccessor`.

```json
{transform_config.to_doc()}
```
"""


@attach_nb_methods(nb_config)
@attach_transform_methods(transform_config)
class GenericAccessor(BaseAccessor, StatsBuilderMixin, PlotsBuilderMixin, metaclass=MetaGenericAccessor):
    """Accessor on top of data of any type. For both, Series and DataFrames.

    Accessible through `pd.Series.vbt` and `pd.DataFrame.vbt`."""

    def __init__(self, obj: tp.SeriesFrame, mapping: tp.Optional[tp.MappingLike] = None, **kwargs) -> None:
        BaseAccessor.__init__(self, obj, mapping=mapping, **kwargs)
        StatsBuilderMixin.__init__(self)
        PlotsBuilderMixin.__init__(self)

        if mapping is not None:
            if isinstance(mapping, str):
                if mapping.lower() == 'index':
                    mapping = self.wrapper.index
                elif mapping.lower() == 'columns':
                    mapping = self.wrapper.columns
            mapping = to_mapping(mapping)
        self._mapping = mapping

    @property
    def sr_accessor_cls(self) -> tp.Type["GenericSRAccessor"]:
        """Accessor class for `pd.Series`."""
        return GenericSRAccessor

    @property
    def df_accessor_cls(self) -> tp.Type["GenericDFAccessor"]:
        """Accessor class for `pd.DataFrame`."""
        return GenericDFAccessor

    @property
    def mapping(self) -> tp.Optional[tp.Mapping]:
        """Mapping."""
        return self._mapping

    def apply_mapping(self, **kwargs) -> tp.SeriesFrame:
        """See `vectorbt.utils.mapping.apply_mapping`."""
        return apply_mapping(self.obj, self.mapping, **kwargs)

    def rolling_std(self, window: int, minp: tp.Optional[int] = None, ddof: int = 1,
                    wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:  # pragma: no cover
        """See `vectorbt.generic.nb.rolling_std_nb`."""
        out = nb.rolling_std_nb(self.to_2d_array(), window, minp=minp, ddof=ddof)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def expanding_std(self, minp: tp.Optional[int] = 1, ddof: int = 1,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:  # pragma: no cover
        """See `vectorbt.generic.nb.expanding_std_nb`."""
        out = nb.expanding_std_nb(self.to_2d_array(), minp=minp, ddof=ddof)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def ewm_mean(self, span: int, minp: tp.Optional[int] = 0, adjust: bool = True,
                 wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:  # pragma: no cover
        """See `vectorbt.generic.nb.ewm_mean_nb`."""
        out = nb.ewm_mean_nb(self.to_2d_array(), span, minp=minp, adjust=adjust)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def ewm_std(self, span: int, minp: tp.Optional[int] = 0, adjust: bool = True, ddof: int = 1,
                wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:  # pragma: no cover
        """See `vectorbt.generic.nb.ewm_std_nb`."""
        out = nb.ewm_std_nb(self.to_2d_array(), span, minp=minp, adjust=adjust, ddof=ddof)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def apply_along_axis(self, apply_func_nb: tp.Union[tp.ApplyFunc, tp.RowApplyFunc], *args, axis: int = 0,
                         wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Apply a function `apply_func_nb` along an axis."""
        checks.assert_numba_func(apply_func_nb)

        if axis == 0:
            out = nb.apply_nb(self.to_2d_array(), apply_func_nb, *args)
        elif axis == 1:
            out = nb.row_apply_nb(self.to_2d_array(), apply_func_nb, *args)
        else:
            raise ValueError("Only axes 0 and 1 are supported")
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def rolling_apply(self, window: int, apply_func_nb: tp.Union[tp.RollApplyFunc, nb.tp.RollMatrixApplyFunc],
                      *args, minp: tp.Optional[int] = None, on_matrix: bool = False,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.rolling_apply_nb` and
        `vectorbt.generic.nb.rolling_matrix_apply_nb` for `on_matrix=True`.

        Usage:
            ```pycon
            >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
            >>> df.vbt.rolling_apply(3, mean_nb)
                          a    b         c
            2020-01-01  1.0  5.0  1.000000
            2020-01-02  1.5  4.5  1.500000
            2020-01-03  2.0  4.0  2.000000
            2020-01-04  3.0  3.0  2.333333
            2020-01-05  4.0  2.0  2.000000

            >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
            >>> df.vbt.rolling_apply(3, mean_matrix_nb, on_matrix=True)
                               a         b         c
            2020-01-01  2.333333  2.333333  2.333333
            2020-01-02  2.500000  2.500000  2.500000
            2020-01-03  2.666667  2.666667  2.666667
            2020-01-04  2.777778  2.777778  2.777778
            2020-01-05  2.666667  2.666667  2.666667
            ```
        """
        checks.assert_numba_func(apply_func_nb)

        if on_matrix:
            out = nb.rolling_matrix_apply_nb(self.to_2d_array(), window, minp, apply_func_nb, *args)
        else:
            out = nb.rolling_apply_nb(self.to_2d_array(), window, minp, apply_func_nb, *args)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def expanding_apply(self, apply_func_nb: tp.Union[tp.RollApplyFunc, nb.tp.RollMatrixApplyFunc],
                        *args, minp: tp.Optional[int] = 1, on_matrix: bool = False,
                        wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.expanding_apply_nb` and
        `vectorbt.generic.nb.expanding_matrix_apply_nb` for `on_matrix=True`.

        Usage:
            ```pycon
            >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
            >>> df.vbt.expanding_apply(mean_nb)
                          a    b    c
            2020-01-01  1.0  5.0  1.0
            2020-01-02  1.5  4.5  1.5
            2020-01-03  2.0  4.0  2.0
            2020-01-04  2.5  3.5  2.0
            2020-01-05  3.0  3.0  1.8

            >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
            >>> df.vbt.expanding_apply(mean_matrix_nb, on_matrix=True)
                               a         b         c
            2020-01-01  2.333333  2.333333  2.333333
            2020-01-02  2.500000  2.500000  2.500000
            2020-01-03  2.666667  2.666667  2.666667
            2020-01-04  2.666667  2.666667  2.666667
            2020-01-05  2.600000  2.600000  2.600000
            ```
        """
        checks.assert_numba_func(apply_func_nb)

        if on_matrix:
            out = nb.expanding_matrix_apply_nb(self.to_2d_array(), minp, apply_func_nb, *args)
        else:
            out = nb.expanding_apply_nb(self.to_2d_array(), minp, apply_func_nb, *args)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def groupby_apply(self, by: tp.PandasGroupByLike,
                      apply_func_nb: tp.Union[tp.GroupByApplyFunc, tp.GroupByMatrixApplyFunc],
                      *args, on_matrix: bool = False, wrap_kwargs: tp.KwargsLike = None,
                      **kwargs) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.groupby_apply_nb` and
        `vectorbt.generic.nb.groupby_matrix_apply_nb` for `on_matrix=True`.

        For `by`, see `pd.DataFrame.groupby`.

        Usage:
            ```pycon
            >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
            >>> df.vbt.groupby_apply([1, 1, 2, 2, 3], mean_nb)
                 a    b    c
            1  1.5  4.5  1.5
            2  3.5  2.5  2.5
            3  5.0  1.0  1.0

            >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
            >>> df.vbt.groupby_apply([1, 1, 2, 2, 3], mean_matrix_nb, on_matrix=True)
                      a         b         c
            1  2.500000  2.500000  2.500000
            2  2.833333  2.833333  2.833333
            3  2.333333  2.333333  2.333333
            ```
        """
        checks.assert_numba_func(apply_func_nb)

        regrouped = self.obj.groupby(by, axis=0, **kwargs)
        groups = Dict()
        for i, (k, v) in enumerate(regrouped.indices.items()):
            groups[i] = np.asarray(v)
        if on_matrix:
            out = nb.groupby_matrix_apply_nb(self.to_2d_array(), groups, apply_func_nb, *args)
        else:
            out = nb.groupby_apply_nb(self.to_2d_array(), groups, apply_func_nb, *args)
        wrap_kwargs = merge_dicts(dict(name_or_index=list(regrouped.indices.keys())), wrap_kwargs)
        return self.wrapper.wrap_reduced(out, group_by=False, **wrap_kwargs)

    def resample_apply(self, freq: tp.PandasFrequencyLike,
                       apply_func_nb: tp.Union[tp.GroupByApplyFunc, tp.GroupByMatrixApplyFunc],
                       *args, on_matrix: bool = False, wrap_kwargs: tp.KwargsLike = None,
                       **kwargs) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.groupby_apply_nb` and
        `vectorbt.generic.nb.groupby_matrix_apply_nb` for `on_matrix=True`.

        For `freq`, see `pd.DataFrame.resample`.

        Usage:
            ```pycon
            >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
            >>> df.vbt.resample_apply('2d', mean_nb)
                          a    b    c
            2020-01-01  1.5  4.5  1.5
            2020-01-03  3.5  2.5  2.5
            2020-01-05  5.0  1.0  1.0

            >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
            >>> df.vbt.resample_apply('2d', mean_matrix_nb, on_matrix=True)
                               a         b         c
            2020-01-01  2.500000  2.500000  2.500000
            2020-01-03  2.833333  2.833333  2.833333
            2020-01-05  2.333333  2.333333  2.333333
            ```
        """
        checks.assert_numba_func(apply_func_nb)

        resampled = self.obj.resample(freq, axis=0, **kwargs)
        groups = Dict()
        for i, (k, v) in enumerate(resampled.indices.items()):
            groups[i] = np.asarray(v)
        if on_matrix:
            out = nb.groupby_matrix_apply_nb(self.to_2d_array(), groups, apply_func_nb, *args)
        else:
            out = nb.groupby_apply_nb(self.to_2d_array(), groups, apply_func_nb, *args)
        out_obj = self.wrapper.wrap(out, group_by=False, index=list(resampled.indices.keys()))
        resampled_arr = np.full((resampled.ngroups, self.to_2d_array().shape[1]), np.nan)
        resampled_obj = self.wrapper.wrap(
            resampled_arr,
            index=resampled.asfreq().index,
            group_by=False,
            **merge_dicts({}, wrap_kwargs)
        )
        resampled_obj.loc[out_obj.index] = out_obj.values
        return resampled_obj

    def applymap(self, apply_func_nb: tp.ApplyMapFunc, *args,
                 wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.applymap_nb`.

        Usage:
            ```pycon
            >>> multiply_nb = njit(lambda i, col, a: a ** 2)
            >>> df.vbt.applymap(multiply_nb)
                           a     b    c
            2020-01-01   1.0  25.0  1.0
            2020-01-02   4.0  16.0  4.0
            2020-01-03   9.0   9.0  9.0
            2020-01-04  16.0   4.0  4.0
            2020-01-05  25.0   1.0  1.0
            ```
        """
        checks.assert_numba_func(apply_func_nb)

        out = nb.applymap_nb(self.to_2d_array(), apply_func_nb, *args)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def filter(self, filter_func_nb: tp.FilterFunc, *args,
               wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.filter_nb`.

        Usage:
            ```pycon
            >>> greater_nb = njit(lambda i, col, a: a > 2)
            >>> df.vbt.filter(greater_nb)
                          a    b    c
            2020-01-01  NaN  5.0  NaN
            2020-01-02  NaN  4.0  NaN
            2020-01-03  3.0  3.0  3.0
            2020-01-04  4.0  NaN  NaN
            2020-01-05  5.0  NaN  NaN
            ```
        """
        checks.assert_numba_func(filter_func_nb)

        out = nb.filter_nb(self.to_2d_array(), filter_func_nb, *args)
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    def apply_and_reduce(self, apply_func_nb: tp.ApplyFunc, reduce_func_nb: tp.ReduceFunc,
                         apply_args: tp.Optional[tuple] = None, reduce_args: tp.Optional[tuple] = None,
                         wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """See `vectorbt.generic.nb.apply_and_reduce_nb`.

        Usage:
            ```pycon
            >>> greater_nb = njit(lambda col, a: a[a > 2])
            >>> mean_nb = njit(lambda col, a: np.nanmean(a))
            >>> df.vbt.apply_and_reduce(greater_nb, mean_nb)
            a    4.0
            b    4.0
            c    3.0
            dtype: float64
            ```
        """
        checks.assert_numba_func(apply_func_nb)
        checks.assert_numba_func(reduce_func_nb)
        if apply_args is None:
            apply_args = ()
        if reduce_args is None:
            reduce_args = ()

        out = nb.apply_and_reduce_nb(self.to_2d_array(), apply_func_nb, apply_args, reduce_func_nb, reduce_args)
        wrap_kwargs = merge_dicts(dict(name_or_index='apply_and_reduce'), wrap_kwargs)
        return self.wrapper.wrap_reduced(out, group_by=False, **wrap_kwargs)

    def reduce(self,
               reduce_func_nb: tp.Union[
                   tp.FlatGroupReduceFunc,
                   tp.FlatGroupReduceArrayFunc,
                   tp.GroupReduceFunc,
                   tp.GroupReduceArrayFunc,
                   tp.ReduceFunc,
                   tp.ReduceArrayFunc
               ],
               *args,
               returns_array: bool = False,
               returns_idx: bool = False,
               flatten: bool = False,
               order: str = 'C',
               to_index: bool = True,
               group_by: tp.GroupByLike = None,
               wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeriesFrame[float]:
        """Reduce by column.

        See `vectorbt.generic.nb.flat_reduce_grouped_to_array_nb` if grouped, `returns_array` is True and `flatten` is True.
        See `vectorbt.generic.nb.flat_reduce_grouped_nb` if grouped, `returns_array` is False and `flatten` is True.
        See `vectorbt.generic.nb.reduce_grouped_to_array_nb` if grouped, `returns_array` is True and `flatten` is False.
        See `vectorbt.generic.nb.reduce_grouped_nb` if grouped, `returns_array` is False and `flatten` is False.
        See `vectorbt.generic.nb.reduce_to_array_nb` if not grouped and `returns_array` is True.
        See `vectorbt.generic.nb.reduce_nb` if not grouped and `returns_array` is False.

        Set `returns_idx` to True if values returned by `reduce_func_nb` are indices/positions.
        Set `to_index` to False to return raw positions instead of labels.

        Usage:
            ```pycon
            >>> mean_nb = njit(lambda col, a: np.nanmean(a))
            >>> df.vbt.reduce(mean_nb)
            a    3.0
            b    3.0
            c    1.8
            dtype: float64

            >>> argmax_nb = njit(lambda col, a: np.argmax(a))
            >>> df.vbt.reduce(argmax_nb, returns_idx=True)
            a   2020-01-05
            b   2020-01-01
            c   2020-01-03
            dtype: datetime64[ns]

            >>> argmax_nb = njit(lambda col, a: np.argmax(a))
            >>> df.vbt.reduce(argmax_nb, returns_idx=True, to_index=False)
            a    4
            b    0
            c    2
            dtype: int64

            >>> min_max_nb = njit(lambda col, a: np.array([np.nanmin(a), np.nanmax(a)]))
            >>> df.vbt.reduce(min_max_nb, returns_array=True, wrap_kwargs=dict(name_or_index=['min', 'max']))
                   a    b    c
            min  1.0  1.0  1.0
            max  5.0  5.0  3.0

            >>> group_by = pd.Series(['first', 'first', 'second'], name='group')
            >>> df.vbt.reduce(mean_nb, group_by=group_by)
            group
            first     3.0
            second    1.8
            dtype: float64

            >>> df.vbt.reduce(min_max_nb, name_or_index=['min', 'max'],
            ...     returns_array=True, group_by=group_by)
            group  first  second
            min      1.0     1.0
            max      5.0     3.0
            ```
        """
        checks.assert_numba_func(reduce_func_nb)

        if self.wrapper.grouper.is_grouped(group_by=group_by):
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            if flatten:
                checks.assert_in(order.upper(), ['C', 'F'])
                in_c_order = order.upper() == 'C'
                if returns_array:
                    out = nb.flat_reduce_grouped_to_array_nb(
                        self.to_2d_array(), group_lens, in_c_order, reduce_func_nb, *args)
                else:
                    out = nb.flat_reduce_grouped_nb(
                        self.to_2d_array(), group_lens, in_c_order, reduce_func_nb, *args)
                if returns_idx:
                    if in_c_order:
                        out //= group_lens  # flattened in C order
                    else:
                        out %= self.wrapper.shape[0]  # flattened in F order
            else:
                if returns_array:
                    out = nb.reduce_grouped_to_array_nb(
                        self.to_2d_array(), group_lens, reduce_func_nb, *args)
                else:
                    out = nb.reduce_grouped_nb(
                        self.to_2d_array(), group_lens, reduce_func_nb, *args)
        else:
            if returns_array:
                out = nb.reduce_to_array_nb(
                    self.to_2d_array(), reduce_func_nb, *args)
            else:
                out = nb.reduce_nb(
                    self.to_2d_array(), reduce_func_nb, *args)

        # Perform post-processing
        wrap_kwargs = merge_dicts(dict(
            name_or_index='reduce' if not returns_array else None,
            to_index=returns_idx and to_index,
            fillna=-1 if returns_idx else None,
            dtype=np.int64 if returns_idx else None
        ), wrap_kwargs)
        return self.wrapper.wrap_reduced(out, group_by=group_by, **wrap_kwargs)

    def min(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return min of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='min'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(nb.min_reduce_nb, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        arr = self.to_2d_array()
        if arr.dtype != int and arr.dtype != float:
            # bottleneck can't consume other than that
            _nanmin = np.nanmin
        else:
            _nanmin = nanmin
        return self.wrapper.wrap_reduced(_nanmin(arr, axis=0), group_by=False, **wrap_kwargs)

    def max(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return max of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='max'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(nb.max_reduce_nb, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        arr = self.to_2d_array()
        if arr.dtype != int and arr.dtype != float:
            # bottleneck can't consume other than that
            _nanmax = np.nanmax
        else:
            _nanmax = nanmax
        return self.wrapper.wrap_reduced(_nanmax(arr, axis=0), group_by=False, **wrap_kwargs)

    def mean(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return mean of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='mean'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(
                nb.mean_reduce_nb, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        arr = self.to_2d_array()
        if arr.dtype != int and arr.dtype != float:
            # bottleneck can't consume other than that
            _nanmean = np.nanmean
        else:
            _nanmean = nanmean
        return self.wrapper.wrap_reduced(_nanmean(arr, axis=0), group_by=False, **wrap_kwargs)

    def median(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return median of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='median'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(nb.median_reduce_nb, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        arr = self.to_2d_array()
        if arr.dtype != int and arr.dtype != float:
            # bottleneck can't consume other than that
            _nanmedian = np.nanmedian
        else:
            _nanmedian = nanmedian
        return self.wrapper.wrap_reduced(_nanmedian(arr, axis=0), group_by=False, **wrap_kwargs)

    def std(self, ddof: int = 1, group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return standard deviation of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='std'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(nb.std_reduce_nb, ddof, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        arr = self.to_2d_array()
        if arr.dtype != int and arr.dtype != float:
            # bottleneck can't consume other than that
            _nanstd = np.nanstd
        else:
            _nanstd = nanstd
        return self.wrapper.wrap_reduced(_nanstd(arr, ddof=ddof, axis=0), group_by=False, **wrap_kwargs)

    def sum(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return sum of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='sum'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(nb.sum_reduce_nb, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        arr = self.to_2d_array()
        if arr.dtype != int and arr.dtype != float:
            # bottleneck can't consume other than that
            _nansum = np.nansum
        else:
            _nansum = nansum
        return self.wrapper.wrap_reduced(_nansum(arr, axis=0), group_by=False, **wrap_kwargs)

    def count(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return count of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='count', dtype=np.int64), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(nb.count_reduce_nb, group_by=group_by, flatten=True, wrap_kwargs=wrap_kwargs)

        return self.wrapper.wrap_reduced(np.sum(~np.isnan(self.to_2d_array()), axis=0), group_by=False, **wrap_kwargs)

    def idxmin(self, group_by: tp.GroupByLike = None, order: str = 'C',
               wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return labeled index of min of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='idxmin'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(
                nb.argmin_reduce_nb,
                group_by=group_by,
                flatten=True,
                returns_idx=True,
                order=order,
                wrap_kwargs=wrap_kwargs
            )

        obj = self.to_2d_array()
        out = np.full(obj.shape[1], np.nan, dtype=object)
        nan_mask = np.all(np.isnan(obj), axis=0)
        out[~nan_mask] = self.wrapper.index[nanargmin(obj[:, ~nan_mask], axis=0)]
        return self.wrapper.wrap_reduced(out, group_by=False, **wrap_kwargs)

    def idxmax(self, group_by: tp.GroupByLike = None, order: str = 'C',
               wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return labeled index of max of non-NaN elements."""
        wrap_kwargs = merge_dicts(dict(name_or_index='idxmax'), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(
                nb.argmax_reduce_nb,
                group_by=group_by,
                flatten=True,
                returns_idx=True,
                order=order,
                wrap_kwargs=wrap_kwargs
            )

        obj = self.to_2d_array()
        out = np.full(obj.shape[1], np.nan, dtype=object)
        nan_mask = np.all(np.isnan(obj), axis=0)
        out[~nan_mask] = self.wrapper.index[nanargmax(obj[:, ~nan_mask], axis=0)]
        return self.wrapper.wrap_reduced(out, group_by=False, **wrap_kwargs)

    def describe(self, percentiles: tp.Optional[tp.ArrayLike] = None, ddof: int = 1,
                 group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.generic.nb.describe_reduce_nb`.

        For `percentiles`, see `pd.DataFrame.describe`.

        Usage:
            ```pycon
            >>> df.vbt.describe()
                          a         b        c
            count  5.000000  5.000000  5.00000
            mean   3.000000  3.000000  1.80000
            std    1.581139  1.581139  0.83666
            min    1.000000  1.000000  1.00000
            25%    2.000000  2.000000  1.00000
            50%    3.000000  3.000000  2.00000
            75%    4.000000  4.000000  2.00000
            max    5.000000  5.000000  3.00000
            ```
        """
        if percentiles is not None:
            percentiles = reshape_fns.to_1d_array(percentiles)
        else:
            percentiles = np.array([0.25, 0.5, 0.75])
        percentiles = percentiles.tolist()
        if 0.5 not in percentiles:
            percentiles.append(0.5)
        percentiles = np.unique(percentiles)
        perc_formatted = pd.io.formats.format.format_percentiles(percentiles)
        index = pd.Index(['count', 'mean', 'std', 'min', *perc_formatted, 'max'])
        wrap_kwargs = merge_dicts(dict(name_or_index=index), wrap_kwargs)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.reduce(
                nb.describe_reduce_nb, percentiles, ddof,
                group_by=group_by, flatten=True, returns_array=True,
                wrap_kwargs=wrap_kwargs)
        return self.reduce(
            nb.describe_reduce_nb, percentiles, ddof,
            returns_array=True, wrap_kwargs=wrap_kwargs)

    def value_counts(self,
                     normalize: bool = False,
                     sort_uniques: bool = True,
                     sort: bool = False,
                     ascending: bool = False,
                     dropna: bool = False,
                     group_by: tp.GroupByLike = None,
                     mapping: tp.Optional[tp.MappingLike] = None,
                     incl_all_keys: bool = False,
                     wrap_kwargs: tp.KwargsLike = None,
                     **kwargs) -> tp.SeriesFrame:
        """Return a Series/DataFrame containing counts of unique values.

        * Enable `normalize` flag to return the relative frequencies of the unique values.
        * Enable `sort_uniques` flag to sort uniques.
        * Enable `sort` flag to sort by frequencies.
        * Enable `ascending` flag to sort in ascending order.
        * Enable `dropna` flag to exclude counts of NaN.
        * Enable `incl_all_keys` to include all mapping keys, no only those that are present in the array.

        Mapping will be applied using `vectorbt.utils.mapping.apply_mapping` with `**kwargs`."""
        from pkg_resources import parse_version

        if mapping is None:
            mapping = self.mapping
        if isinstance(mapping, str):
            if mapping.lower() == 'index':
                mapping = self.wrapper.index
            elif mapping.lower() == 'columns':
                mapping = self.wrapper.columns
            mapping = to_mapping(mapping)
        if parse_version(pd.__version__) < parse_version("1.5.0"):
            codes, uniques = pd.factorize(self.obj.values.flatten(), sort=False, na_sentinel=None)
        else:
            codes, uniques = pd.factorize(self.obj.values.flatten(), sort=False, use_na_sentinel=False)
        codes = codes.reshape(self.wrapper.shape_2d)
        group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
        value_counts = nb.value_counts_nb(codes, len(uniques), group_lens)
        if incl_all_keys and mapping is not None:
            missing_keys = []
            for x in mapping:
                if pd.isnull(x) and pd.isnull(uniques).any():
                    continue
                if x not in uniques:
                    missing_keys.append(x)
            value_counts = np.vstack((value_counts, np.full((len(missing_keys), value_counts.shape[1]), 0)))
            uniques = np.concatenate((uniques, np.array(missing_keys)))
        nan_mask = np.isnan(uniques)
        if dropna:
            value_counts = value_counts[~nan_mask]
            uniques = uniques[~nan_mask]
        if sort_uniques:
            new_indices = uniques.argsort()
            value_counts = value_counts[new_indices]
            uniques = uniques[new_indices]
        value_counts_sum = value_counts.sum(axis=1)
        if normalize:
            value_counts = value_counts / value_counts_sum.sum()
        if sort:
            if ascending:
                new_indices = value_counts_sum.argsort()
            else:
                new_indices = (-value_counts_sum).argsort()
            value_counts = value_counts[new_indices]
            uniques = uniques[new_indices]
        value_counts_pd = self.wrapper.wrap(
            value_counts,
            index=uniques,
            group_by=group_by,
            **merge_dicts({}, wrap_kwargs)
        )
        if mapping is not None:
            value_counts_pd.index = apply_mapping(value_counts_pd.index, mapping, **kwargs)
        return value_counts_pd

    # ############# Resolution ############# #

    def resolve_self(self: GenericAccessorT,
                     cond_kwargs: tp.KwargsLike = None,
                     custom_arg_names: tp.Optional[tp.Set[str]] = None,
                     impacts_caching: bool = True,
                     silence_warnings: bool = False) -> GenericAccessorT:
        """Resolve self.

        See `vectorbt.base.array_wrapper.Wrapping.resolve_self`.

        Creates a copy of this instance `mapping` is different in `cond_kwargs`."""
        if cond_kwargs is None:
            cond_kwargs = {}
        if custom_arg_names is None:
            custom_arg_names = set()

        reself = Wrapping.resolve_self(
            self,
            cond_kwargs=cond_kwargs,
            custom_arg_names=custom_arg_names,
            impacts_caching=impacts_caching,
            silence_warnings=silence_warnings
        )
        if 'mapping' in cond_kwargs:
            self_copy = reself.replace(mapping=cond_kwargs['mapping'])

            if not checks.is_deep_equal(self_copy.mapping, reself.mapping):
                if not silence_warnings:
                    warnings.warn(f"Changing the mapping will create a copy of this object. "
                                  f"Consider setting it upon object creation to re-use existing cache.", stacklevel=2)
                for alias in reself.self_aliases:
                    if alias not in custom_arg_names:
                        cond_kwargs[alias] = self_copy
                cond_kwargs['mapping'] = self_copy.mapping
                if impacts_caching:
                    cond_kwargs['use_caching'] = False
                return self_copy
        return reself

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `GenericAccessor.stats`.

        Merges `vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults` and
        `generic.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        generic_stats_cfg = settings['generic']['stats']

        return merge_dicts(
            StatsBuilderMixin.stats_defaults.__get__(self),
            generic_stats_cfg
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
            count=dict(
                title='Count',
                calc_func='count',
                inv_check_has_mapping=True,
                tags=['generic', 'describe']
            ),
            mean=dict(
                title='Mean',
                calc_func='mean',
                inv_check_has_mapping=True,
                tags=['generic', 'describe']
            ),
            std=dict(
                title='Std',
                calc_func='std',
                inv_check_has_mapping=True,
                tags=['generic', 'describe']
            ),
            min=dict(
                title='Min',
                calc_func='min',
                inv_check_has_mapping=True,
                tags=['generic', 'describe']
            ),
            median=dict(
                title='Median',
                calc_func='median',
                inv_check_has_mapping=True,
                tags=['generic', 'describe']
            ),
            max=dict(
                title='Max',
                calc_func='max',
                inv_check_has_mapping=True,
                tags=['generic', 'describe']
            ),
            idx_min=dict(
                title='Min Index',
                calc_func='idxmin',
                agg_func=None,
                inv_check_has_mapping=True,
                tags=['generic', 'index']
            ),
            idx_max=dict(
                title='Max Index',
                calc_func='idxmax',
                agg_func=None,
                inv_check_has_mapping=True,
                tags=['generic', 'index']
            ),
            value_counts=dict(
                title='Value Counts',
                calc_func=lambda value_counts: reshape_fns.to_dict(value_counts, orient='index_series'),
                resolve_value_counts=True,
                check_has_mapping=True,
                tags=['generic', 'value_counts']
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Conversion ############# #

    def drawdown(self, wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Drawdown series."""
        out = self.to_2d_array() / nb.expanding_max_nb(self.to_2d_array()) - 1
        return self.wrapper.wrap(out, group_by=False, **merge_dicts({}, wrap_kwargs))

    @property
    def ranges(self) -> Ranges:
        """`GenericAccessor.get_ranges` with default arguments."""
        return self.get_ranges()

    def get_ranges(self, wrapper_kwargs: tp.KwargsLike = None, **kwargs) -> Ranges:
        """Generate range records.

        See `vectorbt.generic.ranges.Ranges`."""
        wrapper_kwargs = merge_dicts(self.wrapper.config, wrapper_kwargs)
        return Ranges.from_ts(self.obj, wrapper_kwargs=wrapper_kwargs, **kwargs)

    @property
    def drawdowns(self) -> Drawdowns:
        """`GenericAccessor.get_drawdowns` with default arguments."""
        return self.get_drawdowns()

    def get_drawdowns(self, wrapper_kwargs: tp.KwargsLike = None, **kwargs) -> Drawdowns:
        """Generate drawdown records.

        See `vectorbt.generic.drawdowns.Drawdowns`."""
        wrapper_kwargs = merge_dicts(self.wrapper.config, wrapper_kwargs)
        return Drawdowns.from_ts(self.obj, wrapper_kwargs=wrapper_kwargs, **kwargs)

    def to_mapped(self,
                  dropna: bool = True,
                  dtype: tp.Optional[tp.DTypeLike] = None,
                  group_by: tp.GroupByLike = None,
                  **kwargs) -> MappedArray:
        """Convert this object into an instance of `vectorbt.records.mapped_array.MappedArray`."""
        mapped_arr = self.to_2d_array().flatten(order='F')
        col_arr = np.repeat(np.arange(self.wrapper.shape_2d[1]), self.wrapper.shape_2d[0])
        idx_arr = np.tile(np.arange(self.wrapper.shape_2d[0]), self.wrapper.shape_2d[1])
        if dropna and np.isnan(mapped_arr).any():
            not_nan_mask = ~np.isnan(mapped_arr)
            mapped_arr = mapped_arr[not_nan_mask]
            col_arr = col_arr[not_nan_mask]
            idx_arr = idx_arr[not_nan_mask]
        return MappedArray(
            self.wrapper,
            np.asarray(mapped_arr, dtype=dtype),
            col_arr,
            idx_arr=idx_arr,
            **kwargs
        ).regroup(group_by)

    def to_returns(self, **kwargs) -> tp.SeriesFrame:
        """Get returns of this object."""
        return self.obj.vbt.returns.from_value(self.obj, **kwargs).obj

    # ############# Crossover ############# #

    def crossed_above(self,
                      other: tp.SeriesFrame,
                      wait: int = 0,
                      broadcast_kwargs: tp.KwargsLike = None,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Generate crossover above another array.

        See `vectorbt.generic.nb.crossed_above_nb`.

        Usage:
            ```pycon
            >>> df['b'].vbt.crossed_above(df['c'])
            2020-01-01    False
            2020-01-02    False
            2020-01-03    False
            2020-01-04    False
            2020-01-05    False
            dtype: bool
            >>> df['a'].vbt.crossed_above(df['b'])
            2020-01-01    False
            2020-01-02    False
            2020-01-03    False
            2020-01-04     True
            2020-01-05    False
            dtype: bool
            >>> df['a'].vbt.crossed_above(df['b'], wait=1)
            2020-01-01    False
            2020-01-02    False
            2020-01-03    False
            2020-01-04    False
            2020-01-05     True
            dtype: bool
            ```
        """
        self_obj, other_obj = reshape_fns.broadcast(self.obj, other, **resolve_dict(broadcast_kwargs))
        out = nb.crossed_above_nb(reshape_fns.to_2d_array(self_obj), reshape_fns.to_2d_array(other_obj), wait=wait)
        return ArrayWrapper.from_obj(self_obj).wrap(out, group_by=False, **resolve_dict(wrap_kwargs))

    def crossed_below(self,
                      other: tp.SeriesFrame,
                      wait: int = 0,
                      broadcast_kwargs: tp.KwargsLike = None,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Generate crossover below another array.

        See `vectorbt.generic.nb.crossed_above_nb` but in reversed order."""
        self_obj, other_obj = reshape_fns.broadcast(self.obj, other, **resolve_dict(broadcast_kwargs))
        out = nb.crossed_above_nb(reshape_fns.to_2d_array(other_obj), reshape_fns.to_2d_array(self_obj), wait=wait)
        return ArrayWrapper.from_obj(self_obj).wrap(out, group_by=False, **resolve_dict(wrap_kwargs))

    # ############# Transformation ############# #

    def transform(self, transformer: TransformerT, wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.SeriesFrame:
        """Transform using a transformer.

        A transformer can be any class instance that has `transform` and `fit_transform` methods,
        ideally subclassing `sklearn.base.TransformerMixin` and `sklearn.base.BaseEstimator`.

        Will fit `transformer` if not fitted.

        `**kwargs` are passed to the `transform` or `fit_transform` method.

        Usage:
            ```pycon
            >>> from sklearn.preprocessing import MinMaxScaler

            >>> df.vbt.transform(MinMaxScaler((-1, 1)))
                          a    b    c
            2020-01-01 -1.0  1.0 -1.0
            2020-01-02 -0.5  0.5  0.0
            2020-01-03  0.0  0.0  1.0
            2020-01-04  0.5 -0.5  0.0
            2020-01-05  1.0 -1.0 -1.0

            >>> fitted_scaler = MinMaxScaler((-1, 1)).fit(np.array([[2], [4]]))
            >>> df.vbt.transform(fitted_scaler)
                          a    b    c
            2020-01-01 -2.0  2.0 -2.0
            2020-01-02 -1.0  1.0 -1.0
            2020-01-03  0.0  0.0  0.0
            2020-01-04  1.0 -1.0 -1.0
            2020-01-05  2.0 -2.0 -2.0
            ```
        """
        is_fitted = True
        try:
            check_is_fitted(transformer)
        except NotFittedError:
            is_fitted = False
        if not is_fitted:
            result = transformer.fit_transform(self.to_2d_array(), **kwargs)
        else:
            result = transformer.transform(self.to_2d_array(), **kwargs)
        return self.wrapper.wrap(result, group_by=False, **merge_dicts({}, wrap_kwargs))

    def zscore(self, **kwargs) -> tp.SeriesFrame:
        """Compute z-score using `sklearn.preprocessing.StandardScaler`."""
        return self.scale(with_mean=True, with_std=True, **kwargs)

    def rebase(self, base: float, wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Rebase all series to a given intial base.

        This makes comparing/plotting different series together easier.
        Will forward and backward fill NaN values."""
        result = nb.bfill_nb(nb.ffill_nb(self.to_2d_array()))
        result = result / result[0] * base
        return self.wrapper.wrap(result, group_by=False, **merge_dicts({}, wrap_kwargs))

    # ############# Splitting ############# #

    def split(self, splitter: SplitterT, stack_kwargs: tp.KwargsLike = None, keys: tp.Optional[tp.IndexLike] = None,
              plot: bool = False, trace_names: tp.TraceNames = None, heatmap_kwargs: tp.KwargsLike = None,
              **kwargs) -> SplitOutputT:
        """Split using a splitter.

        Returns a tuple of tuples, each corresponding to a set and composed of a dataframe and split indexes.

        A splitter can be any class instance that has `split` method, ideally subclassing
        `sklearn.model_selection.BaseCrossValidator` or `vectorbt.generic.splitters.BaseSplitter`.

        `heatmap_kwargs` are passed to `vectorbt.generic.plotting.Heatmap` if `plot` is True,
        can be a dictionary or a list per set, for example, to set trace name for each set ('train', 'test', etc.).

        `**kwargs` are passed to the `split` method.

        !!! note
            The datetime-like format of the index will be lost as result of this operation.
            Make sure to store the index metadata such as frequency information beforehand.

        Usage:
            ```pycon
            >>> from sklearn.model_selection import TimeSeriesSplit

            >>> splitter = TimeSeriesSplit(n_splits=3)
            >>> (train_df, train_indexes), (test_df, test_indexes) = sr.vbt.split(splitter)

            >>> train_df
            split_idx    0    1  2
            0          0.0  0.0  0
            1          1.0  1.0  1
            2          2.0  2.0  2
            3          3.0  3.0  3
            4          NaN  4.0  4
            5          NaN  5.0  5
            6          NaN  NaN  6
            7          NaN  NaN  7
            >>> train_indexes
            [DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-01', ..., '2020-01-06'], dtype='datetime64[ns]', name='split_1'),
             DatetimeIndex(['2020-01-01', ..., '2020-01-08'], dtype='datetime64[ns]', name='split_2')]
            >>> test_df
            split_idx  0  1  2
            0          4  6  8
            1          5  7  9
            >>> test_indexes
            [DatetimeIndex(['2020-01-05', '2020-01-06'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-07', '2020-01-08'], dtype='datetime64[ns]', name='split_1'),
             DatetimeIndex(['2020-01-09', '2020-01-10'], dtype='datetime64[ns]', name='split_2')]

            >>> sr.vbt.split(splitter, plot=True, trace_names=['train', 'test'])
            ```

            ![](/assets/images/split_plot.svg)
        """
        total_range_sr = pd.Series(np.arange(len(self.wrapper.index)), index=self.wrapper.index)
        set_ranges = list(splitter.split(total_range_sr, **kwargs))
        if len(set_ranges) == 0:
            raise ValueError("No splits were generated")
        idxs_by_split_and_set = list(zip(*set_ranges))

        results = []
        if keys is not None:
            if not isinstance(keys, pd.Index):
                keys = pd.Index(keys)
        for idxs_by_split in idxs_by_split_and_set:
            split_dfs = []
            split_indexes = []
            for split_idx, idxs in enumerate(idxs_by_split):
                split_dfs.append(self.obj.iloc[idxs].reset_index(drop=True))
                if keys is not None:
                    split_name = keys[split_idx]
                else:
                    split_name = 'split_' + str(split_idx)
                split_indexes.append(pd.Index(self.wrapper.index[idxs], name=split_name))
            set_df = pd.concat(split_dfs, axis=1).reset_index(drop=True)
            if keys is not None:
                split_columns = keys
            else:
                split_columns = pd.Index(np.arange(len(split_indexes)), name='split_idx')
            split_columns = index_fns.repeat_index(split_columns, len(self.wrapper.columns))
            if stack_kwargs is None:
                stack_kwargs = {}
            set_df = set_df.vbt.stack_index(split_columns, **stack_kwargs)
            results.append((set_df, split_indexes))

        if plot:  # pragma: no cover
            if trace_names is None:
                trace_names = list(range(len(results)))
            if isinstance(trace_names, str):
                trace_names = [trace_names]
            nan_df = pd.DataFrame(np.nan, columns=pd.RangeIndex(stop=len(results[0][1])), index=self.wrapper.index)
            fig = None
            for i, (_, split_indexes) in enumerate(results):
                heatmap_df = nan_df.copy()
                for j in range(len(split_indexes)):
                    heatmap_df.loc[split_indexes[j], j] = i
                _heatmap_kwargs = resolve_dict(heatmap_kwargs, i=i)
                fig = heatmap_df.vbt.ts_heatmap(fig=fig, **merge_dicts(
                    dict(
                        trace_kwargs=dict(
                            showscale=False,
                            name=str(trace_names[i]),
                            showlegend=True
                        )
                    ),
                    _heatmap_kwargs
                ))
                if fig.layout.colorway is not None:
                    colorway = fig.layout.colorway
                else:
                    colorway = fig.layout.template.layout.colorway
                if 'colorscale' not in _heatmap_kwargs:
                    fig.data[-1].update(colorscale=[colorway[i], colorway[i]])
            return fig

        if len(results) == 1:
            return results[0]
        return tuple(results)

    def range_split(self, **kwargs) -> SplitOutputT:
        """Split using `GenericAccessor.split` on `vectorbt.generic.splitters.RangeSplitter`.

        Usage:
            ```pycon
            >>> range_df, range_indexes = sr.vbt.range_split(n=2)
            >>> range_df
            split_idx  0  1
            0          0  5
            1          1  6
            2          2  7
            3          3  8
            4          4  9
            >>> range_indexes
            [DatetimeIndex(['2020-01-01', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-06', ..., '2020-01-10'], dtype='datetime64[ns]', name='split_1')]

            >>> range_df, range_indexes = sr.vbt.range_split(range_len=4)
            >>> range_df
            split_idx  0  1  2  3  4  5  6
            0          0  1  2  3  4  5  6
            1          1  2  3  4  5  6  7
            2          2  3  4  5  6  7  8
            3          3  4  5  6  7  8  9
            >>> range_indexes
            [DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-02', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_1'),
             DatetimeIndex(['2020-01-03', ..., '2020-01-06'], dtype='datetime64[ns]', name='split_2'),
             DatetimeIndex(['2020-01-04', ..., '2020-01-07'], dtype='datetime64[ns]', name='split_3'),
             DatetimeIndex(['2020-01-05', ..., '2020-01-08'], dtype='datetime64[ns]', name='split_4'),
             DatetimeIndex(['2020-01-06', ..., '2020-01-09'], dtype='datetime64[ns]', name='split_5'),
             DatetimeIndex(['2020-01-07', ..., '2020-01-10'], dtype='datetime64[ns]', name='split_6')]

            >>> range_df, range_indexes = sr.vbt.range_split(start_idxs=[0, 2], end_idxs=[5, 7])
            >>> range_df
            split_idx  0  1
            0          0  2
            1          1  3
            2          2  4
            3          3  5
            4          4  6
            5          5  7
            >>> range_indexes
            [DatetimeIndex(['2020-01-01', ..., '2020-01-06'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-03', ..., '2020-01-08'], dtype='datetime64[ns]', name='split_1')]

            >>> range_df, range_indexes = sr.vbt.range_split(start_idxs=[0], end_idxs=[2, 3, 4])
            >>> range_df
            split_idx    0    1  2
            0          0.0  0.0  0
            1          1.0  1.0  1
            2          2.0  2.0  2
            3          NaN  3.0  3
            4          NaN  NaN  4
            >>> range_indexes
            [DatetimeIndex(['2020-01-01', ..., '2020-01-03'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_1'),
             DatetimeIndex(['2020-01-01', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_2')]

            >>> range_df, range_indexes = sr.vbt.range_split(
            ...     start_idxs=pd.Index(['2020-01-01', '2020-01-02']),
            ...     end_idxs=pd.Index(['2020-01-04', '2020-01-05'])
            ... )
            >>> range_df
            split_idx  0  1
            0          0  1
            1          1  2
            2          2  3
            3          3  4
            >>> range_indexes
            [DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_0'),
             DatetimeIndex(['2020-01-02', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_1')]

             >>> sr.vbt.range_split(
             ...    start_idxs=pd.Index(['2020-01-01', '2020-01-02', '2020-01-01']),
             ...    end_idxs=pd.Index(['2020-01-08', '2020-01-04', '2020-01-07']),
             ...    plot=True
             ... )
            ```

            ![](/assets/images/range_split_plot.svg)
        """
        return self.split(RangeSplitter(), **kwargs)

    def rolling_split(self, **kwargs) -> SplitOutputT:
        """Split using `GenericAccessor.split` on `vectorbt.generic.splitters.RollingSplitter`.

        Usage:
            ```pycon
            >>> train_set, valid_set, test_set = sr.vbt.rolling_split(
            ...     window_len=5, set_lens=(1, 1), left_to_right=False)
            >>> train_set[0]
            split_idx  0  1  2  3  4  5
            0          0  1  2  3  4  5
            1          1  2  3  4  5  6
            2          2  3  4  5  6  7
            >>> valid_set[0]
            split_idx  0  1  2  3  4  5
            0          3  4  5  6  7  8
            >>> test_set[0]
            split_idx  0  1  2  3  4  5
            0          4  5  6  7  8  9

            >>> sr.vbt.rolling_split(
            ...     window_len=5, set_lens=(1, 1), left_to_right=False,
            ...     plot=True, trace_names=['train', 'valid', 'test'])
            ```

            ![](/assets/images/rolling_split_plot.svg)
        """
        return self.split(RollingSplitter(), **kwargs)

    def expanding_split(self, **kwargs) -> SplitOutputT:
        """Split using `GenericAccessor.split` on `vectorbt.generic.splitters.ExpandingSplitter`.

        Usage:
            ```pycon
            >>> train_set, valid_set, test_set = sr.vbt.expanding_split(
            ...     n=5, set_lens=(1, 1), min_len=3, left_to_right=False)
            >>> train_set[0]
            split_idx    0    1    2    3    4    5    6  7
            0          0.0  0.0  0.0  0.0  0.0  0.0  0.0  0
            1          NaN  1.0  1.0  1.0  1.0  1.0  1.0  1
            2          NaN  NaN  2.0  2.0  2.0  2.0  2.0  2
            3          NaN  NaN  NaN  3.0  3.0  3.0  3.0  3
            4          NaN  NaN  NaN  NaN  4.0  4.0  4.0  4
            5          NaN  NaN  NaN  NaN  NaN  5.0  5.0  5
            6          NaN  NaN  NaN  NaN  NaN  NaN  6.0  6
            7          NaN  NaN  NaN  NaN  NaN  NaN  NaN  7
            >>> valid_set[0]
            split_idx  0  1  2  3  4  5  6  7
            0          1  2  3  4  5  6  7  8
            >>> test_set[0]
            split_idx  0  1  2  3  4  5  6  7
            0          2  3  4  5  6  7  8  9

            >>> sr.vbt.expanding_split(
            ...     set_lens=(1, 1), min_len=3, left_to_right=False,
            ...     plot=True, trace_names=['train', 'valid', 'test'])
            ```

            ![](/assets/images/expanding_split_plot.svg)
        """
        return self.split(ExpandingSplitter(), **kwargs)

    # ############# Plotting ############# #

    def plot(self,
             trace_names: tp.TraceNames = None,
             x_labels: tp.Optional[tp.Labels] = None,
             return_fig: bool = True,
             **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """Create `vectorbt.generic.plotting.Scatter` and return the figure.

        Usage:
            ```pycon
            >>> df.vbt.plot()
            ```

            ![](/assets/images/df_plot.svg)
        """
        if x_labels is None:
            x_labels = self.wrapper.index
        if trace_names is None:
            if self.is_frame() or (self.is_series() and self.wrapper.name is not None):
                trace_names = self.wrapper.columns
        scatter = plotting.Scatter(
            data=self.to_2d_array(),
            trace_names=trace_names,
            x_labels=x_labels,
            **kwargs
        )
        if return_fig:
            return scatter.fig
        return scatter

    def lineplot(self, **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """`GenericAccessor.plot` with 'lines' mode.

        Usage:
            ```pycon
            >>> df.vbt.lineplot()
            ```

            ![](/assets/images/df_lineplot.svg)
        """
        return self.plot(**merge_dicts(dict(trace_kwargs=dict(mode='lines')), kwargs))

    def scatterplot(self, **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """`GenericAccessor.plot` with 'markers' mode.

        Usage:
            ```pycon
            >>> df.vbt.scatterplot()
            ```

            ![](/assets/images/df_scatterplot.svg)
        """
        return self.plot(**merge_dicts(dict(trace_kwargs=dict(mode='markers')), kwargs))

    def barplot(self,
                trace_names: tp.TraceNames = None,
                x_labels: tp.Optional[tp.Labels] = None,
                return_fig: bool = True,
                **kwargs) -> tp.Union[tp.BaseFigure, plotting.Bar]:  # pragma: no cover
        """Create `vectorbt.generic.plotting.Bar` and return the figure.

        Usage:
            ```pycon
            >>> df.vbt.barplot()
            ```

            ![](/assets/images/df_barplot.svg)
        """
        if x_labels is None:
            x_labels = self.wrapper.index
        if trace_names is None:
            if self.is_frame() or (self.is_series() and self.wrapper.name is not None):
                trace_names = self.wrapper.columns
        bar = plotting.Bar(
            data=self.to_2d_array(),
            trace_names=trace_names,
            x_labels=x_labels,
            **kwargs
        )
        if return_fig:
            return bar.fig
        return bar

    def histplot(self,
                 trace_names: tp.TraceNames = None,
                 group_by: tp.GroupByLike = None,
                 return_fig: bool = True,
                 **kwargs) -> tp.Union[tp.BaseFigure, plotting.Histogram]:  # pragma: no cover
        """Create `vectorbt.generic.plotting.Histogram` and return the figure.

        Usage:
            ```pycon
            >>> df.vbt.histplot()
            ```

            ![](/assets/images/df_histplot.svg)
        """
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.flatten_grouped(group_by=group_by).vbt.histplot(trace_names=trace_names, **kwargs)

        if trace_names is None:
            if self.is_frame() or (self.is_series() and self.wrapper.name is not None):
                trace_names = self.wrapper.columns
        hist = plotting.Histogram(
            data=self.to_2d_array(),
            trace_names=trace_names,
            **kwargs
        )
        if return_fig:
            return hist.fig
        return hist

    def boxplot(self,
                trace_names: tp.TraceNames = None,
                group_by: tp.GroupByLike = None,
                return_fig: bool = True,
                **kwargs) -> tp.Union[tp.BaseFigure, plotting.Box]:  # pragma: no cover
        """Create `vectorbt.generic.plotting.Box` and return the figure.

        Usage:
            ```pycon
            >>> df.vbt.boxplot()
            ```

            ![](/assets/images/df_boxplot.svg)
        """
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            return self.flatten_grouped(group_by=group_by).vbt.boxplot(trace_names=trace_names, **kwargs)

        if trace_names is None:
            if self.is_frame() or (self.is_series() and self.wrapper.name is not None):
                trace_names = self.wrapper.columns
        box = plotting.Box(
            data=self.to_2d_array(),
            trace_names=trace_names,
            **kwargs
        )
        if return_fig:
            return box.fig
        return box

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `GenericAccessor.plots`.

        Merges `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults` and
        `generic.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        generic_plots_cfg = settings['generic']['plots']

        return merge_dicts(
            PlotsBuilderMixin.plots_defaults.__get__(self),
            generic_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            plot=dict(
                check_is_not_grouped=True,
                plot_func='plot',
                pass_trace_names=False,
                tags='generic'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


GenericAccessor.override_metrics_doc(__pdoc__)
GenericAccessor.override_subplots_doc(__pdoc__)


class GenericSRAccessor(GenericAccessor, BaseSRAccessor):
    """Accessor on top of data of any type. For Series only.

    Accessible through `pd.Series.vbt`."""

    def __init__(self, obj: tp.Series, mapping: tp.Optional[tp.MappingLike] = None, **kwargs) -> None:
        BaseSRAccessor.__init__(self, obj, **kwargs)
        GenericAccessor.__init__(self, obj, mapping=mapping, **kwargs)

    def squeeze_grouped(self,
                        squeeze_func_nb: tp.GroupSqueezeFunc, *args,
                        group_by: tp.GroupByLike = None,
                        wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Squeeze each group of elements into a single element.

        Based on `vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped`."""
        obj_frame = self.obj.to_frame().transpose()
        squeezed = obj_frame.vbt.squeeze_grouped(squeeze_func_nb, *args, group_by=group_by).iloc[0]
        wrap_kwargs = merge_dicts(dict(name_or_index=self.wrapper.name), wrap_kwargs)
        return ArrayWrapper.from_obj(obj_frame).wrap_reduced(squeezed, group_by=group_by, **wrap_kwargs)

    def flatten_grouped(self,
                        group_by: tp.GroupByLike = None,
                        order: str = 'C',
                        wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Flatten each group of elements.

        Based on `vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped`."""
        obj_frame = self.obj.to_frame().transpose()
        return obj_frame.vbt.flatten_grouped(group_by=group_by, order=order, wrap_kwargs=wrap_kwargs)

    def plot_against(self,
                     other: tp.ArrayLike,
                     trace_kwargs: tp.KwargsLike = None,
                     other_trace_kwargs: tp.Union[str, tp.KwargsLike] = None,
                     pos_trace_kwargs: tp.KwargsLike = None,
                     neg_trace_kwargs: tp.KwargsLike = None,
                     hidden_trace_kwargs: tp.KwargsLike = None,
                     add_trace_kwargs: tp.KwargsLike = None,
                     fig: tp.Optional[tp.BaseFigure] = None,
                     **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot Series as a line against another line.

        Args:
            other (array_like): Second array. Will broadcast.
            trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter`.
            other_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `other`.

                Set to 'hidden' to hide.
            pos_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for positive line.
            neg_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for negative line.
            hidden_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for hidden lines.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> df['a'].vbt.plot_against(df['b'])
            ```

            ![](/assets/images/sr_plot_against.svg)
        """
        if trace_kwargs is None:
            trace_kwargs = {}
        if other_trace_kwargs is None:
            other_trace_kwargs = {}
        if pos_trace_kwargs is None:
            pos_trace_kwargs = {}
        if neg_trace_kwargs is None:
            neg_trace_kwargs = {}
        if hidden_trace_kwargs is None:
            hidden_trace_kwargs = {}
        obj, other = reshape_fns.broadcast(self.obj, other, columns_from='keep')
        checks.assert_instance_of(other, pd.Series)
        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        # TODO: Using masks feels hacky
        pos_mask = self.obj > other
        if pos_mask.any():
            # Fill positive area
            pos_obj = self.obj.copy()
            pos_obj[~pos_mask] = other[~pos_mask]
            other.vbt.plot(
                trace_kwargs=merge_dicts(dict(
                    line=dict(
                        color='rgba(0, 0, 0, 0)',
                        width=0
                    ),
                    opacity=0,
                    hoverinfo='skip',
                    showlegend=False,
                    name=None,
                ), hidden_trace_kwargs),
                add_trace_kwargs=add_trace_kwargs,
                fig=fig
            )
            pos_obj.vbt.plot(
                trace_kwargs=merge_dicts(dict(
                    fillcolor='rgba(0, 128, 0, 0.3)',
                    line=dict(
                        color='rgba(0, 0, 0, 0)',
                        width=0
                    ),
                    opacity=0,
                    fill='tonexty',
                    connectgaps=False,
                    hoverinfo='skip',
                    showlegend=False,
                    name=None
                ), pos_trace_kwargs),
                add_trace_kwargs=add_trace_kwargs,
                fig=fig
            )
        neg_mask = self.obj < other
        if neg_mask.any():
            # Fill negative area
            neg_obj = self.obj.copy()
            neg_obj[~neg_mask] = other[~neg_mask]
            other.vbt.plot(
                trace_kwargs=merge_dicts(dict(
                    line=dict(
                        color='rgba(0, 0, 0, 0)',
                        width=0
                    ),
                    opacity=0,
                    hoverinfo='skip',
                    showlegend=False,
                    name=None
                ), hidden_trace_kwargs),
                add_trace_kwargs=add_trace_kwargs,
                fig=fig
            )
            neg_obj.vbt.plot(
                trace_kwargs=merge_dicts(dict(
                    line=dict(
                        color='rgba(0, 0, 0, 0)',
                        width=0
                    ),
                    fillcolor='rgba(255, 0, 0, 0.3)',
                    opacity=0,
                    fill='tonexty',
                    connectgaps=False,
                    hoverinfo='skip',
                    showlegend=False,
                    name=None
                ), neg_trace_kwargs),
                add_trace_kwargs=add_trace_kwargs,
                fig=fig
            )

        # Plot main traces
        self.plot(trace_kwargs=trace_kwargs, add_trace_kwargs=add_trace_kwargs, fig=fig)
        if other_trace_kwargs == 'hidden':
            other_trace_kwargs = dict(
                line=dict(
                    color='rgba(0, 0, 0, 0)',
                    width=0
                ),
                opacity=0.,
                hoverinfo='skip',
                showlegend=False,
                name=None
            )
        other.vbt.plot(trace_kwargs=other_trace_kwargs, add_trace_kwargs=add_trace_kwargs, fig=fig)
        return fig

    def overlay_with_heatmap(self,
                             other: tp.ArrayLike,
                             trace_kwargs: tp.KwargsLike = None,
                             heatmap_kwargs: tp.KwargsLike = None,
                             add_trace_kwargs: tp.KwargsLike = None,
                             fig: tp.Optional[tp.BaseFigure] = None,
                             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot Series as a line and overlays it with a heatmap.

        Args:
            other (array_like): Second array. Will broadcast.
            trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter`.
            heatmap_kwargs (dict): Keyword arguments passed to `GenericDFAccessor.heatmap`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> df['a'].vbt.overlay_with_heatmap(df['b'])
            ```

            ![](/assets/images/sr_overlay_with_heatmap.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        if trace_kwargs is None:
            trace_kwargs = {}
        if heatmap_kwargs is None:
            heatmap_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}

        obj, other = reshape_fns.broadcast(self.obj, other, columns_from='keep')
        checks.assert_instance_of(other, pd.Series)
        if fig is None:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            if 'width' in plotting_cfg['layout']:
                fig.update_layout(width=plotting_cfg['layout']['width'] + 100)
        fig.update_layout(**layout_kwargs)

        other.vbt.ts_heatmap(**heatmap_kwargs, add_trace_kwargs=add_trace_kwargs, fig=fig)
        self.plot(
            trace_kwargs=merge_dicts(dict(line=dict(color=plotting_cfg['color_schema']['blue'])), trace_kwargs),
            add_trace_kwargs=merge_dicts(dict(secondary_y=True), add_trace_kwargs),
            fig=fig
        )
        return fig

    def heatmap(self,
                x_level: tp.Optional[tp.Level] = None,
                y_level: tp.Optional[tp.Level] = None,
                symmetric: bool = False,
                sort: bool = True,
                x_labels: tp.Optional[tp.Labels] = None,
                y_labels: tp.Optional[tp.Labels] = None,
                slider_level: tp.Optional[tp.Level] = None,
                active: int = 0,
                slider_labels: tp.Optional[tp.Labels] = None,
                return_fig: bool = True,
                fig: tp.Optional[tp.BaseFigure] = None,
                **kwargs) -> tp.Union[tp.BaseFigure, plotting.Heatmap]:  # pragma: no cover
        """Create a heatmap figure based on object's multi-index and values.

        If index is not a multi-index, converts Series into a DataFrame and calls `GenericDFAccessor.heatmap`.

        If multi-index contains more than two levels or you want them in specific order,
        pass `x_level` and `y_level`, each (`int` if index or `str` if name) corresponding
        to an axis of the heatmap. Optionally, pass `slider_level` to use a level as a slider.

        Creates `vectorbt.generic.plotting.Heatmap` and returns the figure.

        Usage:
            ```pycon
            >>> multi_index = pd.MultiIndex.from_tuples([
            ...     (1, 1),
            ...     (2, 2),
            ...     (3, 3)
            ... ])
            >>> sr = pd.Series(np.arange(len(multi_index)), index=multi_index)
            >>> sr
            1  1    0
            2  2    1
            3  3    2
            dtype: int64

            >>> sr.vbt.heatmap()
            ```

            ![](/assets/images/sr_heatmap.svg)

            * Using one level as a slider:

            ```pycon
            >>> multi_index = pd.MultiIndex.from_tuples([
            ...     (1, 1, 1),
            ...     (1, 2, 2),
            ...     (1, 3, 3),
            ...     (2, 3, 3),
            ...     (2, 2, 2),
            ...     (2, 1, 1)
            ... ])
            >>> sr = pd.Series(np.arange(len(multi_index)), index=multi_index)
            >>> sr
            1  1  1    0
               2  2    1
               3  3    2
            2  3  3    3
               2  2    4
               1  1    5
            dtype: int64

            >>> sr.vbt.heatmap(slider_level=0)
            ```

            ![](/assets/images/sr_heatmap_slider.gif)
        """
        if not isinstance(self.wrapper.index, pd.MultiIndex):
            return self.obj.to_frame().vbt.heatmap(
                x_labels=x_labels, y_labels=y_labels,
                return_fig=return_fig, fig=fig, **kwargs)

        (x_level, y_level), (slider_level,) = index_fns.pick_levels(
            self.wrapper.index,
            required_levels=(x_level, y_level),
            optional_levels=(slider_level,)
        )

        x_level_vals = self.wrapper.index.get_level_values(x_level)
        y_level_vals = self.wrapper.index.get_level_values(y_level)
        x_name = x_level_vals.name if x_level_vals.name is not None else 'x'
        y_name = y_level_vals.name if y_level_vals.name is not None else 'y'
        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                hovertemplate=f"{x_name}: %{{x}}<br>" +
                              f"{y_name}: %{{y}}<br>" +
                              "value: %{z}<extra></extra>"
            ),
            xaxis_title=x_level_vals.name,
            yaxis_title=y_level_vals.name
        ), kwargs)

        if slider_level is None:
            # No grouping
            df = self.unstack_to_df(
                index_levels=y_level, column_levels=x_level,
                symmetric=symmetric, sort=sort
            )
            return df.vbt.heatmap(x_labels=x_labels, y_labels=y_labels, fig=fig, return_fig=return_fig, **kwargs)

        # Requires grouping
        # See https://plotly.com/python/sliders/
        if not return_fig:
            raise ValueError("Cannot use return_fig=False and slider_level simultaneously")
        _slider_labels = []
        for i, (name, group) in enumerate(self.obj.groupby(level=slider_level)):
            if slider_labels is not None:
                name = slider_labels[i]
            _slider_labels.append(name)
            df = group.vbt.unstack_to_df(
                index_levels=y_level, column_levels=x_level,
                symmetric=symmetric, sort=sort
            )
            if x_labels is None:
                x_labels = df.columns
            if y_labels is None:
                y_labels = df.index
            _kwargs = merge_dicts(dict(
                trace_kwargs=dict(
                    name=str(name) if name is not None else None,
                    visible=False
                ),
            ), kwargs)
            default_size = fig is None and 'height' not in _kwargs
            fig = plotting.Heatmap(
                data=reshape_fns.to_2d_array(df),
                x_labels=x_labels,
                y_labels=y_labels,
                fig=fig,
                **_kwargs
            ).fig
            if default_size:
                fig.layout['height'] += 100  # slider takes up space
        fig.data[active].visible = True
        steps = []
        for i in range(len(fig.data)):
            step = dict(
                method="update",
                args=[{"visible": [False] * len(fig.data)}, {}],
                label=str(_slider_labels[i]) if _slider_labels[i] is not None else None
            )
            step["args"][0]["visible"][i] = True
            steps.append(step)
        prefix = f'{self.wrapper.index.names[slider_level]}: ' \
            if self.wrapper.index.names[slider_level] is not None else None
        sliders = [dict(
            active=active,
            currentvalue={"prefix": prefix},
            pad={"t": 50},
            steps=steps
        )]
        fig.update_layout(
            sliders=sliders
        )
        return fig

    def ts_heatmap(self, **kwargs) -> tp.Union[tp.BaseFigure, plotting.Heatmap]:  # pragma: no cover
        """Heatmap of time-series data."""
        return self.obj.to_frame().vbt.ts_heatmap(**kwargs)

    def volume(self,
               x_level: tp.Optional[tp.Level] = None,
               y_level: tp.Optional[tp.Level] = None,
               z_level: tp.Optional[tp.Level] = None,
               x_labels: tp.Optional[tp.Labels] = None,
               y_labels: tp.Optional[tp.Labels] = None,
               z_labels: tp.Optional[tp.Labels] = None,
               slider_level: tp.Optional[tp.Level] = None,
               slider_labels: tp.Optional[tp.Labels] = None,
               active: int = 0,
               scene_name: str = 'scene',
               fillna: tp.Optional[tp.Number] = None,
               fig: tp.Optional[tp.BaseFigure] = None,
               return_fig: bool = True,
               **kwargs) -> tp.Union[tp.BaseFigure, plotting.Volume]:  # pragma: no cover
        """Create a 3D volume figure based on object's multi-index and values.

        If multi-index contains more than three levels or you want them in specific order, pass
        `x_level`, `y_level`, and `z_level`, each (`int` if index or `str` if name) corresponding
        to an axis of the volume. Optionally, pass `slider_level` to use a level as a slider.

        Creates `vectorbt.generic.plotting.Volume` and returns the figure.

        Usage:
            ```pycon
            >>> multi_index = pd.MultiIndex.from_tuples([
            ...     (1, 1, 1),
            ...     (2, 2, 2),
            ...     (3, 3, 3)
            ... ])
            >>> sr = pd.Series(np.arange(len(multi_index)), index=multi_index)
            >>> sr
            1  1  1    0
            2  2  2    1
            3  3  3    2
            dtype: int64

            >>> sr.vbt.volume().show()
            ```

            ![](/assets/images/sr_volume.svg)
        """
        (x_level, y_level, z_level), (slider_level,) = index_fns.pick_levels(
            self.wrapper.index,
            required_levels=(x_level, y_level, z_level),
            optional_levels=(slider_level,)
        )

        x_level_vals = self.wrapper.index.get_level_values(x_level)
        y_level_vals = self.wrapper.index.get_level_values(y_level)
        z_level_vals = self.wrapper.index.get_level_values(z_level)
        # Labels are just unique level values
        if x_labels is None:
            x_labels = np.unique(x_level_vals)
        if y_labels is None:
            y_labels = np.unique(y_level_vals)
        if z_labels is None:
            z_labels = np.unique(z_level_vals)

        x_name = x_level_vals.name if x_level_vals.name is not None else 'x'
        y_name = y_level_vals.name if y_level_vals.name is not None else 'y'
        z_name = z_level_vals.name if z_level_vals.name is not None else 'z'
        def_kwargs = dict()
        def_kwargs['trace_kwargs'] = dict(
            hovertemplate=f"{x_name}: %{{x}}<br>" +
                          f"{y_name}: %{{y}}<br>" +
                          f"{z_name}: %{{z}}<br>" +
                          "value: %{value}<extra></extra>"
        )
        def_kwargs[scene_name] = dict(
            xaxis_title=x_level_vals.name,
            yaxis_title=y_level_vals.name,
            zaxis_title=z_level_vals.name
        )
        def_kwargs['scene_name'] = scene_name
        kwargs = merge_dicts(def_kwargs, kwargs)

        contains_nan = False
        if slider_level is None:
            # No grouping
            v = self.unstack_to_array(levels=(x_level, y_level, z_level))
            if fillna is not None:
                v = np.nan_to_num(v, nan=fillna)
            if np.isnan(v).any():
                contains_nan = True
            volume = plotting.Volume(
                data=v,
                x_labels=x_labels,
                y_labels=y_labels,
                z_labels=z_labels,
                fig=fig,
                **kwargs
            )
            if return_fig:
                fig = volume.fig
            else:
                fig = volume
        else:
            # Requires grouping
            # See https://plotly.com/python/sliders/
            if not return_fig:
                raise ValueError("Cannot use return_fig=False and slider_level simultaneously")
            _slider_labels = []
            for i, (name, group) in enumerate(self.obj.groupby(level=slider_level)):
                if slider_labels is not None:
                    name = slider_labels[i]
                _slider_labels.append(name)
                v = group.vbt.unstack_to_array(levels=(x_level, y_level, z_level))
                if fillna is not None:
                    v = np.nan_to_num(v, nan=fillna)
                if np.isnan(v).any():
                    contains_nan = True
                _kwargs = merge_dicts(dict(
                    trace_kwargs=dict(
                        name=str(name) if name is not None else None,
                        visible=False
                    )
                ), kwargs)
                default_size = fig is None and 'height' not in _kwargs
                fig = plotting.Volume(
                    data=v,
                    x_labels=x_labels,
                    y_labels=y_labels,
                    z_labels=z_labels,
                    fig=fig,
                    **_kwargs
                ).fig
                if default_size:
                    fig.layout['height'] += 100  # slider takes up space
            fig.data[active].visible = True
            steps = []
            for i in range(len(fig.data)):
                step = dict(
                    method="update",
                    args=[{"visible": [False] * len(fig.data)}, {}],
                    label=str(_slider_labels[i]) if _slider_labels[i] is not None else None
                )
                step["args"][0]["visible"][i] = True
                steps.append(step)
            prefix = f'{self.wrapper.index.names[slider_level]}: ' \
                if self.wrapper.index.names[slider_level] is not None else None
            sliders = [dict(
                active=active,
                currentvalue={"prefix": prefix},
                pad={"t": 50},
                steps=steps
            )]
            fig.update_layout(
                sliders=sliders
            )

        if contains_nan:
            warnings.warn("Data contains NaNs. Use `fillna` argument or "
                          "`show` method in case of visualization issues.", stacklevel=2)
        return fig

    def qqplot(self,
               sparams: tp.Union[tp.Iterable, tuple, None] = (),
               dist: str = 'norm',
               plot_line: bool = True,
               line_shape_kwargs: tp.KwargsLike = None,
               xref: str = 'x',
               yref: str = 'y',
               fig: tp.Optional[tp.BaseFigure] = None,
               **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot probability plot using `scipy.stats.probplot`.

        `**kwargs` are passed to `GenericAccessor.scatterplot`.

        Usage:
            ```pycon
            >>> pd.Series(np.random.standard_normal(100)).vbt.qqplot()
            ```

            ![](/assets/images/sr_qqplot.svg)
        """
        qq = stats.probplot(self.obj, sparams=sparams, dist=dist)
        fig = pd.Series(qq[0][1], index=qq[0][0]).vbt.scatterplot(fig=fig, **kwargs)

        if plot_line:
            if line_shape_kwargs is None:
                line_shape_kwargs = {}
            x = np.array([qq[0][0][0], qq[0][0][-1]])
            y = qq[1][1] + qq[1][0] * x
            fig.add_shape(**merge_dicts(dict(
                type="line",
                xref=xref,
                yref=yref,
                x0=x[0],
                y0=y[0],
                x1=x[1],
                y1=y[1],
                line=dict(
                    color='red'
                )
            ), line_shape_kwargs))

        return fig


class GenericDFAccessor(GenericAccessor, BaseDFAccessor):
    """Accessor on top of data of any type. For DataFrames only.

    Accessible through `pd.DataFrame.vbt`."""

    def __init__(self, obj: tp.Frame, mapping: tp.Optional[tp.MappingLike] = None, **kwargs) -> None:
        BaseDFAccessor.__init__(self, obj, **kwargs)
        GenericAccessor.__init__(self, obj, mapping=mapping, **kwargs)

    def squeeze_grouped(self,
                        squeeze_func_nb: tp.GroupSqueezeFunc, *args,
                        group_by: tp.GroupByLike = None,
                        wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Squeeze each group of columns into a single column.

        See `vectorbt.generic.nb.squeeze_grouped_nb`.

        Usage:
            ```pycon
            >>> group_by = pd.Series(['first', 'first', 'second'], name='group')
            >>> mean_squeeze_nb = njit(lambda i, group, a: np.nanmean(a))
            >>> df.vbt.squeeze_grouped(mean_squeeze_nb, group_by=group_by)
            group       first  second
            2020-01-01    3.0     1.0
            2020-01-02    3.0     2.0
            2020-01-03    3.0     3.0
            2020-01-04    3.0     2.0
            2020-01-05    3.0     1.0
            ```
        """
        if not self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping required")
        checks.assert_numba_func(squeeze_func_nb)

        group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
        out = nb.squeeze_grouped_nb(self.to_2d_array(), group_lens, squeeze_func_nb, *args)
        return self.wrapper.wrap(out, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    def flatten_grouped(self,
                        group_by: tp.GroupByLike = None,
                        order: str = 'C',
                        wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Flatten each group of columns.

        See `vectorbt.generic.nb.flatten_grouped_nb`.
        If all groups have the same length, see `vectorbt.generic.nb.flatten_uniform_grouped_nb`.

        !!! warning
            Make sure that the distribution of group lengths is close to uniform, otherwise
            groups with less columns will be filled with NaN and needlessly occupy memory.

        Usage:
            ```pycon
            >>> group_by = pd.Series(['first', 'first', 'second'], name='group')
            >>> df.vbt.flatten_grouped(group_by=group_by, order='C')
            group       first  second
            2020-01-01    1.0     1.0
            2020-01-01    5.0     NaN
            2020-01-02    2.0     2.0
            2020-01-02    4.0     NaN
            2020-01-03    3.0     3.0
            2020-01-03    3.0     NaN
            2020-01-04    4.0     2.0
            2020-01-04    2.0     NaN
            2020-01-05    5.0     1.0
            2020-01-05    1.0     NaN

            >>> df.vbt.flatten_grouped(group_by=group_by, order='F')
            group       first  second
            2020-01-01    1.0     1.0
            2020-01-02    2.0     2.0
            2020-01-03    3.0     3.0
            2020-01-04    4.0     2.0
            2020-01-05    5.0     1.0
            2020-01-01    5.0     NaN
            2020-01-02    4.0     NaN
            2020-01-03    3.0     NaN
            2020-01-04    2.0     NaN
            2020-01-05    1.0     NaN
            ```
        """
        if not self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping required")
        checks.assert_in(order.upper(), ['C', 'F'])

        group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
        if np.all(group_lens == group_lens.item(0)):
            func = nb.flatten_uniform_grouped_nb
        else:
            func = nb.flatten_grouped_nb
        if order.upper() == 'C':
            out = func(self.to_2d_array(), group_lens, True)
            new_index = index_fns.repeat_index(self.wrapper.index, np.max(group_lens))
        else:
            out = func(self.to_2d_array(), group_lens, False)
            new_index = index_fns.tile_index(self.wrapper.index, np.max(group_lens))
        wrap_kwargs = merge_dicts(dict(index=new_index), wrap_kwargs)
        return self.wrapper.wrap(out, group_by=group_by, **wrap_kwargs)

    def heatmap(self,
                x_labels: tp.Optional[tp.Labels] = None,
                y_labels: tp.Optional[tp.Labels] = None,
                return_fig: bool = True,
                **kwargs) -> tp.Union[tp.BaseFigure, plotting.Heatmap]:  # pragma: no cover
        """Create `vectorbt.generic.plotting.Heatmap` and return the figure.

        Usage:
            ```pycon
            >>> df = pd.DataFrame([
            ...     [0, np.nan, np.nan],
            ...     [np.nan, 1, np.nan],
            ...     [np.nan, np.nan, 2]
            ... ])
            >>> df.vbt.heatmap()
            ```

            ![](/assets/images/df_heatmap.svg)
        """
        if x_labels is None:
            x_labels = self.wrapper.columns
        if y_labels is None:
            y_labels = self.wrapper.index
        heatmap = plotting.Heatmap(
            data=self.to_2d_array(),
            x_labels=x_labels,
            y_labels=y_labels,
            **kwargs
        )
        if return_fig:
            return heatmap.fig
        return heatmap

    def ts_heatmap(self, is_y_category: bool = True,
                   **kwargs) -> tp.Union[tp.BaseFigure, plotting.Heatmap]:  # pragma: no cover
        """Heatmap of time-series data."""
        return self.obj.transpose().iloc[::-1].vbt.heatmap(is_y_category=is_y_category, **kwargs)
