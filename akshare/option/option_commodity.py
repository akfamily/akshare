# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/14 20:50
Desc: 获取商品期权数据
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


def get_dce_option_daily(trade_date="20200817", symbol="聚丙烯期权"):
    """
    大连商品交易所-期权-日频行情数据
    :param trade_date: str format："20191017"
    :param symbol: str "玉米期权" or "豆粕期权" or "铁矿石期权", or "液化石油气期权" or "聚乙烯期权" or "聚氯乙烯期权" or "聚丙烯期权"
    :return: pandas.DataFrame
    part-1:
            商品名称          合约名称    开盘价    最高价    最低价    收盘价   前结算价    结算价   涨跌  涨跌1  \
    0     玉米  c2001-C-1680  168.5  168.5  168.5  168.5  168.0  167.5  0.5 -0.5
    1     玉米  c2001-C-1700      0    0.0    0.0  148.0  148.0  148.0  0.0  0.0
    2     玉米  c2001-C-1720      0    0.0    0.0  129.0  128.0  129.0  1.0  1.0
    3     玉米  c2001-C-1740    115  115.0  115.0  115.0  108.0  111.0  7.0  3.0
    4     玉米  c2001-C-1760     89   95.5   89.0   95.5   89.0   93.5  6.5  4.5
    ..   ...           ...    ...    ...    ...    ...    ...    ...  ...  ...
    239   玉米  c2009-P-2040      0    0.0    0.0   91.0   88.5   91.0  2.5  2.5
    240   玉米  c2009-P-2060      0    0.0    0.0  106.0  104.0  106.0  2.0  2.0
    241   玉米  c2009-P-2080      0    0.0    0.0  121.5  120.5  121.5  1.0  1.0
    242   玉米  c2009-P-2100      0    0.0    0.0  138.5  137.5  138.5  1.0  1.0
    243   玉米  c2009-P-2120      0    0.0    0.0  155.5  155.5  155.5  0.0  0.0
         Delta 成交量    持仓量 持仓量变化   成交额  行权量
    0     0.98   2    236     0  0.34  0.0
    1     0.96   0    236     0     0  0.0
    2     0.94   0    210     0     0  0.0
    3     0.90  20  1,040     0   2.3  0.0
    4     0.85  12    680     0  1.11  0.0
    ..     ...  ..    ...   ...   ...  ...
    239  -0.70   0     30     0     0  0.0
    240  -0.75   0     50     0     0  0.0
    241  -0.80   0     20     0     0  0.0
    242  -0.84   0     10     0     0  0.0
    243  -0.88   0      0     0     0  0.0

    part-2:
        0   合约系列 隐含波动率(%)
    1  c2001    12.95
    2  c2003     8.74
    3  c2005     8.75
    4  c2007      7.7
    5  c2009     6.85
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
        return table_df[table_df["商品名称"] == "聚乙烯"], another_df[another_df.iloc[:, 0].str.contains("i")]
    elif symbol == "聚氯乙烯期权":
        return table_df[table_df["商品名称"] == "聚氯乙烯"], another_df[another_df.iloc[:, 0].str.contains("v")]
    elif symbol == "聚丙烯期权":
        return table_df[table_df["商品名称"] == "聚丙烯"], another_df[another_df.iloc[:, 0].str.contains("pp")]


def get_czce_option_daily(trade_date="20191017", symbol="白糖期权"):
    """
    郑州商品交易所-期权-日频行情数据
    说明：
    (1) 价格：元/吨
    (2) 成交量、空盘量：手
    (3) 成交额：万元
    (4) 涨跌一：今收盘-昨结算
    (5) 涨跌二：今结算-昨结算
    (6) 隐含波动率：将当日期权合约的结算价代入期权定价模型，反推出来的波动率数值
    :param trade_date: str "20191017"
    :param symbol: str "白糖期权", "棉花期权", "甲醇期权", "PTA期权", "菜籽粕期权"
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


def get_shfe_option_daily(trade_date="20200827", symbol="铝期权"):
    """
    上海期货交易所-期权-日频行情数据
    :param trade_date: str "20191017"
    :param symbol: str "铜期权" or "天胶期权" or "黄金期权" or "铝期权" or "锌期权"
    :return: tuple(pandas.DataFrame)
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
    get_czce_option_daily_df = get_czce_option_daily(trade_date="20200817", symbol="动力煤期权")
    print(get_czce_option_daily_df)
    get_dce_option_daily_one, get_dce_option_daily_two = get_dce_option_daily(trade_date="20210113", symbol="玉米期权")
    print(get_dce_option_daily_one)
    print(get_dce_option_daily_two)
    get_shfe_option_daily_one, get_shfe_option_daily_two = get_shfe_option_daily(trade_date="20210312", symbol="天胶期权")
    print(get_shfe_option_daily_one)
    print(get_shfe_option_daily_two)
