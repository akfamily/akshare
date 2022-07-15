# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/7/3 20:30
Desc: 益盟-F10-主营构成
http://f10.emoney.cn/f10/zbyz/1000001
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_zygc_ym(symbol: str = "000001") -> pd.DataFrame:
    """
    益盟-F10-主营构成
    http://f10.emoney.cn/f10/zbyz/1000001
    :param symbol: 股票代码
    :type symbol: str
    :return: 主营构成
    :rtype: pandas.DataFrame
    """
    url = f"http://f10.emoney.cn/f10/zygc/{symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    year_list = [
        item.text.strip()
        for item in soup.find(attrs={"class": "swlab_t"}).find_all("li")
    ]

    big_df = pd.DataFrame()
    for i, item in enumerate(year_list, 2):
        temp_df = pd.read_html(r.text, header=0)[i]
        temp_df.columns = [
            "分类方向",
            "分类",
            "营业收入",
            "营业收入-同比增长",
            "营业收入-占主营收入比",
            "营业成本",
            "营业成本-同比增长",
            "营业成本-占主营成本比",
            "毛利率",
            "毛利率-同比增长",
        ]
        temp_df["报告期"] = item
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df = big_df[
        [
            "报告期",
            "分类方向",
            "分类",
            "营业收入",
            "营业收入-同比增长",
            "营业收入-占主营收入比",
            "营业成本",
            "营业成本-同比增长",
            "营业成本-占主营成本比",
            "毛利率",
            "毛利率-同比增长",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_zygc_ym_df = stock_zygc_ym(symbol="000001")
    print(stock_zygc_ym_df)
