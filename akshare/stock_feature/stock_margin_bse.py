#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/7/22 19:00
Desc: 北京证券交易所融资融券数据
https://www.bse.cn/disclosure/rzrq_trans_list.html
"""

import json
import re
from typing import Any

import pandas as pd
import requests


def _bse_headers(referer: str) -> dict[str, str]:
    """
    获取北交所融资融券接口请求头。

    :param referer: 请求来源页面
    :type referer: str
    :return: 请求头
    :rtype: dict[str, str]
    """
    return {
        "Referer": referer,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
    }


def _bse_normalize_date(date: str) -> str:
    """
    标准化交易日期为北交所接口格式。

    :param date: 原始交易日期
    :type date: str
    :return: YYYY-MM-DD 格式日期
    :rtype: str
    """
    if not date:
        return ""
    if re.fullmatch(r"\d{8}", date):
        return f"{date[:4]}-{date[4:6]}-{date[6:]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        return date
    raise ValueError("Please check if the date parameter is correct.")


def _parse_bse_jsonp(text: str) -> Any:
    """
    解析北交所 JSONP 响应。

    :param text: JSONP 文本
    :type text: str
    :return: 解析后的对象
    :rtype: Any
    """
    match = re.search(r"^[^(]+\((.*)\)\s*$", text, flags=re.S)
    if not match:
        raise ValueError("Failed to parse the BSE JSONP response.")
    payload = match.group(1)
    payload = re.sub(r",\s*'(\d{4}-\d{2}-\d{2})'\s*\]$", r', "\1"]', payload)
    return json.loads(payload)


def stock_margin_bse(date: str = "20260721") -> pd.DataFrame:
    """
    北京证券交易所-融资融券数据-融资融券汇总。

    :param date: 交易日
    :type date: str
    :return: 融资融券汇总
    :rtype: pandas.DataFrame
    """
    url = "https://www.bse.cn/rzrqjyyexxController/summaryInfoResult.do"
    params = {
        "callback": "cb",
        "transDate": _bse_normalize_date(date),
        "page": "0",
    }
    r = requests.get(
        url,
        params=params,
        headers=_bse_headers("https://www.bse.cn/disclosure/rzrq_trans_list.html"),
        timeout=30,
    )
    data_json = _parse_bse_jsonp(r.text)
    data_list = data_json[0]
    if not data_list:
        return pd.DataFrame(
            columns=["融资买入额", "融资余额", "融券卖出量", "融券余量", "融券余额", "融资融券余额"]
        )
    temp_df = pd.DataFrame(data_list)
    temp_df = temp_df[
        [
            "rzmreRound",
            "rzyeRound",
            "rqmclRound",
            "rqylRound",
            "rqyeRound",
            "rzrqyeRound",
        ]
    ]
    temp_df.columns = [
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    for column in temp_df.columns:
        temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce")
    return temp_df


def stock_margin_detail_bse(date: str = "20260721") -> pd.DataFrame:
    """
    北京证券交易所-融资融券数据-融资融券交易明细。

    :param date: 交易日
    :type date: str
    :return: 融资融券明细
    :rtype: pandas.DataFrame
    """
    url = "https://www.bse.cn/rzrqjyyexxController/detailInfoResult.do"
    normalized_date = _bse_normalize_date(date)
    headers = _bse_headers("https://www.bse.cn/disclosure/rzrq_trans_list.html")
    big_df = pd.DataFrame()
    page = 0
    total_pages = 1
    while page < total_pages:
        r = requests.post(
            url,
            params={"callback": "cb"},
            data={"transDate": normalized_date, "page": str(page)},
            headers=headers,
            timeout=30,
        )
        data_json = _parse_bse_jsonp(r.text)
        page_info = data_json[0][0]
        total_pages = int(page_info["totalPages"])
        temp_df = pd.DataFrame(page_info["content"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
        page += 1
    if big_df.empty:
        return pd.DataFrame(
            columns=[
                "证券代码",
                "证券简称",
                "融资买入额",
                "融资余额",
                "融券卖出量",
                "融券余量",
                "融券余额",
                "融资融券余额",
            ]
        )
    big_df = big_df[
        ["zqdm", "zqjc", "rzmre", "rzye", "rqmcl", "rqyl", "rqye", "rzrqye"]
    ]
    big_df.columns = [
        "证券代码",
        "证券简称",
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    big_df["证券代码"] = big_df["证券代码"].astype(str).str.zfill(6)
    for column in big_df.columns[2:]:
        big_df[column] = pd.to_numeric(big_df[column], errors="coerce")
    return big_df


def stock_margin_underlying_info_bse(date: str = "20260722") -> pd.DataFrame:
    """
    北京证券交易所-融资融券数据-标的证券信息。

    :param date: 交易日
    :type date: str
    :return: 标的证券信息
    :rtype: pandas.DataFrame
    """
    url = "https://www.bse.cn/rzrqbdzqController/infoResult.do"
    normalized_date = _bse_normalize_date(date)
    headers = _bse_headers("https://www.bse.cn/disclosure/rzrq_bdzq_list.html")
    big_df = pd.DataFrame()
    page = 0
    total_pages = 1
    while page < total_pages:
        r = requests.post(
            url,
            params={"callback": "cb"},
            data={"transDate": normalized_date, "zqdm": "", "page": str(page)},
            headers=headers,
            timeout=30,
        )
        data_json = _parse_bse_jsonp(r.text)
        page_info = data_json[0][0]
        total_pages = int(page_info["totalPages"])
        temp_df = pd.DataFrame(page_info["content"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
        page += 1
    if big_df.empty:
        return pd.DataFrame(
            columns=["证券代码", "证券简称", "融资标的", "融券标的", "当日可融资", "当日可融券"]
        )
    big_df = big_df[["zqdm", "zqjc", "rzbd", "rqbd", "drkrz", "drkrq"]]
    big_df.columns = ["证券代码", "证券简称", "融资标的", "融券标的", "当日可融资", "当日可融券"]
    big_df["证券代码"] = big_df["证券代码"].astype(str).str.zfill(6)
    return big_df
