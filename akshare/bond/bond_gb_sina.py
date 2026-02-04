#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/2/4 17:00
Desc: 新浪财经-债券-中国/美国国债收益率
https://vip.stock.finance.sina.com.cn/mkt/#hs_z
"""

import pandas as pd
import requests


def bond_gb_zh_sina(symbol: str = "中国10年期国债") -> pd.DataFrame:
    """
    新浪财经-债券-中国国债收益率行情数据
    https://stock.finance.sina.com.cn/forex/globalbd/cn10yt.html
    :param symbol: choice of {"中国1年期国债", "中国2年期国债", "中国3年期国债", "中国5年期国债", "中国7年期国债", "中国10年期国债", "中国15年期国债", "中国20年期国债", "中国30年期国债"}
    :type symbol: str
    :return: 中国国债收益率行情数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "中国1年期国债": "CN1YT",
        "中国2年期国债": "CN2YT",
        "中国3年期国债": "CN3YT",
        "中国5年期国债": "CN5YT",
        "中国7年期国债": "CN7YT",
        "中国10年期国债": "CN10YT",
        "中国15年期国债": "CN15YT",
        "中国20年期国债": "CN20YT",
        "中国30年期国债": "CN30YT",
    }
    url = f"https://bond.finance.sina.com.cn/hq/gb/daily?symbol={symbol_map[symbol]}"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    return temp_df


def bond_gb_us_sina(symbol: str = "美国10年期国债") -> pd.DataFrame:
    """
    新浪财经-债券-美国国债收益率行情数据
    https://stock.finance.sina.com.cn/forex/globalbd/cn10yt.html
    :param symbol: choice of {"美国1月期国债", "美国2月期国债", "美国3月期国债", "美国4月期国债", "美国6月期国债", "美国1年期国债", "美国2年期国债", "美国3年期国债", "美国5年期国债", "美国7年期国债", "美国10年期国债", "美国20年期国债", "美国30年期国债"}
    :type symbol: str
    :return: 美国国债收益率行情数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "美国1月期国债": "US1MT",
        "美国2月期国债": "US2MT",
        "美国3月期国债": "US3MT",
        "美国4月期国债": "US4MT",
        "美国6月期国债": "US6MT",
        "美国1年期国债": "US1YT",
        "美国2年期国债": "US2YT",
        "美国3年期国债": "US3YT",
        "美国5年期国债": "US5YT",
        "美国7年期国债": "US7YT",
        "美国10年期国债": "US10YT",
        "美国20年期国债": "US20YT",
        "美国30年期国债": "US30YT",
    }
    url = f"https://bond.finance.sina.com.cn/hq/gb/daily?symbol={symbol_map[symbol]}"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    bond_gb_zh_sina_df = bond_gb_zh_sina(symbol="中国10年期国债")
    print(bond_gb_zh_sina_df)

    bond_gb_us_sina_df = bond_gb_us_sina(symbol="美国10年期国债")
    print(bond_gb_us_sina_df)
