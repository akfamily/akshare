# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
date: 2020/11/20 14:02
desc: 东方财富网-数据中心-特色数据-机构调研
http://data.eastmoney.com/jgdy/
东方财富网-数据中心-特色数据-机构调研-机构调研统计: http://data.eastmoney.com/jgdy/tj.html
东方财富网-数据中心-特色数据-机构调研-机构调研详细: http://data.eastmoney.com/jgdy/xx.html
"""
import json

import pandas as pd
import requests


def stock_em_jgdy_tj():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研统计
    http://data.eastmoney.com/jgdy/tj.html
    :return: pandas.DataFrame
    """
    url = "http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/JGDYHZ/GetJGDYMX"
    params = {
        "js": "datatable8554018",
        "tkn": "eastmoney",
        "secuCode": "",
        "sortfield": "0",
        "sortdirec": "1",
        "pageNum": "1",
        "pageSize": "50000",
        "cfg": "jgdyhz",
        "p": "1",
        "pageNo": "1",
        "_": "1605855456546",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split("|") for item in data_json["Data"][0]["Data"]])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df) + 1))
    temp_df.columns = [
        "序号",
        "_",
        "_",
        "_",
        "_",
        "接待机构数量",
        "代码",
        "名称",
        "公告日期",
        "接待日期",
        "_",
        "接待地点",
        "接待方式",
        "_",
        "_",
        "_",
        "接待人员",
        "_",
        "涨跌幅",
        "最新价",
        "_",
    ]

    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "接待机构数量",
            "接待方式",
            "接待人员",
            "接待地点",
            "接待日期",
            "公告日期",
        ]
    ]
    return temp_df


def stock_em_jgdy_detail():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研详细
    http://data.eastmoney.com/jgdy/xx.html
    :return: 机构调研详细
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/JGDYMX/GetJGDYMX"
    params = {
        "js": "datatable8554018",
        "tkn": "eastmoney",
        "secuCode": "",
        "dateTime": "",
        "sortfield": "0",
        "sortdirec": "1",
        "pageNum": "1",
        "pageSize": "50000",
        "cfg": "jgdymx",
        "p": "1",
        "pageNo": "1",
        "_": "1605855456546",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split("|") for item in data_json["Data"][0]["Data"]])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df) + 1))
    temp_df.columns = [
        "序号",
        "_",
        "_",
        "_",
        "调研机构",
        "_",
        "代码",
        "名称",
        "公告日期",
        "调研日期",
        "_",
        "接待地点",
        "接待方式",
        "_",
        "机构类型",
        "调研人员",
        "接待人员",
        "_",
        "涨跌幅",
        "最新价",
    ]

    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "调研机构",
            "机构类型",
            "调研人员",
            "接待方式",
            "接待人员",
            "接待地点",
            "调研日期",
            "公告日期",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_em_jgdy_tj_df = stock_em_jgdy_tj()
    print(stock_em_jgdy_tj_df)
    stock_em_jgdy_detail_df = stock_em_jgdy_detail()
    print(stock_em_jgdy_detail_df)
