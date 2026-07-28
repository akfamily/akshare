# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/5/16 19:00
Desc: 雪球-个股-公司概况-公司简介
https://xueqiu.com/snowman/S/SH601127/detail#/GSJJ
"""

from typing import Any, Optional

import pandas as pd
import requests

from akshare.exceptions import APIError, NetworkError
from akshare.utils.cons import headers


def _get_xq_company_data(
    url: str, symbol: str, token: Optional[str] = None, timeout: Optional[float] = None
) -> dict[str, Any]:
    """
    获取雪球公司简介接口的原始数据

    :param url: 接口地址
    :type url: str
    :param symbol: 证券代码
    :type symbol: str
    :param token: 雪球财经的 xq_a_token
    :type token: Optional[str]
    :param timeout: 设置超时时间
    :type timeout: Optional[float]
    :return: 公司简介接口原始数据
    :rtype: dict[str, Any]
    :raises NetworkError: 网络请求异常
    :raises APIError: 上游接口返回异常或需要有效登录态
    """
    from akshare.stock.cons import xq_a_token

    session = requests.Session()
    xq_token = token or xq_a_token
    request_headers = headers.copy()
    request_headers.update({"cookie": f"xq_a_token={xq_token};"})
    try:
        session.get(url="https://xueqiu.com", headers=request_headers, timeout=timeout)
        r = session.get(
            url, params={"symbol": symbol}, headers=request_headers, timeout=timeout
        )
        data_json = r.json()
    except requests.RequestException as err:
        raise NetworkError(f"Failed to request Xueqiu company endpoint: {err}") from err
    except ValueError as err:
        raise APIError("Xueqiu company endpoint returned invalid JSON") from err

    if "data" not in data_json:
        error_code = data_json.get("error_code")
        error_description = data_json.get("error_description", "Unknown error")
        raise APIError(
            "Xueqiu company endpoint requires a valid xq_a_token or login session; "
            f"upstream returned {error_code}: {error_description}",
            status_code=r.status_code,
        )

    return data_json["data"]


def _build_xq_company_df(data: dict[str, Any]) -> pd.DataFrame:
    """
    构造雪球公司简介数据表

    :param data: 公司简介原始数据
    :type data: dict[str, Any]
    :return: 公司简介数据表
    :rtype: pandas.DataFrame
    """
    if not data:
        return pd.DataFrame(columns=["item", "value"])
    temp_df = pd.DataFrame(data)
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["item", "value"]
    return temp_df


def stock_individual_basic_info_xq(
    symbol: str = "SH601127",
    token: Optional[str] = None,
    timeout: Optional[float] = None,
) -> pd.DataFrame:
    """
    雪球-个股-公司概况-公司简介
    https://xueqiu.com/snowman/S/SH601127/detail#/GSJJ
    :param symbol: 证券代码
    :type symbol: str
    :param token: 雪球财经的 xq_a_token
    :type token: Optional[str]
    :param timeout: 设置超时时间
    :type timeout: Optional[float]
    :return: 公司简介
    :rtype: pandas.DataFrame
    :raises APIError: 雪球接口需要有效登录态时抛出
    """
    url = "https://stock.xueqiu.com/v5/stock/f10/cn/company.json"
    data = _get_xq_company_data(url=url, symbol=symbol, token=token, timeout=timeout)
    return _build_xq_company_df(data=data)


def stock_individual_basic_info_us_xq(
    symbol: str = "NVDA",
    token: Optional[str] = None,
    timeout: Optional[float] = None,
) -> pd.DataFrame:
    """
    雪球-个股-公司概况-公司简介
    https://xueqiu.com/snowman/S/NVDA/detail#/GSJJ
    :param symbol: 证券代码
    :type symbol: str
    :param token: 雪球财经的 xq_a_token
    :type token: Optional[str]
    :param timeout: 设置超时时间
    :type timeout: Optional[float]
    :return: 公司简介
    :rtype: pandas.DataFrame
    :raises APIError: 雪球接口需要有效登录态时抛出
    """
    url = "https://stock.xueqiu.com/v5/stock/f10/us/company.json"
    data = _get_xq_company_data(url=url, symbol=symbol, token=token, timeout=timeout)
    return _build_xq_company_df(data=data)


def stock_individual_basic_info_hk_xq(
    symbol: str = "02097",
    token: Optional[str] = None,
    timeout: Optional[float] = None,
) -> pd.DataFrame:
    """
    雪球-个股-公司概况-公司简介
    https://xueqiu.com/S/00700
    :param symbol: 证券代码
    :type symbol: str
    :param token: 雪球财经的 xq_a_token
    :type token: Optional[str]
    :param timeout: 设置超时时间
    :type timeout: Optional[float]
    :return: 公司简介
    :rtype: pandas.DataFrame
    :raises APIError: 雪球接口需要有效登录态时抛出
    """
    url = "https://stock.xueqiu.com/v5/stock/f10/hk/company.json"
    data = _get_xq_company_data(url=url, symbol=symbol, token=token, timeout=timeout)
    return _build_xq_company_df(data=data)


if __name__ == "__main__":
    stock_individual_basic_info_xq_df = stock_individual_basic_info_xq(
        symbol="SH601127"
    )
    print(stock_individual_basic_info_xq_df)

    stock_us_individual_basic_info_us_xq_df = stock_individual_basic_info_us_xq(
        symbol="NVDA"
    )
    print(stock_us_individual_basic_info_us_xq_df)

    stock_individual_basic_info_hk_xq_df = stock_individual_basic_info_hk_xq(
        symbol="02097"
    )
    print(stock_individual_basic_info_hk_xq_df)
