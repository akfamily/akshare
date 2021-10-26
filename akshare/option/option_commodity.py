#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/29 20:50
Desc: 商品期权数据
说明：
(1) 价格：自2019年12月02日起，纤维板报价单位由元/张改为元/立方米
(2) 价格：元/吨，鸡蛋为元/500千克，纤维板为元/立方米，胶合板为元/张
(3) 成交量、持仓量：手（按双边计算）
(4) 成交额：万元（按双边计算）
(5) 涨跌＝收盘价－前结算价
(6) 涨跌1=今结算价-前结算价
(7) 合约系列：具有相同月份标的期货合约的所有期权合约的统称
(8) 隐含波动率：根据期权市场价格，利用期权定价模型计算的标的期货合约价格波动率
"""
import datetime
import warnings
from io import StringIO, BytesIO

import requests
import pandas as pd

from akshare.option.cons import (
    get_calendar,
    convert_date,
    DCE_DAILY_OPTION_URL,
    SHFE_OPTION_URL,
    CZCE_DAILY_OPTION_URL_3,
    SHFE_HEADERS,
)


def option_dce_daily(trade_date: str = "20210728", symbol: str = "聚乙烯期权") -> pd.DataFrame:
    """
    大连商品交易所-期权-日频行情数据
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"玉米期权", "豆粕期权", "铁矿石期权", "液化石油气期权", "聚乙烯期权", "聚氯乙烯期权", "聚丙烯期权", "棕榈油期权"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    url = DCE_DAILY_OPTION_URL
    payload = {
        "dayQuotes.variety": "all",
        "dayQuotes.trade_type": "1",
        "year": str(day.year),
        "month": str(day.month - 1),
        "day": str(day.day),
        "exportFlag": "excel",
    }
    res = requests.post(url, data=payload)
    table_df = pd.read_excel(BytesIO(res.content), header=0)
    another_df = table_df.iloc[
        table_df[table_df.iloc[:, 0].str.contains("合约")].iloc[-1].name:, [0, 1]
    ]
    another_df.reset_index(inplace=True, drop=True)
    another_df.iloc[0] = another_df.iat[0, 0].split("\t")
    another_df.columns = another_df.iloc[0]
    another_df = another_df.iloc[1:, :]
    if symbol == "豆粕期权":
        return table_df[table_df["商品名称"] == "豆粕"], another_df[another_df.iloc[:, 0].str.contains("m")]
    elif symbol == "玉米期权":
        return table_df[table_df["商品名称"] == "玉米"], another_df[another_df.iloc[:, 0].str.contains("c")]
    elif symbol == "铁矿石期权":
        return table_df[table_df["商品名称"] == "铁矿石"], another_df[another_df.iloc[:, 0].str.contains("i")]
    elif symbol == "液化石油气期权":
        return table_df[table_df["商品名称"] == "液化石油气"], another_df[another_df.iloc[:, 0].str.contains("pg")]
    elif symbol == "聚乙烯期权":
        return table_df[table_df["商品名称"] == "聚乙烯"], another_df[another_df.iloc[:, 0].str.contains("l")]
    elif symbol == "聚氯乙烯期权":
        return table_df[table_df["商品名称"] == "聚氯乙烯"], another_df[another_df.iloc[:, 0].str.contains("v")]
    elif symbol == "聚丙烯期权":
        return table_df[table_df["商品名称"] == "聚丙烯"], another_df[another_df.iloc[:, 0].str.contains("pp")]
    elif symbol == "棕榈油期权":
        return table_df[table_df["商品名称"] == "棕榈油"], another_df[another_df.iloc[:, 0].str.contains(r'^p\d')]


def option_czce_daily(trade_date: str = "20191017", symbol: str = "白糖期权") -> pd.DataFrame:
    """
    郑州商品交易所-期权-日频行情数据
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"白糖期权", "棉花期权", "甲醇期权", "PTA期权", "菜籽粕期权", "动力煤期权"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("{}非交易日".format(day.strftime("%Y%m%d")))
        return None
    if day > datetime.date(2010, 8, 24):
        url = CZCE_DAILY_OPTION_URL_3.format(day.strftime("%Y"), day.strftime("%Y%m%d"))
        try:
            r = requests.get(url)
            f = StringIO(r.text)
            table_df = pd.read_table(f, encoding="utf-8", skiprows=1, sep="|")
            if symbol == "白糖期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SR")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "PTA期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("TA")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "甲醇期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("MA")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "菜籽粕期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("RM")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "动力煤期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("ZC")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            else:
                temp_df = table_df[table_df.iloc[:, 0].str.contains("CF")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
        except:
            return None


def option_shfe_daily(trade_date: str = "20200827", symbol: str = "铝期权") -> pd.DataFrame:
    """
    上海期货交易所-期权-日频行情数据
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"铜期权", "天胶期权", "黄金期权", "铝期权", "锌期权"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    if day > datetime.date(2010, 8, 24):
        url = SHFE_OPTION_URL.format(day.strftime("%Y%m%d"))
        try:
            r = requests.get(url, headers=SHFE_HEADERS)
            json_data = r.json()
            table_df = pd.DataFrame(
                [
                    row
                    for row in json_data["o_curinstrument"]
                    if row["INSTRUMENTID"] not in ["小计", "合计"]
                    and row["INSTRUMENTID"] != ""
                ]
            )
            contract_df = table_df[table_df["PRODUCTNAME"].str.strip() == symbol]
            product_df = pd.DataFrame(json_data["o_curproduct"])
            product_df = product_df[product_df["PRODUCTNAME"].str.strip() == symbol]
            volatility_df = pd.DataFrame(json_data["o_cursigma"])
            volatility_df = volatility_df[
                volatility_df["PRODUCTNAME"].str.strip() == symbol
            ]
            contract_df.columns = [
                "_",
                "_",
                "_",
                "合约代码",
                "前结算价",
                "开盘价",
                "最高价",
                "最低价",
                "收盘价",
                "结算价",
                "涨跌1",
                "涨跌2",
                "成交量",
                "持仓量",
                "持仓量变化",
                "_",
                "行权量",
                "成交额",
                "德尔塔",
                "_",
                "_",
                "_",
                "_",
            ]
            contract_df = contract_df[[
                "合约代码",
                "开盘价",
                "最高价",
                "最低价",
                "收盘价",
                "前结算价",
                "结算价",
                "涨跌1",
                "涨跌2",
                "成交量",
                "持仓量",
                "持仓量变化",
                "成交额",
                "德尔塔",
                "行权量",
            ]]

            volatility_df.columns = [
                "_",
                "_",
                "_",
                "合约系列",
                "成交量",
                "持仓量",
                "持仓量变化",
                "行权量",
                "成交额",
                "隐含波动率",
                "_",
            ]

            volatility_df = volatility_df[[
                "合约系列",
                "成交量",
                "持仓量",
                "持仓量变化",
                "成交额",
                "行权量",
                "隐含波动率",
            ]]
            return contract_df, volatility_df
        except:
            return None


if __name__ == "__main__":
    option_czce_daily_df = option_czce_daily(trade_date="20200817", symbol="动力煤期权")
    print(option_czce_daily_df)

    option_dce_daily_one, option_dce_daily_two = option_dce_daily(trade_date="20210113", symbol="聚乙烯期权")
    print(option_dce_daily_one)
    print(option_dce_daily_two)

    option_shfe_daily_one, option_shfe_daily_two = option_shfe_daily(trade_date="20210312", symbol="天胶期权")
    print(option_shfe_daily_one)
    print(option_shfe_daily_two)
