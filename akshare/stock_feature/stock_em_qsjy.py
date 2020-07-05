# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/5 22:49
Desc: 东方财富网-数据中心-特色数据-券商业绩月报
http://data.eastmoney.com/other/qsjy.html
"""
import demjson
import pandas as pd
import requests


def stock_em_qsjy(trade_date: str = "2020-01-01") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-券商业绩月报
    http://data.eastmoney.com/other/qsjy.html
    :param trade_date: 数据月份，从 2010-06-01 开始, e.g., 需要 2011 年 7 月, 则输入 2011-07-01
    :type trade_date: str
    :return: 券商业绩月报
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "QSYJBG_MReport",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "RQ",
        "sr": "-1",
        "p": "1",
        "ps": "1000",
        "js": "var KAHXVKzA={pages:(tp),data:(x)}",
        "filter": f"(RQ='{trade_date}T00:00:00')",
        "rt": "53132017",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df


if __name__ == '__main__':
    stock_em_qsjy_df = stock_em_qsjy(trade_date="2020-01-01")
    print(stock_em_qsjy_df)
