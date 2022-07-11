#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/1/20 11:34
Desc: 巨潮资讯-首页-数据-预约披露
http://www.cninfo.com.cn/new/commonUrl?url=data/yypl
"""
import pandas as pd
import requests


def stock_report_disclosure(
    market: str = "科创板", period: str = "2019年报"
) -> pd.DataFrame:
    """
    巨潮资讯-首页-数据-预约披露
    http://www.cninfo.com.cn/new/commonUrl?url=data/yypl
    :param market: choice of {"沪深": "szsh", "深市": "sz", "深主板": "szmb", "中小板": "szsme", "创业板": "szcn", "沪市": "sh", "沪主板": "shmb", "科创板": "shkcp"}
    :type market: str
    :param period: 最近四期的财报
    :type period: str
    :return: 指定 market 和 period 的数据
    :rtype: pandas.DataFrame
    """
    market_map = {
        "沪深": "szsh",
        "深市": "sz",
        "深主板": "szmb",
        "中小板": "szsme",
        "创业板": "szcn",
        "沪市": "sh",
        "沪主板": "shmb",
        "科创板": "shkcp",
    }
    year = period[:4]
    period_map = {
        f"{year}一季": f"{year}-03-31",
        f"{year}半年报": f"{year}-06-30",
        f"{year}三季": f"{year}-09-30",
        f"{year}年报": f"{year}-12-31",
    }
    url = "http://www.cninfo.com.cn/new/information/getPrbookInfo"
    params = {
        "sectionTime": period_map[period],
        "firstTime": "",
        "lastTime": "",
        "market": market_map[market],
        "stockCode": "",
        "orderClos": "",
        "isDesc": "",
        "pagesize": "10000",
        "pagenum": "1",
    }
    r = requests.post(url, params=params)
    text_json = r.json()
    temp_df = pd.DataFrame(text_json["prbookinfos"])
    temp_df.columns = [
        "股票代码",
        "股票简称",
        "首次预约",
        "实际披露",
        "初次变更",
        "二次变更",
        "三次变更",
        "报告期",
        "组织码",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "首次预约",
            "初次变更",
            "二次变更",
            "三次变更",
            "实际披露",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_report_disclosure_df = stock_report_disclosure(market="沪深", period="2020年报")
    print(stock_report_disclosure_df)
