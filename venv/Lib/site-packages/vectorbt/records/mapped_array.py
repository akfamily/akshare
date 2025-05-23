# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for working with mapped arrays.

This class takes the mapped array and the corresponding column and (optionally) index arrays,
and offers features to directly process the mapped array without converting it to pandas;
for example, to compute various statistics by column, such as standard deviation.

Consider the following example:

```pycon
>>> import numpy as np
>>> import pandas as pd
>>> from numba import njit
>>> import vectorbt as vbt

>>> a = np.array([10., 11., 12., 13., 14., 15., 16., 17., 18.])
>>> col_arr = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
>>> idx_arr = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
>>> wrapper = vbt.ArrayWrapper(index=['x', 'y', 'z'],
...     columns=['a', 'b', 'c'], ndim=2, freq='1 day')
>>> ma = vbt.MappedArray(wrapper, a, col_arr, idx_arr=idx_arr)
```

## Reducing

Using `MappedArray`, you can then reduce by column as follows:

* Use already provided reducers such as `MappedArray.mean`:

```pycon
>>> ma.mean()
a    11.0
b    14.0
c    17.0
dtype: float64
```

* Use `MappedArray.to_pd` to map to pandas and then reduce manually (expensive):

```pycon
>>> ma.to_pd().mean()
a    11.0
b    14.0
c    17.0
dtype: float64
```

* Use `MappedArray.reduce` to reduce using a custom function:

```pycon
>>> @njit
... def pow_mean_reduce_nb(col, a, pow):
...     return np.mean(a ** pow)

>>> ma.reduce(pow_mean_reduce_nb, 2)
a    121.666667
b    196.666667
c    289.666667
dtype: float64

>>> @njit
... def min_max_reduce_nb(col, a):
...     return np.array([np.min(a), np.max(a)])

>>> ma.reduce(min_max_reduce_nb, returns_array=True, index=['min', 'max'])
        a     b     c
min  10.0  13.0  16.0
max  12.0  15.0  18.0

>>> @njit
... def idxmin_idxmax_reduce_nb(col, a):
...     return np.array([np.argmin(a), np.argmax(a)])

>>> ma.reduce(idxmin_idxmax_reduce_nb, returns_array=True,
...     returns_idx=True, index=['idxmin', 'idxmax'])
        a  b  c
idxmin  x  x  x
idxmax  z  z  z
```

## Mapping

Use `MappedArray.apply` to apply a function on each column/group:

```pycon
>>> @njit
... def cumsum_apply_nb(idxs, col, a):
...     return np.cumsum(a)

>>> ma.apply(cumsum_apply_nb)
<vectorbt.records.mapped_array.MappedArray at 0x7ff061382198>

>>> ma.apply(cumsum_apply_nb).values
array([10., 21., 33., 13., 27., 42., 16., 33., 51.])

>>> group_by = np.array(['first', 'first', 'second'])
>>> ma.apply(cumsum_apply_nb, group_by=group_by, apply_per_group=True).values
array([10., 21., 33., 46., 60., 75., 16., 33., 51.])

Notice how cumsum resets at each column in the first example and at each group in the second example.

## Conversion

You can expand any `MappedArray` instance to pandas:

* Given `idx_arr` was provided:

```pycon
>>> ma.to_pd()
      a     b     c
x  10.0  13.0  16.0
y  11.0  14.0  17.0
z  12.0  15.0  18.0
```

!!! note
    Will raise an error if there are multiple values pointing to the same position.

* In case `group_by` was provided, index can be ignored, or there are position conflicts:

```pycon
>>> ma.to_pd(group_by=np.array(['first', 'first', 'second']), ignore_index=True)
   first  second
0   10.0    16.0
1   11.0    17.0
2   12.0    18.0
3   13.0     NaN
4   14.0     NaN
5   15.0     NaN
```

## Filtering

Use `MappedArray.apply_mask` to filter elements per column/group:

```pycon
>>> mask = [True, False, True, False, True, False, True, False, True]
>>> filtered_ma = ma.apply_mask(mask)
>>> filtered_ma.count()
a    2
b    1
c    2
dtype: int64

>>> filtered_ma.id_arr
array([0, 2, 4, 6, 8])
```

## Plotting

You can build histograms and boxplots of `MappedArray` directly:

```pycon
>>> ma.boxplot()
```

![](/assets/images/mapped_boxplot.svg)

To use scatterplots or any other plots that require index, convert to pandas first:

```pycon
>>> ma.to_pd().vbt.plot()
```

![](/assets/images/mapped_to_pd_plot.svg)

## Grouping

One of the key features of `MappedArray` is that you can perform reducing operations on a group
of columns as if they were a single column. Groups can be specified by `group_by`, which
can be anything from positions or names of column levels, to a NumPy array with actual groups.

There are multiple ways of define grouping:

* When creating `MappedArray`, pass `group_by` to `vectorbt.base.array_wrapper.ArrayWrapper`:

```pycon
>>> group_by = np.array(['first', 'first', 'second'])
>>> grouped_wrapper = wrapper.replace(group_by=group_by)
>>> grouped_ma = vbt.MappedArray(grouped_wrapper, a, col_arr, idx_arr=idx_arr)

>>> grouped_ma.mean()
first     12.5
second    17.0
dtype: float64
```

* Regroup an existing `MappedArray`:

```pycon
>>> ma.regroup(group_by).mean()
first     12.5
second    17.0
dtype: float64
```

* Pass `group_by` directly to the reducing method:

```pycon
>>> ma.mean(group_by=group_by)
first     12.5
second    17.0
dtype: float64
```

By the same way you can disable or modify any existing grouping:

```pycon
>>> grouped_ma.mean(group_by=False)
a    11.0
b    14.0
c    17.0
dtype: float64
```

!!! note
    Grouping applies only to reducing operations, there is no change to the arrays.

## Operators

`MappedArray` implements arithmetic, comparison and logical operators. You can perform basic
operations (such as addition) on mapped arrays as if they were NumPy arrays.

```pycon
>>> ma ** 2
<vectorbt.records.mapped_array.MappedArray at 0x7f97bfc49358>

>>> ma * np.array([1, 2, 3, 4, 5, 6])
<vectorbt.records.mapped_array.MappedArray at 0x7f97bfc65e80>

>>> ma + ma
<vectorbt.records.mapped_array.MappedArray at 0x7fd638004d30>
```

!!! note
    You should ensure that your `MappedArray` operand is on the left if the other operand is an array.

    If two `MappedArray` operands have different metadata, will copy metadata from the first one,
    but at least their `id_arr` and `col_arr` must match.

## Indexing

Like any other class subclassing `vectorbt.base.array_wrapper.Wrapping`, we can do pandas indexing
on a `MappedArray` instance, which forwards indexing operation to each object with columns:

```pycon
>>> ma['a'].values
array([10., 11., 12.])

>>> grouped_ma['first'].values
array([10., 11., 12., 13., 14., 15.])
```

!!! note
    Changing index (time axis) is not supported. The object should be treated as a Series
    rather than a DataFrame; for example, use `some_field.iloc[0]` instead of `some_field.iloc[:, 0]`.

    Indexing behavior depends solely upon `vectorbt.base.array_wrapper.ArrayWrapper`.
    For example, if `group_select` is enabled indexing will be performed on groups,
    otherwise on single columns.

## Caching

`MappedArray` supports caching. If a method or a property requires heavy computation, it's wrapped
with `vectorbt.utils.decorators.cached_method` and `vectorbt.utils.decorators.cached_property`
respectively. Caching can be disabled globally via `caching` in `vectorbt._settings.settings`.

!!! note
    Because of caching, class is meant to be immutable and all properties are read-only.
    To change any attribute, use the `copy` method and pass the attribute as keyword argument.

## Saving and loading

Like any other class subclassing `vectorbt.utils.config.Pickleable`, we can save a `MappedArray`
instance to the disk with `MappedArray.save` and load it with `MappedArray.load`.

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `MappedArray.metrics`.

Metric for mapped arrays are similar to that for `vectorbt.generic.accessors.GenericAccessor`.

```pycon
>>> ma.stats(column='a')
Start                      x
End                        z
Period       3 days 00:00:00
Count                      3
Mean                    11.0
Std                      1.0
Min                     10.0
Median                  11.0
Max                     12.0
Min Index                  x
Max Index                  z
Name: a, dtype: object
```

The main difference unfolds once the mapped array has a mapping:
values are then considered as categorical and usual statistics are meaningless to compute.
For this case, `MappedArray.stats` returns the value counts:

```pycon
>>> mapping = {v: "test_" + str(v) for v in np.unique(ma.values)}
>>> ma.stats(column='a', settings=dict(mapping=mapping))
Start                                    x
End                                      z
Period                     3 days 00:00:00
Count                                    3
Value Counts: test_10.0                  1
Value Counts: test_11.0                  1
Value Counts: test_12.0                  1
Value Counts: test_13.0                  0
Value Counts: test_14.0                  0
Value Counts: test_15.0                  0
Value Counts: test_16.0                  0
Value Counts: test_17.0                  0
Value Counts: test_18.0                  0
Name: a, dtype: object

`MappedArray.stats` also supports (re-)grouping:

```pycon
>>> grouped_ma.stats(column='first')
Start                      x
End                        z
Period       3 days 00:00:00
Count                      6
Mean                    12.5
Std                 1.870829
Min                     10.0
Median                  12.5
Max                     15.0
Min Index                  x
Max Index                  z
Name: first, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `MappedArray.subplots`.

`MappedArray` class has a single subplot based on `MappedArray.to_pd` and
`vectorbt.generic.accessors.GenericAccessor.plot`:

```pycon
>>> ma.plots()
```

![](/assets/images/mapped_to_pd_plot.svg)
"""

import numpy as np
import packaging.version
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.base.reshape_fns import to_1d_array, to_dict
from vectorbt.generic import nb as generic_nb
from vectorbt.generic.plots_builder import PlotsBuilderMixin
from vectorbt.generic.stats_builder import StatsBuilderMixin
from vectorbt.records import nb
from vectorbt.records.col_mapper import ColumnMapper
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, Config, Configured
from vectorbt.utils.decorators import cached_method, attach_binary_magic_methods, attach_unary_magic_methods
from vectorbt.utils.mapping import to_mapping, apply_mapping

MappedArrayT = tp.TypeVar("MappedArrayT", bound="MappedArray")
IndexingMetaT = tp.Tuple[
    ArrayWrapper,
    tp.Array1d,
    tp.Array1d,
    tp.Array1d,
    tp.Optional[tp.Array1d],
    tp.MaybeArray,
    tp.Array1d
]


def combine_mapped_with_other(self: MappedArrayT,
                              other: tp.Union["MappedArray", tp.ArrayLike],
                              np_func: tp.Callable[[tp.ArrayLike, tp.ArrayLike], tp.Array1d]) -> MappedArrayT:
    """Combine `MappedArray` with other compatible object.

    If other object is also `MappedArray`, their `id_arr` and `col_arr` must match."""
    if isinstance(other, MappedArray):
        checks.assert_array_equal(self.id_arr, other.id_arr)
        checks.assert_array_equal(self.col_arr, other.col_arr)
        other = other.values
    return self.replace(mapped_arr=np_func(self.values, other))


class MetaMappedArray(type(StatsBuilderMixin), type(PlotsBuilderMixin)):
    pass


@attach_binary_magic_methods(combine_mapped_with_other)
@attach_unary_magic_methods(lambda self, np_func: self.replace(mapped_arr=np_func(self.values)))
class MappedArray(Wrapping, StatsBuilderMixin, PlotsBuilderMixin, metaclass=MetaMappedArray):
    """Exposes methods for reducing, converting, and plotting arrays mapped by
    `vectorbt.records.base.Records` class.

    Args:
        wrapper (ArrayWrapper): Array wrapper.

            See `vectorbt.base.array_wrapper.ArrayWrapper`.
        mapped_arr (array_like): A one-dimensional array of mapped record values.
        col_arr (array_like): A one-dimensional column array.

            Must be of the same size as `mapped_arr`.
        id_arr (array_like): A one-dimensional id array. Defaults to simple range.

            Must be of the same size as `mapped_arr`.
        idx_arr (array_like): A one-dimensional index array. Optional.

            Must be of the same size as `mapped_arr`.
        mapping (namedtuple, dict or callable): Mapping.
        col_mapper (ColumnMapper): Column mapper if already known.

            !!! note
                It depends upon `wrapper` and `col_arr`, so make sure to invalidate `col_mapper` upon creating
                a `MappedArray` instance with a modified `wrapper` or `col_arr.

                `MappedArray.replace` does it automatically.
        **kwargs: Custom keyword arguments passed to the config.

            Useful if any subclass wants to extend the config.
    """

    def __init__(self,
                 wrapper: ArrayWrapper,
                 mapped_arr: tp.ArrayLike,
                 col_arr: tp.ArrayLike,
                 id_arr: tp.Optional[tp.ArrayLike] = None,
                 idx_arr: tp.Optional[tp.ArrayLike] = None,
                 mapping: tp.Optional[tp.MappingLike] = None,
                 col_mapper: tp.Optional[ColumnMapper] = None,
                 **kwargs) -> None:
        Wrapping.__init__(
            self,
            wrapper,
            mapped_arr=mapped_arr,
            col_arr=col_arr,
            id_arr=id_arr,
            idx_arr=idx_arr,
            mapping=mapping,
            col_mapper=col_mapper,
            **kwargs
        )
        StatsBuilderMixin.__init__(self)

        mapped_arr = np.asarray(mapped_arr)
        col_arr = np.asarray(col_arr)
        checks.assert_shape_equal(mapped_arr, col_arr, axis=0)
        if id_arr is None:
            id_arr = np.arange(len(mapped_arr))
        else:
            id_arr = np.asarray(id_arr)
        if idx_arr is not None:
            idx_arr = np.asarray(idx_arr)
            checks.assert_shape_equal(mapped_arr, idx_arr, axis=0)
        if mapping is not None:
            if isinstance(mapping, str):
                if mapping.lower() == 'index':
                    mapping = self.wrapper.index
                elif mapping.lower() == 'columns':
                    mapping = self.wrapper.columns
            mapping = to_mapping(mapping)

        self._mapped_arr = mapped_arr
        self._id_arr = id_arr
        self._col_arr = col_arr
        self._idx_arr = idx_arr
        self._mapping = mapping
        if col_mapper is None:
            col_mapper = ColumnMapper(wrapper, col_arr)
        self._col_mapper = col_mapper

    def replace(self: MappedArrayT, **kwargs) -> MappedArrayT:
        """See `vectorbt.utils.config.Configured.replace`.

        Also, makes sure that `MappedArray.col_mapper` is not passed to the new instance."""
        if self.config.get('col_mapper', None) is not None:
            if 'wrapper' in kwargs:
                if self.wrapper is not kwargs.get('wrapper'):
                    kwargs['col_mapper'] = None
            if 'col_arr' in kwargs:
                if self.col_arr is not kwargs.get('col_arr'):
                    kwargs['col_mapper'] = None
        return Configured.replace(self, **kwargs)

    def indexing_func_meta(self, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> IndexingMetaT:
        """Perform indexing on `MappedArray` and return metadata."""
        new_wrapper, _, group_idxs, col_idxs = \
            self.wrapper.indexing_func_meta(pd_indexing_func, column_only_select=True, **kwargs)
        new_indices, new_col_arr = self.col_mapper._col_idxs_meta(col_idxs)
        new_mapped_arr = self.values[new_indices]
        new_id_arr = self.id_arr[new_indices]
        if self.idx_arr is not None:
            new_idx_arr = self.idx_arr[new_indices]
        else:
            new_idx_arr = None
        return new_wrapper, new_mapped_arr, new_col_arr, new_id_arr, new_idx_arr, group_idxs, col_idxs

    def indexing_func(self: MappedArrayT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> MappedArrayT:
        """Perform indexing on `MappedArray`."""
        new_wrapper, new_mapped_arr, new_col_arr, new_id_arr, new_idx_arr, _, _ = \
            self.indexing_func_meta(pd_indexing_func, **kwargs)
        return self.replace(
            wrapper=new_wrapper,
            mapped_arr=new_mapped_arr,
            col_arr=new_col_arr,
            id_arr=new_id_arr,
            idx_arr=new_idx_arr
        )

    @property
    def mapped_arr(self) -> tp.Array1d:
        """Mapped array."""
        return self._mapped_arr

    @property
    def values(self) -> tp.Array1d:
        """Mapped array."""
        return self.mapped_arr

    def __len__(self) -> int:
        return len(self.values)

    @property
    def col_arr(self) -> tp.Array1d:
        """Column array."""
        return self._col_arr

    @property
    def col_mapper(self) -> ColumnMapper:
        """Column mapper.

        See `vectorbt.records.col_mapper.ColumnMapper`."""
        return self._col_mapper

    @property
    def id_arr(self) -> tp.Array1d:
        """Id array."""
        return self._id_arr

    @property
    def idx_arr(self) -> tp.Optional[tp.Array1d]:
        """Index array."""
        return self._idx_arr

    @property
    def mapping(self) -> tp.Optional[tp.Mapping]:
        """Mapping."""
        return self._mapping

    @cached_method
    def is_sorted(self, incl_id: bool = False) -> bool:
        """Check whether mapped array is sorted."""
        if incl_id:
            return nb.is_col_idx_sorted_nb(self.col_arr, self.id_arr)
        return nb.is_col_sorted_nb(self.col_arr)

    def sort(self: MappedArrayT,
             incl_id: bool = False,
             idx_arr: tp.Optional[tp.Array1d] = None,
             group_by: tp.GroupByLike = None,
             **kwargs) -> MappedArrayT:
        """Sort mapped array by column array (primary) and id array (secondary, optional).

        `**kwargs` are passed to `MappedArray.replace`."""
        if idx_arr is None:
            idx_arr = self.idx_arr
        if self.is_sorted(incl_id=incl_id):
            return self.replace(idx_arr=idx_arr, **kwargs).regroup(group_by)
        if incl_id:
            ind = np.lexsort((self.id_arr, self.col_arr))  # expensive!
        else:
            ind = np.argsort(self.col_arr)
        return self.replace(
            mapped_arr=self.values[ind],
            col_arr=self.col_arr[ind],
            id_arr=self.id_arr[ind],
            idx_arr=idx_arr[ind] if idx_arr is not None else None,
            **kwargs
        ).regroup(group_by)

    def apply_mask(self: MappedArrayT,
                   mask: tp.Array1d,
                   idx_arr: tp.Optional[tp.Array1d] = None,
                   group_by: tp.GroupByLike = None,
                   **kwargs) -> MappedArrayT:
        """Return a new class instance, filtered by mask.

        `**kwargs` are passed to `MappedArray.replace`."""
        if idx_arr is None:
            idx_arr = self.idx_arr
        mask_indices = np.flatnonzero(mask)
        return self.replace(
            mapped_arr=np.take(self.values, mask_indices),
            col_arr=np.take(self.col_arr, mask_indices),
            id_arr=np.take(self.id_arr, mask_indices),
            idx_arr=np.take(idx_arr, mask_indices) if idx_arr is not None else None,
            **kwargs
        ).regroup(group_by)

    def map_to_mask(self, inout_map_func_nb: tp.MaskInOutMapFunc, *args,
                    group_by: tp.GroupByLike = None) -> tp.Array1d:
        """Map mapped array to a mask.

        See `vectorbt.records.nb.mapped_to_mask_nb`."""
        col_map = self.col_mapper.get_col_map(group_by=group_by)
        return nb.mapped_to_mask_nb(self.values, col_map, inout_map_func_nb, *args)

    @cached_method
    def top_n_mask(self, n: int, **kwargs) -> tp.Array1d:
        """Return mask of top N elements in each column/group."""
        return self.map_to_mask(nb.top_n_inout_map_nb, n, **kwargs)

    @cached_method
    def bottom_n_mask(self, n: int, **kwargs) -> tp.Array1d:
        """Return mask of bottom N elements in each column/group."""
        return self.map_to_mask(nb.bottom_n_inout_map_nb, n, **kwargs)

    @cached_method
    def top_n(self: MappedArrayT, n: int, **kwargs) -> MappedArrayT:
        """Filter top N elements from each column/group."""
        return self.apply_mask(self.top_n_mask(n), **kwargs)

    @cached_method
    def bottom_n(self: MappedArrayT, n: int, **kwargs) -> MappedArrayT:
        """Filter bottom N elements from each column/group."""
        return self.apply_mask(self.bottom_n_mask(n), **kwargs)

    @cached_method
    def is_expandable(self, idx_arr: tp.Optional[tp.Array1d] = None, group_by: tp.GroupByLike = None) -> bool:
        """See `vectorbt.records.nb.is_mapped_expandable_nb`."""
        if idx_arr is None:
            if self.idx_arr is None:
                raise ValueError("Must pass idx_arr")
            idx_arr = self.idx_arr
        col_arr = self.col_mapper.get_col_arr(group_by=group_by)
        target_shape = self.wrapper.get_shape_2d(group_by=group_by)
        return nb.is_mapped_expandable_nb(col_arr, idx_arr, target_shape)

    def to_pd(self,
              idx_arr: tp.Optional[tp.Array1d] = None,
              ignore_index: bool = False,
              fill_value: float = np.nan,
              group_by: tp.GroupByLike = None,
              wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Expand mapped array to a Series/DataFrame.

        If `ignore_index`, will ignore the index and stack data points on top of each other in every column/group
        (see `vectorbt.records.nb.stack_expand_mapped_nb`). Otherwise, see `vectorbt.records.nb.expand_mapped_nb`.

        !!! note
            Will raise an error if there are multiple values pointing to the same position.
            Set `ignore_index` to True in this case.

        !!! warning
            Mapped arrays represent information in the most memory-friendly format.
            Mapping back to pandas may occupy lots of memory if records are sparse."""
        if ignore_index:
            if self.wrapper.ndim == 1:
                return self.wrapper.wrap(
                    self.values,
                    index=np.arange(len(self.values)),
                    group_by=group_by,
                    **merge_dicts({}, wrap_kwargs)
                )
            col_map = self.col_mapper.get_col_map(group_by=group_by)
            out = nb.stack_expand_mapped_nb(self.values, col_map, fill_value)
            return self.wrapper.wrap(
                out, index=np.arange(out.shape[0]),
                group_by=group_by, **merge_dicts({}, wrap_kwargs))
        if idx_arr is None:
            if self.idx_arr is None:
                raise ValueError("Must pass idx_arr")
            idx_arr = self.idx_arr
        if not self.is_expandable(idx_arr=idx_arr, group_by=group_by):
            raise ValueError("Multiple values are pointing to the same position. Use ignore_index.")
        col_arr = self.col_mapper.get_col_arr(group_by=group_by)
        target_shape = self.wrapper.get_shape_2d(group_by=group_by)
        out = nb.expand_mapped_nb(self.values, col_arr, idx_arr, target_shape, fill_value)
        return self.wrapper.wrap(out, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    def apply(self: MappedArrayT,
              apply_func_nb: tp.MappedApplyFunc, *args,
              group_by: tp.GroupByLike = None,
              apply_per_group: bool = False,
              dtype: tp.Optional[tp.DTypeLike] = None,
              **kwargs) -> MappedArrayT:
        """Apply function on mapped array per column/group. Returns mapped array.

        Applies per group if `apply_per_group` is True.

        See `vectorbt.records.nb.apply_on_mapped_nb`.

        `**kwargs` are passed to `MappedArray.replace`."""
        checks.assert_numba_func(apply_func_nb)
        if apply_per_group:
            col_map = self.col_mapper.get_col_map(group_by=group_by)
        else:
            col_map = self.col_mapper.get_col_map(group_by=False)
        mapped_arr = nb.apply_on_mapped_nb(self.values, col_map, apply_func_nb, *args)
        mapped_arr = np.asarray(mapped_arr, dtype=dtype)
        return self.replace(mapped_arr=mapped_arr, **kwargs).regroup(group_by)

    def reduce(self,
               reduce_func_nb: tp.ReduceFunc, *args,
               idx_arr: tp.Optional[tp.Array1d] = None,
               returns_array: bool = False,
               returns_idx: bool = False,
               to_index: bool = True,
               fill_value: tp.Scalar = np.nan,
               group_by: tp.GroupByLike = None,
               wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeriesFrame:
        """Reduce mapped array by column/group.

        If `returns_array` is False and `returns_idx` is False, see `vectorbt.records.nb.reduce_mapped_nb`.
        If `returns_array` is False and `returns_idx` is True, see `vectorbt.records.nb.reduce_mapped_to_idx_nb`.
        If `returns_array` is True and `returns_idx` is False, see `vectorbt.records.nb.reduce_mapped_to_array_nb`.
        If `returns_array` is True and `returns_idx` is True, see `vectorbt.records.nb.reduce_mapped_to_idx_array_nb`.

        If `returns_idx` is True, must pass `idx_arr`. Set `to_index` to False to return raw positions instead
        of labels. Use `fill_value` to set the default value. Set `group_by` to False to disable grouping.
        """
        # Perform checks
        checks.assert_numba_func(reduce_func_nb)
        if idx_arr is None:
            if self.idx_arr is None:
                if returns_idx:
                    raise ValueError("Must pass idx_arr")
            idx_arr = self.idx_arr

        # Perform main computation
        col_map = self.col_mapper.get_col_map(group_by=group_by)
        if not returns_array:
            if not returns_idx:
                out = nb.reduce_mapped_nb(
                    self.values,
                    col_map,
                    fill_value,
                    reduce_func_nb,
                    *args
                )
            else:
                out = nb.reduce_mapped_to_idx_nb(
                    self.values,
                    col_map,
                    idx_arr,
                    fill_value,
                    reduce_func_nb,
                    *args
                )
        else:
            if not returns_idx:
                out = nb.reduce_mapped_to_array_nb(
                    self.values,
                    col_map,
                    fill_value,
                    reduce_func_nb,
                    *args
                )
            else:
                out = nb.reduce_mapped_to_idx_array_nb(
                    self.values,
                    col_map,
                    idx_arr,
                    fill_value,
                    reduce_func_nb,
                    *args
                )

        # Perform post-processing
        wrap_kwargs = merge_dicts(dict(
            name_or_index='reduce' if not returns_array else None,
            to_index=returns_idx and to_index,
            fillna=-1 if returns_idx else None,
            dtype=np.int64 if returns_idx else None
        ), wrap_kwargs)
        return self.wrapper.wrap_reduced(out, group_by=group_by, **wrap_kwargs)

    @cached_method
    def nth(self, n: int, group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return n-th element of each column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='nth'), wrap_kwargs)
        return self.reduce(
            generic_nb.nth_reduce_nb, n,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def nth_index(self, n: int, group_by: tp.GroupByLike = None,
                  wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return index of n-th element of each column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='nth_index'), wrap_kwargs)
        return self.reduce(
            generic_nb.nth_index_reduce_nb, n,
            returns_array=False,
            returns_idx=True,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def min(self, group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return min by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='min'), wrap_kwargs)
        return self.reduce(
            generic_nb.min_reduce_nb,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def max(self, group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return max by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='max'), wrap_kwargs)
        return self.reduce(
            generic_nb.max_reduce_nb,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def mean(self, group_by: tp.GroupByLike = None,
             wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return mean by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='mean'), wrap_kwargs)
        return self.reduce(
            generic_nb.mean_reduce_nb,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def median(self, group_by: tp.GroupByLike = None,
               wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return median by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='median'), wrap_kwargs)
        return self.reduce(
            generic_nb.median_reduce_nb,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def std(self, ddof: int = 1, group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return std by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='std'), wrap_kwargs)
        return self.reduce(
            generic_nb.std_reduce_nb, ddof,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def sum(self, fill_value: tp.Scalar = 0., group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return sum by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='sum'), wrap_kwargs)
        return self.reduce(
            generic_nb.sum_reduce_nb,
            fill_value=fill_value,
            returns_array=False,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def idxmin(self, group_by: tp.GroupByLike = None,
               wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return index of min by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='idxmin'), wrap_kwargs)
        return self.reduce(
            generic_nb.argmin_reduce_nb,
            returns_array=False,
            returns_idx=True,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def idxmax(self, group_by: tp.GroupByLike = None,
               wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Return index of max by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='idxmax'), wrap_kwargs)
        return self.reduce(
            generic_nb.argmax_reduce_nb,
            returns_array=False,
            returns_idx=True,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )

    @cached_method
    def describe(self,
                 percentiles: tp.Optional[tp.ArrayLike] = None,
                 ddof: int = 1,
                 group_by: tp.GroupByLike = None,
                 wrap_kwargs: tp.KwargsLike = None,
                 **kwargs) -> tp.SeriesFrame:
        """Return statistics by column/group."""
        if percentiles is not None:
            percentiles = to_1d_array(percentiles)
        else:
            percentiles = np.array([0.25, 0.5, 0.75])
        percentiles = percentiles.tolist()
        if 0.5 not in percentiles:
            percentiles.append(0.5)
        percentiles = np.unique(percentiles)
        perc_formatted = pd.io.formats.format.format_percentiles(percentiles)
        index = pd.Index(['count', 'mean', 'std', 'min', *perc_formatted, 'max'])
        wrap_kwargs = merge_dicts(dict(name_or_index=index), wrap_kwargs)
        out = self.reduce(
            generic_nb.describe_reduce_nb,
            percentiles,
            ddof,
            returns_array=True,
            returns_idx=False,
            group_by=group_by,
            wrap_kwargs=wrap_kwargs,
            **kwargs
        )
        if isinstance(out, pd.DataFrame):
            out.loc['count'].fillna(0., inplace=True)
        else:
            if np.isnan(out.loc['count']):
                out.loc['count'] = 0.
        return out

    @cached_method
    def count(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return number of values by column/group."""
        wrap_kwargs = merge_dicts(dict(name_or_index='count'), wrap_kwargs)
        return self.wrapper.wrap_reduced(
            self.col_mapper.get_col_map(group_by=group_by)[1],
            group_by=group_by, **wrap_kwargs)

    @cached_method
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
        """See `vectorbt.generic.accessors.GenericAccessor.value_counts`.

        !!! note
            Does not take into account missing values."""
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
            mapped_codes, mapped_uniques = pd.factorize(self.values, sort=False, na_sentinel=None)
        else:
            mapped_codes, mapped_uniques = pd.factorize(self.values, sort=False, use_na_sentinel=False)
        col_map = self.col_mapper.get_col_map(group_by=group_by)
        value_counts = nb.mapped_value_counts_nb(mapped_codes, len(mapped_uniques), col_map)
        if incl_all_keys and mapping is not None:
            missing_keys = []
            for x in mapping:
                if pd.isnull(x) and pd.isnull(mapped_uniques).any():
                    continue
                if x not in mapped_uniques:
                    missing_keys.append(x)
            value_counts = np.vstack((value_counts, np.full((len(missing_keys), value_counts.shape[1]), 0)))
            mapped_uniques = np.concatenate((mapped_uniques, np.array(missing_keys)))
        nan_mask = np.isnan(mapped_uniques)
        if dropna:
            value_counts = value_counts[~nan_mask]
            mapped_uniques = mapped_uniques[~nan_mask]
        if sort_uniques:
            new_indices = mapped_uniques.argsort()
            value_counts = value_counts[new_indices]
            mapped_uniques = mapped_uniques[new_indices]
        value_counts_sum = value_counts.sum(axis=1)
        if normalize:
            value_counts = value_counts / value_counts_sum.sum()
        if sort:
            if ascending:
                new_indices = value_counts_sum.argsort()
            else:
                new_indices = (-value_counts_sum).argsort()
            value_counts = value_counts[new_indices]
            mapped_uniques = mapped_uniques[new_indices]
        value_counts_pd = self.wrapper.wrap(
            value_counts,
            index=mapped_uniques,
            group_by=group_by,
            **merge_dicts({}, wrap_kwargs)
        )
        if mapping is not None:
            value_counts_pd.index = apply_mapping(value_counts_pd.index, mapping, **kwargs)
        return value_counts_pd

    @cached_method
    def apply_mapping(self: MappedArrayT, mapping: tp.Optional[tp.MappingLike] = None, **kwargs) -> MappedArrayT:
        """Apply mapping on each element."""
        if mapping is None:
            mapping = self.mapping
        if isinstance(mapping, str):
            if mapping.lower() == 'index':
                mapping = self.wrapper.index
            elif mapping.lower() == 'columns':
                mapping = self.wrapper.columns
            mapping = to_mapping(mapping)
        return self.replace(mapped_arr=apply_mapping(self.values, mapping), **kwargs)

    def to_index(self):
        """Convert to index."""
        return self.wrapper.index[self.values]

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `MappedArray.stats`.

        Merges `vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults` and
        `mapped_array.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        mapped_array_stats_cfg = settings['mapped_array']['stats']

        return merge_dicts(
            StatsBuilderMixin.stats_defaults.__get__(self),
            mapped_array_stats_cfg
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
                tags='mapped_array'
            ),
            mean=dict(
                title='Mean',
                calc_func='mean',
                inv_check_has_mapping=True,
                tags=['mapped_array', 'describe']
            ),
            std=dict(
                title='Std',
                calc_func='std',
                inv_check_has_mapping=True,
                tags=['mapped_array', 'describe']
            ),
            min=dict(
                title='Min',
                calc_func='min',
                inv_check_has_mapping=True,
                tags=['mapped_array', 'describe']
            ),
            median=dict(
                title='Median',
                calc_func='median',
                inv_check_has_mapping=True,
                tags=['mapped_array', 'describe']
            ),
            max=dict(
                title='Max',
                calc_func='max',
                inv_check_has_mapping=True,
                tags=['mapped_array', 'describe']
            ),
            idx_min=dict(
                title='Min Index',
                calc_func='idxmin',
                inv_check_has_mapping=True,
                agg_func=None,
                tags=['mapped_array', 'index']
            ),
            idx_max=dict(
                title='Max Index',
                calc_func='idxmax',
                inv_check_has_mapping=True,
                agg_func=None,
                tags=['mapped_array', 'index']
            ),
            value_counts=dict(
                title='Value Counts',
                calc_func=lambda value_counts: to_dict(value_counts, orient='index_series'),
                resolve_value_counts=True,
                check_has_mapping=True,
                tags=['mapped_array', 'value_counts']
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def histplot(self, group_by: tp.GroupByLike = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot histogram by column/group."""
        return self.to_pd(group_by=group_by, ignore_index=True).vbt.histplot(**kwargs)

    def boxplot(self, group_by: tp.GroupByLike = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot box plot by column/group."""
        return self.to_pd(group_by=group_by, ignore_index=True).vbt.boxplot(**kwargs)

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `MappedArray.plots`.

        Merges `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults` and
        `mapped_array.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        mapped_array_plots_cfg = settings['mapped_array']['plots']

        return merge_dicts(
            PlotsBuilderMixin.plots_defaults.__get__(self),
            mapped_array_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            to_pd_plot=dict(
                check_is_not_grouped=True,
                plot_func='to_pd.vbt.plot',
                pass_trace_names=False,
                tags='mapped_array'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


__pdoc__ = dict()
MappedArray.override_metrics_doc(__pdoc__)
MappedArray.override_subplots_doc(__pdoc__)
