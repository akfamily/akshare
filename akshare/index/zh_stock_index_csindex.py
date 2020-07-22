# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/07/22 15:00
Desc: 中证指数-所有指数-历史行情数据
"""
import requests
import numpy as np
import pandas as pd

# 获取指定代码的5年收盘数据


def stock_zh_index_hist_csindex(symbol: str = 'H30374') -> pd.DataFrame:
    """
    从中证指数获取某个指数的5年历史行情数据，只有收盘价，正常情况下不应使用该接口，除非指数只有中证网站有
    :param symbol: str e.g., H30374
    :return: pandas.DataFrame
        date        close
        2015-07-22  3948.79
        2015-07-23  4031.31
        2015-07-24  3974.93
        2015-07-27  3705.04
        2015-07-28  3645.59
        ...         ...
        2020-07-15  4388.49
        2020-07-16  4194.77
        2020-07-17  4225.59
        2020-07-20  4330.10
        2020-07-21  4381.20
    """
    url = f'http://www.csindex.com.cn/zh-CN/indices/index-detail/{symbol}?earnings_performance=5年&data_type=json'
    res = requests.get(url)
    data_df = pd.DataFrame(res.json())[['tradedate', 'tclose']]
    data_df['tradedate'] = data_df['tradedate'].str[0:10]
    data_df.columns = ["date", "close"]
    return data_df


if __name__ == "__main__":
    stock_zh_index_hist_csindex_df = stock_zh_index_hist_csindex(
        symbol="H30374")
    print(stock_zh_index_hist_csindex_df)
