#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 九期网-商品期权手续费
https://www.9qihuo.com/qiquanshouxufei
"""

from functools import lru_cache
import re
from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

from akshare.exceptions import APIError, InvalidParameterError, RateLimitError
from akshare.futures.futures_comm_qihuo import _HEADERS
from akshare.utils import http


def _option_comm_page(params: dict = None) -> str:
    """
    取回九期网期权手续费页面
    :param params: 查询参数，如 {"heyue": "si_o"}
    :type params: dict
    :return: 页面 HTML
    :rtype: str
    :raises RateLimitError: 上游返回 429
    :raises APIError: 上游返回其他非 2xx 状态码
    """
    # 九期网拒绝不带浏览器请求头的请求，返回 403；原先因此在解析时报
    # 'NoneType' object has no attribute 'find_all'
    r = http.get(
        "https://www.9qihuo.com/qiquanshouxufei", params=params, headers=_HEADERS
    )
    if r.status_code == 429:
        raise RateLimitError("9qihuo 返回 429，访问过于频繁，请稍后再试")
    if not r.ok:
        raise APIError("9qihuo 请求失败", status_code=r.status_code)
    return r.text


@lru_cache()
def option_comm_symbol() -> pd.DataFrame:
    """
    九期网-商品期权手续费-品种列表
    https://www.9qihuo.com/qiquanshouxufei
    :return: 品种名称与品种代码
    :rtype: pandas.DataFrame
    """
    soup = BeautifulSoup(_option_comm_page(), features="lxml")
    name = [
        item.string.strip()
        for item in soup.find(name="div", attrs={"id": "inst_list"}).find_all(name="a")
    ]
    code = [
        item["href"].split("?")[1].split("=")[1]
        for item in soup.find(name="div", attrs={"id": "inst_list"}).find_all(name="a")
    ]
    temp_df = pd.DataFrame([name, code]).T
    temp_df.columns = ["品种名称", "品种代码"]
    return temp_df


def option_comm_info(symbol: str = "工业硅期权") -> pd.DataFrame:
    """
    九期网-商品期权手续费
    https://www.9qihuo.com/qiquanshouxufei
    :param symbol: choice of {"所有", "上海期货交易所", "大连商品交易所", "郑州商品交易所", "上海国际能源交易中心", "广州期货交易所"}
    :type symbol: str
    :return: 期权手续费
    :rtype: pandas.DataFrame
    """

    symbol_df = option_comm_symbol()
    matched = symbol_df[symbol_df["品种名称"].str.contains(symbol, regex=False)]
    if matched.empty:
        raise InvalidParameterError(
            f"九期网没有品种 {symbol}，可选品种请通过 ak.option_comm_symbol() 获取"
        )
    html = _option_comm_page({"heyue": matched["品种代码"].values[0]})
    temp_df = pd.read_html(StringIO(html))[0]
    market_symbol = temp_df.iloc[0, 0]
    columns = temp_df.iloc[2, :]
    temp_df = temp_df.iloc[3:, :]
    temp_df.columns = columns
    temp_df["交易所"] = market_symbol
    temp_df = temp_df.reset_index(drop=True)
    temp_df.index.name = None
    temp_df.columns.name = None
    temp_df["现价"] = pd.to_numeric(temp_df["现价"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["每跳毛利/元"] = pd.to_numeric(temp_df["每跳毛利/元"], errors="coerce")
    temp_df["每跳净利/元"] = pd.to_numeric(temp_df["每跳净利/元"], errors="coerce")
    soup = BeautifulSoup(html, features="lxml")
    raw_date_text = soup.find(name="a", attrs={"id": "dlink"}).previous
    # 原文如“（期权手续费更新时间：2026-10-30 00:50:17.461，价格更新时间：…。）”；
    # 原先用 strip 按字符集合去前缀，上游加上“期权”二字后前缀去不干净
    times = re.findall(r"更新时间：([\d\-: .]+)", str(raw_date_text))
    comm_update_time, price_update_time = (times + [None, None])[:2]
    temp_df["手续费更新时间"] = comm_update_time
    temp_df["价格更新时间"] = price_update_time
    return temp_df


if __name__ == "__main__":
    option_comm_symbol_df = option_comm_symbol()
    print(option_comm_symbol_df)

    option_comm_info_df = option_comm_info(symbol="工业硅期权")
    print(option_comm_info_df)
