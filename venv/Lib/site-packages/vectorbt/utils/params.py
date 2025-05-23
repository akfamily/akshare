# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for working with parameters."""

import itertools
from collections.abc import Callable

from numba.typed import List

from vectorbt import _typing as tp
from vectorbt.utils import checks


def to_typed_list(lst: list) -> List:
    """Cast Python list to typed list.

    Direct construction is flawed in Numba 0.52.0.
    See https://github.com/numba/numba/issues/6651."""
    nb_lst = List()
    for elem in lst:
        nb_lst.append(elem)
    return nb_lst


def flatten_param_tuples(param_tuples: tp.Sequence) -> tp.List[tp.List]:
    """Flattens a nested list of iterables using unzipping."""
    param_list = []
    unzipped_tuples = zip(*param_tuples)
    for i, unzipped in enumerate(unzipped_tuples):
        unzipped = list(unzipped)
        if isinstance(unzipped[0], tuple):
            param_list.extend(flatten_param_tuples(unzipped))
        else:
            param_list.append(unzipped)
    return param_list


def create_param_combs(op_tree: tp.Tuple, depth: int = 0) -> tp.List[tp.List]:
    """Create arbitrary parameter combinations from the operation tree `op_tree`.

    `op_tree` is a tuple with nested instructions to generate parameters.
    The first element of the tuple should be a callable that takes remaining elements as arguments.
    If one of the elements is a tuple itself and its first argument is a callable, it will be
    unfolded in the same way as above.

    Usage:
        ```pycon
        >>> import numpy as np
        >>> from itertools import combinations, product

        >>> create_param_combs((product, (combinations, [0, 1, 2, 3], 2), [4, 5]))
        [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2],
         [1, 1, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3],
         [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5]]
        ```
    """
    checks.assert_instance_of(op_tree, tuple)
    checks.assert_instance_of(op_tree[0], Callable)
    new_op_tree: tp.Tuple = (op_tree[0],)
    for elem in op_tree[1:]:
        if isinstance(elem, tuple) and isinstance(elem[0], Callable):
            new_op_tree += (create_param_combs(elem, depth=depth + 1),)
        else:
            new_op_tree += (elem,)
    out = list(new_op_tree[0](*new_op_tree[1:]))
    if depth == 0:
        # do something
        return flatten_param_tuples(out)
    return out


def broadcast_params(param_list: tp.Sequence[tp.Sequence], to_n: tp.Optional[int] = None) -> tp.List[tp.List]:
    """Broadcast parameters in `param_list`."""
    if to_n is None:
        to_n = max(list(map(len, param_list)))
    new_param_list = []
    for i in range(len(param_list)):
        params = param_list[i]
        if len(params) in [1, to_n]:
            if len(params) < to_n:
                new_param_list.append([p for _ in range(to_n) for p in params])
            else:
                new_param_list.append(list(params))
        else:
            raise ValueError(f"Parameters at index {i} have length {len(params)} that cannot be broadcast to {to_n}")
    return new_param_list


def create_param_product(param_list: tp.Sequence[tp.Sequence]) -> tp.List[tp.List]:
    """Make Cartesian product out of all params in `param_list`."""
    return list(map(list, zip(*list(itertools.product(*param_list)))))
