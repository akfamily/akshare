# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/01/02 17:37
contact: jindaxiang@163.com
desc: 获取交易法门-工具: https://www.jiaoyifamen.com/tools/
交易法门首页: https://www.jiaoyifamen.com/
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt

from akshare.futures_derivative.jyfm_login_func import jyfm_login

from akshare.futures_derivative.cons import (
    csa_payload,
    csa_url_spread,
    csa_url_ratio,
    csa_url_customize,
)


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


jyfm_exchange_symbol_dict = {
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


if __name__ == "__main__":
    # 如果要测试函数, 请先在交易法门网站: https://www.jiaoyifamen.com/ 注册帐号密码, 填入下载 jyfm_login 函数后再运行!
    headers = jyfm_login(account="", password="")
    jyfm_tools_futures_customize_df = jyfm_tools_futures_customize(
        formula="RB01-1.6*I01-0.5*J01-1200", headers=headers, plot=True
    )
    temp_df = pd.DataFrame(jyfm_tools_futures_customize_df)
    print(temp_df)
    jyfm_tools_receipt_expire_info_df = jyfm_tools_receipt_expire_info(headers=headers)
    print(jyfm_tools_receipt_expire_info_df)
    jyfm_tools_position_limit_info_df = jyfm_tools_position_limit_info(
        exchange="CFFEX", headers=headers
    )
    print(jyfm_tools_position_limit_info_df)
