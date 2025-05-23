from datetime import datetime

import numpy as np
import pandas as pd

import vectorbt as vbt

close_ts = pd.DataFrame({
    'a': [1, 2, 1, 2, 3, 2],
    'b': [3, 2, 3, 2, 1, 2]
}, index=pd.Index([
    datetime(2020, 1, 1),
    datetime(2020, 1, 2),
    datetime(2020, 1, 3),
    datetime(2020, 1, 4),
    datetime(2020, 1, 5),
    datetime(2020, 1, 6)
]))

pos_ths = [np.array([1, 1 / 2]), np.array([2, 1 / 2]), np.array([3, 1 / 2])]
neg_ths = [np.array([1 / 2, 1 / 3]), np.array([1 / 2, 2 / 3]), np.array([1 / 2, 3 / 4])]


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []


def teardown_module():
    vbt.settings.reset()


# ############# generators.py ############# #

class TestGenerators:
    def test_FMEAN(self):
        pd.testing.assert_frame_equal(
            vbt.FMEAN.run(close_ts, window=(2, 3), ewm=False).fmean,
            pd.DataFrame(
                np.array([
                    [1.5, 2.5, 1.6666666666666667, 2.3333333333333335],
                    [1.5, 2.5, 2.0, 2.0],
                    [2.5, 1.5, 2.3333333333333335, 1.6666666666666667],
                    [2.5, 1.5, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, False, 'a'),
                    (2, False, 'b'),
                    (3, False, 'a'),
                    (3, False, 'b'),
                ], names=['fmean_window', 'fmean_ewm', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.FMEAN.run(close_ts, window=(2, 3), ewm=True).fmean,
            pd.DataFrame(
                np.array([
                    [1.8024691358024691, 2.197530864197531, 1.8125, 2.1875],
                    [1.4074074074074074, 2.5925925925925926, 1.625, 2.375],
                    [2.2222222222222223, 1.7777777777777777, 2.25, 1.75],
                    [2.666666666666667, 1.3333333333333335, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, True, 'a'),
                    (2, True, 'b'),
                    (3, True, 'a'),
                    (3, True, 'b'),
                ], names=['fmean_window', 'fmean_ewm', None])
            )
        )

    def test_FSTD(self):
        pd.testing.assert_frame_equal(
            vbt.FSTD.run(close_ts, window=(2, 3), ewm=False).fstd,
            pd.DataFrame(
                np.array([
                    [0.5, 0.5, 0.4714045207910384, 0.4714045207910183],
                    [0.5, 0.5, 0.816496580927726, 0.816496580927726],
                    [0.5, 0.5, 0.4714045207910183, 0.4714045207910384],
                    [0.5, 0.5, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, False, 'a'),
                    (2, False, 'b'),
                    (3, False, 'a'),
                    (3, False, 'b'),
                ], names=['fstd_window', 'fstd_ewm', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.FSTD.run(close_ts, window=(2, 3), ewm=True).fstd,
            pd.DataFrame(
                np.array([
                    [0.64486716348143, 0.6448671634814303, 0.6462561866810479, 0.6462561866810479],
                    [0.8833005039168617, 0.8833005039168604, 0.8591246929842246, 0.8591246929842246],
                    [0.5916079783099623, 0.5916079783099623, 0.5477225575051662, 0.5477225575051662],
                    [0.7071067811865476, 0.7071067811865476, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, True, 'a'),
                    (2, True, 'b'),
                    (3, True, 'a'),
                    (3, True, 'b'),
                ], names=['fstd_window', 'fstd_ewm', None])
            )
        )

    def test_FMIN(self):
        pd.testing.assert_frame_equal(
            vbt.FMIN.run(close_ts, window=(2, 3)).fmin,
            pd.DataFrame(
                np.array([
                    [1.0, 2.0, 1.0, 2.0],
                    [1.0, 2.0, 1.0, 1.0],
                    [2.0, 1.0, 2.0, 1.0],
                    [2.0, 1.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 'a'),
                    (2, 'b'),
                    (3, 'a'),
                    (3, 'b'),
                ], names=['fmin_window', None])
            )
        )

    def test_FMAX(self):
        pd.testing.assert_frame_equal(
            vbt.FMAX.run(close_ts, window=(2, 3)).fmax,
            pd.DataFrame(
                np.array([
                    [2.0, 3.0, 2.0, 3.0],
                    [2.0, 3.0, 3.0, 3.0],
                    [3.0, 2.0, 3.0, 2.0],
                    [3.0, 2.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 'a'),
                    (2, 'b'),
                    (3, 'a'),
                    (3, 'b'),
                ], names=['fmax_window', None])
            )
        )

    def test_FIXLB(self):
        pd.testing.assert_frame_equal(
            vbt.FIXLB.run(close_ts, n=(2, 3)).labels,
            pd.DataFrame(
                np.array([
                    [0.0, 0.0, 1.0, -0.3333333333333333],
                    [0.0, 0.0, 0.5, -0.5],
                    [2.0, -0.6666666666666666, 1.0, -0.3333333333333333],
                    [0.0, 0.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 'a'),
                    (2, 'b'),
                    (3, 'a'),
                    (3, 'b'),
                ], names=['fixlb_n', None])
            )
        )

    def test_MEANLB(self):
        pd.testing.assert_frame_equal(
            vbt.MEANLB.run(close_ts, window=(2, 3), ewm=False).labels,
            pd.DataFrame(
                np.array([
                    [0.5, -0.16666666666666666, 0.6666666666666667, -0.22222222222222218],
                    [-0.25, 0.25, 0.0, 0.0],
                    [1.5, -0.5, 1.3333333333333335, -0.4444444444444444],
                    [0.25, -0.25, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, False, 'a'),
                    (2, False, 'b'),
                    (3, False, 'a'),
                    (3, False, 'b'),
                ], names=['meanlb_window', 'meanlb_ewm', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.MEANLB.run(close_ts, window=(2, 3), ewm=True).labels,
            pd.DataFrame(
                np.array([
                    [0.8024691358024691, -0.2674897119341564, 0.8125, -0.2708333333333333],
                    [-0.2962962962962963, 0.2962962962962963, -0.1875, 0.1875],
                    [1.2222222222222223, -0.40740740740740744, 1.25, -0.4166666666666667],
                    [0.3333333333333335, -0.33333333333333326, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, True, 'a'),
                    (2, True, 'b'),
                    (3, True, 'a'),
                    (3, True, 'b'),
                ], names=['meanlb_window', 'meanlb_ewm', None])
            )
        )

    def test_LEXLB(self):
        pd.testing.assert_frame_equal(
            vbt.LEXLB.run(close_ts, pos_th=pos_ths, neg_th=neg_ths).labels,
            pd.DataFrame(
                np.array([
                    [-1, 1, -1, 1, 0, 0],
                    [1, -1, 0, 0, 0, 0],
                    [-1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [1, -1, 1, -1, 0, 0],
                    [0, 1, 0, 1, 0, 0]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    ('array_0', 'array_0', 'a'),
                    ('array_0', 'array_0', 'b'),
                    ('array_1', 'array_1', 'a'),
                    ('array_1', 'array_1', 'b'),
                    ('array_2', 'array_2', 'a'),
                    ('array_2', 'array_2', 'b')
                ], names=['lexlb_pos_th', 'lexlb_neg_th', None])
            )
        )

    def test_TRENDLB(self):
        pd.testing.assert_frame_equal(
            vbt.TRENDLB.run(close_ts, pos_th=pos_ths, neg_th=neg_ths, mode='Binary').labels,
            pd.DataFrame(
                np.array([
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [0.0, 1.0, 1.0, 0.0, np.nan, np.nan],
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [np.nan, 1.0, np.nan, 1.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    ('array_0', 'array_0', 0, 'a'),
                    ('array_0', 'array_0', 0, 'b'),
                    ('array_1', 'array_1', 0, 'a'),
                    ('array_1', 'array_1', 0, 'b'),
                    ('array_2', 'array_2', 0, 'a'),
                    ('array_2', 'array_2', 0, 'b')
                ], names=['trendlb_pos_th', 'trendlb_neg_th', 'trendlb_mode', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.TRENDLB.run(close_ts, pos_th=pos_ths, neg_th=neg_ths, mode='BinaryCont').labels,
            pd.DataFrame(
                np.array([
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [0.0, 1.0, 0.5, 0.5, np.nan, np.nan],
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [0.5, 0.5, 0.5, 0.5, np.nan, np.nan],
                    [np.nan, 1.0, np.nan, 1.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    ('array_0', 'array_0', 1, 'a'),
                    ('array_0', 'array_0', 1, 'b'),
                    ('array_1', 'array_1', 1, 'a'),
                    ('array_1', 'array_1', 1, 'b'),
                    ('array_2', 'array_2', 1, 'a'),
                    ('array_2', 'array_2', 1, 'b')
                ], names=['trendlb_pos_th', 'trendlb_neg_th', 'trendlb_mode', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.TRENDLB.run(close_ts, pos_th=pos_ths, neg_th=neg_ths, mode='BinaryContSat').labels,
            pd.DataFrame(
                np.array([
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [0.0, 1.0, 0.5, 0.4999999999999999, np.nan, np.nan],
                    [1.0, 0.0, 1.0, 0.0, np.nan, np.nan],
                    [0.6666666666666667, 0.0, 0.5, 0.4999999999999999, np.nan, np.nan],
                    [np.nan, 1.0, np.nan, 1.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    ('array_0', 'array_0', 2, 'a'),
                    ('array_0', 'array_0', 2, 'b'),
                    ('array_1', 'array_1', 2, 'a'),
                    ('array_1', 'array_1', 2, 'b'),
                    ('array_2', 'array_2', 2, 'a'),
                    ('array_2', 'array_2', 2, 'b')
                ], names=['trendlb_pos_th', 'trendlb_neg_th', 'trendlb_mode', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.TRENDLB.run(close_ts, pos_th=pos_ths, neg_th=neg_ths, mode='PctChange').labels,
            pd.DataFrame(
                np.array([
                    [1.0, -0.3333333333333333, 2.0, -0.6666666666666666, np.nan, np.nan],
                    [-0.5, 0.5, 0.5, -0.5, np.nan, np.nan],
                    [2.0, -0.6666666666666666, 2.0, -0.6666666666666666, np.nan, np.nan],
                    [0.5, -0.5, 0.5, -0.5, np.nan, np.nan],
                    [np.nan, 1.0, np.nan, 1.0, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    ('array_0', 'array_0', 3, 'a'),
                    ('array_0', 'array_0', 3, 'b'),
                    ('array_1', 'array_1', 3, 'a'),
                    ('array_1', 'array_1', 3, 'b'),
                    ('array_2', 'array_2', 3, 'a'),
                    ('array_2', 'array_2', 3, 'b')
                ], names=['trendlb_pos_th', 'trendlb_neg_th', 'trendlb_mode', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.TRENDLB.run(close_ts, pos_th=pos_ths, neg_th=neg_ths, mode='PctChangeNorm').labels,
            pd.DataFrame(
                np.array([
                    [0.5, -0.3333333333333333, 0.6666666666666666, -0.6666666666666666, np.nan, np.nan],
                    [-0.5, 0.3333333333333333, 0.3333333333333333, -0.5, np.nan, np.nan],
                    [0.6666666666666666, -0.6666666666666666, 0.6666666666666666,
                     -0.6666666666666666, np.nan, np.nan],
                    [0.3333333333333333, -0.5, 0.3333333333333333, -0.5, np.nan, np.nan],
                    [np.nan, 0.5, np.nan, 0.5, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    ('array_0', 'array_0', 4, 'a'),
                    ('array_0', 'array_0', 4, 'b'),
                    ('array_1', 'array_1', 4, 'a'),
                    ('array_1', 'array_1', 4, 'b'),
                    ('array_2', 'array_2', 4, 'a'),
                    ('array_2', 'array_2', 4, 'b')
                ], names=['trendlb_pos_th', 'trendlb_neg_th', 'trendlb_mode', None])
            )
        )

    def test_BOLB(self):
        pd.testing.assert_frame_equal(
            vbt.BOLB.run(close_ts, window=1, pos_th=pos_ths, neg_th=neg_ths).labels,
            pd.DataFrame(
                np.array([
                    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0],
                    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (1, 'array_0', 'array_0', 'a'),
                    (1, 'array_0', 'array_0', 'b'),
                    (1, 'array_1', 'array_1', 'a'),
                    (1, 'array_1', 'array_1', 'b'),
                    (1, 'array_2', 'array_2', 'a'),
                    (1, 'array_2', 'array_2', 'b')
                ], names=['bolb_window', 'bolb_pos_th', 'bolb_neg_th', None])
            )
        )
        pd.testing.assert_frame_equal(
            vbt.BOLB.run(close_ts, window=2, pos_th=pos_ths, neg_th=neg_ths).labels,
            pd.DataFrame(
                np.array([
                    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0],
                    [1.0, -1.0, 1.0, -1.0, 0.0, 0.0],
                    [0.0, -1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 'array_0', 'array_0', 'a'),
                    (2, 'array_0', 'array_0', 'b'),
                    (2, 'array_1', 'array_1', 'a'),
                    (2, 'array_1', 'array_1', 'b'),
                    (2, 'array_2', 'array_2', 'a'),
                    (2, 'array_2', 'array_2', 'b')
                ], names=['bolb_window', 'bolb_pos_th', 'bolb_neg_th', None])
            )
        )
