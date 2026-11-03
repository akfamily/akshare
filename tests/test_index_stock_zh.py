#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/03
Desc: akshare.index.index_stock_zh 的季度数据测试

get_tx_start_year 在 weekTrends 返回空数据时，会改用带 qfq 参数的 K 线接口，
其返回键名是 qfqday 而不是 day；此处用假响应固定该行为，全程不联网。
"""

import pytest

from akshare.index import index_stock_zh


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text


def test_get_tx_start_year_reads_qfqday_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, params: dict) -> FakeResponse:
        if "weekTrends" in url:
            return FakeResponse('trend_qfq={"code":0,"msg":"ok","data":[]}')
        return FakeResponse(
            'kline_dayqfq={"code":0,"msg":"","data":{"bj920599":{"qfqday":'
            '[["2025-07-08","19.618","20.058","20.178","19.618"]]}}}'
        )

    monkeypatch.setattr(index_stock_zh.http, "get", fake_get)
    assert index_stock_zh.get_tx_start_year(symbol="bj920599") == "2025-07-08"


def test_get_tx_start_year_reads_day(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, params: dict) -> FakeResponse:
        if "weekTrends" in url:
            return FakeResponse('trend_qfq={"code":0,"msg":"ok","data":[]}')
        return FakeResponse(
            'kline_dayqfq={"code":0,"msg":"","data":{"sh600000":{"day":'
            '[["1999-11-10","10.0","10.0","10.0","10.0"]]}}}'
        )

    monkeypatch.setattr(index_stock_zh.http, "get", fake_get)
    assert index_stock_zh.get_tx_start_year(symbol="sh600000") == "1999-11-10"
