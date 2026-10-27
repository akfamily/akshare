#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/28
Desc: 百度股市通-经济数据
https://finance.baidu.com/calendar
"""

import pandas as pd
from akshare.utils.baidu_finance import _baidu_finance_calendar


def _process_economic_data(data_list: list) -> pd.DataFrame:
    """处理经济数据"""
    if not data_list:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_list)
    rename_dict = {
        "date": "日期",
        "time": "时间",
        "title": "事件",
        "star": "重要性",
        "formerVal": "前值",
        "pubVal": "公布",
        "region": "地区",
        "indicateVal": "预期",
        "country": "国家",
        "timePeriod": "统计周期",
    }
    temp_df.rename(columns=rename_dict, inplace=True)
    required_cols = ["公布", "预期", "前值", "重要性"]
    for col in required_cols:
        if col not in temp_df.columns:
            temp_df[col] = None
    available_cols = []
    for col in [
        "日期",
        "时间",
        "国家",
        "地区",
        "事件",
        "统计周期",
        "公布",
        "预期",
        "前值",
        "重要性",
    ]:
        if col in temp_df.columns:
            available_cols.append(col)
    if available_cols:
        temp_df = temp_df[available_cols]
    for col in ["公布", "预期", "前值", "重要性"]:
        if col in temp_df.columns:
            temp_df[col] = pd.to_numeric(temp_df[col], errors="coerce")
    if "日期" in temp_df.columns:
        temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date

    return temp_df


def news_economic_baidu(date: str = "20251126", cookie: str = None) -> pd.DataFrame:
    """
    百度股市通-经济数据
    https://finance.baidu.com/calendar
    :param date: 查询日期 (格式：YYYYMMDD)
    :param cookie: cookie
    :return: 经济数据 pd.DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="economic_data",
        process_func=_process_economic_data,
        cookie=cookie,
    )


if __name__ == "__main__":
    news_economic_baidu_df = news_economic_baidu(date="20251126")
    print(news_economic_baidu_df)
