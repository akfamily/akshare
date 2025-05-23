from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from numba import njit

import vectorbt as vbt
from tests.utils import record_arrays_close
from vectorbt.generic.enums import range_dt, drawdown_dt
from vectorbt.portfolio.enums import order_dt, trade_dt, log_dt

day_dt = np.timedelta64(86400000000000)

example_dt = np.dtype([
    ('id', np.int64),
    ('col', np.int64),
    ('idx', np.int64),
    ('some_field1', np.float64),
    ('some_field2', np.float64)
], align=True)

records_arr = np.asarray([
    (0, 0, 0, 10, 21),
    (1, 0, 1, 11, 20),
    (2, 0, 2, 12, 19),
    (3, 1, 0, 13, 18),
    (4, 1, 1, 14, 17),
    (5, 1, 2, 13, 18),
    (6, 2, 0, 12, 19),
    (7, 2, 1, 11, 20),
    (8, 2, 2, 10, 21)
], dtype=example_dt)
records_nosort_arr = np.concatenate((
    records_arr[0::3],
    records_arr[1::3],
    records_arr[2::3]
))

group_by = pd.Index(['g1', 'g1', 'g2', 'g2'])

wrapper = vbt.ArrayWrapper(
    index=['x', 'y', 'z'],
    columns=['a', 'b', 'c', 'd'],
    ndim=2,
    freq='1 days'
)
wrapper_grouped = wrapper.replace(group_by=group_by)

records = vbt.records.Records(wrapper, records_arr)
records_grouped = vbt.records.Records(wrapper_grouped, records_arr)
records_nosort = records.replace(records_arr=records_nosort_arr)
records_nosort_grouped = vbt.records.Records(wrapper_grouped, records_nosort_arr)


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []


def teardown_module():
    vbt.settings.reset()


# ############# col_mapper.py ############# #


class TestColumnMapper:
    def test_col_arr(self):
        np.testing.assert_array_equal(
            records['a'].col_mapper.col_arr,
            np.array([0, 0, 0])
        )
        np.testing.assert_array_equal(
            records.col_mapper.col_arr,
            np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
        )

    def test_get_col_arr(self):
        np.testing.assert_array_equal(
            records.col_mapper.get_col_arr(),
            records.col_mapper.col_arr
        )
        np.testing.assert_array_equal(
            records_grouped['g1'].col_mapper.get_col_arr(),
            np.array([0, 0, 0, 0, 0, 0])
        )
        np.testing.assert_array_equal(
            records_grouped.col_mapper.get_col_arr(),
            np.array([0, 0, 0, 0, 0, 0, 1, 1, 1])
        )

    def test_col_range(self):
        np.testing.assert_array_equal(
            records['a'].col_mapper.col_range,
            np.array([
                [0, 3]
            ])
        )
        np.testing.assert_array_equal(
            records.col_mapper.col_range,
            np.array([
                [0, 3],
                [3, 6],
                [6, 9],
                [-1, -1]
            ])
        )

    def test_get_col_range(self):
        np.testing.assert_array_equal(
            records.col_mapper.get_col_range(),
            np.array([
                [0, 3],
                [3, 6],
                [6, 9],
                [-1, -1]
            ])
        )
        np.testing.assert_array_equal(
            records_grouped['g1'].col_mapper.get_col_range(),
            np.array([[0, 6]])
        )
        np.testing.assert_array_equal(
            records_grouped.col_mapper.get_col_range(),
            np.array([[0, 6], [6, 9]])
        )

    def test_col_map(self):
        np.testing.assert_array_equal(
            records['a'].col_mapper.col_map[0],
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            records['a'].col_mapper.col_map[1],
            np.array([3])
        )
        np.testing.assert_array_equal(
            records.col_mapper.col_map[0],
            np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        )
        np.testing.assert_array_equal(
            records.col_mapper.col_map[1],
            np.array([3, 3, 3, 0])
        )

    def test_get_col_map(self):
        np.testing.assert_array_equal(
            records.col_mapper.get_col_map()[0],
            records.col_mapper.col_map[0]
        )
        np.testing.assert_array_equal(
            records.col_mapper.get_col_map()[1],
            records.col_mapper.col_map[1]
        )
        np.testing.assert_array_equal(
            records_grouped['g1'].col_mapper.get_col_map()[0],
            np.array([0, 1, 2, 3, 4, 5])
        )
        np.testing.assert_array_equal(
            records_grouped['g1'].col_mapper.get_col_map()[1],
            np.array([6])
        )
        np.testing.assert_array_equal(
            records_grouped.col_mapper.get_col_map()[0],
            np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        )
        np.testing.assert_array_equal(
            records_grouped.col_mapper.get_col_map()[1],
            np.array([6, 3])
        )

    def test_is_sorted(self):
        assert records.col_mapper.is_sorted()
        assert not records_nosort.col_mapper.is_sorted()


# ############# mapped_array.py ############# #

mapped_array = records.map_field('some_field1')
mapped_array_grouped = records_grouped.map_field('some_field1')
mapped_array_nosort = records_nosort.map_field('some_field1')
mapped_array_nosort_grouped = records_nosort_grouped.map_field('some_field1')
mapping = {x: 'test_' + str(x) for x in pd.unique(mapped_array.values)}
mp_mapped_array = mapped_array.replace(mapping=mapping)
mp_mapped_array_grouped = mapped_array_grouped.replace(mapping=mapping)


class TestMappedArray:
    def test_config(self, tmp_path):
        assert vbt.MappedArray.loads(mapped_array.dumps()) == mapped_array
        mapped_array.save(tmp_path / 'mapped_array')
        assert vbt.MappedArray.load(tmp_path / 'mapped_array') == mapped_array

    def test_mapped_arr(self):
        np.testing.assert_array_equal(
            mapped_array['a'].values,
            np.array([10., 11., 12.])
        )
        np.testing.assert_array_equal(
            mapped_array.values,
            np.array([10., 11., 12., 13., 14., 13., 12., 11., 10.])
        )

    def test_id_arr(self):
        np.testing.assert_array_equal(
            mapped_array['a'].id_arr,
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            mapped_array.id_arr,
            np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        )

    def test_col_arr(self):
        np.testing.assert_array_equal(
            mapped_array['a'].col_arr,
            np.array([0, 0, 0])
        )
        np.testing.assert_array_equal(
            mapped_array.col_arr,
            np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
        )

    def test_idx_arr(self):
        np.testing.assert_array_equal(
            mapped_array['a'].idx_arr,
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            mapped_array.idx_arr,
            np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
        )

    def test_is_sorted(self):
        assert mapped_array.is_sorted()
        assert mapped_array.is_sorted(incl_id=True)
        assert not mapped_array_nosort.is_sorted()
        assert not mapped_array_nosort.is_sorted(incl_id=True)

    def test_sort(self):
        assert mapped_array.sort().is_sorted()
        assert mapped_array.sort().is_sorted(incl_id=True)
        assert mapped_array.sort(incl_id=True).is_sorted(incl_id=True)
        assert mapped_array_nosort.sort().is_sorted()
        assert mapped_array_nosort.sort().is_sorted(incl_id=True)
        assert mapped_array_nosort.sort(incl_id=True).is_sorted(incl_id=True)

    def test_apply_mask(self):
        mask_a = mapped_array['a'].values >= mapped_array['a'].values.mean()
        np.testing.assert_array_equal(
            mapped_array['a'].apply_mask(mask_a).id_arr,
            np.array([1, 2])
        )
        mask = mapped_array.values >= mapped_array.values.mean()
        filtered = mapped_array.apply_mask(mask)
        np.testing.assert_array_equal(
            filtered.id_arr,
            np.array([2, 3, 4, 5, 6])
        )
        np.testing.assert_array_equal(filtered.col_arr, mapped_array.col_arr[mask])
        np.testing.assert_array_equal(filtered.idx_arr, mapped_array.idx_arr[mask])
        assert mapped_array_grouped.apply_mask(mask).wrapper == mapped_array_grouped.wrapper
        assert mapped_array_grouped.apply_mask(mask, group_by=False).wrapper.grouper.group_by is None

    def test_map_to_mask(self):
        @njit
        def every_2_nb(inout, idxs, col, mapped_arr):
            inout[idxs[::2]] = True

        np.testing.assert_array_equal(
            mapped_array.map_to_mask(every_2_nb),
            np.array([True, False, True, True, False, True, True, False, True])
        )

    def test_top_n_mask(self):
        np.testing.assert_array_equal(
            mapped_array.top_n_mask(1),
            np.array([False, False, True, False, True, False, True, False, False])
        )

    def test_bottom_n_mask(self):
        np.testing.assert_array_equal(
            mapped_array.bottom_n_mask(1),
            np.array([True, False, False, True, False, False, False, False, True])
        )

    def test_top_n(self):
        np.testing.assert_array_equal(
            mapped_array.top_n(1).id_arr,
            np.array([2, 4, 6])
        )

    def test_bottom_n(self):
        np.testing.assert_array_equal(
            mapped_array.bottom_n(1).id_arr,
            np.array([0, 3, 8])
        )

    def test_to_pd(self):
        target = pd.DataFrame(
            np.array([
                [10., 13., 12., np.nan],
                [11., 14., 11., np.nan],
                [12., 13., 10., np.nan]
            ]),
            index=wrapper.index,
            columns=wrapper.columns
        )
        pd.testing.assert_series_equal(
            mapped_array['a'].to_pd(),
            target['a']
        )
        pd.testing.assert_frame_equal(
            mapped_array.to_pd(),
            target
        )
        pd.testing.assert_frame_equal(
            mapped_array.to_pd(fill_value=0.),
            target.fillna(0.)
        )
        mapped_array2 = vbt.MappedArray(
            wrapper,
            records_arr['some_field1'].tolist() + [1],
            records_arr['col'].tolist() + [2],
            idx_arr=records_arr['idx'].tolist() + [2]
        )
        with pytest.raises(Exception):
            _ = mapped_array2.to_pd()
        pd.testing.assert_series_equal(
            mapped_array['a'].to_pd(ignore_index=True),
            pd.Series(np.array([10., 11., 12.]), name='a')
        )
        pd.testing.assert_frame_equal(
            mapped_array.to_pd(ignore_index=True),
            pd.DataFrame(
                np.array([
                    [10., 13., 12., np.nan],
                    [11., 14., 11., np.nan],
                    [12., 13., 10., np.nan]
                ]),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.to_pd(fill_value=0, ignore_index=True),
            pd.DataFrame(
                np.array([
                    [10., 13., 12., 0.],
                    [11., 14., 11., 0.],
                    [12., 13., 10., 0.]
                ]),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array_grouped.to_pd(ignore_index=True),
            pd.DataFrame(
                np.array([
                    [10., 12.],
                    [11., 11.],
                    [12., 10.],
                    [13., np.nan],
                    [14., np.nan],
                    [13., np.nan],
                ]),
                columns=pd.Index(['g1', 'g2'], dtype='object')
            )
        )

    def test_apply(self):
        @njit
        def cumsum_apply_nb(idxs, col, a):
            return np.cumsum(a)

        np.testing.assert_array_equal(
            mapped_array['a'].apply(cumsum_apply_nb).values,
            np.array([10., 21., 33.])
        )
        np.testing.assert_array_equal(
            mapped_array.apply(cumsum_apply_nb).values,
            np.array([10., 21., 33., 13., 27., 40., 12., 23., 33.])
        )
        np.testing.assert_array_equal(
            mapped_array_grouped.apply(cumsum_apply_nb, apply_per_group=False).values,
            np.array([10., 21., 33., 13., 27., 40., 12., 23., 33.])
        )
        np.testing.assert_array_equal(
            mapped_array_grouped.apply(cumsum_apply_nb, apply_per_group=True).values,
            np.array([10., 21., 33., 46., 60., 73., 12., 23., 33.])
        )
        assert mapped_array_grouped.apply(cumsum_apply_nb).wrapper == \
               mapped_array.apply(cumsum_apply_nb, group_by=group_by).wrapper
        assert mapped_array.apply(cumsum_apply_nb, group_by=False).wrapper.grouper.group_by is None

    def test_reduce(self):
        @njit
        def mean_reduce_nb(col, a):
            return np.mean(a)

        assert mapped_array['a'].reduce(mean_reduce_nb) == 11.
        pd.testing.assert_series_equal(
            mapped_array.reduce(mean_reduce_nb),
            pd.Series(np.array([11., 13.333333333333334, 11., np.nan]), index=wrapper.columns).rename('reduce')
        )
        pd.testing.assert_series_equal(
            mapped_array.reduce(mean_reduce_nb, fill_value=0.),
            pd.Series(np.array([11., 13.333333333333334, 11., 0.]), index=wrapper.columns).rename('reduce')
        )
        pd.testing.assert_series_equal(
            mapped_array.reduce(mean_reduce_nb, wrap_kwargs=dict(to_timedelta=True)),
            pd.Series(np.array([11., 13.333333333333334, 11., np.nan]), index=wrapper.columns).rename('reduce') * day_dt
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.reduce(mean_reduce_nb),
            pd.Series([12.166666666666666, 11.0], index=pd.Index(['g1', 'g2'], dtype='object')).rename('reduce')
        )
        assert mapped_array_grouped['g1'].reduce(mean_reduce_nb) == 12.166666666666666
        pd.testing.assert_series_equal(
            mapped_array_grouped[['g1']].reduce(mean_reduce_nb),
            pd.Series([12.166666666666666], index=pd.Index(['g1'], dtype='object')).rename('reduce')
        )
        pd.testing.assert_series_equal(
            mapped_array.reduce(mean_reduce_nb),
            mapped_array_grouped.reduce(mean_reduce_nb, group_by=False)
        )
        pd.testing.assert_series_equal(
            mapped_array.reduce(mean_reduce_nb, group_by=group_by),
            mapped_array_grouped.reduce(mean_reduce_nb)
        )

    def test_reduce_to_idx(self):
        @njit
        def argmin_reduce_nb(col, a):
            return np.argmin(a)

        assert mapped_array['a'].reduce(argmin_reduce_nb, returns_idx=True) == 'x'
        pd.testing.assert_series_equal(
            mapped_array.reduce(argmin_reduce_nb, returns_idx=True),
            pd.Series(np.array(['x', 'x', 'z', np.nan], dtype=object), index=wrapper.columns).rename('reduce')
        )
        pd.testing.assert_series_equal(
            mapped_array.reduce(argmin_reduce_nb, returns_idx=True, to_index=False),
            pd.Series(np.array([0, 0, 2, -1], dtype=int), index=wrapper.columns).rename('reduce')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.reduce(argmin_reduce_nb, returns_idx=True, to_index=False),
            pd.Series(np.array([0, 2], dtype=int), index=pd.Index(['g1', 'g2'], dtype='object')).rename('reduce')
        )

    def test_reduce_to_array(self):
        @njit
        def min_max_reduce_nb(col, a):
            return np.array([np.min(a), np.max(a)])

        pd.testing.assert_series_equal(
            mapped_array['a'].reduce(min_max_reduce_nb, returns_array=True,
                                     wrap_kwargs=dict(name_or_index=['min', 'max'])),
            pd.Series([10., 12.], index=pd.Index(['min', 'max'], dtype='object'), name='a')
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(min_max_reduce_nb, returns_array=True, wrap_kwargs=dict(name_or_index=['min', 'max'])),
            pd.DataFrame(
                np.array([
                    [10., 13., 10., np.nan],
                    [12., 14., 12., np.nan]
                ]),
                index=pd.Index(['min', 'max'], dtype='object'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(min_max_reduce_nb, returns_array=True, fill_value=0.),
            pd.DataFrame(
                np.array([
                    [10., 13., 10., 0.],
                    [12., 14., 12., 0.]
                ]),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(min_max_reduce_nb, returns_array=True, wrap_kwargs=dict(to_timedelta=True)),
            pd.DataFrame(
                np.array([
                    [10., 13., 10., np.nan],
                    [12., 14., 12., np.nan]
                ]),
                columns=wrapper.columns
            ) * day_dt
        )
        pd.testing.assert_frame_equal(
            mapped_array_grouped.reduce(min_max_reduce_nb, returns_array=True),
            pd.DataFrame(
                np.array([
                    [10., 10.],
                    [14., 12.]
                ]),
                columns=pd.Index(['g1', 'g2'], dtype='object')
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(min_max_reduce_nb, returns_array=True),
            mapped_array_grouped.reduce(min_max_reduce_nb, returns_array=True, group_by=False)
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(min_max_reduce_nb, returns_array=True, group_by=group_by),
            mapped_array_grouped.reduce(min_max_reduce_nb, returns_array=True)
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped['g1'].reduce(min_max_reduce_nb, returns_array=True),
            pd.Series([10., 14.], name='g1')
        )
        pd.testing.assert_frame_equal(
            mapped_array_grouped[['g1']].reduce(min_max_reduce_nb, returns_array=True),
            pd.DataFrame([[10.], [14.]], columns=pd.Index(['g1'], dtype='object'))
        )

    def test_reduce_to_idx_array(self):
        @njit
        def idxmin_idxmax_reduce_nb(col, a):
            return np.array([np.argmin(a), np.argmax(a)])

        pd.testing.assert_series_equal(
            mapped_array['a'].reduce(
                idxmin_idxmax_reduce_nb,
                returns_array=True,
                returns_idx=True,
                wrap_kwargs=dict(name_or_index=['min', 'max'])
            ),
            pd.Series(
                np.array(['x', 'z'], dtype=object),
                index=pd.Index(['min', 'max'], dtype='object'),
                name='a'
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(
                idxmin_idxmax_reduce_nb,
                returns_array=True,
                returns_idx=True,
                wrap_kwargs=dict(name_or_index=['min', 'max'])
            ),
            pd.DataFrame(
                {
                    'a': ['x', 'z'],
                    'b': ['x', 'y'],
                    'c': ['z', 'x'],
                    'd': [np.nan, np.nan]
                },
                index=pd.Index(['min', 'max'], dtype='object')
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.reduce(
                idxmin_idxmax_reduce_nb,
                returns_array=True,
                returns_idx=True,
                to_index=False
            ),
            pd.DataFrame(
                np.array([
                    [0, 0, 2, -1],
                    [2, 1, 0, -1]
                ]),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array_grouped.reduce(
                idxmin_idxmax_reduce_nb,
                returns_array=True,
                returns_idx=True,
                to_index=False
            ),
            pd.DataFrame(
                np.array([
                    [0, 2],
                    [1, 0]
                ]),
                columns=pd.Index(['g1', 'g2'], dtype='object')
            )
        )

    def test_nth(self):
        assert mapped_array['a'].nth(0) == 10.
        pd.testing.assert_series_equal(
            mapped_array.nth(0),
            pd.Series(np.array([10., 13., 12., np.nan]), index=wrapper.columns).rename('nth')
        )
        assert mapped_array['a'].nth(-1) == 12.
        pd.testing.assert_series_equal(
            mapped_array.nth(-1),
            pd.Series(np.array([12., 13., 10., np.nan]), index=wrapper.columns).rename('nth')
        )
        with pytest.raises(Exception):
            _ = mapped_array.nth(10)
        pd.testing.assert_series_equal(
            mapped_array_grouped.nth(0),
            pd.Series(np.array([10., 12.]), index=pd.Index(['g1', 'g2'], dtype='object')).rename('nth')
        )

    def test_nth_index(self):
        assert mapped_array['a'].nth(0) == 10.
        pd.testing.assert_series_equal(
            mapped_array.nth_index(0),
            pd.Series(
                np.array(['x', 'x', 'x', np.nan], dtype='object'),
                index=wrapper.columns
            ).rename('nth_index')
        )
        assert mapped_array['a'].nth(-1) == 12.
        pd.testing.assert_series_equal(
            mapped_array.nth_index(-1),
            pd.Series(
                np.array(['z', 'z', 'z', np.nan], dtype='object'),
                index=wrapper.columns
            ).rename('nth_index')
        )
        with pytest.raises(Exception):
            _ = mapped_array.nth_index(10)
        pd.testing.assert_series_equal(
            mapped_array_grouped.nth_index(0),
            pd.Series(
                np.array(['x', 'x'], dtype='object'),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('nth_index')
        )

    def test_min(self):
        assert mapped_array['a'].min() == mapped_array['a'].to_pd().min()
        pd.testing.assert_series_equal(
            mapped_array.min(),
            mapped_array.to_pd().min().rename('min')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.min(),
            pd.Series([10., 10.], index=pd.Index(['g1', 'g2'], dtype='object')).rename('min')
        )

    def test_max(self):
        assert mapped_array['a'].max() == mapped_array['a'].to_pd().max()
        pd.testing.assert_series_equal(
            mapped_array.max(),
            mapped_array.to_pd().max().rename('max')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.max(),
            pd.Series([14., 12.], index=pd.Index(['g1', 'g2'], dtype='object')).rename('max')
        )

    def test_mean(self):
        assert mapped_array['a'].mean() == mapped_array['a'].to_pd().mean()
        pd.testing.assert_series_equal(
            mapped_array.mean(),
            mapped_array.to_pd().mean().rename('mean')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.mean(),
            pd.Series([12.166667, 11.], index=pd.Index(['g1', 'g2'], dtype='object')).rename('mean')
        )

    def test_median(self):
        assert mapped_array['a'].median() == mapped_array['a'].to_pd().median()
        pd.testing.assert_series_equal(
            mapped_array.median(),
            mapped_array.to_pd().median().rename('median')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.median(),
            pd.Series([12.5, 11.], index=pd.Index(['g1', 'g2'], dtype='object')).rename('median')
        )

    def test_std(self):
        assert mapped_array['a'].std() == mapped_array['a'].to_pd().std()
        pd.testing.assert_series_equal(
            mapped_array.std(),
            mapped_array.to_pd().std().rename('std')
        )
        pd.testing.assert_series_equal(
            mapped_array.std(ddof=0),
            mapped_array.to_pd().std(ddof=0).rename('std')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.std(),
            pd.Series([1.4719601443879746, 1.0], index=pd.Index(['g1', 'g2'], dtype='object')).rename('std')
        )

    def test_sum(self):
        assert mapped_array['a'].sum() == mapped_array['a'].to_pd().sum()
        pd.testing.assert_series_equal(
            mapped_array.sum(),
            mapped_array.to_pd().sum().rename('sum')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.sum(),
            pd.Series([73.0, 33.0], index=pd.Index(['g1', 'g2'], dtype='object')).rename('sum')
        )

    def test_count(self):
        assert mapped_array['a'].count() == mapped_array['a'].to_pd().count()
        pd.testing.assert_series_equal(
            mapped_array.count(),
            mapped_array.to_pd().count().rename('count')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.count(),
            pd.Series([6, 3], index=pd.Index(['g1', 'g2'], dtype='object')).rename('count')
        )

    def test_idxmin(self):
        assert mapped_array['a'].idxmin() == mapped_array['a'].to_pd().idxmin()
        pd.testing.assert_series_equal(
            mapped_array.idxmin(),
            mapped_array.to_pd().idxmin().rename('idxmin')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.idxmin(),
            pd.Series(
                np.array(['x', 'z'], dtype=object),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('idxmin')
        )

    def test_idxmax(self):
        assert mapped_array['a'].idxmax() == mapped_array['a'].to_pd().idxmax()
        pd.testing.assert_series_equal(
            mapped_array.idxmax(),
            mapped_array.to_pd().idxmax().rename('idxmax')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped.idxmax(),
            pd.Series(
                np.array(['y', 'x'], dtype=object),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('idxmax')
        )

    def test_describe(self):
        pd.testing.assert_series_equal(
            mapped_array['a'].describe(),
            mapped_array['a'].to_pd().describe()
        )
        pd.testing.assert_frame_equal(
            mapped_array.describe(percentiles=None),
            mapped_array.to_pd().describe(percentiles=None)
        )
        pd.testing.assert_frame_equal(
            mapped_array.describe(percentiles=[]),
            mapped_array.to_pd().describe(percentiles=[])
        )
        pd.testing.assert_frame_equal(
            mapped_array.describe(percentiles=np.arange(0, 1, 0.1)),
            mapped_array.to_pd().describe(percentiles=np.arange(0, 1, 0.1))
        )
        pd.testing.assert_frame_equal(
            mapped_array_grouped.describe(),
            pd.DataFrame(
                np.array([
                    [6., 3.],
                    [12.16666667, 11.],
                    [1.47196014, 1.],
                    [10., 10.],
                    [11.25, 10.5],
                    [12.5, 11.],
                    [13., 11.5],
                    [14., 12.]
                ]),
                columns=pd.Index(['g1', 'g2'], dtype='object'),
                index=mapped_array.describe().index
            )
        )

    def test_value_counts(self):
        pd.testing.assert_series_equal(
            mapped_array['a'].value_counts(),
            pd.Series(
                np.array([1, 1, 1]),
                index=pd.Index([10.0, 11.0, 12.0], dtype='float64'),
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            mapped_array['a'].value_counts(mapping=mapping),
            pd.Series(
                np.array([1, 1, 1]),
                index=pd.Index(['test_10.0', 'test_11.0', 'test_12.0'], dtype='object'),
                name='a'
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array.value_counts(),
            pd.DataFrame(
                np.array([
                    [1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [0, 2, 0, 0],
                    [0, 1, 0, 0]
                ]),
                index=pd.Index([10.0, 11.0, 12.0, 13.0, 14.0], dtype='float64'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array_grouped.value_counts(),
            pd.DataFrame(
                np.array([
                    [1, 1],
                    [1, 1],
                    [1, 1],
                    [2, 0],
                    [1, 0]
                ]),
                index=pd.Index([10.0, 11.0, 12.0, 13.0, 14.0], dtype='float64'),
                columns=pd.Index(['g1', 'g2'], dtype='object')
            )
        )
        mapped_array2 = mapped_array.replace(mapped_arr=[4, 4, 3, 2, np.nan, 4, 3, 2, 1])
        pd.testing.assert_frame_equal(
            mapped_array2.value_counts(sort_uniques=False),
            pd.DataFrame(
                np.array([
                    [2, 1, 0, 0],
                    [1, 0, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0]
                ]),
                index=pd.Index([4.0, 3.0, 2.0, 1.0, None], dtype='float64'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array2.value_counts(sort_uniques=True),
            pd.DataFrame(
                np.array([
                    [0, 0, 1, 0],
                    [0, 1, 1, 0],
                    [1, 0, 1, 0],
                    [2, 1, 0, 0],
                    [0, 1, 0, 0]
                ]),
                index=pd.Index([1.0, 2.0, 3.0, 4.0, None], dtype='float64'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array2.value_counts(sort=True),
            pd.DataFrame(
                np.array([
                    [2, 1, 0, 0],
                    [0, 1, 1, 0],
                    [1, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0]
                ]),
                index=pd.Index([4.0, 2.0, 3.0, 1.0, np.nan], dtype='float64'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array2.value_counts(sort=True, ascending=True),
            pd.DataFrame(
                np.array([
                    [0, 0, 1, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [1, 0, 1, 0],
                    [2, 1, 0, 0]
                ]),
                index=pd.Index([1.0, np.nan, 2.0, 3.0, 4.0], dtype='float64'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array2.value_counts(sort=True, normalize=True),
            pd.DataFrame(
                np.array([
                    [0.2222222222222222, 0.1111111111111111, 0.0, 0.0],
                    [0.0, 0.1111111111111111, 0.1111111111111111, 0.0],
                    [0.1111111111111111, 0.0, 0.1111111111111111, 0.0],
                    [0.0, 0.0, 0.1111111111111111, 0.0],
                    [0.0, 0.1111111111111111, 0.0, 0.0]
                ]),
                index=pd.Index([4.0, 2.0, 3.0, 1.0, np.nan], dtype='float64'),
                columns=wrapper.columns
            )
        )
        pd.testing.assert_frame_equal(
            mapped_array2.value_counts(sort=True, normalize=True, dropna=True),
            pd.DataFrame(
                np.array([
                    [0.25, 0.125, 0.0, 0.0],
                    [0.0, 0.125, 0.125, 0.0],
                    [0.125, 0.0, 0.125, 0.0],
                    [0.0, 0.0, 0.125, 0.0]
                ]),
                index=pd.Index([4.0, 2.0, 3.0, 1.0], dtype='float64'),
                columns=wrapper.columns
            )
        )

    @pytest.mark.parametrize(
        "test_nosort",
        [False, True],
    )
    def test_indexing(self, test_nosort):
        if test_nosort:
            ma = mapped_array_nosort
            ma_grouped = mapped_array_nosort_grouped
        else:
            ma = mapped_array
            ma_grouped = mapped_array_grouped
        np.testing.assert_array_equal(
            ma['a'].id_arr,
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            ma['a'].col_arr,
            np.array([0, 0, 0])
        )
        pd.testing.assert_index_equal(
            ma['a'].wrapper.columns,
            pd.Index(['a'], dtype='object')
        )
        np.testing.assert_array_equal(
            ma['b'].id_arr,
            np.array([3, 4, 5])
        )
        np.testing.assert_array_equal(
            ma['b'].col_arr,
            np.array([0, 0, 0])
        )
        pd.testing.assert_index_equal(
            ma['b'].wrapper.columns,
            pd.Index(['b'], dtype='object')
        )
        np.testing.assert_array_equal(
            ma[['a', 'a']].id_arr,
            np.array([0, 1, 2, 0, 1, 2])
        )
        np.testing.assert_array_equal(
            ma[['a', 'a']].col_arr,
            np.array([0, 0, 0, 1, 1, 1])
        )
        pd.testing.assert_index_equal(
            ma[['a', 'a']].wrapper.columns,
            pd.Index(['a', 'a'], dtype='object')
        )
        np.testing.assert_array_equal(
            ma[['a', 'b']].id_arr,
            np.array([0, 1, 2, 3, 4, 5])
        )
        np.testing.assert_array_equal(
            ma[['a', 'b']].col_arr,
            np.array([0, 0, 0, 1, 1, 1])
        )
        pd.testing.assert_index_equal(
            ma[['a', 'b']].wrapper.columns,
            pd.Index(['a', 'b'], dtype='object')
        )
        with pytest.raises(Exception):
            _ = ma.iloc[::2, :]  # changing time not supported
        pd.testing.assert_index_equal(
            ma_grouped['g1'].wrapper.columns,
            pd.Index(['a', 'b'], dtype='object')
        )
        assert ma_grouped['g1'].wrapper.ndim == 2
        assert ma_grouped['g1'].wrapper.grouped_ndim == 1
        pd.testing.assert_index_equal(
            ma_grouped['g1'].wrapper.grouper.group_by,
            pd.Index(['g1', 'g1'], dtype='object')
        )
        pd.testing.assert_index_equal(
            ma_grouped['g2'].wrapper.columns,
            pd.Index(['c', 'd'], dtype='object')
        )
        assert ma_grouped['g2'].wrapper.ndim == 2
        assert ma_grouped['g2'].wrapper.grouped_ndim == 1
        pd.testing.assert_index_equal(
            ma_grouped['g2'].wrapper.grouper.group_by,
            pd.Index(['g2', 'g2'], dtype='object')
        )
        pd.testing.assert_index_equal(
            ma_grouped[['g1']].wrapper.columns,
            pd.Index(['a', 'b'], dtype='object')
        )
        assert ma_grouped[['g1']].wrapper.ndim == 2
        assert ma_grouped[['g1']].wrapper.grouped_ndim == 2
        pd.testing.assert_index_equal(
            ma_grouped[['g1']].wrapper.grouper.group_by,
            pd.Index(['g1', 'g1'], dtype='object')
        )
        pd.testing.assert_index_equal(
            ma_grouped[['g1', 'g2']].wrapper.columns,
            pd.Index(['a', 'b', 'c', 'd'], dtype='object')
        )
        assert ma_grouped[['g1', 'g2']].wrapper.ndim == 2
        assert ma_grouped[['g1', 'g2']].wrapper.grouped_ndim == 2
        pd.testing.assert_index_equal(
            ma_grouped[['g1', 'g2']].wrapper.grouper.group_by,
            pd.Index(['g1', 'g1', 'g2', 'g2'], dtype='object')
        )

    def test_magic(self):
        a = vbt.MappedArray(
            wrapper,
            records_arr['some_field1'],
            records_arr['col'],
            id_arr=records_arr['id'],
            idx_arr=records_arr['idx']
        )
        a_inv = vbt.MappedArray(
            wrapper,
            records_arr['some_field1'][::-1],
            records_arr['col'][::-1],
            id_arr=records_arr['id'][::-1],
            idx_arr=records_arr['idx'][::-1]
        )
        b = records_arr['some_field2']
        a_bool = vbt.MappedArray(
            wrapper,
            records_arr['some_field1'] > np.mean(records_arr['some_field1']),
            records_arr['col'],
            id_arr=records_arr['id'],
            idx_arr=records_arr['idx']
        )
        b_bool = records_arr['some_field2'] > np.mean(records_arr['some_field2'])
        assert a ** a == a ** 2
        with pytest.raises(Exception):
            _ = a * a_inv

        # binary ops
        # comparison ops
        np.testing.assert_array_equal((a == b).values, a.values == b)
        np.testing.assert_array_equal((a != b).values, a.values != b)
        np.testing.assert_array_equal((a < b).values, a.values < b)
        np.testing.assert_array_equal((a > b).values, a.values > b)
        np.testing.assert_array_equal((a <= b).values, a.values <= b)
        np.testing.assert_array_equal((a >= b).values, a.values >= b)
        # arithmetic ops
        np.testing.assert_array_equal((a + b).values, a.values + b)
        np.testing.assert_array_equal((a - b).values, a.values - b)
        np.testing.assert_array_equal((a * b).values, a.values * b)
        np.testing.assert_array_equal((a ** b).values, a.values ** b)
        np.testing.assert_array_equal((a % b).values, a.values % b)
        np.testing.assert_array_equal((a // b).values, a.values // b)
        np.testing.assert_array_equal((a / b).values, a.values / b)
        # __r*__ is only called if the left object does not have an __*__ method
        np.testing.assert_array_equal((10 + a).values, 10 + a.values)
        np.testing.assert_array_equal((10 - a).values, 10 - a.values)
        np.testing.assert_array_equal((10 * a).values, 10 * a.values)
        np.testing.assert_array_equal((10 ** a).values, 10 ** a.values)
        np.testing.assert_array_equal((10 % a).values, 10 % a.values)
        np.testing.assert_array_equal((10 // a).values, 10 // a.values)
        np.testing.assert_array_equal((10 / a).values, 10 / a.values)
        # mask ops
        np.testing.assert_array_equal((a_bool & b_bool).values, a_bool.values & b_bool)
        np.testing.assert_array_equal((a_bool | b_bool).values, a_bool.values | b_bool)
        np.testing.assert_array_equal((a_bool ^ b_bool).values, a_bool.values ^ b_bool)
        np.testing.assert_array_equal((True & a_bool).values, True & a_bool.values)
        np.testing.assert_array_equal((True | a_bool).values, True | a_bool.values)
        np.testing.assert_array_equal((True ^ a_bool).values, True ^ a_bool.values)
        # unary ops
        np.testing.assert_array_equal((-a).values, -a.values)
        np.testing.assert_array_equal((+a).values, +a.values)
        np.testing.assert_array_equal((abs(-a)).values, abs((-a.values)))

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Count', 'Mean', 'Std', 'Min', 'Median', 'Max', 'Min Index', 'Max Index'
        ], dtype='object')
        pd.testing.assert_series_equal(
            mapped_array.stats(),
            pd.Series([
                'x', 'z', pd.Timedelta('3 days 00:00:00'),
                2.25, 11.777777777777779, 0.859116756396542, 11.0, 11.666666666666666, 12.666666666666666
            ],
                index=stats_index[:-2],
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            mapped_array.stats(column='a'),
            pd.Series([
                'x', 'z', pd.Timedelta('3 days 00:00:00'),
                3, 11.0, 1.0, 10.0, 11.0, 12.0, 'x', 'z'
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            mapped_array.stats(column='g1', group_by=group_by),
            pd.Series([
                'x', 'z', pd.Timedelta('3 days 00:00:00'),
                6, 12.166666666666666, 1.4719601443879746, 10.0, 12.5, 14.0, 'x', 'y'
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            mapped_array['c'].stats(),
            mapped_array.stats(column='c')
        )
        pd.testing.assert_series_equal(
            mapped_array['c'].stats(),
            mapped_array.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped['g2'].stats(),
            mapped_array_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            mapped_array_grouped['g2'].stats(),
            mapped_array.stats(column='g2', group_by=group_by)
        )
        stats_df = mapped_array.stats(agg_func=None)
        assert stats_df.shape == (4, 11)
        pd.testing.assert_index_equal(stats_df.index, mapped_array.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)

    def test_stats_mapping(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Count', 'Value Counts: test_10.0',
            'Value Counts: test_11.0', 'Value Counts: test_12.0',
            'Value Counts: test_13.0', 'Value Counts: test_14.0'
        ], dtype='object')
        pd.testing.assert_series_equal(
            mp_mapped_array.stats(),
            pd.Series([
                'x',
                'z',
                pd.Timedelta('3 days 00:00:00'),
                2.25, 0.5, 0.5, 0.5, 0.5, 0.25
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            mp_mapped_array.stats(column='a'),
            pd.Series([
                'x',
                'z',
                pd.Timedelta('3 days 00:00:00'),
                3, 1, 1, 1, 0, 0
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            mp_mapped_array.stats(column='g1', group_by=group_by),
            pd.Series([
                'x',
                'z',
                pd.Timedelta('3 days 00:00:00'),
                6, 1, 1, 1, 2, 1
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            mp_mapped_array.stats(),
            mapped_array.stats(settings=dict(mapping=mapping))
        )
        pd.testing.assert_series_equal(
            mp_mapped_array['c'].stats(settings=dict(incl_all_keys=True)),
            mp_mapped_array.stats(column='c')
        )
        pd.testing.assert_series_equal(
            mp_mapped_array['c'].stats(settings=dict(incl_all_keys=True)),
            mp_mapped_array.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            mp_mapped_array_grouped['g2'].stats(settings=dict(incl_all_keys=True)),
            mp_mapped_array_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            mp_mapped_array_grouped['g2'].stats(settings=dict(incl_all_keys=True)),
            mp_mapped_array.stats(column='g2', group_by=group_by)
        )
        stats_df = mp_mapped_array.stats(agg_func=None)
        assert stats_df.shape == (4, 9)
        pd.testing.assert_index_equal(stats_df.index, mp_mapped_array.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)


# ############# base.py ############# #

class TestRecords:
    def test_config(self, tmp_path):
        assert vbt.Records.loads(records['a'].dumps()) == records['a']
        assert vbt.Records.loads(records.dumps()) == records
        records.save(tmp_path / 'records')
        assert vbt.Records.load(tmp_path / 'records') == records

    def test_records(self):
        pd.testing.assert_frame_equal(
            records.records,
            pd.DataFrame.from_records(records_arr)
        )

    def test_recarray(self):
        np.testing.assert_array_equal(records['a'].recarray.some_field1, records['a'].values['some_field1'])
        np.testing.assert_array_equal(records.recarray.some_field1, records.values['some_field1'])

    def test_records_readable(self):
        pd.testing.assert_frame_equal(
            records.records_readable,
            pd.DataFrame([
                [0, 'a', 'x', 10.0, 21.0], [1, 'a', 'y', 11.0, 20.0], [2, 'a', 'z', 12.0, 19.0],
                [3, 'b', 'x', 13.0, 18.0], [4, 'b', 'y', 14.0, 17.0], [5, 'b', 'z', 13.0, 18.0],
                [6, 'c', 'x', 12.0, 19.0], [7, 'c', 'y', 11.0, 20.0], [8, 'c', 'z', 10.0, 21.0]
            ], columns=pd.Index(['Id', 'Column', 'Timestamp', 'some_field1', 'some_field2'], dtype='object'))
        )

    def test_is_sorted(self):
        assert records.is_sorted()
        assert records.is_sorted(incl_id=True)
        assert not records_nosort.is_sorted()
        assert not records_nosort.is_sorted(incl_id=True)

    def test_sort(self):
        assert records.sort().is_sorted()
        assert records.sort().is_sorted(incl_id=True)
        assert records.sort(incl_id=True).is_sorted(incl_id=True)
        assert records_nosort.sort().is_sorted()
        assert records_nosort.sort().is_sorted(incl_id=True)
        assert records_nosort.sort(incl_id=True).is_sorted(incl_id=True)

    def test_apply_mask(self):
        mask_a = records['a'].values['some_field1'] >= records['a'].values['some_field1'].mean()
        record_arrays_close(
            records['a'].apply_mask(mask_a).values,
            np.array([
                (1, 0, 1, 11., 20.), (2, 0, 2, 12., 19.)
            ], dtype=example_dt)
        )
        mask = records.values['some_field1'] >= records.values['some_field1'].mean()
        filtered = records.apply_mask(mask)
        record_arrays_close(
            filtered.values,
            np.array([
                (2, 0, 2, 12., 19.), (3, 1, 0, 13., 18.), (4, 1, 1, 14., 17.),
                (5, 1, 2, 13., 18.), (6, 2, 0, 12., 19.)
            ], dtype=example_dt)
        )
        assert records_grouped.apply_mask(mask).wrapper == records_grouped.wrapper

    def test_map_field(self):
        np.testing.assert_array_equal(
            records['a'].map_field('some_field1').values,
            np.array([10., 11., 12.])
        )
        np.testing.assert_array_equal(
            records.map_field('some_field1').values,
            np.array([10., 11., 12., 13., 14., 13., 12., 11., 10.])
        )
        assert records_grouped.map_field('some_field1').wrapper == \
               records.map_field('some_field1', group_by=group_by).wrapper
        assert records_grouped.map_field('some_field1', group_by=False).wrapper.grouper.group_by is None

    def test_map(self):
        @njit
        def map_func_nb(record):
            return record['some_field1'] + record['some_field2']

        np.testing.assert_array_equal(
            records['a'].map(map_func_nb).values,
            np.array([31., 31., 31.])
        )
        np.testing.assert_array_equal(
            records.map(map_func_nb).values,
            np.array([31., 31., 31., 31., 31., 31., 31., 31., 31.])
        )
        assert records_grouped.map(map_func_nb).wrapper == \
               records.map(map_func_nb, group_by=group_by).wrapper
        assert records_grouped.map(map_func_nb, group_by=False).wrapper.grouper.group_by is None

    def test_map_array(self):
        arr = records_arr['some_field1'] + records_arr['some_field2']
        np.testing.assert_array_equal(
            records['a'].map_array(arr[:3]).values,
            np.array([31., 31., 31.])
        )
        np.testing.assert_array_equal(
            records.map_array(arr).values,
            np.array([31., 31., 31., 31., 31., 31., 31., 31., 31.])
        )
        assert records_grouped.map_array(arr).wrapper == \
               records.map_array(arr, group_by=group_by).wrapper
        assert records_grouped.map_array(arr, group_by=False).wrapper.grouper.group_by is None

    def test_apply(self):
        @njit
        def cumsum_apply_nb(records):
            return np.cumsum(records['some_field1'])

        np.testing.assert_array_equal(
            records['a'].apply(cumsum_apply_nb).values,
            np.array([10., 21., 33.])
        )
        np.testing.assert_array_equal(
            records.apply(cumsum_apply_nb).values,
            np.array([10., 21., 33., 13., 27., 40., 12., 23., 33.])
        )
        np.testing.assert_array_equal(
            records_grouped.apply(cumsum_apply_nb, apply_per_group=False).values,
            np.array([10., 21., 33., 13., 27., 40., 12., 23., 33.])
        )
        np.testing.assert_array_equal(
            records_grouped.apply(cumsum_apply_nb, apply_per_group=True).values,
            np.array([10., 21., 33., 46., 60., 73., 12., 23., 33.])
        )
        assert records_grouped.apply(cumsum_apply_nb).wrapper == \
               records.apply(cumsum_apply_nb, group_by=group_by).wrapper
        assert records_grouped.apply(cumsum_apply_nb, group_by=False).wrapper.grouper.group_by is None

    def test_count(self):
        assert records['a'].count() == 3
        pd.testing.assert_series_equal(
            records.count(),
            pd.Series(
                np.array([3, 3, 3, 0]),
                index=wrapper.columns
            ).rename('count')
        )
        assert records_grouped['g1'].count() == 6
        pd.testing.assert_series_equal(
            records_grouped.count(),
            pd.Series(
                np.array([6, 3]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('count')
        )

    @pytest.mark.parametrize(
        "test_nosort",
        [False, True],
    )
    def test_indexing(self, test_nosort):
        if test_nosort:
            r = records_nosort
            r_grouped = records_nosort_grouped
        else:
            r = records
            r_grouped = records_grouped
        record_arrays_close(
            r['a'].values,
            np.array([
                (0, 0, 0, 10., 21.), (1, 0, 1, 11., 20.), (2, 0, 2, 12., 19.)
            ], dtype=example_dt)
        )
        pd.testing.assert_index_equal(
            r['a'].wrapper.columns,
            pd.Index(['a'], dtype='object')
        )
        pd.testing.assert_index_equal(
            r['b'].wrapper.columns,
            pd.Index(['b'], dtype='object')
        )
        record_arrays_close(
            r[['a', 'a']].values,
            np.array([
                (0, 0, 0, 10., 21.), (1, 0, 1, 11., 20.), (2, 0, 2, 12., 19.),
                (0, 1, 0, 10., 21.), (1, 1, 1, 11., 20.), (2, 1, 2, 12., 19.)
            ], dtype=example_dt)
        )
        pd.testing.assert_index_equal(
            r[['a', 'a']].wrapper.columns,
            pd.Index(['a', 'a'], dtype='object')
        )
        record_arrays_close(
            r[['a', 'b']].values,
            np.array([
                (0, 0, 0, 10., 21.), (1, 0, 1, 11., 20.), (2, 0, 2, 12., 19.),
                (3, 1, 0, 13., 18.), (4, 1, 1, 14., 17.), (5, 1, 2, 13., 18.)
            ], dtype=example_dt)
        )
        pd.testing.assert_index_equal(
            r[['a', 'b']].wrapper.columns,
            pd.Index(['a', 'b'], dtype='object')
        )
        with pytest.raises(Exception):
            _ = r.iloc[::2, :]  # changing time not supported
        pd.testing.assert_index_equal(
            r_grouped['g1'].wrapper.columns,
            pd.Index(['a', 'b'], dtype='object')
        )
        assert r_grouped['g1'].wrapper.ndim == 2
        assert r_grouped['g1'].wrapper.grouped_ndim == 1
        pd.testing.assert_index_equal(
            r_grouped['g1'].wrapper.grouper.group_by,
            pd.Index(['g1', 'g1'], dtype='object')
        )
        pd.testing.assert_index_equal(
            r_grouped['g2'].wrapper.columns,
            pd.Index(['c', 'd'], dtype='object')
        )
        assert r_grouped['g2'].wrapper.ndim == 2
        assert r_grouped['g2'].wrapper.grouped_ndim == 1
        pd.testing.assert_index_equal(
            r_grouped['g2'].wrapper.grouper.group_by,
            pd.Index(['g2', 'g2'], dtype='object')
        )
        pd.testing.assert_index_equal(
            r_grouped[['g1']].wrapper.columns,
            pd.Index(['a', 'b'], dtype='object')
        )
        assert r_grouped[['g1']].wrapper.ndim == 2
        assert r_grouped[['g1']].wrapper.grouped_ndim == 2
        pd.testing.assert_index_equal(
            r_grouped[['g1']].wrapper.grouper.group_by,
            pd.Index(['g1', 'g1'], dtype='object')
        )
        pd.testing.assert_index_equal(
            r_grouped[['g1', 'g2']].wrapper.columns,
            pd.Index(['a', 'b', 'c', 'd'], dtype='object')
        )
        assert r_grouped[['g1', 'g2']].wrapper.ndim == 2
        assert r_grouped[['g1', 'g2']].wrapper.grouped_ndim == 2
        pd.testing.assert_index_equal(
            r_grouped[['g1', 'g2']].wrapper.grouper.group_by,
            pd.Index(['g1', 'g1', 'g2', 'g2'], dtype='object')
        )

    def test_filtering(self):
        filtered_records = vbt.Records(wrapper, records_arr[[0, -1]])
        record_arrays_close(
            filtered_records.values,
            np.array([(0, 0, 0, 10., 21.), (8, 2, 2, 10., 21.)], dtype=example_dt)
        )
        # a
        record_arrays_close(
            filtered_records['a'].values,
            np.array([(0, 0, 0, 10., 21.)], dtype=example_dt)
        )
        np.testing.assert_array_equal(
            filtered_records['a'].map_field('some_field1').id_arr,
            np.array([0])
        )
        assert filtered_records['a'].map_field('some_field1').min() == 10.
        assert filtered_records['a'].count() == 1.
        # b
        record_arrays_close(
            filtered_records['b'].values,
            np.array([], dtype=example_dt)
        )
        np.testing.assert_array_equal(
            filtered_records['b'].map_field('some_field1').id_arr,
            np.array([])
        )
        assert np.isnan(filtered_records['b'].map_field('some_field1').min())
        assert filtered_records['b'].count() == 0.
        # c
        record_arrays_close(
            filtered_records['c'].values,
            np.array([(8, 0, 2, 10., 21.)], dtype=example_dt)
        )
        np.testing.assert_array_equal(
            filtered_records['c'].map_field('some_field1').id_arr,
            np.array([8])
        )
        assert filtered_records['c'].map_field('some_field1').min() == 10.
        assert filtered_records['c'].count() == 1.
        # d
        record_arrays_close(
            filtered_records['d'].values,
            np.array([], dtype=example_dt)
        )
        np.testing.assert_array_equal(
            filtered_records['d'].map_field('some_field1').id_arr,
            np.array([])
        )
        assert np.isnan(filtered_records['d'].map_field('some_field1').min())
        assert filtered_records['d'].count() == 0.

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Count'
        ], dtype='object')
        pd.testing.assert_series_equal(
            records.stats(),
            pd.Series([
                'x', 'z', pd.Timedelta('3 days 00:00:00'), 2.25
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            records.stats(column='a'),
            pd.Series([
                'x', 'z', pd.Timedelta('3 days 00:00:00'), 3
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            records.stats(column='g1', group_by=group_by),
            pd.Series([
                'x', 'z', pd.Timedelta('3 days 00:00:00'), 6
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            records['c'].stats(),
            records.stats(column='c')
        )
        pd.testing.assert_series_equal(
            records['c'].stats(),
            records.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            records_grouped['g2'].stats(),
            records_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            records_grouped['g2'].stats(),
            records.stats(column='g2', group_by=group_by)
        )
        stats_df = records.stats(agg_func=None)
        assert stats_df.shape == (4, 4)
        pd.testing.assert_index_equal(stats_df.index, records.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)


# ############# ranges.py ############# #

ts = pd.DataFrame({
    'a': [1, -1, 3, -1, 5, -1],
    'b': [-1, -1, -1, 4, 5, 6],
    'c': [1, 2, 3, -1, -1, -1],
    'd': [-1, -1, -1, -1, -1, -1]
}, index=[
    datetime(2020, 1, 1),
    datetime(2020, 1, 2),
    datetime(2020, 1, 3),
    datetime(2020, 1, 4),
    datetime(2020, 1, 5),
    datetime(2020, 1, 6)
])

ranges = vbt.Ranges.from_ts(ts, wrapper_kwargs=dict(freq='1 days'))
ranges_grouped = vbt.Ranges.from_ts(ts, wrapper_kwargs=dict(freq='1 days', group_by=group_by))


class TestRanges:
    def test_mapped_fields(self):
        for name in range_dt.names:
            np.testing.assert_array_equal(
                getattr(ranges, name).values,
                ranges.values[name]
            )

    def test_from_ts(self):
        record_arrays_close(
            ranges.values,
            np.array([
                (0, 0, 0, 1, 1), (1, 0, 2, 3, 1), (2, 0, 4, 5, 1), (3, 1, 3, 5, 0), (4, 2, 0, 3, 1)
            ], dtype=range_dt)
        )
        assert ranges.wrapper.freq == day_dt
        pd.testing.assert_index_equal(
            ranges_grouped.wrapper.grouper.group_by,
            group_by
        )

    def test_records_readable(self):
        records_readable = ranges.records_readable

        np.testing.assert_array_equal(
            records_readable['Range Id'].values,
            np.array([
                0, 1, 2, 3, 4
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Column'].values,
            np.array([
                'a', 'a', 'a', 'b', 'c'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Start Timestamp'].values,
            np.array([
                '2020-01-01T00:00:00.000000000', '2020-01-03T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['End Timestamp'].values,
            np.array([
                '2020-01-02T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-06T00:00:00.000000000',
                '2020-01-04T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Status'].values,
            np.array([
                'Closed', 'Closed', 'Closed', 'Open', 'Closed'
            ])
        )

    def test_to_mask(self):
        pd.testing.assert_series_equal(
            ranges['a'].to_mask(),
            ts['a'] != -1
        )
        pd.testing.assert_frame_equal(
            ranges.to_mask(),
            ts != -1
        )
        pd.testing.assert_frame_equal(
            ranges_grouped.to_mask(),
            pd.DataFrame(
                [
                    [True, True],
                    [False, True],
                    [True, True],
                    [True, False],
                    [True, False],
                    [True, False]
                ],
                index=ts.index,
                columns=pd.Index(['g1', 'g2'], dtype='object')
            )
        )

    def test_duration(self):
        np.testing.assert_array_equal(
            ranges['a'].duration.values,
            np.array([1, 1, 1])
        )
        np.testing.assert_array_equal(
            ranges.duration.values,
            np.array([1, 1, 1, 3, 3])
        )

    def test_avg_duration(self):
        assert ranges['a'].avg_duration() == pd.Timedelta('1 days 00:00:00')
        pd.testing.assert_series_equal(
            ranges.avg_duration(),
            pd.Series(
                np.array([86400000000000, 259200000000000, 259200000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=wrapper.columns
            ).rename('avg_duration')
        )
        pd.testing.assert_series_equal(
            ranges_grouped.avg_duration(),
            pd.Series(
                np.array([129600000000000, 259200000000000], dtype='timedelta64[ns]'),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('avg_duration')
        )

    def test_max_duration(self):
        assert ranges['a'].max_duration() == pd.Timedelta('1 days 00:00:00')
        pd.testing.assert_series_equal(
            ranges.max_duration(),
            pd.Series(
                np.array([86400000000000, 259200000000000, 259200000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=wrapper.columns
            ).rename('max_duration')
        )
        pd.testing.assert_series_equal(
            ranges_grouped.max_duration(),
            pd.Series(
                np.array([259200000000000, 259200000000000], dtype='timedelta64[ns]'),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('max_duration')
        )

    def test_coverage(self):
        assert ranges['a'].coverage() == 0.5
        pd.testing.assert_series_equal(
            ranges.coverage(),
            pd.Series(
                np.array([0.5, 0.5, 0.5, np.nan]),
                index=ts2.columns
            ).rename('coverage')
        )
        pd.testing.assert_series_equal(
            ranges.coverage(),
            ranges.replace(records_arr=np.repeat(ranges.values, 2)).coverage()
        )
        pd.testing.assert_series_equal(
            ranges.replace(records_arr=np.repeat(ranges.values, 2)).coverage(overlapping=True),
            pd.Series(
                np.array([1.0, 1.0, 1.0, np.nan]),
                index=ts2.columns
            ).rename('coverage')
        )
        pd.testing.assert_series_equal(
            ranges.coverage(normalize=False),
            pd.Series(
                np.array([3.0, 3.0, 3.0, np.nan]),
                index=ts2.columns
            ).rename('coverage')
        )
        pd.testing.assert_series_equal(
            ranges.replace(records_arr=np.repeat(ranges.values, 2)).coverage(overlapping=True, normalize=False),
            pd.Series(
                np.array([3.0, 3.0, 3.0, np.nan]),
                index=ts2.columns
            ).rename('coverage')
        )
        pd.testing.assert_series_equal(
            ranges_grouped.coverage(),
            pd.Series(
                np.array([0.4166666666666667, 0.25]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('coverage')
        )
        pd.testing.assert_series_equal(
            ranges_grouped.coverage(),
            ranges_grouped.replace(records_arr=np.repeat(ranges_grouped.values, 2)).coverage()
        )

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Coverage', 'Overlap Coverage',
            'Total Records', 'Duration: Min', 'Duration: Median', 'Duration: Max',
            'Duration: Mean', 'Duration: Std'
        ], dtype='object')
        pd.testing.assert_series_equal(
            ranges.stats(),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'), 1.25, pd.Timedelta('2 days 08:00:00'),
                pd.Timedelta('2 days 08:00:00'), pd.Timedelta('2 days 08:00:00'),
                pd.Timedelta('2 days 08:00:00'), pd.Timedelta('0 days 00:00:00')
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            ranges.stats(column='a'),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'), 3, pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('0 days 00:00:00')
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            ranges.stats(column='g1', group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), pd.Timedelta('5 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'), 4, pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('1 days 12:00:00'), pd.Timedelta('1 days 00:00:00')
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            ranges['c'].stats(),
            ranges.stats(column='c')
        )
        pd.testing.assert_series_equal(
            ranges['c'].stats(),
            ranges.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            ranges_grouped['g2'].stats(),
            ranges_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            ranges_grouped['g2'].stats(),
            ranges.stats(column='g2', group_by=group_by)
        )
        stats_df = ranges.stats(agg_func=None)
        assert stats_df.shape == (4, 11)
        pd.testing.assert_index_equal(stats_df.index, ranges.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)


# ############# drawdowns.py ############# #


ts2 = pd.DataFrame({
    'a': [2, 1, 3, 1, 4, 1],
    'b': [1, 2, 1, 3, 1, 4],
    'c': [1, 2, 3, 2, 1, 2],
    'd': [1, 2, 3, 4, 5, 6]
}, index=[
    datetime(2020, 1, 1),
    datetime(2020, 1, 2),
    datetime(2020, 1, 3),
    datetime(2020, 1, 4),
    datetime(2020, 1, 5),
    datetime(2020, 1, 6)
])

drawdowns = vbt.Drawdowns.from_ts(ts2, wrapper_kwargs=dict(freq='1 days'))
drawdowns_grouped = vbt.Drawdowns.from_ts(ts2, wrapper_kwargs=dict(freq='1 days', group_by=group_by))


class TestDrawdowns:
    def test_mapped_fields(self):
        for name in drawdown_dt.names:
            np.testing.assert_array_equal(
                getattr(drawdowns, name).values,
                drawdowns.values[name]
            )

    def test_ts(self):
        pd.testing.assert_frame_equal(
            drawdowns.ts,
            ts2
        )
        pd.testing.assert_series_equal(
            drawdowns['a'].ts,
            ts2['a']
        )
        pd.testing.assert_frame_equal(
            drawdowns_grouped['g1'].ts,
            ts2[['a', 'b']]
        )
        assert drawdowns.replace(ts=None)['a'].ts is None

    def test_from_ts(self):
        record_arrays_close(
            drawdowns.values,
            np.array([
                (0, 0, 0, 1, 1, 2, 2.0, 1.0, 3.0, 1), (1, 0, 2, 3, 3, 4, 3.0, 1.0, 4.0, 1),
                (2, 0, 4, 5, 5, 5, 4.0, 1.0, 1.0, 0), (3, 1, 1, 2, 2, 3, 2.0, 1.0, 3.0, 1),
                (4, 1, 3, 4, 4, 5, 3.0, 1.0, 4.0, 1), (5, 2, 2, 3, 4, 5, 3.0, 1.0, 2.0, 0)
            ], dtype=drawdown_dt)
        )
        assert drawdowns.wrapper.freq == day_dt
        pd.testing.assert_index_equal(
            drawdowns_grouped.wrapper.grouper.group_by,
            group_by
        )

    def test_records_readable(self):
        records_readable = drawdowns.records_readable

        np.testing.assert_array_equal(
            records_readable['Drawdown Id'].values,
            np.array([
                0, 1, 2, 3, 4, 5
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Column'].values,
            np.array([
                'a', 'a', 'a', 'b', 'b', 'c'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Peak Timestamp'].values,
            np.array([
                '2020-01-01T00:00:00.000000000', '2020-01-03T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-04T00:00:00.000000000', '2020-01-03T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Start Timestamp'].values,
            np.array([
                '2020-01-02T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-03T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-04T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Valley Timestamp'].values,
            np.array([
                '2020-01-02T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-03T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-05T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['End Timestamp'].values,
            np.array([
                '2020-01-03T00:00:00.000000000', '2020-01-05T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-06T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Peak Value'].values,
            np.array([
                2., 3., 4., 2., 3., 3.
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Valley Value'].values,
            np.array([
                1., 1., 1., 1., 1., 1.
            ])
        )
        np.testing.assert_array_equal(
            records_readable['End Value'].values,
            np.array([
                3., 4., 1., 3., 4., 2.
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Status'].values,
            np.array([
                'Recovered', 'Recovered', 'Active', 'Recovered', 'Recovered', 'Active'
            ])
        )

    def test_drawdown(self):
        np.testing.assert_array_almost_equal(
            drawdowns['a'].drawdown.values,
            np.array([-0.5, -0.66666667, -0.75])
        )
        np.testing.assert_array_almost_equal(
            drawdowns.drawdown.values,
            np.array([-0.5, -0.66666667, -0.75, -0.5, -0.66666667, -0.66666667])
        )
        pd.testing.assert_frame_equal(
            drawdowns.drawdown.to_pd(),
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [-0.5, np.nan, np.nan, np.nan],
                    [np.nan, -0.5, np.nan, np.nan],
                    [-0.66666669, np.nan, np.nan, np.nan],
                    [-0.75, -0.66666669, -0.66666669, np.nan]
                ]),
                index=ts2.index,
                columns=ts2.columns
            )
        )

    def test_avg_drawdown(self):
        assert drawdowns['a'].avg_drawdown() == -0.6388888888888888
        pd.testing.assert_series_equal(
            drawdowns.avg_drawdown(),
            pd.Series(
                np.array([-0.63888889, -0.58333333, -0.66666667, np.nan]),
                index=wrapper.columns
            ).rename('avg_drawdown')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.avg_drawdown(),
            pd.Series(
                np.array([-0.6166666666666666, -0.6666666666666666]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('avg_drawdown')
        )

    def test_max_drawdown(self):
        assert drawdowns['a'].max_drawdown() == -0.75
        pd.testing.assert_series_equal(
            drawdowns.max_drawdown(),
            pd.Series(
                np.array([-0.75, -0.66666667, -0.66666667, np.nan]),
                index=wrapper.columns
            ).rename('max_drawdown')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.max_drawdown(),
            pd.Series(
                np.array([-0.75, -0.6666666666666666]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('max_drawdown')
        )

    def test_recovery_return(self):
        np.testing.assert_array_almost_equal(
            drawdowns['a'].recovery_return.values,
            np.array([2., 3., 0.])
        )
        np.testing.assert_array_almost_equal(
            drawdowns.recovery_return.values,
            np.array([2., 3., 0., 2., 3., 1.])
        )
        pd.testing.assert_frame_equal(
            drawdowns.recovery_return.to_pd(),
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [2.0, np.nan, np.nan, np.nan],
                    [np.nan, 2.0, np.nan, np.nan],
                    [3.0, np.nan, np.nan, np.nan],
                    [0.0, 3.0, 1.0, np.nan]
                ]),
                index=ts2.index,
                columns=ts2.columns
            )
        )

    def test_avg_recovery_return(self):
        assert drawdowns['a'].avg_recovery_return() == 1.6666666666666667
        pd.testing.assert_series_equal(
            drawdowns.avg_recovery_return(),
            pd.Series(
                np.array([1.6666666666666667, 2.5, 1.0, np.nan]),
                index=wrapper.columns
            ).rename('avg_recovery_return')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.avg_recovery_return(),
            pd.Series(
                np.array([2.0, 1.0]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('avg_recovery_return')
        )

    def test_max_recovery_return(self):
        assert drawdowns['a'].max_recovery_return() == 3.0
        pd.testing.assert_series_equal(
            drawdowns.max_recovery_return(),
            pd.Series(
                np.array([3.0, 3.0, 1.0, np.nan]),
                index=wrapper.columns
            ).rename('max_recovery_return')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.max_recovery_return(),
            pd.Series(
                np.array([3.0, 1.0]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('max_recovery_return')
        )

    def test_duration(self):
        np.testing.assert_array_almost_equal(
            drawdowns['a'].duration.values,
            np.array([1, 1, 1])
        )
        np.testing.assert_array_almost_equal(
            drawdowns.duration.values,
            np.array([1, 1, 1, 1, 1, 3])
        )

    def test_avg_duration(self):
        assert drawdowns['a'].avg_duration() == pd.Timedelta('1 days 00:00:00')
        pd.testing.assert_series_equal(
            drawdowns.avg_duration(),
            pd.Series(
                np.array([86400000000000, 86400000000000, 259200000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=wrapper.columns
            ).rename('avg_duration')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.avg_duration(),
            pd.Series(
                np.array([86400000000000, 259200000000000], dtype='timedelta64[ns]'),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('avg_duration')
        )

    def test_max_duration(self):
        assert drawdowns['a'].max_duration() == pd.Timedelta('1 days 00:00:00')
        pd.testing.assert_series_equal(
            drawdowns.max_duration(),
            pd.Series(
                np.array([86400000000000, 86400000000000, 259200000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=wrapper.columns
            ).rename('max_duration')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.max_duration(),
            pd.Series(
                np.array([86400000000000, 259200000000000], dtype='timedelta64[ns]'),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('max_duration')
        )

    def test_coverage(self):
        assert drawdowns['a'].coverage() == 0.5
        pd.testing.assert_series_equal(
            drawdowns.coverage(),
            pd.Series(
                np.array([0.5, 0.3333333333333333, 0.5, np.nan]),
                index=ts2.columns
            ).rename('coverage')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped.coverage(),
            pd.Series(
                np.array([0.4166666666666667, 0.25]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('coverage')
        )

    def test_decline_duration(self):
        np.testing.assert_array_almost_equal(
            drawdowns['a'].decline_duration.values,
            np.array([1., 1., 1.])
        )
        np.testing.assert_array_almost_equal(
            drawdowns.decline_duration.values,
            np.array([1., 1., 1., 1., 1., 2.])
        )

    def test_recovery_duration(self):
        np.testing.assert_array_almost_equal(
            drawdowns['a'].recovery_duration.values,
            np.array([1, 1, 0])
        )
        np.testing.assert_array_almost_equal(
            drawdowns.recovery_duration.values,
            np.array([1, 1, 0, 1, 1, 1])
        )

    def test_recovery_duration_ratio(self):
        np.testing.assert_array_almost_equal(
            drawdowns['a'].recovery_duration_ratio.values,
            np.array([1., 1., 0.])
        )
        np.testing.assert_array_almost_equal(
            drawdowns.recovery_duration_ratio.values,
            np.array([1., 1., 0., 1., 1., 0.5])
        )

    def test_active_records(self):
        assert isinstance(drawdowns.active, vbt.Drawdowns)
        assert drawdowns.active.wrapper == drawdowns.wrapper
        record_arrays_close(
            drawdowns['a'].active.values,
            np.array([
                (2, 0, 4, 5, 5, 5, 4., 1., 1., 0)
            ], dtype=drawdown_dt)
        )
        record_arrays_close(
            drawdowns['a'].active.values,
            drawdowns.active['a'].values
        )
        record_arrays_close(
            drawdowns.active.values,
            np.array([
                (2, 0, 4, 5, 5, 5, 4.0, 1.0, 1.0, 0), (5, 2, 2, 3, 4, 5, 3.0, 1.0, 2.0, 0)
            ], dtype=drawdown_dt)
        )

    def test_recovered_records(self):
        assert isinstance(drawdowns.recovered, vbt.Drawdowns)
        assert drawdowns.recovered.wrapper == drawdowns.wrapper
        record_arrays_close(
            drawdowns['a'].recovered.values,
            np.array([
                (0, 0, 0, 1, 1, 2, 2.0, 1.0, 3.0, 1), (1, 0, 2, 3, 3, 4, 3.0, 1.0, 4.0, 1)
            ], dtype=drawdown_dt)
        )
        record_arrays_close(
            drawdowns['a'].recovered.values,
            drawdowns.recovered['a'].values
        )
        record_arrays_close(
            drawdowns.recovered.values,
            np.array([
                (0, 0, 0, 1, 1, 2, 2.0, 1.0, 3.0, 1), (1, 0, 2, 3, 3, 4, 3.0, 1.0, 4.0, 1),
                (3, 1, 1, 2, 2, 3, 2.0, 1.0, 3.0, 1), (4, 1, 3, 4, 4, 5, 3.0, 1.0, 4.0, 1)
            ], dtype=drawdown_dt)
        )

    def test_active_drawdown(self):
        assert drawdowns['a'].active_drawdown() == -0.75
        pd.testing.assert_series_equal(
            drawdowns.active_drawdown(),
            pd.Series(
                np.array([-0.75, np.nan, -0.3333333333333333, np.nan]),
                index=wrapper.columns
            ).rename('active_drawdown')
        )
        with pytest.raises(Exception):
            drawdowns_grouped.active_drawdown()

    def test_active_duration(self):
        assert drawdowns['a'].active_duration() == np.timedelta64(86400000000000)
        pd.testing.assert_series_equal(
            drawdowns.active_duration(),
            pd.Series(
                np.array([86400000000000, 'NaT', 259200000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=wrapper.columns
            ).rename('active_duration')
        )
        with pytest.raises(Exception):
            drawdowns_grouped.active_duration()

    def test_active_recovery(self):
        assert drawdowns['a'].active_recovery() == 0.
        pd.testing.assert_series_equal(
            drawdowns.active_recovery(),
            pd.Series(
                np.array([0., np.nan, 0.5, np.nan]),
                index=wrapper.columns
            ).rename('active_recovery')
        )
        with pytest.raises(Exception):
            drawdowns_grouped.active_recovery()

    def test_active_recovery_return(self):
        assert drawdowns['a'].active_recovery_return() == 0.
        pd.testing.assert_series_equal(
            drawdowns.active_recovery_return(),
            pd.Series(
                np.array([0., np.nan, 1., np.nan]),
                index=wrapper.columns
            ).rename('active_recovery_return')
        )
        with pytest.raises(Exception):
            drawdowns_grouped.active_recovery_return()

    def test_active_recovery_duration(self):
        assert drawdowns['a'].active_recovery_duration() == pd.Timedelta('0 days 00:00:00')
        pd.testing.assert_series_equal(
            drawdowns.active_recovery_duration(),
            pd.Series(
                np.array([0, 'NaT', 86400000000000, 'NaT'], dtype='timedelta64[ns]'),
                index=wrapper.columns
            ).rename('active_recovery_duration')
        )
        with pytest.raises(Exception):
            drawdowns_grouped.active_recovery_duration()

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Coverage [%]', 'Total Records',
            'Total Recovered Drawdowns', 'Total Active Drawdowns',
            'Active Drawdown [%]', 'Active Duration', 'Active Recovery [%]',
            'Active Recovery Return [%]', 'Active Recovery Duration',
            'Max Drawdown [%]', 'Avg Drawdown [%]', 'Max Drawdown Duration',
            'Avg Drawdown Duration', 'Max Recovery Return [%]',
            'Avg Recovery Return [%]', 'Max Recovery Duration',
            'Avg Recovery Duration', 'Avg Recovery Duration Ratio'
        ], dtype='object')
        pd.testing.assert_series_equal(
            drawdowns.stats(),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), 44.444444444444436, 1.5, 1.0, 0.5,
                54.166666666666664, pd.Timedelta('2 days 00:00:00'), 25.0, 50.0,
                pd.Timedelta('0 days 12:00:00'), 66.66666666666666, 58.33333333333333,
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'), 300.0, 250.0,
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'), 1.0
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            drawdowns.stats(settings=dict(incl_active=True)),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), 44.444444444444436, 1.5, 1.0, 0.5,
                54.166666666666664, pd.Timedelta('2 days 00:00:00'), 25.0, 50.0,
                pd.Timedelta('0 days 12:00:00'), 69.44444444444444, 62.962962962962955,
                pd.Timedelta('1 days 16:00:00'), pd.Timedelta('1 days 16:00:00'), 300.0, 250.0,
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'), 1.0
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            drawdowns.stats(column='a'),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), 50.0, 3, 2, 1, 75.0, pd.Timedelta('1 days 00:00:00'),
                0.0, 0.0, pd.Timedelta('0 days 00:00:00'), 66.66666666666666, 58.33333333333333,
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'), 300.0, 250.0,
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'), 1.0
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            drawdowns.stats(column='g1', group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-06 00:00:00'),
                pd.Timedelta('6 days 00:00:00'), 41.66666666666667, 5, 4, 1, 66.66666666666666,
                58.33333333333333, pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'),
                300.0, 250.0, pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'), 1.0
            ],
                index=pd.Index([
                    'Start', 'End', 'Period', 'Coverage [%]', 'Total Records',
                    'Total Recovered Drawdowns', 'Total Active Drawdowns',
                    'Max Drawdown [%]', 'Avg Drawdown [%]', 'Max Drawdown Duration',
                    'Avg Drawdown Duration', 'Max Recovery Return [%]',
                    'Avg Recovery Return [%]', 'Max Recovery Duration',
                    'Avg Recovery Duration', 'Avg Recovery Duration Ratio'
                ], dtype='object'),
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            drawdowns['c'].stats(),
            drawdowns.stats(column='c')
        )
        pd.testing.assert_series_equal(
            drawdowns['c'].stats(),
            drawdowns.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped['g2'].stats(),
            drawdowns_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            drawdowns_grouped['g2'].stats(),
            drawdowns.stats(column='g2', group_by=group_by)
        )
        stats_df = drawdowns.stats(agg_func=None)
        assert stats_df.shape == (4, 21)
        pd.testing.assert_index_equal(stats_df.index, drawdowns.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)


# ############# orders.py ############# #

close = pd.Series([1, 2, 3, 4, 5, 6, 7, 8], index=[
    datetime(2020, 1, 1),
    datetime(2020, 1, 2),
    datetime(2020, 1, 3),
    datetime(2020, 1, 4),
    datetime(2020, 1, 5),
    datetime(2020, 1, 6),
    datetime(2020, 1, 7),
    datetime(2020, 1, 8)
]).vbt.tile(4, keys=['a', 'b', 'c', 'd'])

size = np.full(close.shape, np.nan, dtype=np.float64)
size[:, 0] = [1, 0.1, -1, -0.1, np.nan, 1, -1, 2]
size[:, 1] = [-1, -0.1, 1, 0.1, np.nan, -1, 1, -2]
size[:, 2] = [1, 0.1, -1, -0.1, np.nan, 1, -2, 2]
orders = vbt.Portfolio.from_orders(close, size, fees=0.01, freq='1 days').orders
orders_grouped = orders.regroup(group_by)


class TestOrders:
    def test_mapped_fields(self):
        for name in order_dt.names:
            np.testing.assert_array_equal(
                getattr(orders, name).values,
                orders.values[name]
            )

    def test_close(self):
        pd.testing.assert_frame_equal(
            orders.close,
            close
        )
        pd.testing.assert_series_equal(
            orders['a'].close,
            close['a']
        )
        pd.testing.assert_frame_equal(
            orders_grouped['g1'].close,
            close[['a', 'b']]
        )
        assert orders.replace(close=None)['a'].close is None

    def test_records_readable(self):
        records_readable = orders.records_readable

        np.testing.assert_array_equal(
            records_readable['Order Id'].values,
            np.array([
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Timestamp'].values,
            np.array([
                '2020-01-01T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-07T00:00:00.000000000',
                '2020-01-08T00:00:00.000000000', '2020-01-01T00:00:00.000000000',
                '2020-01-02T00:00:00.000000000', '2020-01-03T00:00:00.000000000',
                '2020-01-04T00:00:00.000000000', '2020-01-06T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-07T00:00:00.000000000',
                '2020-01-08T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Column'].values,
            np.array([
                'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'b',
                'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Size'].values,
            np.array([
                1.0, 0.1, 1.0, 0.1, 1.0, 1.0, 2.0, 1.0, 0.1, 1.0, 0.1, 1.0, 1.0,
                2.0, 1.0, 0.1, 1.0, 0.1, 1.0, 2.0, 2.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Price'].values,
            np.array([
                1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0,
                8.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Fees'].values,
            np.array([
                0.01, 0.002, 0.03, 0.004, 0.06, 0.07, 0.16, 0.01, 0.002, 0.03,
                0.004, 0.06, 0.07, 0.16, 0.01, 0.002, 0.03, 0.004, 0.06, 0.14,
                0.16
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Side'].values,
            np.array([
                'Buy', 'Buy', 'Sell', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Sell',
                'Buy', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Buy', 'Sell', 'Sell',
                'Buy', 'Sell', 'Buy'
            ])
        )

    def test_buy_records(self):
        assert isinstance(orders.buy, vbt.Orders)
        assert orders.buy.wrapper == orders.wrapper
        record_arrays_close(
            orders['a'].buy.values,
            np.array([
                (0, 0, 0, 1., 1., 0.01, 0), (1, 0, 1, 0.1, 2., 0.002, 0),
                (4, 0, 5, 1., 6., 0.06, 0), (6, 0, 7, 2., 8., 0.16, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            orders['a'].buy.values,
            orders.buy['a'].values
        )
        record_arrays_close(
            orders.buy.values,
            np.array([
                (0, 0, 0, 1., 1., 0.01, 0), (1, 0, 1, 0.1, 2., 0.002, 0),
                (4, 0, 5, 1., 6., 0.06, 0), (6, 0, 7, 2., 8., 0.16, 0),
                (9, 1, 2, 1., 3., 0.03, 0), (10, 1, 3, 0.1, 4., 0.004, 0),
                (12, 1, 6, 1., 7., 0.07, 0), (14, 2, 0, 1., 1., 0.01, 0),
                (15, 2, 1, 0.1, 2., 0.002, 0), (18, 2, 5, 1., 6., 0.06, 0),
                (20, 2, 7, 2., 8., 0.16, 0)
            ], dtype=order_dt)
        )

    def test_sell_records(self):
        assert isinstance(orders.sell, vbt.Orders)
        assert orders.sell.wrapper == orders.wrapper
        record_arrays_close(
            orders['a'].sell.values,
            np.array([
                (2, 0, 2, 1., 3., 0.03, 1), (3, 0, 3, 0.1, 4., 0.004, 1),
                (5, 0, 6, 1., 7., 0.07, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            orders['a'].sell.values,
            orders.sell['a'].values
        )
        record_arrays_close(
            orders.sell.values,
            np.array([
                (2, 0, 2, 1., 3., 0.03, 1), (3, 0, 3, 0.1, 4., 0.004, 1),
                (5, 0, 6, 1., 7., 0.07, 1), (7, 1, 0, 1., 1., 0.01, 1),
                (8, 1, 1, 0.1, 2., 0.002, 1), (11, 1, 5, 1., 6., 0.06, 1),
                (13, 1, 7, 2., 8., 0.16, 1), (16, 2, 2, 1., 3., 0.03, 1),
                (17, 2, 3, 0.1, 4., 0.004, 1), (19, 2, 6, 2., 7., 0.14, 1)
            ], dtype=order_dt)
        )

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Total Records', 'Total Buy Orders', 'Total Sell Orders',
            'Min Size', 'Max Size', 'Avg Size', 'Avg Buy Size', 'Avg Sell Size',
            'Avg Buy Price', 'Avg Sell Price', 'Total Fees', 'Min Fees', 'Max Fees',
            'Avg Fees', 'Avg Buy Fees', 'Avg Sell Fees'
        ], dtype='object')
        pd.testing.assert_series_equal(
            orders.stats(),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), 5.25, 2.75, 2.5, 0.10000000000000002, 2.0,
                0.9333333333333335, 0.9166666666666666, 0.9194444444444446, 4.388888888888889,
                4.527777777777779, 0.26949999999999996, 0.002, 0.16, 0.051333333333333335,
                0.050222222222222224, 0.050222222222222224
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            orders.stats(column='a'),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), 7, 4, 3, 0.1, 2.0, 0.8857142857142858,
                1.025, 0.7000000000000001, 4.25, 4.666666666666667, 0.33599999999999997,
                0.002, 0.16, 0.047999999999999994, 0.057999999999999996, 0.03466666666666667
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            orders.stats(column='g1', group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), 14, 7, 7, 0.1, 2.0, 0.8857142857142858,
                0.8857142857142856, 0.8857142857142858, 4.428571428571429, 4.428571428571429,
                0.672, 0.002, 0.16, 0.048, 0.048, 0.047999999999999994
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            orders['c'].stats(),
            orders.stats(column='c')
        )
        pd.testing.assert_series_equal(
            orders['c'].stats(),
            orders.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            orders_grouped['g2'].stats(),
            orders_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            orders_grouped['g2'].stats(),
            orders.stats(column='g2', group_by=group_by)
        )
        stats_df = orders.stats(agg_func=None)
        assert stats_df.shape == (4, 19)
        pd.testing.assert_index_equal(stats_df.index, orders.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)


# ############# trades.py ############# #

exit_trades = vbt.ExitTrades.from_orders(orders)
exit_trades_grouped = vbt.ExitTrades.from_orders(orders_grouped)


class TestExitTrades:
    def test_mapped_fields(self):
        for name in trade_dt.names:
            if name == 'return':
                np.testing.assert_array_equal(
                    getattr(exit_trades, 'returns').values,
                    exit_trades.values[name]
                )
            else:
                np.testing.assert_array_equal(
                    getattr(exit_trades, name).values,
                    exit_trades.values[name]
                )

    def test_close(self):
        pd.testing.assert_frame_equal(
            exit_trades.close,
            close
        )
        pd.testing.assert_series_equal(
            exit_trades['a'].close,
            close['a']
        )
        pd.testing.assert_frame_equal(
            exit_trades_grouped['g1'].close,
            close[['a', 'b']]
        )
        assert exit_trades.replace(close=None)['a'].close is None

    def test_records_arr(self):
        record_arrays_close(
            exit_trades.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1),
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2),
                (4, 1, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, -1.95, -1.7875, 1, 1, 3),
                (5, 1, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, -0.296, -2.71333333, 1, 1, 3),
                (6, 1, 1., 5, 6., 0.06, 6, 7., 0.07, -1.13, -0.18833333, 1, 1, 4),
                (7, 1, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 1, 0, 5),
                (8, 2, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 6),
                (9, 2, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 6),
                (10, 2, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 7),
                (11, 2, 1., 6, 7., 0.07, 7, 8., 0.08, -1.15, -0.16428571, 1, 1, 8),
                (12, 2, 1., 7, 8., 0.08, 7, 8., 0., -0.08, -0.01, 0, 0, 9)
            ], dtype=trade_dt)
        )
        reversed_col_orders = orders.replace(records_arr=np.concatenate((
            orders.values[orders.values['col'] == 2],
            orders.values[orders.values['col'] == 1],
            orders.values[orders.values['col'] == 0]
        )))
        record_arrays_close(
            vbt.ExitTrades.from_orders(reversed_col_orders).values,
            exit_trades.values
        )

    def test_records_readable(self):
        records_readable = exit_trades.records_readable

        np.testing.assert_array_equal(
            records_readable['Exit Trade Id'].values,
            np.array([
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Column'].values,
            np.array([
                'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Size'].values,
            np.array([
                1.0, 0.10000000000000009, 1.0, 2.0, 1.0, 0.10000000000000009, 1.0,
                2.0, 1.0, 0.10000000000000009, 1.0, 1.0, 1.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Entry Timestamp'].values,
            np.array([
                '2020-01-01T00:00:00.000000000', '2020-01-01T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000', '2020-01-01T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000', '2020-01-01T00:00:00.000000000',
                '2020-01-06T00:00:00.000000000', '2020-01-07T00:00:00.000000000',
                '2020-01-08T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Avg Entry Price'].values,
            np.array([
                1.0909090909090908, 1.0909090909090908, 6.0, 8.0,
                1.0909090909090908, 1.0909090909090908, 6.0, 8.0,
                1.0909090909090908, 1.0909090909090908, 6.0, 7.0, 8.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Entry Fees'].values,
            np.array([
                0.010909090909090908, 0.0010909090909090918, 0.06, 0.16,
                0.010909090909090908, 0.0010909090909090918, 0.06, 0.16,
                0.010909090909090908, 0.0010909090909090918, 0.06, 0.07, 0.08
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Exit Timestamp'].values,
            np.array([
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-08T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Avg Exit Price'].values,
            np.array([
                3.0, 4.0, 7.0, 8.0, 3.0, 4.0, 7.0, 8.0, 3.0, 4.0, 7.0, 8.0, 8.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Exit Fees'].values,
            np.array([
                0.03, 0.004, 0.07, 0.0, 0.03, 0.004, 0.07, 0.0, 0.03, 0.004, 0.07, 0.08, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['PnL'].values,
            np.array([
                1.8681818181818182, 0.2858181818181821, 0.8699999999999999, -0.16,
                -1.9500000000000002, -0.29600000000000026, -1.1300000000000001,
                -0.16, 1.8681818181818182, 0.2858181818181821, 0.8699999999999999,
                -1.1500000000000001, -0.08
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Return'].values,
            np.array([
                1.7125000000000001, 2.62, 0.145, -0.01, -1.7875000000000003,
                -2.7133333333333334, -0.18833333333333335, -0.01,
                1.7125000000000001, 2.62, 0.145, -0.1642857142857143, -0.01
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Direction'].values,
            np.array([
                'Long', 'Long', 'Long', 'Long', 'Short', 'Short', 'Short',
                'Short', 'Long', 'Long', 'Long', 'Short', 'Long'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Status'].values,
            np.array([
                'Closed', 'Closed', 'Closed', 'Open', 'Closed', 'Closed', 'Closed',
                'Open', 'Closed', 'Closed', 'Closed', 'Closed', 'Open'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Position Id'].values,
            np.array([
                0, 0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9
            ])
        )

    def test_duration(self):
        np.testing.assert_array_almost_equal(
            exit_trades['a'].duration.values,
            np.array([2, 3, 1, 1])
        )
        np.testing.assert_array_almost_equal(
            exit_trades.duration.values,
            np.array([2, 3, 1, 1, 2, 3, 1, 1, 2, 3, 1, 1, 1])
        )

    def test_winning_records(self):
        assert isinstance(exit_trades.winning, vbt.ExitTrades)
        assert exit_trades.winning.wrapper == exit_trades.wrapper
        record_arrays_close(
            exit_trades['a'].winning.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            exit_trades['a'].winning.values,
            exit_trades.winning['a'].values
        )
        record_arrays_close(
            exit_trades.winning.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1),
                (8, 2, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 6),
                (9, 2, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 6),
                (10, 2, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 7)
            ], dtype=trade_dt)
        )

    def test_losing_records(self):
        assert isinstance(exit_trades.losing, vbt.ExitTrades)
        assert exit_trades.losing.wrapper == exit_trades.wrapper
        record_arrays_close(
            exit_trades['a'].losing.values,
            np.array([
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            exit_trades['a'].losing.values,
            exit_trades.losing['a'].values
        )
        record_arrays_close(
            exit_trades.losing.values,
            np.array([
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2),
                (4, 1, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, -1.95, -1.7875, 1, 1, 3),
                (5, 1, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, -0.296, -2.71333333, 1, 1, 3),
                (6, 1, 1., 5, 6., 0.06, 6, 7., 0.07, -1.13, -0.18833333, 1, 1, 4),
                (7, 1, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 1, 0, 5),
                (11, 2, 1., 6, 7., 0.07, 7, 8., 0.08, -1.15, -0.16428571, 1, 1, 8),
                (12, 2, 1., 7, 8., 0.08, 7, 8., 0., -0.08, -0.01, 0, 0, 9)
            ], dtype=trade_dt)
        )

    def test_win_rate(self):
        assert exit_trades['a'].win_rate() == 0.75
        pd.testing.assert_series_equal(
            exit_trades.win_rate(),
            pd.Series(
                np.array([0.75, 0., 0.6, np.nan]),
                index=close.columns
            ).rename('win_rate')
        )
        pd.testing.assert_series_equal(
            exit_trades_grouped.win_rate(),
            pd.Series(
                np.array([0.375, 0.6]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('win_rate')
        )

    def test_winning_streak(self):
        np.testing.assert_array_almost_equal(
            exit_trades['a'].winning_streak.values,
            np.array([1, 2, 3, 0])
        )
        np.testing.assert_array_almost_equal(
            exit_trades.winning_streak.values,
            np.array([1, 2, 3, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0])
        )

    def test_losing_streak(self):
        np.testing.assert_array_almost_equal(
            exit_trades['a'].losing_streak.values,
            np.array([0, 0, 0, 1])
        )
        np.testing.assert_array_almost_equal(
            exit_trades.losing_streak.values,
            np.array([0, 0, 0, 1, 1, 2, 3, 4, 0, 0, 0, 1, 2])
        )

    def test_profit_factor(self):
        assert exit_trades['a'].profit_factor() == 18.9
        pd.testing.assert_series_equal(
            exit_trades.profit_factor(),
            pd.Series(
                np.array([18.9, 0., 2.45853659, np.nan]),
                index=ts2.columns
            ).rename('profit_factor')
        )
        pd.testing.assert_series_equal(
            exit_trades_grouped.profit_factor(),
            pd.Series(
                np.array([0.81818182, 2.45853659]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('profit_factor')
        )

    def test_expectancy(self):
        assert exit_trades['a'].expectancy() == 0.716
        pd.testing.assert_series_equal(
            exit_trades.expectancy(),
            pd.Series(
                np.array([0.716, -0.884, 0.3588, np.nan]),
                index=ts2.columns
            ).rename('expectancy')
        )
        pd.testing.assert_series_equal(
            exit_trades_grouped.expectancy(),
            pd.Series(
                np.array([-0.084, 0.3588]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('expectancy')
        )

    def test_sqn(self):
        assert exit_trades['a'].sqn() == 1.634155521947584
        pd.testing.assert_series_equal(
            exit_trades.sqn(),
            pd.Series(
                np.array([1.63415552, -2.13007307, 0.71660403, np.nan]),
                index=ts2.columns
            ).rename('sqn')
        )
        pd.testing.assert_series_equal(
            exit_trades_grouped.sqn(),
            pd.Series(
                np.array([-0.20404671, 0.71660403]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('sqn')
        )

    def test_long_records(self):
        assert isinstance(exit_trades.long, vbt.ExitTrades)
        assert exit_trades.long.wrapper == exit_trades.wrapper
        record_arrays_close(
            exit_trades['a'].long.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1),
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            exit_trades['a'].long.values,
            exit_trades.long['a'].values
        )
        record_arrays_close(
            exit_trades.long.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1),
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2),
                (8, 2, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 6),
                (9, 2, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 6),
                (10, 2, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 7),
                (12, 2, 1., 7, 8., 0.08, 7, 8., 0., -0.08, -0.01, 0, 0, 9)
            ], dtype=trade_dt)
        )

    def test_short_records(self):
        assert isinstance(exit_trades.short, vbt.ExitTrades)
        assert exit_trades.short.wrapper == exit_trades.wrapper
        record_arrays_close(
            exit_trades['a'].short.values,
            np.array([], dtype=trade_dt)
        )
        record_arrays_close(
            exit_trades['a'].short.values,
            exit_trades.short['a'].values
        )
        record_arrays_close(
            exit_trades.short.values,
            np.array([
                (4, 1, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, -1.95, -1.7875, 1, 1, 3),
                (5, 1, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, -0.296, -2.71333333, 1, 1, 3),
                (6, 1, 1., 5, 6., 0.06, 6, 7., 0.07, -1.13, -0.18833333, 1, 1, 4),
                (7, 1, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 1, 0, 5),
                (11, 2, 1., 6, 7., 0.07, 7, 8., 0.08, -1.15, -0.16428571, 1, 1, 8)
            ], dtype=trade_dt)
        )

    def test_open_records(self):
        assert isinstance(exit_trades.open, vbt.ExitTrades)
        assert exit_trades.open.wrapper == exit_trades.wrapper
        record_arrays_close(
            exit_trades['a'].open.values,
            np.array([
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            exit_trades['a'].open.values,
            exit_trades.open['a'].values
        )
        record_arrays_close(
            exit_trades.open.values,
            np.array([
                (3, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2),
                (7, 1, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 1, 0, 5),
                (12, 2, 1., 7, 8., 0.08, 7, 8., 0., -0.08, -0.01, 0, 0, 9)
            ], dtype=trade_dt)
        )

    def test_closed_records(self):
        assert isinstance(exit_trades.closed, vbt.ExitTrades)
        assert exit_trades.closed.wrapper == exit_trades.wrapper
        record_arrays_close(
            exit_trades['a'].closed.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            exit_trades['a'].closed.values,
            exit_trades.closed['a'].values
        )
        record_arrays_close(
            exit_trades.closed.values,
            np.array([
                (0, 0, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 0),
                (1, 0, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 0),
                (2, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1),
                (4, 1, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, -1.95, -1.7875, 1, 1, 3),
                (5, 1, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, -0.296, -2.71333333, 1, 1, 3),
                (6, 1, 1., 5, 6., 0.06, 6, 7., 0.07, -1.13, -0.18833333, 1, 1, 4),
                (8, 2, 1., 0, 1.09090909, 0.01090909, 2, 3., 0.03, 1.86818182, 1.7125, 0, 1, 6),
                (9, 2, 0.1, 0, 1.09090909, 0.00109091, 3, 4., 0.004, 0.28581818, 2.62, 0, 1, 6),
                (10, 2, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 7),
                (11, 2, 1., 6, 7., 0.07, 7, 8., 0.08, -1.15, -0.16428571, 1, 1, 8)
            ], dtype=trade_dt)
        )

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'First Trade Start', 'Last Trade End',
            'Coverage', 'Overlap Coverage', 'Total Records', 'Total Long Trades',
            'Total Short Trades', 'Total Closed Trades', 'Total Open Trades',
            'Open Trade PnL', 'Win Rate [%]', 'Max Win Streak', 'Max Loss Streak',
            'Best Trade [%]', 'Worst Trade [%]', 'Avg Winning Trade [%]',
            'Avg Losing Trade [%]', 'Avg Winning Trade Duration',
            'Avg Losing Trade Duration', 'Profit Factor', 'Expectancy', 'SQN'
        ], dtype='object')
        pd.testing.assert_series_equal(
            exit_trades.stats(),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-08 00:00:00'), pd.Timedelta('5 days 08:00:00'),
                pd.Timedelta('2 days 00:00:00'), 3.25, 2.0, 1.25, 2.5, 0.75, -0.1,
                58.333333333333336, 2.0, 1.3333333333333333, 168.38888888888889,
                -91.08730158730158, 149.25, -86.3670634920635, pd.Timedelta('2 days 00:00:00'),
                pd.Timedelta('1 days 12:00:00'), np.inf, 0.11705555555555548, 0.18931590012681135
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            exit_trades.stats(settings=dict(incl_open=True)),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-08 00:00:00'), pd.Timedelta('5 days 08:00:00'),
                pd.Timedelta('2 days 00:00:00'), 3.25, 2.0, 1.25, 2.5, 0.75, -0.1,
                58.333333333333336, 2.0, 2.3333333333333335, 174.33333333333334,
                -96.25396825396825, 149.25, -42.39781746031746, pd.Timedelta('2 days 00:00:00'),
                pd.Timedelta('1 days 06:00:00'), 7.11951219512195, 0.06359999999999993, 0.07356215977397455
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            exit_trades.stats(column='a'),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-08 00:00:00'), pd.Timedelta('5 days 00:00:00'),
                pd.Timedelta('2 days 00:00:00'), 4, 4, 0, 3, 1, -0.16, 100.0, 3, 0,
                262.0, 14.499999999999998, 149.25, np.nan, pd.Timedelta('2 days 00:00:00'),
                pd.NaT, np.inf, 1.008, 2.181955050824476
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            exit_trades.stats(column='g1', group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-08 00:00:00'), pd.Timedelta('5 days 00:00:00'),
                pd.Timedelta('5 days 00:00:00'), 8, 4, 4, 6, 2, -0.32, 50.0, 3, 3, 262.0,
                -271.3333333333333, 149.25, -156.30555555555557, pd.Timedelta('2 days 00:00:00'),
                pd.Timedelta('2 days 00:00:00'), 0.895734597156398, -0.058666666666666756, -0.10439051512510047
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_index_equal(
            exit_trades.stats(tags='trades').index,
            pd.Index([
                'First Trade Start', 'Last Trade End', 'Total Long Trades',
                'Total Short Trades', 'Total Closed Trades', 'Total Open Trades',
                'Open Trade PnL', 'Win Rate [%]', 'Max Win Streak', 'Max Loss Streak',
                'Best Trade [%]', 'Worst Trade [%]', 'Avg Winning Trade [%]',
                'Avg Losing Trade [%]', 'Avg Winning Trade Duration',
                'Avg Losing Trade Duration', 'Profit Factor', 'Expectancy', 'SQN'
            ], dtype='object')
        )
        pd.testing.assert_series_equal(
            exit_trades['c'].stats(),
            exit_trades.stats(column='c')
        )
        pd.testing.assert_series_equal(
            exit_trades['c'].stats(),
            exit_trades.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            exit_trades_grouped['g2'].stats(),
            exit_trades_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            exit_trades_grouped['g2'].stats(),
            exit_trades.stats(column='g2', group_by=group_by)
        )
        stats_df = exit_trades.stats(agg_func=None)
        assert stats_df.shape == (4, 25)
        pd.testing.assert_index_equal(stats_df.index, exit_trades.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)


entry_trades = vbt.EntryTrades.from_orders(orders)
entry_trades_grouped = vbt.EntryTrades.from_orders(orders_grouped)


class TestEntryTrades:
    def test_records_arr(self):
        record_arrays_close(
            entry_trades.values,
            np.array([
                (0, 0, 1.0, 0, 1.0, 0.01, 3, 3.0909090909090904, 0.03090909090909091, 2.05, 2.05, 0, 1, 0),
                (1, 0, 0.1, 1, 2.0, 0.002, 3, 3.0909090909090904, 0.003090909090909091,
                 0.10399999999999998, 0.5199999999999999, 0, 1, 0),
                (2, 0, 1.0, 5, 6.0, 0.06, 6, 7.0, 0.07, 0.8699999999999999, 0.145, 0, 1, 1),
                (3, 0, 2.0, 7, 8.0, 0.16, 7, 8.0, 0.0, -0.16, -0.01, 0, 0, 2),
                (4, 1, 1.0, 0, 1.0, 0.01, 3, 3.0909090909090904, 0.03090909090909091,
                 -2.131818181818181, -2.131818181818181, 1, 1, 3),
                (5, 1, 0.1, 1, 2.0, 0.002, 3, 3.0909090909090904, 0.003090909090909091,
                 -0.11418181818181816, -0.5709090909090908, 1, 1, 3),
                (6, 1, 1.0, 5, 6.0, 0.06, 6, 7.0, 0.07, -1.1300000000000001, -0.18833333333333335, 1, 1, 4),
                (7, 1, 2.0, 7, 8.0, 0.16, 7, 8.0, 0.0, -0.16, -0.01, 1, 0, 5),
                (8, 2, 1.0, 0, 1.0, 0.01, 3, 3.0909090909090904, 0.03090909090909091, 2.05, 2.05, 0, 1, 6),
                (9, 2, 0.1, 1, 2.0, 0.002, 3, 3.0909090909090904, 0.003090909090909091,
                 0.10399999999999998, 0.5199999999999999, 0, 1, 6),
                (10, 2, 1.0, 5, 6.0, 0.06, 6, 7.0, 0.07, 0.8699999999999999, 0.145, 0, 1, 7),
                (11, 2, 1.0, 6, 7.0, 0.07, 7, 8.0, 0.08, -1.1500000000000001, -0.1642857142857143, 1, 1, 8),
                (12, 2, 1.0, 7, 8.0, 0.08, 7, 8.0, 0.0, -0.08, -0.01, 0, 0, 9)
            ], dtype=trade_dt)
        )
        reversed_col_orders = orders.replace(records_arr=np.concatenate((
            orders.values[orders.values['col'] == 2],
            orders.values[orders.values['col'] == 1],
            orders.values[orders.values['col'] == 0]
        )))
        record_arrays_close(
            vbt.EntryTrades.from_orders(reversed_col_orders).values,
            entry_trades.values
        )

    def test_records_readable(self):
        records_readable = entry_trades.records_readable

        np.testing.assert_array_equal(
            records_readable['Entry Trade Id'].values,
            np.array([
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Position Id'].values,
            np.array([
                0, 0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9
            ])
        )


positions = vbt.Positions.from_trades(exit_trades)
positions_grouped = vbt.Positions.from_trades(exit_trades_grouped)


class TestPositions:
    def test_records_arr(self):
        record_arrays_close(
            positions.values,
            np.array([
                (0, 0, 1.1, 0, 1.09090909, 0.012, 3, 3.09090909, 0.034, 2.154, 1.795, 0, 1, 0),
                (1, 0, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 1),
                (2, 0, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 0, 0, 2),
                (3, 1, 1.1, 0, 1.09090909, 0.012, 3, 3.09090909, 0.034, -2.246, -1.87166667, 1, 1, 3),
                (4, 1, 1., 5, 6., 0.06, 6, 7., 0.07, -1.13, -0.18833333, 1, 1, 4),
                (5, 1, 2., 7, 8., 0.16, 7, 8., 0., -0.16, -0.01, 1, 0, 5),
                (6, 2, 1.1, 0, 1.09090909, 0.012, 3, 3.09090909, 0.034, 2.154, 1.795, 0, 1, 6),
                (7, 2, 1., 5, 6., 0.06, 6, 7., 0.07, 0.87, 0.145, 0, 1, 7),
                (8, 2, 1., 6, 7., 0.07, 7, 8., 0.08, -1.15, -0.16428571, 1, 1, 8),
                (9, 2, 1., 7, 8., 0.08, 7, 8., 0., -0.08, -0.01, 0, 0, 9)
            ], dtype=trade_dt)
        )
        reversed_col_trades = exit_trades.replace(records_arr=np.concatenate((
            exit_trades.values[exit_trades.values['col'] == 2],
            exit_trades.values[exit_trades.values['col'] == 1],
            exit_trades.values[exit_trades.values['col'] == 0]
        )))
        record_arrays_close(
            vbt.Positions.from_trades(reversed_col_trades).values,
            positions.values
        )

    def test_records_readable(self):
        records_readable = positions.records_readable

        np.testing.assert_array_equal(
            records_readable['Position Id'].values,
            np.array([
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9
            ])
        )
        assert 'Parent Id' not in records_readable.columns


# ############# logs.py ############# #

logs = vbt.Portfolio.from_orders(close, size, fees=0.01, log=True, freq='1 days').logs
logs_grouped = logs.regroup(group_by)


class TestLogs:
    def test_mapped_fields(self):
        for name in log_dt.names:
            np.testing.assert_array_equal(
                getattr(logs, name).values,
                logs.values[name]
            )

    def test_records_readable(self):
        records_readable = logs.records_readable

        np.testing.assert_array_equal(
            records_readable['Log Id'].values,
            np.array([
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Timestamp'].values,
            np.array([
                '2020-01-01T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-06T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-06T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-06T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000',
                '2020-01-01T00:00:00.000000000', '2020-01-02T00:00:00.000000000',
                '2020-01-03T00:00:00.000000000', '2020-01-04T00:00:00.000000000',
                '2020-01-05T00:00:00.000000000', '2020-01-06T00:00:00.000000000',
                '2020-01-07T00:00:00.000000000', '2020-01-08T00:00:00.000000000'
            ], dtype='datetime64[ns]')
        )
        np.testing.assert_array_equal(
            records_readable['Column'].values,
            np.array([
                'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c',
                'c', 'c', 'c', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Group'].values,
            np.array([
                0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Cash'].values,
            np.array([
                100.0, 98.99, 98.788, 101.758, 102.154, 102.154, 96.094, 103.024, 100.0, 100.99, 101.18799999999999,
                98.15799999999999, 97.75399999999999, 97.75399999999999, 103.69399999999999, 96.624, 100.0, 98.99,
                98.788, 101.758, 102.154, 102.154, 96.094, 109.954, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                100.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Position'].values,
            np.array([
                0.0, 1.0, 1.1, 0.10000000000000009, 0.0, 0.0, 1.0, 0.0, 0.0, -1.0, -1.1, -0.10000000000000009, 0.0, 0.0,
                -1.0, 0.0, 0.0, 1.0, 1.1, 0.10000000000000009, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Debt'].values,
            np.array([
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.2, 0.10909090909090913, 0.0, 0.0, 6.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Free Cash'].values,
            np.array([
                100.0, 98.99, 98.788, 101.758, 102.154, 102.154, 96.094, 103.024, 100.0, 98.99, 98.788,
                97.93981818181818, 97.754, 97.754, 91.694, 96.624, 100.0, 98.99, 98.788, 101.758, 102.154, 102.154,
                96.094, 95.954, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Val Price'].values,
            np.array([
                1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0,
                6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Value'].values,
            np.array([
                100.0, 100.99, 102.088, 102.158, 102.154, 102.154, 103.094, 103.024, 100.0, 98.99, 97.88799999999999,
                97.75799999999998, 97.75399999999999, 97.75399999999999, 96.69399999999999, 96.624, 100.0, 100.99,
                102.088, 102.158, 102.154, 102.154, 103.094, 101.954, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                100.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Size'].values,
            np.array([
                1.0, 0.1, -1.0, -0.1, np.nan, 1.0, -1.0, 2.0, -1.0, -0.1, 1.0, 0.1, np.nan, -1.0, 1.0, -2.0, 1.0, 0.1,
                -1.0, -0.1, np.nan, 1.0, -2.0, 2.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Price'].values,
            np.array([
                1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0,
                6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Size Type'].values,
            np.array([
                'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount',
                'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount',
                'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount', 'Amount',
                'Amount', 'Amount'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Direction'].values,
            np.array([
                'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both',
                'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both',
                'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both', 'Both'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Fees'].values,
            np.array([
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Fixed Fees'].values,
            np.array([
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Slippage'].values,
            np.array([
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Min Size'].values,
            np.array([
                1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08,
                1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08,
                1e-08, 1e-08
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Max Size'].values,
            np.array([
                np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                np.inf, np.inf, np.inf, np.inf, np.inf, np.inf
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Size Granularity'].values,
            np.array([
                np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Rejection Prob'].values,
            np.array([
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Lock Cash'].values,
            np.array([
                False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Allow Partial'].values,
            np.array([
                True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                True, True, True, True, True, True, True, True, True, True, True, True, True, True, True
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Raise Rejection'].values,
            np.array([
                False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Request Log'].values,
            np.array([
                True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                True, True, True, True, True, True, True, True, True, True, True, True, True, True, True
            ])
        )
        np.testing.assert_array_equal(
            records_readable['New Cash'].values,
            np.array([
                98.99, 98.788, 101.758, 102.154, 102.154, 96.094, 103.024, 86.864, 100.99, 101.18799999999999,
                98.15799999999999, 97.75399999999999, 97.75399999999999, 103.69399999999999, 96.624, 112.464, 98.99,
                98.788, 101.758, 102.154, 102.154, 96.094, 109.954, 93.794, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                100.0, 100.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['New Position'].values,
            np.array([
                1.0, 1.1, 0.10000000000000009, 0.0, 0.0, 1.0, 0.0, 2.0, -1.0, -1.1, -0.10000000000000009, 0.0, 0.0,
                -1.0, 0.0, -2.0, 1.0, 1.1, 0.10000000000000009, 0.0, 0.0, 1.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['New Debt'].values,
            np.array([
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.2, 0.10909090909090913, 0.0, 0.0, 6.0, 0.0, 16.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['New Free Cash'].values,
            np.array([
                98.99, 98.788, 101.758, 102.154, 102.154, 96.094, 103.024, 86.864, 98.99, 98.788, 97.93981818181818,
                97.754, 97.754, 91.694, 96.624, 80.464, 98.99, 98.788, 101.758, 102.154, 102.154, 96.094, 95.954,
                93.794, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['New Val Price'].values,
            np.array([
                1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0,
                6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['New Value'].values,
            np.array([
                100.0, 100.99, 102.088, 102.158, 102.154, 102.154, 103.094, 103.024, 100.0, 98.99, 97.88799999999999,
                97.75799999999998, 97.75399999999999, 97.75399999999999, 96.69399999999999, 96.624, 100.0, 100.99,
                102.088, 102.158, 102.154, 102.154, 103.094, 101.954, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                100.0
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Result Size'].values,
            np.array([
                1.0, 0.1, 1.0, 0.1, np.nan, 1.0, 1.0, 2.0, 1.0, 0.1, 1.0, 0.1, np.nan, 1.0, 1.0, 2.0, 1.0, 0.1, 1.0,
                0.1, np.nan, 1.0, 2.0, 2.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Result Price'].values,
            np.array([
                1.0, 2.0, 3.0, 4.0, np.nan, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0, 4.0, np.nan, 6.0, 7.0, 8.0, 1.0, 2.0, 3.0,
                4.0, np.nan, 6.0, 7.0, 8.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Result Fees'].values,
            np.array([
                0.01, 0.002, 0.03, 0.004, np.nan, 0.06, 0.07, 0.16, 0.01, 0.002, 0.03, 0.004, np.nan, 0.06, 0.07, 0.16,
                0.01, 0.002, 0.03, 0.004, np.nan, 0.06, 0.14, 0.16, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                np.nan, np.nan
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Result Side'].values,
            np.array([
                'Buy', 'Buy', 'Sell', 'Sell', None, 'Buy', 'Sell', 'Buy', 'Sell', 'Sell', 'Buy', 'Buy', None, 'Sell',
                'Buy', 'Sell', 'Buy', 'Buy', 'Sell', 'Sell', None, 'Buy', 'Sell', 'Buy', None, None, None, None, None,
                None, None, None
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Result Status'].values,
            np.array([
                'Filled', 'Filled', 'Filled', 'Filled', 'Ignored', 'Filled', 'Filled', 'Filled', 'Filled', 'Filled',
                'Filled', 'Filled', 'Ignored', 'Filled', 'Filled', 'Filled', 'Filled', 'Filled', 'Filled', 'Filled',
                'Ignored', 'Filled', 'Filled', 'Filled', 'Ignored', 'Ignored', 'Ignored', 'Ignored', 'Ignored',
                'Ignored', 'Ignored', 'Ignored'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Result Status Info'].values,
            np.array([
                None, None, None, None, 'SizeNaN', None, None, None, None, None, None, None, 'SizeNaN', None, None,
                None, None, None, None, None, 'SizeNaN', None, None, None, 'SizeNaN', 'SizeNaN', 'SizeNaN', 'SizeNaN',
                'SizeNaN', 'SizeNaN', 'SizeNaN', 'SizeNaN'
            ])
        )
        np.testing.assert_array_equal(
            records_readable['Order Id'].values,
            np.array([
                0, 1, 2, 3, -1, 4, 5, 6, 7, 8, 9, 10, -1, 11, 12, 13, 14, 15, 16, 17, -1, 18, 19, 20, -1, -1, -1, -1,
                -1, -1, -1, -1
            ])
        )

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Total Records', 'Status Counts: None',
            'Status Counts: Filled', 'Status Counts: Ignored',
            'Status Counts: Rejected', 'Status Info Counts: None',
            'Status Info Counts: SizeNaN'
        ], dtype='object')
        pd.testing.assert_series_equal(
            logs.stats(),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), 8.0, 0.0, 5.25, 2.75, 0.0, 5.25, 2.75
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            logs.stats(column='a'),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), 8, 0, 7, 1, 0, 7, 1
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            logs.stats(column='g1', group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-08 00:00:00'),
                pd.Timedelta('8 days 00:00:00'), 16, 0, 14, 2, 0, 14, 2
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            logs['c'].stats(),
            logs.stats(column='c')
        )
        pd.testing.assert_series_equal(
            logs['c'].stats(),
            logs.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            logs_grouped['g2'].stats(),
            logs_grouped.stats(column='g2')
        )
        pd.testing.assert_series_equal(
            logs_grouped['g2'].stats(),
            logs.stats(column='g2', group_by=group_by)
        )
        stats_df = logs.stats(agg_func=None)
        assert stats_df.shape == (4, 10)
        pd.testing.assert_index_equal(stats_df.index, logs.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)

    def test_count(self):
        assert logs['a'].count() == 8
        pd.testing.assert_series_equal(
            logs.count(),
            pd.Series(
                np.array([8, 8, 8, 8]),
                index=pd.Index(['a', 'b', 'c', 'd'], dtype='object')
            ).rename('count')
        )
        pd.testing.assert_series_equal(
            logs_grouped.count(),
            pd.Series(
                np.array([16, 16]),
                index=pd.Index(['g1', 'g2'], dtype='object')
            ).rename('count')
        )
