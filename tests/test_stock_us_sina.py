#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/5
Desc: 新浪美股列表翻页的错误处理测试

新浪美股列表接口每页固定 20 条，取全部美股要翻 900 多页；连续翻页时偶发以 200 状态码
返回后端数据库错误（"MySQL server has gone away"），原先接口直接报 KeyError: 'data'，
已翻的页全部作废。现在同一页按指数退避重试，用尽后抛出带页码的 APIError。

本测试全程不联网：用 monkeypatch 顶替 requests.Session.send，按脚本返回 JSONP 文本。
"""

import json
import time

import pytest
import requests

from akshare.exceptions import APIError
from akshare.stock.quote import stock_us_sina

ERROR = {
    "__ERROR": "HY000",
    "__ERRORMSG": "SQLSTATE[HY000]: General error: 2006 MySQL server has gone away",
}


def _jsonp(obj) -> str:
    return (
        "/*<script>location.href='//sina.com';</script>*/\nIO.XSRV2.CallbackList[x]("
        + json.dumps(obj)
        + ");"
    )


@pytest.fixture
def pages(monkeypatch):
    calls, outcomes = [], []
    monkeypatch.setattr(requests.sessions, "get_environ_proxies", lambda *a, **k: {})
    monkeypatch.setattr(time, "sleep", lambda s: None)

    def fake_send(self, request, **kwargs):
        calls.append(request.url)
        response = requests.Response()
        response.request = request
        response.status_code = 200
        response._content = _jsonp(outcomes.pop(0)).encode("utf-8")
        response.encoding = "utf-8"
        return response

    monkeypatch.setattr(requests.Session, "send", fake_send)

    def load(*items):
        outcomes.extend(items)
        return calls

    return load


def test_page_retries_after_sina_backend_error(pages):
    calls = pages(ERROR, {"count": "2", "data": [{"symbol": "AAPL"}]})
    data = stock_us_sina._us_list_page(stock_us_sina._us_list_js_code(), 30)
    assert data["data"] == [{"symbol": "AAPL"}]
    assert len(calls) == 2
    assert all("page=30" in url for url in calls)


def test_page_raises_clear_error_after_retries(pages):
    pages(ERROR, ERROR, ERROR)
    with pytest.raises(APIError, match="第 7 页.*MySQL server has gone away"):
        stock_us_sina._us_list_page(stock_us_sina._us_list_js_code(), 7)


def test_shared_payload_is_not_mutated(pages):
    from akshare.stock.cons import us_sina_stock_dict_payload

    before = dict(us_sina_stock_dict_payload)
    pages({"count": "1", "data": []})
    stock_us_sina._us_list_page(stock_us_sina._us_list_js_code(), 5)
    assert us_sina_stock_dict_payload == before
