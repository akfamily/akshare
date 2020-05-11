# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/11 19:47
Desc: 东方财富网-数据中心-资金流向
http://data.eastmoney.com/zjlx/detail.html
"""
import json
import time

import pandas as pd
import requests


def stock_individual_fund_flow(
    stock: str = "000425", market: str = "sh"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向
    http://data.eastmoney.com/zjlx/detail.html
    :param stock: 股票代码
    :type stock: str
    :param market: 股票市场; 上海证券交易所: sh, 深证证券交易所: sz
    :type market: str
    :return: 近期个股的资金流数据
    :rtype: pandas.DataFrame
    """
    market_map = {"sh": 1, "sz": 0}
    url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "lmt": "0",
        "klt": "101",
        "secid": f"{market_map[market]}.{stock}",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery183003743205523325188_1589197499471",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{") : -2])
    content_list = json_data["data"]["klines"]
    temp_df = pd.DataFrame([item.split(",") for item in content_list])
    temp_df.columns = [
        "日期",
        "主力净流入-净额",
        "小单净流入-净额",
        "中单净流入-净额",
        "大单净流入-净额",
        "超大单净流入-净额",
        "主力净流入-净占比",
        "小单净流入-净占比",
        "中单净流入-净占比",
        "大单净流入-净占比",
        "超大单净流入-净占比",
        "收盘价",
        "涨跌幅",
        "-",
        "-",
    ]
    return temp_df.iloc[:, :-2]


if __name__ == "__main__":
    stock_individual_fund_flow_df = stock_individual_fund_flow(
        stock="600094", market="sh"
    )
    print(stock_individual_fund_flow_df)
