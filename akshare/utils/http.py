#!/usr/bin/env python
"""
Date: 2026/10/30
Desc: 统一的 HTTP 请求入口
数据接口一律经本模块发请求，不直接调用 requests.get / requests.post / requests.Session，
由 pyproject.toml 中 Ruff 的 banned-api 规则强制。未显式传入 timeout、proxies 时，
在调用时从 akshare.utils.context.config 读取全局设置。
"""

import requests

from akshare.utils.context import config


def _apply_defaults(kwargs: dict) -> dict:
    kwargs.setdefault("timeout", config.timeout)
    # proxies 为 None 时 requests 仍会读取 HTTP_PROXY、HTTPS_PROXY 环境变量
    kwargs.setdefault("proxies", config.proxies)
    return kwargs


def request(method: str, url: str, **kwargs) -> requests.Response:
    """
    发送 HTTP 请求，签名与 requests.request 一致
    :param method: 请求方法
    :type method: str
    :param url: 请求地址
    :type url: str
    :return: 响应对象
    :rtype: requests.Response
    """
    return requests.request(method, url, **_apply_defaults(kwargs))


def get(url: str, params=None, **kwargs) -> requests.Response:
    """
    发送 GET 请求，签名与 requests.get 一致
    :param url: 请求地址
    :type url: str
    :param params: 查询参数
    :type params: dict
    :return: 响应对象
    :rtype: requests.Response
    """
    return request("get", url, params=params, **kwargs)


def post(url: str, data=None, json=None, **kwargs) -> requests.Response:
    """
    发送 POST 请求，签名与 requests.post 一致
    :param url: 请求地址
    :type url: str
    :param data: 表单或原始请求体
    :type data: dict or str or bytes
    :param json: JSON 请求体
    :type json: dict or list
    :return: 响应对象
    :rtype: requests.Response
    """
    return request("post", url, data=data, json=json, **kwargs)


class Session(requests.Session):
    """
    requests.Session 的子类，经它发出的每个请求同样应用全局超时与代理
    """

    def request(self, method, url, **kwargs):
        return super().request(method, url, **_apply_defaults(kwargs))
