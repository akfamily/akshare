#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/6/7 20:30
Desc: 东方财富网-个股数据-派现与募资对比
https://data.eastmoney.com/stockdata/
"""

import pandas as pd
import requests


def stock_dividend_financing_em(symbol: str = "000559") -> pd.DataFrame:
    """
    东方财富网-个股数据-派现与募资对比
    https://data.eastmoney.com/stockdata/
    :param symbol: 股票代码
    :type symbol: str
    :return: 派现与募资对比
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_F10_DIVIDENDNEW_PROFILE",
        "columns": "ALL",
        "quoteColumns": "",
        "pageNumber": "1",
        "source": "WEB",
        "client": "WEB",
        "filter": f'(SECURITY_CODE="{symbol}")',
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    columns = [
        "股票代码",
        "股票简称",
        "累计派现",
        "累计募资",
        "派现次数",
        "融资次数",
        "分红率",
        "股利支付率",
        "派现融资比",
        "首发次数",
        "首发募资",
        "增发次数",
        "增发募资",
        "配股次数",
        "配股募资",
        "优先股次数",
        "优先股募资",
        "债券次数",
        "债券募资",
        "再融资次数",
        "再融资募资",
    ]
    temp_df = pd.DataFrame(columns=columns)
    if data_json["result"] is None:
        return temp_df

    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.rename(
        columns={
            "SECURITY_CODE": "股票代码",
            "SECURITY_NAME_ABBR": "股票简称",
            "TOTAL_DIVIDEND": "累计派现",
            "TOTAL_RAISE_FUND": "累计募资",
            "DIVIDEND_NUM": "派现次数",
            "TOTAL_NUM": "融资次数",
            "DIVIDEND_RATIO": "分红率",
            "DIVIDEND_PAY_RATIO": "股利支付率",
            "DIVIDEND_FINANCE_RATIO": "派现融资比",
            "IPO_NUM": "首发次数",
            "IPO_RAISE_FUND": "首发募资",
            "SEO_NUM": "增发次数",
            "SEO_RAISE_FUND": "增发募资",
            "ALLOTMENT_NUM": "配股次数",
            "ALLOTMENT_RAISE_FUND": "配股募资",
            "PREFERRED_NUM": "优先股次数",
            "PREFERRED_RAISE_FUND": "优先股募资",
            "BOND_NUM": "债券次数",
            "BOND_RAISE_FUND": "债券募资",
            "RF_NUM": "再融资次数",
            "RF_RAISE_FUND": "再融资募资",
        },
        inplace=True,
    )
    temp_df = temp_df[columns]

    amount_columns = [
        "累计派现",
        "累计募资",
        "首发募资",
        "增发募资",
        "配股募资",
        "优先股募资",
        "债券募资",
        "再融资募资",
    ]
    count_columns = [
        "派现次数",
        "融资次数",
        "首发次数",
        "增发次数",
        "配股次数",
        "优先股次数",
        "债券次数",
        "再融资次数",
    ]
    ratio_columns = ["分红率", "股利支付率", "派现融资比"]

    for item in amount_columns + count_columns:
        temp_df[item] = pd.to_numeric(temp_df[item], errors="coerce")
    for item in ratio_columns:
        temp_df[item] = pd.to_numeric(temp_df[item], errors="coerce") * 100

    return temp_df


if __name__ == "__main__":
    stock_dividend_financing_em_df = stock_dividend_financing_em(symbol="000559")
    print(stock_dividend_financing_em_df)
