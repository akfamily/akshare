# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/4/29 14:30
Desc: 基金数据-新发基金-新成立基金
http://fund.eastmoney.com/data/xinfound.html
"""
import requests
from akshare.utils import demjson
import pandas as pd


def fund_em_new_found():
    """
    基金数据-新发基金-新成立基金
    http://fund.eastmoney.com/data/xinfound.html
    :return: 新成立基金
    :rtype: pandas.DataFrame
    """
    url = 'http://fund.eastmoney.com/data/FundNewIssue.aspx'
    params = {
        't': 'xcln',
        'sort': 'jzrgq,desc',
        'y': '',
        'page': '1,5000',
        'isbuy': '1',
        'v': '0.4069919776543214',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text.strip("var newfunddata="))
    temp_df = pd.DataFrame(data_json['datas'])
    temp_df.columns = [
        "基金代码",
        "基金简称",
        "发行公司",
        "_",
        "基金类型",
        "募集份额",
        "成立日期",
        "成立来涨幅",
        "基金经理",
        "申购状态",
        "集中认购期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "优惠费率",
    ]
    temp_df = temp_df[[
        "基金代码",
        "基金简称",
        "发行公司",
        "基金类型",
        "集中认购期",
        "募集份额",
        "成立日期",
        "成立来涨幅",
        "基金经理",
        "申购状态",
        "优惠费率",
    ]]
    return temp_df


if __name__ == '__main__':
    fund_em_new_found_df = fund_em_new_found()
    print(fund_em_new_found_df)
