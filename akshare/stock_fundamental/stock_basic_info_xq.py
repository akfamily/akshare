# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/3/10 20:00
Desc: 雪球-个股-公司概况-公司简介
https://xueqiu.com/snowman/S/SH601127/detail#/GSJJ
"""

import pandas as pd
import requests

from akshare.utils.cons import headers


def stock_individual_basic_info_xq(
    symbol: str = "SH601127", token: str = None, timeout: float = None
) -> pd.DataFrame:
    """
    雪球-个股-公司概况-公司简介
    https://xueqiu.com/snowman/S/SH601127/detail#/GSJJ
    :param symbol: 证券代码
    :type symbol: str
    :param token: 雪球财经的 token
    :type token: str
    :param timeout: 设置超时时间
    :type timeout: float
    :return: 公司简介
    :rtype: pandas.DataFrame
    """
    xq_a_token = token or "afb2d000c59b0e6fa5539ff13798ca8e64330985"
    url = "https://stock.xueqiu.com/v5/stock/f10/cn/company.json"
    params = {
        "symbol": symbol,
    }
    headers.update({"cookie": f"xq_a_token={xq_a_token};"})
    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["item", "value"]
    return temp_df


if __name__ == "__main__":
    stock_individual_basic_info_xq_df = stock_individual_basic_info_xq(
        symbol="SH601127"
    )
    print(stock_individual_basic_info_xq_df)
