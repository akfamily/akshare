from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from numba import njit

import vectorbt as vbt
from vectorbt.base import (
    array_wrapper,
    column_grouper,
    combine_fns,
    index_fns,
    indexing,
    reshape_fns
)

ray_available = True
try:
    import ray
except:
    ray_available = False

day_dt = np.timedelta64(86400000000000)

# Initialize global variables
a1 = np.array([1])
a2 = np.array([1, 2, 3])
a3 = np.array([[1, 2, 3]])
a4 = np.array([[1], [2], [3]])
a5 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
sr_none = pd.Series([1])
sr1 = pd.Series([1], index=pd.Index(['x1'], name='i1'), name='a1')
sr2 = pd.Series([1, 2, 3], index=pd.Index(['x2', 'y2', 'z2'], name='i2'), name='a2')
df_none = pd.DataFrame([[1]])
df1 = pd.DataFrame(
    [[1]],
    index=pd.Index(['x3'], name='i3'),
    columns=pd.Index(['a3'], name='c3'))
df2 = pd.DataFrame(
    [[1], [2], [3]],
    index=pd.Index(['x4', 'y4', 'z4'], name='i4'),
    columns=pd.Index(['a4'], name='c4'))
df3 = pd.DataFrame(
    [[1, 2, 3]],
    index=pd.Index(['x5'], name='i5'),
    columns=pd.Index(['a5', 'b5', 'c5'], name='c5'))
df4 = pd.DataFrame(
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    index=pd.Index(['x6', 'y6', 'z6'], name='i6'),
    columns=pd.Index(['a6', 'b6', 'c6'], name='c6'))
multi_i = pd.MultiIndex.from_arrays([['x7', 'y7', 'z7'], ['x8', 'y8', 'z8']], names=['i7', 'i8'])
multi_c = pd.MultiIndex.from_arrays([['a7', 'b7', 'c7'], ['a8', 'b8', 'c8']], names=['c7', 'c8'])
df5 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], index=multi_i, columns=multi_c)


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.broadcasting['index_from'] = 'stack'
    vbt.settings.broadcasting['columns_from'] = 'stack'
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []
    if ray_available:
        ray.init(local_mode=True, num_cpus=1)


def teardown_module():
    if ray_available:
        ray.shutdown()
    vbt.settings.reset()


# ############# column_grouper.py ############# #


grouped_columns = pd.MultiIndex.from_arrays([
    [1, 1, 1, 1, 0, 0, 0, 0],
    [3, 3, 2, 2, 1, 1, 0, 0],
    [7, 6, 5, 4, 3, 2, 1, 0]
], names=['first', 'second', 'third'])


class TestColumnGrouper:
    def test_group_by_to_index(self):
        assert not column_grouper.group_by_to_index(grouped_columns, group_by=False)
        assert column_grouper.group_by_to_index(grouped_columns, group_by=None) is None
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(grouped_columns, group_by=True),
            pd.Index(['group'] * len(grouped_columns))
        )
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(grouped_columns, group_by=0),
            pd.Index([1, 1, 1, 1, 0, 0, 0, 0], dtype='int64', name='first')
        )
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(grouped_columns, group_by='first'),
            pd.Index([1, 1, 1, 1, 0, 0, 0, 0], dtype='int64', name='first')
        )
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(grouped_columns, group_by=[0, 1]),
            pd.MultiIndex.from_tuples([
                (1, 3),
                (1, 3),
                (1, 2),
                (1, 2),
                (0, 1),
                (0, 1),
                (0, 0),
                (0, 0)
            ], names=['first', 'second'])
        )
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(grouped_columns, group_by=['first', 'second']),
            pd.MultiIndex.from_tuples([
                (1, 3),
                (1, 3),
                (1, 2),
                (1, 2),
                (0, 1),
                (0, 1),
                (0, 0),
                (0, 0)
            ], names=['first', 'second'])
        )
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(
                grouped_columns, group_by=np.array([3, 2, 1, 1, 1, 0, 0, 0])),
            pd.Index([3, 2, 1, 1, 1, 0, 0, 0], dtype='int64')
        )
        pd.testing.assert_index_equal(
            column_grouper.group_by_to_index(
                grouped_columns, group_by=pd.Index([3, 2, 1, 1, 1, 0, 0, 0], name='fourth')),
            pd.Index([3, 2, 1, 1, 1, 0, 0, 0], dtype='int64', name='fourth')
        )

    def test_get_groups_and_index(self):
        a, b = column_grouper.get_groups_and_index(grouped_columns, group_by=None)
        np.testing.assert_array_equal(a, np.array([0, 1, 2, 3, 4, 5, 6, 7]))
        pd.testing.assert_index_equal(b, grouped_columns)
        a, b = column_grouper.get_groups_and_index(grouped_columns, group_by=0)
        np.testing.assert_array_equal(a, np.array([0, 0, 0, 0, 1, 1, 1, 1]))
        pd.testing.assert_index_equal(b, pd.Index([1, 0], dtype='int64', name='first'))
        a, b = column_grouper.get_groups_and_index(grouped_columns, group_by=[0, 1])
        np.testing.assert_array_equal(a, np.array([0, 0, 1, 1, 2, 2, 3, 3]))
        pd.testing.assert_index_equal(b, pd.MultiIndex.from_tuples([
            (1, 3),
            (1, 2),
            (0, 1),
            (0, 0)
        ], names=['first', 'second']))

    def test_get_group_lens_nb(self):
        np.testing.assert_array_equal(
            column_grouper.get_group_lens_nb(np.array([0, 0, 0, 0, 1, 1, 1, 1])),
            np.array([4, 4])
        )
        np.testing.assert_array_equal(
            column_grouper.get_group_lens_nb(np.array([0, 1])),
            np.array([1, 1])
        )
        np.testing.assert_array_equal(
            column_grouper.get_group_lens_nb(np.array([0, 0])),
            np.array([2])
        )
        np.testing.assert_array_equal(
            column_grouper.get_group_lens_nb(np.array([0])),
            np.array([1])
        )
        np.testing.assert_array_equal(
            column_grouper.get_group_lens_nb(np.array([])),
            np.array([])
        )
        with pytest.raises(Exception):
            column_grouper.get_group_lens_nb(np.array([1, 1, 0, 0]))
        with pytest.raises(Exception):
            column_grouper.get_group_lens_nb(np.array([0, 1, 0, 1]))

    def test_is_grouped(self):
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouped()
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouped(group_by=True)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouped(group_by=1)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouped(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouped()
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouped(group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouped(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouped(group_by=False)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0) \
            .is_grouped(group_by=grouped_columns.get_level_values(0) + 1)  # only labels

    def test_is_grouping_enabled(self):
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_enabled()
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_enabled(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_enabled(group_by=1)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_enabled(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_enabled()
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouping_enabled(group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouping_enabled(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_enabled(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0) \
            .is_grouping_enabled(group_by=grouped_columns.get_level_values(0) + 1)  # only labels

    def test_is_grouping_disabled(self):
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_disabled()
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_disabled(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_disabled(group_by=1)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_disabled(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_disabled()
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_disabled(group_by=0)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_disabled(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_disabled(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0) \
            .is_grouping_disabled(group_by=grouped_columns.get_level_values(0) + 1)  # only labels

    def test_is_grouping_modified(self):
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_modified()
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_modified(group_by=True)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_modified(group_by=1)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_modified(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_modified()
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouping_modified(group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouping_modified(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_modified(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0) \
            .is_grouping_modified(group_by=grouped_columns.get_level_values(0) + 1)  # only labels

    def test_is_grouping_changed(self):
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_changed()
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_changed(group_by=True)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_changed(group_by=1)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_grouping_changed(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_changed()
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouping_changed(group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns).is_grouping_changed(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_grouping_changed(group_by=False)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0) \
            .is_grouping_changed(group_by=grouped_columns.get_level_values(0) + 1)  # only labels

    def test_is_group_count_changed(self):
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_group_count_changed()
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_group_count_changed(group_by=True)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_group_count_changed(group_by=1)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0).is_group_count_changed(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_group_count_changed()
        assert column_grouper.ColumnGrouper(grouped_columns).is_group_count_changed(group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns).is_group_count_changed(group_by=True)
        assert not column_grouper.ColumnGrouper(grouped_columns).is_group_count_changed(group_by=False)
        assert not column_grouper.ColumnGrouper(grouped_columns, group_by=0) \
            .is_group_count_changed(group_by=grouped_columns.get_level_values(0) + 1)  # only labels

    def test_check_group_by(self):
        column_grouper.ColumnGrouper(grouped_columns, group_by=None, allow_enable=True).check_group_by(group_by=0)
        with pytest.raises(Exception):
            column_grouper.ColumnGrouper(grouped_columns, group_by=None, allow_enable=False).check_group_by(group_by=0)
        column_grouper.ColumnGrouper(grouped_columns, group_by=0, allow_disable=True).check_group_by(group_by=False)
        with pytest.raises(Exception):
            column_grouper.ColumnGrouper(grouped_columns, group_by=0, allow_disable=False).check_group_by(
                group_by=False)
        column_grouper.ColumnGrouper(grouped_columns, group_by=0, allow_modify=True).check_group_by(group_by=1)
        column_grouper.ColumnGrouper(grouped_columns, group_by=0, allow_modify=False).check_group_by(
            group_by=np.array([2, 2, 2, 2, 3, 3, 3, 3]))
        with pytest.raises(Exception):
            column_grouper.ColumnGrouper(grouped_columns, group_by=0, allow_modify=False).check_group_by(group_by=1)

    def test_resolve_group_by(self):
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=None).resolve_group_by() is None  # default
        pd.testing.assert_index_equal(
            column_grouper.ColumnGrouper(grouped_columns, group_by=None).resolve_group_by(group_by=0),  # overrides
            pd.Index([1, 1, 1, 1, 0, 0, 0, 0], dtype='int64', name='first')
        )
        pd.testing.assert_index_equal(
            column_grouper.ColumnGrouper(grouped_columns, group_by=0).resolve_group_by(),  # default
            pd.Index([1, 1, 1, 1, 0, 0, 0, 0], dtype='int64', name='first')
        )
        pd.testing.assert_index_equal(
            column_grouper.ColumnGrouper(grouped_columns, group_by=0).resolve_group_by(group_by=1),  # overrides
            pd.Index([3, 3, 2, 2, 1, 1, 0, 0], dtype='int64', name='second')
        )

    def test_get_groups(self):
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_groups(),
            np.array([0, 1, 2, 3, 4, 5, 6, 7])
        )
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_groups(group_by=0),
            np.array([0, 0, 0, 0, 1, 1, 1, 1])
        )

    def test_get_columns(self):
        pd.testing.assert_index_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_columns(),
            column_grouper.ColumnGrouper(grouped_columns).columns
        )
        pd.testing.assert_index_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_columns(group_by=0),
            pd.Index([1, 0], dtype='int64', name='first')
        )

    def test_get_group_lens(self):
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_group_lens(),
            np.array([1, 1, 1, 1, 1, 1, 1, 1])
        )
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_group_lens(group_by=0),
            np.array([4, 4])
        )

    def test_get_group_start_idxs(self):
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_group_start_idxs(),
            np.array([0, 1, 2, 3, 4, 5, 6, 7])
        )
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_group_start_idxs(group_by=0),
            np.array([0, 4])
        )

    def test_get_group_end_idxs(self):
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_group_end_idxs(),
            np.array([1, 2, 3, 4, 5, 6, 7, 8])
        )
        np.testing.assert_array_equal(
            column_grouper.ColumnGrouper(grouped_columns).get_group_end_idxs(group_by=0),
            np.array([4, 8])
        )

    def test_eq(self):
        assert column_grouper.ColumnGrouper(grouped_columns) == column_grouper.ColumnGrouper(grouped_columns)
        assert column_grouper.ColumnGrouper(grouped_columns, group_by=0) == column_grouper.ColumnGrouper(
            grouped_columns, group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns) != 0
        assert column_grouper.ColumnGrouper(grouped_columns) != column_grouper.ColumnGrouper(grouped_columns,
                                                                                             group_by=0)
        assert column_grouper.ColumnGrouper(grouped_columns) != column_grouper.ColumnGrouper(pd.Index([0]))
        assert column_grouper.ColumnGrouper(grouped_columns) != column_grouper.ColumnGrouper(
            grouped_columns, allow_enable=False)
        assert column_grouper.ColumnGrouper(grouped_columns) != column_grouper.ColumnGrouper(
            grouped_columns, allow_disable=False)
        assert column_grouper.ColumnGrouper(grouped_columns) != column_grouper.ColumnGrouper(
            grouped_columns, allow_modify=False)


# ############# array_wrapper.py ############# #


sr2_wrapper = array_wrapper.ArrayWrapper.from_obj(sr2)
df2_wrapper = array_wrapper.ArrayWrapper.from_obj(df2)
df4_wrapper = array_wrapper.ArrayWrapper.from_obj(df4)

sr2_wrapper_co = sr2_wrapper.replace(column_only_select=True)
df4_wrapper_co = df4_wrapper.replace(column_only_select=True)

sr2_grouped_wrapper = sr2_wrapper.replace(group_by=np.array(['g1']), group_select=True)
df4_grouped_wrapper = df4_wrapper.replace(group_by=np.array(['g1', 'g1', 'g2']), group_select=True)

sr2_grouped_wrapper_co = sr2_grouped_wrapper.replace(column_only_select=True, group_select=True)
df4_grouped_wrapper_co = df4_grouped_wrapper.replace(column_only_select=True, group_select=True)


class TestArrayWrapper:
    def test_config(self, tmp_path):
        assert array_wrapper.ArrayWrapper.loads(sr2_wrapper.dumps()) == sr2_wrapper
        assert array_wrapper.ArrayWrapper.loads(sr2_wrapper_co.dumps()) == sr2_wrapper_co
        assert array_wrapper.ArrayWrapper.loads(sr2_grouped_wrapper.dumps()) == sr2_grouped_wrapper
        assert array_wrapper.ArrayWrapper.loads(sr2_grouped_wrapper_co.dumps()) == sr2_grouped_wrapper_co
        sr2_grouped_wrapper_co.save(tmp_path / 'sr2_grouped_wrapper_co')
        assert array_wrapper.ArrayWrapper.load(tmp_path / 'sr2_grouped_wrapper_co') == sr2_grouped_wrapper_co

    def test_indexing_func_meta(self):
        # not grouped
        a, b, c = sr2_wrapper.indexing_func_meta(lambda x: x.iloc[:2])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        assert b == 0
        assert c == 0
        a, b, c = df4_wrapper.indexing_func_meta(lambda x: x.iloc[0, :2])[1:]
        assert a == 0
        np.testing.assert_array_equal(b, np.array([0, 1]))
        np.testing.assert_array_equal(c, np.array([0, 1]))
        a, b, c = df4_wrapper.indexing_func_meta(lambda x: x.iloc[:2, 0])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        assert b == 0
        assert c == 0
        a, b, c = df4_wrapper.indexing_func_meta(lambda x: x.iloc[:2, [0]])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        np.testing.assert_array_equal(b, np.array([0]))
        np.testing.assert_array_equal(c, np.array([0]))
        a, b, c = df4_wrapper.indexing_func_meta(lambda x: x.iloc[:2, :2])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        np.testing.assert_array_equal(b, np.array([0, 1]))
        np.testing.assert_array_equal(c, np.array([0, 1]))
        with pytest.raises(Exception):
            _ = df4_wrapper.indexing_func_meta(lambda x: x.iloc[0, 0])[1:]
        with pytest.raises(Exception):
            _ = df4_wrapper.indexing_func_meta(lambda x: x.iloc[[0], 0])[1:]

        # not grouped, column only
        a, b, c = df4_wrapper_co.indexing_func_meta(lambda x: x.iloc[0])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        assert b == 0
        assert c == 0
        a, b, c = df4_wrapper_co.indexing_func_meta(lambda x: x.iloc[[0]])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        np.testing.assert_array_equal(b, np.array([0]))
        np.testing.assert_array_equal(c, np.array([0]))
        a, b, c = df4_wrapper_co.indexing_func_meta(lambda x: x.iloc[:2])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        np.testing.assert_array_equal(b, np.array([0, 1]))
        np.testing.assert_array_equal(c, np.array([0, 1]))
        with pytest.raises(Exception):
            _ = sr2_wrapper_co.indexing_func_meta(lambda x: x.iloc[:2])[1:]
        with pytest.raises(Exception):
            _ = df4_wrapper_co.indexing_func_meta(lambda x: x.iloc[:, :2])[1:]

        # grouped
        a, b, c = sr2_grouped_wrapper.indexing_func_meta(lambda x: x.iloc[:2])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        assert b == 0
        assert c == 0
        a, b, c = df4_grouped_wrapper.indexing_func_meta(lambda x: x.iloc[:2, 0])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        assert b == 0
        np.testing.assert_array_equal(c, np.array([0, 1]))
        a, b, c = df4_grouped_wrapper.indexing_func_meta(lambda x: x.iloc[:2, 1])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        assert b == 1
        assert c == 2
        a, b, c = df4_grouped_wrapper.indexing_func_meta(lambda x: x.iloc[:2, [1]])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        np.testing.assert_array_equal(b, np.array([1]))
        np.testing.assert_array_equal(c, np.array([2]))
        a, b, c = df4_grouped_wrapper.indexing_func_meta(lambda x: x.iloc[:2, :2])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1]))
        np.testing.assert_array_equal(b, np.array([0, 1]))
        np.testing.assert_array_equal(c, np.array([0, 1, 2]))
        with pytest.raises(Exception):
            _ = df4_grouped_wrapper.indexing_func_meta(lambda x: x.iloc[0, :2])[1:]

        # grouped, column only
        a, b, c = df4_grouped_wrapper_co.indexing_func_meta(lambda x: x.iloc[0])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        assert b == 0
        np.testing.assert_array_equal(c, np.array([0, 1]))
        a, b, c = df4_grouped_wrapper_co.indexing_func_meta(lambda x: x.iloc[1])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        assert b == 1
        assert c == 2
        a, b, c = df4_grouped_wrapper_co.indexing_func_meta(lambda x: x.iloc[[1]])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        np.testing.assert_array_equal(b, np.array([1]))
        np.testing.assert_array_equal(c, np.array([2]))
        a, b, c = df4_grouped_wrapper_co.indexing_func_meta(lambda x: x.iloc[:2])[1:]
        np.testing.assert_array_equal(a, np.array([0, 1, 2]))
        np.testing.assert_array_equal(b, np.array([0, 1]))
        np.testing.assert_array_equal(c, np.array([0, 1, 2]))

    def test_indexing(self):
        # not grouped
        pd.testing.assert_index_equal(
            sr2_wrapper.iloc[:2].index,
            pd.Index(['x2', 'y2'], dtype='object', name='i2'))
        pd.testing.assert_index_equal(
            sr2_wrapper.iloc[:2].columns,
            pd.Index(['a2'], dtype='object'))
        assert sr2_wrapper.iloc[:2].ndim == 1
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[0, :2].index,
            pd.Index(['a6', 'b6'], dtype='object', name='c6'))
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[0, :2].columns,
            pd.Index(['x6'], dtype='object', name='i6'))
        assert df4_wrapper.iloc[0, :2].ndim == 1
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[:2, 0].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[:2, 0].columns,
            pd.Index(['a6'], dtype='object', name='c6'))
        assert df4_wrapper.iloc[:2, 0].ndim == 1
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[:2, [0]].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[:2, [0]].columns,
            pd.Index(['a6'], dtype='object', name='c6'))
        assert df4_wrapper.iloc[:2, [0]].ndim == 2
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[:2, :2].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_wrapper.iloc[:2, :2].columns,
            pd.Index(['a6', 'b6'], dtype='object', name='c6'))
        assert df4_wrapper.iloc[:2, :2].ndim == 2

        # not grouped, column only
        pd.testing.assert_index_equal(
            df4_wrapper_co.iloc[0].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_wrapper_co.iloc[0].columns,
            pd.Index(['a6'], dtype='object', name='c6'))
        assert df4_wrapper_co.iloc[0].ndim == 1
        pd.testing.assert_index_equal(
            df4_wrapper_co.iloc[[0]].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_wrapper_co.iloc[[0]].columns,
            pd.Index(['a6'], dtype='object', name='c6'))
        assert df4_wrapper_co.iloc[[0]].ndim == 2
        pd.testing.assert_index_equal(
            df4_wrapper_co.iloc[:2].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_wrapper_co.iloc[:2].columns,
            pd.Index(['a6', 'b6'], dtype='object', name='c6'))
        assert df4_wrapper_co.iloc[:2].ndim == 2

        # grouped
        pd.testing.assert_index_equal(
            sr2_grouped_wrapper.iloc[:2].index,
            pd.Index(['x2', 'y2'], dtype='object', name='i2'))
        pd.testing.assert_index_equal(
            sr2_grouped_wrapper.iloc[:2].columns,
            pd.Index(['a2'], dtype='object'))
        assert sr2_grouped_wrapper.iloc[:2].ndim == 1
        assert sr2_grouped_wrapper.iloc[:2].grouped_ndim == 1
        pd.testing.assert_index_equal(
            sr2_grouped_wrapper.iloc[:2].grouper.group_by,
            pd.Index(['g1'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, 0].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, 0].columns,
            pd.Index(['a6', 'b6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper.iloc[:2, 0].ndim == 2
        assert df4_grouped_wrapper.iloc[:2, 0].grouped_ndim == 1
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, 0].grouper.group_by,
            pd.Index(['g1', 'g1'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, 1].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, 1].columns,
            pd.Index(['c6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper.iloc[:2, 1].ndim == 1
        assert df4_grouped_wrapper.iloc[:2, 1].grouped_ndim == 1
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, 1].grouper.group_by,
            pd.Index(['g2'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, [1]].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, [1]].columns,
            pd.Index(['c6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper.iloc[:2, [1]].ndim == 2
        assert df4_grouped_wrapper.iloc[:2, [1]].grouped_ndim == 2
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, [1]].grouper.group_by,
            pd.Index(['g2'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, :2].index,
            pd.Index(['x6', 'y6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, :2].columns,
            pd.Index(['a6', 'b6', 'c6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper.iloc[:2, :2].ndim == 2
        assert df4_grouped_wrapper.iloc[:2, :2].grouped_ndim == 2
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.iloc[:2, :2].grouper.group_by,
            pd.Index(['g1', 'g1', 'g2'], dtype='object'))

        # grouped, column only
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[0].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[0].columns,
            pd.Index(['a6', 'b6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper_co.iloc[0].ndim == 2
        assert df4_grouped_wrapper_co.iloc[0].grouped_ndim == 1
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[0].grouper.group_by,
            pd.Index(['g1', 'g1'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[1].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[1].columns,
            pd.Index(['c6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper_co.iloc[1].ndim == 1
        assert df4_grouped_wrapper_co.iloc[1].grouped_ndim == 1
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[1].grouper.group_by,
            pd.Index(['g2'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[[1]].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[[1]].columns,
            pd.Index(['c6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper_co.iloc[[1]].ndim == 2
        assert df4_grouped_wrapper_co.iloc[[1]].grouped_ndim == 2
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[[1]].grouper.group_by,
            pd.Index(['g2'], dtype='object'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[:2].index,
            pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'))
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[:2].columns,
            pd.Index(['a6', 'b6', 'c6'], dtype='object', name='c6'))
        assert df4_grouped_wrapper_co.iloc[:2].ndim == 2
        assert df4_grouped_wrapper_co.iloc[:2].grouped_ndim == 2
        pd.testing.assert_index_equal(
            df4_grouped_wrapper_co.iloc[:2].grouper.group_by,
            pd.Index(['g1', 'g1', 'g2'], dtype='object'))

    def test_from_obj(self):
        assert array_wrapper.ArrayWrapper.from_obj(sr2) == sr2_wrapper
        assert array_wrapper.ArrayWrapper.from_obj(df4) == df4_wrapper
        assert array_wrapper.ArrayWrapper.from_obj(sr2, column_only_select=True) == sr2_wrapper_co
        assert array_wrapper.ArrayWrapper.from_obj(df4, column_only_select=True) == df4_wrapper_co

    def test_from_shape(self):
        assert array_wrapper.ArrayWrapper.from_shape((3,)) == \
               array_wrapper.ArrayWrapper(
                   pd.RangeIndex(start=0, stop=3, step=1), pd.RangeIndex(start=0, stop=1, step=1), 1)
        assert array_wrapper.ArrayWrapper.from_shape((3, 3)) == \
               array_wrapper.ArrayWrapper.from_obj(pd.DataFrame(np.empty((3, 3))))

    def test_columns(self):
        pd.testing.assert_index_equal(df4_wrapper.columns, df4.columns)
        pd.testing.assert_index_equal(df4_grouped_wrapper.columns, df4.columns)
        pd.testing.assert_index_equal(df4_grouped_wrapper.get_columns(), pd.Index(['g1', 'g2'], dtype='object'))

    def test_name(self):
        assert sr2_wrapper.name == 'a2'
        assert df4_wrapper.name is None
        assert array_wrapper.ArrayWrapper.from_obj(pd.Series([0])).name is None
        assert sr2_grouped_wrapper.name == 'a2'
        assert sr2_grouped_wrapper.get_name() == 'g1'
        assert df4_grouped_wrapper.name is None
        assert df4_grouped_wrapper.get_name() is None

    def test_ndim(self):
        assert sr2_wrapper.ndim == 1
        assert df4_wrapper.ndim == 2
        assert sr2_grouped_wrapper.ndim == 1
        assert sr2_grouped_wrapper.get_ndim() == 1
        assert df4_grouped_wrapper.ndim == 2
        assert df4_grouped_wrapper.get_ndim() == 2
        assert df4_grouped_wrapper['g1'].ndim == 2
        assert df4_grouped_wrapper['g1'].get_ndim() == 1
        assert df4_grouped_wrapper['g2'].ndim == 1
        assert df4_grouped_wrapper['g2'].get_ndim() == 1

    def test_shape(self):
        assert sr2_wrapper.shape == (3,)
        assert df4_wrapper.shape == (3, 3)
        assert sr2_grouped_wrapper.shape == (3,)
        assert sr2_grouped_wrapper.get_shape() == (3,)
        assert df4_grouped_wrapper.shape == (3, 3)
        assert df4_grouped_wrapper.get_shape() == (3, 2)

    def test_shape_2d(self):
        assert sr2_wrapper.shape_2d == (3, 1)
        assert df4_wrapper.shape_2d == (3, 3)
        assert sr2_grouped_wrapper.shape_2d == (3, 1)
        assert sr2_grouped_wrapper.get_shape_2d() == (3, 1)
        assert df4_grouped_wrapper.shape_2d == (3, 3)
        assert df4_grouped_wrapper.get_shape_2d() == (3, 2)

    def test_freq(self):
        assert sr2_wrapper.freq is None
        assert sr2_wrapper.replace(freq='1D').freq == day_dt
        assert sr2_wrapper.replace(index=pd.DatetimeIndex([
            datetime(2020, 1, 1),
            datetime(2020, 1, 2),
            datetime(2020, 1, 3)
        ], freq='1D')).freq == day_dt
        assert sr2_wrapper.replace(index=pd.Index([
            datetime(2020, 1, 1),
            datetime(2020, 1, 2),
            datetime(2020, 1, 3)
        ])).freq == day_dt

    def test_to_timedelta(self):
        sr = pd.Series([1, 2, np.nan], index=['x', 'y', 'z'], name='name')
        pd.testing.assert_series_equal(
            array_wrapper.ArrayWrapper.from_obj(sr, freq='1 days').to_timedelta(sr),
            pd.Series(
                np.array([86400000000000, 172800000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=sr.index,
                name=sr.name
            )
        )
        df = sr.to_frame()
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper.from_obj(df, freq='1 days').to_timedelta(df),
            pd.DataFrame(
                np.array([86400000000000, 172800000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=df.index,
                columns=df.columns
            )
        )

    def test_wrap(self):
        pd.testing.assert_series_equal(
            array_wrapper.ArrayWrapper(index=sr1.index, columns=[0], ndim=1).wrap(a1),  # empty
            pd.Series(a1, index=sr1.index, name=None)
        )
        pd.testing.assert_series_equal(
            array_wrapper.ArrayWrapper(index=sr1.index, columns=[sr1.name], ndim=1).wrap(a1),
            pd.Series(a1, index=sr1.index, name=sr1.name)
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper(index=sr1.index, columns=[sr1.name], ndim=2).wrap(a1),
            pd.DataFrame(a1, index=sr1.index, columns=[sr1.name])
        )
        pd.testing.assert_series_equal(
            array_wrapper.ArrayWrapper(index=sr2.index, columns=[sr2.name], ndim=1).wrap(a2),
            pd.Series(a2, index=sr2.index, name=sr2.name)
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper(index=sr2.index, columns=[sr2.name], ndim=2).wrap(a2),
            pd.DataFrame(a2, index=sr2.index, columns=[sr2.name])
        )
        pd.testing.assert_series_equal(
            array_wrapper.ArrayWrapper(index=df2.index, columns=df2.columns, ndim=1).wrap(a2),
            pd.Series(a2, index=df2.index, name=df2.columns[0])
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper(index=df2.index, columns=df2.columns, ndim=2).wrap(a2),
            pd.DataFrame(a2, index=df2.index, columns=df2.columns)
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper.from_obj(df2).wrap(a2, index=df4.index),
            pd.DataFrame(a2, index=df4.index, columns=df2.columns)
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper(index=df4.index, columns=df4.columns, ndim=2).wrap(
                np.array([[0, 0, np.nan], [1, np.nan, 1], [2, 2, np.nan]]),
                fillna=-1
            ),
            pd.DataFrame([
                [0., 0., -1.],
                [1., -1., 1.],
                [2., 2., -1.]
            ], index=df4.index, columns=df4.columns)
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper(index=df4.index, columns=df4.columns, ndim=2).wrap(
                np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]),
                to_index=True
            ),
            pd.DataFrame([
                ['x6', 'x6', 'x6'],
                ['y6', 'y6', 'y6'],
                ['z6', 'z6', 'z6']
            ], index=df4.index, columns=df4.columns)
        )
        pd.testing.assert_frame_equal(
            array_wrapper.ArrayWrapper(index=df4.index, columns=df4.columns, ndim=2, freq='d').wrap(
                np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]),
                to_timedelta=True
            ),
            pd.DataFrame([
                [pd.Timedelta(days=0), pd.Timedelta(days=0), pd.Timedelta(days=0)],
                [pd.Timedelta(days=1), pd.Timedelta(days=1), pd.Timedelta(days=1)],
                [pd.Timedelta(days=2), pd.Timedelta(days=2), pd.Timedelta(days=2)]
            ], index=df4.index, columns=df4.columns)
        )

    def test_wrap_reduced(self):
        # sr to value
        assert sr2_wrapper.wrap_reduced(0) == 0
        assert sr2_wrapper.wrap_reduced(np.array([0])) == 0  # result of computation on 2d
        # sr to array
        pd.testing.assert_series_equal(
            sr2_wrapper.wrap_reduced(np.array([0, 1])),
            pd.Series(np.array([0, 1]), name=sr2.name)
        )
        pd.testing.assert_series_equal(
            sr2_wrapper.wrap_reduced(np.array([0, 1]), name_or_index=['x', 'y']),
            pd.Series(np.array([0, 1]), index=['x', 'y'], name=sr2.name)
        )
        pd.testing.assert_series_equal(
            sr2_wrapper.wrap_reduced(np.array([0, 1]), name_or_index=['x', 'y'], columns=[0]),
            pd.Series(np.array([0, 1]), index=['x', 'y'], name=None)
        )
        # df to value
        assert df2_wrapper.wrap_reduced(0) == 0
        assert df4_wrapper.wrap_reduced(0) == 0
        # df to value per column
        pd.testing.assert_series_equal(
            df4_wrapper.wrap_reduced(np.array([0, 1, 2]), name_or_index='test'),
            pd.Series(np.array([0, 1, 2]), index=df4.columns, name='test')
        )
        pd.testing.assert_series_equal(
            df4_wrapper.wrap_reduced(np.array([0, 1, 2]), columns=['m', 'n', 'l'], name_or_index='test'),
            pd.Series(np.array([0, 1, 2]), index=['m', 'n', 'l'], name='test')
        )
        # df to array per column
        pd.testing.assert_frame_equal(
            df4_wrapper.wrap_reduced(np.array([[0, 1, 2], [3, 4, 5]]), name_or_index=['x', 'y']),
            pd.DataFrame(np.array([[0, 1, 2], [3, 4, 5]]), index=['x', 'y'], columns=df4.columns)
        )
        pd.testing.assert_frame_equal(
            df4_wrapper.wrap_reduced(
                np.array([[0, 1, 2], [3, 4, 5]]),
                name_or_index=['x', 'y'], columns=['m', 'n', 'l']),
            pd.DataFrame(np.array([[0, 1, 2], [3, 4, 5]]), index=['x', 'y'], columns=['m', 'n', 'l'])
        )

    def test_grouped_wrapping(self):
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.wrap(np.array([[1, 2], [3, 4], [5, 6]])),
            pd.DataFrame(np.array([
                [1, 2],
                [3, 4],
                [5, 6]
            ]), index=df4.index, columns=pd.Index(['g1', 'g2'], dtype='object'))
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.wrap_reduced(np.array([1, 2])),
            pd.Series(np.array([1, 2]), index=pd.Index(['g1', 'g2'], dtype='object'))
        )
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.wrap(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), group_by=False),
            pd.DataFrame(np.array([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]), index=df4.index, columns=df4.columns)
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.wrap_reduced(np.array([1, 2, 3]), group_by=False),
            pd.Series(np.array([1, 2, 3]), index=df4.columns)
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[0].wrap(np.array([1, 2, 3])),
            pd.Series(np.array([1, 2, 3]), index=df4.index, name='g1')
        )
        assert df4_grouped_wrapper_co.iloc[0].wrap_reduced(np.array([1])) == 1
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[0].wrap(np.array([[1], [2], [3]])),
            pd.Series(np.array([1, 2, 3]), index=df4.index, name='g1')
        )
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.iloc[0].wrap(np.array([[1, 2], [3, 4], [5, 6]]), group_by=False),
            pd.DataFrame(np.array([
                [1, 2],
                [3, 4],
                [5, 6]
            ]), index=df4.index, columns=df4.columns[:2])
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[0].wrap_reduced(np.array([1, 2]), group_by=False),
            pd.Series(np.array([1, 2]), index=df4.columns[:2])
        )
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.iloc[[0]].wrap(np.array([1, 2, 3])),
            pd.DataFrame(np.array([
                [1],
                [2],
                [3]
            ]), index=df4.index, columns=pd.Index(['g1'], dtype='object'))
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[[0]].wrap_reduced(np.array([1])),
            pd.Series(np.array([1]), index=pd.Index(['g1'], dtype='object'))
        )
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.iloc[[0]].wrap(np.array([[1, 2], [3, 4], [5, 6]]), group_by=False),
            pd.DataFrame(np.array([
                [1, 2],
                [3, 4],
                [5, 6]
            ]), index=df4.index, columns=df4.columns[:2])
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[[0]].wrap_reduced(np.array([1, 2]), group_by=False),
            pd.Series(np.array([1, 2]), index=df4.columns[:2])
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[1].wrap(np.array([1, 2, 3])),
            pd.Series(np.array([1, 2, 3]), index=df4.index, name='g2')
        )
        assert df4_grouped_wrapper_co.iloc[1].wrap_reduced(np.array([1])) == 1
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[1].wrap(np.array([1, 2, 3]), group_by=False),
            pd.Series(np.array([1, 2, 3]), index=df4.index, name=df4.columns[2])
        )
        assert df4_grouped_wrapper_co.iloc[1].wrap_reduced(np.array([1]), group_by=False) == 1
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.iloc[[1]].wrap(np.array([1, 2, 3])),
            pd.DataFrame(np.array([
                [1],
                [2],
                [3]
            ]), index=df4.index, columns=pd.Index(['g2'], dtype='object'))
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[[1]].wrap_reduced(np.array([1])),
            pd.Series(np.array([1]), index=pd.Index(['g2'], dtype='object'))
        )
        pd.testing.assert_frame_equal(
            df4_grouped_wrapper_co.iloc[[1]].wrap(np.array([1, 2, 3]), group_by=False),
            pd.DataFrame(np.array([
                [1],
                [2],
                [3]
            ]), index=df4.index, columns=df4.columns[2:])
        )
        pd.testing.assert_series_equal(
            df4_grouped_wrapper_co.iloc[[1]].wrap_reduced(np.array([1]), group_by=False),
            pd.Series(np.array([1]), index=df4.columns[2:])
        )

    def test_dummy(self):
        pd.testing.assert_index_equal(
            sr2_wrapper.dummy().index,
            sr2_wrapper.index
        )
        pd.testing.assert_index_equal(
            sr2_wrapper.dummy().to_frame().columns,
            sr2_wrapper.columns
        )
        pd.testing.assert_index_equal(
            df4_wrapper.dummy().index,
            df4_wrapper.index
        )
        pd.testing.assert_index_equal(
            df4_wrapper.dummy().columns,
            df4_wrapper.columns
        )
        pd.testing.assert_index_equal(
            sr2_grouped_wrapper.dummy().index,
            sr2_grouped_wrapper.index
        )
        pd.testing.assert_index_equal(
            sr2_grouped_wrapper.dummy().to_frame().columns,
            sr2_grouped_wrapper.get_columns()
        )
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.dummy().index,
            df4_grouped_wrapper.index
        )
        pd.testing.assert_index_equal(
            df4_grouped_wrapper.dummy().columns,
            df4_grouped_wrapper.get_columns()
        )


sr2_wrapping = array_wrapper.Wrapping(sr2_wrapper)
df4_wrapping = array_wrapper.Wrapping(df4_wrapper)

sr2_grouped_wrapping = array_wrapper.Wrapping(sr2_grouped_wrapper)
df4_grouped_wrapping = array_wrapper.Wrapping(df4_grouped_wrapper)


class TestWrapping:
    def test_regroup(self):
        assert df4_wrapping.regroup(None) == df4_wrapping
        assert df4_wrapping.regroup(False) == df4_wrapping
        assert df4_grouped_wrapping.regroup(None) == df4_grouped_wrapping
        assert df4_grouped_wrapping.regroup(df4_grouped_wrapper.grouper.group_by) == df4_grouped_wrapping
        pd.testing.assert_index_equal(
            df4_wrapping.regroup(df4_grouped_wrapper.grouper.group_by).wrapper.grouper.group_by,
            df4_grouped_wrapper.grouper.group_by
        )
        assert df4_grouped_wrapping.regroup(False).wrapper.grouper.group_by is None

    def test_select_one(self):
        assert sr2_wrapping.select_one() == sr2_wrapping
        assert sr2_grouped_wrapping.select_one() == sr2_grouped_wrapping
        pd.testing.assert_index_equal(
            df4_wrapping.select_one(column='a6').wrapper.get_columns(),
            pd.Index(['a6'], dtype='object', name='c6')
        )
        pd.testing.assert_index_equal(
            df4_grouped_wrapping.select_one(column='g1').wrapper.get_columns(),
            pd.Index(['g1'], dtype='object')
        )
        with pytest.raises(Exception):
            df4_wrapping.select_one()
        with pytest.raises(Exception):
            df4_grouped_wrapping.select_one()


# ############# index_fns.py ############# #

class TestIndexFns:
    def test_get_index(self):
        pd.testing.assert_index_equal(index_fns.get_index(sr1, 0), sr1.index)
        pd.testing.assert_index_equal(index_fns.get_index(sr1, 1), pd.Index([sr1.name]))
        pd.testing.assert_index_equal(index_fns.get_index(pd.Series([1, 2, 3]), 1), pd.Index([0]))  # empty
        pd.testing.assert_index_equal(index_fns.get_index(df1, 0), df1.index)
        pd.testing.assert_index_equal(index_fns.get_index(df1, 1), df1.columns)

    def test_index_from_values(self):
        pd.testing.assert_index_equal(
            index_fns.index_from_values([0.1, 0.2], name='a'),
            pd.Index([0.1, 0.2], dtype='float64', name='a')
        )
        pd.testing.assert_index_equal(
            index_fns.index_from_values(np.tile(np.arange(1, 4)[:, None][:, None], (1, 3, 3)), name='b'),
            pd.Index([1, 2, 3], dtype='int64', name='b')
        )
        pd.testing.assert_index_equal(
            index_fns.index_from_values(np.random.uniform(size=(3, 3, 3)), name='c'),
            pd.Index(['array_0', 'array_1', 'array_2'], dtype='object', name='c')
        )
        pd.testing.assert_index_equal(
            index_fns.index_from_values([(1, 2), (3, 4), (5, 6)], name='c'),
            pd.Index(['tuple_0', 'tuple_1', 'tuple_2'], dtype='object', name='c')
        )

        class A:
            pass

        class B:
            pass

        class C:
            pass

        pd.testing.assert_index_equal(
            index_fns.index_from_values([A(), B(), C()], name='c'),
            pd.Index(['A_0', 'B_1', 'C_2'], dtype='object', name='c')
        )

    def test_repeat_index(self):
        i = pd.Index([1, 2, 3], name='i')
        pd.testing.assert_index_equal(
            index_fns.repeat_index(i, 3),
            pd.Index([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype='int64', name='i')
        )
        pd.testing.assert_index_equal(
            index_fns.repeat_index(multi_i, 3),
            pd.MultiIndex.from_tuples([
                ('x7', 'x8'),
                ('x7', 'x8'),
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('y7', 'y8'),
                ('y7', 'y8'),
                ('z7', 'z8'),
                ('z7', 'z8'),
                ('z7', 'z8')
            ], names=['i7', 'i8'])
        )
        pd.testing.assert_index_equal(
            index_fns.repeat_index([0], 3),  # empty
            pd.Index([0, 1, 2], dtype='int64')
        )
        pd.testing.assert_index_equal(
            index_fns.repeat_index(sr_none.index, 3),  # simple range
            pd.RangeIndex(start=0, stop=3, step=1)
        )

    def test_tile_index(self):
        i = pd.Index([1, 2, 3], name='i')
        pd.testing.assert_index_equal(
            index_fns.tile_index(i, 3),
            pd.Index([1, 2, 3, 1, 2, 3, 1, 2, 3], dtype='int64', name='i')
        )
        pd.testing.assert_index_equal(
            index_fns.tile_index(multi_i, 3),
            pd.MultiIndex.from_tuples([
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('z7', 'z8'),
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('z7', 'z8'),
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('z7', 'z8')
            ], names=['i7', 'i8'])
        )
        pd.testing.assert_index_equal(
            index_fns.tile_index([0], 3),  # empty
            pd.Index([0, 1, 2], dtype='int64')
        )
        pd.testing.assert_index_equal(
            index_fns.tile_index(sr_none.index, 3),  # simple range
            pd.RangeIndex(start=0, stop=3, step=1)
        )

    def test_stack_indexes(self):
        pd.testing.assert_index_equal(
            index_fns.stack_indexes([sr2.index, df2.index, df5.index]),
            pd.MultiIndex.from_tuples([
                ('x2', 'x4', 'x7', 'x8'),
                ('y2', 'y4', 'y7', 'y8'),
                ('z2', 'z4', 'z7', 'z8')
            ], names=['i2', 'i4', 'i7', 'i8'])
        )
        pd.testing.assert_index_equal(
            index_fns.stack_indexes([sr2.index, df2.index, sr2.index], drop_duplicates=False),
            pd.MultiIndex.from_tuples([
                ('x2', 'x4', 'x2'),
                ('y2', 'y4', 'y2'),
                ('z2', 'z4', 'z2')
            ], names=['i2', 'i4', 'i2'])
        )
        pd.testing.assert_index_equal(
            index_fns.stack_indexes([sr2.index, df2.index, sr2.index], drop_duplicates=True),
            pd.MultiIndex.from_tuples([
                ('x4', 'x2'),
                ('y4', 'y2'),
                ('z4', 'z2')
            ], names=['i4', 'i2'])
        )
        pd.testing.assert_index_equal(
            index_fns.stack_indexes([pd.Index([1, 1]), pd.Index([2, 3])], drop_redundant=True),
            pd.Index([2, 3])
        )

    def test_combine_indexes(self):
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([pd.Index([1]), pd.Index([2, 3])], drop_redundant=False),
            pd.MultiIndex.from_tuples([
                (1, 2),
                (1, 3)
            ])
        )
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([pd.Index([1]), pd.Index([2, 3])], drop_redundant=True),
            pd.Index([2, 3], dtype='int64')
        )
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([pd.Index([1], name='i'), pd.Index([2, 3])], drop_redundant=True),
            pd.MultiIndex.from_tuples([
                (1, 2),
                (1, 3)
            ], names=['i', None])
        )
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([pd.Index([1, 2]), pd.Index([3])], drop_redundant=False),
            pd.MultiIndex.from_tuples([
                (1, 3),
                (2, 3)
            ])
        )
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([pd.Index([1, 2]), pd.Index([3])], drop_redundant=True),
            pd.Index([1, 2], dtype='int64')
        )
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([pd.Index([1]), pd.Index([2, 3])], drop_redundant=(False, True)),
            pd.Index([2, 3], dtype='int64')
        )
        pd.testing.assert_index_equal(
            index_fns.combine_indexes([df2.index, df5.index]),
            pd.MultiIndex.from_tuples([
                ('x4', 'x7', 'x8'),
                ('x4', 'y7', 'y8'),
                ('x4', 'z7', 'z8'),
                ('y4', 'x7', 'x8'),
                ('y4', 'y7', 'y8'),
                ('y4', 'z7', 'z8'),
                ('z4', 'x7', 'x8'),
                ('z4', 'y7', 'y8'),
                ('z4', 'z7', 'z8')
            ], names=['i4', 'i7', 'i8'])
        )

    def test_drop_levels(self):
        pd.testing.assert_index_equal(
            index_fns.drop_levels(multi_i, 'i7'),
            pd.Index(['x8', 'y8', 'z8'], dtype='object', name='i8')
        )
        pd.testing.assert_index_equal(
            index_fns.drop_levels(multi_i, 'i8'),
            pd.Index(['x7', 'y7', 'z7'], dtype='object', name='i7')
        )
        pd.testing.assert_index_equal(
            index_fns.drop_levels(multi_i, 'i9', strict=False),
            multi_i
        )
        with pytest.raises(Exception):
            _ = index_fns.drop_levels(multi_i, 'i9')
        pd.testing.assert_index_equal(
            index_fns.drop_levels(multi_i, ['i7', 'i8'], strict=False),  # won't do anything
            pd.MultiIndex.from_tuples([
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('z7', 'z8')
            ], names=['i7', 'i8'])
        )
        with pytest.raises(Exception):
            _ = index_fns.drop_levels(multi_i, ['i7', 'i8'])

    def test_rename_levels(self):
        i = pd.Index([1, 2, 3], name='i')
        pd.testing.assert_index_equal(
            index_fns.rename_levels(i, {'i': 'f'}),
            pd.Index([1, 2, 3], dtype='int64', name='f')
        )
        pd.testing.assert_index_equal(
            index_fns.rename_levels(i, {'a': 'b'}, strict=False),
            i
        )
        with pytest.raises(Exception):
            _ = index_fns.rename_levels(i, {'a': 'b'}, strict=True)
        pd.testing.assert_index_equal(
            index_fns.rename_levels(multi_i, {'i7': 'f7', 'i8': 'f8'}),
            pd.MultiIndex.from_tuples([
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('z7', 'z8')
            ], names=['f7', 'f8'])
        )

    def test_select_levels(self):
        pd.testing.assert_index_equal(
            index_fns.select_levels(multi_i, 'i7'),
            pd.Index(['x7', 'y7', 'z7'], dtype='object', name='i7')
        )
        pd.testing.assert_index_equal(
            index_fns.select_levels(multi_i, ['i7']),
            pd.MultiIndex.from_tuples([
                ('x7',),
                ('y7',),
                ('z7',)
            ], names=['i7'])
        )
        pd.testing.assert_index_equal(
            index_fns.select_levels(multi_i, ['i7', 'i8']),
            pd.MultiIndex.from_tuples([
                ('x7', 'x8'),
                ('y7', 'y8'),
                ('z7', 'z8')
            ], names=['i7', 'i8'])
        )

    def test_drop_redundant_levels(self):
        pd.testing.assert_index_equal(
            index_fns.drop_redundant_levels(pd.Index(['a', 'a'])),
            pd.Index(['a', 'a'], dtype='object')
        )  # if one unnamed, leaves as-is
        pd.testing.assert_index_equal(
            index_fns.drop_redundant_levels(pd.MultiIndex.from_arrays([['a', 'a'], ['b', 'b']])),
            pd.MultiIndex.from_tuples([
                ('a', 'b'),
                ('a', 'b')
            ])  # if all unnamed, leaves as-is
        )
        pd.testing.assert_index_equal(
            index_fns.drop_redundant_levels(pd.MultiIndex.from_arrays([['a', 'a'], ['b', 'b']], names=['hi', None])),
            pd.Index(['a', 'a'], dtype='object', name='hi')  # removes level with single unnamed value
        )
        pd.testing.assert_index_equal(
            index_fns.drop_redundant_levels(pd.MultiIndex.from_arrays([['a', 'b'], ['a', 'b']], names=['hi', 'hi2'])),
            pd.MultiIndex.from_tuples([
                ('a', 'a'),
                ('b', 'b')
            ], names=['hi', 'hi2'])  # legit
        )
        pd.testing.assert_index_equal(  # ignores 0-to-n
            index_fns.drop_redundant_levels(pd.MultiIndex.from_arrays([[0, 1], ['a', 'b']], names=[None, 'hi2'])),
            pd.Index(['a', 'b'], dtype='object', name='hi2')
        )
        pd.testing.assert_index_equal(  # legit
            index_fns.drop_redundant_levels(pd.MultiIndex.from_arrays([[0, 2], ['a', 'b']], names=[None, 'hi2'])),
            pd.MultiIndex.from_tuples([
                (0, 'a'),
                (2, 'b')
            ], names=[None, 'hi2'])
        )
        pd.testing.assert_index_equal(  # legit (w/ name)
            index_fns.drop_redundant_levels(pd.MultiIndex.from_arrays([[0, 1], ['a', 'b']], names=['hi', 'hi2'])),
            pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b')
            ], names=['hi', 'hi2'])
        )

    def test_drop_duplicate_levels(self):
        pd.testing.assert_index_equal(
            index_fns.drop_duplicate_levels(pd.MultiIndex.from_arrays(
                [[1, 2, 3], [1, 2, 3]], names=['a', 'a'])),
            pd.Index([1, 2, 3], dtype='int64', name='a')
        )
        pd.testing.assert_index_equal(
            index_fns.drop_duplicate_levels(pd.MultiIndex.from_tuples(
                [(0, 1, 2, 1), ('a', 'b', 'c', 'b')], names=['x', 'y', 'z', 'y']), keep='last'),
            pd.MultiIndex.from_tuples([
                (0, 2, 1),
                ('a', 'c', 'b')
            ], names=['x', 'z', 'y'])
        )
        pd.testing.assert_index_equal(
            index_fns.drop_duplicate_levels(pd.MultiIndex.from_tuples(
                [(0, 1, 2, 1), ('a', 'b', 'c', 'b')], names=['x', 'y', 'z', 'y']), keep='first'),
            pd.MultiIndex.from_tuples([
                (0, 1, 2),
                ('a', 'b', 'c')
            ], names=['x', 'y', 'z'])
        )

    def test_align_index_to(self):
        index1 = pd.Index(['c', 'b', 'a'], name='name1')
        assert index_fns.align_index_to(index1, index1) == pd.IndexSlice[:]
        index2 = pd.Index(['a', 'b', 'c', 'a', 'b', 'c'], name='name1')
        np.testing.assert_array_equal(
            index_fns.align_index_to(index1, index2),
            np.array([2, 1, 0, 2, 1, 0])
        )
        with pytest.raises(Exception):
            index_fns.align_index_to(pd.Index(['a']), pd.Index(['a', 'b', 'c']))
        index3 = pd.MultiIndex.from_tuples([
            (0, 'c'),
            (0, 'b'),
            (0, 'a'),
            (1, 'c'),
            (1, 'b'),
            (1, 'a')
        ], names=['name2', 'name1'])
        np.testing.assert_array_equal(
            index_fns.align_index_to(index1, index3),
            np.array([0, 1, 2, 0, 1, 2])
        )
        with pytest.raises(Exception):
            index_fns.align_index_to(
                pd.Index(['b', 'a'], name='name1'),
                index3
            )
        with pytest.raises(Exception):
            index_fns.align_index_to(
                pd.Index(['c', 'b', 'a', 'a'], name='name1'),
                index3
            )
        index4 = pd.MultiIndex.from_tuples([
            (0, 'a'),
            (0, 'b'),
            (0, 'c'),
            (1, 'a'),
            (1, 'b'),
            (1, 'c')
        ], names=['name2', 'name1'])
        np.testing.assert_array_equal(
            index_fns.align_index_to(index1, index4),
            np.array([2, 1, 0, 2, 1, 0])
        )

    def test_align_indexes(self):
        index1 = pd.Index(['a', 'b', 'c'])
        index2 = pd.MultiIndex.from_tuples([
            (0, 'a'),
            (0, 'b'),
            (0, 'c'),
            (1, 'a'),
            (1, 'b'),
            (1, 'c')
        ])
        index3 = pd.MultiIndex.from_tuples([
            (2, 0, 'a'),
            (2, 0, 'b'),
            (2, 0, 'c'),
            (2, 1, 'a'),
            (2, 1, 'b'),
            (2, 1, 'c'),
            (3, 0, 'a'),
            (3, 0, 'b'),
            (3, 0, 'c'),
            (3, 1, 'a'),
            (3, 1, 'b'),
            (3, 1, 'c')
        ])
        indices1, indices2, indices3 = index_fns.align_indexes([index1, index2, index3])
        np.testing.assert_array_equal(
            indices1,
            np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
        )
        np.testing.assert_array_equal(
            indices2,
            np.array([0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5])
        )
        assert indices3 == pd.IndexSlice[:]

    def test_pick_levels(self):
        index = index_fns.stack_indexes([multi_i, multi_c])
        assert index_fns.pick_levels(index, required_levels=[], optional_levels=[]) \
               == ([], [])
        assert index_fns.pick_levels(index, required_levels=['c8', 'c7', 'i8', 'i7'], optional_levels=[]) \
               == ([3, 2, 1, 0], [])
        assert index_fns.pick_levels(index, required_levels=['c8', None, 'i8', 'i7'], optional_levels=[]) \
               == ([3, 2, 1, 0], [])
        assert index_fns.pick_levels(index, required_levels=[None, 'c7', 'i8', 'i7'], optional_levels=[]) \
               == ([3, 2, 1, 0], [])
        assert index_fns.pick_levels(index, required_levels=[None, None, None, None], optional_levels=[]) \
               == ([0, 1, 2, 3], [])
        assert index_fns.pick_levels(index, required_levels=['c8', 'c7', 'i8'], optional_levels=['i7']) \
               == ([3, 2, 1], [0])
        assert index_fns.pick_levels(index, required_levels=['c8', None, 'i8'], optional_levels=['i7']) \
               == ([3, 2, 1], [0])
        assert index_fns.pick_levels(index, required_levels=[None, 'c7', 'i8'], optional_levels=['i7']) \
               == ([3, 2, 1], [0])
        assert index_fns.pick_levels(index, required_levels=[None, None, None, None], optional_levels=[None]) \
               == ([0, 1, 2, 3], [None])
        with pytest.raises(Exception):
            index_fns.pick_levels(index, required_levels=['i8', 'i8', 'i8', 'i8'], optional_levels=[])
        with pytest.raises(Exception):
            index_fns.pick_levels(index, required_levels=['c8', 'c7', 'i8', 'i7'], optional_levels=['i7'])


# ############# reshape_fns.py ############# #


class TestReshapeFns:
    def test_soft_to_ndim(self):
        np.testing.assert_array_equal(reshape_fns.soft_to_ndim(a2, 1), a2)
        pd.testing.assert_series_equal(reshape_fns.soft_to_ndim(sr2, 1), sr2)
        pd.testing.assert_series_equal(reshape_fns.soft_to_ndim(df2, 1), df2.iloc[:, 0])
        pd.testing.assert_frame_equal(reshape_fns.soft_to_ndim(df4, 1), df4)  # cannot -> do nothing
        np.testing.assert_array_equal(reshape_fns.soft_to_ndim(a2, 2), a2[:, None])
        pd.testing.assert_frame_equal(reshape_fns.soft_to_ndim(sr2, 2), sr2.to_frame())
        pd.testing.assert_frame_equal(reshape_fns.soft_to_ndim(df2, 2), df2)

    def test_to_1d(self):
        np.testing.assert_array_equal(reshape_fns.to_1d(None), np.asarray([None]))
        np.testing.assert_array_equal(reshape_fns.to_1d(0), np.asarray([0]))
        np.testing.assert_array_equal(reshape_fns.to_1d(a2), a2)
        pd.testing.assert_series_equal(reshape_fns.to_1d(sr2), sr2)
        pd.testing.assert_series_equal(reshape_fns.to_1d(df2), df2.iloc[:, 0])
        np.testing.assert_array_equal(reshape_fns.to_1d(df2, raw=True), df2.iloc[:, 0].values)

    def test_to_2d(self):
        np.testing.assert_array_equal(reshape_fns.to_2d(None), np.asarray([[None]]))
        np.testing.assert_array_equal(reshape_fns.to_2d(0), np.asarray([[0]]))
        np.testing.assert_array_equal(reshape_fns.to_2d(a2), a2[:, None])
        pd.testing.assert_frame_equal(reshape_fns.to_2d(sr2), sr2.to_frame())
        pd.testing.assert_frame_equal(reshape_fns.to_2d(df2), df2)
        np.testing.assert_array_equal(reshape_fns.to_2d(df2, raw=True), df2.values)

    def test_repeat_axis0(self):
        target = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3])
        np.testing.assert_array_equal(reshape_fns.repeat(0, 3, axis=0), np.full(3, 0))
        np.testing.assert_array_equal(
            reshape_fns.repeat(a2, 3, axis=0),
            target)
        pd.testing.assert_series_equal(
            reshape_fns.repeat(sr2, 3, axis=0),
            pd.Series(target, index=index_fns.repeat_index(sr2.index, 3), name=sr2.name))
        pd.testing.assert_frame_equal(
            reshape_fns.repeat(df2, 3, axis=0),
            pd.DataFrame(target, index=index_fns.repeat_index(df2.index, 3), columns=df2.columns))

    def test_repeat_axis1(self):
        target = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        np.testing.assert_array_equal(reshape_fns.repeat(0, 3, axis=1), np.full((1, 3), 0))
        np.testing.assert_array_equal(
            reshape_fns.repeat(a2, 3, axis=1),
            target)
        pd.testing.assert_frame_equal(
            reshape_fns.repeat(sr2, 3, axis=1),
            pd.DataFrame(target, index=sr2.index, columns=index_fns.repeat_index([sr2.name], 3)))
        pd.testing.assert_frame_equal(
            reshape_fns.repeat(df2, 3, axis=1),
            pd.DataFrame(target, index=df2.index, columns=index_fns.repeat_index(df2.columns, 3)))

    def test_tile_axis0(self):
        target = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
        np.testing.assert_array_equal(reshape_fns.tile(0, 3, axis=0), np.full(3, 0))
        np.testing.assert_array_equal(
            reshape_fns.tile(a2, 3, axis=0),
            target)
        pd.testing.assert_series_equal(
            reshape_fns.tile(sr2, 3, axis=0),
            pd.Series(target, index=index_fns.tile_index(sr2.index, 3), name=sr2.name))
        pd.testing.assert_frame_equal(
            reshape_fns.tile(df2, 3, axis=0),
            pd.DataFrame(target, index=index_fns.tile_index(df2.index, 3), columns=df2.columns))

    def test_tile_axis1(self):
        target = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        np.testing.assert_array_equal(reshape_fns.tile(0, 3, axis=1), np.full((1, 3), 0))
        np.testing.assert_array_equal(
            reshape_fns.tile(a2, 3, axis=1),
            target)
        pd.testing.assert_frame_equal(
            reshape_fns.tile(sr2, 3, axis=1),
            pd.DataFrame(target, index=sr2.index, columns=index_fns.tile_index([sr2.name], 3)))
        pd.testing.assert_frame_equal(
            reshape_fns.tile(df2, 3, axis=1),
            pd.DataFrame(target, index=df2.index, columns=index_fns.tile_index(df2.columns, 3)))

    def test_broadcast_numpy(self):
        # 1d
        to_broadcast = 0, a1, a2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(*to_broadcast)
        for i in range(len(broadcasted)):
            np.testing.assert_array_equal(
                broadcasted[i],
                broadcasted_arrs[i]
            )
        # 2d
        to_broadcast = 0, a1, a2, a3, a4, a5
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(*to_broadcast)
        for i in range(len(broadcasted)):
            np.testing.assert_array_equal(
                broadcasted[i],
                broadcasted_arrs[i]
            )

    def test_broadcast_stack(self):
        # 1d
        to_broadcast = 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            index_from='stack',
            columns_from='stack',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_series_equal(
                broadcasted[i],
                pd.Series(
                    broadcasted_arrs[i],
                    index=pd.MultiIndex.from_tuples([
                        ('x1', 'x2'),
                        ('x1', 'y2'),
                        ('x1', 'z2')
                    ], names=['i1', 'i2']),
                    name=None
                )
            )
        # 2d
        to_broadcast_a = 0, a1, a2, a3, a4, a5
        to_broadcast_sr = sr_none, sr1, sr2
        to_broadcast_df = df_none, df1, df2, df3, df4
        broadcasted_arrs = list(np.broadcast_arrays(
            *to_broadcast_a,
            *[x.to_frame() for x in to_broadcast_sr],  # here is the difference
            *to_broadcast_df
        ))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast_a, *to_broadcast_sr, *to_broadcast_df,
            index_from='stack',
            columns_from='stack',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_frame_equal(
                broadcasted[i],
                pd.DataFrame(
                    broadcasted_arrs[i],
                    index=pd.MultiIndex.from_tuples([
                        ('x1', 'x2', 'x3', 'x4', 'x5', 'x6'),
                        ('x1', 'y2', 'x3', 'y4', 'x5', 'y6'),
                        ('x1', 'z2', 'x3', 'z4', 'x5', 'z6')
                    ], names=['i1', 'i2', 'i3', 'i4', 'i5', 'i6']),
                    columns=pd.MultiIndex.from_tuples([
                        ('a3', 'a4', 'a5', 'a6'),
                        ('a3', 'a4', 'b5', 'b6'),
                        ('a3', 'a4', 'c5', 'c6')
                    ], names=['c3', 'c4', 'c5', 'c6'])
                )
            )

        broadcasted = reshape_fns.broadcast(
            pd.DataFrame([[1, 2, 3]], columns=pd.Index(['a', 'b', 'c'], name='i1')),
            pd.DataFrame([[4, 5, 6]], columns=pd.Index(['a', 'b', 'c'], name='i2')),
            index_from='stack',
            columns_from='stack',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        pd.testing.assert_frame_equal(
            broadcasted[0],
            pd.DataFrame([[1, 2, 3]], columns=pd.MultiIndex.from_tuples([
                ('a', 'a'), ('b', 'b'), ('c', 'c')
            ], names=['i1', 'i2']))
        )
        pd.testing.assert_frame_equal(
            broadcasted[1],
            pd.DataFrame([[4, 5, 6]], columns=pd.MultiIndex.from_tuples([
                ('a', 'a'), ('b', 'b'), ('c', 'c')
            ], names=['i1', 'i2']))
        )

    def test_broadcast_keep(self):
        # 1d
        to_broadcast = 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            index_from='keep',
            columns_from='keep',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(4):
            pd.testing.assert_series_equal(
                broadcasted[i],
                pd.Series(broadcasted_arrs[i], index=pd.RangeIndex(start=0, stop=3, step=1))
            )
        pd.testing.assert_series_equal(
            broadcasted[4],
            pd.Series(broadcasted_arrs[4], index=pd.Index(['x1', 'x1', 'x1'], name='i1'), name=sr1.name)
        )
        pd.testing.assert_series_equal(
            broadcasted[5],
            pd.Series(broadcasted_arrs[5], index=sr2.index, name=sr2.name)
        )
        # 2d
        to_broadcast_a = 0, a1, a2, a3, a4, a5
        to_broadcast_sr = sr_none, sr1, sr2
        to_broadcast_df = df_none, df1, df2, df3, df4
        broadcasted_arrs = list(np.broadcast_arrays(
            *to_broadcast_a,
            *[x.to_frame() for x in to_broadcast_sr],  # here is the difference
            *to_broadcast_df
        ))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast_a, *to_broadcast_sr, *to_broadcast_df,
            index_from='keep',
            columns_from='keep',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(7):
            pd.testing.assert_frame_equal(
                broadcasted[i],
                pd.DataFrame(
                    broadcasted_arrs[i],
                    index=pd.RangeIndex(start=0, stop=3, step=1),
                    columns=pd.RangeIndex(start=0, stop=3, step=1)
                )
            )
        pd.testing.assert_frame_equal(
            broadcasted[7],
            pd.DataFrame(
                broadcasted_arrs[7],
                index=pd.Index(['x1', 'x1', 'x1'], dtype='object', name='i1'),
                columns=pd.Index(['a1', 'a1', 'a1'], dtype='object')
            )
        )
        pd.testing.assert_frame_equal(
            broadcasted[8],
            pd.DataFrame(
                broadcasted_arrs[8],
                index=sr2.index,
                columns=pd.Index(['a2', 'a2', 'a2'], dtype='object')
            )
        )
        pd.testing.assert_frame_equal(
            broadcasted[9],
            pd.DataFrame(
                broadcasted_arrs[9],
                index=pd.RangeIndex(start=0, stop=3, step=1),
                columns=pd.RangeIndex(start=0, stop=3, step=1)
            )
        )
        pd.testing.assert_frame_equal(
            broadcasted[10],
            pd.DataFrame(
                broadcasted_arrs[10],
                index=pd.Index(['x3', 'x3', 'x3'], dtype='object', name='i3'),
                columns=pd.Index(['a3', 'a3', 'a3'], dtype='object', name='c3')
            )
        )
        pd.testing.assert_frame_equal(
            broadcasted[11],
            pd.DataFrame(
                broadcasted_arrs[11],
                index=df2.index,
                columns=pd.Index(['a4', 'a4', 'a4'], dtype='object', name='c4')
            )
        )
        pd.testing.assert_frame_equal(
            broadcasted[12],
            pd.DataFrame(
                broadcasted_arrs[12],
                index=pd.Index(['x5', 'x5', 'x5'], dtype='object', name='i5'),
                columns=df3.columns
            )
        )
        pd.testing.assert_frame_equal(
            broadcasted[13],
            pd.DataFrame(
                broadcasted_arrs[13],
                index=df4.index,
                columns=df4.columns
            )
        )

    def test_broadcast_specify(self):
        # 1d
        to_broadcast = 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            index_from=multi_i,
            columns_from=['name'],  # should translate to Series name
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_series_equal(
                broadcasted[i],
                pd.Series(
                    broadcasted_arrs[i],
                    index=multi_i,
                    name='name'
                )
            )
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            index_from=multi_i,
            columns_from=[0],  # should translate to None
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_series_equal(
                broadcasted[i],
                pd.Series(
                    broadcasted_arrs[i],
                    index=multi_i,
                    name=None
                )
            )
        # 2d
        to_broadcast_a = 0, a1, a2, a3, a4, a5
        to_broadcast_sr = sr_none, sr1, sr2
        to_broadcast_df = df_none, df1, df2, df3, df4
        broadcasted_arrs = list(np.broadcast_arrays(
            *to_broadcast_a,
            *[x.to_frame() for x in to_broadcast_sr],  # here is the difference
            *to_broadcast_df
        ))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast_a, *to_broadcast_sr, *to_broadcast_df,
            index_from=multi_i,
            columns_from=multi_c,
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_frame_equal(
                broadcasted[i],
                pd.DataFrame(
                    broadcasted_arrs[i],
                    index=multi_i,
                    columns=multi_c
                )
            )

    def test_broadcast_idx(self):
        # 1d
        to_broadcast = 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            index_from=-1,
            columns_from=-1,  # should translate to Series name
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_series_equal(
                broadcasted[i],
                pd.Series(
                    broadcasted_arrs[i],
                    index=sr2.index,
                    name=sr2.name
                )
            )
        with pytest.raises(Exception):
            _ = reshape_fns.broadcast(
                *to_broadcast,
                index_from=0,
                columns_from=0,
                drop_duplicates=True,
                drop_redundant=True,
                ignore_sr_names=True
            )
        # 2d
        to_broadcast_a = 0, a1, a2, a3, a4, a5
        to_broadcast_sr = sr_none, sr1, sr2
        to_broadcast_df = df_none, df1, df2, df3, df4
        broadcasted_arrs = list(np.broadcast_arrays(
            *to_broadcast_a,
            *[x.to_frame() for x in to_broadcast_sr],  # here is the difference
            *to_broadcast_df
        ))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast_a, *to_broadcast_sr, *to_broadcast_df,
            index_from=-1,
            columns_from=-1,
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_frame_equal(
                broadcasted[i],
                pd.DataFrame(
                    broadcasted_arrs[i],
                    index=df4.index,
                    columns=df4.columns
                )
            )

    def test_broadcast_strict(self):
        # 1d
        to_broadcast = sr1, sr2
        with pytest.raises(Exception):
            _ = reshape_fns.broadcast(
                *to_broadcast,
                index_from='strict',  # changing index not allowed
                columns_from='stack',
                drop_duplicates=True,
                drop_redundant=True,
                ignore_sr_names=True
            )
        # 2d
        to_broadcast = df1, df2
        with pytest.raises(Exception):
            _ = reshape_fns.broadcast(
                *to_broadcast,
                index_from='stack',
                columns_from='strict',  # changing columns not allowed
                drop_duplicates=True,
                drop_redundant=True,
                ignore_sr_names=True
            )

    def test_broadcast_dirty(self):
        # 1d
        to_broadcast = sr2, 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            index_from='stack',
            columns_from='stack',
            drop_duplicates=False,
            drop_redundant=False,
            ignore_sr_names=False
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_series_equal(
                broadcasted[i],
                pd.Series(
                    broadcasted_arrs[i],
                    index=pd.MultiIndex.from_tuples([
                        ('x2', 'x1', 'x2'),
                        ('y2', 'x1', 'y2'),
                        ('z2', 'x1', 'z2')
                    ], names=['i2', 'i1', 'i2']),
                    name=('a2', 'a1', 'a2')
                )
            )

    def test_broadcast_to_shape(self):
        to_broadcast = 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = [
            np.broadcast_to(x.to_frame() if isinstance(x, pd.Series) else x, (3, 3))
            for x in to_broadcast
        ]
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            to_shape=(3, 3),
            index_from='stack',
            columns_from='stack',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            pd.testing.assert_frame_equal(
                broadcasted[i],
                pd.DataFrame(
                    broadcasted_arrs[i],
                    index=pd.MultiIndex.from_tuples([
                        ('x1', 'x2'),
                        ('x1', 'y2'),
                        ('x1', 'z2')
                    ], names=['i1', 'i2']),
                    columns=None
                )
            )

    @pytest.mark.parametrize(
        "test_to_pd",
        [False, [False, False, False, False, False, False]],
    )
    def test_broadcast_to_pd(self, test_to_pd):
        to_broadcast = 0, a1, a2, sr_none, sr1, sr2
        broadcasted_arrs = list(np.broadcast_arrays(*to_broadcast))
        broadcasted = reshape_fns.broadcast(
            *to_broadcast,
            to_pd=test_to_pd,  # to NumPy
            index_from='stack',
            columns_from='stack',
            drop_duplicates=True,
            drop_redundant=True,
            ignore_sr_names=True
        )
        for i in range(len(broadcasted)):
            np.testing.assert_array_equal(
                broadcasted[i],
                broadcasted_arrs[i]
            )

    def test_broadcast_require_kwargs(self):
        a, b = reshape_fns.broadcast(np.empty((1,)), np.empty((1,)))  # readonly
        assert not a.flags.writeable
        assert not b.flags.writeable
        a, b = reshape_fns.broadcast(
            np.empty((1,)), np.empty((1,)),
            require_kwargs=[{'requirements': 'W'}, {}])  # writeable
        assert a.flags.writeable
        assert not b.flags.writeable
        a, b = reshape_fns.broadcast(
            np.empty((1,)), np.empty((1,)),
            require_kwargs=[{'requirements': ('W', 'C')}, {}])  # writeable, C order
        assert a.flags.writeable  # writeable since it was copied to make C order
        assert not b.flags.writeable
        assert not np.isfortran(a)
        assert not np.isfortran(b)

    def test_broadcast_meta(self):
        _0, _a2, _sr2, _df2 = reshape_fns.broadcast(0, a2, sr2, df2, keep_raw=True)
        assert _0 == 0
        np.testing.assert_array_equal(_a2, a2)
        np.testing.assert_array_equal(_sr2, sr2.values[:, None])
        np.testing.assert_array_equal(_df2, df2.values)
        _0, _a2, _sr2, _df2 = reshape_fns.broadcast(0, a2, sr2, df2, keep_raw=[False, True, True, True])
        test_shape = (3, 3)
        test_index = pd.MultiIndex.from_tuples([
            ('x2', 'x4'),
            ('y2', 'y4'),
            ('z2', 'z4')
        ], names=['i2', 'i4'])
        test_columns = pd.Index(['a4', 'a4', 'a4'], name='c4', dtype='object')
        pd.testing.assert_frame_equal(
            _0,
            pd.DataFrame(
                np.zeros(test_shape, dtype=int),
                index=test_index,
                columns=test_columns
            )
        )
        np.testing.assert_array_equal(_a2, a2)
        np.testing.assert_array_equal(_sr2, sr2.values[:, None])
        np.testing.assert_array_equal(_df2, df2.values)
        _, new_shape, new_index, new_columns = reshape_fns.broadcast(0, a2, sr2, df2, return_meta=True)
        assert new_shape == test_shape
        pd.testing.assert_index_equal(new_index, test_index)
        pd.testing.assert_index_equal(new_columns, test_columns)

    def test_broadcast_align(self):
        index1 = pd.Index(['a', 'b', 'c'])
        index2 = pd.MultiIndex.from_tuples([
            (0, 'a'),
            (0, 'b'),
            (0, 'c'),
            (1, 'a'),
            (1, 'b'),
            (1, 'c')
        ])
        index3 = pd.MultiIndex.from_tuples([
            (2, 0, 'a'),
            (2, 0, 'b'),
            (2, 0, 'c'),
            (2, 1, 'a'),
            (2, 1, 'b'),
            (2, 1, 'c'),
            (3, 0, 'a'),
            (3, 0, 'b'),
            (3, 0, 'c'),
            (3, 1, 'a'),
            (3, 1, 'b'),
            (3, 1, 'c')
        ])
        sr1 = pd.Series(np.arange(len(index1)), index=index1)
        df2 = pd.DataFrame(
            np.reshape(np.arange(len(index2) * len(index2)), (len(index2), len(index2))),
            index=index2, columns=index2
        )
        df3 = pd.DataFrame(
            np.reshape(np.arange(len(index3) * len(index3)), (len(index3), len(index3))),
            index=index3, columns=index3
        )
        _df1, _df2, _df3 = reshape_fns.broadcast(sr1, df2, df3, align_index=True, align_columns=True)
        pd.testing.assert_frame_equal(
            _df1,
            pd.DataFrame(np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            ]), index=index3, columns=index3)
        )
        pd.testing.assert_frame_equal(
            _df2,
            pd.DataFrame(np.array([
                [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10, 11, 6, 7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17, 12, 13, 14, 15, 16, 17],
                [18, 19, 20, 21, 22, 23, 18, 19, 20, 21, 22, 23],
                [24, 25, 26, 27, 28, 29, 24, 25, 26, 27, 28, 29],
                [30, 31, 32, 33, 34, 35, 30, 31, 32, 33, 34, 35],
                [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10, 11, 6, 7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17, 12, 13, 14, 15, 16, 17],
                [18, 19, 20, 21, 22, 23, 18, 19, 20, 21, 22, 23],
                [24, 25, 26, 27, 28, 29, 24, 25, 26, 27, 28, 29],
                [30, 31, 32, 33, 34, 35, 30, 31, 32, 33, 34, 35]
            ]), index=index3, columns=index3)
        )
        pd.testing.assert_frame_equal(_df3, df3)

    def test_broadcast_to(self):
        np.testing.assert_array_equal(reshape_fns.broadcast_to(0, a5), np.broadcast_to(0, a5.shape))
        pd.testing.assert_series_equal(
            reshape_fns.broadcast_to(0, sr2),
            pd.Series(np.broadcast_to(0, sr2.shape), index=sr2.index, name=sr2.name)
        )
        pd.testing.assert_frame_equal(
            reshape_fns.broadcast_to(0, df5),
            pd.DataFrame(np.broadcast_to(0, df5.shape), index=df5.index, columns=df5.columns)
        )
        pd.testing.assert_frame_equal(
            reshape_fns.broadcast_to(sr2, df5),
            pd.DataFrame(np.broadcast_to(sr2.to_frame(), df5.shape), index=df5.index, columns=df5.columns)
        )
        pd.testing.assert_frame_equal(
            reshape_fns.broadcast_to(sr2, df5, index_from=0, columns_from=0),
            pd.DataFrame(
                np.broadcast_to(sr2.to_frame(), df5.shape),
                index=sr2.index,
                columns=pd.Index(['a2', 'a2', 'a2'], dtype='object'))
        )

    @pytest.mark.parametrize(
        "test_input",
        [0, a2, a5, sr2, df5, np.zeros((2, 2, 2))],
    )
    def test_broadcast_to_array_of(self, test_input):
        # broadcasting first element to be an array out of the second argument
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_array_of(0.1, test_input),
            np.full((1, *np.asarray(test_input).shape), 0.1)
        )
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_array_of([0.1], test_input),
            np.full((1, *np.asarray(test_input).shape), 0.1)
        )
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_array_of([0.1, 0.2], test_input),
            np.concatenate((
                np.full((1, *np.asarray(test_input).shape), 0.1),
                np.full((1, *np.asarray(test_input).shape), 0.2)
            ))
        )
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_array_of(np.expand_dims(np.asarray(test_input), 0), test_input),  # do nothing
            np.expand_dims(np.asarray(test_input), 0)
        )

    def test_broadcast_to_axis_of(self):
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_axis_of(10, np.empty((2,)), 0),
            np.full(2, 10)
        )
        assert reshape_fns.broadcast_to_axis_of(10, np.empty((2,)), 1) == 10
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_axis_of(10, np.empty((2, 3)), 0),
            np.full(2, 10)
        )
        np.testing.assert_array_equal(
            reshape_fns.broadcast_to_axis_of(10, np.empty((2, 3)), 1),
            np.full(3, 10)
        )
        assert reshape_fns.broadcast_to_axis_of(10, np.empty((2, 3)), 2) == 10

    def test_unstack_to_array(self):
        i = pd.MultiIndex.from_arrays([[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']])
        sr = pd.Series([1, 2, 3, 4], index=i)
        np.testing.assert_array_equal(
            reshape_fns.unstack_to_array(sr),
            np.asarray([[
                [1., np.nan, np.nan, np.nan],
                [np.nan, 2., np.nan, np.nan]
            ], [
                [np.nan, np.nan, 3., np.nan],
                [np.nan, np.nan, np.nan, 4.]
            ]])
        )
        np.testing.assert_array_equal(
            reshape_fns.unstack_to_array(sr, levels=(0,)),
            np.asarray([2., 4.])
        )
        np.testing.assert_array_equal(
            reshape_fns.unstack_to_array(sr, levels=(2, 0)),
            np.asarray([
                [1., np.nan],
                [2., np.nan],
                [np.nan, 3.],
                [np.nan, 4.],
            ])
        )

    def test_make_symmetric(self):
        pd.testing.assert_frame_equal(
            reshape_fns.make_symmetric(sr2),
            pd.DataFrame(
                np.array([
                    [np.nan, 1.0, 2.0, 3.0],
                    [1.0, np.nan, np.nan, np.nan],
                    [2.0, np.nan, np.nan, np.nan],
                    [3.0, np.nan, np.nan, np.nan]
                ]),
                index=pd.Index(['a2', 'x2', 'y2', 'z2'], dtype='object', name=('i2', None)),
                columns=pd.Index(['a2', 'x2', 'y2', 'z2'], dtype='object', name=('i2', None))
            )
        )
        pd.testing.assert_frame_equal(
            reshape_fns.make_symmetric(df2),
            pd.DataFrame(
                np.array([
                    [np.nan, 1.0, 2.0, 3.0],
                    [1.0, np.nan, np.nan, np.nan],
                    [2.0, np.nan, np.nan, np.nan],
                    [3.0, np.nan, np.nan, np.nan]
                ]),
                index=pd.Index(['a4', 'x4', 'y4', 'z4'], dtype='object', name=('i4', 'c4')),
                columns=pd.Index(['a4', 'x4', 'y4', 'z4'], dtype='object', name=('i4', 'c4'))
            )
        )
        pd.testing.assert_frame_equal(
            reshape_fns.make_symmetric(df5),
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, 1.0, 4.0, 7.0],
                    [np.nan, np.nan, np.nan, 2.0, 5.0, 8.0],
                    [np.nan, np.nan, np.nan, 3.0, 6.0, 9.0],
                    [1.0, 2.0, 3.0, np.nan, np.nan, np.nan],
                    [4.0, 5.0, 6.0, np.nan, np.nan, np.nan],
                    [7.0, 8.0, 9.0, np.nan, np.nan, np.nan]
                ]),
                index=pd.MultiIndex.from_tuples([
                    ('a7', 'a8'),
                    ('b7', 'b8'),
                    ('c7', 'c8'),
                    ('x7', 'x8'),
                    ('y7', 'y8'),
                    ('z7', 'z8')
                ], names=[('i7', 'c7'), ('i8', 'c8')]),
                columns=pd.MultiIndex.from_tuples([
                    ('a7', 'a8'),
                    ('b7', 'b8'),
                    ('c7', 'c8'),
                    ('x7', 'x8'),
                    ('y7', 'y8'),
                    ('z7', 'z8')
                ], names=[('i7', 'c7'), ('i8', 'c8')])
            )
        )
        pd.testing.assert_frame_equal(
            reshape_fns.make_symmetric(pd.Series([1, 2, 3], name='yo'), sort=False),
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, 1.0],
                    [np.nan, np.nan, np.nan, 2.0],
                    [np.nan, np.nan, np.nan, 3.0],
                    [1.0, 2.0, 3.0, np.nan]
                ]),
                index=pd.Index([0, 1, 2, 'yo'], dtype='object'),
                columns=pd.Index([0, 1, 2, 'yo'], dtype='object')
            )
        )

    def test_unstack_to_df(self):
        pd.testing.assert_frame_equal(
            reshape_fns.unstack_to_df(df5.iloc[0]),
            pd.DataFrame(
                np.array([
                    [1.0, np.nan, np.nan],
                    [np.nan, 2.0, np.nan],
                    [np.nan, np.nan, 3.0]
                ]),
                index=pd.Index(['a7', 'b7', 'c7'], dtype='object', name='c7'),
                columns=pd.Index(['a8', 'b8', 'c8'], dtype='object', name='c8')
            )
        )
        i = pd.MultiIndex.from_arrays([[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']])
        sr = pd.Series([1, 2, 3, 4], index=i)
        pd.testing.assert_frame_equal(
            reshape_fns.unstack_to_df(sr, index_levels=0, column_levels=1),
            pd.DataFrame(
                np.array([
                    [1.0, 2.0],
                    [3.0, 4.0]
                ]),
                index=pd.Index([1, 2], dtype='int64'),
                columns=pd.Index([3, 4], dtype='int64')
            )
        )
        pd.testing.assert_frame_equal(
            reshape_fns.unstack_to_df(sr, index_levels=(0, 1), column_levels=2),
            pd.DataFrame(
                np.array([
                    [1.0, np.nan, np.nan, np.nan],
                    [np.nan, 2.0, np.nan, np.nan],
                    [np.nan, np.nan, 3.0, np.nan],
                    [np.nan, np.nan, np.nan, 4.0]
                ]),
                index=pd.MultiIndex.from_tuples([
                    (1, 3),
                    (1, 4),
                    (2, 3),
                    (2, 4)
                ]),
                columns=pd.Index(['a', 'b', 'c', 'd'], dtype='object')
            )
        )
        pd.testing.assert_frame_equal(
            reshape_fns.unstack_to_df(sr, index_levels=0, column_levels=1, symmetric=True),
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, 1.0, 2.0],
                    [np.nan, np.nan, 3.0, 4.0],
                    [1.0, 3.0, np.nan, np.nan],
                    [2.0, 4.0, np.nan, np.nan]
                ]),
                index=pd.Index([1, 2, 3, 4], dtype='int64'),
                columns=pd.Index([1, 2, 3, 4], dtype='int64')
            )
        )

    @pytest.mark.parametrize(
        "test_inputs",
        [
            (0, a1, a2, sr_none, sr1, sr2),
            (0, a1, a2, a3, a4, a5, sr_none, sr1, sr2, df_none, df1, df2, df3, df4)
        ],
    )
    def test_flex(self, test_inputs):
        raw_args = reshape_fns.broadcast(*test_inputs, keep_raw=True)
        bc_args = reshape_fns.broadcast(*test_inputs, keep_raw=False)
        for r in range(len(test_inputs)):
            raw_arg = raw_args[r]
            bc_arg = np.array(bc_args[r])
            bc_arg_2d = reshape_fns.to_2d(bc_arg)
            def_i, def_col = reshape_fns.flex_choose_i_and_col_nb(raw_arg, flex_2d=bc_arg.ndim == 2)
            for col in range(bc_arg_2d.shape[1]):
                for i in range(bc_arg_2d.shape[0]):
                    assert bc_arg_2d[i, col] == reshape_fns.flex_select_nb(
                        raw_arg, i, col, def_i, def_col, bc_arg.ndim == 2)


# ############# indexing.py ############# #


called_dict = {}

PandasIndexer = indexing.PandasIndexer
ParamIndexer = indexing.build_param_indexer(['param1', 'param2', 'tuple'])


class H(PandasIndexer, ParamIndexer):
    def __init__(self, a, param1_mapper, param2_mapper, tuple_mapper, level_names):
        self.a = a

        self._param1_mapper = param1_mapper
        self._param2_mapper = param2_mapper
        self._tuple_mapper = tuple_mapper
        self._level_names = level_names

        PandasIndexer.__init__(self, calling='PandasIndexer')
        ParamIndexer.__init__(
            self,
            [param1_mapper, param2_mapper, tuple_mapper],
            level_names=[level_names[0], level_names[1], level_names],
            calling='ParamIndexer'
        )

    def indexing_func(self, pd_indexing_func, calling=None):
        # As soon as you call iloc etc., performs it on each dataframe and mapper and returns a new class instance
        called_dict[calling] = True
        param1_mapper = indexing.indexing_on_mapper(self._param1_mapper, self.a, pd_indexing_func)
        param2_mapper = indexing.indexing_on_mapper(self._param2_mapper, self.a, pd_indexing_func)
        tuple_mapper = indexing.indexing_on_mapper(self._tuple_mapper, self.a, pd_indexing_func)
        return H(pd_indexing_func(self.a), param1_mapper, param2_mapper, tuple_mapper, self._level_names)

    @classmethod
    def run(cls, a, params1, params2, level_names=('p1', 'p2')):
        a = reshape_fns.to_2d(a)
        # Build column hierarchy
        params1_idx = pd.Index(params1, name=level_names[0])
        params2_idx = pd.Index(params2, name=level_names[1])
        params_idx = index_fns.stack_indexes([params1_idx, params2_idx])
        new_columns = index_fns.combine_indexes([params_idx, a.columns])

        # Build mappers
        param1_mapper = np.repeat(params1, len(a.columns))
        param1_mapper = pd.Series(param1_mapper, index=new_columns)

        param2_mapper = np.repeat(params2, len(a.columns))
        param2_mapper = pd.Series(param2_mapper, index=new_columns)

        tuple_mapper = list(zip(*list(map(lambda x: x.values, [param1_mapper, param2_mapper]))))
        tuple_mapper = pd.Series(tuple_mapper, index=new_columns)

        # Tile a to match the length of new_columns
        a = array_wrapper.ArrayWrapper(a.index, new_columns, 2).wrap(reshape_fns.tile(a.values, 4, axis=1))
        return cls(a, param1_mapper, param2_mapper, tuple_mapper, level_names)


# Similate an indicator with two params
h = H.run(df4, [0.1, 0.1, 0.2, 0.2], [0.3, 0.4, 0.5, 0.6])


class TestIndexing:
    def test_kwargs(self):
        _ = h[(0.1, 0.3, 'a6')]
        assert called_dict['PandasIndexer']
        _ = h.param1_loc[0.1]
        assert called_dict['ParamIndexer']

    def test_pandas_indexing(self):
        # __getitem__
        pd.testing.assert_series_equal(
            h[(0.1, 0.3, 'a6')].a,
            pd.Series(
                np.array([1, 4, 7]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                name=(0.1, 0.3, 'a6')
            )
        )
        # loc
        pd.testing.assert_frame_equal(
            h.loc[:, (0.1, 0.3, 'a6'):(0.1, 0.3, 'c6')].a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.MultiIndex.from_tuples([
                    (0.1, 0.3, 'a6'),
                    (0.1, 0.3, 'b6'),
                    (0.1, 0.3, 'c6')
                ], names=['p1', 'p2', 'c6'])
            )
        )
        # iloc
        pd.testing.assert_frame_equal(
            h.iloc[-2:, -2:].a,
            pd.DataFrame(
                np.array([
                    [5, 6],
                    [8, 9]
                ]),
                index=pd.Index(['y6', 'z6'], dtype='object', name='i6'),
                columns=pd.MultiIndex.from_tuples([
                    (0.2, 0.6, 'b6'),
                    (0.2, 0.6, 'c6')
                ], names=['p1', 'p2', 'c6'])
            )
        )
        # xs
        pd.testing.assert_frame_equal(
            h.xs((0.1, 0.3), level=('p1', 'p2'), axis=1).a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.Index(['a6', 'b6', 'c6'], dtype='object', name='c6')
            )
        )

    def test_param_indexing(self):
        # param1
        pd.testing.assert_frame_equal(
            h.param1_loc[0.1].a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3, 1, 2, 3],
                    [4, 5, 6, 4, 5, 6],
                    [7, 8, 9, 7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.MultiIndex.from_tuples([
                    (0.3, 'a6'),
                    (0.3, 'b6'),
                    (0.3, 'c6'),
                    (0.4, 'a6'),
                    (0.4, 'b6'),
                    (0.4, 'c6')
                ], names=['p2', 'c6'])
            )
        )
        # param2
        pd.testing.assert_frame_equal(
            h.param2_loc[0.3].a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.MultiIndex.from_tuples([
                    (0.1, 'a6'),
                    (0.1, 'b6'),
                    (0.1, 'c6')
                ], names=['p1', 'c6'])
            )
        )
        # tuple
        pd.testing.assert_frame_equal(
            h.tuple_loc[(0.1, 0.3)].a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.Index(['a6', 'b6', 'c6'], dtype='object', name='c6')
            )
        )
        pd.testing.assert_frame_equal(
            h.tuple_loc[(0.1, 0.3):(0.1, 0.3)].a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.MultiIndex.from_tuples([
                    (0.1, 0.3, 'a6'),
                    (0.1, 0.3, 'b6'),
                    (0.1, 0.3, 'c6')
                ], names=['p1', 'p2', 'c6'])
            )
        )
        pd.testing.assert_frame_equal(
            h.tuple_loc[[(0.1, 0.3), (0.1, 0.3)]].a,
            pd.DataFrame(
                np.array([
                    [1, 2, 3, 1, 2, 3],
                    [4, 5, 6, 4, 5, 6],
                    [7, 8, 9, 7, 8, 9]
                ]),
                index=pd.Index(['x6', 'y6', 'z6'], dtype='object', name='i6'),
                columns=pd.MultiIndex.from_tuples([
                    (0.1, 0.3, 'a6'),
                    (0.1, 0.3, 'b6'),
                    (0.1, 0.3, 'c6'),
                    (0.1, 0.3, 'a6'),
                    (0.1, 0.3, 'b6'),
                    (0.1, 0.3, 'c6')
                ], names=['p1', 'p2', 'c6'])
            )
        )


# ############# combine_fns.py ############# #

class TestCombineFns:
    def test_apply_and_concat_one(self):
        def apply_func(i, x, a):
            return x + a[i]

        @njit
        def apply_func_nb(i, x, a):
            return x + a[i]

        # 1d
        target = np.array([
            [11, 21, 31],
            [12, 22, 32],
            [13, 23, 33]
        ])
        np.testing.assert_array_equal(
            combine_fns.apply_and_concat_one(3, apply_func, sr2.values, [10, 20, 30]),
            target
        )
        np.testing.assert_array_equal(
            combine_fns.apply_and_concat_one_nb(3, apply_func_nb, sr2.values, (10, 20, 30)),
            target
        )
        # 2d
        target2 = np.array([
            [11, 12, 13, 21, 22, 23, 31, 32, 33],
            [14, 15, 16, 24, 25, 26, 34, 35, 36],
            [17, 18, 19, 27, 28, 29, 37, 38, 39]
        ])
        np.testing.assert_array_equal(
            combine_fns.apply_and_concat_one(3, apply_func, df4.values, [10, 20, 30]),
            target2
        )
        np.testing.assert_array_equal(
            combine_fns.apply_and_concat_one_nb(3, apply_func_nb, df4.values, (10, 20, 30)),
            target2
        )

    def test_apply_and_concat_multiple(self):
        def apply_func(i, x, a):
            return (x, x + a[i])

        @njit
        def apply_func_nb(i, x, a):
            return (x, x + a[i])

        # 1d
        target_a = np.array([
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3]
        ])
        target_b = np.array([
            [11, 21, 31],
            [12, 22, 32],
            [13, 23, 33]
        ])
        a, b = combine_fns.apply_and_concat_multiple(3, apply_func, sr2.values, [10, 20, 30])
        np.testing.assert_array_equal(a, target_a)
        np.testing.assert_array_equal(b, target_b)
        a, b = combine_fns.apply_and_concat_multiple_nb(3, apply_func_nb, sr2.values, (10, 20, 30))
        np.testing.assert_array_equal(a, target_a)
        np.testing.assert_array_equal(b, target_b)
        # 2d
        target_a = np.array([
            [1, 2, 3, 1, 2, 3, 1, 2, 3],
            [4, 5, 6, 4, 5, 6, 4, 5, 6],
            [7, 8, 9, 7, 8, 9, 7, 8, 9]
        ])
        target_b = np.array([
            [11, 12, 13, 21, 22, 23, 31, 32, 33],
            [14, 15, 16, 24, 25, 26, 34, 35, 36],
            [17, 18, 19, 27, 28, 29, 37, 38, 39]
        ])
        a, b = combine_fns.apply_and_concat_multiple(3, apply_func, df4.values, [10, 20, 30])
        np.testing.assert_array_equal(a, target_a)
        np.testing.assert_array_equal(b, target_b)
        a, b = combine_fns.apply_and_concat_multiple_nb(3, apply_func_nb, df4.values, (10, 20, 30))
        np.testing.assert_array_equal(a, target_a)
        np.testing.assert_array_equal(b, target_b)

    def test_combine_and_concat(self):
        def combine_func(x, y, a):
            return x + y + a

        @njit
        def combine_func_nb(x, y, a):
            return x + y + a

        # 1d
        target = np.array([
            [103, 104],
            [106, 108],
            [109, 112]
        ])
        np.testing.assert_array_equal(
            combine_fns.combine_and_concat(
                sr2.values, (sr2.values * 2, sr2.values * 3), combine_func, 100),
            target
        )
        np.testing.assert_array_equal(
            combine_fns.combine_and_concat_nb(
                sr2.values, (sr2.values * 2, sr2.values * 3), combine_func_nb, 100),
            target
        )
        # 2d
        target2 = np.array([
            [103, 106, 109, 104, 108, 112],
            [112, 115, 118, 116, 120, 124],
            [121, 124, 127, 128, 132, 136]
        ])
        np.testing.assert_array_equal(
            combine_fns.combine_and_concat(
                df4.values, (df4.values * 2, df4.values * 3), combine_func, 100),
            target2
        )
        np.testing.assert_array_equal(
            combine_fns.combine_and_concat_nb(
                df4.values, (df4.values * 2, df4.values * 3), combine_func_nb, 100),
            target2
        )

    def test_combine_multiple(self):
        def combine_func(x, y, a):
            return x + y + a

        @njit
        def combine_func_nb(x, y, a):
            return x + y + a

        # 1d
        target = np.array([206, 212, 218])
        np.testing.assert_array_equal(
            combine_fns.combine_multiple(
                (sr2.values, sr2.values * 2, sr2.values * 3), combine_func, 100),
            target
        )
        np.testing.assert_array_equal(
            combine_fns.combine_multiple_nb(
                (sr2.values, sr2.values * 2, sr2.values * 3), combine_func_nb, 100),
            target
        )
        # 2d
        target2 = np.array([
            [206, 212, 218],
            [224, 230, 236],
            [242, 248, 254]
        ])
        np.testing.assert_array_equal(
            combine_fns.combine_multiple(
                (df4.values, df4.values * 2, df4.values * 3), combine_func, 100),
            target2
        )
        np.testing.assert_array_equal(
            combine_fns.combine_multiple_nb(
                (df4.values, df4.values * 2, df4.values * 3), combine_func_nb, 100),
            target2
        )


# ############# accessors.py ############# #

class TestAccessors:
    def test_indexing(self):
        pd.testing.assert_series_equal(df4.vbt['a6'].obj, df4['a6'].vbt.obj)

    def test_freq(self):
        ts = pd.Series([1, 2, 3], index=pd.DatetimeIndex([
            datetime(2018, 1, 1),
            datetime(2018, 1, 2),
            datetime(2018, 1, 3)
        ]))
        assert ts.vbt.wrapper.freq == day_dt
        assert ts.vbt(freq='2D').wrapper.freq == day_dt * 2
        assert pd.Series([1, 2, 3]).vbt.wrapper.freq is None
        assert pd.Series([1, 2, 3]).vbt(freq='3D').wrapper.freq == day_dt * 3
        assert pd.Series([1, 2, 3]).vbt(freq=np.timedelta64(4, 'D')).wrapper.freq == day_dt * 4

    def test_props(self):
        assert sr1.vbt.is_series()
        assert not sr1.vbt.is_frame()
        assert not df1.vbt.is_series()
        assert df2.vbt.is_frame()

    def test_wrapper(self):
        pd.testing.assert_index_equal(sr2.vbt.wrapper.index, sr2.index)
        pd.testing.assert_index_equal(sr2.vbt.wrapper.columns, sr2.to_frame().columns)
        assert sr2.vbt.wrapper.ndim == sr2.ndim
        assert sr2.vbt.wrapper.name == sr2.name
        assert pd.Series([1, 2, 3]).vbt.wrapper.name is None
        assert sr2.vbt.wrapper.shape == sr2.shape
        assert sr2.vbt.wrapper.shape_2d == (sr2.shape[0], 1)
        pd.testing.assert_index_equal(df4.vbt.wrapper.index, df4.index)
        pd.testing.assert_index_equal(df4.vbt.wrapper.columns, df4.columns)
        assert df4.vbt.wrapper.ndim == df4.ndim
        assert df4.vbt.wrapper.name is None
        assert df4.vbt.wrapper.shape == df4.shape
        assert df4.vbt.wrapper.shape_2d == df4.shape
        pd.testing.assert_series_equal(sr2.vbt.wrapper.wrap(a2), sr2)
        pd.testing.assert_series_equal(sr2.vbt.wrapper.wrap(df2), sr2)
        pd.testing.assert_series_equal(
            sr2.vbt.wrapper.wrap(df2.values, index=df2.index, columns=df2.columns),
            pd.Series(df2.values[:, 0], index=df2.index, name=df2.columns[0])
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.wrapper.wrap(df4.values, columns=df4.columns),
            pd.DataFrame(df4.values, index=sr2.index, columns=df4.columns)
        )
        pd.testing.assert_frame_equal(df2.vbt.wrapper.wrap(a2), df2)
        pd.testing.assert_frame_equal(df2.vbt.wrapper.wrap(sr2), df2)
        pd.testing.assert_frame_equal(
            df2.vbt.wrapper.wrap(df4.values, columns=df4.columns),
            pd.DataFrame(df4.values, index=df2.index, columns=df4.columns)
        )

    def test_empty(self):
        pd.testing.assert_series_equal(
            pd.Series.vbt.empty(5, index=np.arange(10, 15), name='a', fill_value=5),
            pd.Series(np.full(5, 5), index=np.arange(10, 15), name='a')
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.empty((5, 3), index=np.arange(10, 15), columns=['a', 'b', 'c'], fill_value=5),
            pd.DataFrame(np.full((5, 3), 5), index=np.arange(10, 15), columns=['a', 'b', 'c'])
        )
        pd.testing.assert_series_equal(
            pd.Series.vbt.empty_like(sr2, fill_value=5),
            pd.Series(np.full(sr2.shape, 5), index=sr2.index, name=sr2.name)
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.empty_like(df4, fill_value=5),
            pd.DataFrame(np.full(df4.shape, 5), index=df4.index, columns=df4.columns)
        )

    def test_apply_func_on_index(self):
        pd.testing.assert_frame_equal(
            df1.vbt.apply_on_index(lambda idx: idx + '_yo', axis=0),
            pd.DataFrame(
                np.asarray([1]),
                index=pd.Index(['x3_yo'], dtype='object', name='i3'),
                columns=pd.Index(['a3'], dtype='object', name='c3')
            )
        )
        pd.testing.assert_frame_equal(
            df1.vbt.apply_on_index(lambda idx: idx + '_yo', axis=1),
            pd.DataFrame(
                np.asarray([1]),
                index=pd.Index(['x3'], dtype='object', name='i3'),
                columns=pd.Index(['a3_yo'], dtype='object', name='c3')
            )
        )
        df1_copy = df1.copy()
        df1_copy.vbt.apply_on_index(lambda idx: idx + '_yo', axis=0, inplace=True)
        pd.testing.assert_frame_equal(
            df1_copy,
            pd.DataFrame(
                np.asarray([1]),
                index=pd.Index(['x3_yo'], dtype='object', name='i3'),
                columns=pd.Index(['a3'], dtype='object', name='c3')
            )
        )
        df1_copy2 = df1.copy()
        df1_copy2.vbt.apply_on_index(lambda idx: idx + '_yo', axis=1, inplace=True)
        pd.testing.assert_frame_equal(
            df1_copy2,
            pd.DataFrame(
                np.asarray([1]),
                index=pd.Index(['x3'], dtype='object', name='i3'),
                columns=pd.Index(['a3_yo'], dtype='object', name='c3')
            )
        )

    def test_stack_index(self):
        pd.testing.assert_frame_equal(
            df5.vbt.stack_index([1, 2, 3], on_top=True),
            pd.DataFrame(
                df5.values,
                index=df5.index,
                columns=pd.MultiIndex.from_tuples([
                    (1, 'a7', 'a8'),
                    (2, 'b7', 'b8'),
                    (3, 'c7', 'c8')
                ], names=[None, 'c7', 'c8'])
            )
        )
        pd.testing.assert_frame_equal(
            df5.vbt.stack_index([1, 2, 3], on_top=False),
            pd.DataFrame(
                df5.values,
                index=df5.index,
                columns=pd.MultiIndex.from_tuples([
                    ('a7', 'a8', 1),
                    ('b7', 'b8', 2),
                    ('c7', 'c8', 3)
                ], names=['c7', 'c8', None])
            )
        )

    def test_drop_levels(self):
        pd.testing.assert_frame_equal(
            df5.vbt.drop_levels('c7'),
            pd.DataFrame(
                df5.values,
                index=df5.index,
                columns=pd.Index(['a8', 'b8', 'c8'], dtype='object', name='c8')
            )
        )

    def test_rename_levels(self):
        pd.testing.assert_frame_equal(
            df5.vbt.rename_levels({'c8': 'c9'}),
            pd.DataFrame(
                df5.values,
                index=df5.index,
                columns=pd.MultiIndex.from_tuples([
                    ('a7', 'a8'),
                    ('b7', 'b8'),
                    ('c7', 'c8')
                ], names=['c7', 'c9'])
            )
        )

    def test_select_levels(self):
        pd.testing.assert_frame_equal(
            df5.vbt.select_levels('c8'),
            pd.DataFrame(
                df5.values,
                index=df5.index,
                columns=pd.Index(['a8', 'b8', 'c8'], dtype='object', name='c8')
            )
        )

    def test_drop_redundant_levels(self):
        pd.testing.assert_frame_equal(
            df5.vbt.stack_index(pd.RangeIndex(start=0, step=1, stop=3)).vbt.drop_redundant_levels(),
            df5
        )

    def test_drop_duplicate_levels(self):
        pd.testing.assert_frame_equal(
            df5.vbt.stack_index(df5.columns.get_level_values(0)).vbt.drop_duplicate_levels(),
            df5
        )

    def test_to_array(self):
        np.testing.assert_array_equal(sr2.vbt.to_1d_array(), sr2.values)
        np.testing.assert_array_equal(sr2.vbt.to_2d_array(), sr2.to_frame().values)
        np.testing.assert_array_equal(df2.vbt.to_1d_array(), df2.iloc[:, 0].values)
        np.testing.assert_array_equal(df2.vbt.to_2d_array(), df2.values)

    def test_tile(self):
        pd.testing.assert_frame_equal(
            df4.vbt.tile(2, keys=['a', 'b'], axis=0),
            pd.DataFrame(
                np.asarray([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]),
                index=pd.MultiIndex.from_tuples([
                    ('a', 'x6'),
                    ('a', 'y6'),
                    ('a', 'z6'),
                    ('b', 'x6'),
                    ('b', 'y6'),
                    ('b', 'z6')
                ], names=[None, 'i6']),
                columns=df4.columns
            )
        )
        pd.testing.assert_frame_equal(
            df4.vbt.tile(2, keys=['a', 'b'], axis=1),
            pd.DataFrame(
                np.asarray([
                    [1, 2, 3, 1, 2, 3],
                    [4, 5, 6, 4, 5, 6],
                    [7, 8, 9, 7, 8, 9]
                ]),
                index=df4.index,
                columns=pd.MultiIndex.from_tuples([
                    ('a', 'a6'),
                    ('a', 'b6'),
                    ('a', 'c6'),
                    ('b', 'a6'),
                    ('b', 'b6'),
                    ('b', 'c6')
                ], names=[None, 'c6'])
            )
        )

    def test_repeat(self):
        pd.testing.assert_frame_equal(
            df4.vbt.repeat(2, keys=['a', 'b'], axis=0),
            pd.DataFrame(
                np.asarray([
                    [1, 2, 3],
                    [1, 2, 3],
                    [4, 5, 6],
                    [4, 5, 6],
                    [7, 8, 9],
                    [7, 8, 9]
                ]),
                index=pd.MultiIndex.from_tuples([
                    ('x6', 'a'),
                    ('x6', 'b'),
                    ('y6', 'a'),
                    ('y6', 'b'),
                    ('z6', 'a'),
                    ('z6', 'b')
                ], names=['i6', None]),
                columns=df4.columns
            )
        )
        pd.testing.assert_frame_equal(
            df4.vbt.repeat(2, keys=['a', 'b'], axis=1),
            pd.DataFrame(
                np.asarray([
                    [1, 1, 2, 2, 3, 3],
                    [4, 4, 5, 5, 6, 6],
                    [7, 7, 8, 8, 9, 9]
                ]),
                index=df4.index,
                columns=pd.MultiIndex.from_tuples([
                    ('a6', 'a'),
                    ('a6', 'b'),
                    ('b6', 'a'),
                    ('b6', 'b'),
                    ('c6', 'a'),
                    ('c6', 'b')
                ], names=['c6', None])
            )
        )

    def test_align_to(self):
        multi_c1 = pd.MultiIndex.from_arrays([['a8', 'b8']], names=['c8'])
        multi_c2 = pd.MultiIndex.from_arrays([['a7', 'a7', 'c7', 'c7'], ['a8', 'b8', 'a8', 'b8']], names=['c7', 'c8'])
        df10 = pd.DataFrame([[1, 2], [4, 5], [7, 8]], columns=multi_c1)
        df20 = pd.DataFrame([[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10]], columns=multi_c2)
        pd.testing.assert_frame_equal(
            df10.vbt.align_to(df20),
            pd.DataFrame(
                np.asarray([
                    [1, 2, 1, 2],
                    [4, 5, 4, 5],
                    [7, 8, 7, 8]
                ]),
                index=pd.RangeIndex(start=0, stop=3, step=1),
                columns=multi_c2
            )
        )

    def test_broadcast(self):
        a, b = pd.Series.vbt.broadcast(sr2, 10)
        b_target = pd.Series(np.full(sr2.shape, 10), index=sr2.index, name=sr2.name)
        pd.testing.assert_series_equal(a, sr2)
        pd.testing.assert_series_equal(b, b_target)
        a, b = sr2.vbt.broadcast(10)
        pd.testing.assert_series_equal(a, sr2)
        pd.testing.assert_series_equal(b, b_target)

    def test_broadcast_to(self):
        pd.testing.assert_frame_equal(sr2.vbt.broadcast_to(df2), df2)
        pd.testing.assert_frame_equal(sr2.vbt.broadcast_to(df2.vbt), df2)

    def test_apply(self):
        pd.testing.assert_series_equal(sr2.vbt.apply(apply_func=lambda x: x ** 2), sr2 ** 2)
        pd.testing.assert_series_equal(sr2.vbt.apply(apply_func=lambda x: x ** 2, to_2d=True), sr2 ** 2)
        pd.testing.assert_frame_equal(df4.vbt.apply(apply_func=lambda x: x ** 2), df4 ** 2)

    def test_concat(self):
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.concat(pd.Series([1, 2, 3]), pd.Series([1, 2, 3])),
            pd.DataFrame({0: pd.Series([1, 2, 3]), 1: pd.Series([1, 2, 3])})
        )
        target = pd.DataFrame(
            np.array([
                [1, 1, 1, 10, 10, 10, 1, 2, 3],
                [2, 2, 2, 10, 10, 10, 4, 5, 6],
                [3, 3, 3, 10, 10, 10, 7, 8, 9]
            ]),
            index=pd.MultiIndex.from_tuples([
                ('x2', 'x6'),
                ('y2', 'y6'),
                ('z2', 'z6')
            ], names=['i2', 'i6']),
            columns=pd.MultiIndex.from_tuples([
                ('a', 'a6'),
                ('a', 'b6'),
                ('a', 'c6'),
                ('b', 'a6'),
                ('b', 'b6'),
                ('b', 'c6'),
                ('c', 'a6'),
                ('c', 'b6'),
                ('c', 'c6')
            ], names=[None, 'c6'])
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.concat(sr2, 10, df4, keys=['a', 'b', 'c']),
            target
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.concat(10, df4, keys=['a', 'b', 'c']),
            target
        )

    def test_apply_and_concat(self):
        def apply_func(i, x, y, c, d=1):
            return x + y[i] + c + d

        @njit
        def apply_func_nb(i, x, y, c, d):
            return x + y[i] + c + d

        target = pd.DataFrame(
            np.array([
                [112, 113, 114],
                [113, 114, 115],
                [114, 115, 116]
            ]),
            index=pd.Index(['x2', 'y2', 'z2'], dtype='object', name='i2'),
            columns=pd.Index(['a', 'b', 'c'], dtype='object')
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.apply_and_concat(
                3, np.array([1, 2, 3]), 10, apply_func=apply_func, d=100,
                keys=['a', 'b', 'c']
            ),
            target
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.apply_and_concat(
                3, np.array([1, 2, 3]), 10, 100, apply_func=apply_func_nb, numba_loop=True,
                keys=['a', 'b', 'c']
            ),
            target
        )
        if ray_available:
            with pytest.raises(Exception):
                sr2.vbt.apply_and_concat(
                    3, np.array([1, 2, 3]), 10, 100, apply_func=apply_func_nb, numba_loop=True, use_ray=True,
                    keys=['a', 'b', 'c']
                )
            pd.testing.assert_frame_equal(
                sr2.vbt.apply_and_concat(
                    3, np.array([1, 2, 3]), 10, apply_func=apply_func, d=100,
                    keys=['a', 'b', 'c'], use_ray=True
                ),
                target
            )
        pd.testing.assert_frame_equal(
            sr2.vbt.apply_and_concat(
                3, np.array([1, 2, 3]), 10, apply_func=apply_func, d=100
            ),
            pd.DataFrame(
                target.values,
                index=target.index,
                columns=pd.Index([0, 1, 2], dtype='int64', name='apply_idx')
            )
        )

        def apply_func2(i, x, y, c, d=1):
            return x + y + c + d

        pd.testing.assert_frame_equal(
            sr2.vbt.apply_and_concat(
                3, np.array([[1], [2], [3]]), 10, apply_func=apply_func2, d=100,
                keys=['a', 'b', 'c'],
                to_2d=True  # otherwise (3, 1) + (1, 3) = (3, 3) != (3, 1) -> error
            ),
            pd.DataFrame(
                np.array([
                    [112, 112, 112],
                    [114, 114, 114],
                    [116, 116, 116]
                ]),
                index=target.index,
                columns=target.columns
            )
        )
        target2 = pd.DataFrame(
            np.array([
                [112, 113, 114],
                [113, 114, 115],
                [114, 115, 116]
            ]),
            index=pd.Index(['x4', 'y4', 'z4'], dtype='object', name='i4'),
            columns=pd.MultiIndex.from_tuples([
                ('a', 'a4'),
                ('b', 'a4'),
                ('c', 'a4')
            ], names=[None, 'c4'])
        )
        pd.testing.assert_frame_equal(
            df2.vbt.apply_and_concat(
                3, np.array([1, 2, 3]), 10, apply_func=apply_func, d=100,
                keys=['a', 'b', 'c']
            ),
            target2
        )
        pd.testing.assert_frame_equal(
            df2.vbt.apply_and_concat(
                3, np.array([1, 2, 3]), 10, 100, apply_func=apply_func_nb, numba_loop=True,
                keys=['a', 'b', 'c']
            ),
            target2
        )
        if ray_available:
            pd.testing.assert_frame_equal(
                df2.vbt.apply_and_concat(
                    3, np.array([1, 2, 3]), 10, apply_func=apply_func, d=100,
                    keys=['a', 'b', 'c'], use_ray=True
                ),
                target2
            )

    def test_combine(self):
        def combine_func(x, y, a, b=1):
            return x + y + a + b

        @njit
        def combine_func_nb(x, y, a, b):
            return x + y + a + b

        pd.testing.assert_series_equal(
            sr2.vbt.combine(10, 100, b=1000, combine_func=combine_func),
            pd.Series(
                np.array([1111, 1112, 1113]),
                index=pd.Index(['x2', 'y2', 'z2'], dtype='object', name='i2'),
                name=sr2.name
            )
        )
        pd.testing.assert_series_equal(
            sr2.vbt.combine(10, 100, 1000, combine_func=combine_func_nb),
            pd.Series(
                np.array([1111, 1112, 1113]),
                index=pd.Index(['x2', 'y2', 'z2'], dtype='object', name='i2'),
                name=sr2.name
            )
        )

        @njit
        def combine_func2_nb(x, y):
            return x + y + np.array([[1], [2], [3]])

        pd.testing.assert_series_equal(
            sr2.vbt.combine(10, combine_func=combine_func2_nb, to_2d=True),
            pd.Series(
                np.array([12, 14, 16]),
                index=pd.Index(['x2', 'y2', 'z2'], dtype='object', name='i2'),
                name='a2'
            )
        )

        @njit
        def combine_func3_nb(x, y):
            return x + y

        pd.testing.assert_frame_equal(
            df4.vbt.combine(sr2, combine_func=combine_func3_nb),
            pd.DataFrame(
                np.array([
                    [2, 3, 4],
                    [6, 7, 8],
                    [10, 11, 12]
                ]),
                index=pd.MultiIndex.from_tuples([
                    ('x6', 'x2'),
                    ('y6', 'y2'),
                    ('z6', 'z2')
                ], names=['i6', 'i2']),
                columns=pd.Index(['a6', 'b6', 'c6'], dtype='object', name='c6')
            )
        )

        target = pd.DataFrame(
            np.array([
                [232, 233, 234],
                [236, 237, 238],
                [240, 241, 242]
            ]),
            index=pd.MultiIndex.from_tuples([
                ('x2', 'x6'),
                ('y2', 'y6'),
                ('z2', 'z6')
            ], names=['i2', 'i6']),
            columns=pd.Index(['a6', 'b6', 'c6'], dtype='object', name='c6')
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.combine(
                [10, df4], 10, b=100,
                combine_func=combine_func
            ),
            target
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.combine(
                [10, df4], 10, 100,
                combine_func=combine_func_nb, numba_loop=True
            ),
            target
        )
        if ray_available:
            with pytest.raises(Exception):
                sr2.vbt.combine(
                    [10, df4], 10, 100,
                    combine_func=combine_func_nb, numba_loop=True, use_ray=True
                )
        pd.testing.assert_frame_equal(
            df4.vbt.combine(
                [10, sr2], 10, b=100,
                combine_func=combine_func
            ),
            pd.DataFrame(
                target.values,
                index=pd.MultiIndex.from_tuples([
                    ('x6', 'x2'),
                    ('y6', 'y2'),
                    ('z6', 'z2')
                ], names=['i6', 'i2']),
                columns=target.columns
            )
        )
        target2 = pd.DataFrame(
            np.array([
                [121, 121, 121, 112, 113, 114],
                [122, 122, 122, 116, 117, 118],
                [123, 123, 123, 120, 121, 122]
            ]),
            index=pd.MultiIndex.from_tuples([
                ('x2', 'x6'),
                ('y2', 'y6'),
                ('z2', 'z6')
            ], names=['i2', 'i6']),
            columns=pd.MultiIndex.from_tuples([
                (0, 'a6'),
                (0, 'b6'),
                (0, 'c6'),
                (1, 'a6'),
                (1, 'b6'),
                (1, 'c6')
            ], names=['combine_idx', 'c6'])
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.combine(
                [10, df4], 10, b=100,
                combine_func=combine_func,
                concat=True
            ),
            target2
        )
        pd.testing.assert_frame_equal(
            sr2.vbt.combine(
                [10, df4], 10, 100,
                combine_func=combine_func_nb, numba_loop=True,
                concat=True
            ),
            target2
        )
        if ray_available:
            pd.testing.assert_frame_equal(
                sr2.vbt.combine(
                    [10, df4], 10, b=100,
                    combine_func=combine_func,
                    concat=True,
                    use_ray=True
                ),
                target2
            )
        pd.testing.assert_frame_equal(
            sr2.vbt.combine(
                [10, df4], 10, b=100,
                combine_func=lambda x, y, a, b=1: x + y + a + b,
                concat=True,
                keys=['a', 'b']
            ),
            pd.DataFrame(
                target2.values,
                index=target2.index,
                columns=pd.MultiIndex.from_tuples([
                    ('a', 'a6'),
                    ('a', 'b6'),
                    ('a', 'c6'),
                    ('b', 'a6'),
                    ('b', 'b6'),
                    ('b', 'c6')
                ], names=[None, 'c6'])
            )
        )
