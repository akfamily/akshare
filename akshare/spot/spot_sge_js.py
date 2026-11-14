#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 金十数据-上海黄金交易所报告
https://datacenter.jin10.com/reportType/dc_sge_report
"""

import time
import pandas as pd
from akshare.utils import http


def spot_sge_report_js() -> pd.DataFrame:
    """
    上海黄金交易所报告，数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_sge_report
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = http.get(
        url="https://cdn.jin10.com/data_center/reports/sge.json", params=params
    )
    json_data = res.json()
    big_df = pd.DataFrame()
    for item in json_data["values"].keys():
        temp_df = pd.DataFrame(json_data["values"][item])
        temp_df["date"] = item
        temp_df.columns = [
            "商品",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "涨跌",
            "涨跌幅",
            "加权平均价",
            "成交量",
            "成交金额",
            "持仓量",
            "交收方向",
            "交收量",
            "日期",
        ]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df = big_df[
        [
            "日期",
            "商品",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "涨跌",
            "涨跌幅",
            "加权平均价",
            "成交量",
            "成交金额",
            "持仓量",
            "交收方向",
            "交收量",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df = big_df.sort_values(["日期"], ignore_index=True)
    big_df["持仓量"] = pd.to_numeric(big_df["持仓量"], errors="coerce")
    big_df["交收量"] = pd.to_numeric(big_df["交收量"], errors="coerce")
    return big_df


if __name__ == "__main__":
    spot_sge_report_js_df = spot_sge_report_js()
    print(spot_sge_report_js_df)
