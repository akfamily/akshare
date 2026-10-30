#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: akshare.utils.http.request_with_retry 的重试策略与东方财富 push2 限流识别测试

2026-10-30 实测：push2 系服务器在短时间内请求较多时直接断开连接（RemoteDisconnected），
被封期间继续请求会延长封禁。因此识别出来后必须立即报错、不再重试；其他域名的同类
错误仍按普通网络故障重试。原先散落各处的重试实现已统一到 request_with_retry，
这里一并覆盖它们迁移后的行为。

本测试全程不联网：用 monkeypatch 顶替 requests.Session.send，按脚本依次返回响应或抛出
异常，并把 time.sleep 换成记录等待时长的空函数。
"""

import json
import time
import warnings
from http.client import RemoteDisconnected

import pytest
import requests
from urllib3.exceptions import ProtocolError

from akshare.exceptions import APIError, NetworkError, RateLimitError
from akshare.utils import http

PUSH2_URL = "https://82.push2.eastmoney.com/api/qt/clist/get"
DATACENTER_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"


def _remote_disconnected() -> requests.exceptions.ConnectionError:
    """
    与 requests 实际抛出的形态一致：ConnectionError(ProtocolError(..., RemoteDisconnected))
    """
    return requests.exceptions.ConnectionError(
        ProtocolError(
            "Connection aborted.",
            RemoteDisconnected("Remote end closed connection without response"),
        )
    )


@pytest.fixture
def script(monkeypatch):
    """
    按顺序给出每次请求的结果：异常实例则抛出，整数为状态码，dict 为 200 的 JSON 正文
    返回 (calls, sleeps)，分别记录请求的地址与每次等待的秒数
    """
    calls, sleeps, outcomes = [], [], []
    monkeypatch.setattr(requests.sessions, "get_environ_proxies", lambda *a, **k: {})
    monkeypatch.setattr(time, "sleep", lambda s: sleeps.append(s))

    def fake_send(self, request, **kwargs):
        calls.append(request.url)
        outcome = outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        response = requests.Response()
        response.request = request
        response.url = request.url
        if isinstance(outcome, dict):
            response.status_code = 200
            response._content = json.dumps(outcome).encode("utf-8")
        else:
            response.status_code = outcome
            response._content = b""
        return response

    monkeypatch.setattr(requests.Session, "send", fake_send)

    def load(*items):
        outcomes.extend(items)
        return calls, sleeps

    return load


@pytest.mark.parametrize(
    "url",
    [
        PUSH2_URL,
        "https://push2.eastmoney.com/api/qt/stock/get",
        "https://push2his.eastmoney.com/api/qt/stock/kline/get",
        "https://63.push2his.eastmoney.com/api/qt/stock/kline/get",
        "https://push2ex.eastmoney.com/getTopicZTPool",
        "https://push2delay.eastmoney.com/api/qt/clist/get",
    ],
)
def test_push2_disconnect_raises_rate_limit_without_retry(script, url):
    calls, sleeps = script(_remote_disconnected())
    with pytest.raises(http.Push2RateLimitError) as excinfo:
        http.request_with_retry("get", url)
    assert len(calls) == 1
    assert sleeps == []
    assert "限流" in str(excinfo.value)
    # 兼容：原先捕获 requests.ConnectionError 的代码仍能捕获
    assert isinstance(excinfo.value, RateLimitError)
    assert isinstance(excinfo.value, requests.exceptions.ConnectionError)


def test_push2_disconnect_detected_on_plain_get_and_session(script):
    script(_remote_disconnected(), _remote_disconnected())
    with pytest.raises(http.Push2RateLimitError):
        http.get(PUSH2_URL)
    with pytest.raises(http.Push2RateLimitError):
        http.Session().get(PUSH2_URL)


@pytest.mark.parametrize(
    "url",
    [DATACENTER_URL, "https://push2.example.com/api", "https://quote.eastmoney.com/"],
)
def test_disconnect_on_other_hosts_is_retried(script, url):
    calls, sleeps = script(*[_remote_disconnected() for _ in range(3)])
    with pytest.raises(requests.exceptions.ConnectionError) as excinfo:
        http.request_with_retry("get", url)
    assert not isinstance(excinfo.value, RateLimitError)
    assert len(calls) == 3
    assert len(sleeps) == 2


def test_push2_proxy_error_is_not_treated_as_ban(script):
    """
    经代理时偶发的 ProxyError 不是东方财富限流，实测 5 秒后即恢复，应正常重试
    """
    calls, _ = script(requests.exceptions.ProxyError("proxy down"), {"data": 1})
    assert http.request_with_retry("get", PUSH2_URL).json() == {"data": 1}
    assert len(calls) == 2


def test_retryable_status_then_success(script):
    calls, sleeps = script(503, 502, {"ok": True})
    r = http.request_with_retry("get", DATACENTER_URL, base_delay=1.0)
    assert r.status_code == 200
    assert len(calls) == 3
    # 指数退避：第一次等 1～2 秒，第二次等 2～3 秒
    assert 1 <= sleeps[0] < 2 and 2 <= sleeps[1] < 3


def test_retryable_status_exhausted_returns_last_response(script):
    calls, _ = script(500, 500, 500)
    assert http.request_with_retry("get", DATACENTER_URL).status_code == 500
    assert len(calls) == 3


def test_client_error_not_retried(script):
    calls, sleeps = script(404)
    assert http.request_with_retry("get", DATACENTER_URL).status_code == 404
    assert len(calls) == 1 and sleeps == []


def test_timeout_exhausted_raises_last_exception(script):
    calls, _ = script(*[requests.exceptions.ReadTimeout("slow") for _ in range(3)])
    with pytest.raises(requests.exceptions.ReadTimeout):
        http.request_with_retry("get", DATACENTER_URL)
    assert len(calls) == 3


def test_fresh_session_also_detects_ban(script):
    calls, _ = script(_remote_disconnected())
    with pytest.raises(http.Push2RateLimitError):
        http.request_with_retry("get", PUSH2_URL, fresh_session=True)
    assert len(calls) == 1


def test_fetch_paginated_data_stops_at_ban(script):
    from akshare.utils.func import fetch_paginated_data

    page = {"data": {"total": 300, "diff": [{"f3": 1}] * 100}}
    calls, _ = script(page, _remote_disconnected())
    with pytest.raises(http.Push2RateLimitError):
        fetch_paginated_data(PUSH2_URL, {"pn": "1", "pz": "100"})
    # 第 1 页成功、第 2 页被断开后立即停止，不再重试，也不再请求第 3 页
    assert len(calls) == 2


def test_fetch_paginated_data_retries_transient_error(script):
    from akshare.utils.func import fetch_paginated_data

    page = {"data": {"total": 200, "diff": [{"f3": 1}] * 100}}
    calls, _ = script(page, requests.exceptions.ReadTimeout("slow"), page)
    assert len(fetch_paginated_data(PUSH2_URL, {"pn": "1", "pz": "100"})) == 200
    assert len(calls) == 3


def test_make_request_with_retry_json_contract(script):
    from akshare.request import make_request_with_retry_json

    script({"result": 1})
    assert make_request_with_retry_json(DATACENTER_URL) == {"result": 1}
    script(500, 500, 500)
    with pytest.raises(APIError) as excinfo:
        make_request_with_retry_json(DATACENTER_URL)
    assert excinfo.value.status_code == 500
    script(429)
    with pytest.raises(RateLimitError):
        make_request_with_retry_json(DATACENTER_URL, max_retries=1)
    script(*[requests.exceptions.ConnectTimeout("down") for _ in range(3)])
    with pytest.raises(NetworkError):
        make_request_with_retry_json(DATACENTER_URL)
    script(_remote_disconnected())
    with pytest.raises(RateLimitError):
        make_request_with_retry_json(PUSH2_URL)


def test_requests_link_returns_none_after_retries(script):
    from akshare.futures.requests_fun import requests_link

    calls, sleeps = script(
        *[requests.exceptions.ConnectTimeout("down") for _ in range(3)]
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert requests_link("https://www.shfe.com.cn/data") is None
    assert len(calls) == 3
    # 原先固定等 5 秒、最多 20 次，最坏要等近 2 分钟
    assert sum(sleeps) < 10
    assert any("链接失败" in str(w.message) for w in caught)


def test_requests_link_rejects_bad_method_without_request(script):
    from akshare.futures.requests_fun import requests_link

    calls, _ = script()
    with pytest.raises(ValueError):
        requests_link("https://www.shfe.com.cn/data", method="put")
    assert calls == []


def test_dce_contract_list_no_longer_loops_forever(script):
    import datetime

    from akshare.futures.futures_cot import _get_dce_contract_list

    calls, _ = script(*[requests.exceptions.ConnectTimeout("down") for _ in range(3)])
    with pytest.raises(requests.exceptions.ConnectTimeout):
        _get_dce_contract_list(datetime.date(2026, 10, 28), "V")
    assert len(calls) == 3
