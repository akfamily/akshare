# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/07/22 15:00
Desc: 中证指数-所有指数-历史行情数据
http://www.csindex.com.cn/zh-CN/indices/index-detail/H30374
"""
import pandas as pd
import requests


def stock_zh_index_hist_csindex(symbol: str = "H30374") -> pd.DataFrame:
    """
    中证指数获取某个指数的 5 年历史行情数据
    P.S. 只有收盘价，正常情况下不应使用该接口，除非指数只有中证网站有
    http://www.csindex.com.cn/zh-CN/indices/index-detail/H30374
    :param symbol: 指数代码; e.g., H30374
    :type symbol: str
    :return: 包含日期和收盘价的指数数据
    :rtype: pandas.DataFrame
    """
    url = f"http://www.csindex.com.cn/zh-CN/indices/index-detail/{symbol}"
    params = {
        "earnings_performance": "5年",
        "data_type": "json"
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    data_df = pd.DataFrame(data_json)[["tradedate", "tclose"]]
    data_df["tradedate"] = pd.to_datetime(data_df["tradedate"])
    data_df.columns = ["date", "close"]
    return data_df


if __name__ == "__main__":
    stock_zh_index_hist_csindex_df = stock_zh_index_hist_csindex(symbol="H30374")
    print(stock_zh_index_hist_csindex_df)
