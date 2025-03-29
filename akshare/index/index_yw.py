#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/17 19:17
Desc: 义乌小商品指数
https://www.ywindex.com/Home/Product/index/
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def index_yw(symbol: str = "月景气指数") -> pd.DataFrame:
    """
    义乌小商品指数
    https://www.ywindex.com/Home/Product/index/
    :param symbol: choice of {"周价格指数", "月价格指数", "月景气指数"}
    :type symbol: str
    :return: 指数结果
    :rtype: pandas.DataFrame
    """
    import urllib3

    # 禁用InsecureRequestWarning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    name_num_dict = {
        "周价格指数": 1,
        "月价格指数": 3,
        "月景气指数": 5,
    }
    url = "https://www.ywindex.com/Home/Product/index/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, features="lxml")
    table_name = (
        soup.find_all(attrs={"class": "tablex"})[name_num_dict[symbol]]
        .get_text()
        .split("\n\n\n\n\n")[2]
        .split("\n")
    )
    table_content = (
        soup.find_all(attrs={"class": "tablex"})[name_num_dict[symbol]]
        .get_text()
        .split("\n\n\n\n\n")[3]
        .split("\n\n")
    )
    if symbol == "月景气指数":
        table_df = pd.DataFrame([item.split("\n") for item in table_content]).iloc[
            :, :5
        ]
        table_df.columns = ["期数", "景气指数", "规模指数", "效益指数", "市场信心指数"]
        table_df["期数"] = pd.to_datetime(table_df["期数"], errors="coerce").dt.date
        table_df["景气指数"] = pd.to_numeric(table_df["景气指数"], errors="coerce")
        table_df["规模指数"] = pd.to_numeric(table_df["规模指数"], errors="coerce")
        table_df["效益指数"] = pd.to_numeric(table_df["效益指数"], errors="coerce")
        table_df["市场信心指数"] = pd.to_numeric(
            table_df["市场信心指数"], errors="coerce"
        )
        table_df.sort_values(["期数"], inplace=True, ignore_index=True)
        return table_df
    elif symbol == "周价格指数":
        table_df = pd.DataFrame([item.split("\n") for item in table_content]).iloc[
            :, :6
        ]
        table_df.columns = table_name
        table_df["期数"] = pd.to_datetime(table_df["期数"], errors="coerce").dt.date
        table_df["价格指数"] = pd.to_numeric(table_df["价格指数"], errors="coerce")
        table_df["场内价格指数"] = pd.to_numeric(
            table_df["场内价格指数"], errors="coerce"
        )
        table_df["网上价格指数"] = pd.to_numeric(
            table_df["网上价格指数"], errors="coerce"
        )
        table_df["订单价格指数"] = pd.to_numeric(
            table_df["订单价格指数"], errors="coerce"
        )
        table_df["出口价格指数"] = pd.to_numeric(
            table_df["出口价格指数"], errors="coerce"
        )
        table_df.sort_values(["期数"], inplace=True, ignore_index=True)
        return table_df
    elif symbol == "月价格指数":
        table_df = pd.DataFrame([item.split("\n") for item in table_content]).iloc[
            :, :6
        ]
        table_df.columns = table_name
        table_df["期数"] = pd.to_datetime(table_df["期数"], errors="coerce").dt.date
        table_df["价格指数"] = pd.to_numeric(table_df["价格指数"], errors="coerce")
        table_df["场内价格指数"] = pd.to_numeric(
            table_df["场内价格指数"], errors="coerce"
        )
        table_df["网上价格指数"] = pd.to_numeric(
            table_df["网上价格指数"], errors="coerce"
        )
        table_df["订单价格指数"] = pd.to_numeric(
            table_df["订单价格指数"], errors="coerce"
        )
        table_df["出口价格指数"] = pd.to_numeric(
            table_df["出口价格指数"], errors="coerce"
        )
        table_df.sort_values(["期数"], inplace=True, ignore_index=True)
        return table_df


if __name__ == "__main__":
    index_yw_df = index_yw(symbol="周价格指数")
    print(index_yw_df)

    index_yw_df = index_yw(symbol="月价格指数")
    print(index_yw_df)

    index_yw_df = index_yw(symbol="月景气指数")
    print(index_yw_df)
