from collections import namedtuple
from datetime import datetime
from itertools import product

import numpy as np
import pandas as pd
import pytest
from numba import njit

import vectorbt as vbt

ray_available = True
try:
    import ray
except:
    ray_available = False

ta_available = True
try:
    import ta
except:
    ta_available = False

pandas_ta_available = True
try:
    import pandas_ta
except:
    pandas_ta_available = False

talib_available = True
try:
    import talib
except:
    talib_available = False

seed = 42


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []
    if ray_available:
        ray.init(local_mode=True, num_cpus=1)


def teardown_module():
    if ray_available:
        ray.shutdown()
    vbt.settings.reset()


# ############# factory.py ############# #

ts = pd.DataFrame({
    'a': [1., 2., 3., 4., 5.],
    'b': [5., 4., 3., 2., 1.],
    'c': [1., 2., 3., 2., 1.]
}, index=pd.DatetimeIndex([
    datetime(2018, 1, 1),
    datetime(2018, 1, 2),
    datetime(2018, 1, 3),
    datetime(2018, 1, 4),
    datetime(2018, 1, 5)
]))


class TestFactory:
    def test_config(self, tmp_path):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def apply_func(ts, p, a, b=10):
            return ts * p + a + b

        I = F.from_apply_func(apply_func, var_args=True)
        indicator = I.run(ts, [0, 1], 10, b=100)
        assert I.loads(indicator.dumps()) == indicator
        indicator.save(tmp_path / 'indicator')
        assert I.load(tmp_path / 'indicator') == indicator

    def test_from_custom_func(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def apply_func(i, ts, p, a, b=10):
            return ts * p[i] + a + b

        @njit
        def apply_func_nb(i, ts, p, a, b):
            return ts * p[i] + a + b  # numba doesn't support **kwargs

        def custom_func(ts, p, *args, **kwargs):
            return vbt.base.combine_fns.apply_and_concat_one(len(p), apply_func, ts, p, *args, **kwargs)

        @njit
        def custom_func_nb(ts, p, *args):
            return vbt.base.combine_fns.apply_and_concat_one_nb(len(p), apply_func_nb, ts, p, *args)

        target = pd.DataFrame(
            np.array([
                [110., 110., 110., 111., 115., 111.],
                [110., 110., 110., 112., 114., 112.],
                [110., 110., 110., 113., 113., 113.],
                [110., 110., 110., 114., 112., 112.],
                [110., 110., 110., 115., 111., 111.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func, var_args=True).run(ts, [0, 1], 10, b=100).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func_nb, var_args=True).run(ts, [0, 1], 10, 100).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [110., 115., 112.],
                [110., 114., 114.],
                [110., 113., 116.],
                [110., 112., 114.],
                [110., 111., 112.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func, var_args=True).run(ts, [0, 1, 2], 10, b=100, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func_nb, var_args=True).run(ts, [0, 1, 2], 10, 100, per_column=True).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [110., 111.],
                [110., 112.],
                [110., 113.],
                [110., 114.],
                [110., 115.]
            ]),
            index=ts.index,
            columns=pd.Index([0, 1], dtype='int64', name='custom_p')
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func, var_args=True).run(ts['a'], [0, 1], 10, b=100).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func_nb, var_args=True).run(ts['a'], [0, 1], 10, 100).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [110.],
                [110.],
                [110.],
                [110.],
                [110.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([(0, 'a')], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func, var_args=True).run(ts[['a']], 0, 10, b=100, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func_nb, var_args=True).run(ts[['a']], 0, 10, 100, per_column=True).out,
            target
        )
        target = pd.Series(
            np.array([110., 110., 110., 110., 110.]),
            index=ts.index,
            name=(0, 'a')
        )
        pd.testing.assert_series_equal(
            F.from_custom_func(custom_func, var_args=True).run(ts['a'], 0, 10, b=100).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_custom_func(custom_func_nb, var_args=True).run(ts['a'], 0, 10, 100).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_custom_func(custom_func, var_args=True).run(ts['a'], 0, 10, b=100, per_column=True).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_custom_func(custom_func_nb, var_args=True).run(ts['a'], 0, 10, 100, per_column=True).out,
            target
        )

    def test_from_apply_func(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def apply_func(ts, p, a, b=10):
            return ts * p + a + b

        @njit
        def apply_func_nb(ts, p, a, b):
            return ts * p + a + b  # numba doesn't support **kwargs

        target = pd.DataFrame(
            np.array([
                [110., 110., 110., 111., 115., 111.],
                [110., 110., 110., 112., 114., 112.],
                [110., 110., 110., 113., 113., 113.],
                [110., 110., 110., 114., 112., 112.],
                [110., 110., 110., 115., 111., 111.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts, [0, 1], 10, b=100).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, var_args=True).run(ts, [0, 1], 10, 100).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [110., 115., 112.],
                [110., 114., 114.],
                [110., 113., 116.],
                [110., 112., 114.],
                [110., 111., 112.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts, [0, 1, 2], 10, b=100, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts, [0, 1, 2], 10, 100, per_column=True).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [110., 111.],
                [110., 112.],
                [110., 113.],
                [110., 114.],
                [110., 115.]
            ]),
            index=ts.index,
            columns=pd.Index([0, 1], dtype='int64', name='custom_p')
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts['a'], [0, 1], 10, b=100).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, var_args=True).run(ts['a'], [0, 1], 10, 100).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [110.],
                [110.],
                [110.],
                [110.],
                [110.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([(0, 'a')], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts[['a']], 0, 10, b=100, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts[['a']], 0, 10, 100, per_column=True).out,
            target
        )
        target = pd.Series(
            np.array([110., 110., 110., 110., 110.]),
            index=ts.index,
            name=(0, 'a')
        )
        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts['a'], 0, 10, b=100).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, var_args=True)
                .run(ts['a'], 0, 10, 100).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func, var_args=True).run(ts['a'], 0, 10, b=100, per_column=True).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, var_args=True)
                .run(ts['a'], 0, 10, 100, per_column=True).out,
            target
        )

    def test_use_ray(self):
        if ray_available:
            F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

            def apply_func(ts, p, a, b=10):
                return ts * p + a + b

            pd.testing.assert_frame_equal(
                F.from_apply_func(apply_func, var_args=True)
                    .run(ts, np.arange(10), 10, b=100).out,
                F.from_apply_func(apply_func, var_args=True)
                    .run(ts, np.arange(10), 10, b=100, use_ray=True).out,
            )

    def test_no_inputs(self):
        F = vbt.IndicatorFactory(param_names=['p'], output_names=['out'])

        def apply_func(p):
            return np.full((3, 3), p)

        @njit
        def apply_func_nb(p):
            return np.full((3, 3), p)

        target = pd.DataFrame(
            np.array([
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1]
            ]),
            index=pd.RangeIndex(start=0, stop=3, step=1),
            columns=pd.MultiIndex.from_tuples([
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 0),
                (1, 1),
                (1, 2)
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run([0, 1]).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run([0, 1]).out,
            target
        )
        with pytest.raises(Exception):
            F.from_apply_func(apply_func).run([0, 1], per_column=True)

    def test_input_shape(self):
        F = vbt.IndicatorFactory(param_names=['p'], output_names=['out'])

        def apply_func(input_shape, p):
            return np.full(input_shape, p)

        @njit
        def apply_func_nb(input_shape, p):
            return np.full(input_shape, p)

        target = pd.Series(
            np.array([0, 0, 0, 0, 0]),
            index=pd.RangeIndex(start=0, stop=5, step=1)
        )
        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func, require_input_shape=True).run(5, 0).out,
            target
        )
        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, require_input_shape=True).run(5, 0).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1]
            ]),
            index=pd.RangeIndex(start=0, stop=5, step=1),
            columns=pd.Index([0, 1], dtype='int64', name='custom_p')
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, require_input_shape=True).run(5, [0, 1]).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, require_input_shape=True).run(5, [0, 1]).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, require_input_shape=True).run(
                (5, 3), [0, 1], input_index=ts.index, input_columns=ts.columns).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, require_input_shape=True).run(
                (5, 3), [0, 1], input_index=ts.index, input_columns=ts.columns).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0, 1, 2],
                [0, 1, 2],
                [0, 1, 2],
                [0, 1, 2],
                [0, 1, 2]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, require_input_shape=True).run(
                (5, 3), [0, 1, 2], input_index=ts.index, input_columns=ts.columns, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, require_input_shape=True).run(
                (5, 3), [0, 1, 2], input_index=ts.index, input_columns=ts.columns, per_column=True).out,
            target
        )

    def test_multiple_inputs(self):
        F = vbt.IndicatorFactory(input_names=['ts1', 'ts2'], param_names=['p'], output_names=['out'])

        def apply_func(ts1, ts2, p):
            return ts1 * ts2 * p

        @njit
        def apply_func_nb(ts1, ts2, p):
            return ts1 * ts2 * p

        target = pd.DataFrame(
            np.array([
                [0., 0., 0., 1., 25., 1.],
                [0., 0., 0., 4., 16., 4.],
                [0., 0., 0., 9., 9., 9.],
                [0., 0., 0., 16., 4., 4.],
                [0., 0., 0., 25., 1., 1.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, ts, [0, 1]).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, ts, [0, 1]).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0., 25., 2.],
                [0., 16., 8.],
                [0., 9., 18.],
                [0., 4., 8.],
                [0., 1., 2.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, ts, [0, 1, 2], per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, ts, [0, 1, 2], per_column=True).out,
            target
        )

    def test_no_params(self):
        F = vbt.IndicatorFactory(input_names=['ts'], output_names=['out'])

        def apply_func(ts):
            return ts * 2

        @njit
        def apply_func_nb(ts):
            return ts * 2

        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts).out,
            ts * 2
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts).out,
            ts * 2
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, per_column=True).out,
            ts * 2
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, per_column=True).out,
            ts * 2
        )

    def test_no_inputs_and_params(self):
        F = vbt.IndicatorFactory(output_names=['out'])

        def apply_func():
            return np.full((3, 3), 1)

        @njit
        def apply_func_nb():
            return np.full((3, 3), 1)

        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run().out,
            pd.DataFrame(np.full((3, 3), 1))
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run().out,
            pd.DataFrame(np.full((3, 3), 1))
        )
        with pytest.raises(Exception):
            F.from_apply_func(apply_func).run(per_column=True)

    def test_multiple_params(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        def apply_func(ts, p1, p2):
            return ts * (p1 + p2)

        @njit
        def apply_func_nb(ts, p1, p2):
            return ts * (p1 + p2)

        target = pd.DataFrame(
            np.array([
                [2., 10., 2., 3., 15., 3.],
                [4., 8., 4., 6., 12., 6.],
                [6., 6., 6., 9., 9., 9.],
                [8., 4., 4., 12., 6., 6.],
                [10., 2., 2., 15., 3., 3.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 2, 'a'),
                (0, 2, 'b'),
                (0, 2, 'c'),
                (1, 2, 'a'),
                (1, 2, 'b'),
                (1, 2, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1]), 2).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, np.asarray([0, 1]), 2).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [2., 15., 4.],
                [4., 12., 8.],
                [6., 9., 12.],
                [8., 6., 8.],
                [10., 3., 4.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 2, 'a'),
                (1, 2, 'b'),
                (2, 2, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1, 2]), 2, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, np.asarray([0, 1, 2]), 2, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1, 2]), [2], per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1, 2]), np.array([2]), per_column=True).out,
            target
        )
        with pytest.raises(Exception):
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1]), 2, per_column=True)
        with pytest.raises(Exception):
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1, 2, 3]), 2, per_column=True)

    def test_param_settings(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def apply_func(ts, p):
            return ts * p

        @njit
        def apply_func_nb(ts, p):
            return ts * p

        target = pd.DataFrame(
            np.array([
                [0., 5., 2.],
                [0., 4., 4.],
                [0., 3., 6.],
                [0., 2., 4.],
                [0., 1., 2.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                ('array_0', 'a'),
                ('array_0', 'b'),
                ('array_0', 'c'),
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1, 2]), param_settings={'p': {
                'is_array_like': True
            }}).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, np.asarray([0, 1, 2]), param_settings={'p': {
                'is_array_like': True
            }}).out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0., 5., 2.],
                [0., 4., 4.],
                [0., 3., 6.],
                [0., 2., 4.],
                [0., 1., 2.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c'),
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, np.asarray([0, 1, 2]), param_settings={'p': {
                'is_array_like': True,
                'bc_to_input': 1,
                'per_column': True
            }}).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, np.asarray([0, 1, 2]), param_settings={'p': {
                'is_array_like': True,
                'bc_to_input': 1,
                'per_column': True
            }}).out,
            target
        )

        def apply_func2(ts, p):
            return ts * np.expand_dims(p, 1)

        @njit
        def apply_func2_nb(ts, p):
            return ts * np.expand_dims(p, 1)

        target = pd.DataFrame(
            np.array([
                [0., 0., 0.],
                [2., 4., 2.],
                [6., 6., 6.],
                [12., 6., 6.],
                [20., 4., 4.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                ('array_0', 'a'),
                ('array_0', 'b'),
                ('array_0', 'c'),
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func2).run(ts, np.asarray([0, 1, 2, 3, 4]), param_settings={'p': {
                'is_array_like': True,
                'bc_to_input': 0
            }}).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func2_nb).run(ts, np.asarray([0, 1, 2, 3, 4]), param_settings={'p': {
                'is_array_like': True,
                'bc_to_input': 0
            }}).out,
            target
        )

        def apply_func3(ts, p):
            return ts * (p[0] + p[1])

        @njit
        def apply_func3_nb(ts, p):
            return ts * (p[0] + p[1])

        target = pd.DataFrame(
            np.array([
                [1., 5., 1.],
                [2., 4., 2.],
                [3., 3., 3.],
                [4., 2., 2.],
                [5., 1., 1.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                ('tuple_0', 'a'),
                ('tuple_0', 'b'),
                ('tuple_0', 'c'),
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func3).run(ts, (0, 1), param_settings={'p': {
                'is_tuple': True
            }}).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func3_nb).run(ts, (0, 1), param_settings={'p': {
                'is_tuple': True
            }}).out,
            target
        )

    def test_param_product(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        def apply_func(ts, p1, p2):
            return ts * (p1 + p2)

        @njit
        def apply_func_nb(ts, p1, p2):
            return ts * (p1 + p2)

        target = pd.DataFrame(
            np.array([
                [2., 10., 2., 3., 15., 3., 3., 15., 3., 4., 20., 4.],
                [4., 8., 4., 6., 12., 6., 6., 12., 6., 8., 16., 8.],
                [6., 6., 6., 9., 9., 9., 9., 9., 9., 12., 12., 12.],
                [8., 4., 4., 12., 6., 6., 12., 6., 6., 16., 8., 8.],
                [10., 2., 2., 15., 3., 3., 15., 3., 3., 20., 4., 4.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 2, 'a'),
                (0, 2, 'b'),
                (0, 2, 'c'),
                (0, 3, 'a'),
                (0, 3, 'b'),
                (0, 3, 'c'),
                (1, 2, 'a'),
                (1, 2, 'b'),
                (1, 2, 'c'),
                (1, 3, 'a'),
                (1, 3, 'b'),
                (1, 3, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [0, 1], [2, 3], param_product=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, [0, 1], [2, 3], param_product=True).out,
            target
        )

    def test_default(self):
        F = vbt.IndicatorFactory(
            input_names=['ts1', 'ts2'],
            param_names=['p1', 'p2'],
            in_output_names=['in_out1', 'in_out2'],
            output_names=['out']
        )

        def apply_func(ts1, ts2, in_out1, in_out2, p1, p2):
            in_out1[::2] = ts1[::2] * ts2[::2] * (p1 + p2)
            in_out2[::2] = ts1[::2] * ts2[::2] * (p1 + p2)
            return ts1 * ts2 * (p1 + p2)

        # default inputs
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, ts2=0).run(ts, [1, 2], 3).out,
            F.from_apply_func(apply_func).run(ts, 0, [1, 2], 3).out
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, ts2='ts1').run(ts, [1, 2], 3).out,
            F.from_apply_func(apply_func).run(ts, ts, [1, 2], 3).out
        )
        # default params
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, p2=0, hide_default=False)
                .run(ts, ts, [1, 2]).out,
            F.from_apply_func(apply_func, hide_default=False)
                .run(ts, ts, [1, 2], 0).out
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, p2='p1', hide_default=False)
                .run(ts, ts, [1, 2]).out,
            F.from_apply_func(apply_func, hide_default=False)
                .run(ts, ts, [1, 2], [1, 2]).out
        )
        with pytest.raises(Exception):
            pd.testing.assert_frame_equal(
                F.from_apply_func(apply_func, in_out1=1, in_out2=2)
                    .run(ts, ts, [1, 2], 3).in_out1,
                F.from_apply_func(apply_func, in_out1=1, in_out2=2)
                    .run(ts, ts, [1, 2], 3).in_out2
            )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, in_out1=1, in_out2='in_out1')
                .run(ts, ts, [1, 2], 3).in_out2,
            F.from_apply_func(apply_func, in_out1=1, in_out2=1)
                .run(ts, ts, [1, 2], 3).in_out2
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, in_out1=1, in_out2='ts1')
                .run(ts, ts, [1, 2], 3).in_out2,
            F.from_apply_func(apply_func, in_out1=1, in_out2=ts)
                .run(ts, ts, [1, 2], 3).in_out2
        )

    def test_hide_params(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        assert F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2, hide_params=[]) \
                   .run(ts, [0, 1], 2) \
                   .out.columns.names == ['custom_p1', 'custom_p2', None]
        assert F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2, hide_params=['p2']) \
                   .run(ts, [0, 1], 2) \
                   .out.columns.names == ['custom_p1', None]

    def test_hide_default(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        assert F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2, p2=2, hide_default=False) \
                   .run(ts, [0, 1]) \
                   .out.columns.names == ['custom_p1', 'custom_p2', None]
        assert F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2, p2=2, hide_default=True) \
                   .run(ts, [0, 1]) \
                   .out.columns.names == ['custom_p1', None]

    def test_multiple_outputs(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['o1', 'o2'])

        def apply_func(ts, p):
            return (ts * p, (ts * p) ** 2)

        @njit
        def apply_func_nb(ts, p):
            return (ts * p, (ts * p) ** 2)

        target = pd.DataFrame(
            np.array([
                [0., 0., 0., 1., 5., 1.],
                [0., 0., 0., 2., 4., 2.],
                [0., 0., 0., 3., 3., 3.],
                [0., 0., 0., 4., 2., 2.],
                [0., 0., 0., 5., 1., 1.]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [0, 1]).o1,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, [0, 1]).o1,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts.vbt.tile(2), [0, 0, 0, 1, 1, 1], per_column=True).o1,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True)
                .run(ts.vbt.tile(2), [0, 0, 0, 1, 1, 1], per_column=True).o1,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0., 0., 0., 1., 25., 1.],
                [0., 0., 0., 4., 16., 4.],
                [0., 0., 0., 9., 9., 9.],
                [0., 0., 0., 16., 4., 4.],
                [0., 0., 0., 25., 1., 1.]
            ]),
            index=target.index,
            columns=target.columns
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [0, 1]).o2,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, [0, 1]).o2,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts.vbt.tile(2), [0, 0, 0, 1, 1, 1], per_column=True).o2,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True)
                .run(ts.vbt.tile(2), [0, 0, 0, 1, 1, 1], per_column=True).o2,
            target
        )

    def test_in_outputs(self):
        F = vbt.IndicatorFactory(
            input_names=['ts'], param_names=['p'],
            output_names=['out'], in_output_names=['in_out']
        )

        def apply_func(ts, in_out, p):
            in_out[:, 0] = p
            return ts * p

        @njit
        def apply_func_nb(ts, in_out, p):
            in_out[:, 0] = p
            return ts * p

        target = pd.DataFrame(
            np.array([
                [0, -1, -1, 1, -1, -1],
                [0, -1, -1, 1, -1, -1],
                [0, -1, -1, 1, -1, -1],
                [0, -1, -1, 1, -1, -1],
                [0, -1, -1, 1, -1, -1]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        assert F.from_apply_func(apply_func).run(ts, [0, 1])._in_out.dtype == np.float64
        assert F.from_apply_func(apply_func, in_output_settings={'in_out': {'dtype': np.int64}}) \
                   .run(ts, [0, 1])._in_out.dtype == np.int64
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, in_out=-1).run(ts, [0, 1]).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, in_out=-1).run(ts, [0, 1]).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [0, 1], in_out=-1).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, [0, 1], in_out=-1).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [0, 1], in_out=np.full(ts.shape, -1, dtype=int)).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True)
                .run(ts, [0, 1], in_out=np.full(ts.shape, -1, dtype=int)).in_out,
            target
        )
        target = pd.DataFrame(
            np.array([
                [0, 1, 2],
                [0, 1, 2],
                [0, 1, 2],
                [0, 1, 2],
                [0, 1, 2]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [0, 1, 2], in_out=-1, per_column=True).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True).run(ts, [0, 1, 2], in_out=-1, per_column=True).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func)
                .run(ts, [0, 1, 2], in_out=np.full(ts.shape, -1, dtype=int), per_column=True).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True)
                .run(ts, [0, 1, 2], in_out=np.full(ts.shape, -1, dtype=int), per_column=True).in_out,
            target
        )

    def test_no_outputs(self):
        F = vbt.IndicatorFactory(
            param_names=['p'], in_output_names=['in_out']
        )

        def apply_func(in_out, p):
            in_out[:] = p

        @njit
        def apply_func_nb(in_out, p):
            in_out[:] = p

        target = pd.DataFrame(
            np.array([
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, in_output_settings=dict(in_out=dict(dtype=np.int64)))
                .run([0, 1], input_shape=ts.shape, input_index=ts.index, input_columns=ts.columns).in_out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, in_output_settings=dict(in_out=dict(dtype=np.int64)))
                .run([0, 1], input_shape=ts.shape, input_index=ts.index, input_columns=ts.columns).in_out,
            target
        )

    def test_kwargs_to_args(self):
        F = vbt.IndicatorFactory(input_names=['ts'], output_names=['out'])

        def apply_func(ts, kw):
            return ts * kw

        @njit
        def apply_func_nb(ts, kw):
            return ts * kw

        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func, kwargs_to_args=['kw']).run(ts, kw=2).out,
            ts * 2
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func_nb, numba_loop=True, kwargs_to_args=['kw']).run(ts, kw=2).out,
            ts * 2
        )

    def test_cache(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def cache_func(ts, ps):
            np.random.seed(seed)
            return np.random.uniform(0, 1)

        @njit
        def cache_func_nb(ts, ps):
            np.random.seed(seed)
            return np.random.uniform(0, 1)

        def apply_func(ts, p, c):
            return ts * p + c

        @njit
        def apply_func_nb(ts, p, c):
            return ts * p + c

        target = pd.DataFrame(
            np.array([
                [0.37454012, 0.37454012, 0.37454012, 1.37454012, 5.37454012, 1.37454012],
                [0.37454012, 0.37454012, 0.37454012, 2.37454012, 4.37454012, 2.37454012],
                [0.37454012, 0.37454012, 0.37454012, 3.37454012, 3.37454012, 3.37454012],
                [0.37454012, 0.37454012, 0.37454012, 4.37454012, 2.37454012, 2.37454012],
                [0.37454012, 0.37454012, 0.37454012, 5.37454012, 1.37454012, 1.37454012]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (0, 'b'),
                (0, 'c'),
                (1, 'a'),
                (1, 'b'),
                (1, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func,
                cache_func=cache_func
            ).run(ts, [0, 1]).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func_nb,
                cache_func=cache_func_nb
            ).run(ts, [0, 1]).out,
            target
        )
        # return_cache
        cache = F.from_apply_func(
            apply_func,
            cache_func=cache_func
        ).run(ts, [0, 1], return_cache=True)
        assert cache == 0.3745401188473625
        cache = F.from_apply_func(
            apply_func_nb,
            cache_func=cache_func_nb
        ).run(ts, [0, 1], return_cache=True)
        assert cache == 0.3745401188473625
        # use_cache
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func
            ).run(ts, [0, 1], use_cache=cache).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func_nb
            ).run(ts, [0, 1], use_cache=cache).out,
            target
        )

        # per_column
        def cache_func(col, ts, ps):
            np.random.seed(seed + col)
            return np.random.uniform(0, 1)

        @njit
        def cache_func_nb(col, ts, ps):
            np.random.seed(seed + col)
            return np.random.uniform(0, 1)

        cache = F.from_apply_func(
            apply_func,
            cache_func=cache_func,
            pass_col=True
        ).run(ts, [0, 1, 2], return_cache=True, per_column=True)
        assert cache == [0.3745401188473625, 0.11505456638977896, 0.8348421486656494]
        cache = F.from_apply_func(
            apply_func_nb,
            cache_func=cache_func_nb,
            pass_col=True
        ).run(ts, [0, 1, 2], return_cache=True, per_column=True)
        assert cache == [0.3745401188473625, 0.11505456638977896, 0.8348421486656494]
        target = pd.DataFrame(
            np.array([
                [0.37454012, 5.115054566389779, 2.8348421486656497],
                [0.37454012, 4.115054566389779, 4.8348421486656497],
                [0.37454012, 3.115054566389779, 6.8348421486656497],
                [0.37454012, 2.115054566389779, 4.8348421486656497],
                [0.37454012, 1.115054566389779, 2.8348421486656497]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (0, 'a'),
                (1, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func
            ).run(ts, [0, 1, 2], use_cache=cache, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func_nb
            ).run(ts, [0, 1, 2], use_cache=cache, per_column=True).out,
            target
        )

    def test_raw(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def apply_func(ts, p, a, b=10):
            return ts * p + a + b

        @njit
        def apply_func_nb(ts, p, a, b):
            return ts * p + a + b

        target = np.array([
            [110., 110., 110., 111., 115., 111.],
            [110., 110., 110., 112., 114., 112.],
            [110., 110., 110., 113., 113., 113.],
            [110., 110., 110., 114., 112., 112.],
            [110., 110., 110., 115., 111., 111.]
        ])
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func, var_args=True
            ).run(ts, [0, 1], 10, b=100, return_raw=True)[0][0],
            target
        )
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func_nb, var_args=True
            ).run(ts, [0, 1], 10, 100, return_raw=True)[0][0],
            target
        )
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func, var_args=True
            ).run(ts, [0, 1], 10, b=100, return_raw=True)[1],
            [(0,), (1,)]
        )
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func_nb, var_args=True
            ).run(ts, [0, 1], 10, 100, return_raw=True)[1],
            [(0,), (1,)]
        )
        assert F.from_apply_func(
            apply_func, var_args=True
        ).run(ts, [0, 1], 10, b=100, return_raw=True)[2] == 3
        assert F.from_apply_func(
            apply_func_nb, var_args=True
        ).run(ts, [0, 1], 10, 100, return_raw=True)[2] == 3
        assert F.from_apply_func(
            apply_func, var_args=True
        ).run(ts, [0, 1], 10, b=100, return_raw=True)[3] == []
        assert F.from_apply_func(
            apply_func_nb, var_args=True
        ).run(ts, [0, 1], 10, 100, return_raw=True)[3] == []
        raw_results = F.from_apply_func(
            apply_func, var_args=True
        ).run(ts, [0, 1, 2], 10, b=100, return_raw=True)
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func, var_args=True
            ).run(ts, [0, 1], 10, b=100, use_raw=raw_results).out,
            F.from_apply_func(
                apply_func_nb, var_args=True
            ).run(ts, [0, 1], 10, 100).out
        )

        # per_column
        target = np.array([
            [110., 115., 112.],
            [110., 114., 114.],
            [110., 113., 116.],
            [110., 112., 114.],
            [110., 111., 112.]
        ])
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func, var_args=True
            ).run(ts, [0, 1, 2], 10, b=100, return_raw=True, per_column=True)[0][0],
            target
        )
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func_nb, var_args=True
            ).run(ts, [0, 1, 2], 10, 100, return_raw=True, per_column=True)[0][0],
            target
        )
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func, var_args=True
            ).run(ts, [0, 1, 2], 10, b=100, return_raw=True, per_column=True)[1],
            [(0,), (1,), (2,)]
        )
        np.testing.assert_array_equal(
            F.from_apply_func(
                apply_func_nb, var_args=True
            ).run(ts, [0, 1, 2], 10, 100, return_raw=True, per_column=True)[1],
            [(0,), (1,), (2,)]
        )
        assert F.from_apply_func(
            apply_func, var_args=True
        ).run(ts, [0, 1, 2], 10, b=100, return_raw=True)[2] == 3
        assert F.from_apply_func(
            apply_func_nb, var_args=True
        ).run(ts, [0, 1, 2], 10, 100, return_raw=True)[2] == 3
        assert F.from_apply_func(
            apply_func, var_args=True
        ).run(ts, [0, 1, 2], 10, b=100, return_raw=True)[3] == []
        assert F.from_apply_func(
            apply_func_nb, var_args=True
        ).run(ts, [0, 1, 2], 10, 100, return_raw=True)[3] == []
        raw_results = F.from_apply_func(
            apply_func, var_args=True
        ).run(ts, [0, 1, 2], 10, b=100, return_raw=True)
        pd.testing.assert_frame_equal(
            F.from_apply_func(
                apply_func, var_args=True
            ).run(ts, [0, 0, 0], 10, b=100, use_raw=raw_results).out,
            F.from_apply_func(
                apply_func_nb, var_args=True
            ).run(ts, [0, 0, 0], 10, 100).out
        )

    @pytest.mark.parametrize(
        "test_to_2d,test_keep_pd",
        [
            (False, False),
            (False, True),
            (True, False),
            (True, True)
        ]
    )
    def test_to_2d_and_keep_pd(self, test_to_2d, test_keep_pd):
        F = vbt.IndicatorFactory(input_names=['ts'], in_output_names=['in_out'], output_names=['out'])

        def custom_func(_ts, _in_out):
            if test_to_2d:
                assert _ts.ndim == 2
                for __in_out in _in_out:
                    assert __in_out.ndim == 2
                if test_keep_pd:
                    pd.testing.assert_frame_equal(_ts, ts[['a']].vbt.wrapper.wrap(_ts.values))
                    for __in_out in _in_out:
                        pd.testing.assert_frame_equal(__in_out, ts[['a']].vbt.wrapper.wrap(__in_out.values))
            else:
                assert _ts.ndim == 1
                for __in_out in _in_out:
                    assert __in_out.ndim == 1
                if test_keep_pd:
                    pd.testing.assert_series_equal(_ts, ts['a'].vbt.wrapper.wrap(_ts.values))
                    for __in_out in _in_out:
                        pd.testing.assert_series_equal(__in_out, ts['a'].vbt.wrapper.wrap(__in_out.values))
            return _ts

        def apply_func(_ts, _in_out):
            if test_to_2d:
                assert _ts.ndim == 2
                assert _in_out.ndim == 2
                if test_keep_pd:
                    pd.testing.assert_frame_equal(_ts, ts[['a']].vbt.wrapper.wrap(_ts.values))
                    pd.testing.assert_frame_equal(_in_out, ts[['a']].vbt.wrapper.wrap(_in_out.values))
            else:
                assert _ts.ndim == 1
                assert _in_out.ndim == 1
                if test_keep_pd:
                    pd.testing.assert_series_equal(_ts, ts['a'].vbt.wrapper.wrap(_ts.values))
                    pd.testing.assert_series_equal(_in_out, ts['a'].vbt.wrapper.wrap(_in_out.values))
            return _ts

        _ = F.from_custom_func(custom_func, to_2d=test_to_2d, keep_pd=test_keep_pd, var_args=True) \
            .run(ts['a'])
        _ = F.from_apply_func(apply_func, to_2d=test_to_2d, keep_pd=test_keep_pd, var_args=True) \
            .run(ts['a'])

        def custom_func(_ts, _in_out, col=None):
            if test_to_2d:
                assert _ts.ndim == 2
                for __in_out in _in_out:
                    assert __in_out.ndim == 2
                if test_keep_pd:
                    pd.testing.assert_frame_equal(_ts, ts.iloc[:, [col]].vbt.wrapper.wrap(_ts.values))
                    for __in_out in _in_out:
                        pd.testing.assert_frame_equal(__in_out, ts.iloc[:, [col]].vbt.wrapper.wrap(__in_out.values))
            else:
                assert _ts.ndim == 1
                for __in_out in _in_out:
                    assert __in_out.ndim == 1
                if test_keep_pd:
                    pd.testing.assert_series_equal(_ts, ts.iloc[:, col].vbt.wrapper.wrap(_ts.values))
                    for __in_out in _in_out:
                        pd.testing.assert_series_equal(__in_out, ts.iloc[:, col].vbt.wrapper.wrap(__in_out.values))
            return _ts

        def apply_func(col, _ts, _in_out):
            if test_to_2d:
                assert _ts.ndim == 2
                assert _in_out.ndim == 2
                if test_keep_pd:
                    pd.testing.assert_frame_equal(_ts, ts.iloc[:, [col]].vbt.wrapper.wrap(_ts.values))
                    pd.testing.assert_frame_equal(_in_out, ts.iloc[:, [col]].vbt.wrapper.wrap(_in_out.values))
            else:
                assert _ts.ndim == 1
                assert _in_out.ndim == 1
                if test_keep_pd:
                    pd.testing.assert_series_equal(_ts, ts.iloc[:, col].vbt.wrapper.wrap(_ts.values))
                    pd.testing.assert_series_equal(_in_out, ts.iloc[:, col].vbt.wrapper.wrap(_in_out.values))
            return _ts

        _ = F.from_custom_func(custom_func, to_2d=test_to_2d, keep_pd=test_keep_pd, var_args=True) \
            .run(ts['a'], per_column=True, pass_col=True)
        _ = F.from_apply_func(apply_func, to_2d=test_to_2d, keep_pd=test_keep_pd, var_args=True) \
            .run(ts['a'], per_column=True, pass_col=True)

    def test_as_lists(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out'])

        def custom_func(input_list, in_output_list, param_list):
            return input_list[0] * param_list[0][0]

        @njit
        def custom_func_nb(input_list, in_output_list, param_list):
            return input_list[0] * param_list[0][0]

        target = pd.DataFrame(
            ts.values * 2,
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (2, 'a'),
                (2, 'b'),
                (2, 'c')
            ], names=['custom_p', None])
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func, as_lists=True).run(ts, 2).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func_nb, as_lists=True).run(ts, 2).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func, as_lists=True).run(ts, 2, per_column=True).out,
            target
        )
        pd.testing.assert_frame_equal(
            F.from_custom_func(custom_func_nb, as_lists=True).run(ts, 2, per_column=True).out,
            target
        )

    def test_other(self):
        F = vbt.IndicatorFactory(input_names=['ts'], output_names=['o1', 'o2'])

        def custom_func(ts):
            return ts, ts + 1, ts + 2

        @njit
        def custom_func_nb(ts):
            return ts, ts + 1, ts + 2

        obj, other = F.from_custom_func(custom_func).run(ts)
        np.testing.assert_array_equal(other, ts + 2)
        obj, other = F.from_custom_func(custom_func_nb).run(ts)
        np.testing.assert_array_equal(other, ts + 2)
        obj, *others = F.from_custom_func(custom_func).run(ts, per_column=True)
        for i, other in enumerate(others):
            np.testing.assert_array_equal(other[0], ts.iloc[:, [i]] + 2)
        obj, *others = F.from_custom_func(custom_func_nb).run(ts, per_column=True)
        for i, other in enumerate(others):
            np.testing.assert_array_equal(other[0], ts.iloc[:, [i]] + 2)

    def test_run_unique(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        def apply_func(ts, p1, p2):
            return ts * (p1 + p2)

        pd.testing.assert_series_equal(
            F.from_apply_func(apply_func).run(ts['a'], 2, 3, run_unique=True).out,
            F.from_apply_func(apply_func).run(ts['a'], 2, 3, run_unique=False).out
        )
        raw = F.from_apply_func(apply_func).run(ts['a'], [2, 2, 2], [3, 3, 3], run_unique=True, return_raw=True)
        np.testing.assert_array_equal(
            raw[0][0],
            np.array([[5.], [10.], [15.], [20.], [25.]])
        )
        assert raw[1] == [(2, 3)]
        assert raw[2] == 1
        assert raw[3] == []
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts['a'], [2, 2, 2], [3, 3, 3], run_unique=True).out,
            F.from_apply_func(apply_func).run(ts['a'], [2, 2, 2], [3, 3, 3], run_unique=False).out
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, 2, 3, run_unique=True).out,
            F.from_apply_func(apply_func).run(ts, 2, 3, run_unique=False).out
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [2, 2, 2], [3, 3, 3], run_unique=True).out,
            F.from_apply_func(apply_func).run(ts, [2, 2, 2], [3, 3, 3], run_unique=False).out
        )
        pd.testing.assert_frame_equal(
            F.from_apply_func(apply_func).run(ts, [2, 3, 4], [4, 3, 2], run_unique=True).out,
            F.from_apply_func(apply_func).run(ts, [2, 3, 4], [4, 3, 2], run_unique=False).out
        )

    def test_run_combs(self):
        # itertools.combinations
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        ind1 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run(ts, [2, 2, 3], [10, 10, 11], short_name='custom_1')
        ind2 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run(ts, [3, 4, 4], [11, 12, 12], short_name='custom_2')
        ind1_1, ind2_1 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run_combs(ts, [2, 3, 4], [10, 11, 12], r=2, run_unique=False)
        ind1_2, ind2_2 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run_combs(ts, [2, 3, 4], [10, 11, 12], r=2, run_unique=True)
        pd.testing.assert_frame_equal(
            ind1.out,
            ind1_1.out
        )
        pd.testing.assert_frame_equal(
            ind2.out,
            ind2_1.out
        )
        pd.testing.assert_frame_equal(
            ind1.out,
            ind1_2.out
        )
        pd.testing.assert_frame_equal(
            ind2.out,
            ind2_2.out
        )
        # itertools.product
        ind3 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run(ts, [2, 2, 2, 3, 3, 3, 4, 4, 4], [10, 10, 10, 11, 11, 11, 12, 12, 12], short_name='custom_1')
        ind4 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run(ts, [2, 3, 4, 2, 3, 4, 2, 3, 4], [10, 11, 12, 10, 11, 12, 10, 11, 12], short_name='custom_2')
        ind3_1, ind4_1 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run_combs(ts, [2, 3, 4], [10, 11, 12], r=2, comb_func=product, run_unique=False)
        ind3_2, ind4_2 = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2) \
            .run_combs(ts, [2, 3, 4], [10, 11, 12], r=2, comb_func=product, run_unique=True)
        pd.testing.assert_frame_equal(
            ind3.out,
            ind3_1.out
        )
        pd.testing.assert_frame_equal(
            ind4.out,
            ind4_1.out
        )
        pd.testing.assert_frame_equal(
            ind3.out,
            ind3_2.out
        )
        pd.testing.assert_frame_equal(
            ind4.out,
            ind4_2.out
        )

    def test_wrapper(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts['a'], 0, 1)
        assert obj.wrapper.ndim == 1
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 1, 'a')
            ], names=['custom_p1', 'custom_p2', None])
        )
        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts['a'], [0, 1], 2)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 2),
                (1, 2),
            ], names=['custom_p1', 'custom_p2'])
        )
        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts, 0, 1)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 1, 'a'),
                (0, 1, 'b'),
                (0, 1, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )
        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts, [1, 2], 3)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (1, 3, 'a'),
                (1, 3, 'b'),
                (1, 3, 'c'),
                (2, 3, 'a'),
                (2, 3, 'b'),
                (2, 3, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )
        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts['a'], 0, 1, per_column=True)
        assert obj.wrapper.ndim == 1
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 1, 'a')
            ], names=['custom_p1', 'custom_p2', None])
        )
        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts[['a']], 0, 1, per_column=True)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 1, 'a')
            ], names=['custom_p1', 'custom_p2', None])
        )
        obj = F.from_apply_func(lambda ts, p1, p2: ts * p1 * p2).run(ts, 0, 1, per_column=True)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 1, 'a'),
                (0, 1, 'b'),
                (0, 1, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )

    @pytest.mark.parametrize(
        "test_config",
        [
            lambda F, shape, *args, **kwargs: F.from_apply_func(
                lambda input_shape, p1, p2: np.empty(input_shape) * p1 * p2, require_input_shape=True)
                .run(shape, *args, **kwargs),
            lambda F, shape, *args, **kwargs: F.from_apply_func(
                lambda p1, p2: np.full(shape, p1 + p2))
                .run(*args, **kwargs)
        ]
    )
    def test_no_inputs_wrapper(self, test_config):
        F = vbt.IndicatorFactory(param_names=['p1', 'p2'], output_names=['out'])

        obj = test_config(F, (5,), 0, 1)
        assert obj.wrapper.ndim == 1
        pd.testing.assert_index_equal(obj.wrapper.index, pd.RangeIndex(start=0, stop=5, step=1))
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 1),
            ], names=['custom_p1', 'custom_p2'])
        )
        obj = test_config(F, (5,), [0, 1], 2)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, pd.RangeIndex(start=0, stop=5, step=1))
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 2),
                (1, 2)
            ], names=['custom_p1', 'custom_p2'])
        )
        obj = test_config(F, (5, 3), [0, 1], 2)
        assert obj.wrapper.ndim == 2
        pd.testing.assert_index_equal(obj.wrapper.index, pd.RangeIndex(start=0, stop=5, step=1))
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 2, 0),
                (0, 2, 1),
                (0, 2, 2),
                (1, 2, 0),
                (1, 2, 1),
                (1, 2, 2)
            ], names=['custom_p1', 'custom_p2', None])
        )
        obj = test_config(F, ts.shape, [0, 1], 2, input_index=ts.index, input_columns=ts.columns)
        assert obj.wrapper.ndim == ts.ndim
        pd.testing.assert_index_equal(obj.wrapper.index, ts.index)
        pd.testing.assert_index_equal(
            obj.wrapper.columns,
            pd.MultiIndex.from_tuples([
                (0, 2, 'a'),
                (0, 2, 'b'),
                (0, 2, 'c'),
                (1, 2, 'a'),
                (1, 2, 'b'),
                (1, 2, 'c')
            ], names=['custom_p1', 'custom_p2', None])
        )

    def test_mappers(self):
        F = vbt.IndicatorFactory(input_names=['ts'], param_names=['p1', 'p2'], output_names=['out'])

        obj = F.from_apply_func(lambda ts, p1, p2: ts * (p1 + p2)) \
            .run(ts, 0, 2)
        np.testing.assert_array_equal(
            obj._input_mapper,
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            obj._p1_mapper,
            np.array([0, 0, 0])
        )
        np.testing.assert_array_equal(
            obj._p2_mapper,
            np.array([2, 2, 2])
        )
        assert obj._tuple_mapper == [(0, 2), (0, 2), (0, 2)]
        obj = F.from_apply_func(lambda ts, p1, p2: ts * (p1 + p2)) \
            .run(ts, [0, 1], [1, 2])
        np.testing.assert_array_equal(
            obj._input_mapper,
            np.array([0, 1, 2, 0, 1, 2])
        )
        np.testing.assert_array_equal(
            obj._p1_mapper,
            np.array([0, 0, 0, 1, 1, 1])
        )
        np.testing.assert_array_equal(
            obj._p2_mapper,
            np.array([1, 1, 1, 2, 2, 2])
        )
        assert obj._tuple_mapper == [(0, 1), (0, 1), (0, 1), (1, 2), (1, 2), (1, 2)]
        obj = F.from_apply_func(lambda ts, p1, p2: ts * (p1 + p2)) \
            .run(ts, [0, 1, 2], 3, per_column=True)
        np.testing.assert_array_equal(
            obj._input_mapper,
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            obj._p1_mapper,
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            obj._p2_mapper,
            np.array([3, 3, 3])
        )
        assert obj._tuple_mapper == [(0, 3), (1, 3), (2, 3)]

    def test_properties(self):
        I = vbt.IndicatorFactory(
            input_names=['ts1', 'ts2'],
            param_names=['p1', 'p2'],
            output_names=['o1', 'o2'],
            in_output_names=['in_o1', 'in_o2'],
            output_flags={'o1': 'Hello'}
        ).from_apply_func(lambda ts1, ts2, p1, p2, in_o1, in_o2: (ts1, ts2))
        obj = I.run(ts, ts, [0, 1], 2)

        # Class properties
        assert I.input_names == ('ts1', 'ts2')
        assert I.param_names == ('p1', 'p2')
        assert I.output_names == ('o1', 'o2')
        assert I.in_output_names == ('in_o1', 'in_o2')
        assert I.output_flags == {'o1': 'Hello'}

        # Instance properties
        assert obj.input_names == ('ts1', 'ts2')
        assert obj.param_names == ('p1', 'p2')
        assert obj.output_names == ('o1', 'o2')
        assert obj.in_output_names == ('in_o1', 'in_o2')
        assert obj.output_flags == {'o1': 'Hello'}
        assert obj.short_name == 'custom'
        assert obj.level_names == ('custom_p1', 'custom_p2')
        assert obj.p1_list == [0, 1]
        assert obj.p2_list == [2, 2]

    @pytest.mark.parametrize(
        "test_attr",
        ['ts1', 'ts2', 'o1', 'o2', 'in_o1', 'in_o2', 'co1', 'co2']
    )
    def test_indexing(self, test_attr):
        obj = vbt.IndicatorFactory(
            input_names=['ts1', 'ts2'],
            param_names=['p1', 'p2'],
            output_names=['o1', 'o2'],
            in_output_names=['in_o1', 'in_o2'],
            custom_output_props={
                'co1': lambda self: self.ts1 + self.ts2,
                'co2': lambda self: self.o1 + self.o2
            }
        ).from_apply_func(lambda ts1, ts2, p1, p2, in_o1, in_o2: (ts1, ts2)).run(ts, ts + 1, [1, 2], 3)

        pd.testing.assert_frame_equal(
            getattr(obj.iloc[np.arange(3), np.arange(3)], test_attr),
            getattr(obj, test_attr).iloc[np.arange(3), np.arange(3)]
        )
        pd.testing.assert_series_equal(
            getattr(obj.loc[:, (1, 3, 'a')], test_attr),
            getattr(obj, test_attr).loc[:, (1, 3, 'a')]
        )
        pd.testing.assert_frame_equal(
            getattr(obj.loc[:, (1, 3)], test_attr),
            getattr(obj, test_attr).loc[:, (1, 3)]
        )
        pd.testing.assert_frame_equal(
            getattr(obj[(1, 3)], test_attr),
            getattr(obj, test_attr)[(1, 3)]
        )
        pd.testing.assert_frame_equal(
            getattr(obj.xs(1, axis=1, level=0), test_attr),
            getattr(obj, test_attr).xs(1, axis=1, level=0)
        )
        pd.testing.assert_frame_equal(
            getattr(obj.p1_loc[2], test_attr),
            getattr(obj, test_attr).xs(2, level='custom_p1', axis=1)
        )
        pd.testing.assert_frame_equal(
            getattr(obj.p1_loc[1:2], test_attr),
            pd.concat((
                getattr(obj, test_attr).xs(1, level='custom_p1', drop_level=False, axis=1),
                getattr(obj, test_attr).xs(2, level='custom_p1', drop_level=False, axis=1)
            ), axis=1)
        )
        pd.testing.assert_frame_equal(
            getattr(obj.p1_loc[[1, 1, 1]], test_attr),
            pd.concat((
                getattr(obj, test_attr).xs(1, level='custom_p1', drop_level=False, axis=1),
                getattr(obj, test_attr).xs(1, level='custom_p1', drop_level=False, axis=1),
                getattr(obj, test_attr).xs(1, level='custom_p1', drop_level=False, axis=1)
            ), axis=1)
        )
        pd.testing.assert_frame_equal(
            getattr(obj.tuple_loc[(1, 3)], test_attr),
            getattr(obj, test_attr).xs((1, 3), level=('custom_p1', 'custom_p2'), axis=1)
        )
        pd.testing.assert_frame_equal(
            getattr(obj.tuple_loc[(1, 3):(2, 3)], test_attr),
            pd.concat((
                getattr(obj, test_attr).xs((1, 3), level=('custom_p1', 'custom_p2'), drop_level=False, axis=1),
                getattr(obj, test_attr).xs((2, 3), level=('custom_p1', 'custom_p2'), drop_level=False, axis=1)
            ), axis=1)
        )
        pd.testing.assert_frame_equal(
            getattr(obj.tuple_loc[[(1, 3), (1, 3), (1, 3)]], test_attr),
            pd.concat((
                getattr(obj, test_attr).xs((1, 3), level=('custom_p1', 'custom_p2'), drop_level=False, axis=1),
                getattr(obj, test_attr).xs((1, 3), level=('custom_p1', 'custom_p2'), drop_level=False, axis=1),
                getattr(obj, test_attr).xs((1, 3), level=('custom_p1', 'custom_p2'), drop_level=False, axis=1)
            ), axis=1)
        )

    def test_numeric_attr(self):
        obj = vbt.IndicatorFactory(input_names=['ts'], param_names=['p'], output_names=['out']) \
            .from_apply_func(lambda ts, p: ts * p).run(ts, 1)

        pd.testing.assert_frame_equal(obj.out_above(2), obj.out > 2)
        target = pd.DataFrame(
            np.array([
                [False, True, False, False, True, False],
                [False, True, False, False, True, False],
                [True, True, True, False, False, False],
                [True, False, False, True, False, False],
                [True, False, False, True, False, False]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (2, 1, 'a'),
                (2, 1, 'b'),
                (2, 1, 'c'),
                (3, 1, 'a'),
                (3, 1, 'b'),
                (3, 1, 'c'),
            ], names=['custom_out_above', 'custom_p', None])
        )
        pd.testing.assert_frame_equal(
            obj.out_above([2, 3]),
            target
        )
        columns = target.columns.set_names('my_above', level=0)
        pd.testing.assert_frame_equal(
            obj.out_above([2, 3], level_name='my_above'),
            pd.DataFrame(
                target.values,
                index=target.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            obj.out_crossed_above(2),
            pd.DataFrame(
                np.array([
                    [False, False, False],
                    [False, False, False],
                    [True, False, True],
                    [False, False, False],
                    [False, False, False]
                ]),
                index=ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (1, 'a'),
                    (1, 'b'),
                    (1, 'c'),
                ], names=['custom_p', None])
            )
        )
        pd.testing.assert_series_equal(
            obj.out_stats(),
            pd.Series([
                pd.Timestamp('2018-01-01 00:00:00'),
                pd.Timestamp('2018-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'),
                5.0, 2.6, 1.3329792289008184, 1.0, 2.6666666666666665, 4.333333333333333
            ],
                index=pd.Index([
                    'Start', 'End', 'Period', 'Count', 'Mean', 'Std', 'Min', 'Median', 'Max'
                ], dtype='object'),
                name='agg_func_mean'
            )
        )

    def test_boolean_attr(self):
        obj = vbt.IndicatorFactory(
            input_names=['ts'], param_names=['p'], output_names=['out'],
            attr_settings=dict(out=dict(dtype=np.bool_))) \
            .from_apply_func(lambda ts, p: ts > p).run(ts, 2)

        pd.testing.assert_frame_equal(obj.out_and(True), obj.out)
        target = pd.DataFrame(
            np.array([
                [False, False, False, False, True, False],
                [False, False, False, False, True, False],
                [False, False, False, True, True, True],
                [False, False, False, True, False, False],
                [False, False, False, True, False, False]
            ]),
            index=ts.index,
            columns=pd.MultiIndex.from_tuples([
                (False, 2, 'a'),
                (False, 2, 'b'),
                (False, 2, 'c'),
                (True, 2, 'a'),
                (True, 2, 'b'),
                (True, 2, 'c'),
            ], names=['custom_out_and', 'custom_p', None])
        )
        pd.testing.assert_frame_equal(
            obj.out_and([False, True]),
            target
        )
        columns = target.columns.set_names('my_and', level=0)
        pd.testing.assert_frame_equal(
            obj.out_and([False, True], level_name='my_and'),
            pd.DataFrame(
                target.values,
                index=target.index,
                columns=columns
            )
        )
        pd.testing.assert_series_equal(
            obj.out_stats(),
            pd.Series([
                pd.Timestamp('2018-01-01 00:00:00'), pd.Timestamp('2018-01-05 00:00:00'),
                pd.Timedelta('5 days 00:00:00'), 2.3333333333333335, 46.666666666666664,
                pd.Timestamp('2018-01-02 08:00:00'), pd.Timestamp('2018-01-03 16:00:00'), 0.0,
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('1 days 00:00:00'),
                pd.Timedelta('1 days 00:00:00'), pd.Timedelta('0 days 00:00:00'),
                1.0, 55.55555555555555, pd.Timedelta('2 days 08:00:00'),
                pd.Timedelta('2 days 08:00:00'), pd.Timedelta('2 days 08:00:00'),
                pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT
            ],
                index=pd.Index([
                    'Start', 'End', 'Period', 'Total', 'Rate [%]', 'First Index',
                    'Last Index', 'Norm Avg Index [-1, 1]', 'Distance: Min',
                    'Distance: Max', 'Distance: Mean', 'Distance: Std', 'Total Partitions',
                    'Partition Rate [%]', 'Partition Length: Min', 'Partition Length: Max',
                    'Partition Length: Mean', 'Partition Length: Std',
                    'Partition Distance: Min', 'Partition Distance: Max',
                    'Partition Distance: Mean', 'Partition Distance: Std'
                ], dtype='object'),
                name='agg_func_mean'
            )
        )

    def test_mapping_attr(self):
        TestEnum = namedtuple('TestEnum', ['Hello', 'World'])(0, 1)
        obj = vbt.IndicatorFactory(
            output_names=['out'],
            attr_settings=dict(out=dict(dtype=TestEnum))) \
            .from_apply_func(lambda: np.array([[0, 1], [1, -1]])).run()

        pd.testing.assert_frame_equal(
            obj.out_readable,
            pd.DataFrame([
                ['Hello', 'World'],
                ['World', None]
            ])
        )
        pd.testing.assert_series_equal(
            obj.out_stats(),
            pd.Series([
                0.0, 1.0, 2.0, 0.5, 0.5, 1.0
            ],
                index=pd.Index([
                    'Start', 'End', 'Period', 'Value Counts: None', 'Value Counts: Hello', 'Value Counts: World'
                ], dtype='object'),
                name='agg_func_mean'
            )
        )

    def test_stats(self):
        @njit
        def apply_func_nb(ts):
            return ts ** 2, ts ** 3

        MyInd = vbt.IndicatorFactory(
            input_names=['ts'],
            output_names=['out1', 'out2'],
            metrics=dict(
                sum_diff=dict(
                    calc_func=lambda self, const: self.out2.sum() * self.out1.sum() + const
                )
            ),
            stats_defaults=dict(settings=dict(const=1000))
        ).from_apply_func(
            apply_func_nb
        )

        myind = MyInd.run(ts)
        pd.testing.assert_series_equal(
            myind.stats(),
            pd.Series([9535.0], index=['sum_diff'], name='agg_func_mean')
        )

    def test_dir(self):
        TestEnum = namedtuple('TestEnum', ['Hello', 'World'])(0, 1)
        F = vbt.IndicatorFactory(
            input_names=['ts'], output_names=['o1', 'o2'], in_output_names=['in_out'], param_names=['p1', 'p2'],
            attr_settings={
                'ts': {'dtype': None},
                'o1': {'dtype': np.float64},
                'o2': {'dtype': np.bool_},
                'in_out': {'dtype': TestEnum}
            }
        )
        ind = F.from_apply_func(lambda ts, in_out, p1, p2: (ts + in_out, ts + in_out)).run(ts, 100, 200)
        test_attr_list = dir(ind)
        assert test_attr_list == [
            '__annotations__',
            '__class__',
            '__delattr__',
            '__dict__',
            '__dir__',
            '__doc__',
            '__eq__',
            '__format__',
            '__ge__',
            '__getattribute__',
            '__getitem__',
            '__gt__',
            '__hash__',
            '__init__',
            '__init_subclass__',
            '__le__',
            '__lt__',
            '__module__',
            '__ne__',
            '__new__',
            '__reduce__',
            '__reduce_ex__',
            '__repr__',
            '__setattr__',
            '__sizeof__',
            '__str__',
            '__subclasshook__',
            '__weakref__',
            '_config',
            '_iloc',
            '_in_out',
            '_in_output_names',
            '_indexing_kwargs',
            '_input_mapper',
            '_input_names',
            '_level_names',
            '_loc',
            '_metrics',
            '_o1',
            '_o2',
            '_output_flags',
            '_output_names',
            '_p1_list',
            '_p1_loc',
            '_p1_mapper',
            '_p2_list',
            '_p2_loc',
            '_p2_mapper',
            '_param_names',
            '_run',
            '_run_combs',
            '_short_name',
            '_subplots',
            '_ts',
            '_tuple_loc',
            '_tuple_mapper',
            '_wrapper',
            'apply_func',
            'build_metrics_doc',
            'build_subplots_doc',
            'config',
            'copy',
            'custom_func',
            'deep_getattr',
            'dumps',
            'iloc',
            'in_out',
            'in_out_readable',
            'in_out_stats',
            'in_output_names',
            'indexing_func',
            'indexing_kwargs',
            'input_names',
            'level_names',
            'load',
            'loads',
            'loc',
            'metrics',
            'o1',
            'o1_above',
            'o1_below',
            'o1_crossed_above',
            'o1_crossed_below',
            'o1_equal',
            'o1_stats',
            'o2',
            'o2_and',
            'o2_or',
            'o2_stats',
            'o2_xor',
            'output_flags',
            'output_names',
            'override_metrics_doc',
            'override_subplots_doc',
            'p1_list',
            'p1_loc',
            'p2_list',
            'p2_loc',
            'param_names',
            'plots',
            'plots_defaults',
            'post_resolve_attr',
            'pre_resolve_attr',
            'regroup',
            'replace',
            'resolve_attr',
            'resolve_self',
            'run',
            'run_combs',
            'save',
            'select_one',
            'select_one_from_obj',
            'self_aliases',
            'short_name',
            'stats',
            'stats_defaults',
            'subplots',
            'to_doc',
            'ts',
            'ts_above',
            'ts_below',
            'ts_crossed_above',
            'ts_crossed_below',
            'ts_equal',
            'ts_stats',
            'tuple_loc',
            'update_config',
            'wrapper',
            'writeable_attrs',
            'xs'
        ]

    def test_get_talib_indicators(self):
        if talib_available:
            assert len(vbt.IndicatorFactory.get_talib_indicators()) > 0

    def test_from_talib(self):
        if talib_available:
            # with params
            target = pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan],
                    [2.5, 5.5, 2.5],
                    [3.5, 4.5, 3.5],
                    [4.5, 3.5, 3.5],
                    [5.5, 2.5, 2.5]
                ]),
                index=ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 2, 2, 'a'),
                    (2, 2, 2, 'b'),
                    (2, 2, 2, 'c')
                ], names=['bbands_timeperiod', 'bbands_nbdevup', 'bbands_nbdevdn', None])
            )
            BBANDS = vbt.talib('BBANDS')
            pd.testing.assert_frame_equal(
                BBANDS.run(ts, timeperiod=2, nbdevup=2, nbdevdn=2).upperband,
                target
            )
            pd.testing.assert_frame_equal(
                BBANDS.run(ts, timeperiod=2, nbdevup=2, nbdevdn=2).middleband,
                target - 1
            )
            pd.testing.assert_frame_equal(
                BBANDS.run(ts, timeperiod=2, nbdevup=2, nbdevdn=2).lowerband,
                target - 2
            )
            target = pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [2.5, 5.5, 2.5, 2.5, 5.5, 2.5],
                    [3.5, 4.5, 3.5, 3.5, 4.5, 3.5],
                    [4.5, 3.5, 3.5, 4.5, 3.5, 3.5],
                    [5.5, 2.5, 2.5, 5.5, 2.5, 2.5]
                ]),
                index=ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 2, 2, 'a'),
                    (2, 2, 2, 'b'),
                    (2, 2, 2, 'c'),
                    (2, 2, 2, 'a'),
                    (2, 2, 2, 'b'),
                    (2, 2, 2, 'c')
                ], names=['bbands_timeperiod', 'bbands_nbdevup', 'bbands_nbdevdn', None])
            )
            BBANDS = vbt.talib('BBANDS')
            pd.testing.assert_frame_equal(
                BBANDS.run(ts, timeperiod=[2, 2], nbdevup=2, nbdevdn=2).upperband,
                target
            )
            pd.testing.assert_frame_equal(
                BBANDS.run(ts, timeperiod=[2, 2], nbdevup=2, nbdevdn=2).middleband,
                target - 1
            )
            pd.testing.assert_frame_equal(
                BBANDS.run(ts, timeperiod=[2, 2], nbdevup=2, nbdevdn=2).lowerband,
                target - 2
            )
            # without params
            OBV = vbt.talib('OBV')
            pd.testing.assert_frame_equal(
                OBV.run(ts, ts * 2).real,
                pd.DataFrame(
                    np.array([
                        [2., 10., 2.],
                        [6., 2., 6.],
                        [12., -4., 12.],
                        [20., -8., 8.],
                        [30., -10., 6.]
                    ]),
                    index=ts.index,
                    columns=ts.columns
                )
            )

    def test_get_pandas_ta_indicators(self):
        if pandas_ta_available:
            assert len(vbt.IndicatorFactory.get_pandas_ta_indicators()) > 0

    def test_from_pandas_ta(self):
        if pandas_ta_available:
            pd.testing.assert_frame_equal(
                vbt.pandas_ta('SMA').run(ts, 2).sma,
                pd.DataFrame(
                    ts.rolling(2).mean().values,
                    index=ts.index,
                    columns=pd.MultiIndex.from_tuples([(2, 'a'), (2, 'b'), (2, 'c')], names=['sma_length', None])
                )
            )
            pd.testing.assert_frame_equal(
                vbt.pandas_ta('SMA').run(ts['a'], [2, 3, 4]).sma,
                pd.DataFrame(
                    np.column_stack((
                        ts['a'].rolling(2).mean().values,
                        ts['a'].rolling(3).mean().values,
                        ts['a'].rolling(4).mean().values
                    )),
                    index=ts.index,
                    columns=pd.Index([2, 3, 4], dtype='int64', name='sma_length')
                )
            )

    def test_get_ta_indicators(self):
        if ta_available:
            assert len(vbt.IndicatorFactory.get_ta_indicators()) > 0

    def test_from_ta(self):
        if ta_available:
            pd.testing.assert_frame_equal(
                vbt.ta('SMAIndicator').run(ts, 2).sma_indicator,
                pd.DataFrame(
                    ts.rolling(2).mean().values,
                    index=ts.index,
                    columns=pd.MultiIndex.from_tuples([(2, 'a'), (2, 'b'), (2, 'c')],
                                                      names=['smaindicator_window', None])
                )
            )
            pd.testing.assert_frame_equal(
                vbt.ta('SMAIndicator').run(ts['a'], [2, 3, 4]).sma_indicator,
                pd.DataFrame(
                    np.column_stack((
                        ts['a'].rolling(2).mean().values,
                        ts['a'].rolling(3).mean().values,
                        ts['a'].rolling(4).mean().values
                    )),
                    index=ts.index,
                    columns=pd.Index([2, 3, 4], dtype='int64', name='smaindicator_window')
                )
            )
            target = pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan],
                    [2.5, 5.5, 2.5],
                    [3.5, 4.5, 3.5],
                    [4.5, 3.5, 3.5],
                    [5.5, 2.5, 2.5]
                ]),
                index=ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, 2, 'a'),
                    (2, 2, 'b'),
                    (2, 2, 'c')
                ], names=['bollingerbands_window', 'bollingerbands_window_dev', None])
            )
            BollingerBands = vbt.ta('BollingerBands')
            pd.testing.assert_frame_equal(
                BollingerBands.run(ts, window=2, window_dev=2).bollinger_hband,
                target
            )
            pd.testing.assert_frame_equal(
                BollingerBands.run(ts, window=2, window_dev=2).bollinger_mavg,
                target - 1
            )
            pd.testing.assert_frame_equal(
                BollingerBands.run(ts, window=2, window_dev=2).bollinger_lband,
                target - 2
            )


# ############# basic.py ############# #

close_ts = pd.Series([1, 2, 3, 4, 3, 2, 1], index=pd.DatetimeIndex([
    datetime(2018, 1, 1),
    datetime(2018, 1, 2),
    datetime(2018, 1, 3),
    datetime(2018, 1, 4),
    datetime(2018, 1, 5),
    datetime(2018, 1, 6),
    datetime(2018, 1, 7)
]))
high_ts = close_ts * 1.1
low_ts = close_ts * 0.9
volume_ts = pd.Series([4, 3, 2, 1, 2, 3, 4], index=close_ts.index)


class TestBasic:
    def test_MA(self):
        pd.testing.assert_frame_equal(
            vbt.MA.run(close_ts, window=(2, 3), ewm=(False, True), param_product=True).ma,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan],
                    [1.5, 1.66666667, np.nan, np.nan],
                    [2.5, 2.55555556, 2., 2.25],
                    [3.5, 3.51851852, 3., 3.125],
                    [3.5, 3.17283951, 3.33333333, 3.0625],
                    [2.5, 2.3909465, 3., 2.53125],
                    [1.5, 1.46364883, 2., 1.765625]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, False),
                    (2, True),
                    (3, False),
                    (3, True)
                ], names=['ma_window', 'ma_ewm'])
            )
        )

    def test_MSTD(self):
        pd.testing.assert_frame_equal(
            vbt.MSTD.run(close_ts, window=(2, 3), ewm=(False, True), param_product=True).mstd,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan],
                    [0.5, 0.70710678, np.nan, np.nan],
                    [0.5, 0.97467943, 0.81649658, 1.04880885],
                    [0.5, 1.11434207, 0.81649658, 1.30018314],
                    [0.5, 0.73001838, 0.47140452, 0.91715673],
                    [0.5, 0.88824841, 0.81649658, 0.9182094],
                    [0.5, 1.05965735, 0.81649658, 1.14049665]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, False),
                    (2, True),
                    (3, False),
                    (3, True)
                ], names=['mstd_window', 'mstd_ewm'])
            )
        )

    def test_BBANDS(self):
        columns = pd.MultiIndex.from_tuples([
            (2, False, 2.0),
            (2, False, 3.0),
            (2, True, 2.0),
            (2, True, 3.0),
            (3, False, 2.0),
            (3, False, 3.0),
            (3, True, 2.0),
            (3, True, 3.0)
        ], names=['bb_window', 'bb_ewm', 'bb_alpha'])
        pd.testing.assert_frame_equal(
            vbt.BBANDS.run(
                close_ts,
                window=(2, 3),
                alpha=(2., 3.),
                ewm=(False, True),
                param_product=True
            ).middle,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [1.5, 1.5, 1.66666667, 1.66666667, np.nan,
                     np.nan, np.nan, np.nan],
                    [2.5, 2.5, 2.55555556, 2.55555556, 2.,
                     2., 2.25, 2.25],
                    [3.5, 3.5, 3.51851852, 3.51851852, 3.,
                     3., 3.125, 3.125],
                    [3.5, 3.5, 3.17283951, 3.17283951, 3.33333333,
                     3.33333333, 3.0625, 3.0625],
                    [2.5, 2.5, 2.3909465, 2.3909465, 3.,
                     3., 2.53125, 2.53125],
                    [1.5, 1.5, 1.46364883, 1.46364883, 2.,
                     2., 1.765625, 1.765625]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.BBANDS.run(
                close_ts,
                window=(2, 3),
                alpha=(2., 3.),
                ewm=(False, True),
                param_product=True
            ).upper,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [2.5, 3., 3.08088023, 3.78798701, np.nan,
                     np.nan, np.nan, np.nan],
                    [3.5, 4., 4.50491442, 5.47959386, 3.63299316,
                     4.44948974, 4.3476177, 5.39642654],
                    [4.5, 5., 5.74720265, 6.86154472, 4.63299316,
                     5.44948974, 5.72536627, 7.02554941],
                    [4.5, 5., 4.63287626, 5.36289463, 4.27614237,
                     4.7475469, 4.89681346, 5.8139702],
                    [3.5, 4., 4.16744332, 5.05569172, 4.63299316,
                     5.44948974, 4.3676688, 5.2858782],
                    [2.5, 3., 3.58296354, 4.64262089, 3.63299316,
                     4.44948974, 4.04661829, 5.18711494]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.BBANDS.run(
                close_ts,
                window=(2, 3),
                alpha=(2., 3.),
                ewm=(False, True),
                param_product=True
            ).lower,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [0.5, 0., 0.2524531, -0.45465368, np.nan,
                     np.nan, np.nan, np.nan],
                    [1.5, 1., 0.60619669, -0.36848275, 0.36700684,
                     -0.44948974, 0.1523823, -0.89642654],
                    [2.5, 2., 1.28983438, 0.17549232, 1.36700684,
                     0.55051026, 0.52463373, -0.77554941],
                    [2.5, 2., 1.71280275, 0.98278438, 2.39052429,
                     1.91911977, 1.22818654, 0.3110298],
                    [1.5, 1., 0.61444969, -0.27379872, 1.36700684,
                     0.55051026, 0.6948312, -0.2233782],
                    [0.5, 0., -0.65566587, -1.71532322, 0.36700684,
                     -0.44948974, -0.51536829, -1.65586494]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.BBANDS.run(
                close_ts,
                window=(2, 3),
                alpha=(2., 3.),
                ewm=(False, True),
                param_product=True
            ).percent_b,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [0.75, 0.66666667, 0.61785113, 0.57856742, np.nan,
                     np.nan, np.nan, np.nan],
                    [0.75, 0.66666667, 0.61399759, 0.5759984, 0.80618622,
                     0.70412415, 0.67877424, 0.61918282],
                    [0.75, 0.66666667, 0.60801923, 0.57201282, 0.80618622,
                     0.70412415, 0.66824553, 0.61216369],
                    [0.25, 0.33333333, 0.44080988, 0.46053992, 0.3232233,
                     0.38214887, 0.48296365, 0.48864244],
                    [0.25, 0.33333333, 0.38996701, 0.42664468, 0.19381378,
                     0.29587585, 0.35535707, 0.40357138],
                    [0.25, 0.33333333, 0.3906135, 0.42707567, 0.19381378,
                     0.29587585, 0.3321729, 0.38811526]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.BBANDS.run(
                close_ts,
                window=(2, 3),
                alpha=(2., 3.),
                ewm=(False, True),
                param_product=True
            ).bandwidth,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [1.33333333, 2., 1.69705627, 2.54558441, np.nan,
                     np.nan, np.nan, np.nan],
                    [0.8, 1.2, 1.5255852, 2.2883778, 1.63299316,
                     2.44948974, 1.86454906, 2.7968236],
                    [0.57142857, 0.85714286, 1.26683098, 1.90024647, 1.08866211,
                     1.63299316, 1.66423442, 2.49635162],
                    [0.57142857, 0.85714286, 0.92033445, 1.38050168, 0.56568542,
                     0.84852814, 1.197919, 1.79687849],
                    [0.8, 1.2, 1.48601971, 2.22902956, 1.08866211,
                     1.63299316, 1.45099757, 2.17649636],
                    [1.33333333, 2., 2.8959333, 4.34389996, 1.63299316,
                     2.44948974, 2.58378001, 3.87567002]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )

    def test_RSI(self):
        pd.testing.assert_frame_equal(
            vbt.RSI.run(close_ts, window=(2, 3), ewm=(False, True), param_product=True).rsi,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan],
                    [100., 100., np.nan, np.nan],
                    [100., 100., 100., 100.],
                    [50., 33.33333333, 66.66666667, 50.],
                    [0., 11.11111111, 33.33333333, 25.],
                    [0., 3.7037037, 0., 12.5]
                ]),
                index=close_ts.index,
                columns=pd.MultiIndex.from_tuples([
                    (2, False),
                    (2, True),
                    (3, False),
                    (3, True)
                ], names=['rsi_window', 'rsi_ewm'])
            )
        )

    def test_STOCH(self):
        columns = pd.MultiIndex.from_tuples([
            (2, 2, False),
            (2, 2, True),
            (2, 3, False),
            (2, 3, True),
            (3, 2, False),
            (3, 2, True),
            (3, 3, False),
            (3, 3, True)
        ], names=['stoch_k_window', 'stoch_d_window', 'stoch_d_ewm'])
        pd.testing.assert_frame_equal(
            vbt.STOCH.run(
                high_ts,
                low_ts,
                close_ts,
                k_window=(2, 3),
                d_window=(2, 3),
                d_ewm=(False, True),
                param_product=True
            ).percent_k,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [84.61538462, 84.61538462, 84.61538462, 84.61538462, np.nan,
                     np.nan, np.nan, np.nan],
                    [80., 80., 80., 80., 87.5,
                     87.5, 87.5, 87.5],
                    [76.47058824, 76.47058824, 76.47058824, 76.47058824, 84.61538462,
                     84.61538462, 84.61538462, 84.61538462],
                    [17.64705882, 17.64705882, 17.64705882, 17.64705882, 17.64705882,
                     17.64705882, 17.64705882, 17.64705882],
                    [13.33333333, 13.33333333, 13.33333333, 13.33333333, 7.69230769,
                     7.69230769, 7.69230769, 7.69230769],
                    [7.69230769, 7.69230769, 7.69230769, 7.69230769, 4.16666667,
                     4.16666667, 4.16666667, 4.16666667]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.STOCH.run(
                high_ts,
                low_ts,
                close_ts,
                k_window=(2, 3),
                d_window=(2, 3),
                d_ewm=(False, True),
                param_product=True
            ).percent_d,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [82.30769231, 81.53846154, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan],
                    [78.23529412, 78.15987934, 80.36199095, 79.38914027, 86.05769231,
                     85.57692308, np.nan, np.nan],
                    [47.05882353, 37.81799899, 58.03921569, 48.51809955, 51.13122172,
                     40.29034691, 63.25414781, 51.85237557],
                    [15.49019608, 21.49488855, 35.81699346, 30.92571644, 12.66968326,
                     18.55832076, 36.65158371, 29.77234163],
                    [10.51282051, 12.29316798, 12.89089995, 19.30901207, 5.92948718,
                     8.9638847, 9.83534439, 16.96950415]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )

    def test_MACD(self):
        columns = pd.MultiIndex.from_tuples([
            (2, 3, 2, False, False),
            (2, 3, 2, False, True),
            (2, 3, 2, True, False),
            (2, 3, 2, True, True),
            (2, 3, 3, False, False),
            (2, 3, 3, False, True),
            (2, 3, 3, True, False),
            (2, 3, 3, True, True),
            (2, 4, 2, False, False),
            (2, 4, 2, False, True),
            (2, 4, 2, True, False),
            (2, 4, 2, True, True),
            (2, 4, 3, False, False),
            (2, 4, 3, False, True),
            (2, 4, 3, True, False),
            (2, 4, 3, True, True),
            (3, 3, 2, False, False),
            (3, 3, 2, False, True),
            (3, 3, 2, True, False),
            (3, 3, 2, True, True),
            (3, 3, 3, False, False),
            (3, 3, 3, False, True),
            (3, 3, 3, True, False),
            (3, 3, 3, True, True),
            (3, 4, 2, False, False),
            (3, 4, 2, False, True),
            (3, 4, 2, True, False),
            (3, 4, 2, True, True),
            (3, 4, 3, False, False),
            (3, 4, 3, False, True),
            (3, 4, 3, True, False),
            (3, 4, 3, True, True)
        ], names=['macd_fast_window', 'macd_slow_window', 'macd_signal_window', 'macd_macd_ewm', 'macd_signal_ewm'])

        pd.testing.assert_frame_equal(
            vbt.MACD.run(
                close_ts,
                fast_window=(2, 3),
                slow_window=(3, 4),
                signal_window=(2, 3),
                macd_ewm=(False, True),
                signal_ewm=(False, True),
                param_product=True
            ).macd,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [0.5, 0.5, 0.30555556, 0.30555556, 0.5,
                     0.5, 0.30555556, 0.30555556, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, 0., 0., 0., 0.,
                     0., 0., 0., 0., np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [0.5, 0.5, 0.39351852, 0.39351852, 0.5,
                     0.5, 0.39351852, 0.39351852, 1., 1.,
                     0.69451852, 0.69451852, 1., 1., 0.69451852,
                     0.69451852, 0., 0., 0., 0.,
                     0., 0., 0., 0., 0.5,
                     0.5, 0.301, 0.301, 0.5, 0.5,
                     0.301, 0.301],
                    [0.16666667, 0.16666667, 0.11033951, 0.11033951, 0.16666667,
                     0.16666667, 0.11033951, 0.11033951, 0.5, 0.5,
                     0.27843951, 0.27843951, 0.5, 0.5, 0.27843951,
                     0.27843951, 0., 0., 0., 0.,
                     0., 0., 0., 0., 0.33333333,
                     0.33333333, 0.1681, 0.1681, 0.33333333, 0.33333333,
                     0.1681, 0.1681],
                    [-0.5, -0.5, -0.1403035, -0.1403035, -0.5,
                     -0.5, -0.1403035, -0.1403035, -0.5, -0.5,
                     -0.1456935, -0.1456935, -0.5, -0.5, -0.1456935,
                     -0.1456935, 0., 0., 0., 0.,
                     0., 0., 0., 0., 0.,
                     0., -0.00539, -0.00539, 0., 0.,
                     -0.00539, -0.00539],
                    [-0.5, -0.5, -0.30197617, -0.30197617, -0.5,
                     -0.5, -0.30197617, -0.30197617, -1., -1.,
                     -0.45833517, -0.45833517, -1., -1., -0.45833517,
                     -0.45833517, 0., 0., 0., 0.,
                     0., 0., 0., 0., -0.5,
                     -0.5, -0.156359, -0.156359, -0.5, -0.5,
                     -0.156359, -0.156359]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.MACD.run(
                close_ts,
                fast_window=(2, 3),
                slow_window=(3, 4),
                signal_window=(2, 3),
                macd_ewm=(False, True),
                signal_ewm=(False, True),
                param_product=True
            ).signal,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [0.5, 0.5, 0.34953704, 0.36419753, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, 0., 0., 0., 0.,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [0.33333333, 0.27777778, 0.25192901, 0.19495885, 0.38888889,
                     0.33333333, 0.26980453, 0.22993827, 0.75, 0.66666667,
                     0.48647901, 0.41713251, np.nan, np.nan, np.nan,
                     np.nan, 0., 0., 0., 0.,
                     0., 0., 0., 0., 0.41666667,
                     0.38888889, 0.23455, 0.2124, np.nan, np.nan,
                     np.nan, np.nan],
                    [-0.16666667, -0.24074074, -0.014982, -0.02854938, 0.05555556,
                     -0.08333333, 0.12118484, 0.04481739, 0., -0.11111111,
                     0.066373, 0.04191517, 0.33333333, 0.125, 0.27575484,
                     0.17039276, 0., 0., 0., 0.,
                     0., 0., 0., 0., 0.16666667,
                     0.12962963, 0.081355, 0.06720667, 0.27777778, 0.20833333,
                     0.15457, 0.11458],
                    [-0.5, -0.41358025, -0.22113983, -0.2108339, -0.27777778,
                     -0.29166667, -0.11064672, -0.12857939, -0.75, -0.7037037,
                     -0.30201433, -0.29158505, -0.33333333, -0.4375, -0.10852972,
                     -0.1439712, 0., 0., 0., 0.,
                     0., 0., 0., 0., -0.25,
                     -0.29012346, -0.0808745, -0.08183711, -0.05555556, -0.14583333,
                     0.002117, -0.0208895]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.MACD.run(
                close_ts,
                fast_window=(2, 3),
                slow_window=(3, 4),
                signal_window=(2, 3),
                macd_ewm=(False, True),
                signal_ewm=(False, True),
                param_product=True
            ).hist,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [0., 0., 0.04398148, 0.02932099, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, 0., 0., 0., 0.,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan],
                    [-0.16666667, -0.11111111, -0.14158951, -0.08461934, -0.22222222,
                     -0.16666667, -0.15946502, -0.11959877, -0.25, -0.16666667,
                     -0.20803951, -0.138693, np.nan, np.nan, np.nan,
                     np.nan, 0., 0., 0., 0.,
                     0., 0., 0., 0., -0.08333333,
                     -0.05555556, -0.06645, -0.0443, np.nan, np.nan,
                     np.nan, np.nan],
                    [-0.33333333, -0.25925926, -0.1253215, -0.11175412, -0.55555556,
                     -0.41666667, -0.26148834, -0.18512088, -0.5, -0.38888889,
                     -0.2120665, -0.18760867, -0.83333333, -0.625, -0.42144834,
                     -0.31608626, 0., 0., 0., 0.,
                     0., 0., 0., 0., -0.16666667,
                     -0.12962963, -0.086745, -0.07259667, -0.27777778, -0.20833333,
                     -0.15996, -0.11997],
                    [0., -0.08641975, -0.08083633, -0.09114226, -0.22222222,
                     -0.20833333, -0.19132945, -0.17339678, -0.25, -0.2962963,
                     -0.15632083, -0.16675011, -0.66666667, -0.5625, -0.34980545,
                     -0.31436396, 0., 0., 0., 0.,
                     0., 0., 0., 0., -0.25,
                     -0.20987654, -0.0754845, -0.07452189, -0.44444444, -0.35416667,
                     -0.158476, -0.1354695]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )

    def test_ATR(self):
        columns = pd.MultiIndex.from_tuples([
            (2, False),
            (2, True),
            (3, False),
            (3, True)
        ], names=['atr_window', 'atr_ewm'])
        pd.testing.assert_frame_equal(
            vbt.ATR.run(high_ts, low_ts, close_ts, window=(2, 3), ewm=(False, True), param_product=True).tr,
            pd.DataFrame(
                np.array([
                    [0.2, 0.2, 0.2, 0.2],
                    [1.2, 1.2, 1.2, 1.2],
                    [1.3, 1.3, 1.3, 1.3],
                    [1.4, 1.4, 1.4, 1.4],
                    [1.3, 1.3, 1.3, 1.3],
                    [1.2, 1.2, 1.2, 1.2],
                    [1.1, 1.1, 1.1, 1.1]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )
        pd.testing.assert_frame_equal(
            vbt.ATR.run(high_ts, low_ts, close_ts, window=(2, 3), ewm=(False, True), param_product=True).atr,
            pd.DataFrame(
                np.array([
                    [np.nan, np.nan, np.nan, np.nan],
                    [0.7, 0.86666667, np.nan, np.nan],
                    [1.25, 1.15555556, 0.9, 1.],
                    [1.35, 1.31851852, 1.3, 1.2],
                    [1.35, 1.30617284, 1.33333333, 1.25],
                    [1.25, 1.23539095, 1.3, 1.225],
                    [1.15, 1.14513032, 1.2, 1.1625]
                ]),
                index=close_ts.index,
                columns=columns
            )
        )

    def test_OBV(self):
        pd.testing.assert_series_equal(
            vbt.OBV.run(close_ts, volume_ts).obv,
            pd.Series(
                np.array([4, 7, 9, 10, 8, 5, 1]),
                index=close_ts.index,
                name=close_ts.name
            )
        )
