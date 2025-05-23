# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for working with records.

vectorbt works with two different representations of data: matrices and records.

A matrix, in this context, is just an array of one-dimensional arrays, each corresponding
to a separate feature. The matrix itself holds only one kind of information (one attribute).
For example, one can create a matrix for entry signals, with columns being different strategy
configurations. But what if the matrix is huge and sparse? What if there is more
information we would like to represent by each element? Creating multiple matrices would be
a waste of memory.

Records make possible representing complex, sparse information in a dense format. They are just
an array of one-dimensional arrays of fixed schema. You can imagine records being a DataFrame,
where each row represents a record and each column represents a specific attribute.

```plaintext
               a     b
         0   1.0   5.0
attr1 =  1   2.0   NaN
         2   NaN   7.0
         3   4.0   8.0
               a     b
         0   9.0  13.0
attr2 =  1  10.0   NaN
         2   NaN  15.0
         3  12.0  16.0
            |
            v
      id  col  idx  attr1  attr2
0      0    0    0      1      9
1      1    0    1      2     10
2      2    0    3      4     12
3      3    1    0      5     13
4      4    1    1      7     15
5      5    1    3      8     16
```

Another advantage of records is that they are not constrained by size. Multiple records can map
to a single element in a matrix. For example, one can define multiple orders at the same time step,
which is impossible to represent in a matrix form without using complex data types.

Consider the following example:

```pycon
>>> import numpy as np
>>> import pandas as pd
>>> from numba import njit
>>> from collections import namedtuple
>>> import vectorbt as vbt

>>> example_dt = np.dtype([
...     ('id', np.int64),
...     ('col', np.int64),
...     ('idx', np.int64),
...     ('some_field', np.float64)
... ])
>>> records_arr = np.array([
...     (0, 0, 0, 10.),
...     (1, 0, 1, 11.),
...     (2, 0, 2, 12.),
...     (3, 1, 0, 13.),
...     (4, 1, 1, 14.),
...     (5, 1, 2, 15.),
...     (6, 2, 0, 16.),
...     (7, 2, 1, 17.),
...     (8, 2, 2, 18.)
... ], dtype=example_dt)
>>> wrapper = vbt.ArrayWrapper(index=['x', 'y', 'z'],
...     columns=['a', 'b', 'c'], ndim=2, freq='1 day')
>>> records = vbt.Records(wrapper, records_arr)
```

## Printing

There are two ways to print records:

* Raw dataframe that preserves field names and data types:

```pycon
>>> records.records
   id  col  idx  some_field
0   0    0    0        10.0
1   1    0    1        11.0
2   2    0    2        12.0
3   3    1    0        13.0
4   4    1    1        14.0
5   5    1    2        15.0
6   6    2    0        16.0
7   7    2    1        17.0
8   8    2    2        18.0
```

* Readable dataframe that takes into consideration `Records.field_config`:

```pycon
>>> records.records_readable
   Id Column Timestamp  some_field
0   0      a         x        10.0
1   1      a         y        11.0
2   2      a         z        12.0
3   3      b         x        13.0
4   4      b         y        14.0
5   5      b         z        15.0
6   6      c         x        16.0
7   7      c         y        17.0
8   8      c         z        18.0
```

## Mapping

`Records` are just [structured arrays](https://numpy.org/doc/stable/user/basics.rec.html) with a bunch
of methods and properties for processing them. Their main feature is to map the records array and
to reduce it by column (similar to the MapReduce paradigm). The main advantage is that it all happens
without conversion to the matrix form and wasting memory resources.

`Records` can be mapped to `vectorbt.records.mapped_array.MappedArray` in several ways:

* Use `Records.map_field` to map a record field:

```pycon
>>> records.map_field('some_field')
<vectorbt.records.mapped_array.MappedArray at 0x7ff49bd31a58>

>>> records.map_field('some_field').values
array([10., 11., 12., 13., 14., 15., 16., 17., 18.])
```

* Use `Records.map` to map records using a custom function.

```pycon
>>> @njit
... def power_map_nb(record, pow):
...     return record.some_field ** pow

>>> records.map(power_map_nb, 2)
<vectorbt.records.mapped_array.MappedArray at 0x7ff49c990cf8>

>>> records.map(power_map_nb, 2).values
array([100., 121., 144., 169., 196., 225., 256., 289., 324.])
```

* Use `Records.map_array` to convert an array to `vectorbt.records.mapped_array.MappedArray`.

```pycon
>>> records.map_array(records_arr['some_field'] ** 2)
<vectorbt.records.mapped_array.MappedArray object at 0x7fe9bccf2978>

>>> records.map_array(records_arr['some_field'] ** 2).values
array([100., 121., 144., 169., 196., 225., 256., 289., 324.])
```

* Use `Records.apply` to apply a function on each column/group:

```pycon
>>> @njit
... def cumsum_apply_nb(records):
...     return np.cumsum(records.some_field)

>>> records.apply(cumsum_apply_nb)
<vectorbt.records.mapped_array.MappedArray at 0x7ff49c990cf8>

>>> records.apply(cumsum_apply_nb).values
array([10., 21., 33., 13., 27., 42., 16., 33., 51.])

>>> group_by = np.array(['first', 'first', 'second'])
>>> records.apply(cumsum_apply_nb, group_by=group_by, apply_per_group=True).values
array([10., 21., 33., 46., 60., 75., 16., 33., 51.])
```

Notice how cumsum resets at each column in the first example and at each group in the second example.

## Filtering

Use `Records.apply_mask` to filter elements per column/group:

```pycon
>>> mask = [True, False, True, False, True, False, True, False, True]
>>> filtered_records = records.apply_mask(mask)
>>> filtered_records.count()
a    2
b    1
c    2
dtype: int64

>>> filtered_records.values['id']
array([0, 2, 4, 6, 8])
```

## Grouping

One of the key features of `Records` is that you can perform reducing operations on a group
of columns as if they were a single column. Groups can be specified by `group_by`, which
can be anything from positions or names of column levels, to a NumPy array with actual groups.

There are multiple ways of define grouping:

* When creating `Records`, pass `group_by` to `vectorbt.base.array_wrapper.ArrayWrapper`:

```pycon
>>> group_by = np.array(['first', 'first', 'second'])
>>> grouped_wrapper = wrapper.replace(group_by=group_by)
>>> grouped_records = vbt.Records(grouped_wrapper, records_arr)

>>> grouped_records.map_field('some_field').mean()
first     12.5
second    17.0
dtype: float64
```

* Regroup an existing `Records`:

```pycon
>>> records.regroup(group_by).map_field('some_field').mean()
first     12.5
second    17.0
dtype: float64
```

* Pass `group_by` directly to the mapping method:

```pycon
>>> records.map_field('some_field', group_by=group_by).mean()
first     12.5
second    17.0
dtype: float64
```

* Pass `group_by` directly to the reducing method:

```pycon
>>> records.map_field('some_field').mean(group_by=group_by)
a    11.0
b    14.0
c    17.0
dtype: float64
```

!!! note
    Grouping applies only to reducing operations, there is no change to the arrays.

## Indexing

Like any other class subclassing `vectorbt.base.array_wrapper.Wrapping`, we can do pandas indexing
on a `Records` instance, which forwards indexing operation to each object with columns:

```pycon
>>> records['a'].records
   id  col  idx  some_field
0   0    0    0        10.0
1   1    0    1        11.0
2   2    0    2        12.0

>>> grouped_records['first'].records
   id  col  idx  some_field
0   0    0    0        10.0
1   1    0    1        11.0
2   2    0    2        12.0
3   3    1    0        13.0
4   4    1    1        14.0
5   5    1    2        15.0
```

!!! note
    Changing index (time axis) is not supported. The object should be treated as a Series
    rather than a DataFrame; for example, use `some_field.iloc[0]` instead of `some_field.iloc[:, 0]`.

    Indexing behavior depends solely upon `vectorbt.base.array_wrapper.ArrayWrapper`.
    For example, if `group_select` is enabled indexing will be performed on groups,
    otherwise on single columns.

## Caching

`Records` supports caching. If a method or a property requires heavy computation, it's wrapped
with `vectorbt.utils.decorators.cached_method` and `vectorbt.utils.decorators.cached_property`
respectively. Caching can be disabled globally via `caching` in `vectorbt._settings.settings`.

!!! note
    Because of caching, class is meant to be immutable and all properties are read-only.
    To change any attribute, use the `copy` method and pass the attribute as keyword argument.

## Saving and loading

Like any other class subclassing `vectorbt.utils.config.Pickleable`, we can save a `Records`
instance to the disk with `Records.save` and load it with `Records.load`.

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Records.metrics`.

```pycon
>>> records.stats(column='a')
Start                          x
End                            z
Period           3 days 00:00:00
Total Records                  3
Name: a, dtype: object
```

`Records.stats` also supports (re-)grouping:

```pycon
>>> grouped_records.stats(column='first')
Start                          x
End                            z
Period           3 days 00:00:00
Total Records                  6
Name: first, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `Records.subplots`.

This class is too generic to have any subplots, but feel free to add custom subplots to your subclass.

## Extending

`Records` class can be extended by subclassing.

In case some of our fields have the same meaning but different naming (such as the base field `idx`)
or other properties, we can override `field_config` using `vectorbt.records.decorators.override_field_config`.
It will look for configs of all base classes and merge our config on top of them. This preserves
any base class property that is not explicitly listed in our config.

```pycon
>>> from vectorbt.records.decorators import override_field_config

>>> my_dt = np.dtype([
...     ('my_id', np.int64),
...     ('my_col', np.int64),
...     ('my_idx', np.int64)
... ])

>>> my_fields_config = dict(
...     dtype=my_dt,
...     settings=dict(
...         id=dict(name='my_id'),
...         col=dict(name='my_col'),
...         idx=dict(name='my_idx')
...     )
... )
>>> @override_field_config(my_fields_config)
... class MyRecords(vbt.Records):
...     pass

>>> records_arr = np.array([
...     (0, 0, 0),
...     (1, 0, 1),
...     (2, 1, 0),
...     (3, 1, 1)
... ], dtype=my_dt)
>>> wrapper = vbt.ArrayWrapper(index=['x', 'y'],
...     columns=['a', 'b'], ndim=2, freq='1 day')
>>> my_records = MyRecords(wrapper, records_arr)

>>> my_records.id_arr
array([0, 1, 2, 3])

>>> my_records.col_arr
array([0, 0, 1, 1])

>>> my_records.idx_arr
array([0, 1, 0, 1])
```

Alternatively, we can override the `_field_config` class attribute.

```pycon
>>> @override_field_config
... class MyRecords(vbt.Records):
...     _field_config = dict(
...         dtype=my_dt,
...         settings=dict(
...             id=dict(name='my_id'),
...             idx=dict(name='my_idx'),
...             col=dict(name='my_col')
...         )
...     )
```

!!! note
    Don't forget to decorate the class with `@override_field_config` to inherit configs from base classes.

    You can stop inheritance by not decorating or passing `merge_configs=False` to the decorator.
"""

import inspect
import string

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.base.reshape_fns import to_1d_array
from vectorbt.generic.plots_builder import PlotsBuilderMixin
from vectorbt.generic.stats_builder import StatsBuilderMixin
from vectorbt.records import nb
from vectorbt.records.col_mapper import ColumnMapper
from vectorbt.records.mapped_array import MappedArray
from vectorbt.utils import checks
from vectorbt.utils.attr_ import get_dict_attr
from vectorbt.utils.config import merge_dicts, Config, Configured
from vectorbt.utils.decorators import cached_method

__pdoc__ = {}

RecordsT = tp.TypeVar("RecordsT", bound="Records")
IndexingMetaT = tp.Tuple[ArrayWrapper, tp.RecordArray, tp.MaybeArray, tp.Array1d]


class MetaFields(type):
    """Meta class that exposes a read-only class property `MetaFields.field_config`."""

    @property
    def field_config(cls) -> Config:
        """Field config."""
        return cls._field_config


class RecordsWithFields(metaclass=MetaFields):
    """Class exposes a read-only class property `RecordsWithFields.field_config`."""

    @property
    def field_config(self) -> Config:
        """Field config of `${cls_name}`.

        ```json
        ${field_config}
        ```
        """
        return self._field_config


class MetaRecords(type(StatsBuilderMixin), type(PlotsBuilderMixin), type(RecordsWithFields)):
    pass


class Records(Wrapping, StatsBuilderMixin, PlotsBuilderMixin, RecordsWithFields, metaclass=MetaRecords):
    """Wraps the actual records array (such as trades) and exposes methods for mapping
    it to some array of values (such as PnL of each trade).

    Args:
        wrapper (ArrayWrapper): Array wrapper.

            See `vectorbt.base.array_wrapper.ArrayWrapper`.
        records_arr (array_like): A structured NumPy array of records.

            Must have the fields `id` (record index) and `col` (column index).
        col_mapper (ColumnMapper): Column mapper if already known.

            !!! note
                It depends on `records_arr`, so make sure to invalidate `col_mapper` upon creating
                a `Records` instance with a modified `records_arr`.

                `Records.replace` does it automatically.
        **kwargs: Custom keyword arguments passed to the config.

            Useful if any subclass wants to extend the config.
    """

    _field_config: tp.ClassVar[Config] = Config(
        dict(
            dtype=None,
            settings=dict(
                id=dict(
                    name='id',
                    title='Id'
                ),
                col=dict(
                    name='col',
                    title='Column',
                    mapping='columns'
                ),
                idx=dict(
                    name='idx',
                    title='Timestamp',
                    mapping='index'
                )
            )
        ),
        readonly=True,
        as_attrs=False
    )

    @property
    def field_config(self) -> Config:
        """Field config of `${cls_name}`.

        ```json
        ${field_config}
        ```
        """
        return self._field_config

    def __init__(self,
                 wrapper: ArrayWrapper,
                 records_arr: tp.RecordArray,
                 col_mapper: tp.Optional[ColumnMapper] = None,
                 **kwargs) -> None:
        Wrapping.__init__(
            self,
            wrapper,
            records_arr=records_arr,
            col_mapper=col_mapper,
            **kwargs
        )
        StatsBuilderMixin.__init__(self)

        # Check fields
        records_arr = np.asarray(records_arr)
        checks.assert_not_none(records_arr.dtype.fields)
        field_names = {
            dct.get('name', field_name)
            for field_name, dct in self.field_config.get('settings', {}).items()
        }
        dtype = self.field_config.get('dtype', None)
        if dtype is not None:
            for field in dtype.names:
                if field not in records_arr.dtype.names:
                    if field not in field_names:
                        raise TypeError(f"Field '{field}' from {dtype} cannot be found in records or config")

        self._records_arr = records_arr
        if col_mapper is None:
            col_mapper = ColumnMapper(wrapper, self.col_arr)
        self._col_mapper = col_mapper

    def replace(self: RecordsT, **kwargs) -> RecordsT:
        """See `vectorbt.utils.config.Configured.replace`.

        Also, makes sure that `Records.col_mapper` is not passed to the new instance."""
        if self.config.get('col_mapper', None) is not None:
            if 'wrapper' in kwargs:
                if self.wrapper is not kwargs.get('wrapper'):
                    kwargs['col_mapper'] = None
            if 'records_arr' in kwargs:
                if self.records_arr is not kwargs.get('records_arr'):
                    kwargs['col_mapper'] = None
        return Configured.replace(self, **kwargs)

    def get_by_col_idxs(self, col_idxs: tp.Array1d) -> tp.RecordArray:
        """Get records corresponding to column indices.

        Returns new records array."""
        if self.col_mapper.is_sorted():
            new_records_arr = nb.record_col_range_select_nb(
                self.values, self.col_mapper.col_range, to_1d_array(col_idxs))  # faster
        else:
            new_records_arr = nb.record_col_map_select_nb(
                self.values, self.col_mapper.col_map, to_1d_array(col_idxs))
        return new_records_arr

    def indexing_func_meta(self, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> IndexingMetaT:
        """Perform indexing on `Records` and return metadata."""
        new_wrapper, _, group_idxs, col_idxs = \
            self.wrapper.indexing_func_meta(pd_indexing_func, column_only_select=True, **kwargs)
        new_records_arr = self.get_by_col_idxs(col_idxs)
        return new_wrapper, new_records_arr, group_idxs, col_idxs

    def indexing_func(self: RecordsT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> RecordsT:
        """Perform indexing on `Records`."""
        new_wrapper, new_records_arr, _, _ = self.indexing_func_meta(pd_indexing_func, **kwargs)
        return self.replace(
            wrapper=new_wrapper,
            records_arr=new_records_arr
        )

    @property
    def records_arr(self) -> tp.RecordArray:
        """Records array."""
        return self._records_arr

    @property
    def values(self) -> tp.RecordArray:
        """Records array."""
        return self.records_arr

    def __len__(self) -> int:
        return len(self.values)

    @property
    def records(self) -> tp.Frame:
        """Records."""
        return pd.DataFrame.from_records(self.values)

    @property
    def recarray(self) -> tp.RecArray:
        return self.values.view(np.recarray)

    @property
    def col_mapper(self) -> ColumnMapper:
        """Column mapper.

        See `vectorbt.records.col_mapper.ColumnMapper`."""
        return self._col_mapper

    @property
    def records_readable(self) -> tp.Frame:
        """Records in readable format."""
        df = self.records.copy()
        field_settings = self.field_config.get('settings', {})
        for col_name in df.columns:
            if col_name in field_settings:
                dct = field_settings[col_name]
                if dct.get('ignore', False):
                    df = df.drop(columns=col_name)
                    continue
                field_name = dct.get('name', col_name)
                if 'title' in dct:
                    title = dct['title']
                    new_columns = dict()
                    new_columns[field_name] = title
                    df.rename(columns=new_columns, inplace=True)
                else:
                    title = field_name
                if 'mapping' in dct:
                    if isinstance(dct['mapping'], str) and dct['mapping'] == 'index':
                        df[title] = self.get_map_field_to_index(col_name)
                    else:
                        df[title] = self.get_apply_mapping_arr(col_name)
        return df

    def get_field_setting(self, field: str, setting: str, default: tp.Any = None) -> tp.Any:
        """Resolve any setting of the field. Uses `Records.field_config`."""
        return self.field_config.get('settings', {}).get(field, {}).get(setting, default)

    def get_field_name(self, field: str) -> str:
        """Resolve the name of the field. Uses `Records.field_config`.."""
        return self.get_field_setting(field, 'name', field)

    def get_field_title(self, field: str) -> str:
        """Resolve the title of the field. Uses `Records.field_config`."""
        return self.get_field_setting(field, 'title', field)

    def get_field_mapping(self, field: str) -> tp.Optional[tp.MappingLike]:
        """Resolve the mapping of the field. Uses `Records.field_config`."""
        return self.get_field_setting(field, 'mapping', None)

    def get_field_arr(self, field: str) -> tp.Array1d:
        """Resolve the array of the field. Uses `Records.field_config`."""
        return self.values[self.get_field_name(field)]

    def get_map_field(self, field: str, **kwargs) -> MappedArray:
        """Resolve the mapped array of the field. Uses `Records.field_config`."""
        return self.map_field(self.get_field_name(field), mapping=self.get_field_mapping(field), **kwargs)

    def get_apply_mapping_arr(self, field: str, **kwargs) -> tp.Array1d:
        """Resolve the mapped array on the field, with mapping applied. Uses `Records.field_config`."""
        return self.get_map_field(field, **kwargs).apply_mapping().values

    def get_map_field_to_index(self, field: str, **kwargs) -> tp.Index:
        """Resolve the mapped array on the field, with index applied. Uses `Records.field_config`."""
        return self.get_map_field(field, **kwargs).to_index()

    @property
    def id_arr(self) -> tp.Array1d:
        """Get id array."""
        return self.values[self.get_field_name('id')]

    @property
    def col_arr(self) -> tp.Array1d:
        """Get column array."""
        return self.values[self.get_field_name('col')]

    @property
    def idx_arr(self) -> tp.Optional[tp.Array1d]:
        """Get index array."""
        idx_field_name = self.get_field_name('idx')
        if idx_field_name is None:
            return None
        return self.values[idx_field_name]

    @cached_method
    def is_sorted(self, incl_id: bool = False) -> bool:
        """Check whether records are sorted."""
        if incl_id:
            return nb.is_col_idx_sorted_nb(self.col_arr, self.id_arr)
        return nb.is_col_sorted_nb(self.col_arr)

    def sort(self: RecordsT, incl_id: bool = False, group_by: tp.GroupByLike = None, **kwargs) -> RecordsT:
        """Sort records by columns (primary) and ids (secondary, optional).

        !!! note
            Sorting is expensive. A better approach is to append records already in the correct order."""
        if self.is_sorted(incl_id=incl_id):
            return self.replace(**kwargs).regroup(group_by)
        if incl_id:
            ind = np.lexsort((self.id_arr, self.col_arr))  # expensive!
        else:
            ind = np.argsort(self.col_arr)
        return self.replace(records_arr=self.values[ind], **kwargs).regroup(group_by)

    def apply_mask(self: RecordsT, mask: tp.Array1d, group_by: tp.GroupByLike = None, **kwargs) -> RecordsT:
        """Return a new class instance, filtered by mask."""
        mask_indices = np.flatnonzero(mask)
        return self.replace(
            records_arr=np.take(self.values, mask_indices),
            **kwargs
        ).regroup(group_by)

    def map_array(self,
                  a: tp.ArrayLike,
                  idx_arr: tp.Optional[tp.ArrayLike] = None,
                  mapping: tp.Optional[tp.MappingLike] = None,
                  group_by: tp.GroupByLike = None,
                  **kwargs) -> MappedArray:
        """Convert array to mapped array.

         The length of the array should match that of the records."""
        if not isinstance(a, np.ndarray):
            a = np.asarray(a)
        checks.assert_shape_equal(a, self.values)
        if idx_arr is None:
            idx_arr = self.idx_arr
        return MappedArray(
            self.wrapper,
            a,
            self.col_arr,
            id_arr=self.id_arr,
            idx_arr=idx_arr,
            mapping=mapping,
            col_mapper=self.col_mapper,
            **kwargs
        ).regroup(group_by)

    def map_field(self, field: str, **kwargs) -> MappedArray:
        """Convert field to mapped array.

        `**kwargs` are passed to `Records.map_array`."""
        mapped_arr = self.values[field]
        return self.map_array(mapped_arr, **kwargs)

    def map(self,
            map_func_nb: tp.RecordMapFunc, *args,
            dtype: tp.Optional[tp.DTypeLike] = None,
            **kwargs) -> MappedArray:
        """Map each record to a scalar value. Returns mapped array.

        See `vectorbt.records.nb.map_records_nb`.

        `**kwargs` are passed to `Records.map_array`."""
        checks.assert_numba_func(map_func_nb)
        mapped_arr = nb.map_records_nb(self.values, map_func_nb, *args)
        mapped_arr = np.asarray(mapped_arr, dtype=dtype)
        return self.map_array(mapped_arr, **kwargs)

    def apply(self,
              apply_func_nb: tp.RecordApplyFunc, *args,
              group_by: tp.GroupByLike = None,
              apply_per_group: bool = False,
              dtype: tp.Optional[tp.DTypeLike] = None,
              **kwargs) -> MappedArray:
        """Apply function on records per column/group. Returns mapped array.

        Applies per group if `apply_per_group` is True.

        See `vectorbt.records.nb.apply_on_records_nb`.

        `**kwargs` are passed to `Records.map_array`."""
        checks.assert_numba_func(apply_func_nb)
        if apply_per_group:
            col_map = self.col_mapper.get_col_map(group_by=group_by)
        else:
            col_map = self.col_mapper.get_col_map(group_by=False)
        mapped_arr = nb.apply_on_records_nb(self.values, col_map, apply_func_nb, *args)
        mapped_arr = np.asarray(mapped_arr, dtype=dtype)
        return self.map_array(mapped_arr, group_by=group_by, **kwargs)

    @cached_method
    def count(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Return count by column."""
        wrap_kwargs = merge_dicts(dict(name_or_index='count'), wrap_kwargs)
        return self.wrapper.wrap_reduced(
            self.col_mapper.get_col_map(group_by=group_by)[1],
            group_by=group_by, **wrap_kwargs)

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Records.stats`.

        Merges `vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults` and
        `records.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        records_stats_cfg = settings['records']['stats']

        return merge_dicts(
            StatsBuilderMixin.stats_defaults.__get__(self),
            records_stats_cfg
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
                tags='records'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Records.plots`.

        Merges `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults` and
        `records.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        records_plots_cfg = settings['records']['plots']

        return merge_dicts(
            PlotsBuilderMixin.plots_defaults.__get__(self),
            records_plots_cfg
        )

    @property
    def subplots(self) -> Config:
        return self._subplots

    # ############# Docs ############# #

    @classmethod
    def build_field_config_doc(cls, source_cls: tp.Optional[type] = None) -> str:
        """Build field config documentation."""
        if source_cls is None:
            source_cls = Records
        return string.Template(
            inspect.cleandoc(get_dict_attr(source_cls, 'field_config').__doc__)
        ).substitute(
            {'field_config': cls.field_config.to_doc(), 'cls_name': cls.__name__}
        )

    @classmethod
    def override_field_config_doc(cls, __pdoc__: dict, source_cls: tp.Optional[type] = None) -> None:
        """Call this method on each subclass that overrides `field_config`."""
        __pdoc__[cls.__name__ + '.field_config'] = cls.build_field_config_doc(source_cls=source_cls)


Records.override_field_config_doc(__pdoc__)
Records.override_metrics_doc(__pdoc__)
Records.override_subplots_doc(__pdoc__)
