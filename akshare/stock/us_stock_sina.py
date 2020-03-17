# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 18:47
contact: jindaxiang@163.com
desc: 获取新浪财经-美股实时行情数据和历史行情数据
优化: 在美股行情的获取上采用多线程模式(新浪会封IP, 不再优化)
"""
import json

import execjs
import pandas as pd
import requests
from tqdm import tqdm

from akshare.stock.cons import (
    js_hash_text,
    hk_js_decode,
    us_sina_stock_list_url,
    us_sina_stock_dict_payload,
    us_sina_stock_hist_url,
    us_sina_stock_hist_qfq_url,
)


def get_us_page_count():
    page = "1"
    us_js_decode = f"US_CategoryService.getList?page={page}&num=20&sort=&asc=0&market=&id="
    js_code = execjs.compile(js_hash_text)
    dict_list = js_code.call("d", us_js_decode)  # 执行js解密代码
    us_sina_stock_dict_payload.update({"page": "{}".format(page)})
    res = requests.get(
        us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload
    )
    data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
    if not isinstance(int(data_json["count"]) / 20, int):
        page_count = int(int(data_json["count"]) / 20) + 1
    else:
        page_count = int(int(data_json["count"]) / 20)
    return page_count


def get_us_stock_name() -> pd.DataFrame:
    """
    u.s. stock's english name, chinese name and symbol
    you should use symbol to get apply into the next function
    :return: stock's english name, chinese name and symbol
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_us_page_count()
    for page in tqdm(range(1, page_count + 1)):
        # page = "1"
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(
            page
        )
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call("d", us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        res = requests.get(
            us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload
        )
        data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df[["name", "cname", "symbol"]]


def stock_us_spot():
    big_df = pd.DataFrame()
    page_count = get_us_page_count()
    for page in tqdm(range(1, page_count + 1)):
        # page = "1"
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(
            page
        )
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call("d", us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        res = requests.get(
            us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload
        )
        data_json = json.loads(res.text[res.text.find("({") + 1 : res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df


def stock_us_daily(symbol="BRK.A", factor=""):
    res = requests.get(us_sina_stock_hist_url.format(symbol))
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df.astype("float")
    res = requests.get(us_sina_stock_hist_qfq_url.format(symbol))
    qfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])["data"])
    qfq_factor_df.columns = ["date", "qfq_factor", "-"]
    if factor == "qfq":
        return qfq_factor_df.iloc[:, :2]
    else:
        return data_df


if __name__ == "__main__":
    stock_us_stock_name_df = get_us_stock_name()
    print(stock_us_stock_name_df)
    stock_us_spot_df = stock_us_spot()
    print(stock_us_spot_df)
    stock_us_daily_df = stock_us_daily(symbol="AAPL", factor="qfq")
    print(stock_us_daily_df)
