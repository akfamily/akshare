# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc:
"""
import datetime
import warnings

import requests
import pandas as pd

from akshare.option.cons import (DCE_OPTION_URL,
                                 DCE_PAYLOAD,
                                 DCE_DAILY_OPTION_URL,
                                 SHFE_OPTION_URL)
from akshare.futures import cons

calendar = cons.get_calendar()


def get_dce_option_daily(trade_date="20191017", symbol_type="玉米期权"):
    """
    获取大连商品交易所-期权-日频行情数据
    :param trade_date: str format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param symbol_type: str "玉米期权"
    :return: pandas.DataFrame
        symbol        合约代码
        trade_date          日期
        open          开盘价
        high          最高价
        low           最低价
        close         收盘价
        pre_settle      前结算价
        settle         结算价
        delta          对冲值
        volume         成交量
        open_interest     持仓量
        oi_change       持仓变化
        turnover        成交额
        implied_volatility 隐含波动率
        exercise_volume   行权量
        variety        合约类别
或 None(给定日期没有交易数据)
    """
    day = cons.convert_date(trade_date) if trade_date is not None else datetime.trade_date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % day.strftime('%Y%m%d'))
        return None
    url = DCE_DAILY_OPTION_URL
    payload = {
        "dayQuotes.variety": "all",
        "dayQuotes.trade_type": "1",
        "year": "2019",
        "month": "9",
        "day": "17",
        "exportFlag": "txt"
    }
    res = requests.post(url, data=payload)
    with open("temp.txt", "w") as f:
        f.write(res.text)
    table_df = pd.read_table("temp.txt", encoding="gbk", skiprows=2, header=None, sep=r"\t\t", engine="python")
    another_df = table_df.iloc[table_df[table_df.iloc[:, 0].str.contains("合约")].iloc[-1].name:, [0, 1]]
    another_df.reset_index(inplace=True, drop=True)
    another_df.iloc[0] = another_df.iat[0, 0].split("\t")
    another_df.columns = another_df.iloc[0]
    another_df = another_df.iloc[1:, :]

    table_df = table_df.join(table_df.iloc[:, 1].str.split(r"\t", expand=True), lsuffix="l")
    table_df.columns = ["商品名称", "_", "最高价", "最低价", "收盘价", "前结算价", "结算价", "涨跌", "涨跌1", "Delta", "成交量", "持仓量", "持仓量变化", "成交额", "行权量", "合约名称", "开盘价"]
    table_df = table_df[["商品名称", "合约名称", "开盘价", "最高价", "最低价", "收盘价", "前结算价", "结算价", "涨跌", "涨跌1", "Delta", "成交量", "持仓量", "持仓量变化", "成交额", "行权量"]]
    table_df.dropna(axis=1, how="all", inplace=True)
    product_one_df = table_df.iloc[:table_df[table_df.iloc[:, 0].str.contains("小计")].iloc[0].name, :]
    product_two_df = table_df.iloc[table_df[table_df.iloc[:, 0].str.contains("小计")].iloc[0].name+1:table_df[table_df.iloc[:, 0].str.contains("小计")].iloc[1].name, :]
    if symbol_type == "玉米期权":
        return product_one_df, another_df[another_df.iloc[:, 0].str.contains("c")]
    else:
        return product_two_df, another_df[another_df.iloc[:, 0].str.contains("m")]


def get_czce_option_daily(trade_date="20191017", symbol_type="白糖期权"):
    """
    获取郑州商品交易所-期权-日频行情数据
    :param trade_date: str "20191017"
    :param symbol_type: str "白糖期权"
    :return: pandas.DataFrame
    郑商所每日期权交易数据
             品种代码        昨结算         今开盘         最高价         最低价         今收盘      \
    0    CF001C10800  1,579.00    0.00        0.00        0.00        0.00
    1    CF001C11000  1,392.00    0.00        0.00        0.00        0.00
    2    CF001C11200  1,211.00    0.00        0.00        0.00        0.00
    3    CF001C11400  1,038.00    1,396.00    1,396.00    1,396.00    1,396.00
    4    CF001C11600  874.00      0.00        0.00        0.00        0.00
    ..           ...         ...         ...         ...         ...         ...
    398   SR009P5900  576.00      0.00        0.00        0.00        0.00
    399   SR009P6000  653.00      0.00        0.00        0.00        0.00
    400    小计
    401    SR合计
    402    总计
            今结算        涨跌1         涨跌2           成交量(手)     空盘量         增减量      \
    0    1,866.00    287.00      287.00      0           0           0
    1    1,672.00    280.00      280.00      0           0           0
    2    1,481.00    270.00      270.00      0           4           0
    3    1,295.00    358.00      257.00      2           68          0
    4    1,114.00    240.00      240.00      0           224         0
    ..          ...         ...         ...         ...         ...         ...
    398  580.00      4.00        4.00        0           0           0
    399  658.00      5.00        5.00        0           0           0
    400                                      656         860         400
    401                                      32,098      276,900     2252
    402                                      110,664     474,154     14770
         成交额(万元)  DELTA            隐含波动率  行权量
    0       0.00  0.9765      22.29         0
    1       0.00  0.9621      21.84         0
    2       0.00  0.9423      21.38         0
    3       1.40  0.9155      20.91         0
    4       0.00  0.8800      20.45         0
    ..       ...         ...         ...  ...
    398     0.00  -0.6639     16.24         0
    399     0.00  -0.7007     16.58         0
    400    97.28                            0
    401  2138.41                            0
    402  8769.52                            2
    """
    # date = "20191017"
    day = cons.convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % day.strftime('%Y%m%d'))
        return None
    if day > datetime.date(2010, 8, 24):
        if day > datetime.date(2015, 9, 19):
            u = cons.CZCE_DAILY_OPTION_URL_3
            url = u % (day.strftime('%Y'), day.strftime('%Y%m%d'))
        try:
            r = requests.get(url)
            html = r.text
            with open("temp.txt", "w") as f:
                f.write(html)
            table_df = pd.read_table("temp.txt", encoding="gbk", skiprows=1, sep="|")
            if symbol_type == "白糖期权":
                return table_df[table_df.iloc[:, 0].str.contains("SR")]
            else:
                return table_df[table_df["品种代码"].str.contains("CF")]
        except:
            return None


def get_shfe_option_daily(trade_date="20191017", symbol_type="铜期权"):
    day = cons.convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % day.strftime('%Y%m%d'))
        return None
    if day > datetime.date(2010, 8, 24):
        if day > datetime.date(2015, 9, 19):
            url = SHFE_OPTION_URL.format(day.strftime('%Y%m%d'))
        try:
            r = requests.get(url, headers=cons.shfe_headers)
            json_data = r.json()
            table_df = pd.DataFrame([row for row in json_data['o_curinstrument'] if row['INSTRUMENTID'] not in ['小计', '合计'] and row['INSTRUMENTID'] != ''])
            contract_df = table_df[table_df["PRODUCTNAME"].str.strip() == symbol_type]
            product_df = pd.DataFrame(json_data['o_curproduct'])
            product_df = product_df[product_df["PRODUCTNAME"].str.strip() == symbol_type]
            volatility_df = pd.DataFrame(json_data['o_cursigma'])
            volatility_df = volatility_df[volatility_df["PRODUCTNAME"].str.strip() == symbol_type]
            return contract_df, product_df, volatility_df
        except:
            return None


if __name__ == "__main__":
    # df_test = get_czce_option_daily(trade_date="20191017", symbol_type="白糖期权")
    # print(df_test)
    one, two = get_dce_option_daily(trade_date="20191017", symbol_type="玉米期权")
    print(one)
    print(two)
    # one, two, three = get_shfe_option_daily(trade_date="20191017", symbol_type="天胶期权")
    # print(one)
    # print(two)
    # print(three)
