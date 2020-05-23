# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/3/23 19:12
Desc: 东方财富网-数据中心-沪深港通持股
http://data.eastmoney.com/hsgtcg/
http://finance.eastmoney.com/news/1622,20161118685370149.html
"""
import requests
import json
import demjson
import pandas as pd
from bs4 import BeautifulSoup


def stock_em_hsgt_north_net_flow_in(indicator="沪股通"):
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


def stock_em_hsgt_north_cash(indicator="沪股通"):
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


def stock_em_hsgt_north_acc_flow_in(indicator="沪股通"):
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


def stock_em_hsgt_south_net_flow_in(indicator="沪股通"):
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


def stock_em_hsgt_south_cash(indicator="沪股通"):
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


def stock_em_hsgt_south_acc_flow_in(indicator="沪股通"):
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


def stock_em_hsgt_hold_stock(market="沪股通", indicator="年排行"):
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

    stock_em_hsgt_hold_stock_df = stock_em_hsgt_hold_stock(market="北向", indicator="今日排行")
    print(stock_em_hsgt_hold_stock_df.columns)
