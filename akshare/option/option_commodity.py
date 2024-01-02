#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/11/17 17:00
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
from typing import Tuple, Any

import pandas as pd
import requests

from akshare.option.cons import (
    get_calendar,
    convert_date,
    DCE_DAILY_OPTION_URL,
    SHFE_OPTION_URL,
    CZCE_DAILY_OPTION_URL_3,
    SHFE_HEADERS,
)


def option_dce_daily(
        symbol: str = "聚乙烯期权", trade_date: str = "20210728"
) -> Tuple[Any, Any]:
    """
    大连商品交易所-期权-日频行情数据
    http://www.dce.com.cn/
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"玉米期权", "豆粕期权", "铁矿石期权", "液化石油气期权", "聚乙烯期权", "聚氯乙烯期权", "聚丙烯期权", "棕榈油期权", "黄大豆1号期权", "黄大豆2号期权", "豆油期权", "乙二醇期权", "苯乙烯期权"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return
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
    table_df = pd.read_excel(BytesIO(res.content), header=1)
    another_df = table_df.iloc[
                 table_df[table_df.iloc[:, 0].str.contains("合约")].iloc[-1].name:,
                 [0, 1],
                 ]
    another_df.reset_index(inplace=True, drop=True)
    another_df.columns = another_df.iloc[0]
    another_df = another_df.iloc[1:, :]
    if symbol == "豆粕期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "豆粕"],
            another_df[another_df.iloc[:, 0].str.contains("m")],
        )
    elif symbol == "玉米期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "玉米"],
            another_df[another_df.iloc[:, 0].str.contains("c")],
        )
    elif symbol == "铁矿石期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "铁矿石"],
            another_df[another_df.iloc[:, 0].str.contains("i")],
        )
    elif symbol == "液化石油气期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "液化石油气"],
            another_df[another_df.iloc[:, 0].str.contains("pg")],
        )
    elif symbol == "聚乙烯期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "聚乙烯"],
            another_df[another_df.iloc[:, 0].str.contains("l")],
        )
    elif symbol == "聚氯乙烯期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "聚氯乙烯"],
            another_df[another_df.iloc[:, 0].str.contains("v")],
        )
    elif symbol == "聚丙烯期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "聚丙烯"],
            another_df[another_df.iloc[:, 0].str.contains("pp")],
        )
    elif symbol == "棕榈油期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "棕榈油"],
            another_df[another_df.iloc[:, 0].str.contains(r"^p\d")],
        )
    elif symbol == "黄大豆1号期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "豆一"],
            another_df[another_df.iloc[:, 0].str.contains("a")],
        )
    elif symbol == "黄大豆2号期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "豆二"],
            another_df[another_df.iloc[:, 0].str.contains("b")],
        )
    elif symbol == "豆油期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "豆油"],
            another_df[another_df.iloc[:, 0].str.contains("y")],
        )
    elif symbol == "乙二醇期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "乙二醇"],
            another_df[another_df.iloc[:, 0].str.contains("eg")],
        )
    elif symbol == "苯乙烯期权":
        result_one_df, result_two_df = (
            table_df[table_df["商品名称"] == "苯乙烯"],
            another_df[another_df.iloc[:, 0].str.contains("eb")],
        )
    result_one_df.reset_index(inplace=True, drop=True)
    result_two_df.reset_index(inplace=True, drop=True)
    result_two_df.columns.name = None
    return result_one_df, result_two_df


def option_czce_daily(
        symbol: str = "白糖期权", trade_date: str = "20191017"
) -> pd.DataFrame:
    """
    郑州商品交易所-期权-日频行情数据

    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"白糖期权", "棉花期权", "甲醇期权", "PTA期权", "菜籽粕期权", "动力煤期权", "菜籽油期权", "花生期权"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("{}非交易日".format(day.strftime("%Y%m%d")))
        return pd.DataFrame()
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
            elif symbol == "菜籽油期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("OI")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "花生期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PK")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "棉花期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("CF")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "短纤期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PF")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "纯碱期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SA")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "锰硅期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SM")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "硅铁期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SF")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            elif symbol == "尿素期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("UR")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
            else:
                temp_df = table_df[table_df.iloc[:, 0].str.contains("AP")]
                temp_df.reset_index(inplace=True, drop=True)
                return temp_df.iloc[:-1, :]
        except:
            return pd.DataFrame()


def option_shfe_daily(
        symbol: str = "铝期权", trade_date: str = "20200827"
) -> pd.DataFrame:
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
        return
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
            contract_df = contract_df[
                [
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
                ]
            ]

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

            volatility_df = volatility_df[
                [
                    "合约系列",
                    "成交量",
                    "持仓量",
                    "持仓量变化",
                    "成交额",
                    "行权量",
                    "隐含波动率",
                ]
            ]
            contract_df.reset_index(inplace=True, drop=True)
            volatility_df.reset_index(inplace=True, drop=True)
            return contract_df, volatility_df
        except:
            return


def option_gfex_daily(symbol: str = "工业硅", trade_date: str = "20230724"):
    """
    广州期货交易所-日频率-量价数据
    http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"工业硅", "碳酸锂"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return
    url = "http://www.gfex.com.cn/u/interfacesWebTiDayQuotes/loadList"
    payload = {"trade_date": day.strftime("%Y%m%d"), "trade_type": "1"}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "32",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.gfex.com.cn",
        "Origin": "http://www.gfex.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "content-type": "application/x-www-form-urlencoded",
    }
    r = requests.post(url, data=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.rename(
        columns={
            "variety": "商品名称",
            "diffI": "持仓量变化",
            "high": "最高价",
            "turnover": "成交额",
            "impliedVolatility": "隐含波动率",
            "diff": "涨跌",
            "delta": "Delta",
            "close": "收盘价",
            "diff1": "涨跌1",
            "lastClear": "前结算价",
            "open": "开盘价",
            "matchQtySum": "行权量",
            "delivMonth": "合约名称",
            "low": "最低价",
            "clearPrice": "结算价",
            "varietyOrder": "品种代码",
            "openInterest": "持仓量",
            "volumn": "成交量",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "商品名称",
            "合约名称",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "前结算价",
            "结算价",
            "涨跌",
            "涨跌1",
            "Delta",
            "成交量",
            "持仓量",
            "持仓量变化",
            "成交额",
            "行权量",
            "隐含波动率",
        ]
    ]
    temp_df = temp_df[temp_df['商品名称'].str.contains(symbol)]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def option_gfex_vol_daily(symbol: str = "碳酸锂", trade_date: str = "20230724"):
    """
    广州期货交易所-日频率-合约隐含波动率
    http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml
    :param symbol: choice of choice of {"工业硅", "碳酸锂"}
    :type symbol: str
    :param trade_date: 交易日
    :type trade_date: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    symbol_code_map = {
        "工业硅": "si",
        "碳酸锂": "lc",
    }
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return
    url = "http://www.gfex.com.cn/u/interfacesWebTiDayQuotes/loadListOptVolatility"
    payload = {"trade_date": day.strftime("%Y%m%d")}
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "32",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.gfex.com.cn",
        "Origin": "http://www.gfex.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "content-type": "application/x-www-form-urlencoded",
    }
    r = requests.post(url, data=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.rename(
        columns={
            "seriesId": "合约系列",
            "varietyId": "-",
            "hisVolatility": "隐含波动率",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "合约系列",
            "隐含波动率",
        ]
    ]
    temp_df = temp_df[temp_df['合约系列'].str.contains(symbol_code_map[symbol])]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    option_czce_daily_df = option_czce_daily(symbol="动力煤期权", trade_date="20220808")
    print(option_czce_daily_df)

    option_dce_daily_one, option_dce_daily_two = option_dce_daily(
        symbol="黄大豆2号期权", trade_date="20220808"
    )
    print(option_dce_daily_one)
    print(option_dce_daily_two)

    option_dce_daily_one, option_dce_daily_two = option_dce_daily(
        symbol="苯乙烯期权", trade_date="20230516"
    )
    print(option_dce_daily_one)
    print(option_dce_daily_two)

    option_dce_daily_one, option_dce_daily_two = option_dce_daily(
        symbol="乙二醇期权", trade_date="20230516"
    )
    print(option_dce_daily_one)
    print(option_dce_daily_two)

    option_shfe_daily_one, option_shfe_daily_two = option_shfe_daily(
        symbol="天胶期权", trade_date="20210312"
    )
    print(option_shfe_daily_one)
    print(option_shfe_daily_two)

    option_gfex_daily_df = option_gfex_daily(symbol="工业硅", trade_date="20240102")
    print(option_gfex_daily_df)

    option_gfex_vol_daily_df = option_gfex_vol_daily(symbol="工业硅", trade_date="20230418")
    print(option_gfex_vol_daily_df)

    option_czce_daily_df = option_czce_daily(symbol="短纤期权", trade_date="20231116")
    print(option_czce_daily_df)
