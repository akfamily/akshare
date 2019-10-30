# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 11:28
contact: jindaxiang@163.com
desc:
"""
import requests
import demjson
import pandas as pd
import execjs

from akshare.stock.cons import (hk_js_decode,
                                hk_sina_stock_dict_payload,
                                hk_sina_stock_list_url,
                                hk_sina_stock_hist_url,
                                hk_sina_stock_hist_hfq_url,
                                hk_sina_stock_hist_qfq_url)


def get_hk_stock_name():
    res = requests.get(hk_sina_stock_list_url, params=hk_sina_stock_dict_payload)
    data_json = [demjson.decode(tt) for tt in [item + "}" for item in res.text[1:-1].split("},") if not item.endswith("}")]]
    data_df = pd.DataFrame(data_json)
    return data_df


def get_hk_stock_hist_data(symbol="00001"):
    res = requests.get(hk_sina_stock_hist_url.format(symbol))
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call('d', res.text.split("=")[1].split(";")[0].replace('"', ""))  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df.astype("float")
    res = requests.get(hk_sina_stock_hist_hfq_url.format(symbol))
    hfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])['data'])
    res = requests.get(hk_sina_stock_hist_qfq_url.format(symbol))
    qfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])['data'])
    return data_df, hfq_factor_df, qfq_factor_df


if __name__ == "__main__":
    a, b, c = get_hk_stock_hist_data(symbol="00005")
    df = get_hk_stock_name()