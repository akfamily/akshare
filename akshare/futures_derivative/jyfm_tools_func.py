# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/01/02 17:37
Desc: 获取交易法门-工具: https://www.jiaoyifamen.com/tools/
交易法门首页: https://www.jiaoyifamen.com/

# 交易法门-工具-套利分析
交易法门-工具-套利分析-跨期价差(自由价差)
交易法门-工具-套利分析-自由价比
交易法门-工具-套利分析-多腿组合
交易法门-工具-套利分析-FullCarry
交易法门-工具-套利分析-套利价差矩阵

# 交易法门-工具-资讯汇总
交易法门-工具-资讯汇总-研报查询
交易法门-工具-资讯汇总-交易日历

# 交易法门-工具-持仓分析
交易法门-工具-持仓分析-期货持仓
交易法门-工具-持仓分析-席位持仓
交易法门-工具-持仓分析-持仓季节性

# 交易法门-工具-资金分析
交易法门-工具-资金分析-资金流向
交易法门-工具-资金分析-沉淀资金
交易法门-工具-资金分析-资金季节性
交易法门-工具-资金分析-成交排名

# 交易法门-工具-席位分析
交易法门-工具-席位分析-持仓结构
交易法门-工具-席位分析-持仓成本
交易法门-工具-席位分析-建仓过程

# 交易法门-工具-仓单分析
交易法门-工具-仓单分析-仓单日报
交易法门-工具-仓单分析-仓单查询
交易法门-工具-仓单分析-虚实盘比日报
交易法门-工具-仓单分析-虚实盘比查询

# 交易法门-工具-期限分析
交易法门-工具-期限分析-基差日报
交易法门-工具-期限分析-基差分析
交易法门-工具-期限分析-期限结构
交易法门-工具-期限分析-价格季节性

# 交易法门-工具-行情分析
交易法门-工具-行情分析-行情数据

# 交易法门-工具-交易规则
交易法门-工具-交易规则-限仓规定
交易法门-工具-交易规则-仓单有效期
交易法门-工具-交易规则-品种手册
"""
import time

import matplotlib.pyplot as plt
import pandas as pd
import requests

from akshare.futures_derivative.cons import (
    csa_payload,
    csa_url_spread,
    csa_url_ratio,
    csa_url_customize,
)
from akshare.futures_derivative.jyfm_login_func import jyfm_login


# pd.set_option('display.max_columns', None)


# 交易法门-工具-套利分析
def jyfm_tools_futures_spread(
    type_1="RB", type_2="RB", code_1="01", code_2="05", headers="", plot=True
):
    """
    交易法门-工具-套利分析-跨期价差(自由价差)
    :param type_1: str
    :param type_2: str
    :param code_1: str
    :param code_2: str
    :param plot: Bool
    :return: pandas.Series or pic
    """
    csa_payload_his = csa_payload.copy()
    csa_payload_his.update({"type1": type_1})
    csa_payload_his.update({"type2": type_2})
    csa_payload_his.update({"code1": code_1})
    csa_payload_his.update({"code2": code_2})
    res = requests.get(csa_url_spread, params=csa_payload_his, headers=headers)
    data_json = res.json()
    data_df = pd.DataFrame([data_json["category"], data_json["value"]]).T
    data_df.index = pd.to_datetime(data_df.iloc[:, 0])
    data_df = data_df.iloc[:, 1]
    data_df.name = "value"
    if plot:
        data_df.plot()
        plt.legend(loc="best")
        plt.xlabel("date")
        plt.ylabel("value")
        plt.show()
        return data_df
    else:
        return data_df


def jyfm_tools_futures_ratio(
    type_1="RB", type_2="RB", code_1="01", code_2="05", headers="", plot=True
):
    """
    交易法门-工具-套利分析-自由价比
    :param type_1: str
    :param type_2: str
    :param code_1: str
    :param code_2: str
    :param plot: Bool
    :return: pandas.Series or pic
    2013-01-04   -121
    2013-01-07   -124
    2013-01-08   -150
    2013-01-09   -143
    2013-01-10   -195
                 ...
    2019-10-21    116
    2019-10-22    126
    2019-10-23    123
    2019-10-24    126
    2019-10-25    134
    """
    csa_payload_his = csa_payload.copy()
    csa_payload_his.update({"type1": type_1})
    csa_payload_his.update({"type2": type_2})
    csa_payload_his.update({"code1": code_1})
    csa_payload_his.update({"code2": code_2})
    res = requests.get(csa_url_ratio, params=csa_payload_his, headers=headers)
    data_json = res.json()
    data_df = pd.DataFrame([data_json["category"], data_json["value"]]).T
    data_df.index = pd.to_datetime(data_df.iloc[:, 0])
    data_df = data_df.iloc[:, 1]
    data_df.name = "value"
    if plot:
        data_df.plot()
        plt.legend(loc="best")
        plt.xlabel("date")
        plt.ylabel("value")
        plt.show()
        return data_df
    else:
        return data_df


def jyfm_tools_futures_customize(
    formula="RB01-1.6*I01-0.5*J01-1200", headers="", plot=True
):
    """
    交易法门-工具-套利分析-多腿组合
    :param formula: str
    :param plot: Bool
    :return: pandas.Series or pic
    """
    params = {"formula": formula}
    res = requests.get(csa_url_customize, params=params, headers=headers)
    data_json = res.json()
    data_df = pd.DataFrame([data_json["category"], data_json["value"]]).T
    data_df.index = pd.to_datetime(data_df.iloc[:, 0])
    data_df = data_df.iloc[:, 1]
    data_df.name = "value"
    if plot:
        data_df.plot()
        plt.legend(loc="best")
        plt.xlabel("date")
        plt.ylabel("value")
        plt.show()
        return data_df
    else:
        return data_df


def jyfm_tools_futures_full_carry(
    begin_code="05", end_code="09", ratio="4", headers=""
):
    """
    交易法门-工具-套利分析-FullCarry
    https://www.jiaoyifamen.com/tools/future/full/carry?beginCode=05&endCode=09&ratio=4
    注: 正向转抛成本主要是仓储费和资金成本，手续费占比很小，故忽略。增值税不确定，故也未列入计算。使用该表时注意仓单有效期问题、升贴水问题以及生鲜品种其他较高费用的问题。实际Full Carry水平要略高于这里的测算水平。
    :param begin_code: 开始月份
    :type begin_code: str
    :param end_code: 结束月份
    :type end_code: str
    :param ratio: 百分比, 这里输入绝对值
    :type ratio: str
    :param headers: 请求头
    :type headers: dict
    :return: 正向市场转抛成本估算
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/future/full/carry"
    params = {
        "beginCode": begin_code,
        "endCode": end_code,
        "ratio": ratio,
    }
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["table_data"])


def jyfm_tools_futures_arbitrage_matrix(
    category="1", type1="RB", type2="RB", headers=""
):
    """
    交易法门-工具-套利分析-跨期价差矩阵
    https://www.jiaoyifamen.com/tools/future/arbitrage/matrix
    :param category: 1: 跨期价差; 2: 自由价差; 3: 自由价比
    :type category: str
    :param type1: 种类一
    :type type1: str
    :param type2: 种类二
    :type type2: str
    :param headers: 请求头
    :type headers: dict
    :return: 对应的矩阵
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/future/arbitrage/matrix"
    params = {
        "category": category,
        "type1": type1,
        "type2": type2,
        "_": "1583846468579",
    }
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"])


def jyfm_exchange_symbol_dict():
    jyfm_exchange_symbol_dict_inner = {
        "中国金融期货交易所": {
            "TF": "五债",
            "T": "十债",
            "IC": "中证500",
            "IF": "沪深300",
            "IH": "上证50",
            "TS": "二债",
        },
        "郑州商品交易所": {
            "FG": "玻璃",
            "RS": "菜籽",
            "CF": "棉花",
            "LR": "晚稻",
            "CJ": "红枣",
            "JR": "粳稻",
            "ZC": "动力煤",
            "TA": "PTA",
            "SA": "纯碱",
            "AP": "苹果",
            "WH": "强麦",
            "SF": "硅铁",
            "MA": "甲醇",
            "CY": "棉纱",
            "RI": "早稻",
            "OI": "菜油",
            "SM": "硅锰",
            "RM": "菜粕",
            "UR": "尿素",
            "PM": "普麦",
            "SR": "白糖",
        },
        "大连商品交易所": {
            "PP": "PP",
            "RR": "粳米",
            "BB": "纤板",
            "A": "豆一",
            "EG": "乙二醇",
            "B": "豆二",
            "C": "玉米",
            "JM": "焦煤",
            "I": "铁矿",
            "J": "焦炭",
            "L": "塑料",
            "M": "豆粕",
            "P": "棕榈",
            "CS": "淀粉",
            "V": "PVC",
            "Y": "豆油",
            "JD": "鸡蛋",
            "FB": "胶板",
            "EB": "苯乙烯",
        },
        "上海期货交易所": {
            "SS": "不锈钢",
            "RU": "橡胶",
            "AG": "沪银",
            "AL": "沪铝",
            "FU": "燃油",
            "RB": "螺纹",
            "CU": "沪铜",
            "PB": "沪铅",
            "BU": "沥青",
            "AU": "沪金",
            "ZN": "沪锌",
            "SN": "沪锡",
            "HC": "热卷",
            "NI": "沪镍",
            "WR": "线材",
            "SP": "纸浆",
        },
        "上海国际能源交易中心": {"SC": "原油", "NR": "20号胶"},
    }
    return jyfm_exchange_symbol_dict_inner


# 交易法门-工具-资讯汇总
def jyfm_tools_research_query(limit="100", headers=""):
    """
    交易法门-工具-资讯汇总-研报查询
    https://www.jiaoyifamen.com/tools/research/qryPageList
    :param limit: 返回条数
    :type limit: str
    :return: 返回研报信息数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/research/qryPageList"
    params = {
        "page": "1",
        "limit": limit,
    }
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"])


def jyfm_tools_trade_calendar(trade_date="2020-01-03", headers=""):
    """
    交易法门-工具-资讯汇总-交易日历
    此函数可以返回未来的交易日历数据
    https://www.jiaoyifamen.com/tools/trade-calendar/events
    :param trade_date: 指定交易日
    :type trade_date: str
    :return: 返回指定交易日的交易日历数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/trade-calendar/events"
    params = {
        "page": "1",
        "limit": "1000",
        "day": trade_date,
    }
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"])


# 交易法门-工具-持仓分析
def jyfm_tools_position_detail(
    symbol="JM", code="jm2005", trade_date="2020-01-03", headers=""
):
    """
    交易法门-工具-持仓分析-期货持仓
    :param symbol: 指定品种
    :type symbol: str
    :param code: 指定合约
    :type code: str
    :param trade_date: 指定交易日
    :type trade_date: str
    :param headers: headers with cookies
    :type headers:dict
    :return: 指定品种的指定合约的指定交易日的期货持仓数据
    :rtype: pandas.DataFrame
    """
    url = f"https://www.jiaoyifamen.com/tools/position/details/{symbol}?code={code}&day={trade_date}&_=1578040551329"
    res = requests.get(url, headers=headers)
    return pd.DataFrame(res.json()["short_rank_table"])


def jyfm_tools_position_seat(seat="永安期货", trade_date="2020-01-03", headers=""):
    """
    交易法门-工具-持仓分析-持仓分析-席位持仓
    :param seat: 指定期货公司
    :type seat: str
    :param trade_date: 具体交易日
    :type trade_date: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定期货公司指定交易日的席位持仓数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/position/seat"
    params = {
        "seat": seat,
        "day": trade_date,
        "type": "",
        "_": "1578040989932",
    }
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"])


def jyfm_tools_position_season(symbol="RB", code="05", headers=""):
    """
    交易法门-工具-持仓分析-持仓分析-持仓季节性
    https://www.jiaoyifamen.com/tools/position/season
    :param symbol: 具体品种
    :type symbol: str
    :param code: 具体合约月份
    :type code: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 合约持仓季节性规律
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/position/season"
    params = {
        "type": symbol,
        "code": code,
    }
    res = requests.get(url, params=params, headers=headers)
    data_json = res.json()
    temp_df = pd.DataFrame(
        [
            data_json["year2013"],
            data_json["year2014"],
            data_json["year2015"],
            data_json["year2016"],
            data_json["year2017"],
            data_json["year2018"],
            data_json["year2019"],
            data_json["year2020"],
        ],
        columns=data_json["dataCategory"],
    ).T
    temp_df.columns = ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    return temp_df


# 交易法门-工具-资金分析
def jyfm_tools_position_fund_direction(
    trade_date="2020-02-24", indicator="期货品种资金流向排名", headers=""
):
    """
    交易法门-工具-资金分析-资金流向
    https://www.jiaoyifamen.com/tools/position/fund/?day=2020-01-08
    :param trade_date: 指定交易日
    :type trade_date: str
    :param indicator: "期货品种资金流向排名" or "期货主力合约资金流向排名"
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日的资金流向数据
    :rtype: pandas.DataFrame
    """
    params = {
        "day": trade_date,
    }
    url = "https://www.jiaoyifamen.com/tools/position/fund/"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    if indicator == "期货品种资金流向排名":
        return pd.DataFrame(
            [
                [data_json["tradingDay"]] * len(data_json["flowCategory"]),
                data_json["flowCategory"],
                data_json["flowValue"],
            ],
            index=["date", "symbol", "fund"],
        ).T
    else:
        return pd.DataFrame(
            [
                [data_json["tradingDay"]] * len(data_json["dominantFlowCategory"]),
                data_json["dominantFlowCategory"],
                data_json["dominantFlowValue"],
            ],
            index=["date", "symbol", "fund"],
        ).T


def jyfm_tools_position_fund_down(
    trade_date="2020-02-24", indicator="期货品种沉淀资金排名", headers=""
):
    """
    交易法门-工具-资金分析-沉淀资金
    https://www.jiaoyifamen.com/tools/position/fund/?day=2020-01-08
    :param trade_date: 指定交易日
    :type trade_date: str
    :param indicator: "期货品种沉淀资金排名" or "期货主力合约沉淀资金排名"
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日的沉淀资金
    :rtype: pandas.DataFrame
    """
    params = {
        "day": trade_date,
    }
    url = "https://www.jiaoyifamen.com/tools/position/fund/"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    if indicator == "期货品种沉淀资金排名":
        return pd.DataFrame(
            [
                [data_json["tradingDay"]] * len(data_json["precipitationCategory"]),
                data_json["precipitationCategory"],
                data_json["precipitationValue"],
            ],
            index=["date", "symbol", "fund"],
        ).T
    else:
        return pd.DataFrame(
            [
                [data_json["tradingDay"]]
                * len(data_json["dominantPrecipitationCategory"]),
                data_json["dominantPrecipitationCategory"],
                data_json["dominantPrecipitationValue"],
            ],
            index=["date", "symbol", "fund"],
        ).T


def jyfm_tools_position_fund_season(symbol="RB", code="05", headers=""):
    """
    交易法门-工具-资金分析-资金季节性
    https://www.jiaoyifamen.com/tools/position/fund/?day=2020-01-08
    :param symbol: 指定品种
    :type symbol: str
    :param code: 合约到期月
    :type code: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日的资金资金季节性
    :rtype: pandas.DataFrame
    """
    params = {
        "type": symbol,
        "code": code,
    }
    url = "https://www.jiaoyifamen.com/tools/position/fund/season"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    data_df = pd.DataFrame(
        [
            data_json["dataCategory"],
            data_json["year2013"],
            data_json["year2014"],
            data_json["year2015"],
            data_json["year2016"],
            data_json["year2017"],
            data_json["year2018"],
            data_json["year2019"],
            data_json["year2020"],
        ],
        index=["date", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"],
    ).T
    return data_df


def jyfm_tools_position_fund_deal(
    trade_date="2020-02-24", indicator="期货品种成交量排名", headers=""
):
    """
    交易法门-工具-资金分析-成交排名
    https://www.jiaoyifamen.com/tools/position/fund/?day=2020-01-08
    :param trade_date: 指定交易日
    :type trade_date: str
    :param indicator: "期货品种成交量排名" or "期货主力合约成交量排名"
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日的资金成交排名
    :rtype: pandas.DataFrame
    """
    params = {
        "day": trade_date,
    }
    url = "https://www.jiaoyifamen.com/tools/position/fund/"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    if indicator == "期货品种成交量排名":
        return pd.DataFrame(
            [
                [data_json["tradingDay"]] * len(data_json["turnOverCategory"]),
                data_json["turnOverCategory"],
                data_json["turnOverValue"],
            ],
            index=["date", "symbol", "fund"],
        ).T
    else:
        return pd.DataFrame(
            [
                [data_json["tradingDay"]] * len(data_json["dominantTurnOverCategory"]),
                data_json["dominantTurnOverCategory"],
                data_json["dominantTurnOverValue"],
            ],
            index=["date", "symbol", "fund"],
        ).T


# 交易法门-工具-席位分析-持仓结构
def jyfm_tools_position_structure(
    trade_date="2020-03-02", seat="永安期货", indicator="持仓变化", headers=""
):
    """
    交易法门-工具-席位分析-持仓结构
    https://www.jiaoyifamen.com/tools/position/seat
    :param trade_date: 指定交易日
    :type trade_date: str
    :param seat: broker name, e.g., seat="永安期货"
    :type seat: str
    :param indicator: 持仓变化，净持仓分布，总持仓分布; 持仓变化总，净持仓分布总，总持仓分布总
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日指定机构的持仓结构
    :rtype: pandas.DataFrame
    """
    indicator_dict = {"持仓变化": 1, "净持仓分布": 2, "总持仓分布": 3}
    params = {
        "seat": seat,
        "day": trade_date,
        "type": indicator_dict[indicator],
        "_": int(time.time() * 1000),
    }
    url = "https://www.jiaoyifamen.com/tools/position/struct"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    if indicator == "持仓变化":
        return pd.DataFrame(data_json["varieties"])
    if indicator == "净持仓分布":
        return pd.DataFrame(data_json["varieties"])
    if indicator == "总持仓分布":
        return pd.DataFrame(data_json["varieties"])
    if indicator == "持仓变化总":
        return pd.DataFrame(data_json["ratio"])
    if indicator == "净持仓分布总":
        return pd.DataFrame(data_json["ratio"])
    if indicator == "总持仓分布总":
        return pd.DataFrame(data_json["ratio"])


# 交易法门-工具-席位分析-持仓成本
def jyfm_tools_position_seat_cost(seat="永安期货", symbol="RB", code="10", headers=""):
    """
    交易法门-工具-席位分析-持仓成本
    https://www.jiaoyifamen.com/tools/position/seat
    :param seat: broker name, e.g., seat="永安期货"
    :type seat: str
    :param symbol: e.g., RB
    :type symbol: str
    :param code: e.g., 10
    :type code: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日指定机构的持仓结构
    :rtype: pandas.DataFrame
    """
    params = {
        "seat": seat,
        "type": symbol,
        "code": code,
        "_": int(time.time() * 1000),
    }
    url = "https://www.jiaoyifamen.com/tools/position/seat-cost"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    return pd.DataFrame(data_json["seatCost"])


# 交易法门-工具-席位分析-建仓过程
def jyfm_tools_position_interest_process(seat="永安期货", symbol="RB", instrument="rb2005", indicator="建仓过程", headers=""):
    """
    交易法门-工具-席位分析-持仓成本
    https://www.jiaoyifamen.com/tools/position/seat
    :param seat: broker name, e.g., seat="永安期货"
    :type seat: str
    :param symbol: e.g., RB
    :type symbol: str
    :param instrument: e.g., rb2005
    :type instrument: str
    :param indicator: e.g., "建仓过程", "净持仓量", "盈亏图"
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日指定机构的持仓结构
    :rtype: pandas.DataFrame
    """
    params = {
        "seat": seat,
        "type": symbol,
        "instrument": instrument,
        "_": int(time.time() * 1000),
    }
    url = "https://www.jiaoyifamen.com/tools/position/interest-process"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    if indicator == "建仓过程":
        return pd.DataFrame(data_json["kLine"], index=data_json["category"], columns=["open", "close", "low", "high"])
    if indicator == "净持仓量":
        return pd.DataFrame(data_json["neatPosition"], index=data_json["category"], columns=["净持仓量"])
    if indicator == "盈亏图":
        return pd.DataFrame(data_json["profit"], index=data_json["category"], columns=["持仓盈亏"])


# 交易法门-工具-仓单分析
def jyfm_tools_warehouse_receipt_daily(trade_date="2020-01-02", headers=""):
    """
    交易法门-工具-仓单分析-仓单日报
    https://www.jiaoyifamen.com/tools/warehouse-receipt/daily
    :param trade_date: 指定交易日
    :type trade_date: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定交易日的仓单日报数据
    :rtype: pandas.DataFrame
    """
    params = {
        "day": trade_date,
        "_": "1578555328412",
    }
    url = "https://www.jiaoyifamen.com/tools/warehouse-receipt/daily"
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"])


def jyfm_tools_warehouse_receipt_query(symbol="AL", indicator="仓单数据走势图", headers=""):
    """
    交易法门-工具-仓单分析-仓单查询
    https://www.jiaoyifamen.com/tools/warehouse-receipt/query
    :param symbol: 指定品种
    :type symbol: str
    :param indicator: 指定需要获取的指标, ["仓单数据走势图", "仓单数据季节图"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定品种的仓单数量走势图/季节图数据
    :rtype: pandas.DataFrame
    """
    params = {
        "type": symbol,
    }
    url = "https://www.jiaoyifamen.com/tools/warehouse-receipt/query"
    res = requests.get(url, params=params, headers=headers)
    data_json = res.json()
    if indicator == "仓单数据走势图":
        return pd.DataFrame(
            [data_json["category"], data_json["value"], data_json["value2"]]
        ).T
    return pd.DataFrame(
        [
            data_json["dataCategory"],
            data_json["year2013"],
            data_json["year2014"],
            data_json["year2015"],
            data_json["year2016"],
            data_json["year2017"],
            data_json["year2018"],
            data_json["year2019"],
            data_json["year2020"],
        ],
        index=[
            "date",
            "year2013",
            "year2014",
            "year2015",
            "year2016",
            "year2017",
            "year2018",
            "year2019",
            "year2020",
        ],
    ).T


def jyfm_tools_warehouse_virtual_fact_daily(trade_date="2020-01-20", headers=""):
    """
    交易法门-工具-仓单分析-虚实盘比日报
    https://www.jiaoyifamen.com/tools/warehouse-receipt/virtualfact/daily?day=&_=1579532255369
    :param trade_date: 指定日期
    :type trade_date: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定品种指定合约的虚实盘比数据
    :rtype: pandas.DataFrame
    """
    params = {
        "day": trade_date,
        "_": "1579532255370",
    }
    url = "https://www.jiaoyifamen.com/tools/warehouse-receipt/virtualfact/daily"
    res = requests.get(url, params=params, headers=headers)
    data_json = res.json()["data"]
    return pd.DataFrame(data_json)


def jyfm_tools_warehouse_virtual_fact_ratio(symbol="AL", code="05", headers=""):
    """
    交易法门-工具-仓单分析-虚实盘比查询
    https://www.jiaoyifamen.com/tools/warehouse-receipt/ratio
    :param symbol: 指定品种
    :type symbol: str
    :param code: 指定日期的合约
    :type code: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定品种指定合约的虚实盘比数据
    :rtype: pandas.DataFrame
    """
    params = {
        "type": symbol,
        "code": code,
    }
    url = "https://www.jiaoyifamen.com/tools/warehouse-receipt/ratio"
    res = requests.get(url, params=params, headers=headers)
    data_json = res.json()
    return pd.DataFrame(
        [
            data_json["dataCategory"],
            data_json["year2013"],
            data_json["year2014"],
            data_json["year2015"],
            data_json["year2016"],
            data_json["year2017"],
            data_json["year2018"],
            data_json["year2019"],
            data_json["year2020"],
        ],
        index=[
            "date",
            "year2013",
            "year2014",
            "year2015",
            "year2016",
            "year2017",
            "year2018",
            "year2019",
            "year2020",
        ],
    ).T


# 交易法门-工具-期限分析-基差日报
def jyfm_tools_futures_basis_daily(
    trade_date="2020-02-05", indicator="基差率", headers=""
):
    """
    交易法门-工具-期限分析-基差日报
    :param trade_date: 指定交易日期, 注意格式为 "2020-01-02"
    :type trade_date: str
    :param indicator: ["基差率", "基差日报"] 二选一
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定日期的基差日报数据
    :rtype: pandas.DataFrame
    """
    params = {
        "day": trade_date,
    }
    url = "https://www.jiaoyifamen.com/tools/future/basis/daily"
    res = requests.get(url, params=params, headers=headers)
    json_data = res.json()

    if indicator == "基差率":
        # x 轴, y 轴
        return pd.DataFrame(
            [json_data["category"], json_data["value"]], index=["x", "y"]
        ).T

    if indicator == "基差日报":
        return pd.DataFrame(json_data["table_data"])


# 交易法门-工具-期限分析-基差日报-地区选取
def jyfm_tools_futures_basis_daily_area(symbol="Y", headers=""):
    """
    交易法门-工具-期限分析-基差日报-地区选取
    :param symbol: 品种代码
    :type symbol: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定品种的可选地区
    :rtype: list
    """
    params = {
        "type": symbol,
    }
    url = "https://www.jiaoyifamen.com/tools/future/area"
    res = requests.get(url, params=params, headers=headers)
    return res.json()["areas"]


def jyfm_tools_futures_basis_analysis(
    symbol="RB", area="上海", indicator="基差率分布图", headers=""
):
    """
    交易法门-工具-期限分析-基差分析
    :param symbol: 品种代码
    :type symbol: str
    :param area: one of ["上海", "天津"], 不同品种不同日期通过 jyfm_tools_futures_basis_daily_area 返回
    :type area: str
    :param indicator: one of ["基差走势图", "基差率季节图", "基差率分布图"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定品种和地区的基差日报
    :rtype: pandas.DataFrame
    """
    url = "https://www.jiaoyifamen.com/tools/future/basis/analysis"
    params = {
        "type": symbol,
        "area": area,
    }
    res = requests.get(url, params=params, headers=headers)
    json_data = res.json()
    if indicator == "基差走势图":
        # x 轴 y 轴
        return pd.DataFrame(
            [json_data["cashValue"], json_data["futureValue"], json_data["basisValue"]],
            columns=json_data["category"],
            index=["现货", "期货", "基差"],
        ).T

    if indicator == "基差率季节图":
        # x 轴 y 轴
        return pd.DataFrame(
            [
                json_data["year2013"],
                json_data["year2014"],
                json_data["year2015"],
                json_data["year2016"],
                json_data["year2017"],
                json_data["year2018"],
                json_data["year2019"],
                json_data["year2020"],
            ],
            index=[
                "year2013",
                "year2014",
                "year2015",
                "year2016",
                "year2017",
                "year2018",
                "year2019",
                "year2020",
            ],
            columns=json_data["dataCategory"],
        ).T

    if indicator == "基差率分布图":
        # x 轴 y 轴
        return pd.DataFrame(
            [json_data["limitCategory"], json_data["limitValue"]], index=["x", "y"]
        ).T


def jyfm_tools_futures_basis_structure(symbol="RB", headers=""):
    """
    交易法门-工具-期限分析-期限结构
    :param symbol: 合约品种
    :type symbol: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 指定品种的期限结构数据
    :rtype: pandas.DataFrame
    """
    params = {
        "type": symbol,
    }
    url = "https://www.jiaoyifamen.com/tools/future/basis/structure"
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json())


def jyfm_tools_futures_basis_rule(
    symbol="RB", code="05", indicator="期货涨跌统计", headers=""
):
    """
    交易法门-工具-期限分析-价格季节性
    :param symbol: 品种
    :type symbol: str
    :param code: 合约具体月份
    :type code: str
    :param indicator: ["期货涨跌统计", "季节性走势图"], 默认为: 期货涨跌统计
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: 期货涨跌统计 or 季节性走势图
    :rtype: pandas.DataFrame
    """
    params = {
        "type": symbol,
        "code": code,
    }
    url = "https://www.jiaoyifamen.com/tools/future/basis/rule"
    res = requests.get(url, params=params, headers=headers)
    data_json = res.json()
    if indicator == "期货涨跌统计":
        return pd.DataFrame(data_json["ratioData"])
    if indicator == "季节性走势图":
        return pd.DataFrame(
            [
                data_json["dataCategory"],
                data_json["year2013"],
                data_json["year2014"],
                data_json["year2015"],
                data_json["year2016"],
                data_json["year2017"],
                data_json["year2018"],
                data_json["year2019"],
                data_json["year2020"],
            ],
            index=[
                "date",
                "2013",
                "2014",
                "2015",
                "2016",
                "2017",
                "2018",
                "2019",
                "2020",
            ],
        ).T


# 交易法门-工具-行情分析-行情数据
def jyfm_tools_futures_market(symbol="RB", code="10", start_date="2020-01-02", end_date="2020-04-02", option="daily", headers=""):
    """
    交易法门-工具-交易规则-限仓规定
    :param symbol: e.g., "RB"
    :type symbol: str
    :param code: e.g., "10"
    :type code: str
    :param start_date: e.g., "2020-01-02"
    :type start_date: str
    :param end_date: e.g., "2020-04-02"
    :type end_date: str
    :param option: e.g., "daily", "weekly", "monthly"
    :type option: str
    :param headers: headers with cookies
    :type headers: dict
    :return:
    :rtype: pandas.DataFrame
    """
    params = {
        "type": symbol,
        "code": code,
        "beginDay": start_date,
        "endDay": end_date,
        "option": option,
        "_": "1585748470772",
    }
    url = "https://www.jiaoyifamen.com/tools/future/market"
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["tableData"])


# 交易法门-工具-交易规则
def jyfm_tools_position_limit_info(exchange="CFFEX", headers=""):
    """
    交易法门-工具-交易规则-限仓规定
    :param exchange: one of ["INE", "DCE", "CZCE", "SHFE", "CFFEX"], default is "CFFEX"]
    :type exchange: str
    :param headers: headers with cookies
    :type headers: dict
    :return:
    :rtype: pandas.DataFrame
    """
    params = {
        "page": "1",
        "limit": "10",
        "exchange": exchange,
    }
    url = "https://www.jiaoyifamen.com/tools/position-limit/query"
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"])


def jyfm_tools_receipt_expire_info(headers=""):
    """
    交易法门-工具-交易规则-仓单有效期
    :param headers: headers with cookies
    :type headers: dict
    :return: all history data
    :rtype: pandas.DataFrame
    """
    temp_df = pd.DataFrame()
    for page in range(1, 4):
        params = {
            "page": str(page),
            "limit": "20",
        }
        res = requests.get(
            f"https://www.jiaoyifamen.com/tools/receipt-expire-info/all",
            params=params,
            headers=headers,
        )
        temp_df = temp_df.append(pd.DataFrame(res.json()["data"]), ignore_index=True)
    return temp_df


def jyfm_tools_symbol_handbook(headers=""):
    """
    交易法门-工具-交易规则-品种手册
    :param headers: headers with cookies
    :type headers: dict
    :return: all history data
    :rtype: pandas.DataFrame
    """
    res = requests.get(
        "https://www.jiaoyifamen.com/tools/receipt-expire-info/variety", headers=headers
    )
    temp_df = pd.DataFrame(res.json()["data"])
    return temp_df


if __name__ == "__main__":
    # 如果要测试函数, 请先在交易法门网站: https://www.jiaoyifamen.com/ 注册帐号密码, 在下面输入对应的帐号和密码后再运行 jyfm_login 函数!
    headers = jyfm_login(account="link", password="loveloli888")

    # 交易法门-工具-套利分析
    jyfm_tools_futures_spread_df = jyfm_tools_futures_spread(
        type_1="RB", type_2="RB", code_1="01", code_2="05", headers=headers, plot=True
    )
    print(jyfm_tools_futures_spread_df)
    jyfm_tools_futures_ratio_df = jyfm_tools_futures_ratio(
        type_1="RB", type_2="RB", code_1="01", code_2="05", headers=headers, plot=True
    )
    print(jyfm_tools_futures_ratio_df)
    jyfm_tools_futures_customize_df = jyfm_tools_futures_customize(
        formula="RB01-1.6*I01-0.5*J01-1200", headers=headers, plot=True
    )
    print(jyfm_tools_futures_customize_df)
    jyfm_tools_futures_full_carry_df = jyfm_tools_futures_full_carry(
        begin_code="05", end_code="09", ratio="4", headers=headers
    )
    print(jyfm_tools_futures_full_carry_df)
    jyfm_tools_futures_arbitrage_matrix_df = jyfm_tools_futures_arbitrage_matrix(
        category="1", type1="RB", type2="RB", headers=headers
    )
    print(jyfm_tools_futures_arbitrage_matrix_df)

    # 交易法门-工具-资讯汇总
    jyfm_tools_research_query_df = jyfm_tools_research_query(
        limit="100", headers=headers
    )
    print(jyfm_tools_research_query_df)
    jyfm_tools_trade_calendar_df = jyfm_tools_trade_calendar(
        trade_date="2020-01-03", headers=headers
    )
    print(jyfm_tools_trade_calendar_df)

    # 交易法门-工具-持仓分析
    jyfm_tools_position_detail_df = jyfm_tools_position_detail(
        symbol="JM", code="jm2005", trade_date="2020-01-03", headers=headers
    )
    print(jyfm_tools_position_detail_df)
    jyfm_tools_position_seat_df = jyfm_tools_position_seat(
        seat="永安期货", trade_date="2020-01-03", headers=headers
    )
    print(jyfm_tools_position_seat_df)
    jyfm_tools_position_season_df = jyfm_tools_position_season(
        symbol="RB", code="05", headers=headers
    )
    print(jyfm_tools_position_season_df)

    # 交易法门-工具-资金分析
    # 交易法门-工具-资金分析-资金流向
    jyfm_tools_position_fund_direction_df = jyfm_tools_position_fund_direction(
        trade_date="2020-02-24", indicator="期货主力合约资金流向排名", headers=headers
    )
    print(jyfm_tools_position_fund_direction_df)
    # 交易法门-工具-资金分析-沉淀资金
    jyfm_tools_position_fund_down_df = jyfm_tools_position_fund_down(
        trade_date="2020-02-24", indicator="期货主力合约沉淀资金排名", headers=headers
    )
    print(jyfm_tools_position_fund_down_df)
    # 交易法门-工具-资金分析-资金季节性
    jyfm_tools_position_fund_season_df = jyfm_tools_position_fund_season(
        symbol="RB", code="05", headers=headers
    )
    print(jyfm_tools_position_fund_season_df)
    # 交易法门-工具-资金分析-成交排名
    jyfm_tools_position_fund_deal_df = jyfm_tools_position_fund_deal(
        trade_date="2020-02-24", indicator="期货主力合约成交量排名", headers=headers
    )
    print(jyfm_tools_position_fund_deal_df)

    # 交易法门-工具-席位分析
    # 交易法门-工具-席位分析-持仓结构
    jyfm_tools_position_structure_df = jyfm_tools_position_structure(
        trade_date="2020-03-02", seat="永安期货", indicator="持仓变化", headers=headers
    )
    print(jyfm_tools_position_structure_df)
    # 交易法门-工具-席位分析-持仓成本
    jyfm_tools_position_seat_cost_df = jyfm_tools_position_seat_cost(seat="永安期货", symbol="RB", code="10", headers=headers)
    print(jyfm_tools_position_seat_cost_df)
    # 交易法门-工具-席位分析-建仓过程
    jyfm_tools_position_interest_process_df = jyfm_tools_position_interest_process(seat="永安期货", symbol="RB", instrument="rb2005", indicator="建仓过程", headers=headers)
    print(jyfm_tools_position_interest_process_df)

    # 交易法门-工具-仓单分析
    # 交易法门-工具-仓单分析-仓单日报
    jyfm_tools_warehouse_receipt_daily_df = jyfm_tools_warehouse_receipt_daily(
        trade_date="2020-01-02", headers=headers
    )
    print(jyfm_tools_warehouse_receipt_daily_df)
    # 交易法门-工具-仓单分析-仓单查询
    jyfm_tools_warehouse_receipt_query_df = jyfm_tools_warehouse_receipt_query(
        symbol="AL", indicator="仓单数据走势图", headers=headers
    )
    print(jyfm_tools_warehouse_receipt_query_df)
    # 交易法门-工具-仓单分析-虚实盘比日报
    jyfm_tools_warehouse_virtual_fact_daily_df = jyfm_tools_warehouse_virtual_fact_daily(
        trade_date="2020-01-20", headers=headers
    )
    print(jyfm_tools_warehouse_virtual_fact_daily_df)
    # 交易法门-工具-仓单分析-虚实盘比查询
    jyfm_tools_warehouse_receipt_ratio_df = jyfm_tools_warehouse_virtual_fact_ratio(
        symbol="AL", code="05", headers=headers
    )
    print(jyfm_tools_warehouse_receipt_ratio_df)

    # 交易法门-工具-期限分析
    jyfm_tools_futures_basis_daily_df = jyfm_tools_futures_basis_daily(
        trade_date="2020-01-02", indicator="基差率", headers=headers
    )
    print(jyfm_tools_futures_basis_daily_df)
    jyfm_tools_futures_basis_analysis_area_df = jyfm_tools_futures_basis_daily_area(
        symbol="Y", headers=headers
    )
    print(jyfm_tools_futures_basis_analysis_area_df)
    jyfm_tools_futures_basis_analysis_df = jyfm_tools_futures_basis_analysis(
        symbol="RB", area="上海", indicator="基差率分布图", headers=headers
    )
    print(jyfm_tools_futures_basis_analysis_df)
    jyfm_tools_futures_basis_structure_df = jyfm_tools_futures_basis_structure(
        symbol="RB", headers=headers
    )
    print(jyfm_tools_futures_basis_structure_df)
    jyfm_tools_futures_basis_rule_df = jyfm_tools_futures_basis_rule(
        symbol="RB", code="05", indicator="期货涨跌统计", headers=headers
    )
    print(jyfm_tools_futures_basis_rule_df)

    # 交易法门-工具-行情分析
    # 交易法门-工具-行情分析-行情数据
    jyfm_tools_futures_market_df = jyfm_tools_futures_market(symbol="RB", code="10", start_date="2020-01-02", end_date="2020-04-02", option="daily", headers=headers)
    print(jyfm_tools_futures_market_df)

    # 交易法门-工具-交易规则
    # 交易法门-工具-交易规则-限仓规定
    jyfm_tools_receipt_expire_info_df = jyfm_tools_receipt_expire_info(headers=headers)
    print(jyfm_tools_receipt_expire_info_df)
    # 交易法门-工具-交易规则-仓单有效期
    jyfm_tools_position_limit_info_df = jyfm_tools_position_limit_info(
        exchange="CFFEX", headers=headers
    )
    print(jyfm_tools_position_limit_info_df)
    # 交易法门-工具-交易规则-品种手册
    jyfm_tools_symbol_handbook_df = jyfm_tools_symbol_handbook(headers=headers)
    print(jyfm_tools_symbol_handbook_df)
