#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/11/8 17:17
Desc: 东方财富网-数据中心-特色数据-股东户数
http://data.eastmoney.com/gdhs/
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_zh_a_gdhs(symbol: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股东户数
    http://data.eastmoney.com/gdhs/
    :param symbol: choice of {"最新", "每个季度末"}
    :type symbol: str
    :return: 股东户数
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    if symbol == "最新":
        params = {
            "sortColumns": "HOLD_NOTICE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": "500",
            "pageNumber": "1",
            "reportName": "RPT_HOLDERNUMLATEST",
            "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,END_DATE,INTERVAL_CHRATE,AVG_MARKET_CAP,AVG_HOLD_NUM,TOTAL_MARKET_CAP,TOTAL_A_SHARES,HOLD_NOTICE_DATE,HOLDER_NUM,PRE_HOLDER_NUM,HOLDER_NUM_CHANGE,HOLDER_NUM_RATIO,END_DATE,PRE_END_DATE",
            "quoteColumns": "f2,f3",
            "source": "WEB",
            "client": "WEB",
        }
    else:
        params = {
            "sortColumns": "HOLD_NOTICE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": "500",
            "pageNumber": "1",
            "reportName": "RPT_HOLDERNUM_DET",
            "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,END_DATE,INTERVAL_CHRATE,AVG_MARKET_CAP,AVG_HOLD_NUM,TOTAL_MARKET_CAP,TOTAL_A_SHARES,HOLD_NOTICE_DATE,HOLDER_NUM,PRE_HOLDER_NUM,HOLDER_NUM_CHANGE,HOLDER_NUM_RATIO,END_DATE,PRE_END_DATE",
            "quoteColumns": "f2,f3",
            "source": "WEB",
            "client": "WEB",
            'filter': f"(END_DATE='{symbol[:4] + '-' +  symbol[4:6] + '-' +  symbol[6:]}')",
        }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page_num in tqdm(range(1, total_page_num + 1), leave=False):
        params.update({
            "pageNumber": page_num,
        })
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
    big_df['最新价'] = pd.to_numeric(big_df['最新价'], errors="coerce")
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'], errors="coerce")
    big_df['股东户数-本次'] = pd.to_numeric(big_df['股东户数-本次'], errors="coerce")
    big_df['股东户数-上次'] = pd.to_numeric(big_df['股东户数-上次'], errors="coerce")
    big_df['股东户数-增减'] = pd.to_numeric(big_df['股东户数-增减'], errors="coerce")
    big_df['股东户数-增减比例'] = pd.to_numeric(big_df['股东户数-增减比例'], errors="coerce")
    big_df['区间涨跌幅'] = pd.to_numeric(big_df['区间涨跌幅'], errors="coerce")
    big_df['股东户数统计截止日-本次'] = pd.to_datetime(big_df['股东户数统计截止日-本次']).dt.date
    big_df['股东户数统计截止日-上次'] = pd.to_datetime(big_df['股东户数统计截止日-上次']).dt.date
    big_df['户均持股市值'] = pd.to_numeric(big_df['户均持股市值'])
    big_df['户均持股数量'] = pd.to_numeric(big_df['户均持股数量'])
    big_df['总市值'] = pd.to_numeric(big_df['总市值'])
    big_df['总股本'] = pd.to_numeric(big_df['总股本'])
    big_df['公告日期'] = pd.to_datetime(big_df['公告日期']).dt.date
    return big_df


def stock_zh_a_gdhs_detail_em(symbol: str = "000002") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股东户数详情
    https://data.eastmoney.com/gdhs/detail/000002.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 股东户数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'sortColumns': 'END_DATE',
        'sortTypes': '-1',
        'pageSize': '500',
        'pageNumber': '1',
        'reportName': 'RPT_HOLDERNUM_DET',
        'columns': 'SECURITY_CODE,SECURITY_NAME_ABBR,CHANGE_SHARES,CHANGE_REASON,END_DATE,INTERVAL_CHRATE,AVG_MARKET_CAP,AVG_HOLD_NUM,TOTAL_MARKET_CAP,TOTAL_A_SHARES,HOLD_NOTICE_DATE,HOLDER_NUM,PRE_HOLDER_NUM,HOLDER_NUM_CHANGE,HOLDER_NUM_RATIO,END_DATE,PRE_END_DATE',
        'quoteColumns': 'f2,f3',
        'filter': f'(SECURITY_CODE="{symbol}")',
        'source': 'WEB',
        'client': 'WEB',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page_num in tqdm(range(1, total_page_num + 1), leave=False):
        params.update({
            "pageNumber": page_num,
        })
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        "代码",
        "名称",
        "股本变动",
        "股本变动原因",
        "股东户数统计截止日",
        "区间涨跌幅",
        "户均持股市值",
        "户均持股数量",
        "总市值",
        "总股本",
        "股东户数公告日期",
        "股东户数-本次",
        "股东户数-上次",
        "股东户数-增减",
        "股东户数-增减比例",
        "-",
        "-",
        "-",
    ]
    big_df = big_df[
        [
            "股东户数统计截止日",
            "区间涨跌幅",
            "股东户数-本次",
            "股东户数-上次",
            "股东户数-增减",
            "股东户数-增减比例",
            "户均持股市值",
            "户均持股数量",
            "总市值",
            "总股本",
            "股本变动",
            "股本变动原因",
            "股东户数公告日期",
            "代码",
            "名称",
        ]
    ]
    big_df['区间涨跌幅'] = pd.to_numeric(big_df['区间涨跌幅'], errors="coerce")
    big_df['股东户数-本次'] = pd.to_numeric(big_df['股东户数-本次'], errors="coerce")
    big_df['股东户数-上次'] = pd.to_numeric(big_df['股东户数-上次'], errors="coerce")
    big_df['股东户数-增减'] = pd.to_numeric(big_df['股东户数-增减'], errors="coerce")
    big_df['股东户数-增减比例'] = pd.to_numeric(big_df['股东户数-增减比例'], errors="coerce")
    big_df['户均持股市值'] = pd.to_numeric(big_df['户均持股市值'])
    big_df['户均持股数量'] = pd.to_numeric(big_df['户均持股数量'])
    big_df['总市值'] = pd.to_numeric(big_df['总市值'])
    big_df['总股本'] = pd.to_numeric(big_df['总股本'])
    big_df['股本变动'] = pd.to_numeric(big_df['股本变动'])
    big_df['股东户数统计截止日'] = pd.to_datetime(big_df['股东户数统计截止日']).dt.date
    big_df['股东户数公告日期'] = pd.to_datetime(big_df['股东户数公告日期']).dt.date
    return big_df


if __name__ == "__main__":
    stock_zh_a_gdhs_df = stock_zh_a_gdhs(symbol='20210930')
    print(stock_zh_a_gdhs_df)

    stock_zh_a_gdhs_detail_em_df = stock_zh_a_gdhs_detail_em(symbol="000002")
    print(stock_zh_a_gdhs_detail_em_df)
