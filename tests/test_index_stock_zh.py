#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/08
Desc: akshare.index.index_stock_zh 中腾讯接口的离线测试

北交所股票的 weekTrends 返回空数据，get_tx_start_year 改为从日 K 线向前翻页，
直到某页不足 640 条，取最早的交易日。stock_zh_index_daily_tx 的原始数组依次为
日期、开、收、高、低、成交量、占位、换手率（%）、成交额（万元）、占位、占位，
输出 volume 统一为股、turnover 为小数、amount 统一为元。
此处用假响应固定这些行为，全程不联网。
"""

import json

import pytest

from akshare.exceptions import APIError, DataParsingError
from akshare.index import index_stock_zh
from akshare.stock.quote.stock_hist_tx import _normalize_tx_symbol

PAGE_SIZE = index_stock_zh._TX_KLINE_PAGE_SIZE


class FakeResponse:
    status_code = 200

    def __init__(self, text: str) -> None:
        self.text = text


def _rows(first_date: str, count: int) -> list:
    return [[first_date, "1", "1", "1", "1", "100"]] + [
        ["2026-11-02", "1", "1", "1", "1", "100"]
    ] * (count - 1)


def _kline_text(symbol: str, key: str, rows: list) -> str:
    return "kline_day=" + json.dumps({"code": 0, "data": {symbol: {key: rows}}})


def _install(monkeypatch: pytest.MonkeyPatch, week_trends: str, pages: dict) -> list:
    """pages 以请求参数中的结束日期为键；返回实际发出的 K 线请求参数"""
    calls = []

    def fake_get(url: str, params: dict) -> FakeResponse:
        if "weekTrends" in url:
            return FakeResponse(week_trends)
        calls.append(params["param"])
        end_date = params["param"].split(",")[3]
        return FakeResponse(pages[end_date])

    monkeypatch.setattr(index_stock_zh.http, "get", fake_get)
    return calls


EMPTY_WEEK = 'trend_qfq={"code":0,"msg":"ok","data":[]}'


def test_week_trends_path_unchanged(monkeypatch: pytest.MonkeyPatch) -> None:
    week = 'trend_qfq={"code":0,"data":[["1999-11-10","1"],["1999-11-17","1"]]}'
    calls = _install(monkeypatch, week, {})
    assert index_stock_zh.get_tx_start_year(symbol="sh600000") == "1999-11-10"
    assert calls == []


def test_week_trends_error_payload_falls_back_to_kline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    symbol = "bj871981"
    pages = {"": _kline_text(symbol, "day", _rows("2020-12-22", 51))}
    error_week = 'trend_qfq={"code":-1,"msg":[],"data":"invalid code"}'
    calls = _install(monkeypatch, error_week, pages)
    assert index_stock_zh.get_tx_start_year(symbol=symbol) == "2020-12-22"
    assert len(calls) == 1


def test_fallback_pages_back_to_first_trading_day(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    symbol = "bj920599"
    pages = {
        "": _kline_text(symbol, "day", _rows("2024-03-12", PAGE_SIZE + 1)),
        "2024-03-12": _kline_text(symbol, "day", _rows("2021-07-21", PAGE_SIZE)),
        "2021-07-21": _kline_text(symbol, "day", _rows("2021-02-22", 103)),
    }
    calls = _install(monkeypatch, EMPTY_WEEK, pages)
    assert index_stock_zh.get_tx_start_year(symbol=symbol) == "2021-02-22"
    assert len(calls) == 3


@pytest.mark.parametrize("key", ["qfqday", "hfqday"])
def test_fallback_reads_adjusted_keys(
    monkeypatch: pytest.MonkeyPatch, key: str
) -> None:
    symbol = "bj920002"
    pages = {"": _kline_text(symbol, key, _rows("2024-05-30", 589))}
    _install(monkeypatch, EMPTY_WEEK, pages)
    assert index_stock_zh.get_tx_start_year(symbol=symbol) == "2024-05-30"


def test_fallback_stops_when_page_does_not_move(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    symbol = "bj920599"
    page = _kline_text(symbol, "day", _rows("2021-02-22", PAGE_SIZE))
    calls = _install(monkeypatch, EMPTY_WEEK, {"": page, "2021-02-22": page})
    assert index_stock_zh.get_tx_start_year(symbol=symbol) == "2021-02-22"
    assert len(calls) == 2


def test_fallback_without_data_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    pages = {"": 'kline_day={"code":0,"msg":"","data":{}}'}
    _install(monkeypatch, EMPTY_WEEK, pages)
    with pytest.raises(APIError, match="bj999999"):
        index_stock_zh.get_tx_start_year(symbol="bj999999")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("920599", "bj920599"),
        ("830799", "bj830799"),
        ("834000", "bj834000"),
        ("871981", "bj871981"),
        ("880001", "bj880001"),
        ("BJ920599", "bj920599"),
    ],
)
def test_normalize_beijing_symbols(raw: str, expected: str) -> None:
    assert _normalize_tx_symbol(symbol=raw) == expected


def _daily_row(date: str) -> list:
    """取自 sh000300 2026-11-06 的真实返回"""
    return [
        date,
        "4017.94",
        "4054.28",
        "4069.07",
        "4013.79",
        "192152012.00",
        {},
        "0.57",
        "47884039.99",
        "0.00",
        "0.00",
    ]


def _install_daily(
    monkeypatch: pytest.MonkeyPatch, symbol: str, rows: list, key: str = "day"
) -> None:
    def fake_get(url: str, params: dict) -> FakeResponse:
        if "weekTrends" in url:
            return FakeResponse('trend_qfq={"data":[["1991-04-03","1"]]}')
        return FakeResponse(_kline_text(symbol, key, rows))

    monkeypatch.setattr(index_stock_zh.http, "get", fake_get)


@pytest.mark.parametrize(
    ("symbol", "multiplier"),
    [("sh000300", 100), ("sz399001", 100), ("sh600519", 100), ("sh688981", 1)],
)
def test_daily_tx_columns_and_units(
    monkeypatch: pytest.MonkeyPatch, symbol: str, multiplier: int
) -> None:
    rows = [_daily_row("2026-11-05"), _daily_row("2026-11-06")]
    _install_daily(monkeypatch, symbol, rows)
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol=symbol, start_date="20261105", end_date="20261106"
    )
    assert list(df.columns) == index_stock_zh._TX_COLUMNS
    row = df.iloc[-1]
    assert str(row["date"]) == "2026-11-06"
    assert row["volume"] == pytest.approx(192152012 * multiplier)
    assert row["turnover"] == pytest.approx(0.0057)
    assert row["amount"] == pytest.approx(478840399900)


def test_daily_tx_reads_qfqday_key(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = [_daily_row("2026-11-05"), _daily_row("2026-11-06")]
    _install_daily(monkeypatch, "sh000300", rows, key="qfqday")
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol="sh000300", start_date="20261105", end_date="20261106"
    )
    assert len(df) == 2


def test_daily_tx_filters_date_range(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = [_daily_row("2026-11-05"), _daily_row("2026-11-06")]
    _install_daily(monkeypatch, "sh000300", rows)
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol="sh000300", start_date="20261106", end_date="20261106"
    )
    assert [str(d) for d in df["date"]] == ["2026-11-06"]


def test_daily_tx_short_rows_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_daily(monkeypatch, "sh000300", [_daily_row("2026-11-06")[:6]])
    with pytest.raises(DataParsingError, match="6 个字段"):
        index_stock_zh.stock_zh_index_daily_tx(
            symbol="sh000300", start_date="20261106", end_date="20261106"
        )


def test_daily_tx_without_rows_returns_empty_frame(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_daily(monkeypatch, "sh000300", [])
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol="sh000300", start_date="20261106", end_date="20261106"
    )
    assert df.empty
    assert list(df.columns) == index_stock_zh._TX_COLUMNS
