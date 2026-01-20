#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/1/20 15:00
Desc: 深圳证券交易所-ETF基金份额数据
https://fund.szse.cn/marketdata/fundslist/index.html
"""

import warnings

import pandas as pd
import requests


def fund_etf_scale_szse() -> pd.DataFrame:
    """
    深圳证券交易所-基金产品-基金列表-ETF基金份额
    https://fund.szse.cn/marketdata/fundslist/index.html
    :return: ETF基金份额数据
    :rtype: pandas.DataFrame
    """
    url = "https://fund.szse.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "1000_lf",
        "TABKEY": "tab1",
        "random": "0.07610353191740105",
    }
    headers = {
        "Referer": "https://fund.szse.cn/marketdata/fundslist/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(r.content, engine="openpyxl", dtype={"基金代码": str})
    temp_df.rename(
        columns={
            "当前规模(份)": "基金份额",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "基金代码",
            "基金简称",
            "基金类别",
            "投资类别",
            "上市日期",
            "基金份额",
            "基金管理人",
            "基金发起人",
            "基金托管人",
            "净值",
        ]
    ]
    temp_df["上市日期"] = pd.to_datetime(temp_df["上市日期"], errors="coerce").dt.date
    temp_df["基金份额"] = (
        temp_df["基金份额"].astype(str).str.replace(",", "", regex=False)
    )
    temp_df["基金份额"] = pd.to_numeric(temp_df["基金份额"], errors="coerce")
    temp_df["净值"] = pd.to_numeric(temp_df["净值"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    fund_etf_scale_szse_df = fund_etf_scale_szse()
    print(fund_etf_scale_szse_df)
