# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Functions for reshaping arrays.

Reshape functions transform a pandas object/NumPy array in some way, such as tiling, broadcasting,
and unstacking."""

import functools
from collections.abc import Sequence

import numpy as np
import pandas as pd
from numba import njit
try:
    from numpy import broadcast_shapes

    broadcast_shape = None
except ImportError:
    from numpy.lib.stride_tricks import _broadcast_shape as broadcast_shape

    broadcast_shapes = None

from vectorbt import _typing as tp
from vectorbt.base import index_fns, array_wrapper
from vectorbt.utils import checks
from vectorbt.utils.config import resolve_dict


def to_any_array(arg: tp.ArrayLike, raw: bool = False) -> tp.AnyArray:
    """Convert any array-like object to an array.

    Pandas objects are kept as-is."""
    if not raw and checks.is_any_array(arg):
        return arg
    return np.asarray(arg)


def to_pd_array(arg: tp.ArrayLike) -> tp.SeriesFrame:
    """Convert any array-like object to a pandas object."""
    if checks.is_pandas(arg):
        return arg
    arg = np.asarray(arg)
    if arg.ndim == 1:
        return pd.Series(arg)
    if arg.ndim == 2:
        return pd.DataFrame(arg)
    raise ValueError("Wrong number of dimensions: cannot convert to Series or DataFrame")


def soft_to_ndim(arg: tp.ArrayLike, ndim: int, raw: bool = False) -> tp.AnyArray:
    """Try to softly bring `arg` to the specified number of dimensions `ndim` (max 2)."""
    arg = to_any_array(arg, raw=raw)
    if ndim == 1:
        if arg.ndim == 2:
            if arg.shape[1] == 1:
                if checks.is_frame(arg):
                    return arg.iloc[:, 0]
                return arg[:, 0]  # downgrade
    if ndim == 2:
        if arg.ndim == 1:
            if checks.is_series(arg):
                return arg.to_frame()
            return arg[:, None]  # upgrade
    return arg  # do nothing


def to_1d(arg: tp.ArrayLike, raw: bool = False) -> tp.AnyArray1d:
    """Reshape argument to one dimension. 

    If `raw` is True, returns NumPy array.
    If 2-dim, will collapse along axis 1 (i.e., DataFrame with one column to Series)."""
    arg = to_any_array(arg, raw=raw)
    if arg.ndim == 2:
        if arg.shape[1] == 1:
            if checks.is_frame(arg):
                return arg.iloc[:, 0]
            return arg[:, 0]
    if arg.ndim == 1:
        return arg
    elif arg.ndim == 0:
        return arg.reshape((1,))
    raise ValueError(f"Cannot reshape a {arg.ndim}-dimensional array to 1 dimension")


to_1d_array = functools.partial(to_1d, raw=True)


def to_2d(arg: tp.ArrayLike, raw: bool = False, expand_axis: int = 1) -> tp.AnyArray2d:
    """Reshape argument to two dimensions. 

    If `raw` is True, returns NumPy array.
    If 1-dim, will expand along axis 1 (i.e., Series to DataFrame with one column)."""
    arg = to_any_array(arg, raw=raw)
    if arg.ndim == 2:
        return arg
    elif arg.ndim == 1:
        if checks.is_series(arg):
            if expand_axis == 0:
                return pd.DataFrame(arg.values[None, :], columns=arg.index)
            elif expand_axis == 1:
                return arg.to_frame()
        return np.expand_dims(arg, expand_axis)
    elif arg.ndim == 0:
        return arg.reshape((1, 1))
    raise ValueError(f"Cannot reshape a {arg.ndim}-dimensional array to 2 dimensions")


to_2d_array = functools.partial(to_2d, raw=True)


def to_dict(arg: tp.ArrayLike, orient: str = 'dict') -> dict:
    """Convert object to dict."""
    arg = to_pd_array(arg)
    if orient == 'index_series':
        return {arg.index[i]: arg.iloc[i] for i in range(len(arg.index))}
    return arg.to_dict(orient)


def repeat(arg: tp.ArrayLike, n: int, axis: int = 1, raw: bool = False) -> tp.AnyArray:
    """Repeat each element in `arg` `n` times along the specified axis."""
    arg = to_any_array(arg, raw=raw)
    if axis == 0:
        if checks.is_pandas(arg):
            return array_wrapper.ArrayWrapper.from_obj(arg).wrap(
                np.repeat(arg.values, n, axis=0), index=index_fns.repeat_index(arg.index, n))
        return np.repeat(arg, n, axis=0)
    elif axis == 1:
        arg = to_2d(arg)
        if checks.is_pandas(arg):
            return array_wrapper.ArrayWrapper.from_obj(arg).wrap(
                np.repeat(arg.values, n, axis=1), columns=index_fns.repeat_index(arg.columns, n))
        return np.repeat(arg, n, axis=1)
    else:
        raise ValueError("Only axis 0 and 1 are supported")


def tile(arg: tp.ArrayLike, n: int, axis: int = 1, raw: bool = False) -> tp.AnyArray:
    """Repeat the whole `arg` `n` times along the specified axis."""
    arg = to_any_array(arg, raw=raw)
    if axis == 0:
        if arg.ndim == 2:
            if checks.is_pandas(arg):
                return array_wrapper.ArrayWrapper.from_obj(arg).wrap(
                    np.tile(arg.values, (n, 1)), index=index_fns.tile_index(arg.index, n))
            return np.tile(arg, (n, 1))
        if checks.is_pandas(arg):
            return array_wrapper.ArrayWrapper.from_obj(arg).wrap(
                np.tile(arg.values, n), index=index_fns.tile_index(arg.index, n))
        return np.tile(arg, n)
    elif axis == 1:
        arg = to_2d(arg)
        if checks.is_pandas(arg):
            return array_wrapper.ArrayWrapper.from_obj(arg).wrap(
                np.tile(arg.values, (1, n)), columns=index_fns.tile_index(arg.columns, n))
        return np.tile(arg, (1, n))
    else:
        raise ValueError("Only axis 0 and 1 are supported")


IndexFromLike = tp.Union[None, str, int, tp.Any]
"""Any object that can be coerced into a `index_from` argument."""


def broadcast_index(args: tp.Sequence[tp.AnyArray],
                    to_shape: tp.Shape,
                    index_from: IndexFromLike = None,
                    axis: int = 0,
                    ignore_sr_names: tp.Optional[bool] = None,
                    **kwargs) -> tp.Optional[tp.Index]:
    """Produce a broadcast index/columns.

    Args:
        args (list of array_like): Array-like objects.
        to_shape (tuple of int): Target shape.
        index_from (any): Broadcasting rule for this index/these columns.

            Accepts the following values:

            * 'keep' or None - keep the original index/columns of the objects in `args`
            * 'stack' - stack different indexes/columns using `vectorbt.base.index_fns.stack_indexes`
            * 'strict' - ensure that all pandas objects have the same index/columns
            * 'reset' - reset any index/columns (they become a simple range)
            * integer - use the index/columns of the i-th object in `args`
            * everything else will be converted to `pd.Index`

        axis (int): Set to 0 for index and 1 for columns.
        ignore_sr_names (bool): Whether to ignore Series names if they are in conflict.

            Conflicting Series names are those that are different but not None.
        **kwargs: Keyword arguments passed to `vectorbt.base.index_fns.stack_indexes`.

    For defaults, see `broadcasting` in `vectorbt._settings.settings`.

    !!! note
        Series names are treated as columns with a single element but without a name.
        If a column level without a name loses its meaning, better to convert Series to DataFrames
        with one column prior to broadcasting. If the name of a Series is not that important,
        better to drop it altogether by setting it to None.
    """
    from vectorbt._settings import settings
    broadcasting_cfg = settings['broadcasting']

    if ignore_sr_names is None:
        ignore_sr_names = broadcasting_cfg['ignore_sr_names']
    index_str = 'columns' if axis == 1 else 'index'
    to_shape_2d = (to_shape[0], 1) if len(to_shape) == 1 else to_shape
    # maxlen stores the length of the longest index
    maxlen = to_shape_2d[1] if axis == 1 else to_shape_2d[0]
    new_index = None

    if index_from is None or (isinstance(index_from, str) and index_from.lower() == 'keep'):
        return None
    if isinstance(index_from, int):
        # Take index/columns of the object indexed by index_from
        if not checks.is_pandas(args[index_from]):
            raise TypeError(f"Argument under index {index_from} must be a pandas object")
        new_index = index_fns.get_index(args[index_from], axis)
    elif isinstance(index_from, str):
        if index_from.lower() == 'reset':
            # Ignore index/columns
            new_index = pd.RangeIndex(start=0, stop=maxlen, step=1)
        elif index_from.lower() in ('stack', 'strict'):
            # Check whether all indexes/columns are equal
            last_index = None  # of type pd.Index
            index_conflict = False
            for arg in args:
                if checks.is_pandas(arg):
                    index = index_fns.get_index(arg, axis)
                    if last_index is not None:
                        if not checks.is_index_equal(index, last_index):
                            index_conflict = True
                    last_index = index
                    continue
            if not index_conflict:
                new_index = last_index
            else:
                # If pandas objects have different index/columns, stack them together
                for arg in args:
                    if checks.is_pandas(arg):
                        index = index_fns.get_index(arg, axis)
                        if axis == 1 and checks.is_series(arg) and ignore_sr_names:
                            # ignore Series name
                            continue
                        if checks.is_default_index(index):
                            # ignore simple ranges without name
                            continue
                        if new_index is None:
                            new_index = index
                        else:
                            if checks.is_index_equal(index, new_index):
                                continue
                            if index_from.lower() == 'strict':
                                # If pandas objects have different index/columns, raise an exception
                                raise ValueError(
                                    f"Broadcasting {index_str} is not allowed when {index_str}_from=strict")
                            # Broadcasting index must follow the rules of a regular broadcasting operation
                            # https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html#general-broadcasting-rules
                            # 1. rule: if indexes are of the same length, they are simply stacked
                            # 2. rule: if index has one element, it gets repeated and then stacked

                            if len(index) != len(new_index):
                                if len(index) > 1 and len(new_index) > 1:
                                    raise ValueError("Indexes could not be broadcast together")
                                if len(index) > len(new_index):
                                    new_index = index_fns.repeat_index(new_index, len(index))
                                elif len(index) < len(new_index):
                                    index = index_fns.repeat_index(index, len(new_index))
                            new_index = index_fns.stack_indexes([new_index, index], **kwargs)
        else:
            raise ValueError(f"Invalid value '{index_from}' for {'columns' if axis == 1 else 'index'}_from")
    else:
        new_index = index_from
    if new_index is not None:
        if maxlen > len(new_index):
            if isinstance(index_from, str) and index_from.lower() == 'strict':
                raise ValueError(f"Broadcasting {index_str} is not allowed when {index_str}_from=strict")
            # This happens only when some numpy object is longer than the new pandas index
            # In this case, new pandas index (one element) should be repeated to match this length.
            if maxlen > 1 and len(new_index) > 1:
                raise ValueError("Indexes could not be broadcast together")
            new_index = index_fns.repeat_index(new_index, maxlen)
    else:
        # new_index=None can mean two things: 1) take original metadata or 2) reset index/columns
        # In case when index_from is not None, we choose 2)
        new_index = pd.RangeIndex(start=0, stop=maxlen, step=1)
    return new_index


def wrap_broadcasted(old_arg: tp.AnyArray,
                     new_arg: tp.Array,
                     is_pd: bool = False,
                     new_index: tp.Optional[tp.Index] = None,
                     new_columns: tp.Optional[tp.Index] = None) -> tp.AnyArray:
    """If the newly brodcasted array was originally a pandas object, make it pandas object again 
    and assign it the newly broadcast index/columns."""
    if is_pd:
        if checks.is_pandas(old_arg):
            if new_index is None:
                # Take index from original pandas object
                old_index = index_fns.get_index(old_arg, 0)
                if old_arg.shape[0] == new_arg.shape[0]:
                    new_index = old_index
                else:
                    new_index = index_fns.repeat_index(old_index, new_arg.shape[0])
            if new_columns is None:
                # Take columns from original pandas object
                old_columns = index_fns.get_index(old_arg, 1)
                new_ncols = new_arg.shape[1] if new_arg.ndim == 2 else 1
                if len(old_columns) == new_ncols:
                    new_columns = old_columns
                else:
                    new_columns = index_fns.repeat_index(old_columns, new_ncols)
        if new_arg.ndim == 2:
            return pd.DataFrame(new_arg, index=new_index, columns=new_columns)
        if new_columns is not None and len(new_columns) == 1:
            name = new_columns[0]
            if name == 0:
                name = None
        else:
            name = None
        return pd.Series(new_arg, index=new_index, name=name)
    return new_arg


BCRT = tp.Union[
    tp.MaybeTuple[tp.AnyArray],
    tp.Tuple[tp.MaybeTuple[tp.AnyArray], tp.Shape, tp.Optional[tp.Index], tp.Optional[tp.Index]]
]


def broadcast(*args: tp.ArrayLike,
              to_shape: tp.Optional[tp.RelaxedShape] = None,
              to_pd: tp.Optional[tp.MaybeSequence[bool]] = None,
              to_frame: tp.Optional[bool] = None,
              align_index: tp.Optional[bool] = None,
              align_columns: tp.Optional[bool] = None,
              index_from: tp.Optional[IndexFromLike] = None,
              columns_from: tp.Optional[IndexFromLike] = None,
              require_kwargs: tp.KwargsLikeSequence = None,
              keep_raw: tp.Optional[tp.MaybeSequence[bool]] = False,
              return_meta: bool = False,
              **kwargs) -> BCRT:
    """Bring any array-like object in `args` to the same shape by using NumPy broadcasting.

    See [Broadcasting](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).

    Can broadcast pandas objects by broadcasting their index/columns with `broadcast_index`.

    Args:
        *args (array_like): Array-like objects.
        to_shape (tuple of int): Target shape. If set, will broadcast every element in `args` to `to_shape`.
        to_pd (bool or list of bool): Whether to convert all output arrays to pandas, otherwise returns
            raw NumPy arrays. If None, converts only if there is at least one pandas object among them.

            If sequence, applies to each argument.
        to_frame (bool): Whether to convert all Series to DataFrames.
        align_index (bool): Whether to align index of pandas objects using multi-index.

            Pass None to use the default.
        align_columns (bool): Whether to align columns of pandas objects using multi-index.

            Pass None to use the default.
        index_from (any): Broadcasting rule for index.

            Pass None to use the default.
        columns_from (any): Broadcasting rule for columns.

            Pass None to use the default.
        require_kwargs (dict or list of dict): Keyword arguments passed to `np.require`.

            If sequence, applies to each argument.
        keep_raw (bool or list of bool): Whether to keep the unbroadcasted version of the array.

            Only makes sure that the array can be broadcast to the target shape.

            If sequence, applies to each argument.
        return_meta (bool): Whether to also return new shape, index and columns.
        **kwargs: Keyword arguments passed to `broadcast_index`.

    For defaults, see `broadcasting` in `vectorbt._settings.settings`.

    Usage:
        * Without broadcasting index and columns:

        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from vectorbt.base.reshape_fns import broadcast

        >>> v = 0
        >>> a = np.array([1, 2, 3])
        >>> sr = pd.Series([1, 2, 3], index=pd.Index(['x', 'y', 'z']), name='a')
        >>> df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        ...     index=pd.Index(['x2', 'y2', 'z2']),
        ...     columns=pd.Index(['a2', 'b2', 'c2']))

        >>> for i in broadcast(
        ...     v, a, sr, df,
        ...     index_from='keep',
        ...     columns_from='keep',
        ... ): print(i)
           0  1  2
        0  0  0  0
        1  0  0  0
        2  0  0  0
           0  1  2
        0  1  2  3
        1  1  2  3
        2  1  2  3
           a  a  a
        x  1  1  1
        y  2  2  2
        z  3  3  3
            a2  b2  c2
        x2   1   2   3
        y2   4   5   6
        z2   7   8   9
        ```

        * Taking new index and columns from position:

        ```pycon
        >>> for i in broadcast(
        ...     v, a, sr, df,
        ...     index_from=2,
        ...     columns_from=3
        ... ): print(i)
           a2  b2  c2
        x   0   0   0
        y   0   0   0
        z   0   0   0
           a2  b2  c2
        x   1   2   3
        y   1   2   3
        z   1   2   3
           a2  b2  c2
        x   1   1   1
        y   2   2   2
        z   3   3   3
           a2  b2  c2
        x   1   2   3
        y   4   5   6
        z   7   8   9
        ```

        * Broadcasting index and columns through stacking:

        ```pycon
        >>> for i in broadcast(
        ...     v, a, sr, df,
        ...     index_from='stack',
        ...     columns_from='stack'
        ... ): print(i)
              a2  b2  c2
        x x2   0   0   0
        y y2   0   0   0
        z z2   0   0   0
              a2  b2  c2
        x x2   1   2   3
        y y2   1   2   3
        z z2   1   2   3
              a2  b2  c2
        x x2   1   1   1
        y y2   2   2   2
        z z2   3   3   3
              a2  b2  c2
        x x2   1   2   3
        y y2   4   5   6
        z z2   7   8   9
        ```

        * Setting index and columns manually:

        ```pycon
        >>> for i in broadcast(
        ...     v, a, sr, df,
        ...     index_from=['a', 'b', 'c'],
        ...     columns_from=['d', 'e', 'f']
        ... ): print(i)
           d  e  f
        a  0  0  0
        b  0  0  0
        c  0  0  0
           d  e  f
        a  1  2  3
        b  1  2  3
        c  1  2  3
           d  e  f
        a  1  1  1
        b  2  2  2
        c  3  3  3
           d  e  f
        a  1  2  3
        b  4  5  6
        c  7  8  9
        ```
    """
    from vectorbt._settings import settings
    broadcasting_cfg = settings['broadcasting']

    is_pd = False
    is_2d = False
    if require_kwargs is None:
        require_kwargs = {}
    if align_index is None:
        align_index = broadcasting_cfg['align_index']
    if align_columns is None:
        align_columns = broadcasting_cfg['align_columns']
    if index_from is None:
        index_from = broadcasting_cfg['index_from']
    if columns_from is None:
        columns_from = broadcasting_cfg['columns_from']

    # Convert to np.ndarray object if not numpy or pandas
    # Also check whether we broadcast to pandas and whether work on 2-dim data
    arr_args = []
    for i in range(len(args)):
        arg = to_any_array(args[i])
        if arg.ndim > 1:
            is_2d = True
        if checks.is_pandas(arg):
            is_pd = True
        arr_args.append(arg)

    # If target shape specified, check again if we work on 2-dim data
    if to_shape is not None:
        if isinstance(to_shape, int):
            to_shape = (to_shape,)
        checks.assert_instance_of(to_shape, tuple)
        if len(to_shape) > 1:
            is_2d = True

    if to_frame is not None:
        # force either keeping Series or converting them to DataFrames
        is_2d = to_frame

    if to_pd is not None:
        # force either raw or pandas
        if isinstance(to_pd, Sequence):
            is_pd = any(to_pd)
        else:
            is_pd = to_pd

    # Align pandas objects
    if align_index:
        index_to_align = []
        for i in range(len(arr_args)):
            if checks.is_pandas(arr_args[i]) and len(arr_args[i].index) > 1:
                index_to_align.append(i)
        if len(index_to_align) > 1:
            indexes = [arr_args[i].index for i in index_to_align]
            if len(set(map(len, indexes))) > 1:
                index_indices = index_fns.align_indexes(indexes)
                for i in index_to_align:
                    arr_args[i] = arr_args[i].iloc[index_indices[index_to_align.index(i)]]
    if align_columns:
        cols_to_align = []
        for i in range(len(arr_args)):
            if checks.is_frame(arr_args[i]) and len(arr_args[i].columns) > 1:
                cols_to_align.append(i)
        if len(cols_to_align) > 1:
            indexes = [arr_args[i].columns for i in cols_to_align]
            if len(set(map(len, indexes))) > 1:
                col_indices = index_fns.align_indexes(indexes)
                for i in cols_to_align:
                    arr_args[i] = arr_args[i].iloc[:, col_indices[cols_to_align.index(i)]]

    # Convert all pd.Series objects to pd.DataFrame if we work on 2-dim data
    arr_args_2d = [arg.to_frame() if is_2d and checks.is_series(arg) else arg for arg in arr_args]

    # Get final shape
    if to_shape is None:
        if broadcast_shapes is not None:
            to_shape = broadcast_shapes(*map(lambda x: np.asarray(x).shape, arr_args_2d))
        else:
            to_shape = broadcast_shape(*map(np.asarray, arr_args_2d))

    # Perform broadcasting
    new_args = []
    for i, arg in enumerate(arr_args_2d):
        if isinstance(keep_raw, Sequence):
            _keep_raw = keep_raw[i]
        else:
            _keep_raw = keep_raw
        bc_arg = np.broadcast_to(arg, to_shape)
        if _keep_raw:
            new_args.append(arg)
            continue
        new_args.append(bc_arg)

    # Force to match requirements
    for i in range(len(new_args)):
        _require_kwargs = resolve_dict(require_kwargs, i=i)
        new_args[i] = np.require(new_args[i], **_require_kwargs)

    if is_pd:
        # Decide on index and columns
        # NOTE: Important to pass arr_args, not arr_args_2d, to preserve original shape info
        new_index = broadcast_index(arr_args, to_shape, index_from=index_from, axis=0, **kwargs)
        new_columns = broadcast_index(arr_args, to_shape, index_from=columns_from, axis=1, **kwargs)
    else:
        new_index, new_columns = None, None

    # Bring arrays to their old types (e.g. array -> pandas)
    for i in range(len(new_args)):
        if isinstance(keep_raw, Sequence):
            _keep_raw = keep_raw[i]
        else:
            _keep_raw = keep_raw
        if _keep_raw:
            continue
        if isinstance(to_pd, Sequence):
            _is_pd = to_pd[i]
        else:
            _is_pd = is_pd
        new_args[i] = wrap_broadcasted(
            arr_args[i],
            new_args[i],
            is_pd=_is_pd,
            new_index=new_index,
            new_columns=new_columns
        )

    if len(new_args) > 1:
        if return_meta:
            return tuple(new_args), to_shape, new_index, new_columns
        return tuple(new_args)
    if return_meta:
        return new_args[0], to_shape, new_index, new_columns
    return new_args[0]


def broadcast_to(arg1: tp.ArrayLike,
                 arg2: tp.ArrayLike,
                 to_pd: tp.Optional[bool] = None,
                 index_from: tp.Optional[IndexFromLike] = None,
                 columns_from: tp.Optional[IndexFromLike] = None,
                 **kwargs) -> BCRT:
    """Broadcast `arg1` to `arg2`.

    Pass None to `index_from`/`columns_from` to use index/columns of the second argument.

    Keyword arguments `**kwargs` are passed to `broadcast`.

    Usage:
        ```pycon
        >>> import numpy as np
        >>> import pandas as pd
        >>> from vectorbt.base.reshape_fns import broadcast_to

        >>> a = np.array([1, 2, 3])
        >>> sr = pd.Series([4, 5, 6], index=pd.Index(['x', 'y', 'z']), name='a')

        >>> broadcast_to(a, sr)
        x    1
        y    2
        z    3
        Name: a, dtype: int64

        >>> broadcast_to(sr, a)
        array([4, 5, 6])
        ```
    """
    arg1 = to_any_array(arg1)
    arg2 = to_any_array(arg2)
    if to_pd is None:
        to_pd = checks.is_pandas(arg2)
    if to_pd:
        # Take index and columns from arg2
        if index_from is None:
            index_from = index_fns.get_index(arg2, 0)
        if columns_from is None:
            columns_from = index_fns.get_index(arg2, 1)
    return broadcast(arg1, to_shape=arg2.shape, to_pd=to_pd, index_from=index_from, columns_from=columns_from, **kwargs)


def broadcast_to_array_of(arg1: tp.ArrayLike, arg2: tp.ArrayLike) -> tp.Array:
    """Broadcast `arg1` to the shape `(1, *arg2.shape)`.

    `arg1` must be either a scalar, a 1-dim array, or have 1 dimension more than `arg2`.

    Usage:
        ```pycon
        >>> import numpy as np
        >>> from vectorbt.base.reshape_fns import broadcast_to_array_of

        >>> broadcast_to_array_of([0.1, 0.2], np.empty((2, 2)))
        [[[0.1 0.1]
          [0.1 0.1]]

         [[0.2 0.2]
          [0.2 0.2]]]
        ```
    """
    arg1 = np.asarray(arg1)
    arg2 = np.asarray(arg2)
    if arg1.ndim == arg2.ndim + 1:
        if arg1.shape[1:] == arg2.shape:
            return arg1
    # From here on arg1 can be only a 1-dim array
    if arg1.ndim == 0:
        arg1 = to_1d(arg1)
    checks.assert_ndim(arg1, 1)

    if arg2.ndim == 0:
        return arg1
    for i in range(arg2.ndim):
        arg1 = np.expand_dims(arg1, axis=-1)
    return np.tile(arg1, (1, *arg2.shape))


def broadcast_to_axis_of(arg1: tp.ArrayLike, arg2: tp.ArrayLike, axis: int,
                         require_kwargs: tp.KwargsLike = None) -> tp.Array:
    """Broadcast `arg1` to an axis of `arg2`.

    If `arg2` has less dimensions than requested, will broadcast `arg1` to a single number.

    For other keyword arguments, see `broadcast`."""
    if require_kwargs is None:
        require_kwargs = {}
    arg2 = to_any_array(arg2)
    if arg2.ndim < axis + 1:
        return np.broadcast_to(arg1, (1,))[0]  # to a single number
    arg1 = np.broadcast_to(arg1, (arg2.shape[axis],))
    arg1 = np.require(arg1, **require_kwargs)
    return arg1


def get_multiindex_series(arg: tp.SeriesFrame) -> tp.Series:
    """Get Series with a multi-index.

    If DataFrame has been passed, should at maximum have one row or column."""
    checks.assert_instance_of(arg, (pd.Series, pd.DataFrame))
    if checks.is_frame(arg):
        if arg.shape[0] == 1:
            arg = arg.iloc[0, :]
        elif arg.shape[1] == 1:
            arg = arg.iloc[:, 0]
        else:
            raise ValueError("Supported are either Series or DataFrame with one column/row")
    checks.assert_instance_of(arg.index, pd.MultiIndex)
    return arg


def unstack_to_array(arg: tp.SeriesFrame, levels: tp.Optional[tp.MaybeLevelSequence] = None) -> tp.Array:
    """Reshape `arg` based on its multi-index into a multi-dimensional array.

    Use `levels` to specify what index levels to unstack and in which order.

    Usage:
        ```pycon
        >>> import pandas as pd
        >>> from vectorbt.base.reshape_fns import unstack_to_array

        >>> index = pd.MultiIndex.from_arrays(
        ...     [[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']])
        >>> sr = pd.Series([1, 2, 3, 4], index=index)

        >>> unstack_to_array(sr).shape
        (2, 2, 4)

        >>> unstack_to_array(sr)
        [[[ 1. nan nan nan]
         [nan  2. nan nan]]

         [[nan nan  3. nan]
        [nan nan nan  4.]]]

        >>> unstack_to_array(sr, levels=(2, 0))
        [[ 1. nan]
         [ 2. nan]
         [nan  3.]
         [nan  4.]]
        ```
    """
    # Extract series
    sr: tp.Series = to_1d(get_multiindex_series(arg))
    if sr.index.duplicated().any():
        raise ValueError("Index contains duplicate entries, cannot reshape")

    unique_idx_list = []
    vals_idx_list = []
    if levels is None:
        levels = range(sr.index.nlevels)
    if isinstance(levels, (int, str)):
        levels = (levels,)
    for level in levels:
        vals = index_fns.select_levels(sr.index, level).to_numpy()
        unique_vals = np.unique(vals)
        unique_idx_list.append(unique_vals)
        idx_map = dict(zip(unique_vals, range(len(unique_vals))))
        vals_idx = list(map(lambda x: idx_map[x], vals))
        vals_idx_list.append(vals_idx)

    a = np.full(list(map(len, unique_idx_list)), np.nan)
    a[tuple(zip(vals_idx_list))] = sr.values
    return a


def make_symmetric(arg: tp.SeriesFrame, sort: bool = True) -> tp.Frame:
    """Make `arg` symmetric.

    The index and columns of the resulting DataFrame will be identical.

    Requires the index and columns to have the same number of levels.

    Pass `sort=False` if index and columns should not be sorted, but concatenated
    and get duplicates removed.

    Usage:
        ```pycon
        >>> import pandas as pd
        >>> from vectorbt.base.reshape_fns import make_symmetric

        >>> df = pd.DataFrame([[1, 2], [3, 4]], index=['a', 'b'], columns=['c', 'd'])

        >>> make_symmetric(df)
             a    b    c    d
        a  NaN  NaN  1.0  2.0
        b  NaN  NaN  3.0  4.0
        c  1.0  3.0  NaN  NaN
        d  2.0  4.0  NaN  NaN
        ```
    """
    checks.assert_instance_of(arg, (pd.Series, pd.DataFrame))
    df: tp.Frame = to_2d(arg)
    if isinstance(df.index, pd.MultiIndex) or isinstance(df.columns, pd.MultiIndex):
        checks.assert_instance_of(df.index, pd.MultiIndex)
        checks.assert_instance_of(df.columns, pd.MultiIndex)
        checks.assert_array_equal(df.index.nlevels, df.columns.nlevels)
        names1, names2 = tuple(df.index.names), tuple(df.columns.names)
    else:
        names1, names2 = df.index.name, df.columns.name

    if names1 == names2:
        new_name = names1
    else:
        if isinstance(df.index, pd.MultiIndex):
            new_name = tuple(zip(*[names1, names2]))
        else:
            new_name = (names1, names2)
    if sort:
        idx_vals = np.unique(np.concatenate((df.index, df.columns))).tolist()
    else:
        idx_vals = list(dict.fromkeys(np.concatenate((df.index, df.columns))))
    df_index = df.index.copy()
    df_columns = df.columns.copy()
    if isinstance(df.index, pd.MultiIndex):
        unique_index = pd.MultiIndex.from_tuples(idx_vals, names=new_name)
        df_index.names = new_name
        df_columns.names = new_name
    else:
        unique_index = pd.Index(idx_vals, name=new_name)
        df_index.name = new_name
        df_columns.name = new_name
    df = df.copy(deep=False)
    df.index = df_index
    df.columns = df_columns
    df_out_dtype = np.promote_types(df.values.dtype, np.min_scalar_type(np.nan))
    df_out = pd.DataFrame(index=unique_index, columns=unique_index, dtype=df_out_dtype)
    df_out.loc[:, :] = df
    df_out[df_out.isnull()] = df.transpose()
    return df_out


def unstack_to_df(arg: tp.SeriesFrame,
                  index_levels: tp.Optional[tp.MaybeLevelSequence] = None,
                  column_levels: tp.Optional[tp.MaybeLevelSequence] = None,
                  symmetric: bool = False,
                  sort: bool = True) -> tp.Frame:
    """Reshape `arg` based on its multi-index into a DataFrame.

    Use `index_levels` to specify what index levels will form new index, and `column_levels` 
    for new columns. Set `symmetric` to True to make DataFrame symmetric.

    Usage:
        ```pycon
        >>> import pandas as pd
        >>> from vectorbt.base.reshape_fns import unstack_to_df

        >>> index = pd.MultiIndex.from_arrays(
        ...     [[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']],
        ...     names=['x', 'y', 'z'])
        >>> sr = pd.Series([1, 2, 3, 4], index=index)

        >>> unstack_to_df(sr, index_levels=(0, 1), column_levels=2)
        z      a    b    c    d
        x y
        1 3  1.0  NaN  NaN  NaN
        1 4  NaN  2.0  NaN  NaN
        2 3  NaN  NaN  3.0  NaN
        2 4  NaN  NaN  NaN  4.0
        ```
    """
    # Extract series
    sr: tp.Series = to_1d(get_multiindex_series(arg))

    if len(sr.index.levels) > 2:
        if index_levels is None:
            raise ValueError("index_levels must be specified")
        if column_levels is None:
            raise ValueError("column_levels must be specified")
    else:
        if index_levels is None:
            index_levels = 0
        if column_levels is None:
            column_levels = 1

    # Build new index and column hierarchies
    new_index = index_fns.select_levels(arg.index, index_levels).unique()
    new_columns = index_fns.select_levels(arg.index, column_levels).unique()

    # Unstack and post-process
    unstacked = unstack_to_array(sr, levels=(index_levels, column_levels))
    df = pd.DataFrame(unstacked, index=new_index, columns=new_columns)
    if symmetric:
        return make_symmetric(df, sort=sort)
    return df


@njit(cache=True)
def flex_choose_i_and_col_nb(a: tp.Array, flex_2d: bool = True) -> tp.Tuple[int, int]:
    """Choose selection index and column based on the array's shape.

    Instead of expensive broadcasting, keep the original shape and do indexing in a smart way.
    A nice feature of this is that it has almost no memory footprint and can broadcast in
    any direction infinitely.

    Call it once before using `flex_select_nb`.

    if `flex_2d` is True, 1-dim array will correspond to columns, otherwise to rows."""
    i = -1
    col = -1
    if a.ndim == 0:
        i = 0
        col = 0
    elif a.ndim == 1:
        if flex_2d:
            i = 0
            if a.shape[0] == 1:
                col = 0
        else:
            col = 0
            if a.shape[0] == 1:
                i = 0
    else:
        if a.shape[0] == 1:
            i = 0
        if a.shape[1] == 1:
            col = 0
    return i, col


@njit(cache=True)
def flex_select_nb(a: tp.Array, i: int, col: int, flex_i: int, flex_col: int, flex_2d: bool = True) -> tp.Any:
    """Select element of `a` as if it has been broadcast."""
    if flex_i == -1:
        flex_i = i
    if flex_col == -1:
        flex_col = col
    if a.ndim == 0:
        return a.item()
    if a.ndim == 1:
        if flex_2d:
            return a[flex_col]
        return a[flex_i]
    return a[flex_i, flex_col]


@njit(cache=True)
def flex_select_auto_nb(a: tp.Array, i: int, col: int, flex_2d: bool = True) -> tp.Any:
    """Combines `flex_choose_i_and_col_nb` and `flex_select_nb`."""
    flex_i, flex_col = flex_choose_i_and_col_nb(a, flex_2d)
    return flex_select_nb(a, i, col, flex_i, flex_col, flex_2d)
