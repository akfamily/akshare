#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/4/13 13:00
Desc: 股票基本信息
"""
import json
import warnings
from io import BytesIO
from functools import lru_cache

import pandas as pd
import requests
from tqdm import tqdm


def stock_info_sz_name_code(indicator: str = "A股列表") -> pd.DataFrame:
    """
    深圳证券交易所-股票列表
    http://www.szse.cn/market/product/stock/list/index.html
    :param indicator: choice of {"A股列表", "B股列表", "CDR列表", "AB股列表"}
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport"
    indicator_map = {
        "A股列表": "tab1",
        "B股列表": "tab2",
        "CDR列表": "tab3",
        "AB股列表": "tab4",
    }
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "1110",
        "TABKEY": indicator_map[indicator],
        "random": "0.6935816432433362",
    }
    r = requests.get(url, params=params)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content))
    if len(temp_df) > 10:
        if indicator == "A股列表":
            temp_df["A股代码"] = (
                temp_df["A股代码"]
                .astype(str)
                .str.split(".", expand=True)
                .iloc[:, 0]
                .str.zfill(6)
                .str.replace("000nan", "")
            )
            temp_df = temp_df[
                [
                    "板块",
                    "A股代码",
                    "A股简称",
                    "A股上市日期",
                    "A股总股本",
                    "A股流通股本",
                    "所属行业",
                ]
            ]
        elif indicator == "B股列表":
            temp_df["B股代码"] = (
                temp_df["B股代码"]
                .astype(str)
                .str.split(".", expand=True)
                .iloc[:, 0]
                .str.zfill(6)
                .str.replace("000nan", "")
            )
            temp_df = temp_df[
                [
                    "板块",
                    "B股代码",
                    "B股简称",
                    "B股上市日期",
                    "B股总股本",
                    "B股流通股本",
                    "所属行业",
                ]
            ]
        elif indicator == "AB股列表":
            temp_df["A股代码"] = (
                temp_df["A股代码"]
                .astype(str)
                .str.split(".", expand=True)
                .iloc[:, 0]
                .str.zfill(6)
                .str.replace("000nan", "")
            )
            temp_df["B股代码"] = (
                temp_df["B股代码"]
                .astype(str)
                .str.split(".", expand=True)
                .iloc[:, 0]
                .str.zfill(6)
                .str.replace("000nan", "")
            )
            temp_df = temp_df[
                [
                    "板块",
                    "A股代码",
                    "A股简称",
                    "A股上市日期",
                    "B股代码",
                    "B股简称",
                    "B股上市日期",
                    "所属行业",
                ]
            ]
        return temp_df
    else:
        return temp_df


def stock_info_sh_name_code(indicator: str = "主板A股") -> pd.DataFrame:
    """
    上海证券交易所-股票列表
    http://www.sse.com.cn/assortment/stock/list/share/
    :param indicator: choice of {"主板A股": "1", "主板B股": "2", "科创板": "8"}
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    indicator_map = {"主板A股": "1", "主板B股": "2", "科创板": "8"}
    url = "http://query.sse.com.cn/sseQuery/commonQuery.do"
    headers = {
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "STOCK_TYPE": indicator_map[indicator],
        "REG_PROVINCE": "",
        "CSRC_CODE": "",
        "STOCK_CODE": "",
        "sqlId": "COMMON_SSE_CP_GPJCTPZ_GPLB_GP_L",
        "COMPANY_STATUS": "2,4,5,7,8",
        "type": "inParams",
        "isPagination": "true",
        "pageHelp.cacheSize": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.pageSize": "10000",
        "pageHelp.pageNo": "1",
        "pageHelp.endPage": "1",
        "_": "1653291270045",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"])
    columns = [
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "证券简称",
        "扩位证券简称",
        "-",
        "上市日期",
        "-",
        "-",
        "-",
    ]

    # column index 3=A_STOCK_CODE, 8=B_STOCK_CODE, 11=COMPANY_CODE
    if indicator == "主板B股":
        columns[8] = "证券代码"
    else:
        columns[3] = "证券代码"

    temp_df.columns = columns

    temp_df = temp_df[
        [
            "证券代码",
            "证券简称",
            "扩位证券简称",
            "上市日期",
        ]
    ]
    temp_df["上市日期"] = pd.to_datetime(temp_df["上市日期"]).dt.date
    return temp_df


def stock_info_bj_name_code() -> pd.DataFrame:
    """
    北京证券交易所-股票列表
    http://www.bse.cn/nq/listedcompany.html
    :return: 股票列表
    :rtype: pandas.DataFrame
    """
    url = "http://www.bse.cn/nqxxController/nqxxCnzq.do"
    payload = {
        "page": "0",
        "typejb": "T",
        "xxfcbj[]": "2",
        "xxzqdm": "",
        "sortfield": "xxzqdm",
        "sorttype": "asc",
    }
    r = requests.post(url, data=payload)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("[") : -1])
    total_page = data_json[0]["totalPages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(total_page), leave=False):
        payload.update({"page": page})
        r = requests.post(url, data=payload)
        data_text = r.text
        data_json = json.loads(data_text[data_text.find("[") : -1])
        temp_df = data_json[0]["content"]
        temp_df = pd.DataFrame(temp_df)
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [
        "上市日期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "流通股本",
        "-",
        "-",
        "-",
        "-",
        "-",
        "所属行业",
        "-",
        "-",
        "-",
        "-",
        "报告日期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "地区",
        "-",
        "-",
        "-",
        "-",
        "-",
        "券商",
        "总股本",
        "-",
        "证券代码",
        "-",
        "证券简称",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    big_df = big_df[
        [
            "证券代码",
            "证券简称",
            "总股本",
            "流通股本",
            "上市日期",
            "所属行业",
            "地区",
            "报告日期",
        ]
    ]
    big_df["报告日期"] = pd.to_datetime(big_df["报告日期"]).dt.date
    big_df["上市日期"] = pd.to_datetime(big_df["上市日期"]).dt.date
    return big_df


def stock_info_sh_delist() -> pd.DataFrame:
    """
    上海证券交易所-终止上市公司
    http://www.sse.com.cn/assortment/stock/list/delisting/
    :return: 终止上市公司
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/commonQuery.do"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    }
    params = {
        "sqlId": "COMMON_SSE_CP_GPJCTPZ_GPLB_GP_L",
        "isPagination": "true",
        "STOCK_CODE": "",
        "CSRC_CODE": "",
        "REG_PROVINCE": "",
        "STOCK_TYPE": "1,2",
        "COMPANY_STATUS": "3",
        "type": "inParams",
        "pageHelp.cacheSize": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.pageSize": "500",
        "pageHelp.pageNo": "1",
        "pageHelp.endPage": "1",
        "_": "1643035608183",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"])
    temp_df.columns = [
        "-",
        "-",
        "公司简称",
        "-",
        "暂停上市日期",
        "-",
        "-",
        "-",
        "-",
        "上市日期",
        "-",
        "公司代码",
        "-",
    ]
    temp_df = temp_df[
        [
            "公司代码",
            "公司简称",
            "上市日期",
            "暂停上市日期",
        ]
    ]
    temp_df["上市日期"] = pd.to_datetime(temp_df["上市日期"]).dt.date
    temp_df["暂停上市日期"] = pd.to_datetime(temp_df["暂停上市日期"]).dt.date
    return temp_df


def stock_info_sz_delist(indicator: str = "暂停上市公司") -> pd.DataFrame:
    """
    深证证券交易所-暂停上市公司-终止上市公司
    http://www.szse.cn/market/stock/suspend/index.html
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
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content))
        temp_df["证券代码"] = temp_df["证券代码"].astype("str").str.zfill(6)
        return temp_df


def stock_info_sz_change_name(indicator: str = "全称变更") -> pd.DataFrame:
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
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content))
        temp_df["证券代码"] = temp_df["证券代码"].astype("str").str.zfill(6)
        return temp_df


def stock_info_change_name(symbol: str = "000503") -> pd.DataFrame:
    """
    新浪财经-股票曾用名
    http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/300378.phtml
    :param symbol: 股票代码
    :type symbol: str
    :return: 股票曾用名
    :rtype: list
    """
    url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{symbol}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[3].iloc[:, :2]
    temp_df.dropna(inplace=True)
    temp_df.columns = ["item", "value"]
    temp_df["item"] = temp_df["item"].str.split("：", expand=True)[0]
    try:
        name_list = (
            temp_df[temp_df["item"] == "证券简称更名历史"].value.tolist()[0].split(" ")
        )
        big_df = pd.DataFrame(name_list)
        big_df.reset_index(inplace=True)
        big_df["index"] = big_df.index + 1
        big_df.columns = ["index", "name"]
        return big_df
    except IndexError as e:
        return pd.DataFrame()


@lru_cache()
def stock_info_a_code_name() -> pd.DataFrame:
    """
    沪深京 A 股列表
    :return: 沪深京 A 股数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    stock_sh = stock_info_sh_name_code(indicator="主板A股")
    stock_sh = stock_sh[["证券代码", "证券简称"]]

    stock_sz = stock_info_sz_name_code(indicator="A股列表")
    stock_sz["A股代码"] = stock_sz["A股代码"].astype(str).str.zfill(6)
    big_df = pd.concat([big_df, stock_sz[["A股代码", "A股简称"]]], ignore_index=True)
    big_df.columns = ["证券代码", "证券简称"]

    stock_kcb = stock_info_sh_name_code(indicator="科创板")
    stock_kcb = stock_kcb[["证券代码", "证券简称"]]

    stock_bse = stock_info_bj_name_code()
    stock_bse = stock_bse[["证券代码", "证券简称"]]
    stock_bse.columns = ["证券代码", "证券简称"]

    big_df = pd.concat([big_df, stock_sh], ignore_index=True)
    big_df = pd.concat([big_df, stock_kcb], ignore_index=True)
    big_df = pd.concat([big_df, stock_bse], ignore_index=True)
    big_df.columns = ["code", "name"]
    return big_df


if __name__ == "__main__":
    stock_info_sh_name_code_df = stock_info_sh_name_code(indicator="主板A股")
    print(stock_info_sh_name_code_df)

    stock_info_sh_name_code_df = stock_info_sh_name_code(indicator="主板B股")
    print(stock_info_sh_name_code_df)

    stock_info_sz_name_code_df = stock_info_sz_name_code(indicator="A股列表")
    print(stock_info_sz_name_code_df)

    stock_info_sz_df = stock_info_sz_name_code(indicator="B股列表")
    print(stock_info_sz_df)

    stock_info_sz_df = stock_info_sz_name_code(indicator="AB股列表")
    print(stock_info_sz_df)

    stock_info_sz_df = stock_info_sz_name_code(indicator="CDR列表")
    print(stock_info_sz_df)

    stock_info_sh_delist_df = stock_info_sh_delist()
    print(stock_info_sh_delist_df)

    stock_info_sz_change_name_df = stock_info_sz_change_name(indicator="全称变更")
    print(stock_info_sz_change_name_df)

    stock_info_change_name_df = stock_info_change_name(symbol="000503")
    print(stock_info_change_name_df)

    stock_info_a_code_name_df = stock_info_a_code_name()
    print(stock_info_a_code_name_df)

    stock_info_bj_name_code_df = stock_info_bj_name_code()
    print(stock_info_bj_name_code_df)
