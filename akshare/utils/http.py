#!/usr/bin/env python
"""
Date: 2026/10/30
Desc: 统一的 HTTP 请求入口
数据接口一律经本模块发请求，不直接调用 requests 或 curl_cffi.requests 的 get / post /
Session，由 pyproject.toml 中 Ruff 的 banned-api 规则强制。未显式传入 timeout、proxies
时，在调用时从 akshare.utils.context.config 读取全局设置。
需要模拟浏览器 TLS 指纹的数据源改用 curl_get / curl_post / CurlSession。
需要重试时用 request_with_retry，不要在模块里自己写重试循环。
"""

import io
import random
import re
import time
from http.client import RemoteDisconnected
from urllib.parse import urlsplit

import requests
from curl_cffi import requests as curl_requests
from requests.adapters import HTTPAdapter

from akshare.exceptions import RateLimitError
from akshare.utils.context import config

# 东方财富 push2 系行情服务器（push2、push2his、push2ex、push2delay 及 82.push2 等编号子域）
# 在短时间内请求较多时直接断开连接，表现为 RemoteDisconnected。实测 2026-10-30：
# 翻页约 5 页即被封，首次约 5 分钟恢复；解封后再请求一两次又会被封，冷却 7 分钟仍未
# 恢复。此时重试只会延长封禁，因此识别出来后立即报错，不再重试
_PUSH2_HOST = re.compile(r"^(?:\d+\.)?push2(?:his|ex|delay)?\.eastmoney\.com$")
_PUSH2_BAN_MESSAGE = (
    "东方财富 push2 行情服务器断开了连接，通常是短时间内请求过多，当前 IP 被临时限流。"
    "首次限流一般约 5 分钟后恢复，反复触发后可能需要 40 分钟以上；"
    "等待期间不要重复调用东方财富的行情接口，否则会延长限流。"
)
# 值得重试的状态码；其余状态码原样返回，由调用方处理
_RETRY_STATUS = frozenset({429, 500, 502, 503, 504})
# 值得重试的异常：连接失败（含代理、SSL）、超时、传输中断
_RETRY_EXCEPTIONS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.ChunkedEncodingError,
)


class Push2RateLimitError(RateLimitError, requests.exceptions.ConnectionError):
    """
    东方财富 push2 限流。同时是 RateLimitError 与 requests.ConnectionError 的子类，
    原先捕获 requests.ConnectionError 的代码不受影响
    """


def _closed_without_response(exc: BaseException) -> bool:
    """
    判断异常链中是否有服务器未响应就断开连接的错误；requests 会把它包装为
    ConnectionError(ProtocolError("Connection aborted.", RemoteDisconnected(...)))
    """
    stack, seen = [exc], set()
    while stack:
        e = stack.pop()
        if id(e) in seen:
            continue
        seen.add(id(e))
        if isinstance(e, (RemoteDisconnected, ConnectionResetError)):
            return True
        stack.extend(a for a in e.args if isinstance(a, BaseException))
        stack.extend(x for x in (e.__cause__, e.__context__) if x is not None)
    return False


def _raise_if_push2_ban(url: str, exc: requests.exceptions.ConnectionError) -> None:
    host = urlsplit(url).hostname or ""
    if _PUSH2_HOST.match(host) and _closed_without_response(exc):
        raise Push2RateLimitError(_PUSH2_BAN_MESSAGE) from exc


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
    :raises Push2RateLimitError: 东方财富 push2 限流
    """
    try:
        return requests.request(method, url, **_apply_defaults(kwargs))
    except requests.exceptions.ConnectionError as exc:
        _raise_if_push2_ban(url, exc)
        raise


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
        try:
            return super().request(method, url, **_apply_defaults(kwargs))
        except requests.exceptions.ConnectionError as exc:
            _raise_if_push2_ban(url, exc)
            raise


def request_with_retry(
    method: str,
    url: str,
    *,
    max_retries: int = 3,
    base_delay: float = 1.0,
    fresh_session: bool = False,
    **kwargs,
) -> requests.Response:
    """
    带重试的 HTTP 请求，其余参数与 requests.request 一致
    连接失败、超时、传输中断与 429、5xx 状态码按指数退避加随机抖动重试；
    其他状态码不重试、原样返回，由调用方处理；东方财富 push2 限流立即抛出，不重试
    :param method: 请求方法
    :type method: str
    :param url: 请求地址
    :type url: str
    :param max_retries: 最多请求次数，含第一次
    :type max_retries: int
    :param base_delay: 第一次重试前的基础等待秒数，之后每次翻倍
    :type base_delay: float
    :param fresh_session: 每次请求都新建连接、不复用连接池；部分东方财富接口复用连接时会被断开
    :type fresh_session: bool
    :return: 响应对象；用尽次数后若仍是 429 或 5xx，返回最后一次的响应
    :rtype: requests.Response
    :raises Push2RateLimitError: 东方财富 push2 限流
    :raises requests.RequestException: 用尽次数后仍连接失败或超时，抛出最后一次的异常
    """
    last_exc = None
    for attempt in range(max_retries):
        try:
            if fresh_session:
                with Session() as session:
                    adapter = HTTPAdapter(pool_connections=1, pool_maxsize=1)
                    session.mount("http://", adapter)
                    session.mount("https://", adapter)
                    response = session.request(method, url, **kwargs)
            else:
                response = request(method, url, **kwargs)
        except Push2RateLimitError:
            raise
        except _RETRY_EXCEPTIONS as exc:
            last_exc = exc
        else:
            if response.status_code not in _RETRY_STATUS or attempt == max_retries - 1:
                return response
            last_exc = None
        if attempt < max_retries - 1:
            time.sleep(base_delay * 2**attempt + random.uniform(0, base_delay))
    raise last_exc


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
