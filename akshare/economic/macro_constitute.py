#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/1/6 12:08
Desc: 金十数据-数据中心-主要机构-宏观经济
https://datacenter.jin10.com/
"""
import json
import time
import math

import pandas as pd
import requests
from tqdm import tqdm

from akshare.economic.cons import (
    JS_CONS_GOLD_ETF_URL,
    JS_CONS_SLIVER_ETF_URL,
    JS_CONS_OPEC_URL,
)


def macro_cons_gold_volume() -> pd.Series:
    """
    全球最大黄金 ETF—SPDR Gold Trust 持仓报告, 数据区间从 20041118-至今
    https://datacenter.jin10.com/reportType/dc_etf_gold
    :return: 持仓报告
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CONS_GOLD_ETF_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["黄金"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["总库存(吨)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "etf",
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
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)

    for_times = math.ceil(int(str((temp_df.index[-1] - value_df.index[-1])).split(' ')[0]) / 20)
    big_df = temp_df
    big_df.columns = ['总库存']

    for i in tqdm(range(for_times), leave=False):
        params = {
            "max_date": temp_df.index[-1],
            "category": "etf",
            "attr_id": "1",
            "_": str(int(round(t * 1000))),
        }
        r = requests.get(url, params=params, headers=headers)
        temp_df = pd.DataFrame(r.json()["data"]["values"])
        temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
        temp_df = temp_df.iloc[:, 1:]
        temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][1:]
        big_df = big_df.append(temp_df.iloc[:, [0]])

    big_df.dropna(inplace=True)
    big_df.sort_index(inplace=True)
    big_df = big_df.reset_index()
    big_df.drop_duplicates(subset="index", keep="last", inplace=True)
    big_df.set_index("index", inplace=True)
    big_df = big_df.squeeze()
    big_df.index.name = None
    big_df.name = "gold_volume"
    big_df = big_df.astype(float)
    return big_df


def macro_cons_gold_change():
    """
    全球最大黄金 ETF—SPDR Gold Trust 持仓报告, 数据区间从 20041118-至今
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CONS_GOLD_ETF_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["黄金"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["增持/减持(吨)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "etf",
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
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, [0, 2]]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)

    for_times = math.ceil(int(str((temp_df.index[-1] - value_df.index[-1])).split(' ')[0]) / 20)
    big_df = temp_df
    big_df.columns = ['增持/减持']

    for i in tqdm(range(for_times), leave=False):
        params = {
            "max_date": temp_df.index[-1],
            "category": "etf",
            "attr_id": "1",
            "_": str(int(round(t * 1000))),
        }
        r = requests.get(url, params=params, headers=headers)
        temp_df = pd.DataFrame(r.json()["data"]["values"])
        temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
        temp_df = temp_df.iloc[:, 1:]
        temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][1:]
        big_df = big_df.append(temp_df.iloc[:, [1]])

    big_df.dropna(inplace=True)
    big_df.sort_index(inplace=True)
    big_df = big_df.reset_index()
    big_df.drop_duplicates(subset="index", keep="last", inplace=True)
    big_df.set_index("index", inplace=True)

    big_df = big_df.squeeze()
    big_df.index.name = None
    big_df.name = "gold_change"
    big_df = big_df.astype(float)
    return big_df


def macro_cons_gold_amount():
    """
    全球最大黄金 ETF—SPDR Gold Trust 持仓报告, 数据区间从 20041118-至今
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CONS_GOLD_ETF_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["黄金"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["总价值(美元)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "etf",
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
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, [0, 3]]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)

    for_times = math.ceil(int(str((temp_df.index[-1] - value_df.index[-1])).split(' ')[0]) / 20)
    big_df = temp_df
    big_df.columns = ['总价值']

    for i in tqdm(range(for_times), leave=False):
        params = {
            "max_date": temp_df.index[-1],
            "category": "etf",
            "attr_id": "1",
            "_": str(int(round(t * 1000))),
        }
        r = requests.get(url, params=params, headers=headers)
        temp_df = pd.DataFrame(r.json()["data"]["values"])
        temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
        temp_df = temp_df.iloc[:, 1:]
        temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][1:]
        big_df = big_df.append(temp_df.iloc[:, [2]])

    big_df.dropna(inplace=True)
    big_df.sort_index(inplace=True)
    big_df = big_df.reset_index()
    big_df.drop_duplicates(subset="index", keep="last", inplace=True)
    big_df.set_index("index", inplace=True)

    big_df = big_df.squeeze()
    big_df.index.name = None
    big_df.name = "gold_change"
    big_df = big_df.astype(float)
    return big_df


def macro_cons_silver_volume():
    """
    全球最大白银 ETF--iShares Silver Trust 持仓报告, 数据区间从 20060429-至今
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CONS_SLIVER_ETF_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["白银"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["总库存(吨)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "etf",
        "attr_id": "2",
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
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, [0, 1]]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "silver_volume"

    url = "https://cdn.jin10.com/data_center/reports/etf_2.json"
    r = requests.get(url)
    data_json = r.json()
    append_temp_df = pd.DataFrame(data_json["values"]).T
    append_temp_df.columns = [item["name"] for item in data_json["keys"]]
    temp_append_df = append_temp_df["总库存"]
    temp_append_df.name = "silver_volume"

    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df["index"].astype(str)
    temp_df = temp_df.append(temp_append_df.reset_index())
    temp_df.drop_duplicates(subset=["index"], keep="last", inplace=True)
    temp_df.index = pd.to_datetime(temp_df["index"])
    del temp_df["index"]
    temp_df = temp_df[temp_df != 'Show All']
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.astype(float)

    return temp_df


def macro_cons_silver_change():
    """
    全球最大白银ETF--iShares Silver Trust持仓报告, 数据区间从20060429-至今
    :return: pandas.Series
    2006-04-29         0
    2006-05-02      0.00
    2006-05-03    342.11
    2006-05-04    202.15
    2006-05-05    108.86
                   ...
    2019-10-17    -58.16
    2019-10-18      0.00
    2019-10-21    -34.89
    2019-10-22    -61.06
    2019-10-23      0.00
    """
    t = time.time()
    res = requests.get(
        JS_CONS_SLIVER_ETF_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["白银"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["增持/减持(吨)"]
    temp_df.name = "silver_change"
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "etf",
        "attr_id": "2",
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
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, [0, 2]]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "silver_change"

    url = "https://cdn.jin10.com/data_center/reports/etf_2.json"
    r = requests.get(url)
    data_json = r.json()
    append_temp_df = pd.DataFrame(data_json["values"]).T
    append_temp_df.columns = [item["name"] for item in data_json["keys"]]
    temp_append_df = append_temp_df["增持/减持"]
    temp_append_df.name = "silver_change"

    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df["index"].astype(str)
    temp_df = temp_df.append(temp_append_df.reset_index())
    temp_df.drop_duplicates(subset=["index"], keep="last", inplace=True)
    temp_df.index = pd.to_datetime(temp_df["index"])
    del temp_df["index"]
    temp_df = temp_df[temp_df != 'Show All']
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.astype(float)

    return temp_df


def macro_cons_silver_amount():
    """
    全球最大白银ETF--iShares Silver Trust持仓报告, 数据区间从20060429-至今
    :return: pandas.Series
    2006-04-29    263651152
    2006-05-02    263651152
    2006-05-03    445408550
    2006-05-04    555123947
    2006-05-05    574713264
                    ...
    2019-10-17     Show All
    2019-10-18     Show All
    2019-10-21     Show All
    2019-10-22     Show All
    2019-10-23     Show All
    """
    t = time.time()
    res = requests.get(
        JS_CONS_SLIVER_ETF_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["白银"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["总价值(美元)"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "etf",
        "attr_id": "2",
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
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, [0, 3]]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "silver_amount"

    url = "https://cdn.jin10.com/data_center/reports/etf_2.json"
    r = requests.get(url)
    data_json = r.json()
    append_temp_df = pd.DataFrame(data_json["values"]).T
    append_temp_df.columns = [item["name"] for item in data_json["keys"]]
    temp_append_df = append_temp_df["总价值"]
    temp_append_df.name = "silver_amount"

    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df["index"].astype(str)
    temp_df = temp_df.append(temp_append_df.reset_index())
    temp_df.drop_duplicates(subset=["index"], keep="last", inplace=True)
    temp_df.index = pd.to_datetime(temp_df["index"])
    del temp_df["index"]
    temp_df = temp_df[temp_df != 'Show All']
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.astype(float)
    return temp_df


def _macro_cons_opec_month():
    """
    欧佩克报告-月度, 数据区间从 20170118-至今
    这里返回的具体索引日期的数据为上一个月的数据, 由于某些国家的数据有缺失,
    只选择有数据的国家返回
    :return: pandas.Series
                阿尔及利亚    安哥拉  厄瓜多尔    加蓬     伊朗    伊拉克    科威特    利比亚   尼日利亚  \
    2017-01-18  108.0  172.4  54.5  21.3  372.0  463.2  281.2   60.8  154.2
    2017-02-13  104.5  165.1  52.7  19.9  377.5  447.6  271.8   67.5  157.6
    2017-03-14  105.3  164.1  52.6  19.4  381.4  441.4  270.9   66.9  160.8
    2017-04-12  105.6  161.4  52.6  19.8  379.0  440.2  270.2   62.2  154.5
    2017-05-11  104.7  169.2  52.4  20.6  375.9  437.3  270.2   55.0  150.8
    2017-06-13  105.9  161.3  52.8  20.4  379.5  442.4  270.5   73.0  168.0
    2017-07-12  106.0  166.8  52.7  19.7  379.0  450.2  270.9   85.2  173.3
    2017-08-10  105.9  164.6  53.6  20.5  382.4  446.8  270.3  100.1  174.8
    2017-09-12  106.5  164.6  53.7  17.3  382.8  444.8  270.2   89.0  186.1
    2017-10-11  104.6  164.1  53.6  20.1  382.7  449.4  270.0   92.3  185.5
    2017-11-13  101.2  171.1  54.1  20.3  382.3  438.3  270.8   96.2  173.8
    2017-12-13  101.3  158.1  53.3  19.7  381.8  439.6  270.3   97.3  179.0
    2018-01-18  103.7  163.3  52.6  19.7  382.9  440.5  270.0   96.2  186.1
    2018-04-12   98.4  152.4  51.8  18.3  381.4  442.6  270.4   96.8  181.0
    2018-05-14   99.7  151.5  52.0  18.3  382.3  442.9  270.5   98.2  179.1
    2018-06-12  103.1  152.5  51.9  18.9  382.9  445.5  270.1   95.5  171.1
    2018-07-11  103.9  143.1  51.9  19.0  379.9  453.3  273.1   70.8  166.0
    2018-08-13  106.2  145.6  52.5  18.8  373.7  455.6  279.1   66.4  166.7
    2018-09-12  104.5  144.8  52.9  18.7  358.4  464.9  280.2   92.6  172.5
    2018-10-11  104.9  151.9  53.1  18.7  344.7  465.0  281.2  105.3  174.8
    2018-11-13  105.4  153.3  52.5  18.6  329.6  465.4  276.4  111.4  175.1
    2018-12-12  105.2  152.1  52.5  17.6  295.4  463.1  280.9  110.4  173.6
    2019-03-14  102.6  145.7  52.2  20.3  274.3  463.3  270.9   90.6  174.1
    2019-04-10  101.8  145.4  52.4  21.4  269.8  452.2  270.9  109.8  173.3
    2019-06-13  102.9  147.1  52.9  21.1  237.0  472.4  271.0  117.4  173.3
                    沙特    阿联酋   委内瑞拉   欧佩克产量
    2017-01-18  1047.4  307.1  202.1  3308.5
    2017-02-13   994.6  293.1  200.4  3213.9
    2017-03-14   979.7  292.5  198.7  3195.8
    2017-04-12   999.4  289.5  197.2  3192.8
    2017-05-11   995.4  284.2  195.6  3173.2
    2017-06-13   994.0  288.5  196.3  3213.9
    2017-07-12   995.0  289.8  193.8  3261.1
    2017-08-10  1006.7  290.5  193.2  3286.9
    2017-09-12  1002.2  290.1  191.8  3275.5
    2017-10-11   997.5  290.5  189.0  3274.8
    2017-11-13  1000.0  291.1  186.3  3258.9
    2017-12-13   999.6  288.3  183.4  3244.8
    2018-01-18   991.8  287.8  174.5  3241.6
    2018-04-12   993.4  286.4  148.8  3195.8
    2018-05-14   995.9  287.2  143.6  3193.0
    2018-06-12   998.7  286.5  139.2  3186.9
    2018-07-11  1042.0  289.7  134.0  3232.7
    2018-08-13  1038.7  295.9  127.8  3232.3
    2018-09-12  1040.1  297.2  123.5  3256.5
    2018-10-11  1051.2  300.4  119.7  3276.1
    2018-11-13  1063.0  316.0  117.1  3290.0
    2018-12-12  1101.6  324.6  113.7  3296.5
    2019-03-14  1008.7  307.2  100.8  3054.9
    2019-04-10   979.4  305.9   73.2  3002.2
    2019-06-13   969.0  306.1   74.1  2987.6
    """
    t = time.time()
    res = requests.get(
        JS_CONS_OPEC_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    big_df = pd.DataFrame()
    for country in [item["datas"] for item in json_data["list"]][0].keys():
        try:
            value_list = [item["datas"][country] for item in json_data["list"]]
            value_df = pd.DataFrame(value_list)
            value_df.columns = json_data["kinds"]
            value_df.index = pd.to_datetime(date_list)
            temp_df = value_df["上个月"]
            temp_df.name = country
            big_df = big_df.append(temp_df)
        except:
            continue

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_opec_report",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    res = requests.get(f"https://datacenter-api.jin10.com/reports/dates?category=opec&_={str(int(round(t * 1000)))}",
                       headers=headers)  # 日期序列
    all_date_list = res.json()["data"]
    need_date_list = [item for item in all_date_list if
                      item.split("-")[0] + item.split("-")[1] + item.split("-")[2] not in date_list]
    for item in reversed(need_date_list):
        res = requests.get(
            f"https://datacenter-api.jin10.com/reports/list?category=opec&date={item}&_={str(int(round(t * 1000)))}",
            headers=headers)
        temp_df = pd.DataFrame(res.json()["data"]["values"],
                               columns=pd.DataFrame(res.json()["data"]["keys"])["name"].tolist()).T
        temp_df.columns = temp_df.iloc[0, :]
        temp_df = temp_df[['阿尔及利亚', '安哥拉', '厄瓜多尔', '加蓬', '伊朗', '伊拉克', '科威特', '利比亚', '尼日利亚', '沙特',
                           '阿联酋', '委内瑞拉', '欧佩克产量']].iloc[-2, :]
        big_df[item] = temp_df

    return big_df.T


def macro_cons_opec_month():
    """
    欧佩克报告-月度, 数据区间从 20170118-至今
    这里返回的具体索引日期的数据为上一个月的数据, 由于某些国家的数据有缺失
    只选择有数据的国家返回
    20200312:fix:由于 “厄瓜多尔” 已经有几个月没有更新数据，在这里加以剔除
    https://datacenter.jin10.com/reportType/dc_opec_report
    :return: pandas.Series
    """
    t = time.time()
    big_df = pd.DataFrame()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_opec_report",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    res = requests.get(f"https://datacenter-api.jin10.com/reports/dates?category=opec&_={str(int(round(t * 1000)))}",
                       headers=headers)  # 日期序列
    all_date_list = res.json()["data"]
    bar = tqdm(reversed(all_date_list))

    for item in bar:
        bar.set_description(f"Please wait for a moment, now downloading {item}'s data")
        res = requests.get(
            f"https://datacenter-api.jin10.com/reports/list?category=opec&date={item}&_={str(int(round(t * 1000)))}",
            headers=headers)
        temp_df = pd.DataFrame(res.json()["data"]["values"],
                               columns=pd.DataFrame(res.json()["data"]["keys"])["name"].tolist()).T
        temp_df.columns = temp_df.iloc[0, :]
        temp_df = temp_df.iloc[1:, :]
        try:
            temp_df = temp_df[['阿尔及利亚', '安哥拉', '加蓬', '伊朗', '伊拉克', '科威特', '利比亚', '尼日利亚', '沙特',
                               '阿联酋', '委内瑞拉', '欧佩克产量']].iloc[-2, :]
        except:
            temp_df = temp_df[['阿尔及利亚', '安哥拉', '加蓬', '伊朗', '伊拉克', '科威特', '利比亚', '尼日利亚', '沙特',
                               '阿联酋', '委内瑞拉', '欧佩克产量']].iloc[-1, :]
        temp_df.dropna(inplace=True)
        big_df[temp_df.name] = temp_df
    big_df = big_df.T
    big_df.columns.name = "日期"
    big_df = big_df.astype(float)
    return big_df


if __name__ == "__main__":
    macro_cons_gold_volume_df = macro_cons_gold_volume()
    print(macro_cons_gold_volume_df)

    macro_cons_gold_change_df = macro_cons_gold_change()
    print(macro_cons_gold_change_df)

    macro_cons_gold_amount_df = macro_cons_gold_amount()
    print(macro_cons_gold_amount_df)

    print(pd.concat([macro_cons_gold_volume_df, macro_cons_gold_change_df, macro_cons_gold_amount_df], axis=1))

    macro_cons_silver_volume_df = macro_cons_silver_volume()
    print(macro_cons_silver_volume_df)

    macro_cons_silver_change_df = macro_cons_silver_change()
    print(macro_cons_silver_change_df)

    macro_cons_silver_amount_df = macro_cons_silver_amount()
    print(macro_cons_silver_amount_df)

    print(pd.concat([macro_cons_silver_volume_df, macro_cons_silver_change_df, macro_cons_silver_amount_df], axis=1))

    macro_cons_opec_month_df = macro_cons_opec_month()
    print(macro_cons_opec_month_df)
