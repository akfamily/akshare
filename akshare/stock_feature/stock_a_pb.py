# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/12 21:54
Desc: A股市净率
https://www.legulegu.com/stockdata/market_pb
"""
import pandas as pd
import requests


def stock_a_pb(market: str = "sh") -> pd.DataFrame:
    """
    A股市净率
    https://www.legulegu.com/stockdata/market_pb
    :param market: choice of {"sh", "sz", "cz", "zx", "000016.XSHG" ...}
    :type market: str
    :return: 指定市场的 A 股平均市盈率
    :rtype: pandas.DataFrame
    """
    url = "https://www.legulegu.com/stockdata/market_pb/getmarket_pb"
    params = {
        "token": "9f6e7b4b8e54798bdec8ced0ce07e8d1"
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["cySharesPBList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    cy_df = temp_df[["close", "pb"]]

    temp_df = pd.DataFrame(data_json["shSharesPBList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    sh_df = temp_df[["close", "pb"]]

    temp_df = pd.DataFrame(data_json["szSharesPBList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    sz_df = temp_df[["close", "pb"]]

    temp_df = pd.DataFrame(data_json["zxSharesPBList"])
    temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    zx_df = temp_df[["close", "pb"]]

    if market in ["000016.XSHG",
                  "000016.XSHG",
                  "000010.XSHG",
                  "000009.XSHG",
                  "000902.XSHG",
                  "000903.XSHG",
                  "000905.XSHG",
                  "000906.XSHG",
                  "000852.XSHG"]:
        url = "https://www.legulegu.com/stockdata/market-index-pb/get-data"
        params = {
            "token": "9f6e7b4b8e54798bdec8ced0ce07e8d1",
            "marketId": market
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.index = pd.to_datetime(temp_df["date"], unit="ms").dt.date
        index_df = temp_df[["equalWeightAveragePB", "middlePB", "weightingAveragePB", "close"]]
        return index_df

    if market == "sh":
        return sh_df
    elif market == "sz":
        return sz_df
    elif market == "cy":
        return cy_df
    elif market == "zx":
        return zx_df


if __name__ == '__main__':
    stock_a_pb_df = stock_a_pb(market="000016.XSHG")
    print(stock_a_pb_df)
