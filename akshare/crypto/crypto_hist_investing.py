# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/23 13:52
Desc: 加密货币
https://cn.investing.com/crypto/currencies
高频数据
https://bitcoincharts.com/about/markets-api/
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option("mode.chained_assignment", None)


def crypto_name_map() -> dict:
    """
    加密货币名称
    :return: 加密货币历史数据获取
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = "https://cn.investing.com/crypto/Service/LoadCryptoCurrencies"
    payload = {"lastRowId": "0"}
    r = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(r.json()["html"], "lxml")
    crypto_url_list = [
        "https://cn.investing.com" + item["href"] + "/historical-data"
        for item in soup.find_all("a")
        if "-" not in item["href"]
    ]
    crypto_url_list.append("https://cn.investing.com/crypto/bitcoin/historical-data")
    crypto_name_list = [
        item.get_text() for item in soup.find_all("a") if "-" not in item["href"]
    ]
    crypto_name_list.append("比特币")
    name_url_dict = dict(zip(crypto_name_list, crypto_url_list))
    temp_df = pd.DataFrame.from_dict(name_url_dict, orient="index")
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["name", "url"]
    return temp_df


def crypto_hist(
    symbol: str = "以太坊",
    period: str = "每日",
    start_date: str = "20191020",
    end_date: str = "20201020",
):
    """
    加密货币历史数据
    https://cn.investing.com/crypto/ethereum/historical-data
    :param symbol: 货币名称
    :type symbol: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: '20151020', 注意格式
    :type start_date: str
    :param end_date: '20201020', 注意格式
    :type end_date: str
    :return: 加密货币历史数据获取
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    start_date = "/".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "/".join([end_date[:4], end_date[4:6], end_date[6:]])
    name_url_df = crypto_name_map()
    temp_url = name_url_df[name_url_df["name"] == symbol]["url"].values[0]
    res = requests.post(temp_url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find_all(text=re.compile("window.histDataExcessInfo"))[0].strip()
    para_data = re.findall(r"\d+", data)
    url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    payload = {
        "curr_id": para_data[0],
        "smlID": para_data[1],
        "header": "null",
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": period_map[period],
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    r = requests.post(url, data=payload, headers=headers)
    temp_df = pd.read_html(r.text)[0]
    df_data = temp_df
    if period == "每月":
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月")
    else:
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    if any(df_data["交易量"].astype(str).str.contains("-")):
        df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][
            df_data["交易量"].str.contains("-")
        ].replace("-", 0)
    if any(df_data["交易量"].astype(str).str.contains("B")):
        df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)]
            .str.replace("B", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000000
        )
    if any(df_data["交易量"].astype(str).str.contains("M")):
        df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)]
            .str.replace("M", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000
        )
    if any(df_data["交易量"].astype(str).str.contains("K")):
        df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)]
            .str.replace("K", "")
            .str.replace(",", "")
            .astype(float)
            * 1000
        )
    df_data["交易量"] = df_data["交易量"].astype(float)
    df_data["涨跌幅"] = pd.DataFrame(
        round(
            df_data["涨跌幅"].str.replace(",", "").str.replace("%", "").astype(float)
            / 100,
            6,
        )
    )
    del df_data["日期"]
    return df_data


if __name__ == "__main__":
    crypto_name_map_df = crypto_name_map()
    print(crypto_name_map_df)
    crypto_hist_df = crypto_hist(
        symbol="比特币", period="每日", start_date="20151020", end_date="20210107"
    )
    print(crypto_hist_df)
