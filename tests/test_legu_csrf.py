#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/9/16
Desc: get_cookie_csrf 的响应校验测试，覆盖 issue #7417

乐咕乐股的 14 个接口共用 get_cookie_csrf 取 CSRF 令牌。上游对它拒绝的客户端
返回 nginx 403，该错误页不含 _csrf meta 标签，早先的实现会在 None 上取 .attrs，
而抛出的 AttributeError: 'NoneType' object has no attribute 'attrs' 既不含
状态码也不提上游，用户无从自查。同一报错自 2024 年起已复发多次，
见 #4680、#4782、#4785、#4787、#7237、#7417。

本测试全程不联网：用 monkeypatch 顶替 requests.Session.get，与 test_registry.py
的做法一致。
"""

import pytest
import requests

from akshare.exceptions import APIError, DataParsingError
from akshare.stock_feature.stock_a_indicator import get_cookie_csrf

# 上游拒绝请求时实际返回的页面，正文取自真实响应（nginx/1.22.1，153 字节）
NGINX_403_BODY = (
    "<html>\r\n<head><title>403 Forbidden</title></head>\r\n"
    "<body>\r\n<center><h1>403 Forbidden</h1></center>\r\n"
    "<hr><center>nginx/1.22.1</center>\r\n</body>\r\n</html>\r\n"
)

# 正常页面里 CSRF 令牌所在的标签形态
OK_TOKEN = "bb9300d0-1c09-45d6-aba2-f76223e7000d"
OK_BODY = (
    f'<html><head><meta content="{OK_TOKEN}" name="_csrf"/></head><body></body></html>'
)


def _fake_response(status_code: int, text: str) -> requests.Response:
    """
    造一个只带状态码与正文的响应对象。

    直接构造 requests.Response 而不是自定义替身，这样 raise_for_status 与 cookies
    都是真实实现，测的才是模块在真实响应对象上的行为。

    :param status_code: HTTP 状态码
    :type status_code: int
    :param text: 响应正文
    :type text: str
    :return: 可供模块消费的响应对象
    :rtype: requests.Response
    """
    response = requests.Response()
    response.status_code = status_code
    response._content = text.encode("utf-8")
    response.encoding = "utf-8"
    response.url = "https://legulegu.com/stockdata/marketcap-gdp"
    return response


@pytest.fixture
def patch_get(monkeypatch):
    """
    顶替 requests.Session.get，使其返回指定响应。

    :param monkeypatch: pytest 提供的替换工具
    :return: 接收响应对象的注册函数
    """

    def _patch(response: requests.Response) -> None:
        monkeypatch.setattr(
            requests.Session, "get", lambda self, *args, **kwargs: response
        )

    return _patch


def test_csrf_raises_api_error_on_403(patch_get):
    """
    上游返回 403 时应抛出带状态码的 APIError，而不是 AttributeError。
    """
    patch_get(_fake_response(403, NGINX_403_BODY))
    with pytest.raises(APIError) as exc_info:
        get_cookie_csrf(url="https://legulegu.com/stockdata/marketcap-gdp")
    assert exc_info.value.status_code == 403


def test_csrf_error_message_mentions_status_and_source(patch_get):
    """
    错误信息必须让用户看出是上游拒绝：带上状态码与站点名。

    这是本次修复的要点——原先的 AttributeError 两者都不含，用户只能来提 issue。
    """
    patch_get(_fake_response(403, NGINX_403_BODY))
    with pytest.raises(APIError) as exc_info:
        get_cookie_csrf(url="https://legulegu.com/stockdata/marketcap-gdp")
    message = str(exc_info.value)
    assert "403" in message
    assert "legulegu" in message


def test_csrf_wraps_connection_error_without_response(monkeypatch):
    """
    连接类异常的 response 为 None，取状态码时不得再引发 AttributeError。
    """

    def _boom(self, *args, **kwargs):
        raise requests.exceptions.ConnectionError("dns failure")

    monkeypatch.setattr(requests.Session, "get", _boom)
    with pytest.raises(APIError) as exc_info:
        get_cookie_csrf(url="https://legulegu.com/stockdata/marketcap-gdp")
    assert exc_info.value.status_code is None


def test_csrf_raises_parsing_error_when_tag_missing(patch_get):
    """
    状态码正常但页面缺少 _csrf 标签时，应抛出 DataParsingError。

    对应上游改版或返回了 200 的拦截页，此时不该再在 None 上取 .attrs。
    """
    patch_get(_fake_response(200, "<html><head></head><body>hi</body></html>"))
    with pytest.raises(DataParsingError):
        get_cookie_csrf(url="https://legulegu.com/stockdata/marketcap-gdp")


def test_csrf_returns_token_on_normal_page(patch_get):
    """
    正常页面仍须照常取出令牌并放进请求头，确保改动没有影响成功路径。
    """
    patch_get(_fake_response(200, OK_BODY))
    result = get_cookie_csrf(url="https://legulegu.com/stockdata/marketcap-gdp")
    assert result["headers"]["X-CSRF-Token"] == OK_TOKEN
    assert "cookies" in result


def test_csrf_does_not_mutate_shared_headers(patch_get):
    """
    不得污染 akshare.utils.cons.headers——它是全库共用的字典。
    """
    from akshare.utils.cons import headers

    patch_get(_fake_response(200, OK_BODY))
    get_cookie_csrf(url="https://legulegu.com/stockdata/marketcap-gdp")
    assert "X-CSRF-Token" not in headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
