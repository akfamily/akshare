# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/21 14:31
Desc: 市场总貌
http://www.szse.cn/market/overview/index.html
http://www.sse.com.cn/market/stockdata/statistic/
"""
from io import BytesIO

import pandas as pd
import requests


def stock_szse_summary(date: str = "20200619") -> pd.DataFrame:
    """
    深证证券交易所-总貌
    http://www.szse.cn/market/overview/index.html
    :param date: 最近结束交易日
    :type date: str
    :return: 深证证券交易所-总貌
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "1803_sczm",
        "TABKEY": "tab1",
        "txtQueryDate": "-".join([date[:4], date[4:6], date[6:]]),
        "random": "0.39339437497296137",
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df["证券类别"] = temp_df["证券类别"].str.strip()
    temp_df.iloc[:, 2:] = temp_df.iloc[:, 2:].applymap(lambda x: x.replace(",", ""))
    return temp_df


def stock_sse_summary() -> pd.DataFrame:
    """
    上海证券交易所-总貌
    http://www.sse.com.cn/market/stockdata/statistic/
    :return: 上海证券交易所-总貌
    :rtype: pandas.DataFrame
    """
    url = "http://www.sse.com.cn/market/stockdata/statistic/"
    r = requests.get(url)
    r.encoding = "utf-8"
    big_df = pd.DataFrame()
    temp_list = ["总貌", "主板", "科创板"]
    for i in range(len(pd.read_html(r.text))):
        for j in range(0, 2):
            inner_df = pd.read_html(r.text)[i].iloc[:, j].str.split("  ", expand=True)
            inner_df["item"] = temp_list[i]
            big_df = big_df.append(inner_df)
    big_df.dropna(how="any", inplace=True)
    big_df.columns = ["item", "number", "type"]
    big_df = big_df[["type", "item", "number"]]
    return big_df


if __name__ == '__main__':
    stock_szse_summary_df = stock_szse_summary(date="20200619")
    print(stock_szse_summary_df)

    stock_sse_summary_df = stock_sse_summary()
    print(stock_sse_summary_df)
