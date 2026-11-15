#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/15
Desc: 新浪 *_hist_sina 接口的 period 参数与日线合成周线、月线的测试

新浪的数据源只有日线，周线、月线由 akshare.utils.func.resample_kline 合成。全程不联网。
"""

import datetime
import inspect

import pandas as pd
import pytest

import akshare as ak
from akshare.exceptions import InvalidParameterError
from akshare.stock.quote import stock_zh_a_sina
from akshare.utils.func import check_kline_period, resample_kline

HIST_SINA = [
    "stock_zh_a_hist_sina",
    "stock_zh_a_cdr_hist_sina",
    "stock_zh_b_hist_sina",
    "stock_zh_kcb_hist_sina",
    "stock_hk_hist_sina",
    "stock_us_hist_sina",
]


def _daily() -> pd.DataFrame:
    """2024-01-29（周一）至 2024-02-08（周四）的 9 个交易日，跨两周、两个月"""
    days = pd.bdate_range("2024-01-29", "2024-02-08")
    n = len(days)
    return pd.DataFrame(
        {
            "date": [d.date() for d in days],
            "open": [10.0 + i for i in range(n)],
            "high": [11.0 + i for i in range(n)],
            "low": [9.0 + i for i in range(n)],
            "close": [10.5 + i for i in range(n)],
            "volume": [100.0 * (i + 1) for i in range(n)],
            "amount": [1000.0 * (i + 1) for i in range(n)],
            "outstanding_share": [5000.0] * 5 + [6000.0] * 4,
            "turnover": [0.01] * n,
        }
    )


def test_weekly_bars():
    df = resample_kline(_daily(), "weekly")
    assert list(df.columns) == list(_daily().columns)
    assert df["date"].tolist() == [datetime.date(2024, 2, 2), datetime.date(2024, 2, 8)]
    assert df["open"].tolist() == [10.0, 15.0]
    assert df["high"].tolist() == [15.0, 19.0]
    assert df["low"].tolist() == [9.0, 14.0]
    assert df["close"].tolist() == [14.5, 18.5]
    assert df["volume"].tolist() == [1500.0, 3000.0]
    assert df["amount"].tolist() == [15000.0, 30000.0]
    assert df["outstanding_share"].tolist() == [5000.0, 6000.0]
    assert df["turnover"].tolist() == pytest.approx([0.05, 0.04])


def test_monthly_bars():
    df = resample_kline(_daily(), "monthly")
    assert df["date"].tolist() == [
        datetime.date(2024, 1, 31),
        datetime.date(2024, 2, 8),
    ]
    assert df["open"].tolist() == [10.0, 13.0]
    assert df["close"].tolist() == [12.5, 18.5]
    assert df["volume"].tolist() == [600.0, 3900.0]


def test_daily_is_returned_unchanged():
    daily = _daily()
    assert resample_kline(daily, "daily") is daily


def test_date_range_filters_bars_but_keeps_them_whole():
    """日期范围从一周的中间开始时，这一周的 K 线仍由整周的日线合成"""
    df = resample_kline(_daily(), "weekly", "20240201", "20240205")
    assert df["date"].tolist() == [datetime.date(2024, 2, 2)]
    assert df["open"].tolist() == [10.0] and df["volume"].tolist() == [1500.0]


def test_timestamp_dates_and_unsorted_input():
    daily = _daily()
    daily["date"] = pd.to_datetime(daily["date"])
    df = resample_kline(daily.iloc[::-1].reset_index(drop=True), "weekly")
    assert df["date"].tolist() == [
        pd.Timestamp("2024-02-02"),
        pd.Timestamp("2024-02-08"),
    ]
    assert df["open"].tolist() == [10.0, 15.0]


def test_all_missing_sum_column_stays_missing():
    """已退市的股票没有股本，换手率整列为空；合成后仍为空而不是 0"""
    daily = _daily()
    daily["turnover"] = float("nan")
    assert resample_kline(daily, "weekly")["turnover"].isna().all()


def test_check_kline_period():
    for period in ("daily", "weekly", "monthly"):
        check_kline_period(period, "qfq")
    check_kline_period("daily", "qfq-factor")
    with pytest.raises(InvalidParameterError, match="daily、weekly、monthly"):
        check_kline_period("20240101")
    with pytest.raises(InvalidParameterError, match="复权因子"):
        check_kline_period("weekly", "hfq-factor")


@pytest.mark.parametrize("name", HIST_SINA)
def test_hist_sina_signature(name):
    """period 排在 symbol 之后、默认 daily，与 stock_zh_a_hist_em 一致"""
    params = list(inspect.signature(getattr(ak, name)).parameters.values())
    assert [p.name for p in params[:2]] == ["symbol", "period"]
    assert params[1].default == "daily"
    assert not hasattr(ak, name.replace("_hist_sina", "_daily_sina"))


def test_hist_sina_resamples_the_full_daily_history(monkeypatch):
    """周线先取完整日线再按日期筛选；日线直接把日期范围交给原有逻辑"""
    calls = []

    def fake_daily(symbol, start_date="19900101", end_date="21000118", adjust=""):
        calls.append((symbol, start_date, end_date, adjust))
        return _daily()

    monkeypatch.setattr(stock_zh_a_sina, "_stock_zh_a_daily_sina", fake_daily)
    weekly = ak.stock_zh_a_hist_sina(
        symbol="sh600000",
        period="weekly",
        start_date="20240205",
        end_date="20240209",
        adjust="qfq",
    )
    assert calls == [("sh600000", "19900101", "21000118", "qfq")]
    assert weekly["date"].tolist() == [datetime.date(2024, 2, 8)]
    ak.stock_zh_a_hist_sina(
        symbol="sh600000", start_date="20240205", end_date="20240209"
    )
    assert calls[-1] == ("sh600000", "20240205", "20240209", "")
    with pytest.raises(InvalidParameterError):
        ak.stock_zh_a_hist_sina(symbol="sh600000", period="20240205")
    assert len(calls) == 2
