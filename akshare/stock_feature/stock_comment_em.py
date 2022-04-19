#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/4/15 15:28
Desc: 东方财富网-数据中心-特色数据-千股千评
http://data.eastmoney.com/stockcomment/
"""
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime


def stock_comment_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-千股千评
    http://data.eastmoney.com/stockcomment/
    :return: 千股千评数据
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "SECURITY_CODE",
        "sortTypes": "1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_DMSK_TS_STOCKNEW",
        "quoteColumns": "f2~01~SECURITY_CODE~CLOSE_PRICE,f8~01~SECURITY_CODE~TURNOVERRATE,f3~01~SECURITY_CODE~CHANGE_RATE,f9~01~SECURITY_CODE~PE_DYNAMIC",
        "columns": "ALL",
        "filter": "",
        "token": "894050c76af8597a853f5b408b759f5d",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "代码",
        "-",
        "交易日",
        "名称",
        "-",
        "-",
        "-",
        "最新价",
        "涨跌幅",
        "-",
        "换手率",
        "主力成本",
        "市盈率",
        "-",
        "-",
        "机构参与度",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "综合得分",
        "上升",
        "目前排名",
        "关注指数",
        "-",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "换手率",
            "市盈率",
            "主力成本",
            "机构参与度",
            "综合得分",
            "上升",
            "目前排名",
            "关注指数",
            "交易日",
        ]
    ]

    big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["换手率"] = pd.to_numeric(big_df["换手率"], errors="coerce")
    big_df["市盈率"] = pd.to_numeric(big_df["市盈率"], errors="coerce")
    big_df["主力成本"] = pd.to_numeric(big_df["主力成本"], errors="coerce")
    big_df["机构参与度"] = pd.to_numeric(big_df["机构参与度"], errors="coerce")
    big_df["综合得分"] = pd.to_numeric(big_df["综合得分"], errors="coerce")
    big_df["上升"] = pd.to_numeric(big_df["上升"], errors="coerce")
    big_df["目前排名"] = pd.to_numeric(big_df["目前排名"], errors="coerce")
    big_df["关注指数"] = pd.to_numeric(big_df["关注指数"], errors="coerce")
    big_df["交易日"] = pd.to_datetime(big_df["交易日"]).dt.date
    return big_df


def stock_comment_detail_zlkp_jgcyd_em(symbol: str = "600000") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度
    https://data.eastmoney.com/stockcomment/stock/600000.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 主力控盘-机构参与度
    :rtype: pandas.DataFrame
    """
    url = f"https://data.eastmoney.com/stockcomment/api/{symbol}.json"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame([data_json['ApiResults']['zlkp']['jgcyd']['XData'], data_json['ApiResults']['zlkp']['jgcyd']['Ydata']['JGCYD']]).T
    temp_df.columns = ['date', 'value']
    temp_df['date'] = str(datetime.now().year) + '-' + temp_df['date']
    temp_df['date'] = pd.to_datetime(temp_df['date']).dt.date
    temp_df.sort_values(['date'], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    temp_df['value'] = pd.to_numeric(temp_df['value'])
    return temp_df


if __name__ == "__main__":
    stock_comment_em_df = stock_comment_em()
    print(stock_comment_em_df)

    stock_comment_detail_zlkp_jgcyd_em_df = stock_comment_detail_zlkp_jgcyd_em(symbol="600000")
    print(stock_comment_detail_zlkp_jgcyd_em_df)
