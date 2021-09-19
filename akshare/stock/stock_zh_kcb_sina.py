# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2019/10/30 11:28
Desc: 新浪财经-科创板-实时行情数据和历史行情数据(包含前复权和后复权因子)
"""
import datetime
import re

from akshare.utils import demjson
import pandas as pd
import requests
from tqdm import tqdm

from akshare.stock.cons import (zh_sina_kcb_stock_payload,
                                zh_sina_kcb_stock_url,
                                zh_sina_kcb_stock_count_url,
                                zh_sina_kcb_stock_hist_url,
                                zh_sina_kcb_stock_hfq_url,
                                zh_sina_kcb_stock_qfq_url,
                                zh_sina_kcb_stock_amount_url)


def get_zh_kcb_page_count() -> int:
    """
    所有股票的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_a
    :return: int 需要抓取的股票总页数
    """
    res = requests.get(zh_sina_kcb_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_kcb_spot() -> pd.DataFrame:
    """
    从新浪财经-A股获取所有A股的实时行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk
    :return: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_zh_kcb_page_count()
    zh_sina_stock_payload_copy = zh_sina_kcb_stock_payload.copy()
    for page in tqdm(range(1, page_count+1)):
        zh_sina_stock_payload_copy.update({"page": page})
        zh_sina_stock_payload_copy.update({"_s_r_a": "page"})
        res = requests.get(
            zh_sina_kcb_stock_url,
            params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    return big_df


def stock_zh_kcb_daily(symbol: str = "sh688399", adjust: str = "") -> pd.DataFrame:
    """
    从新浪财经-A股获取某个股票的历史行情数据, 大量抓取容易封IP
    :param symbol: str e.g., sh600000
    :param adjust: str 默认为空, 不复权; qfq, 前复权因子; hfq, 后复权因子;
    :return: pandas.DataFrame
    不复权数据
                日期     开盘价     最高价     最低价     收盘价        成交    盘后量      盘后额
    0   2019-07-22  91.300  97.200  66.300  74.920  58330685  40778  3055088
    1   2019-07-23  70.020  78.880  70.000  74.130  23906020  43909  3254974
    2   2019-07-24  74.130  76.550  72.500  75.880  21608530  23149  1756546
    3   2019-07-25  75.000  79.980  74.600  78.000  24626920  66921  5219838
    4   2019-07-26  76.780  76.780  70.300  71.680  16831530  49106  3519918
    ..         ...     ...     ...     ...     ...       ...    ...      ...
    67  2019-10-31  59.790  60.500  57.800  58.290   2886407   3846   224183
    68  2019-11-01  57.900  59.960  57.600  59.250   2246059      0        0
    69  2019-11-04  60.040  61.880  60.040  61.740   3945106   1782   110021
    70  2019-11-05  61.100  62.780  60.850  62.160   4187105    400    24864
    71  2019-11-06  62.320  62.620  60.900  61.130   2331354   1300    79469

    后复权因子
             date          hfq_factor
    0  2019-07-22  1.0000000000000000
    1  1900-01-01  1.0000000000000000

    前复权因子
                 date          qfq_factor
    0  2019-07-22  1.0000000000000000
    1  1900-01-01  1.0000000000000000
    """
    res = requests.get(zh_sina_kcb_stock_hist_url.format(symbol, datetime.datetime.now().strftime("%Y_%m_%d"), symbol))
    data_json = demjson.decode(res.text[res.text.find("["):res.text.rfind("]")+1])
    data_df = pd.DataFrame(data_json)
    data_df.index = pd.to_datetime(data_df["d"])
    data_df.index.name = "date"
    del data_df["d"]

    r = requests.get(zh_sina_kcb_stock_amount_url.format(symbol, symbol))
    amount_data_json = demjson.decode(r.text[r.text.find("["): r.text.rfind("]")+1])
    amount_data_df = pd.DataFrame(amount_data_json)
    amount_data_df.index = pd.to_datetime(amount_data_df.date)
    del amount_data_df["date"]
    temp_df = pd.merge(data_df, amount_data_df, left_index=True, right_index=True, how="left")
    temp_df.fillna(method="ffill", inplace=True)
    temp_df = temp_df.astype(float)
    temp_df["amount"] = temp_df["amount"] * 10000
    temp_df["turnover"] = temp_df["v"] / temp_df["amount"]
    temp_df.columns = ["open", "high", "low", "close", "volume", "after_volume", "after_amount", "outstanding_share", "turnover"]

    if not adjust:
        return temp_df

    if adjust == "hfq":
        res = requests.get(zh_sina_kcb_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        hfq_factor_df.columns = ["date", "hfq_factor"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]

        temp_df = pd.merge(
            temp_df, hfq_factor_df, left_index=True, right_index=True, how="left"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] * temp_df["hfq_factor"]
        temp_df["high"] = temp_df["high"] * temp_df["hfq_factor"]
        temp_df["close"] = temp_df["close"] * temp_df["hfq_factor"]
        temp_df["low"] = temp_df["low"] * temp_df["hfq_factor"]
        return temp_df.iloc[:, :-1]

    if adjust == "qfq":
        res = requests.get(zh_sina_kcb_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]

        temp_df = pd.merge(
            temp_df, qfq_factor_df, left_index=True, right_index=True, how="left"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] / temp_df["qfq_factor"]
        temp_df["high"] = temp_df["high"] / temp_df["qfq_factor"]
        temp_df["close"] = temp_df["close"] / temp_df["qfq_factor"]
        temp_df["low"] = temp_df["low"] / temp_df["qfq_factor"]
        return temp_df.iloc[:, :-1]

    if adjust == "hfq-factor":
        res = requests.get(zh_sina_kcb_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        hfq_factor_df.columns = ["date", "hfq_factor"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]
        return hfq_factor_df

    if adjust == "qfq-factor":
        res = requests.get(zh_sina_kcb_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]
        return qfq_factor_df


if __name__ == "__main__":
    stock_zh_kcb_daily_qfq_df = stock_zh_kcb_daily(symbol="sh688399", adjust="qfq")
    print(stock_zh_kcb_daily_qfq_df)
    stock_zh_kcb_daily_hfq_df = stock_zh_kcb_daily(symbol="sh688399", adjust="hfq")
    print(stock_zh_kcb_daily_hfq_df)
    stock_zh_kcb_daily_df = stock_zh_kcb_daily(symbol="sh688399", adjust="qfq-factor")
    print(stock_zh_kcb_daily_df)
    stock_zh_kcb_spot_df = stock_zh_kcb_spot()
    print(stock_zh_kcb_spot_df)
