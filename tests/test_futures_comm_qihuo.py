#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: futures_comm_info 的请求次数与响应校验测试

九期网限流较严。早先 symbol="所有" 时每处理一个交易所就重新取一次页面，
一次调用共发 14 个请求，自身就会触发 429；而 429 页面里没有表格，
最终报出 ValueError: No tables found 或 AttributeError: 'NoneType' object
has no attribute 'previous'，用户无从判断是被限流了。

本测试全程不联网：用 monkeypatch 顶替 requests.Session.get，与
test_legu_csrf.py 的做法一致。
"""

import pytest
import requests

from akshare.exceptions import APIError, DataParsingError, RateLimitError
from akshare.futures.futures_comm_qihuo import futures_comm_info

NGINX_429_BODY = (
    "<html>\r\n<head><title>429 Too Many Requests</title></head>\r\n"
    "<body>\r\n<center><h1>429 Too Many Requests</h1></center>\r\n"
    "<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n"
)


def _fake_response(status_code: int, text: str) -> requests.Response:
    """
    造一个只带状态码与正文的响应对象
    """
    response = requests.Response()
    response.status_code = status_code
    response._content = text.encode("utf-8")
    response.encoding = "utf-8"
    return response


@pytest.fixture
def respond(monkeypatch):
    """
    让所有 Session.get 返回同一个响应，并记录请求次数
    """
    calls = []

    def install(status_code: int, text: str):
        def fake_get(self, url, **kwargs):
            calls.append(url)
            return _fake_response(status_code, text)

        monkeypatch.setattr(requests.Session, "get", fake_get)
        return calls

    return install


def test_429_raises_rate_limit_error(respond):
    respond(429, NGINX_429_BODY)
    with pytest.raises(RateLimitError, match="429"):
        futures_comm_info(symbol="所有")


def test_other_error_status_raises_api_error(respond):
    respond(503, "<html><body>Service Unavailable</body></html>")
    with pytest.raises(APIError) as excinfo:
        futures_comm_info(symbol="所有")
    assert excinfo.value.status_code == 503


def test_page_without_update_time_raises_parsing_error(respond):
    calls = respond(200, "<html><body><p>改版后的页面</p></body></html>")
    with pytest.raises(DataParsingError, match="更新时间"):
        futures_comm_info(symbol="所有")
    # 首页取 Cookie 一次、手续费页一次，不再按交易所重复取页
    assert len(calls) == 2
