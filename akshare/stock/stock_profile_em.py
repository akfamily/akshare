#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/9/11 13:00
Desc: 东方财富-港股-公司概况
https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile
"""

import pandas as pd
import requests


def stock_hk_security_profile_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-证券资料
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile
    :param symbol: 股票代码
    :type symbol: str
    :return: 证券资料
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_HKF10_INFO_SECURITYINFO',
        'columns': 'SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,SECURITY_TYPE,LISTING_DATE,ISIN_CODE,BOARD,'
                   'TRADE_UNIT,TRADE_MARKET,GANGGUTONGBIAODISHEN,GANGGUTONGBIAODIHU,PAR_VALUE,'
                   'ISSUE_PRICE,ISSUE_NUM,YEAR_SETTLE_DAY',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}.HK")',
        'pageNumber': '1',
        'pageSize': '200',
        'sortTypes': '',
        'sortColumns': '',
        'source': 'F10',
        'client': 'PC',
        'v': '04748497219912483'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['result']['data'])
    field_mapping = {
        "BOARD": "板块",
        "GANGGUTONGBIAODIHU": "是否沪港通标的",
        "GANGGUTONGBIAODISHEN": "是否深港通标的",
        "ISIN_CODE": "ISIN（国际证券识别编码）",
        "ISSUE_NUM": "发行量(股)",
        "ISSUE_PRICE": "发行价",
        "LISTING_DATE": "上市日期",
        "PAR_VALUE": "每股面值",
        "SECUCODE": "证券代码",
        "SECURITY_NAME_ABBR": "证券简称",
        "SECURITY_TYPE": "证券类型",
        "TRADE_MARKET": "交易所",
        "TRADE_UNIT": "每手股数",
        "YEAR_SETTLE_DAY": "年结日"
    }
    temp_df.rename(columns=field_mapping, inplace=True)
    temp_df = temp_df[[
        "证券代码",
        "证券简称",
        "上市日期",
        "证券类型",
        "发行价",
        "发行量(股)",
        "每手股数",
        "每股面值",
        "交易所",
        "板块",
        "年结日",
        "ISIN（国际证券识别编码）",
        "是否沪港通标的",
        "是否深港通标的",
    ]]
    return temp_df


def stock_hk_company_profile_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-公司资料
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CompanyProfile
    :param symbol: 股票代码
    :type symbol: str
    :return: 公司资料
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_HKF10_INFO_ORGPROFILE',
        'columns': 'SECUCODE,SECURITY_CODE,ORG_NAME,ORG_EN_ABBR,BELONG_INDUSTRY,FOUND_DATE,CHAIRMAN,'
                   'SECRETARY,ACCOUNT_FIRM,REG_ADDRESS,ADDRESS,YEAR_SETTLE_DAY,EMP_NUM,ORG_TEL,ORG_FAX,ORG_EMAIL,'
                   'ORG_WEB,ORG_PROFILE,REG_PLACE',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}.HK")',
        'pageNumber': '1',
        'pageSize': '200',
        'sortTypes': '',
        'sortColumns': '',
        'source': 'F10',
        'client': 'PC',
        'v': '04748497219912483'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['result']['data'])
    field_mapping = {
        'ACCOUNT_FIRM': '核数师',
        'ADDRESS': '办公地址',
        'BELONG_INDUSTRY': '所属行业',
        'CHAIRMAN': '董事长',
        'EMP_NUM': '员工人数',
        'FOUND_DATE': '公司成立日期',
        'ORG_EMAIL': 'E-MAIL',
        'ORG_EN_ABBR': '英文名称',
        'ORG_FAX': '传真',
        'ORG_NAME': '公司名称',
        'ORG_PROFILE': '公司介绍',
        'ORG_TEL': '联系电话',
        'ORG_WEB': '公司网址',
        'REG_ADDRESS': '注册地址',
        'REG_PLACE': '注册地',
        'SECRETARY': '公司秘书',
        'SECUCODE': '股票代码',
        'SECURITY_CODE': '证券代码',
        'YEAR_SETTLE_DAY': '年结日'
    }
    temp_df.rename(columns=field_mapping, inplace=True)
    temp_df = temp_df[[
        "公司名称",
        "英文名称",
        "注册地",
        "注册地址",
        "公司成立日期",
        "所属行业",
        "董事长",
        "公司秘书",
        "员工人数",
        "办公地址",
        "公司网址",
        "E-MAIL",
        "年结日",
        "联系电话",
        "核数师",
        "传真",
        "公司介绍",
    ]]
    return temp_df


def stock_hk_financial_indicator_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-核心必读-最新指标
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CoreReading
    :param symbol: 股票代码
    :type symbol: str
    :return: 财务指标
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_CUSTOM_HKF10_FN_MAININDICATORMAX',
        'columns': 'ORG_CODE,SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,SECURITY_INNER_CODE,REPORT_DATE,BASIC_EPS,'
                   'PER_NETCASH_OPERATE,BPS,BPS_NEDILUTED,COMMON_ACS,PER_SHARES,ISSUED_COMMON_SHARES,HK_COMMON_SHARES,'
                   'TOTAL_MARKET_CAP,HKSK_MARKET_CAP,OPERATE_INCOME,OPERATE_INCOME_SQ,OPERATE_INCOME_QOQ,'
                   'OPERATE_INCOME_QOQ_SQ,HOLDER_PROFIT,HOLDER_PROFIT_SQ,HOLDER_PROFIT_QOQ,HOLDER_PROFIT_QOQ_SQ,PE_TTM,'
                   'PE_TTM_SQ,PB_TTM,PB_TTM_SQ,NET_PROFIT_RATIO,NET_PROFIT_RATIO_SQ,ROE_AVG,ROE_AVG_SQ,ROA,'
                   'ROA_SQ,DIVIDEND_TTM,DIVIDEND_LFY,DIVI_RATIO,DIVIDEND_RATE,IS_CNY_CODE',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}.HK")',
        'pageNumber': '1',
        'pageSize': '200',
        'sortTypes': '-1',
        'sortColumns': 'REPORT_DATE',
        'source': 'F10',
        'client': 'PC',
        'v': '07945646099062258'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['result']['data'])
    field_mapping = {
        'SECURITY_CODE': '股票代码',
        'BASIC_EPS': '基本每股收益(元)',
        'BPS': '每股净资产(元)',
        'COMMON_ACS': '法定股本(股)',
        'PER_SHARES': '每手股',
        'DIVIDEND_TTM': '每股股息TTM(港元)',
        'DIVI_RATIO': '派息比率(%)',
        'ISSUED_COMMON_SHARES': '已发行股本(股)',
        'HK_COMMON_SHARES': '已发行股本-H股(股)',
        'PER_NETCASH_OPERATE': '每股经营现金流(元)',
        'DIVIDEND_RATE': '股息率TTM(%)',
        'TOTAL_MARKET_CAP': '总市值(港元)',
        'HKSK_MARKET_CAP': '港股市值(港元)',
        'OPERATE_INCOME': '营业总收入',
        'OPERATE_INCOME_QOQ': '营业总收入滚动环比增长(%)',
        'NET_PROFIT_RATIO': '销售净利率(%)',
        'HOLDER_PROFIT': '净利润',
        'HOLDER_PROFIT_QOQ': '净利润滚动环比增长(%)',
        'ROE_AVG': '股东权益回报率(%)',
        'PE_TTM': '市盈率',
        'PB_TTM': '市净率',
        'ROA': '总资产回报率(%)'
    }
    temp_df.rename(columns=field_mapping, inplace=True)
    temp_df = temp_df[[
        "基本每股收益(元)",
        "每股净资产(元)",
        "法定股本(股)",
        "每手股",
        "每股股息TTM(港元)",
        "派息比率(%)",
        "已发行股本(股)",
        "已发行股本-H股(股)",
        "每股经营现金流(元)",
        "股息率TTM(%)",
        "总市值(港元)",
        "港股市值(港元)",
        "营业总收入",
        "营业总收入滚动环比增长(%)",
        "销售净利率(%)",
        "净利润",
        "净利润滚动环比增长(%)",
        "股东权益回报率(%)",
        "市盈率",
        "市净率",
        "总资产回报率(%)"

    ]]
    return temp_df


def stock_hk_dividend_payout_em(symbol: str = "03900") -> pd.DataFrame:
    """
    东方财富-港股-核心必读-分红派息
    https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CoreReading
    :param symbol: 股票代码
    :type symbol: str
    :return: 分红派息
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    params = {
        'reportName': 'RPT_HKF10_MAIN_DIVBASIC',
        'columns': 'SECURITY_CODE,UPDATE_DATE,REPORT_TYPE,EX_DIVIDEND_DATE,DIVIDEND_DATE,'
                   'TRANSFER_END_DATE,YEAR,PLAN_EXPLAIN,IS_BFP',
        'quoteColumns': '',
        'filter': f'(SECURITY_CODE="{symbol}")(IS_BFP="0")',
        'pageNumber': '1',
        'pageSize': '200',
        'sortTypes': '-1,-1',
        'sortColumns': 'NOTICE_DATE,EX_DIVIDEND_DATE',
        'source': 'F10',
        'client': 'PC',
        'v': '035584639294227527'
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    field_mapping = {
        'SECURITY_CODE': '股票代码',
        'UPDATE_DATE': '最新公告日期',
        'REPORT_TYPE': '分配类型',
        'EX_DIVIDEND_DATE': '除净日',
        'DIVIDEND_DATE': '发放日',
        'TRANSFER_END_DATE': '截至过户日',
        'YEAR': '财政年度',
        'PLAN_EXPLAIN': '分红方案',
        'IS_BFP': 'IS_BFP'
    }
    columns = [
        "最新公告日期",
        "财政年度",
        "分红方案",
        "分配类型",
        "除净日",
        "截至过户日",
        "发放日",
    ]

    temp_df = pd.DataFrame(columns=columns)
    if data_json['result'] is not None:
        temp_df = pd.DataFrame(data_json['result']['data'])
        temp_df.rename(columns=field_mapping, inplace=True)
        temp_df = temp_df[columns]
        temp_df['最新公告日期'] = pd.to_datetime(temp_df['最新公告日期'], errors='coerce').dt.date
        temp_df['除净日'] = pd.to_datetime(temp_df['除净日'], errors='coerce').dt.date
        temp_df['发放日'] = pd.to_datetime(temp_df['发放日'], format='%Y-%m-%d', errors='coerce').dt.date
    return temp_df


if __name__ == "__main__":
    stock_hk_security_profile_em_df = stock_hk_security_profile_em(symbol="03900")
    print(stock_hk_security_profile_em_df)

    stock_hk_company_profile_em_df = stock_hk_company_profile_em(symbol="03900")
    print(stock_hk_company_profile_em_df)

    stock_hk_financial_indicator_em_df = stock_hk_financial_indicator_em(symbol="03900")
    print(stock_hk_financial_indicator_em_df)

    stock_hk_dividend_payout_em_df = stock_hk_dividend_payout_em(symbol="03900")
    print(stock_hk_dividend_payout_em_df)
