# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/11 15:20
Desc: 腾讯财经-A+H股数据, 实时行情数据和历史行情数据(后复权)
https://stockapp.finance.qq.com/mstats/#mod=list&id=hk_ah&module=HK&type=AH&sort=3&page=3&max=20
"""
import random

import requests
import pandas as pd
import demjson
from tqdm import tqdm

from akshare.stock.cons import (hk_url,
                                hk_headers,
                                hk_payload,
                                hk_stock_url,
                                hk_stock_headers,
                                hk_stock_payload)


def _get_zh_stock_ah_page_count() -> int:
    """
    腾讯财经-港股-AH-总页数
    https://stockapp.finance.qq.com/mstats/#mod=list&id=hk_ah&module=HK&type=AH&sort=3&page=3&max=20
    :return: 总页数
    :rtype: int
    """
    hk_payload_copy = hk_payload.copy()
    hk_payload_copy.update({"reqPage": 1})
    res = requests.get(hk_url, params=hk_payload_copy, headers=hk_headers)
    data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    page_count = data_json["data"]["page_count"]
    return page_count


def stock_zh_ah_spot() -> pd.DataFrame:
    """
    腾讯财经-港股-AH-实时行情
    https://stockapp.finance.qq.com/mstats/#mod=list&id=hk_ah&module=HK&type=AH&sort=3&page=3&max=20
    :return: 腾讯财经-港股-AH-实时行情
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_stock_ah_page_count() + 1
    for i in tqdm(range(1, page_count)):
        hk_payload.update({"reqPage": i})
        res = requests.get(hk_url, params=hk_payload, headers=hk_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        big_df = big_df.append(pd.DataFrame(data_json["data"]["page_data"]).iloc[:, 0].str.split("~", expand=True), ignore_index=True).iloc[:, :-1]
    big_df.columns = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "买入", "卖出", "成交量", "成交额", "今开", "昨收", "最高", "最低"]
    return big_df


def stock_zh_ah_name() -> dict:
    """
    腾讯财经-港股-AH-股票名称
    :return: 股票代码和股票名称的字典
    :rtype: dict
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_stock_ah_page_count() + 1
    for i in tqdm(range(1, page_count)):
        hk_payload.update({"reqPage": i})
        res = requests.get(hk_url, params=hk_payload, headers=hk_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        big_df = big_df.append(pd.DataFrame(data_json["data"]["page_data"]).iloc[:, 0].str.split("~", expand=True), ignore_index=True).iloc[:, :-1]
    big_df.columns = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "买入", "卖出", "成交量", "成交额", "今开", "昨收", "最高", "最低"]
    code_name_dict = dict(zip(big_df["代码"], big_df["名称"]))
    return code_name_dict


def stock_zh_ah_daily(symbol: str = "02318", start_year: str = "2000", end_year: str = "2019") -> pd.DataFrame:
    """
    腾讯财经-港股-AH-股票历史行情
    http://gu.qq.com/hk01033/gp
    :param symbol: 股票代码
    :type symbol: str
    :param start_year: 开始年份; e.g., “2000”
    :type start_year: str
    :param end_year: 结束年份; e.g., “2019”
    :type end_year: str
    :return: 指定股票在指定年份的日频率历史行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    for year in tqdm(range(int(start_year), int(end_year))):
        hk_stock_payload_copy = hk_stock_payload.copy()
        hk_stock_payload_copy.update({"_var": f"kline_dayhfq{year}"})
        hk_stock_payload_copy.update({"param": f"hk{symbol},day,{year}-01-01,{int(year) + 1}-12-31,640,hfq"})
        hk_stock_payload_copy.update({"r": random.random()})
        res = requests.get(hk_stock_url, params=hk_stock_payload_copy, headers=hk_stock_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        try:
            temp_df = pd.DataFrame(data_json["data"][f"hk{symbol}"]["hfqday"])
        except:
            continue
        temp_df.columns = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "_", "_", "_"]
        temp_df = temp_df[["日期", "开盘", "收盘", "最高", "最低", "成交量"]]
        # print("正在采集{}第{}年的数据".format(symbol, year))
        big_df = big_df.append(temp_df, ignore_index=True)
    return big_df


if __name__ == "__main__":
    stock_zh_ah_spot_df = stock_zh_ah_spot()
    print(stock_zh_ah_spot_df)
    big_dict = stock_zh_ah_name()
    print(big_dict)
    for item in big_dict.keys():
        stock_zh_ah_daily_df = stock_zh_ah_daily(symbol=item, start_year="2000", end_year="2019")
        print(stock_zh_ah_daily_df)
