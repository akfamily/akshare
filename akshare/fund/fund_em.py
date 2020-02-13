# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/2/5 22:48
contact: jindaxiang@163.com
desc: 东方财富网站-天天基金网-基金数据
http://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn20;pi1;scabbname;stasc

1.基金经理基本数据,建议包含:基金经理代码,基金经理姓名,从业起始日期,现任基金公司,管理资产总规模,上述数据可在"基金经理列表http://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn20;pi1;scabbname;stasc 和"基金经理理档案如:http://fund.eastmoney.com/manager/30040164.html 获取.

2.基金经理任职数据:可调取全部或特定经理,管理的基金数据,建议包含:基金经理代码,基金经理姓名,基金代码,基金简称,经理位次(在当前基金的经理中排第几位),起始任职时间,截止任职时间,任职回报.在特定基金的经理信息中可以获取如:http://fundf10.eastmoney.com/jjjl_001810.html

3.在接口：fund_basic"公募基金列表"增加数据"基金经理代码"(或第一基金经理代码),"基金经理姓名"(或第一基金经理姓名),"当前基金经理人数","当前经理任职起始时间".
用户ID:269993
"""
import demjson
import pandas as pd
import requests


def fund_em_daily():
    """
    东方财富网站-天天基金网-基金数据-开放式基金净值
    :return:
    :rtype:
    """
    url = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx"
    params = {
        "t": "1",
        "lx": "1",
        "letter": "",
        "gsid": "",
        "text": "",
        "sort": "zdf,desc",
        "page": "2,10000",
        "dt": "1580914040623",
        "atfc": "",
        "onlySale": "0",
    }
    res = requests.get(url, params=params)
    text = res.text
    data_json = demjson.decode(text.strip("var db="))
    return pd.DataFrame(data_json["datas"])


def fund_em_info(fund="710001", indicator="单位净值走势"):
    """

    :param fund:
    :type fund:
    :param indicator:
    :type indicator:
    :return:
    :rtype:
    """
    # url = f"http://fundgz.1234567.com.cn/js/{fund}.js"  # 描述信息
    url = f"http://fund.eastmoney.com/pingzhongdata/{fund}.js"  # 各类数据都在里面
    res = requests.get(url)
    text = res.text
    # 单位净值走势
    if indicator == "单位净值走势":
        data_json = demjson.decode(text[text.find("Data_netWorthTrend") + 21: text.find("Data_ACWorthTrend")-15])
        temp_df = pd.DataFrame(data_json)
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms")
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 累计净值走势
    if indicator == "累计净值走势":
        data_json = demjson.decode(text[text.find("Data_ACWorthTrend") + 20: text.find("Data_grandTotal")-16])
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["x", "y"]
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms")
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 累计收益率走势
    if indicator == "累计收益率走势":
        data_json = demjson.decode(text[text.find("Data_grandTotal") + 18: text.find("Data_rateInSimilarType")-15])
        temp_df_main = pd.DataFrame(data_json[0]["data"])  # 本产品
        temp_df_mean = pd.DataFrame(data_json[1]["data"])  # 同类平均
        temp_df_hs = pd.DataFrame(data_json[2]["data"])  # 沪深300
        temp_df_main.columns = ["x", "y"]
        temp_df_main["x"] = pd.to_datetime(temp_df_main["x"], unit="ms")
        temp_df_main["x"] = temp_df_main["x"].dt.date
        return temp_df_main

    # 同类排名走势
    if indicator == "同类排名走势":
        data_json = demjson.decode(text[text.find("Data_rateInSimilarType") + 25: text.find("Data_rateInSimilarPersent")-16])
        temp_df = pd.DataFrame(data_json)
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms")
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 同类排名百分比
    if indicator == "同类排名百分比":
        data_json = demjson.decode(text[text.find("Data_rateInSimilarPersent") + 26: text.find("Data_fluctuationScale")-23])
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["x", "y"]
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms")
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df


if __name__ == '__main__':
    fund_em_daily_df = fund_em_daily()
    print(fund_em_daily_df)

    fund_em_info_net_df = fund_em_info(fund="710001", indicator="单位净值走势")
    print(fund_em_info_net_df)
    fund_em_info_net_acc_df = fund_em_info(fund="710001", indicator="累计净值走势")
    print(fund_em_info_net_acc_df)
    fund_em_info_acc_return_df = fund_em_info(fund="710001", indicator="累计收益率走势")
    print(fund_em_info_acc_return_df)
    fund_em_info_rank_df = fund_em_info(fund="710001", indicator="同类排名走势")
    print(fund_em_info_rank_df)
    fund_em_info_rank_per_df = fund_em_info(fund="710001", indicator="同类排名百分比")
    print(fund_em_info_rank_per_df)
