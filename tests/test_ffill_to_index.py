"""
akshare.utils.func.ffill_to_index：把按变动日期记录的股本、复权因子对齐到交易日。
新浪日线接口原先用 outer merge 加 ffill 合并这类数据，再按开高低收量去重删掉合并带进来的
非交易日行，结果把价量恰好与更早交易日相同的真实交易日也删掉了（#7477）。
"""

import pandas as pd

from akshare.utils.func import ffill_to_index


def _dates(*items):
    return pd.DatetimeIndex(pd.to_datetime(list(items)))


def test_takes_latest_value_on_or_before_each_date():
    factor = pd.DataFrame(
        {"qfq_factor": [1.0, 2.0]}, index=_dates("2024-01-02", "2024-01-04")
    )
    dates = _dates("2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05")
    result = ffill_to_index(factor, dates)
    assert result.index.equals(dates)
    assert result["qfq_factor"].tolist() == [1.0, 1.0, 2.0, 2.0]


def test_change_on_non_trading_day_applies_from_next_trading_day():
    # 除权日落在周末时，新因子从下一个交易日起生效，且不产生周末那一行
    factor = pd.DataFrame(
        {"qfq_factor": [1.0, 2.0]}, index=_dates("2024-01-01", "2024-01-06")
    )
    dates = _dates("2024-01-05", "2024-01-08")
    result = ffill_to_index(factor, dates)
    assert result.index.equals(dates)
    assert result["qfq_factor"].tolist() == [1.0, 2.0]


def test_dates_before_first_record_are_nan():
    factor = pd.DataFrame({"qfq_factor": [2.0]}, index=_dates("2024-01-04"))
    result = ffill_to_index(factor, _dates("2024-01-03", "2024-01-04"))
    assert result["qfq_factor"].isna().tolist() == [True, False]


def test_unsorted_and_duplicated_records():
    # 新浪的因子表按日期倒序排列
    factor = pd.DataFrame(
        {"qfq_factor": [3.0, 2.0, 1.0, 1.5]},
        index=_dates("2024-01-05", "2024-01-03", "2024-01-01", "2024-01-01"),
    )
    result = ffill_to_index(factor, _dates("2024-01-02", "2024-01-04", "2024-01-05"))
    assert result["qfq_factor"].tolist() == [1.5, 2.0, 3.0]


def test_empty_records_give_nan_columns():
    empty = pd.DataFrame(
        {"outstanding_share": []}, index=pd.DatetimeIndex([], name="date")
    )
    dates = _dates("2024-01-02", "2024-01-03")
    result = ffill_to_index(empty, dates)
    assert result.index.equals(dates)
    assert list(result.columns) == ["outstanding_share"]
    assert result["outstanding_share"].isna().all()


def test_identical_rows_on_different_dates_are_kept():
    # 价量完全相同的两个交易日都要保留，这正是 #7477 丢掉的那类行
    prices = pd.DataFrame(
        {"close": [1.0, 1.0, 1.0], "volume": [500.0, 500.0, 500.0]},
        index=_dates("2024-01-02", "2024-01-03", "2024-01-04"),
    )
    factor = pd.DataFrame({"qfq_factor": [1.0]}, index=_dates("1900-01-01"))
    joined = prices.join(ffill_to_index(factor, prices.index))
    assert len(joined) == 3
    assert joined["qfq_factor"].tolist() == [1.0, 1.0, 1.0]
