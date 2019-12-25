# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 11:28
contact: jindaxiang@163.com
desc: 新浪财经-港股-实时行情数据和历史行情数据(包含前复权和后复权因子)
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


def stock_hk_spot():
    """
    从新浪财经-港股获取所有港股的实时行情数据
    **行情延迟 15 分钟**
    http://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk
    :return: pandas.DataFrame
    """
    res = requests.get(
        hk_sina_stock_list_url,
        params=hk_sina_stock_dict_payload)
    data_json = [demjson.decode(tt) for tt in
                 [item + "}" for item in res.text[1:-1].split("},") if not item.endswith("}")]]
    data_df = pd.DataFrame(data_json)
    data_df = data_df[["symbol",
                       "name",
                       "engname",
                       "tradetype",
                       "lasttrade",
                       "prevclose",
                       "open",
                       "high",
                       "low",
                       "volume",
                       "amount",
                       "ticktime",
                       "buy",
                       "sell",
                       "pricechange",
                       "changepercent"]]
    return data_df


def stock_hk_daily(symbol="00001", factor=""):
    res = requests.get(hk_sina_stock_hist_url.format(symbol))
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call(
        'd', res.text.split("=")[1].split(";")[0].replace(
            '"', ""))  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df.astype("float")
    if not factor:
        return data_df
    if factor == "hfq":
        res = requests.get(hk_sina_stock_hist_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        hfq_factor_df.columns = ["date", "hfq_factor", "cash"]
        return hfq_factor_df
    if factor == "qfq":
        res = requests.get(hk_sina_stock_hist_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        return qfq_factor_df


if __name__ == "__main__":
    hist_data_df = stock_hk_daily(symbol="00005", factor="hfq")
    print(hist_data_df)
    current_data_df = stock_hk_spot()
    print(current_data_df)
