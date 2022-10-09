#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/9 15:26
Desc: 百度股市通- A 股-财务报表-估值数据
https://gushitong.baidu.com/stock/ab-002044
"""
import requests
import pandas as pd


def stock_zh_valuation_baidu(
    symbol: str = "002044", indicator: str = "总市值"
) -> pd.DataFrame:
    """
    百度股市通- A 股-财务报表-估值数据
    https://gushitong.baidu.com/stock/ab-002044
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"总市值", "市盈率(TTM)", "市盈率(静)", "市净率", "市现率"}
    :type indicator: str
    :return: 估值数据
    :rtype: pandas.DataFrame
    """
    url = "https://finance.pae.baidu.com/selfselect/openapi"
    params = {
        "srcid": "51171",
        "code": symbol,
        "market": "ab",
        "tag": f"{indicator}",
        "chart_select": "全部",
        "skip_industry": "0",
        "finClientType": "pc",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["Result"]["chartInfo"][0]["body"])
    temp_df.columns = ["date", "value"]
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["value"] = pd.to_numeric(temp_df["value"])
    return temp_df


if __name__ == "__main__":
    stock_zh_valuation_baidu_df = stock_zh_valuation_baidu(
        symbol="002044", indicator="总市值"
    )
    print(stock_zh_valuation_baidu_df)
