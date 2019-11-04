# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 18:47
contact: jindaxiang@163.com
desc: 获取新浪财经-美股实时数据和历史数据
"""
import json

import requests
import pandas as pd
import execjs

from akshare.stock.cons import (js_hash_text,
                                us_sina_stock_list_url,
                                us_sina_stock_dict_payload,
                                us_sina_stock_hist_url,
                                hk_js_decode,
                                us_sina_stock_hist_qfq_url)


def get_us_current_stock_price():
    big_df = pd.DataFrame()
    for page in range(1, 489):
        # page = "1"
        print("正在抓取第{}页的美股数据".format(page))
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(page)
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call('d', us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        res = requests.get(us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload)
        data_json = json.loads(res.text[res.text.find("({")+1: res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df


def get_us_stock_name():
    big_df = pd.DataFrame()
    for page in range(1, 5):
        # page = "1"
        print("正在抓取第{}页的美股数据".format(page))
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(page)
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call('d', us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        res = requests.get(us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload)
        data_json = json.loads(res.text[res.text.find("({")+1: res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df


def get_us_stock_hist_data(symbol="BRK.A"):
    res = requests.get(us_sina_stock_hist_url.format(symbol))
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call('d', res.text.split("=")[1].split(";")[0].replace('"', ""))  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df.astype("float")
    res = requests.get(us_sina_stock_hist_qfq_url.format(symbol))
    qfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])['data'])
    qfq_factor_df.columns = ["date", "qfq_factor"]
    return data_df, qfq_factor_df


if __name__ == "__main__":
    df = get_us_stock_name()
    print(df)
    original_df, fq_df = get_us_stock_hist_data(symbol="AMZN")
    print(original_df)
    print(fq_df)
