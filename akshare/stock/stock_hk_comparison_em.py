#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/9/24 15:00
Desc: 东方财富-港股-行业对比
https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/IndustryComparison
"""

import pandas as pd
import requests


def stock_hk_growth_comparison_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-行业对比-成长性对比
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/IndustryComparison
    :param symbol: 股票代码
    :type symbol: str
    :return: 成长性对比
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_PCF10_INDUSTRY_HKGROWTH',
        'columns': 'SECUCODE,SECURITY_CODE,ORG_CODE,REPORT_DATE,TYPE_ID,TYPE_TYPE,'
                   'TYPE_NAME,TYPE_NAME_EN,CORRE_SECURITY_CODE,CORRE_SECUCODE,'
                   'CORRE_SECURITY_NAME,EPS_YOY,OPERATE_INCOME_YOY,OPERATE_PROFIT_YOY,'
                   'TOTAL_ASSET_YOY,EPS_YOY_RANK,OPINCOME_YOY_RANK,OPROFIT_YOY_RANK,TOASSET_YOY_RANK',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}.HK")(CORRE_SECUCODE="{symbol}.HK")',
        'pageNumber': '1',
        'pageSize': '',
        'sortTypes': '',
        'sortColumns': '',
        'source': 'F10',
        'client': 'PC',
        'v': '03313416193688571'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    field_mapping = {
        'CORRE_SECURITY_CODE': '代码',
        'CORRE_SECURITY_NAME': '简称',
        'EPS_YOY': '基本每股收益同比增长率',
        'EPS_YOY_RANK': '基本每股收益同比增长率排名',
        'OPERATE_INCOME_YOY': '营业收入同比增长率',
        'OPINCOME_YOY_RANK': '营业收入同比增长率排名',
        'OPERATE_PROFIT_YOY': '营业利润率同比增长率',
        'OPROFIT_YOY_RANK': '营业利润率同比增长率排名',
        'TOTAL_ASSET_YOY': '基本每股收总资产同比增长率益同比增长率',
        'TOASSET_YOY_RANK': '总资产同比增长率排名',
    }
    temp_df = pd.DataFrame(columns=field_mapping.values())
    if data_json['result'] is not None:
        temp_df = pd.DataFrame(data_json['result']['data'])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[field_mapping.values()]
    return temp_df


def stock_hk_valuation_comparison_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-行业对比-估值对比
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/IndustryComparison
    :param symbol: 股票代码
    :type symbol: str
    :return: 估值对比
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_PCF10_INDUSTRY_HKCVALUE',
        'columns': 'SECUCODE,SECURITY_CODE,ORG_CODE,REPORT_DATE,TYPE_ID,'
                   'TYPE_TYPE,TYPE_NAME,TYPE_NAME_EN,CORRE_SECURITY_CODE,'
                   'CORRE_SECUCODE,CORRE_SECURITY_NAME,PE_TTM,PE_LYR,PB_MQR,'
                   'PB_LYR,PS_TTM,PS_LYR,PCE_TTM,PCE_LYR,PE_TTM_RANK,PE_LYR_RANK,'
                   'PB_MQR_RANK,PB_LYR_RANK,PS_TTM_RANK,PS_LYR_RANK,PCE_TTM_RANK,PCE_LYR_RANK',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}.HK")(CORRE_SECUCODE="{symbol}.HK")',
        'pageNumber': '1',
        'pageSize': '',
        'sortTypes': '',
        'sortColumns': '',
        'source': 'F10',
        'client': 'PC',
        'v': '03445297742754925'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    field_mapping = {
        'CORRE_SECURITY_CODE': '代码',
        'CORRE_SECURITY_NAME': '简称',
        'PE_TTM': '市盈率-TTM',
        'PE_TTM_RANK': '市盈率-TTM排名',
        'PE_LYR': '市盈率-LYR',
        'PE_LYR_RANK': '市盈率-LYR排名',
        'PB_MQR': '市净率-MRQ',
        'PB_MQR_RANK': '市净率-MRQ排名',
        'PB_LYR': '市净率-LYR',
        'PB_LYR_RANK': '市净率-LYR排名',
        'PS_TTM': '市销率-TTM',
        'PS_TTM_RANK': '市销率-TTM排名',
        'PS_LYR': '市销率-LYR',
        'PS_LYR_RANK': '市销率-LYR排名',
        'PCE_TTM': '市现率-TTM',
        'PCE_TTM_RANK': '市现率-TTM排名',
        'PCE_LYR': '市现率-LYR',
        'PCE_LYR_RANK': '市现率-LYR排名',
    }
    temp_df = pd.DataFrame(columns=field_mapping.values())
    if data_json['result'] is not None:
        temp_df = pd.DataFrame(data_json['result']['data'])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[field_mapping.values()]
    return temp_df


def stock_hk_scale_comparison_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-行业对比-规模对比
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/IndustryComparison
    :param symbol: 股票代码
    :type symbol: str
    :return: 规模对比
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_PCF10_INDUSTRY_SCALE',
        'columns': 'SECURITY_CODE,SECUCODE,TYPE_ID,TYPE_TYPE,TYPE_NAME,'
                   'TYPE_NAME_EN,CORRE_SECURITY_CODE,CORRE_SECUCODE,'
                   'CORRE_SECURITY_NAME,MAXSTDREPORTDATE,HKSDQMV,'
                   'HKTOTAL_MARKET_CAP,OPERATE_INCOME,GROSS_PROFIT,'
                   'HKSDQMV_RANK,HKTOTAL_CAP_RANK,OPERATE_INCOME_RANK,GROSS_PROFIT_RANK',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}.HK")(CORRE_SECUCODE="{symbol}.HK")',
        'pageNumber': '1',
        'pageSize': '',
        'sortTypes': '',
        'sortColumns': '',
        'source': 'F10',
        'client': 'PC',
        'v': '07839693368708753'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    field_mapping = {
        'CORRE_SECURITY_CODE': '代码',
        'CORRE_SECURITY_NAME': '简称',
        'HKSDQMV': '总市值',
        'HKSDQMV_RANK': '总市值排名',
        'HKTOTAL_MARKET_CAP': '流通市值',
        'HKTOTAL_CAP_RANK': '流通市值排名',
        'OPERATE_INCOME': '营业总收入',
        'OPERATE_INCOME_RANK': '营业总收入排名',
        'GROSS_PROFIT': '净利润',
        'GROSS_PROFIT_RANK': '净利润排名',
    }
    temp_df = pd.DataFrame(columns=field_mapping.values())
    if data_json['result'] is not None:
        temp_df = pd.DataFrame(data_json['result']['data'])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[field_mapping.values()]
    return temp_df


if __name__ == "__main__":
    stock_hk_growth_comparison_em_df = stock_hk_growth_comparison_em(symbol="03900")
    print(stock_hk_growth_comparison_em_df)

    stock_hk_valuation_comparison_em_df = stock_hk_valuation_comparison_em(symbol="03900")
    print(stock_hk_valuation_comparison_em_df)

    stock_hk_scale_comparison_em_df = stock_hk_scale_comparison_em(symbol="03900")
    print(stock_hk_scale_comparison_em_df)
