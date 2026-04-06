#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/4/2 22:00
Desc: 深圳证券交易所-基金规模日频数据
https://www.szse.cn/market/fund/volume/etf/index.html
"""

import io
import random
import warnings
from datetime import date, datetime

import pandas as pd
import requests


def _parse_date(date_str: str) -> date:
    if len(date_str) != 8 or not date_str.isdigit():
        raise ValueError("start_date 和 end_date 格式应为 YYYYMMDD")
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError as err:
        raise ValueError("start_date 和 end_date 应为有效日期") from err


def fund_scale_daily_szse(
    start_date: str = "20260401", end_date: str = "20260401", symbol: str = "ETF"
) -> pd.DataFrame:
    """
    深圳证券交易所-基金产品-基金规模-日频数据
    https://www.szse.cn/market/fund/volume/etf/index.html
    :param start_date: 开始日期, 格式如 "20260401"
    :type start_date: str
    :param end_date: 结束日期, 格式如 "20260401"
    :type end_date: str
    :param symbol: 基金类别, choice of {"ETF", "LOF", "REITS"}
    :type symbol: str
    :return: 深交所基金规模日频数据;
        日期范围不能超过 6 个月, 否则返回带表头的空 DataFrame
    :rtype: pandas.DataFrame
    """
    columns = ["日期", "基金代码", "基金简称", "基金份额"]
    symbol_map = {
        "ETF": {
            "jjlb": "ETF",
            "referer": "https://www.szse.cn/market/fund/volume/etf/index.html",
        },
        "LOF": {
            "jjlb": "LOF",
            "referer": "https://www.szse.cn/market/fund/volume/lof/index.html",
        },
        "REITS": {
            "jjlb": "不动产基金",
            "referer": "https://www.szse.cn/market/fund/volume/reits/index.html",
        },
    }
    if symbol not in symbol_map:
        raise ValueError("symbol 应为 {'ETF', 'LOF', 'REITS'}")
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if start > end:
        raise ValueError("start_date 不能大于 end_date")

    url = "https://www.szse.cn/api/report/ShowReport"
    headers = {
        "Host": "www.szse.cn",
        "Referer": symbol_map[symbol]["referer"],
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    }
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "scsj_fund_jjgm",
        "TABKEY": "tab1",
        "txtStart": start.strftime("%Y-%m-%d"),
        "txtEnd": end.strftime("%Y-%m-%d"),
        "jjlb": symbol_map[symbol]["jjlb"],
        "random": str(random.random()),
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(io.BytesIO(r.content), engine="openpyxl")

    temp_df = temp_df.dropna(how="all")
    if temp_df.empty:
        return pd.DataFrame(columns=columns)

    temp_df.rename(
        columns={
            "基金规模(份)": "基金份额",
        },
        inplace=True,
    )

    if "基金代码" in temp_df.columns:
        code_series = pd.to_numeric(temp_df["基金代码"], errors="coerce")
        temp_df = temp_df[code_series.notna()].copy()
        temp_df["基金代码"] = (
            code_series[code_series.notna()].astype(int).astype(str).str.zfill(6)
        )

    if "日期" in temp_df.columns:
        temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
        temp_df = temp_df[temp_df["日期"].notna()]

    if temp_df.empty:
        return pd.DataFrame(columns=columns)

    for item in ["基金份额"]:
        if item in temp_df.columns:
            temp_df[item] = temp_df[item].astype(str).str.replace(",", "", regex=False)
            temp_df[item] = pd.to_numeric(temp_df[item], errors="coerce")

    for item in columns:
        if item not in temp_df.columns:
            temp_df[item] = pd.NA
    temp_df = temp_df[columns]
    return temp_df


if __name__ == "__main__":
    for item_symbol in ["ETF", "LOF", "REITS"]:
        fund_scale_daily_szse_df = fund_scale_daily_szse(
            start_date="20260401", end_date="20260402", symbol=item_symbol
        )
        print(item_symbol)
        print(fund_scale_daily_szse_df)
