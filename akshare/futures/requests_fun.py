#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 请求网站内容的函数：链接失败时按 akshare.utils.http.request_with_retry 的策略重试
"""

from io import StringIO
from typing import Dict
import warnings

import pandas as pd
import requests

from akshare.utils import http


def _request(url: str, method: str, data: Dict, headers: Dict):
    """
    发送带重试的请求；用尽次数后仍失败时给出警告并返回 None
    """
    if method not in ("get", "post"):
        raise ValueError("请提供正确的请求方式")
    try:
        return http.request_with_retry(
            method, url, timeout=20, data=data, headers=headers
        )
    except requests.exceptions.RequestException as e:
        warnings.warn(f"{url} 链接失败，已尝试 3 次：{e}")
        return None


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
    :return: requests.response 爬取返回内容：response；链接失败时为 None
    """
    r = _request(url, method, data, headers)
    if r is not None:
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
    :return: list 网页中的表格；链接失败时为 None
    """
    r = _request(url, method, data, headers)
    if r is None:
        return None
    r.encoding = encoding
    return pd.read_html(StringIO(r.text), encoding=encoding)
