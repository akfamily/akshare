# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Custom pandas accessors.

Methods can be accessed as follows:

* `BaseSRAccessor` -> `pd.Series.vbt.*`
* `BaseDFAccessor` -> `pd.DataFrame.vbt.*`

For example:

```pycon
>>> import pandas as pd
>>> import vectorbt as vbt

>>> # vectorbt.base.accessors.BaseAccessor.make_symmetric
>>> pd.Series([1, 2, 3]).vbt.make_symmetric()
     0    1    2
0  1.0  2.0  3.0
1  2.0  NaN  NaN
2  3.0  NaN  NaN
```

It contains base methods for working with pandas objects. Most of these methods are adaptations
of combine/reshape/index functions that can work with pandas objects. For example,
`vectorbt.base.reshape_fns.broadcast` can take an arbitrary number of pandas objects, thus
you can find its variations as accessor methods.

```pycon
>>> sr = pd.Series([1])
>>> df = pd.DataFrame([1, 2, 3])

>>> vbt.base.reshape_fns.broadcast_to(sr, df)
   0
0  1
1  1
2  1
>>> sr.vbt.broadcast_to(df)
   0
0  1
1  1
2  1
```

Additionally, `BaseAccessor` implements arithmetic (such as `+`), comparison (such as `>`) and
logical operators (such as `&`) by doing 1) NumPy-like broadcasting and 2) the compuation with NumPy
under the hood, which is mostly much faster than with pandas.

```pycon
>>> df = pd.DataFrame(np.random.uniform(size=(1000, 1000)))

>>> %timeit df * 2  # pandas
296 ms ± 27.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
>>> %timeit df.vbt * 2  # vectorbt
5.48 ms ± 1.12 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

!!! note
    You should ensure that your `*.vbt` operand is on the left if the other operand is an array.

    Accessors do not utilize caching.

    Grouping is only supported by the methods that accept the `group_by` argument."""

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base import combine_fns, index_fns, reshape_fns
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.base.column_grouper import ColumnGrouper
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, get_func_arg_names
from vectorbt.utils.decorators import class_or_instancemethod, attach_binary_magic_methods, attach_unary_magic_methods

BaseAccessorT = tp.TypeVar("BaseAccessorT", bound="BaseAccessor")


@attach_binary_magic_methods(
    lambda self, other, np_func: self.combine(other, allow_multiple=False, combine_func=np_func))
@attach_unary_magic_methods(lambda self, np_func: self.apply(apply_func=np_func))
class BaseAccessor(Wrapping):
    """Accessor on top of Series and DataFrames.

    Accessible through `pd.Series.vbt` and `pd.DataFrame.vbt`, and all child accessors.

    Series is just a DataFrame with one column, hence to avoid defining methods exclusively for 1-dim data,
    we will convert any Series to a DataFrame and perform matrix computation on it. Afterwards,
    by using `BaseAccessor.wrapper`, we will convert the 2-dim output back to a Series.

    `**kwargs` will be passed to `vectorbt.base.array_wrapper.ArrayWrapper`."""

    def __init__(self, obj: tp.SeriesFrame, wrapper: tp.Optional[ArrayWrapper] = None, **kwargs) -> None:
        checks.assert_instance_of(obj, (pd.Series, pd.DataFrame))

        self._obj = obj

        wrapper_arg_names = get_func_arg_names(ArrayWrapper.__init__)
        grouper_arg_names = get_func_arg_names(ColumnGrouper.__init__)
        wrapping_kwargs = dict()
        for k in list(kwargs.keys()):
            if k in wrapper_arg_names or k in grouper_arg_names:
                wrapping_kwargs[k] = kwargs.pop(k)
        if wrapper is None:
            wrapper = ArrayWrapper.from_obj(obj, **wrapping_kwargs)
        else:
            wrapper = wrapper.replace(**wrapping_kwargs)
        Wrapping.__init__(self, wrapper, obj=obj, **kwargs)

    def __call__(self: BaseAccessorT, **kwargs) -> BaseAccessorT:
        """Allows passing arguments to the initializer."""

        return self.replace(**kwargs)

    @property
    def sr_accessor_cls(self) -> tp.Type["BaseSRAccessor"]:
        """Accessor class for `pd.Series`."""
        return BaseSRAccessor

    @property
    def df_accessor_cls(self) -> tp.Type["BaseDFAccessor"]:
        """Accessor class for `pd.DataFrame`."""
        return BaseDFAccessor

    def indexing_func(self: BaseAccessorT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> BaseAccessorT:
        """Perform indexing on `BaseAccessor`."""
        new_wrapper, idx_idxs, _, col_idxs = self.wrapper.indexing_func_meta(pd_indexing_func, **kwargs)
        new_obj = new_wrapper.wrap(self.to_2d_array()[idx_idxs, :][:, col_idxs], group_by=False)
        if checks.is_series(new_obj):
            return self.replace(
                cls_=self.sr_accessor_cls,
                obj=new_obj,
                wrapper=new_wrapper
            )
        return self.replace(
            cls_=self.df_accessor_cls,
            obj=new_obj,
            wrapper=new_wrapper
        )

    @property
    def obj(self):
        """Pandas object."""
        return self._obj

    @class_or_instancemethod
    def is_series(cls_or_self) -> bool:
        raise NotImplementedError

    @class_or_instancemethod
    def is_frame(cls_or_self) -> bool:
        raise NotImplementedError

    # ############# Creation ############# #

    @classmethod
    def empty(cls, shape: tp.Shape, fill_value: tp.Scalar = np.nan, **kwargs) -> tp.SeriesFrame:
        """Generate an empty Series/DataFrame of shape `shape` and fill with `fill_value`."""
        if not isinstance(shape, tuple) or (isinstance(shape, tuple) and len(shape) == 1):
            return pd.Series(np.full(shape, fill_value), **kwargs)
        return pd.DataFrame(np.full(shape, fill_value), **kwargs)

    @classmethod
    def empty_like(cls, other: tp.SeriesFrame, fill_value: tp.Scalar = np.nan, **kwargs) -> tp.SeriesFrame:
        """Generate an empty Series/DataFrame like `other` and fill with `fill_value`."""
        if checks.is_series(other):
            return cls.empty(other.shape, fill_value=fill_value, index=other.index, name=other.name, **kwargs)
        return cls.empty(other.shape, fill_value=fill_value, index=other.index, columns=other.columns, **kwargs)

    # ############# Index and columns ############# #

    def apply_on_index(self, apply_func: tp.Callable, *args, axis: int = 1,
                       inplace: bool = False, **kwargs) -> tp.Optional[tp.SeriesFrame]:
        """Apply function `apply_func` on index of the pandas object.

        Set `axis` to 1 for columns and 0 for index.
        If `inplace` is True, modifies the pandas object. Otherwise, returns a copy."""
        checks.assert_in(axis, (0, 1))

        if axis == 1:
            obj_index = self.wrapper.columns
        else:
            obj_index = self.wrapper.index
        obj_index = apply_func(obj_index, *args, **kwargs)
        if inplace:
            if axis == 1:
                self.obj.columns = obj_index
            else:
                self.obj.index = obj_index
            return None
        else:
            obj = self.obj.copy()
            if axis == 1:
                obj.columns = obj_index
            else:
                obj.index = obj_index
            return obj

    def stack_index(self, index: tp.Index, on_top: bool = True, axis: int = 1,
                    inplace: bool = False, **kwargs) -> tp.Optional[tp.SeriesFrame]:
        """See `vectorbt.base.index_fns.stack_indexes`.

        Set `on_top` to False to stack at bottom.

        See `BaseAccessor.apply_on_index` for other keyword arguments."""

        def apply_func(obj_index: tp.Index) -> tp.Index:
            if on_top:
                return index_fns.stack_indexes([index, obj_index], **kwargs)
            return index_fns.stack_indexes([obj_index, index], **kwargs)

        return self.apply_on_index(apply_func, axis=axis, inplace=inplace)

    def drop_levels(self, levels: tp.MaybeLevelSequence, axis: int = 1,
                    inplace: bool = False, strict: bool = True) -> tp.Optional[tp.SeriesFrame]:
        """See `vectorbt.base.index_fns.drop_levels`.

        See `BaseAccessor.apply_on_index` for other keyword arguments."""

        def apply_func(obj_index: tp.Index) -> tp.Index:
            return index_fns.drop_levels(obj_index, levels, strict=strict)

        return self.apply_on_index(apply_func, axis=axis, inplace=inplace)

    def rename_levels(self, name_dict: tp.Dict[str, tp.Any], axis: int = 1,
                      inplace: bool = False, strict: bool = True) -> tp.Optional[tp.SeriesFrame]:
        """See `vectorbt.base.index_fns.rename_levels`.

        See `BaseAccessor.apply_on_index` for other keyword arguments."""

        def apply_func(obj_index: tp.Index) -> tp.Index:
            return index_fns.rename_levels(obj_index, name_dict, strict=strict)

        return self.apply_on_index(apply_func, axis=axis, inplace=inplace)

    def select_levels(self, level_names: tp.MaybeLevelSequence, axis: int = 1,
                      inplace: bool = False) -> tp.Optional[tp.SeriesFrame]:
        """See `vectorbt.base.index_fns.select_levels`.

        See `BaseAccessor.apply_on_index` for other keyword arguments."""

        def apply_func(obj_index: tp.Index) -> tp.Index:
            return index_fns.select_levels(obj_index, level_names)

        return self.apply_on_index(apply_func, axis=axis, inplace=inplace)

    def drop_redundant_levels(self, axis: int = 1, inplace: bool = False) -> tp.Optional[tp.SeriesFrame]:
        """See `vectorbt.base.index_fns.drop_redundant_levels`.

        See `BaseAccessor.apply_on_index` for other keyword arguments."""

        def apply_func(obj_index: tp.Index) -> tp.Index:
            return index_fns.drop_redundant_levels(obj_index)

        return self.apply_on_index(apply_func, axis=axis, inplace=inplace)

    def drop_duplicate_levels(self, keep: tp.Optional[str] = None, axis: int = 1,
                              inplace: bool = False) -> tp.Optional[tp.SeriesFrame]:
        """See `vectorbt.base.index_fns.drop_duplicate_levels`.

        See `BaseAccessor.apply_on_index` for other keyword arguments."""

        def apply_func(obj_index: tp.Index) -> tp.Index:
            return index_fns.drop_duplicate_levels(obj_index, keep=keep)

        return self.apply_on_index(apply_func, axis=axis, inplace=inplace)

    # ############# Reshaping ############# #

    def to_1d_array(self) -> tp.Array1d:
        """Convert to 1-dim NumPy array

        See `vectorbt.base.reshape_fns.to_1d`."""
        return reshape_fns.to_1d_array(self.obj)

    def to_2d_array(self) -> tp.Array2d:
        """Convert to 2-dim NumPy array.

        See `vectorbt.base.reshape_fns.to_2d`."""
        return reshape_fns.to_2d_array(self.obj)

    def tile(self, n: int, keys: tp.Optional[tp.IndexLike] = None, axis: int = 1,
             wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.base.reshape_fns.tile`.

        Set `axis` to 1 for columns and 0 for index.
        Use `keys` as the outermost level."""
        tiled = reshape_fns.tile(self.obj, n, axis=axis)
        if keys is not None:
            if axis == 1:
                new_columns = index_fns.combine_indexes([keys, self.wrapper.columns])
                return ArrayWrapper.from_obj(tiled).wrap(
                    tiled.values, **merge_dicts(dict(columns=new_columns), wrap_kwargs))
            else:
                new_index = index_fns.combine_indexes([keys, self.wrapper.index])
                return ArrayWrapper.from_obj(tiled).wrap(
                    tiled.values, **merge_dicts(dict(index=new_index), wrap_kwargs))
        return tiled

    def repeat(self, n: int, keys: tp.Optional[tp.IndexLike] = None, axis: int = 1,
               wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """See `vectorbt.base.reshape_fns.repeat`.

        Set `axis` to 1 for columns and 0 for index.
        Use `keys` as the outermost level."""
        repeated = reshape_fns.repeat(self.obj, n, axis=axis)
        if keys is not None:
            if axis == 1:
                new_columns = index_fns.combine_indexes([self.wrapper.columns, keys])
                return ArrayWrapper.from_obj(repeated).wrap(
                    repeated.values, **merge_dicts(dict(columns=new_columns), wrap_kwargs))
            else:
                new_index = index_fns.combine_indexes([self.wrapper.index, keys])
                return ArrayWrapper.from_obj(repeated).wrap(
                    repeated.values, **merge_dicts(dict(index=new_index), wrap_kwargs))
        return repeated

    def align_to(self, other: tp.SeriesFrame, wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Align to `other` on their axes.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> import pandas as pd

            >>> df1 = pd.DataFrame([[1, 2], [3, 4]], index=['x', 'y'], columns=['a', 'b'])
            >>> df1
               a  b
            x  1  2
            y  3  4

            >>> df2 = pd.DataFrame([[5, 6, 7, 8], [9, 10, 11, 12]], index=['x', 'y'],
            ...     columns=pd.MultiIndex.from_arrays([[1, 1, 2, 2], ['a', 'b', 'a', 'b']]))
            >>> df2
                   1       2
               a   b   a   b
            x  5   6   7   8
            y  9  10  11  12

            >>> df1.vbt.align_to(df2)
                  1     2
               a  b  a  b
            x  1  2  1  2
            y  3  4  3  4
            ```
        """
        checks.assert_instance_of(other, (pd.Series, pd.DataFrame))
        obj = reshape_fns.to_2d(self.obj)
        other = reshape_fns.to_2d(other)

        aligned_index = index_fns.align_index_to(obj.index, other.index)
        aligned_columns = index_fns.align_index_to(obj.columns, other.columns)
        obj = obj.iloc[aligned_index, aligned_columns]
        return self.wrapper.wrap(
            obj.values, group_by=False,
            **merge_dicts(dict(index=other.index, columns=other.columns), wrap_kwargs))

    @class_or_instancemethod
    def broadcast(cls_or_self, *others: tp.Union[tp.ArrayLike, "BaseAccessor"], **kwargs) -> reshape_fns.BCRT:
        """See `vectorbt.base.reshape_fns.broadcast`."""
        others = tuple(map(lambda x: x.obj if isinstance(x, BaseAccessor) else x, others))
        if isinstance(cls_or_self, type):
            return reshape_fns.broadcast(*others, **kwargs)
        return reshape_fns.broadcast(cls_or_self.obj, *others, **kwargs)

    def broadcast_to(self, other: tp.Union[tp.ArrayLike, "BaseAccessor"], **kwargs) -> reshape_fns.BCRT:
        """See `vectorbt.base.reshape_fns.broadcast_to`."""
        if isinstance(other, BaseAccessor):
            other = other.obj
        return reshape_fns.broadcast_to(self.obj, other, **kwargs)

    def make_symmetric(self) -> tp.Frame:  # pragma: no cover
        """See `vectorbt.base.reshape_fns.make_symmetric`."""
        return reshape_fns.make_symmetric(self.obj)

    def unstack_to_array(self, **kwargs) -> tp.Array:  # pragma: no cover
        """See `vectorbt.base.reshape_fns.unstack_to_array`."""
        return reshape_fns.unstack_to_array(self.obj, **kwargs)

    def unstack_to_df(self, **kwargs) -> tp.Frame:  # pragma: no cover
        """See `vectorbt.base.reshape_fns.unstack_to_df`."""
        return reshape_fns.unstack_to_df(self.obj, **kwargs)

    def to_dict(self, **kwargs) -> tp.Mapping:
        """See `vectorbt.base.reshape_fns.to_dict`."""
        return reshape_fns.to_dict(self.obj, **kwargs)

    # ############# Combining ############# #

    def apply(self, *args, apply_func: tp.Optional[tp.Callable] = None, keep_pd: bool = False,
              to_2d: bool = False, wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.SeriesFrame:
        """Apply a function `apply_func`.

        Args:
            *args: Variable arguments passed to `apply_func`.
            apply_func (callable): Apply function.

                Can be Numba-compiled.
            keep_pd (bool): Whether to keep inputs as pandas objects, otherwise convert to NumPy arrays.
            to_2d (bool): Whether to reshape inputs to 2-dim arrays, otherwise keep as-is.
            wrap_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper.wrap`.
            **kwargs: Keyword arguments passed to `combine_func`.

        !!! note
            The resulted array must have the same shape as the original array.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> import pandas as pd

            >>> sr = pd.Series([1, 2], index=['x', 'y'])
            >>> sr2.vbt.apply(apply_func=lambda x: x ** 2)
            i2
            x2    1
            y2    4
            z2    9
            Name: a2, dtype: int64
            ```
        """
        checks.assert_not_none(apply_func)
        # Optionally cast to 2d array
        if to_2d:
            obj = reshape_fns.to_2d(self.obj, raw=not keep_pd)
        else:
            if not keep_pd:
                obj = np.asarray(self.obj)
            else:
                obj = self.obj
        result = apply_func(obj, *args, **kwargs)
        return self.wrapper.wrap(result, group_by=False, **merge_dicts({}, wrap_kwargs))

    @class_or_instancemethod
    def concat(cls_or_self, *others: tp.ArrayLike, broadcast_kwargs: tp.KwargsLike = None,
               keys: tp.Optional[tp.IndexLike] = None) -> tp.Frame:
        """Concatenate with `others` along columns.

        Args:
            *others (array_like): List of objects to be concatenated with this array.
            broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            keys (index_like): Outermost column level.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> import pandas as pd

            >>> sr = pd.Series([1, 2], index=['x', 'y'])
            >>> df = pd.DataFrame([[3, 4], [5, 6]], index=['x', 'y'], columns=['a', 'b'])
            >>> sr.vbt.concat(df, keys=['c', 'd'])
                  c     d
               a  b  a  b
            x  1  1  3  4
            y  2  2  5  6
            ```
        """
        others = tuple(map(lambda x: x.obj if isinstance(x, BaseAccessor) else x, others))
        if isinstance(cls_or_self, type):
            objs = others
        else:
            objs = (cls_or_self.obj,) + others
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        broadcasted = reshape_fns.broadcast(*objs, **broadcast_kwargs)
        broadcasted = tuple(map(reshape_fns.to_2d, broadcasted))
        out = pd.concat(broadcasted, axis=1, keys=keys)
        if not isinstance(out.columns, pd.MultiIndex) and np.all(out.columns == 0):
            out.columns = pd.RangeIndex(start=0, stop=len(out.columns), step=1)
        return out

    def apply_and_concat(self, ntimes: int, *args, apply_func: tp.Optional[tp.Callable] = None,
                         keep_pd: bool = False, to_2d: bool = False, numba_loop: bool = False,
                         use_ray: bool = False, keys: tp.Optional[tp.IndexLike] = None,
                         wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.Frame:
        """Apply `apply_func` `ntimes` times and concatenate the results along columns.
        See `vectorbt.base.combine_fns.apply_and_concat_one`.

        Args:
            ntimes (int): Number of times to call `apply_func`.
            *args: Variable arguments passed to `apply_func`.
            apply_func (callable): Apply function.

                Can be Numba-compiled.
            keep_pd (bool): Whether to keep inputs as pandas objects, otherwise convert to NumPy arrays.
            to_2d (bool): Whether to reshape inputs to 2-dim arrays, otherwise keep as-is.
            numba_loop (bool): Whether to loop using Numba.

                Set to True when iterating large number of times over small input,
                but note that Numba doesn't support variable keyword arguments.
            use_ray (bool): Whether to use Ray to execute `combine_func` in parallel.

                Only works with `numba_loop` set to False and `concat` is set to True.
                See `vectorbt.base.combine_fns.ray_apply` for related keyword arguments.
            keys (index_like): Outermost column level.
            wrap_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper.wrap`.
            **kwargs: Keyword arguments passed to `combine_func`.

        !!! note
            The resulted arrays to be concatenated must have the same shape as broadcast input arrays.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> import pandas as pd

            >>> df = pd.DataFrame([[3, 4], [5, 6]], index=['x', 'y'], columns=['a', 'b'])
            >>> df.vbt.apply_and_concat(3, [1, 2, 3],
            ...     apply_func=lambda i, a, b: a * b[i], keys=['c', 'd', 'e'])
                  c       d       e
               a  b   a   b   a   b
            x  3  4   6   8   9  12
            y  5  6  10  12  15  18
            ```

            * Use Ray for small inputs and large processing times:

            ```pycon
            >>> def apply_func(i, a):
            ...     time.sleep(1)
            ...     return a

            >>> sr = pd.Series([1, 2, 3])

            >>> %timeit sr.vbt.apply_and_concat(3, apply_func=apply_func)
            3.01 s ± 2.15 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

            >>> %timeit sr.vbt.apply_and_concat(3, apply_func=apply_func, use_ray=True)
            1.01 s ± 2.31 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
            ```
        """
        checks.assert_not_none(apply_func)
        # Optionally cast to 2d array
        if to_2d:
            obj = reshape_fns.to_2d(self.obj, raw=not keep_pd)
        else:
            if not keep_pd:
                obj = np.asarray(self.obj)
            else:
                obj = self.obj
        if checks.is_numba_func(apply_func) and numba_loop:
            if use_ray:
                raise ValueError("Ray cannot be used within Numba")
            result = combine_fns.apply_and_concat_one_nb(ntimes, apply_func, obj, *args, **kwargs)
        else:
            if use_ray:
                result = combine_fns.apply_and_concat_one_ray(ntimes, apply_func, obj, *args, **kwargs)
            else:
                result = combine_fns.apply_and_concat_one(ntimes, apply_func, obj, *args, **kwargs)
        # Build column hierarchy
        if keys is not None:
            new_columns = index_fns.combine_indexes([keys, self.wrapper.columns])
        else:
            top_columns = pd.Index(np.arange(ntimes), name='apply_idx')
            new_columns = index_fns.combine_indexes([top_columns, self.wrapper.columns])
        return self.wrapper.wrap(result, group_by=False, **merge_dicts(dict(columns=new_columns), wrap_kwargs))

    def combine(self, other: tp.MaybeTupleList[tp.Union[tp.ArrayLike, "BaseAccessor"]], *args,
                allow_multiple: bool = True, combine_func: tp.Optional[tp.Callable] = None,
                keep_pd: bool = False, to_2d: bool = False, concat: bool = False, numba_loop: bool = False,
                use_ray: bool = False, broadcast: bool = True, broadcast_kwargs: tp.KwargsLike = None,
                keys: tp.Optional[tp.IndexLike] = None, wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.SeriesFrame:
        """Combine with `other` using `combine_func`.

        Args:
            other (array_like): Object to combine this array with.
            *args: Variable arguments passed to `combine_func`.
            allow_multiple (bool): Whether a tuple/list will be considered as multiple objects in `other`.
            combine_func (callable): Function to combine two arrays.

                Can be Numba-compiled.
            keep_pd (bool): Whether to keep inputs as pandas objects, otherwise convert to NumPy arrays.
            to_2d (bool): Whether to reshape inputs to 2-dim arrays, otherwise keep as-is.
            concat (bool): Whether to concatenate the results along the column axis.
                Otherwise, pairwise combine into a Series/DataFrame of the same shape.

                If True, see `vectorbt.base.combine_fns.combine_and_concat`.
                If False, see `vectorbt.base.combine_fns.combine_multiple`.
            numba_loop (bool): Whether to loop using Numba.

                Set to True when iterating large number of times over small input,
                but note that Numba doesn't support variable keyword arguments.
            use_ray (bool): Whether to use Ray to execute `combine_func` in parallel.

                Only works with `numba_loop` set to False and `concat` is set to True.
                See `vectorbt.base.combine_fns.ray_apply` for related keyword arguments.
            broadcast (bool): Whether to broadcast all inputs.
            broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            keys (index_like): Outermost column level.
            wrap_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper.wrap`.
            **kwargs: Keyword arguments passed to `combine_func`.

        !!! note
            If `combine_func` is Numba-compiled, will broadcast using `WRITEABLE` and `C_CONTIGUOUS`
            flags, which can lead to an expensive computation overhead if passed objects are large and
            have different shape/memory order. You also must ensure that all objects have the same data type.

            Also remember to bring each in `*args` to a Numba-compatible format.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> import pandas as pd

            >>> sr = pd.Series([1, 2], index=['x', 'y'])
            >>> df = pd.DataFrame([[3, 4], [5, 6]], index=['x', 'y'], columns=['a', 'b'])

            >>> sr.vbt.combine(df, combine_func=lambda x, y: x + y)
               a  b
            x  4  5
            y  7  8

            >>> sr.vbt.combine([df, df*2], combine_func=lambda x, y: x + y)
                a   b
            x  10  13
            y  17  20

            >>> sr.vbt.combine([df, df*2], combine_func=lambda x, y: x + y, concat=True, keys=['c', 'd'])
                  c       d
               a  b   a   b
            x  4  5   7   9
            y  7  8  12  14
            ```

            * Use Ray for small inputs and large processing times:

            ```pycon
            >>> def combine_func(a, b):
            ...     time.sleep(1)
            ...     return a + b

            >>> sr = pd.Series([1, 2, 3])

            >>> %timeit sr.vbt.combine([1, 1, 1], combine_func=combine_func)
            3.01 s ± 2.98 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

            >>> %timeit sr.vbt.combine([1, 1, 1], combine_func=combine_func, concat=True, use_ray=True)
            1.02 s ± 2.32 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
            ```
        """
        if not allow_multiple or not isinstance(other, (tuple, list)):
            others = (other,)
        else:
            others = other
        others = tuple(map(lambda x: x.obj if isinstance(x, BaseAccessor) else x, others))
        checks.assert_not_none(combine_func)
        # Broadcast arguments
        if broadcast:
            if broadcast_kwargs is None:
                broadcast_kwargs = {}
            if checks.is_numba_func(combine_func):
                # Numba requires writeable arrays
                # Plus all of our arrays must be in the same order
                broadcast_kwargs = merge_dicts(dict(require_kwargs=dict(requirements=['W', 'C'])), broadcast_kwargs)
            new_obj, *new_others = reshape_fns.broadcast(self.obj, *others, **broadcast_kwargs)
        else:
            new_obj, new_others = self.obj, others
        if not checks.is_pandas(new_obj):
            new_obj = ArrayWrapper.from_shape(new_obj.shape).wrap(new_obj)
        # Optionally cast to 2d array
        if to_2d:
            inputs = tuple(map(lambda x: reshape_fns.to_2d(x, raw=not keep_pd), (new_obj, *new_others)))
        else:
            if not keep_pd:
                inputs = tuple(map(lambda x: np.asarray(x), (new_obj, *new_others)))
            else:
                inputs = new_obj, *new_others
        if len(inputs) == 2:
            result = combine_func(inputs[0], inputs[1], *args, **kwargs)
            return ArrayWrapper.from_obj(new_obj).wrap(result, **merge_dicts({}, wrap_kwargs))
        if concat:
            # Concat the results horizontally
            if checks.is_numba_func(combine_func) and numba_loop:
                if use_ray:
                    raise ValueError("Ray cannot be used within Numba")
                for i in range(1, len(inputs)):
                    checks.assert_meta_equal(inputs[i - 1], inputs[i])
                result = combine_fns.combine_and_concat_nb(
                    inputs[0], inputs[1:], combine_func, *args, **kwargs)
            else:
                if use_ray:
                    result = combine_fns.combine_and_concat_ray(
                        inputs[0], inputs[1:], combine_func, *args, **kwargs)
                else:
                    result = combine_fns.combine_and_concat(
                        inputs[0], inputs[1:], combine_func, *args, **kwargs)
            columns = ArrayWrapper.from_obj(new_obj).columns
            if keys is not None:
                new_columns = index_fns.combine_indexes([keys, columns])
            else:
                top_columns = pd.Index(np.arange(len(new_others)), name='combine_idx')
                new_columns = index_fns.combine_indexes([top_columns, columns])
            return ArrayWrapper.from_obj(new_obj).wrap(result, **merge_dicts(dict(columns=new_columns), wrap_kwargs))
        else:
            # Combine arguments pairwise into one object
            if use_ray:
                raise ValueError("Ray cannot be used with concat=False")
            if checks.is_numba_func(combine_func) and numba_loop:
                for i in range(1, len(inputs)):
                    checks.assert_dtype_equal(inputs[i - 1], inputs[i])
                result = combine_fns.combine_multiple_nb(inputs, combine_func, *args, **kwargs)
            else:
                result = combine_fns.combine_multiple(inputs, combine_func, *args, **kwargs)
            return ArrayWrapper.from_obj(new_obj).wrap(result, **merge_dicts({}, wrap_kwargs))


class BaseSRAccessor(BaseAccessor):
    """Accessor on top of Series.

    Accessible through `pd.Series.vbt` and all child accessors."""

    def __init__(self, obj: tp.Series, **kwargs) -> None:
        checks.assert_instance_of(obj, pd.Series)

        BaseAccessor.__init__(self, obj, **kwargs)

    @class_or_instancemethod
    def is_series(cls_or_self) -> bool:
        return True

    @class_or_instancemethod
    def is_frame(cls_or_self) -> bool:
        return False


class BaseDFAccessor(BaseAccessor):
    """Accessor on top of DataFrames.

    Accessible through `pd.DataFrame.vbt` and all child accessors."""

    def __init__(self, obj: tp.Frame, **kwargs) -> None:
        checks.assert_instance_of(obj, pd.DataFrame)

        BaseAccessor.__init__(self, obj, **kwargs)

    @class_or_instancemethod
    def is_series(cls_or_self) -> bool:
        return False

    @class_or_instancemethod
    def is_frame(cls_or_self) -> bool:
        return True
