# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/5 22:48
Desc: 东方财富网站-天天基金网-基金数据-开放式基金净值
http://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn20;pi1;scabbname;stasc
# TODO 完善其他类型基金净值数据
1.基金经理基本数据, 建议包含:基金经理代码,基金经理姓名,从业起始日期,现任基金公司,管理资产总规模,上述数据可在"基金经理列表: http://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn20;pi1;scabbname;stasc 和"基金经理理档案如:http://fund.eastmoney.com/manager/30040164.html 获取.
2.基金经理任职数据:可调取全部或特定经理,管理的基金数据,建议包含:基金经理代码,基金经理姓名,基金代码,基金简称,经理位次(在当前基金的经理中排第几位),起始任职时间,截止任职时间,任职回报.在特定基金的经理信息中可以获取如:http://fundf10.eastmoney.com/jjjl_001810.html
3.在接口：fund_basic"公募基金列表"增加数据"基金经理代码"(或第一基金经理代码),"基金经理姓名"(或第一基金经理姓名),"当前基金经理人数","当前经理任职起始时间".
用户ID:269993
"""
import time
import json

import demjson
import pandas as pd
import requests


def fund_em_fund_name() -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-所有基金的名称和类型
    http://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn20;pi1;scabbname;stasc
    :return: 所有基金的名称和类型
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    res = requests.get(url, headers=headers)
    text_data = res.text
    data_json = demjson.decode(text_data.strip("var r = ")[:-1])
    temp_df = pd.DataFrame(data_json)
    temp_df.columns = ["基金代码", "拼音缩写", "基金简称", "基金类型", "拼音全称"]
    return temp_df


def fund_em_open_fund_daily() -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-开放式基金净值
    http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1
    :return: 当前交易日的所有开放式基金净值数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = f"http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx"
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
    res = requests.get(url, params=params, headers=headers)
    text_data = res.text
    data_json = demjson.decode(text_data.strip("var db="))
    temp_df = pd.DataFrame(data_json["datas"])
    show_day = data_json["showday"]
    temp_df.columns = [
        "基金代码",
        "基金简称",
        "-",
        f"{show_day[0]}-单位净值",
        f"{show_day[0]}-累计净值",
        f"{show_day[1]}-单位净值",
        f"{show_day[1]}-累计净值",
        "日增长值",
        "日增长率",
        "申购状态",
        "赎回状态",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "手续费",
        "-",
        "-",
        "-",
    ]
    data_df = temp_df[
        [
            "基金代码",
            "基金简称",
            f"{show_day[0]}-单位净值",
            f"{show_day[0]}-累计净值",
            f"{show_day[1]}-单位净值",
            f"{show_day[1]}-累计净值",
            "日增长值",
            "日增长率",
            "申购状态",
            "赎回状态",
            "手续费",
        ]
    ]
    return data_df


def fund_em_open_fund_info(
    fund: str = "710001", indicator: str = "单位净值走势"
) -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-开放式基金净值
    http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1
    :param fund: 基金代码, 可以通过调用 fund_em_open_fund_daily 获取所有开放式基金代码
    :type fund: str
    :param indicator: 需要获取的指标
    :type indicator: str
    :return: 指定基金指定指标的数据
    :rtype: pandas.DataFrame
    """
    # url = f"http://fundgz.1234567.com.cn/js/{fund}.js"  # 描述信息
    url = f"http://fund.eastmoney.com/pingzhongdata/{fund}.js"  # 各类数据都在里面
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    text = res.text

    # 单位净值走势
    if indicator == "单位净值走势":
        data_json = demjson.decode(
            text[
                text.find("Data_netWorthTrend")
                + 21 : text.find("Data_ACWorthTrend")
                - 15
            ]
        )
        temp_df = pd.DataFrame(data_json)
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms", utc=True).dt.tz_convert(
            "Asia/Shanghai"
        )
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 累计净值走势
    if indicator == "累计净值走势":
        data_json = demjson.decode(
            text[
                text.find("Data_ACWorthTrend") + 20 : text.find("Data_grandTotal") - 16
            ]
        )
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["x", "y"]
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms", utc=True).dt.tz_convert(
            "Asia/Shanghai"
        )
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 累计收益率走势
    if indicator == "累计收益率走势":
        data_json = demjson.decode(
            text[
                text.find("Data_grandTotal")
                + 18 : text.find("Data_rateInSimilarType")
                - 15
            ]
        )
        temp_df_main = pd.DataFrame(data_json[0]["data"])  # 本产品
        temp_df_mean = pd.DataFrame(data_json[1]["data"])  # 同类平均
        temp_df_hs = pd.DataFrame(data_json[2]["data"])  # 沪深300
        temp_df_main.columns = ["x", "y"]
        temp_df_main["x"] = pd.to_datetime(
            temp_df_main["x"], unit="ms", utc=True
        ).dt.tz_convert("Asia/Shanghai")
        temp_df_main["x"] = temp_df_main["x"].dt.date
        return temp_df_main

    # 同类排名走势
    if indicator == "同类排名走势":
        data_json = demjson.decode(
            text[
                text.find("Data_rateInSimilarType")
                + 25 : text.find("Data_rateInSimilarPersent")
                - 16
            ]
        )
        temp_df = pd.DataFrame(data_json)
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms", utc=True).dt.tz_convert(
            "Asia/Shanghai"
        )
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 同类排名百分比
    if indicator == "同类排名百分比":
        data_json = demjson.decode(
            text[
                text.find("Data_rateInSimilarPersent")
                + 26 : text.find("Data_fluctuationScale")
                - 23
            ]
        )
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["x", "y"]
        temp_df["x"] = pd.to_datetime(temp_df["x"], unit="ms", utc=True).dt.tz_convert(
            "Asia/Shanghai"
        )
        temp_df["x"] = temp_df["x"].dt.date
        return temp_df

    # 分红送配详情
    if indicator == "分红送配详情":
        url = f"http://fundf10.eastmoney.com/fhsp_{fund}.html"
        r = requests.get(url, headers=headers)
        return pd.read_html(r.text)[1]

    # 拆分详情
    if indicator == "拆分详情":
        url = f"http://fundf10.eastmoney.com/fhsp_{fund}.html"
        r = requests.get(url, headers=headers)
        return pd.read_html(r.text)[2]


def fund_em_money_fund_daily() -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-货币型基金收益
    http://fund.eastmoney.com/HBJJ_pjsyl.html
    :return: 当前交易日的所有货币型基金收益数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://fund.eastmoney.com/HBJJ_pjsyl.html"
    r = requests.get(url, headers=headers)
    r.encoding = "gb2312"
    show_day = pd.read_html(r.text)[1].iloc[0, 5:11].tolist()
    temp_df = pd.read_html(r.text)[1].iloc[1:, 2:]
    temp_df_columns = temp_df.iloc[0, :].tolist()[1:]
    temp_df = temp_df.iloc[1:, 1:]
    temp_df.columns = temp_df_columns
    temp_df["基金简称"] = temp_df["基金简称"].str.strip("基金吧档案")
    temp_df.columns = [
        "基金代码",
        "基金简称",
        f"{show_day[0]}-万份收益",
        f"{show_day[1]}-7日年化%",
        f"{show_day[2]}-单位净值",
        f"{show_day[3]}-万份收益",
        f"{show_day[4]}-7日年化%",
        f"{show_day[5]}-单位净值",
        "日涨幅",
        "成立日期",
        "基金经理",
        "手续费",
        "可购全部",
    ]
    return temp_df


def fund_em_money_fund_info(fund: str = "000009") -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-货币型基金收益-历史净值数据
    http://fundf10.eastmoney.com/jjjz_004186.html
    :param fund: 货币型基金代码, 可以通过 fund_em_money_fund_daily 来获取
    :type fund: str
    :return: 东方财富网站-天天基金网-基金数据-货币型基金收益-历史净值数据
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/f10/lsjz"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
    }
    params = {
        "callback": "jQuery18306461675574671744_1588245122574",
        "fundCode": fund,
        "pageIndex": "1",
        "pageSize": "10000",
        "startDate": "",
        "endDate": "",
        "_": round(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{") : -1])
    temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
    temp_df.columns = [
        "净值日期",
        "每万份收益",
        "7日年化收益率",
        "_",
        "_",
        "_",
        "_",
        "申购状态",
        "赎回状态",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[["净值日期", "每万份收益", "7日年化收益率", "申购状态", "赎回状态"]]
    return temp_df


def fund_em_financial_fund_daily() -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-理财型基金收益
    http://fund.eastmoney.com/lcjj.html#1_1__0__ljjz,desc_1_os1
    :return: 当前交易日的所有理财型基金收益
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/lcjj.html",
    }
    url = "http://api.fund.eastmoney.com/FundNetValue/GetLCJJJZ"
    params = {
        "letter": "",
        "jjgsid": "0",
        "searchtext": "",
        "sort": "ljjz,desc",
        "page": "1,100",
        "AttentionCodes": "",
        "cycle": "",
        "OnlySale": "1",
        "callback": "jQuery18306581512555641693_1588248310204",
        "_": "1588248310234",
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{") : -1])
    temp_df = pd.DataFrame(data_json["Data"]["List"])
    show_day = data_json["Data"]["showday"]
    data_df = temp_df[
        [
            "Id",
            "actualsyi",
            "cycle",
            "fcode",
            "kfr",
            "mui",
            "shortname",
            "syi",
            "zrmui",
            "zrsyi",
        ]
    ]
    data_df.columns = [
        "序号",
        "上一期年化收益率",
        "封闭期",
        "基金代码",
        "申购状态",
        f"{show_day[0]}-万份收益",
        "基金简称",
        f"{show_day[0]}-7日年华",
        f"{show_day[1]}-万份收益",
        f"{show_day[1]}-7日年华",
    ]
    data_df = data_df[
        [
            "序号",
            "基金代码",
            "基金简称",
            "上一期年化收益率",
            f"{show_day[0]}-万份收益",
            f"{show_day[0]}-7日年华",
            f"{show_day[1]}-万份收益",
            f"{show_day[1]}-7日年华",
            "封闭期",
            "申购状态",
        ]
    ]
    return data_df


def fund_em_financial_fund_info(fund: str = "000134") -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值数据
    http://fundf10.eastmoney.com/jjjz_000791.html
    :param fund: 理财型基金代码, 可以通过 fund_em_financial_fund_daily 来获取
    :type fund: str
    :return: 东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值数据
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/f10/lsjz"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
    }
    params = {
        "callback": "jQuery18307915911837995662_1588249228826",
        "fundCode": fund,
        "pageIndex": "1",
        "pageSize": "10000",
        "startDate": "",
        "endDate": "",
        "_": round(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{") : -1])
    temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
    temp_df.columns = [
        "净值日期",
        "每万份收益",
        "7日年化收益率",
        "_",
        "_",
        "_",
        "_",
        "申购状态",
        "赎回状态",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[["净值日期", "每万份收益", "7日年化收益率", "申购状态", "赎回状态"]]
    return temp_df


def fund_em_graded_fund_daily() -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-分级基金净值
    http://fund.eastmoney.com/fjjj.html#1_1__0__zdf,desc_1
    :return: 当前交易日的所有分级基金净值
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fjjj.html",
    }
    url = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx"
    params = {
        "t": "1",
        "lx": "9",
        "letter": "",
        "gsid": "0",
        "text": "",
        "sort": "zdf,desc",
        "page": "1,10000",
        "dt": "1580914040623",
        "atfc": "",
    }
    res = requests.get(url, params=params, headers=headers)
    text_data = res.text
    data_json = demjson.decode(text_data.strip("var db="))
    temp_df = pd.DataFrame(data_json["datas"])
    show_day = data_json["showday"]
    temp_df.columns = [
        "基金代码",
        "基金简称",
        "-",
        f"{show_day[0]}-单位净值",
        f"{show_day[0]}-累计净值",
        f"{show_day[1]}--单位净值",
        f"{show_day[1]}--累计净值",
        "日增长值",
        "日增长率",
        "市价",
        "折价率",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "手续费",
    ]
    data_df = temp_df[
        [
            "基金代码",
            "基金简称",
            f"{show_day[0]}-单位净值",
            f"{show_day[0]}-累计净值",
            f"{show_day[1]}--单位净值",
            f"{show_day[1]}--累计净值",
            "日增长值",
            "日增长率",
            "市价",
            "折价率",
            "手续费",
        ]
    ]
    return data_df


def fund_em_graded_fund_info(fund: str = "150232") -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-分级基金净值-历史净值明细
    http://fundf10.eastmoney.com/jjjz_150232.html
    :param fund: 分级基金代码, 可以通过 fund_em_money_fund_daily 来获取
    :type fund: str
    :return: 东方财富网站-天天基金网-基金数据-分级基金净值-历史净值明细
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/f10/lsjz"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
    }
    params = {
        "callback": "jQuery18309549480723031107_1588250168187",
        "fundCode": fund,
        "pageIndex": "1",
        "pageSize": "10000",
        "startDate": "",
        "endDate": "",
        "_": round(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{"): -1])
    temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
    temp_df.columns = [
        "净值日期",
        "单位净值",
        "累计净值",
        "_",
        "_",
        "_",
        "日增长率",
        "申购状态",
        "赎回状态",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[["净值日期", "单位净值", "累计净值", "日增长率", "申购状态", "赎回状态"]]
    return temp_df


def fund_em_etf_fund_daily() -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-场内交易基金
    http://fund.eastmoney.com/cnjy_dwjz.html
    :return: 当前交易日的所有场内交易基金数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://fund.eastmoney.com/cnjy_dwjz.html"
    r = requests.get(url, headers=headers)
    r.encoding = "gb2312"
    show_day = pd.read_html(r.text)[1].iloc[0, 6:10].tolist()
    temp_df = pd.read_html(r.text)[1].iloc[1:, 2:]
    temp_df_columns = temp_df.iloc[0, :].tolist()[1:]
    temp_df = temp_df.iloc[1:, 1:]
    temp_df.columns = temp_df_columns
    temp_df["基金简称"] = temp_df["基金简称"].str.strip("基金吧档案")
    temp_df.reset_index(inplace=True, drop=True)
    temp_df.columns = ['基金代码', '基金简称', '类型', f'{show_day[0]}-单位净值', f'{show_day[0]}-累计净值', f'{show_day[1]}-单位净值', f'{show_day[1]}-累计净值', '增长值', '增长率', '市价', '折价率']
    return temp_df


def fund_em_etf_fund_info(fund: str = "511280") -> pd.DataFrame:
    """
    东方财富网站-天天基金网-基金数据-场内交易基金-历史净值明细
    http://fundf10.eastmoney.com/jjjz_511280.html
    :param fund: 场内交易基金代码, 可以通过 fund_em_etf_fund_daily 来获取
    :type fund: str
    :return: 东方财富网站-天天基金网-基金数据-场内交易基金-历史净值明细
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/f10/lsjz"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"http://fundf10.eastmoney.com/jjjz_{fund}.html",
    }
    params = {
        "callback": "jQuery183023608994033331676_1588250653363",
        "fundCode": fund,
        "pageIndex": "1",
        "pageSize": "10000",
        "startDate": "",
        "endDate": "",
        "_": round(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{") : -1])
    temp_df = pd.DataFrame(data_json["Data"]["LSJZList"])
    temp_df.columns = [
        "净值日期",
        "单位净值",
        "累计净值",
        "_",
        "_",
        "_",
        "日增长率",
        "申购状态",
        "赎回状态",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[["净值日期", "单位净值", "累计净值", "日增长率", "申购状态", "赎回状态"]]
    return temp_df


def fund_em_value_estimation() -> pd.DataFrame:
    """
    东方财富网-数据中心-净值估算
    http://fund.eastmoney.com/fundguzhi.html
    :return: 近期净值估算数据
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/FundGuZhi/GetFundGZList"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fundguzhi.html",
    }
    params = {
        "type": "1",
        "sort": "3",
        "orderType": "desc",
        "canbuy": "0",
        "pageIndex": "1",
        "pageSize": "10000",
        "callback": "jQuery18306504687615774458_1589361322986",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{"): -1])
    temp_df = pd.DataFrame(json_data["Data"]["list"])
    value_day = json_data["Data"]["gzrq"]
    cal_day = json_data["Data"]["gxrq"]
    temp_df.columns = [
        "基金代码",
        "-",
        "-",
        "-",
        "-",
        "-",
        "基金类型",
        "-",
        "-",
        "-",
        "-",
        "估算日期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        f"{cal_day}-估算值",
        f"{cal_day}-估算增长率",
        "-",
        f"{value_day}-单位净值",
        "-",
        "-",
        "基金名称",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[[
        "基金代码",
        "基金类型",
        f"{cal_day}-估算值",
        f"{cal_day}-估算增长率",
        f"{value_day}-单位净值",
        "基金名称",
    ]]
    return temp_df


if __name__ == "__main__":
    fund_em_fund_name_df = fund_em_fund_name()
    print(fund_em_fund_name_df)
    fund_em_open_fund_daily_df = fund_em_open_fund_daily()
    print(fund_em_open_fund_daily_df)
    time.sleep(3)
    fund_em_info_net_df = fund_em_open_fund_info(fund="710001", indicator="单位净值走势")
    print(fund_em_info_net_df)
    time.sleep(3)
    fund_em_info_net_acc_df = fund_em_open_fund_info(fund="710001", indicator="累计净值走势")
    print(fund_em_info_net_acc_df)
    time.sleep(3)
    fund_em_info_acc_return_df = fund_em_open_fund_info(
        fund="710001", indicator="累计收益率走势"
    )
    print(fund_em_info_acc_return_df)
    time.sleep(3)
    fund_em_info_rank_df = fund_em_open_fund_info(fund="710001", indicator="同类排名走势")
    print(fund_em_info_rank_df)
    time.sleep(3)
    fund_em_info_rank_per_df = fund_em_open_fund_info(
        fund="710001", indicator="同类排名百分比"
    )
    print(fund_em_info_rank_per_df)
    time.sleep(3)
    fund_em_info_cash_df = fund_em_open_fund_info(fund="161606", indicator="分红送配详情")
    print(fund_em_info_cash_df)
    time.sleep(3)
    fund_em_info_div_per_df = fund_em_open_fund_info(fund="161725", indicator="拆分详情")
    print(fund_em_info_div_per_df)

    fund_em_money_fund_daily_df = fund_em_money_fund_daily()
    print(fund_em_money_fund_daily_df)

    fund_em_money_fund_info_df = fund_em_money_fund_info(fund="000009")
    print(fund_em_money_fund_info_df)

    fund_em_financial_fund_daily_df = fund_em_financial_fund_daily()
    print(fund_em_financial_fund_daily_df)

    fund_em_financial_fund_info_df = fund_em_financial_fund_info(fund="000134")
    print(fund_em_financial_fund_info_df)

    fund_em_graded_fund_daily_df = fund_em_graded_fund_daily()
    print(fund_em_graded_fund_daily_df)

    fund_em_graded_fund_info_df = fund_em_graded_fund_info(fund="150232")
    print(fund_em_graded_fund_info_df)

    fund_em_etf_fund_daily_df = fund_em_etf_fund_daily()
    print(fund_em_etf_fund_daily_df)

    fund_em_etf_fund_info_df = fund_em_etf_fund_info(fund="511280")
    print(fund_em_etf_fund_info_df)

    fund_em_value_estimation_df = fund_em_value_estimation()
    print(fund_em_value_estimation_df)
