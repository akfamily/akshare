# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/9/21 16:36
Desc: 行情中心-沪深股市-次新股
http://vip.stock.finance.sina.com.cn/mkt/#new_stock
"""
import math

import pandas as pd
import requests


def stock_zh_a_new():
    """
    行情中心-沪深股市-次新股
    http://vip.stock.finance.sina.com.cn/mkt/#new_stock
    :return: 次新股行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount"
    params = {"node": "new_stock"}
    r = requests.get(url, params=params)
    total_page = math.ceil(int(r.json()) / 80)
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    big_df = pd.DataFrame()
    for page in range(1, total_page + 1):
        params = {
            "page": str(page),
            "num": "80",
            "sort": "symbol",
            "asc": "1",
            "node": "new_stock",
            "symbol": "",
            "_s_r_a": "page",
        }
        r = requests.get(url, params=params)
        r.encoding = "gb2312"
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df = big_df[
        [
            "symbol",
            "code",
            "name",
            "open",
            "high",
            "low",
            "volume",
            "amount",
            "mktcap",
            "turnoverratio",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_zh_a_new_df = stock_zh_a_new()
    print(stock_zh_a_new_df)
