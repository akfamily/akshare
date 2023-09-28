# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/8/11 11:44
Desc: 东方财富网-个股-股票信息
https://quote.eastmoney.com/concept/sh603777.html?from=classic
"""
import pandas as pd
import requests

from akshare.stock_feature.stock_hist_em import code_id_map_em
from akshare.utils import demjson

def stock_individual_info_em(symbol: str = "00600", timeout: float = None) -> pd.DataFrame:
    """
    东方财富-个股-股票信息
    https://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param timeout: choice of None or a positive float number
    :type timeout: float
    :return: 股票信息
    :rtype: pandas.DataFrame
    """
    code_id_dict = code_id_map_em()
    url = "http://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fltt": "2",
        "invt": "2",
        "fields": "f120,f121,f122,f174,f175,f59,f163,f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f255,f256,f257,f258,f127,f199,f128,f198,f259,f260,f261,f171,f277,f278,f279,f288,f152,f250,f251,f252,f253,f254,f269,f270,f271,f272,f273,f274,f275,f276,f265,f266,f289,f290,f286,f285,f292,f293,f294,f295",
        "secid": f"{code_id_dict[symbol]}.{symbol}",
        "_": "1640157544804",
    }
    r = requests.get(url, params=params, timeout=timeout)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df.reset_index(inplace=True)
    del temp_df["rc"]
    del temp_df["rt"]
    del temp_df["svr"]
    del temp_df["lt"]
    del temp_df["full"]
    code_name_map = {
        "f57": "股票代码",
        "f58": "股票简称",
        "f84": "总股本",
        "f85": "流通股",
        "f127": "行业",
        "f116": "总市值",
        "f117": "流通市值",
        "f189": "上市时间",
    }
    temp_df["index"] = temp_df["index"].map(code_name_map)
    temp_df = temp_df[pd.notna(temp_df["index"])]
    if "dlmkts" in temp_df.columns:
        del temp_df["dlmkts"]
    temp_df.columns = [
        "item",
        "value",
    ]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def stock_hk_individual_info_em(symbol: str = "00700") -> pd.DataFrame:
    """
    东方财富网-行情-港股-个股-股票信息
    https://quote.eastmoney.com/hk/00700.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 港股个股公司信息
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/web/api/data/v1/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": f"https://quote.eastmoney.com/hk/{symbol}.html",
    }
    params = {
        "callback": "jQuery35108686720163178234_1695810647631",
        "reportName": "RPT_HK_ORGPROFILE",
        "columns": "SECUCODE,SECURITY_CODE,ORG_CODE,SECURITY_INNER_CODE,SECURITY_NAME_ABBR,ORG_NAME,ORG_EN_ABBR,INDUSTRY,PE,TOTAL_EQUITY,AVERAGEPRICE_30,HK_SHARES,ORG_WEB,TRADE_UNIT",
        "quoteColumns": "",
        "filter": "(SECUCODE=\"%s.HK\")" % symbol,
        "pageNumber": "1",
        "pageSize": "200",
        "sortTypes": "",
        "sortColumns": "",
        "source": "QuoteWeb",
        "client": "WEB",
        "_": "1695810647632",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    data_json = demjson.decode(text_data[text_data.find("{") : -2])
    temp_df = pd.DataFrame(data_json["result"]['data'])
    temp_df.reset_index(inplace=True)
    temp_df = pd.melt(temp_df, var_name="item", value_name="value")
    code_name_map = {
        "SECURITY_CODE": "股票代码",
        "AVERAGEPRICE_30": "30天均价(元)",
        "PE": "PE",
        "ORG_EN_ABBR": "公司英文名",
        "ORG_NAME": "公司名",
        "INDUSTRY": "行业",
        "HK_SHARES": "港股股本(万股)",
        "TOTAL_EQUITY": "总股本(万股)",
        "TRADE_UNIT": "每手股数",
        "ORG_WEB": "网站",
    }
    temp_df["item"] = temp_df["item"].map(code_name_map)
    temp_df = temp_df[pd.notna(temp_df["item"])]
    return temp_df



if __name__ == "__main__":
    stock_individual_info_em_df = stock_individual_info_em(symbol="000001", timeout=None)
    print(stock_individual_info_em_df)

    stock_hk_individual_info_em_df = stock_hk_individual_info_em("00700")
    print(stock_hk_individual_info_em_df)
