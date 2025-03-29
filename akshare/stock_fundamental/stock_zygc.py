# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/9/3 16:30
Desc: 主营构成
https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/Index?type=web&code=SH688041#
https://f10.emoney.cn/f10/zbyz/1000001
"""

from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_zygc_ym(symbol: str = "000001") -> pd.DataFrame:
    """
    益盟-F10-主营构成
    https://f10.emoney.cn/f10/zbyz/1000001
    :param symbol: 股票代码
    :type symbol: str
    :return: 主营构成
    :rtype: pandas.DataFrame
    """
    url = f"http://f10.emoney.cn/f10/zygc/{symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    year_list = [
        item.text.strip()
        for item in soup.find(attrs={"class": "swlab_t"}).find_all("li")
    ]
    big_df = pd.DataFrame()
    for i, item in enumerate(year_list, 2):
        temp_df = pd.read_html(StringIO(r.text), header=0)[i]
        temp_df.columns = [
            "分类方向",
            "分类",
            "营业收入",
            "营业收入-同比增长",
            "营业收入-占主营收入比",
            "营业成本",
            "营业成本-同比增长",
            "营业成本-占主营成本比",
            "毛利率",
            "毛利率-同比增长",
        ]
        temp_df["报告期"] = item
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df = big_df[
        [
            "报告期",
            "分类方向",
            "分类",
            "营业收入",
            "营业收入-同比增长",
            "营业收入-占主营收入比",
            "营业成本",
            "营业成本-同比增长",
            "营业成本-占主营成本比",
            "毛利率",
            "毛利率-同比增长",
        ]
    ]
    return big_df


def stock_zygc_em(symbol: str = "SH688041") -> pd.DataFrame:
    """
    东方财富网-个股-主营构成
    https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/Index?type=web&code=SH688041#
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :return: 主营构成
    :rtype: pandas.DataFrame
    """
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/PageAjax"
    params = {"code": symbol}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["zygcfx"])
    temp_df.rename(
        columns={
            "SECUCODE": "-",
            "SECURITY_CODE": "股票代码",
            "REPORT_DATE": "报告日期",
            "MAINOP_TYPE": "分类类型",
            "ITEM_NAME": "主营构成",
            "MAIN_BUSINESS_INCOME": "主营收入",
            "MBI_RATIO": "收入比例",
            "MAIN_BUSINESS_COST": "主营成本",
            "MBC_RATIO": "成本比例",
            "MAIN_BUSINESS_RPOFIT": "主营利润",
            "MBR_RATIO": "利润比例",
            "GROSS_RPOFIT_RATIO": "毛利率",
            "RANK": "-",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "股票代码",
            "报告日期",
            "分类类型",
            "主营构成",
            "主营收入",
            "收入比例",
            "主营成本",
            "成本比例",
            "主营利润",
            "利润比例",
            "毛利率",
        ]
    ]
    temp_df["报告日期"] = pd.to_datetime(temp_df["报告日期"], errors="coerce").dt.date
    temp_df["分类类型"] = temp_df["分类类型"].map(
        {"2": "按产品分类", "3": "按地区分类"}
    )
    temp_df["主营收入"] = pd.to_numeric(temp_df["主营收入"], errors="coerce")
    temp_df["收入比例"] = pd.to_numeric(temp_df["收入比例"], errors="coerce")
    temp_df["主营成本"] = pd.to_numeric(temp_df["主营成本"], errors="coerce")
    temp_df["成本比例"] = pd.to_numeric(temp_df["成本比例"], errors="coerce")
    temp_df["主营利润"] = pd.to_numeric(temp_df["主营利润"], errors="coerce")
    temp_df["利润比例"] = pd.to_numeric(temp_df["利润比例"], errors="coerce")
    temp_df["毛利率"] = pd.to_numeric(temp_df["毛利率"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_zygc_ym_df = stock_zygc_ym(symbol="000338")
    print(stock_zygc_ym_df)

    stock_zygc_em_df = stock_zygc_em(symbol="SH688041")
    print(stock_zygc_em_df)
