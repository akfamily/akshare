#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/17 18:21
Desc: 金十数据中心-经济指标-央行利率-主要央行利率
https://datacenter.jin10.com/economic
输出数据格式为 float64
美联储利率决议报告
欧洲央行决议报告
新西兰联储决议报告
中国央行决议报告
瑞士央行决议报告
英国央行决议报告
澳洲联储决议报告
日本央行决议报告
俄罗斯央行决议报告
印度央行决议报告
巴西央行决议报告
"""
import datetime
import time

import pandas as pd
import requests


# 金十数据中心-经济指标-央行利率-主要央行利率-美联储利率决议报告
def macro_bank_usa_interest_rate() -> pd.DataFrame:
    """
    美联储利率决议报告, 数据区间从 19820927-至今
    https://datacenter.jin10.com/reportType/dc_usa_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_usa_interest_rate_decision_all.js?v=1578581921
    :return: 美联储利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "24",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "美联储利率决议"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-欧洲央行决议报告
def macro_bank_euro_interest_rate() -> pd.DataFrame:
    """
    欧洲央行决议报告, 数据区间从 19990101-至今
    https://datacenter.jin10.com/reportType/dc_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_interest_rate_decision_all.js?v=1578581663
    :return: 欧洲央行决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "21",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "欧元区利率决议"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-新西兰联储决议报告
def macro_bank_newzealand_interest_rate() -> pd.DataFrame:
    """
    新西兰联储决议报告, 数据区间从 19990401-至今
    https://datacenter.jin10.com/reportType/dc_newzealand_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_newzealand_interest_rate_decision_all.js?v=1578582075
    :return: 新西兰联储决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "23",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "新西兰利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-中国央行决议报告
def macro_bank_china_interest_rate() -> pd.DataFrame:
    """
    中国人民银行利率报告, 数据区间从 19910501-至今
    https://datacenter.jin10.com/reportType/dc_china_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_china_interest_rate_decision_all.js?v=1578582163
    :return: 中国人民银行利率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "91",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "中国人民银行利率报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-瑞士央行决议报告
def macro_bank_switzerland_interest_rate() -> pd.DataFrame:
    """
    瑞士央行利率决议报告, 数据区间从 20080313-至今
    https://datacenter.jin10.com/reportType/dc_switzerland_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_switzerland_interest_rate_decision_all.js?v=1578582240
    :return: 瑞士央行利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "25",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "瑞士央行利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-英国央行决议报告
def macro_bank_english_interest_rate() -> pd.DataFrame:
    """
    英国央行决议报告, 数据区间从 19700101-至今
    https://datacenter.jin10.com/reportType/dc_english_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_english_interest_rate_decision_all.js?v=1578582331
    :return: 英国央行决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "26",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "英国利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-澳洲联储决议报告
def macro_bank_australia_interest_rate() -> pd.DataFrame:
    """
    澳洲联储决议报告, 数据区间从 19800201-至今
    https://datacenter.jin10.com/reportType/dc_australia_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_australia_interest_rate_decision_all.js?v=1578582414
    :return: 澳洲联储决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "27",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "澳大利亚利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-日本央行决议报告
def macro_bank_japan_interest_rate() -> pd.DataFrame:
    """
    日本利率决议报告, 数据区间从 20080214-至今
    https://datacenter.jin10.com/reportType/dc_japan_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_japan_interest_rate_decision_all.js?v=1578582485
    :return: 日本利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "22",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "日本利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-俄罗斯央行决议报告
def macro_bank_russia_interest_rate() -> pd.DataFrame:
    """
    俄罗斯利率决议报告, 数据区间从 20030601-至今
    https://datacenter.jin10.com/reportType/dc_russia_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_russia_interest_rate_decision_all.js?v=1578582572
    :return: 俄罗斯利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "64",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "俄罗斯利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-印度央行决议报告
def macro_bank_india_interest_rate() -> pd.DataFrame:
    """
    印度利率决议报告, 数据区间从 20000801-至今
    https://datacenter.jin10.com/reportType/dc_india_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_india_interest_rate_decision_all.js?v=1578582645
    :return: 印度利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "68",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "印度利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-巴西央行决议报告
def macro_bank_brazil_interest_rate() -> pd.DataFrame:
    """
    巴西利率决议报告, 数据区间从 20080201-至今
    https://datacenter.jin10.com/reportType/dc_brazil_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_brazil_interest_rate_decision_all.js?v=1578582718
    :return: 巴西利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "55",
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = big_df.append(temp_df, ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = "巴西利率决议报告"
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    return big_df


if __name__ == "__main__":
    # 金十数据中心-经济指标-央行利率-主要央行利率-美联储利率决议报告
    macro_bank_usa_interest_rate_df = macro_bank_usa_interest_rate()
    print(macro_bank_usa_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-欧洲央行决议报告
    macro_bank_euro_interest_rate_df = macro_bank_euro_interest_rate()
    print(macro_bank_euro_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-新西兰联储决议报告
    macro_bank_newzealand_interest_rate_df = macro_bank_newzealand_interest_rate()
    print(macro_bank_newzealand_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-中国央行决议报告
    macro_bank_china_interest_rate_df = macro_bank_china_interest_rate()
    print(macro_bank_china_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-瑞士央行决议报告
    macro_bank_switzerland_interest_rate_df = macro_bank_switzerland_interest_rate()
    print(macro_bank_switzerland_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-英国央行决议报告
    macro_bank_english_interest_rate_df = macro_bank_english_interest_rate()
    print(macro_bank_english_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-澳洲联储决议报告
    macro_bank_australia_interest_rate_df = macro_bank_australia_interest_rate()
    print(macro_bank_australia_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-日本央行决议报告
    macro_bank_japan_interest_rate_df = macro_bank_japan_interest_rate()
    print(macro_bank_japan_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-俄罗斯央行决议报告
    macro_bank_russia_interest_rate_df = macro_bank_russia_interest_rate()
    print(macro_bank_russia_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-印度央行决议报告
    macro_bank_india_interest_rate_df = macro_bank_india_interest_rate()
    print(macro_bank_india_interest_rate_df)

    # 金十数据中心-经济指标-央行利率-主要央行利率-巴西央行决议报告
    macro_bank_brazil_interest_rate_df = macro_bank_brazil_interest_rate()
    print(macro_bank_brazil_interest_rate_df)
