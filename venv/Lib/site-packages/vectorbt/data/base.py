# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base data class.

Class `Data` allows storing, downloading, updating, and managing data. It stores data
as a dictionary of Series/DataFrames keyed by symbol, and makes sure that
all pandas objects have the same index and columns by aligning them.

## Downloading

Data can be downloaded by overriding the `Data.download_symbol` class method. What `Data` does
under the hood is iterating over all symbols and calling this method.

Let's create a simple data class `RandomData` that generates price based on
random returns with provided mean and standard deviation:

```pycon
>>> import numpy as np
>>> import pandas as pd
>>> import vectorbt as vbt

>>> class RandomData(vbt.Data):
...     @classmethod
...     def download_symbol(cls, symbol, mean=0., stdev=0.1, start_value=100,
...                         start_dt='2021-01-01', end_dt='2021-01-10'):
...         index = pd.date_range(start_dt, end_dt)
...         rand_returns = np.random.normal(mean, stdev, size=len(index))
...         rand_price = start_value + np.cumprod(rand_returns + 1)
...         return pd.Series(rand_price, index=index)

>>> rand_data = RandomData.download(['RANDNX1', 'RANDNX2'])
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  101.042956  100.920462
2021-01-02  100.987327  100.956455
2021-01-03  101.022333  100.955128
2021-01-04  101.084243  100.791793
2021-01-05  101.158619  100.781000
2021-01-06  101.172688  100.786198
2021-01-07  101.311609  100.848192
2021-01-08  101.331841  100.861500
2021-01-09  101.440530  100.944935
2021-01-10  101.585689  100.993223
```

To provide different keyword arguments for different symbols, we can use `symbol_dict`:

```pycon
>>> start_value = vbt.symbol_dict({'RANDNX2': 200})
>>> rand_data = RandomData.download(['RANDNX1', 'RANDNX2'], start_value=start_value)
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  101.083324  200.886078
2021-01-02  101.113405  200.791934
2021-01-03  101.169194  200.852877
2021-01-04  101.164033  200.820111
2021-01-05  101.326248  201.060448
2021-01-06  101.394482  200.876984
2021-01-07  101.494227  200.845519
2021-01-08  101.422012  200.963474
2021-01-09  101.493162  200.790369
2021-01-10  101.606052  200.752296
```

In case two symbols have different index or columns, they are automatically aligned based on
`missing_index` and `missing_columns` respectively (see `data` in `vectorbt._settings.settings`):

```pycon
>>> start_dt = vbt.symbol_dict({'RANDNX2': '2021-01-03'})
>>> end_dt = vbt.symbol_dict({'RANDNX2': '2021-01-07'})
>>> rand_data = RandomData.download(
...     ['RANDNX1', 'RANDNX2'], start_value=start_value,
...     start_dt=start_dt, end_dt=end_dt)
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  101.028054         NaN
2021-01-02  101.032090         NaN
2021-01-03  101.038531  200.936283
2021-01-04  101.068265  200.926764
2021-01-05  100.878492  200.898898
2021-01-06  100.857444  200.922368
2021-01-07  100.933123  200.987094
2021-01-08  100.938034         NaN
2021-01-09  101.044736         NaN
2021-01-10  101.098133         NaN
```

## Updating

Updating can be implemented by overriding the `Data.update_symbol` instance method, which takes
the same arguments as `Data.download_symbol`. In contrast to the download method, the update
method is an instance method and can access the data downloaded earlier. It can also access the
keyword arguments initially passed to the download method, accessible under `Data.download_kwargs`.
Those arguments can be used as default arguments and overridden by arguments passed directly
to the update method, using `vectorbt.utils.config.merge_dicts`.

Let's define an update method that updates the latest data point and adds two news data points.
Note that updating data always returns a new `Data` instance.

```pycon
>>> from datetime import timedelta
>>> from vectorbt.utils.config import merge_dicts

>>> class RandomData(vbt.Data):
...     @classmethod
...     def download_symbol(cls, symbol, mean=0., stdev=0.1, start_value=100,
...                         start_dt='2021-01-01', end_dt='2021-01-10'):
...         index = pd.date_range(start_dt, end_dt)
...         rand_returns = np.random.normal(mean, stdev, size=len(index))
...         rand_price = start_value + np.cumprod(rand_returns + 1)
...         return pd.Series(rand_price, index=index)
...
...     def update_symbol(self, symbol, **kwargs):
...         download_kwargs = self.select_symbol_kwargs(symbol, self.download_kwargs)
...         download_kwargs['start_dt'] = self.data[symbol].index[-1]
...         download_kwargs['end_dt'] = download_kwargs['start_dt'] + timedelta(days=2)
...         kwargs = merge_dicts(download_kwargs, kwargs)
...         return self.download_symbol(symbol, **kwargs)

>>> rand_data = RandomData.download(['RANDNX1', 'RANDNX2'], end_dt='2021-01-05')
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  100.956601  100.970865
2021-01-02  100.919011  100.987026
2021-01-03  101.062733  100.835376
2021-01-04  100.960535  100.820817
2021-01-05  100.834387  100.866549

>>> rand_data = rand_data.update()
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  100.956601  100.970865
2021-01-02  100.919011  100.987026
2021-01-03  101.062733  100.835376
2021-01-04  100.960535  100.820817
2021-01-05  101.011255  100.887049 < updated from here
2021-01-06  101.004149  100.808410
2021-01-07  101.023673  100.714583

>>> rand_data = rand_data.update()
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  100.956601  100.970865
2021-01-02  100.919011  100.987026
2021-01-03  101.062733  100.835376
2021-01-04  100.960535  100.820817
2021-01-05  101.011255  100.887049
2021-01-06  101.004149  100.808410
2021-01-07  100.883400  100.874922 < updated from here
2021-01-08  101.011738  100.780188
2021-01-09  100.912639  100.934014
```

## Merging

You can merge symbols from different `Data` instances either by subclassing `Data` and
defining custom download and update methods, or by manually merging their data dicts
into one data dict and passing it to the `Data.from_data` class method.

```pycon
>>> rand_data1 = RandomData.download('RANDNX1', mean=0.2)
>>> rand_data2 = RandomData.download('RANDNX2', start_value=200, start_dt='2021-01-05')
>>> merged_data = vbt.Data.from_data(vbt.merge_dicts(rand_data1.data, rand_data2.data))
>>> merged_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  101.160718         NaN
2021-01-02  101.421020         NaN
2021-01-03  101.959176         NaN
2021-01-04  102.076670         NaN
2021-01-05  102.447234  200.916198
2021-01-06  103.195187  201.033907
2021-01-07  103.595915  200.908229
2021-01-08  104.332550  201.000497
2021-01-09  105.159708  201.019157
2021-01-10  106.729495  200.910210
```

## Indexing

Like any other class subclassing `vectorbt.base.array_wrapper.Wrapping`, we can do pandas indexing
on a `Data` instance, which forwards indexing operation to each Series/DataFrame:

```pycon
>>> rand_data.loc['2021-01-07':'2021-01-09']
<__main__.RandomData at 0x7fdba4e36198>

>>> rand_data.loc['2021-01-07':'2021-01-09'].get()
symbol         RANDNX1     RANDNX2
2021-01-07  100.883400  100.874922
2021-01-08  101.011738  100.780188
2021-01-09  100.912639  100.934014
```

## Saving and loading

Like any other class subclassing `vectorbt.utils.config.Pickleable`, we can save a `Data`
instance to the disk with `Data.save` and load it with `Data.load`:

```pycon
>>> rand_data.save('rand_data')
>>> rand_data = RandomData.load('rand_data')
>>> rand_data.get()
symbol         RANDNX1     RANDNX2
2021-01-01  100.956601  100.970865
2021-01-02  100.919011  100.987026
2021-01-03  101.062733  100.835376
2021-01-04  100.960535  100.820817
2021-01-05  101.011255  100.887049
2021-01-06  101.004149  100.808410
2021-01-07  100.883400  100.874922
2021-01-08  101.011738  100.780188
2021-01-09  100.912639  100.934014
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Data.metrics`.

```pycon
>>> rand_data = RandomData.download(['RANDNX1', 'RANDNX2'])

>>> rand_data.stats(column='a')
Start                   2021-01-01 00:00:00+00:00
End                     2021-01-10 00:00:00+00:00
Period                           10 days 00:00:00
Total Symbols                                   2
Null Counts: RANDNX1                            0
Null Counts: RANDNX2                            0
dtype: object
```

`Data.stats` also supports (re-)grouping:

```pycon
>>> rand_data.stats(group_by=True)
Start                   2021-01-01 00:00:00+00:00
End                     2021-01-10 00:00:00+00:00
Period                           10 days 00:00:00
Total Symbols                                   2
Null Counts: RANDNX1                            0
Null Counts: RANDNX2                            0
Name: group, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `Data.subplots`.

`Data` class has a single subplot based on `Data.plot`:

```pycon
>>> rand_data.plots(settings=dict(base=100)).show_svg()
```

![](/assets/images/data_plots.svg)
"""

import warnings

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.generic import plotting
from vectorbt.generic.plots_builder import PlotsBuilderMixin
from vectorbt.generic.stats_builder import StatsBuilderMixin
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.datetime_ import is_tz_aware, to_timezone
from vectorbt.utils.decorators import cached_method

__pdoc__ = {}


class symbol_dict(dict):
    """Dict that contains symbols as keys."""
    pass


class MetaData(type(StatsBuilderMixin), type(PlotsBuilderMixin)):
    pass


DataT = tp.TypeVar("DataT", bound="Data")


class Data(Wrapping, StatsBuilderMixin, PlotsBuilderMixin, metaclass=MetaData):
    """Class that downloads, updates, and manages data coming from a data source."""

    def __init__(self,
                 wrapper: ArrayWrapper,
                 data: tp.Data,
                 tz_localize: tp.Optional[tp.TimezoneLike],
                 tz_convert: tp.Optional[tp.TimezoneLike],
                 missing_index: str,
                 missing_columns: str,
                 download_kwargs: dict,
                 **kwargs) -> None:
        Wrapping.__init__(
            self,
            wrapper,
            data=data,
            tz_localize=tz_localize,
            tz_convert=tz_convert,
            missing_index=missing_index,
            missing_columns=missing_columns,
            download_kwargs=download_kwargs,
            **kwargs
        )
        StatsBuilderMixin.__init__(self)
        PlotsBuilderMixin.__init__(self)

        checks.assert_instance_of(data, dict)
        for k, v in data.items():
            checks.assert_meta_equal(v, data[list(data.keys())[0]])
        self._data = data
        self._tz_localize = tz_localize
        self._tz_convert = tz_convert
        self._missing_index = missing_index
        self._missing_columns = missing_columns
        self._download_kwargs = download_kwargs

    def indexing_func(self: DataT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> DataT:
        """Perform indexing on `Data`."""
        new_wrapper = pd_indexing_func(self.wrapper)
        new_data = {k: pd_indexing_func(v) for k, v in self.data.items()}
        return self.replace(
            wrapper=new_wrapper,
            data=new_data
        )

    @property
    def data(self) -> tp.Data:
        """Data dictionary keyed by symbol."""
        return self._data

    @property
    def symbols(self) -> tp.List[tp.Label]:
        """List of symbols."""
        return list(self.data.keys())

    @property
    def tz_localize(self) -> tp.Optional[tp.TimezoneLike]:
        """`tz_localize` initially passed to `Data.download_symbol`."""
        return self._tz_localize

    @property
    def tz_convert(self) -> tp.Optional[tp.TimezoneLike]:
        """`tz_convert` initially passed to `Data.download_symbol`."""
        return self._tz_convert

    @property
    def missing_index(self) -> str:
        """`missing_index` initially passed to `Data.download_symbol`."""
        return self._missing_index

    @property
    def missing_columns(self) -> str:
        """`missing_columns` initially passed to `Data.download_symbol`."""
        return self._missing_columns

    @property
    def download_kwargs(self) -> dict:
        """Keyword arguments initially passed to `Data.download_symbol`."""
        return self._download_kwargs

    @classmethod
    def align_index(cls, data: tp.Data, missing: str = 'nan') -> tp.Data:
        """Align data to have the same index.

        The argument `missing` accepts the following values:

        * 'nan': set missing data points to NaN
        * 'drop': remove missing data points
        * 'raise': raise an error"""
        if len(data) == 1:
            return data

        index = None
        for k, v in data.items():
            if index is None:
                index = v.index
            else:
                if len(index.intersection(v.index)) != len(index.union(v.index)):
                    if missing == 'nan':
                        warnings.warn("Symbols have mismatching index. "
                                      "Setting missing data points to NaN.", stacklevel=2)
                        index = index.union(v.index)
                    elif missing == 'drop':
                        warnings.warn("Symbols have mismatching index. "
                                      "Dropping missing data points.", stacklevel=2)
                        index = index.intersection(v.index)
                    elif missing == 'raise':
                        raise ValueError("Symbols have mismatching index")
                    else:
                        raise ValueError(f"missing='{missing}' is not recognized")

        # reindex
        new_data = {k: v.reindex(index=index) for k, v in data.items()}
        return new_data

    @classmethod
    def align_columns(cls, data: tp.Data, missing: str = 'raise') -> tp.Data:
        """Align data to have the same columns.

        See `Data.align_index` for `missing`."""
        if len(data) == 1:
            return data

        columns = None
        multiple_columns = False
        name_is_none = False
        for k, v in data.items():
            if isinstance(v, pd.Series):
                if v.name is None:
                    name_is_none = True
                v = v.to_frame()
            else:
                multiple_columns = True
            if columns is None:
                columns = v.columns
            else:
                if len(columns.intersection(v.columns)) != len(columns.union(v.columns)):
                    if missing == 'nan':
                        warnings.warn("Symbols have mismatching columns. "
                                      "Setting missing data points to NaN.", stacklevel=2)
                        columns = columns.union(v.columns)
                    elif missing == 'drop':
                        warnings.warn("Symbols have mismatching columns. "
                                      "Dropping missing data points.", stacklevel=2)
                        columns = columns.intersection(v.columns)
                    elif missing == 'raise':
                        raise ValueError("Symbols have mismatching columns")
                    else:
                        raise ValueError(f"missing='{missing}' is not recognized")

        # reindex
        new_data = {}
        for k, v in data.items():
            if isinstance(v, pd.Series):
                v = v.to_frame()
            v = v.reindex(columns=columns)
            if not multiple_columns:
                v = v[columns[0]]
                if name_is_none:
                    v = v.rename(None)
            new_data[k] = v
        return new_data

    @classmethod
    def select_symbol_kwargs(cls, symbol: tp.Label, kwargs: dict) -> dict:
        """Select keyword arguments belonging to `symbol`."""
        _kwargs = dict()
        for k, v in kwargs.items():
            if isinstance(v, symbol_dict):
                if symbol in v:
                    _kwargs[k] = v[symbol]
            else:
                _kwargs[k] = v
        return _kwargs

    @classmethod
    def from_data(cls: tp.Type[DataT],
                  data: tp.Data,
                  tz_localize: tp.Optional[tp.TimezoneLike] = None,
                  tz_convert: tp.Optional[tp.TimezoneLike] = None,
                  missing_index: tp.Optional[str] = None,
                  missing_columns: tp.Optional[str] = None,
                  wrapper_kwargs: tp.KwargsLike = None,
                  **kwargs) -> DataT:
        """Create a new `Data` instance from (aligned) data.

        Args:
            data (dict): Dictionary of array-like objects keyed by symbol.
            tz_localize (timezone_like): If the index is tz-naive, convert to a timezone.

                See `vectorbt.utils.datetime_.to_timezone`.
            tz_convert (timezone_like): Convert the index from one timezone to another.

                See `vectorbt.utils.datetime_.to_timezone`.
            missing_index (str): See `Data.align_index`.
            missing_columns (str): See `Data.align_columns`.
            wrapper_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper`.
            **kwargs: Keyword arguments passed to the `__init__` method.

        For defaults, see `data` in `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        data_cfg = settings['data']

        # Get global defaults
        if tz_localize is None:
            tz_localize = data_cfg['tz_localize']
        if tz_convert is None:
            tz_convert = data_cfg['tz_convert']
        if missing_index is None:
            missing_index = data_cfg['missing_index']
        if missing_columns is None:
            missing_columns = data_cfg['missing_columns']
        if wrapper_kwargs is None:
            wrapper_kwargs = {}

        data = data.copy()
        for k, v in data.items():
            # Convert array to pandas
            if not isinstance(v, (pd.Series, pd.DataFrame)):
                v = np.asarray(v)
                if v.ndim == 1:
                    v = pd.Series(v)
                else:
                    v = pd.DataFrame(v)

            # Perform operations with datetime-like index
            if isinstance(v.index, pd.DatetimeIndex):
                if tz_localize is not None:
                    if not is_tz_aware(v.index):
                        v = v.tz_localize(to_timezone(tz_localize))
                if tz_convert is not None:
                    v = v.tz_convert(to_timezone(tz_convert))
                v.index.freq = v.index.inferred_freq
            data[k] = v

        # Align index and columns
        data = cls.align_index(data, missing=missing_index)
        data = cls.align_columns(data, missing=missing_columns)

        # Create new instance
        symbols = list(data.keys())
        wrapper = ArrayWrapper.from_obj(data[symbols[0]], **wrapper_kwargs)
        return cls(
            wrapper,
            data,
            tz_localize=tz_localize,
            tz_convert=tz_convert,
            missing_index=missing_index,
            missing_columns=missing_columns,
            **kwargs
        )

    @classmethod
    def download_symbol(cls, symbol: tp.Label, **kwargs) -> tp.SeriesFrame:
        """Abstract method to download a symbol."""
        raise NotImplementedError

    @classmethod
    def download(cls: tp.Type[DataT],
                 symbols: tp.Union[tp.Label, tp.Labels],
                 tz_localize: tp.Optional[tp.TimezoneLike] = None,
                 tz_convert: tp.Optional[tp.TimezoneLike] = None,
                 missing_index: tp.Optional[str] = None,
                 missing_columns: tp.Optional[str] = None,
                 wrapper_kwargs: tp.KwargsLike = None,
                 **kwargs) -> DataT:
        """Download data using `Data.download_symbol`.

        Args:
            symbols (hashable or sequence of hashable): One or multiple symbols.

                !!! note
                    Tuple is considered as a single symbol (since hashable).
            tz_localize (any): See `Data.from_data`.
            tz_convert (any): See `Data.from_data`.
            missing_index (str): See `Data.from_data`.
            missing_columns (str): See `Data.from_data`.
            wrapper_kwargs (dict): See `Data.from_data`.
            **kwargs: Passed to `Data.download_symbol`.

                If two symbols require different keyword arguments, pass `symbol_dict` for each argument.
        """
        if checks.is_hashable(symbols):
            symbols = [symbols]
        elif not checks.is_sequence(symbols):
            raise TypeError("Symbols must be either hashable or sequence of hashable")

        data = dict()
        for s in symbols:
            # Select keyword arguments for this symbol
            _kwargs = cls.select_symbol_kwargs(s, kwargs)

            # Download data for this symbol
            data[s] = cls.download_symbol(s, **_kwargs)

        # Create new instance from data
        return cls.from_data(
            data,
            tz_localize=tz_localize,
            tz_convert=tz_convert,
            missing_index=missing_index,
            missing_columns=missing_columns,
            wrapper_kwargs=wrapper_kwargs,
            download_kwargs=kwargs
        )

    def update_symbol(self, symbol: tp.Label, **kwargs) -> tp.SeriesFrame:
        """Abstract method to update a symbol."""
        raise NotImplementedError

    def update(self: DataT, **kwargs) -> DataT:
        """Update the data using `Data.update_symbol`.

        Args:
            **kwargs: Passed to `Data.update_symbol`.

                If two symbols require different keyword arguments, pass `symbol_dict` for each argument.

        !!! note
            Returns a new `Data` instance."""
        new_data = dict()
        for k, v in self.data.items():
            # Select keyword arguments for this symbol
            _kwargs = self.select_symbol_kwargs(k, kwargs)

            # Download new data for this symbol
            new_obj = self.update_symbol(k, **_kwargs)

            # Convert array to pandas
            if not isinstance(new_obj, (pd.Series, pd.DataFrame)):
                new_obj = np.asarray(new_obj)
                index = pd.RangeIndex(
                    start=v.index[-1],
                    stop=v.index[-1] + new_obj.shape[0],
                    step=1
                )
                if new_obj.ndim == 1:
                    new_obj = pd.Series(new_obj, index=index)
                else:
                    new_obj = pd.DataFrame(new_obj, index=index)

            # Perform operations with datetime-like index
            if isinstance(new_obj.index, pd.DatetimeIndex):
                if self.tz_localize is not None:
                    if not is_tz_aware(new_obj.index):
                        new_obj = new_obj.tz_localize(to_timezone(self.tz_localize))
                if self.tz_convert is not None:
                    new_obj = new_obj.tz_convert(to_timezone(self.tz_convert))

            new_data[k] = new_obj

        # Align index and columns
        new_data = self.align_index(new_data, missing=self.missing_index)
        new_data = self.align_columns(new_data, missing=self.missing_columns)

        # Concatenate old and new data
        for k, v in new_data.items():
            if isinstance(self.data[k], pd.Series):
                if isinstance(v, pd.DataFrame):
                    v = v[self.data[k].name]
            else:
                v = v[self.data[k].columns]
            v = pd.concat((self.data[k], v), axis=0)
            v = v[~v.index.duplicated(keep='last')]
            if isinstance(v.index, pd.DatetimeIndex):
                v.index.freq = v.index.inferred_freq
            new_data[k] = v

        # Create new instance
        new_index = new_data[self.symbols[0]].index
        return self.replace(
            wrapper=self.wrapper.replace(index=new_index),
            data=new_data
        )

    @cached_method
    def concat(self, level_name: str = 'symbol') -> tp.Data:
        """Return a dict of Series/DataFrames with symbols as columns, keyed by column name."""
        first_data = self.data[self.symbols[0]]
        index = first_data.index
        if isinstance(first_data, pd.Series):
            columns = pd.Index([first_data.name])
        else:
            columns = first_data.columns
        if len(self.symbols) > 1:
            new_data = {c: pd.DataFrame(
                index=index,
                columns=pd.Index(self.symbols, name=level_name)
            ) for c in columns}
        else:
            new_data = {c: pd.Series(
                index=index,
                name=self.symbols[0]
            ) for c in columns}
        for c in columns:
            for s in self.symbols:
                if isinstance(self.data[s], pd.Series):
                    col_data = self.data[s]
                else:
                    col_data = self.data[s][c]
                if len(self.symbols) > 1:
                    new_data[c].loc[:, s] = col_data
                else:
                    new_data[c].loc[:] = col_data
        for c in columns:
            new_data[c] = new_data[c].infer_objects()
        return new_data

    def get(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.MaybeTuple[tp.SeriesFrame]:
        """Get column data.

        If one symbol, returns data for that symbol.
        If multiple symbols, performs concatenation first and returns a DataFrame if one column
        and a tuple of DataFrames if a list of columns passed."""
        if len(self.symbols) == 1:
            if column is None:
                return self.data[self.symbols[0]]
            return self.data[self.symbols[0]][column]

        concat_data = self.concat(**kwargs)
        if len(concat_data) == 1:
            return tuple(concat_data.values())[0]
        if column is not None:
            if isinstance(column, list):
                return tuple([concat_data[c] for c in column])
            return concat_data[column]
        return tuple(concat_data.values())

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Data.stats`.

        Merges `vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults` and
        `data.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        data_stats_cfg = settings['data']['stats']

        return merge_dicts(
            StatsBuilderMixin.stats_defaults.__get__(self),
            data_stats_cfg
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
            total_symbols=dict(
                title='Total Symbols',
                calc_func=lambda self: len(self.symbols),
                agg_func=None,
                tags='data'
            ),
            null_counts=dict(
                title='Null Counts',
                calc_func=lambda self, group_by:
                {
                    k: v.isnull().vbt(wrapper=self.wrapper).sum(group_by=group_by)
                    for k, v in self.data.items()
                },
                tags='data'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             base: tp.Optional[float] = None,
             **kwargs) -> tp.Union[tp.BaseFigure, plotting.Scatter]:  # pragma: no cover
        """Plot orders.

        Args:
            column (str): Name of the column to plot.
            base (float): Rebase all series of a column to a given intial base.

                !!! note
                    The column should contain prices.
            kwargs (dict): Keyword arguments passed to `vectorbt.generic.accessors.GenericAccessor.plot`.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> start = '2021-01-01 UTC'  # crypto is in UTC
            >>> end = '2021-06-01 UTC'
            >>> data = vbt.YFData.download(['BTC-USD', 'ETH-USD', 'ADA-USD'], start=start, end=end)

            >>> data.plot(column='Close', base=1)
            ```

            ![](/assets/images/data_plot.svg)
        """
        self_col = self.select_one(column=column, group_by=False)
        data = self_col.get()
        if base is not None:
            data = data.vbt.rebase(base)
        return data.vbt.plot(**kwargs)

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Data.plots`.

        Merges `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults` and
        `data.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        data_plots_cfg = settings['data']['plots']

        return merge_dicts(
            PlotsBuilderMixin.plots_defaults.__get__(self),
            data_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            plot=dict(
                check_is_not_grouped=True,
                plot_func='plot',
                pass_add_trace_kwargs=True,
                tags='data'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


Data.override_metrics_doc(__pdoc__)
Data.override_subplots_doc(__pdoc__)
