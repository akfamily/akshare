#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/3 16:08
Desc: 金十数据-数据中心-主要机构-宏观经济
https://datacenter.jin10.com/
"""

import datetime
import time

import pandas as pd

from akshare.utils import http


def fund_gold_etf_holding_js() -> pd.DataFrame:
    """
    全球最大黄金 ETF—SPDR Gold Trust 持仓报告，数据区间从 20041118-至今
    https://datacenter.jin10.com/reportType/dc_etf_gold
    :return: 持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "x-csrf-token",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "category": "etf",
        "attr_id": "1",
        "max_date": "",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = http.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df.columns = [
        "日期",
        "总库存",
        "增持/减持",
        "总价值",
    ]
    big_df["商品"] = "黄金"
    big_df = big_df[
        [
            "商品",
            "日期",
            "总库存",
            "增持/减持",
            "总价值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["总库存"] = pd.to_numeric(big_df["总库存"], errors="coerce")
    big_df["增持/减持"] = pd.to_numeric(big_df["增持/减持"], errors="coerce")
    big_df["总价值"] = pd.to_numeric(big_df["总价值"], errors="coerce")
    big_df = big_df.sort_values(["日期"])
    big_df = big_df.reset_index(drop=True)
    return big_df


def fund_silver_etf_holding_js() -> pd.DataFrame:
    """
    全球最大白银 ETF—SPDR Gold Trust 持仓报告，数据区间从 20041118-至今
    https://datacenter.jin10.com/reportType/dc_etf_sliver
    :return: 持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "x-csrf-token",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "category": "etf",
        "attr_id": "2",
        "max_date": "",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = http.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df.columns = [
        "日期",
        "总库存",
        "增持/减持",
        "总价值",
    ]
    big_df["商品"] = "白银"
    big_df = big_df[
        [
            "商品",
            "日期",
            "总库存",
            "增持/减持",
            "总价值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["总库存"] = pd.to_numeric(big_df["总库存"], errors="coerce")
    big_df["增持/减持"] = pd.to_numeric(big_df["增持/减持"], errors="coerce")
    big_df["总价值"] = pd.to_numeric(big_df["总价值"], errors="coerce")
    big_df = big_df.sort_values(["日期"])
    big_df = big_df.reset_index(drop=True)
    return big_df


if __name__ == "__main__":
    fund_gold_etf_holding_js_df = fund_gold_etf_holding_js()
    print(fund_gold_etf_holding_js_df)

    fund_silver_etf_holding_js_df = fund_silver_etf_holding_js()
    print(fund_silver_etf_holding_js_df)
