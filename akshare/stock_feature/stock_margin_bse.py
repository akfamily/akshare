#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/6/14 17:00
Desc: 北京证券交易所-融资融券数据
https://www.bseinfo.net/disclosure/rzrq_trans_list.html
"""

import json
import random
import re
import time
import warnings
from io import BytesIO

import pandas as pd
import requests


def stock_margin_underlying_info_bse(date: str = "20260605") -> pd.DataFrame:
    """
    北京证券交易所-融资融券数据-标的证券信息
    https://www.bseinfo.net/disclosure/rzrq_bdzq_list.html
    :param date: 交易日
    :type date: str
    :return: 标的证券信息
    :rtype: pandas.DataFrame
    """
    url = "https://www.bseinfo.net/rzrqbdzqController/export.do"
    params = {
        "zqdm": "",
        "transDate": "-".join([date[:4], date[4:6], date[6:]]),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content), engine="xlrd", dtype={"证券代码": str})
    # 去掉最后一行的日期统计行
    temp_df = temp_df[temp_df["证券代码"].str.match(r"^\d+$", na=False)]
    return temp_df


def stock_margin_bse(date: str = "20260603") -> pd.DataFrame:
    """
    北京证券交易所-融资融券数据-融资融券汇总
    https://www.bseinfo.net/disclosure/rzrq_trans_list.html
    :param date: 交易日
    :type date: str
    :return: 融资融券汇总
    :rtype: pandas.DataFrame
    """
    url = "https://www.bseinfo.net/rzrqjyyexxController/summaryInfoResult.do"
    # 生成jQuery风格的JSONP callback参数和防缓存参数
    timestamp = int(time.time() * 1000)
    callback = f"jQuery{random.randint(10**18, 10**19-1)}_{timestamp}"
    params = {
        "callback": callback,
        "transDate": "-".join([date[:4], date[4:6], date[6:]]),
        "page": "0",
        "_": str(timestamp),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    # 解析JSONP响应
    json_str = re.search(r"\((.*)\)", r.text).group(1)
    json_str = json_str.replace("'", '"')
    data_json = json.loads(json_str)
    temp_df = pd.DataFrame(data_json[0])
    temp_df = temp_df[
        [
            "rzmre",
            "rzye",
            "rqmcl",
            "rqyl",
            "rqye",
            "rzrqye",
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
    temp_df["融资买入额"] = temp_df["融资买入额"].astype(str).str.replace(",", "")
    temp_df["融资买入额"] = pd.to_numeric(temp_df["融资买入额"], errors="coerce")
    temp_df["融资余额"] = temp_df["融资余额"].astype(str).str.replace(",", "")
    temp_df["融资余额"] = pd.to_numeric(temp_df["融资余额"], errors="coerce")
    temp_df["融券卖出量"] = temp_df["融券卖出量"].astype(str).str.replace(",", "")
    temp_df["融券卖出量"] = pd.to_numeric(temp_df["融券卖出量"], errors="coerce")
    temp_df["融券余量"] = temp_df["融券余量"].astype(str).str.replace(",", "")
    temp_df["融券余量"] = pd.to_numeric(temp_df["融券余量"], errors="coerce")
    temp_df["融券余额"] = temp_df["融券余额"].astype(str).str.replace(",", "")
    temp_df["融券余额"] = pd.to_numeric(temp_df["融券余额"], errors="coerce")
    temp_df["融资融券余额"] = temp_df["融资融券余额"].astype(str).str.replace(",", "")
    temp_df["融资融券余额"] = pd.to_numeric(temp_df["融资融券余额"], errors="coerce")
    return temp_df


def stock_margin_detail_bse(date: str = "20260603") -> pd.DataFrame:
    """
    北京证券交易所-融资融券数据-融资融券交易明细
    https://www.bseinfo.net/disclosure/rzrq_trans_list.html
    :param date: 交易日期
    :type date: str
    :return: 融资融券明细
    :rtype: pandas.DataFrame
    """
    url = "https://www.bseinfo.net/rzrqjyyexxController/exportDetail.do"
    params = {
        "transDateDetail": "-".join([date[:4], date[4:6], date[6:]]),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content), engine="xlrd", dtype={"证券代码": str})
    # 去掉最后一行的日期统计行
    temp_df = temp_df[temp_df["证券代码"].str.match(r"^\d+$", na=False)]
    temp_df.columns = [
        "证券代码",
        "证券简称",
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    temp_df["证券简称"] = temp_df["证券简称"].astype(str).str.replace("&nbsp;", "")
    temp_df["融资买入额"] = temp_df["融资买入额"].astype(str).str.replace(",", "")
    temp_df["融资买入额"] = pd.to_numeric(temp_df["融资买入额"], errors="coerce")
    temp_df["融资余额"] = temp_df["融资余额"].astype(str).str.replace(",", "")
    temp_df["融资余额"] = pd.to_numeric(temp_df["融资余额"], errors="coerce")
    temp_df["融券卖出量"] = temp_df["融券卖出量"].astype(str).str.replace(",", "")
    temp_df["融券卖出量"] = pd.to_numeric(temp_df["融券卖出量"], errors="coerce")
    temp_df["融券余量"] = temp_df["融券余量"].astype(str).str.replace(",", "")
    temp_df["融券余量"] = pd.to_numeric(temp_df["融券余量"], errors="coerce")
    temp_df["融券余额"] = temp_df["融券余额"].astype(str).str.replace(",", "")
    temp_df["融券余额"] = pd.to_numeric(temp_df["融券余额"], errors="coerce")
    temp_df["融资融券余额"] = temp_df["融资融券余额"].astype(str).str.replace(",", "")
    temp_df["融资融券余额"] = pd.to_numeric(temp_df["融资融券余额"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_margin_underlying_info_bse_df = stock_margin_underlying_info_bse(date="20260605")
    print(stock_margin_underlying_info_bse_df)

    stock_margin_bse_df = stock_margin_bse(date="20260603")
    print(stock_margin_bse_df)

    stock_margin_detail_bse_df = stock_margin_detail_bse(date="20260604")
    print(stock_margin_detail_bse_df)
