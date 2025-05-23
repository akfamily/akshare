from copy import deepcopy
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest
from numba import njit, typeof
from numba.typed import List

import vectorbt as vbt
from tests.utils import record_arrays_close
from vectorbt.generic.enums import drawdown_dt
from vectorbt.portfolio import nb
from vectorbt.portfolio.enums import *
from vectorbt.utils.random_ import set_seed

seed = 42

day_dt = np.timedelta64(86400000000000)

price = pd.Series([1., 2., 3., 4., 5.], index=pd.Index([
    datetime(2020, 1, 1),
    datetime(2020, 1, 2),
    datetime(2020, 1, 3),
    datetime(2020, 1, 4),
    datetime(2020, 1, 5)
]))
price_wide = price.vbt.tile(3, keys=['a', 'b', 'c'])
big_price = pd.DataFrame(np.random.uniform(size=(1000,)))
big_price.index = [datetime(2018, 1, 1) + timedelta(days=i) for i in range(1000)]
big_price_wide = big_price.vbt.tile(1000)


# ############# Global ############# #

def setup_module():
    vbt.settings.numba['check_func_suffix'] = True
    vbt.settings.portfolio['attach_call_seq'] = True
    vbt.settings.caching.enabled = False
    vbt.settings.caching.whitelist = []
    vbt.settings.caching.blacklist = []


def teardown_module():
    vbt.settings.reset()


# ############# nb ############# #

def assert_same_tuple(tup1, tup2):
    for i in range(len(tup1)):
        assert tup1[i] == tup2[i] or np.isnan(tup1[i]) and np.isnan(tup2[i])


def test_execute_order_nb():
    # Errors, ignored and rejected orders
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(-100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(np.nan, 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., np.inf, 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., np.nan, 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., np.nan, 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., -10., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., np.nan, 10., 1100., 0, 0),
            nb.order_nb(10, 10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, size_type=-2))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, size_type=20))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, direction=-2))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, direction=20))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., -100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, direction=Direction.LongOnly))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, direction=Direction.ShortOnly))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, np.inf))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, -10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, fees=np.inf))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, fees=np.nan))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, fixed_fees=np.inf))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, fixed_fees=np.nan))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, slippage=np.inf))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, slippage=-1))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, min_size=np.inf))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, min_size=-1))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, max_size=0))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, max_size=-10))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, reject_prob=np.nan))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, reject_prob=-1))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
            nb.order_nb(10, 10, reject_prob=2))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., 10., 1100.),
            nb.order_nb(10, 10, size_granularity=-10))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., np.nan, 0, 0),
        nb.order_nb(1, 10, size_type=SizeType.TargetPercent))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=1, status_info=3))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., -10., 0, 0),
        nb.order_nb(1, 10, size_type=SizeType.TargetPercent))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=4))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., np.inf, 1100., 0, 0),
            nb.order_nb(10, 10, size_type=SizeType.Value))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., -10., 1100, 0, 0),
            nb.order_nb(10, 10, size_type=SizeType.Value))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., np.nan, 1100., 0, 0),
        nb.order_nb(10, 10, size_type=SizeType.Value))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., np.inf, 1100., 0, 0),
            nb.order_nb(10, 10, size_type=SizeType.TargetValue))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(100., 100., 0., 100., -10., 1100, 0, 0),
            nb.order_nb(10, 10, size_type=SizeType.TargetValue))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., np.nan, 1100., 0, 0),
        nb.order_nb(10, 10, size_type=SizeType.TargetValue))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=1, status_info=2))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., -10., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(np.inf, 10, direction=Direction.ShortOnly))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-20.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., -10., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(-np.inf, 10, direction=Direction.Both))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-20.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 10., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(0, 10))
    assert exec_state == ExecuteOrderState(cash=100.0, position=10.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=1, status_info=5))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(15, 10, max_size=10, allow_partial=False))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=9))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(10, 10, reject_prob=1.))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=10))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(0., 100., 0., 0., 10., 1100., 0, 0),
        nb.order_nb(10, 10, direction=Direction.LongOnly))
    assert exec_state == ExecuteOrderState(cash=0.0, position=100.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=7))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(0., 100., 0., 0., 10., 1100., 0, 0),
        nb.order_nb(10, 10, direction=Direction.Both))
    assert exec_state == ExecuteOrderState(cash=0.0, position=100.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=7))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(np.inf, 100, 0., np.inf, np.nan, 1100., 0, 0),
            nb.order_nb(np.inf, 10, direction=Direction.LongOnly))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(np.inf, 100., 0., np.inf, 10., 1100., 0, 0),
            nb.order_nb(np.inf, 10, direction=Direction.Both))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(-10, 10, direction=Direction.ShortOnly))
    assert exec_state == ExecuteOrderState(cash=100.0, position=0.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=8))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(np.inf, 100., 0., np.inf, 10., 1100., 0, 0),
            nb.order_nb(-np.inf, 10, direction=Direction.ShortOnly))
    with pytest.raises(Exception):
        _ = nb.execute_order_nb(
            ProcessOrderState(np.inf, 100., 0., np.inf, 10., 1100., 0, 0),
            nb.order_nb(-np.inf, 10, direction=Direction.Both))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(-10, 10, direction=Direction.LongOnly))
    assert exec_state == ExecuteOrderState(cash=100.0, position=0.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=8))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(10, 10, fixed_fees=100))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=11))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(10, 10, min_size=100))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=12))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(100, 10, allow_partial=False))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=13))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(-10, 10, min_size=100))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=12))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(-200, 10, direction=Direction.LongOnly, allow_partial=False))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=13))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 100., 0., 100., 10., 1100., 0, 0),
        nb.order_nb(-10, 10, fixed_fees=1000))
    assert exec_state == ExecuteOrderState(cash=100.0, position=100.0, debt=0.0, free_cash=100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=11))

    # Calculations
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(10, 10, fees=0.1, fixed_fees=1, slippage=0.1))
    assert exec_state == ExecuteOrderState(cash=0.0, position=8.18181818181818, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=8.18181818181818, price=11.0, fees=10.000000000000014, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(100, 10, fees=0.1, fixed_fees=1, slippage=0.1))
    assert exec_state == ExecuteOrderState(cash=0.0, position=8.18181818181818, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=8.18181818181818, price=11.0, fees=10.000000000000014, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-10, 10, fees=0.1, fixed_fees=1, slippage=0.1))
    assert exec_state == ExecuteOrderState(cash=180.0, position=-10.0, debt=90.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10.0, price=9.0, fees=10.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-100, 10, fees=0.1, fixed_fees=1, slippage=0.1))
    assert exec_state == ExecuteOrderState(cash=909.0, position=-100.0, debt=900.0, free_cash=-891.0)
    assert_same_tuple(order_result, OrderResult(
        size=100.0, price=9.0, fees=91.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(10, 10, fees=-0.1, fixed_fees=-1, slippage=0.1))
    assert exec_state == ExecuteOrderState(cash=2.0, position=10.0, debt=0.0, free_cash=2.0)
    assert_same_tuple(order_result, OrderResult(
        size=10.0, price=11.0, fees=-12.0, side=0, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(10, 10, size_type=SizeType.TargetAmount))
    assert exec_state == ExecuteOrderState(cash=0.0, position=10.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-10, 10, size_type=SizeType.TargetAmount))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-10.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=1, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(100, 10, size_type=SizeType.Value))
    assert exec_state == ExecuteOrderState(cash=0.0, position=10.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-100, 10, size_type=SizeType.Value))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-10.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=1, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(100, 10, size_type=SizeType.TargetValue))
    assert exec_state == ExecuteOrderState(cash=0.0, position=10.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-100, 10, size_type=SizeType.TargetValue))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-10.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=1, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(1, 10, size_type=SizeType.TargetPercent))
    assert exec_state == ExecuteOrderState(cash=0.0, position=10.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-1, 10, size_type=SizeType.TargetPercent))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-10.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=1, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(1, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=0.0, position=10.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=5.0, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(0.5, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=25.0, position=7.5, debt=0.0, free_cash=25.0)
    assert_same_tuple(order_result, OrderResult(
        size=2.5, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(-0.5, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=125.0, position=-2.5, debt=25.0, free_cash=75.0)
    assert_same_tuple(order_result, OrderResult(
        size=7.5, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(-1, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-10.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=15.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 0., 0., 50., 10., 100., 0, 0),
        nb.order_nb(1, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=0.0, position=5.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=5.0, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 0., 0., 50., 10., 100., 0, 0),
        nb.order_nb(0.5, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=25.0, position=2.5, debt=0.0, free_cash=25.0)
    assert_same_tuple(order_result, OrderResult(
        size=2.5, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 0., 0., 50., 10., 100., 0, 0),
        nb.order_nb(-0.5, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=75.0, position=-2.5, debt=25.0, free_cash=25.0)
    assert_same_tuple(order_result, OrderResult(
        size=2.5, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., 0., 0., 50., 10., 100., 0, 0),
        nb.order_nb(-1, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=100.0, position=-5.0, debt=50.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=5.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., -5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(1, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=0.0, position=0.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=5.0, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., -5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(0.5, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=25.0, position=-2.5, debt=0.0, free_cash=25.0)
    assert_same_tuple(order_result, OrderResult(
        size=2.5, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., -5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(-0.5, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=75.0, position=-7.5, debt=25.0, free_cash=25.0)
    assert_same_tuple(order_result, OrderResult(
        size=2.5, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(50., -5., 0., 50., 10., 100., 0, 0),
        nb.order_nb(-1, 10, size_type=SizeType.Percent))
    assert exec_state == ExecuteOrderState(cash=100.0, position=-10.0, debt=50.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=5.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(np.inf, 10))
    assert exec_state == ExecuteOrderState(cash=0.0, position=10.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., -5., 0., 100., 10., 100., 0, 0),
        nb.order_nb(np.inf, 10))
    assert exec_state == ExecuteOrderState(cash=0.0, position=5.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-np.inf, 10))
    assert exec_state == ExecuteOrderState(cash=200.0, position=-10.0, debt=100.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10., price=10.0, fees=0., side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(150., -5., 0., 150., 10., 100., 0, 0),
        nb.order_nb(-np.inf, 10))
    assert exec_state == ExecuteOrderState(cash=300.0, position=-20.0, debt=150.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=15.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., 0., 0., 50., 10., 100., 0, 0),
        nb.order_nb(10, 10, lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=50.0, position=5.0, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=5.0, price=10.0, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(1000., -5., 50., 50., 10., 100., 0, 0),
        nb.order_nb(10, 17.5, lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=850.0, position=3.571428571428571, debt=0.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=8.571428571428571, price=17.5, fees=0.0, side=0, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(100., -5., 50., 50., 10., 100., 0, 0),
        nb.order_nb(10, 100, lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=37.5, position=-4.375, debt=43.75, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=0.625, price=100.0, fees=0.0, side=0, status=0, status_info=-1))

    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(0., 10., 0., -50., 10., 100., 0, 0),
        nb.order_nb(-20, 10, lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=150.0, position=-5.0, debt=50.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=15.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(0., 1., 0., -50., 10., 100., 0, 0),
        nb.order_nb(-10, 10, lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=10.0, position=0.0, debt=0.0, free_cash=-40.0)
    assert_same_tuple(order_result, OrderResult(
        size=1.0, price=10.0, fees=0.0, side=1, status=0, status_info=-1))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(0., 0., 0., -100., 10., 100., 0, 0),
        nb.order_nb(-10, 10, lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=0.0, position=0.0, debt=0.0, free_cash=-100.0)
    assert_same_tuple(order_result, OrderResult(
        size=np.nan, price=np.nan, fees=np.nan, side=-1, status=2, status_info=6))
    exec_state, order_result = nb.execute_order_nb(
        ProcessOrderState(0., 0., 0., 100., 10., 100., 0, 0),
        nb.order_nb(-20, 10, fees=0.1, slippage=0.1, fixed_fees=1., lock_cash=True))
    assert exec_state == ExecuteOrderState(cash=80.0, position=-10.0, debt=90.0, free_cash=0.0)
    assert_same_tuple(order_result, OrderResult(
        size=10.0, price=9.0, fees=10.0, side=1, status=0, status_info=-1))


def test_build_call_seq_nb():
    group_lens = np.array([1, 2, 3, 4])
    np.testing.assert_array_equal(
        nb.build_call_seq_nb((10, 10), group_lens, CallSeqType.Default),
        nb.build_call_seq((10, 10), group_lens, CallSeqType.Default)
    )
    np.testing.assert_array_equal(
        nb.build_call_seq_nb((10, 10), group_lens, CallSeqType.Reversed),
        nb.build_call_seq((10, 10), group_lens, CallSeqType.Reversed)
    )
    set_seed(seed)
    out1 = nb.build_call_seq_nb((10, 10), group_lens, CallSeqType.Random)
    set_seed(seed)
    out2 = nb.build_call_seq((10, 10), group_lens, CallSeqType.Random)
    np.testing.assert_array_equal(out1, out2)


# ############# from_orders ############# #

order_size = pd.Series([np.inf, -np.inf, np.nan, np.inf, -np.inf], index=price.index)
order_size_wide = order_size.vbt.tile(3, keys=['a', 'b', 'c'])
order_size_one = pd.Series([1, -1, np.nan, 1, -1], index=price.index)


def from_orders_both(close=price, size=order_size, **kwargs):
    return vbt.Portfolio.from_orders(close, size, direction='both', **kwargs)


def from_orders_longonly(close=price, size=order_size, **kwargs):
    return vbt.Portfolio.from_orders(close, size, direction='longonly', **kwargs)


def from_orders_shortonly(close=price, size=order_size, **kwargs):
    return vbt.Portfolio.from_orders(close, size, direction='shortonly', **kwargs)


class TestFromOrders:
    def test_one_column(self):
        record_arrays_close(
            from_orders_both().order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1), (2, 0, 3, 100.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly().order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 100.0, 2.0, 0.0, 1), (2, 0, 3, 50.0, 4.0, 0.0, 0),
                (3, 0, 4, 50.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly().order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1), (1, 0, 1, 100.0, 2.0, 0.0, 0)
            ], dtype=order_dt)
        )
        pf = from_orders_both()
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'])
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            pd.Index([0], dtype='int64')
        )
        assert pf.wrapper.ndim == 1
        assert pf.wrapper.freq == day_dt
        assert pf.wrapper.grouper.group_by is None

    def test_multiple_columns(self):
        record_arrays_close(
            from_orders_both(close=price_wide).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1), (2, 0, 3, 100.0, 4.0, 0.0, 0),
                (3, 1, 0, 100.0, 1.0, 0.0, 0), (4, 1, 1, 200.0, 2.0, 0.0, 1), (5, 1, 3, 100.0, 4.0, 0.0, 0),
                (6, 2, 0, 100.0, 1.0, 0.0, 0), (7, 2, 1, 200.0, 2.0, 0.0, 1), (8, 2, 3, 100.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(close=price_wide).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 100.0, 2.0, 0.0, 1), (2, 0, 3, 50.0, 4.0, 0.0, 0),
                (3, 0, 4, 50.0, 5.0, 0.0, 1), (4, 1, 0, 100.0, 1.0, 0.0, 0), (5, 1, 1, 100.0, 2.0, 0.0, 1),
                (6, 1, 3, 50.0, 4.0, 0.0, 0), (7, 1, 4, 50.0, 5.0, 0.0, 1), (8, 2, 0, 100.0, 1.0, 0.0, 0),
                (9, 2, 1, 100.0, 2.0, 0.0, 1), (10, 2, 3, 50.0, 4.0, 0.0, 0), (11, 2, 4, 50.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(close=price_wide).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1), (1, 0, 1, 100.0, 2.0, 0.0, 0), (2, 1, 0, 100.0, 1.0, 0.0, 1),
                (3, 1, 1, 100.0, 2.0, 0.0, 0), (4, 2, 0, 100.0, 1.0, 0.0, 1), (5, 2, 1, 100.0, 2.0, 0.0, 0)
            ], dtype=order_dt)
        )
        pf = from_orders_both(close=price_wide)
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'])
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            pd.Index(['a', 'b', 'c'], dtype='object')
        )
        assert pf.wrapper.ndim == 2
        assert pf.wrapper.freq == day_dt
        assert pf.wrapper.grouper.group_by is None

    def test_size_inf(self):
        record_arrays_close(
            from_orders_both(size=[[np.inf, -np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 1, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=[[np.inf, -np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=[[np.inf, -np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_size_granularity(self):
        record_arrays_close(
            from_orders_both(fees=0.1, fixed_fees=0.1, size_granularity=1).order_records,
            np.array([
                (0, 0, 0, 90., 1., 9.1, 0), (1, 0, 1, 164., 2., 32.9, 1),
                (2, 0, 3, 67., 4., 26.9, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(fees=0.1, fixed_fees=0.1, size_granularity=1).order_records,
            np.array([
                (0, 0, 0, 90.0, 1.0, 9.1, 0), (1, 0, 1, 90.0, 2.0, 18.1, 1),
                (2, 0, 3, 36.0, 4.0, 14.5, 0), (3, 0, 4, 36.0, 5.0, 18.1, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(fees=0.1, fixed_fees=0.1, size_granularity=1).order_records,
            np.array([
                (0, 0, 0, 90., 1., 9.1, 1), (1, 0, 1, 82., 2., 16.5, 0)
            ], dtype=order_dt)
        )

    def test_price(self):
        record_arrays_close(
            from_orders_both(price=price * 1.01).order_records,
            np.array([
                (0, 0, 0, 99.00990099009901, 1.01, 0.0, 0), (1, 0, 1, 198.01980198019803, 2.02, 0.0, 1),
                (2, 0, 3, 99.00990099009901, 4.04, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(price=price * 1.01).order_records,
            np.array([
                (0, 0, 0, 99.00990099009901, 1.01, 0.0, 0), (1, 0, 1, 99.00990099009901, 2.02, 0.0, 1),
                (2, 0, 3, 49.504950495049506, 4.04, 0.0, 0), (3, 0, 4, 49.504950495049506, 5.05, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(price=price * 1.01).order_records,
            np.array([
                (0, 0, 0, 99.00990099009901, 1.01, 0.0, 1), (1, 0, 1, 99.00990099009901, 2.02, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(price=np.inf).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1), (2, 0, 3, 100.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(price=np.inf).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 100.0, 2.0, 0.0, 1),
                (2, 0, 3, 50.0, 4.0, 0.0, 0), (3, 0, 4, 50.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(price=np.inf).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1), (1, 0, 1, 100.0, 2.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(price=-np.inf).order_records,
            np.array([
                (0, 0, 1, 100.0, 1.0, 0.0, 1), (1, 0, 3, 66.66666666666667, 3.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(price=-np.inf).order_records,
            np.array([
                (0, 0, 3, 33.333333333333336, 3.0, 0.0, 0), (1, 0, 4, 33.333333333333336, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(price=-np.inf).order_records,
            np.array([
                (0, 0, 3, 33.333333333333336, 3.0, 0.0, 1), (1, 0, 4, 33.333333333333336, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_val_price(self):
        price_nan = pd.Series([1, 2, np.nan, 4, 5], index=price.index)
        record_arrays_close(
            from_orders_both(close=price_nan, size=order_size_one, val_price=np.inf,
                             size_type='value').order_records,
            from_orders_both(close=price_nan, size=order_size_one, val_price=price,
                             size_type='value').order_records
        )
        record_arrays_close(
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=np.inf,
                                 size_type='value').order_records,
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=price,
                                 size_type='value').order_records
        )
        record_arrays_close(
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=np.inf,
                                  size_type='value').order_records,
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=price,
                                  size_type='value').order_records
        )
        shift_price = price_nan.ffill().shift(1)
        record_arrays_close(
            from_orders_both(close=price_nan, size=order_size_one, val_price=-np.inf,
                             size_type='value').order_records,
            from_orders_both(close=price_nan, size=order_size_one, val_price=shift_price,
                             size_type='value').order_records
        )
        record_arrays_close(
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=-np.inf,
                                 size_type='value').order_records,
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=shift_price,
                                 size_type='value').order_records
        )
        record_arrays_close(
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=-np.inf,
                                  size_type='value').order_records,
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=shift_price,
                                  size_type='value').order_records
        )
        record_arrays_close(
            from_orders_both(close=price_nan, size=order_size_one, val_price=np.inf,
                             size_type='value', ffill_val_price=False).order_records,
            from_orders_both(close=price_nan, size=order_size_one, val_price=price_nan,
                             size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=np.inf,
                                 size_type='value', ffill_val_price=False).order_records,
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=price_nan,
                                 size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=np.inf,
                                  size_type='value', ffill_val_price=False).order_records,
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=price_nan,
                                  size_type='value', ffill_val_price=False).order_records
        )
        shift_price_nan = price_nan.shift(1)
        record_arrays_close(
            from_orders_both(close=price_nan, size=order_size_one, val_price=-np.inf,
                             size_type='value', ffill_val_price=False).order_records,
            from_orders_both(close=price_nan, size=order_size_one, val_price=shift_price_nan,
                             size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=-np.inf,
                                 size_type='value', ffill_val_price=False).order_records,
            from_orders_longonly(close=price_nan, size=order_size_one, val_price=shift_price_nan,
                                 size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=-np.inf,
                                  size_type='value', ffill_val_price=False).order_records,
            from_orders_shortonly(close=price_nan, size=order_size_one, val_price=shift_price_nan,
                                  size_type='value', ffill_val_price=False).order_records
        )

    def test_fees(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 1, 1.0, 2.0, -0.2, 1), (2, 0, 3, 1.0, 4.0, -0.4, 0),
                (3, 0, 4, 1.0, 5.0, -0.5, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1), (8, 2, 0, 1.0, 1.0, 0.1, 0),
                (9, 2, 1, 1.0, 2.0, 0.2, 1), (10, 2, 3, 1.0, 4.0, 0.4, 0), (11, 2, 4, 1.0, 5.0, 0.5, 1),
                (12, 3, 0, 1.0, 1.0, 1.0, 0), (13, 3, 1, 1.0, 2.0, 2.0, 1), (14, 3, 3, 1.0, 4.0, 4.0, 0),
                (15, 3, 4, 1.0, 5.0, 5.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 1, 1.0, 2.0, -0.2, 1), (2, 0, 3, 1.0, 4.0, -0.4, 0),
                (3, 0, 4, 1.0, 5.0, -0.5, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1), (8, 2, 0, 1.0, 1.0, 0.1, 0),
                (9, 2, 1, 1.0, 2.0, 0.2, 1), (10, 2, 3, 1.0, 4.0, 0.4, 0), (11, 2, 4, 1.0, 5.0, 0.5, 1),
                (12, 3, 0, 1.0, 1.0, 1.0, 0), (13, 3, 1, 1.0, 2.0, 2.0, 1), (14, 3, 3, 1.0, 4.0, 4.0, 0),
                (15, 3, 4, 1.0, 5.0, 5.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 1), (1, 0, 1, 1.0, 2.0, -0.2, 0), (2, 0, 3, 1.0, 4.0, -0.4, 1),
                (3, 0, 4, 1.0, 5.0, -0.5, 0), (4, 1, 0, 1.0, 1.0, 0.0, 1), (5, 1, 1, 1.0, 2.0, 0.0, 0),
                (6, 1, 3, 1.0, 4.0, 0.0, 1), (7, 1, 4, 1.0, 5.0, 0.0, 0), (8, 2, 0, 1.0, 1.0, 0.1, 1),
                (9, 2, 1, 1.0, 2.0, 0.2, 0), (10, 2, 3, 1.0, 4.0, 0.4, 1), (11, 2, 4, 1.0, 5.0, 0.5, 0),
                (12, 3, 0, 1.0, 1.0, 1.0, 1), (13, 3, 1, 1.0, 2.0, 2.0, 0), (14, 3, 3, 1.0, 4.0, 4.0, 1),
                (15, 3, 4, 1.0, 5.0, 5.0, 0)
            ], dtype=order_dt)
        )

    def test_fixed_fees(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, fixed_fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 1, 1.0, 2.0, -0.1, 1), (2, 0, 3, 1.0, 4.0, -0.1, 0),
                (3, 0, 4, 1.0, 5.0, -0.1, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1), (8, 2, 0, 1.0, 1.0, 0.1, 0),
                (9, 2, 1, 1.0, 2.0, 0.1, 1), (10, 2, 3, 1.0, 4.0, 0.1, 0), (11, 2, 4, 1.0, 5.0, 0.1, 1),
                (12, 3, 0, 1.0, 1.0, 1.0, 0), (13, 3, 1, 1.0, 2.0, 1.0, 1), (14, 3, 3, 1.0, 4.0, 1.0, 0),
                (15, 3, 4, 1.0, 5.0, 1.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, fixed_fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 1, 1.0, 2.0, -0.1, 1), (2, 0, 3, 1.0, 4.0, -0.1, 0),
                (3, 0, 4, 1.0, 5.0, -0.1, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1), (8, 2, 0, 1.0, 1.0, 0.1, 0),
                (9, 2, 1, 1.0, 2.0, 0.1, 1), (10, 2, 3, 1.0, 4.0, 0.1, 0), (11, 2, 4, 1.0, 5.0, 0.1, 1),
                (12, 3, 0, 1.0, 1.0, 1.0, 0), (13, 3, 1, 1.0, 2.0, 1.0, 1), (14, 3, 3, 1.0, 4.0, 1.0, 0),
                (15, 3, 4, 1.0, 5.0, 1.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, fixed_fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 1), (1, 0, 1, 1.0, 2.0, -0.1, 0), (2, 0, 3, 1.0, 4.0, -0.1, 1),
                (3, 0, 4, 1.0, 5.0, -0.1, 0), (4, 1, 0, 1.0, 1.0, 0.0, 1), (5, 1, 1, 1.0, 2.0, 0.0, 0),
                (6, 1, 3, 1.0, 4.0, 0.0, 1), (7, 1, 4, 1.0, 5.0, 0.0, 0), (8, 2, 0, 1.0, 1.0, 0.1, 1),
                (9, 2, 1, 1.0, 2.0, 0.1, 0), (10, 2, 3, 1.0, 4.0, 0.1, 1), (11, 2, 4, 1.0, 5.0, 0.1, 0),
                (12, 3, 0, 1.0, 1.0, 1.0, 1), (13, 3, 1, 1.0, 2.0, 1.0, 0), (14, 3, 3, 1.0, 4.0, 1.0, 1),
                (15, 3, 4, 1.0, 5.0, 1.0, 0)
            ], dtype=order_dt)
        )

    def test_slippage(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, slippage=[[0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 1.0, 2.0, 0.0, 1), (2, 0, 3, 1.0, 4.0, 0.0, 0),
                (3, 0, 4, 1.0, 5.0, 0.0, 1), (4, 1, 0, 1.0, 1.1, 0.0, 0), (5, 1, 1, 1.0, 1.8, 0.0, 1),
                (6, 1, 3, 1.0, 4.4, 0.0, 0), (7, 1, 4, 1.0, 4.5, 0.0, 1), (8, 2, 0, 1.0, 2.0, 0.0, 0),
                (9, 2, 1, 1.0, 0.0, 0.0, 1), (10, 2, 3, 1.0, 8.0, 0.0, 0), (11, 2, 4, 1.0, 0.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, slippage=[[0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 1.0, 2.0, 0.0, 1), (2, 0, 3, 1.0, 4.0, 0.0, 0),
                (3, 0, 4, 1.0, 5.0, 0.0, 1), (4, 1, 0, 1.0, 1.1, 0.0, 0), (5, 1, 1, 1.0, 1.8, 0.0, 1),
                (6, 1, 3, 1.0, 4.4, 0.0, 0), (7, 1, 4, 1.0, 4.5, 0.0, 1), (8, 2, 0, 1.0, 2.0, 0.0, 0),
                (9, 2, 1, 1.0, 0.0, 0.0, 1), (10, 2, 3, 1.0, 8.0, 0.0, 0), (11, 2, 4, 1.0, 0.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, slippage=[[0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 1, 1.0, 2.0, 0.0, 0), (2, 0, 3, 1.0, 4.0, 0.0, 1),
                (3, 0, 4, 1.0, 5.0, 0.0, 0), (4, 1, 0, 1.0, 0.9, 0.0, 1), (5, 1, 1, 1.0, 2.2, 0.0, 0),
                (6, 1, 3, 1.0, 3.6, 0.0, 1), (7, 1, 4, 1.0, 5.5, 0.0, 0), (8, 2, 0, 1.0, 0.0, 0.0, 1),
                (9, 2, 1, 1.0, 4.0, 0.0, 0), (10, 2, 3, 1.0, 0.0, 0.0, 1), (11, 2, 4, 1.0, 10.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_min_size(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, min_size=[[0., 1., 2.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 1.0, 2.0, 0.0, 1), (2, 0, 3, 1.0, 4.0, 0.0, 0),
                (3, 0, 4, 1.0, 5.0, 0.0, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, min_size=[[0., 1., 2.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 1.0, 2.0, 0.0, 1), (2, 0, 3, 1.0, 4.0, 0.0, 0),
                (3, 0, 4, 1.0, 5.0, 0.0, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, min_size=[[0., 1., 2.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 1, 1.0, 2.0, 0.0, 0), (2, 0, 3, 1.0, 4.0, 0.0, 1),
                (3, 0, 4, 1.0, 5.0, 0.0, 0), (4, 1, 0, 1.0, 1.0, 0.0, 1), (5, 1, 1, 1.0, 2.0, 0.0, 0),
                (6, 1, 3, 1.0, 4.0, 0.0, 1), (7, 1, 4, 1.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_max_size(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, max_size=[[0.5, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 0.5, 1.0, 0.0, 0), (1, 0, 1, 0.5, 2.0, 0.0, 1), (2, 0, 3, 0.5, 4.0, 0.0, 0),
                (3, 0, 4, 0.5, 5.0, 0.0, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1), (8, 2, 0, 1.0, 1.0, 0.0, 0),
                (9, 2, 1, 1.0, 2.0, 0.0, 1), (10, 2, 3, 1.0, 4.0, 0.0, 0), (11, 2, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, max_size=[[0.5, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 0.5, 1.0, 0.0, 0), (1, 0, 1, 0.5, 2.0, 0.0, 1), (2, 0, 3, 0.5, 4.0, 0.0, 0),
                (3, 0, 4, 0.5, 5.0, 0.0, 1), (4, 1, 0, 1.0, 1.0, 0.0, 0), (5, 1, 1, 1.0, 2.0, 0.0, 1),
                (6, 1, 3, 1.0, 4.0, 0.0, 0), (7, 1, 4, 1.0, 5.0, 0.0, 1), (8, 2, 0, 1.0, 1.0, 0.0, 0),
                (9, 2, 1, 1.0, 2.0, 0.0, 1), (10, 2, 3, 1.0, 4.0, 0.0, 0), (11, 2, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, max_size=[[0.5, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 0.5, 1.0, 0.0, 1), (1, 0, 1, 0.5, 2.0, 0.0, 0), (2, 0, 3, 0.5, 4.0, 0.0, 1),
                (3, 0, 4, 0.5, 5.0, 0.0, 0), (4, 1, 0, 1.0, 1.0, 0.0, 1), (5, 1, 1, 1.0, 2.0, 0.0, 0),
                (6, 1, 3, 1.0, 4.0, 0.0, 1), (7, 1, 4, 1.0, 5.0, 0.0, 0), (8, 2, 0, 1.0, 1.0, 0.0, 1),
                (9, 2, 1, 1.0, 2.0, 0.0, 0), (10, 2, 3, 1.0, 4.0, 0.0, 1), (11, 2, 4, 1.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_reject_prob(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, reject_prob=[[0., 0.5, 1.]], seed=42).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 1.0, 2.0, 0.0, 1), (2, 0, 3, 1.0, 4.0, 0.0, 0),
                (3, 0, 4, 1.0, 5.0, 0.0, 1), (4, 1, 1, 1.0, 2.0, 0.0, 1), (5, 1, 3, 1.0, 4.0, 0.0, 0),
                (6, 1, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, reject_prob=[[0., 0.5, 1.]], seed=42).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 1.0, 2.0, 0.0, 1), (2, 0, 3, 1.0, 4.0, 0.0, 0),
                (3, 0, 4, 1.0, 5.0, 0.0, 1), (4, 1, 3, 1.0, 4.0, 0.0, 0), (5, 1, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, reject_prob=[[0., 0.5, 1.]], seed=42).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 1, 1.0, 2.0, 0.0, 0), (2, 0, 3, 1.0, 4.0, 0.0, 1),
                (3, 0, 4, 1.0, 5.0, 0.0, 0), (4, 1, 3, 1.0, 4.0, 0.0, 1), (5, 1, 4, 1.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_lock_cash(self):
        pf = vbt.Portfolio.from_orders(
            pd.Series([1, 1]),
            pd.DataFrame([[-25, -25], [np.inf, np.inf]]),
            group_by=True, cash_sharing=True,
            lock_cash=False, fees=0.01, fixed_fees=1., slippage=0.01)
        np.testing.assert_array_equal(
            pf.asset_flow().values,
            np.array([
                [-25.0, -25.0],
                [143.12812469365747, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True).values,
            np.array([
                [123.5025, 147.005],
                [0.0, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True, free=True).values,
            np.array([
                [74.0025, 48.004999999999995],
                [-49.5, -49.5]
            ])
        )
        pf = vbt.Portfolio.from_orders(
            pd.Series([1, 1]),
            pd.DataFrame([[-25, -25], [np.inf, np.inf]]),
            group_by=True, cash_sharing=True,
            lock_cash=True, fees=0.01, fixed_fees=1., slippage=0.01)
        np.testing.assert_array_equal(
            pf.asset_flow().values,
            np.array([
                [-25.0, -25.0],
                [94.6034702480149, 47.54435839623566]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True).values,
            np.array([
                [123.5025, 147.005],
                [49.5, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True, free=True).values,
            np.array([
                [74.0025, 48.004999999999995],
                [0.0, 0.0]
            ])
        )
        pf = vbt.Portfolio.from_orders(
            pd.Series([1, 100]),
            pd.DataFrame([[-25, -25], [np.inf, np.inf]]),
            group_by=True, cash_sharing=True,
            lock_cash=False, fees=0.01, fixed_fees=1., slippage=0.01)
        np.testing.assert_array_equal(
            pf.asset_flow().values,
            np.array([
                [-25.0, -25.0],
                [1.4312812469365748, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True).values,
            np.array([
                [123.5025, 147.005],
                [0.0, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True, free=True).values,
            np.array([
                [74.0025, 48.004999999999995],
                [-96.16606313106556, -96.16606313106556]
            ])
        )
        pf = vbt.Portfolio.from_orders(
            pd.Series([1, 100]),
            pd.DataFrame([[-25, -25], [np.inf, np.inf]]),
            group_by=True, cash_sharing=True,
            lock_cash=True, fees=0.01, fixed_fees=1., slippage=0.01)
        np.testing.assert_array_equal(
            pf.asset_flow().values,
            np.array([
                [-25.0, -25.0],
                [0.4699090272918124, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True).values,
            np.array([
                [123.5025, 147.005],
                [98.06958012596222, 98.06958012596222]
            ])
        )
        np.testing.assert_array_equal(
            pf.cash(group_by=False, in_sim_order=True, free=True).values,
            np.array([
                [74.0025, 48.004999999999995],
                [0.0, 0.0]
            ])
        )
        pf = from_orders_both(size=order_size_one * 1000, lock_cash=[[False, True]])
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 1, 1000., 2., 0., 1),
                (2, 0, 3, 500., 4., 0., 0), (3, 0, 4, 1000., 5., 0., 1),
                (4, 1, 0, 100., 1., 0., 0), (5, 1, 1, 200., 2., 0., 1),
                (6, 1, 3, 100., 4., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.cash(free=True).values,
            np.array([
                [0.0, 0.0],
                [-1600.0, 0.0],
                [-1600.0, 0.0],
                [-1600.0, 0.0],
                [-6600.0, 0.0]
            ])
        )
        pf = from_orders_longonly(size=order_size_one * 1000, lock_cash=[[False, True]])
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 1, 100., 2., 0., 1),
                (2, 0, 3, 50., 4., 0., 0), (3, 0, 4, 50., 5., 0., 1),
                (4, 1, 0, 100., 1., 0., 0), (5, 1, 1, 100., 2., 0., 1),
                (6, 1, 3, 50., 4., 0., 0), (7, 1, 4, 50., 5., 0., 1)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.cash(free=True).values,
            np.array([
                [0.0, 0.0],
                [200.0, 200.0],
                [200.0, 200.0],
                [0.0, 0.0],
                [250.0, 250.0]
            ])
        )
        pf = from_orders_shortonly(size=order_size_one * 1000, lock_cash=[[False, True]])
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 1000., 1., 0., 1), (1, 0, 1, 550., 2., 0., 0),
                (2, 0, 3, 1000., 4., 0., 1), (3, 0, 4, 800., 5., 0., 0),
                (4, 1, 0, 100., 1., 0., 1), (5, 1, 1, 100., 2., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.cash(free=True).values,
            np.array([
                [-900.0, 0.0],
                [-900.0, 0.0],
                [-900.0, 0.0],
                [-4900.0, 0.0],
                [-3989.6551724137926, 0.0]
            ])
        )

    def test_allow_partial(self):
        record_arrays_close(
            from_orders_both(size=order_size_one * 1000, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 1000.0, 2.0, 0.0, 1), (2, 0, 3, 500.0, 4.0, 0.0, 0),
                (3, 0, 4, 1000.0, 5.0, 0.0, 1), (4, 1, 1, 1000.0, 2.0, 0.0, 1), (5, 1, 4, 1000.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one * 1000, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 100.0, 2.0, 0.0, 1), (2, 0, 3, 50.0, 4.0, 0.0, 0),
                (3, 0, 4, 50.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one * 1000, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 1000.0, 1.0, 0.0, 1), (1, 0, 1, 550.0, 2.0, 0.0, 0), (2, 0, 3, 1000.0, 4.0, 0.0, 1),
                (3, 0, 4, 800.0, 5.0, 0.0, 0), (4, 1, 0, 1000.0, 1.0, 0.0, 1), (5, 1, 3, 1000.0, 4.0, 0.0, 1),
                (6, 1, 4, 1000.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(size=order_size, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1), (2, 0, 3, 100.0, 4.0, 0.0, 0),
                (3, 1, 0, 100.0, 1.0, 0.0, 0), (4, 1, 1, 200.0, 2.0, 0.0, 1), (5, 1, 3, 100.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 100.0, 2.0, 0.0, 1), (2, 0, 3, 50.0, 4.0, 0.0, 0),
                (3, 0, 4, 50.0, 5.0, 0.0, 1), (4, 1, 0, 100.0, 1.0, 0.0, 0), (5, 1, 1, 100.0, 2.0, 0.0, 1),
                (6, 1, 3, 50.0, 4.0, 0.0, 0), (7, 1, 4, 50.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1), (1, 0, 1, 100.0, 2.0, 0.0, 0), (2, 1, 0, 100.0, 1.0, 0.0, 1),
                (3, 1, 1, 100.0, 2.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_raise_reject(self):
        record_arrays_close(
            from_orders_both(size=order_size_one * 1000, allow_partial=True, raise_reject=True).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 1000.0, 2.0, 0.0, 1), (2, 0, 3, 500.0, 4.0, 0.0, 0),
                (3, 0, 4, 1000.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one * 1000, allow_partial=True, raise_reject=True).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 100.0, 2.0, 0.0, 1), (2, 0, 3, 50.0, 4.0, 0.0, 0),
                (3, 0, 4, 50.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one * 1000, allow_partial=True, raise_reject=True).order_records,
            np.array([
                (0, 0, 0, 1000.0, 1.0, 0.0, 1), (1, 0, 1, 550.0, 2.0, 0.0, 0), (2, 0, 3, 1000.0, 4.0, 0.0, 1),
                (3, 0, 4, 800.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        with pytest.raises(Exception):
            _ = from_orders_both(size=order_size_one * 1000, allow_partial=False, raise_reject=True).order_records
        with pytest.raises(Exception):
            _ = from_orders_longonly(size=order_size_one * 1000, allow_partial=False, raise_reject=True).order_records
        with pytest.raises(Exception):
            _ = from_orders_shortonly(size=order_size_one * 1000, allow_partial=False, raise_reject=True).order_records

    def test_log(self):
        record_arrays_close(
            from_orders_both(log=True).log_records,
            np.array([
                (0, 0, 0, 0, 100.0, 0.0, 0.0, 100.0, 1.0, 100.0, np.inf, 1.0, 0, 2,
                 0.0, 0.0, 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 0.0,
                 100.0, 0.0, 0.0, 1.0, 100.0, 100.0, 1.0, 0.0, 0, 0, -1, 0),
                (1, 0, 0, 1, 0.0, 100.0, 0.0, 0.0, 2.0, 200.0, -np.inf, 2.0, 0, 2,
                 0.0, 0.0, 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 400.0,
                 -100.0, 200.0, 0.0, 2.0, 200.0, 200.0, 2.0, 0.0, 1, 0, -1, 1),
                (2, 0, 0, 2, 400.0, -100.0, 200.0, 0.0, 3.0, 100.0, np.nan, 3.0, 0,
                 2, 0.0, 0.0, 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 400.0,
                 -100.0, 200.0, 0.0, 3.0, 100.0, np.nan, np.nan, np.nan, -1, 1, 0, -1),
                (3, 0, 0, 3, 400.0, -100.0, 200.0, 0.0, 4.0, 0.0, np.inf, 4.0, 0, 2,
                 0.0, 0.0, 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 0.0, 0.0,
                 0.0, 0.0, 4.0, 0.0, 100.0, 4.0, 0.0, 0, 0, -1, 2),
                (4, 0, 0, 4, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, -np.inf, 5.0, 0, 2, 0.0,
                 0.0, 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 0.0, 0.0,
                 0.0, 0.0, 5.0, 0.0, np.nan, np.nan, np.nan, -1, 2, 6, -1)
            ], dtype=log_dt)
        )

    def test_group_by(self):
        pf = from_orders_both(close=price_wide, group_by=np.array([0, 0, 1]))
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1), (2, 0, 3, 100.0, 4.0, 0.0, 0),
                (3, 1, 0, 100.0, 1.0, 0.0, 0), (4, 1, 1, 200.0, 2.0, 0.0, 1), (5, 1, 3, 100.0, 4.0, 0.0, 0),
                (6, 2, 0, 100.0, 1.0, 0.0, 0), (7, 2, 1, 200.0, 2.0, 0.0, 1), (8, 2, 3, 100.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        pd.testing.assert_index_equal(
            pf.wrapper.grouper.group_by,
            pd.Index([0, 0, 1], dtype='int64')
        )
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series([200., 100.], index=pd.Index([0, 1], dtype='int64')).rename('init_cash')
        )
        assert not pf.cash_sharing

    def test_cash_sharing(self):
        pf = from_orders_both(close=price_wide, group_by=np.array([0, 0, 1]), cash_sharing=True)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 1, 200., 2., 0., 1),
                (2, 0, 3, 100., 4., 0., 0), (3, 2, 0, 100., 1., 0., 0),
                (4, 2, 1, 200., 2., 0., 1), (5, 2, 3, 100., 4., 0., 0)
            ], dtype=order_dt)
        )
        pd.testing.assert_index_equal(
            pf.wrapper.grouper.group_by,
            pd.Index([0, 0, 1], dtype='int64')
        )
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series([100., 100.], index=pd.Index([0, 1], dtype='int64')).rename('init_cash')
        )
        assert pf.cash_sharing
        with pytest.raises(Exception):
            _ = pf.regroup(group_by=False)

    def test_call_seq(self):
        pf = from_orders_both(close=price_wide, group_by=np.array([0, 0, 1]), cash_sharing=True)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 1, 200., 2., 0., 1),
                (2, 0, 3, 100., 4., 0., 0), (3, 2, 0, 100., 1., 0., 0),
                (4, 2, 1, 200., 2., 0., 1), (5, 2, 3, 100., 4., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ])
        )
        pf = from_orders_both(
            close=price_wide, group_by=np.array([0, 0, 1]),
            cash_sharing=True, call_seq='reversed')
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 1, 0, 100., 1., 0., 0), (1, 1, 1, 200., 2., 0., 1),
                (2, 1, 3, 100., 4., 0., 0), (3, 2, 0, 100., 1., 0., 0),
                (4, 2, 1, 200., 2., 0., 1), (5, 2, 3, 100., 4., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0]
            ])
        )
        pf = from_orders_both(
            close=price_wide, group_by=np.array([0, 0, 1]),
            cash_sharing=True, call_seq='random', seed=seed)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 1, 0, 100., 1., 0., 0), (1, 1, 1, 200., 2., 0., 1),
                (2, 1, 3, 100., 4., 0., 0), (3, 2, 0, 100., 1., 0., 0),
                (4, 2, 1, 200., 2., 0., 1), (5, 2, 3, 100., 4., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [1, 0, 0],
                [0, 1, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0]
            ])
        )
        kwargs = dict(
            close=1.,
            size=pd.DataFrame([
                [0., 0., np.inf],
                [0., np.inf, -np.inf],
                [np.inf, -np.inf, 0.],
                [-np.inf, 0., np.inf],
                [0., np.inf, -np.inf],
            ]),
            group_by=np.array([0, 0, 0]),
            cash_sharing=True,
            call_seq='auto'
        )
        pf = from_orders_both(**kwargs)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100., 1., 0., 0), (1, 2, 1, 200., 1., 0., 1),
                (2, 1, 1, 200., 1., 0., 0), (3, 1, 2, 200., 1., 0., 1),
                (4, 0, 2, 200., 1., 0., 0), (5, 0, 3, 200., 1., 0., 1),
                (6, 2, 3, 200., 1., 0., 0), (7, 2, 4, 200., 1., 0., 1),
                (8, 1, 4, 200., 1., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 2],
                [2, 0, 1],
                [1, 2, 0],
                [0, 1, 2],
                [2, 0, 1]
            ])
        )
        pf = from_orders_longonly(**kwargs)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100., 1., 0., 0), (1, 2, 1, 100., 1., 0., 1),
                (2, 1, 1, 100., 1., 0., 0), (3, 1, 2, 100., 1., 0., 1),
                (4, 0, 2, 100., 1., 0., 0), (5, 0, 3, 100., 1., 0., 1),
                (6, 2, 3, 100., 1., 0., 0), (7, 2, 4, 100., 1., 0., 1),
                (8, 1, 4, 100., 1., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 2],
                [2, 0, 1],
                [1, 2, 0],
                [0, 1, 2],
                [2, 0, 1]
            ])
        )
        pf = from_orders_shortonly(**kwargs)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100., 1., 0., 1), (1, 2, 1, 100., 1., 0., 0),
                (2, 0, 2, 100., 1., 0., 1), (3, 0, 3, 100., 1., 0., 0),
                (4, 1, 4, 100., 1., 0., 1)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [2, 0, 1],
                [1, 0, 2],
                [0, 2, 1],
                [2, 1, 0],
                [1, 0, 2]
            ])
        )

    def test_value(self):
        record_arrays_close(
            from_orders_both(size=order_size_one, size_type='value').order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 0.5, 2.0, 0.0, 1),
                (2, 0, 3, 0.25, 4.0, 0.0, 0), (3, 0, 4, 0.2, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=order_size_one, size_type='value').order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 0.5, 2.0, 0.0, 1),
                (2, 0, 3, 0.25, 4.0, 0.0, 0), (3, 0, 4, 0.2, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=order_size_one, size_type='value').order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 1, 0.5, 2.0, 0.0, 0),
                (2, 0, 3, 0.25, 4.0, 0.0, 1), (3, 0, 4, 0.2, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_target_amount(self):
        record_arrays_close(
            from_orders_both(size=[[75., -75.]], size_type='targetamount').order_records,
            np.array([
                (0, 0, 0, 75.0, 1.0, 0.0, 0), (1, 1, 0, 75.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=[[75., -75.]], size_type='targetamount').order_records,
            np.array([
                (0, 0, 0, 75.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=[[75., -75.]], size_type='targetamount').order_records,
            np.array([
                (0, 0, 0, 75.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(
                close=price_wide, size=75., size_type='targetamount',
                group_by=np.array([0, 0, 0]), cash_sharing=True).order_records,
            np.array([
                (0, 0, 0, 75.0, 1.0, 0.0, 0), (1, 1, 0, 25.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_target_value(self):
        record_arrays_close(
            from_orders_both(size=[[50., -50.]], size_type='targetvalue').order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 0, 1, 25.0, 2.0, 0.0, 1),
                (2, 0, 2, 8.333333333333332, 3.0, 0.0, 1), (3, 0, 3, 4.166666666666668, 4.0, 0.0, 1),
                (4, 0, 4, 2.5, 5.0, 0.0, 1), (5, 1, 0, 50.0, 1.0, 0.0, 1),
                (6, 1, 1, 25.0, 2.0, 0.0, 0), (7, 1, 2, 8.333333333333332, 3.0, 0.0, 0),
                (8, 1, 3, 4.166666666666668, 4.0, 0.0, 0), (9, 1, 4, 2.5, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=[[50., -50.]], size_type='targetvalue').order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 0, 1, 25.0, 2.0, 0.0, 1),
                (2, 0, 2, 8.333333333333332, 3.0, 0.0, 1), (3, 0, 3, 4.166666666666668, 4.0, 0.0, 1),
                (4, 0, 4, 2.5, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=[[50., -50.]], size_type='targetvalue').order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 1), (1, 0, 1, 25.0, 2.0, 0.0, 0),
                (2, 0, 2, 8.333333333333332, 3.0, 0.0, 0), (3, 0, 3, 4.166666666666668, 4.0, 0.0, 0),
                (4, 0, 4, 2.5, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(
                close=price_wide, size=50., size_type='targetvalue',
                group_by=np.array([0, 0, 0]), cash_sharing=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 1, 0, 50.0, 1.0, 0.0, 0),
                (2, 0, 1, 25.0, 2.0, 0.0, 1), (3, 1, 1, 25.0, 2.0, 0.0, 1),
                (4, 2, 1, 25.0, 2.0, 0.0, 0), (5, 0, 2, 8.333333333333332, 3.0, 0.0, 1),
                (6, 1, 2, 8.333333333333332, 3.0, 0.0, 1), (7, 2, 2, 8.333333333333332, 3.0, 0.0, 1),
                (8, 0, 3, 4.166666666666668, 4.0, 0.0, 1), (9, 1, 3, 4.166666666666668, 4.0, 0.0, 1),
                (10, 2, 3, 4.166666666666668, 4.0, 0.0, 1), (11, 0, 4, 2.5, 5.0, 0.0, 1),
                (12, 1, 4, 2.5, 5.0, 0.0, 1), (13, 2, 4, 2.5, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_target_percent(self):
        record_arrays_close(
            from_orders_both(size=[[0.5, -0.5]], size_type='targetpercent').order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 0, 1, 12.5, 2.0, 0.0, 1), (2, 0, 2, 6.25, 3.0, 0.0, 1),
                (3, 0, 3, 3.90625, 4.0, 0.0, 1), (4, 0, 4, 2.734375, 5.0, 0.0, 1), (5, 1, 0, 50.0, 1.0, 0.0, 1),
                (6, 1, 1, 37.5, 2.0, 0.0, 0), (7, 1, 2, 6.25, 3.0, 0.0, 0), (8, 1, 3, 2.34375, 4.0, 0.0, 0),
                (9, 1, 4, 1.171875, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=[[0.5, -0.5]], size_type='targetpercent').order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 0, 1, 12.5, 2.0, 0.0, 1), (2, 0, 2, 6.25, 3.0, 0.0, 1),
                (3, 0, 3, 3.90625, 4.0, 0.0, 1), (4, 0, 4, 2.734375, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=[[0.5, -0.5]], size_type='targetpercent').order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 1), (1, 0, 1, 37.5, 2.0, 0.0, 0), (2, 0, 2, 6.25, 3.0, 0.0, 0),
                (3, 0, 3, 2.34375, 4.0, 0.0, 0), (4, 0, 4, 1.171875, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(
                close=price_wide, size=0.5, size_type='targetpercent',
                group_by=np.array([0, 0, 0]), cash_sharing=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 1, 0, 50.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_update_value(self):
        record_arrays_close(
            from_orders_both(size=0.5, size_type='targetpercent', fees=0.01, slippage=0.01,
                             update_value=False).order_records,
            from_orders_both(size=0.5, size_type='targetpercent', fees=0.01, slippage=0.01,
                             update_value=True).order_records
        )
        record_arrays_close(
            from_orders_both(
                close=price_wide, size=0.5, size_type='targetpercent', fees=0.01, slippage=0.01,
                group_by=np.array([0, 0, 0]), cash_sharing=True, update_value=False).order_records,
            np.array([
                (0, 0, 0, 50.0, 1.01, 0.505, 0),
                (1, 1, 0, 48.02960494069208, 1.01, 0.485099009900992, 0),
                (2, 0, 1, 0.9851975296539592, 1.98, 0.019506911087148394, 1),
                (3, 1, 1, 0.9465661198057499, 2.02, 0.019120635620076154, 0),
                (4, 0, 2, 0.019315704924103727, 2.9699999999999998, 0.0005736764362458806, 1),
                (5, 1, 2, 0.018558300554959377, 3.0300000000000002, 0.0005623165068152705, 0),
                (6, 0, 3, 0.00037870218456959037, 3.96, 1.4996606508955778e-05, 1),
                (7, 1, 3, 0.0003638525743521767, 4.04, 1.4699644003827875e-05, 0),
                (8, 0, 4, 7.424805112066224e-06, 4.95, 3.675278530472781e-07, 1),
                (9, 1, 4, 7.133664827307231e-06, 5.05, 3.6025007377901643e-07, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(
                close=price_wide, size=0.5, size_type='targetpercent', fees=0.01, slippage=0.01,
                group_by=np.array([0, 0, 0]), cash_sharing=True, update_value=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 1.01, 0.505, 0),
                (1, 1, 0, 48.02960494069208, 1.01, 0.485099009900992, 0),
                (2, 0, 1, 0.9851975296539592, 1.98, 0.019506911087148394, 1),
                (3, 1, 1, 0.7303208018821721, 2.02, 0.014752480198019875, 0),
                (4, 2, 1, 0.21624531792357785, 2.02, 0.0043681554220562635, 0),
                (5, 0, 2, 0.019315704924103727, 2.9699999999999998, 0.0005736764362458806, 1),
                (6, 1, 2, 0.009608602243410758, 2.9699999999999998, 0.00028537548662929945, 1),
                (7, 2, 2, 0.02779013180558861, 3.0300000000000002, 0.0008420409937093393, 0),
                (8, 0, 3, 0.0005670876809631409, 3.96, 2.2456672166140378e-05, 1),
                (9, 1, 3, 0.00037770350099464167, 3.96, 1.4957058639387809e-05, 1),
                (10, 2, 3, 0.0009077441794302741, 4.04, 3.6672864848982974e-05, 0),
                (11, 0, 4, 1.8523501267964093e-05, 4.95, 9.169133127642227e-07, 1),
                (12, 1, 4, 1.2972670177191503e-05, 4.95, 6.421471737709794e-07, 1),
                (13, 2, 4, 3.0261148547590434e-05, 5.05, 1.5281880016533242e-06, 0)
            ], dtype=order_dt)
        )

    def test_percent(self):
        record_arrays_close(
            from_orders_both(size=[[0.5, -0.5]], size_type='percent').order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 0), (1, 0, 1, 12.5, 2., 0., 0),
                (2, 0, 2, 4.16666667, 3., 0., 0), (3, 0, 3, 1.5625, 4., 0., 0),
                (4, 0, 4, 0.625, 5., 0., 0), (5, 1, 0, 50., 1., 0., 1),
                (6, 1, 1, 12.5, 2., 0., 1), (7, 1, 2, 4.16666667, 3., 0., 1),
                (8, 1, 3, 1.5625, 4., 0., 1), (9, 1, 4, 0.625, 5., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_longonly(size=[[0.5, -0.5]], size_type='percent').order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 0), (1, 0, 1, 12.5, 2., 0., 0),
                (2, 0, 2, 4.16666667, 3., 0., 0), (3, 0, 3, 1.5625, 4., 0., 0),
                (4, 0, 4, 0.625, 5., 0., 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_shortonly(size=[[0.5, -0.5]], size_type='percent').order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 1), (1, 0, 1, 12.5, 2., 0., 1),
                (2, 0, 2, 4.16666667, 3., 0., 1), (3, 0, 3, 1.5625, 4., 0., 1),
                (4, 0, 4, 0.625, 5., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_orders_both(
                close=price_wide, size=0.5, size_type='percent',
                group_by=np.array([0, 0, 0]), cash_sharing=True).order_records,
            np.array([
                (0, 0, 0, 5.00000000e+01, 1., 0., 0), (1, 1, 0, 2.50000000e+01, 1., 0., 0),
                (2, 2, 0, 1.25000000e+01, 1., 0., 0), (3, 0, 1, 3.12500000e+00, 2., 0., 0),
                (4, 1, 1, 1.56250000e+00, 2., 0., 0), (5, 2, 1, 7.81250000e-01, 2., 0., 0),
                (6, 0, 2, 2.60416667e-01, 3., 0., 0), (7, 1, 2, 1.30208333e-01, 3., 0., 0),
                (8, 2, 2, 6.51041667e-02, 3., 0., 0), (9, 0, 3, 2.44140625e-02, 4., 0., 0),
                (10, 1, 3, 1.22070312e-02, 4., 0., 0), (11, 2, 3, 6.10351562e-03, 4., 0., 0),
                (12, 0, 4, 2.44140625e-03, 5., 0., 0), (13, 1, 4, 1.22070312e-03, 5., 0., 0),
                (14, 2, 4, 6.10351562e-04, 5., 0., 0)
            ], dtype=order_dt)
        )

    def test_auto_seq(self):
        target_hold_value = pd.DataFrame({
            'a': [0., 70., 30., 0., 70.],
            'b': [30., 0., 70., 30., 30.],
            'c': [70., 30., 0., 70., 0.]
        }, index=price.index)
        pd.testing.assert_frame_equal(
            from_orders_both(
                close=1., size=target_hold_value, size_type='targetvalue',
                group_by=np.array([0, 0, 0]), cash_sharing=True,
                call_seq='auto').asset_value(group_by=False),
            target_hold_value
        )
        pd.testing.assert_frame_equal(
            from_orders_both(
                close=1., size=target_hold_value / 100, size_type='targetpercent',
                group_by=np.array([0, 0, 0]), cash_sharing=True,
                call_seq='auto').asset_value(group_by=False),
            target_hold_value
        )

    def test_max_orders(self):
        _ = from_orders_both(close=price_wide)
        _ = from_orders_both(close=price_wide, max_orders=9)
        with pytest.raises(Exception):
            _ = from_orders_both(close=price_wide, max_orders=8)

    def test_max_logs(self):
        _ = from_orders_both(close=price_wide, log=True)
        _ = from_orders_both(close=price_wide, log=True, max_logs=15)
        with pytest.raises(Exception):
            _ = from_orders_both(close=price_wide, log=True, max_logs=14)


# ############# from_signals ############# #

entries = pd.Series([True, True, True, False, False], index=price.index)
entries_wide = entries.vbt.tile(3, keys=['a', 'b', 'c'])

exits = pd.Series([False, False, True, True, True], index=price.index)
exits_wide = exits.vbt.tile(3, keys=['a', 'b', 'c'])


def from_signals_both(close=price, entries=entries, exits=exits, **kwargs):
    return vbt.Portfolio.from_signals(close, entries, exits, direction='both', **kwargs)


def from_signals_longonly(close=price, entries=entries, exits=exits, **kwargs):
    return vbt.Portfolio.from_signals(close, entries, exits, direction='longonly', **kwargs)


def from_signals_shortonly(close=price, entries=entries, exits=exits, **kwargs):
    return vbt.Portfolio.from_signals(close, entries, exits, direction='shortonly', **kwargs)


def from_ls_signals_both(close=price, entries=entries, exits=exits, **kwargs):
    return vbt.Portfolio.from_signals(close, entries, False, exits, False, **kwargs)


def from_ls_signals_longonly(close=price, entries=entries, exits=exits, **kwargs):
    return vbt.Portfolio.from_signals(close, entries, exits, False, False, **kwargs)


def from_ls_signals_shortonly(close=price, entries=entries, exits=exits, **kwargs):
    return vbt.Portfolio.from_signals(close, False, False, entries, exits, **kwargs)


class TestFromSignals:
    @pytest.mark.parametrize(
        "test_ls",
        [False, True],
    )
    def test_one_column(self, test_ls):
        _from_signals_both = from_ls_signals_both if test_ls else from_signals_both
        _from_signals_longonly = from_ls_signals_longonly if test_ls else from_signals_longonly
        _from_signals_shortonly = from_ls_signals_shortonly if test_ls else from_signals_shortonly
        record_arrays_close(
            _from_signals_both().order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 3, 200., 4., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            _from_signals_longonly().order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 3, 100., 4., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            _from_signals_shortonly().order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 1), (1, 0, 3, 50., 4., 0., 0)
            ], dtype=order_dt)
        )
        pf = _from_signals_both()
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'])
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            pd.Index([0], dtype='int64')
        )
        assert pf.wrapper.ndim == 1
        assert pf.wrapper.freq == day_dt
        assert pf.wrapper.grouper.group_by is None

    @pytest.mark.parametrize(
        "test_ls",
        [False, True],
    )
    def test_multiple_columns(self, test_ls):
        _from_signals_both = from_ls_signals_both if test_ls else from_signals_both
        _from_signals_longonly = from_ls_signals_longonly if test_ls else from_signals_longonly
        _from_signals_shortonly = from_ls_signals_shortonly if test_ls else from_signals_shortonly
        record_arrays_close(
            _from_signals_both(close=price_wide).order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 3, 200., 4., 0., 1),
                (2, 1, 0, 100., 1., 0., 0), (3, 1, 3, 200., 4., 0., 1),
                (4, 2, 0, 100., 1., 0., 0), (5, 2, 3, 200., 4., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            _from_signals_longonly(close=price_wide).order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 3, 100., 4., 0., 1),
                (2, 1, 0, 100., 1., 0., 0), (3, 1, 3, 100., 4., 0., 1),
                (4, 2, 0, 100., 1., 0., 0), (5, 2, 3, 100., 4., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            _from_signals_shortonly(close=price_wide).order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 1), (1, 0, 3, 50., 4., 0., 0),
                (2, 1, 0, 100., 1., 0., 1), (3, 1, 3, 50., 4., 0., 0),
                (4, 2, 0, 100., 1., 0., 1), (5, 2, 3, 50., 4., 0., 0)
            ], dtype=order_dt)
        )
        pf = _from_signals_both(close=price_wide)
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'])
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            pd.Index(['a', 'b', 'c'], dtype='object')
        )
        assert pf.wrapper.ndim == 2
        assert pf.wrapper.freq == day_dt
        assert pf.wrapper.grouper.group_by is None

    def test_custom_signal_func(self):
        @njit
        def signal_func_nb(c, long_num_arr, short_num_arr):
            long_num = nb.get_elem_nb(c, long_num_arr)
            short_num = nb.get_elem_nb(c, short_num_arr)
            is_long_entry = long_num > 0
            is_long_exit = long_num < 0
            is_short_entry = short_num > 0
            is_short_exit = short_num < 0
            return is_long_entry, is_long_exit, is_short_entry, is_short_exit

        pf_base = vbt.Portfolio.from_signals(
            pd.Series([1, 2, 3, 4, 5]),
            entries=pd.Series([True, False, False, False, False]),
            exits=pd.Series([False, False, True, False, False]),
            short_entries=pd.Series([False, True, False, True, False]),
            short_exits=pd.Series([False, False, False, False, True]),
            size=1,
            upon_opposite_entry='ignore'
        )
        pf = vbt.Portfolio.from_signals(
            pd.Series([1, 2, 3, 4, 5]),
            signal_func_nb=signal_func_nb,
            signal_args=(vbt.Rep('long_num_arr'), vbt.Rep('short_num_arr')),
            broadcast_named_args=dict(
                long_num_arr=pd.Series([1, 0, -1, 0, 0]),
                short_num_arr=pd.Series([0, 1, 0, 1, -1])
            ),
            size=1,
            upon_opposite_entry='ignore'
        )
        record_arrays_close(
            pf_base.order_records,
            pf.order_records
        )

    def test_amount(self):
        record_arrays_close(
            from_signals_both(size=[[0, 1, np.inf]], size_type='amount').order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 1, 3, 2.0, 4.0, 0.0, 1),
                (2, 2, 0, 100.0, 1.0, 0.0, 0), (3, 2, 3, 200.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=[[0, 1, np.inf]], size_type='amount').order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 1, 3, 1.0, 4.0, 0.0, 1),
                (2, 2, 0, 100.0, 1.0, 0.0, 0), (3, 2, 3, 100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=[[0, 1, np.inf]], size_type='amount').order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 1), (1, 1, 3, 1.0, 4.0, 0.0, 0),
                (2, 2, 0, 100.0, 1.0, 0.0, 1), (3, 2, 3, 50.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_value(self):
        record_arrays_close(
            from_signals_both(size=[[0, 1, np.inf]], size_type='value').order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 1, 3, 1.25, 4.0, 0.0, 1),
                (2, 2, 0, 100.0, 1.0, 0.0, 0), (3, 2, 3, 200.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=[[0, 1, np.inf]], size_type='value').order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 1, 3, 1.0, 4.0, 0.0, 1),
                (2, 2, 0, 100.0, 1.0, 0.0, 0), (3, 2, 3, 100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=[[0, 1, np.inf]], size_type='value').order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 1), (1, 1, 3, 1.0, 4.0, 0.0, 0),
                (2, 2, 0, 100.0, 1.0, 0.0, 1), (3, 2, 3, 50.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_percent(self):
        with pytest.raises(Exception):
            _ = from_signals_both(size=0.5, size_type='percent')
        record_arrays_close(
            from_signals_both(size=0.5, size_type='percent', upon_opposite_entry='close').order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 0), (1, 0, 3, 50., 4., 0., 1), (2, 0, 4, 25., 5., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(size=0.5, size_type='percent', upon_opposite_entry='close',
                              accumulate=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 1.0, 0.0, 0), (1, 0, 1, 12.5, 2.0, 0.0, 0),
                (2, 0, 3, 62.5, 4.0, 0.0, 1), (3, 0, 4, 27.5, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=0.5, size_type='percent').order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 0), (1, 0, 3, 50., 4., 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=0.5, size_type='percent').order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 1), (1, 0, 3, 37.5, 4., 0., 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=price_wide, size=0.5, size_type='percent',
                group_by=np.array([0, 0, 0]), cash_sharing=True).order_records,
            np.array([
                (0, 0, 0, 50., 1., 0., 0), (1, 1, 0, 25., 1., 0., 0),
                (2, 2, 0, 12.5, 1., 0., 0), (3, 0, 3, 50., 4., 0., 1),
                (4, 1, 3, 25., 4., 0., 1), (5, 2, 3, 12.5, 4., 0., 1)
            ], dtype=order_dt)
        )

    def test_price(self):
        record_arrays_close(
            from_signals_both(price=price * 1.01).order_records,
            np.array([
                (0, 0, 0, 99.00990099009901, 1.01, 0.0, 0), (1, 0, 3, 198.01980198019803, 4.04, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(price=price * 1.01).order_records,
            np.array([
                (0, 0, 0, 99.00990099, 1.01, 0., 0), (1, 0, 3, 99.00990099, 4.04, 0., 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(price=price * 1.01).order_records,
            np.array([
                (0, 0, 0, 99.00990099009901, 1.01, 0.0, 1), (1, 0, 3, 49.504950495049506, 4.04, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(price=np.inf).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 200.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(price=np.inf).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(price=np.inf).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1), (1, 0, 3, 50.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(price=-np.inf).order_records,
            np.array([
                (0, 0, 1, 100.0, 1.0, 0.0, 0), (1, 0, 3, 200.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(price=-np.inf).order_records,
            np.array([
                (0, 0, 1, 100.0, 1.0, 0.0, 0), (1, 0, 3, 100.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(price=-np.inf).order_records,
            np.array([
                (0, 0, 1, 100.0, 1.0, 0.0, 1), (1, 0, 3, 66.66666666666667, 3.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_val_price(self):
        price_nan = pd.Series([1, 2, np.nan, 4, 5], index=price.index)
        record_arrays_close(
            from_signals_both(close=price_nan, size=1, val_price=np.inf,
                              size_type='value').order_records,
            from_signals_both(close=price_nan, size=1, val_price=price,
                              size_type='value').order_records
        )
        record_arrays_close(
            from_signals_longonly(close=price_nan, size=1, val_price=np.inf,
                                  size_type='value').order_records,
            from_signals_longonly(close=price_nan, size=1, val_price=price,
                                  size_type='value').order_records
        )
        record_arrays_close(
            from_signals_shortonly(close=price_nan, size=1, val_price=np.inf,
                                   size_type='value').order_records,
            from_signals_shortonly(close=price_nan, size=1, val_price=price,
                                   size_type='value').order_records
        )
        shift_price = price_nan.ffill().shift(1)
        record_arrays_close(
            from_signals_both(close=price_nan, size=1, val_price=-np.inf,
                              size_type='value').order_records,
            from_signals_both(close=price_nan, size=1, val_price=shift_price,
                              size_type='value').order_records
        )
        record_arrays_close(
            from_signals_longonly(close=price_nan, size=1, val_price=-np.inf,
                                  size_type='value').order_records,
            from_signals_longonly(close=price_nan, size=1, val_price=shift_price,
                                  size_type='value').order_records
        )
        record_arrays_close(
            from_signals_shortonly(close=price_nan, size=1, val_price=-np.inf,
                                   size_type='value').order_records,
            from_signals_shortonly(close=price_nan, size=1, val_price=shift_price,
                                   size_type='value').order_records
        )
        record_arrays_close(
            from_signals_both(close=price_nan, size=1, val_price=np.inf,
                              size_type='value', ffill_val_price=False).order_records,
            from_signals_both(close=price_nan, size=1, val_price=price_nan,
                              size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_signals_longonly(close=price_nan, size=1, val_price=np.inf,
                                  size_type='value', ffill_val_price=False).order_records,
            from_signals_longonly(close=price_nan, size=1, val_price=price_nan,
                                  size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_signals_shortonly(close=price_nan, size=1, val_price=np.inf,
                                   size_type='value', ffill_val_price=False).order_records,
            from_signals_shortonly(close=price_nan, size=1, val_price=price_nan,
                                   size_type='value', ffill_val_price=False).order_records
        )
        shift_price_nan = price_nan.shift(1)
        record_arrays_close(
            from_signals_both(close=price_nan, size=1, val_price=-np.inf,
                              size_type='value', ffill_val_price=False).order_records,
            from_signals_both(close=price_nan, size=1, val_price=shift_price_nan,
                              size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_signals_longonly(close=price_nan, size=1, val_price=-np.inf,
                                  size_type='value', ffill_val_price=False).order_records,
            from_signals_longonly(close=price_nan, size=1, val_price=shift_price_nan,
                                  size_type='value', ffill_val_price=False).order_records
        )
        record_arrays_close(
            from_signals_shortonly(close=price_nan, size=1, val_price=-np.inf,
                                   size_type='value', ffill_val_price=False).order_records,
            from_signals_shortonly(close=price_nan, size=1, val_price=shift_price_nan,
                                   size_type='value', ffill_val_price=False).order_records
        )

    def test_fees(self):
        record_arrays_close(
            from_signals_both(size=1, fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 3, 2.0, 4.0, -0.8, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 2.0, 4.0, 0.0, 1), (4, 2, 0, 1.0, 1.0, 0.1, 0), (5, 2, 3, 2.0, 4.0, 0.8, 1),
                (6, 3, 0, 1.0, 1.0, 1.0, 0), (7, 3, 3, 2.0, 4.0, 8.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1, fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 3, 1.0, 4.0, -0.4, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 1.0, 4.0, 0.0, 1), (4, 2, 0, 1.0, 1.0, 0.1, 0), (5, 2, 3, 1.0, 4.0, 0.4, 1),
                (6, 3, 0, 1.0, 1.0, 1.0, 0), (7, 3, 3, 1.0, 4.0, 4.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1, fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 1), (1, 0, 3, 1.0, 4.0, -0.4, 0), (2, 1, 0, 1.0, 1.0, 0.0, 1),
                (3, 1, 3, 1.0, 4.0, 0.0, 0), (4, 2, 0, 1.0, 1.0, 0.1, 1), (5, 2, 3, 1.0, 4.0, 0.4, 0),
                (6, 3, 0, 1.0, 1.0, 1.0, 1), (7, 3, 3, 1.0, 4.0, 4.0, 0)
            ], dtype=order_dt)
        )

    def test_fixed_fees(self):
        record_arrays_close(
            from_signals_both(size=1, fixed_fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 3, 2.0, 4.0, -0.1, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 2.0, 4.0, 0.0, 1), (4, 2, 0, 1.0, 1.0, 0.1, 0), (5, 2, 3, 2.0, 4.0, 0.1, 1),
                (6, 3, 0, 1.0, 1.0, 1.0, 0), (7, 3, 3, 2.0, 4.0, 1.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1, fixed_fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 0), (1, 0, 3, 1.0, 4.0, -0.1, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 1.0, 4.0, 0.0, 1), (4, 2, 0, 1.0, 1.0, 0.1, 0), (5, 2, 3, 1.0, 4.0, 0.1, 1),
                (6, 3, 0, 1.0, 1.0, 1.0, 0), (7, 3, 3, 1.0, 4.0, 1.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1, fixed_fees=[[-0.1, 0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, -0.1, 1), (1, 0, 3, 1.0, 4.0, -0.1, 0), (2, 1, 0, 1.0, 1.0, 0.0, 1),
                (3, 1, 3, 1.0, 4.0, 0.0, 0), (4, 2, 0, 1.0, 1.0, 0.1, 1), (5, 2, 3, 1.0, 4.0, 0.1, 0),
                (6, 3, 0, 1.0, 1.0, 1.0, 1), (7, 3, 3, 1.0, 4.0, 1.0, 0)
            ], dtype=order_dt)
        )

    def test_slippage(self):
        record_arrays_close(
            from_signals_both(size=1, slippage=[[0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 2.0, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.1, 0.0, 0),
                (3, 1, 3, 2.0, 3.6, 0.0, 1), (4, 2, 0, 1.0, 2.0, 0.0, 0), (5, 2, 3, 2.0, 0.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1, slippage=[[0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 1.0, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.1, 0.0, 0),
                (3, 1, 3, 1.0, 3.6, 0.0, 1), (4, 2, 0, 1.0, 2.0, 0.0, 0), (5, 2, 3, 1.0, 0.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1, slippage=[[0., 0.1, 1.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 3, 1.0, 4.0, 0.0, 0), (2, 1, 0, 1.0, 0.9, 0.0, 1),
                (3, 1, 3, 1.0, 4.4, 0.0, 0), (4, 2, 0, 1.0, 0.0, 0.0, 1), (5, 2, 3, 1.0, 8.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_min_size(self):
        record_arrays_close(
            from_signals_both(size=1, min_size=[[0., 1., 2.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 2.0, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 2.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1, min_size=[[0., 1., 2.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 1.0, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 1.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1, min_size=[[0., 1., 2.]]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 3, 1.0, 4.0, 0.0, 0), (2, 1, 0, 1.0, 1.0, 0.0, 1),
                (3, 1, 3, 1.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_max_size(self):
        record_arrays_close(
            from_signals_both(size=1, max_size=[[0.5, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 0.5, 1.0, 0.0, 0), (1, 0, 3, 0.5, 4.0, 0.0, 1), (2, 0, 4, 0.5, 5.0, 0.0, 1),
                (3, 1, 0, 1.0, 1.0, 0.0, 0), (4, 1, 3, 1.0, 4.0, 0.0, 1), (5, 1, 4, 1.0, 5.0, 0.0, 1),
                (6, 2, 0, 1.0, 1.0, 0.0, 0), (7, 2, 3, 2.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1, max_size=[[0.5, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 0.5, 1.0, 0.0, 0), (1, 0, 3, 0.5, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 3, 1.0, 4.0, 0.0, 1), (4, 2, 0, 1.0, 1.0, 0.0, 0), (5, 2, 3, 1.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1, max_size=[[0.5, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 0.5, 1.0, 0.0, 1), (1, 0, 3, 0.5, 4.0, 0.0, 0), (2, 1, 0, 1.0, 1.0, 0.0, 1),
                (3, 1, 3, 1.0, 4.0, 0.0, 0), (4, 2, 0, 1.0, 1.0, 0.0, 1), (5, 2, 3, 1.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_reject_prob(self):
        record_arrays_close(
            from_signals_both(size=1., reject_prob=[[0., 0.5, 1.]], seed=42).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 2.0, 4.0, 0.0, 1), (2, 1, 1, 1.0, 2.0, 0.0, 0),
                (3, 1, 3, 2.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1., reject_prob=[[0., 0.5, 1.]], seed=42).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 1.0, 4.0, 0.0, 1), (2, 1, 1, 1.0, 2.0, 0.0, 0),
                (3, 1, 3, 1.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1., reject_prob=[[0., 0.5, 1.]], seed=42).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 3, 1.0, 4.0, 0.0, 0), (2, 1, 1, 1.0, 2.0, 0.0, 1),
                (3, 1, 3, 1.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_allow_partial(self):
        record_arrays_close(
            from_signals_both(size=1000, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 1100.0, 4.0, 0.0, 1), (2, 1, 3, 1000.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1000, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1000, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 1000.0, 1.0, 0.0, 1), (1, 0, 3, 275.0, 4.0, 0.0, 0), (2, 1, 0, 1000.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(size=np.inf, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 200.0, 4.0, 0.0, 1), (2, 1, 0, 100.0, 1.0, 0.0, 0),
                (3, 1, 3, 200.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=np.inf, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 100.0, 4.0, 0.0, 1), (2, 1, 0, 100.0, 1.0, 0.0, 0),
                (3, 1, 3, 100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=np.inf, allow_partial=[[True, False]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1), (1, 0, 3, 50.0, 4.0, 0.0, 0), (2, 1, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_raise_reject(self):
        record_arrays_close(
            from_signals_both(size=1000, allow_partial=True, raise_reject=True).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 1100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1000, allow_partial=True, raise_reject=True).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 100.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        with pytest.raises(Exception):
            _ = from_signals_shortonly(size=1000, allow_partial=True, raise_reject=True).order_records
        with pytest.raises(Exception):
            _ = from_signals_both(size=1000, allow_partial=False, raise_reject=True).order_records
        with pytest.raises(Exception):
            _ = from_signals_longonly(size=1000, allow_partial=False, raise_reject=True).order_records
        with pytest.raises(Exception):
            _ = from_signals_shortonly(size=1000, allow_partial=False, raise_reject=True).order_records

    def test_log(self):
        record_arrays_close(
            from_signals_both(log=True).log_records,
            np.array([
                (0, 0, 0, 0, 100.0, 0.0, 0.0, 100.0, 1.0, 100.0, np.inf, 1.0, 0, 2, 0.0, 0.0,
                 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 0.0, 100.0, 0.0, 0.0, 1.0,
                 100.0, 100.0, 1.0, 0.0, 0, 0, -1, 0),
                (1, 0, 0, 3, 0.0, 100.0, 0.0, 0.0, 4.0, 400.0, -np.inf, 4.0, 0, 2, 0.0,
                 0.0, 0.0, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 800.0, -100.0,
                 400.0, 0.0, 4.0, 400.0, 200.0, 4.0, 0.0, 1, 0, -1, 1)
            ], dtype=log_dt)
        )

    def test_accumulate(self):
        record_arrays_close(
            from_signals_both(size=1, accumulate=[['disabled', 'addonly', 'removeonly', 'both']]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 2.0, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 1, 1.0, 2.0, 0.0, 0), (4, 1, 3, 3.0, 4.0, 0.0, 1), (5, 1, 4, 1.0, 5.0, 0.0, 1),
                (6, 2, 0, 1.0, 1.0, 0.0, 0), (7, 2, 3, 1.0, 4.0, 0.0, 1), (8, 2, 4, 1.0, 5.0, 0.0, 1),
                (9, 3, 0, 1.0, 1.0, 0.0, 0), (10, 3, 1, 1.0, 2.0, 0.0, 0), (11, 3, 3, 1.0, 4.0, 0.0, 1),
                (12, 3, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(size=1, accumulate=[['disabled', 'addonly', 'removeonly', 'both']]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 3, 1.0, 4.0, 0.0, 1), (2, 1, 0, 1.0, 1.0, 0.0, 0),
                (3, 1, 1, 1.0, 2.0, 0.0, 0), (4, 1, 3, 2.0, 4.0, 0.0, 1), (5, 2, 0, 1.0, 1.0, 0.0, 0),
                (6, 2, 3, 1.0, 4.0, 0.0, 1), (7, 3, 0, 1.0, 1.0, 0.0, 0), (8, 3, 1, 1.0, 2.0, 0.0, 0),
                (9, 3, 3, 1.0, 4.0, 0.0, 1), (10, 3, 4, 1.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(size=1, accumulate=[['disabled', 'addonly', 'removeonly', 'both']]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 3, 1.0, 4.0, 0.0, 0), (2, 1, 0, 1.0, 1.0, 0.0, 1),
                (3, 1, 1, 1.0, 2.0, 0.0, 1), (4, 1, 3, 2.0, 4.0, 0.0, 0), (5, 2, 0, 1.0, 1.0, 0.0, 1),
                (6, 2, 3, 1.0, 4.0, 0.0, 0), (7, 3, 0, 1.0, 1.0, 0.0, 1), (8, 3, 1, 1.0, 2.0, 0.0, 1),
                (9, 3, 3, 1.0, 4.0, 0.0, 0), (10, 3, 4, 1.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_upon_long_conflict(self):
        kwargs = dict(
            close=price[:3],
            entries=pd.DataFrame([
                [True, True, True, True, True, True, True],
                [True, True, True, True, False, True, False],
                [True, True, True, True, True, True, True]
            ]),
            exits=pd.DataFrame([
                [True, True, True, True, True, True, True],
                [False, False, False, False, True, False, True],
                [True, True, True, True, True, True, True]
            ]),
            size=1.,
            accumulate=True,
            upon_long_conflict=[[
                'ignore',
                'entry',
                'exit',
                'adjacent',
                'adjacent',
                'opposite',
                'opposite'
            ]]
        )
        record_arrays_close(
            from_signals_longonly(**kwargs).order_records,
            np.array([
                (0, 0, 1, 1.0, 2.0, 0.0, 0),
                (1, 1, 0, 1.0, 1.0, 0.0, 0), (2, 1, 1, 1.0, 2.0, 0.0, 0), (3, 1, 2, 1.0, 3.0, 0.0, 0),
                (4, 2, 1, 1.0, 2.0, 0.0, 0), (5, 2, 2, 1.0, 3.0, 0.0, 1),
                (6, 3, 1, 1.0, 2.0, 0.0, 0), (7, 3, 2, 1.0, 3.0, 0.0, 0),
                (8, 5, 1, 1.0, 2.0, 0.0, 0), (9, 5, 2, 1.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_upon_short_conflict(self):
        kwargs = dict(
            close=price[:3],
            entries=pd.DataFrame([
                [True, True, True, True, True, True, True],
                [True, True, True, True, False, True, False],
                [True, True, True, True, True, True, True]
            ]),
            exits=pd.DataFrame([
                [True, True, True, True, True, True, True],
                [False, False, False, False, True, False, True],
                [True, True, True, True, True, True, True]
            ]),
            size=1.,
            accumulate=True,
            upon_short_conflict=[[
                'ignore',
                'entry',
                'exit',
                'adjacent',
                'adjacent',
                'opposite',
                'opposite'
            ]]
        )
        record_arrays_close(
            from_signals_shortonly(**kwargs).order_records,
            np.array([
                (0, 0, 1, 1.0, 2.0, 0.0, 1),
                (1, 1, 0, 1.0, 1.0, 0.0, 1), (2, 1, 1, 1.0, 2.0, 0.0, 1), (3, 1, 2, 1.0, 3.0, 0.0, 1),
                (4, 2, 1, 1.0, 2.0, 0.0, 1), (5, 2, 2, 1.0, 3.0, 0.0, 0),
                (6, 3, 1, 1.0, 2.0, 0.0, 1), (7, 3, 2, 1.0, 3.0, 0.0, 1),
                (8, 5, 1, 1.0, 2.0, 0.0, 1), (9, 5, 2, 1.0, 3.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_upon_dir_conflict(self):
        kwargs = dict(
            close=price[:3],
            entries=pd.DataFrame([
                [True, True, True, True, True, True, True],
                [True, True, True, True, False, True, False],
                [True, True, True, True, True, True, True]
            ]),
            exits=pd.DataFrame([
                [True, True, True, True, True, True, True],
                [False, False, False, False, True, False, True],
                [True, True, True, True, True, True, True]
            ]),
            size=1.,
            accumulate=True,
            upon_dir_conflict=[[
                'ignore',
                'long',
                'short',
                'adjacent',
                'adjacent',
                'opposite',
                'opposite'
            ]]
        )
        record_arrays_close(
            from_signals_both(**kwargs).order_records,
            np.array([
                (0, 0, 1, 1.0, 2.0, 0.0, 0),
                (1, 1, 0, 1.0, 1.0, 0.0, 0), (2, 1, 1, 1.0, 2.0, 0.0, 0), (3, 1, 2, 1.0, 3.0, 0.0, 0),
                (4, 2, 0, 1.0, 1.0, 0.0, 1), (5, 2, 1, 1.0, 2.0, 0.0, 0), (6, 2, 2, 1.0, 3.0, 0.0, 1),
                (7, 3, 1, 1.0, 2.0, 0.0, 0), (8, 3, 2, 1.0, 3.0, 0.0, 0),
                (9, 4, 1, 1.0, 2.0, 0.0, 1), (10, 4, 2, 1.0, 3.0, 0.0, 1),
                (11, 5, 1, 1.0, 2.0, 0.0, 0), (12, 5, 2, 1.0, 3.0, 0.0, 1),
                (13, 6, 1, 1.0, 2.0, 0.0, 1), (14, 6, 2, 1.0, 3.0, 0.0, 0)
            ], dtype=order_dt)
        )

    def test_upon_opposite_entry(self):
        kwargs = dict(
            close=price[:3],
            entries=pd.DataFrame([
                [True, False, True, False, True, False, True, False, True, False],
                [False, True, False, True, False, True, False, True, False, True],
                [True, False, True, False, True, False, True, False, True, False]
            ]),
            exits=pd.DataFrame([
                [False, True, False, True, False, True, False, True, False, True],
                [True, False, True, False, True, False, True, False, True, False],
                [False, True, False, True, False, True, False, True, False, True]
            ]),
            size=1.,
            upon_opposite_entry=[[
                'ignore',
                'ignore',
                'close',
                'close',
                'closereduce',
                'closereduce',
                'reverse',
                'reverse',
                'reversereduce',
                'reversereduce'
            ]]
        )
        record_arrays_close(
            from_signals_both(**kwargs).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0),
                (1, 1, 0, 1.0, 1.0, 0.0, 1),
                (2, 2, 0, 1.0, 1.0, 0.0, 0), (3, 2, 1, 1.0, 2.0, 0.0, 1), (4, 2, 2, 1.0, 3.0, 0.0, 0),
                (5, 3, 0, 1.0, 1.0, 0.0, 1), (6, 3, 1, 1.0, 2.0, 0.0, 0), (7, 3, 2, 1.0, 3.0, 0.0, 1),
                (8, 4, 0, 1.0, 1.0, 0.0, 0), (9, 4, 1, 1.0, 2.0, 0.0, 1), (10, 4, 2, 1.0, 3.0, 0.0, 0),
                (11, 5, 0, 1.0, 1.0, 0.0, 1), (12, 5, 1, 1.0, 2.0, 0.0, 0), (13, 5, 2, 1.0, 3.0, 0.0, 1),
                (14, 6, 0, 1.0, 1.0, 0.0, 0), (15, 6, 1, 2.0, 2.0, 0.0, 1), (16, 6, 2, 2.0, 3.0, 0.0, 0),
                (17, 7, 0, 1.0, 1.0, 0.0, 1), (18, 7, 1, 2.0, 2.0, 0.0, 0), (19, 7, 2, 2.0, 3.0, 0.0, 1),
                (20, 8, 0, 1.0, 1.0, 0.0, 0), (21, 8, 1, 2.0, 2.0, 0.0, 1), (22, 8, 2, 2.0, 3.0, 0.0, 0),
                (23, 9, 0, 1.0, 1.0, 0.0, 1), (24, 9, 1, 2.0, 2.0, 0.0, 0), (25, 9, 2, 2.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(**kwargs, accumulate=True).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 2, 1.0, 3.0, 0.0, 0),
                (2, 1, 0, 1.0, 1.0, 0.0, 1), (3, 1, 2, 1.0, 3.0, 0.0, 1),
                (4, 2, 0, 1.0, 1.0, 0.0, 0), (5, 2, 1, 1.0, 2.0, 0.0, 1), (6, 2, 2, 1.0, 3.0, 0.0, 0),
                (7, 3, 0, 1.0, 1.0, 0.0, 1), (8, 3, 1, 1.0, 2.0, 0.0, 0), (9, 3, 2, 1.0, 3.0, 0.0, 1),
                (10, 4, 0, 1.0, 1.0, 0.0, 0), (11, 4, 1, 1.0, 2.0, 0.0, 1), (12, 4, 2, 1.0, 3.0, 0.0, 0),
                (13, 5, 0, 1.0, 1.0, 0.0, 1), (14, 5, 1, 1.0, 2.0, 0.0, 0), (15, 5, 2, 1.0, 3.0, 0.0, 1),
                (16, 6, 0, 1.0, 1.0, 0.0, 0), (17, 6, 1, 2.0, 2.0, 0.0, 1), (18, 6, 2, 2.0, 3.0, 0.0, 0),
                (19, 7, 0, 1.0, 1.0, 0.0, 1), (20, 7, 1, 2.0, 2.0, 0.0, 0), (21, 7, 2, 2.0, 3.0, 0.0, 1),
                (22, 8, 0, 1.0, 1.0, 0.0, 0), (23, 8, 1, 1.0, 2.0, 0.0, 1), (24, 8, 2, 1.0, 3.0, 0.0, 0),
                (25, 9, 0, 1.0, 1.0, 0.0, 1), (26, 9, 1, 1.0, 2.0, 0.0, 0), (27, 9, 2, 1.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_init_cash(self):
        record_arrays_close(
            from_signals_both(close=price_wide, size=1., init_cash=[0., 1., 100.]).order_records,
            np.array([
                (0, 0, 3, 1.0, 4.0, 0.0, 1), (1, 1, 0, 1.0, 1.0, 0.0, 0), (2, 1, 3, 2.0, 4.0, 0.0, 1),
                (3, 2, 0, 1.0, 1.0, 0.0, 0), (4, 2, 3, 2.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(close=price_wide, size=1., init_cash=[0., 1., 100.]).order_records,
            np.array([
                (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 1, 3, 1.0, 4.0, 0.0, 1), (2, 2, 0, 1.0, 1.0, 0.0, 0),
                (3, 2, 3, 1.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(close=price_wide, size=1., init_cash=[0., 1., 100.]).order_records,
            np.array([
                (0, 0, 0, 1.0, 1.0, 0.0, 1), (1, 0, 3, 0.25, 4.0, 0.0, 0), (2, 1, 0, 1.0, 1.0, 0.0, 1),
                (3, 1, 3, 0.5, 4.0, 0.0, 0), (4, 2, 0, 1.0, 1.0, 0.0, 1), (5, 2, 3, 1.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        with pytest.raises(Exception):
            _ = from_signals_both(init_cash=np.inf).order_records
        with pytest.raises(Exception):
            _ = from_signals_longonly(init_cash=np.inf).order_records
        with pytest.raises(Exception):
            _ = from_signals_shortonly(init_cash=np.inf).order_records

    def test_group_by(self):
        pf = from_signals_both(close=price_wide, group_by=np.array([0, 0, 1]))
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 3, 200.0, 4.0, 0.0, 1), (2, 1, 0, 100.0, 1.0, 0.0, 0),
                (3, 1, 3, 200.0, 4.0, 0.0, 1), (4, 2, 0, 100.0, 1.0, 0.0, 0), (5, 2, 3, 200.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        pd.testing.assert_index_equal(
            pf.wrapper.grouper.group_by,
            pd.Index([0, 0, 1], dtype='int64')
        )
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series([200., 100.], index=pd.Index([0, 1], dtype='int64')).rename('init_cash')
        )
        assert not pf.cash_sharing

    def test_cash_sharing(self):
        pf = from_signals_both(close=price_wide, group_by=np.array([0, 0, 1]), cash_sharing=True)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 3, 200., 4., 0., 1),
                (2, 2, 0, 100., 1., 0., 0), (3, 2, 3, 200., 4., 0., 1)
            ], dtype=order_dt)
        )
        pd.testing.assert_index_equal(
            pf.wrapper.grouper.group_by,
            pd.Index([0, 0, 1], dtype='int64')
        )
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series([100., 100.], index=pd.Index([0, 1], dtype='int64')).rename('init_cash')
        )
        assert pf.cash_sharing
        with pytest.raises(Exception):
            _ = pf.regroup(group_by=False)

    def test_call_seq(self):
        pf = from_signals_both(close=price_wide, group_by=np.array([0, 0, 1]), cash_sharing=True)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100., 1., 0., 0), (1, 0, 3, 200., 4., 0., 1),
                (2, 2, 0, 100., 1., 0., 0), (3, 2, 3, 200., 4., 0., 1)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ])
        )
        pf = from_signals_both(
            close=price_wide, group_by=np.array([0, 0, 1]),
            cash_sharing=True, call_seq='reversed')
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 1, 0, 100., 1., 0., 0), (1, 1, 3, 200., 4., 0., 1),
                (2, 2, 0, 100., 1., 0., 0), (3, 2, 3, 200., 4., 0., 1)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0]
            ])
        )
        pf = from_signals_both(
            close=price_wide, group_by=np.array([0, 0, 1]),
            cash_sharing=True, call_seq='random', seed=seed)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 1, 0, 100., 1., 0., 0), (1, 1, 3, 200., 4., 0., 1),
                (2, 2, 0, 100., 1., 0., 0), (3, 2, 3, 200., 4., 0., 1)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [1, 0, 0],
                [0, 1, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0]
            ])
        )
        kwargs = dict(
            close=1.,
            entries=pd.DataFrame([
                [False, False, True],
                [False, True, False],
                [True, False, False],
                [False, False, True],
                [False, True, False],
            ]),
            exits=pd.DataFrame([
                [False, False, False],
                [False, False, True],
                [False, True, False],
                [True, False, False],
                [False, False, True],
            ]),
            group_by=np.array([0, 0, 0]),
            cash_sharing=True,
            call_seq='auto'
        )
        pf = from_signals_both(**kwargs)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100., 1., 0., 0), (1, 2, 1, 200., 1., 0., 1),
                (2, 1, 1, 200., 1., 0., 0), (3, 1, 2, 200., 1., 0., 1),
                (4, 0, 2, 200., 1., 0., 0), (5, 0, 3, 200., 1., 0., 1),
                (6, 2, 3, 200., 1., 0., 0), (7, 2, 4, 200., 1., 0., 1),
                (8, 1, 4, 200., 1., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 2],
                [2, 0, 1],
                [1, 2, 0],
                [0, 1, 2],
                [2, 0, 1]
            ])
        )
        pf = from_signals_longonly(**kwargs)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100., 1., 0., 0), (1, 2, 1, 100., 1., 0., 1),
                (2, 1, 1, 100., 1., 0., 0), (3, 1, 2, 100., 1., 0., 1),
                (4, 0, 2, 100., 1., 0., 0), (5, 0, 3, 100., 1., 0., 1),
                (6, 2, 3, 100., 1., 0., 0), (7, 2, 4, 100., 1., 0., 1),
                (8, 1, 4, 100., 1., 0., 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 2],
                [2, 0, 1],
                [1, 2, 0],
                [0, 1, 2],
                [2, 0, 1]
            ])
        )
        pf = from_signals_shortonly(**kwargs)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100., 1., 0., 1), (1, 2, 1, 100., 1., 0., 0),
                (2, 0, 2, 100., 1., 0., 1), (3, 0, 3, 100., 1., 0., 0),
                (4, 1, 4, 100., 1., 0., 1)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [2, 0, 1],
                [1, 0, 2],
                [0, 1, 2],
                [2, 1, 0],
                [1, 0, 2]
            ])
        )
        pf = from_signals_longonly(**kwargs, size=1., size_type='percent')
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 2, 0, 100.0, 1.0, 0.0, 0), (1, 2, 1, 100.0, 1.0, 0.0, 1), (2, 1, 1, 100.0, 1.0, 0.0, 0),
                (3, 1, 2, 100.0, 1.0, 0.0, 1), (4, 0, 2, 100.0, 1.0, 0.0, 0), (5, 0, 3, 100.0, 1.0, 0.0, 1),
                (6, 2, 3, 100.0, 1.0, 0.0, 0), (7, 2, 4, 100.0, 1.0, 0.0, 1), (8, 1, 4, 100.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 2],
                [2, 0, 1],
                [1, 0, 2],
                [0, 1, 2],
                [2, 0, 1]
            ])
        )

    def test_sl_stop(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)

        with pytest.raises(Exception):
            _ = from_signals_both(sl_stop=-0.1)

        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)
        open = close + 0.25
        high = close + 0.5
        low = close - 0.5
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 0),
                (1, 1, 0, 20.0, 5.0, 0.0, 0), (2, 1, 1, 20.0, 4.0, 0.0, 1),
                (3, 2, 0, 20.0, 5.0, 0.0, 0), (4, 2, 3, 20.0, 2.0, 0.0, 1),
                (5, 3, 0, 20.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 1),
                (1, 1, 0, 20.0, 5.0, 0.0, 1),
                (2, 2, 0, 20.0, 5.0, 0.0, 1),
                (3, 3, 0, 20.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=exits, exits=entries,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.1, 0.15, 0.2, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 0),
                (1, 1, 0, 20.0, 5.0, 0.0, 0), (2, 1, 1, 20.0, 4.25, 0.0, 1),
                (3, 2, 0, 20.0, 5.0, 0.0, 0), (4, 2, 1, 20.0, 4.25, 0.0, 1),
                (5, 3, 0, 20.0, 5.0, 0.0, 0), (6, 3, 1, 20.0, 4.0, 0.0, 1),
                (7, 4, 0, 20.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.1, 0.15, 0.2, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 1),
                (1, 1, 0, 20.0, 5.0, 0.0, 1),
                (2, 2, 0, 20.0, 5.0, 0.0, 1),
                (3, 3, 0, 20.0, 5.0, 0.0, 1),
                (4, 4, 0, 20.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )

        close = pd.Series([1., 2., 3., 4., 5.], index=price.index)
        open = close - 0.25
        high = close + 0.5
        low = close - 0.5
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0),
                (1, 1, 0, 100.0, 1.0, 0.0, 0),
                (2, 2, 0, 100.0, 1.0, 0.0, 0),
                (3, 3, 0, 100.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1),
                (1, 1, 0, 100.0, 1.0, 0.0, 1), (2, 1, 1, 100.0, 2.0, 0.0, 0),
                (3, 2, 0, 100.0, 1.0, 0.0, 1), (4, 2, 3, 50.0, 4.0, 0.0, 0),
                (5, 3, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=exits, exits=entries,
                sl_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.5, 0.75, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0),
                (1, 1, 0, 100.0, 1.0, 0.0, 0),
                (2, 2, 0, 100.0, 1.0, 0.0, 0),
                (3, 3, 0, 100.0, 1.0, 0.0, 0),
                (4, 4, 0, 100.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.5, 0.75, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1),
                (1, 1, 0, 100.0, 1.0, 0.0, 1), (2, 1, 1, 100.0, 1.75, 0.0, 0),
                (3, 2, 0, 100.0, 1.0, 0.0, 1), (4, 2, 1, 100.0, 1.75, 0.0, 0),
                (5, 3, 0, 100.0, 1.0, 0.0, 1), (6, 3, 1, 100.0, 2.0, 0.0, 0),
                (7, 4, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_ts_stop(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)

        with pytest.raises(Exception):
            _ = from_signals_both(ts_stop=-0.1)

        close = pd.Series([4., 5., 4., 3., 2.], index=price.index)
        open = close + 0.25
        high = close + 0.5
        low = close - 0.5
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 25.0, 4.0, 0.0, 0),
                (1, 1, 0, 25.0, 4.0, 0.0, 0), (2, 1, 2, 25.0, 4.0, 0.0, 1),
                (3, 2, 0, 25.0, 4.0, 0.0, 0), (4, 2, 4, 25.0, 2.0, 0.0, 1),
                (5, 3, 0, 25.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 25.0, 4.0, 0.0, 1),
                (1, 1, 0, 25.0, 4.0, 0.0, 1), (2, 1, 1, 25.0, 5.0, 0.0, 0),
                (3, 2, 0, 25.0, 4.0, 0.0, 1),
                (4, 3, 0, 25.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]], sl_trail=True).order_records,
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]], sl_trail=True).order_records
        )
        print('here')
        record_arrays_close(
            from_signals_both(
                close=close, entries=exits, exits=entries,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]], sl_trail=True).order_records,
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.1, 0.5, np.inf]], sl_trail=True).order_records
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.15, 0.2, 0.25, np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 25.0, 4.0, 0.0, 0),
                (1, 1, 0, 25.0, 4.0, 0.0, 0), (2, 1, 2, 25.0, 4.25, 0.0, 1),
                (3, 2, 0, 25.0, 4.0, 0.0, 0), (4, 2, 2, 25.0, 4.25, 0.0, 1),
                (5, 3, 0, 25.0, 4.0, 0.0, 0), (6, 3, 2, 25.0, 4.125, 0.0, 1),
                (7, 4, 0, 25.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.15, 0.2, 0.25, np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 25.0, 4.0, 0.0, 1),
                (1, 1, 0, 25.0, 4.0, 0.0, 1), (2, 1, 1, 25.0, 5.25, 0.0, 0),
                (3, 2, 0, 25.0, 4.0, 0.0, 1), (4, 2, 1, 25.0, 5.25, 0.0, 0),
                (5, 3, 0, 25.0, 4.0, 0.0, 1), (6, 3, 1, 25.0, 5.25, 0.0, 0),
                (7, 4, 0, 25.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )

        close = pd.Series([2., 1., 2., 3., 4.], index=price.index)
        open = close - 0.25
        high = close + 0.5
        low = close - 0.5
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 2.0, 0.0, 0),
                (1, 1, 0, 50.0, 2.0, 0.0, 0), (2, 1, 1, 50.0, 1.0, 0.0, 1),
                (3, 2, 0, 50.0, 2.0, 0.0, 0),
                (4, 3, 0, 50.0, 2.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 2.0, 0.0, 1),
                (1, 1, 0, 50.0, 2.0, 0.0, 1), (2, 1, 2, 50.0, 2.0, 0.0, 0),
                (3, 2, 0, 50.0, 2.0, 0.0, 1), (4, 2, 4, 50.0, 4.0, 0.0, 0),
                (5, 3, 0, 50.0, 2.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]], sl_trail=True).order_records,
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]], sl_trail=True).order_records
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=exits, exits=entries,
                sl_stop=[[np.nan, 0.5, 3., np.inf]], sl_trail=True).order_records,
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                sl_stop=[[np.nan, 0.5, 3., np.inf]], sl_trail=True).order_records
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.5, 0.75, 1., np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 2.0, 0.0, 0),
                (1, 1, 0, 50.0, 2.0, 0.0, 0), (2, 1, 1, 50.0, 0.75, 0.0, 1),
                (3, 2, 0, 50.0, 2.0, 0.0, 0), (4, 2, 1, 50.0, 0.5, 0.0, 1),
                (5, 3, 0, 50.0, 2.0, 0.0, 0),
                (6, 4, 0, 50.0, 2.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[np.nan, 0.5, 0.75, 1., np.inf]], sl_trail=True).order_records,
            np.array([
                (0, 0, 0, 50.0, 2.0, 0.0, 1),
                (1, 1, 0, 50.0, 2.0, 0.0, 1), (2, 1, 2, 50.0, 1.75, 0.0, 0),
                (3, 2, 0, 50.0, 2.0, 0.0, 1), (4, 2, 2, 50.0, 1.75, 0.0, 0),
                (5, 3, 0, 50.0, 2.0, 0.0, 1), (6, 3, 2, 50.0, 1.75, 0.0, 0),
                (7, 4, 0, 50.0, 2.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_tp_stop(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)

        with pytest.raises(Exception):
            _ = from_signals_both(sl_stop=-0.1)

        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)
        open = close + 0.25
        high = close + 0.5
        low = close - 0.5
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 0),
                (1, 1, 0, 20.0, 5.0, 0.0, 0),
                (2, 2, 0, 20.0, 5.0, 0.0, 0),
                (3, 3, 0, 20.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 1),
                (1, 1, 0, 20.0, 5.0, 0.0, 1), (2, 1, 1, 20.0, 4.0, 0.0, 0),
                (3, 2, 0, 20.0, 5.0, 0.0, 1), (4, 2, 3, 20.0, 2.0, 0.0, 0),
                (5, 3, 0, 20.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=exits, exits=entries,
                tp_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records,
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.1, 0.5, np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                tp_stop=[[np.nan, 0.1, 0.15, 0.2, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 0),
                (1, 1, 0, 20.0, 5.0, 0.0, 0),
                (2, 2, 0, 20.0, 5.0, 0.0, 0),
                (3, 3, 0, 20.0, 5.0, 0.0, 0),
                (4, 4, 0, 20.0, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                tp_stop=[[np.nan, 0.1, 0.15, 0.2, np.inf]]).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 1),
                (1, 1, 0, 20.0, 5.0, 0.0, 1), (2, 1, 1, 20.0, 4.25, 0.0, 0),
                (3, 2, 0, 20.0, 5.0, 0.0, 1), (4, 2, 1, 20.0, 4.25, 0.0, 0),
                (5, 3, 0, 20.0, 5.0, 0.0, 1), (6, 3, 1, 20.0, 4.0, 0.0, 0),
                (7, 4, 0, 20.0, 5.0, 0.0, 1)
            ], dtype=order_dt)
        )

        close = pd.Series([1., 2., 3., 4., 5.], index=price.index)
        open = close - 0.25
        high = close + 0.5
        low = close - 0.5
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0),
                (1, 1, 0, 100.0, 1.0, 0.0, 0), (2, 1, 1, 100.0, 2.0, 0.0, 1),
                (3, 2, 0, 100.0, 1.0, 0.0, 0), (4, 2, 3, 100.0, 4.0, 0.0, 1),
                (5, 3, 0, 100.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1),
                (1, 1, 0, 100.0, 1.0, 0.0, 1),
                (2, 2, 0, 100.0, 1.0, 0.0, 1),
                (3, 3, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.5, 3., np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=exits, exits=entries,
                tp_stop=[[np.nan, 0.5, 3., np.inf]]).order_records,
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                tp_stop=[[np.nan, 0.5, 3., np.inf]]).order_records
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                tp_stop=[[np.nan, 0.5, 0.75, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0),
                (1, 1, 0, 100.0, 1.0, 0.0, 0), (2, 1, 1, 100.0, 1.75, 0.0, 1),
                (3, 2, 0, 100.0, 1.0, 0.0, 0), (4, 2, 1, 100.0, 1.75, 0.0, 1),
                (5, 3, 0, 100.0, 1.0, 0.0, 0), (6, 3, 1, 100.0, 2.0, 0.0, 1),
                (7, 4, 0, 100.0, 1.0, 0.0, 0)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_shortonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                tp_stop=[[np.nan, 0.5, 0.75, 1., np.inf]]).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 1),
                (1, 1, 0, 100.0, 1.0, 0.0, 1),
                (2, 2, 0, 100.0, 1.0, 0.0, 1),
                (3, 3, 0, 100.0, 1.0, 0.0, 1),
                (4, 4, 0, 100.0, 1.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_stop_entry_price(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)
        open = close + 0.25
        high = close + 0.5
        low = close - 0.5

        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close, val_price=1.05 * close,
                stop_entry_price='val_price',
                stop_exit_price='stoplimit', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (1, 0, 1, 16.52892561983471, 4.25, 0.0, 1),
                (2, 1, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (3, 1, 2, 16.52892561983471, 2.625, 0.0, 1),
                (4, 2, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (5, 2, 4, 16.52892561983471, 1.25, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close, val_price=1.05 * close,
                stop_entry_price='price',
                stop_exit_price='stoplimit', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (1, 0, 1, 16.52892561983471, 4.25, 0.0, 1),
                (2, 1, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (3, 1, 2, 16.52892561983471, 2.75, 0.0, 1),
                (4, 2, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (5, 2, 4, 16.52892561983471, 1.25, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close, val_price=1.05 * close,
                stop_entry_price='fillprice',
                stop_exit_price='stoplimit', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (1, 0, 1, 16.52892561983471, 4.25, 0.0, 1),
                (2, 1, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (3, 1, 2, 16.52892561983471, 3.0250000000000004, 0.0, 1),
                (4, 2, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (5, 2, 3, 16.52892561983471, 1.5125000000000002, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close, val_price=1.05 * close,
                stop_entry_price='close',
                stop_exit_price='stoplimit', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (1, 0, 1, 16.52892561983471, 4.25, 0.0, 1),
                (2, 1, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (3, 1, 2, 16.52892561983471, 2.5, 0.0, 1),
                (4, 2, 0, 16.52892561983471, 6.050000000000001, 0.0, 0),
                (5, 2, 4, 16.52892561983471, 1.25, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_stop_exit_price(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)
        open = close + 0.25
        high = close + 0.5
        low = close - 0.5

        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close,
                stop_exit_price='stoplimit', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.528926, 6.05, 0.0, 0), (1, 0, 1, 16.528926, 4.25, 0.0, 1),
                (2, 1, 0, 16.528926, 6.05, 0.0, 0), (3, 1, 2, 16.528926, 2.5, 0.0, 1),
                (4, 2, 0, 16.528926, 6.05, 0.0, 0), (5, 2, 4, 16.528926, 1.25, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close,
                stop_exit_price='stopmarket', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.528926, 6.05, 0.0, 0), (1, 0, 1, 16.528926, 3.825, 0.0, 1),
                (2, 1, 0, 16.528926, 6.05, 0.0, 0), (3, 1, 2, 16.528926, 2.25, 0.0, 1),
                (4, 2, 0, 16.528926, 6.05, 0.0, 0), (5, 2, 4, 16.528926, 1.125, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close,
                stop_exit_price='close', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.528926, 6.05, 0.0, 0), (1, 0, 1, 16.528926, 3.6, 0.0, 1),
                (2, 1, 0, 16.528926, 6.05, 0.0, 0), (3, 1, 2, 16.528926, 2.7, 0.0, 1),
                (4, 2, 0, 16.528926, 6.05, 0.0, 0), (5, 2, 4, 16.528926, 0.9, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                open=open, high=high, low=low,
                sl_stop=[[0.05, 0.5, 0.75]], price=1.1 * close,
                stop_exit_price='price', slippage=0.1).order_records,
            np.array([
                (0, 0, 0, 16.528926, 6.05, 0.0, 0), (1, 0, 1, 16.528926, 3.9600000000000004, 0.0, 1),
                (2, 1, 0, 16.528926, 6.05, 0.0, 0), (3, 1, 2, 16.528926, 2.97, 0.0, 1),
                (4, 2, 0, 16.528926, 6.05, 0.0, 0), (5, 2, 4, 16.528926, 0.9900000000000001, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_upon_stop_exit(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits, size=1,
                sl_stop=0.1, upon_stop_exit=[['close', 'closereduce', 'reverse', 'reversereduce']],
                accumulate=True).order_records,
            np.array([
                (0, 0, 0, 1.0, 5.0, 0.0, 0), (1, 0, 1, 1.0, 4.0, 0.0, 1),
                (2, 1, 0, 1.0, 5.0, 0.0, 0), (3, 1, 1, 1.0, 4.0, 0.0, 1),
                (4, 2, 0, 1.0, 5.0, 0.0, 0), (5, 2, 1, 2.0, 4.0, 0.0, 1),
                (6, 3, 0, 1.0, 5.0, 0.0, 0), (7, 3, 1, 1.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )
        record_arrays_close(
            from_signals_both(
                close=close, entries=entries, exits=exits, size=1,
                sl_stop=0.1, upon_stop_exit=[['close', 'closereduce', 'reverse', 'reversereduce']]).order_records,
            np.array([
                (0, 0, 0, 1.0, 5.0, 0.0, 0), (1, 0, 1, 1.0, 4.0, 0.0, 1),
                (2, 1, 0, 1.0, 5.0, 0.0, 0), (3, 1, 1, 1.0, 4.0, 0.0, 1),
                (4, 2, 0, 1.0, 5.0, 0.0, 0), (5, 2, 1, 2.0, 4.0, 0.0, 1),
                (6, 3, 0, 1.0, 5.0, 0.0, 0), (7, 3, 1, 2.0, 4.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_upon_stop_update(self):
        entries = pd.Series([True, True, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)
        sl_stop = pd.Series([0.4, np.nan, np.nan, np.nan, np.nan])
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits, accumulate=True, size=1.,
                sl_stop=sl_stop, upon_stop_update=[['keep', 'override', 'overridenan']]).order_records,
            np.array([
                (0, 0, 0, 1.0, 5.0, 0.0, 0), (1, 0, 1, 1.0, 4.0, 0.0, 0), (2, 0, 2, 2.0, 3.0, 0.0, 1),
                (3, 1, 0, 1.0, 5.0, 0.0, 0), (4, 1, 1, 1.0, 4.0, 0.0, 0), (5, 1, 2, 2.0, 3.0, 0.0, 1),
                (6, 2, 0, 1.0, 5.0, 0.0, 0), (7, 2, 1, 1.0, 4.0, 0.0, 0)
            ], dtype=order_dt)
        )
        sl_stop = pd.Series([0.4, 0.4, np.nan, np.nan, np.nan])
        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits, accumulate=True, size=1.,
                sl_stop=sl_stop, upon_stop_update=[['keep', 'override']]).order_records,
            np.array([
                (0, 0, 0, 1.0, 5.0, 0.0, 0), (1, 0, 1, 1.0, 4.0, 0.0, 0), (2, 0, 2, 2.0, 3.0, 0.0, 1),
                (3, 1, 0, 1.0, 5.0, 0.0, 0), (4, 1, 1, 1.0, 4.0, 0.0, 0), (5, 1, 3, 2.0, 2.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_adjust_sl_func(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([5., 4., 3., 2., 1.], index=price.index)

        @njit
        def adjust_sl_func_nb(c, dur):
            return 0. if c.i - c.init_i >= dur else c.curr_stop, c.curr_trail

        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=np.inf, adjust_sl_func_nb=adjust_sl_func_nb, adjust_sl_args=(2,)).order_records,
            np.array([
                (0, 0, 0, 20.0, 5.0, 0.0, 0), (1, 0, 2, 20.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_adjust_ts_func(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([10., 11., 12., 11., 10.], index=price.index)

        @njit
        def adjust_sl_func_nb(c, dur):
            return 0. if c.i - c.curr_i >= dur else c.curr_stop, c.curr_trail

        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                sl_stop=np.inf, adjust_sl_func_nb=adjust_sl_func_nb, adjust_sl_args=(2,)).order_records,
            np.array([
                (0, 0, 0, 10.0, 10.0, 0.0, 0), (1, 0, 4, 10.0, 10.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_adjust_tp_func(self):
        entries = pd.Series([True, False, False, False, False], index=price.index)
        exits = pd.Series([False, False, False, False, False], index=price.index)
        close = pd.Series([1., 2., 3., 4., 5.], index=price.index)

        @njit
        def adjust_tp_func_nb(c, dur):
            return 0. if c.i - c.init_i >= dur else c.curr_stop

        record_arrays_close(
            from_signals_longonly(
                close=close, entries=entries, exits=exits,
                tp_stop=np.inf, adjust_tp_func_nb=adjust_tp_func_nb, adjust_tp_args=(2,)).order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 2, 100.0, 3.0, 0.0, 1)
            ], dtype=order_dt)
        )

    def test_max_orders(self):
        _ = from_signals_both(close=price_wide)
        _ = from_signals_both(close=price_wide, max_orders=6)
        with pytest.raises(Exception):
            _ = from_signals_both(close=price_wide, max_orders=5)

    def test_max_logs(self):
        _ = from_signals_both(close=price_wide, log=True)
        _ = from_signals_both(close=price_wide, log=True, max_logs=6)
        with pytest.raises(Exception):
            _ = from_signals_both(close=price_wide, log=True, max_logs=5)


# ############# from_holding ############# #

class TestFromHolding:
    def test_from_holding(self):
        record_arrays_close(
            vbt.Portfolio.from_holding(price).order_records,
            vbt.Portfolio.from_signals(price, True, False, accumulate=False).order_records
        )


# ############# from_random_signals ############# #

class TestFromRandomSignals:
    def test_from_random_n(self):
        result = vbt.Portfolio.from_random_signals(price, n=2, seed=seed)
        record_arrays_close(
            result.order_records,
            vbt.Portfolio.from_signals(
                price,
                [True, False, True, False, False],
                [False, True, False, False, True]
            ).order_records
        )
        pd.testing.assert_index_equal(
            result.wrapper.index,
            price.vbt.wrapper.index
        )
        pd.testing.assert_index_equal(
            result.wrapper.columns,
            price.vbt.wrapper.columns
        )
        result = vbt.Portfolio.from_random_signals(price, n=[1, 2], seed=seed)
        record_arrays_close(
            result.order_records,
            vbt.Portfolio.from_signals(
                price,
                [[False, True], [True, False], [False, True], [False, False], [False, False]],
                [[False, False], [False, True], [False, False], [False, True], [True, False]]
            ).order_records
        )
        pd.testing.assert_index_equal(
            result.wrapper.index,
            pd.DatetimeIndex([
                '2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'
            ], dtype='datetime64[ns]', freq=None)
        )
        pd.testing.assert_index_equal(
            result.wrapper.columns,
            pd.Index([1, 2], dtype='int64', name='randnx_n')
        )

    def test_from_random_prob(self):
        result = vbt.Portfolio.from_random_signals(price, prob=0.5, seed=seed)
        record_arrays_close(
            result.order_records,
            vbt.Portfolio.from_signals(
                price,
                [True, False, False, False, False],
                [False, False, False, False, True]
            ).order_records
        )
        pd.testing.assert_index_equal(
            result.wrapper.index,
            price.vbt.wrapper.index
        )
        pd.testing.assert_index_equal(
            result.wrapper.columns,
            price.vbt.wrapper.columns
        )
        result = vbt.Portfolio.from_random_signals(price, prob=[0.25, 0.5], seed=seed)
        record_arrays_close(
            result.order_records,
            vbt.Portfolio.from_signals(
                price,
                [[False, True], [False, False], [False, False], [False, False], [True, False]],
                [[False, False], [False, True], [False, False], [False, False], [False, False]]
            ).order_records
        )
        pd.testing.assert_index_equal(
            result.wrapper.index,
            pd.DatetimeIndex([
                '2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'
            ], dtype='datetime64[ns]', freq=None)
        )
        pd.testing.assert_index_equal(
            result.wrapper.columns,
            pd.MultiIndex.from_tuples(
                [(0.25, 0.25), (0.5, 0.5)],
                names=['rprobnx_entry_prob', 'rprobnx_exit_prob'])
        )


# ############# from_order_func ############# #

@njit
def order_func_nb(c, size):
    _size = nb.get_elem_nb(c, size)
    return nb.order_nb(_size if c.i % 2 == 0 else -_size)


@njit
def log_order_func_nb(c, size):
    _size = nb.get_elem_nb(c, size)
    return nb.order_nb(_size if c.i % 2 == 0 else -_size, log=True)


@njit
def flex_order_func_nb(c, size):
    if c.call_idx < c.group_len:
        _size = nb.get_col_elem_nb(c, c.from_col + c.call_idx, size)
        return c.from_col + c.call_idx, nb.order_nb(_size if c.i % 2 == 0 else -_size)
    return -1, nb.order_nothing_nb()


@njit
def log_flex_order_func_nb(c, size):
    if c.call_idx < c.group_len:
        _size = nb.get_col_elem_nb(c, c.from_col + c.call_idx, size)
        return c.from_col + c.call_idx, nb.order_nb(_size if c.i % 2 == 0 else -_size, log=True)
    return -1, nb.order_nothing_nb()


class TestFromOrderFunc:
    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_one_column(self, test_row_wise, test_flexible):
        order_func = flex_order_func_nb if test_flexible else order_func_nb
        pf = vbt.Portfolio.from_order_func(
            price.tolist(), order_func, np.asarray(np.inf), row_wise=test_row_wise, flexible=test_flexible)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1),
                (2, 0, 2, 133.33333333333334, 3.0, 0.0, 0), (3, 0, 3, 66.66666666666669, 4.0, 0.0, 1),
                (4, 0, 4, 53.33333333333335, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        pf = vbt.Portfolio.from_order_func(
            price, order_func, np.asarray(np.inf), row_wise=test_row_wise, flexible=test_flexible)
        record_arrays_close(
            pf.order_records,
            np.array([
                (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 0, 1, 200.0, 2.0, 0.0, 1),
                (2, 0, 2, 133.33333333333334, 3.0, 0.0, 0), (3, 0, 3, 66.66666666666669, 4.0, 0.0, 1),
                (4, 0, 4, 53.33333333333335, 5.0, 0.0, 0)
            ], dtype=order_dt)
        )
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'])
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            pd.Index([0], dtype='int64')
        )
        assert pf.wrapper.ndim == 1
        assert pf.wrapper.freq == day_dt
        assert pf.wrapper.grouper.group_by is None

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    @pytest.mark.parametrize("test_use_numba", [False, True])
    def test_multiple_columns(self, test_row_wise, test_flexible, test_use_numba):
        order_func = flex_order_func_nb if test_flexible else order_func_nb
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, vbt.Rep('size'), broadcast_named_args=dict(size=[0, 1, np.inf]),
            row_wise=test_row_wise, flexible=test_flexible, use_numba=test_use_numba)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 2, 0, 100.0, 1.0, 0.0, 0),
                    (2, 1, 1, 1.0, 2.0, 0.0, 1), (3, 2, 1, 200.0, 2.0, 0.0, 1),
                    (4, 1, 2, 1.0, 3.0, 0.0, 0), (5, 2, 2, 133.33333333333334, 3.0, 0.0, 0),
                    (6, 1, 3, 1.0, 4.0, 0.0, 1), (7, 2, 3, 66.66666666666669, 4.0, 0.0, 1),
                    (8, 1, 4, 1.0, 5.0, 0.0, 0), (9, 2, 4, 53.33333333333335, 5.0, 0.0, 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 1, 0, 1.0, 1.0, 0.0, 0), (1, 1, 1, 1.0, 2.0, 0.0, 1),
                    (2, 1, 2, 1.0, 3.0, 0.0, 0), (3, 1, 3, 1.0, 4.0, 0.0, 1),
                    (4, 1, 4, 1.0, 5.0, 0.0, 0), (5, 2, 0, 100.0, 1.0, 0.0, 0),
                    (6, 2, 1, 200.0, 2.0, 0.0, 1), (7, 2, 2, 133.33333333333334, 3.0, 0.0, 0),
                    (8, 2, 3, 66.66666666666669, 4.0, 0.0, 1), (9, 2, 4, 53.33333333333335, 5.0, 0.0, 0)
                ], dtype=order_dt)
            )
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'])
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            pd.Index(['a', 'b', 'c'], dtype='object')
        )
        assert pf.wrapper.ndim == 2
        assert pf.wrapper.freq == day_dt
        assert pf.wrapper.grouper.group_by is None

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_group_by(self, test_row_wise, test_flexible):
        order_func = flex_order_func_nb if test_flexible else order_func_nb
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(np.inf),
            group_by=np.array([0, 0, 1]), row_wise=test_row_wise, flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 1, 0, 100.0, 1.0, 0.0, 0),
                    (2, 2, 0, 100.0, 1.0, 0.0, 0), (3, 0, 1, 200.0, 2.0, 0.0, 1),
                    (4, 1, 1, 200.0, 2.0, 0.0, 1), (5, 2, 1, 200.0, 2.0, 0.0, 1),
                    (6, 0, 2, 133.33333333333334, 3.0, 0.0, 0), (7, 1, 2, 133.33333333333334, 3.0, 0.0, 0),
                    (8, 2, 2, 133.33333333333334, 3.0, 0.0, 0), (9, 0, 3, 66.66666666666669, 4.0, 0.0, 1),
                    (10, 1, 3, 66.66666666666669, 4.0, 0.0, 1), (11, 2, 3, 66.66666666666669, 4.0, 0.0, 1),
                    (12, 0, 4, 53.33333333333335, 5.0, 0.0, 0), (13, 1, 4, 53.33333333333335, 5.0, 0.0, 0),
                    (14, 2, 4, 53.33333333333335, 5.0, 0.0, 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 100.0, 1.0, 0.0, 0), (1, 1, 0, 100.0, 1.0, 0.0, 0),
                    (2, 0, 1, 200.0, 2.0, 0.0, 1), (3, 1, 1, 200.0, 2.0, 0.0, 1),
                    (4, 0, 2, 133.33333333333334, 3.0, 0.0, 0), (5, 1, 2, 133.33333333333334, 3.0, 0.0, 0),
                    (6, 0, 3, 66.66666666666669, 4.0, 0.0, 1), (7, 1, 3, 66.66666666666669, 4.0, 0.0, 1),
                    (8, 0, 4, 53.33333333333335, 5.0, 0.0, 0), (9, 1, 4, 53.33333333333335, 5.0, 0.0, 0),
                    (10, 2, 0, 100.0, 1.0, 0.0, 0), (11, 2, 1, 200.0, 2.0, 0.0, 1),
                    (12, 2, 2, 133.33333333333334, 3.0, 0.0, 0), (13, 2, 3, 66.66666666666669, 4.0, 0.0, 1),
                    (14, 2, 4, 53.33333333333335, 5.0, 0.0, 0)
                ], dtype=order_dt)
            )
        pd.testing.assert_index_equal(
            pf.wrapper.grouper.group_by,
            pd.Index([0, 0, 1], dtype='int64')
        )
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series([200., 100.], index=pd.Index([0, 1], dtype='int64')).rename('init_cash')
        )
        assert not pf.cash_sharing

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_cash_sharing(self, test_row_wise, test_flexible):
        order_func = flex_order_func_nb if test_flexible else order_func_nb
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(np.inf),
            group_by=np.array([0, 0, 1]), cash_sharing=True, row_wise=test_row_wise, flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 100., 1., 0., 0), (1, 2, 0, 100., 1., 0., 0),
                    (2, 0, 1, 200., 2., 0., 1), (3, 2, 1, 200., 2., 0., 1),
                    (4, 0, 2, 133.33333333, 3., 0., 0), (5, 2, 2, 133.33333333, 3., 0., 0),
                    (6, 0, 3, 66.66666667, 4., 0., 1), (7, 2, 3, 66.66666667, 4., 0., 1),
                    (8, 0, 4, 53.33333333, 5., 0., 0), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 100., 1., 0., 0), (1, 0, 1, 200., 2., 0., 1),
                    (2, 0, 2, 133.33333333, 3., 0., 0), (3, 0, 3, 66.66666667, 4., 0., 1),
                    (4, 0, 4, 53.33333333, 5., 0., 0), (5, 2, 0, 100., 1., 0., 0),
                    (6, 2, 1, 200., 2., 0., 1), (7, 2, 2, 133.33333333, 3., 0., 0),
                    (8, 2, 3, 66.66666667, 4., 0., 1), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        pd.testing.assert_index_equal(
            pf.wrapper.grouper.group_by,
            pd.Index([0, 0, 1], dtype='int64')
        )
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series([100., 100.], index=pd.Index([0, 1], dtype='int64')).rename('init_cash')
        )
        assert pf.cash_sharing

    @pytest.mark.parametrize(
        "test_row_wise",
        [False, True],
    )
    def test_call_seq(self, test_row_wise):
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, np.asarray(np.inf), group_by=np.array([0, 0, 1]),
            cash_sharing=True, row_wise=test_row_wise)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 100., 1., 0., 0), (1, 2, 0, 100., 1., 0., 0),
                    (2, 0, 1, 200., 2., 0., 1), (3, 2, 1, 200., 2., 0., 1),
                    (4, 0, 2, 133.33333333, 3., 0., 0), (5, 2, 2, 133.33333333, 3., 0., 0),
                    (6, 0, 3, 66.66666667, 4., 0., 1), (7, 2, 3, 66.66666667, 4., 0., 1),
                    (8, 0, 4, 53.33333333, 5., 0., 0), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 100., 1., 0., 0), (1, 0, 1, 200., 2., 0., 1),
                    (2, 0, 2, 133.33333333, 3., 0., 0), (3, 0, 3, 66.66666667, 4., 0., 1),
                    (4, 0, 4, 53.33333333, 5., 0., 0), (5, 2, 0, 100., 1., 0., 0),
                    (6, 2, 1, 200., 2., 0., 1), (7, 2, 2, 133.33333333, 3., 0., 0),
                    (8, 2, 3, 66.66666667, 4., 0., 1), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ])
        )
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, np.asarray(np.inf), group_by=np.array([0, 0, 1]),
            cash_sharing=True, call_seq='reversed', row_wise=test_row_wise)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 1, 0, 100., 1., 0., 0), (1, 2, 0, 100., 1., 0., 0),
                    (2, 1, 1, 200., 2., 0., 1), (3, 2, 1, 200., 2., 0., 1),
                    (4, 1, 2, 133.33333333, 3., 0., 0), (5, 2, 2, 133.33333333, 3., 0., 0),
                    (6, 1, 3, 66.66666667, 4., 0., 1), (7, 2, 3, 66.66666667, 4., 0., 1),
                    (8, 1, 4, 53.33333333, 5., 0., 0), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 1, 0, 100., 1., 0., 0), (1, 1, 1, 200., 2., 0., 1),
                    (2, 1, 2, 133.33333333, 3., 0., 0), (3, 1, 3, 66.66666667, 4., 0., 1),
                    (4, 1, 4, 53.33333333, 5., 0., 0), (5, 2, 0, 100., 1., 0., 0),
                    (6, 2, 1, 200., 2., 0., 1), (7, 2, 2, 133.33333333, 3., 0., 0),
                    (8, 2, 3, 66.66666667, 4., 0., 1), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0]
            ])
        )
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, np.asarray(np.inf), group_by=np.array([0, 0, 1]),
            cash_sharing=True, call_seq='random', seed=seed, row_wise=test_row_wise)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 1, 0, 100., 1., 0., 0), (1, 2, 0, 100., 1., 0., 0),
                    (2, 1, 1, 200., 2., 0., 1), (3, 2, 1, 200., 2., 0., 1),
                    (4, 1, 2, 133.33333333, 3., 0., 0), (5, 2, 2, 133.33333333, 3., 0., 0),
                    (6, 1, 3, 66.66666667, 4., 0., 1), (7, 2, 3, 66.66666667, 4., 0., 1),
                    (8, 1, 4, 53.33333333, 5., 0., 0), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 1, 0, 100., 1., 0., 0), (1, 1, 1, 200., 2., 0., 1),
                    (2, 1, 2, 133.33333333, 3., 0., 0), (3, 1, 3, 66.66666667, 4., 0., 1),
                    (4, 1, 4, 53.33333333, 5., 0., 0), (5, 2, 0, 100., 1., 0., 0),
                    (6, 2, 1, 200., 2., 0., 1), (7, 2, 2, 133.33333333, 3., 0., 0),
                    (8, 2, 3, 66.66666667, 4., 0., 1), (9, 2, 4, 53.33333333, 5., 0., 0)
                ], dtype=order_dt)
            )
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [1, 0, 0],
                [0, 1, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0]
            ])
        )
        with pytest.raises(Exception):
            _ = vbt.Portfolio.from_order_func(
                price_wide, order_func_nb, np.asarray(np.inf), group_by=np.array([0, 0, 1]),
                cash_sharing=True, call_seq='auto', row_wise=test_row_wise
            )

        target_hold_value = pd.DataFrame({
            'a': [0., 70., 30., 0., 70.],
            'b': [30., 0., 70., 30., 30.],
            'c': [70., 30., 0., 70., 0.]
        }, index=price.index)

        @njit
        def pre_segment_func_nb(c, target_hold_value):
            order_size = np.copy(target_hold_value[c.i, c.from_col:c.to_col])
            order_size_type = np.full(c.group_len, SizeType.TargetValue)
            direction = np.full(c.group_len, Direction.Both)
            order_value_out = np.empty(c.group_len, dtype=np.float64)
            c.last_val_price[c.from_col:c.to_col] = c.close[c.i, c.from_col:c.to_col]
            nb.sort_call_seq_nb(c, order_size, order_size_type, direction, order_value_out)
            return order_size, order_size_type, direction

        @njit
        def pct_order_func_nb(c, order_size, order_size_type, direction):
            col_i = c.call_seq_now[c.call_idx]
            return nb.order_nb(
                order_size[col_i],
                c.close[c.i, col_i],
                size_type=order_size_type[col_i],
                direction=direction[col_i]
            )

        pf = vbt.Portfolio.from_order_func(
            price_wide * 0 + 1, pct_order_func_nb, group_by=np.array([0, 0, 0]),
            cash_sharing=True, pre_segment_func_nb=pre_segment_func_nb,
            pre_segment_args=(target_hold_value.values,), row_wise=test_row_wise)
        np.testing.assert_array_equal(
            pf.call_seq.values,
            np.array([
                [0, 1, 2],
                [2, 1, 0],
                [0, 2, 1],
                [1, 0, 2],
                [2, 1, 0]
            ])
        )
        pd.testing.assert_frame_equal(
            pf.asset_value(group_by=False),
            target_hold_value
        )

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_target_value(self, test_row_wise, test_flexible):
        @njit
        def target_val_pre_segment_func_nb(c, val_price):
            c.last_val_price[c.from_col:c.to_col] = val_price[c.i]
            return ()

        if test_flexible:
            @njit
            def target_val_order_func_nb(c):
                col = c.from_col + c.call_idx
                if c.call_idx < c.group_len:
                    return col, nb.order_nb(50., nb.get_col_elem_nb(c, col, c.close), size_type=SizeType.TargetValue)
                return -1, nb.order_nothing_nb()
        else:
            @njit
            def target_val_order_func_nb(c):
                return nb.order_nb(50., nb.get_elem_nb(c, c.close), size_type=SizeType.TargetValue)

        pf = vbt.Portfolio.from_order_func(
            price.iloc[1:], target_val_order_func_nb, row_wise=test_row_wise, flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 1, 25.0, 3.0, 0.0, 0), (1, 0, 2, 8.333333333333332, 4.0, 0.0, 1),
                    (2, 0, 3, 4.166666666666668, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 1, 25.0, 3.0, 0.0, 0), (1, 0, 2, 8.333333333333332, 4.0, 0.0, 1),
                    (2, 0, 3, 4.166666666666668, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )
        pf = vbt.Portfolio.from_order_func(
            price.iloc[1:], target_val_order_func_nb,
            pre_segment_func_nb=target_val_pre_segment_func_nb,
            pre_segment_args=(price.iloc[:-1].values,), row_wise=test_row_wise, flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 50.0, 2.0, 0.0, 0), (1, 0, 1, 25.0, 3.0, 0.0, 1),
                    (2, 0, 2, 8.333333333333332, 4.0, 0.0, 1), (3, 0, 3, 4.166666666666668, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 50.0, 2.0, 0.0, 0), (1, 0, 1, 25.0, 3.0, 0.0, 1),
                    (2, 0, 2, 8.333333333333332, 4.0, 0.0, 1), (3, 0, 3, 4.166666666666668, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_target_percent(self, test_row_wise, test_flexible):
        @njit
        def target_pct_pre_segment_func_nb(c, val_price):
            c.last_val_price[c.from_col:c.to_col] = val_price[c.i]
            return ()

        if test_flexible:
            @njit
            def target_pct_order_func_nb(c):
                col = c.from_col + c.call_idx
                if c.call_idx < c.group_len:
                    return col, nb.order_nb(0.5, nb.get_col_elem_nb(c, col, c.close), size_type=SizeType.TargetPercent)
                return -1, nb.order_nothing_nb()
        else:
            @njit
            def target_pct_order_func_nb(c):
                return nb.order_nb(0.5, nb.get_elem_nb(c, c.close), size_type=SizeType.TargetPercent)

        pf = vbt.Portfolio.from_order_func(
            price.iloc[1:], target_pct_order_func_nb, row_wise=test_row_wise, flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 1, 25.0, 3.0, 0.0, 0), (1, 0, 2, 8.333333333333332, 4.0, 0.0, 1),
                    (2, 0, 3, 1.0416666666666679, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 1, 25.0, 3.0, 0.0, 0), (1, 0, 2, 8.333333333333332, 4.0, 0.0, 1),
                    (2, 0, 3, 1.0416666666666679, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )
        pf = vbt.Portfolio.from_order_func(
            price.iloc[1:], target_pct_order_func_nb,
            pre_segment_func_nb=target_pct_pre_segment_func_nb,
            pre_segment_args=(price.iloc[:-1].values,), row_wise=test_row_wise, flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 50.0, 2.0, 0.0, 0), (1, 0, 1, 25.0, 3.0, 0.0, 1),
                    (2, 0, 3, 3.125, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 50.0, 2.0, 0.0, 0), (1, 0, 1, 25.0, 3.0, 0.0, 1),
                    (2, 0, 3, 3.125, 5.0, 0.0, 1)
                ], dtype=order_dt)
            )

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_update_value(self, test_row_wise, test_flexible):
        if test_flexible:
            @njit
            def order_func_nb(c):
                col = c.from_col + c.call_idx
                if c.call_idx < c.group_len:
                    return col, nb.order_nb(
                        np.inf if c.i % 2 == 0 else -np.inf,
                        nb.get_col_elem_nb(c, col, c.close),
                        fees=0.01,
                        fixed_fees=1.,
                        slippage=0.01
                    )
                return -1, nb.order_nothing_nb()
        else:
            @njit
            def order_func_nb(c):
                return nb.order_nb(
                    np.inf if c.i % 2 == 0 else -np.inf,
                    nb.get_elem_nb(c, c.close),
                    fees=0.01,
                    fixed_fees=1.,
                    slippage=0.01
                )

        @njit
        def post_order_func_nb(c, value_before, value_now):
            value_before[c.i, c.col] = c.value_before
            value_now[c.i, c.col] = c.value_now

        value_before = np.empty_like(price.values[:, None])
        value_now = np.empty_like(price.values[:, None])

        _ = vbt.Portfolio.from_order_func(
            price,
            order_func_nb,
            post_order_func_nb=post_order_func_nb,
            post_order_args=(value_before, value_now),
            row_wise=test_row_wise,
            update_value=False,
            flexible=test_flexible)

        np.testing.assert_array_equal(
            value_before,
            value_now
        )

        _ = vbt.Portfolio.from_order_func(
            price,
            order_func_nb,
            post_order_func_nb=post_order_func_nb,
            post_order_args=(value_before, value_now),
            row_wise=test_row_wise,
            update_value=True,
            flexible=test_flexible)

        np.testing.assert_array_equal(
            value_before,
            np.array([
                [100.0],
                [97.04930889128518],
                [185.46988117104038],
                [82.47853456223025],
                [104.65775576218027]
            ])
        )
        np.testing.assert_array_equal(
            value_now,
            np.array([
                [98.01980198019803],
                [187.36243097890815],
                [83.30331990785257],
                [105.72569204546781],
                [73.54075125567473]
            ])
        )

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_states(self, test_row_wise, test_flexible):
        close = np.array([
            [1, 1, 1],
            [np.nan, 2, 2],
            [3, np.nan, 3],
            [4, 4, np.nan],
            [5, 5, 5]
        ])
        size = np.array([
            [1, 1, 1],
            [-1, -1, -1],
            [1, 1, 1],
            [-1, -1, -1],
            [1, 1, 1]
        ])
        value_arr1 = np.empty((size.shape[0], 2), dtype=np.float64)
        value_arr2 = np.empty(size.shape, dtype=np.float64)
        value_arr3 = np.empty(size.shape, dtype=np.float64)
        return_arr1 = np.empty((size.shape[0], 2), dtype=np.float64)
        return_arr2 = np.empty(size.shape, dtype=np.float64)
        return_arr3 = np.empty(size.shape, dtype=np.float64)
        pos_record_arr1 = np.empty(size.shape, dtype=trade_dt)
        pos_record_arr2 = np.empty(size.shape, dtype=trade_dt)
        pos_record_arr3 = np.empty(size.shape, dtype=trade_dt)

        def pre_segment_func_nb(c):
            value_arr1[c.i, c.group] = c.last_value[c.group]
            return_arr1[c.i, c.group] = c.last_return[c.group]
            for col in range(c.from_col, c.to_col):
                pos_record_arr1[c.i, col] = c.last_pos_record[col]
            if c.i > 0:
                c.last_val_price[c.from_col:c.to_col] = c.last_val_price[c.from_col:c.to_col] + 0.5
            return ()

        if test_flexible:
            def order_func_nb(c):
                col = c.from_col + c.call_idx
                if c.call_idx < c.group_len:
                    value_arr2[c.i, col] = c.last_value[c.group]
                    return_arr2[c.i, col] = c.last_return[c.group]
                    pos_record_arr2[c.i, col] = c.last_pos_record[col]
                    return col, nb.order_nb(size[c.i, col], fixed_fees=1.)
                return -1, nb.order_nothing_nb()
        else:
            def order_func_nb(c):
                value_arr2[c.i, c.col] = c.value_now
                return_arr2[c.i, c.col] = c.return_now
                pos_record_arr2[c.i, c.col] = c.pos_record_now
                return nb.order_nb(size[c.i, c.col], fixed_fees=1.)

        def post_order_func_nb(c):
            value_arr3[c.i, c.col] = c.value_now
            return_arr3[c.i, c.col] = c.return_now
            pos_record_arr3[c.i, c.col] = c.pos_record_now

        _ = vbt.Portfolio.from_order_func(
            close,
            order_func_nb,
            pre_segment_func_nb=pre_segment_func_nb,
            post_order_func_nb=post_order_func_nb,
            use_numba=False,
            row_wise=test_row_wise,
            update_value=True,
            ffill_val_price=True,
            group_by=[0, 0, 1],
            cash_sharing=True,
            flexible=test_flexible
        )

        np.testing.assert_array_equal(
            value_arr1,
            np.array([
                [100.0, 100.0],
                [98.0, 99.0],
                [98.5, 99.0],
                [99.0, 98.0],
                [99.0, 98.5]
            ])
        )
        np.testing.assert_array_equal(
            value_arr2,
            np.array([
                [100.0, 99.0, 100.0],
                [99.0, 99.0, 99.5],
                [99.0, 99.0, 99.0],
                [100.0, 100.0, 98.5],
                [99.0, 98.5, 99.0]
            ])
        )
        np.testing.assert_array_equal(
            value_arr3,
            np.array([
                [99.0, 98.0, 99.0],
                [99.0, 98.5, 99.0],
                [99.0, 99.0, 98.0],
                [100.0, 99.0, 98.5],
                [98.5, 97.0, 99.0]
            ])
        )
        np.testing.assert_array_equal(
            return_arr1,
            np.array([
                [np.nan, np.nan],
                [-0.02, -0.01],
                [0.00510204081632653, 0.0],
                [0.005076142131979695, -0.010101010101010102],
                [0.0, 0.00510204081632653]
            ])
        )
        np.testing.assert_array_equal(
            return_arr2,
            np.array([
                [0.0, -0.01, 0.0],
                [-0.01, -0.01, -0.005],
                [0.01020408163265306, 0.01020408163265306, 0.0],
                [0.015228426395939087, 0.015228426395939087, -0.005050505050505051],
                [0.0, -0.005050505050505051, 0.01020408163265306]
            ])
        )
        np.testing.assert_array_equal(
            return_arr3,
            np.array([
                [-0.01, -0.02, -0.01],
                [-0.01, -0.015, -0.01],
                [0.01020408163265306, 0.01020408163265306, -0.010101010101010102],
                [0.015228426395939087, 0.005076142131979695, -0.005050505050505051],
                [-0.005050505050505051, -0.020202020202020204, 0.01020408163265306]
            ])
        )
        record_arrays_close(
            pos_record_arr1.flatten()[3:],
            np.array([
                (0, 0, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -1.0, -1.0, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -1.0, -1.0, 0, 0, 0),
                (0, 2, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -1.0, -1.0, 0, 0, 0),
                (0, 0, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -0.5, -0.5, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (0, 2, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (0, 0, 2.0, 0, 2.0, 2.0, -1, np.nan, 0.0, 0.0, 0.0, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (1, 2, 1.0, 2, 3.0, 1.0, -1, np.nan, 0.0, -1.0, -0.3333333333333333, 0, 0, 1),
                (0, 0, 2.0, 0, 2.0, 2.0, -1, 4.0, 1.0, 1.0, 0.25, 0, 0, 0),
                (1, 1, 1.0, 3, 4.0, 1.0, -1, np.nan, 0.0, -1.0, -0.25, 1, 0, 1),
                (1, 2, 1.0, 2, 3.0, 1.0, -1, np.nan, 0.0, -0.5, -0.16666666666666666, 0, 0, 1)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            pos_record_arr2.flatten()[3:],
            np.array([
                (0, 0, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -0.5, -0.5, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -0.5, -0.5, 0, 0, 0),
                (0, 2, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -0.5, -0.5, 0, 0, 0),
                (0, 0, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, 0.0, 0.0, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (0, 2, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (0, 0, 2.0, 0, 2.0, 2.0, -1, np.nan, 0.0, 1.0, 0.25, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (1, 2, 1.0, 2, 3.0, 1.0, -1, np.nan, 0.0, -0.5, -0.16666666666666666, 0, 0, 1),
                (0, 0, 2.0, 0, 2.0, 2.0, -1, 4.0, 1.0, 1.5, 0.375, 0, 0, 0),
                (1, 1, 1.0, 3, 4.0, 1.0, -1, np.nan, 0.0, -1.5, -0.375, 1, 0, 1),
                (1, 2, 1.0, 2, 3.0, 1.0, -1, np.nan, 0.0, 0.0, 0.0, 0, 0, 1)
            ], dtype=trade_dt)
        )
        record_arrays_close(
            pos_record_arr3.flatten(),
            np.array([
                (0, 0, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -1.0, -1.0, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -1.0, -1.0, 0, 0, 0),
                (0, 2, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -1.0, -1.0, 0, 0, 0),
                (0, 0, 1.0, 0, 1.0, 1.0, -1, np.nan, 0.0, -0.5, -0.5, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (0, 2, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (0, 0, 2.0, 0, 2.0, 2.0, -1, np.nan, 0.0, 0.0, 0.0, 0, 0, 0),
                (0, 1, 1.0, 0, 1.0, 1.0, 1, 2.0, 1.0, -1.0, -1.0, 0, 1, 0),
                (1, 2, 1.0, 2, 3.0, 1.0, -1, np.nan, 0.0, -1.0, -0.3333333333333333, 0, 0, 1),
                (0, 0, 2.0, 0, 2.0, 2.0, -1, 4.0, 1.0, 1.0, 0.25, 0, 0, 0),
                (1, 1, 1.0, 3, 4.0, 1.0, -1, np.nan, 0.0, -1.0, -0.25, 1, 0, 1),
                (1, 2, 1.0, 2, 3.0, 1.0, -1, np.nan, 0.0, -0.5, -0.16666666666666666, 0, 0, 1),
                (0, 0, 3.0, 0, 3.0, 3.0, -1, 4.0, 1.0, 1.0, 0.1111111111111111, 0, 0, 0),
                (1, 1, 1.0, 3, 4.0, 1.0, 4, 5.0, 1.0, -3.0, -0.75, 1, 1, 1),
                (1, 2, 2.0, 2, 4.0, 2.0, -1, np.nan, 0.0, 0.0, 0.0, 0, 0, 1)
            ], dtype=trade_dt)
        )

        cash_arr = np.empty((size.shape[0], 2), dtype=np.float64)
        position_arr = np.empty(size.shape, dtype=np.float64)
        val_price_arr = np.empty(size.shape, dtype=np.float64)
        value_arr = np.empty((size.shape[0], 2), dtype=np.float64)
        return_arr = np.empty((size.shape[0], 2), dtype=np.float64)
        sim_order_cash_arr = np.empty(size.shape, dtype=np.float64)
        sim_order_value_arr = np.empty(size.shape, dtype=np.float64)
        sim_order_return_arr = np.empty(size.shape, dtype=np.float64)

        def post_order_func_nb(c):
            sim_order_cash_arr[c.i, c.col] = c.cash_now
            sim_order_value_arr[c.i, c.col] = c.value_now
            sim_order_return_arr[c.i, c.col] = c.value_now
            if c.i == 0 and c.call_idx == 0:
                sim_order_return_arr[c.i, c.col] -= c.init_cash[c.group]
                sim_order_return_arr[c.i, c.col] /= c.init_cash[c.group]
            else:
                if c.call_idx == 0:
                    prev_i = c.i - 1
                    prev_col = c.to_col - 1
                else:
                    prev_i = c.i
                    prev_col = c.from_col + c.call_idx - 1
                sim_order_return_arr[c.i, c.col] -= sim_order_value_arr[prev_i, prev_col]
                sim_order_return_arr[c.i, c.col] /= sim_order_value_arr[prev_i, prev_col]

        def post_segment_func_nb(c):
            cash_arr[c.i, c.group] = c.last_cash[c.group]
            for col in range(c.from_col, c.to_col):
                position_arr[c.i, col] = c.last_position[col]
                val_price_arr[c.i, col] = c.last_val_price[col]
            value_arr[c.i, c.group] = c.last_value[c.group]
            return_arr[c.i, c.group] = c.last_return[c.group]

        pf = vbt.Portfolio.from_order_func(
            close,
            order_func_nb,
            post_order_func_nb=post_order_func_nb,
            post_segment_func_nb=post_segment_func_nb,
            use_numba=False,
            row_wise=test_row_wise,
            update_value=True,
            ffill_val_price=True,
            group_by=[0, 0, 1],
            cash_sharing=True,
            flexible=test_flexible
        )

        np.testing.assert_array_equal(
            cash_arr,
            pf.cash().values
        )
        np.testing.assert_array_equal(
            position_arr,
            pf.assets().values
        )
        np.testing.assert_array_equal(
            val_price_arr,
            pf.get_filled_close().values
        )
        np.testing.assert_array_equal(
            value_arr,
            pf.value().values
        )
        np.testing.assert_array_equal(
            return_arr,
            pf.returns().values
        )
        if test_flexible:
            with pytest.raises(Exception):
                pf.cash(in_sim_order=True, group_by=False)
            with pytest.raises(Exception):
                pf.value(in_sim_order=True, group_by=False)
            with pytest.raises(Exception):
                pf.returns(in_sim_order=True, group_by=False)
        else:
            np.testing.assert_array_equal(
                sim_order_cash_arr,
                pf.cash(in_sim_order=True, group_by=False).values
            )
            np.testing.assert_array_equal(
                sim_order_value_arr,
                pf.value(in_sim_order=True, group_by=False).values
            )
            np.testing.assert_array_equal(
                sim_order_return_arr,
                pf.returns(in_sim_order=True, group_by=False).values
            )

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_post_sim_ctx(self, test_row_wise, test_flexible):
        if test_flexible:
            def order_func(c):
                col = c.from_col + c.call_idx
                if c.call_idx < c.group_len:
                    return col, nb.order_nb(
                        1.,
                        nb.get_col_elem_nb(c, col, c.close),
                        fees=0.01,
                        fixed_fees=1.,
                        slippage=0.01,
                        log=True
                    )
                return -1, nb.order_nothing_nb()
        else:
            def order_func(c):
                return nb.order_nb(
                    1.,
                    nb.get_elem_nb(c, c.close),
                    fees=0.01,
                    fixed_fees=1.,
                    slippage=0.01,
                    log=True
                )

        def post_sim_func(c, lst):
            lst.append(deepcopy(c))

        lst = []

        _ = vbt.Portfolio.from_order_func(
            price_wide,
            order_func,
            post_sim_func_nb=post_sim_func,
            post_sim_args=(lst,),
            row_wise=test_row_wise,
            update_value=True,
            max_logs=price_wide.shape[0] * price_wide.shape[1],
            use_numba=False,
            group_by=[0, 0, 1],
            cash_sharing=True,
            flexible=test_flexible
        )

        c = lst[-1]

        assert c.target_shape == price_wide.shape
        np.testing.assert_array_equal(
            c.close,
            price_wide.values
        )
        np.testing.assert_array_equal(
            c.group_lens,
            np.array([2, 1])
        )
        np.testing.assert_array_equal(
            c.init_cash,
            np.array([100., 100.])
        )
        assert c.cash_sharing
        if test_flexible:
            assert c.call_seq is None
        else:
            np.testing.assert_array_equal(
                c.call_seq,
                np.array([
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0]
                ])
            )
        np.testing.assert_array_equal(
            c.segment_mask,
            np.array([
                [True, True],
                [True, True],
                [True, True],
                [True, True],
                [True, True]
            ])
        )
        assert c.ffill_val_price
        assert c.update_value
        if test_row_wise:
            record_arrays_close(
                c.order_records,
                np.array([
                    (0, 0, 0, 1.0, 1.01, 1.0101, 0), (1, 1, 0, 1.0, 1.01, 1.0101, 0),
                    (2, 2, 0, 1.0, 1.01, 1.0101, 0), (3, 0, 1, 1.0, 2.02, 1.0202, 0),
                    (4, 1, 1, 1.0, 2.02, 1.0202, 0), (5, 2, 1, 1.0, 2.02, 1.0202, 0),
                    (6, 0, 2, 1.0, 3.0300000000000002, 1.0303, 0), (7, 1, 2, 1.0, 3.0300000000000002, 1.0303, 0),
                    (8, 2, 2, 1.0, 3.0300000000000002, 1.0303, 0), (9, 0, 3, 1.0, 4.04, 1.0404, 0),
                    (10, 1, 3, 1.0, 4.04, 1.0404, 0), (11, 2, 3, 1.0, 4.04, 1.0404, 0),
                    (12, 0, 4, 1.0, 5.05, 1.0505, 0), (13, 1, 4, 1.0, 5.05, 1.0505, 0),
                    (14, 2, 4, 1.0, 5.05, 1.0505, 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                c.order_records,
                np.array([
                    (0, 0, 0, 1.0, 1.01, 1.0101, 0), (1, 1, 0, 1.0, 1.01, 1.0101, 0),
                    (2, 0, 1, 1.0, 2.02, 1.0202, 0), (3, 1, 1, 1.0, 2.02, 1.0202, 0),
                    (4, 0, 2, 1.0, 3.0300000000000002, 1.0303, 0), (5, 1, 2, 1.0, 3.0300000000000002, 1.0303, 0),
                    (6, 0, 3, 1.0, 4.04, 1.0404, 0), (7, 1, 3, 1.0, 4.04, 1.0404, 0),
                    (8, 0, 4, 1.0, 5.05, 1.0505, 0), (9, 1, 4, 1.0, 5.05, 1.0505, 0),
                    (10, 2, 0, 1.0, 1.01, 1.0101, 0), (11, 2, 1, 1.0, 2.02, 1.0202, 0),
                    (12, 2, 2, 1.0, 3.0300000000000002, 1.0303, 0), (13, 2, 3, 1.0, 4.04, 1.0404, 0),
                    (14, 2, 4, 1.0, 5.05, 1.0505, 0)
                ], dtype=order_dt)
            )
        if test_row_wise:
            record_arrays_close(
                c.log_records,
                np.array([
                    (0, 0, 0, 0, 100.0, 0.0, 0.0, 100.0, np.nan, 100.0, 1.0, 1.0, 0, 2, 0.01, 1.0, 0.01,
                     0.0, np.inf, np.nan, 0.0, False, True, False, True, 97.9799, 1.0, 0.0, 97.9799, 1.01,
                     98.9899, 1.0, 1.01, 1.0101, 0, 0, -1, 0),
                    (1, 0, 1, 0, 97.9799, 0.0, 0.0, 97.9799, np.nan, 98.9899, 1.0, 1.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 95.9598, 1.0, 0.0,
                     95.9598, 1.01, 97.97980000000001, 1.0, 1.01, 1.0101, 0, 0, -1, 1),
                    (2, 1, 2, 0, 100.0, 0.0, 0.0, 100.0, np.nan, 100.0, 1.0, 1.0, 0, 2, 0.01, 1.0, 0.01,
                     0.0, np.inf, np.nan, 0.0, False, True, False, True, 97.9799, 1.0, 0.0, 97.9799, 1.01,
                     98.9899, 1.0, 1.01, 1.0101, 0, 0, -1, 2),
                    (3, 0, 0, 1, 95.9598, 1.0, 0.0, 95.9598, 1.0, 97.9598, 1.0, 2.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 92.9196, 2.0, 0.0,
                     92.9196, 2.02, 97.95960000000001, 1.0, 2.02, 1.0202, 0, 0, -1, 3),
                    (4, 0, 1, 1, 92.9196, 1.0, 0.0, 92.9196, 1.0, 97.95960000000001, 1.0, 2.0,
                     0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     89.8794, 2.0, 0.0, 89.8794, 2.02, 97.95940000000002, 1.0, 2.02, 1.0202, 0, 0, -1, 4),
                    (5, 1, 2, 1, 97.9799, 1.0, 0.0, 97.9799, 1.0, 98.9799, 1.0, 2.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 94.9397, 2.0, 0.0,
                     94.9397, 2.02, 98.97970000000001, 1.0, 2.02, 1.0202, 0, 0, -1, 5),
                    (6, 0, 0, 2, 89.8794, 2.0, 0.0, 89.8794, 2.0, 97.8794, 1.0, 3.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 85.8191, 3.0, 0.0,
                     85.8191, 3.0300000000000002, 98.90910000000001, 1.0, 3.0300000000000002, 1.0303, 0, 0, -1, 6),
                    (7, 0, 1, 2, 85.8191, 2.0, 0.0, 85.8191, 2.0, 98.90910000000001, 1.0, 3.0, 0,
                     2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     81.75880000000001, 3.0, 0.0, 81.75880000000001, 3.0300000000000002, 99.93880000000001,
                     1.0, 3.0300000000000002, 1.0303, 0, 0, -1, 7),
                    (8, 1, 2, 2, 94.9397, 2.0, 0.0, 94.9397, 2.0, 98.9397, 1.0, 3.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 90.8794, 3.0, 0.0,
                     90.8794, 3.0300000000000002, 99.96940000000001, 1.0, 3.0300000000000002, 1.0303, 0, 0, -1, 8),
                    (9, 0, 0, 3, 81.75880000000001, 3.0, 0.0, 81.75880000000001, 3.0, 99.75880000000001,
                     1.0, 4.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     76.67840000000001, 4.0, 0.0, 76.67840000000001, 4.04, 101.83840000000001, 1.0,
                     4.04, 1.0404, 0, 0, -1, 9),
                    (10, 0, 1, 3, 76.67840000000001, 3.0, 0.0, 76.67840000000001, 3.0, 101.83840000000001,
                     1.0, 4.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     71.59800000000001, 4.0, 0.0, 71.59800000000001, 4.04, 103.918, 1.0, 4.04, 1.0404,
                     0, 0, -1, 10),
                    (11, 1, 2, 3, 90.8794, 3.0, 0.0, 90.8794, 3.0, 99.8794, 1.0, 4.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 85.799, 4.0, 0.0, 85.799,
                     4.04, 101.959, 1.0, 4.04, 1.0404, 0, 0, -1, 11),
                    (12, 0, 0, 4, 71.59800000000001, 4.0, 0.0, 71.59800000000001, 4.0, 103.59800000000001,
                     1.0, 5.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     65.49750000000002, 5.0, 0.0, 65.49750000000002, 5.05, 106.74750000000002, 1.0,
                     5.05, 1.0505, 0, 0, -1, 12),
                    (13, 0, 1, 4, 65.49750000000002, 4.0, 0.0, 65.49750000000002, 4.0, 106.74750000000002,
                     1.0, 5.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     59.39700000000002, 5.0, 0.0, 59.39700000000002, 5.05, 109.89700000000002, 1.0,
                     5.05, 1.0505, 0, 0, -1, 13),
                    (14, 1, 2, 4, 85.799, 4.0, 0.0, 85.799, 4.0, 101.799, 1.0, 5.0, 0, 2, 0.01, 1.0,
                     0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 79.69850000000001, 5.0, 0.0,
                     79.69850000000001, 5.05, 104.94850000000001, 1.0, 5.05, 1.0505, 0, 0, -1, 14)
                ], dtype=log_dt)
            )
        else:
            record_arrays_close(
                c.log_records,
                np.array([
                    (0, 0, 0, 0, 100.0, 0.0, 0.0, 100.0, np.nan, 100.0, 1.0, 1.0, 0, 2, 0.01, 1.0, 0.01,
                     0.0, np.inf, np.nan, 0.0, False, True, False, True, 97.9799, 1.0, 0.0, 97.9799, 1.01,
                     98.9899, 1.0, 1.01, 1.0101, 0, 0, -1, 0),
                    (1, 0, 1, 0, 97.9799, 0.0, 0.0, 97.9799, np.nan, 98.9899, 1.0, 1.0, 0, 2, 0.01, 1.0,
                     0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 95.9598, 1.0, 0.0, 95.9598,
                     1.01, 97.97980000000001, 1.0, 1.01, 1.0101, 0, 0, -1, 1),
                    (2, 0, 0, 1, 95.9598, 1.0, 0.0, 95.9598, 1.0, 97.9598, 1.0, 2.0, 0, 2, 0.01, 1.0,
                     0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 92.9196, 2.0, 0.0, 92.9196,
                     2.02, 97.95960000000001, 1.0, 2.02, 1.0202, 0, 0, -1, 2),
                    (3, 0, 1, 1, 92.9196, 1.0, 0.0, 92.9196, 1.0, 97.95960000000001, 1.0, 2.0, 0, 2,
                     0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 89.8794, 2.0, 0.0,
                     89.8794, 2.02, 97.95940000000002, 1.0, 2.02, 1.0202, 0, 0, -1, 3),
                    (4, 0, 0, 2, 89.8794, 2.0, 0.0, 89.8794, 2.0, 97.8794, 1.0, 3.0, 0, 2, 0.01, 1.0,
                     0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 85.8191, 3.0, 0.0, 85.8191,
                     3.0300000000000002, 98.90910000000001, 1.0, 3.0300000000000002, 1.0303, 0, 0, -1, 4),
                    (5, 0, 1, 2, 85.8191, 2.0, 0.0, 85.8191, 2.0, 98.90910000000001, 1.0, 3.0, 0, 2,
                     0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 81.75880000000001,
                     3.0, 0.0, 81.75880000000001, 3.0300000000000002, 99.93880000000001, 1.0,
                     3.0300000000000002, 1.0303, 0, 0, -1, 5),
                    (6, 0, 0, 3, 81.75880000000001, 3.0, 0.0, 81.75880000000001, 3.0, 99.75880000000001,
                     1.0, 4.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     76.67840000000001, 4.0, 0.0, 76.67840000000001, 4.04, 101.83840000000001, 1.0,
                     4.04, 1.0404, 0, 0, -1, 6),
                    (7, 0, 1, 3, 76.67840000000001, 3.0, 0.0, 76.67840000000001, 3.0, 101.83840000000001,
                     1.0, 4.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     71.59800000000001, 4.0, 0.0, 71.59800000000001, 4.04, 103.918, 1.0, 4.04, 1.0404, 0, 0, -1, 7),
                    (8, 0, 0, 4, 71.59800000000001, 4.0, 0.0, 71.59800000000001, 4.0, 103.59800000000001,
                     1.0, 5.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     65.49750000000002, 5.0, 0.0, 65.49750000000002, 5.05, 106.74750000000002, 1.0,
                     5.05, 1.0505, 0, 0, -1, 8),
                    (9, 0, 1, 4, 65.49750000000002, 4.0, 0.0, 65.49750000000002, 4.0, 106.74750000000002,
                     1.0, 5.0, 0, 2, 0.01, 1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True,
                     59.39700000000002, 5.0, 0.0, 59.39700000000002, 5.05, 109.89700000000002, 1.0,
                     5.05, 1.0505, 0, 0, -1, 9),
                    (10, 1, 2, 0, 100.0, 0.0, 0.0, 100.0, np.nan, 100.0, 1.0, 1.0, 0, 2, 0.01, 1.0, 0.01,
                     0.0, np.inf, np.nan, 0.0, False, True, False, True, 97.9799, 1.0, 0.0, 97.9799, 1.01,
                     98.9899, 1.0, 1.01, 1.0101, 0, 0, -1, 10),
                    (11, 1, 2, 1, 97.9799, 1.0, 0.0, 97.9799, 1.0, 98.9799, 1.0, 2.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 94.9397, 2.0, 0.0,
                     94.9397, 2.02, 98.97970000000001, 1.0, 2.02, 1.0202, 0, 0, -1, 11),
                    (12, 1, 2, 2, 94.9397, 2.0, 0.0, 94.9397, 2.0, 98.9397, 1.0, 3.0, 0, 2, 0.01,
                     1.0, 0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 90.8794, 3.0, 0.0, 90.8794,
                     3.0300000000000002, 99.96940000000001, 1.0, 3.0300000000000002, 1.0303, 0, 0, -1, 12),
                    (13, 1, 2, 3, 90.8794, 3.0, 0.0, 90.8794, 3.0, 99.8794, 1.0, 4.0, 0, 2, 0.01, 1.0,
                     0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 85.799, 4.0, 0.0, 85.799, 4.04,
                     101.959, 1.0, 4.04, 1.0404, 0, 0, -1, 13),
                    (14, 1, 2, 4, 85.799, 4.0, 0.0, 85.799, 4.0, 101.799, 1.0, 5.0, 0, 2, 0.01, 1.0,
                     0.01, 0.0, np.inf, np.nan, 0.0, False, True, False, True, 79.69850000000001, 5.0, 0.0,
                     79.69850000000001, 5.05, 104.94850000000001, 1.0, 5.05, 1.0505, 0, 0, -1, 14)
                ], dtype=log_dt)
            )
        np.testing.assert_array_equal(
            c.last_cash,
            np.array([59.39700000000002, 79.69850000000001])
        )
        np.testing.assert_array_equal(
            c.last_position,
            np.array([5., 5., 5.])
        )
        np.testing.assert_array_equal(
            c.last_val_price,
            np.array([5.0, 5.0, 5.0])
        )
        np.testing.assert_array_equal(
            c.last_value,
            np.array([109.39700000000002, 104.69850000000001])
        )
        np.testing.assert_array_equal(
            c.second_last_value,
            np.array([103.59800000000001, 101.799])
        )
        np.testing.assert_array_equal(
            c.last_return,
            np.array([0.05597598409235705, 0.028482598060884715])
        )
        np.testing.assert_array_equal(
            c.last_debt,
            np.array([0., 0., 0.])
        )
        np.testing.assert_array_equal(
            c.last_free_cash,
            np.array([59.39700000000002, 79.69850000000001])
        )
        if test_row_wise:
            np.testing.assert_array_equal(
                c.last_oidx,
                np.array([12, 13, 14])
            )
            np.testing.assert_array_equal(
                c.last_lidx,
                np.array([12, 13, 14])
            )
        else:
            np.testing.assert_array_equal(
                c.last_oidx,
                np.array([8, 9, 14])
            )
            np.testing.assert_array_equal(
                c.last_lidx,
                np.array([8, 9, 14])
            )
        assert c.order_records[c.last_oidx[0]]['col'] == 0
        assert c.order_records[c.last_oidx[1]]['col'] == 1
        assert c.order_records[c.last_oidx[2]]['col'] == 2
        assert c.log_records[c.last_lidx[0]]['col'] == 0
        assert c.log_records[c.last_lidx[1]]['col'] == 1
        assert c.log_records[c.last_lidx[2]]['col'] == 2

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_free_cash(self, test_row_wise, test_flexible):
        if test_flexible:
            def order_func(c, size):
                col = c.from_col + c.call_idx
                if c.call_idx < c.group_len:
                    return col, nb.order_nb(
                        size[c.i, col],
                        nb.get_col_elem_nb(c, col, c.close),
                        fees=0.01,
                        fixed_fees=1.,
                        slippage=0.01
                    )
                return -1, nb.order_nothing_nb()
        else:
            def order_func(c, size):
                return nb.order_nb(
                    size[c.i, c.col],
                    nb.get_elem_nb(c, c.close),
                    fees=0.01,
                    fixed_fees=1.,
                    slippage=0.01
                )

        def post_order_func(c, debt, free_cash):
            debt[c.i, c.col] = c.debt_now
            if c.cash_sharing:
                free_cash[c.i, c.group] = c.free_cash_now
            else:
                free_cash[c.i, c.col] = c.free_cash_now

        size = np.array([
            [5, -5, 5],
            [5, -5, -10],
            [-5, 5, 10],
            [-5, 5, -10],
            [-5, 5, 10]
        ])
        debt = np.empty(price_wide.shape, dtype=np.float64)
        free_cash = np.empty(price_wide.shape, dtype=np.float64)
        pf = vbt.Portfolio.from_order_func(
            price_wide,
            order_func, size,
            post_order_func_nb=post_order_func,
            post_order_args=(debt, free_cash,),
            row_wise=test_row_wise,
            use_numba=False,
            flexible=test_flexible
        )
        np.testing.assert_array_equal(
            debt,
            np.array([
                [0.0, 4.95, 0.0],
                [0.0, 14.850000000000001, 9.9],
                [0.0, 7.425000000000001, 0.0],
                [0.0, 0.0, 19.8],
                [24.75, 0.0, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            free_cash,
            np.array([
                [93.8995, 94.0005, 93.8995],
                [82.6985, 83.00150000000001, 92.70150000000001],
                [96.39999999999999, 81.55000000000001, 80.8985],
                [115.002, 74.998, 79.5025],
                [89.0045, 48.49550000000001, 67.0975]
            ])
        )
        np.testing.assert_almost_equal(
            free_cash,
            pf.cash(free=True).values
        )

        debt = np.empty(price_wide.shape, dtype=np.float64)
        free_cash = np.empty(price_wide.shape, dtype=np.float64)
        pf = vbt.Portfolio.from_order_func(
            price_wide.vbt.wrapper.wrap(price_wide.values[::-1]),
            order_func, size,
            post_order_func_nb=post_order_func,
            post_order_args=(debt, free_cash,),
            row_wise=test_row_wise,
            use_numba=False,
            flexible=test_flexible
        )
        np.testing.assert_array_equal(
            debt,
            np.array([
                [0.0, 24.75, 0.0],
                [0.0, 44.55, 19.8],
                [0.0, 22.275, 0.0],
                [0.0, 0.0, 9.9],
                [4.95, 0.0, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            free_cash,
            np.array([
                [73.4975, 74.0025, 73.4975],
                [52.0955, 53.00449999999999, 72.1015],
                [65.797, 81.25299999999999, 80.0985],
                [74.598, 114.60199999999998, 78.9005],
                [68.5985, 108.50149999999998, 87.49949999999998]
            ])
        )
        np.testing.assert_almost_equal(
            free_cash,
            pf.cash(free=True).values
        )

        debt = np.empty(price_wide.shape, dtype=np.float64)
        free_cash = np.empty((price_wide.shape[0], 2), dtype=np.float64)
        pf = vbt.Portfolio.from_order_func(
            price_wide,
            order_func, size,
            post_order_func_nb=post_order_func,
            post_order_args=(debt, free_cash,),
            row_wise=test_row_wise,
            use_numba=False,
            group_by=[0, 0, 1],
            cash_sharing=True,
            flexible=test_flexible
        )
        np.testing.assert_array_equal(
            debt,
            np.array([
                [0.0, 4.95, 0.0],
                [0.0, 14.850000000000001, 9.9],
                [0.0, 7.425000000000001, 0.0],
                [0.0, 0.0, 19.8],
                [24.75, 0.0, 0.0]
            ])
        )
        np.testing.assert_array_equal(
            free_cash,
            np.array([
                [87.9, 93.8995],
                [65.70000000000002, 92.70150000000001],
                [77.95000000000002, 80.8985],
                [90.00000000000001, 79.5025],
                [37.500000000000014, 67.0975]
            ])
        )
        np.testing.assert_almost_equal(
            free_cash,
            pf.cash(free=True).values
        )

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_init_cash(self, test_row_wise, test_flexible):
        order_func = flex_order_func_nb if test_flexible else order_func_nb
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(10.), row_wise=test_row_wise,
            init_cash=[1., 10., np.inf], flexible=test_flexible)
        if test_row_wise:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 1, 0, 10.0, 1.0, 0.0, 0),
                    (2, 2, 0, 10.0, 1.0, 0.0, 0), (3, 0, 1, 10.0, 2.0, 0.0, 1),
                    (4, 1, 1, 10.0, 2.0, 0.0, 1), (5, 2, 1, 10.0, 2.0, 0.0, 1),
                    (6, 0, 2, 6.666666666666667, 3.0, 0.0, 0), (7, 1, 2, 6.666666666666667, 3.0, 0.0, 0),
                    (8, 2, 2, 10.0, 3.0, 0.0, 0), (9, 0, 3, 10.0, 4.0, 0.0, 1),
                    (10, 1, 3, 10.0, 4.0, 0.0, 1), (11, 2, 3, 10.0, 4.0, 0.0, 1),
                    (12, 0, 4, 8.0, 5.0, 0.0, 0), (13, 1, 4, 8.0, 5.0, 0.0, 0),
                    (14, 2, 4, 10.0, 5.0, 0.0, 0)
                ], dtype=order_dt)
            )
        else:
            record_arrays_close(
                pf.order_records,
                np.array([
                    (0, 0, 0, 1.0, 1.0, 0.0, 0), (1, 0, 1, 10.0, 2.0, 0.0, 1),
                    (2, 0, 2, 6.666666666666667, 3.0, 0.0, 0), (3, 0, 3, 10.0, 4.0, 0.0, 1),
                    (4, 0, 4, 8.0, 5.0, 0.0, 0), (5, 1, 0, 10.0, 1.0, 0.0, 0),
                    (6, 1, 1, 10.0, 2.0, 0.0, 1), (7, 1, 2, 6.666666666666667, 3.0, 0.0, 0),
                    (8, 1, 3, 10.0, 4.0, 0.0, 1), (9, 1, 4, 8.0, 5.0, 0.0, 0),
                    (10, 2, 0, 10.0, 1.0, 0.0, 0), (11, 2, 1, 10.0, 2.0, 0.0, 1),
                    (12, 2, 2, 10.0, 3.0, 0.0, 0), (13, 2, 3, 10.0, 4.0, 0.0, 1),
                    (14, 2, 4, 10.0, 5.0, 0.0, 0)
                ], dtype=order_dt)
            )
        assert type(pf._init_cash) == np.ndarray
        base_pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(10.), row_wise=test_row_wise,
            init_cash=np.inf, flexible=test_flexible)
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(10.), row_wise=test_row_wise,
            init_cash=InitCashMode.Auto, flexible=test_flexible)
        record_arrays_close(
            pf.order_records,
            base_pf.orders.values
        )
        assert pf._init_cash == InitCashMode.Auto
        pf = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(10.), row_wise=test_row_wise,
            init_cash=InitCashMode.AutoAlign, flexible=test_flexible)
        record_arrays_close(
            pf.order_records,
            base_pf.orders.values
        )
        assert pf._init_cash == InitCashMode.AutoAlign

    def test_func_calls(self):
        @njit
        def pre_sim_func_nb(c, call_i, pre_sim_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_sim_func_nb(c, call_i, post_sim_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_group_func_nb(c, call_i, pre_group_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_group_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_group_func_nb(c, call_i, post_group_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_group_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_segment_func_nb(c, call_i, pre_segment_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_segment_func_nb(c, call_i, post_segment_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def order_func_nb(c, call_i, order_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            order_lst.append(call_i[0])
            return NoOrder

        @njit
        def post_order_func_nb(c, call_i, post_order_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_order_lst.append(call_i[0])

        sub_arg = vbt.RepEval('np.prod([target_shape[0], target_shape[1]])')

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_group_lst = List.empty_list(typeof(0))
        post_group_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_group_func_nb=pre_group_func_nb, pre_group_args=(pre_group_lst, sub_arg),
            post_group_func_nb=post_group_func_nb, post_group_args=(post_group_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            row_wise=False, template_mapping=dict(np=np)
        )
        assert call_i[0] == 56
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [56]
        assert list(pre_group_lst) == [2, 34]
        assert list(post_group_lst) == [33, 55]
        assert list(pre_segment_lst) == [3, 9, 15, 21, 27, 35, 39, 43, 47, 51]
        assert list(post_segment_lst) == [8, 14, 20, 26, 32, 38, 42, 46, 50, 54]
        assert list(order_lst) == [4, 6, 10, 12, 16, 18, 22, 24, 28, 30, 36, 40, 44, 48, 52]
        assert list(post_order_lst) == [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41, 45, 49, 53]

        segment_mask = np.array([
            [False, False],
            [False, True],
            [True, False],
            [True, True],
            [False, False],
        ])
        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_group_lst = List.empty_list(typeof(0))
        post_group_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_group_func_nb=pre_group_func_nb, pre_group_args=(pre_group_lst, sub_arg),
            post_group_func_nb=post_group_func_nb, post_group_args=(post_group_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            segment_mask=segment_mask, call_pre_segment=True, call_post_segment=True,
            row_wise=False, template_mapping=dict(np=np)
        )
        assert call_i[0] == 38
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [38]
        assert list(pre_group_lst) == [2, 22]
        assert list(post_group_lst) == [21, 37]
        assert list(pre_segment_lst) == [3, 5, 7, 13, 19, 23, 25, 29, 31, 35]
        assert list(post_segment_lst) == [4, 6, 12, 18, 20, 24, 28, 30, 34, 36]
        assert list(order_lst) == [8, 10, 14, 16, 26, 32]
        assert list(post_order_lst) == [9, 11, 15, 17, 27, 33]

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_group_lst = List.empty_list(typeof(0))
        post_group_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_group_func_nb=pre_group_func_nb, pre_group_args=(pre_group_lst, sub_arg),
            post_group_func_nb=post_group_func_nb, post_group_args=(post_group_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            segment_mask=segment_mask, call_pre_segment=False, call_post_segment=False,
            row_wise=False, template_mapping=dict(np=np)
        )
        assert call_i[0] == 26
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [26]
        assert list(pre_group_lst) == [2, 16]
        assert list(post_group_lst) == [15, 25]
        assert list(pre_segment_lst) == [3, 9, 17, 21]
        assert list(post_segment_lst) == [8, 14, 20, 24]
        assert list(order_lst) == [4, 6, 10, 12, 18, 22]
        assert list(post_order_lst) == [5, 7, 11, 13, 19, 23]

    def test_func_calls_flexible(self):
        @njit
        def pre_sim_func_nb(c, call_i, pre_sim_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_sim_func_nb(c, call_i, post_sim_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_group_func_nb(c, call_i, pre_group_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_group_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_group_func_nb(c, call_i, post_group_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_group_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_segment_func_nb(c, call_i, pre_segment_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_segment_func_nb(c, call_i, post_segment_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def flex_order_func_nb(c, call_i, order_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            order_lst.append(call_i[0])
            col = c.from_col + c.call_idx
            if c.call_idx < c.group_len:
                return col, NoOrder
            return -1, NoOrder

        @njit
        def post_order_func_nb(c, call_i, post_order_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_order_lst.append(call_i[0])

        sub_arg = vbt.RepEval('np.prod([target_shape[0], target_shape[1]])')

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_group_lst = List.empty_list(typeof(0))
        post_group_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, flex_order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_group_func_nb=pre_group_func_nb, pre_group_args=(pre_group_lst, sub_arg),
            post_group_func_nb=post_group_func_nb, post_group_args=(post_group_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            row_wise=False, flexible=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 66
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [66]
        assert list(pre_group_lst) == [2, 39]
        assert list(post_group_lst) == [38, 65]
        assert list(pre_segment_lst) == [3, 10, 17, 24, 31, 40, 45, 50, 55, 60]
        assert list(post_segment_lst) == [9, 16, 23, 30, 37, 44, 49, 54, 59, 64]
        assert list(order_lst) == [
            4, 6, 8, 11, 13, 15, 18, 20, 22, 25, 27, 29, 32, 34,
            36, 41, 43, 46, 48, 51, 53, 56, 58, 61, 63
        ]
        assert list(post_order_lst) == [5, 7, 12, 14, 19, 21, 26, 28, 33, 35, 42, 47, 52, 57, 62]

        segment_mask = np.array([
            [False, False],
            [False, True],
            [True, False],
            [True, True],
            [False, False],
        ])
        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_group_lst = List.empty_list(typeof(0))
        post_group_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, flex_order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_group_func_nb=pre_group_func_nb, pre_group_args=(pre_group_lst, sub_arg),
            post_group_func_nb=post_group_func_nb, post_group_args=(post_group_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            segment_mask=segment_mask, call_pre_segment=True, call_post_segment=True,
            row_wise=False, flexible=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 42
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [42]
        assert list(pre_group_lst) == [2, 24]
        assert list(post_group_lst) == [23, 41]
        assert list(pre_segment_lst) == [3, 5, 7, 14, 21, 25, 27, 32, 34, 39]
        assert list(post_segment_lst) == [4, 6, 13, 20, 22, 26, 31, 33, 38, 40]
        assert list(order_lst) == [8, 10, 12, 15, 17, 19, 28, 30, 35, 37]
        assert list(post_order_lst) == [9, 11, 16, 18, 29, 36]

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_group_lst = List.empty_list(typeof(0))
        post_group_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, flex_order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_group_func_nb=pre_group_func_nb, pre_group_args=(pre_group_lst, sub_arg),
            post_group_func_nb=post_group_func_nb, post_group_args=(post_group_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            segment_mask=segment_mask, call_pre_segment=False, call_post_segment=False,
            row_wise=False, flexible=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 30
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [30]
        assert list(pre_group_lst) == [2, 18]
        assert list(post_group_lst) == [17, 29]
        assert list(pre_segment_lst) == [3, 10, 19, 24]
        assert list(post_segment_lst) == [9, 16, 23, 28]
        assert list(order_lst) == [4, 6, 8, 11, 13, 15, 20, 22, 25, 27]
        assert list(post_order_lst) == [5, 7, 12, 14, 21, 26]

    def test_func_calls_row_wise(self):
        @njit
        def pre_sim_func_nb(c, call_i, pre_sim_lst):
            call_i[0] += 1
            pre_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_sim_func_nb(c, call_i, post_sim_lst):
            call_i[0] += 1
            post_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_row_func_nb(c, call_i, pre_row_lst):
            call_i[0] += 1
            pre_row_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_row_func_nb(c, call_i, post_row_lst):
            call_i[0] += 1
            post_row_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_segment_func_nb(c, call_i, pre_segment_lst):
            call_i[0] += 1
            pre_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_segment_func_nb(c, call_i, post_segment_lst):
            call_i[0] += 1
            post_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def order_func_nb(c, call_i, order_lst):
            call_i[0] += 1
            order_lst.append(call_i[0])
            return NoOrder

        @njit
        def post_order_func_nb(c, call_i, post_order_lst):
            call_i[0] += 1
            post_order_lst.append(call_i[0])

        sub_arg = vbt.RepEval('np.prod([target_shape[0], target_shape[1]])')

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_row_lst = List.empty_list(typeof(0))
        post_row_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, order_lst,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst),
            pre_row_func_nb=pre_row_func_nb, pre_row_args=(pre_row_lst,),
            post_row_func_nb=post_row_func_nb, post_row_args=(post_row_lst,),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst,),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst,),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst,),
            row_wise=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 62
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [62]
        assert list(pre_row_lst) == [2, 14, 26, 38, 50]
        assert list(post_row_lst) == [13, 25, 37, 49, 61]
        assert list(pre_segment_lst) == [3, 9, 15, 21, 27, 33, 39, 45, 51, 57]
        assert list(post_segment_lst) == [8, 12, 20, 24, 32, 36, 44, 48, 56, 60]
        assert list(order_lst) == [4, 6, 10, 16, 18, 22, 28, 30, 34, 40, 42, 46, 52, 54, 58]
        assert list(post_order_lst) == [5, 7, 11, 17, 19, 23, 29, 31, 35, 41, 43, 47, 53, 55, 59]

        segment_mask = np.array([
            [False, False],
            [False, True],
            [True, False],
            [True, True],
            [False, False],
        ])
        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_row_lst = List.empty_list(typeof(0))
        post_row_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, order_lst,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst),
            pre_row_func_nb=pre_row_func_nb, pre_row_args=(pre_row_lst,),
            post_row_func_nb=post_row_func_nb, post_row_args=(post_row_lst,),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst,),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst,),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst,),
            segment_mask=segment_mask, call_pre_segment=True, call_post_segment=True,
            row_wise=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 44
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [44]
        assert list(pre_row_lst) == [2, 8, 16, 26, 38]
        assert list(post_row_lst) == [7, 15, 25, 37, 43]
        assert list(pre_segment_lst) == [3, 5, 9, 11, 17, 23, 27, 33, 39, 41]
        assert list(post_segment_lst) == [4, 6, 10, 14, 22, 24, 32, 36, 40, 42]
        assert list(order_lst) == [12, 18, 20, 28, 30, 34]
        assert list(post_order_lst) == [13, 19, 21, 29, 31, 35]

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_row_lst = List.empty_list(typeof(0))
        post_row_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func_nb, order_lst,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst),
            pre_row_func_nb=pre_row_func_nb, pre_row_args=(pre_row_lst,),
            post_row_func_nb=post_row_func_nb, post_row_args=(post_row_lst,),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst,),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst,),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst,),
            segment_mask=segment_mask, call_pre_segment=False, call_post_segment=False,
            row_wise=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 32
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [32]
        assert list(pre_row_lst) == [2, 4, 10, 18, 30]
        assert list(post_row_lst) == [3, 9, 17, 29, 31]
        assert list(pre_segment_lst) == [5, 11, 19, 25]
        assert list(post_segment_lst) == [8, 16, 24, 28]
        assert list(order_lst) == [6, 12, 14, 20, 22, 26]
        assert list(post_order_lst) == [7, 13, 15, 21, 23, 27]

    def test_func_calls_row_wise_flexible(self):
        @njit
        def pre_sim_func_nb(c, call_i, pre_sim_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_sim_func_nb(c, call_i, post_sim_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_sim_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_row_func_nb(c, call_i, pre_row_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_row_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_row_func_nb(c, call_i, post_row_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_row_lst.append(call_i[0])
            return (call_i,)

        @njit
        def pre_segment_func_nb(c, call_i, pre_segment_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            pre_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def post_segment_func_nb(c, call_i, post_segment_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_segment_lst.append(call_i[0])
            return (call_i,)

        @njit
        def flex_order_func_nb(c, call_i, order_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            order_lst.append(call_i[0])
            col = c.from_col + c.call_idx
            if c.call_idx < c.group_len:
                return col, NoOrder
            return -1, NoOrder

        @njit
        def post_order_func_nb(c, call_i, post_order_lst, sub_arg):
            if sub_arg != 15:
                raise ValueError
            call_i[0] += 1
            post_order_lst.append(call_i[0])

        sub_arg = vbt.RepEval('np.prod([target_shape[0], target_shape[1]])')

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_row_lst = List.empty_list(typeof(0))
        post_row_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, flex_order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_row_func_nb=pre_row_func_nb, pre_row_args=(pre_row_lst, sub_arg),
            post_row_func_nb=post_row_func_nb, post_row_args=(post_row_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            row_wise=True, flexible=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 72
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [72]
        assert list(pre_row_lst) == [2, 16, 30, 44, 58]
        assert list(post_row_lst) == [15, 29, 43, 57, 71]
        assert list(pre_segment_lst) == [3, 10, 17, 24, 31, 38, 45, 52, 59, 66]
        assert list(post_segment_lst) == [9, 14, 23, 28, 37, 42, 51, 56, 65, 70]
        assert list(order_lst) == [
            4, 6, 8, 11, 13, 18, 20, 22, 25, 27, 32, 34, 36,
            39, 41, 46, 48, 50, 53, 55, 60, 62, 64, 67, 69
        ]
        assert list(post_order_lst) == [5, 7, 12, 19, 21, 26, 33, 35, 40, 47, 49, 54, 61, 63, 68]

        segment_mask = np.array([
            [False, False],
            [False, True],
            [True, False],
            [True, True],
            [False, False],
        ])
        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_row_lst = List.empty_list(typeof(0))
        post_row_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, flex_order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_row_func_nb=pre_row_func_nb, pre_row_args=(pre_row_lst, sub_arg),
            post_row_func_nb=post_row_func_nb, post_row_args=(post_row_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            segment_mask=segment_mask, call_pre_segment=True, call_post_segment=True,
            row_wise=True, flexible=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 48
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [48]
        assert list(pre_row_lst) == [2, 8, 17, 28, 42]
        assert list(post_row_lst) == [7, 16, 27, 41, 47]
        assert list(pre_segment_lst) == [3, 5, 9, 11, 18, 25, 29, 36, 43, 45]
        assert list(post_segment_lst) == [4, 6, 10, 15, 24, 26, 35, 40, 44, 46]
        assert list(order_lst) == [12, 14, 19, 21, 23, 30, 32, 34, 37, 39]
        assert list(post_order_lst) == [13, 20, 22, 31, 33, 38]

        call_i = np.array([0])
        pre_sim_lst = List.empty_list(typeof(0))
        post_sim_lst = List.empty_list(typeof(0))
        pre_row_lst = List.empty_list(typeof(0))
        post_row_lst = List.empty_list(typeof(0))
        pre_segment_lst = List.empty_list(typeof(0))
        post_segment_lst = List.empty_list(typeof(0))
        order_lst = List.empty_list(typeof(0))
        post_order_lst = List.empty_list(typeof(0))
        _ = vbt.Portfolio.from_order_func(
            price_wide, flex_order_func_nb, order_lst, sub_arg,
            group_by=np.array([0, 0, 1]),
            pre_sim_func_nb=pre_sim_func_nb, pre_sim_args=(call_i, pre_sim_lst, sub_arg),
            post_sim_func_nb=post_sim_func_nb, post_sim_args=(call_i, post_sim_lst, sub_arg),
            pre_row_func_nb=pre_row_func_nb, pre_row_args=(pre_row_lst, sub_arg),
            post_row_func_nb=post_row_func_nb, post_row_args=(post_row_lst, sub_arg),
            pre_segment_func_nb=pre_segment_func_nb, pre_segment_args=(pre_segment_lst, sub_arg),
            post_segment_func_nb=post_segment_func_nb, post_segment_args=(post_segment_lst, sub_arg),
            post_order_func_nb=post_order_func_nb, post_order_args=(post_order_lst, sub_arg),
            segment_mask=segment_mask, call_pre_segment=False, call_post_segment=False,
            row_wise=True, flexible=True, template_mapping=dict(np=np)
        )
        assert call_i[0] == 36
        assert list(pre_sim_lst) == [1]
        assert list(post_sim_lst) == [36]
        assert list(pre_row_lst) == [2, 4, 11, 20, 34]
        assert list(post_row_lst) == [3, 10, 19, 33, 35]
        assert list(pre_segment_lst) == [5, 12, 21, 28]
        assert list(post_segment_lst) == [9, 18, 27, 32]
        assert list(order_lst) == [6, 8, 13, 15, 17, 22, 24, 26, 29, 31]
        assert list(post_order_lst) == [7, 14, 16, 23, 25, 30]

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_max_orders(self, test_row_wise, test_flexible):
        order_func = flex_order_func_nb if test_flexible else order_func_nb
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(np.inf),
            row_wise=test_row_wise, flexible=test_flexible)
        _ = vbt.Portfolio.from_order_func(
            price_wide, order_func, np.asarray(np.inf),
            row_wise=test_row_wise, max_orders=15, flexible=test_flexible)
        with pytest.raises(Exception):
            _ = vbt.Portfolio.from_order_func(
                price_wide, order_func, np.asarray(np.inf),
                row_wise=test_row_wise, max_orders=14, flexible=test_flexible)

    @pytest.mark.parametrize("test_row_wise", [False, True])
    @pytest.mark.parametrize("test_flexible", [False, True])
    def test_max_logs(self, test_row_wise, test_flexible):
        log_order_func = log_flex_order_func_nb if test_flexible else log_order_func_nb
        _ = vbt.Portfolio.from_order_func(
            price_wide, log_order_func, np.asarray(np.inf),
            row_wise=test_row_wise, flexible=test_flexible)
        _ = vbt.Portfolio.from_order_func(
            price_wide, log_order_func, np.asarray(np.inf),
            row_wise=test_row_wise, max_logs=15, flexible=test_flexible)
        with pytest.raises(Exception):
            _ = vbt.Portfolio.from_order_func(
                price_wide, log_order_func, np.asarray(np.inf),
                row_wise=test_row_wise, max_logs=14, flexible=test_flexible)


# ############# Portfolio ############# #

price_na = pd.DataFrame({
    'a': [np.nan, 2., 3., 4., 5.],
    'b': [1., 2., np.nan, 4., 5.],
    'c': [1., 2., 3., 4., np.nan]
}, index=price.index)
order_size_new = pd.Series([1., 0.1, -1., -0.1, 1.])
directions = ['longonly', 'shortonly', 'both']
group_by = pd.Index(['first', 'first', 'second'], name='group')

pf = vbt.Portfolio.from_orders(
    price_na, order_size_new, size_type='amount', direction=directions,
    fees=0.01, fixed_fees=0.1, slippage=0.01, log=True,
    call_seq='reversed', group_by=None,
    init_cash=[100., 100., 100.], freq='1D', attach_call_seq=True
)  # independent

pf_grouped = vbt.Portfolio.from_orders(
    price_na, order_size_new, size_type='amount', direction=directions,
    fees=0.01, fixed_fees=0.1, slippage=0.01, log=True,
    call_seq='reversed', group_by=group_by, cash_sharing=False,
    init_cash=[100., 100., 100.], freq='1D', attach_call_seq=True
)  # grouped

pf_shared = vbt.Portfolio.from_orders(
    price_na, order_size_new, size_type='amount', direction=directions,
    fees=0.01, fixed_fees=0.1, slippage=0.01, log=True,
    call_seq='reversed', group_by=group_by, cash_sharing=True,
    init_cash=[200., 100.], freq='1D', attach_call_seq=True
)  # shared


class TestPortfolio:
    def test_config(self, tmp_path):
        pf2 = pf.copy()
        pf2._metrics = pf2._metrics.copy()
        pf2.metrics['hello'] = 'world'
        pf2._subplots = pf2.subplots.copy()
        pf2.subplots['hello'] = 'world'
        assert vbt.Portfolio.loads(pf2['a'].dumps()) == pf2['a']
        assert vbt.Portfolio.loads(pf2.dumps()) == pf2
        pf2.save(tmp_path / 'pf')
        assert vbt.Portfolio.load(tmp_path / 'pf') == pf2

    def test_wrapper(self):
        pd.testing.assert_index_equal(
            pf.wrapper.index,
            price_na.index
        )
        pd.testing.assert_index_equal(
            pf.wrapper.columns,
            price_na.columns
        )
        assert pf.wrapper.ndim == 2
        assert pf.wrapper.grouper.group_by is None
        assert pf.wrapper.grouper.allow_enable
        assert pf.wrapper.grouper.allow_disable
        assert pf.wrapper.grouper.allow_modify
        pd.testing.assert_index_equal(
            pf_grouped.wrapper.index,
            price_na.index
        )
        pd.testing.assert_index_equal(
            pf_grouped.wrapper.columns,
            price_na.columns
        )
        assert pf_grouped.wrapper.ndim == 2
        pd.testing.assert_index_equal(
            pf_grouped.wrapper.grouper.group_by,
            group_by
        )
        assert pf_grouped.wrapper.grouper.allow_enable
        assert pf_grouped.wrapper.grouper.allow_disable
        assert pf_grouped.wrapper.grouper.allow_modify
        pd.testing.assert_index_equal(
            pf_shared.wrapper.index,
            price_na.index
        )
        pd.testing.assert_index_equal(
            pf_shared.wrapper.columns,
            price_na.columns
        )
        assert pf_shared.wrapper.ndim == 2
        pd.testing.assert_index_equal(
            pf_shared.wrapper.grouper.group_by,
            group_by
        )
        assert not pf_shared.wrapper.grouper.allow_enable
        assert pf_shared.wrapper.grouper.allow_disable
        assert not pf_shared.wrapper.grouper.allow_modify

    def test_indexing(self):
        assert pf['a'].wrapper == pf.wrapper['a']
        assert pf['a'].orders == pf.orders['a']
        assert pf['a'].logs == pf.logs['a']
        assert pf['a'].init_cash == pf.init_cash['a']
        pd.testing.assert_series_equal(pf['a'].call_seq, pf.call_seq['a'])

        assert pf['c'].wrapper == pf.wrapper['c']
        assert pf['c'].orders == pf.orders['c']
        assert pf['c'].logs == pf.logs['c']
        assert pf['c'].init_cash == pf.init_cash['c']
        pd.testing.assert_series_equal(pf['c'].call_seq, pf.call_seq['c'])

        assert pf[['c']].wrapper == pf.wrapper[['c']]
        assert pf[['c']].orders == pf.orders[['c']]
        assert pf[['c']].logs == pf.logs[['c']]
        pd.testing.assert_series_equal(pf[['c']].init_cash, pf.init_cash[['c']])
        pd.testing.assert_frame_equal(pf[['c']].call_seq, pf.call_seq[['c']])

        assert pf_grouped['first'].wrapper == pf_grouped.wrapper['first']
        assert pf_grouped['first'].orders == pf_grouped.orders['first']
        assert pf_grouped['first'].logs == pf_grouped.logs['first']
        assert pf_grouped['first'].init_cash == pf_grouped.init_cash['first']
        pd.testing.assert_frame_equal(pf_grouped['first'].call_seq, pf_grouped.call_seq[['a', 'b']])

        assert pf_grouped[['first']].wrapper == pf_grouped.wrapper[['first']]
        assert pf_grouped[['first']].orders == pf_grouped.orders[['first']]
        assert pf_grouped[['first']].logs == pf_grouped.logs[['first']]
        pd.testing.assert_series_equal(
            pf_grouped[['first']].init_cash,
            pf_grouped.init_cash[['first']])
        pd.testing.assert_frame_equal(pf_grouped[['first']].call_seq, pf_grouped.call_seq[['a', 'b']])

        assert pf_grouped['second'].wrapper == pf_grouped.wrapper['second']
        assert pf_grouped['second'].orders == pf_grouped.orders['second']
        assert pf_grouped['second'].logs == pf_grouped.logs['second']
        assert pf_grouped['second'].init_cash == pf_grouped.init_cash['second']
        pd.testing.assert_series_equal(pf_grouped['second'].call_seq, pf_grouped.call_seq['c'])

        assert pf_grouped[['second']].orders == pf_grouped.orders[['second']]
        assert pf_grouped[['second']].wrapper == pf_grouped.wrapper[['second']]
        assert pf_grouped[['second']].orders == pf_grouped.orders[['second']]
        assert pf_grouped[['second']].logs == pf_grouped.logs[['second']]
        pd.testing.assert_series_equal(
            pf_grouped[['second']].init_cash,
            pf_grouped.init_cash[['second']])
        pd.testing.assert_frame_equal(pf_grouped[['second']].call_seq, pf_grouped.call_seq[['c']])

        assert pf_shared['first'].wrapper == pf_shared.wrapper['first']
        assert pf_shared['first'].orders == pf_shared.orders['first']
        assert pf_shared['first'].logs == pf_shared.logs['first']
        assert pf_shared['first'].init_cash == pf_shared.init_cash['first']
        pd.testing.assert_frame_equal(pf_shared['first'].call_seq, pf_shared.call_seq[['a', 'b']])

        assert pf_shared[['first']].orders == pf_shared.orders[['first']]
        assert pf_shared[['first']].wrapper == pf_shared.wrapper[['first']]
        assert pf_shared[['first']].orders == pf_shared.orders[['first']]
        assert pf_shared[['first']].logs == pf_shared.logs[['first']]
        pd.testing.assert_series_equal(
            pf_shared[['first']].init_cash,
            pf_shared.init_cash[['first']])
        pd.testing.assert_frame_equal(pf_shared[['first']].call_seq, pf_shared.call_seq[['a', 'b']])

        assert pf_shared['second'].wrapper == pf_shared.wrapper['second']
        assert pf_shared['second'].orders == pf_shared.orders['second']
        assert pf_shared['second'].logs == pf_shared.logs['second']
        assert pf_shared['second'].init_cash == pf_shared.init_cash['second']
        pd.testing.assert_series_equal(pf_shared['second'].call_seq, pf_shared.call_seq['c'])

        assert pf_shared[['second']].wrapper == pf_shared.wrapper[['second']]
        assert pf_shared[['second']].orders == pf_shared.orders[['second']]
        assert pf_shared[['second']].logs == pf_shared.logs[['second']]
        pd.testing.assert_series_equal(
            pf_shared[['second']].init_cash,
            pf_shared.init_cash[['second']])
        pd.testing.assert_frame_equal(pf_shared[['second']].call_seq, pf_shared.call_seq[['c']])

    def test_regroup(self):
        assert pf.regroup(None) == pf
        assert pf.regroup(False) == pf
        assert pf.regroup(group_by) != pf
        pd.testing.assert_index_equal(pf.regroup(group_by).wrapper.grouper.group_by, group_by)
        assert pf_grouped.regroup(None) == pf_grouped
        assert pf_grouped.regroup(False) != pf_grouped
        assert pf_grouped.regroup(False).wrapper.grouper.group_by is None
        assert pf_grouped.regroup(group_by) == pf_grouped
        assert pf_shared.regroup(None) == pf_shared
        with pytest.raises(Exception):
            _ = pf_shared.regroup(False)
        assert pf_shared.regroup(group_by) == pf_shared

    def test_cash_sharing(self):
        assert not pf.cash_sharing
        assert not pf_grouped.cash_sharing
        assert pf_shared.cash_sharing

    def test_call_seq(self):
        pd.testing.assert_frame_equal(
            pf.call_seq,
            pd.DataFrame(
                np.array([
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf_grouped.call_seq,
            pd.DataFrame(
                np.array([
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf_shared.call_seq,
            pd.DataFrame(
                np.array([
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )

    def test_orders(self):
        record_arrays_close(
            pf.orders.values,
            np.array([
                (0, 0, 1, 0.1, 2.02, 0.10202, 0), (1, 0, 2, 0.1, 2.9699999999999998, 0.10297, 1),
                (2, 0, 4, 1.0, 5.05, 0.1505, 0), (3, 1, 0, 1.0, 0.99, 0.10990000000000001, 1),
                (4, 1, 1, 0.1, 1.98, 0.10198, 1), (5, 1, 3, 0.1, 4.04, 0.10404000000000001, 0),
                (6, 1, 4, 1.0, 4.95, 0.14950000000000002, 1), (7, 2, 0, 1.0, 1.01, 0.1101, 0),
                (8, 2, 1, 0.1, 2.02, 0.10202, 0), (9, 2, 2, 1.0, 2.9699999999999998, 0.1297, 1),
                (10, 2, 3, 0.1, 3.96, 0.10396000000000001, 1)
            ], dtype=order_dt)
        )
        result = pd.Series(
            np.array([3, 4, 4]),
            index=price_na.columns
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.orders.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_orders(group_by=False).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.get_orders(group_by=False).count(),
            result
        )
        result = pd.Series(
            np.array([7, 4]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.get_orders(group_by=group_by).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.orders.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.orders.count(),
            result
        )

    def test_logs(self):
        record_arrays_close(
            pf.logs.values,
            np.array([
                (0, 0, 0, 0, 100.0, 0.0, 0.0, 100.0, np.nan, 100.0, 1.0, np.nan, 0, 0, 0.01, 0.1,
                 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 100.0, 0.0, 0.0, 100.0,
                 np.nan, 100.0, np.nan, np.nan, np.nan, -1, 1, 1, -1),
                (1, 0, 0, 1, 100.0, 0.0, 0.0, 100.0, 2.0, 100.0, 0.1, 2.0, 0, 0, 0.01, 0.1,
                 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 99.69598, 0.1, 0.0,
                 99.69598, 2.0, 100.0, 0.1, 2.02, 0.10202, 0, 0, -1, 0),
                (2, 0, 0, 2, 99.69598, 0.1, 0.0, 99.69598, 3.0, 99.99598, -1.0, 3.0, 0,
                 0, 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True,
                 99.89001, 0.0, 0.0, 99.89001, 3.0, 99.99598, 0.1, 2.9699999999999998, 0.10297, 1, 0, -1, 1),
                (3, 0, 0, 3, 99.89001, 0.0, 0.0, 99.89001, 4.0, 99.89001, -0.1, 4.0, 0, 0,
                 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 99.89001,
                 0.0, 0.0, 99.89001, 4.0, 99.89001, np.nan, np.nan, np.nan, -1, 2, 8, -1),
                (4, 0, 0, 4, 99.89001, 0.0, 0.0, 99.89001, 5.0, 99.89001, 1.0, 5.0, 0, 0,
                 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 94.68951,
                 1.0, 0.0, 94.68951, 5.0, 99.89001, 1.0, 5.05, 0.1505, 0, 0, -1, 2),
                (5, 1, 1, 0, 100.0, 0.0, 0.0, 100.0, 1.0, 100.0, 1.0, 1.0, 0, 1, 0.01, 0.1, 0.01,
                 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 100.8801, -1.0, 0.99, 98.9001,
                 1.0, 100.0, 1.0, 0.99, 0.10990000000000001, 1, 0, -1, 3),
                (6, 1, 1, 1, 100.8801, -1.0, 0.99, 98.9001, 2.0, 98.8801, 0.1, 2.0, 0, 1, 0.01,
                 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 100.97612, -1.1,
                 1.188, 98.60011999999999, 2.0, 98.8801, 0.1, 1.98, 0.10198, 1, 0, -1, 4),
                (7, 1, 1, 2, 100.97612, -1.1, 1.188, 98.60011999999999, 2.0, 98.77611999999999,
                 -1.0, np.nan, 0, 1, 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 100.97612,
                 -1.1, 1.188, 98.60011999999999, 2.0, 98.77611999999999, np.nan, np.nan, np.nan, -1, 1, 1, -1),
                (8, 1, 1, 3, 100.97612, -1.1, 1.188, 98.60011999999999, 4.0, 96.57611999999999, -0.1, 4.0,
                 0, 1, 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 100.46808, -1.0,
                 1.08, 98.30807999999999, 4.0, 96.57611999999999, 0.1, 4.04, 0.10404000000000001, 0, 0, -1, 5),
                (9, 1, 1, 4, 100.46808, -1.0, 1.08, 98.30807999999999, 5.0, 95.46808, 1.0, 5.0, 0, 1,
                 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 105.26858, -2.0, 6.03,
                 93.20857999999998, 5.0, 95.46808, 1.0, 4.95, 0.14950000000000002, 1, 0, -1, 6),
                (10, 2, 2, 0, 100.0, 0.0, 0.0, 100.0, 1.0, 100.0, 1.0, 1.0, 0, 2, 0.01, 0.1, 0.01, 1e-08,
                 np.inf, np.nan, 0.0, False, True, False, True, 98.8799, 1.0, 0.0, 98.8799, 1.0, 100.0, 1.0,
                 1.01, 0.1101, 0, 0, -1, 7),
                (11, 2, 2, 1, 98.8799, 1.0, 0.0, 98.8799, 2.0, 100.8799, 0.1, 2.0, 0, 2, 0.01,
                 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True, 98.57588000000001,
                 1.1, 0.0, 98.57588000000001, 2.0, 100.8799, 0.1, 2.02, 0.10202, 0, 0, -1, 8),
                (12, 2, 2, 2, 98.57588000000001, 1.1, 0.0, 98.57588000000001, 3.0, 101.87588000000001,
                 -1.0, 3.0, 0, 2, 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True,
                 101.41618000000001, 0.10000000000000009, 0.0, 101.41618000000001, 3.0, 101.87588000000001,
                 1.0, 2.9699999999999998, 0.1297, 1, 0, -1, 9),
                (13, 2, 2, 3, 101.41618000000001, 0.10000000000000009, 0.0, 101.41618000000001, 4.0,
                 101.81618000000002, -0.1, 4.0, 0, 2, 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False,
                 True, False, True, 101.70822000000001, 0.0, 0.0, 101.70822000000001, 4.0,
                 101.81618000000002, 0.1, 3.96, 0.10396000000000001, 1, 0, -1, 10),
                (14, 2, 2, 4, 101.70822000000001, 0.0, 0.0, 101.70822000000001, 4.0, 101.70822000000001,
                 1.0, np.nan, 0, 2, 0.01, 0.1, 0.01, 1e-08, np.inf, np.nan, 0.0, False, True, False, True,
                 101.70822000000001, 0.0, 0.0, 101.70822000000001, 4.0, 101.70822000000001, np.nan,
                 np.nan, np.nan, -1, 1, 1, -1)
            ], dtype=log_dt)
        )
        result = pd.Series(
            np.array([5, 5, 5]),
            index=price_na.columns
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.logs.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_logs(group_by=False).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.get_logs(group_by=False).count(),
            result
        )
        result = pd.Series(
            np.array([10, 5]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.get_logs(group_by=group_by).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.logs.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.logs.count(),
            result
        )

    def test_entry_trades(self):
        record_arrays_close(
            pf.entry_trades.values,
            np.array([
                (0, 0, 0.1, 1, 2.02, 0.10202, 2, 2.9699999999999998, 0.10297,
                 -0.10999000000000003, -0.5445049504950497, 0, 1, 0),
                (1, 0, 1.0, 4, 5.05, 0.1505, 4, 5.0, 0.0, -0.20049999999999982, -0.03970297029702967, 0, 0, 1),
                (2, 1, 1.0, 0, 0.99, 0.10990000000000001, 4, 4.954285714285714,
                 0.049542857142857145, -4.12372857142857, -4.165382395382394, 1, 0, 2),
                (3, 1, 0.1, 1, 1.98, 0.10198, 4, 4.954285714285714, 0.004954285714285714,
                 -0.4043628571428571, -2.0422366522366517, 1, 0, 2),
                (4, 1, 1.0, 4, 4.95, 0.14950000000000002, 4, 4.954285714285714,
                 0.049542857142857145, -0.20332857142857072, -0.04107647907647893, 1, 0, 2),
                (5, 2, 1.0, 0, 1.01, 0.1101, 3, 3.0599999999999996, 0.21241818181818184,
                 1.727481818181818, 1.71037803780378, 0, 1, 3),
                (6, 2, 0.1, 1, 2.02, 0.10202, 3, 3.0599999999999996, 0.021241818181818185,
                 -0.019261818181818203, -0.09535553555355546, 0, 1, 3)
            ], dtype=trade_dt)
        )
        result = pd.Series(
            np.array([2, 3, 2]),
            index=price_na.columns
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.entry_trades.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_entry_trades(group_by=False).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.get_entry_trades(group_by=False).count(),
            result
        )
        result = pd.Series(
            np.array([5, 2]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.get_entry_trades(group_by=group_by).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.entry_trades.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.entry_trades.count(),
            result
        )

    def test_exit_trades(self):
        record_arrays_close(
            pf.exit_trades.values,
            np.array([
                (0, 0, 0.1, 1, 2.02, 0.10202, 2, 2.9699999999999998, 0.10297,
                 -0.10999000000000003, -0.5445049504950497, 0, 1, 0),
                (1, 0, 1.0, 4, 5.05, 0.1505, 4, 5.0, 0.0,
                 -0.20049999999999982, -0.03970297029702967, 0, 0, 1),
                (2, 1, 0.1, 0, 1.0799999999999998, 0.019261818181818182,
                 3, 4.04, 0.10404000000000001, -0.4193018181818182, -3.882424242424243, 1, 1, 2),
                (3, 1, 2.0, 0, 3.015, 0.3421181818181819, 4, 5.0, 0.0,
                 -4.312118181818182, -0.7151108095884214, 1, 0, 2),
                (4, 2, 1.0, 0, 1.1018181818181818, 0.19283636363636364, 2,
                 2.9699999999999998, 0.1297, 1.5456454545454543, 1.4028135313531351, 0, 1, 3),
                (5, 2, 0.10000000000000009, 0, 1.1018181818181818, 0.019283636363636378,
                 3, 3.96, 0.10396000000000001, 0.1625745454545457, 1.4755115511551162, 0, 1, 3)
            ], dtype=trade_dt)
        )
        result = pd.Series(
            np.array([2, 2, 2]),
            index=price_na.columns
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.exit_trades.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_exit_trades(group_by=False).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.get_exit_trades(group_by=False).count(),
            result
        )
        result = pd.Series(
            np.array([4, 2]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.get_exit_trades(group_by=group_by).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.exit_trades.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.exit_trades.count(),
            result
        )

    def test_positions(self):
        record_arrays_close(
            pf.positions.values,
            np.array([
                (0, 0, 0.1, 1, 2.02, 0.10202, 2, 2.9699999999999998,
                 0.10297, -0.10999000000000003, -0.5445049504950497, 0, 1, 0),
                (1, 0, 1.0, 4, 5.05, 0.1505, 4, 5.0, 0.0,
                 -0.20049999999999982, -0.03970297029702967, 0, 0, 1),
                (2, 1, 2.1, 0, 2.9228571428571426, 0.36138000000000003, 4, 4.954285714285714,
                 0.10404000000000001, -4.731420000000001, -0.7708406647116326, 1, 0, 2),
                (3, 2, 1.1, 0, 1.1018181818181818, 0.21212000000000003, 3,
                 3.06, 0.23366000000000003, 1.7082200000000003, 1.4094224422442245, 0, 1, 3)
            ], dtype=trade_dt)
        )
        result = pd.Series(
            np.array([2, 1, 1]),
            index=price_na.columns
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.positions.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_positions(group_by=False).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.get_positions(group_by=False).count(),
            result
        )
        result = pd.Series(
            np.array([3, 1]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.get_positions(group_by=group_by).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.positions.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.positions.count(),
            result
        )

    def test_drawdowns(self):
        record_arrays_close(
            pf.drawdowns.values,
            np.array([
                (0, 0, 0, 1, 4, 4, 100.0, 99.68951, 99.68951, 0),
                (1, 1, 0, 1, 4, 4, 99.8801, 95.26858, 95.26858, 0),
                (2, 2, 2, 3, 3, 4, 101.71618000000001, 101.70822000000001, 101.70822000000001, 0)
            ], dtype=drawdown_dt)
        )
        result = pd.Series(
            np.array([1, 1, 1]),
            index=price_na.columns
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.drawdowns.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_drawdowns(group_by=False).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.get_drawdowns(group_by=False).count(),
            result
        )
        result = pd.Series(
            np.array([1, 1]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('count')
        pd.testing.assert_series_equal(
            pf.get_drawdowns(group_by=group_by).count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.drawdowns.count(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.drawdowns.count(),
            result
        )

    def test_close(self):
        pd.testing.assert_frame_equal(pf.close, price_na)
        pd.testing.assert_frame_equal(pf_grouped.close, price_na)
        pd.testing.assert_frame_equal(pf_shared.close, price_na)

    def test_get_filled_close(self):
        pd.testing.assert_frame_equal(
            pf.get_filled_close(),
            price_na.ffill().bfill()
        )

    def test_asset_flow(self):
        pd.testing.assert_frame_equal(
            pf.asset_flow(direction='longonly'),
            pd.DataFrame(
                np.array([
                    [0., 0., 1.],
                    [0.1, 0., 0.1],
                    [-0.1, 0., -1.],
                    [0., 0., -0.1],
                    [1., 0., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf.asset_flow(direction='shortonly'),
            pd.DataFrame(
                np.array([
                    [0., 1., 0.],
                    [0., 0.1, 0.],
                    [0., 0., 0.],
                    [0., -0.1, 0.],
                    [0., 1., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [0., -1., 1.],
                [0.1, -0.1, 0.1],
                [-0.1, 0., -1.],
                [0., 0.1, -0.1],
                [1., -1., 0.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.asset_flow(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.asset_flow(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.asset_flow(),
            result
        )

    def test_assets(self):
        pd.testing.assert_frame_equal(
            pf.assets(direction='longonly'),
            pd.DataFrame(
                np.array([
                    [0., 0., 1.],
                    [0.1, 0., 1.1],
                    [0., 0., 0.1],
                    [0., 0., 0.],
                    [1., 0., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf.assets(direction='shortonly'),
            pd.DataFrame(
                np.array([
                    [0., 1., 0.],
                    [0., 1.1, 0.],
                    [0., 1.1, 0.],
                    [0., 1., 0.],
                    [0., 2., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [0., -1., 1.],
                [0.1, -1.1, 1.1],
                [0., -1.1, 0.1],
                [0., -1., 0.],
                [1., -2., 0.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.assets(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.assets(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.assets(),
            result
        )

    def test_position_mask(self):
        pd.testing.assert_frame_equal(
            pf.position_mask(direction='longonly'),
            pd.DataFrame(
                np.array([
                    [False, False, True],
                    [True, False, True],
                    [False, False, True],
                    [False, False, False],
                    [True, False, False]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf.position_mask(direction='shortonly'),
            pd.DataFrame(
                np.array([
                    [False, True, False],
                    [False, True, False],
                    [False, True, False],
                    [False, True, False],
                    [False, True, False]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [False, True, True],
                [True, True, True],
                [False, True, True],
                [False, True, False],
                [True, True, False]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.position_mask(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.position_mask(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.position_mask(group_by=False),
            result
        )
        result = pd.DataFrame(
            np.array([
                [True, True],
                [True, True],
                [True, True],
                [True, False],
                [True, False]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.position_mask(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.position_mask(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.position_mask(),
            result
        )

    def test_position_coverage(self):
        pd.testing.assert_series_equal(
            pf.position_coverage(direction='longonly'),
            pd.Series(np.array([0.4, 0., 0.6]), index=price_na.columns).rename('position_coverage')
        )
        pd.testing.assert_series_equal(
            pf.position_coverage(direction='shortonly'),
            pd.Series(np.array([0., 1., 0.]), index=price_na.columns).rename('position_coverage')
        )
        result = pd.Series(np.array([0.4, 1., 0.6]), index=price_na.columns).rename('position_coverage')
        pd.testing.assert_series_equal(
            pf.position_coverage(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.position_coverage(group_by=False),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.position_coverage(group_by=False),
            result
        )
        result = pd.Series(
            np.array([0.7, 0.6]),
            pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('position_coverage')
        pd.testing.assert_series_equal(
            pf.position_coverage(group_by=group_by),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.position_coverage(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.position_coverage(),
            result
        )

    def test_cash_flow(self):
        pd.testing.assert_frame_equal(
            pf.cash_flow(free=True),
            pd.DataFrame(
                np.array([
                    [0.0, -1.0998999999999999, -1.1201],
                    [-0.30402, -0.2999800000000002, -0.3040200000000002],
                    [0.19402999999999998, 0.0, 2.8402999999999996],
                    [0.0, -0.2920400000000002, 0.29204000000000035],
                    [-5.2005, -5.0995, 0.0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [0., 0.8801, -1.1201],
                [-0.30402, 0.09602, -0.30402],
                [0.19403, 0., 2.8403],
                [0., -0.50804, 0.29204],
                [-5.2005, 4.8005, 0.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.cash_flow(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.cash_flow(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.cash_flow(group_by=False),
            result
        )
        result = pd.DataFrame(
            np.array([
                [0.8801, -1.1201],
                [-0.208, -0.30402],
                [0.19403, 2.8403],
                [-0.50804, 0.29204],
                [-0.4, 0.]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.cash_flow(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.cash_flow(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.cash_flow(),
            result
        )

    def test_init_cash(self):
        pd.testing.assert_series_equal(
            pf.init_cash,
            pd.Series(np.array([100., 100., 100.]), index=price_na.columns).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            pf_grouped.get_init_cash(group_by=False),
            pd.Series(np.array([100., 100., 100.]), index=price_na.columns).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            pf_shared.get_init_cash(group_by=False),
            pd.Series(np.array([200., 200., 100.]), index=price_na.columns).rename('init_cash')
        )
        result = pd.Series(
            np.array([200., 100.]),
            pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('init_cash')
        pd.testing.assert_series_equal(
            pf.get_init_cash(group_by=group_by),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.init_cash,
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.init_cash,
            result
        )
        pd.testing.assert_series_equal(
            vbt.Portfolio.from_orders(
                price_na, 1000., init_cash=InitCashMode.Auto, group_by=None).init_cash,
            pd.Series(
                np.array([14000., 12000., 10000.]),
                index=price_na.columns
            ).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            vbt.Portfolio.from_orders(
                price_na, 1000., init_cash=InitCashMode.Auto, group_by=group_by).init_cash,
            pd.Series(
                np.array([26000.0, 10000.0]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            vbt.Portfolio.from_orders(
                price_na, 1000., init_cash=InitCashMode.Auto, group_by=group_by, cash_sharing=True).init_cash,
            pd.Series(
                np.array([26000.0, 10000.0]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            vbt.Portfolio.from_orders(
                price_na, 1000., init_cash=InitCashMode.AutoAlign, group_by=None).init_cash,
            pd.Series(
                np.array([14000., 14000., 14000.]),
                index=price_na.columns
            ).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            vbt.Portfolio.from_orders(
                price_na, 1000., init_cash=InitCashMode.AutoAlign, group_by=group_by).init_cash,
            pd.Series(
                np.array([26000.0, 26000.0]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('init_cash')
        )
        pd.testing.assert_series_equal(
            vbt.Portfolio.from_orders(
                price_na, 1000., init_cash=InitCashMode.AutoAlign, group_by=group_by, cash_sharing=True).init_cash,
            pd.Series(
                np.array([26000.0, 26000.0]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('init_cash')
        )

    def test_cash(self):
        pd.testing.assert_frame_equal(
            pf.cash(free=True),
            pd.DataFrame(
                np.array([
                    [100.0, 98.9001, 98.8799],
                    [99.69598, 98.60011999999999, 98.57588000000001],
                    [99.89001, 98.60011999999999, 101.41618000000001],
                    [99.89001, 98.30807999999999, 101.70822000000001],
                    [94.68951, 93.20857999999998, 101.70822000000001]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [100., 100.8801, 98.8799],
                [99.69598, 100.97612, 98.57588],
                [99.89001, 100.97612, 101.41618],
                [99.89001, 100.46808, 101.70822],
                [94.68951, 105.26858, 101.70822]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.cash(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.cash(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.cash(group_by=False),
            pd.DataFrame(
                np.array([
                    [200., 200.8801, 98.8799],
                    [199.69598, 200.97612, 98.57588],
                    [199.89001, 200.97612, 101.41618],
                    [199.89001, 200.46808, 101.70822],
                    [194.68951, 205.26858, 101.70822]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf_shared.cash(group_by=False, in_sim_order=True),
            pd.DataFrame(
                np.array([
                    [200.8801, 200.8801, 98.8799],
                    [200.6721, 200.97612, 98.57588000000001],
                    [200.86613, 200.6721, 101.41618000000001],
                    [200.35809, 200.35809, 101.70822000000001],
                    [199.95809, 205.15859, 101.70822000000001]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [200.8801, 98.8799],
                [200.6721, 98.57588],
                [200.86613, 101.41618],
                [200.35809, 101.70822],
                [199.95809, 101.70822]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.cash(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.cash(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.cash(),
            result
        )

    def test_asset_value(self):
        pd.testing.assert_frame_equal(
            pf.asset_value(direction='longonly'),
            pd.DataFrame(
                np.array([
                    [0., 0., 1.],
                    [0.2, 0., 2.2],
                    [0., 0., 0.3],
                    [0., 0., 0.],
                    [5., 0., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf.asset_value(direction='shortonly'),
            pd.DataFrame(
                np.array([
                    [0., 1., 0.],
                    [0., 2.2, 0.],
                    [0., 2.2, 0.],
                    [0., 4., 0.],
                    [0., 10., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [0., -1., 1.],
                [0.2, -2.2, 2.2],
                [0., -2.2, 0.3],
                [0., -4., 0.],
                [5., -10., 0.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.asset_value(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.asset_value(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.asset_value(group_by=False),
            result
        )
        result = pd.DataFrame(
            np.array([
                [-1., 1.],
                [-2., 2.2],
                [-2.2, 0.3],
                [-4., 0.],
                [-5., 0.]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.asset_value(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.asset_value(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.asset_value(),
            result
        )

    def test_gross_exposure(self):
        pd.testing.assert_frame_equal(
            pf.gross_exposure(direction='longonly'),
            pd.DataFrame(
                np.array([
                    [0., 0., 0.01001202],
                    [0.00200208, 0., 0.02183062],
                    [0., 0., 0.00294938],
                    [0., 0., 0.],
                    [0.05015573, 0., 0.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf.gross_exposure(direction='shortonly'),
            pd.DataFrame(
                np.array([
                    [0.0, 0.01000999998999, 0.0],
                    [0.0, 0.021825370842812494, 0.0],
                    [0.0, 0.021825370842812494, 0.0],
                    [0.0, 0.03909759620159034, 0.0],
                    [0.0, 0.09689116931945001, 0.0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [0.0, -0.010214494162927312, 0.010012024441354066],
                [0.00200208256628545, -0.022821548354919067, 0.021830620581035857],
                [0.0, -0.022821548354919067, 0.002949383274126105],
                [0.0, -0.04241418126633477, 0.0],
                [0.050155728521486365, -0.12017991413866216, 0.0]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.gross_exposure(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.gross_exposure(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.gross_exposure(group_by=False),
            pd.DataFrame(
                np.array([
                    [0.0, -0.00505305454620791, 0.010012024441354066],
                    [0.0010005203706447724, -0.011201622483733716, 0.021830620581035857],
                    [0.0, -0.011201622483733716, 0.002949383274126105],
                    [0.0, -0.020585865497718882, 0.0],
                    [0.025038871596209537, -0.0545825965137659, 0.0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [-0.00505305454620791, 0.010012024441354066],
                [-0.010188689433972452, 0.021830620581035857],
                [-0.0112078992458765, 0.002949383274126105],
                [-0.02059752492931316, 0.0],
                [-0.027337628293439265, 0.0]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.gross_exposure(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.gross_exposure(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.gross_exposure(),
            result
        )

    def test_net_exposure(self):
        result = pd.DataFrame(
            np.array([
                [0.0, -0.01000999998999, 0.010012024441354066],
                [0.00200208256628545, -0.021825370842812494, 0.021830620581035857],
                [0.0, -0.021825370842812494, 0.002949383274126105],
                [0.0, -0.03909759620159034, 0.0],
                [0.050155728521486365, -0.09689116931945001, 0.0]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.net_exposure(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.net_exposure(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.net_exposure(group_by=False),
            pd.DataFrame(
                np.array([
                    [0.0, -0.005002498748124688, 0.010012024441354066],
                    [0.0010005203706447724, -0.010956168751293576, 0.021830620581035857],
                    [0.0, -0.010956168751293576, 0.002949383274126105],
                    [0.0, -0.019771825228137207, 0.0],
                    [0.025038871596209537, -0.049210520540028384, 0.0]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [-0.005002498748124688, 0.010012024441354066],
                [-0.009965205542937988, 0.021830620581035857],
                [-0.010962173376438594, 0.002949383274126105],
                [-0.019782580537729116, 0.0],
                [-0.0246106361476199, 0.0]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.net_exposure(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.net_exposure(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.net_exposure(),
            result
        )

    def test_value(self):
        result = pd.DataFrame(
            np.array([
                [100., 99.8801, 99.8799],
                [99.89598, 98.77612, 100.77588],
                [99.89001, 98.77612, 101.71618],
                [99.89001, 96.46808, 101.70822],
                [99.68951, 95.26858, 101.70822]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.value(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.value(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.value(group_by=False),
            pd.DataFrame(
                np.array([
                    [200., 199.8801, 99.8799],
                    [199.89598, 198.77612, 100.77588],
                    [199.89001, 198.77612, 101.71618],
                    [199.89001, 196.46808, 101.70822],
                    [199.68951, 195.26858, 101.70822]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf_shared.value(group_by=False, in_sim_order=True),
            pd.DataFrame(
                np.array([
                    [199.8801, 199.8801, 99.8799],
                    [198.6721, 198.77612000000002, 100.77588000000002],
                    [198.66613, 198.6721, 101.71618000000001],
                    [196.35809, 196.35809, 101.70822000000001],
                    [194.95809, 195.15859, 101.70822000000001]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [199.8801, 99.8799],
                [198.6721, 100.77588],
                [198.66613, 101.71618],
                [196.35809, 101.70822],
                [194.95809, 101.70822]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.value(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.value(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.value(),
            result
        )

    def test_total_profit(self):
        result = pd.Series(
            np.array([-0.31049, -4.73142, 1.70822]),
            index=price_na.columns
        ).rename('total_profit')
        pd.testing.assert_series_equal(
            pf.total_profit(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.total_profit(group_by=False),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.total_profit(group_by=False),
            result
        )
        result = pd.Series(
            np.array([-5.04191, 1.70822]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('total_profit')
        pd.testing.assert_series_equal(
            pf.total_profit(group_by=group_by),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.total_profit(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.total_profit(),
            result
        )

    def test_final_value(self):
        result = pd.Series(
            np.array([99.68951, 95.26858, 101.70822]),
            index=price_na.columns
        ).rename('final_value')
        pd.testing.assert_series_equal(
            pf.final_value(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.final_value(group_by=False),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.final_value(group_by=False),
            pd.Series(
                np.array([199.68951, 195.26858, 101.70822]),
                index=price_na.columns
            ).rename('final_value')
        )
        result = pd.Series(
            np.array([194.95809, 101.70822]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('final_value')
        pd.testing.assert_series_equal(
            pf.final_value(group_by=group_by),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.final_value(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.final_value(),
            result
        )

    def test_total_return(self):
        result = pd.Series(
            np.array([-0.0031049, -0.0473142, 0.0170822]),
            index=price_na.columns
        ).rename('total_return')
        pd.testing.assert_series_equal(
            pf.total_return(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.total_return(group_by=False),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.total_return(group_by=False),
            pd.Series(
                np.array([-0.00155245, -0.0236571, 0.0170822]),
                index=price_na.columns
            ).rename('total_return')
        )
        result = pd.Series(
            np.array([-0.02520955, 0.0170822]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('total_return')
        pd.testing.assert_series_equal(
            pf.total_return(group_by=group_by),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.total_return(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.total_return(),
            result
        )

    def test_returns(self):
        result = pd.DataFrame(
            np.array([
                [0.00000000e+00, -1.19900000e-03, -1.20100000e-03],
                [-1.04020000e-03, -1.10530526e-02, 8.97057366e-03],
                [-5.97621646e-05, 0.0, 9.33060570e-03],
                [0.00000000e+00, -0.023366376407576966, -7.82569695e-05],
                [-2.00720773e-03, -1.24341648e-02, 0.00000000e+00]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.returns(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.returns(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.returns(group_by=False),
            pd.DataFrame(
                np.array([
                    [0.00000000e+00, -5.99500000e-04, -1.20100000e-03],
                    [-5.20100000e-04, -5.52321117e-03, 8.97057366e-03],
                    [-2.98655331e-05, 0.0, 9.33060570e-03],
                    [0.00000000e+00, -0.011611253907159497, -7.82569695e-05],
                    [-1.00305163e-03, -6.10531746e-03, 0.00000000e+00]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_frame_equal(
            pf_shared.returns(group_by=False, in_sim_order=True),
            pd.DataFrame(
                np.array([
                    [0.0, -0.0005995000000000062, -1.20100000e-03],
                    [-0.0005233022960706736, -0.005523211165093367, 8.97057366e-03],
                    [-3.0049513746473233e-05, 0.0, 9.33060570e-03],
                    [0.0, -0.011617682390048093, -7.82569695e-05],
                    [-0.0010273695869600474, -0.0061087373583639994, 0.00000000e+00]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [-5.99500000e-04, -1.20100000e-03],
                [-6.04362315e-03, 8.97057366e-03],
                [-3.0049513746473233e-05, 9.33060570e-03],
                [-0.011617682390048093, -7.82569695e-05],
                [-7.12983101e-03, 0.00000000e+00]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.returns(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.returns(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.returns(),
            result
        )

    def test_asset_returns(self):
        result = pd.DataFrame(
            np.array([
                [0., -np.inf, -np.inf],
                [-np.inf, -1.10398, 0.89598],
                [-0.02985, 0.0, 0.42740909],
                [0., -1.0491090909090908, -0.02653333],
                [-np.inf, -0.299875, 0.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.asset_returns(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.asset_returns(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.asset_returns(group_by=False),
            result
        )
        result = pd.DataFrame(
            np.array([
                [-np.inf, -np.inf],
                [-1.208, 0.89598],
                [-0.0029850000000000154, 0.42740909],
                [-1.0491090909090908, -0.02653333],
                [-0.35, 0.]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.asset_returns(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.asset_returns(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.asset_returns(),
            result
        )

    def test_benchmark_value(self):
        result = pd.DataFrame(
            np.array([
                [100., 100., 100.],
                [100., 200., 200.],
                [150., 200., 300.],
                [200., 400., 400.],
                [250., 500., 400.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.benchmark_value(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.benchmark_value(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.benchmark_value(group_by=False),
            pd.DataFrame(
                np.array([
                    [200., 200., 100.],
                    [200., 400., 200.],
                    [300., 400., 300.],
                    [400., 800., 400.],
                    [500., 1000., 400.]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        result = pd.DataFrame(
            np.array([
                [200., 100.],
                [300., 200.],
                [350., 300.],
                [600., 400.],
                [750., 400.]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.benchmark_value(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.benchmark_value(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.benchmark_value(),
            result
        )

    def test_benchmark_returns(self):
        result = pd.DataFrame(
            np.array([
                [0., 0., 0.],
                [0., 1., 1.],
                [0.5, 0., 0.5],
                [0.33333333, 1., 0.33333333],
                [0.25, 0.25, 0.]
            ]),
            index=price_na.index,
            columns=price_na.columns
        )
        pd.testing.assert_frame_equal(
            pf.benchmark_returns(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.benchmark_returns(group_by=False),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.benchmark_returns(group_by=False),
            result
        )
        result = pd.DataFrame(
            np.array([
                [0., 0.],
                [0.5, 1.],
                [0.16666667, 0.5],
                [0.71428571, 0.33333333],
                [0.25, 0.]
            ]),
            index=price_na.index,
            columns=pd.Index(['first', 'second'], dtype='object', name='group')
        )
        pd.testing.assert_frame_equal(
            pf.benchmark_returns(group_by=group_by),
            result
        )
        pd.testing.assert_frame_equal(
            pf_grouped.benchmark_returns(),
            result
        )
        pd.testing.assert_frame_equal(
            pf_shared.benchmark_returns(),
            result
        )

    def test_total_benchmark_return(self):
        result = pd.Series(
            np.array([1.5, 4., 3.]),
            index=price_na.columns
        ).rename('total_benchmark_return')
        pd.testing.assert_series_equal(
            pf.total_benchmark_return(),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.total_benchmark_return(group_by=False),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.total_benchmark_return(group_by=False),
            result
        )
        result = pd.Series(
            np.array([2.75, 3.]),
            index=pd.Index(['first', 'second'], dtype='object', name='group')
        ).rename('total_benchmark_return')
        pd.testing.assert_series_equal(
            pf.total_benchmark_return(group_by=group_by),
            result
        )
        pd.testing.assert_series_equal(
            pf_grouped.total_benchmark_return(),
            result
        )
        pd.testing.assert_series_equal(
            pf_shared.total_benchmark_return(),
            result
        )

    def test_return_method(self):
        pd.testing.assert_frame_equal(
            pf_shared.cumulative_returns(),
            pd.DataFrame(
                np.array([
                    [-0.000599499999999975, -0.0012009999999998966],
                    [-0.006639499999999909, 0.007758800000000177],
                    [-0.006669349999999907, 0.017161800000000005],
                    [-0.01820955000000002, 0.017082199999999936],
                    [-0.025209550000000136, 0.017082199999999936]
                ]),
                index=price_na.index,
                columns=pd.Index(['first', 'second'], dtype='object', name='group')
            )
        )
        pd.testing.assert_frame_equal(
            pf_shared.cumulative_returns(group_by=False),
            pd.DataFrame(
                np.array([
                    [0.0, -0.000599499999999975, -0.0012009999999998966],
                    [-0.0005201000000001343, -0.006119399999999886, 0.007758800000000177],
                    [-0.0005499500000001323, -0.006119399999999886, 0.017161800000000005],
                    [-0.0005499500000001323, -0.017659599999999886, 0.017082199999999936],
                    [-0.0015524500000001495, -0.023657099999999875, 0.017082199999999936]
                ]),
                index=price_na.index,
                columns=price_na.columns
            )
        )
        pd.testing.assert_series_equal(
            pf_shared.sharpe_ratio(),
            pd.Series(
                np.array([-20.095906945591288, 12.345065267401496]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('sharpe_ratio')
        )
        pd.testing.assert_series_equal(
            pf_shared.sharpe_ratio(risk_free=0.01),
            pd.Series(
                np.array([-59.62258787402645, -23.91718815937344]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('sharpe_ratio')
        )
        pd.testing.assert_series_equal(
            pf_shared.sharpe_ratio(year_freq='365D'),
            pd.Series(
                np.array([-20.095906945591288, 12.345065267401496]),
                index=pd.Index(['first', 'second'], dtype='object', name='group')
            ).rename('sharpe_ratio')
        )
        pd.testing.assert_series_equal(
            pf_shared.sharpe_ratio(group_by=False),
            pd.Series(
                np.array([-13.30950646054953, -19.278625117344564, 12.345065267401496]),
                index=price_na.columns
            ).rename('sharpe_ratio')
        )
        pd.testing.assert_series_equal(
            pf_shared.information_ratio(group_by=False),
            pd.Series(
                np.array([-0.9988561334618041, -0.8809478746008806, -0.884780642352239]),
                index=price_na.columns
            ).rename('information_ratio')
        )
        with pytest.raises(Exception):
            _ = pf_shared.information_ratio(pf_shared.benchmark_returns(group_by=False) * 2)

    def test_stats(self):
        stats_index = pd.Index([
            'Start', 'End', 'Period', 'Start Value', 'End Value',
            'Total Return [%]', 'Benchmark Return [%]', 'Max Gross Exposure [%]',
            'Total Fees Paid', 'Max Drawdown [%]', 'Max Drawdown Duration',
            'Total Trades', 'Total Closed Trades', 'Total Open Trades',
            'Open Trade PnL', 'Win Rate [%]', 'Best Trade [%]', 'Worst Trade [%]',
            'Avg Winning Trade [%]', 'Avg Losing Trade [%]',
            'Avg Winning Trade Duration', 'Avg Losing Trade Duration',
            'Profit Factor', 'Expectancy', 'Sharpe Ratio', 'Calmar Ratio',
            'Omega Ratio', 'Sortino Ratio'
        ], dtype='object')
        pd.testing.assert_series_equal(
            pf.stats(),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 100.0, 98.88877000000001, -1.11123, 283.3333333333333,
                    2.05906183131983, 0.42223000000000005, 1.6451238489727062, pd.Timedelta('3 days 08:00:00'),
                    2.0, 1.3333333333333333, 0.6666666666666666, -1.5042060606060605, 33.333333333333336,
                    -98.38058805880588, -100.8038553855386, 143.91625412541256, -221.34645964596464,
                    pd.Timedelta('2 days 12:00:00'), pd.Timedelta('2 days 00:00:00'), np.inf, 0.10827272727272726,
                    -6.751008013903537, 10378.930331014584, 4.768700318817701, 31.599760994679134
                ]),
                index=stats_index,
                name='agg_func_mean')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a'),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 100.0, 99.68951, -0.3104899999999997, 150.0,
                    5.015572852148637, 0.35549, 0.3104900000000015, pd.Timedelta('4 days 00:00:00'),
                    2, 1, 1, -0.20049999999999982, 0.0, -54.450495049504966, -54.450495049504966,
                    np.nan, -54.450495049504966, pd.NaT, pd.Timedelta('1 days 00:00:00'), 0.0,
                    -0.10999000000000003, -13.30804491478906, -65.40868619923044, 0.0, -11.738864633265454
                ]),
                index=stats_index,
                name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', settings=dict(freq='10 days', year_freq='200 days')),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('50 days 00:00:00'), 100.0, 99.68951, -0.3104899999999997, 150.0,
                    5.015572852148637, 0.35549, 0.3104900000000015, pd.Timedelta('40 days 00:00:00'),
                    2, 1, 1, -0.20049999999999982, 0.0, -54.450495049504966, -54.450495049504966,
                    np.nan, -54.450495049504966, pd.NaT, pd.Timedelta('10 days 00:00:00'), 0.0, -0.10999000000000003,
                    -3.1151776875290866, -3.981409131683691, 0.0, -2.7478603669149457
                ]),
                index=stats_index,
                name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', settings=dict(trade_type='positions')),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 100.0, 99.68951, -0.3104899999999997, 150.0,
                    5.015572852148637, 0.35549, 0.3104900000000015, pd.Timedelta('4 days 00:00:00'),
                    2, 1, 1, -0.20049999999999982, 0.0, -54.450495049504966, -54.450495049504966,
                    np.nan, -54.450495049504966, pd.NaT, pd.Timedelta('1 days 00:00:00'), 0.0,
                    -0.10999000000000003, -13.30804491478906, -65.40868619923044, 0.0, -11.738864633265454
                ]),
                index=pd.Index([
                    'Start', 'End', 'Period', 'Start Value', 'End Value',
                    'Total Return [%]', 'Benchmark Return [%]', 'Max Gross Exposure [%]',
                    'Total Fees Paid', 'Max Drawdown [%]', 'Max Drawdown Duration',
                    'Total Trades', 'Total Closed Trades', 'Total Open Trades',
                    'Open Trade PnL', 'Win Rate [%]', 'Best Trade [%]',
                    'Worst Trade [%]', 'Avg Winning Trade [%]',
                    'Avg Losing Trade [%]', 'Avg Winning Trade Duration',
                    'Avg Losing Trade Duration', 'Profit Factor', 'Expectancy',
                    'Sharpe Ratio', 'Calmar Ratio', 'Omega Ratio', 'Sortino Ratio'
                ], dtype='object'),
                name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', settings=dict(required_return=0.1, risk_free=0.01)),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 100.0, 99.68951, -0.3104899999999997, 150.0,
                    5.015572852148637, 0.35549, 0.3104900000000015, pd.Timedelta('4 days 00:00:00'),
                    2, 1, 1, -0.20049999999999982, 0.0, -54.450495049504966, -54.450495049504966,
                    np.nan, -54.450495049504966, pd.NaT, pd.Timedelta('1 days 00:00:00'), 0.0,
                    -0.10999000000000003, -227.45862849586334, -65.40868619923044, 0.0, -19.104372472268942
                ]),
                index=stats_index,
                name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', settings=dict(use_asset_returns=True)),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 100.0, 99.68951, -0.3104899999999997,
                    150.0, 5.015572852148637, 0.35549, 0.3104900000000015, pd.Timedelta('4 days 00:00:00'),
                    2, 1, 1, -0.20049999999999982, 0.0, -54.450495049504966, -54.450495049504966, np.nan,
                    -54.450495049504966, pd.NaT, pd.Timedelta('1 days 00:00:00'), 0.0, -0.10999000000000003,
                    np.nan, np.nan, 0.0, np.nan
                ]),
                index=stats_index,
                name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', settings=dict(incl_open=True)),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 100.0, 99.68951, -0.3104899999999997, 150.0,
                    5.015572852148637, 0.35549, 0.3104900000000015, pd.Timedelta('4 days 00:00:00'),
                    2, 1, 1, -0.20049999999999982, 0.0, -3.9702970297029667, -54.450495049504966,
                    np.nan, -29.210396039603964, pd.NaT, pd.Timedelta('1 days 00:00:00'), 0.0,
                    -0.1552449999999999, -13.30804491478906, -65.40868619923044, 0.0, -11.738864633265454
                ]),
                index=stats_index,
                name='a')
        )
        pd.testing.assert_series_equal(
            pf_grouped.stats(column='first'),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), 200.0, 194.95809, -2.520955, 275.0, -0.505305454620791,
                    0.82091, 2.46248125751388, pd.Timedelta('4 days 00:00:00'), 4, 2, 2, -4.512618181818182,
                    0.0, -54.450495049504966, -388.2424242424243, np.nan, -221.34645964596461, pd.NaT,
                    pd.Timedelta('2 days 00:00:00'), 0.0, -0.2646459090909091, -20.095906945591288,
                    -34.312217430388344, 0.0, -14.554511690523578
                ]),
                index=stats_index,
                name='first')
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', tags='trades and open and not closed', settings=dict(incl_open=True)),
            pd.Series(
                np.array([
                    1, -0.20049999999999982
                ]),
                index=pd.Index([
                    'Total Open Trades', 'Open Trade PnL'
                ], dtype='object'),
                name='a')
        )
        max_winning_streak = (
            'max_winning_streak',
            dict(
                title='Max Winning Streak',
                calc_func=lambda trades: trades.winning_streak.max(),
                resolve_trades=True
            )
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', metrics=max_winning_streak),
            pd.Series([0.0], index=['Max Winning Streak'], name='a')
        )
        max_winning_streak = (
            'max_winning_streak',
            dict(
                title='Max Winning Streak',
                calc_func=lambda self, group_by: self.get_trades(group_by=group_by).winning_streak.max()
            )
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', metrics=max_winning_streak),
            pd.Series([0.0], index=['Max Winning Streak'], name='a')
        )
        max_winning_streak = (
            'max_winning_streak',
            dict(
                title='Max Winning Streak',
                calc_func=lambda self, settings:
                self.get_trades(group_by=settings['group_by']).winning_streak.max(),
                resolve_calc_func=False
            )
        )
        pd.testing.assert_series_equal(
            pf.stats(column='a', metrics=max_winning_streak),
            pd.Series([0.0], index=['Max Winning Streak'], name='a')
        )
        vbt.settings.portfolio.stats['settings']['my_arg'] = 100
        my_arg_metric = ('my_arg_metric', dict(title='My Arg', calc_func=lambda my_arg: my_arg))
        pd.testing.assert_series_equal(
            pf.stats(my_arg_metric, column='a'),
            pd.Series([100], index=['My Arg'], name='a')
        )
        vbt.settings.portfolio.stats.reset()
        pd.testing.assert_series_equal(
            pf.stats(my_arg_metric, column='a', settings=dict(my_arg=200)),
            pd.Series([200], index=['My Arg'], name='a')
        )
        my_arg_metric = ('my_arg_metric', dict(title='My Arg', my_arg=300, calc_func=lambda my_arg: my_arg))
        pd.testing.assert_series_equal(
            pf.stats(my_arg_metric, column='a', settings=dict(my_arg=200)),
            pd.Series([300], index=['My Arg'], name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(my_arg_metric, column='a', settings=dict(my_arg=200),
                     metric_settings=dict(my_arg_metric=dict(my_arg=400))),
            pd.Series([400], index=['My Arg'], name='a')
        )
        trade_min_pnl_cnt = (
            'trade_min_pnl_cnt',
            dict(
                title=vbt.Sub('Trades with PnL over $$${min_pnl}'),
                calc_func=lambda trades, min_pnl: trades.apply_mask(
                    trades.pnl.values >= min_pnl).count(),
                resolve_trades=True
            )
        )
        pd.testing.assert_series_equal(
            pf.stats(
                metrics=trade_min_pnl_cnt, column='a',
                metric_settings=dict(trade_min_pnl_cnt=dict(min_pnl=0))),
            pd.Series([0], index=['Trades with PnL over $0'], name='a')
        )
        pd.testing.assert_series_equal(
            pf.stats(
                metrics=[
                    trade_min_pnl_cnt,
                    trade_min_pnl_cnt,
                    trade_min_pnl_cnt
                ],
                column='a',
                metric_settings=dict(
                    trade_min_pnl_cnt_0=dict(min_pnl=0),
                    trade_min_pnl_cnt_1=dict(min_pnl=10),
                    trade_min_pnl_cnt_2=dict(min_pnl=20))
            ),
            pd.Series([0, 0, 0], index=[
                'Trades with PnL over $0',
                'Trades with PnL over $10',
                'Trades with PnL over $20'
            ], name='a')
        )
        pd.testing.assert_frame_equal(
            pf.stats(metrics='total_trades', agg_func=None, settings=dict(trades_type='entry_trades')),
            pd.DataFrame([2, 2, 2], index=price_na.columns, columns=['Total Trades'])
        )
        pd.testing.assert_frame_equal(
            pf.stats(metrics='total_trades', agg_func=None, settings=dict(trades_type='exit_trades')),
            pd.DataFrame([2, 2, 2], index=price_na.columns, columns=['Total Trades'])
        )
        pd.testing.assert_frame_equal(
            pf.stats(metrics='total_trades', agg_func=None, settings=dict(trades_type='positions')),
            pd.DataFrame([2, 2, 2], index=price_na.columns, columns=['Total Trades'])
        )
        pd.testing.assert_series_equal(
            pf['c'].stats(),
            pf.stats(column='c')
        )
        pd.testing.assert_series_equal(
            pf['c'].stats(),
            pf_grouped.stats(column='c', group_by=False)
        )
        pd.testing.assert_series_equal(
            pf_grouped['second'].stats(),
            pf_grouped.stats(column='second')
        )
        pd.testing.assert_series_equal(
            pf_grouped['second'].stats(),
            pf.stats(column='second', group_by=group_by)
        )
        pd.testing.assert_series_equal(
            pf.replace(wrapper=pf.wrapper.replace(freq='10d')).stats(),
            pf.stats(settings=dict(freq='10d'))
        )
        stats_df = pf.stats(agg_func=None)
        assert stats_df.shape == (3, 28)
        pd.testing.assert_index_equal(stats_df.index, pf.wrapper.columns)
        pd.testing.assert_index_equal(stats_df.columns, stats_index)

    def test_returns_stats(self):
        pd.testing.assert_series_equal(
            pf.returns_stats(column='a'),
            pd.Series(
                np.array([
                    pd.Timestamp('2020-01-01 00:00:00'), pd.Timestamp('2020-01-05 00:00:00'),
                    pd.Timedelta('5 days 00:00:00'), -0.3104900000000077, 150.0, -20.30874297799884,
                    1.7044081500801351, 0.3104900000000077, pd.Timedelta('4 days 00:00:00'),
                    -13.30804491478906, -65.40868619923044, 0.0, -11.738864633265454,
                    -1.2191070234483876, 0.12297560887596681, 0.0, 0.0, -0.0018138061822238526,
                    -0.24888299449497553, 0.0007493142128979539
                ]),
                index=pd.Index([
                    'Start', 'End', 'Period', 'Total Return [%]', 'Benchmark Return [%]',
                    'Annualized Return [%]', 'Annualized Volatility [%]',
                    'Max Drawdown [%]', 'Max Drawdown Duration', 'Sharpe Ratio',
                    'Calmar Ratio', 'Omega Ratio', 'Sortino Ratio', 'Skew', 'Kurtosis',
                    'Tail Ratio', 'Common Sense Ratio', 'Value at Risk', 'Alpha', 'Beta'
                ], dtype='object'),
                name='a')
        )

    def test_plots(self):
        _ = pf.plot(column='a', subplots='all')
        _ = pf_grouped.plot(column='first', subplots='all')
        _ = pf_grouped.plot(column='a', subplots='all', group_by=False)
        _ = pf_shared.plot(column='a', subplots='all', group_by=False)
        with pytest.raises(Exception):
            _ = pf.plot(subplots='all')
        with pytest.raises(Exception):
            _ = pf_grouped.plot(subplots='all')
