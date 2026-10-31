"""
带重试的 GET 请求并校验响应；重试本身由 akshare.utils.http.request_with_retry 完成
"""

from requests.exceptions import RequestException

from akshare.exceptions import APIError, DataParsingError, NetworkError, RateLimitError
from akshare.utils import http


def _get_checked(url, params, headers, proxies, max_retries, retry_delay):
    """
    发送带重试的 GET 请求，并把失败统一映射为 akshare 的异常
    :return: 状态码为 200 的响应
    :rtype: requests.Response
    :raises RateLimitError: 上游返回 429，或东方财富 push2 限流
    :raises APIError: 上游返回 200 与 429 以外的状态码
    :raises NetworkError: 用尽重试次数后仍连接失败或超时
    """
    kwargs = dict(params=params, headers=headers)
    # 未指定时不传 proxies，由 http 读取 ak.set_proxies 的全局设置
    if proxies is not None:
        kwargs["proxies"] = proxies
    try:
        response = http.request_with_retry(
            "get", url, max_retries=max_retries, base_delay=retry_delay, **kwargs
        )
    except RateLimitError:
        raise
    except RequestException as e:
        raise NetworkError(
            f"Failed to connect after {max_retries} attempts: {str(e)}"
        ) from e
    if response.status_code == 429:
        raise RateLimitError(
            f"Rate limit exceeded. Status code: {response.status_code}"
        )
    if response.status_code != 200:
        raise APIError(
            f"API request failed. Status code: {response.status_code}",
            status_code=response.status_code,
        )
    return response


def make_request_with_retry_json(
    url, params=None, headers=None, proxies=None, max_retries=3, retry_delay=1
):
    """
    发送 HTTP GET 请求，支持重试机制和代理设置。

    :param url: 请求的 URL
    :param params: URL 参数 (可选)
    :param headers: 请求头 (可选)
    :param proxies: 代理设置 (可选)，未指定时使用 ak.set_proxies 的全局设置
    :param max_retries: 最多请求次数
    :param retry_delay: 初始重试延迟（秒）
    :return: 解析后的 JSON 数据
    """
    response = _get_checked(url, params, headers, proxies, max_retries, retry_delay)
    try:
        data = response.json()
    except ValueError as e:
        raise DataParsingError("Failed to parse JSON response") from e
    if not data:
        raise DataParsingError("Empty response data")
    return data


def make_request_with_retry_text(
    url, params=None, headers=None, proxies=None, max_retries=3, retry_delay=1
):
    """
    发送 HTTP GET 请求，支持重试机制和代理设置。

    :param url: 请求的 URL
    :param params: URL 参数 (可选)
    :param headers: 请求头 (可选)
    :param proxies: 代理设置 (可选)，未指定时使用 ak.set_proxies 的全局设置
    :param max_retries: 最多请求次数
    :param retry_delay: 初始重试延迟（秒）
    :return: 响应文本
    """
    response = _get_checked(url, params, headers, proxies, max_retries, retry_delay)
    if not response.text:
        raise DataParsingError("Empty response data")
    return response.text
