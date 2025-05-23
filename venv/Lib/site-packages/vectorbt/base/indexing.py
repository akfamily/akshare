# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Classes for indexing.

The main purpose of indexing classes is to provide pandas-like indexing to user-defined classes
holding objects that have rows and/or columns. This is done by forwarding indexing commands
to each structured object and constructing the new user-defined class using them. This way,
one can manipulate complex classes with dozens of pandas objects using a single command."""

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base import index_fns, reshape_fns
from vectorbt.utils import checks


class IndexingError(Exception):
    """Exception raised when an indexing error has occurred."""


IndexingBaseT = tp.TypeVar("IndexingBaseT", bound="IndexingBase")


class IndexingBase:
    """Class that supports indexing through `IndexingBase.indexing_func`."""

    def indexing_func(self: IndexingBaseT, pd_indexing_func: tp.Callable, **kwargs) -> IndexingBaseT:
        """Apply `pd_indexing_func` on all pandas objects in question and return a new instance of the class.

        Should be overridden."""
        raise NotImplementedError


class LocBase:
    """Class that implements location-based indexing."""

    def __init__(self, indexing_func: tp.Callable, **kwargs) -> None:
        self._indexing_func = indexing_func
        self._indexing_kwargs = kwargs

    @property
    def indexing_func(self) -> tp.Callable:
        """Indexing function."""
        return self._indexing_func

    @property
    def indexing_kwargs(self) -> dict:
        """Keyword arguments passed to `LocBase.indexing_func`."""
        return self._indexing_kwargs

    def __getitem__(self, key: tp.Any) -> tp.Any:
        raise NotImplementedError


class iLoc(LocBase):
    """Forwards `pd.Series.iloc`/`pd.DataFrame.iloc` operation to each
    Series/DataFrame and returns a new class instance."""

    def __getitem__(self, key: tp.Any) -> tp.Any:
        return self.indexing_func(lambda x: x.iloc.__getitem__(key), **self.indexing_kwargs)


class Loc(LocBase):
    """Forwards `pd.Series.loc`/`pd.DataFrame.loc` operation to each
    Series/DataFrame and returns a new class instance."""

    def __getitem__(self, key: tp.Any) -> tp.Any:
        return self.indexing_func(lambda x: x.loc.__getitem__(key), **self.indexing_kwargs)


PandasIndexerT = tp.TypeVar("PandasIndexerT", bound="PandasIndexer")


class PandasIndexer(IndexingBase):
    """Implements indexing using `iloc`, `loc`, `xs` and `__getitem__`.

    Usage:
        ```pycon
        >>> import pandas as pd
        >>> from vectorbt.base.indexing import PandasIndexer

        >>> class C(PandasIndexer):
        ...     def __init__(self, df1, df2):
        ...         self.df1 = df1
        ...         self.df2 = df2
        ...         super().__init__()
        ...
        ...     def indexing_func(self, pd_indexing_func):
        ...         return self.__class__(
        ...             pd_indexing_func(self.df1),
        ...             pd_indexing_func(self.df2)
        ...         )

        >>> df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> df2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})
        >>> c = C(df1, df2)

        >>> c.iloc[:, 0]
        <__main__.C object at 0x1a1cacbbe0>

        >>> c.iloc[:, 0].df1
        0    1
        1    2
        Name: a, dtype: int64

        >>> c.iloc[:, 0].df2
        0    5
        1    6
        Name: a, dtype: int64
        ```
    """

    def __init__(self, **kwargs) -> None:
        self._iloc = iLoc(self.indexing_func, **kwargs)
        self._loc = Loc(self.indexing_func, **kwargs)
        self._indexing_kwargs = kwargs

    @property
    def indexing_kwargs(self) -> dict:
        """Indexing keyword arguments."""
        return self._indexing_kwargs

    @property
    def iloc(self) -> iLoc:
        """Purely integer-location based indexing for selection by position."""
        return self._iloc

    iloc.__doc__ = iLoc.__doc__

    @property
    def loc(self) -> Loc:
        """Purely label-location based indexer for selection by label."""
        return self._loc

    loc.__doc__ = Loc.__doc__

    def xs(self: PandasIndexerT, *args, **kwargs) -> PandasIndexerT:
        """Forwards `pd.Series.xs`/`pd.DataFrame.xs`
        operation to each Series/DataFrame and returns a new class instance."""
        return self.indexing_func(lambda x: x.xs(*args, **kwargs), **self.indexing_kwargs)

    def __getitem__(self: PandasIndexerT, key: tp.Any) -> PandasIndexerT:
        return self.indexing_func(lambda x: x.__getitem__(key), **self.indexing_kwargs)


class ParamLoc(LocBase):
    """Access a group of columns by parameter using `pd.Series.loc`.

    Uses `mapper` to establish link between columns and parameter values."""

    def __init__(self, mapper: tp.Series, indexing_func: tp.Callable, level_name: tp.Level = None, **kwargs) -> None:
        checks.assert_instance_of(mapper, pd.Series)

        if mapper.dtype == 'O':
            # If params are objects, we must cast them to string first
            # The original mapper isn't touched
            mapper = mapper.astype(str)
        self._mapper = mapper
        self._level_name = level_name

        LocBase.__init__(self, indexing_func, **kwargs)

    @property
    def mapper(self) -> tp.Series:
        """Mapper."""
        return self._mapper

    @property
    def level_name(self) -> tp.Level:
        """Level name."""
        return self._level_name

    def get_indices(self, key: tp.Any) -> tp.Array1d:
        """Get array of indices affected by this key."""
        if self.mapper.dtype == 'O':
            # We must also cast the key to string
            if isinstance(key, slice):
                start = str(key.start) if key.start is not None else None
                stop = str(key.stop) if key.stop is not None else None
                key = slice(start, stop, key.step)
            elif isinstance(key, (list, np.ndarray)):
                key = list(map(str, key))
            else:
                # Tuples, objects, etc.
                key = str(key)
        # Use pandas to perform indexing
        mapper = pd.Series(np.arange(len(self.mapper.index)), index=self.mapper.values)
        indices = mapper.loc.__getitem__(key)
        if isinstance(indices, pd.Series):
            indices = indices.values
        return indices

    def __getitem__(self, key: tp.Any) -> tp.Any:
        indices = self.get_indices(key)
        is_multiple = isinstance(key, (slice, list, np.ndarray))

        def pd_indexing_func(obj: tp.SeriesFrame) -> tp.MaybeSeriesFrame:
            new_obj = obj.iloc[:, indices]
            if not is_multiple:
                # If we selected only one param, then remove its columns levels to keep it clean
                if self.level_name is not None:
                    if checks.is_frame(new_obj):
                        if isinstance(new_obj.columns, pd.MultiIndex):
                            new_obj.columns = index_fns.drop_levels(new_obj.columns, self.level_name)
            return new_obj

        return self.indexing_func(pd_indexing_func, **self.indexing_kwargs)


def indexing_on_mapper(mapper: tp.Series, ref_obj: tp.SeriesFrame,
                       pd_indexing_func: tp.Callable) -> tp.Optional[tp.Series]:
    """Broadcast `mapper` Series to `ref_obj` and perform pandas indexing using `pd_indexing_func`."""
    checks.assert_instance_of(mapper, pd.Series)
    checks.assert_instance_of(ref_obj, (pd.Series, pd.DataFrame))

    df_range_mapper = reshape_fns.broadcast_to(np.arange(len(mapper.index)), ref_obj)
    loced_range_mapper = pd_indexing_func(df_range_mapper)
    new_mapper = mapper.iloc[loced_range_mapper.values[0]]
    if checks.is_frame(loced_range_mapper):
        return pd.Series(new_mapper.values, index=loced_range_mapper.columns, name=mapper.name)
    elif checks.is_series(loced_range_mapper):
        return pd.Series([new_mapper], index=[loced_range_mapper.name], name=mapper.name)
    return None


def build_param_indexer(param_names: tp.Sequence[str], class_name: str = 'ParamIndexer',
                        module_name: tp.Optional[str] = None) -> tp.Type[IndexingBase]:
    """A factory to create a class with parameter indexing.

    Parameter indexer enables accessing a group of rows and columns by a parameter array (similar to `loc`).
    This way, one can query index/columns by another Series called a parameter mapper, which is just a
    `pd.Series` that maps columns (its index) to params (its values).

    Parameter indexing is important, since querying by column/index labels alone is not always the best option.
    For example, `pandas` doesn't let you query by list at a specific index/column level.

    Args:
        param_names (list of str): Names of the parameters.
        class_name (str): Name of the generated class.
        module_name (str): Name of the module to which the class should be bound.

    Usage:
        ```pycon
        >>> import pandas as pd
        >>> from vectorbt.base.indexing import build_param_indexer, indexing_on_mapper

        >>> MyParamIndexer = build_param_indexer(['my_param'])
        >>> class C(MyParamIndexer):
        ...     def __init__(self, df, param_mapper):
        ...         self.df = df
        ...         self._my_param_mapper = param_mapper
        ...         super().__init__([param_mapper])
        ...
        ...     def indexing_func(self, pd_indexing_func):
        ...         return self.__class__(
        ...             pd_indexing_func(self.df),
        ...             indexing_on_mapper(self._my_param_mapper, self.df, pd_indexing_func)
        ...         )

        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> param_mapper = pd.Series(['First', 'Second'], index=['a', 'b'])
        >>> c = C(df, param_mapper)

        >>> c.my_param_loc['First'].df
        0    1
        1    2
        Name: a, dtype: int64

        >>> c.my_param_loc['Second'].df
        0    3
        1    4
        Name: b, dtype: int64

        >>> c.my_param_loc[['First', 'First', 'Second', 'Second']].df
              a     b
        0  1  1  3  3
        1  2  2  4  4
        ```
    """

    class ParamIndexer(IndexingBase):
        def __init__(self, param_mappers: tp.Sequence[tp.Series],
                     level_names: tp.Optional[tp.LevelSequence] = None, **kwargs) -> None:
            checks.assert_len_equal(param_names, param_mappers)

            for i, param_name in enumerate(param_names):
                level_name = level_names[i] if level_names is not None else None
                _param_loc = ParamLoc(param_mappers[i], self.indexing_func, level_name=level_name, **kwargs)
                setattr(self, f'_{param_name}_loc', _param_loc)

    for i, param_name in enumerate(param_names):
        def param_loc(self, _param_name=param_name) -> ParamLoc:
            return getattr(self, f'_{_param_name}_loc')

        param_loc.__doc__ = f"""Access a group of columns by parameter `{param_name}` using `pd.Series.loc`.
        
        Forwards this operation to each Series/DataFrame and returns a new class instance.
        """

        setattr(ParamIndexer, param_name + '_loc', property(param_loc))

    ParamIndexer.__name__ = class_name
    ParamIndexer.__qualname__ = class_name
    if module_name is not None:
        ParamIndexer.__module__ = module_name

    return ParamIndexer
