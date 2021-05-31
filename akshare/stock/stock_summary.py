# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/30 14:31
Desc: 股票数据-总貌-市场总貌
股票数据-总貌-成交概括
http://www.szse.cn/market/overview/index.html
http://www.sse.com.cn/market/stockdata/statistic/
"""
from io import BytesIO

import demjson
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
    temp_df = pd.read_excel(BytesIO(r.content), engine="xlrd")
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


def stock_sse_deal_daily(date: str = "20210325") -> pd.DataFrame:
    """
    上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
    http://www.sse.com.cn/market/stockdata/overview/day/
    :return: 每日股票情况
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/commonQuery.do"
    params = {
        "jsonCallBack": "jsonpCallback89906",
        "searchDate": "-".join([date[:4], date[4:6], date[6:]]),
        "sqlId": "COMMON_SSE_SJ_GPSJ_CJGK_DAYCJGK_C",
        "stockType": "90",
        "_": "1616744620492",
    }
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text.strip("\r\njsonpCallback89906(")[:-1])
    temp_df = pd.DataFrame(data_json["result"])
    temp_df = temp_df.T
    temp_df.reset_index(inplace=True)
    temp_df.columns = [
        "单日情况",
        "主板A",
        "股票",
        "主板B",
        "_",
        "股票回购",
        "科创板",
    ]
    temp_df = temp_df[
        [
            "单日情况",
            "股票",
            "主板A",
            "主板B",
            "科创板",
            "股票回购",
        ]
    ]
    temp_df["单日情况"] = [
        "流通市值",
        "流通换手率",
        "平均市盈率",
        "_",
        "市价总值",
        "_",
        "换手率",
        "_",
        "挂牌数",
        "_",
        "_",
        "_",
        "_",
        "_",
        "成交笔数",
        "成交金额",
        "成交量",
        "次新股换手率",
        "_",
        "_",
    ]

    temp_df = temp_df[temp_df["单日情况"] != "_"]
    temp_df["单日情况"] = temp_df["单日情况"].astype("category")
    list_custom_new = [
        "挂牌数",
        "市价总值",
        "流通市值",
        "成交金额",
        "成交量",
        "成交笔数",
        "平均市盈率",
        "换手率",
        "次新股换手率",
        "流通换手率",
    ]
    temp_df["单日情况"].cat.set_categories(list_custom_new, inplace=True)
    temp_df.sort_values("单日情况", ascending=True, inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


if __name__ == "__main__":
    stock_szse_summary_df = stock_szse_summary(date="20200619")
    print(stock_szse_summary_df)

    stock_sse_summary_df = stock_sse_summary()
    print(stock_sse_summary_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20201111")
    print(stock_sse_deal_daily_df)
