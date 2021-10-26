#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/6/22 17:41
Desc: 芝加哥商业交易所-比特币成交量报告
https://datacenter.jin10.com/reportType/dc_cme_btc_report
"""
import pandas as pd
import requests


def crypto_bitcoin_cme(date: str = "20210609") -> pd.DataFrame:
    """
    芝加哥商业交易所-比特币成交量报告
    https://datacenter.jin10.com/reportType/dc_cme_btc_report
    :return: 比特币成交量报告
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-api.jin10.com/reports/list"
    params = {
        "category": "cme",
        "date": "-".join([date[:4], date[4:6], date[6:]]),
        "attr_id": "4",
        "_": "1624354777843",
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [item for item in data_json["data"]["values"]],
        columns=[item["name"] for item in data_json["data"]["keys"]],
    )
    return temp_df


if __name__ == "__main__":
    crypto_bitcoin_cme_df = crypto_bitcoin_cme(date="20210621")
    print(crypto_bitcoin_cme_df)
