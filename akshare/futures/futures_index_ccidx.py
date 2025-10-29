# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2025/10/29 15:00
Desc: 中证商品指数
http://www.ccidx.com/
"""

import json

import pandas as pd
import requests


def futures_index_ccidx(symbol: str = "中证商品期货指数") -> pd.DataFrame:
    """
    中证商品指数-商品指数-日频率
    http://www.ccidx.com/index.html
    :param symbol: choice of {"中证商品期货指数", "中证商品期货价格指数"}
    :type symbol: str
    :return: 商品指数-日频率
    :rtype: pandas.DataFrame
    """
    futures_index_map = {
        "中证商品期货指数": "100001.CCI",
        "中证商品期货价格指数": "000001.CCI",
    }
    url = "http://www.ccidx.com/CCI-ZZZS/index/getDateLine"
    params = {"indexId": futures_index_map[symbol]}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [json.loads(item) for item in data_json["data"]["dateLineJson"]]
    )
    temp_df.rename(
        columns={
            "tradeDate": "日期",
            "indexId": "指数代码",
            "closingPrice": "收盘点位",
            "settlePrice": "结算点位",
            "dailyIncreaseAndDecrease": "涨跌",
            "dailyIncreaseAndDecreasePercentage": "涨跌幅",
        },
        inplace=True,
    )

    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["收盘点位"] = pd.to_numeric(temp_df["收盘点位"], errors="coerce")
    temp_df["结算点位"] = pd.to_numeric(temp_df["结算点位"], errors="coerce")
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df.sort_values(by=["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    futures_index_ccidx_df = futures_index_ccidx(symbol="中证商品期货指数")
    print(futures_index_ccidx_df)
