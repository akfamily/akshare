# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/3/23 17:28
Desc: 东方财富网-数据中心-特色数据-千股千评
http://data.eastmoney.com/stockcomment/
"""
import demjson
import pandas as pd
import requests


def stock_em_comment():
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "QGQP_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "Code",
        "sr": "1",
        "p": "1",
        "ps": "10000",
        "js": "var fHdHpFHW={pages:(tp),data:(x),font:(font)}",
        "filter": "",
        "rt": "52831859",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    data_df = pd.DataFrame(data_json["data"])
    return data_df


if __name__ == '__main__':
    stock_em_comment_df = stock_em_comment()
    print(stock_em_comment_df)
