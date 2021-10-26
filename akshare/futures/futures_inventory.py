#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/1/13 13:58
Desc: 99 期货网-大宗商品库存数据
http://www.99qh.com/d/store.aspx
"""
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.futures.cons import (
    qh_headers,
    sample_headers,
    inventory_temp_headers,
)


def futures_inventory_99(
    exchange: int = 3, symbol: int = 11, plot: bool = False
) -> pd.DataFrame:
    """
    调用此函数, 请调用 try except
    # 交易所代码
    {'1': '上海期货交易所', '2': '郑州商品交易所', '3': '大连商品交易所', '7': 'LME', '8': 'NYMEX', '9': 'CBOT', '11': 'NYBOT', '12': 'TOCOM', '14': '上海国际能源交易中心', '15': 'OSE'}
    # 交易所对应合约代码
    '上海期货交易所': {'6': '铜', '7': '铝', '8': '橡胶', '21': '燃料油', '54': '锌', '58': '黄金', '59': '螺纹钢', '62': '线材', '64': '铅', '69': '白银', '78': '石油沥青', '85': '热轧卷板', '93': '锡', '94': '镍', '103': '纸浆', '109': '不锈钢'},
    '郑州商品交易所': {'9': '强麦', '10': '硬麦', '23': '一号棉', '51': '白糖', '53': 'PTA', '55': '菜籽油', '60': '早籼稻', '66': '甲醇',
    '67': '普麦', '72': '玻璃', '73': '油菜籽', '74': '菜籽粕', '81': '粳稻', '88': '晚籼稻',
    '90': '硅铁', '91': '锰硅', '99': '棉纱', '100': '苹果', '105': '红枣', '106': '尿素', '111': '纯碱'},
    '大连商品交易所': {'11': '豆一', '12': '豆二', '16': '豆粕', '24': '玉米', '52': '豆油', '56': '聚乙烯',
    '57': '棕榈油', '61': '聚氯乙烯', '65': '焦炭', '75': '焦煤', '79': '铁矿石', '80': '鸡蛋',
    '82': '中密度纤维板', '83': '细木工板', '84': '聚丙烯', '92': '玉米淀粉', '104': '乙二醇', '108': '粳米', '110': '苯乙烯', '112': '纤维板', '113': '液化石油气'},
    '上海国际能源交易中心': {'102': '原油', '107': '20号胶', '114': '低硫燃料油'}}
    'LME': {'18': 'LME铜', '19': 'LME铝', '25': 'LME镍', '26': 'LME铅', '27': 'LME锌', '45': 'LME锡', '50': 'LME铝合金'},
    'NYMEX': {'20': 'COMEX铜', '31': 'COMEX金', '32': 'COMEX银'},
    'CBOT': {'22': 'CBOT大豆', '46': 'CBOT小麦', '47': 'CBOT玉米', '48': 'CBOT燕麦', '49': 'CBOT糙米'},
    'NYBOT': {'30': 'NYBOT2号棉'}
    'TOCOM': {'44': 'TOCOM橡胶'}
    'OSE': {'44': 'OSE橡胶'}
    :param exchange: int 交易所, 请对照 __doc__ 中的代码输入
    :param symbol: int 品种, 请对照 __doc__ 中的代码输入对应交易所的品种
    # :param dir_path: str 存放图片的目录
    :param plot: Bool 画出历史库存曲线图
    :return: pandas.DataFrame and picture
    """
    data_code = {
        "1": [
            "6",
            "7",
            "8",
            "21",
            "54",
            "58",
            "59",
            "62",
            "64",
            "69",
            "78",
            "85",
            "93",
            "94",
            "103",
            "109",
        ],
        "2": [
            "9",
            "10",
            "23",
            "51",
            "53",
            "55",
            "60",
            "66",
            "67",
            "72",
            "73",
            "74",
            "81",
            "88",
            "90",
            "91",
            "99",
            "100",
            "105",
            "106",
            "111",
        ],
        "3": [
            "11",
            "12",
            "16",
            "24",
            "52",
            "56",
            "57",
            "61",
            "65",
            "75",
            "79",
            "80",
            "82",
            "83",
            "84",
            "92",
            "104",
            '108',
            '110',
            '112',
            '113',
        ],
        "7": ["18", "19", "25", "26", "27", "45", "50"],
        "8": ["20", "31", "32"],
        "9": ["22", "46", "47", "48", "49"],
        "11": ["30"],
        "12": ["44"],
        "14": ["102",
               '107',
               '114'],
        "15": ["6"],
    }
    data_name = {
        "1": [
            "铜",
            "铝",
            "橡胶",
            "燃料油",
            "锌",
            "黄金",
            "螺纹钢",
            "线材",
            "铅",
            "白银",
            "石油沥青",
            "热轧卷板",
            "锡",
            "镍",
            "纸浆",
            "不锈钢",
        ],
        "2": [
            "强麦",
            "硬麦",
            "一号棉",
            "白糖",
            "PTA",
            "菜籽油",
            "早籼稻",
            "甲醇",
            "普麦",
            "玻璃",
            "油菜籽",
            "菜籽粕",
            "粳稻",
            "晚籼稻",
            "硅铁",
            "锰硅",
            "棉纱",
            "苹果",
            "红枣",
            "尿素",
            "纯碱",
        ],
        "3": [
            "豆一",
            "豆二",
            "豆粕",
            "玉米",
            "豆油",
            "聚乙烯",
            "棕榈油",
            "聚氯乙烯",
            "焦炭",
            "焦煤",
            "铁矿石",
            "鸡蛋",
            "中密度纤维板",
            "细木工板",
            "聚丙烯",
            "玉米淀粉",
            "乙二醇",
            '粳米',
            '苯乙烯',
            '纤维板',
            '液化石油气',
        ],
        "7": ["LME铜", "LME铝", "LME镍", "LME铅", "LME锌", "LME锡", "LME铝合金"],
        "8": ["COMEX铜", "COMEX金", "COMEX银"],
        "9": ["CBOT大豆", "CBOT小麦", "CBOT玉米", "CBOT燕麦", "CBOT糙米"],
        "11": ["NYBOT2号棉"],
        "12": ["TOCOM橡胶"],
        "14": ["原油", '20号胶', '低硫燃料油'],
        "15": ["OSE橡胶"],
    }
    out_exchange_name = {
        "1": "上海期货交易所",
        "2": "郑州商品交易所",
        "3": "大连商品交易所",
        "7": "LME",
        "8": "NYMEX",
        "9": "CBOT",
        "11": "NYBOT",
        "12": "TOCOM",
        "14": "上海国际能源交易中心",
        "15": "OSE",
    }
    name_temp_dict = {}
    code_temp_dict = {}
    for num in data_code.keys():
        name_temp_dict[out_exchange_name[num]] = dict(
            zip(data_code[num], data_name[num])
        )
        code_temp_dict[num] = dict(zip(data_code[num], data_name[num]))
    while True:
        try:

            if exchange != 1:
                url = "http://service.99qh.com/Storage/Storage.aspx"
                params = {
                    "page": "99qh"
                }
                res = requests.get(url, params=params, headers=sample_headers)
                soup = BeautifulSoup(res.text, "lxml")
                view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
                even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0][
                    "value"
                ]
                # print(symbol)
                payload = {
                    "__EVENTTARGET": "ddlExchName",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": view_state,
                    "__VIEWSTATEGENERATOR": "6EAC22FA",
                    "__EVENTVALIDATION": even_validation,
                    "ddlExchName": int(exchange),
                    "ddlGoodsName": 6,
                }
                res = requests.post(url, data=payload, headers=qh_headers)
                soup = BeautifulSoup(res.text, "lxml")
                exchange_name = (
                    soup.find_all("select")[0]
                    .find_all(attrs={"selected": "selected"})[0]
                    .get_text()
                )
                # print("切换后", exchange_name)
                view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
                even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0][
                    "value"
                ]
                payload = {
                    "__EVENTTARGET": "ddlGoodsName",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": view_state,
                    "__VIEWSTATEGENERATOR": "6EAC22FA",
                    "__EVENTVALIDATION": even_validation,
                    "ddlExchName": int(exchange),
                    "ddlGoodsName": int(symbol),
                }
                res = requests.post(url, data=payload, headers=qh_headers)
                soup = BeautifulSoup(res.text, "lxml")
                small_code = (
                    soup.find_all(attrs={"id": "chartData"})[0]["src"]
                    .split("&")[-2]
                    .split("=")[1]
                )
                # print(small_code)
                payload = {
                    "__EVENTTARGET": "btnZoomAll",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": view_state,
                    "__VIEWSTATEGENERATOR": "6EAC22FA",
                    "__EVENTVALIDATION": even_validation,
                    "ddlExchName": int(exchange),
                    "ddlGoodsName": int(symbol),
                }
                res = requests.post(url, data=payload, headers=qh_headers)
                soup = BeautifulSoup(res.text, "lxml")
                inventory_table = pd.read_html(res.text)[-1].T
                inventory_table.columns = inventory_table.iloc[0, :]
                inventory_table = inventory_table.iloc[1:, :]
                inventory_table.reset_index(inplace=True, drop=True)
                inventory_table.columns.name = None

                params = {
                    "ChartDirectorChartImage": "chart_chartData",
                    "cacheId": soup.find_all(attrs={"id": "chartData"})[0]["src"]
                    .split("&")[-2]
                    .split("=")[1],
                    "page": "99qh",
                }
                res = requests.get(
                    "http://service.99qh.com/Storage/Storage.aspx",
                    params=params,
                    headers=inventory_temp_headers,
                )
                if plot:
                    with open(
                        "{}_{}.jpg".format(
                            exchange_name, code_temp_dict[str(exchange)][str(symbol)]
                        ),
                        "wb",
                    ) as fs:
                        print("保存图片到本地: {}".format(os.getcwd()))
                        fs.write(res.content)
                return inventory_table

            else:
                url = "http://service.99qh.com/Storage/Storage.aspx"
                params = {
                    "page": "99qh"
                }
                res = requests.get(url, params=params, headers=sample_headers)
                soup = BeautifulSoup(res.text, "lxml")
                view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
                even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0][
                    "value"
                ]
                url = "http://service.99qh.com/Storage/Storage.aspx"
                params = {
                    "page": "99qh"
                }
                res = requests.get(url, params=params, headers=sample_headers)
                soup = BeautifulSoup(res.text, "lxml")
                view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
                even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0][
                    "value"
                ]
                # print(symbol)
                payload = {
                    "__EVENTTARGET": "btnZoomAll",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": view_state,
                    "__VIEWSTATEGENERATOR": "6EAC22FA",
                    "__EVENTVALIDATION": even_validation,
                    "ddlExchName": int(exchange),
                    "ddlGoodsName": int(symbol),
                }
                res = requests.post(url, data=payload, headers=qh_headers)
                inventory_table = pd.read_html(res.text)[-1].T
                inventory_table.columns = inventory_table.iloc[0, :]
                inventory_table = inventory_table.iloc[1:, :]
                inventory_table.reset_index(inplace=True, drop=True)
                inventory_table.columns.name = None

                soup = BeautifulSoup(res.text, "lxml")
                exchange_name = (
                    soup.find_all("select")[0]
                    .find_all(attrs={"selected": "selected"})[0]
                    .get_text()
                )
                params = {
                    "ChartDirectorChartImage": "chart_chartData",
                    "cacheId": soup.find_all(attrs={"id": "chartData"})[0]["src"]
                    .split("&")[-2]
                    .split("=")[1],
                    "page": "99qh",
                }
                res = requests.get(
                    "http://service.99qh.com/Storage/Storage.aspx",
                    params=params,
                    headers=inventory_temp_headers,
                )
                if plot:
                    with open(
                        "{}_{}.jpg".format(
                            exchange_name, code_temp_dict[str(exchange)][str(symbol)]
                        ),
                        "wb",
                    ) as fs:
                        print("保存图片到本地: {}".format(os.getcwd()))
                        fs.write(res.content)
                return inventory_table
        except:
            continue


if __name__ == "__main__":
    futures_inventory_99_df = futures_inventory_99(exchange=1, symbol=6, plot=False)
    print(futures_inventory_99_df)
