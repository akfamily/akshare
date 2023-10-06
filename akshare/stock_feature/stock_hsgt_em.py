# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/3/10 16:32
Desc: 东方财富网-数据中心-沪深港通持股
https://data.eastmoney.com/hsgtcg/
沪深港通详情: https://finance.eastmoney.com/news/1622,20161118685370149.html
"""
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def stock_hsgt_fund_flow_summary_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-沪深港通资金流向
    https://data.eastmoney.com/hsgt/index.html#lssj
    :return: 沪深港通资金流向
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_MUTUAL_QUOTA",
        "columns": "TRADE_DATE,MUTUAL_TYPE,BOARD_TYPE,MUTUAL_TYPE_NAME,FUNDS_DIRECTION,INDEX_CODE,INDEX_NAME,BOARD_CODE",
        "quoteColumns": "status~07~BOARD_CODE,dayNetAmtIn~07~BOARD_CODE,dayAmtRemain~07~BOARD_CODE,dayAmtThreshold~07~BOARD_CODE,f104~07~BOARD_CODE,f105~07~BOARD_CODE,f106~07~BOARD_CODE,f3~03~INDEX_CODE~INDEX_f3,netBuyAmt~07~BOARD_CODE",
        'quoteType': '0',
        "pageNumber": "1",
        "pageSize": "2000",
        "sortTypes": "1",
        "sortColumns": "MUTUAL_TYPE",
        "source": "WEB",
        "client": "WEB",
        "_": "1669047266881",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "交易日",
        "-",
        "类型",
        "板块",
        "资金方向",
        "-",
        "相关指数",
        "-",
        "交易状态",
        "资金净流入",
        "当日资金余额",
        "-",
        "上涨数",
        "下跌数",
        "持平数",
        "指数涨跌幅",
        "成交净买额",
    ]
    temp_df = temp_df[[
        "交易日",
        "类型",
        "板块",
        "资金方向",
        "交易状态",
        "成交净买额",
        "资金净流入",
        "当日资金余额",
        "上涨数",
        "持平数",
        "下跌数",
        "相关指数",
        "指数涨跌幅",
    ]]
    temp_df['交易日'] = pd.to_datetime(temp_df['交易日']).dt.date
    temp_df['成交净买额'] = pd.to_numeric(temp_df['成交净买额'], errors="coerce")
    temp_df['资金净流入'] = pd.to_numeric(temp_df['资金净流入'], errors="coerce")
    temp_df['当日资金余额'] = pd.to_numeric(temp_df['当日资金余额'], errors="coerce")
    temp_df['上涨数'] = pd.to_numeric(temp_df['上涨数'], errors="coerce")
    temp_df['持平数'] = pd.to_numeric(temp_df['持平数'], errors="coerce")
    temp_df['下跌数'] = pd.to_numeric(temp_df['下跌数'], errors="coerce")
    temp_df['指数涨跌幅'] = pd.to_numeric(temp_df['指数涨跌幅'], errors="coerce")

    temp_df['成交净买额'] = temp_df['成交净买额'] / 10000
    temp_df['资金净流入'] = temp_df['资金净流入'] / 10000
    temp_df['当日资金余额'] = temp_df['当日资金余额'] / 10000

    return temp_df


def stock_hk_ggt_components_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-港股市场-港股通成份股
    https://quote.eastmoney.com/center/gridlist.html#hk_components
    :return: 港股通成份股
    :rtype: pandas.DataFrame
    """
    url = "https://33.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "fid": "f3",
        "fs": "b:DLMK0146,b:DLMK0144",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152",
        "_": "1639974456250",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "-",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "-",
        "-",
        "-",
        "-",
        "-",
        "代码",
        "-",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "今开",
            "最高",
            "最低",
            "昨收",
            "成交量",
            "成交额",
        ]
    ]
    return temp_df


def stock_hsgt_north_net_flow_in_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-北向概括-净流入
    http://data.eastmoney.com/hsgtcg/
    :param symbol: choice of {"沪股通", "深股通", "北上"}
    :type symbol: str
    :return: 东方财富网-数据中心-沪深港通持股-北向概括-净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f52",
        "klt": "101",
        "lmt": "5000",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    if symbol == "沪股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["hk2sh"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "深股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["hk2sz"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "北上":
        temp_df = (
            pd.DataFrame(data_json["data"]["s2n"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


def stock_hsgt_north_cash_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-北向概括-资金余额
    http://data.eastmoney.com/hsgtcg/
    :param symbol: choice of {"沪股通", "深股通", "北上"}
    :type symbol: str
    :return: 东方财富网-数据中心-沪深港通持股-北向概括-资金余额
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f53",
        "klt": "101",
        "lmt": "5000",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    if symbol == "沪股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["hk2sh"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "深股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["hk2sz"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "北上":
        temp_df = (
            pd.DataFrame(data_json["data"]["s2n"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


def stock_hsgt_north_acc_flow_in_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-北向概况-累计净流入
    http://data.eastmoney.com/hsgtcg/
    :param symbol: choice of {"沪股通", "深股通", "北上"}
    :type symbol: str
    :return: 东方财富网-数据中心-沪深港通持股-北向概括-累计净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f54",
        "klt": "101",
        "lmt": "5000",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    if symbol == "沪股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["hk2sh"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "深股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["hk2sz"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "北上":
        temp_df = (
            pd.DataFrame(data_json["data"]["s2n"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


def stock_hsgt_south_net_flow_in_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-南向概括-净流入
    http://data.eastmoney.com/hsgtcg/
    :param symbol: choice of {"沪股通", "深股通", "南下"}
    :type symbol: str
    :return: 东方财富网-数据中心-沪深港通持股-南向概括-净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f2,f4,f6",
        "fields2": "f51,f52",
        "klt": "101",
        "lmt": "5000",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18307854355493858363_1584963487410",
        "_": "1584964176697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    if symbol == "沪股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["sh2hk"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "深股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["sz2hk"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "南下":
        temp_df = (
            pd.DataFrame(data_json["data"]["n2s"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


def stock_hsgt_south_cash_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-南向概括-资金余额
    http://data.eastmoney.com/hsgtcg/
    :param symbol: choice of {"沪股通", "深股通", "南下"}
    :type symbol: str
    :return: 东方财富网-数据中心-沪深港通持股-南向概括-资金余额
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f2,f4,f6",
        "fields2": "f51,f53",
        "klt": "101",
        "lmt": "5000",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18307854355493858363_1584963487410",
        "_": "1584964176697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    if symbol == "沪股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["sh2hk"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "深股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["sz2hk"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "南下":
        temp_df = (
            pd.DataFrame(data_json["data"]["n2s"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


def stock_hsgt_south_acc_flow_in_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-南向概括-累计净流入
    http://data.eastmoney.com/hsgtcg/
    :param symbol: choice of {"沪股通", "深股通", "南下"}
    :type symbol: str
    :return: 东方财富网-数据中心-沪深港通持股-南向概括-累计净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f2,f4,f6",
        "fields2": "f51,f54",
        "klt": "101",
        "lmt": "5000",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18307854355493858363_1584963487410",
        "_": "1584964176697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -2])
    if symbol == "沪股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["sh2hk"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "深股通":
        temp_df = (
            pd.DataFrame(data_json["data"]["sz2hk"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    if symbol == "南下":
        temp_df = (
            pd.DataFrame(data_json["data"]["n2s"])
            .iloc[:, 0]
            .str.split(",", expand=True)
        )
        temp_df.columns = ["date", "value"]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


def stock_hsgt_hold_stock_em(
    market: str = "沪股通", indicator: str = "5日排行"
) -> pd.DataFrame:
    """
    东方财富-数据中心-沪深港通持股-个股排行
    http://data.eastmoney.com/hsgtcg/list.html
    :param market: choice of {"北向", "沪股通", "深股通"}
    :type market: str
    :param indicator: choice of {"今日排行", "3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"}
    :type indicator: str
    :return: 指定 sector 和 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/hsgtcg/list.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    date = (
        soup.find("div", attrs={"class": "title"})
        .find("span")
        .text.strip("（")
        .strip("）")
    )
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    if indicator == "今日排行":
        indicator_type = "1"
    if indicator == "3日排行":
        indicator_type = "3"
    if indicator == "5日排行":
        indicator_type = "5"
    if indicator == "10日排行":
        indicator_type = "10"
    if indicator == "月排行":
        indicator_type = "M"
    if indicator == "季排行":
        indicator_type = "Q"
    if indicator == "年排行":
        indicator_type = "Y"
    if market == "北向":
        filter_str = (
            f"""(TRADE_DATE='{date}')(INTERVAL_TYPE="{indicator_type}")"""
        )
    elif market == "沪股通":
        filter_str = f"""(TRADE_DATE='{date}')(INTERVAL_TYPE="{indicator_type}")(MUTUAL_TYPE="001")"""
    elif market == "深股通":
        filter_str = f"""(TRADE_DATE='{date}')(INTERVAL_TYPE="{indicator_type}")(MUTUAL_TYPE="003")"""
    params = {
        "sortColumns": "ADD_MARKET_CAP",
        "sortTypes": "-1",
        "pageSize": "50000",
        "pageNumber": "1",
        "reportName": "RPT_MUTUAL_STOCK_NORTHSTA",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": filter_str,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "_",
        "日期",
        "_",
        "名称",
        "_",
        "_",
        "代码",
        "_",
        "_",
        "_",
        "_",
        "今日持股-股数",
        "今日持股-市值",
        "今日持股-占流通股比",
        "今日持股-占总股本比",
        "今日收盘价",
        "今日涨跌幅",
        "_",
        "所属板块",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        f'{indicator.split("排")[0]}增持估计-市值',
        f'{indicator.split("排")[0]}增持估计-股数',
        f'{indicator.split("排")[0]}增持估计-市值增幅',
        f'{indicator.split("排")[0]}增持估计-占流通股比',
        f'{indicator.split("排")[0]}增持估计-占总股本比',
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "今日收盘价",
            "今日涨跌幅",
            "今日持股-股数",
            "今日持股-市值",
            "今日持股-占流通股比",
            "今日持股-占总股本比",
            f'{indicator.split("排")[0]}增持估计-股数',
            f'{indicator.split("排")[0]}增持估计-市值',
            f'{indicator.split("排")[0]}增持估计-市值增幅',
            f'{indicator.split("排")[0]}增持估计-占流通股比',
            f'{indicator.split("排")[0]}增持估计-占总股本比',
            "所属板块",
            "日期",
        ]
    ]
    big_df["今日收盘价"] = pd.to_numeric(big_df["今日收盘价"])
    big_df["今日涨跌幅"] = pd.to_numeric(big_df["今日涨跌幅"])
    big_df["今日持股-股数"] = pd.to_numeric(big_df["今日持股-股数"])
    big_df["今日持股-市值"] = pd.to_numeric(big_df["今日持股-市值"])
    big_df["今日持股-占流通股比"] = pd.to_numeric(big_df["今日持股-占流通股比"])
    big_df["今日持股-占总股本比"] = pd.to_numeric(big_df["今日持股-占总股本比"])
    big_df[f'{indicator.split("排")[0]}增持估计-股数'] = pd.to_numeric(
        big_df[f'{indicator.split("排")[0]}增持估计-股数']
    )
    big_df[f'{indicator.split("排")[0]}增持估计-市值'] = pd.to_numeric(
        big_df[f'{indicator.split("排")[0]}增持估计-市值']
    )
    big_df[f'{indicator.split("排")[0]}增持估计-市值增幅'] = pd.to_numeric(
        big_df[f'{indicator.split("排")[0]}增持估计-市值增幅']
    )
    big_df[f'{indicator.split("排")[0]}增持估计-占流通股比'] = pd.to_numeric(
        big_df[f'{indicator.split("排")[0]}增持估计-占流通股比']
    )
    big_df[f'{indicator.split("排")[0]}增持估计-占总股本比'] = pd.to_numeric(
        big_df[f'{indicator.split("排")[0]}增持估计-占总股本比']
    )
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    return big_df


def stock_hsgt_stock_statistics_em(
    symbol: str = "北向持股",
    start_date: str = "20230113",
    end_date: str = "20230113",
):
    """
    东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计
    https://data.eastmoney.com/hsgtcg/StockStatistics.aspx
    market=001, 沪股通持股
    market=003, 深股通持股
    :param symbol: choice of {"北向持股", "南向持股"}
    :type symbol: str
    :param start_date: 指定数据获取开始的时间, e.g., "20200713"
    :type start_date: str
    :param end_date: 指定数据获取结束的时间, e.g., "20200715"
    :type end_date:str
    :return: 指定市场和指定时间段的每日个股统计数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    if symbol == "南向持股":
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "pageSize": "1000",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(INTERVAL_TYPE="1")(RN=1)(TRADE_DATE>='{start_date}')(TRADE_DATE<='{end_date}')""",
            "rt": "53160469",
            "reportName": "RPT_MUTUAL_STOCK_HOLDRANKS",
        }
        if start_date == end_date:
            params.update(
                {
                    "filter": f"""(INTERVAL_TYPE="1")(RN=1)(TRADE_DATE='{start_date}')"""
                }
            )
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, int(total_page) + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)

        big_df.columns = [
            "-",
            "持股日期",
            "-",
            "-",
            "股票简称",
            "股票代码",
            "-",
            "-",
            "-",
            "-",
            "持股数量",
            "持股市值",
            "-",
            "-",
            "-",
            "-",
            "当日收盘价",
            "当日涨跌幅",
            "-",
            "-",
            "-",
            "-",
            "-",
            "持股数量占发行股百分比",
            "-",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "-",
        ]
        big_df = big_df[
            [
                "持股日期",
                "股票代码",
                "股票简称",
                "当日收盘价",
                "当日涨跌幅",
                "持股数量",
                "持股市值",
                "持股数量占发行股百分比",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["当日收盘价"] = pd.to_numeric(big_df["当日收盘价"])
        big_df["当日涨跌幅"] = pd.to_numeric(big_df["当日涨跌幅"])
        big_df["持股数量"] = pd.to_numeric(big_df["持股数量"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股数量占发行股百分比"] = pd.to_numeric(big_df["持股数量占发行股百分比"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
    elif symbol == "北向持股":
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "pageSize": "1000",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(INTERVAL_TYPE="1")(MUTUAL_TYPE in ("001","003"))(TRADE_DATE>='{start_date}')(TRADE_DATE<='{end_date}')""",
            "rt": "53160469",
            "reportName": "RPT_MUTUAL_STOCK_NORTHSTA",
        }
        if start_date == end_date:
            params.update(
                {
                    "filter": f"""(INTERVAL_TYPE="1")(MUTUAL_TYPE in ("001","003"))(TRADE_DATE='{start_date}')"""
                }
            )
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, int(total_page) + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)

        big_df.columns = [
            "-",
            "-",
            "持股日期",
            "-",
            "股票简称",
            "-",
            "-",
            "股票代码",
            "-",
            "-",
            "-",
            "-",
            "持股数量",
            "持股市值",
            "-",
            "持股数量占发行股百分比",
            "当日收盘价",
            "当日涨跌幅",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "-",
            "-",
        ]
        big_df = big_df[
            [
                "持股日期",
                "股票代码",
                "股票简称",
                "当日收盘价",
                "当日涨跌幅",
                "持股数量",
                "持股市值",
                "持股数量占发行股百分比",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["当日收盘价"] = pd.to_numeric(big_df["当日收盘价"])
        big_df["当日涨跌幅"] = pd.to_numeric(big_df["当日涨跌幅"])
        big_df["持股数量"] = pd.to_numeric(big_df["持股数量"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股数量占发行股百分比"] = pd.to_numeric(big_df["持股数量占发行股百分比"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
    elif symbol == "沪股通持股":
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "pageSize": "1000",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(INTERVAL_TYPE="1")(MUTUAL_TYPE="001")(TRADE_DATE>='{start_date}')(TRADE_DATE<='{end_date}')""",
            "reportName": "RPT_MUTUAL_STOCK_NORTHSTA",
        }
        if start_date == end_date:
            params.update(
                {
                    "filter": f"""(INTERVAL_TYPE="1")(MUTUAL_TYPE="001")(TRADE_DATE='{start_date}')"""
                }
            )
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, int(total_page) + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        big_df.columns = [
            "-",
            "-",
            "持股日期",
            "-",
            "股票简称",
            "-",
            "-",
            "股票代码",
            "-",
            "-",
            "-",
            "-",
            "持股数量",
            "持股市值",
            "-",
            "持股数量占发行股百分比",
            "当日收盘价",
            "当日涨跌幅",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "-",
            "-",
        ]
        big_df = big_df[
            [
                "持股日期",
                "股票代码",
                "股票简称",
                "当日收盘价",
                "当日涨跌幅",
                "持股数量",
                "持股市值",
                "持股数量占发行股百分比",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["当日收盘价"] = pd.to_numeric(big_df["当日收盘价"])
        big_df["当日涨跌幅"] = pd.to_numeric(big_df["当日涨跌幅"])
        big_df["持股数量"] = pd.to_numeric(big_df["持股数量"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股数量占发行股百分比"] = pd.to_numeric(big_df["持股数量占发行股百分比"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
    elif symbol == "深股通持股":
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "pageSize": "1000",
            "pageNumber": "1",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(INTERVAL_TYPE="1")(MUTUAL_TYPE="003")(TRADE_DATE>='{start_date}')(TRADE_DATE<='{end_date}')""",
            "reportName": "RPT_MUTUAL_STOCK_NORTHSTA",
        }
        if start_date == end_date:
            params.update(
                {
                    "filter": f"""(INTERVAL_TYPE="1")(MUTUAL_TYPE="003")(TRADE_DATE='{start_date}')"""
                }
            )
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, int(total_page) + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        big_df.columns = [
            "-",
            "-",
            "持股日期",
            "-",
            "股票简称",
            "-",
            "-",
            "股票代码",
            "-",
            "-",
            "-",
            "-",
            "持股数量",
            "持股市值",
            "-",
            "持股数量占发行股百分比",
            "当日收盘价",
            "当日涨跌幅",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "-",
            "-",
        ]
        big_df = big_df[
            [
                "持股日期",
                "股票代码",
                "股票简称",
                "当日收盘价",
                "当日涨跌幅",
                "持股数量",
                "持股市值",
                "持股数量占发行股百分比",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["当日收盘价"] = pd.to_numeric(big_df["当日收盘价"])
        big_df["当日涨跌幅"] = pd.to_numeric(big_df["当日涨跌幅"])
        big_df["持股数量"] = pd.to_numeric(big_df["持股数量"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股数量占发行股百分比"] = pd.to_numeric(big_df["持股数量占发行股百分比"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
    return big_df


def stock_hsgt_institution_statistics_em(
    market: str = "北向持股",
    start_date: str = "20220601",
    end_date: str = "20220609",
):
    """
    东方财富网-数据中心-沪深港通-沪深港通持股-每日机构统计
    http://data.eastmoney.com/hsgtcg/InstitutionStatistics.aspx
    :param market: choice of {"北向持股", "南向持股", "沪股通持股", "深股通持股"}
    :type market: str
    :param start_date: 指定数据获取开始的时间, e.g., "20200713"
    :type start_date: str
    :param end_date: 指定数据获取结束的时间, e.g., "20200715"
    :type end_date:str
    :return: 指定市场和指定时间段的每日个股统计数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    if market == "南向持股":
        params = {
            "sortColumns": "HOLD_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": "1",
            "reportName": "PRT_MUTUAL_ORG_STA",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(MARKET_TYPE="S")(HOLD_DATE>='{start_date}')(HOLD_DATE<='{end_date}')""",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        temp_df.columns = [
            "持股日期",
            "_",
            "持股只数",
            "_",
            "持股市值",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "_",
            "机构名称",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
        temp_df = temp_df[
            [
                "持股日期",
                "机构名称",
                "持股只数",
                "持股市值",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        temp_df["持股日期"] = pd.to_datetime(temp_df["持股日期"]).dt.date
        temp_df["持股只数"] = pd.to_numeric(temp_df["持股只数"])
        temp_df["持股市值"] = pd.to_numeric(temp_df["持股市值"])
        temp_df["持股市值变化-1日"] = pd.to_numeric(temp_df["持股市值变化-1日"])
        temp_df["持股市值变化-5日"] = pd.to_numeric(temp_df["持股市值变化-5日"])
        temp_df["持股市值变化-10日"] = pd.to_numeric(temp_df["持股市值变化-10日"])
        return temp_df

    elif market == "北向持股":
        params = {
            "sortColumns": "HOLD_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": "1",
            "reportName": "PRT_MUTUAL_ORG_STA",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(MARKET_TYPE="N")(HOLD_DATE>='{start_date}')(HOLD_DATE<='{end_date}')""",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, total_page + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params, headers=headers)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        big_df.columns = [
            "持股日期",
            "_",
            "持股只数",
            "_",
            "持股市值",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "_",
            "机构名称",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
        big_df = big_df[
            [
                "持股日期",
                "机构名称",
                "持股只数",
                "持股市值",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["持股只数"] = pd.to_numeric(big_df["持股只数"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
        return big_df
    elif market == "沪股通持股":
        params = {
            "sortColumns": "HOLD_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": "1",
            "reportName": "PRT_MUTUAL_ORG_STA",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(MARKET_TYPE="001")(HOLD_DATE>='{start_date}')(HOLD_DATE<='{end_date}')""",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, total_page + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params, headers=headers)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        big_df.columns = [
            "持股日期",
            "_",
            "持股只数",
            "_",
            "持股市值",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "_",
            "机构名称",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
        big_df = big_df[
            [
                "持股日期",
                "机构名称",
                "持股只数",
                "持股市值",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["持股只数"] = pd.to_numeric(big_df["持股只数"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
        return big_df
    elif market == "深股通持股":
        params = {
            "sortColumns": "HOLD_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": "1",
            "reportName": "PRT_MUTUAL_ORG_STA",
            "columns": "ALL",
            "source": "WEB",
            "client": "WEB",
            "filter": f"""(MARKET_TYPE="003")(HOLD_DATE>='{start_date}')(HOLD_DATE<='{end_date}')""",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, total_page + 1), leave=False):
            params.update({"pageNumber": page})
            r = requests.get(url, params=params, headers=headers)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        big_df.columns = [
            "持股日期",
            "_",
            "持股只数",
            "_",
            "持股市值",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
            "_",
            "机构名称",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
        big_df = big_df[
            [
                "持股日期",
                "机构名称",
                "持股只数",
                "持股市值",
                "持股市值变化-1日",
                "持股市值变化-5日",
                "持股市值变化-10日",
            ]
        ]
        big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
        big_df["持股只数"] = pd.to_numeric(big_df["持股只数"])
        big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
        big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
        big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
        big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
        return big_df


def stock_hsgt_hist_em(symbol: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据
    http://data.eastmoney.com/hsgt/index.html
    :param symbol: choice of {"沪股通", "深股通", "港股通沪", "港股通深"}
    :type symbol: str
    :return: 沪深港通历史数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {"沪股通": "1", "深股通": "3", "港股通沪": "2", "港股通深": "4"}
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "TRADE_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_MUTUAL_DEAL_HISTORY",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f'(MUTUAL_TYPE="00{symbol_map[symbol]}")',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    if symbol == "沪股通":
        index_name = "上证指数"
    elif symbol == "深股通":
        index_name = "深证指数"
    else:
        index_name = "恒生指数"

    big_df.rename(
        columns={
            "MUTUAL_TYPE": "-",
            "TRADE_DATE": "日期",
            "FUND_INFLOW": "当日资金流入",
            "NET_DEAL_AMT": "当日成交净买额",
            "QUOTA_BALANCE": "当日余额",
            "ACCUM_DEAL_AMT": "历史累计净买额",
            "BUY_AMT": "买入成交额",
            "SELL_AMT": "卖出成交额",
            "LEAD_STOCKS_CODE": "-",
            "LEAD_STOCKS_NAME": "领涨股",
            "LS_CHANGE_RATE": "领涨股涨跌幅",
            "INDEX_CLOSE_PRICE": index_name,
            "INDEX_CHANGE_RATE": "涨跌幅",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "日期",
            "当日成交净买额",
            "买入成交额",
            "卖出成交额",
            "历史累计净买额",
            "当日资金流入",
            "当日余额",
            "领涨股",
            "领涨股涨跌幅",
            index_name,
            "涨跌幅",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["当日资金流入"] = pd.to_numeric(big_df["当日资金流入"]) / 100
    big_df["当日余额"] = pd.to_numeric(big_df["当日余额"]) / 100
    if symbol == "沪股通" or symbol == "深股通":
        big_df["历史累计净买额"] = pd.to_numeric(big_df["历史累计净买额"]) / 100
    else:
        big_df["历史累计净买额"] = pd.to_numeric(big_df["历史累计净买额"]) / 100 / 10000
    big_df["当日成交净买额"] = pd.to_numeric(big_df["当日成交净买额"]) / 100
    big_df["买入成交额"] = pd.to_numeric(big_df["买入成交额"]) / 100
    big_df["卖出成交额"] = pd.to_numeric(big_df["卖出成交额"]) / 100
    big_df["领涨股涨跌幅"] = pd.to_numeric(big_df["领涨股涨跌幅"])
    big_df[index_name] = pd.to_numeric(big_df[index_name])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    return big_df


def stock_hsgt_board_rank_em(
    symbol: str = "北向资金增持行业板块排行", indicator: str = "今日"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-行业板块排行-北向资金增持行业板块排行
    https://data.eastmoney.com/hsgtcg/hy.html
    :param symbol: choice of {"北向资金增持行业板块排行", "北向资金增持概念板块排行", "北向资金增持地域板块排行"}
    :type symbol: str
    :param indicator: choice of {"今日", "3日", "5日", "10日", "1月", "1季", "1年"}
    :type indicator: str
    :return: 北向资金增持行业板块排行
    :rtype: pandas.DataFrame
    """
    url = "https://data.eastmoney.com/hsgtcg/hy.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    current_date = (
        soup.find(attrs={"id": "bkph_date"}).text.strip("（").strip("）")
    )
    symbol_map = {
        "北向资金增持行业板块排行": "5",
        "北向资金增持概念板块排行": "4",
        "北向资金增持地域板块排行": "3",
    }
    indicator_map = {
        "今日": "1",
        "3日": "3",
        "5日": "5",
        "10日": "10",
        "1月": "M",
        "1季": "Q",
        "1年": "Y",
    }
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "ADD_MARKET_CAP",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_MUTUAL_BOARD_HOLDRANK_WEB",
        "columns": "ALL",
        "quoteColumns": "f3~05~SECURITY_CODE~INDEX_CHANGE_RATIO",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(BOARD_TYPE="{symbol_map[symbol]}")(TRADE_DATE='{current_date}')(INTERVAL_TYPE="{indicator_map[indicator]}")""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "_",
        "_",
        "名称",
        "_",
        "最新涨跌幅",
        "报告时间",
        "_",
        "_",
        "北向资金今日增持估计-股票只数",
        "北向资金今日持股-股票只数",
        "北向资金今日增持估计-市值",
        "北向资金今日增持估计-市值增幅",
        "-",
        "北向资金今日增持估计-占板块比",
        "北向资金今日增持估计-占北向资金比",
        "北向资金今日持股-市值",
        "北向资金今日持股-占北向资金比",
        "北向资金今日持股-占板块比",
        "_",
        "_",
        "今日增持最大股-市值",
        "_",
        "_",
        "今日减持最大股-市值",
        "今日增持最大股-占总市值比",
        "_",
        "_",
        "今日减持最大股-占总市值比",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "名称",
            "最新涨跌幅",
            "北向资金今日持股-股票只数",
            "北向资金今日持股-市值",
            "北向资金今日持股-占板块比",
            "北向资金今日持股-占北向资金比",
            "北向资金今日增持估计-股票只数",
            "北向资金今日增持估计-市值",
            "北向资金今日增持估计-市值增幅",
            "北向资金今日增持估计-占板块比",
            "北向资金今日增持估计-占北向资金比",
            "今日增持最大股-市值",
            "今日增持最大股-占总市值比",
            "今日减持最大股-市值",
            "今日减持最大股-占总市值比",
            "报告时间",
        ]
    ]
    temp_df["最新涨跌幅"] = pd.to_numeric(temp_df["最新涨跌幅"])
    temp_df["北向资金今日持股-股票只数"] = pd.to_numeric(temp_df["北向资金今日持股-股票只数"])
    temp_df["北向资金今日持股-市值"] = pd.to_numeric(temp_df["北向资金今日持股-市值"])
    temp_df["北向资金今日持股-占板块比"] = pd.to_numeric(temp_df["北向资金今日持股-占板块比"])
    temp_df["北向资金今日持股-占北向资金比"] = pd.to_numeric(temp_df["北向资金今日持股-占北向资金比"])
    temp_df["北向资金今日增持估计-股票只数"] = pd.to_numeric(temp_df["北向资金今日增持估计-股票只数"])
    temp_df["北向资金今日增持估计-市值"] = pd.to_numeric(temp_df["北向资金今日增持估计-市值"])
    temp_df["北向资金今日增持估计-市值增幅"] = pd.to_numeric(temp_df["北向资金今日增持估计-市值增幅"])
    temp_df["北向资金今日增持估计-占板块比"] = pd.to_numeric(temp_df["北向资金今日增持估计-占板块比"])
    temp_df["北向资金今日增持估计-占北向资金比"] = pd.to_numeric(temp_df["北向资金今日增持估计-占北向资金比"])
    temp_df["报告时间"] = pd.to_datetime(temp_df["报告时间"]).dt.date
    return temp_df


def stock_hsgt_individual_em(stock: str = "002008") -> pd.DataFrame:
    """
    东方财富-数据中心-沪深港通-沪深港通持股-具体股票
    https://data.eastmoney.com/hsgtcg/StockHdStatistics/002008.html
    :param stock: 股票代码
    :type stock: str
    :return: 具体股票-沪深港通持股
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "TRADE_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_MUTUAL_HOLDSTOCKNORTH_STA",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(SECURITY_CODE="{stock}")(TRADE_DATE>='2020-07-25')""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.rename(
        columns={
            "SECURITY_INNER_CODE": "-",
            "SECUCODE": "-",
            "TRADE_DATE": "持股日期",
            "SECURITY_CODE": "-",
            "SECURITY_NAME": "-",
            "MUTUAL_TYPE": "-",
            "CHANGE_RATE": "当日涨跌幅",
            "CLOSE_PRICE": "当日收盘价",
            "HOLD_SHARES": "持股数量",
            "HOLD_MARKET_CAP": "持股市值",
            "A_SHARES_RATIO": "-",
            "HOLD_SHARES_RATIO": "持股数量占A股百分比",
            "FREE_SHARES_RATIO": "-",
            "TOTAL_SHARES_RATIO": "-",
            "HOLD_MARKETCAP_CHG1": "持股市值变化-1日",
            "HOLD_MARKETCAP_CHG5": "持股市值变化-5日",
            "HOLD_MARKETCAP_CHG10": "持股市值变化-10日",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "持股日期",
            "当日收盘价",
            "当日涨跌幅",
            "持股数量",
            "持股市值",
            "持股数量占A股百分比",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
        ]
    ]
    temp_df["持股日期"] = pd.to_datetime(temp_df["持股日期"]).dt.date
    temp_df["当日收盘价"] = pd.to_numeric(temp_df["当日收盘价"])
    temp_df["当日涨跌幅"] = pd.to_numeric(temp_df["当日涨跌幅"])
    temp_df["持股数量"] = pd.to_numeric(temp_df["持股数量"])
    temp_df["持股市值"] = pd.to_numeric(temp_df["持股市值"])
    temp_df["持股数量占A股百分比"] = pd.to_numeric(temp_df["持股数量占A股百分比"])
    temp_df["持股市值变化-1日"] = pd.to_numeric(temp_df["持股市值变化-1日"])
    temp_df["持股市值变化-5日"] = pd.to_numeric(temp_df["持股市值变化-5日"])
    temp_df["持股市值变化-10日"] = pd.to_numeric(temp_df["持股市值变化-10日"])
    return temp_df


def stock_hsgt_individual_detail_em(
    symbol: str = "002008",
    start_date: str = "20220130",
    end_date: str = "20220330",
) -> pd.DataFrame:
    """
    东方财富-数据中心-沪深港通-沪深港通持股-具体股票详情
    https://data.eastmoney.com/hsgtcg/StockHdStatistics/002008.html
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 沪深港通持股-具体股票详情
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "HOLD_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_MUTUAL_HOLD_DET",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(SECURITY_CODE="{symbol}")(MARKET_CODE="003")(HOLD_DATE>='{'-'.join([start_date[:4], start_date[4:6], start_date[6:]])}')(HOLD_DATE<='{'-'.join([end_date[:4], end_date[4:6], end_date[6:]])}')""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    try:
        data_json["result"]["pages"]
    except TypeError as e:
        params.update(
            {
                "filter": f"""(SECURITY_CODE="{symbol}")(MARKET_CODE="001")(HOLD_DATE>='{'-'.join([start_date[:4], start_date[4:6], start_date[6:]])}')(HOLD_DATE<='{'-'.join([end_date[:4], end_date[4:6], end_date[6:]])}')""",
            }
        )
        r = requests.get(url, params=params)
        data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.rename(
        columns={
            "SECUCODE": "-",
            "SECURITY_CODE": "-",
            "SECURITY_INNER_CODE": "-",
            "SECURITY_NAME_ABBR": "-",
            "HOLD_DATE": "持股日期",
            "ORG_CODE": "-",
            "ORG_NAME": "机构名称",
            "HOLD_NUM": "持股数量",
            "MARKET_CODE": "-",
            "HOLD_SHARES_RATIO": "持股数量占A股百分比",
            "HOLD_MARKET_CAP": "持股市值",
            "CLOSE_PRICE": "当日收盘价",
            "CHANGE_RATE": "当日涨跌幅",
            "HOLD_MARKET_CAPONE": "持股市值变化-1日",
            "HOLD_MARKET_CAPFIVE": "持股市值变化-5日",
            "HOLD_MARKET_CAPTEN": "持股市值变化-10日",
            "PARTICIPANT_CODE": "-",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "持股日期",
            "当日收盘价",
            "当日涨跌幅",
            "机构名称",
            "持股数量",
            "持股市值",
            "持股数量占A股百分比",
            "持股市值变化-1日",
            "持股市值变化-5日",
            "持股市值变化-10日",
        ]
    ]
    big_df["持股日期"] = pd.to_datetime(big_df["持股日期"]).dt.date
    big_df["当日收盘价"] = pd.to_numeric(big_df["当日收盘价"])
    big_df["当日涨跌幅"] = pd.to_numeric(big_df["当日涨跌幅"])
    big_df["持股数量"] = pd.to_numeric(big_df["持股数量"])
    big_df["持股市值"] = pd.to_numeric(big_df["持股市值"])
    big_df["持股数量占A股百分比"] = pd.to_numeric(big_df["持股数量占A股百分比"])
    big_df["持股市值变化-1日"] = pd.to_numeric(big_df["持股市值变化-1日"])
    big_df["持股市值变化-5日"] = pd.to_numeric(big_df["持股市值变化-5日"])
    big_df["持股市值变化-10日"] = pd.to_numeric(big_df["持股市值变化-10日"])
    return big_df


if __name__ == "__main__":
    stock_hsgt_fund_flow_summary_em_df = stock_hsgt_fund_flow_summary_em()
    print(stock_hsgt_fund_flow_summary_em_df)

    stock_hk_ggt_components_em_df = stock_hk_ggt_components_em()
    print(stock_hk_ggt_components_em_df)

    stock_hsgt_north_net_flow_in_em_df = stock_hsgt_north_net_flow_in_em(
        symbol="沪股通"
    )
    print(stock_hsgt_north_net_flow_in_em_df)

    stock_hsgt_north_net_flow_in_em_df = stock_hsgt_north_net_flow_in_em(
        symbol="深股通"
    )
    print(stock_hsgt_north_net_flow_in_em_df)

    stock_hsgt_north_net_flow_in_em_df = stock_hsgt_north_net_flow_in_em(
        symbol="北上"
    )
    print(stock_hsgt_north_net_flow_in_em_df)

    stock_hsgt_north_cash_em_df = stock_hsgt_north_cash_em(symbol="沪股通")
    print(stock_hsgt_north_cash_em_df)

    stock_hsgt_north_acc_flow_in_em_df = stock_hsgt_north_acc_flow_in_em(
        symbol="北上"
    )
    print(stock_hsgt_north_acc_flow_in_em_df)

    stock_hsgt_south_net_flow_in_em_df = stock_hsgt_south_net_flow_in_em(
        symbol="沪股通"
    )
    print(stock_hsgt_south_net_flow_in_em_df)

    stock_hsgt_south_cash_em_df = stock_hsgt_south_cash_em(symbol="沪股通")
    print(stock_hsgt_south_cash_em_df)

    stock_hsgt_south_acc_flow_in_em_df = stock_hsgt_south_acc_flow_in_em(
        symbol="沪股通"
    )
    print(stock_hsgt_south_acc_flow_in_em_df)

    stock_hsgt_hold_stock_em_df = stock_hsgt_hold_stock_em(
        market="北向", indicator="今日排行"
    )
    print(stock_hsgt_hold_stock_em_df)

    stock_hsgt_hold_stock_em_df = stock_hsgt_hold_stock_em(
        market="沪股通", indicator="5日排行"
    )
    print(stock_hsgt_hold_stock_em_df)

    stock_hsgt_hold_stock_em_df = stock_hsgt_hold_stock_em(
        market="深股通", indicator="5日排行"
    )
    print(stock_hsgt_hold_stock_em_df)

    stock_hsgt_hold_stock_em_df = stock_hsgt_hold_stock_em(
        market="沪股通", indicator="10日排行"
    )
    print(stock_hsgt_hold_stock_em_df)

    stock_hsgt_stock_statistics_em_df = stock_hsgt_stock_statistics_em(
        symbol="北向持股", start_date="20230901", end_date="20230930"
    )
    print(stock_hsgt_stock_statistics_em_df)

    stock_hsgt_stock_statistics_em_df = stock_hsgt_stock_statistics_em(
        symbol="南向持股", start_date="20220601", end_date="20220615"
    )
    print(stock_hsgt_stock_statistics_em_df)

    stock_hsgt_stock_statistics_em_df = stock_hsgt_stock_statistics_em(
        symbol="沪股通持股", start_date="20220601", end_date="20220609"
    )
    print(stock_hsgt_stock_statistics_em_df)

    stock_hsgt_stock_statistics_em_df = stock_hsgt_stock_statistics_em(
        symbol="深股通持股", start_date="20220601", end_date="20220609"
    )
    print(stock_hsgt_stock_statistics_em_df)

    stock_hsgt_institution_statistics_em_df = (
        stock_hsgt_institution_statistics_em(
            market="北向持股", start_date="20220601", end_date="20220609"
        )
    )
    print(stock_hsgt_institution_statistics_em_df)

    stock_hsgt_institution_statistics_em_df = (
        stock_hsgt_institution_statistics_em(
            market="南向持股", start_date="20220601", end_date="20220609"
        )
    )
    print(stock_hsgt_institution_statistics_em_df)

    stock_hsgt_institution_statistics_em_df = (
        stock_hsgt_institution_statistics_em(
            market="沪股通持股", start_date="20220601", end_date="20220609"
        )
    )
    print(stock_hsgt_institution_statistics_em_df)

    stock_hsgt_institution_statistics_em_df = (
        stock_hsgt_institution_statistics_em(
            market="深股通持股", start_date="20220601", end_date="20220609"
        )
    )
    print(stock_hsgt_institution_statistics_em_df)

    stock_hsgt_hist_em_df = stock_hsgt_hist_em(symbol="港股通沪")
    print(stock_hsgt_hist_em_df)

    stock_hsgt_board_rank_em_df = stock_hsgt_board_rank_em(
        symbol="北向资金增持行业板块排行", indicator="今日"
    )
    print(stock_hsgt_board_rank_em_df)

    stock_hsgt_individual_em_df = stock_hsgt_individual_em(stock="002008")
    print(stock_hsgt_individual_em_df)

    stock_hsgt_individual_detail_em_df = stock_hsgt_individual_detail_em(
        symbol="002008", start_date="20220601", end_date="20220609"
    )
    print(stock_hsgt_individual_detail_em_df)
