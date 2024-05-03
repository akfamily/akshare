# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/4/21 17:00
Desc: funddb-工具-估值情绪-恐惧贪婪指数
https://funddb.cn/tool/fear
"""

import json

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

from akshare.datasets import get_ths_js


def _get_file_content_ths(file: str = "cninfo.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_ths_js(file)
    with open(setting_file_path, encoding="utf8") as f:
        file_data = f.read()
    return file_data


def index_fear_greed_funddb(symbol: str = "上证指数") -> pd.DataFrame:
    """
    funddb-工具-估值情绪-恐惧贪婪指数
    https://funddb.cn/tool/fear
    :param symbol: choice of {"上证指数", "沪深300"}
    :type symbol: str
    :return: 恐惧贪婪指数
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "上证指数": "000001.SH",
        "沪深300": "000300.SH",
    }
    url = "https://api.jiucaishuo.com/v2/kjtl/kjtlconnect"
    payload = {
        "gu_code": symbol_map[symbol],
        "type": "h5",
        "version": "2.4.5",
        "act_time": 1697623588394,
    }
    r = requests.post(url, json=payload)
    data_json = r.json()
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("cninfo.js")
    js_code.eval(js_content)
    mcode = js_code.call("new_my_decode", data_json)
    data_json = json.loads(mcode)
    date_list = data_json["data"]["xAxis"]["categories"]
    tl_list = data_json["data"]["series"][0]["data"]
    sz_list = data_json["data"]["series"][1]["data"]
    temp_df = pd.DataFrame([date_list, tl_list, sz_list]).T
    temp_df.columns = ["date", "fear", "index"]
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df["fear"] = pd.to_numeric(temp_df["fear"], errors="coerce")
    temp_df["index"] = pd.to_numeric(temp_df["index"], errors="coerce")

    temp_df["fear"] = temp_df["fear"].round(2)
    temp_df["index"] = temp_df["index"].round(2)
    return temp_df


if __name__ == "__main__":
    index_fear_greed_funddb_df = index_fear_greed_funddb(symbol="上证指数")
    print(index_fear_greed_funddb_df)

    index_fear_greed_funddb_df = index_fear_greed_funddb(symbol="沪深300")
    print(index_fear_greed_funddb_df)
