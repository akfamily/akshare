# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/15 19:12
Desc: 东方财富网-数据中心-沪深港通持股
http://data.eastmoney.com/hsgtcg/
沪深港通详情: http://finance.eastmoney.com/news/1622,20161118685370149.html
"""
import json

import demjson
import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_em_hsgt_north_net_flow_in(indicator: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-净流入
    http://data.eastmoney.com/hsgtcg/
    :param indicator: choice of {"沪股通", "深股通", "北上"}
    :type indicator: str
    :return: 东方财富网-数据中心-沪深港通持股-净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f52",
        "klt": "101",
        "lmt": "500",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):-2])
    if indicator == "沪股通":
        temp_df = pd.DataFrame(data_json["data"]["hk2sh"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "深股通":
        temp_df = pd.DataFrame(data_json["data"]["hk2sz"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "北上":
        temp_df = pd.DataFrame(data_json["data"]["s2n"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df


def stock_em_hsgt_north_cash(indicator: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-资金余额
    http://data.eastmoney.com/hsgtcg/
    :param indicator: choice of {"沪股通", "深股通", "北上"}
    :type indicator: str
    :return: 东方财富网-数据中心-沪深港通持股-资金余额
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f53",
        "klt": "101",
        "lmt": "500",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):-2])
    if indicator == "沪股通":
        temp_df = pd.DataFrame(data_json["data"]["hk2sh"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "深股通":
        temp_df = pd.DataFrame(data_json["data"]["hk2sz"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "北上":
        temp_df = pd.DataFrame(data_json["data"]["s2n"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df


def stock_em_hsgt_north_acc_flow_in(indicator: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-累计净流入
    http://data.eastmoney.com/hsgtcg/
    :param indicator: choice of {"沪股通", "深股通", "北上"}
    :type indicator: str
    :return: 东方财富网-数据中心-沪深港通持股-累计净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f1,f3,f5",
        "fields2": "f51,f54",
        "klt": "101",
        "lmt": "500",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18305732402561585701_1584961751919",
        "_": "1584962164273",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):-2])
    if indicator == "沪股通":
        temp_df = pd.DataFrame(data_json["data"]["hk2sh"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "深股通":
        temp_df = pd.DataFrame(data_json["data"]["hk2sz"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "北上":
        temp_df = pd.DataFrame(data_json["data"]["s2n"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df


def stock_em_hsgt_south_net_flow_in(indicator: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-南向概括-净流入
    http://data.eastmoney.com/hsgtcg/
    :param indicator: choice of {"沪股通", "深股通", "南下"}
    :type indicator: str
    :return: 东方财富网-数据中心-沪深港通持股-南向概括-净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f2,f4,f6",
        "fields2": "f51,f52",
        "klt": "101",
        "lmt": "500",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18307854355493858363_1584963487410",
        "_": "1584964176697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):-2])
    if indicator == "沪股通":
        temp_df = pd.DataFrame(data_json["data"]["sh2hk"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "深股通":
        temp_df = pd.DataFrame(data_json["data"]["sz2hk"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "南下":
        temp_df = pd.DataFrame(data_json["data"]["n2s"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df


def stock_em_hsgt_south_cash(indicator: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-南向概括-资金余额
    http://data.eastmoney.com/hsgtcg/
    :param indicator: choice of {"沪股通", "深股通", "南下"}
    :type indicator: str
    :return: 东方财富网-数据中心-沪深港通持股-南向概括-资金余额
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f2,f4,f6",
        "fields2": "f51,f53",
        "klt": "101",
        "lmt": "500",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18307854355493858363_1584963487410",
        "_": "1584964176697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):-2])
    if indicator == "沪股通":
        temp_df = pd.DataFrame(data_json["data"]["sh2hk"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "深股通":
        temp_df = pd.DataFrame(data_json["data"]["sz2hk"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "南下":
        temp_df = pd.DataFrame(data_json["data"]["n2s"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df


def stock_em_hsgt_south_acc_flow_in(indicator: str = "沪股通") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-南向概括-累计净流入
    http://data.eastmoney.com/hsgtcg/
    :param indicator: choice of {"沪股通", "深股通", "南下"}
    :type indicator: str
    :return: 东方财富网-数据中心-沪深港通持股-南向概括-累计净流入
    :rtype: pandas.DataFrame
    """
    url = "http://push2his.eastmoney.com/api/qt/kamt.kline/get"
    params = {
        "fields1": "f2,f4,f6",
        "fields2": "f51,f54",
        "klt": "101",
        "lmt": "500",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery18307854355493858363_1584963487410",
        "_": "1584964176697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):-2])
    if indicator == "沪股通":
        temp_df = pd.DataFrame(data_json["data"]["sh2hk"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "深股通":
        temp_df = pd.DataFrame(data_json["data"]["sz2hk"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df
    if indicator == "南下":
        temp_df = pd.DataFrame(data_json["data"]["n2s"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
        return temp_df


def stock_em_hsgt_hold_stock(market: str = "沪股通", indicator: str = "年排行") -> pd.DataFrame:
    """
    东方财富网-数据中心-沪深港通持股-个股排行
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
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    date = soup.find(attrs={"class": "tit"}).find("span").text.strip("（").strip("）")
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    if indicator == "今日排行":
        indicator_type = "1"
    if indicator == "3日排行":
        indicator_type = "3"
    if indicator == "5日排行":
        indicator_type = "5"
    if indicator == "10日排行":
        indicator_type = "5"
    if indicator == "月排行":
        indicator_type = "m"
    if indicator == "季排行":
        indicator_type = "jd"
    if indicator == "年排行":
        indicator_type = "y"
    if market == "北向":
        filter_str = "(DateType='" + indicator_type + "' and HdDate='" + f"{date}')"
    elif market == "沪股通":
        filter_str = "(Market='001' and DateType='" + indicator_type + "' and HdDate='" + f"{date}')"
    elif market == "深股通":
        filter_str = "(Market='003' and DateType='" + indicator_type + "' and HdDate='" + f"{date}')"
    params = {
        "type": "HSGT20_GGTJ_SUM",
        "token": "894050c76af8597a853f5b408b759f5d",
        "st": "ShareSZ_Chg_One",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var orksULCQ={pages:(tp),data:(x)}",
        "filter": filter_str,
        "rt": "53001697",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    return pd.DataFrame(data_json["data"])


def stock_em_hsgt_stock_statistics(market="南向持股", start_date="20200713", end_date="20200714"):
    """
    东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计
    http://data.eastmoney.com/hsgtcg/StockStatistics.aspx
    market=001, 沪股通持股
    market=003, 深股通持股
    :param market: choice of {"北向持股", "南向持股"}
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
            "type": "HSGTHDSTA",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "st": "HDDATE,SHAREHOLDPRICE",
            "sr": "3",
            "p": "1",
            "ps": "10000",
            "js": "var AxDXinef={pages:(tp),data:(x)}",
            "filter": f"(MARKET='S')(HDDATE>=^{start_date}^ and HDDATE<=^{end_date}^)",
            "rt": "53160469",
        }
    elif market == "北向持股":
        params = {
            "type": "HSGTHDSTA",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "st": "HDDATE,SHAREHOLDPRICE",
            "sr": "3",
            "p": "1",
            "ps": "10000",
            "js": "var AxDXinef={pages:(tp),data:(x)}",
            "filter": f"(MARKET in ('001','003'))(HDDATE>=^{start_date}^ and HDDATE<=^{end_date}^)",
            "rt": "53160469",
        }

    url = "http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get"
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df


def stock_em_hsgt_institution_statistics(market="北向持股", start_date="20200713", end_date="20200714"):
    """
    东方财富网-数据中心-沪深港通-沪深港通持股-每日机构统计
    http://data.eastmoney.com/hsgtcg/InstitutionStatistics.aspx
    market=001, 沪股通持股
    market=003, 深股通持股
    :param market: choice of {"北向持股", "南向持股"}
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
            "type": "HSGTCOMSTA",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "st": "HDDATE,SHAREHOLDCOUNT",
            "sr": "3",
            "p": "1",
            "ps": "5000",
            "js": "var gvfJjbLz={pages:(tp),data:(x)}",
            "filter": f"(MARKET in ('001','003'))(HDDATE>=^{start_date}^ and HDDATE<=^{end_date}^)",
            "rt": "53160469",
        }
    elif market == "北向持股":
        params = {
            "type": "HSGTCOMSTA",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "st": "HDDATE,SHAREHOLDCOUNT",
            "sr": "3",
            "p": "1",
            "ps": "5000",
            "js": "var gvfJjbLz={pages:(tp),data:(x)}",
            "filter": f"(MARKET in ('001','003'))(HDDATE>=^{start_date}^ and HDDATE<=^{end_date}^)",
            "rt": "53160469",
        }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    url = "http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get"
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df


def stock_em_hsgt_hist(symbol: str = "港股通沪") -> pd.DataFrame:
    """
    东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据
    http://data.eastmoney.com/hsgt/index.html
    :param symbol: choice of {"沪股通", "深股通", "港股通沪", "港股通深"}
    :type symbol: str
    :return: 沪深港通历史数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {"沪股通": "1", "深股通": "3", "港股通沪": "2", "港股通深": "4"}
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "HSGTHIS",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "filter": f"(MarketType={symbol_map[symbol]})",
        "js": 'var VIIlLPMH={"data":(x),"pages":(tp)}',
        "ps": "2000",
        "p": "1",
        "sr": "-1",
        "st": "DetailDate",
        "rt": "53231355",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.columns = ["_",
                       "日期",
                       "当日资金流入",
                       "当日余额",
                       "历史资金累计流入",
                       "当日成交净买额",
                       "买入成交额",
                       "卖出成交额",
                       "_",
                       "领涨股",
                       "领涨股涨跌幅",
                       "对应指数",
                       "涨跌幅",
                       ]
    temp_df = temp_df[[
                       "日期",
                       "当日资金流入",
                       "当日余额",
                       "历史资金累计流入",
                       "当日成交净买额",
                       "买入成交额",
                       "卖出成交额",
                       "领涨股",
                       "领涨股涨跌幅",
                       "对应指数",
                       "涨跌幅",
                       ]]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"])
    return temp_df


if __name__ == '__main__':
    stock_em_hsgt_north_net_flow_in_df = stock_em_hsgt_north_net_flow_in(indicator="沪股通")
    print(stock_em_hsgt_north_net_flow_in_df)
    stock_em_hsgt_north_cash_df = stock_em_hsgt_north_cash(indicator="沪股通")
    print(stock_em_hsgt_north_cash_df)
    stock_em_hsgt_north_acc_flow_in_df = stock_em_hsgt_north_acc_flow_in(indicator="沪股通")
    print(stock_em_hsgt_north_acc_flow_in_df)
    stock_em_hsgt_south_net_flow_in_df = stock_em_hsgt_south_net_flow_in(indicator="沪股通")
    print(stock_em_hsgt_south_net_flow_in_df)
    stock_em_hsgt_south_cash_df = stock_em_hsgt_south_cash(indicator="沪股通")
    print(stock_em_hsgt_south_cash_df)
    stock_em_hsgt_south_acc_flow_in_df = stock_em_hsgt_south_acc_flow_in(indicator="沪股通")
    print(stock_em_hsgt_south_acc_flow_in_df)

    stock_em_hsgt_hold_stock_df = stock_em_hsgt_hold_stock(market="沪股通", indicator="10日排行")
    print(stock_em_hsgt_hold_stock_df)

    stock_em_hsgt_stock_statistics_df = stock_em_hsgt_stock_statistics(market="南向持股", start_date="20200922", end_date="20200922")
    print(stock_em_hsgt_stock_statistics_df)

    stock_em_hsgt_institution_statistics_df = stock_em_hsgt_institution_statistics(market="北向持股", start_date="20200913", end_date="20200914")
    print(stock_em_hsgt_institution_statistics_df)

    stock_em_hsgt_hist_df = stock_em_hsgt_hist(symbol="港股通沪")
    print(stock_em_hsgt_hist_df)
