#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/11/27 19:58
Desc: 东方财富网-数据中心-期货库存数据
https://data.eastmoney.com/ifdata/kcsj.html
"""
import pandas as pd
import requests


def futures_inventory_em(symbol: str = "沪铝") -> pd.DataFrame:
    """
    东方财富网-数据中心-期货库存数据
    https://data.eastmoney.com/ifdata/kcsj.html
    :param symbol: https://data.eastmoney.com/ifdata/kcsj.html 对应的中文名称, 如: 沪铝
    :type symbol: str
    :return: 指定品种的库存数据
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_FUTU_POSITIONCODE",
        "columns": "TRADE_MARKET_CODE,TRADE_CODE,TRADE_TYPE",
        "filter": '(IS_MAINCODE="1")',
        "pageNumber": "1",
        "pageSize": "500",
        "source": "WEB",
        "client": "WEB",
        "_": "1669352163467",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    symbol_dict = dict(zip(temp_df["TRADE_TYPE"], temp_df["TRADE_CODE"]))

    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_FUTU_STOCKDATA",
        "columns": "SECURITY_CODE,TRADE_DATE,ON_WARRANT_NUM,ADDCHANGE",
        "filter": f"""(SECURITY_CODE="{symbol_dict[symbol]}")(TRADE_DATE>='2020-10-28')""",
        "pageNumber": "1",
        "pageSize": "500",
        "sortTypes": "-1",
        "sortColumns": "TRADE_DATE",
        "source": "WEB",
        "client": "WEB",
        "_": "1669352163467",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])

    temp_df.columns = ["-", "日期", "库存", "增减"]
    temp_df = temp_df[["日期", "库存", "增减"]]
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["库存"] = pd.to_numeric(temp_df["库存"], errors="coerce")
    temp_df["增减"] = pd.to_numeric(temp_df["增减"], errors="coerce")
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    return temp_df


if __name__ == "__main__":
    futures_inventory_em_df = futures_inventory_em(symbol="豆一")
    print(futures_inventory_em_df)
