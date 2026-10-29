#!/usr/bin/env python
"""
Date: 2026/10/30
Desc: 统一的 HTTP 请求入口
数据接口一律经本模块发请求，不直接调用 requests 或 curl_cffi.requests 的 get / post /
Session，由 pyproject.toml 中 Ruff 的 banned-api 规则强制。未显式传入 timeout、proxies
时，在调用时从 akshare.utils.context.config 读取全局设置。
需要模拟浏览器 TLS 指纹的数据源改用 curl_get / curl_post / CurlSession。
"""

import io

import requests
from curl_cffi import requests as curl_requests

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


def get_buffer(url: str, **kwargs) -> io.BytesIO:
    """
    下载文件并包装为内存缓冲区，供 pandas 读取，如 pd.read_csv(http.get_buffer(url))
    pandas 直接读 URL 时自行用 urllib 下载，不受全局超时与代理控制，因此改经本函数
    :param url: 文件地址
    :type url: str
    :return: 文件内容
    :rtype: io.BytesIO
    :raises requests.HTTPError: 上游返回非 2xx，与 pandas 直接读 URL 时一样报错
    """
    r = get(url, **kwargs)
    r.raise_for_status()
    return io.BytesIO(r.content)


class Session(requests.Session):
    """
    requests.Session 的子类，经它发出的每个请求同样应用全局超时与代理
    """

    def request(self, method, url, **kwargs):
        return super().request(method, url, **_apply_defaults(kwargs))


def curl_request(method: str, url: str, **kwargs) -> curl_requests.Response:
    """
    经 curl_cffi 发送 HTTP 请求，签名与 curl_cffi.requests.request 一致
    注意 curl_cffi 把连接超时与读取超时组成的二元组的两项之和当作整个请求的总时长上限，
    与 requests 中读取超时表示两次收到数据之间的最长间隔不同
    :param method: 请求方法
    :type method: str
    :param url: 请求地址
    :type url: str
    :return: 响应对象
    :rtype: curl_cffi.requests.Response
    """
    return curl_requests.request(method=method, url=url, **_apply_defaults(kwargs))


def curl_get(url: str, **kwargs) -> curl_requests.Response:
    """
    经 curl_cffi 发送 GET 请求，签名与 curl_cffi.requests.get 一致
    :param url: 请求地址
    :type url: str
    :return: 响应对象
    :rtype: curl_cffi.requests.Response
    """
    return curl_request("GET", url, **kwargs)


def curl_post(url: str, **kwargs) -> curl_requests.Response:
    """
    经 curl_cffi 发送 POST 请求，签名与 curl_cffi.requests.post 一致
    :param url: 请求地址
    :type url: str
    :return: 响应对象
    :rtype: curl_cffi.requests.Response
    """
    return curl_request("POST", url, **kwargs)


class CurlSession(curl_requests.Session):
    """
    curl_cffi.requests.Session 的子类，经它发出的每个请求同样应用全局超时与代理
    """

    def request(self, method, url, *args, **kwargs):
        return super().request(method, url, *args, **_apply_defaults(kwargs))
