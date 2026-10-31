# !/usr/bin/env python
"""
Date: 2026/10/30
Desc: HTTP 请求工具函数
重试逻辑已并入 akshare.utils.http.request_with_retry，本模块仅为兼容保留
"""

from typing import Dict, Tuple

import requests

from akshare.utils import http


def request_with_retry(
    url: str,
    params: Dict = None,
    max_retries: int = 3,
    base_delay: float = 1.0,
    random_delay_range: Tuple[float, float] = (0.5, 1.5),
) -> requests.Response:
    """
    带重试机制的 HTTP GET 请求，每次新建连接；新代码请直接使用 http.request_with_retry
    :param url: 请求 URL
    :type url: str
    :param params: 请求参数
    :type params: dict
    :param max_retries: 最大重试次数
    :type max_retries: int
    :param base_delay: 基础延迟时间（秒），用于指数退避
    :type base_delay: float
    :param random_delay_range: 已不再使用，保留以兼容原有调用
    :type random_delay_range: tuple
    :return: Response 对象
    :rtype: requests.Response
    :raises: 最后一次请求的异常；状态码非 2xx 时抛出 requests.HTTPError
    """
    r = http.request_with_retry(
        "get",
        url,
        params=params,
        max_retries=max_retries,
        base_delay=base_delay,
        fresh_session=True,
    )
    r.raise_for_status()
    return r
