# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
Date: 2020/3/23 19:12
Contact: jindaxiang@163.com
Desc: 东方财富网-数据中心-沪深港通持股
http://data.eastmoney.com/hsgtcg/
"""
import requests
import json
import pandas as pd


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
    if indicator == "北上":
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
    if indicator == "北上":
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
    if indicator == "北上":
        temp_df = pd.DataFrame(data_json["data"]["n2s"]).iloc[:, 0].str.split(",", expand=True)
        temp_df.columns = ["date", "value"]
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
