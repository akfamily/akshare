#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/9/30 15:30
Desc: Drewry 集装箱指数
https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry
https://infogram.com/world-container-index-1h17493095xl4zj
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils import demjson


def drewry_wci_index(symbol: str = "composite") -> pd.DataFrame:
    """
    Drewry 集装箱指数
    https://infogram.com/world-container-index-1h17493095xl4zj
    :param symbol: choice of {"composite", "shanghai-rotterdam", "rotterdam-shanghai", "shanghai-los angeles", "los angeles-shanghai", "shanghai-genoa", "new york-rotterdam", "rotterdam-new york"}
    :type symbol: str
    :return: Drewry 集装箱指数
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "composite": 0,
        "shanghai-rotterdam": 1,
        "rotterdam-shanghai": 2,
        "shanghai-los angeles": 3,
        "los angeles-shanghai": 4,
        "shanghai-genoa": 5,
        "new york-rotterdam": 6,
        "rotterdam-new york": 7,
    }
    url = "https://infogram.com/world-container-index-1h17493095xl4zj"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find_all("script")[-4].string.strip("window.infographicData=")[:-1]
    data_json = demjson.decode(data_text)
    temp_df = pd.DataFrame(data_json["elements"][2]["data"][symbol_map[symbol]])
    temp_df = temp_df.iloc[1:, :]
    temp_df.columns = ["date", "wci"]
    temp_df["date"] = [item["value"] for item in temp_df["date"]]
    temp_df["wci"] = [item["value"] for item in temp_df["wci"]]
    day = temp_df["date"].str.split("-", expand=True).iloc[:, 0].str.strip()
    month = temp_df["date"].str.split("-", expand=True).iloc[:, 1].str.strip()
    month = month.str.replace("July", "Jul")
    year = temp_df["date"].str.split("-", expand=True).iloc[:, 2].str.strip()
    temp_df["date"] = day + "-" + month + "-" + year
    # 修正数据源中日期格式的错误
    temp_df["date"] = temp_df["date"].str.replace("Sept", "Sep")
    temp_df["date"] = pd.to_datetime(temp_df["date"], format="%d-%b-%y").dt.date
    temp_df["wci"] = pd.to_numeric(temp_df["wci"], errors="coerce")
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    drewry_wci_index_df = drewry_wci_index(symbol="composite")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="shanghai-rotterdam")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="rotterdam-shanghai")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="shanghai-los angeles")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="los angeles-shanghai")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="shanghai-genoa")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="new york-rotterdam")
    print(drewry_wci_index_df)

    drewry_wci_index_df = drewry_wci_index(symbol="rotterdam-new york")
    print(drewry_wci_index_df)
