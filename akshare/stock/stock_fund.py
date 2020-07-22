# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/11 19:47
Desc: 东方财富网-数据中心-资金流向
http://data.eastmoney.com/zjlx/detail.html
"""
import json
import time

import pandas as pd
import requests


def stock_individual_fund_flow(
    stock: str = "600094", market: str = "sh"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-个股
    http://data.eastmoney.com/zjlx/detail.html
    :param stock: 股票代码
    :type stock: str
    :param market: 股票市场; 上海证券交易所: sh, 深证证券交易所: sz
    :type market: str
    :return: 近期个股的资金流数据
    :rtype: pandas.DataFrame
    """
    market_map = {"sh": 1, "sz": 0}
    url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "lmt": "0",
        "klt": "101",
        "secid": f"{market_map[market]}.{stock}",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery183003743205523325188_1589197499471",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{") : -2])
    content_list = json_data["data"]["klines"]
    temp_df = pd.DataFrame([item.split(",") for item in content_list])
    temp_df.columns = [
        "日期",
        "主力净流入-净额",
        "小单净流入-净额",
        "中单净流入-净额",
        "大单净流入-净额",
        "超大单净流入-净额",
        "主力净流入-净占比",
        "小单净流入-净占比",
        "中单净流入-净占比",
        "大单净流入-净占比",
        "超大单净流入-净占比",
        "收盘价",
        "涨跌幅",
        "-",
        "-",
    ]
    return temp_df.iloc[:, :-2]


def stock_individual_fund_flow_rank(indicator: str = "今日") -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-排名
    http://data.eastmoney.com/zjlx/detail.html
    :param indicator: choice of {"今日", "3日", "5日", "10日"}
    :type indicator: str
    :return: 指定 indicator 资金流向排行
    :rtype: pandas.DataFrame
    """
    indicator_map = {
        "今日": ["f62", "1"],
        "3日": ["f267", "3"],
        "5日": ["f164", "5"],
        "10日": ["f174", "10"],
    }
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": "2",
        "invt": "2",
        "fid0": "f4001",
        "fid": indicator_map[indicator][0],
        "fs": "m:0 t:6 f:!2,m:0 t:13 f:!2,m:0 t:80 f:!2,m:1 t:2 f:!2,m:1 t:23 f:!2,m:0 t:7 f:!2,m:1 t:3 f:!2",
        "stat": indicator_map[indicator][1],
        "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124",
        "rt": "52975151",
        "cb": "jQuery18303745396043640481_1589254432189",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{") : -2])
    temp_df = pd.DataFrame(json_data["data"]["diff"])
    temp_df.columns = [
        "最新价",
        "涨跌幅",
        "代码",
        "名称",
        "主力净流入-净额",
        "超大单净流入-净额",
        "超大单净流入-净占比",
        "大单净流入-净额",
        "大单净流入-净占比",
        "中单净流入-净额",
        "中单净流入-净占比",
        "小单净流入-净额",
        "小单净流入-净占比",
        "-",
        "主力净流入-净占比",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "最新价",
            "涨跌幅",
            "代码",
            "名称",
            "主力净流入-净额",
            "主力净流入-净占比",
            "超大单净流入-净额",
            "超大单净流入-净占比",
            "大单净流入-净额",
            "大单净流入-净占比",
            "中单净流入-净额",
            "中单净流入-净占比",
            "小单净流入-净额",
            "小单净流入-净占比",
        ]
    ]
    return temp_df


def stock_market_fund_flow() -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-大盘
    http://data.eastmoney.com/zjlx/dpzjlx.html
    :return: 近期大盘的资金流数据
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "lmt": "0",
        "klt": "101",
        "secid": "1.000001",
        "secid2": "0.399001",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery183003743205523325188_1589197499471",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{") : -2])
    content_list = json_data["data"]["klines"]
    temp_df = pd.DataFrame([item.split(",") for item in content_list])
    temp_df.columns = [
        "日期",
        "主力净流入-净额",
        "小单净流入-净额",
        "中单净流入-净额",
        "大单净流入-净额",
        "超大单净流入-净额",
        "主力净流入-净占比",
        "小单净流入-净占比",
        "中单净流入-净占比",
        "大单净流入-净占比",
        "超大单净流入-净占比",
        "上证-收盘价",
        "上证-涨跌幅",
        "深证-收盘价",
        "深证-涨跌幅",
    ]
    return temp_df


def stock_sector_fund_flow_rank(
    indicator: str = "5日", sector_type: str = "地域资金流"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-板块资金流-排名
    http://data.eastmoney.com/bkzj/hy.html
    :param indicator: choice of {"今日", "5日", "10日"}
    :type indicator: str
    :param sector_type: choice of {"行业资金流": "2", "概念资金流": "3", "地域资金流": "1"}
    :type sector_type: str
    :return: 指定参数的资金流排名数据
    :rtype: pandas.DataFrame
    """
    sector_type_map = {"行业资金流": "2", "概念资金流": "3", "地域资金流": "1"}
    indicator_map = {"今日": ["f62", "1"], "5日": ["f164", "5"], "10日": ["f174", "10"]}
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": "2",
        "invt": "2",
        "fid0": indicator_map[indicator][0],
        "fs": f"m:90 t:{sector_type_map[sector_type]}",
        "stat": indicator_map[indicator][1],
        "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124",
        "rt": "52975239",
        "cb": "jQuery18308357908311220152_1589256588824",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{") : -2])
    temp_df = pd.DataFrame(json_data["data"]["diff"])
    temp_df.columns = [
        "-",
        "涨跌幅",
        "板块代码",
        "板块名称",
        "主力净流入-净额",
        "超大单净流入-净额",
        "超大单净流入-净占比",
        "大单净流入-净额",
        "大单净流入-净占比",
        "中单净流入-净额",
        "中单净流入-净占比",
        "小单净流入-净额",
        "小单净流入-净占比",
        "-",
        "主力净流入-净占比",
        "主力净流入最大股",
        "主力净流入最大股代码",
        "是否净流入",
    ]
    temp_df = temp_df[
        [
            "涨跌幅",
            "板块代码",
            "板块名称",
            "主力净流入-净额",
            "主力净流入-净占比",
            "超大单净流入-净额",
            "超大单净流入-净占比",
            "大单净流入-净额",
            "大单净流入-净占比",
            "中单净流入-净额",
            "中单净流入-净占比",
            "小单净流入-净额",
            "小单净流入-净占比",
            "主力净流入最大股",
            "主力净流入最大股代码",
            "是否净流入",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_individual_fund_flow_df = stock_individual_fund_flow(
        stock="600094", market="sh"
    )
    print(stock_individual_fund_flow_df)

    stock_individual_fund_flow_rank_df = stock_individual_fund_flow_rank(indicator="今日")
    print(stock_individual_fund_flow_rank_df)

    stock_market_fund_flow_df = stock_market_fund_flow()
    print(stock_market_fund_flow_df)

    stock_sector_fund_flow_rank_df = stock_sector_fund_flow_rank(
        indicator="5日", sector_type="行业资金流"
    )
    print(stock_sector_fund_flow_rank_df)
