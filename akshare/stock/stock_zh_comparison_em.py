#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/9/24 15:00
Desc: 东方财富-行情中心-同行比较
https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj
"""

import pandas as pd
import requests


def stock_zh_growth_comparison_em(symbol: str = "SZ000895") -> pd.DataFrame:
    """
    东方财富-行情中心-同行比较-成长性比较
    https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/czxbj
    :param symbol: 股票代码
    :type symbol: str
    :return: 成长性比较
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_PCF10_INDUSTRY_GROWTH",
        "columns": "ALL",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{symbol[2:]}.{symbol[:2]}")',
        "pageNumber": "",
        "pageSize": "",
        "sortTypes": "1",
        "sortColumns": "PAIMING",
        "source": "HSF10",
        "client": "PC",
        "v": "02747607708067783",
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    field_mapping = {
        "CORRE_SECURITY_CODE": "代码",
        "CORRE_SECURITY_NAME": "简称",
        "MGSY_3Y": "基本每股收益增长率-3年复合",
        "MGSYTB": "基本每股收益增长率-24A",
        "MGSYTTM": "基本每股收益增长率-TTM",
        "MGSY_1E": "基本每股收益增长率-25E",
        "MGSY_2E": "基本每股收益增长率-26E",
        "MGSY_3E": "基本每股收益增长率-27E",
        "YYSR_3Y": "营业收入增长率-3年复合",
        "YYSRTB": "营业收入增长率-24A",
        "YYSRTTM": "营业收入增长率-TTM",
        "YYSR_1E": "营业收入增长率-25E",
        "YYSR_2E": "营业收入增长率-26E",
        "YYSR_3E": "营业收入增长率-27E",
        "JLR_3Y": "净利润增长率-3年复合",
        "JLRTB": "净利润增长率-24A",
        "JLRTTM": "净利润增长率-TTM",
        "JLR_1E": "净利润增长率-25E",
        "JLR_2E": "净利润增长率-26E",
        "JLR_3E": "净利润增长率-27E",
        "PAIMING": "基本每股收益增长率-3年复合排名",
    }

    temp_df = pd.DataFrame(columns=field_mapping.values())
    if data_json["result"] is not None:
        temp_df = pd.DataFrame(data_json["result"]["data"])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[field_mapping.values()]

    return temp_df


def stock_zh_valuation_comparison_em(symbol: str = "SZ000895") -> pd.DataFrame:
    """
    东方财富-行情中心-同行比较-估值比较
    https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/gzbj
    :param symbol: 股票代码
    :type symbol: str
    :return: 估值比较
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_PCF10_INDUSTRY_CVALUE",
        "columns": "ALL",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{symbol[2:]}.{symbol[:2]}")',
        "pageNumber": "",
        "pageSize": "",
        "sortTypes": "1",
        "sortColumns": "PAIMING",
        "source": "HSF10",
        "client": "PC",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    field_mapping_result = {
        "CORRE_SECUCODE": "对应证券代码",
        "CORRE_SECURITY_CODE": "代码",
        "CORRE_SECURITY_NAME": "简称",
        "PB": "市净率-24A",
        "PB_MRQ": "市净率-MRQ",
        "PCE": "市现率1-24A",
        "PCE_TTM": "市现率1-TTM",
        "PCF": "市现率2-24A",
        "PCF_TTM": "市现率2-TTM",
        "PEG": "PEG",
        "PE_1Y": "市盈率-25E",
        "PE_2Y": "市盈率-26E",
        "PE_3Y": "市盈率-27E",
        "PE_TTM": "市盈率-TTM",
        "PS": "市销率-24A",
        "PS_1Y": "市销率-25E",
        "PS_2Y": "市销率-26E",
        "PS_3Y": "市销率-27E",
        "PS_TTM": "市销率-TTM",
        "QYBS": "EV/EBITDA-24A",
        "REPORT_DATE": "报告日期",
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "行业标识",
        "TOTAL_COUNT": "证券数量",
        "PAIMING": "排名",
    }
    temp_df.rename(columns=field_mapping_result, inplace=True)
    temp_df = temp_df[
        [
            "排名",
            "代码",
            "简称",
            "PEG",
            "市盈率-TTM",
            "市盈率-25E",
            "市盈率-26E",
            "市盈率-27E",
            "市销率-24A",
            "市销率-TTM",
            "市销率-25E",
            "市销率-26E",
            "市销率-27E",
            "市净率-24A",
            "市净率-MRQ",
            "市现率1-24A",
            "市现率1-TTM",
            "市现率2-24A",
            "市现率2-TTM",
            "EV/EBITDA-24A",
        ]
    ]
    temp_df = pd.concat([temp_df.iloc[-1:], temp_df.iloc[:-1]]).reset_index(drop=True)
    temp_df["排名"] = temp_df["排名"].astype(str)
    temp_df.iloc[0, 0] = (
        f"{temp_df.iloc[0, 0]}/{data_json['result']['data'][0]['TOTAL_COUNT']}"
    )
    row1 = temp_df.iloc[1].copy()
    row2 = temp_df.iloc[2].copy()
    # 交换位置
    temp_df.iloc[1] = row2
    temp_df.iloc[2] = row1
    return temp_df


def stock_zh_dupont_comparison_em(symbol: str = "SZ000895") -> pd.DataFrame:
    """
    东方财富-行情中心-同行比较-杜邦分析比较
    https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/dbfxbj
    :param symbol: 股票代码
    :type symbol: str
    :return: 杜邦分析比较
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_PCF10_INDUSTRY_DBFX",
        "columns": "ALL",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{symbol[2:]}.{symbol[:2]}")',
        "pageNumber": "",
        "pageSize": "",
        "sortTypes": "1",
        "sortColumns": "PAIMING",
        "source": "HSF10",
        "client": "PC",
        "v": "05086361194054821",
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    field_mapping = {
        "CORRE_SECURITY_CODE": "代码",
        "CORRE_SECURITY_NAME": "简称",
        "ROE_AVG": "ROE-3年平均",
        "ROEPJ_L3": "ROE-22A",
        "ROEPJ_L2": "ROE-23A",
        "ROEPJ_L1": "ROE-24A",
        "XSJLL_AVG": "净利率-3年平均",
        "XSJLL_L3": "净利率-22A",
        "XSJLL_L2": "净利率-23A",
        "XSJLL_L1": "净利率-24A",
        "TOAZZL_AVG": "总资产周转率-3年平均",
        "TOAZZL_L3": "总资产周转率-22A",
        "TOAZZL_L2": "总资产周转率-23A",
        "TOAZZL_L1": "总资产周转率-24A",
        "QYCS_AVG": "权益乘数-3年平均",
        "QYCS_L3": "权益乘数-22A",
        "QYCS_L2": "权益乘数-23A",
        "QYCS_L1": "权益乘数-24A",
        "PAIMING": "ROE-3年平均排名",
    }

    temp_df = pd.DataFrame(columns=field_mapping.values())
    if data_json["result"] is not None:
        temp_df = pd.DataFrame(data_json["result"]["data"])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[field_mapping.values()]

    return temp_df


def stock_zh_scale_comparison_em(symbol: str = "SZ000895") -> pd.DataFrame:
    """
    东方财富-行情中心-同行比较-公司规模
    https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=000895&color=b#/thbj/gsgm
    :type symbol: str
    :return: 公司规模
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_PCF10_INDUSTRY_MARKET",
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,"
        "CORRE_SECUCODE,CORRE_SECURITY_CODE,CORRE_SECURITY_NAME,"
        "CORRE_ORG_CODE,TOTAL_CAP,FREECAP,TOTAL_OPERATEINCOME,"
        "NETPROFIT,REPORT_TYPE,TOTAL_CAP_RANK,FREECAP_RANK,"
        "TOTAL_OPERATEINCOME_RANK,NETPROFIT_RANK",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{symbol[2:]}.{symbol[:2]}")(CORRE_SECUCODE="{symbol[2:]}.{symbol[:2]}")',
        "pageNumber": "1",
        "pageSize": "5",
        "sortTypes": "-1",
        "sortColumns": "TOTAL_CAP",
        "source": "HSF10",
        "client": "PC",
        "v": "005391946600478148",
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    field_mapping = {
        "CORRE_SECURITY_CODE": "代码",
        "CORRE_SECURITY_NAME": "简称",
        "TOTAL_CAP": "总市值",
        "TOTAL_CAP_RANK": "总市值排名",
        "FREECAP": "流通市值",
        "FREECAP_RANK": "流通市值排名",
        "TOTAL_OPERATEINCOME": "营业收入",
        "TOTAL_OPERATEINCOME_RANK": "营业收入排名",
        "NETPROFIT": "净利润",
        "NETPROFIT_RANK": "净利润排名",
    }

    temp_df = pd.DataFrame(columns=field_mapping.values())
    if data_json["result"] is not None:
        temp_df = pd.DataFrame(data_json["result"]["data"])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[field_mapping.values()]

    return temp_df


if __name__ == "__main__":
    stock_zh_growth_comparison_em_df = stock_zh_growth_comparison_em(symbol="SZ000895")
    print(stock_zh_growth_comparison_em_df)

    stock_zh_valuation_comparison_em_df = stock_zh_valuation_comparison_em(
        symbol="SZ000895"
    )
    print(stock_zh_valuation_comparison_em_df)

    stock_zh_dupont_comparison_em_df = stock_zh_dupont_comparison_em(symbol="SZ000895")
    print(stock_zh_dupont_comparison_em_df)

    stock_zh_scale_comparison_em_df = stock_zh_scale_comparison_em(symbol="SZ000895")
    print(stock_zh_scale_comparison_em_df)
