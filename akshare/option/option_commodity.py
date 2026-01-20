#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 21:00
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
from io import StringIO

import pandas as pd
import requests

from akshare.option.cons import (
    get_calendar,
    convert_date,
    CZCE_DAILY_OPTION_URL_3,
    SHFE_HEADERS,
)


def option_hist_dce(
    symbol: str = "聚丙烯期权", trade_date: str = "20251016"
) -> pd.DataFrame:
    """
    大连商品交易所-期权-日频行情数据
    http://www.dce.com.cn/
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"玉米期权", "豆粕期权", "铁矿石期权", "液化石油气期权", "聚乙烯期权", "聚氯乙烯期权",
    "聚丙烯期权", "棕榈油期权", "黄大豆1号期权", "黄大豆2号期权", "豆油期权", "乙二醇期权", "苯乙烯期权",
    "鸡蛋期权", "玉米淀粉期权", "生猪期权", "原木期权"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    option_code_map = {
        "玉米期权": "c",
        "豆粕期权": "m",
        "铁矿石期权": "i",
        "液化石油气期权": "pg",
        "聚乙烯期权": "l",
        "聚氯乙烯期权": "v",
        "聚丙烯期权": "pp",
        "棕榈油期权": "p",
        "黄大豆1号期权": "a",
        "黄大豆2号期权": "b",
        "豆油期权": "y",
        "乙二醇期权": "eg",
        "苯乙烯期权": "eb",
        "鸡蛋期权": "jd",
        "玉米淀粉期权": "cs",
        "生猪期权": "lh",
        "原木期权": "lg",
    }
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return pd.DataFrame()
    url = "http://www.dce.com.cn/dcereport/publicweb/dailystat/dayQuotes"
    payload = {
        "contractId": "",
        "lang": "zh",
        "optionSeries": "",
        "statisticsType": 0,
        "tradeDate": f"{trade_date}",
        "tradeType": "2",
        "varietyId": f"{option_code_map[symbol]}",
    }
    r = requests.post(url, json=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.rename(
        columns={
            "variety": "品种名称",
            "contractId": "合约",
            "open": "开盘价",
            "high": "最高价",
            "low": "最低价",
            "close": "收盘价",
            "lastClear": "前结算价",
            "clearPrice": "结算价",
            "diff": "涨跌",
            "diff1": "涨跌1",
            "delta": "Delta",
            "volumn": "成交量",  # 注意：你写的是“volumn”，可能是拼写错误，应为“volume”
            "openInterest": "持仓量",
            "diffI": "持仓量变化",
            "turnover": "成交额",
            "matchQtySum": "行权量",
            "impliedVolatility": "隐含波动率(%)",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "品种名称",
            "合约",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "前结算价",
            "结算价",
            "涨跌",
            "涨跌1",
            "Delta",
            "隐含波动率(%)",
            "成交量",
            "持仓量",
            "持仓量变化",
            "成交额",
            "行权量",
        ]
    ]
    comma_cols = [
        "开盘价",
        "最高价",
        "最低价",
        "收盘价",
        "前结算价",
        "结算价",
        "涨跌",
        "涨跌1",
        "Delta",
        "隐含波动率(%)",
        "成交额",
    ]  # 需要处理的列
    for col in comma_cols:
        temp_df[col] = (
            temp_df[col]
            .astype(str)
            .str.replace(",", "")
            .pipe(pd.to_numeric, errors="coerce")
        )
    return temp_df


def __option_czce_daily_convert_numeric_columns(df):
    # 定义要处理的列
    columns_to_convert = [
        "昨结算",
        "今开盘",
        "最高价",
        "最低价",
        "今收盘",
        "今结算",
        "涨跌1",
        "涨跌2",
        "成交量(手)",
        "持仓量",
        "增减量",
        "成交额(万元)",
        "DELTA",
        "隐含波动率",
        "行权量",
    ]

    # 转换函数：去除逗号并转换为float
    def convert_to_float(x):
        try:
            return float(str(x).replace(",", ""))
        except:  # noqa: E722
            return x

    # 创建 DataFrame 的副本以避免 SettingWithCopyWarning
    df_copy = df.copy()
    df_copy.columns = [item.strip() for item in df_copy]
    # 应用转换
    for col in columns_to_convert:
        df_copy[col] = df_copy[col].apply(convert_to_float)

    return df_copy


def option_hist_czce(
    symbol: str = "白糖期权", trade_date: str = "20191017"
) -> pd.DataFrame:
    """
    郑州商品交易所-期权-日频行情数据
    http://www.czce.com.cn/cn/sspz/dejbqhqq/H770227index_1.htm#tabs-2
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {"白糖期权", "棉花期权", "甲醇期权", "PTA期权", "动力煤期权", "菜籽粕期权", "菜籽油期权",
    "花生期权", "对二甲苯期权", "烧碱期权", "纯碱期权", "短纤期权", "锰硅期权", "硅铁期权", "尿素期权", "苹果期权", "红枣期权",
    "玻璃期权", "瓶片期权", "丙烯期货"}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("{}非交易日".format(day.strftime("%Y%m%d")))
        return pd.DataFrame()
    if day > datetime.date(year=2010, month=8, day=24):
        url = CZCE_DAILY_OPTION_URL_3.format(day.strftime("%Y"), day.strftime("%Y%m%d"))
        try:
            r = requests.get(url)
            f = StringIO(r.text)
            table_df = pd.read_table(f, encoding="utf-8", skiprows=1, sep="|")
            table_df.columns = [
                "合约代码",
                "昨结算",
                "今开盘",
                "最高价",
                "最低价",
                "今收盘",
                "今结算",
                "涨跌1",
                "涨跌2",
                "成交量(手)",
                "持仓量",
                "增减量",
                "成交额(万元)",
                "DELTA",
                "隐含波动率",
                "行权量",
            ]
            if symbol == "白糖期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SR")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "棉花期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("CF")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "甲醇期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("MA")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "PTA期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("TA")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "动力煤期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("ZC")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "菜籽粕期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("RM")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "菜籽油期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("OI")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "花生期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PK")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "短纤期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PF")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "对二甲苯期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PX")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "烧碱期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SH")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "纯碱期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SA")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "短纤期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PF")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "锰硅期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SM")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "硅铁期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("SF")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "尿素期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("UR")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "苹果期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("AP")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "红枣期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("CJ")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "玻璃期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("FG")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "瓶片期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PR")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            elif symbol == "丙烯期权":
                temp_df = table_df[table_df.iloc[:, 0].str.contains("PL")]
                temp_df.reset_index(inplace=True, drop=True)
                temp_df = temp_df.iloc[:-1, :].copy()
                new_df = __option_czce_daily_convert_numeric_columns(temp_df)
                return new_df
            else:
                return pd.DataFrame()
        except:  # noqa: E722
            return pd.DataFrame()
    else:
        return pd.DataFrame()


def option_hist_shfe(
    symbol: str = "铝期权", trade_date: str = "20250418"
) -> pd.DataFrame:
    """
    上海期货交易所-期权-日频行情数据
    https://www.shfe.com.cn/reports/tradedata/dailyandweeklydata/
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {'原油期权', '铜期权', '铝期权', '锌期权', '铅期权', '螺纹钢期权', '镍期权', '锡期权', '氧化铝期权',
    '黄金期权', '白银期权', '丁二烯橡胶期权', '天胶期权'}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return pd.DataFrame()
    if day > datetime.date(year=2010, month=8, day=24):
        url = f"""https://www.shfe.com.cn/data/tradedata/option/dailydata/kx{day.strftime("%Y%m%d")}.dat"""
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
            contract_df.rename(
                columns={
                    "INSTRUMENTID": "合约代码",
                    "OPENPRICE": "开盘价",
                    "HIGHESTPRICE": "最高价",
                    "LOWESTPRICE": "最低价",
                    "CLOSEPRICE": "收盘价",
                    "PRESETTLEMENTPRICE": "前结算价",
                    "SETTLEMENTPRICE": "结算价",
                    "ZD1_CHG": "涨跌1",
                    "ZD2_CHG": "涨跌2",
                    "VOLUME": "成交量",
                    "OPENINTEREST": "持仓量",
                    "OPENINTERESTCHG": "持仓量变化",
                    "TURNOVER": "成交额",
                    "DELTA": "德尔塔",
                    "EXECVOLUME": "行权量",
                },
                inplace=True,
            )
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
            contract_df.reset_index(inplace=True, drop=True)
            return contract_df
        except:  # noqa: E722
            return pd.DataFrame()
    else:
        return pd.DataFrame()


def option_vol_shfe(
    symbol: str = "铝期权", trade_date: str = "20250418"
) -> pd.DataFrame:
    """
    上海期货交易所-期权-日频行情数据
    https://www.shfe.com.cn/reports/tradedata/dailyandweeklydata/
    :param trade_date: 交易日
    :type trade_date: str
    :param symbol: choice of {'原油期权', '铜期权', '铝期权', '锌期权', '铅期权', '螺纹钢期权', '镍期权', '锡期权', '氧化铝期权',
    '黄金期权', '白银期权', '丁二烯橡胶期权', '天胶期权'}
    :type symbol: str
    :return: 日频行情数据
    :rtype: pandas.DataFrame
    """
    calendar = get_calendar()
    day = convert_date(trade_date) if trade_date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return pd.DataFrame()
    if day > datetime.date(year=2010, month=8, day=24):
        url = f"""https://www.shfe.com.cn/data/tradedata/option/dailydata/kx{day.strftime("%Y%m%d")}.dat"""
        try:
            r = requests.get(url, headers=SHFE_HEADERS)
            json_data = r.json()
            volatility_df = pd.DataFrame(json_data["o_cursigma"])
            volatility_df = volatility_df[
                volatility_df["PRODUCTNAME"].str.strip() == symbol
            ]
            volatility_df.rename(
                columns={
                    "INSTRUMENTID": "合约系列",
                    "VOLUME": "成交量",
                    "OPENINTEREST": "持仓量",
                    "OPENINTERESTCHG": "持仓量变化",
                    "TURNOVER": "成交额",
                    "EXECVOLUME": "行权量",
                    "SIGMA": "隐含波动率",
                },
                inplace=True,
            )
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
            volatility_df.reset_index(inplace=True, drop=True)
            return volatility_df
        except:  # noqa: E722
            return pd.DataFrame()
    else:
        return pd.DataFrame()


def option_hist_gfex(
    symbol: str = "工业硅", trade_date: str = "20230724"
) -> pd.DataFrame:
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
        return pd.DataFrame()
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/108.0.0.0 Safari/537.36",
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
    temp_df = temp_df[temp_df["商品名称"].str.contains(symbol)]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def option_vol_gfex(symbol: str = "碳酸锂", trade_date: str = "20230724"):
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
        "多晶硅": "ps",
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/108.0.0.0 Safari/537.36",
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
    temp_df = temp_df[temp_df["合约系列"].str.contains(symbol_code_map[symbol])]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    option_hist_czce_df = option_hist_czce(symbol="白糖期权", trade_date="20250812")
    print(option_hist_czce_df)

    option_hist_dce_df = option_hist_dce(symbol="聚丙烯期权", trade_date="20250812")
    print(option_hist_dce_df)

    option_hist_shfe_df = option_hist_shfe(symbol="天胶期权", trade_date="20250418")
    print(option_hist_shfe_df)

    option_vol_shfe_df = option_vol_shfe(symbol="天胶期权", trade_date="20250418")
    print(option_vol_shfe_df)

    option_hist_gfex_df = option_hist_gfex(symbol="工业硅", trade_date="20250801")
    print(option_hist_gfex_df)

    option_vol_gfex_df = option_vol_gfex(symbol="多晶硅", trade_date="20250123")
    print(option_vol_gfex_df)
