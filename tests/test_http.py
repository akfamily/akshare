#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: akshare.utils.http 的默认超时与代理测试

数据接口全部经 akshare.utils.http 发请求，全局超时与代理是否真正送达传输层，
决定了 ak.set_timeout / ak.set_proxies 对 1000 多个接口是否生效。

本测试全程不联网：用 monkeypatch 顶替 requests.Session.send，记录最终交给
传输层的 timeout 与 proxies，再返回一个空响应。
"""

import pytest
import requests

import akshare as ak
from akshare.utils import http
from akshare.utils.context import DEFAULT_TIMEOUT, config

PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


@pytest.fixture
def sent(monkeypatch):
    """
    记录每次 send 收到的请求与参数，并隔离全局配置与代理环境变量
    """
    # requests 除环境变量外还会读系统代理设置（Windows 注册表、macOS 网络配置），
    # 直接屏蔽其入口，避免测试结果随运行机器变化
    monkeypatch.setattr(requests.sessions, "get_environ_proxies", lambda *a, **k: {})
    monkeypatch.setattr(config, "timeout", DEFAULT_TIMEOUT)
    monkeypatch.setattr(config, "proxies", None)
    calls = []

    def fake_send(self, request, **kwargs):
        calls.append((request, kwargs))
        response = requests.Response()
        response.status_code = 200
        response.request = request
        response._content = b""
        return response

    monkeypatch.setattr(requests.Session, "send", fake_send)
    return calls


@pytest.mark.parametrize(
    "call",
    [
        lambda: http.get("https://example.com"),
        lambda: http.post("https://example.com", data={"a": "1"}),
        lambda: http.request("GET", "https://example.com"),
        lambda: http.Session().get("https://example.com"),
        lambda: http.Session().post("https://example.com", json={"a": 1}),
    ],
    ids=["get", "post", "request", "session-get", "session-post"],
)
def test_default_timeout_reaches_transport(sent, call):
    call()
    assert sent[-1][1]["timeout"] == DEFAULT_TIMEOUT


def test_explicit_timeout_wins(sent):
    http.get("https://example.com", timeout=3)
    http.Session().get("https://example.com", timeout=4)
    assert [kw["timeout"] for _, kw in sent] == [3, 4]


def test_set_timeout_applies_at_call_time(sent):
    ak.set_timeout(5)
    http.get("https://example.com")
    assert ak.get_timeout() == 5
    assert sent[-1][1]["timeout"] == 5


def test_set_proxies_applies_to_get_and_session(sent):
    ak.set_proxies(PROXY)
    http.get("https://example.com")
    http.Session().get("https://example.com")
    assert [kw["proxies"] for _, kw in sent] == [PROXY, PROXY]


def test_proxy_context_restores(sent):
    with ak.ProxyContext(PROXY):
        http.get("https://example.com")
    http.get("https://example.com")
    assert sent[0][1]["proxies"] == PROXY
    assert sent[1][1]["proxies"] == {}
    assert ak.get_proxies() is None


def test_session_proxies_kept_without_global(sent):
    """
    未设置全局代理时，模块自己给 session.proxies 赋的值不能被覆盖
    """
    session = http.Session()
    session.proxies = PROXY
    session.get("https://example.com")
    assert sent[-1][1]["proxies"] == PROXY


def test_positional_arguments_match_requests(sent):
    http.get("https://example.com/api", {"page": "2"})
    http.post("https://example.com/api", "raw-body")
    assert sent[0][0].url == "https://example.com/api?page=2"
    assert sent[1][0].body == "raw-body"


@pytest.fixture
def curl_sent(monkeypatch):
    """
    记录 curl_cffi Session.request 收到的参数，不发真实请求
    """
    from curl_cffi import requests as curl_requests

    monkeypatch.setattr(config, "timeout", DEFAULT_TIMEOUT)
    monkeypatch.setattr(config, "proxies", None)
    calls = []

    def fake_request(self, method, url, *args, **kwargs):
        calls.append((method, url, kwargs))
        return curl_requests.Response()

    monkeypatch.setattr(curl_requests.Session, "request", fake_request)
    return calls


@pytest.mark.parametrize(
    "call",
    [
        lambda: http.curl_get("https://example.com", impersonate="chrome"),
        lambda: http.curl_post("https://example.com", json={"a": 1}),
        lambda: http.CurlSession(impersonate="chrome").get("https://example.com"),
    ],
    ids=["curl-get", "curl-post", "curl-session-get"],
)
def test_curl_defaults_reach_session(curl_sent, call):
    ak.set_proxies(PROXY)
    call()
    kwargs = curl_sent[-1][2]
    assert kwargs["timeout"] == DEFAULT_TIMEOUT
    assert kwargs["proxies"] == PROXY


def test_curl_explicit_timeout_wins(curl_sent):
    http.curl_get("https://example.com", timeout=30)
    assert curl_sent[-1][2]["timeout"] == 30


def test_get_buffer_returns_content_with_defaults(monkeypatch, sent):
    def fake_send(self, request, **kwargs):
        sent.append((request, kwargs))
        response = requests.Response()
        response.status_code = 200
        response._content = b"a,b\n1,2\n"
        return response

    monkeypatch.setattr(requests.Session, "send", fake_send)
    buffer = http.get_buffer("https://example.com/data.csv")
    assert buffer.read() == b"a,b\n1,2\n"
    assert sent[-1][1]["timeout"] == DEFAULT_TIMEOUT


def test_get_buffer_raises_on_error_status(monkeypatch, sent):
    """
    与 pandas 直接读 URL 一样，错误状态码要报错，而不是把错误页当数据解析
    """

    def fake_send(self, request, **kwargs):
        response = requests.Response()
        response.status_code = 403
        response.url = request.url
        return response

    monkeypatch.setattr(requests.Session, "send", fake_send)
    with pytest.raises(requests.HTTPError, match="403"):
        http.get_buffer("https://example.com/data.csv")
