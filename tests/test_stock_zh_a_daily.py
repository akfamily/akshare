#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: stock_zh_a_daily 对已退市与不存在代码的处理测试

已退市的股票（如 sh600001）新浪仍有历史行情，但股本接口返回 (null)，原先直接解析空文本，
报出与原因无关的 JSONDecodeError；不存在的代码行情接口返回 404，原先报 KeyError: 'date'。
全程不联网：用 monkeypatch 顶替 http.get，并跳过 JS 解密。
"""

import warnings

import pandas as pd
import pytest

from akshare.exceptions import InvalidParameterError
from akshare.stock.quote import stock_zh_a_sina

# 新浪解密后的日期带 UTC 时区，形如 1999-11-10T00:00:00.000Z
ROWS = [
    {
        "date": "2024-01-02T00:00:00.000Z",
        "open": 10,
        "high": 11,
        "low": 9,
        "close": 10.5,
        "volume": 1000,
        "amount": 10500,
    },
    {
        "date": "2024-01-03T00:00:00.000Z",
        "open": 10.5,
        "high": 12,
        "low": 10,
        "close": 11,
        "volume": 2000,
        "amount": 22000,
    },
]
AMOUNT_OK = (
    "/*<script>location.href='//sina.com';</script>*/\n"
    'var KKE_ShareAmount_sh600000=([{"date":"2023-06-30","amount":100},{"date":"2024-01-03","amount":200}]);'
)
AMOUNT_NULL = "/*<script>location.href='//sina.com';</script>*/\nvar KKE_ShareAmount_sh600001=(null);"


class _Resp:
    def __init__(self, status_code=200, text=""):
        self.status_code = status_code
        self.text = text


class _Racer:
    def eval(self, code):
        pass

    def call(self, name, payload):
        return ROWS


@pytest.fixture
def fake_sina(monkeypatch):
    def install(hist_status=200, amount_text=AMOUNT_OK):
        def fake_get(url, *args, **kwargs):
            if "ShareAmount" in url:
                return _Resp(text=amount_text)
            return _Resp(status_code=hist_status, text='var x="payload";')

        monkeypatch.setattr(stock_zh_a_sina.http, "get", fake_get)
        monkeypatch.setattr(stock_zh_a_sina.py_mini_racer, "MiniRacer", _Racer)

    return install


def test_normal_symbol(fake_sina):
    fake_sina()
    df = stock_zh_a_sina.stock_zh_a_daily(
        symbol="sh600000", start_date="20240101", end_date="20240110"
    )
    assert len(df) == 2
    assert df["outstanding_share"].tolist() == [1000000.0, 2000000.0]
    assert [str(d) for d in df["date"]] == ["2024-01-02", "2024-01-03"]


def test_delisted_symbol_returns_prices_without_share_data(fake_sina):
    fake_sina(amount_text=AMOUNT_NULL)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        df = stock_zh_a_sina.stock_zh_a_daily(
            symbol="sh600001", start_date="20240101", end_date="20240110"
        )
    assert len(df) == 2
    assert df["close"].tolist() == [10.5, 11.0]
    assert df["outstanding_share"].isna().all() and df["turnover"].isna().all()
    assert any("股本" in str(w.message) for w in caught)


def test_unknown_symbol_raises_clear_error(fake_sina):
    fake_sina(hist_status=404, amount_text=AMOUNT_NULL)
    with pytest.raises(InvalidParameterError, match="sh609999"):
        stock_zh_a_sina.stock_zh_a_daily(symbol="sh609999")


def test_result_columns_unchanged(fake_sina):
    fake_sina()
    df = stock_zh_a_sina.stock_zh_a_daily(
        symbol="sh600000", start_date="20240101", end_date="20240110"
    )
    assert list(df.columns) == [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "outstanding_share",
        "turnover",
    ]
    assert isinstance(df, pd.DataFrame)
