# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/9 22:52
contact: jindaxiang@163.com
desc: 金十数据中心-经济指标-央行利率-主要央行利率
https://datacenter.jin10.com/economic
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
import json
import time

import pandas as pd
import requests


# 金十数据中心-经济指标-央行利率-主要央行利率-美联储利率决议报告
def macro_bank_usa_interest_rate():
    """
    美联储利率决议报告, 数据区间从19820927-至今
    https://datacenter.jin10.com/reportType/dc_usa_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_usa_interest_rate_decision_all.js?v=1578581921
    :return: 美联储利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_usa_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国利率决议"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "usa_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-欧洲央行决议报告
def macro_bank_euro_interest_rate():
    """
    欧洲央行决议报告, 数据区间从19990101-至今
    https://datacenter.jin10.com/reportType/dc_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_interest_rate_decision_all.js?v=1578581663
    :return: 欧洲央行决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区利率决议"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "euro_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-新西兰联储决议报告
def macro_bank_newzealand_interest_rate():
    """
    新西兰联储决议报告, 数据区间从19990401-至今
    https://datacenter.jin10.com/reportType/dc_newzealand_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_newzealand_interest_rate_decision_all.js?v=1578582075
    :return: 新西兰联储决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_newzealand_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["新西兰利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "newzealand_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-中国央行决议报告
def macro_bank_china_interest_rate():
    """
    中国人民银行利率报告, 数据区间从19910501-至今
    https://datacenter.jin10.com/reportType/dc_china_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_china_interest_rate_decision_all.js?v=1578582163
    :return: 中国人民银行利率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_china_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国人民银行利率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "china_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-瑞士央行决议报告
def macro_bank_switzerland_interest_rate():
    """
    瑞士央行利率决议报告, 数据区间从20080313-至今
    https://datacenter.jin10.com/reportType/dc_switzerland_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_switzerland_interest_rate_decision_all.js?v=1578582240
    :return: 瑞士央行利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_switzerland_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["瑞士央行利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "switzerland_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-英国央行决议报告
def macro_bank_english_interest_rate():
    """
    英国央行决议报告, 数据区间从19700101-至今
    https://datacenter.jin10.com/reportType/dc_english_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_english_interest_rate_decision_all.js?v=1578582331
    :return: 英国央行决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_english_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["英国利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "english_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-澳洲联储决议报告
def macro_bank_australia_interest_rate():
    """
    澳洲联储决议报告, 数据区间从19800201-至今
    https://datacenter.jin10.com/reportType/dc_australia_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_australia_interest_rate_decision_all.js?v=1578582414
    :return: 澳洲联储决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_australia_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["澳大利亚利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "australia_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-日本央行决议报告
def macro_bank_japan_interest_rate():
    """
    日本利率决议报告, 数据区间从20080214-至今
    https://datacenter.jin10.com/reportType/dc_japan_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_japan_interest_rate_decision_all.js?v=1578582485
    :return: 日本利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_japan_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["日本利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "japan_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-俄罗斯央行决议报告
def macro_bank_russia_interest_rate():
    """
    俄罗斯利率决议报告, 数据区间从20030601-至今
    https://datacenter.jin10.com/reportType/dc_russia_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_russia_interest_rate_decision_all.js?v=1578582572
    :return: 俄罗斯利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_russia_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["俄罗斯利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "russia_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-印度央行决议报告
def macro_bank_india_interest_rate():
    """
    印度利率决议报告, 数据区间从20000801-至今
    https://datacenter.jin10.com/reportType/dc_india_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_india_interest_rate_decision_all.js?v=1578582645
    :return: 印度利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_india_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["印度利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "india_interest_rate"
    return temp_df


# 金十数据中心-经济指标-央行利率-主要央行利率-巴西央行决议报告
def macro_bank_brazil_interest_rate():
    """
    巴西利率决议报告, 数据区间从20080201-至今
    https://datacenter.jin10.com/reportType/dc_brazil_interest_rate_decision
    https://cdn.jin10.com/dc/reports/dc_brazil_interest_rate_decision_all.js?v=1578582718
    :return: 巴西利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_brazil_interest_rate_decision_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["巴西利率决议报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "brazil_interest_rate"
    return temp_df


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
