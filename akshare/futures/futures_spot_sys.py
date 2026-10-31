#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/5 20:20
Desc: 生意社-商品与期货-现期图
https://www.100ppi.com/sf/792.html
"""

from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

from akshare.utils import http


def __get_sys_spot_futures_dict() -> dict:
    """
    生意社-商品与期货-现期图：品种和网址字典
    https://www.100ppi.com/sf/792.html
    :return: 品种和网址字典
    :rtype: dict
    """
    url = "https://www.100ppi.com/sf/792.html"
    res = http.get(url)
    soup = BeautifulSoup(res.text, features="lxml")
    temp_item = soup.find(name="div", attrs={"class": "q8"}).find_all("li")
    name_url_dict = dict(
        zip(
            [item.find("a").get_text().strip() for item in temp_item],
            [item.find("a")["href"] for item in temp_item],
        )
    )
    return name_url_dict


def futures_spot_sys(symbol: str = "铜", indicator: str = "市场价格") -> pd.DataFrame:
    """
    生意社-商品与期货-现期图
    https://www.100ppi.com/sf/792.html
    :param symbol: 期货品种
    :type symbol: str
    :param indicator: 市场价格；choice of {"市场价格", "基差率", "主力基差"}
    :type indicator: str
    :return: pandas.DataFrame
    :rtype: dict
    """
    name_url_dict = __get_sys_spot_futures_dict()
    url = name_url_dict[symbol]
    r = http.get("https://www.100ppi.com" + url)
    if indicator == "市场价格":
        table_df_one = pd.read_html(StringIO(r.text), header=0, index_col=0)[1].T
        table_df_one["现货价格"] = pd.to_numeric(
            table_df_one["现货价格"], errors="coerce"
        )
        table_df_one["主力合约"] = pd.to_numeric(
            table_df_one["主力合约"], errors="coerce"
        )
        table_df_one["最近合约"] = pd.to_numeric(
            table_df_one["最近合约"], errors="coerce"
        )
        table_df_one = table_df_one.reset_index()
        table_df_one.columns.name = None
        table_df_one = table_df_one.rename(columns={"index": "日期"})
        return table_df_one
    elif indicator == "基差率":
        table_df_two = pd.read_html(StringIO(r.text), header=0, index_col=0)[2].T
        table_df_two["基差率"] = table_df_two["基差率"].str.replace("%", "")
        table_df_two["基差率"] = pd.to_numeric(table_df_two["基差率"], errors="coerce")
        table_df_two = table_df_two.reset_index()
        table_df_two.columns.name = None
        table_df_two = table_df_two.rename(columns={"index": "日期"})
        return table_df_two
    else:
        table_df_three = pd.read_html(StringIO(r.text), header=0, index_col=0)[3].T
        table_df_three["主力基差"] = pd.to_numeric(
            table_df_three["主力基差"], errors="coerce"
        )
        table_df_three = table_df_three.reset_index()
        table_df_three.columns.name = None
        table_df_three = table_df_three.rename(columns={"index": "日期"})
        return table_df_three


if __name__ == "__main__":
    futures_spot_sys_df = futures_spot_sys(symbol="铜", indicator="市场价格")
    print(futures_spot_sys_df)

    futures_spot_sys_df = futures_spot_sys(symbol="铜", indicator="基差率")
    print(futures_spot_sys_df)

    futures_spot_sys_df = futures_spot_sys(symbol="铜", indicator="主力基差")
    print(futures_spot_sys_df)
