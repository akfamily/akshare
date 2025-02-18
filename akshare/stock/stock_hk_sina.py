#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/2/18 16:00
Desc: 新浪财经-港股-实时行情数据和历史行情数据(包含前复权和后复权因子)
https://stock.finance.sina.com.cn/hkstock/quotes/00700.html
"""

import pandas as pd
import requests
import py_mini_racer

from akshare.stock.cons import (
    hk_js_decode,
    hk_sina_stock_dict_payload,
    hk_sina_stock_list_url,
    hk_sina_stock_hist_url,
    hk_sina_stock_hist_hfq_url,
    hk_sina_stock_hist_qfq_url,
)
from akshare.utils import demjson


def stock_hk_spot() -> pd.DataFrame:
    """
    新浪财经-港股的所有港股的实时行情数据
    https://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk
    :return: 实时行情数据
    :rtype: pandas.DataFrame
    """
    res = requests.get(hk_sina_stock_list_url, params=hk_sina_stock_dict_payload)
    data_json = [
        demjson.decode(tt)
        for tt in [
            item + "}" for item in res.text[1:-1].split("},") if not item.endswith("}")
        ]
    ]
    data_df = pd.DataFrame(data_json)
    data_df = data_df[
        [
            "symbol",
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
            "changepercent",
        ]
    ]
    return data_df


def stock_hk_daily(symbol: str = "00981", adjust: str = "") -> pd.DataFrame:
    """
    新浪财经-港股-个股的历史行情数据
    https://stock.finance.sina.com.cn/hkstock/quotes/02912.html
    :param symbol: 可以使用 stock_hk_spot 获取
    :type symbol: str
    :param adjust: "": 返回未复权的数据 ; qfq: 返回前复权后的数据; qfq-factor: 返回前复权因子和调整;
    :type adjust: str
    :return: 指定 adjust 的数据
    :rtype: pandas.DataFrame
    """
    r = requests.get(hk_sina_stock_hist_url.format(symbol))
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", r.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df.index = pd.to_datetime(data_df["date"]).dt.date
    del data_df["date"]
    data_df = data_df.astype("float")

    if adjust == "":
        data_df.reset_index(inplace=True)
        data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
        return data_df

    if adjust == "hfq":
        r = requests.get(hk_sina_stock_hist_hfq_url.format(symbol))
        try:
            hfq_factor_df = pd.DataFrame(
                eval(r.text.split("=")[1].split("\n")[0])["data"]
            )
            if len(hfq_factor_df) == 1:
                data_df.reset_index(inplace=True)
                data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
                return data_df
        except SyntaxError:
            data_df.reset_index(inplace=True)
            data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
            return data_df
        hfq_factor_df.columns = ["date", "hfq_factor", "cash"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]

        # 处理复权因子
        temp_date_range = pd.date_range(
            "1900-01-01", hfq_factor_df.index[0].isoformat()
        )
        temp_df = pd.DataFrame(range(len(temp_date_range)), temp_date_range)
        new_range = pd.merge(
            temp_df, hfq_factor_df, left_index=True, right_index=True, how="outer"
        )
        try:
            # try for pandas >= 2.1.0
            new_range.ffill(inplace=True)
        except Exception:
            try:
                new_range.fillna(method="ffill", inplace=True)
            except Exception as e:
                print("Error:", e)
        new_range = new_range.iloc[:, [1, 2]]

        temp_df = pd.merge(
            data_df, new_range, left_index=True, right_index=True, how="outer"
        )
        try:
            # try for pandas >= 2.1.0
            temp_df.ffill(inplace=True)
        except Exception:
            try:
                # try for pandas < 2.1.0
                temp_df.fillna(method="ffill", inplace=True)
            except Exception as e:
                print("Error:", e)
        temp_df.drop_duplicates(
            subset=["open", "high", "low", "close", "volume"], inplace=True
        )
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] * temp_df["hfq_factor"] + temp_df["cash"]
        temp_df["high"] = temp_df["high"] * temp_df["hfq_factor"] + temp_df["cash"]
        temp_df["close"] = temp_df["close"] * temp_df["hfq_factor"] + temp_df["cash"]
        temp_df["low"] = temp_df["low"] * temp_df["hfq_factor"] + temp_df["cash"]
        temp_df = temp_df.apply(lambda x: round(x, 4))
        temp_df.dropna(how="any", inplace=True)
        temp_df = temp_df.iloc[:, :-2]
        temp_df.reset_index(inplace=True)
        temp_df.rename({"index": "date"}, axis="columns", inplace=True)
        temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
        return temp_df

    if adjust == "qfq":
        r = requests.get(hk_sina_stock_hist_qfq_url.format(symbol))
        try:
            qfq_factor_df = pd.DataFrame(
                eval(r.text.split("=")[1].split("\n")[0])["data"]
            )
            if len(qfq_factor_df) == 1:
                data_df.reset_index(inplace=True)
                data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
                return data_df

        except SyntaxError:
            data_df.reset_index(inplace=True)
            data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
            return data_df
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]

        temp_date_range = pd.date_range(
            "1900-01-01", qfq_factor_df.index[0].isoformat()
        )
        temp_df = pd.DataFrame(range(len(temp_date_range)), temp_date_range)
        new_range = pd.merge(
            temp_df, qfq_factor_df, left_index=True, right_index=True, how="outer"
        )
        try:
            # try for pandas >= 2.1.0
            new_range.ffill(inplace=True)
        except Exception:
            try:
                # try for pandas < 2.1.0
                new_range.fillna(method="ffill", inplace=True)
            except Exception as e:
                print("Error:", e)
        new_range = new_range.iloc[:, [1]]

        temp_df = pd.merge(
            data_df, new_range, left_index=True, right_index=True, how="outer"
        )
        try:
            # try for pandas >= 2.1.0
            temp_df.ffill(inplace=True)
        except Exception:
            try:
                # try for pandas < 2.1.0
                temp_df.fillna(method="ffill", inplace=True)
            except Exception as e:
                print("Error:", e)
        temp_df.drop_duplicates(
            subset=["open", "high", "low", "close", "volume"], inplace=True
        )
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] * temp_df["qfq_factor"]
        temp_df["high"] = temp_df["high"] * temp_df["qfq_factor"]
        temp_df["close"] = temp_df["close"] * temp_df["qfq_factor"]
        temp_df["low"] = temp_df["low"] * temp_df["qfq_factor"]
        temp_df = temp_df.apply(lambda x: round(x, 4))
        temp_df.dropna(how="any", inplace=True)
        temp_df = temp_df.iloc[:, :-1]
        temp_df.reset_index(inplace=True)
        temp_df.rename({"index": "date"}, axis="columns", inplace=True)
        temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
        return temp_df

    if adjust == "hfq-factor":
        r = requests.get(hk_sina_stock_hist_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(eval(r.text.split("=")[1].split("\n")[0])["data"])
        hfq_factor_df.columns = ["date", "hfq_factor", "cash"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]
        hfq_factor_df.reset_index(inplace=True)
        hfq_factor_df["date"] = pd.to_datetime(hfq_factor_df["date"]).dt.date
        return hfq_factor_df

    if adjust == "qfq-factor":
        r = requests.get(hk_sina_stock_hist_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(eval(r.text.split("=")[1].split("\n")[0])["data"])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]
        qfq_factor_df.reset_index(inplace=True)
        qfq_factor_df["date"] = pd.to_datetime(qfq_factor_df["date"]).dt.date
        return qfq_factor_df


if __name__ == "__main__":
    stock_hk_daily_hfq_df = stock_hk_daily(symbol="00700", adjust="")
    print(stock_hk_daily_hfq_df)

    stock_hk_daily_hfq_df = stock_hk_daily(symbol="00700", adjust="hfq")
    print(stock_hk_daily_hfq_df)

    stock_hk_daily_hfq_df = stock_hk_daily(symbol="01591", adjust="hfq")
    print(stock_hk_daily_hfq_df)

    stock_hk_daily_hfq_df = stock_hk_daily(symbol="00700", adjust="qfq")
    print(stock_hk_daily_hfq_df)

    stock_hk_daily_df = stock_hk_daily(symbol="01302", adjust="qfq")
    print(stock_hk_daily_df)

    stock_hk_daily_hfq_factor_df = stock_hk_daily(symbol="00700", adjust="hfq-factor")
    print(stock_hk_daily_hfq_factor_df)

    stock_hk_spot_df = stock_hk_spot()
    print(stock_hk_spot_df)
