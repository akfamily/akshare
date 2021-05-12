# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/12 17:47
Desc: 中国公路物流运价、运量指数
http://index.0256.cn/expx.htm
"""
import pandas as pd
import requests


def index_cflp_price(symbol: str = "周指数") -> pd.DataFrame:
    """
    中国公路物流运价指数
    http://index.0256.cn/expx.htm
    :param symbol: choice of {"周指数", "月指数", "季度指数", "年度指数"}
    :type symbol: str
    :return: 中国公路物流运价指数
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "周指数": "2",
        "月指数": "3",
        "季度指数": "4",
        "年度指数": "5",
    }
    url = "http://index.0256.cn/expcenter_trend.action"
    params = {
        "marketId": "1",
        "attribute1": "5",
        "exponentTypeId": symbol_map[symbol],
        "cateId": "2",
        "attribute2": "华北",
        "city": "",
        "startLine": "",
        "endLine": "",
    }
    headers = {
        "Origin": "http://index.0256.cn",
        "Referer": "http://index.0256.cn/expx.htm",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    }
    r = requests.post(url, data=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [
            data_json["chart1"]["xLebal"],
            data_json["chart1"]["yLebal"],
            data_json["chart2"]["yLebal"],
            data_json["chart3"]["yLebal"],
        ]
    ).T
    temp_df.columns = ["日期", "定基指数", "环比指数", "同比指数"]
    return temp_df


def index_cflp_volume(symbol: str = "月指数") -> pd.DataFrame:
    """
    中国公路物流运量指数
    http://index.0256.cn/expx.htm
    :param symbol: choice of {"月指数", "季度指数", "年度指数"}
    :type symbol: str
    :return: 中国公路物流运量指数
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "月指数": "3",
        "季度指数": "4",
        "年度指数": "5",
    }
    url = "http://index.0256.cn/volume_query.action"
    params = {
        "type": "1",
        "marketId": "1",
        "expTypeId": symbol_map[symbol],
        "startDate1": "",
        "endDate1": "",
        "city": "",
        "startDate3": "",
        "endDate3": "",
    }
    headers = {
        "Origin": "http://index.0256.cn",
        "Referer": "http://index.0256.cn/expx.htm",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    }
    r = requests.post(url, data=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [
            data_json["chart1"]["xLebal"],
            data_json["chart1"]["yLebal"],
            data_json["chart2"]["yLebal"],
            data_json["chart3"]["yLebal"],
        ]
    ).T
    temp_df.columns = ["日期", "定基指数", "环比指数", "同比指数"]
    return temp_df


if __name__ == "__main__":
    index_cflp_price_df = index_cflp_price(symbol="周指数")
    print(index_cflp_price_df)

    index_cflp_price_df = index_cflp_price(symbol="月指数")
    print(index_cflp_price_df)

    index_cflp_price_df = index_cflp_price(symbol="季度指数")
    print(index_cflp_price_df)

    index_cflp_price_df = index_cflp_price(symbol="年度指数")
    print(index_cflp_price_df)

    index_cflp_volume_df = index_cflp_volume(symbol="月指数")
    print(index_cflp_volume_df)

    index_cflp_volume_df = index_cflp_volume(symbol="季度指数")
    print(index_cflp_volume_df)

    index_cflp_volume_df = index_cflp_volume(symbol="年度指数")
    print(index_cflp_volume_df)
