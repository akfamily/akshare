#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 请求网站内容的函数：链接失败时按 akshare.utils.http.request_with_retry 的策略重试
"""

from io import StringIO
from typing import Dict

import pandas as pd

from akshare.utils import http


def _request(url: str, method: str, data: Dict, headers: Dict):
    """
    发送带重试的请求；用尽次数后仍失败时抛出最后一次的网络异常
    """
    if method not in ("get", "post"):
        raise ValueError("请提供正确的请求方式")
    return http.request_with_retry(method, url, data=data, headers=headers)


def requests_link(
    url: str,
    encoding: str = "utf-8",
    method: str = "get",
    data: Dict = None,
    headers: Dict = None,
):
    """
    利用 requests 请求网站，爬取网站内容，如网站链接失败，最多尝试 3 次
    :param url: string 网站地址
    :param encoding: string 编码类型："utf-8", "gbk", "gb2312"
    :param method: string 访问方法："get", "post"
    :param data: dict 上传数据：键值对
    :param headers: dict 游览器请求头：键值对
    :return: requests.response 爬取返回内容：response；状态码不做检查，由调用方处理
    :raises requests.RequestException: 用尽重试次数后仍连接失败或超时
    """
    # 1.20.9 及以前失败时返回 None，调用方都没有检查，用户只能看到
    # 'NoneType' object has no attribute 'text' 这类与原因无关的报错
    r = _request(url, method, data, headers)
    r.encoding = encoding
    return r


def pandas_read_html_link(
    url: str,
    encoding: str = "utf-8",
    method: str = "get",
    data: Dict = None,
    headers: Dict = None,
):
    """
    利用 pandas 提供的 read_html 函数来直接提取网页中的表格内容，如网站链接失败，最多尝试 3 次
    :param url: string 网站地址
    :param encoding: string 编码类型："utf-8", "gbk", "gb2312"
    :param method: string 访问方法："get", "post"
    :param data: dict 上传数据：键值对
    :param headers: dict 游览器请求头：键值对
    :return: list 网页中的表格
    :raises requests.RequestException: 用尽重试次数后仍连接失败或超时
    """
    r = _request(url, method, data, headers)
    r.encoding = encoding
    return pd.read_html(StringIO(r.text), encoding=encoding)
