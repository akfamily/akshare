#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/08
Desc: akshare.index.index_stock_zh.stock_zh_index_daily_tx 的离线测试

固定响应数组字段语义：原始数组为
[日期, 开, 收, 高, 低, 成交量(手), 占位, 换手率(%), 成交额(万), 占位, 占位]，
输出 volume 统一为股、turnover 为换手率小数、amount 统一为元；
全程用假响应，不联网。
"""

import json

import pandas as pd
import pytest

from akshare.index import index_stock_zh

SYMBOL = "sh000300"


def _row(date: str) -> list:
    """仿真实响应的 11 字段数组（取自 sh000300 2026-11-06 真实抓取）。"""
    return [
        date,
        "4017.94",
        "4054.28",
        "4069.07",
        "4013.79",
        "192152012",
        "{}",
        "0.57",
        "47884039.99",
        "0.00",
        "0.00",
    ]


def _install(monkeypatch: pytest.MonkeyPatch, key: str = "day") -> None:
    """拦截全部 HTTP 请求：weekTrends 返回最早日期，newfqkline 返回假 K 线数组。"""

    def fake_get(url: str, params: dict):
        if "weekTrends" in url:
            text = 'trend_qfq={"data":[["1991-04-03","1"]]}'
        else:
            rows = [_row("2026-11-05"), _row("2026-11-06")]
            text = "kline_dayqfq=" + json.dumps({"data": {SYMBOL: {key: rows}}})
        return type("FakeResponse", (), {"text": text, "status_code": 200})()

    monkeypatch.setattr(index_stock_zh.http, "get", fake_get)


def test_columns_and_units_normalized(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch)
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol=SYMBOL, start_date="20261105", end_date="20261106"
    )
    assert list(df.columns) == [
        "date",
        "open",
        "close",
        "high",
        "low",
        "volume",
        "turnover",
        "amount",
    ]
    row = df[df["date"].astype(str) == "2026-11-06"].iloc[0]
    # volume: 手 → 股(×100)；turnover: 换手率 % → 小数(÷100)；amount: 万元 → 元(×10000)
    assert row["volume"] == pytest.approx(192152012 * 100)
    assert row["turnover"] == pytest.approx(0.57 / 100)
    assert row["amount"] == pytest.approx(47884039.99 * 10000)
    assert str(df["date"].min()) == "2026-11-05"


def test_qfqday_key_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, key="qfqday")
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol=SYMBOL, start_date="20261105", end_date="20261106"
    )
    assert len(df) == 2


def test_short_arrays_fail_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    """旧实现静默截断成 6 列并错标 amount；现行为不足 9 字段时显式报错。"""

    def fake_get(url: str, params: dict):
        if "weekTrends" in url:
            text = 'trend_qfq={"data":[["1991-04-03","1"]]}'
        else:
            rows = [[r] for r in _row("2026-11-06")[:6]]
            text = "kline_dayqfq=" + json.dumps({"data": {SYMBOL: {"day": rows}}})
        return type("FakeResponse", (), {"text": text, "status_code": 200})()

    monkeypatch.setattr(index_stock_zh.http, "get", fake_get)
    with pytest.raises(IndexError):
        index_stock_zh.stock_zh_index_daily_tx(
            symbol=SYMBOL, start_date="20261106", end_date="20261106"
        )


def test_date_range_filtering(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch)
    df = index_stock_zh.stock_zh_index_daily_tx(
        symbol=SYMBOL, start_date="20261106", end_date="20261106"
    )
    assert [str(d) for d in df["date"]] == ["2026-11-06"]
    assert pd.api.types.is_numeric_dtype(df["volume"])
    assert pd.api.types.is_numeric_dtype(df["turnover"])
    assert pd.api.types.is_numeric_dtype(df["amount"])
