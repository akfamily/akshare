#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/3/9 20:26
Desc: 百度股市通-港股-财务报表-估值数据
https://gushitong.baidu.com/stock/hk-06969
"""
import http.client
import json
import urllib

import pandas as pd


def stock_hk_valuation_baidu(
    symbol: str = "06969", indicator: str = "总市值", period: str = "近一年"
) -> pd.DataFrame:
    """
    百度股市通-港股-财务报表-估值数据
    https://gushitong.baidu.com/stock/hk-06969
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"总市值", "市盈率(TTM)", "市盈率(静)", "市净率", "市现率"}
    :type indicator: str
    :param period: choice of {"近一年", "近三年", "近五年", "近十年", "全部"}
    :type period: str
    :return: 估值数据
    :rtype: pandas.DataFrame
    """
    params = {
        "srcid": "51171",
        "code": symbol,
        "market": "hk",
        "tag": indicator,
        "chart_select": period,
        "skip_industry": "0",
        "finClientType": "pc",
    }
    conn = http.client.HTTPSConnection("finance.pae.baidu.com")
    conn.request("GET", f"/selfselect/openapi?{urllib.parse.urlencode(params)}")
    r = conn.getresponse()
    data_json = json.loads(r.read())
    temp_df = pd.DataFrame(data_json["Result"]["chartInfo"][0]["body"])
    temp_df.columns = ["date", "value"]
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["value"] = pd.to_numeric(temp_df["value"])
    return temp_df


if __name__ == "__main__":
    stock_hk_valuation_baidu_df = stock_hk_valuation_baidu(
        symbol="00700", indicator="总市值", period="近五年"
    )
    print(stock_hk_valuation_baidu_df)
