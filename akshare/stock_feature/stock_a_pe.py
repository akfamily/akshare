# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/12 21:30
Desc: A股市盈率
https://www.legulegu.com/stockdata/market_pe
"""
import pandas as pd
import requests


def stock_a_pe(market: str = "sh") -> pd.DataFrame:
    """
    A 股市盈率
    https://www.legulegu.com/stockdata/market_pe
    :param market: choice of {"sh", "sz", "cz", "zx"}
    :type market: str
    :return: 指定市场的 A 股平均市盈率
    :rtype: pandas.DataFrame
    """
    url = "https://www.legulegu.com/stockdata/market_pe/getmarket_pe"
    params = {
        "token": "9f6e7b4b8e54798bdec8ced0ce07e8d1"
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["cySharesPEList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    cy_df = temp_df[["close", "pe"]]

    temp_df = pd.DataFrame(data_json["shSharesPEList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    sh_df = temp_df[["close", "pe"]]

    temp_df = pd.DataFrame(data_json["szSharesPEList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    sz_df = temp_df[["close", "pe"]]

    temp_df = pd.DataFrame(data_json["zxSharesPEList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    zx_df = temp_df[["close", "pe"]]

    if market == "sh":
        return sh_df
    elif market == "sz":
        return sz_df
    elif market == "cy":
        return cy_df
    elif market == "zx":
        return zx_df
    elif market == "kc":
        url = "https://www.legulegu.com/stockdata/get-ke-chuang-ban-pe"
        params = {
            "token": "9f6e7b4b8e54798bdec8ced0ce07e8d1"
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        kc_df = pd.DataFrame(data_json["data"]["items"], columns=data_json["data"]["fields"])
        return kc_df
    elif market == "all":
        url = "https://www.legulegu.com/stockdata/market-ttm-lyr/get-data"
        params = {
            "token": "9f6e7b4b8e54798bdec8ced0ce07e8d1",
            "marketId": "5"
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
        all_df = temp_df[["averagePELYR", "averagePETTM", "middlePELYR", "middlePETTM", "close"]]
        return all_df
    if market in ["000016.XSHG",
                  "000016.XSHG",
                  "000010.XSHG",
                  "000009.XSHG",
                  "000902.XSHG",
                  "000903.XSHG",
                  "000905.XSHG",
                  "000906.XSHG",
                  "000852.XSHG"]:
        url = "https://www.legulegu.com/stockdata/market-ttm-lyr/get-data"
        params = {
            "token": "9f6e7b4b8e54798bdec8ced0ce07e8d1",
            "marketId": market
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
        index_df = temp_df[["averagePELYR", "averagePETTM", "middlePELYR", "middlePETTM", "close"]]
        return index_df


if __name__ == '__main__':
    stock_a_pe_df = stock_a_pe(market="000016.XSHG")
    print(stock_a_pe_df)
