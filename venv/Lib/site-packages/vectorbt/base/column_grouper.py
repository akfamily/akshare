# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Class that exposes methods to group columns.

Class `ColumnGrouper` stores metadata related to grouping columns. It can return, for example,
the number of groups, the start indices of groups, and other information useful for reducing
operations that utilize grouping. It also allows to dynamically enable/disable/modify groups
and checks whether a certain operation is permitted."""

import numpy as np
import pandas as pd
from numba import njit

from vectorbt import _typing as tp
from vectorbt.base import index_fns
from vectorbt.utils import checks
from vectorbt.utils.array_ import is_sorted
from vectorbt.utils.config import Configured
from vectorbt.utils.decorators import cached_method

GroupByT = tp.Union[None, bool, tp.Index]


def group_by_to_index(index: tp.Index, group_by: tp.GroupByLike) -> GroupByT:
    """Convert mapper `group_by` to `pd.Index`.

    !!! note
        Index and mapper must have the same length."""
    if group_by is None or group_by is False:
        return group_by
    if group_by is True:
        group_by = pd.Index(['group'] * len(index))  # one group
    elif isinstance(group_by, (int, str)):
        group_by = index_fns.select_levels(index, group_by)
    elif checks.is_sequence(group_by):
        if len(group_by) != len(index) \
                and isinstance(group_by[0], (int, str)) \
                and isinstance(index, pd.MultiIndex) \
                and len(group_by) <= len(index.names):
            try:
                group_by = index_fns.select_levels(index, group_by)
            except (IndexError, KeyError):
                pass
    if not isinstance(group_by, pd.Index):
        group_by = pd.Index(group_by)
    if len(group_by) != len(index):
        raise ValueError("group_by and index must have the same length")
    return group_by


def get_groups_and_index(index: tp.Index, group_by: tp.GroupByLike) -> tp.Tuple[tp.Array1d, tp.Index]:
    """Return array of group indices pointing to the original index, and grouped index.
    """
    if group_by is None or group_by is False:
        return np.arange(len(index)), index

    group_by = group_by_to_index(index, group_by)
    codes, uniques = pd.factorize(group_by)
    if not isinstance(uniques, pd.Index):
        new_index = pd.Index(uniques)
    else:
        new_index = uniques
    if isinstance(group_by, pd.MultiIndex):
        new_index.names = group_by.names
    elif isinstance(group_by, (pd.Index, pd.Series)):
        new_index.name = group_by.name
    return codes, new_index


@njit(cache=True)
def get_group_lens_nb(groups: tp.Array1d) -> tp.Array1d:
    """Return count per group."""
    result = np.empty(groups.shape[0], dtype=np.int64)
    j = 0
    last_group = -1
    group_len = 0
    for i in range(groups.shape[0]):
        cur_group = groups[i]
        if cur_group < last_group:
            raise ValueError("Groups must be coherent and sorted (such as [0, 0, 1, 2, 2, ...])")
        if cur_group != last_group:
            if last_group != -1:
                # Process previous group
                result[j] = group_len
                j += 1
                group_len = 0
            last_group = cur_group
        group_len += 1
        if i == groups.shape[0] - 1:
            # Process last group
            result[j] = group_len
            j += 1
            group_len = 0
    return result[:j]


class ColumnGrouper(Configured):
    """Class that exposes methods to group columns.

    `group_by` can be:

    * boolean (False for no grouping, True for one group),
    * integer (level by position),
    * string (level by name),
    * sequence of integers or strings that is shorter than `columns` (multiple levels),
    * any other sequence that has the same length as `columns` (group per column).

    Set `allow_enable` to False to prohibit grouping if `ColumnGrouper.group_by` is None.
    Set `allow_disable` to False to prohibit disabling of grouping if `ColumnGrouper.group_by` is not None.
    Set `allow_modify` to False to prohibit modifying groups (you can still change their labels).

    All properties are read-only to enable caching.

    !!! note
        Columns should build groups that are coherent and sorted for using `get_group_lens_nb`.

    !!! note
        This class is meant to be immutable. To change any attribute, use `ColumnGrouper.replace`."""

    def __init__(self, columns: tp.Index, group_by: tp.GroupByLike = None, allow_enable: bool = True,
                 allow_disable: bool = True, allow_modify: bool = True) -> None:
        Configured.__init__(
            self,
            columns=columns,
            group_by=group_by,
            allow_enable=allow_enable,
            allow_disable=allow_disable,
            allow_modify=allow_modify
        )

        checks.assert_instance_of(columns, pd.Index)
        self._columns = columns
        if group_by is None or group_by is False:
            self._group_by = None
        else:
            self._group_by = group_by_to_index(columns, group_by)

        # Everything is allowed by default
        self._allow_enable = allow_enable
        self._allow_disable = allow_disable
        self._allow_modify = allow_modify

    @property
    def columns(self) -> tp.Index:
        """Original columns."""
        return self._columns

    @property
    def group_by(self) -> GroupByT:
        """Mapper for grouping."""
        return self._group_by

    @property
    def allow_enable(self) -> bool:
        """Whether to allow enabling grouping."""
        return self._allow_enable

    @property
    def allow_disable(self) -> bool:
        """Whether to allow disabling grouping."""
        return self._allow_disable

    @property
    def allow_modify(self) -> bool:
        """Whether to allow changing groups."""
        return self._allow_modify

    def is_grouped(self, group_by: tp.GroupByLike = None) -> bool:
        """Check whether columns are grouped."""
        if group_by is False:
            return False
        if group_by is None:
            group_by = self.group_by
        return group_by is not None

    def is_grouping_enabled(self, group_by: tp.GroupByLike = None) -> bool:
        """Check whether column grouping has been enabled."""
        return self.group_by is None and self.is_grouped(group_by=group_by)

    def is_grouping_disabled(self, group_by: tp.GroupByLike = None) -> bool:
        """Check whether column grouping has been disabled."""
        return self.group_by is not None and not self.is_grouped(group_by=group_by)

    @cached_method
    def is_grouping_modified(self, group_by: tp.GroupByLike = None) -> bool:
        """Check whether column grouping has been modified.

        Doesn't care if grouping labels have been changed."""
        if group_by is None or (group_by is False and self.group_by is None):
            return False
        group_by = group_by_to_index(self.columns, group_by)
        if isinstance(group_by, pd.Index) and isinstance(self.group_by, pd.Index):
            if not pd.Index.equals(group_by, self.group_by):
                groups1 = get_groups_and_index(self.columns, group_by)[0]
                groups2 = get_groups_and_index(self.columns, self.group_by)[0]
                if not np.array_equal(groups1, groups2):
                    return True
            return False
        return True

    @cached_method
    def is_grouping_changed(self, group_by: tp.GroupByLike = None) -> bool:
        """Check whether column grouping has changed in any way."""
        if group_by is None or (group_by is False and self.group_by is None):
            return False
        if isinstance(group_by, pd.Index) and isinstance(self.group_by, pd.Index):
            if pd.Index.equals(group_by, self.group_by):
                return False
        return True

    def is_group_count_changed(self, group_by: tp.GroupByLike = None) -> bool:
        """Check whether the number of groups has changed."""
        if group_by is None or (group_by is False and self.group_by is None):
            return False
        if isinstance(group_by, pd.Index) and isinstance(self.group_by, pd.Index):
            return len(group_by) != len(self.group_by)
        return True

    def check_group_by(self, group_by: tp.GroupByLike = None, allow_enable: tp.Optional[bool] = None,
                       allow_disable: tp.Optional[bool] = None, allow_modify: tp.Optional[bool] = None) -> None:
        """Check passed `group_by` object against restrictions."""
        if allow_enable is None:
            allow_enable = self.allow_enable
        if allow_disable is None:
            allow_disable = self.allow_disable
        if allow_modify is None:
            allow_modify = self.allow_modify

        if self.is_grouping_enabled(group_by=group_by):
            if not allow_enable:
                raise ValueError("Enabling grouping is not allowed")
        elif self.is_grouping_disabled(group_by=group_by):
            if not allow_disable:
                raise ValueError("Disabling grouping is not allowed")
        elif self.is_grouping_modified(group_by=group_by):
            if not allow_modify:
                raise ValueError("Modifying groups is not allowed")

    def resolve_group_by(self, group_by: tp.GroupByLike = None, **kwargs) -> GroupByT:
        """Resolve `group_by` from either object variable or keyword argument."""
        if group_by is None:
            group_by = self.group_by
        if group_by is False and self.group_by is None:
            group_by = None
        self.check_group_by(group_by=group_by, **kwargs)
        return group_by_to_index(self.columns, group_by)

    @cached_method
    def get_groups_and_columns(self, group_by: tp.GroupByLike = None, **kwargs) -> tp.Tuple[tp.Array1d, tp.Index]:
        """See `get_groups_and_index`."""
        group_by = self.resolve_group_by(group_by=group_by, **kwargs)
        return get_groups_and_index(self.columns, group_by)

    def get_groups(self, **kwargs) -> tp.Array1d:
        """Return groups array."""
        return self.get_groups_and_columns(**kwargs)[0]

    def get_columns(self, **kwargs) -> tp.Index:
        """Return grouped columns."""
        return self.get_groups_and_columns(**kwargs)[1]

    @cached_method
    def is_sorted(self, group_by: tp.GroupByLike = None, **kwargs) -> bool:
        """Return whether groups are coherent and sorted."""
        group_by = self.resolve_group_by(group_by=group_by, **kwargs)
        groups = self.get_groups(group_by=group_by)
        return is_sorted(groups)

    @cached_method
    def get_group_lens(self, group_by: tp.GroupByLike = None, **kwargs) -> tp.Array1d:
        """See get_group_lens_nb."""
        if not self.is_sorted(group_by=group_by):
            raise ValueError("group_by must lead to groups that are coherent and sorted "
                             "(such as [0, 0, 1, 2, 2, ...])")
        group_by = self.resolve_group_by(group_by=group_by, **kwargs)
        if group_by is None or group_by is False:  # no grouping
            return np.full(len(self.columns), 1)
        groups = self.get_groups(group_by=group_by)
        return get_group_lens_nb(groups)

    @cached_method
    def get_group_count(self, **kwargs) -> int:
        """Get number of groups."""
        return len(self.get_group_lens(**kwargs))

    @cached_method
    def get_group_start_idxs(self, **kwargs) -> tp.Array1d:
        """Get first index of each group as an array."""
        group_lens = self.get_group_lens(**kwargs)
        return np.cumsum(group_lens) - group_lens

    @cached_method
    def get_group_end_idxs(self, **kwargs) -> tp.Array1d:
        """Get end index of each group as an array."""
        group_lens = self.get_group_lens(**kwargs)
        return np.cumsum(group_lens)
