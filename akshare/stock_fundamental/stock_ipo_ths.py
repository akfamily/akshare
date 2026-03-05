#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/03/04
Desc: 同花顺-数据中心-新股申购与中签
https://data.10jqka.com.cn/ipo/xgsgyzq/
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_ipo_ths(symbol: str = "全部A股") -> pd.DataFrame:
    """
    同花顺-数据中心-新股申购与中签
    https://data.10jqka.com.cn/ipo/xgsgyzq/
    :param symbol: choice of {"全部A股", "沪市主板", "深市主板", "创业板", "科创板", "京市主板"}
    :type symbol: str
    :return: 新股申购与中签数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "全部A股": "all",
        "沪市主板": "hszb",
        "深市主板": "sszb",
        "创业板": "cyb",
        "科创板": "kcbsg",
        "京市主板": "bjzb",
    }
    if symbol not in symbol_map:
        raise ValueError(
            f"Invalid symbol: {symbol}. "
            f"Please choose from {list(symbol_map.keys())}"
        )

    url = f"https://data.10jqka.com.cn/ipo/xgsgyzq/{symbol_map[symbol]}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    # 查找表格
    table = soup.find("table", id="maintable")
    if not table:
        table = soup.find("table", class_="m_table")
    if not table:
        raise ValueError("未找到数据表格，请检查网页结构是否发生变化")

    # 获取表头
    thead = table.find("thead")
    if thead:
        headers_list = [th.get_text(strip=True) for th in thead.find_all("th")]
    else:
        headers_list = []

    # 获取表格数据
    tbody = table.find("tbody")
    if not tbody:
        tbody = table  # 有些表格没有tbody标签

    data = []
    for row in tbody.find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if cells:
            data.append(cells)

    # 创建DataFrame
    if headers_list and data:
        temp_df = pd.DataFrame(data, columns=headers_list)
    elif data:
        temp_df = pd.DataFrame(data)
    else:
        temp_df = pd.DataFrame()

    return temp_df


def stock_ipo_hk_ths() -> pd.DataFrame:
    """
    同花顺-数据中心-新股申购与中签-港股
    https://data.10jqka.com.cn/ipo/xgsgyzq/
    :return: 港股新股申购与中签数据
    :rtype: pandas.DataFrame
    """
    url = "https://data.10jqka.com.cn/ipo/xgsgyzq/hkstock/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    # 查找表格
    table = soup.find("table", id="maintable")
    if not table:
        table = soup.find("table", class_="m_table")
    if not table:
        raise ValueError("未找到数据表格，请检查网页结构是否发生变化")

    # 获取表头
    thead = table.find("thead")
    if thead:
        headers_list = [th.get_text(strip=True) for th in thead.find_all("th")]
    else:
        headers_list = []

    # 获取表格数据
    tbody = table.find("tbody")
    if not tbody:
        tbody = table  # 有些表格没有tbody标签

    data = []
    for row in tbody.find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if cells:
            data.append(cells)

    # 创建DataFrame
    if headers_list and data:
        temp_df = pd.DataFrame(data, columns=headers_list)
    elif data:
        temp_df = pd.DataFrame(data)
    else:
        temp_df = pd.DataFrame()

    return temp_df


if __name__ == "__main__":
    stock_ipo_ths_df = stock_ipo_ths(symbol="全部A股")
    print(stock_ipo_ths_df)

    stock_ipo_hk_ths_df = stock_ipo_hk_ths()
    print(stock_ipo_hk_ths_df)
