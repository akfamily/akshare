#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/1/10 19:00
Desc: 99 期货网-大宗商品库存数据
http://www.99qh.com/d/store.aspx
"""
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.futures.cons import (
    qh_headers,
    sample_headers,
)


def futures_inventory_99(
        exchange: str = "大连商品交易所", symbol: str = "豆一"
) -> pd.DataFrame:
    """
    99 期货网-大宗商品库存数据
    http://www.99qh.com/d/store.aspx
    :param exchange: 交易所名称; choice of {"上海期货交易所", "郑州商品交易所", "大连商品交易所", "LME", "NYMEX", "CBOT", "NYBOT", "TOCOM", "上海国际能源交易中心", "OSE"}
    :type exchange: str
    :param symbol: 交易所对应的具体品种; 如：大连商品交易所的 豆一
    :type symbol: str
    :return: 大宗商品库存数据
    :rtype: pandas.DataFrame
    """
    data_code = {
        "1": [
            "1",
            "2",
            "3",
            "12",
            "32",
            "36",
            "37",
            "40",
            "42",
            "47",
            "56",
            "63",
            "69",
            "70",
            "79",
            "85",
        ],
        "2": [
            "4",
            "14",
            "29",
            "31",
            "33",
            "38",
            "44",
            "45",
            "50",
            "51",
            "52",
            "55",
            "59",
            "64",
            "66",
            "67",
            "75",
            "76",
            "81",
            "82",
            "87",
            "92",
            "95",
        ],
        "3": [
            "6",
            "7",
            "8",
            "15",
            "30",
            "34",
            "35",
            "39",
            "43",
            "53",
            "57",
            "58",
            "61",
            "62",
            "68",
            "80",
            "84",
            "86",
            "88",
            "89",
            "94",
        ],
        "4": ["9", "10", "16", "17", "18", "23", "28"],
        "5": ["11", "20", "21"],
        "6": ["13", "24", "25", "26", "27"],
        "7": ["19"],
        "8": ["22"],
        "10": ["78", "83", "90", "93"],
        "11": ["91"],
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
            "动力煤",
            "粳稻",
            "晚籼稻",
            "硅铁",
            "锰硅",
            "棉纱",
            "苹果",
            "红枣",
            "尿素",
            "纯碱",
            "短纤",
            "花生",
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
            "胶合板",
            "聚丙烯",
            "玉米淀粉",
            "乙二醇",
            "粳米",
            "苯乙烯",
            "纤维板",
            "液化石油气",
            "生猪",
        ],
        "4": ["LME铜", "LME铝", "LME镍", "LME铅", "LME锌", "LME锡", "LME铝合金"],
        "5": ["COMEX铜", "COMEX金", "COMEX银"],
        "6": ["CBOT大豆", "CBOT小麦", "CBOT玉米", "CBOT燕麦", "CBOT糙米"],
        "7": ["NYBOT2号棉"],
        "8": ["TOCOM橡胶"],
        "10": ["原油", "20号胶", "低硫燃料油", "国际铜"],
        "11": ["OSE橡胶"],
    }
    temp_out_exchange_name = {
        "1": "上海期货交易所",
        "2": "郑州商品交易所",
        "3": "大连商品交易所",
        "4": "LME",
        "5": "NYMEX",
        "6": "CBOT",
        "7": "NYBOT",
        "8": "TOCOM",
        "10": "上海国际能源交易中心",
        "11": "OSE",
    }
    exchange_map = {
        value: key for key, value in temp_out_exchange_name.items()
    }
    exchange = exchange_map[exchange]
    temp_symbol_code_map = dict(zip(data_name[exchange], data_code[exchange]))
    symbol = temp_symbol_code_map[symbol]
    out_exchange_name = {
        "1": "上海期货交易所",
        "2": "郑州商品交易所",
        "3": "大连商品交易所",
        "4": "LME",
        "5": "NYMEX",
        "6": "CBOT",
        "7": "NYBOT",
        "8": "TOCOM",
        "10": "上海国际能源交易中心",
        "11": "OSE",
    }
    name_temp_dict = {}
    code_temp_dict = {}
    for num in data_code.keys():
        name_temp_dict[out_exchange_name[num]] = dict(
            zip(data_code[num], data_name[num])
        )
        code_temp_dict[num] = dict(zip(data_code[num], data_name[num]))
    n = 10
    while n != 0:
        try:
            n -= 1
            session = requests.Session()
            url = "http://service.99qh.com/Storage/Storage.aspx"
            params = {"page": "99qh"}
            r = session.post(url, params=params, headers=sample_headers)
            cookie = r.cookies.get_dict()
            url = "http://service.99qh.com/Storage/Storage.aspx"
            params = {"page": "99qh"}
            r = requests.post(
                url, params=params, headers=sample_headers, cookies=cookie
            )
            soup = BeautifulSoup(r.text, "lxml")
            view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
            even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[
                0
            ]["value"]
            payload = {
                "__EVENTTARGET": "ddlExchName",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": view_state,
                "__VIEWSTATEGENERATOR": "6EAC22FA",
                "__EVENTVALIDATION": even_validation,
                "ddlExchName": int(exchange),
                "ddlGoodsName": 1,
            }
            res = requests.post(
                url,
                params={"page": "99qh"},
                data=payload,
                headers=qh_headers,
                cookies=cookie,
            )
            soup = BeautifulSoup(res.text, "lxml")
            view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
            even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[
                0
            ]["value"]
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
            res = requests.post(
                url,
                params=params,
                data=payload,
                headers=qh_headers,
                cookies=cookie,
            )
            data_df = pd.read_html(StringIO(res.text))[-1].T
            data_df.columns = data_df.iloc[0, :]
            data_df = data_df.iloc[1:, :]
            data_df.reset_index(inplace=True, drop=True)
            data_df.columns.name = None
            data_df["日期"] = pd.to_datetime(data_df["日期"]).dt.date
            data_df["库存"] = pd.to_numeric(data_df["库存"])
            data_df["增减"] = pd.to_numeric(data_df["增减"])
            data_df.sort_values("日期", inplace=True)
            data_df.reset_index(inplace=True, drop=True)
            return data_df
        except:
            continue


if __name__ == "__main__":
    futures_inventory_99_df = futures_inventory_99(
        exchange="郑州商品交易所", symbol="菜籽油"
    )
    print(futures_inventory_99_df)
