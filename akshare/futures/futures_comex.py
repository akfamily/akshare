# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/9/25 13:46
Desc: 东方财富网-数据中心-COMEX库存数据
http://data.eastmoney.com/pmetal/comex/by.html
"""
import demjson
import pandas as pd
import requests


def futures_comex_inventory(symbol="黄金"):
    """
    东方财富网-数据中心-COMEX库存数据
    http://data.eastmoney.com/pmetal/comex/by.html
    :param symbol: choice of {"黄金", "白银"}
    :type symbol: str
    :return: COMEX库存数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "黄金": "(ID='EMI00069026')",
        "白银": "(ID='EMI00069027')",
    }
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "HJBY_KC",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "p": "1",
        "ps": "5000",
        "st": "DATADATE",
        "sr": "-1",
        "filter": symbol_map[symbol],
        "js": "var hVtWMLwm={pages:(tp),data:(x)}",
        "rt": "53367096",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    del temp_df["ID"]
    temp_df["DATADATE"] = pd.to_datetime(temp_df["DATADATE"])
    temp_df.columns = ["date", "value1", "value2"]
    return temp_df


if __name__ == '__main__':
    futures_comex_inventory_df = futures_comex_inventory(symbol="黄金")
    print(futures_comex_inventory_df)
