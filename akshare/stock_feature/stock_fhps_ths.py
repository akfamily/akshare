#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/4/9 21:44
Desc: 同花顺-分红融资
https://basic.10jqka.com.cn/new/603444/bonus.html
"""
import pandas as pd
import requests


def stock_fhps_detail_ths(symbol: str = "603444") -> pd.DataFrame:
    """
    同花顺-分红融资
    https://basic.10jqka.com.cn/new/603444/bonus.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 分红融资
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/new/{symbol}/bonus.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    r.encoding = "gbk"
    temp_df = pd.read_html(r.text)[0]
    return temp_df


if __name__ == "__main__":
    stock_fhps_detail_ths_df = stock_fhps_detail_ths(symbol="603444")
    print(stock_fhps_detail_ths_df)
