# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/21 12:08
Desc: 获取金十数据-数据中心-主要机构-宏观经济
"""
import json
import time

import pandas as pd
import requests
from tqdm import tqdm

from akshare.economic.cons import (
    JS_CONS_GOLD_ETF_URL,
    JS_CONS_SLIVER_ETF_URL,
    JS_CONS_OPEC_URL,
)


def macro_cons_gold_volume():
    """
    全球最大黄金ETF—SPDR Gold Trust持仓报告, 数据区间从20041118-至今
    :return: pandas.Series
    2004-11-18      8.09
    2004-11-19     57.85
    2004-11-22     87.09
    2004-11-23     87.09
    2004-11-24     96.42
                   ...
    2019-10-20    924.64
    2019-10-21    924.64
    2019-10-22    919.66
    2019-10-23    918.48
    2019-10-24    918.48
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
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "gold_volume"
    temp_df = temp_df.astype(float)
    return temp_df


def macro_cons_gold_change():
    """
    全球最大黄金ETF—SPDR Gold Trust持仓报告, 数据区间从20041118-至今
    :return: pandas.Series
    2004-11-18        0
    2004-11-19    49.76
    2004-11-22    29.24
    2004-11-23     0.00
    2004-11-24     9.33
                  ...
    2019-10-20     0.00
    2019-10-21     0.00
    2019-10-22    -4.98
    2019-10-23    -1.18
    2019-10-24     0.00
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
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "gold_change"
    temp_df = temp_df.astype(float)
    return temp_df


def macro_cons_gold_amount():
    """
    全球最大黄金ETF—SPDR Gold Trust持仓报告, 数据区间从20041118-至今
    :return: pandas.Series
    2004-11-18      114920000.00
    2004-11-19      828806907.20
    2004-11-22     1253785205.50
    2004-11-23     1254751438.19
    2004-11-24     1390568824.08
                       ...
    2019-10-20    44286078486.23
    2019-10-21    44333677232.68
    2019-10-22    43907962483.56
    2019-10-23    44120217405.82
    2019-10-24    44120217405.82
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
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "gold_amount"
    temp_df = temp_df.astype(float)
    return temp_df


def macro_cons_silver_volume():
    """
    全球最大白银ETF--iShares Silver Trust持仓报告, 数据区间从20060429-至今
    :return: pandas.Series
    2006-04-29      653.17
    2006-05-02      653.17
    2006-05-03      995.28
    2006-05-04     1197.43
    2006-05-05     1306.29
                    ...
    2019-10-17    11847.91
    2019-10-18    11847.91
    2019-10-21    11813.02
    2019-10-22    11751.96
    2019-10-23    11751.96
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


def macro_cons_opec_near_change():
    """
    欧佩克报告-变动, 数据区间从20170118-至今
    :return: pandas.Series
                阿尔及利亚    安哥拉   厄瓜多尔     加蓬     伊朗     伊拉克    科威特    利比亚   尼日利亚  \
    2017-01-18  -0.87   3.56  -0.25  -0.87   0.95    4.26   0.20   3.13 -11.35
    2017-02-13  -4.17  -2.32  -1.67  -1.00   5.02  -16.57 -14.12   6.47  10.18
    2017-03-14  -0.02  -1.82  -0.44  -0.69   3.61   -6.20  -0.93  -1.11   5.80
    2017-04-12   0.45  -1.87  -0.28   0.19  -2.87   -0.85  -0.95  -6.08  -2.98
    2017-05-11  -0.75   9.71  -0.06   0.88  -3.47   -3.91   0.03  -6.16   5.08
    2017-06-13   0.96  -5.42   0.22  -0.13   0.45    4.44   0.00  17.82  17.42
    2017-07-12  -0.09   6.60  -0.21  -0.77   1.67    6.06  -0.02  12.70   9.67
    2017-08-10  -0.10  -1.93   0.85   0.71   0.69   -3.31  -0.74  15.43   3.43
    2017-09-12   0.41   0.83  -0.03  -3.23  -0.23   -2.31   0.01 -11.23  13.83
    2017-10-11  -0.85  -0.29  -0.05   1.44   0.09    3.16  -0.17   5.39   5.08
    2017-11-13  -3.84   6.98   0.71   0.18  -1.13  -13.10  -0.37   4.23  -5.44
    2017-12-13   1.41 -10.87  -0.51  -0.47  -0.22    0.10  -0.53   0.61   9.58
    2018-01-18   3.03   4.48  -0.72  -0.01   1.32    0.79  -0.25  -0.70   7.57
    2018-04-12  -4.95  -8.17   0.26  -0.91   0.33   -1.31   0.23  -3.72   1.82
    2018-05-14   1.77  -0.78   0.31  -0.93   1.00   -0.07   0.08   0.69  -0.83
    2018-06-12   3.90   1.40   0.06   0.18   0.56    2.77  -0.57  -2.43  -5.35
    2018-07-11   0.46  -8.83  -0.09   0.35  -2.27    7.15   2.73 -25.43   2.78
    2018-08-13   1.38   1.17   0.42  -0.34  -5.63    2.41   7.85  -5.67   7.05
    2018-09-12  -1.40  -0.80   0.40  18.80 -15.00    9.00   0.80  25.60   7.40
    2018-10-11  -0.80   5.70  53.10  -0.10 -15.00    0.80   0.60  10.30   2.60
    2018-11-13  -0.40   2.20  -0.30   0.30 -15.60  465.30  -3.30   6.00  -1.70
    2018-12-12  -0.50   0.30   0.10  -1.10 -38.00   -2.30   4.50  -1.10  -3.00
    2019-03-14   0.20   2.20   0.50   0.70   1.20   -7.00  -1.40   2.30   1.00
    2019-04-10  -0.70   0.70  52.40   0.90  -2.80  -12.60  -0.10  19.60   1.10
    2019-06-13   0.60   7.40  -0.10   2.30 -22.70    9.40   1.30  -0.30  -9.20
                   沙特    阿联酋   委内瑞拉  欧佩克产量
    2017-01-18 -14.93  -0.63  -4.52 -22.09
    2017-02-13 -49.62 -15.93  -3.05 -89.02
    2017-03-14  -6.81  -3.69  -1.60 -13.95
    2017-04-12   4.16  -3.27  -2.59 -15.27
    2017-05-11   4.92  -6.23  -2.60  -1.82
    2017-06-13   0.23  -1.80  -0.77  33.61
    2017-07-12   5.13  -0.07  -1.36  39.35
    2017-08-10   3.18  -0.67  -1.58  17.26
    2017-09-12  -1.03  -2.02  -3.19  -7.91
    2017-10-11  -0.07  -0.84  -5.19   8.85
    2017-11-13   1.69  -0.60  -4.36 -15.09
    2017-12-13  -4.54  -3.55  -4.16 -13.35
    2018-01-18  -1.09  -0.70  -8.22   4.24
    2018-04-12  -4.69   4.49  -5.53 -20.14
    2018-05-14   4.65   0.61  -4.17   1.21
    2018-06-12   8.55  -0.63  -4.25   3.54
    2018-07-11  40.54   3.51  -4.75  17.34
    2018-08-13  -5.28   6.92  -4.77   4.07
    2018-09-12   3.80   1.20  -3.60  27.80
    2018-10-11  10.80   3.00  -4.20  13.20
    2018-11-13  12.70  14.20  -4.00  12.70
    2018-12-12  37.70   7.10  -5.20  -1.10
    2019-03-14  -8.60  -0.40 -14.20 -22.10
    2019-04-10 -32.40  -0.90 -28.90 -53.40
    2019-06-13  -7.60   0.30  -3.50 -23.60
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
    bar = tqdm(reversed(all_date_list[:-1]))

    for item in bar:
        bar.set_description(f"Please wait for a moment, now downing {item}'s data")
        res = requests.get(
            f"https://datacenter-api.jin10.com/reports/list?category=opec&date={item}&_={str(int(round(t * 1000)))}",
            headers=headers)
        temp_df = pd.DataFrame(res.json()["data"]["values"],
                               columns=pd.DataFrame(res.json()["data"]["keys"])["name"].tolist()).T
        temp_df.columns = temp_df.iloc[0, :]
        temp_df = temp_df.iloc[1:, :]
        try:
            temp_df = temp_df[['阿尔及利亚', '安哥拉', '加蓬', '伊朗', '伊拉克', '科威特', '利比亚', '尼日利亚', '沙特',
                               '阿联酋', '委内瑞拉', '欧佩克产量']].iloc[-1, :]
        except:
            temp_df = temp_df[['阿尔及利亚', '安哥拉', '加蓬', '伊朗', '伊拉克', '科威特', '利比亚', '尼日利亚', '沙特',
                               '阿联酋', '委内瑞拉', '欧佩克产量']].iloc[-1, :]
        big_df[temp_df.name] = temp_df
    big_df = big_df.T
    big_df.columns.name = "日期"
    big_df = big_df.astype(float)
    return big_df


def _macro_cons_opec_month():
    """
    欧佩克报告-月度, 数据区间从20170118-至今
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
        bar.set_description(f"Please wait for a moment, now downing {item}'s data")
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
    macro_cons_opec_near_change_df = macro_cons_opec_near_change()
    print(macro_cons_opec_near_change_df)
    macro_cons_opec_month_df = macro_cons_opec_month()
    print(macro_cons_opec_month_df)
