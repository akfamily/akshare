#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/5/23 14:05
Desc: 东方财富网-数据中心-特色数据-停复牌信息
http://data.eastmoney.com/tfpxx/
"""
import pandas as pd
import requests


def stock_tfp_em(date: str = "20220523") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-停复牌信息
    http://data.eastmoney.com/tfpxx/
    :param date: specific date as "2020-03-19"
    :type date: str
    :return: 停复牌信息表
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "SUSPEND_START_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CUSTOM_SUSPEND_DATA_INTERFACE",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(MARKET="全部")(DATETIME='{"-".join([date[:4], date[4:6], date[6:]])}')""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "代码",
        "名称",
        "停牌时间",
        "停牌截止时间",
        "停牌期限",
        "停牌原因",
        "所属市场",
        "停牌开始日期",
        "预计复牌时间",
        "-",
        "-",
    ]
    temp_df = temp_df[
        ["序号", "代码", "名称", "停牌时间", "停牌截止时间", "停牌期限", "停牌原因", "所属市场", "预计复牌时间"]
    ]
    temp_df["停牌时间"] = pd.to_datetime(temp_df["停牌时间"]).dt.date
    temp_df["停牌截止时间"] = pd.to_datetime(temp_df["停牌截止时间"]).dt.date
    temp_df["预计复牌时间"] = pd.to_datetime(temp_df["预计复牌时间"]).dt.date
    return temp_df


if __name__ == "__main__":
    stock_tfp_em_df = stock_tfp_em(date="20220523")
    print(stock_tfp_em_df)
