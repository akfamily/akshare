from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from numba import njit

import vectorbt as vbt
from tests.utils import record_arrays_close
from vectorbt.generic import nb as generic_nb
from vectorbt.generic.enums import range_dt

seed = 42

day_dt = np.timedelta64(86400000000000)

mask = pd.DataFrame([
    [True, False, False],
    [False, True, False],
    [False, False, True],
    [True, False, False],
    [False, True, False]
], index=pd.Index([
    datetime(2020, 1, 1),
    datetime(2020, 1, 2),
    datetime(2020, 1, 3),
    datetime(2020, 1, 4),
    datetime(2020, 1, 5)
]), columns=['a', 'b', 'c'])

ts = pd.Series([1., 2., 3., 2., 1.], index=mask.index)

price = pd.DataFrame({
    'open': [10, 11, 12, 11, 10],
    'high': [11, 12, 13, 12, 11],
    'low': [9, 10, 11, 10, 9],
    'close': [11, 12, 11, 10, 9]
})

group_by = pd.Index(['g1', 'g1', 'g2'])


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []


def teardown_module():
    vbt.settings.reset()


# ############# accessors.py ############# #


class TestAccessors:
    def test_indexing(self):
        assert mask.vbt.signals['a'].total() == mask['a'].vbt.signals.total()

    def test_freq(self):
        assert mask.vbt.signals.wrapper.freq == day_dt
        assert mask['a'].vbt.signals.wrapper.freq == day_dt
        assert mask.vbt.signals(freq='2D').wrapper.freq == day_dt * 2
        assert mask['a'].vbt.signals(freq='2D').wrapper.freq == day_dt * 2
        assert pd.Series([False, True]).vbt.signals.wrapper.freq is None
        assert pd.Series([False, True]).vbt.signals(freq='3D').wrapper.freq == day_dt * 3
        assert pd.Series([False, True]).vbt.signals(freq=np.timedelta64(4, 'D')).wrapper.freq == day_dt * 4

    @pytest.mark.parametrize(
        "test_n",
        [1, 2, 3, 4, 5],
    )
    def test_fshift(self, test_n):
        pd.testing.assert_series_equal(mask['a'].vbt.signals.fshift(test_n), mask['a'].shift(test_n, fill_value=False))
        np.testing.assert_array_equal(
            mask['a'].vbt.signals.fshift(test_n).values,
            generic_nb.fshift_1d_nb(mask['a'].values, test_n, fill_value=False)
        )
        pd.testing.assert_frame_equal(mask.vbt.signals.fshift(test_n), mask.shift(test_n, fill_value=False))

    @pytest.mark.parametrize(
        "test_n",
        [1, 2, 3, 4, 5],
    )
    def test_bshift(self, test_n):
        pd.testing.assert_series_equal(
            mask['a'].vbt.signals.bshift(test_n),
            mask['a'].shift(-test_n, fill_value=False))
        np.testing.assert_array_equal(
            mask['a'].vbt.signals.bshift(test_n).values,
            generic_nb.bshift_1d_nb(mask['a'].values, test_n, fill_value=False)
        )
        pd.testing.assert_frame_equal(mask.vbt.signals.bshift(test_n), mask.shift(-test_n, fill_value=False))

    def test_empty(self):
        pd.testing.assert_series_equal(
            pd.Series.vbt.signals.empty(5, index=np.arange(10, 15), name='a'),
            pd.Series(np.full(5, False), index=np.arange(10, 15), name='a')
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.empty((5, 3), index=np.arange(10, 15), columns=['a', 'b', 'c']),
            pd.DataFrame(np.full((5, 3), False), index=np.arange(10, 15), columns=['a', 'b', 'c'])
        )
        pd.testing.assert_series_equal(
            pd.Series.vbt.signals.empty_like(mask['a']),
            pd.Series(np.full(mask['a'].shape, False), index=mask['a'].index, name=mask['a'].name)
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.empty_like(mask),
            pd.DataFrame(np.full(mask.shape, False), index=mask.index, columns=mask.columns)
        )

    def test_generate(self):
        @njit
        def choice_func_nb(from_i, to_i, col, n):
            if col == 0:
                return np.arange(from_i, to_i)
            elif col == 1:
                return np.full(1, from_i)
            else:
                return np.full(1, to_i - n)

        pd.testing.assert_series_equal(
            pd.Series.vbt.signals.generate(5, choice_func_nb, 1, index=mask['a'].index, name=mask['a'].name),
            pd.Series(
                np.array([True, True, True, True, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        with pytest.raises(Exception):
            _ = pd.Series.vbt.signals.generate((5, 2), choice_func_nb, 1)
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate(
                (5, 3), choice_func_nb, 1, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [True, True, False],
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                    [True, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate(
                (5, 3), choice_func_nb, 1, pick_first=True, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [True, True, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_generate_both(self):
        @njit
        def entry_func_nb(from_i, to_i, col, temp_int):
            temp_int[0] = from_i
            return temp_int[:1]

        @njit
        def exit_func_nb(from_i, to_i, col, temp_int):
            temp_int[0] = from_i
            return temp_int[:1]

        temp_int = np.empty((mask.shape[0],), dtype=np.int64)

        en, ex = pd.Series.vbt.signals.generate_both(
            5, entry_func_nb, (temp_int,), exit_func_nb, (temp_int,),
            index=mask['a'].index, name=mask['a'].name)
        pd.testing.assert_series_equal(
            en,
            pd.Series(
                np.array([True, False, True, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(
                np.array([False, True, False, True, False]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_both(
            (5, 3), entry_func_nb, (temp_int,), exit_func_nb, (temp_int,),
            index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                    [True, True, True],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.Series.vbt.signals.generate_both(
            (5,), entry_func_nb, (temp_int,), exit_func_nb, (temp_int,),
            index=mask['a'].index, name=mask['a'].name, entry_wait=1, exit_wait=0)
        pd.testing.assert_series_equal(
            en,
            pd.Series(
                np.array([True, True, True, True, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(
                np.array([True, True, True, True, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        en, ex = pd.Series.vbt.signals.generate_both(
            (5,), entry_func_nb, (temp_int,), exit_func_nb, (temp_int,),
            index=mask['a'].index, name=mask['a'].name, entry_wait=0, exit_wait=1)
        pd.testing.assert_series_equal(
            en,
            pd.Series(
                np.array([True, True, True, True, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(
                np.array([False, True, True, True, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )

        @njit
        def entry_func2_nb(from_i, to_i, col, temp_int):
            temp_int[0] = from_i
            if from_i + 1 < to_i:
                temp_int[1] = from_i + 1
                return temp_int[:2]
            return temp_int[:1]

        @njit
        def exit_func2_nb(from_i, to_i, col, temp_int):
            temp_int[0] = from_i
            if from_i + 1 < to_i:
                temp_int[1] = from_i + 1
                return temp_int[:2]
            return temp_int[:1]

        en, ex = pd.DataFrame.vbt.signals.generate_both(
            (5, 3), entry_func2_nb, (temp_int,), exit_func2_nb, (temp_int,),
            entry_pick_first=False, exit_pick_first=False,
            index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True],
                    [False, False, False],
                    [False, False, False],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [True, True, True],
                    [True, True, True],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_generate_exits(self):
        @njit
        def choice_func_nb(from_i, to_i, col, temp_int):
            temp_int[0] = from_i
            return temp_int[:1]

        temp_int = np.empty((mask.shape[0],), dtype=np.int64)

        pd.testing.assert_series_equal(
            mask['a'].vbt.signals.generate_exits(choice_func_nb, temp_int),
            pd.Series(
                np.array([False, True, False, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_exits(choice_func_nb, temp_int),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_exits(choice_func_nb, temp_int, wait=0),
            pd.DataFrame(
                np.array([
                    [True, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, False, False],
                    [False, True, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

        @njit
        def choice_func2_nb(from_i, to_i, col, temp_int):
            for i in range(from_i, to_i):
                temp_int[i - from_i] = i
            return temp_int[:to_i - from_i]

        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_exits(choice_func2_nb, temp_int, until_next=False, pick_first=False),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [True, True, False],
                    [True, True, True],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

        mask2 = pd.Series([True, True, True, True, True], index=mask.index)
        pd.testing.assert_series_equal(
            mask2.vbt.signals.generate_exits(choice_func_nb, temp_int, until_next=False, skip_until_exit=True),
            pd.Series(
                np.array([False, True, False, True, False]),
                index=mask.index
            )
        )

    def test_clean(self):
        entries = pd.DataFrame([
            [True, False, True],
            [True, False, False],
            [True, True, True],
            [False, True, False],
            [False, True, True]
        ], index=mask.index, columns=mask.columns)
        exits = pd.Series([True, False, True, False, True], index=mask.index)
        pd.testing.assert_frame_equal(
            entries.vbt.signals.clean(),
            pd.DataFrame(
                np.array([
                    [True, False, True],
                    [False, False, False],
                    [False, True, True],
                    [False, False, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.clean(entries),
            pd.DataFrame(
                np.array([
                    [True, False, True],
                    [False, False, False],
                    [False, True, True],
                    [False, False, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            entries.vbt.signals.clean(exits)[0],
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [False, False, False],
                    [False, True, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            entries.vbt.signals.clean(exits)[1],
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            entries.vbt.signals.clean(exits, entry_first=False)[0],
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [False, False, False],
                    [False, True, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            entries.vbt.signals.clean(exits, entry_first=False)[1],
            pd.DataFrame(
                np.array([
                    [False, True, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.clean(entries, exits)[0],
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [False, False, False],
                    [False, True, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.clean(entries, exits)[1],
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        with pytest.raises(Exception):
            _ = pd.Series.vbt.signals.clean(entries, entries, entries)

    def test_generate_random(self):
        pd.testing.assert_series_equal(
            pd.Series.vbt.signals.generate_random(
                5, n=3, seed=seed, index=mask['a'].index, name=mask['a'].name),
            pd.Series(
                np.array([False, True, True, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        with pytest.raises(Exception):
            _ = pd.Series.vbt.signals.generate_random((5, 2), n=3)
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate_random(
                (5, 3), n=3, seed=seed, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [False, False, True],
                    [True, True, True],
                    [True, True, False],
                    [False, True, True],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate_random(
                (5, 3), n=[0, 1, 2], seed=seed, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [False, False, True],
                    [False, False, True],
                    [False, False, False],
                    [False, True, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_series_equal(
            pd.Series.vbt.signals.generate_random(
                5, prob=0.5, seed=seed, index=mask['a'].index, name=mask['a'].name),
            pd.Series(
                np.array([True, False, False, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        with pytest.raises(Exception):
            _ = pd.Series.vbt.signals.generate_random((5, 2), prob=3)
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate_random(
                (5, 3), prob=0.5, seed=seed, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [False, True, False],
                    [False, False, False],
                    [False, False, True],
                    [True, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate_random(
                (5, 3), prob=[0., 0.5, 1.], seed=seed, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [False, True, True],
                    [False, True, True],
                    [False, False, True],
                    [False, False, True],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        with pytest.raises(Exception):
            pd.DataFrame.vbt.signals.generate_random((5, 3))
        pd.testing.assert_frame_equal(
            pd.DataFrame.vbt.signals.generate_random(
                (5, 3), prob=[0., 0.5, 1.], pick_first=True, seed=seed, index=mask.index, columns=mask.columns),
            pd.DataFrame(
                np.array([
                    [False, True, True],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_generate_random_both(self):
        # n
        en, ex = pd.Series.vbt.signals.generate_random_both(
            5, n=2, seed=seed, index=mask['a'].index, name=mask['a'].name)
        pd.testing.assert_series_equal(
            en,
            pd.Series(
                np.array([True, False, True, False, False]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(
                np.array([False, True, False, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), n=2, seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [False, False, False],
                    [True, True, False],
                    [False, False, True],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                    [False, True, False],
                    [True, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), n=[0, 1, 2], seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [False, False, True],
                    [False, True, False],
                    [False, False, False],
                    [False, False, True],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, True],
                    [False, False, False],
                    [False, True, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both((2, 3), n=2, seed=seed, entry_wait=1, exit_wait=0)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True],
                ])
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True]
                ])
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both((3, 3), n=2, seed=seed, entry_wait=0, exit_wait=1)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True],
                    [False, False, False]
                ])
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, True, True],
                    [True, True, True],
                ])
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both((7, 3), n=2, seed=seed, entry_wait=2, exit_wait=2)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                    [False, False, False]
                ])
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [True, True, True]
                ])
            )
        )
        n = 10
        a = np.full(n * 2, 0.)
        for i in range(10000):
            en, ex = pd.Series.vbt.signals.generate_random_both(1000, n, entry_wait=2, exit_wait=2)
            _a = np.empty((n * 2,), dtype=np.int64)
            _a[0::2] = np.flatnonzero(en)
            _a[1::2] = np.flatnonzero(ex)
            a += _a
        greater = a > 10000000 / (2 * n + 1) * np.arange(0, 2 * n)
        less = a < 10000000 / (2 * n + 1) * np.arange(2, 2 * n + 2)
        assert np.all(greater & less)

        # probs
        en, ex = pd.Series.vbt.signals.generate_random_both(
            5, entry_prob=0.5, exit_prob=1., seed=seed, index=mask['a'].index, name=mask['a'].name)
        pd.testing.assert_series_equal(
            en,
            pd.Series(
                np.array([True, False, False, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(
                np.array([False, True, False, False, False]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), entry_prob=0.5, exit_prob=1., seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [False, False, False],
                    [False, False, False],
                    [False, False, True],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, True, True],
                    [False, False, False],
                    [False, False, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), entry_prob=[0., 0.5, 1.], exit_prob=[0., 0.5, 1.],
            seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [False, True, True],
                    [False, False, False],
                    [False, False, True],
                    [False, False, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, True, True],
                    [False, False, False],
                    [False, False, True],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), entry_prob=1., exit_prob=1., exit_wait=0,
            seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), entry_prob=1., exit_prob=1., entry_pick_first=False, exit_pick_first=True,
            seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        en, ex = pd.DataFrame.vbt.signals.generate_random_both(
            (5, 3), entry_prob=1., exit_prob=1., entry_pick_first=True, exit_pick_first=False,
            seed=seed, index=mask.index, columns=mask.columns)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(
                np.array([
                    [True, True, True],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True],
                    [True, True, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        # none
        with pytest.raises(Exception):
            pd.DataFrame.vbt.signals.generate_random((5, 3))

    def test_generate_random_exits(self):
        pd.testing.assert_series_equal(
            mask['a'].vbt.signals.generate_random_exits(seed=seed),
            pd.Series(
                np.array([False, False, True, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_random_exits(seed=seed),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [True, True, False],
                    [False, False, False],
                    [True, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_random_exits(seed=seed, wait=0),
            pd.DataFrame(
                np.array([
                    [True, False, False],
                    [False, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, True, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_series_equal(
            mask['a'].vbt.signals.generate_random_exits(prob=1., seed=seed),
            pd.Series(
                np.array([False, True, False, False, True]),
                index=mask['a'].index,
                name=mask['a'].name
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_random_exits(prob=1., seed=seed),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_random_exits(prob=[0., 0.5, 1.], seed=seed),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, True, True],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_random_exits(prob=1., wait=0, seed=seed),
            pd.DataFrame(
                np.array([
                    [True, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, False, False],
                    [False, True, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_random_exits(prob=1., until_next=False, seed=seed),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [True, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_generate_stop_exits(self):
        e = pd.Series([True, False, False, False, False, False])
        t = pd.Series([2, 3, 4, 3, 2, 1]).astype(np.float64)

        # stop loss
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(t, -0.1),
            pd.Series(np.array([False, False, False, False, False, True]))
        )
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(t, -0.1, trailing=True),
            pd.Series(np.array([False, False, False, True, False, False]))
        )
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(t, -0.1, trailing=True, pick_first=False),
            pd.Series(np.array([False, False, False, True, True, True]))
        )
        pd.testing.assert_frame_equal(
            e.vbt.signals.generate_stop_exits(t.vbt.tile(3), [np.nan, -0.5, -1.], trailing=True, pick_first=False),
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, True, False],
                [False, True, False]
            ]))
        )
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(t, -0.1, trailing=True, exit_wait=3),
            pd.Series(np.array([False, False, False, False, True, False]))
        )
        # take profit
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(4 - t, 0.1),
            pd.Series(np.array([False, False, False, False, False, True]))
        )
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(4 - t, 0.1, trailing=True),
            pd.Series(np.array([False, False, False, True, False, False]))
        )
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(4 - t, 0.1, trailing=True, pick_first=False),
            pd.Series(np.array([False, False, False, True, True, True]))
        )
        pd.testing.assert_frame_equal(
            e.vbt.signals.generate_stop_exits((4 - t).vbt.tile(3), [np.nan, 0.5, 1.], trailing=True, pick_first=False),
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, True, True],
                [False, True, True],
                [False, True, True]
            ]))
        )
        pd.testing.assert_series_equal(
            e.vbt.signals.generate_stop_exits(4 - t, 0.1, trailing=True, exit_wait=3),
            pd.Series(np.array([False, False, False, False, True, False]))
        )
        # chain
        e = pd.Series([True, True, True, True, True, True])
        en, ex = e.vbt.signals.generate_stop_exits(t, -0.1, trailing=True, chain=True)
        pd.testing.assert_series_equal(
            en,
            pd.Series(np.array([True, False, False, False, True, False]))
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(np.array([False, False, False, True, False, True]))
        )
        en, ex = e.vbt.signals.generate_stop_exits(t, -0.1, trailing=True, entry_wait=2, chain=True)
        pd.testing.assert_series_equal(
            en,
            pd.Series(np.array([True, False, False, False, False, True]))
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(np.array([False, False, False, True, False, False]))
        )
        en, ex = e.vbt.signals.generate_stop_exits(t, -0.1, trailing=True, exit_wait=2, chain=True)
        pd.testing.assert_series_equal(
            en,
            pd.Series(np.array([True, False, False, False, True, False]))
        )
        pd.testing.assert_series_equal(
            ex,
            pd.Series(np.array([False, False, False, True, False, False]))
        )
        # until_next and pick_first
        e2 = pd.Series([True, True, True, True, True, True])
        t2 = pd.Series([6, 5, 4, 3, 2, 1]).astype(np.float64)
        ex = e2.vbt.signals.generate_stop_exits(t2, -0.1, until_next=False, pick_first=False)
        pd.testing.assert_series_equal(
            ex,
            pd.Series(np.array([False, True, True, True, True, True]))
        )

    def test_generate_ohlc_stop_exits(self):
        with pytest.raises(Exception):
            _ = mask.vbt.signals.generate_ohlc_stop_exits(ts, sl_stop=-0.1)
        with pytest.raises(Exception):
            _ = mask.vbt.signals.generate_ohlc_stop_exits(ts, tp_stop=-0.1)

        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_stop_exits(ts, -0.1),
            mask.vbt.signals.generate_ohlc_stop_exits(ts, sl_stop=0.1)
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_stop_exits(ts, -0.1, trailing=True),
            mask.vbt.signals.generate_ohlc_stop_exits(ts, sl_stop=0.1, sl_trail=True)
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_stop_exits(ts, 0.1),
            mask.vbt.signals.generate_ohlc_stop_exits(ts, tp_stop=0.1)
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_stop_exits(ts, 0.1),
            mask.vbt.signals.generate_ohlc_stop_exits(ts, sl_stop=0.1, reverse=True)
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_stop_exits(ts, 0.1, trailing=True),
            mask.vbt.signals.generate_ohlc_stop_exits(ts, sl_stop=0.1, sl_trail=True, reverse=True)
        )
        pd.testing.assert_frame_equal(
            mask.vbt.signals.generate_stop_exits(ts, -0.1),
            mask.vbt.signals.generate_ohlc_stop_exits(ts, tp_stop=0.1, reverse=True)
        )

        def _test_ohlc_stop_exits(**kwargs):
            out_dict = {'stop_price': np.nan, 'stop_type': -1}
            result = mask.vbt.signals.generate_ohlc_stop_exits(
                price['open'], price['high'], price['low'], price['close'],
                out_dict=out_dict, **kwargs
            )
            if isinstance(result, tuple):
                _, ex = result
            else:
                ex = result
            return result, out_dict['stop_price'], out_dict['stop_type']

        ex, stop_price, stop_type = _test_ohlc_stop_exits()
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, False, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1]
            ]), index=mask.index, columns=mask.columns)
        )
        ex, stop_price, stop_type = _test_ohlc_stop_exits(sl_stop=0.1)
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, False, True],
                [True, False, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, 10.8],
                [9.9, np.nan, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, 0],
                [0, -1, -1]
            ]), index=mask.index, columns=mask.columns)
        )
        ex, stop_price, stop_type = _test_ohlc_stop_exits(sl_stop=0.1, sl_trail=True)
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, True, True],
                [True, False, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, 11.7, 10.8],
                [9.9, np.nan, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, 1, 1],
                [1, -1, -1]
            ]), index=mask.index, columns=mask.columns)
        )
        ex, stop_price, stop_type = _test_ohlc_stop_exits(tp_stop=0.1)
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [True, False, False],
                [False, True, False],
                [False, False, False],
                [False, False, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [11.0, np.nan, np.nan],
                [np.nan, 12.1, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [2, -1, -1],
                [-1, 2, -1],
                [-1, -1, -1],
                [-1, -1, -1]
            ]), index=mask.index, columns=mask.columns)
        )
        ex, stop_price, stop_type = _test_ohlc_stop_exits(sl_stop=0.1, sl_trail=True, tp_stop=0.1)
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [True, False, False],
                [False, True, False],
                [False, False, True],
                [True, False, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [11.0, np.nan, np.nan],
                [np.nan, 12.1, np.nan],
                [np.nan, np.nan, 10.8],
                [9.9, np.nan, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [2, -1, -1],
                [-1, 2, -1],
                [-1, -1, 1],
                [1, -1, -1]
            ]), index=mask.index, columns=mask.columns)
        )
        ex, stop_price, stop_type = _test_ohlc_stop_exits(
            sl_stop=[np.nan, 0.1, 0.2], sl_trail=True, tp_stop=[np.nan, 0.1, 0.2])
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, True, False],
                [False, False, False],
                [False, False, True]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, 12.1, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, 9.6]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, 2, -1],
                [-1, -1, -1],
                [-1, -1, 1]
            ]), index=mask.index, columns=mask.columns)
        )
        ex, stop_price, stop_type = _test_ohlc_stop_exits(sl_stop=0.1, sl_trail=True, tp_stop=0.1, exit_wait=0)
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [True, False, False],
                [False, False, False],
                [False, True, False],
                [False, False, True],
                [True, True, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [9.0, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, 12.1, np.nan],
                [np.nan, np.nan, 11.7],
                [10.8, 9.0, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [1, -1, -1],
                [-1, -1, -1],
                [-1, 2, -1],
                [-1, -1, 1],
                [1, 1, -1]
            ]), index=mask.index, columns=mask.columns)
        )
        (en, ex), stop_price, stop_type = _test_ohlc_stop_exits(
            sl_stop=0.1, sl_trail=True, tp_stop=0.1, chain=True)
        pd.testing.assert_frame_equal(
            en,
            pd.DataFrame(np.array([
                [True, False, False],
                [False, True, False],
                [False, False, True],
                [True, False, False],
                [False, True, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            ex,
            pd.DataFrame(np.array([
                [False, False, False],
                [True, False, False],
                [False, True, False],
                [False, False, True],
                [True, False, False]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [11.0, np.nan, np.nan],
                [np.nan, 12.1, np.nan],
                [np.nan, np.nan, 10.8],
                [9.9, np.nan, np.nan]
            ]), index=mask.index, columns=mask.columns)
        )
        pd.testing.assert_frame_equal(
            stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [2, -1, -1],
                [-1, 2, -1],
                [-1, -1, 1],
                [1, -1, -1]
            ]), index=mask.index, columns=mask.columns)
        )

    def test_between_ranges(self):
        ranges = mask.vbt.signals.between_ranges()
        record_arrays_close(
            ranges.values,
            np.array([
                (0, 0, 0, 3, 1), (1, 1, 1, 4, 1)
            ], dtype=range_dt)
        )
        assert ranges.wrapper == mask.vbt.wrapper

        mask2 = pd.DataFrame([
            [True, True, True],
            [True, True, True],
            [False, False, False],
            [False, False, False],
            [False, False, False]
        ], index=mask.index, columns=mask.columns)

        other_mask = pd.DataFrame([
            [False, False, False],
            [True, False, False],
            [True, True, False],
            [False, True, True],
            [False, False, True]
        ], index=mask.index, columns=mask.columns)

        ranges = mask2.vbt.signals.between_ranges(other=other_mask)
        record_arrays_close(
            ranges.values,
            np.array([
                (0, 0, 0, 1, 1), (1, 0, 1, 1, 1), (2, 1, 0, 2, 1),
                (3, 1, 1, 2, 1), (4, 2, 0, 3, 1), (5, 2, 1, 3, 1)
            ], dtype=range_dt)
        )
        assert ranges.wrapper == mask2.vbt.wrapper

        ranges = mask2.vbt.signals.between_ranges(other=other_mask, from_other=True)
        record_arrays_close(
            ranges.values,
            np.array([
                (0, 0, 1, 1, 1), (1, 0, 1, 2, 1), (2, 1, 1, 2, 1),
                (3, 1, 1, 3, 1), (4, 2, 1, 3, 1), (5, 2, 1, 4, 1)
            ], dtype=range_dt)
        )
        assert ranges.wrapper == mask2.vbt.wrapper

    def test_partition_ranges(self):
        mask2 = pd.DataFrame([
            [False, False, False],
            [True, False, False],
            [True, True, False],
            [False, True, True],
            [True, False, True]
        ], index=mask.index, columns=mask.columns)

        ranges = mask2.vbt.signals.partition_ranges()
        record_arrays_close(
            ranges.values,
            np.array([
                (0, 0, 1, 3, 1), (1, 0, 4, 4, 0), (2, 1, 2, 4, 1), (3, 2, 3, 4, 0)
            ], dtype=range_dt)
        )
        assert ranges.wrapper == mask2.vbt.wrapper

    def test_between_partition_ranges(self):
        mask2 = pd.DataFrame([
            [True, False, False],
            [True, True, False],
            [False, True, True],
            [True, False, True],
            [False, True, False]
        ], index=mask.index, columns=mask.columns)

        ranges = mask2.vbt.signals.between_partition_ranges()
        record_arrays_close(
            ranges.values,
            np.array([
                (0, 0, 1, 3, 1), (1, 1, 2, 4, 1)
            ], dtype=range_dt)
        )
        assert ranges.wrapper == mask2.vbt.wrapper

    def test_pos_rank(self):
        pd.testing.assert_series_equal(
            (~mask['a']).vbt.signals.pos_rank(),
            pd.Series([-1, 0, 1, -1, 0], index=mask['a'].index, name=mask['a'].name)
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.pos_rank(),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 1],
                    [1, 0, -1],
                    [-1, 1, 0],
                    [0, -1, 1]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.pos_rank(after_false=True),
            pd.DataFrame(
                np.array([
                    [-1, -1, -1],
                    [0, -1, -1],
                    [1, 0, -1],
                    [-1, 1, 0],
                    [0, -1, 1]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.pos_rank(allow_gaps=True),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 1],
                    [1, 1, -1],
                    [-1, 2, 2],
                    [2, -1, 3]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.pos_rank(reset_by=mask['a'], allow_gaps=True),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 1],
                    [1, 1, -1],
                    [-1, 0, 0],
                    [0, -1, 1]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.pos_rank(reset_by=mask, allow_gaps=True),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 1],
                    [1, 0, -1],
                    [-1, 1, 0],
                    [0, -1, 1]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_partition_pos_rank(self):
        pd.testing.assert_series_equal(
            (~mask['a']).vbt.signals.partition_pos_rank(),
            pd.Series([-1, 0, 0, -1, 1], index=mask['a'].index, name=mask['a'].name)
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.partition_pos_rank(),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 0],
                    [0, 1, -1],
                    [-1, 1, 1],
                    [1, -1, 1]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.partition_pos_rank(after_false=True),
            pd.DataFrame(
                np.array([
                    [-1, -1, -1],
                    [0, -1, -1],
                    [0, 0, -1],
                    [-1, 0, 0],
                    [1, -1, 0]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.partition_pos_rank(reset_by=mask['a']),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 0],
                    [0, 1, -1],
                    [-1, 0, 0],
                    [0, -1, 0]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.partition_pos_rank(reset_by=mask),
            pd.DataFrame(
                np.array([
                    [-1, 0, 0],
                    [0, -1, 0],
                    [0, 0, -1],
                    [-1, 0, 0],
                    [0, -1, 0]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_pos_rank_fns(self):
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.first(),
            pd.DataFrame(
                np.array([
                    [False, True, True],
                    [True, False, False],
                    [False, True, False],
                    [False, False, True],
                    [True, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.nth(1),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, True],
                    [True, False, False],
                    [False, True, False],
                    [False, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.nth(2),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False],
                    [False, False, False]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )
        pd.testing.assert_frame_equal(
            (~mask).vbt.signals.from_nth(0),
            pd.DataFrame(
                np.array([
                    [False, True, True],
                    [True, False, True],
                    [True, True, False],
                    [False, True, True],
                    [True, False, True]
                ]),
                index=mask.index,
                columns=mask.columns
            )
        )

    def test_pos_rank_mapped(self):
        mask2 = pd.DataFrame([
            [True, False, False],
            [True, True, False],
            [False, True, True],
            [True, False, True],
            [False, True, False]
        ], index=mask.index, columns=mask.columns)

        mapped = mask2.vbt.signals.pos_rank_mapped()
        np.testing.assert_array_equal(
            mapped.values,
            np.array([0, 1, 0, 0, 1, 0, 0, 1])
        )
        np.testing.assert_array_equal(
            mapped.col_arr,
            np.array([0, 0, 0, 1, 1, 1, 2, 2])
        )
        np.testing.assert_array_equal(
            mapped.idx_arr,
            np.array([0, 1, 3, 1, 2, 4, 2, 3])
        )
        assert mapped.wrapper == mask2.vbt.wrapper

    def test_partition_pos_rank_mapped(self):
        mask2 = pd.DataFrame([
            [True, False, False],
            [True, True, False],
            [False, True, True],
            [True, False, True],
            [False, True, False]
        ], index=mask.index, columns=mask.columns)

        mapped = mask2.vbt.signals.partition_pos_rank_mapped()
        np.testing.assert_array_equal(
            mapped.values,
            np.array([0, 0, 1, 0, 0, 1, 0, 0])
        )
        np.testing.assert_array_equal(
            mapped.col_arr,
            np.array([0, 0, 0, 1, 1, 1, 2, 2])
        )
        np.testing.assert_array_equal(
            mapped.idx_arr,
            np.array([0, 1, 3, 1, 2, 4, 2, 3])
        )
        assert mapped.wrapper == mask2.vbt.wrapper

    def test_nth_index(self):
        assert mask['a'].vbt.signals.nth_index(0) == pd.Timestamp('2020-01-01 00:00:00')
        pd.testing.assert_series_equal(
            mask.vbt.signals.nth_index(0),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-02 00:00:00'),
                pd.Timestamp('2020-01-03 00:00:00')
            ], index=mask.columns, name='nth_index', dtype='datetime64[ns]')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.nth_index(-1),
            pd.Series([
                pd.Timestamp('2020-01-04 00:00:00'),
                pd.Timestamp('2020-01-05 00:00:00'),
                pd.Timestamp('2020-01-03 00:00:00')
            ], index=mask.columns, name='nth_index', dtype='datetime64[ns]')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.nth_index(-2),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-02 00:00:00'),
                np.nan
            ], index=mask.columns, name='nth_index', dtype='datetime64[ns]')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.nth_index(0, group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-03 00:00:00')
            ], index=['g1', 'g2'], name='nth_index', dtype='datetime64[ns]')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.nth_index(-1, group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-05 00:00:00'),
                pd.Timestamp('2020-01-03 00:00:00')
            ], index=['g1', 'g2'], name='nth_index', dtype='datetime64[ns]')
        )

    def test_norm_avg_index(self):
        assert mask['a'].vbt.signals.norm_avg_index() == -0.25
        pd.testing.assert_series_equal(
            mask.vbt.signals.norm_avg_index(),
            pd.Series([-0.25, 0.25, 0.0], index=mask.columns, name='norm_avg_index')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.norm_avg_index(group_by=group_by),
            pd.Series([0.0, 0.0], index=['g1', 'g2'], name='norm_avg_index')
        )

    def test_index_mapped(self):
        mapped = mask.vbt.signals.index_mapped()
        np.testing.assert_array_equal(
            mapped.values,
            np.array([0, 3, 1, 4, 2])
        )
        np.testing.assert_array_equal(
            mapped.col_arr,
            np.array([0, 0, 1, 1, 2])
        )
        np.testing.assert_array_equal(
            mapped.idx_arr,
            np.array([0, 3, 1, 4, 2])
        )
        assert mapped.wrapper == mask.vbt.wrapper

    def test_total(self):
        assert mask['a'].vbt.signals.total() == 2
        pd.testing.assert_series_equal(
            mask.vbt.signals.total(),
            pd.Series([2, 2, 1], index=mask.columns, name='total')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.total(group_by=group_by),
            pd.Series([4, 1], index=['g1', 'g2'], name='total')
        )

    def test_rate(self):
        assert mask['a'].vbt.signals.rate() == 0.4
        pd.testing.assert_series_equal(
            mask.vbt.signals.rate(),
            pd.Series([0.4, 0.4, 0.2], index=mask.columns, name='rate')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.rate(group_by=group_by),
            pd.Series([0.4, 0.2], index=['g1', 'g2'], name='rate')
        )

    def test_total_partitions(self):
        assert mask['a'].vbt.signals.total_partitions() == 2
        pd.testing.assert_series_equal(
            mask.vbt.signals.total_partitions(),
            pd.Series([2, 2, 1], index=mask.columns, name='total_partitions')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.total_partitions(group_by=group_by),
            pd.Series([4, 1], index=['g1', 'g2'], name='total_partitions')
        )

    def test_partition_rate(self):
        assert mask['a'].vbt.signals.partition_rate() == 1.0
        pd.testing.assert_series_equal(
            mask.vbt.signals.partition_rate(),
            pd.Series([1.0, 1.0, 1.0], index=mask.columns, name='partition_rate')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.partition_rate(group_by=group_by),
            pd.Series([1.0, 1.0], index=['g1', 'g2'], name='partition_rate')
        )

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Total', 'Rate [%]', 'First Index',
            'Last Index', 'Norm Avg Index [-1, 1]', 'Distance: Min',
            'Distance: Max', 'Distance: Mean', 'Distance: Std', 'Total Partitions',
            'Partition Rate [%]', 'Partition Length: Min', 'Partition Length: Max',
            'Partition Length: Mean', 'Partition Length: Std',
            'Partition Distance: Min', 'Partition Distance: Max',
            'Partition Distance: Mean', 'Partition Distance: Std'
        ], dtype='object')
        pd.testing.assert_series_equal(
            mask.vbt.signals.stats(),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'),
                1.6666666666666667,
                33.333333333333336,
                pd.Timestamp('2020-01-02 00:00:00'),
                pd.Timestamp('2020-01-04 00:00:00'),
                0.0,
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                np.nan,
                1.6666666666666667,
                100.0,
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                np.nan
            ],
                index=stats_index,
                name='agg_func_mean'
            )
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.stats(column='a'),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'),
                2,
                40.0,
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-04 00:00:00'),
                -0.25,
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                np.nan,
                2,
                100.0,
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                np.nan
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.stats(column='a', settings=dict(to_timedelta=False)),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'), 5, 2, 40.0,
                pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-04 00:00:00'), -0.25, 3.0,
                3.0, 3.0, np.nan, 2, 100.0, 1.0, 1.0, 1.0, 0.0, 3.0, 3.0, 3.0, np.nan
            ],
                index=stats_index,
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.stats(column='a', settings=dict(other=mask['b'], from_other=True)),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'),
                2,
                40.0,
                0,
                0.0,
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-04 00:00:00'),
                -0.25,
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'),
                2,
                100.0,
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                np.nan
            ],
                index=pd.Index([
                    'Start', 'End', 'Period', 'Total', 'Rate [%]', 'Total Overlapping',
                    'Overlapping Rate [%]', 'First Index', 'Last Index',
                    'Norm Avg Index [-1, 1]', 'Distance <- Other: Min',
                    'Distance <- Other: Max', 'Distance <- Other: Mean',
                    'Distance <- Other: Std', 'Total Partitions', 'Partition Rate [%]',
                    'Partition Length: Min', 'Partition Length: Max',
                    'Partition Length: Mean', 'Partition Length: Std',
                    'Partition Distance: Min', 'Partition Distance: Max',
                    'Partition Distance: Mean', 'Partition Distance: Std'
                ], dtype='object'),
                name='a'
            )
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals.stats(column='g1', group_by=group_by),
            pd.Series([
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'),
                4,
                40.0,
                pd.Timestamp('2020-01-01 00:00:00'),
                pd.Timestamp('2020-01-05 00:00:00'),
                0.0,
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'),
                4,
                100.0,
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('3 days 00:00:00'),
                pd.Timedelta('0 days 00:00:00')
            ],
                index=stats_index,
                name='g1'
            )
        )
        pd.testing.assert_series_equal(
            mask['c'].vbt.signals.stats(),
            mask.vbt.signals.stats(column='c')
        )
        pd.testing.assert_series_equal(
            mask['c'].vbt.signals.stats(),
            mask.vbt.signals.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals(group_by=group_by)['g2'].stats(),
            mask.vbt.signals(group_by=group_by).stats(column='g2')
        )
        pd.testing.assert_series_equal(
            mask.vbt.signals(group_by=group_by)['g2'].stats(),
            mask.vbt.signals.stats(column='g2', group_by=group_by)
        )
        stats_df = mask.vbt.signals.stats(agg_func=None)
        assert stats_df.shape == (3, 22)
        pd.testing.assert_index_equal(stats_df.index, mask.vbt.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)

    @pytest.mark.parametrize(
        "test_func,test_func_pd",
        [
            (lambda x, *args, **kwargs: x.AND(args, **kwargs), lambda x, y: x & y),
            (lambda x, *args, **kwargs: x.OR(args, **kwargs), lambda x, y: x | y),
            (lambda x, *args, **kwargs: x.XOR(args, **kwargs), lambda x, y: x ^ y)
        ],
    )
    def test_logical_funcs(self, test_func, test_func_pd):
        pd.testing.assert_series_equal(
            test_func(mask['a'].vbt.signals, True, [True, False, False, False, False]),
            test_func_pd(test_func_pd(mask['a'], True), [True, False, False, False, False])
        )
        pd.testing.assert_frame_equal(
            test_func(mask['a'].vbt.signals, True, [True, False, False, False, False], concat=True),
            pd.concat((
                test_func_pd(mask['a'], True),
                test_func_pd(mask['a'], [True, False, False, False, False])
            ), axis=1, keys=[0, 1], names=['combine_idx'])
        )
        pd.testing.assert_frame_equal(
            test_func(mask.vbt.signals, True, [[True], [False], [False], [False], [False]]),
            test_func_pd(test_func_pd(mask, True),
                         np.broadcast_to([[True], [False], [False], [False], [False]], (5, 3)))
        )
        pd.testing.assert_frame_equal(
            test_func(mask.vbt.signals, True, [[True], [False], [False], [False], [False]], concat=True),
            pd.concat((
                test_func_pd(mask, True),
                test_func_pd(mask, np.broadcast_to([[True], [False], [False], [False], [False]], (5, 3)))
            ), axis=1, keys=[0, 1], names=['combine_idx'])
        )


# ############# factory.py ############# #


class TestFactory:
    def test_entries(self):
        @njit
        def choice_nb(from_i, to_i, col, ts, in_out, n, arg, temp_idx_arr, kw):
            in_out[from_i, col] = ts[from_i, col] * n + arg + kw
            temp_idx_arr[0] = from_i
            return temp_idx_arr[:1]

        MySignals = vbt.SignalFactory(
            mode='entries',
            input_names=['ts2'],
            in_output_names=['in_out2'],
            param_names=['n2']
        ).from_choice_func(
            entry_choice_func=choice_nb,
            entry_settings=dict(
                pass_inputs=['ts2'],
                pass_in_outputs=['in_out2'],
                pass_params=['n2'],
                pass_kwargs=['temp_idx_arr2', ('kw2', 1000)],
                pass_cache=True
            ),
            in_output_settings=dict(
                in_out2=dict(
                    dtype=np.float64
                )
            ),
            in_out2=np.nan,
            var_args=True
        )
        my_sig = MySignals.run((5,), np.arange(5), [1, 0], 100)
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [False, False],
                [False, False],
                [False, False]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [1100.0, 1100.0],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [np.nan, np.nan],
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )

    def test_exits(self):
        @njit
        def choice_nb(from_i, to_i, col, ts, in_out, n, arg, temp_idx_arr, kw):
            in_out[from_i, col] = ts[from_i, col] * n + arg + kw
            temp_idx_arr[0] = from_i
            return temp_idx_arr[:1]

        MySignals = vbt.SignalFactory(
            mode='exits',
            input_names=['ts2'],
            in_output_names=['in_out2'],
            param_names=['n2']
        ).from_choice_func(
            exit_choice_func=choice_nb,
            exit_settings=dict(
                pass_inputs=['ts2'],
                pass_in_outputs=['in_out2'],
                pass_params=['n2'],
                pass_kwargs=['temp_idx_arr2', ('kw2', 1000)],
                pass_cache=True
            ),
            in_output_settings=dict(
                in_out2=dict(
                    dtype=np.float64
                )
            ),
            in_out2=np.nan,
            var_args=True
        )
        e = np.array([True, False, True, False, True])
        my_sig = MySignals.run(e, np.arange(5), [1, 0], 100)
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [True, True],
                [False, False],
                [True, True]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.exits,
            pd.DataFrame(np.array([
                [False, False],
                [True, True],
                [False, False],
                [True, True],
                [False, False]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [np.nan, np.nan],
                [1101.0, 1100.0],
                [np.nan, np.nan],
                [1103.0, 1100.0],
                [np.nan, np.nan],
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        e = np.array([True, False, False, True, False, False])
        my_sig = MySignals.run(e, np.arange(6), [1, 0], 100, wait=2)
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [False, False],
                [True, True],
                [False, False],
                [False, False]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.exits,
            pd.DataFrame(np.array([
                [False, False],
                [False, False],
                [True, True],
                [False, False],
                [False, False],
                [True, True]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1102.0, 1100.0],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1105.0, 1100.0]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )

    def test_chain(self):
        @njit
        def choice_nb(from_i, to_i, col, ts, in_out, n, arg, temp_idx_arr, kw):
            in_out[from_i, col] = ts[from_i, col] * n + arg + kw
            temp_idx_arr[0] = from_i
            return temp_idx_arr[:1]

        MySignals = vbt.SignalFactory(
            mode='chain',
            input_names=['ts2'],
            in_output_names=['in_out2'],
            param_names=['n2']
        ).from_choice_func(
            exit_choice_func=choice_nb,
            exit_settings=dict(
                pass_inputs=['ts2'],
                pass_in_outputs=['in_out2'],
                pass_params=['n2'],
                pass_kwargs=['temp_idx_arr2', ('kw2', 1000)],
                pass_cache=True
            ),
            in_output_settings=dict(
                in_out2=dict(
                    dtype=np.float64
                )
            ),
            in_out2=np.nan,
            var_args=True
        )
        e = np.array([True, True, True, True, True])
        my_sig = MySignals.run(e, np.arange(5), [1, 0], 100)
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [True, True],
                [True, True],
                [True, True],
                [True, True]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.new_entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [True, True],
                [False, False],
                [True, True]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.exits,
            pd.DataFrame(np.array([
                [False, False],
                [True, True],
                [False, False],
                [True, True],
                [False, False]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [np.nan, np.nan],
                [1101.0, 1100.0],
                [np.nan, np.nan],
                [1103.0, 1100.0],
                [np.nan, np.nan],
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        e = np.array([True, True, True, True, True, True])
        my_sig = MySignals.run(e, np.arange(6), [1, 0], 100, wait=2)
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [True, True],
                [True, True],
                [True, True],
                [True, True],
                [True, True]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.new_entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [False, False],
                [True, True],
                [False, False],
                [False, False]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.exits,
            pd.DataFrame(np.array([
                [False, False],
                [False, False],
                [True, True],
                [False, False],
                [False, False],
                [True, True]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1102.0, 1100.0],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1105.0, 1100.0]
            ]), columns=pd.Index([1, 0], dtype='int64', name='custom_n2')
            )
        )

    def test_both(self):
        @njit
        def cache_nb(ts1, ts2, in_out1, in_out2, n1, n2, arg0, temp_idx_arr0, kw0):
            return arg0

        @njit
        def choice_nb(from_i, to_i, col, ts, in_out, n, arg, temp_idx_arr, kw, cache):
            in_out[from_i, col] = ts[from_i, col] * n + arg + kw + cache
            temp_idx_arr[0] = from_i
            return temp_idx_arr[:1]

        MySignals = vbt.SignalFactory(
            input_names=['ts1', 'ts2'],
            in_output_names=['in_out1', 'in_out2'],
            param_names=['n1', 'n2']
        ).from_choice_func(
            cache_func=cache_nb,
            cache_settings=dict(
                pass_inputs=['ts1', 'ts2'],
                pass_in_outputs=['in_out1', 'in_out2'],
                pass_params=['n1', 'n2'],
                pass_kwargs=['temp_idx_arr0', ('kw0', 1000)]
            ),
            entry_choice_func=choice_nb,
            entry_settings=dict(
                pass_inputs=['ts1'],
                pass_in_outputs=['in_out1'],
                pass_params=['n1'],
                pass_kwargs=['temp_idx_arr1', ('kw1', 1000)],
                pass_cache=True
            ),
            exit_choice_func=choice_nb,
            exit_settings=dict(
                pass_inputs=['ts2'],
                pass_in_outputs=['in_out2'],
                pass_params=['n2'],
                pass_kwargs=['temp_idx_arr2', ('kw2', 1000)],
                pass_cache=True
            ),
            in_output_settings=dict(
                in_out1=dict(
                    dtype=np.float64
                ),
                in_out2=dict(
                    dtype=np.float64
                )
            ),
            in_out1=np.nan,
            in_out2=np.nan,
            var_args=True,
            require_input_shape=False
        )
        my_sig = MySignals.run(
            np.arange(5), np.arange(5), [0, 1], [1, 0],
            cache_args=(0,), entry_args=(100,), exit_args=(100,)
        )
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [True, True],
                [False, False],
                [True, True]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.exits,
            pd.DataFrame(np.array([
                [False, False],
                [True, True],
                [False, False],
                [True, True],
                [False, False],
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out1,
            pd.DataFrame(np.array([
                [1100.0, 1100.0],
                [np.nan, np.nan],
                [1100.0, 1102.0],
                [np.nan, np.nan],
                [1100.0, 1104.0]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [np.nan, np.nan],
                [1101.0, 1100.0],
                [np.nan, np.nan],
                [1103.0, 1100.0],
                [np.nan, np.nan],
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        my_sig = MySignals.run(
            np.arange(7), np.arange(7), [0, 1], [1, 0],
            cache_args=(0,), entry_args=(100,), exit_args=(100,),
            entry_kwargs=dict(wait=2), exit_kwargs=dict(wait=2)
        )
        pd.testing.assert_frame_equal(
            my_sig.entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [False, False],
                [False, False],
                [True, True],
                [False, False],
                [False, False]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.exits,
            pd.DataFrame(np.array([
                [False, False],
                [False, False],
                [True, True],
                [False, False],
                [False, False],
                [False, False],
                [True, True]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out1,
            pd.DataFrame(np.array([
                [1100.0, 1100.0],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1100.0, 1104.0],
                [np.nan, np.nan],
                [np.nan, np.nan]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )
        pd.testing.assert_frame_equal(
            my_sig.in_out2,
            pd.DataFrame(np.array([
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1102.0, 1100.0],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [np.nan, np.nan],
                [1106.0, 1100.0]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0, 1), (1, 0)],
                names=['custom_n1', 'custom_n2'])
            )
        )


# ############# generators.py ############# #

class TestGenerators:
    def test_RAND(self):
        rand = vbt.RAND.run(n=1, input_shape=(6,), seed=seed)
        pd.testing.assert_series_equal(
            rand.entries,
            pd.Series(np.array([True, False, False, False, False, False]), name=1)
        )
        rand = vbt.RAND.run(n=[1, 2, 3], input_shape=(6,), seed=seed)
        pd.testing.assert_frame_equal(
            rand.entries,
            pd.DataFrame(np.array([
                [True, True, True],
                [False, False, True],
                [False, False, False],
                [False, True, False],
                [False, False, True],
                [False, False, False]
            ]), columns=pd.Index([1, 2, 3], dtype='int64', name='rand_n')
            )
        )
        rand = vbt.RAND.run(n=[np.array([1, 2]), np.array([3, 4])], input_shape=(8, 2), seed=seed)
        pd.testing.assert_frame_equal(
            rand.entries,
            pd.DataFrame(np.array([
                [False, False, True, False],
                [True, False, False, False],
                [False, False, False, True],
                [False, True, True, False],
                [False, False, False, False],
                [False, False, False, True],
                [False, False, True, True],
                [False, True, False, True]
            ]), columns=pd.MultiIndex.from_tuples([
                (1, 0),
                (2, 1),
                (3, 0),
                (4, 1)
            ], names=['rand_n', None])
            )
        )

    def test_RANDX(self):
        randx = vbt.RANDX.run(mask, seed=seed)
        pd.testing.assert_frame_equal(
            randx.exits,
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [True, True, False],
                [False, False, False],
                [True, False, True]
            ]), columns=mask.columns, index=mask.index)
        )

    def test_RANDNX(self):
        randnx = vbt.RANDNX.run(n=1, input_shape=(6,), seed=seed)
        pd.testing.assert_series_equal(
            randnx.entries,
            pd.Series(np.array([True, False, False, False, False, False]), name=1)
        )
        pd.testing.assert_series_equal(
            randnx.exits,
            pd.Series(np.array([False, True, False, False, False, False]), name=1)
        )
        randnx = vbt.RANDNX.run(n=[1, 2, 3], input_shape=(6,), seed=seed)
        pd.testing.assert_frame_equal(
            randnx.entries,
            pd.DataFrame(np.array([
                [True, True, True],
                [False, False, False],
                [False, True, True],
                [False, False, False],
                [False, False, True],
                [False, False, False]
            ]), columns=pd.Index([1, 2, 3], dtype='int64', name='randnx_n')
            )
        )
        pd.testing.assert_frame_equal(
            randnx.exits,
            pd.DataFrame(np.array([
                [False, False, False],
                [True, True, True],
                [False, False, False],
                [False, True, True],
                [False, False, False],
                [False, False, True]
            ]), columns=pd.Index([1, 2, 3], dtype='int64', name='randnx_n')
            )
        )
        randnx = vbt.RANDNX.run(n=[np.array([1, 2]), np.array([3, 4])], input_shape=(8, 2), seed=seed)
        pd.testing.assert_frame_equal(
            randnx.entries,
            pd.DataFrame(np.array([
                [False, True, True, True],
                [True, False, False, False],
                [False, False, False, True],
                [False, False, True, False],
                [False, True, False, True],
                [False, False, True, False],
                [False, False, False, True],
                [False, False, False, False]
            ]), columns=pd.MultiIndex.from_tuples([
                (1, 0),
                (2, 1),
                (3, 0),
                (4, 1)
            ], names=['randnx_n', None])
            )
        )
        pd.testing.assert_frame_equal(
            randnx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False],
                [False, False, True, True],
                [False, False, False, False],
                [False, True, False, True],
                [False, False, True, False],
                [True, False, False, True],
                [False, False, True, False],
                [False, True, False, True]
            ]), columns=pd.MultiIndex.from_tuples([
                (1, 0),
                (2, 1),
                (3, 0),
                (4, 1)
            ], names=['randnx_n', None])
            )
        )

    def test_RPROB(self):
        rprob = vbt.RPROB.run(prob=1, input_shape=(5,), seed=seed)
        pd.testing.assert_series_equal(
            rprob.entries,
            pd.Series(np.array([True, True, True, True, True]), name=1)
        )
        rprob = vbt.RPROB.run(prob=[0, 0.5, 1], input_shape=(5,), seed=seed)
        pd.testing.assert_frame_equal(
            rprob.entries,
            pd.DataFrame(np.array([
                [False, True, True],
                [False, True, True],
                [False, False, True],
                [False, False, True],
                [False, False, True]
            ]), columns=pd.Index([0, 0.5, 1], dtype='float64', name='rprob_prob')
            )
        )
        rprob = vbt.RPROB.run(prob=[np.array([0, 0.25]), np.array([0.75, 1])], input_shape=(5, 2), seed=seed)
        pd.testing.assert_frame_equal(
            rprob.entries,
            pd.DataFrame(np.array([
                [False, True, True, True],
                [False, True, False, True],
                [False, False, False, True],
                [False, False, True, True],
                [False, False, True, True]
            ]), columns=pd.MultiIndex.from_tuples([
                ('array_0', 0),
                ('array_0', 1),
                ('array_1', 0),
                ('array_1', 1)
            ], names=['rprob_prob', None])
            )
        )

    def test_RPROBX(self):
        rprobx = vbt.RPROBX.run(mask, prob=[0., 0.5, 1.], seed=seed)
        pd.testing.assert_frame_equal(
            rprobx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, True, False, False],
                [False, False, False, False, True, False, False, True, False],
                [False, False, False, False, False, False, False, False, True],
                [False, False, False, False, False, False, True, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.0, 'a'),
                (0.0, 'b'),
                (0.0, 'c'),
                (0.5, 'a'),
                (0.5, 'b'),
                (0.5, 'c'),
                (1.0, 'a'),
                (1.0, 'b'),
                (1.0, 'c')
            ], names=['rprobx_prob', None])
            )
        )

    def test_RPROBCX(self):
        rprobcx = vbt.RPROBCX.run(mask, prob=[0., 0.5, 1.], seed=seed)
        pd.testing.assert_frame_equal(
            rprobcx.new_entries,
            pd.DataFrame(np.array([
                [True, False, False, True, False, False, True, False, False],
                [False, True, False, False, True, False, False, True, False],
                [False, False, True, False, False, True, False, False, True],
                [False, False, False, True, False, False, True, False, False],
                [False, False, False, False, True, False, False, True, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.0, 'a'),
                (0.0, 'b'),
                (0.0, 'c'),
                (0.5, 'a'),
                (0.5, 'b'),
                (0.5, 'c'),
                (1.0, 'a'),
                (1.0, 'b'),
                (1.0, 'c')
            ], names=['rprobcx_prob', None])
            )
        )
        pd.testing.assert_frame_equal(
            rprobcx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, True, False, False],
                [False, False, False, True, False, False, False, True, False],
                [False, False, False, False, True, True, False, False, True],
                [False, False, False, False, False, False, True, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.0, 'a'),
                (0.0, 'b'),
                (0.0, 'c'),
                (0.5, 'a'),
                (0.5, 'b'),
                (0.5, 'c'),
                (1.0, 'a'),
                (1.0, 'b'),
                (1.0, 'c')
            ], names=['rprobcx_prob', None])
            )
        )

    def test_RPROBNX(self):
        rprobnx = vbt.RPROBNX.run(entry_prob=1., exit_prob=1., input_shape=(5,), seed=seed)
        pd.testing.assert_series_equal(
            rprobnx.entries,
            pd.Series(np.array([True, False, True, False, True]), name=(1.0, 1.0))
        )
        pd.testing.assert_series_equal(
            rprobnx.exits,
            pd.Series(np.array([False, True, False, True, False]), name=(1.0, 1.0))
        )
        rprobnx = vbt.RPROBNX.run(
            entry_prob=np.asarray([1., 0., 1., 0., 1.]),
            exit_prob=np.asarray([0., 1., 0., 1., 0.]),
            input_shape=(5,), seed=seed)
        pd.testing.assert_series_equal(
            rprobnx.entries,
            pd.Series(np.array([True, False, True, False, True]), name=('array_0', 'array_0'))
        )
        pd.testing.assert_series_equal(
            rprobnx.exits,
            pd.Series(np.array([False, True, False, True, False]), name=('array_0', 'array_0'))
        )
        rprobnx = vbt.RPROBNX.run(entry_prob=[0.5, 1.], exit_prob=[1., 0.5], input_shape=(5,), seed=seed)
        pd.testing.assert_frame_equal(
            rprobnx.entries,
            pd.DataFrame(np.array([
                [True, True],
                [False, False],
                [False, True],
                [False, False],
                [True, False]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0.5, 1.0), (1.0, 0.5)],
                names=['rprobnx_entry_prob', 'rprobnx_exit_prob'])
            )
        )
        pd.testing.assert_frame_equal(
            rprobnx.exits,
            pd.DataFrame(np.array([
                [False, False],
                [True, True],
                [False, False],
                [False, False],
                [False, False]
            ]), columns=pd.MultiIndex.from_tuples(
                [(0.5, 1.0), (1.0, 0.5)],
                names=['rprobnx_entry_prob', 'rprobnx_exit_prob'])
            )
        )

    def test_STX(self):
        stx = vbt.STX.run(mask, ts, 0.1)
        pd.testing.assert_frame_equal(
            stx.exits,
            pd.DataFrame(np.array([
                [False, False, False],
                [True, False, False],
                [False, True, False],
                [False, False, False],
                [False, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, 'a'),
                (0.1, 'b'),
                (0.1, 'c')
            ], names=['stx_stop', None])
            )
        )
        stx = vbt.STX.run(mask, ts, np.asarray([0.1, 0.1, -0.1, -0.1, -0.1])[:, None])
        pd.testing.assert_frame_equal(
            stx.exits,
            pd.DataFrame(np.array([
                [False, False, False],
                [True, False, False],
                [False, True, False],
                [False, False, True],
                [True, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                ('array_0', 'a'),
                ('array_0', 'b'),
                ('array_0', 'c')
            ], names=['stx_stop', None])
            )
        )
        stx = vbt.STX.run(mask, ts, [0.1, 0.1, -0.1, -0.1], trailing=[False, True, False, True])
        pd.testing.assert_frame_equal(
            stx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [True, False, False, True, False, False, False, False, False, False, False, False],
                [False, True, False, False, True, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, True, False, True, True],
                [False, False, False, False, False, False, True, False, False, True, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, 'a'),
                (0.1, False, 'b'),
                (0.1, False, 'c'),
                (0.1, True, 'a'),
                (0.1, True, 'b'),
                (0.1, True, 'c'),
                (-0.1, False, 'a'),
                (-0.1, False, 'b'),
                (-0.1, False, 'c'),
                (-0.1, True, 'a'),
                (-0.1, True, 'b'),
                (-0.1, True, 'c')
            ], names=['stx_stop', 'stx_trailing', None])
            )
        )

    def test_STCX(self):
        stcx = vbt.STCX.run(mask, ts, [0.1, 0.1, -0.1, -0.1], trailing=[False, True, False, True])
        pd.testing.assert_frame_equal(
            stcx.new_entries,
            pd.DataFrame(np.array([
                [True, False, False, True, False, False, True, False, False, True, False, False],
                [False, True, False, False, True, False, False, True, False, False, True, False],
                [False, False, True, False, False, True, False, False, True, False, False, True],
                [True, False, False, True, False, False, False, False, False, False, False, False],
                [False, True, False, False, True, False, False, False, False, False, True, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, 'a'),
                (0.1, False, 'b'),
                (0.1, False, 'c'),
                (0.1, True, 'a'),
                (0.1, True, 'b'),
                (0.1, True, 'c'),
                (-0.1, False, 'a'),
                (-0.1, False, 'b'),
                (-0.1, False, 'c'),
                (-0.1, True, 'a'),
                (-0.1, True, 'b'),
                (-0.1, True, 'c')
            ], names=['stcx_stop', 'stcx_trailing', None])
            )
        )
        pd.testing.assert_frame_equal(
            stcx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [True, False, False, True, False, False, False, False, False, False, False, False],
                [False, True, False, False, True, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, True, True, True, True],
                [False, False, False, False, False, False, False, True, False, False, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, 'a'),
                (0.1, False, 'b'),
                (0.1, False, 'c'),
                (0.1, True, 'a'),
                (0.1, True, 'b'),
                (0.1, True, 'c'),
                (-0.1, False, 'a'),
                (-0.1, False, 'b'),
                (-0.1, False, 'c'),
                (-0.1, True, 'a'),
                (-0.1, True, 'b'),
                (-0.1, True, 'c')
            ], names=['stcx_stop', 'stcx_trailing', None])
            )
        )

    def test_OHLCSTX(self):
        ohlcstx = vbt.OHLCSTX.run(
            mask, price['open'], price['high'], price['low'], price['close'],
            sl_stop=0.1
        )
        pd.testing.assert_frame_equal(
            ohlcstx.exits,
            pd.DataFrame(np.array([
                [False, False, False],
                [False, False, False],
                [False, False, False],
                [False, False, True],
                [True, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, 'a'),
                (0.1, 'b'),
                (0.1, 'c')
            ], names=['ohlcstx_sl_stop', None])
            )
        )
        pd.testing.assert_frame_equal(
            ohlcstx.stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan],
                [np.nan, np.nan, 10.8],
                [9.9, np.nan, np.nan]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, 'a'),
                (0.1, 'b'),
                (0.1, 'c')
            ], names=['ohlcstx_sl_stop', None])
            )
        )
        pd.testing.assert_frame_equal(
            ohlcstx.stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, 0],
                [0, -1, -1]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, 'a'),
                (0.1, 'b'),
                (0.1, 'c')
            ], names=['ohlcstx_sl_stop', None])
            )
        )
        ohlcstx = vbt.OHLCSTX.run(
            mask, price['open'], price['high'], price['low'], price['close'],
            sl_stop=[0.1, 0.1, np.nan], sl_trail=[False, True, False], tp_stop=[np.nan, np.nan, 0.1]
        )
        pd.testing.assert_frame_equal(
            ohlcstx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, True, False, False],
                [False, False, False, False, False, False, False, True, False],
                [False, False, True, False, True, True, False, False, False],
                [True, False, False, True, False, False, False, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, np.nan, 'a'),
                (0.1, False, np.nan, 'b'),
                (0.1, False, np.nan, 'c'),
                (0.1, True, np.nan, 'a'),
                (0.1, True, np.nan, 'b'),
                (0.1, True, np.nan, 'c'),
                (np.nan, False, 0.1, 'a'),
                (np.nan, False, 0.1, 'b'),
                (np.nan, False, 0.1, 'c')
            ], names=['ohlcstx_sl_stop', 'ohlcstx_sl_trail', 'ohlcstx_tp_stop', None])
            )
        )
        pd.testing.assert_frame_equal(
            ohlcstx.stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 11., np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 12.1, np.nan],
                [np.nan, np.nan, 10.8, np.nan, 11.7, 10.8, np.nan, np.nan, np.nan],
                [9.9, np.nan, np.nan, 9.9, np.nan, np.nan, np.nan, np.nan, np.nan]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, np.nan, 'a'),
                (0.1, False, np.nan, 'b'),
                (0.1, False, np.nan, 'c'),
                (0.1, True, np.nan, 'a'),
                (0.1, True, np.nan, 'b'),
                (0.1, True, np.nan, 'c'),
                (np.nan, False, 0.1, 'a'),
                (np.nan, False, 0.1, 'b'),
                (np.nan, False, 0.1, 'c')
            ], names=['ohlcstx_sl_stop', 'ohlcstx_sl_trail', 'ohlcstx_tp_stop', None])
            )
        )
        pd.testing.assert_frame_equal(
            ohlcstx.stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 2, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, 2, -1],
                [-1, -1, 0, -1, 1, 1, -1, -1, -1],
                [0, -1, -1, 1, -1, -1, -1, -1, -1]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, np.nan, 'a'),
                (0.1, False, np.nan, 'b'),
                (0.1, False, np.nan, 'c'),
                (0.1, True, np.nan, 'a'),
                (0.1, True, np.nan, 'b'),
                (0.1, True, np.nan, 'c'),
                (np.nan, False, 0.1, 'a'),
                (np.nan, False, 0.1, 'b'),
                (np.nan, False, 0.1, 'c')
            ], names=['ohlcstx_sl_stop', 'ohlcstx_sl_trail', 'ohlcstx_tp_stop', None])
            )
        )
        np.testing.assert_array_equal(
            vbt.OHLCSTX.run(
                mask, price['open'], price['high'], price['low'], price['close'],
                sl_stop=[0.1, np.nan], sl_trail=False, tp_stop=[np.nan, 0.1], reverse=False
            ).exits.values,
            vbt.OHLCSTX.run(
                mask, price['open'], price['high'], price['low'], price['close'],
                sl_stop=[np.nan, 0.1], sl_trail=False, tp_stop=[0.1, np.nan], reverse=True
            ).exits.values
        )

    def test_OHLCSTCX(self):
        ohlcstcx = vbt.OHLCSTCX.run(
            mask, price['open'], price['high'], price['low'], price['close'],
            sl_stop=[0.1, 0.1, np.nan], sl_trail=[False, True, False], tp_stop=[np.nan, np.nan, 0.1]
        )
        pd.testing.assert_frame_equal(
            ohlcstcx.exits,
            pd.DataFrame(np.array([
                [False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, True, False, False],
                [False, False, False, False, False, False, False, True, False],
                [False, False, True, True, True, True, False, False, False],
                [True, True, False, False, False, False, False, False, False]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, np.nan, 'a'),
                (0.1, False, np.nan, 'b'),
                (0.1, False, np.nan, 'c'),
                (0.1, True, np.nan, 'a'),
                (0.1, True, np.nan, 'b'),
                (0.1, True, np.nan, 'c'),
                (np.nan, False, 0.1, 'a'),
                (np.nan, False, 0.1, 'b'),
                (np.nan, False, 0.1, 'c')
            ], names=['ohlcstcx_sl_stop', 'ohlcstcx_sl_trail', 'ohlcstcx_tp_stop', None])
            )
        )
        pd.testing.assert_frame_equal(
            ohlcstcx.stop_price,
            pd.DataFrame(np.array([
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 11., np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 12.1, np.nan],
                [np.nan, np.nan, 10.8, 11.7, 11.7, 10.8, np.nan, np.nan, np.nan],
                [9.0, 9.9, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, np.nan, 'a'),
                (0.1, False, np.nan, 'b'),
                (0.1, False, np.nan, 'c'),
                (0.1, True, np.nan, 'a'),
                (0.1, True, np.nan, 'b'),
                (0.1, True, np.nan, 'c'),
                (np.nan, False, 0.1, 'a'),
                (np.nan, False, 0.1, 'b'),
                (np.nan, False, 0.1, 'c')
            ], names=['ohlcstcx_sl_stop', 'ohlcstcx_sl_trail', 'ohlcstcx_tp_stop', None])
            )
        )
        pd.testing.assert_frame_equal(
            ohlcstcx.stop_type,
            pd.DataFrame(np.array([
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 2, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, 2, -1],
                [-1, -1, 0, 1, 1, 1, -1, -1, -1],
                [0, 0, -1, -1, -1, -1, -1, -1, -1]
            ]), index=mask.index, columns=pd.MultiIndex.from_tuples([
                (0.1, False, np.nan, 'a'),
                (0.1, False, np.nan, 'b'),
                (0.1, False, np.nan, 'c'),
                (0.1, True, np.nan, 'a'),
                (0.1, True, np.nan, 'b'),
                (0.1, True, np.nan, 'c'),
                (np.nan, False, 0.1, 'a'),
                (np.nan, False, 0.1, 'b'),
                (np.nan, False, 0.1, 'c')
            ], names=['ohlcstcx_sl_stop', 'ohlcstcx_sl_trail', 'ohlcstcx_tp_stop', None])
            )
        )
