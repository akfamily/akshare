# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/11/9 14:00
Desc: 中证商品指数
http://www.ccidx.com/
"""
from io import BytesIO

import pandas as pd
import requests


def futures_index_ccidx(symbol: str = "中证商品期货指数") -> pd.DataFrame:
    """
    中证商品指数-商品指数-日频率
    http://www.ccidx.com/index.html
    :param symbol: choice of {"中证商品期货指数", "中证商品期货价格指数"}
    :type symbol: str
    :return: 商品指数-日频率
    :rtype: pandas.DataFrame
    """
    futures_index_map = {
        "中证商品期货指数": "100001.CCI",
        "中证商品期货价格指数": "000001.CCI",
    }
    url = "http://www.ccidx.com/front/ajax_downZSHQ.do"
    params = {"indexCode": futures_index_map[symbol]}
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content), header=1, engine="openpyxl")
    temp_df.columns = [
        "日期",
        "指数代码",
        "指数中文全称",
        "指数中文简称",
        "指数英文全称",
        "指数英文简称",
        "开盘",
        "最高",
        "最低",
        "收盘",
        "结算",
        "涨跌",
        "涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["结算"] = pd.to_numeric(temp_df["结算"], errors="coerce")
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df.sort_values(by=['日期'], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def futures_index_min_ccidx(symbol: str = "中证监控油脂油料期货指数") -> pd.DataFrame:
    """
    中证商品指数-商品指数-分时数据
    http://www.ccidx.com/index.html
    :param symbol: choice of {"中证商品期货指数", "中证商品期货价格指数", "中证监控油脂油料期货指数", "中证监控软商品期货指数",  "中证监控能化期货指数", "中证监控钢铁期货指数"}
    :type symbol: str
    :return: 商品指数-分时数据
    :rtype: pandas.DataFrame
    """
    futures_index_map = {
        "中证商品期货指数": ["100001.CCI", "0"],
        "中证商品期货价格指数": ["000001.CCI", "1"],
        "中证监控油脂油料期货指数": ["606005.CCI", "2"],
        "中证监控软商品期货指数": ["606008.CCI", "3"],
        "中证监控能化期货指数": ["606010.CCI", "4"],
        "中证监控钢铁期货指数": ["606011.CCI", "5"],
    }
    url = "http://www.ccidx.com/cscidx/csciAction/loadTimeData"
    params = {"r": "0.08644997232349438"}
    payload = {
        "indexCode": futures_index_map[symbol][0],
        "indexType": futures_index_map[symbol][1],
        "pointer": "all",
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "44",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.ccidx.com",
        "Origin": "http://www.ccidx.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.ccidx.com/cscidx/quote1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(url, params=params, data=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [data_json["dataMap"]["axisList"], data_json["dataMap"]["lineList"]]
    ).T
    temp_df.columns = [
        "datetime",
        "value",
    ]
    temp_df["value"] = pd.to_numeric(temp_df["value"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    futures_index_ccidx_df = futures_index_ccidx(symbol="中证商品期货指数")
    print(futures_index_ccidx_df)

    futures_index_min_ccidx_df = futures_index_min_ccidx(symbol="中证商品期货指数")
    print(futures_index_min_ccidx_df)
