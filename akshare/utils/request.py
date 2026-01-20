# !/usr/bin/env python
"""
Date: 2025/12/31
Desc: HTTP 请求工具函数
"""

import random
import time
from typing import Dict, Tuple

import requests
from requests.adapters import HTTPAdapter


def request_with_retry(
    url: str,
    params: Dict = None,
    timeout: int = 15,
    max_retries: int = 3,
    base_delay: float = 1.0,
    random_delay_range: Tuple[float, float] = (0.5, 1.5),
) -> requests.Response:
    """
    带重试机制的 HTTP GET 请求
    :param url: 请求 URL
    :type url: str
    :param params: 请求参数
    :type params: dict
    :param timeout: 超时时间（秒）
    :type timeout: int
    :param max_retries: 最大重试次数
    :type max_retries: int
    :param base_delay: 基础延迟时间（秒），用于指数退避
    :type base_delay: float
    :param random_delay_range: 随机延迟范围（秒）
    :type random_delay_range: tuple
    :return: Response 对象
    :rtype: requests.Response
    :raises: 最后一次请求的异常
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            # 每次请求创建新的 Session，避免复用连接
            with requests.Session() as session:
                # 禁用连接池复用
                adapter = HTTPAdapter(pool_connections=1, pool_maxsize=1)
                session.mount("http://", adapter)
                session.mount("https://", adapter)

                response = session.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                return response

        except (requests.RequestException, ValueError) as e:
            last_exception = e

            if attempt < max_retries - 1:
                # 指数退避 + 随机抖动
                delay = base_delay * (2**attempt) + random.uniform(*random_delay_range)
                time.sleep(delay)

    raise last_exception
