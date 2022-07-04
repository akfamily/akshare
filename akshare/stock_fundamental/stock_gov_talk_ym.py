# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/7/3 20:30
Desc: 益盟-F10-管理层讨论与分析
http://f10.emoney.cn/f10/zbyz/1000001
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def stock_gov_talk_ym(symbol: str = "000001") -> pd.DataFrame:
    """
    益盟-F10-管理层讨论与分析
    http://f10.emoney.cn/f10/zbyz/1000001
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
    return big_df


if __name__ == "__main__":
    stock_gov_talk_ym_df = stock_gov_talk_ym(symbol="000001")
    print(stock_gov_talk_ym_df)
