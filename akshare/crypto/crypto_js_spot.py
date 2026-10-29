#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/28
Desc: 金十数据-加密货币实时行情
https://datacenter.jin10.com/reportType/dc_bitcoin_current
"""

import pandas as pd

from akshare.utils import http


def crypto_js_spot() -> pd.DataFrame:
    """
    主流加密货币的实时行情数据，一次请求返回具体某一时刻行情数据
    https://datacenter.jin10.com/reportType/dc_bitcoin_current
    :return: pandas.DataFrame
    """
    url = "https://datacenter-api.jin10.com/crypto_currency/list"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "x-csrf-token",
        "x-version": "1.0.0",
    }
    r = http.get(url, headers=headers)
    data_json = r.json()
    data_df = pd.DataFrame(data_json["data"])
    data_df["reported_at"] = pd.to_datetime(data_df["reported_at"])
    data_df.columns = [
        "市场",
        "交易品种",
        "最近报价",
        "涨跌额",
        "涨跌幅",
        "24小时最高",
        "24小时最低",
        "24小时成交量",
        "更新时间",
    ]
    data_df["最近报价"] = pd.to_numeric(data_df["最近报价"], errors="coerce")
    data_df["涨跌额"] = pd.to_numeric(data_df["涨跌额"], errors="coerce")
    data_df["涨跌幅"] = pd.to_numeric(data_df["涨跌幅"], errors="coerce")
    data_df["24小时最高"] = pd.to_numeric(data_df["24小时最高"], errors="coerce")
    data_df["24小时最低"] = pd.to_numeric(data_df["24小时最低"], errors="coerce")
    data_df["24小时成交量"] = pd.to_numeric(data_df["24小时成交量"], errors="coerce")
    data_df["更新时间"] = data_df["更新时间"].astype(str)
    return data_df


if __name__ == "__main__":
    crypto_js_spot_df = crypto_js_spot()
    print(crypto_js_spot_df)
