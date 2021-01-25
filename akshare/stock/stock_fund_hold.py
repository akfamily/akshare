# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/25 20:09
Desc: 东方财富网-数据中心-主力数据-基金持仓
http://data.eastmoney.com/zlsj/2020-06-30-1-2.html
"""
import demjson
import pandas as pd
import requests


def stock_report_fund_hold(symbol: str = "基金持仓", date: str = "20201231") -> pd.DataFrame:
    """
    东方财富网-数据中心-主力数据-基金持仓
    http://data.eastmoney.com/zlsj/2020-12-31-1-2.html
    :param symbol: choice of {"基金持仓", "QFII持仓", "社保持仓", "券商持仓", "保险持仓", "信托持仓"}
    :type symbol: str
    :param date: 财报发布日期, xxxx-03-31, xxxx-06-30, xxxx-09-30, xxxx-12-31
    :type date: str
    :return: 基金持仓数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "基金持仓": "1",
        "QFII持仓": "2",
        "社保持仓": "3",
        "券商持仓": "4",
        "保险持仓": "5",
        "信托持仓": "6",
    }
    date = "-".join([date[:4], date[4:6], date[6:]])
    url = "http://data.eastmoney.com/dataapi/zlsj/list"
    params = {
        "tkn": "eastmoney",
        "ReportDate": date,
        "code": "",
        "type": symbol_map[symbol],
        "zjc": "0",
        "sortField": "Count",
        "sortDirec": "1",
        "pageNum": "1",
        "pageSize": "50000",
        "cfg": "jjsjtj",
        "p": "1",
        "pageNo": "1",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df)+1))
    if temp_df.empty:
        return None
    temp_df.columns = [
        "序号",
        "股票代码",
        "股票简称",
        "_",
        "_",
        "_",
        "持有基金家数",
        "持股变化",
        "持股总数",
        "持股市值",
        "持股变动比例",
        "_",
        "持股变动数值",
        "_",
    ]
    temp_df = temp_df[[
        "序号",
        "股票代码",
        "股票简称",
        "持有基金家数",
        "持股总数",
        "持股市值",
        "持股变化",
        "持股变动数值",
        "持股变动比例",
    ]]
    return temp_df


def stock_report_fund_hold_detail(symbol: str = "005827", date: str = "20201231") -> pd.DataFrame:
    """
    东方财富网-数据中心-主力数据-基金持仓-明细
    http://data.eastmoney.com/zlsj/ccjj/2020-12-31-008286.html
    :param symbol: 基金代码
    :type symbol: str
    :param date: 财报发布日期, xxxx-03-31, xxxx-06-30, xxxx-09-30, xxxx-12-31
    :type date: str
    :return: 基金持仓-明细数据
    :rtype: pandas.DataFrame
    """
    date = "-".join([date[:4], date[4:6], date[6:]])
    url = "http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/ZLCCMX/GetZLCCMX"
    params = {
        "js": "datatable8848106",
        "tkn": "eastmoney",
        "SHType": "1",
        "SHCode": symbol,
        "SCode": "",
        "ReportDate": date,
        "sortField": "SCode",
        "sortDirec": "1",
        "pageNum": "1",
        "pageSize": "500",
        "cfg": "ZLCCMX",
        "_": "1611579153269",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):-1])
    temp_df = pd.DataFrame(data_json["Data"][0])
    temp_df = temp_df["Data"].str.split("|", expand=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "股票代码",
        "股票简称",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "持股数",
        "持股市值",
        "占总股本比例",
        "占流通股本比例",
    ]
    temp_df = temp_df[[
        "序号",
        "股票代码",
        "股票简称",
        "持股数",
        "持股市值",
        "占总股本比例",
        "占流通股本比例",
    ]]
    return temp_df


if __name__ == "__main__":
    for item in ["基金持仓", "QFII持仓", "社保持仓", "券商持仓", "保险持仓", "信托持仓"]:
        stock_report_fund_hold_df = stock_report_fund_hold(symbol=item, date="20201231")
        print(stock_report_fund_hold_df)
        break

    stock_report_fund_hold_detail_df = stock_report_fund_hold_detail(symbol="005827", date="20201231")
    print(stock_report_fund_hold_detail_df)
