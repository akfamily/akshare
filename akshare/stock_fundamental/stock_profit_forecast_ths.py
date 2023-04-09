#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/4/9 21:44
Desc: 同花顺-盈利预测
https://basic.10jqka.com.cn/new/600519/worth.html
"""
import pandas as pd
import requests


def stock_profit_forecast_ths(
    symbol: str = "600519", indicator: str = "预测年报每股收益"
) -> pd.DataFrame:
    """
    同花顺-盈利预测
    https://basic.10jqka.com.cn/new/600519/worth.html
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"预测年报每股收益", "预测年报净利润", "业绩预测详表-机构", "业绩预测详表-详细指标预测"}
    :type indicator: str
    :return: 盈利预测
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/new/{symbol}/worth.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    r.encoding = "gbk"
    if indicator == "预测年报每股收益":
        temp_df = pd.read_html(r.text)[0]
        temp_df["年度"] = temp_df["年度"].astype(str)
        return temp_df
    if indicator == "预测年报净利润":
        temp_df = pd.read_html(r.text)[1]
        temp_df["年度"] = temp_df["年度"].astype(str)
        return temp_df
    if indicator == "业绩预测详表-机构":
        temp_df = pd.read_html(r.text)[2]
        columns_list = []
        for item in temp_df.columns:
            columns_list.append(item[1])
        columns_list[2] = "预测年报每股收益" + columns_list[2]
        columns_list[3] = "预测年报每股收益" + columns_list[3]
        columns_list[4] = "预测年报每股收益" + columns_list[4]
        columns_list[5] = "预测年报净利润" + columns_list[5]
        columns_list[6] = "预测年报净利润" + columns_list[6]
        columns_list[7] = "预测年报净利润" + columns_list[7]
        temp_df.columns = columns_list
        temp_df["报告日期"] = pd.to_datetime(temp_df["报告日期"]).dt.date
        return temp_df
    if indicator == "业绩预测详表-详细指标预测":
        temp_df = pd.read_html(r.text)[3]
        temp_df.columns = [
            item.replace("（", "-").replace("）", "") for item in temp_df.columns
        ]
        return temp_df


if __name__ == "__main__":
    for item in ["预测年报每股收益", "预测年报净利润", "业绩预测详表-机构", "业绩预测详表-详细指标预测"]:
        stock_profit_forecast_ths_df = stock_profit_forecast_ths(symbol="600519", indicator=item)
        print(stock_profit_forecast_ths_df)
