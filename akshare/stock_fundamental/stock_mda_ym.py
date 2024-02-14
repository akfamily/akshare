# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/2/14 12:30
Desc: 益盟-F10-管理层讨论与分析
https://f10.emoney.cn/f10/zbyz/1000001
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_mda_ym(symbol: str = "000001") -> pd.DataFrame:
    """
    益盟-F10-管理层讨论与分析
    https://f10.emoney.cn/f10/zbyz/1000001
    :param symbol: 股票代码
    :type symbol: str
    :return: 管理层讨论与分析
    :rtype: pandas.DataFrame
    """
    url = f"http://f10.emoney.cn/f10/zygc/{symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    year_list = [
        item.text.strip()
        for item in soup.find(attrs={"class": "swlab_t"}).find_all("li")
    ]
    talk_list = [
        item.text.strip().replace("\xa0", " ")
        for item in soup.find_all(attrs={"class": "cnt"})
    ]
    big_df = pd.DataFrame([year_list, talk_list]).T
    big_df.columns = ["报告期", "内容"]
    return big_df


if __name__ == "__main__":
    stock_mda_ym_df = stock_mda_ym(symbol="000002")
    print(stock_mda_ym_df)
