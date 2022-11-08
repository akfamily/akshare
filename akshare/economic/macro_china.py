#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/8/15 15:40
Desc: 宏观数据-中国
"""
import json
import math
import time

import pandas as pd
import requests
from tqdm import tqdm

from akshare.economic.cons import (
    JS_CHINA_CPI_YEARLY_URL,
    JS_CHINA_CPI_MONTHLY_URL,
    JS_CHINA_M2_YEARLY_URL,
    JS_CHINA_PPI_YEARLY_URL,
    JS_CHINA_PMI_YEARLY_URL,
    JS_CHINA_GDP_YEARLY_URL,
    JS_CHINA_CX_PMI_YEARLY_URL,
    JS_CHINA_FX_RESERVES_YEARLY_URL,
    JS_CHINA_ENERGY_DAILY_URL,
    JS_CHINA_NON_MAN_PMI_MONTHLY_URL,
    JS_CHINA_CX_SERVICE_PMI_YEARLY_URL,
    JS_CHINA_MARKET_MARGIN_SH_URL,
)
from akshare.utils import demjson


# 企业商品价格指数
def macro_china_qyspjg() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国-企业商品价格指数
    http://data.eastmoney.com/cjsj/qyspjg.html
    :return: 企业商品价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "9",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "总指数-指数值",
        "总指数-同比增长",
        "总指数-环比增长",
        "农产品-指数值",
        "农产品-同比增长",
        "农产品-环比增长",
        "矿产品-指数值",
        "矿产品-同比增长",
        "矿产品-环比增长",
        "煤油电-指数值",
        "煤油电-同比增长",
        "煤油电-环比增长",
    ]
    temp_df["总指数-指数值"] = pd.to_numeric(temp_df["总指数-指数值"])
    temp_df["总指数-同比增长"] = pd.to_numeric(temp_df["总指数-同比增长"])
    temp_df["总指数-环比增长"] = pd.to_numeric(temp_df["总指数-环比增长"])
    temp_df["农产品-指数值"] = pd.to_numeric(temp_df["农产品-指数值"])
    temp_df["农产品-同比增长"] = pd.to_numeric(temp_df["农产品-同比增长"])
    temp_df["农产品-环比增长"] = pd.to_numeric(temp_df["农产品-环比增长"])
    temp_df["矿产品-指数值"] = pd.to_numeric(temp_df["矿产品-指数值"])
    temp_df["矿产品-同比增长"] = pd.to_numeric(temp_df["矿产品-同比增长"])
    temp_df["矿产品-环比增长"] = pd.to_numeric(temp_df["矿产品-环比增长"])
    temp_df["煤油电-指数值"] = pd.to_numeric(temp_df["煤油电-指数值"])
    temp_df["煤油电-同比增长"] = pd.to_numeric(temp_df["煤油电-同比增长"])
    temp_df["煤油电-环比增长"] = pd.to_numeric(temp_df["煤油电-环比增长"])
    temp_df["月份"] = pd.to_datetime(temp_df["月份"]).dt.date
    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


# 外商直接投资数据
def macro_china_fdi() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国-外商直接投资数据
    http://data.eastmoney.com/cjsj/fdi.html
    :return: 外商直接投资数据
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "15",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长",
    ]
    temp_df["当月"] = pd.to_numeric(temp_df["当月"])
    temp_df["当月-同比增长"] = pd.to_numeric(temp_df["当月-同比增长"])
    temp_df["当月-环比增长"] = pd.to_numeric(temp_df["当月-环比增长"])
    temp_df["累计"] = pd.to_numeric(temp_df["累计"])
    temp_df["累计-同比增长"] = pd.to_numeric(temp_df["累计-同比增长"])
    temp_df["月份"] = pd.to_datetime(temp_df["月份"]).dt.date
    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


# 中国社会融资规模数据
def macro_china_shrzgm() -> pd.DataFrame:
    """
    商务数据中心-国内贸易-社会融资规模增量统计
    http://data.mofcom.gov.cn/gnmy/shrzgm.shtml
    :return: 社会融资规模增量统计
    :rtype: pandas.DataFrame
    """
    url = "http://data.mofcom.gov.cn/datamofcom/front/gnmy/shrzgmQuery"
    r = requests.post(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df.columns = [
        "月份",
        "其中-未贴现银行承兑汇票",
        "其中-委托贷款",
        "其中-委托贷款外币贷款",
        "其中-人民币贷款",
        "其中-企业债券",
        "社会融资规模增量",
        "其中-非金融企业境内股票融资",
        "其中-信托贷款",
    ]
    temp_df = temp_df[
        [
            "月份",
            "社会融资规模增量",
            "其中-人民币贷款",
            "其中-委托贷款外币贷款",
            "其中-委托贷款",
            "其中-信托贷款",
            "其中-未贴现银行承兑汇票",
            "其中-企业债券",
            "其中-非金融企业境内股票融资",
        ]
    ]
    temp_df["社会融资规模增量"] = pd.to_numeric(temp_df["社会融资规模增量"])
    temp_df["其中-人民币贷款"] = pd.to_numeric(temp_df["其中-人民币贷款"])
    temp_df["其中-委托贷款外币贷款"] = pd.to_numeric(temp_df["其中-委托贷款外币贷款"])
    temp_df["其中-委托贷款"] = pd.to_numeric(temp_df["其中-委托贷款"])
    temp_df["其中-信托贷款"] = pd.to_numeric(temp_df["其中-信托贷款"])
    temp_df["其中-未贴现银行承兑汇票"] = pd.to_numeric(temp_df["其中-未贴现银行承兑汇票"])
    temp_df["其中-企业债券"] = pd.to_numeric(temp_df["其中-企业债券"])
    temp_df["其中-非金融企业境内股票融资"] = pd.to_numeric(temp_df["其中-非金融企业境内股票融资"])
    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
def macro_china_gdp_yearly() -> pd.DataFrame:
    """
    金十数据中心-中国 GDP 年率报告, 数据区间从 20110120-至今
    https://datacenter.jin10.com/reportType/dc_chinese_gdp_yoy
    :return: 中国 GDP 年率报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    r = requests.get(
        JS_CHINA_GDP_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(r.text[r.text.find("{") : r.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国GDP年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "57",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = pd.concat([temp_df, temp_se])
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.columns = ["date", "value"]
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["value"] = pd.to_numeric(temp_df["value"])
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
def macro_china_cpi_yearly() -> pd.DataFrame:
    """
    中国年度 CPI 数据, 数据区间从 19860201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_cpi_yoy
    :return: 中国年度 CPI 数据
    :rtype: pandas.DataFrame
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CPI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df["date"] = pd.to_datetime(date_list)
    temp_df = value_df[["date", "今值(%)"]]
    temp_df.columns = ["date", "value"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "56",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.columns = ["date", "value"]
    temp_df = pd.concat([temp_df, temp_se], ignore_index=True)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df.dropna(inplace=True)
    temp_df.sort_values(["date"], inplace=True)
    temp_df.drop_duplicates(subset="date", inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["value"] = pd.to_numeric(temp_df["value"], errors="coerce")
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI月率报告
def macro_china_cpi_monthly() -> pd.DataFrame:
    """
    中国月度 CPI 数据, 数据区间从 19960201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_cpi_mom
    :return: 中国月度 CPI 数据
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CPI_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "72",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "cpi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
def macro_china_ppi_yearly() -> pd.DataFrame:
    """
    中国年度 PPI 数据, 数据区间从 19950801-至今
    https://datacenter.jin10.com/reportType/dc_chinese_ppi_yoy
    :return: 中国年度PPI数据
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_PPI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国PPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "60",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "ppi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
def macro_china_exports_yoy() -> pd.DataFrame:
    """
    中国以美元计算出口年率报告, 数据区间从19820201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_exports_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_exports_yoy_all.js?v=1578754453
    :return: 中国以美元计算出口年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_exports_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国以美元计算出口年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "66",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "china_exports_yoy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
def macro_china_imports_yoy() -> pd.DataFrame:
    """
    中国以美元计算进口年率报告, 数据区间从 19960201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_imports_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_imports_yoy_all.js?v=1578754588
    :return: 中国以美元计算进口年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_imports_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国以美元计算进口年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "77",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "china_imports_yoy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-贸易状况-以美元计算贸易帐(亿美元)
def macro_china_trade_balance() -> pd.DataFrame:
    """
    中国以美元计算贸易帐报告, 数据区间从 19810201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_trade_balance
    https://cdn.jin10.com/dc/reports/dc_chinese_trade_balance_all.js?v=1578754677
    :return: 中国以美元计算贸易帐报告-今值(亿美元)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_trade_balance_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国以美元计算贸易帐报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "61",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "china_trade_balance"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-规模以上工业增加值年率
def macro_china_industrial_production_yoy() -> pd.DataFrame:
    """
    中国规模以上工业增加值年率报告, 数据区间从19900301-至今
    https://datacenter.jin10.com/reportType/dc_chinese_industrial_production_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_industrial_production_yoy_all.js?v=1578754779
    :return: 中国规模以上工业增加值年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_industrial_production_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [
        item["datas"]["中国规模以上工业增加值年率报告"] for item in json_data["list"]
    ]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "58",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "china_industrial_production_yoy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-官方制造业PMI
def macro_china_pmi_yearly() -> pd.DataFrame:
    """
    中国年度 PMI 数据, 数据区间从20050201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_manufacturing_pmi_all.js?v=1578817858
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国官方制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "65",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-财新制造业PMI终值
def macro_china_cx_pmi_yearly() -> pd.DataFrame:
    """
    中国年度财新PMI数据, 数据区间从 20120120-至今
    https://datacenter.jin10.com/reportType/dc_chinese_caixin_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_caixin_manufacturing_pmi_all.js?v=1578818009
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CX_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [
        item["datas"]["中国财新制造业PMI终值报告"] for item in json_data["list"]
    ]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "73",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "cx_pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-财新服务业PMI
def macro_china_cx_services_pmi_yearly() -> pd.DataFrame:
    """
    中国财新服务业PMI报告, 数据区间从 20120405-至今
    https://datacenter.jin10.com/reportType/dc_chinese_caixin_services_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_caixin_services_pmi_all.js?v=1578818109
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CX_SERVICE_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国财新服务业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "67",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "cx_services_pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-中国官方非制造业PMI
def macro_china_non_man_pmi() -> pd.DataFrame:
    """
    中国官方非制造业 PMI, 数据区间从 20160101-至今
    https://datacenter.jin10.com/reportType/dc_chinese_non_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_non_manufacturing_pmi_all.js?v=1578818248
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_NON_MAN_PMI_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国官方非制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "75",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "non_pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-金融指标-外汇储备(亿美元)
def macro_china_fx_reserves_yearly() -> pd.DataFrame:
    """
    中国年度外汇储备数据, 数据区间从 20140115-至今
    https://datacenter.jin10.com/reportType/dc_chinese_fx_reserves
    https://cdn.jin10.com/dc/reports/dc_chinese_fx_reserves_all.js?v=1578818365
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_FX_RESERVES_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国外汇储备报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "76",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "fx_reserves"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-金融指标-M2货币供应年率
def macro_china_m2_yearly() -> pd.DataFrame:
    """
    中国年度 M2 数据, 数据区间从 19980201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_m2_money_supply_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_m2_money_supply_yoy_all.js?v=1578818474
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_M2_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国M2货币供应年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "59",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "gpd"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-中国-金融指标-上海银行业同业拆借报告
def macro_china_shibor_all() -> pd.DataFrame:
    """
    上海银行业同业拆借报告, 数据区间从20170317-至今
    https://datacenter.jin10.com/reportType/dc_shibor
    https://cdn.jin10.com/dc/reports/dc_shibor_all.js?v=1578755058
    :return: 上海银行业同业拆借报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/il_1.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    big_df["O/N_定价"] = temp_df["O/N"].apply(lambda x: x[0])
    big_df["O/N_涨跌幅"] = temp_df["O/N"].apply(lambda x: x[1])
    big_df["1W_定价"] = temp_df["1W"].apply(lambda x: x[0])
    big_df["1W_涨跌幅"] = temp_df["1W"].apply(lambda x: x[1])
    big_df["2W_定价"] = temp_df["2W"].apply(lambda x: x[0])
    big_df["2W_涨跌幅"] = temp_df["2W"].apply(lambda x: x[1])
    big_df["1M_定价"] = temp_df["1M"].apply(lambda x: x[0])
    big_df["1M_涨跌幅"] = temp_df["1M"].apply(lambda x: x[1])
    big_df["3M_定价"] = temp_df["3M"].apply(lambda x: x[0])
    big_df["3M_涨跌幅"] = temp_df["3M"].apply(lambda x: x[1])
    big_df["6M_定价"] = temp_df["6M"].apply(lambda x: x[0])
    big_df["6M_涨跌幅"] = temp_df["6M"].apply(lambda x: x[1])
    big_df["9M_定价"] = temp_df["9M"].apply(lambda x: x[0])
    big_df["9M_涨跌幅"] = temp_df["9M"].apply(lambda x: x[1])
    big_df["1Y_定价"] = temp_df["1Y"].apply(lambda x: x[0])
    big_df["1Y_涨跌幅"] = temp_df["1Y"].apply(lambda x: x[1])
    # big_df["ON_定价"] = temp_df["ON"].apply(lambda x: x[0])
    # big_df["ON_涨跌幅"] = temp_df["ON"].apply(lambda x: x[1])
    # big_df["2M_定价"] = temp_df["2M"].apply(lambda x: x[0])
    # big_df["2M_涨跌幅"] = temp_df["2M"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", pd.NA))
    big_df = big_df.apply(lambda x: x.replace([None], pd.NA))
    big_df.sort_index(inplace=True)
    return big_df


# 金十数据中心-经济指标-中国-金融指标-人民币香港银行同业拆息
def macro_china_hk_market_info() -> pd.DataFrame:
    """
    香港同业拆借报告, 数据区间从 20170320-至今
    https://datacenter.jin10.com/reportType/dc_hk_market_info
    https://cdn.jin10.com/dc/reports/dc_hk_market_info_all.js?v=1578755471
    :return: 香港同业拆借报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/il_2.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    # big_df["O/N_定价"] = temp_df["O/N"].apply(lambda x: x[0])
    # big_df["O/N_涨跌幅"] = temp_df["O/N"].apply(lambda x: x[1])
    big_df["1W_定价"] = temp_df["1W"].apply(lambda x: x[0])
    big_df["1W_涨跌幅"] = temp_df["1W"].apply(lambda x: x[1])
    big_df["2W_定价"] = temp_df["2W"].apply(lambda x: x[0])
    big_df["2W_涨跌幅"] = temp_df["2W"].apply(lambda x: x[1])
    big_df["1M_定价"] = temp_df["1M"].apply(lambda x: x[0])
    big_df["1M_涨跌幅"] = temp_df["1M"].apply(lambda x: x[1])
    big_df["3M_定价"] = temp_df["3M"].apply(lambda x: x[0])
    big_df["3M_涨跌幅"] = temp_df["3M"].apply(lambda x: x[1])
    big_df["6M_定价"] = temp_df["6M"].apply(lambda x: x[0])
    big_df["6M_涨跌幅"] = temp_df["6M"].apply(lambda x: x[1])
    # big_df["9M_定价"] = temp_df["9M"].apply(lambda x: x[0])
    # big_df["9M_涨跌幅"] = temp_df["9M"].apply(lambda x: x[1])
    big_df["1Y_定价"] = temp_df["1Y"].apply(lambda x: x[0])
    big_df["1Y_涨跌幅"] = temp_df["1Y"].apply(lambda x: x[1])
    big_df["ON_定价"] = temp_df["ON"].apply(lambda x: x[0])
    big_df["ON_涨跌幅"] = temp_df["ON"].apply(lambda x: x[1])
    big_df["2M_定价"] = temp_df["2M"].apply(lambda x: x[0])
    big_df["2M_涨跌幅"] = temp_df["2M"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", pd.NA))
    big_df = big_df.apply(lambda x: x.replace([None], pd.NA))
    big_df.sort_index(inplace=True)
    big_df.reset_index(inplace=True)
    big_df.columns = [
        "日期",
        "1W_定价",
        "1W_涨跌幅",
        "2W_定价",
        "2W_涨跌幅",
        "1M_定价",
        "1M_涨跌幅",
        "3M_定价",
        "3M_涨跌幅",
        "6M_定价",
        "6M_涨跌幅",
        "1Y_定价",
        "1Y_涨跌幅",
        "ON_定价",
        "ON_涨跌幅",
        "2M_定价",
        "2M_涨跌幅",
    ]

    big_df["1W_定价"] = pd.to_numeric(big_df["1W_定价"])
    big_df["1W_涨跌幅"] = pd.to_numeric(big_df["1W_涨跌幅"])
    big_df["2W_定价"] = pd.to_numeric(big_df["2W_定价"])
    big_df["2W_涨跌幅"] = pd.to_numeric(big_df["2W_涨跌幅"])
    big_df["1M_定价"] = pd.to_numeric(big_df["1M_定价"])
    big_df["1M_涨跌幅"] = pd.to_numeric(big_df["1M_涨跌幅"])
    big_df["3M_定价"] = pd.to_numeric(big_df["3M_定价"])
    big_df["3M_涨跌幅"] = pd.to_numeric(big_df["3M_涨跌幅"])
    big_df["6M_定价"] = pd.to_numeric(big_df["6M_定价"])
    big_df["6M_涨跌幅"] = pd.to_numeric(big_df["6M_涨跌幅"])
    big_df["1Y_定价"] = pd.to_numeric(big_df["1Y_定价"])
    big_df["1Y_涨跌幅"] = pd.to_numeric(big_df["1Y_涨跌幅"])
    big_df["ON_定价"] = pd.to_numeric(big_df["ON_定价"])
    big_df["ON_涨跌幅"] = pd.to_numeric(big_df["ON_涨跌幅"])
    big_df["2M_定价"] = pd.to_numeric(big_df["2M_定价"])
    big_df["2M_涨跌幅"] = pd.to_numeric(big_df["2M_涨跌幅"])

    return big_df


# 金十数据中心-经济指标-中国-其他-中国日度沿海六大电库存数据
def macro_china_daily_energy() -> pd.DataFrame:
    """
    中国日度沿海六大电库存数据, 数据区间从20160101-至今
    https://datacenter.jin10.com/reportType/dc_qihuo_energy_report
    https://cdn.jin10.com/dc/reports/dc_qihuo_energy_report_all.js?v=1578819100
    :return: pandas.Series
                 沿海六大电库存      日耗 存煤可用天数
    2016-01-01  1167.60   64.20   18.19
    2016-01-02  1162.90   63.40   18.34
    2016-01-03  1160.80   62.60   18.54
    2016-01-04  1185.30   57.60   20.58
    2016-01-05  1150.20   57.20   20.11
                  ...     ...    ...
    2019-05-17   1639.47   61.71  26.56
    2019-05-21   1591.92   62.67  25.40
    2019-05-22   1578.63   59.54  26.51
    2019-05-24   1671.83   60.65  27.56
    2019-06-21   1786.64   66.57  26.84
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_ENERGY_DAILY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["沿海六大电厂库存动态报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df[["沿海六大电库存", "日耗", "存煤可用天数"]]
    temp_df.name = "energy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-其他-中国人民币汇率中间价报告
def macro_china_rmb() -> pd.DataFrame:
    """
    中国人民币汇率中间价报告, 数据区间从 20170103-至今
    https://datacenter.jin10.com/reportType/dc_rmb_data
    :return: 中国人民币汇率中间价报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/exchange_rate.json",
        params=params,
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    big_df["美元/人民币_中间价"] = temp_df["美元/人民币"].apply(lambda x: x[0])
    big_df["美元/人民币_涨跌幅"] = temp_df["美元/人民币"].apply(lambda x: x[1])
    big_df["欧元/人民币_中间价"] = temp_df["欧元/人民币"].apply(lambda x: x[0])
    big_df["欧元/人民币_涨跌幅"] = temp_df["欧元/人民币"].apply(lambda x: x[1])
    big_df["100日元/人民币_中间价"] = temp_df["100日元/人民币"].apply(lambda x: x[0])
    big_df["100日元/人民币_涨跌幅"] = temp_df["100日元/人民币"].apply(lambda x: x[1])
    big_df["港元/人民币_中间价"] = temp_df["港元/人民币"].apply(lambda x: x[0])
    big_df["港元/人民币_涨跌幅"] = temp_df["港元/人民币"].apply(lambda x: x[1])
    big_df["英镑/人民币_中间价"] = temp_df["英镑/人民币"].apply(lambda x: x[0])
    big_df["英镑/人民币_涨跌幅"] = temp_df["英镑/人民币"].apply(lambda x: x[1])
    big_df["澳元/人民币_中间价"] = temp_df["澳元/人民币"].apply(lambda x: x[0])
    big_df["澳元/人民币_涨跌幅"] = temp_df["澳元/人民币"].apply(lambda x: x[1])
    big_df["新西兰元/人民币_中间价"] = temp_df["新西兰元/人民币"].apply(lambda x: x[0])
    big_df["新西兰元/人民币_涨跌幅"] = temp_df["新西兰元/人民币"].apply(lambda x: x[1])
    big_df["新加坡元/人民币_中间价"] = temp_df["新加坡元/人民币"].apply(lambda x: x[0])
    big_df["新加坡元/人民币_涨跌幅"] = temp_df["新加坡元/人民币"].apply(lambda x: x[1])
    big_df["瑞郎/人民币_中间价"] = temp_df["瑞郎/人民币"].apply(lambda x: x[0])
    big_df["瑞郎/人民币_涨跌幅"] = temp_df["瑞郎/人民币"].apply(lambda x: x[1])
    big_df["加元/人民币_中间价"] = temp_df["加元/人民币"].apply(lambda x: x[0])
    big_df["加元/人民币_涨跌幅"] = temp_df["加元/人民币"].apply(lambda x: x[1])
    big_df["人民币/马来西亚林吉特_中间价"] = temp_df["人民币/马来西亚林吉特"].apply(lambda x: x[0])
    big_df["人民币/马来西亚林吉特_涨跌幅"] = temp_df["人民币/马来西亚林吉特"].apply(lambda x: x[1])
    big_df["人民币/俄罗斯卢布_中间价"] = temp_df["人民币/俄罗斯卢布"].apply(lambda x: x[0])
    big_df["人民币/俄罗斯卢布_涨跌幅"] = temp_df["人民币/俄罗斯卢布"].apply(lambda x: x[1])
    big_df["人民币/南非兰特_中间价"] = temp_df["人民币/南非兰特"].apply(lambda x: x[0])
    big_df["人民币/南非兰特_涨跌幅"] = temp_df["人民币/南非兰特"].apply(lambda x: x[1])
    big_df["人民币/韩元_中间价"] = temp_df["人民币/韩元"].apply(lambda x: x[0])
    big_df["人民币/韩元_涨跌幅"] = temp_df["人民币/韩元"].apply(lambda x: x[1])
    big_df["人民币/阿联酋迪拉姆_中间价"] = temp_df["人民币/阿联酋迪拉姆"].apply(lambda x: x[0])
    big_df["人民币/阿联酋迪拉姆_涨跌幅"] = temp_df["人民币/阿联酋迪拉姆"].apply(lambda x: x[1])
    big_df["人民币/沙特里亚尔_中间价"] = temp_df["人民币/沙特里亚尔"].apply(lambda x: x[0])
    big_df["人民币/沙特里亚尔_涨跌幅"] = temp_df["人民币/沙特里亚尔"].apply(lambda x: x[1])
    big_df["人民币/匈牙利福林_中间价"] = temp_df["人民币/匈牙利福林"].apply(lambda x: x[0])
    big_df["人民币/匈牙利福林_涨跌幅"] = temp_df["人民币/匈牙利福林"].apply(lambda x: x[1])
    big_df["人民币/波兰兹罗提_中间价"] = temp_df["人民币/波兰兹罗提"].apply(lambda x: x[0])
    big_df["人民币/波兰兹罗提_涨跌幅"] = temp_df["人民币/波兰兹罗提"].apply(lambda x: x[1])
    big_df["人民币/丹麦克朗_中间价"] = temp_df["人民币/丹麦克朗"].apply(lambda x: x[0])
    big_df["人民币/丹麦克朗_涨跌幅"] = temp_df["人民币/丹麦克朗"].apply(lambda x: x[1])
    big_df["人民币/瑞典克朗_中间价"] = temp_df["人民币/瑞典克朗"].apply(lambda x: x[0])
    big_df["人民币/瑞典克朗_涨跌幅"] = temp_df["人民币/瑞典克朗"].apply(lambda x: x[1])
    big_df["人民币/挪威克朗_中间价"] = temp_df["人民币/挪威克朗"].apply(lambda x: x[0])
    big_df["人民币/挪威克朗_涨跌幅"] = temp_df["人民币/挪威克朗"].apply(lambda x: x[1])
    big_df["人民币/土耳其里拉_中间价"] = temp_df["人民币/土耳其里拉"].apply(lambda x: x[0])
    big_df["人民币/土耳其里拉_涨跌幅"] = temp_df["人民币/土耳其里拉"].apply(lambda x: x[1])
    big_df["人民币/墨西哥比索_中间价"] = temp_df["人民币/墨西哥比索"].apply(lambda x: x[0])
    big_df["人民币/墨西哥比索_涨跌幅"] = temp_df["人民币/墨西哥比索"].apply(lambda x: x[1])
    big_df["人民币/泰铢_定价"] = temp_df["人民币/泰铢"].apply(lambda x: x[0])
    big_df["人民币/泰铢_涨跌幅"] = temp_df["人民币/泰铢"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", pd.NA))
    big_df = big_df.apply(lambda x: x.replace([None], pd.NA))
    big_df.sort_index(inplace=True)
    big_df.fillna(0, inplace=True)
    big_df = big_df.astype("float")
    big_df.reset_index(inplace=True)
    big_df.rename(columns={"index": "日期"}, inplace=True)
    return big_df


# 金十数据中心-经济指标-中国-其他-深圳融资融券报告
def macro_china_market_margin_sz() -> pd.DataFrame:
    """
    深圳融资融券报告, 数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sz
    :return: pandas.DataFrame
                   融资买入额(元)       融资余额(元)  融券卖出量(股)    融券余量(股)     融券余额(元)  \
    2010-03-31       684569        670796      4000       3900       70895
    2010-04-08      6713260      14467758      2100       3100       56023
    2010-04-09      9357095      19732998      6700       5400      108362
    2010-04-12     10406563      24813027      2200       1000        8100
    2010-04-15     16607172      47980287      4200       5200       97676
                     ...           ...       ...        ...         ...
    2019-12-12  25190412075  423457288662  29769255  209557883  2504593151
    2019-12-13  29636811209  423422868505  32820867  206092170  2509424768
    2019-12-16  39166060634  428851154451  44000215  217123568  2647520178
    2019-12-17  46930557203  433966722200  40492711  220945538  2750371397
    2019-12-18  41043515833  438511398249  39150376  224554586  2761303194
                   融资融券余额(元)
    2010-03-31        741691
    2010-04-08      14523781
    2010-04-09      19841360
    2010-04-12      24821127
    2010-04-15      48077963
                      ...
    2019-12-12  425961881813
    2019-12-13  425932293273
    2019-12-16  431498674629
    2019-12-17  436717093597
    2019-12-18  441272701443
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/fs_2.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.columns = ["融资买入额", "融资余额", "融券卖出量", "融券余量", "融券余额", "融资融券余额"]
    temp_df.sort_index(inplace=True)
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-中国-其他-上海融资融券报告
def macro_china_market_margin_sh() -> pd.DataFrame:
    """
    上海融资融券报告, 数据区间从 20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sse
    :return: pandas.DataFrame
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_MARKET_MARGIN_SH_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(
        res.text[res.text.find("{") : res.text.rfind("}") + 1]
    )
    date_list = [item["date"] for item in json_data["list"]]
    value_list_1 = [item["datas"]["总量"][0] for item in json_data["list"]]
    value_list_2 = [item["datas"]["总量"][1] for item in json_data["list"]]
    value_list_3 = [item["datas"]["总量"][2] for item in json_data["list"]]
    value_list_4 = [item["datas"]["总量"][3] for item in json_data["list"]]
    value_list_5 = [item["datas"]["总量"][4] for item in json_data["list"]]
    value_list_6 = [item["datas"]["总量"][5] for item in json_data["list"]]
    value_df = pd.DataFrame(
        [
            value_list_1,
            value_list_2,
            value_list_3,
            value_list_4,
            value_list_5,
            value_list_6,
        ]
    ).T
    value_df.columns = [
        "融资余额",
        "融资买入额",
        "融券余量",
        "融券余额",
        "融券卖出量",
        "融资融券余额",
    ]
    value_df.index = pd.to_datetime(date_list)
    value_df.name = "market_margin_sh"
    value_df.index = pd.to_datetime(value_df.index)
    value_df = value_df.astype(float)

    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "fs",
        "attr_id": "1",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_market_margin_sse",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.DataFrame(r.json()["data"]["values"])
    temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
    temp_df = temp_df.iloc[:, 1:]
    temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][1:]

    for_times = math.ceil(
        int(str((temp_df.index[-1] - value_df.index[-1])).split(" ")[0]) / 20
    )
    big_df = temp_df
    for i in tqdm(range(for_times)):
        params = {
            "max_date": temp_df.index[-1],
            "category": "fs",
            "attr_id": "1",
            "_": str(int(round(t * 1000))),
        }
        r = requests.get(url, params=params, headers=headers)
        temp_df = pd.DataFrame(r.json()["data"]["values"])
        temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
        temp_df = temp_df.iloc[:, 1:]
        temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][
            1:
        ]
        big_df = big_df.append(temp_df)

    value_df = value_df.append(big_df)
    value_df.drop_duplicates(inplace=True)
    value_df.sort_index(inplace=True)
    return value_df


# 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
def macro_china_au_report() -> pd.DataFrame:
    """
    上海黄金交易所报告, 数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_sge_report
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/sge.json", params=params
    )
    json_data = res.json()
    big_df = pd.DataFrame()
    for item in json_data["values"].keys():
        temp_df = pd.DataFrame(json_data["values"][item])
        temp_df["date"] = item
        temp_df.columns = [
            "商品",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "涨跌",
            "涨跌幅",
            "加权平均价",
            "成交量",
            "成交金额",
            "持仓量",
            "交收方向",
            "交收量",
            "日期",
        ]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.index = pd.to_datetime(big_df["日期"])
    del big_df["日期"]
    big_df.sort_index(inplace=True)
    return big_df


# 发改委-中国电煤价格指数-全国综合电煤价格指数
def macro_china_ctci() -> pd.DataFrame:
    """
    中国电煤价格指数-全国综合电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :return: 20140101-至今的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = "http://59.252.41.60/portal//out/dm?t=1578298533594"
    r = requests.get(url)
    temp_df = pd.Series(r.json()["data"][0])
    temp_df.index = pd.to_datetime(r.json()["periods"])
    temp_df = temp_df.astype(float)
    return temp_df


# 发改委-中国电煤价格指数-各价区电煤价格指数
def macro_china_ctci_detail() -> pd.DataFrame:
    """
    2019年11月各价区电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :return:
    :rtype:
    """
    url = "http://59.252.41.60/portal//out/dm/list/cebdf627f9c24c22a507e2f2e25e2b43?t=1578298533161"
    res = requests.get(url)
    data_df = pd.DataFrame(res.json()["data"])
    data_df.index = res.json()["names"]
    data_df.columns = ["-", "环比", "上期", "同比", "本期"]
    temp = data_df[["环比", "上期", "同比", "本期"]]
    temp = temp.astype(float)
    return temp


# 发改委-中国电煤价格指数-历史电煤价格指数
def macro_china_ctci_detail_hist(year: str = "2018") -> pd.DataFrame:
    """
    历史电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :param year: 2014-2019 年
    :type year: str
    :return: 制定年份的中国电煤价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://59.252.41.60/portal//out/dm/listAll?t=1578299685398"
    params = {
        "CONF_ID": "cebdf627f9c24c22a507e2f2e25e2b43",
        "year": f"{year}",
    }
    res = requests.post(url, data=params)
    data_df = pd.DataFrame(res.json()["data"])
    data_df.columns = res.json()["names"]
    data_df.index = data_df["地区"]
    del data_df["地区"]
    temp_df = data_df
    temp_df = temp_df.astype(float)
    return temp_df


# 中国-利率-贷款报价利率
def macro_china_lpr() -> pd.DataFrame:
    """
    http://data.eastmoney.com/cjsj/globalRateLPR.html
    LPR品种详细数据
    :return: LPR品种详细数据
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPTA_WEB_RATE",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "p": "1",
        "ps": "2000",
        "st": "TRADE_DATE",
        "sr": "-1",
        "var": "WPuRCBoA",
        "rt": "52826782",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text.strip("var WPuRCBoA=")[:-1])
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df["TRADE_DATE"] = pd.to_datetime(temp_df["TRADE_DATE"]).dt.date
    temp_df["LPR1Y"] = pd.to_numeric(temp_df["LPR1Y"])
    temp_df["LPR5Y"] = pd.to_numeric(temp_df["LPR5Y"])
    temp_df["RATE_1"] = pd.to_numeric(temp_df["RATE_1"])
    temp_df["RATE_2"] = pd.to_numeric(temp_df["RATE_2"])
    temp_df.sort_values(["TRADE_DATE"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


# 中国-新房价指数
def macro_china_new_house_price() -> pd.DataFrame:
    """
    中国-新房价指数
    http://data.eastmoney.com/cjsj/newhouse.html
    :return: 新房价指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable6451982",
        "type": "GJZB",
        "sty": "XFJLB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "19",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "日期",
        "城市",
        "新建住宅价格指数-环比",
        "新建住宅价格指数-同比",
        "新建住宅价格指数-定基",
        "新建商品住宅价格指数-环比",
        "新建商品住宅价格指数-同比",
        "新建商品住宅价格指数-定基",
        "二手住宅价格指数-环比",
        "二手住宅价格指数-同比",
        "二手住宅价格指数-定基",
    ]
    return temp_df


# 中国-企业景气及企业家信心指数
def macro_china_enterprise_boom_index() -> pd.DataFrame:
    """
    http://data.eastmoney.com/cjsj/qyjqzs.html
    中国-企业景气及企业家信心指数
    :return: 企业景气及企业家信心指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable6607710",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "季度",
        "企业景气指数-指数",
        "企业景气指数-同比",
        "企业景气指数-环比",
        "企业家信心指数-指数",
        "企业家信心指数-同比",
        "企业家信心指数-环比",
    ]
    return temp_df


# 中国-全国税收收入
def macro_china_national_tax_receipts() -> pd.DataFrame:
    """
    中国-全国税收收入
    http://data.eastmoney.com/cjsj/qgsssr.html
    :return: 全国税收收入
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = ["季度", "税收收入合计", "较上年同期", "季度环比"]
    temp_df["税收收入合计"] = pd.to_numeric(temp_df["税收收入合计"])
    temp_df["较上年同期"] = pd.to_numeric(temp_df["较上年同期"])
    temp_df["季度环比"] = pd.to_numeric(temp_df["季度环比"])
    return temp_df


# 中国-银行理财产品发行数量
def macro_china_bank_financing() -> pd.DataFrame:
    """
    银行理财产品发行数量
    https://data.eastmoney.com/cjsj/hyzs_list_EMI01516267.html
    :return: 银行理财产品发行数量
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI01516267")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["最新值"] = pd.to_numeric(temp_df["最新值"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["近3月涨跌幅"] = pd.to_numeric(temp_df["近3月涨跌幅"])
    temp_df["近6月涨跌幅"] = pd.to_numeric(temp_df["近6月涨跌幅"])
    temp_df["近1年涨跌幅"] = pd.to_numeric(temp_df["近1年涨跌幅"])
    temp_df["近2年涨跌幅"] = pd.to_numeric(temp_df["近2年涨跌幅"])
    temp_df["近3年涨跌幅"] = pd.to_numeric(temp_df["近3年涨跌幅"])
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def macro_china_insurance_income() -> pd.DataFrame:
    """
    原保险保费收入
    https://data.eastmoney.com/cjsj/hyzs_list_EMM00088870.html
    :return: 原保险保费收入
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMM00088870")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["最新值"] = pd.to_numeric(temp_df["最新值"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["近3月涨跌幅"] = pd.to_numeric(temp_df["近3月涨跌幅"])
    temp_df["近6月涨跌幅"] = pd.to_numeric(temp_df["近6月涨跌幅"])
    temp_df["近1年涨跌幅"] = pd.to_numeric(temp_df["近1年涨跌幅"])
    temp_df["近2年涨跌幅"] = pd.to_numeric(temp_df["近2年涨跌幅"])
    temp_df["近3年涨跌幅"] = pd.to_numeric(temp_df["近3年涨跌幅"])
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def macro_china_mobile_number() -> pd.DataFrame:
    """
    手机出货量
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00225823.html
    :return: 手机出货量
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00225823")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.drop_duplicates(inplace=True)
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["最新值"] = pd.to_numeric(temp_df["最新值"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["近3月涨跌幅"] = pd.to_numeric(temp_df["近3月涨跌幅"])
    temp_df["近6月涨跌幅"] = pd.to_numeric(temp_df["近6月涨跌幅"])
    temp_df["近1年涨跌幅"] = pd.to_numeric(temp_df["近1年涨跌幅"])
    temp_df["近2年涨跌幅"] = pd.to_numeric(temp_df["近2年涨跌幅"])
    temp_df["近3年涨跌幅"] = pd.to_numeric(temp_df["近3年涨跌幅"])
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def macro_china_vegetable_basket() -> pd.DataFrame:
    """
    菜篮子产品批发价格指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00009275.html
    :return: 菜篮子产品批发价格指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00009275")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_agricultural_product() -> pd.DataFrame:
    """
    农产品批发价格总指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00009274.html
    :return: 农产品批发价格总指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00009274")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_agricultural_index() -> pd.DataFrame:
    """
    农副指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00662543.html
    :return: 农副指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662543")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_energy_index() -> pd.DataFrame:
    """
    能源指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00662539.html
    :return: 能源指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662539")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_commodity_price_index() -> pd.DataFrame:
    """
    大宗商品价格
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00662535.html
    :return: 大宗商品价格
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662535")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_global_sox_index() -> pd.DataFrame:
    """
    费城半导体指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00055562.html
    :return: 费城半导体指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00055562")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_yw_electronic_index() -> pd.DataFrame:
    """
    义乌小商品指数-电子元器件
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00055551.html
    :return: 义乌小商品指数-电子元器件
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00055551")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_construction_index() -> pd.DataFrame:
    """
    建材指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00662541.html
    :return: 建材指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662541")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_construction_price_index() -> pd.DataFrame:
    """
    建材价格指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00237146.html
    :return: 建材价格指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00237146")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_lpi_index() -> pd.DataFrame:
    """
    物流景气指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00352262.html
    :return: 物流景气指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00352262")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_bdti_index() -> pd.DataFrame:
    """
    原油运输指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00107668.html
    :return: 原油运输指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00107668")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_bsi_index() -> pd.DataFrame:
    """
    超灵便型船运价指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00107667.html
    :return: 超灵便型船运价指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00107667")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def macro_china_new_financial_credit() -> pd.DataFrame:
    """
    中国-新增信贷数据
    http://data.eastmoney.com/cjsj/xzxd.html
    :return: 新增信贷数据
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable4364401",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "7",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = ["月份", "当月", "当月-同比增长", "当月-环比增长", "累计", "累计-同比增长"]
    temp_df["当月-同比增长"] = temp_df["当月-同比增长"].str.replace("%", "")
    temp_df["当月-环比增长"] = temp_df["当月-环比增长"].str.replace("%", "")
    temp_df["累计-同比增长"] = temp_df["累计-同比增长"].str.replace("%", "")

    temp_df["月份"] = pd.to_datetime(temp_df["月份"]).dt.date
    temp_df["当月"] = pd.to_numeric(temp_df["当月"])
    temp_df["当月-同比增长"] = pd.to_numeric(temp_df["当月-同比增长"])
    temp_df["当月-环比增长"] = pd.to_numeric(temp_df["当月-环比增长"])
    temp_df["累计"] = pd.to_numeric(temp_df["累计"])
    temp_df["累计-同比增长"] = pd.to_numeric(temp_df["累计-同比增长"])

    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def macro_china_fx_gold() -> pd.DataFrame:
    """
    东方财富-外汇和黄金储备
    http://data.eastmoney.com/cjsj/hjwh.html
    :return: 外汇和黄金储备
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "columns": "REPORT_DATE,TIME,GOLD_RESERVES,GOLD_RESERVES_SAME,GOLD_RESERVES_SEQUENTIAL,FOREX,FOREX_SAME,FOREX_SEQUENTIAL",
        "pageNumber": "1",
        "pageSize": "1000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_GOLD_CURRENCY",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1660718498421",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "月份",
        "黄金储备-数值",
        "黄金储备-同比",
        "黄金储备-环比",
        "国家外汇储备-数值",
        "国家外汇储备-同比",
        "国家外汇储备-环比",
    ]
    temp_df = temp_df[
        [
            "月份",
            "黄金储备-数值",
            "黄金储备-同比",
            "黄金储备-环比",
            "国家外汇储备-数值",
            "国家外汇储备-同比",
            "国家外汇储备-环比",
        ]
    ]
    temp_df["国家外汇储备-数值"] = pd.to_numeric(temp_df["国家外汇储备-数值"])
    temp_df["国家外汇储备-同比"] = pd.to_numeric(temp_df["国家外汇储备-同比"])
    temp_df["国家外汇储备-环比"] = pd.to_numeric(temp_df["国家外汇储备-环比"])
    temp_df["黄金储备-数值"] = pd.to_numeric(temp_df["黄金储备-数值"])
    temp_df["黄金储备-同比"] = pd.to_numeric(temp_df["黄金储备-同比"])
    temp_df["黄金储备-环比"] = pd.to_numeric(temp_df["黄金储备-环比"])
    temp_df.sort_values(["月份"], inplace=True, ignore_index=True)
    return temp_df


def macro_china_stock_market_cap() -> pd.DataFrame:
    """
    东方财富-全国股票交易统计表
    http://data.eastmoney.com/cjsj/gpjytj.html
    :return: 全国股票交易统计表
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "cb": "",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "2",
        "_": "1608999482942",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "数据日期",
        "发行总股本-上海",
        "发行总股本-深圳",
        "市价总值-上海",
        "市价总值-深圳",
        "成交金额-上海",
        "成交金额-深圳",
        "成交量-上海",
        "成交量-深圳",
        "A股最高综合股价指数-上海",
        "A股最高综合股价指数-深圳",
        "A股最低综合股价指数-上海",
        "A股最低综合股价指数-深圳",
    ]
    temp_df["发行总股本-上海"] = pd.to_numeric(temp_df["发行总股本-上海"])
    temp_df["发行总股本-深圳"] = pd.to_numeric(temp_df["发行总股本-深圳"])
    temp_df["市价总值-上海"] = pd.to_numeric(temp_df["市价总值-上海"])
    temp_df["市价总值-深圳"] = pd.to_numeric(temp_df["市价总值-深圳"])
    temp_df["成交金额-上海"] = pd.to_numeric(temp_df["成交金额-上海"])
    temp_df["成交金额-深圳"] = pd.to_numeric(temp_df["成交金额-深圳"])
    temp_df["成交量-上海"] = pd.to_numeric(temp_df["成交量-上海"])
    temp_df["成交量-深圳"] = pd.to_numeric(temp_df["成交量-深圳"])
    temp_df["A股最高综合股价指数-上海"] = pd.to_numeric(temp_df["A股最高综合股价指数-上海"])
    temp_df["A股最高综合股价指数-深圳"] = pd.to_numeric(temp_df["A股最高综合股价指数-深圳"])
    temp_df["A股最低综合股价指数-上海"] = pd.to_numeric(temp_df["A股最低综合股价指数-上海"])
    temp_df["A股最低综合股价指数-深圳"] = pd.to_numeric(temp_df["A股最低综合股价指数-深圳"])
    return temp_df


def macro_china_money_supply() -> pd.DataFrame:
    """
    东方财富-货币供应量
    http://data.eastmoney.com/cjsj/hbgyl.html
    :return: 货币供应量
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "p": "1",
        "ps": "200",
        "mkt": "11",
    }
    r = requests.get(url=url, params=params)
    data_text = r.text
    tmp_list = data_text[data_text.find("[") + 2 : -3]
    tmp_list = tmp_list.split('","')
    res_list = []
    for li in tmp_list:
        res_list.append(li.split(","))
    columns = [
        "月份",
        "货币和准货币(M2)数量(亿元)",
        "货币和准货币(M2)同比增长",
        "货币和准货币(M2)环比增长",
        "货币(M1)数量(亿元)",
        "货币(M1)同比增长",
        "货币(M1)环比增长",
        "流通中的现金(M0)数量(亿元)",
        "流通中的现金(M0)同比增长",
        "流通中的现金(M0)环比增长",
    ]
    data_df = pd.DataFrame(res_list, columns=columns)
    data_df["货币和准货币(M2)数量(亿元)"] = pd.to_numeric(data_df["货币和准货币(M2)数量(亿元)"])
    data_df["货币和准货币(M2)同比增长"] = pd.to_numeric(data_df["货币和准货币(M2)同比增长"])
    data_df["货币和准货币(M2)环比增长"] = pd.to_numeric(data_df["货币和准货币(M2)环比增长"])
    data_df["货币(M1)数量(亿元)"] = pd.to_numeric(data_df["货币(M1)数量(亿元)"])
    data_df["货币(M1)同比增长"] = pd.to_numeric(data_df["货币(M1)同比增长"])
    data_df["货币(M1)环比增长"] = pd.to_numeric(data_df["货币(M1)环比增长"])
    data_df["流通中的现金(M0)数量(亿元)"] = pd.to_numeric(data_df["流通中的现金(M0)数量(亿元)"])
    data_df["流通中的现金(M0)同比增长"] = pd.to_numeric(data_df["流通中的现金(M0)同比增长"])
    data_df["流通中的现金(M0)环比增长"] = pd.to_numeric(data_df["流通中的现金(M0)环比增长"])
    return data_df


def macro_china_cpi() -> pd.DataFrame:
    """
    东方财富-中国居民消费价格指数
    http://data.eastmoney.com/cjsj/cpi.html
    :return: 东方财富-中国居民消费价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "19",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "全国-当月",
        "全国-同比增长",
        "全国-环比增长",
        "全国-累计",
        "城市-当月",
        "城市-同比增长",
        "城市-环比增长",
        "城市-累计",
        "农村-当月",
        "农村-同比增长",
        "农村-环比增长",
        "农村-累计",
    ]
    temp_df["全国-当月"] = pd.to_numeric(temp_df["全国-当月"])
    temp_df["全国-同比增长"] = pd.to_numeric(temp_df["全国-同比增长"])
    temp_df["全国-环比增长"] = pd.to_numeric(temp_df["全国-环比增长"])
    temp_df["全国-累计"] = pd.to_numeric(temp_df["全国-累计"])
    temp_df["城市-当月"] = pd.to_numeric(temp_df["城市-当月"])
    temp_df["城市-同比增长"] = pd.to_numeric(temp_df["城市-同比增长"])
    temp_df["城市-环比增长"] = pd.to_numeric(temp_df["城市-环比增长"])
    temp_df["城市-累计"] = pd.to_numeric(temp_df["城市-累计"])
    temp_df["农村-当月"] = pd.to_numeric(temp_df["农村-当月"])
    temp_df["农村-同比增长"] = pd.to_numeric(temp_df["农村-同比增长"])
    temp_df["农村-环比增长"] = pd.to_numeric(temp_df["农村-环比增长"])
    temp_df["农村-累计"] = pd.to_numeric(temp_df["农村-累计"])
    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def macro_china_gdp() -> pd.DataFrame:
    """
    东方财富-中国国内生产总值
    http://data.eastmoney.com/cjsj/gdp.html
    :return: 东方财富中国国内生产总值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "20",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "季度",
        "国内生产总值-绝对值",
        "国内生产总值-同比增长",
        "第一产业-绝对值",
        "第一产业-同比增长",
        "第二产业-绝对值",
        "第二产业-同比增长",
        "第三产业-绝对值",
        "第三产业-同比增长",
    ]
    temp_df["国内生产总值-绝对值"] = pd.to_numeric(temp_df["国内生产总值-绝对值"])
    temp_df["国内生产总值-同比增长"] = pd.to_numeric(temp_df["国内生产总值-同比增长"])
    temp_df["第一产业-绝对值"] = pd.to_numeric(temp_df["第一产业-绝对值"])
    temp_df["第一产业-同比增长"] = pd.to_numeric(temp_df["第一产业-同比增长"])
    temp_df["第二产业-绝对值"] = pd.to_numeric(temp_df["第二产业-绝对值"])
    temp_df["第二产业-同比增长"] = pd.to_numeric(temp_df["第二产业-同比增长"])
    temp_df["第三产业-绝对值"] = pd.to_numeric(temp_df["第三产业-绝对值"])
    temp_df["第三产业-同比增长"] = pd.to_numeric(temp_df["第三产业-同比增长"])
    return temp_df


def macro_china_ppi() -> pd.DataFrame:
    """
    东方财富-中国工业品出厂价格指数
    http://data.eastmoney.com/cjsj/ppi.html
    :return: 东方财富中国工业品出厂价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable6912149",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "22",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = ["月份", "当月", "当月同比增长", "累计"]
    return temp_df


def macro_china_pmi() -> pd.DataFrame:
    """
    东方财富-中国采购经理人指数
    http://data.eastmoney.com/cjsj/pmi.html
    :return: 东方财富中国采购经理人指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "21",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "制造业-指数",
        "制造业-同比增长",
        "非制造业-指数",
        "非制造业-同比增长",
    ]
    temp_df["制造业-指数"] = pd.to_numeric(temp_df["制造业-指数"])
    temp_df["制造业-同比增长"] = pd.to_numeric(temp_df["制造业-同比增长"])
    temp_df["非制造业-指数"] = pd.to_numeric(temp_df["非制造业-指数"])
    temp_df["非制造业-同比增长"] = pd.to_numeric(temp_df["非制造业-同比增长"])
    return temp_df


def macro_china_gdzctz() -> pd.DataFrame:
    """
    东方财富-中国城镇固定资产投资
    http://data.eastmoney.com/cjsj/gdzctz.html
    :return: 东方财富中国城镇固定资产投资
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable1891672",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "12",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "自年初累计",
    ]
    return temp_df


def macro_china_hgjck() -> pd.DataFrame:
    """
    东方财富-海关进出口增减情况一览表
    http://data.eastmoney.com/cjsj/hgjck.html
    :return: 东方财富-海关进出口增减情况一览表
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月出口额-金额",
        "当月出口额-同比增长",
        "当月出口额-环比增长",
        "当月进口额-金额",
        "当月进口额-同比增长",
        "当月进口额-环比增长",
        "累计出口额-金额",
        "累计出口额-同比增长",
        "累计进口额-金额",
        "累计进口额-同比增长",
    ]
    temp_df["当月出口额-金额"] = pd.to_numeric(temp_df["当月出口额-金额"])
    temp_df["当月出口额-同比增长"] = pd.to_numeric(temp_df["当月出口额-同比增长"])
    temp_df["当月出口额-环比增长"] = pd.to_numeric(temp_df["当月出口额-环比增长"])
    temp_df["当月进口额-金额"] = pd.to_numeric(temp_df["当月进口额-金额"])
    temp_df["当月进口额-同比增长"] = pd.to_numeric(temp_df["当月进口额-同比增长"])
    temp_df["当月进口额-环比增长"] = pd.to_numeric(temp_df["当月进口额-环比增长"])
    temp_df["累计出口额-金额"] = pd.to_numeric(temp_df["累计出口额-金额"])
    temp_df["累计出口额-同比增长"] = pd.to_numeric(temp_df["累计出口额-同比增长"])
    temp_df["累计进口额-金额"] = pd.to_numeric(temp_df["累计进口额-金额"])
    temp_df["累计进口额-同比增长"] = pd.to_numeric(temp_df["累计进口额-同比增长"])
    return temp_df


def macro_china_czsr() -> pd.DataFrame:
    """
    东方财富-财政收入
    http://data.eastmoney.com/cjsj/czsr.html
    :return: 东方财富-财政收入
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable5011006",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "14",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长",
    ]
    return temp_df


def macro_china_whxd() -> pd.DataFrame:
    """
    东方财富-外汇贷款数据
    http://data.eastmoney.com/cjsj/whxd.html
    :return: 东方财富-外汇贷款数据
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable8618737",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "17",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    return temp_df


def macro_china_wbck() -> pd.DataFrame:
    """
    东方财富-本外币存款
    http://data.eastmoney.com/cjsj/wbck.html
    :return: 东方财富-本外币存款
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable3653904",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "18",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    return temp_df


def macro_china_hb(symbol: str = "weekly") -> pd.DataFrame:
    """
    中国-货币净投放与净回笼
    http://www.chinamoney.com.cn/chinese/hb/
    :param symbol: choice of {"weekly", "monthly"}
    :type symbol: str
    :return: 货币净投放与净回笼
    :rtype: pandas.DataFrame
    """
    import warnings

    warnings.warn("由于目标网站未更新数据，该接口即将移除", DeprecationWarning)

    # if symbol == "weekly":
    #     current_year = datetime.today().year
    #     url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-publish/TicketPutAndBackStatByWeek"
    #     params = {
    #         "t": "1597986289666",
    #         "t": "1597986289666",
    #     }
    #     big_df = pd.DataFrame()
    #     for year in tqdm(range(1997, current_year + 1)):
    #         payload = {
    #             "startWeek": f"{year}-01",
    #             "endWeek": f"{year}-52",
    #             "pageSize": "5000",
    #             "pageNo": "1",
    #         }
    #         r = requests.post(url, params=params, data=payload)
    #         temp_df = pd.DataFrame(r.json()["data"]["resultList"])
    #         big_df = big_df.append(temp_df, ignore_index=True)
    #     big_df = big_df.sort_values(by=["startDate"])
    #     big_df.reset_index(inplace=True, drop=True)
    #     big_df.columns = ["日期", "投放量", "回笼量", "净投放", "开始日期", "结束日期"]
    #     big_df = big_df[["日期", "开始日期", "结束日期", "投放量", "回笼量", "净投放"]]
    #     big_df["开始日期"] = pd.to_datetime(big_df["开始日期"]).dt.date
    #     big_df["结束日期"] = pd.to_datetime(big_df["结束日期"]).dt.date
    #     big_df["投放量"] = pd.to_numeric(big_df["投放量"])
    #     big_df["回笼量"] = pd.to_numeric(big_df["回笼量"])
    #     big_df["净投放"] = pd.to_numeric(big_df["净投放"])
    #     return big_df
    # else:
    #     current_year = datetime.today().year
    #     url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-publish/TicketPutAndBackStatByMonth"
    #     params = {
    #         "t": "1597986289666",
    #         "t": "1597986289666",
    #     }
    #     big_df = pd.DataFrame()
    #     for year in tqdm(range(1997, current_year + 1)):
    #         payload = {
    #             "startMonth": f"{year}-01",
    #             "endMonth": f"{year}-12",
    #             "pageSize": "5000",
    #             "pageNo": "1",
    #         }
    #         r = requests.post(url, params=params, data=payload)
    #         temp_df = pd.DataFrame(r.json()["data"]["resultList"])
    #         big_df = big_df.append(temp_df, ignore_index=True)
    #     big_df.columns = ["日期", "投放量", "回笼量", "净投放", "-", "-"]
    #     big_df = big_df[["日期", "投放量", "回笼量", "净投放"]]
    #     big_df["投放量"] = pd.to_numeric(big_df["投放量"])
    #     big_df["回笼量"] = pd.to_numeric(big_df["回笼量"])
    #     big_df["净投放"] = pd.to_numeric(big_df["净投放"])
    #     return big_df


def macro_china_gksccz() -> pd.DataFrame:
    """
    中国外汇交易中心暨全国银行间同业拆借中心-央行公开市场操作
    http://www.chinamoney.com.cn/chinese/yhgkscczh/
    :return: 央行公开市场操作
    :rtype: pandas.DataFrame
    """
    import warnings

    warnings.warn("由于目标网站未更新数据，该接口即将移除", DeprecationWarning)
    # url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-publish/TicketHandle"
    # params = {
    #     "t": "1597986289666",
    #     "t": "1597986289666",
    # }
    # payload = {
    #     "pageSize": "15",
    #     "pageNo": "1",
    # }
    # headers = {
    #     "Accept": "application/json, text/javascript, */*; q=0.01",
    #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #     "Referer": "https://www.chinamoney.com.cn/chinese/yhgkscczh/",
    #     "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": '"Windows"',
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    #     "X-Requested-With": "XMLHttpRequest",
    # }
    # r = requests.post(url, params=params, data=payload, headers=headers)
    # data_json = r.json()
    # total_page = data_json["data"]["pageTotal"]
    # big_df = pd.DataFrame()
    # for page in tqdm(range(1, total_page + 1)):
    #     payload.update(
    #         {
    #             "pageNo": page,
    #         }
    #     )
    #     r = requests.post(url, params=params, data=payload)
    #     data_json = r.json()
    #     temp_df = pd.DataFrame(data_json["data"]["resultList"])
    #     big_df = big_df.append(temp_df, ignore_index=True)
    # big_df.columns = [
    #     "操作日期",
    #     "期限",
    #     "交易量",
    #     "中标利率",
    #     "正/逆回购",
    # ]
    # big_df["操作日期"] = pd.to_datetime(big_df["操作日期"]).dt.date
    # big_df["期限"] = pd.to_numeric(big_df["期限"])
    # big_df["交易量"] = pd.to_numeric(big_df["交易量"])
    # big_df["中标利率"] = pd.to_numeric(big_df["中标利率"])
    # return big_df


def macro_china_bond_public() -> pd.DataFrame:
    """
    中国-债券信息披露-债券发行
    http://www.chinamoney.com.cn/chinese/xzjfx/
    :return: 债券发行
    :rtype: pandas.DataFrame
    """
    url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-an/bnBondEmit"
    payload = {
        "enty": "",
        "bondType": "",
        "bondNameCode": "",
        "leadUnderwriter": "",
        "pageNo": "1",
        "pageSize": "1000",
        "limit": "1",
    }
    r = requests.post(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "债券全称",
        "债券类型",
        "-",
        "发行日期",
        "-",
        "计息方式",
        "-",
        "债券期限",
        "-",
        "债券评级",
        "-",
        "价格",
        "计划发行量",
    ]
    temp_df = temp_df[
        [
            "债券全称",
            "债券类型",
            "发行日期",
            "计息方式",
            "价格",
            "债券期限",
            "计划发行量",
            "债券评级",
        ]
    ]
    temp_df["价格"] = pd.to_numeric(temp_df["价格"], errors="coerce")
    temp_df["计划发行量"] = pd.to_numeric(temp_df["计划发行量"], errors="coerce")
    return temp_df


def macro_china_xfzxx() -> pd.DataFrame:
    """
    东方财富网-经济数据一览-消费者信心指数
    https://data.eastmoney.com/cjsj/xfzxx.html
    :return: 消费者信心指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625824314514",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "消费者信心指数-指数值",
        "消费者信心指数-同比增长",
        "消费者信心指数-环比增长",
        "消费者满意指数-指数值",
        "消费者满意指数-同比增长",
        "消费者满意指数-环比增长",
        "消费者预期指数-指数值",
        "消费者预期指数-同比增长",
        "消费者预期指数-环比增长",
    ]
    temp_df["消费者信心指数-指数值"] = pd.to_numeric(temp_df["消费者信心指数-指数值"])
    temp_df["消费者信心指数-同比增长"] = pd.to_numeric(temp_df["消费者信心指数-同比增长"])
    temp_df["消费者信心指数-环比增长"] = pd.to_numeric(temp_df["消费者信心指数-环比增长"])
    temp_df["消费者满意指数-指数值"] = pd.to_numeric(temp_df["消费者满意指数-指数值"])
    temp_df["消费者满意指数-同比增长"] = pd.to_numeric(temp_df["消费者满意指数-同比增长"])
    temp_df["消费者满意指数-环比增长"] = pd.to_numeric(temp_df["消费者满意指数-环比增长"])
    temp_df["消费者预期指数-指数值"] = pd.to_numeric(temp_df["消费者满意指数-指数值"])
    temp_df["消费者预期指数-同比增长"] = pd.to_numeric(temp_df["消费者预期指数-同比增长"])
    temp_df["消费者预期指数-环比增长"] = pd.to_numeric(temp_df["消费者预期指数-环比增长"])
    return temp_df


def macro_china_gyzjz() -> pd.DataFrame:
    """
    东方财富网-经济数据-工业增加值增长
    https://data.eastmoney.com/cjsj/gyzjz.html
    :return: 工业增加值增长
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "0",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625824314514",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "同比增长",
        "累计增长",
    ]
    temp_df["同比增长"] = pd.to_numeric(temp_df["同比增长"])
    temp_df["累计增长"] = pd.to_numeric(temp_df["累计增长"])
    return temp_df


def macro_china_reserve_requirement_ratio() -> pd.DataFrame:
    """
    存款准备金率
    https://data.eastmoney.com/cjsj/ckzbj.html
    :return: 存款准备金率
    :rtype: pandas.DataFrame
    """
    url = "https://data.eastmoney.com/DataCenter_V3/Chart/cjsj/reserverequirementratio.ashx"
    params = {
        "r": "0.12301106148653584",
        "isxml": "false",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [
            ["20" + item for item in data_json["X"].split(",")],
            [item for item in data_json["Y"][0].split(",")],
            [item for item in data_json["Y"][1].split(",")],
        ]
    ).T
    temp_df.columns = ["月份", "大型金融机构-调整后", "中小金融机构-调整后"]
    temp_df = temp_df.astype(
        {
            "大型金融机构-调整后": float,
            "中小金融机构-调整后": float,
        }
    )
    return temp_df


def macro_china_consumer_goods_retail() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-社会消费品零售总额
    http://data.eastmoney.com/cjsj/xfp.html
    :return: 社会消费品零售总额
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "5",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625822628225",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
        "累计-同比增长",
    ]
    temp_df["当月"] = pd.to_numeric(temp_df["当月"])
    temp_df["同比增长"] = pd.to_numeric(temp_df["同比增长"])
    temp_df["环比增长"] = pd.to_numeric(temp_df["环比增长"])
    temp_df["累计"] = pd.to_numeric(temp_df["累计"])
    temp_df["累计-同比增长"] = pd.to_numeric(temp_df["累计-同比增长"])
    return temp_df


def macro_china_society_electricity() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-全社会用电分类情况表
    http://finance.sina.com.cn/mac/#industry-6-0-31-1
    :return: 全社会用电分类情况表
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601557771972/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "6",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601557771972",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in range(1, page_num):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.columns = [
        "统计时间",
        "全社会用电量",
        "全社会用电量同比",
        "各行业用电量合计",
        "各行业用电量合计同比",
        "第一产业用电量",
        "第一产业用电量同比",
        "第二产业用电量",
        "第二产业用电量同比",
        "第三产业用电量",
        "第三产业用电量同比",
        "城乡居民生活用电量合计",
        "城乡居民生活用电量合计同比",
        "城镇居民用电量",
        "城镇居民用电量同比",
        "乡村居民用电量",
        "乡村居民用电量同比",
    ]
    return big_df


def macro_china_society_traffic_volume() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-全社会客货运输量
    http://finance.sina.com.cn/mac/#industry-10-0-31-1
    :return: 全社会客货运输量
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601559094538/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "10",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601557771972",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"]["非累计"])
    for i in tqdm(range(1, page_num), leave=False):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"]["非累计"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_postal_telecommunicational() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-邮电业务基本情况
    http://finance.sina.com.cn/mac/#industry-11-0-31-1
    :return: 邮电业务基本情况
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601624495046/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "11",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"]["非累计"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"]["非累计"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    for item in big_df.columns[1:]:
        big_df[item] = pd.to_numeric(big_df[item], errors="coerce")
    return big_df


def macro_china_international_tourism_fx() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-国际旅游外汇收入构成
    http://finance.sina.com.cn/mac/#industry-15-0-31-3
    :return: 国际旅游外汇收入构成
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "15",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_passenger_load_factor() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-民航客座率及载运率
    http://finance.sina.com.cn/mac/#industry-20-0-31-1
    :return: 民航客座率及载运率
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "20",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def _macro_china_freight_index() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-航贸运价指数
    http://finance.sina.com.cn/mac/#industry-22-0-31-2
    :return: 航贸运价指数
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "22",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_freight_index() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-航贸运价指数
    http://finance.sina.com.cn/mac/#industry-22-0-31-2
    :return: 航贸运价指数
    :rtype: pandas.DataFrame
    """
    url = "http://quotes.sina.cn/mac/view/vMacExcle.php"
    params = {
        "cate": "industry",
        "event": "22",
        "from": "0",
        "num": 5000,
        "condition": "",
    }
    r = requests.get(url, params=params)
    columns_list = r.content.decode("gbk").split("\n")[2].split(", ")
    columns_list = [item.strip() for item in columns_list]
    content_list = r.content.decode("gbk").split("\n")[3:]
    big_df = (
        pd.DataFrame(
            [item.split(", ") for item in content_list], columns=columns_list
        )
        .dropna(axis=1, how="all")
        .dropna(axis=0)
        .iloc[:, :-1]
    )
    big_df["波罗的海好望角型船运价指数BCI"] = pd.to_numeric(big_df["波罗的海好望角型船运价指数BCI"])
    big_df["灵便型船综合运价指数BHMI"] = pd.to_numeric(big_df["灵便型船综合运价指数BHMI"])
    big_df["波罗的海超级大灵便型船BSI指数"] = pd.to_numeric(big_df["波罗的海超级大灵便型船BSI指数"])
    big_df["波罗的海综合运价指数BDI"] = pd.to_numeric(big_df["波罗的海综合运价指数BDI"])
    big_df["HRCI国际集装箱租船指数"] = pd.to_numeric(big_df["HRCI国际集装箱租船指数"])
    big_df["油轮运价指数成品油运价指数BCTI"] = pd.to_numeric(big_df["油轮运价指数成品油运价指数BCTI"])
    big_df["油轮运价指数原油运价指数BDTI"] = pd.to_numeric(big_df["油轮运价指数原油运价指数BDTI"])
    return big_df


def macro_china_central_bank_balance() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-央行货币当局资产负债
    http://finance.sina.com.cn/mac/#fininfo-8-0-31-2
    :return: 央行货币当局资产负债
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "8",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_insurance() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-保险业经营情况
    http://finance.sina.com.cn/mac/#fininfo-19-0-31-3
    :return: 保险业经营情况
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "19",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_supply_of_money() -> pd.DataFrame:
    """
    新浪财经-中国宏观经济数据-货币供应量
    http://finance.sina.com.cn/mac/#fininfo-1-0-31-1
    :return: 货币供应量
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "1",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_swap_rate(
    start_date: str = "20220212", end_date: str = "20220312"
) -> pd.DataFrame:
    """
    FR007利率互换曲线历史数据; 只能获取近一年的数据
    http://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007
    :param start_date: 开始日期, 开始和结束日期不得超过一个月
    :type start_date: str
    :param end_date: 结束日期, 开始和结束日期不得超过一个月
    :type end_date: str
    :return: FR007利率互换曲线历史数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bk-shibor/IfccHis"
    params = {
        "cfgItemType": "72",
        "interestRateType": "0",
        "startDate": start_date,
        "endDate": end_date,
        "bidAskType": "",
        "lang": "CN",
        "quoteTime": "全部",
        "pageSize": "5000",
        "pageNum": "1",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "日期",
        "_",
        "_",
        "时刻",
        "_",
        "_",
        "_",
        "_",
        "_",
        "价格类型",
        "_",
        "曲线名称",
        "_",
        "_",
        "_",
        "_",
        "data",
    ]
    price_df = pd.DataFrame([item for item in temp_df["data"]])
    price_df.columns = [
        "1M",
        "3M",
        "6M",
        "9M",
        "1Y",
        "2Y",
        "3Y",
        "4Y",
        "5Y",
        "7Y",
        "10Y",
    ]
    big_df = pd.concat([temp_df, price_df], axis=1)
    big_df = big_df[
        [
            "日期",
            "曲线名称",
            "时刻",
            "价格类型",
            "1M",
            "3M",
            "6M",
            "9M",
            "1Y",
            "2Y",
            "3Y",
            "4Y",
            "5Y",
            "7Y",
            "10Y",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["1M"] = pd.to_numeric(big_df["1M"])
    big_df["3M"] = pd.to_numeric(big_df["3M"])
    big_df["6M"] = pd.to_numeric(big_df["6M"])
    big_df["9M"] = pd.to_numeric(big_df["9M"])
    big_df["1Y"] = pd.to_numeric(big_df["1Y"])
    big_df["2Y"] = pd.to_numeric(big_df["2Y"])
    big_df["3Y"] = pd.to_numeric(big_df["3Y"])
    big_df["4Y"] = pd.to_numeric(big_df["4Y"])
    big_df["5Y"] = pd.to_numeric(big_df["5Y"])
    big_df["7Y"] = pd.to_numeric(big_df["7Y"])
    big_df["10Y"] = pd.to_numeric(big_df["10Y"])
    return big_df


def macro_china_foreign_exchange_gold() -> pd.DataFrame:
    """
    央行黄金和外汇储备
    http://finance.sina.com.cn/mac/#fininfo-5-0-31-2
    :return: 央行黄金和外汇储备
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "5",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_retail_price_index() -> pd.DataFrame:
    """
    商品零售价格指数
    http://finance.sina.com.cn/mac/#price-12-0-31-1
    :return: 商品零售价格指数
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "price",
        "event": "12",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_real_estate() -> pd.DataFrame:
    """
    国房景气指数
    http://data.eastmoney.com/cjsj/hyzs_list_EMM00121987.html
    :return: 国房景气指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMM00121987")',
        "source": "WEB",
        "client": "WEB",
    }
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
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.drop_duplicates(inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


if __name__ == "__main__":
    # 企业商品价格指数
    macro_china_qyspjg_df = macro_china_qyspjg()
    print(macro_china_qyspjg_df)

    # 外商直接投资数据
    macro_china_fdi_df = macro_china_fdi()
    print(macro_china_fdi_df)

    # 社会融资规模增量
    macro_china_shrzgm_df = macro_china_shrzgm()
    print(macro_china_shrzgm_df)

    # 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
    macro_china_gdp_yearly_df = macro_china_gdp_yearly()
    print(macro_china_gdp_yearly_df)

    # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
    macro_china_cpi_yearly_df = macro_china_cpi_yearly()
    print(macro_china_cpi_yearly_df)

    # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI月率报告
    macro_china_cpi_monthly_df = macro_china_cpi_monthly()
    print(macro_china_cpi_monthly_df)

    # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
    macro_china_ppi_yearly_df = macro_china_ppi_yearly()
    print(macro_china_ppi_yearly_df)

    # 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
    macro_china_exports_yoy_df = macro_china_exports_yoy()
    print(macro_china_exports_yoy_df)

    # 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
    macro_china_imports_yoy_df = macro_china_imports_yoy()
    print(macro_china_imports_yoy_df)

    # 金十数据中心-经济指标-中国-贸易状况-以美元计算贸易帐(亿美元)
    macro_china_trade_balance_df = macro_china_trade_balance()
    print(macro_china_trade_balance_df)

    # 金十数据中心-经济指标-中国-产业指标-规模以上工业增加值年率
    macro_china_industrial_production_yoy_df = (
        macro_china_industrial_production_yoy()
    )
    print(macro_china_industrial_production_yoy_df)

    # 金十数据中心-经济指标-中国-产业指标-官方制造业PMI
    macro_china_pmi_yearly_df = macro_china_pmi_yearly()
    print(macro_china_pmi_yearly_df)

    # 金十数据中心-经济指标-中国-产业指标-财新制造业PMI终值
    macro_china_cx_pmi_yearly_df = macro_china_cx_pmi_yearly()
    print(macro_china_cx_pmi_yearly_df)

    # 金十数据中心-经济指标-中国-产业指标-财新服务业PMI
    macro_china_cx_services_pmi_yearly_df = (
        macro_china_cx_services_pmi_yearly()
    )
    print(macro_china_cx_services_pmi_yearly_df)

    # 金十数据中心-经济指标-中国-产业指标-中国官方非制造业PMI
    macro_china_non_man_pmi_df = macro_china_non_man_pmi()
    print(macro_china_non_man_pmi_df)

    # 金十数据中心-经济指标-中国-金融指标-外汇储备(亿美元)
    macro_china_fx_reserves_yearly_df = macro_china_fx_reserves_yearly()
    print(macro_china_fx_reserves_yearly_df)

    # 金十数据中心-经济指标-中国-金融指标-M2货币供应年率
    macro_china_m2_yearly_df = macro_china_m2_yearly()
    print(macro_china_m2_yearly_df)

    # 金十数据中心-经济指标-中国-金融指标-上海银行业同业拆借报告
    macro_china_shibor_all_df = macro_china_shibor_all()
    print(macro_china_shibor_all_df)

    # 金十数据中心-经济指标-中国-金融指标-人民币香港银行同业拆息
    macro_china_hk_market_info_df = macro_china_hk_market_info()
    print(macro_china_hk_market_info_df)

    # 金十数据中心-经济指标-中国-其他-中国日度沿海六大电库存数据
    macro_china_daily_energy_df = macro_china_daily_energy()
    print(macro_china_daily_energy_df)

    # 金十数据中心-经济指标-中国-其他-中国人民币汇率中间价报告
    macro_china_rmb_df = macro_china_rmb()
    print(macro_china_rmb_df)

    # 金十数据中心-经济指标-中国-其他-深圳融资融券报告
    macro_china_market_margin_sz_df = macro_china_market_margin_sz()
    print(macro_china_market_margin_sz_df)

    # 金十数据中心-经济指标-中国-其他-上海融资融券报告
    macro_china_market_margin_sh_df = macro_china_market_margin_sh()
    print(macro_china_market_margin_sh_df)

    # 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
    macro_china_au_report_df = macro_china_au_report()
    print(macro_china_au_report_df)

    # 发改委-中国电煤价格指数-全国综合电煤价格指数
    macro_china_ctci_df = macro_china_ctci()
    print(macro_china_ctci_df)
    # 发改委-中国电煤价格指数-各价区电煤价格指数
    macro_china_ctci_detail_df = macro_china_ctci_detail()
    print(macro_china_ctci_detail_df)
    # 发改委-中国电煤价格指数-历史电煤价格指数
    macro_china_ctci_detail_hist_df = macro_china_ctci_detail_hist()
    print(macro_china_ctci_detail_hist_df)

    # 中国-新房价指数
    macro_china_new_house_price_df = macro_china_new_house_price()
    print(macro_china_new_house_price_df)

    # 中国-企业景气及企业家信心指数
    macro_china_enterprise_boom_index_df = macro_china_enterprise_boom_index()
    print(macro_china_enterprise_boom_index_df)

    # 中国-全国税收收入
    macro_china_national_tax_receipts_df = macro_china_national_tax_receipts()
    print(macro_china_national_tax_receipts_df)

    # 中国-新增信贷数据
    macro_china_new_financial_credit_df = macro_china_new_financial_credit()
    print(macro_china_new_financial_credit_df)

    # 中国-外汇和黄金储备
    macro_china_fx_gold_df = macro_china_fx_gold()
    print(macro_china_fx_gold_df)

    macro_china_stock_market_cap_df = macro_china_stock_market_cap()
    print(macro_china_stock_market_cap_df)

    macro_china_money_supply_df = macro_china_money_supply()
    print(macro_china_money_supply_df)

    macro_china_cpi_df = macro_china_cpi()
    print(macro_china_cpi_df)

    macro_china_gdp_df = macro_china_gdp()
    print(macro_china_gdp_df)

    macro_china_ppi_df = macro_china_ppi()
    print(macro_china_ppi_df)

    macro_china_pmi_df = macro_china_pmi()
    print(macro_china_pmi_df)

    macro_china_gdzctz_df = macro_china_gdzctz()
    print(macro_china_gdzctz_df)

    macro_china_hgjck_df = macro_china_hgjck()
    print(macro_china_hgjck_df)

    macro_china_czsr_df = macro_china_czsr()
    print(macro_china_czsr_df)

    macro_china_whxd_df = macro_china_whxd()
    print(macro_china_whxd_df)

    macro_china_wbck_df = macro_china_wbck()
    print(macro_china_wbck_df)

    macro_china_hb_df = macro_china_hb(symbol="weekly")
    print(macro_china_hb_df)

    macro_china_gksccz_df = macro_china_gksccz()
    print(macro_china_gksccz_df)

    macro_china_bond_public_df = macro_china_bond_public()
    print(macro_china_bond_public_df)

    macro_china_xfzxx_df = macro_china_xfzxx()
    print(macro_china_xfzxx_df)

    macro_china_gyzjz_df = macro_china_gyzjz
    print(macro_china_gyzjz_df)

    macro_china_reserve_requirement_ratio_df = (
        macro_china_reserve_requirement_ratio()
    )
    print(macro_china_reserve_requirement_ratio_df)

    macro_china_consumer_goods_retail_df = macro_china_consumer_goods_retail()
    print(macro_china_consumer_goods_retail_df)

    macro_china_society_electricity_df = macro_china_society_electricity()
    print(macro_china_society_electricity_df)

    macro_china_society_traffic_volume_df = (
        macro_china_society_traffic_volume()
    )
    print(macro_china_society_traffic_volume_df)

    macro_china_postal_telecommunicational_df = (
        macro_china_postal_telecommunicational()
    )
    print(macro_china_postal_telecommunicational_df)

    macro_china_international_tourism_fx_df = (
        macro_china_international_tourism_fx()
    )
    print(macro_china_international_tourism_fx_df)

    macro_china_passenger_load_factor_df = macro_china_passenger_load_factor()
    print(macro_china_passenger_load_factor_df)

    macro_china_freight_index_df = macro_china_freight_index()
    print(macro_china_freight_index_df)

    macro_china_central_bank_balance_df = macro_china_central_bank_balance()
    print(macro_china_central_bank_balance_df)

    macro_china_insurance_df = macro_china_insurance()
    print(macro_china_insurance_df)

    macro_china_supply_of_money_df = macro_china_supply_of_money()
    print(macro_china_supply_of_money_df)

    macro_china_swap_rate_df = macro_china_swap_rate(
        start_date="2020-09-06", end_date="2020-10-06"
    )
    print(macro_china_swap_rate_df)

    macro_china_foreign_exchange_gold_df = macro_china_foreign_exchange_gold()
    print(macro_china_foreign_exchange_gold_df)

    macro_china_retail_price_index_df = macro_china_retail_price_index()
    print(macro_china_retail_price_index_df)

    macro_china_real_estate_df = macro_china_real_estate()
    print(macro_china_real_estate_df)
