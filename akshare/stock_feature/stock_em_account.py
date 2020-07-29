# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/27 18:02
Desc: 东方财富网-数据中心-特色数据-股票账户统计
东方财富网-数据中心-特色数据-股票账户统计: 股票账户统计详细数据
http://data.eastmoney.com/cjsj/gpkhsj.html
"""
import demjson
import pandas as pd
import requests
from tqdm import tqdm


def _get_page_num_account() -> int:
    """
    东方财富网-数据中心-特色数据-股票账户统计
    http://data.eastmoney.com/cjsj/gpkhsj.html
    :return: 股票账户统计的总页数
    :rtype: int
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "GPKHData",
        "token": "894050c76af8597a853f5b408b759f5d",
        "st": "SDATE",
        "sr": "-1",
        "p": "1",
        "ps": "50",
        "js": "var CMvgBzme={pages:(tp),data:(x)}",
        "rt": "52589731",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("={") + 1:])
    return data_json["pages"]


def stock_em_account() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股票账户统计
    http://data.eastmoney.com/cjsj/gpkhsj.html
    :return: 股票账户统计数据
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_account()
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "GPKHData",
            "token": "894050c76af8597a853f5b408b759f5d",
            "st": "SDATE",
            "sr": "-1",
            "p": str(page),
            "ps": "50",
            "js": "var CMvgBzme={pages:(tp),data:(x)}",
            "rt": "52589731",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "数据日期",
        "新增投资者-数量",
        "新增投资者-环比",
        "新增投资者-同比",
        "期末投资者-总量",
        "期末投资者-A股账户",
        "期末投资者-B股账户",
        "上证指数-收盘",
        "上证指数-涨跌幅",
        "沪深总市值",
        "沪深户均市值",
    ]
    return temp_df


if __name__ == "__main__":
    stock_em_account_df = stock_em_account()
    print(stock_em_account_df)
