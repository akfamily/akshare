# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/27 19:47
contact: jindaxiang@163.com
desc: 获取交易法门网站-工具-套利工具
"""
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from akshare.futures_derivative.jyfm_login_func import jyfm_login


from akshare.futures_derivative.cons import (csa_payload,
                                             csa_url_spread,
                                             csa_url_ratio,
                                             csa_url_customize)


def jyfm_tools_receipt_expire_info(headers=""):
    """
    返回可以试用的参数, e.g., 交易所, 品种
    :return: dict
    {'中国金融期货交易所': {'TF': '五债', 'T': '十债', 'IC': '中证500', 'IF': '沪深300', 'IH': '上证50', 'TS': '二债'}, '郑州商品交易所': {'FG': '玻璃', 'RS': '菜籽', 'CF': '郑棉', 'LR': '晚稻', 'CJ': '红枣', 'JR': '粳稻', 'ZC': '郑煤', 'TA': 'PTA', 'AP': '苹果', 'WH': '郑麦', 'SF': '硅铁', 'MA': '郑醇', 'CY': '棉纱', 'RI': '早稻', 'OI': '郑油', 'SM': '硅锰', 'RM': '菜粕', 'UR': '尿素', 'PM': '普麦', 'SR': '白糖'}, '大连商品交易所': {'PP': 'PP', 'RR': '粳米', 'BB': '纤板', 'A': '豆一', 'EG': '乙二醇', 'B': '豆二', 'C': '玉米', 'JM': '焦煤', 'I': '铁矿', 'J': '焦炭', 'L': '塑料', 'M': '豆粕', 'P': '棕榈', 'CS': '淀粉', 'V': 'PVC', 'Y': '豆油', 'JD': '鸡蛋', 'FB': '胶板', 'EB': '苯乙烯'}, '上海期货交易所': {'SS': '不锈钢', 'RU': '橡胶', 'AG': '沪银', 'AL': '沪铝', 'FU': '燃油', 'RB': '螺纹', 'CU': '沪铜', 'PB': '沪铅', 'BU': '沥青', 'AU': '沪金', 'ZN': '沪锌', 'SN': '沪锡', 'HC': '热卷', 'NI': '沪镍', 'WR': '线材', 'SP': '纸浆'}, '上海国际能源交易中心': {'SC': '原油', 'NR': '20号胶'}}
    """
    temp_df = pd.DataFrame()
    for i in range(1, 4):
        res = requests.get(f"https://www.jiaoyifamen.com/tools/receipt-expire-info/all?page={i}&limit=20", headers=headers)
        temp_df = temp_df.append(pd.DataFrame(res.json()["data"]), ignore_index=True)
    return temp_df


def jyfm_tools_futures_spread(type_1="RB", type_2="RB", code_1="01", code_2="05",  headers="", plot=True):
    """
    获取某两个合约的价差走势数据和图
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


def jyfm_tools_futures_ratio(type_1="RB", type_2="RB", code_1="01", code_2="05",  headers="", plot=True):
    """
    获取某两个合约的价差走势数据和图
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


def jyfm_tools_futures_customize(formula="RB01-1.6*I01-0.5*J01-1200",  headers="", plot=True):
    """
    获取某两个合约的价差走势数据和图
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
    params = {
        "formula": formula
    }
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


def get_futures_csa_seasonally(type_1="RB", type_2="RB", code_1="01", code_2="05", plot=True, headers=""):
    """
    获取某两个合约的价差季节图
    :param type_1: str
    :param type_2: str
    :param code_1: str
    :param code_2: str
    :param plot: Bool
    :return: pd.DataFrame
                      year2019  year2018  year2017  year2016  year2015  year2014  \
    dataCategory
    01-02            452.0     406.0       NaN       NaN       NaN    -262.0
    01-03            408.0     409.0      90.0       NaN       NaN    -249.0
    01-04            380.0     412.0      50.0      60.0       NaN       NaN
    01-05              NaN     377.0      67.0      56.0      20.0       NaN
    01-06              NaN       NaN      48.0      80.0       1.0    -242.0
                    ...       ...       ...       ...       ...       ...
    12-27              NaN     490.0     298.0      -4.0       NaN       NaN
    12-28              NaN     448.0     383.0       NaN      77.0       NaN
    12-29              NaN       NaN     454.0      17.0      67.0      93.0
    12-30              NaN       NaN       NaN      56.0      63.0      44.0
    12-31              NaN       NaN       NaN       NaN      61.0       1.0
                  year2013
    dataCategory
    01-02              NaN
    01-03              NaN
    01-04           -121.0
    01-05              NaN
    01-06              NaN
                    ...
    12-27           -174.0
    12-28              NaN
    12-29              NaN
    12-30           -194.0
    12-31           -223.0
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
    big_df = pd.DataFrame()
    name_list = []
    for item in list(data_json.keys()):
        if item not in ["category", "value"]:
            name_list.append(item)
            big_df = pd.concat([big_df, pd.DataFrame(data_json[item])], axis=1)
    big_df.columns = name_list
    big_df.index = big_df["dataCategory"]
    del big_df["dataCategory"]
    big_df.replace("NaN", np.nan, inplace=True)
    if plot:
        for item in big_df.columns:
            temp_df = big_df[item].dropna()
            temp_df.astype("float").plot()
        plt.legend(loc="best")
        plt.xlabel("date")
        plt.ylabel("value")
        plt.show()
        return big_df
    else:
        return big_df


if __name__ == "__main__":
    headers = jyfm_login(account="jindaxiang@163.com", password="king0575")
    df = jyfm_tools_futures_customize(formula="RB01-1.6*I01-0.5*J01-1200",  headers=headers, plot=True)
    temp_df = pd.DataFrame(df)
    print(temp_df)

