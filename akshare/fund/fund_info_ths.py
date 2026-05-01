#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/05/01
Desc: 同花顺-基金基本信息
https://fund.10jqka.com.cn/161130/interduce.html
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils.cons import headers


def fund_info_ths(symbol: str = "161130") -> pd.DataFrame:
    """
    同花顺-基金数据-基金基本信息
    https://fund.10jqka.com.cn/161130/interduce.html
    :param symbol: 基金代码
    :type symbol: str
    :return: 基金基本信息
    :rtype: pandas.DataFrame
    """
    url = f"https://fund.10jqka.com.cn/{symbol}/interduce.html"
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.content, features="lxml", from_encoding="utf-8")

    # 查找基金信息对话框
    g_dialog = soup.find("ul", class_="g-dialog")
    if not g_dialog:
        raise ValueError("未找到基金信息，可能网页结构已变化")

    # 提取所有基金信息
    fund_data = {}
    lis = g_dialog.find_all("li")
    for li in lis:
        key_elem = li.find("span", class_="key")
        value_elem = li.find("span", class_="value")
        if key_elem and value_elem:
            key = key_elem.get_text(strip=True)
            value = value_elem.get_text(strip=True)
            fund_data[key] = value

    # 转换为DataFrame
    temp_df = pd.DataFrame(list(fund_data.items()), columns=["字段", "值"])

    return temp_df


if __name__ == "__main__":
    # 测试获取基金基本信息
    fund_info_ths_df = fund_info_ths(symbol="161130")
    print(fund_info_ths_df)
