# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/29 13:04
Desc: 中国外汇交易中心暨全国银行间同业拆借中心-回购定盘利率-历史数据
"""
import pandas as pd
import requests


def repo_rate_hist(start_date: str = "20200930", end_date: str = "20201029") -> pd.DataFrame:
    """
    中国外汇交易中心暨全国银行间同业拆借中心-回购定盘利率-历史数据
    http://www.chinamoney.com.cn/chinese/bkfrr/
    :param start_date: 开始时间, 开始时间与结束时间需要在一个月内
    :type start_date: str
    :param end_date: 结束时间, 开始时间与结束时间需要在一个月内
    :type end_date: str
    :return: 回购定盘利率-历史数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/FrrHis"
    params = {
        "lang": "CN",
        "startDate": start_date,
        "endDate": end_date,
        "pageSize": "5000",
    }
    r = requests.post(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df = pd.DataFrame([item for item in temp_df["frValueMap"].to_list()])
    temp_df = temp_df[[
        "date",
        "FR001",
        "FR007",
        "FR014",
        "FDR001",
        "FDR007",
        "FDR014",
    ]]
    return temp_df


if __name__ == '__main__':
    repo_rate_hist_df = repo_rate_hist(start_date="20200830", end_date="20200929")
    print(repo_rate_hist_df)
