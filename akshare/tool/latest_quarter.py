#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/5/4 20:30
Desc: 天天基金网-交易季度
https://fund.eastmoney.com/data/gmbdlist.html
"""
import requests

from akshare.utils import demjson


def latest_quarter() -> str:
    """
    天天基金网-基金数据-规模份额-规模变动-最新季度
    https://fund.eastmoney.com/data/gmbdlist.html
    :return: 最新季度字符串，如 "2026_1"
    :rtype: str
    """
    url = "https://fund.eastmoney.com/data/FundDataPortfolio_Interface.aspx"
    params = {
        "dt": "13",
        "pi": "1",
        "pn": "50",
        "mc": "quarterlist",
        "collname": "Gmbd",
    }
    r = requests.get(url, params=params)
    date_text = r.text
    start = date_text.find("[")
    end = date_text.rfind("]")
    quarter_list = demjson.decode(date_text[start : end + 1])
    return quarter_list[0]


if __name__ == "__main__":
    latest_quarter_str = latest_quarter()
    print(latest_quarter_str)