# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/19 17:31
Desc: 新浪财经-股票基本信息
"""
import json
from io import BytesIO

import pandas as pd
import requests


def stock_info_sz_name_code(indicator="A股列表"):
    """
    深圳证券交易所-股票列表
    http://www.szse.cn/market/companys/company/index.html
    :param indicator: choice of {"A股列表", "B股列表", "AB股列表", "上市公司列表", "主板", "中小企业板", "创业板"}
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport"
    if indicator in {"A股列表", "B股列表", "AB股列表"}:
        indicator_map = {"A股列表": "tab1", "B股列表": "tab2", "AB股列表": "tab3"}
        params = {
             "SHOWTYPE": "xlsx",
             "CATALOGID": "1110",
             "TABKEY": indicator_map[indicator],
             "random": "0.6935816432433362",
        }
    else:
        indicator_map = {"上市公司列表": "tab1", "主板": "tab2", "中小企业板": "tab3", "创业板": "tab4"}
        params = {
            "SHOWTYPE": "xlsx",
            "CATALOGID": "1110x",
            "TABKEY": indicator_map[indicator],
            "random": "0.6935816432433362",
        }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df["A股代码"] = temp_df["A股代码"].astype(str).str.zfill(6)
    return temp_df


def stock_info_sh_name_code(indicator="主板A股"):
    """
    上海证券交易所-股票列表
    http://www.sse.com.cn/assortment/stock/list/share/
    :param indicator: choice of {"主板A股": "1", "主板B股": "2", "科创板": "8"}
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    indicator_map = {"主板A股": "1", "主板B股": "2", "科创板": "8"}
    url = "http://query.sse.com.cn/security/stock/getStockListData.do"
    headers = {
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "jsonCallBack": "jsonpCallback66942",
        "isPagination": "true",
        "stockCode": "",
        "csrcCode": "",
        "areaName": "",
        "stockType": indicator_map[indicator],
        "pageHelp.cacheSize": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.pageSize": "2000",
        "pageHelp.pageNo": "1",
        "pageHelp.endPage": "11",
        "_": "1589881387934",
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{"):-1])
    temp_df = pd.DataFrame(json_data["result"])
    return temp_df


def stock_info_sh_delist(indicator="暂停上市公司"):
    """
    上海证券交易所-暂停上市公司-终止上市公司
    http://www.sse.com.cn/assortment/stock/list/firstissue/
    :param indicator: choice of {"终止上市公司": "5", "暂停上市公司": "4"}
    :type indicator: str
    :return: 暂停上市公司 or 终止上市公司 的数据
    :rtype: pandas.DataFrame
    """
    indicator_map = {"终止上市公司": "5", "暂停上市公司": "4"}
    url = "http://query.sse.com.cn/security/stock/getStockListData2.do"
    headers = {
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "jsonCallBack": "jsonpCallback66942",
        "isPagination": "true",
        "stockCode": "",
        "csrcCode": "",
        "areaName": "",
        "stockType": indicator_map[indicator],
        "pageHelp.cacheSize": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.pageSize": "2000",
        "pageHelp.pageNo": "1",
        "pageHelp.endPage": "11",
        "_": "1589881387934",
    }
    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{"):-1])
    temp_df = pd.DataFrame(json_data["result"])
    return temp_df


def stock_info_sz_delist(indicator="暂停上市公司"):
    """
    深证证券交易所-暂停上市公司-终止上市公司
    http://www.szse.cn/market/companys/suspend/index.html
    :param indicator: choice of {"暂停上市公司", "终止上市公司"}
    :type indicator: str
    :return: 暂停上市公司 or 终止上市公司 的数据
    :rtype: pandas.DataFrame
    """
    indicator_map = {"暂停上市公司": "tab1", "终止上市公司": "tab2"}
    url = "http://www.szse.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "1793_ssgs",
        "TABKEY": indicator_map[indicator],
        "random": "0.6935816432433362",
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df["证券代码"] = temp_df["证券代码"].astype("str").str.zfill(6)
    return temp_df


def stock_info_sz_change_name(indicator="全称变更"):
    """
    深证证券交易所-更名公司
    http://www.szse.cn/market/companys/changename/index.html
    :param indicator: choice of {"全称变更": "tab1", "简称变更": "tab2"}
    :type indicator: str
    :return: 全称变更 or 简称变更 的数据
    :rtype: pandas.DataFrame
    """
    indicator_map = {"全称变更": "tab1", "简称变更": "tab2"}
    url = "http://www.szse.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "SSGSGMXX",
        "TABKEY": indicator_map[indicator],
        "random": "0.6935816432433362",
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df["证券代码"] = temp_df["证券代码"].astype("str").str.zfill(6)
    return temp_df


def stock_info_change_name(stock="688588"):
    """
    新浪财经-股票曾用名
    http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/300378.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 股票曾用名列表
    :rtype: list
    """
    url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[3].iloc[:, :2]
    temp_df.dropna(inplace=True)
    temp_df.columns = ["item", "value"]
    temp_df["item"] = temp_df["item"].str.split("：", expand=True)[0]
    try:
        name_list = temp_df[temp_df["item"] == "证券简称更名历史"].value.tolist()[0].split(" ")
        return name_list
    except:
        return None


def stock_info_a_code_name():
    """
    沪深 A 股列表
    :return: 沪深 A 股数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    stock_sh = stock_info_sh_name_code(indicator="主板A股")
    stock_sh = stock_sh[["SECURITY_CODE_A", "SECURITY_ABBR_A"]]
    stock_sh.columns = ["公司代码", "公司简称"]

    stock_sz = stock_info_sz_name_code(indicator="A股列表")
    stock_sz["A股代码"] = stock_sz["A股代码"].astype(str).str.zfill(6)
    big_df = big_df.append(stock_sz[["A股代码", "A股简称"]], ignore_index=True)
    big_df.columns = ["公司代码", "公司简称"]
    big_df = big_df.append(stock_sh, ignore_index=True)
    big_df.columns = ["code", "name"]
    return big_df


if __name__ == '__main__':
    for item in {"A股列表", "B股列表", "AB股列表", "上市公司列表", "主板", "中小企业板", "创业板"}:
        stock_info_sz_df = stock_info_sz_name_code(indicator=item)
        print(stock_info_sz_df)

    stock_info_sh_df = stock_info_sh_name_code(indicator="主板A股")
    print(stock_info_sh_df)

    stock_info_sh_delist_df = stock_info_sh_delist(indicator="终止上市公司")
    print(stock_info_sh_delist_df)

    stock_info_sz_delist_df = stock_info_sz_delist(indicator="终止上市公司")
    print(stock_info_sz_delist_df)

    stock_info_sz_change_name_df = stock_info_sz_change_name(indicator="全称变更")
    print(stock_info_sz_change_name_df)

    stock_info_change_name_list = stock_info_change_name(stock="000503")
    print(stock_info_change_name_list)

    stock_info_a_code_name_df = stock_info_a_code_name()
    print(stock_info_a_code_name_df)
