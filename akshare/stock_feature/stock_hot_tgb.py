# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/4/27 17:01
Desc: 淘股吧-热门股票
https://www.taoguba.com.cn/stock/moreHotStock
"""
import pandas as pd
import requests


def stock_hot_tgb() -> pd.DataFrame:
    """
    淘股吧-热门股票
    https://www.taoguba.com.cn/stock/moreHotStock
    :return: 热门股票
    :rtype: pandas.DataFrame
    """
    url = "https://www.taoguba.com.cn/stock/moreHotStock"
    r = requests.get(url)
    temp_df = pd.concat([pd.read_html(r.text, header=0)[0], pd.read_html(r.text, header=0)[1]])
    temp_df = temp_df[[
        "个股代码",
        "个股名称",
    ]]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == '__main__':
    stock_hot_tgb_df = stock_hot_tgb()
    print(stock_hot_tgb_df)
