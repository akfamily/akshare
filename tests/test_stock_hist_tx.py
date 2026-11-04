#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/03
Desc: akshare.stock.quote.stock_hist_tx.stock_zh_a_hist_tx 的离线测试

固定日期解析与请求范围：start_date / end_date 接受 YYYYMMDD 与 YYYY-MM-DD，
每次请求覆盖两个自然年并按两年步进；全程用假响应，不联网。
"""

import datetime
import json

import pytest

from akshare.exceptions import InvalidParameterError
from akshare.stock.quote import stock_hist_tx

SYMBOL = "sz000001"


def _row(date: str) -> list:
    return [date, "10", "11", "12", "9", "1000", "{}", "1.5", "2.5"]


def _install(monkeypatch: pytest.MonkeyPatch, first_date: str = "1991-04-03") -> list:
    """返回实际发出的 K 线请求，每项为开始日期与结束日期"""
    windows = []

    def fake_get(url: str, params: dict):
        if "weekTrends" in url:
            text = "trend_qfq=" + json.dumps({"data": [[first_date, "1"]]})
        else:
            _, _, begin, end, _, _ = params["param"].split(",")
            windows.append((begin, end))
            years = range(int(begin[:4]), int(end[:4]) + 1)
            rows = [_row(f"{y}-{md}") for y in years for md in ("01-02", "07-01")]
            text = "kline_day=" + json.dumps({"data": {SYMBOL: {"day": rows}}})
        return type("FakeResponse", (), {"text": text, "status_code": 200})()

    monkeypatch.setattr(stock_hist_tx.http, "get", fake_get)
    return windows


@pytest.mark.parametrize(
    ("start_date", "end_date"),
    [("20200101", "20231027"), ("2020-01-01", "2023-10-27")],
)
def test_requests_two_years_per_window(
    monkeypatch: pytest.MonkeyPatch, start_date: str, end_date: str
) -> None:
    windows = _install(monkeypatch)
    df = stock_hist_tx.stock_zh_a_hist_tx(
        symbol=SYMBOL, start_date=start_date, end_date=end_date
    )
    assert windows == [("2020-01-01", "2021-12-31"), ("2022-01-01", "2023-12-31")]
    assert list(df.columns) == stock_hist_tx._TX_COLUMNS
    assert str(df["date"].min()) == "2020-01-02"
    assert str(df["date"].max()) == "2023-07-01"
    assert len(df) == 8


def test_end_date_after_today_stops_at_current_year(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windows = _install(monkeypatch)
    stock_hist_tx.stock_zh_a_hist_tx(
        symbol=SYMBOL, start_date="20200101", end_date="20500101"
    )
    this_year = datetime.date.today().year
    assert windows[0][0] == "2020-01-01"
    assert int(windows[-1][0][:4]) <= this_year <= int(windows[-1][1][:4])
    assert len(windows) == (this_year - 2020) // 2 + 1


def test_start_date_is_clamped_to_first_trading_day(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windows = _install(monkeypatch, first_date="2021-02-22")
    df = stock_hist_tx.stock_zh_a_hist_tx(
        symbol=SYMBOL, start_date="19000101", end_date="20221231"
    )
    assert windows == [("2021-01-01", "2022-12-31")]
    assert str(df["date"].min()) == "2021-07-01"


def test_future_range_returns_empty_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    windows = _install(monkeypatch)
    df = stock_hist_tx.stock_zh_a_hist_tx(
        symbol=SYMBOL, start_date="20990101", end_date="20991231"
    )
    assert windows == []
    assert df.empty
    assert list(df.columns) == stock_hist_tx._TX_COLUMNS


@pytest.mark.parametrize("bad", ["2023/01/01", "2023", "20231340", "abc"])
def test_invalid_date_raises(monkeypatch: pytest.MonkeyPatch, bad: str) -> None:
    _install(monkeypatch)
    with pytest.raises(InvalidParameterError, match="YYYYMMDD"):
        stock_hist_tx.stock_zh_a_hist_tx(symbol=SYMBOL, start_date=bad)
    with pytest.raises(InvalidParameterError, match="YYYYMMDD"):
        stock_hist_tx.stock_zh_a_hist_tx(symbol=SYMBOL, end_date=bad)


def test_start_after_end_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch)
    with pytest.raises(InvalidParameterError, match="不能晚于"):
        stock_hist_tx.stock_zh_a_hist_tx(
            symbol=SYMBOL, start_date="20240101", end_date="20231231"
        )


@pytest.mark.parametrize(
    ("symbol", "expected"),
    [
        ("sz000651", 100),
        ("sz000001", 100),
        ("sz300533", 100),
        ("sz002594", 100),
        ("sh600000", 100),
        ("bj920599", 100),
        ("sh900901", 100),
        ("sh510300", 100),
        ("sz159915", 100),
        ("sh000001", 100),
        ("sh000688", 100),
        ("sz399001", 100),
        ("sh688981", 1),
        ("sh689009", 1),
    ],
)
def test_tx_volume_multiplier(symbol: str, expected: int) -> None:
    assert stock_hist_tx._tx_volume_multiplier(symbol) == expected


@pytest.mark.parametrize(
    ("symbol", "multiplier"),
    [("sz000651", 100), ("sh000001", 100), ("sh688981", 1), ("sh689009", 1)],
)
def test_volume_is_normalized_to_shares(
    monkeypatch: pytest.MonkeyPatch, symbol: str, multiplier: int
) -> None:
    def fake_get(url: str, params: dict):
        if "weekTrends" in url:
            text = 'trend_qfq={"data":[["1996-11-18","1"]]}'
        else:
            rows = [_row("2026-11-03")]
            text = "kline_day=" + json.dumps({"data": {symbol: {"day": rows}}})
        return type("FakeResponse", (), {"text": text, "status_code": 200})()

    monkeypatch.setattr(stock_hist_tx.http, "get", fake_get)
    df = stock_hist_tx.stock_zh_a_hist_tx(
        symbol=symbol, start_date="20261103", end_date="20261103"
    )

    assert df["volume"].iloc[0] == 1000 * multiplier
