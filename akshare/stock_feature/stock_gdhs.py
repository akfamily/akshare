# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/6/5 18:17
Desc: 东方财富网-数据中心-特色数据-股东户数
http://data.eastmoney.com/gdhs/
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_zh_a_gdhs() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股东户数
    http://data.eastmoney.com/gdhs/
    :return: 股东户数
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "HOLD_NOTICE_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_HOLDERNUMLATEST",
        "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,END_DATE,INTERVAL_CHRATE,AVG_MARKET_CAP,AVG_HOLD_NUM,TOTAL_MARKET_CAP,TOTAL_A_SHARES,HOLD_NOTICE_DATE,HOLDER_NUM,PRE_HOLDER_NUM,HOLDER_NUM_CHANGE,HOLDER_NUM_RATIO,END_DATE,PRE_END_DATE",
        "quoteColumns": "f2,f3",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page_num in tqdm(range(1, total_page_num + 1)):
        params = {
            "sortColumns": "HOLD_NOTICE_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": page_num,
            "reportName": "RPT_HOLDERNUMLATEST",
            "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,END_DATE,INTERVAL_CHRATE,AVG_MARKET_CAP,AVG_HOLD_NUM,TOTAL_MARKET_CAP,TOTAL_A_SHARES,HOLD_NOTICE_DATE,HOLDER_NUM,PRE_HOLDER_NUM,HOLDER_NUM_CHANGE,HOLDER_NUM_RATIO,END_DATE,PRE_END_DATE",
            "quoteColumns": "f2,f3",
            "source": "WEB",
            "client": "WEB",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        "代码",
        "名称",
        "股东户数统计截止日-本次",
        "区间涨跌幅",
        "户均持股市值",
        "户均持股数量",
        "总市值",
        "总股本",
        "公告日期",
        "股东户数-本次",
        "股东户数-上次",
        "股东户数-增减",
        "股东户数-增减比例",
        "股东户数统计截止日-上次",
        "最新价",
        "涨跌幅",
    ]
    big_df = big_df[
        [
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "股东户数-本次",
            "股东户数-上次",
            "股东户数-增减",
            "股东户数-增减比例",
            "区间涨跌幅",
            "股东户数统计截止日-本次",
            "股东户数统计截止日-上次",
            "户均持股市值",
            "户均持股数量",
            "总市值",
            "总股本",
            "公告日期",
        ]
    ]
    big_df['股东户数统计截止日-本次'] = pd.to_datetime(big_df['股东户数统计截止日-本次']).dt.date
    big_df['股东户数统计截止日-上次'] = pd.to_datetime(big_df['股东户数统计截止日-上次']).dt.date
    big_df['公告日期'] = pd.to_datetime(big_df['公告日期']).dt.date
    return big_df


if __name__ == "__main__":
    stock_zh_a_gdhs_df = stock_zh_a_gdhs()
    print(stock_zh_a_gdhs_df)
