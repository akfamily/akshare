#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/3/27 14:00
Desc: 美股-基本面数据
https://emweb.eastmoney.com/PC_USF10/pages/index.html?code=TSLA&type=web&color=w#/cwfx
"""

import pandas as pd

from akshare.utils import http
from akshare.utils.params import reject_old_symbol_usage
from akshare.utils.cons import headers


def __stock_financial_us_report_query_market_em(symbol: str = "TSLA") -> str:
    """
    东方财富-美股-财务分析-三大报表-查询市场
    https://emweb.eastmoney.com/PC_USF10/pages/index.html?code=TSLA&type=web&color=w#/cwfx
    :param symbol: 股票代码
    :type symbol: str
    :return: 查询市场
    :rtype: str
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_USF10_INFO_ORGPROFILE",
        "columns": "SECUCODE,SECURITY_CODE,ORG_CODE,SECURITY_INNER_CODE,ORG_NAME,ORG_EN_ABBR,BELONG_INDUSTRY,"
        "FOUND_DATE,CHAIRMAN,REG_PLACE,ADDRESS,EMP_NUM,ORG_TEL,ORG_FAX,ORG_EMAIL,ORG_WEB,ORG_PROFILE",
        "quoteColumns": "",
        "filter": f'(SECURITY_CODE="{symbol}")',
        "pageNumber": "1",
        "pageSize": "200",
        "sortTypes": "",
        "sortColumns": "",
        "source": "SECURITIES",
        "client": "PC",
        "v": "04406064331266868",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    stock_code = data_json["result"]["data"][0]["SECUCODE"]
    return stock_code


def __stock_financial_us_report_em(
    stock: str = "TSLA", symbol: str = "综合损益表", indicator: str = "年报"
) -> str:
    """
    东方财富-美股-财务分析-三大报表
    https://emweb.eastmoney.com/PC_USF10/pages/index.html?code=TSLA&type=web&color=w#/cwfx
    :param stock: 股票代码
    :type stock: str
    :param symbol: choice of {"资产负债表", "综合损益表", "现金流量表"}
    :type symbol: str
    :param indicator: choice of {"年报", "单季报", "累计季报"}
    :type indicator: str
    :return: 东方财富-美股-财务分析-三大报表
    :rtype: str
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    stock = __stock_financial_us_report_query_market_em(stock)
    if symbol == "资产负债表":
        report_name = "RPT_USF10_FN_BALANCE"
    elif symbol == "综合损益表":
        report_name = "RPT_USF10_FN_INCOME"
    elif symbol == "现金流量表":
        report_name = "RPT_USSK_FN_CASHFLOW"
    else:
        raise ValueError("请输入正确的 symbol 参数")
    params = {
        "reportName": report_name,
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,REPORT,REPORT_DATE,FISCAL_YEAR,CURRENCY,"
        "ACCOUNT_STANDARD,REPORT_TYPE,DATE_TYPE_CODE",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{stock}")',
        "pageNumber": "",
        "pageSize": "",
        "sortTypes": "-1",
        "sortColumns": "REPORT_DATE",
        "source": "SECURITIES",
        "client": "PC",
        "v": "09583551779242467",
    }
    r = http.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_tuple = tuple(dict.fromkeys(temp_df["REPORT"].tolist()))
    if indicator == "年报":
        tuple_data = tuple(item.strip() for item in temp_tuple if "FY" in item)
    elif indicator == "单季报":
        tuple_data = tuple(
            item.strip()
            for item in temp_tuple
            if any(q in item for q in ["Q1", "Q2", "Q3", "Q4"])
        )
    elif indicator == "累计季报":
        tuple_data = tuple(
            item.strip() for item in temp_tuple if "Q6" in item or "Q9" in item
        )
    else:
        raise ValueError("请输入正确的 indicator 参数")
    sorted_tuple = tuple(
        sorted(tuple_data, key=lambda x: x.split("/")[0], reverse=True)
    )
    double_quotes_str = str(sorted_tuple).replace("'", '"')
    double_quotes_str = double_quotes_str.replace(" ", "")
    return double_quotes_str


def stock_financial_us_report_em(
    symbol: str = "TSLA", indicator: str = "资产负债表", period: str = "年报"
) -> pd.DataFrame:
    """
    东方财富-美股-财务分析-三大报表
    https://emweb.eastmoney.com/PC_USF10/pages/index.html?code=TSLA&type=web&color=w#/cwfx
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"资产负债表", "综合损益表", "现金流量表"}
    :type indicator: str
    :param period: choice of {"年报", "单季报", "累计季报"}
    :type period: str
    :return: 东方财富-美股-财务分析-三大报表
    :rtype: pandas.DataFrame
    """
    reject_old_symbol_usage(
        symbol,
        ("资产负债表", "综合损益表", "现金流量表"),
        "stock_financial_us_report_em",
        'symbol="TSLA", indicator="资产负债表", period="年报"',
    )
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    date_str = __stock_financial_us_report_em(
        stock=symbol, symbol=indicator, indicator=period
    )
    symbol = __stock_financial_us_report_query_market_em(symbol)
    if indicator == "资产负债表":
        report_name = "RPT_USF10_FN_BALANCE"
    elif indicator == "综合损益表":
        report_name = "RPT_USF10_FN_INCOME"
    elif indicator == "现金流量表":
        report_name = "RPT_USSK_FN_CASHFLOW"
    else:
        raise ValueError("请输入正确的 symbol 参数")
    params = {
        "reportName": report_name,
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,REPORT_DATE,REPORT_TYPE,REPORT,"
        "STD_ITEM_CODE,AMOUNT,ITEM_NAME",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{symbol}")(REPORT in ' + date_str + ")",
        "pageNumber": "",
        "pageSize": "",
        "sortTypes": "1,-1",
        "sortColumns": "STD_ITEM_CODE,REPORT_DATE",
        "source": "SECURITIES",
        "client": "PC",
        "v": "09583551779242467",
    }
    r = http.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df = temp_df.rename(
        columns={
            "SECUCODE": "证券代码",
            "SECURITY_CODE": "股票代码",
            "SECURITY_NAME_ABBR": "股票简称",
            "REPORT_DATE": "报告期",
            "REPORT_TYPE": "报告类型",
            "REPORT": "报告期名称",
            "STD_ITEM_CODE": "项目代码",
            "AMOUNT": "金额",
            "ITEM_NAME": "项目名称",
        }
    )
    return temp_df


def stock_financial_us_analysis_indicator_em(
    symbol: str = "TSLA", indicator: str = "年报"
) -> pd.DataFrame:
    """
    东方财富-美股-财务分析-主要指标
    https://emweb.eastmoney.com/PC_USF10/pages/index.html?code=TSLA&type=web&color=w#/cwfx
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"年报", "单季报", "累计季报"}
    :type indicator: str
    :return: 东方财富-美股-财务分析-主要指标
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    symbol = __stock_financial_us_report_query_market_em(symbol)
    params = {
        "reportName": "RPT_USF10_FN_GMAININDICATOR",
        "columns": "USF10_FN_GMAININDICATOR",
        "quoteColumns": "",
        "pageNumber": "",
        "pageSize": "",
        "sortTypes": "-1",
        "sortColumns": "REPORT_DATE",
        "source": "SECURITIES",
        "client": "PC",
    }
    if "_" in symbol:
        params["reportName"] = "RPT_USF10_FN_IMAININDICATOR"
        params["columns"] = (
            "ORG_CODE,SECURITY_CODE,SECUCODE,SECURITY_NAME_ABBR,SECURITY_INNER_CODE,"
            "STD_REPORT_DATE,REPORT_DATE,DATE_TYPE,DATE_TYPE_CODE,REPORT_TYPE,REPORT_DATA_TYPE,"
            "FISCAL_YEAR,START_DATE,NOTICE_DATE,ACCOUNT_STANDARD,ACCOUNT_STANDARD_NAME,CURRENCY,"
            "CURRENCY_NAME,ORGTYPE,TOTAL_INCOME,TOTAL_INCOME_YOY,PREMIUM_INCOME,PREMIUM_INCOME_YOY,"
            "PARENT_HOLDER_NETPROFIT,PARENT_HOLDER_NETPROFIT_YOY,BASIC_EPS_CS,BASIC_EPS_CS_YOY,"
            "DILUTED_EPS_CS,PAYOUT_RATIO,CAPITIAL_RATIO,ROE,ROE_YOY,ROA,ROA_YOY,DEBT_RATIO,"
            "DEBT_RATIO_YOY,EQUITY_RATIO"
        )
    if indicator == "年报":
        params.update({"filter": f"""(SECUCODE="{symbol}")(DATE_TYPE_CODE="001")"""})
    elif indicator == "单季报":
        params.update(
            {
                "filter": f"""(SECUCODE="{symbol}")(DATE_TYPE_CODE in ("003","006","007","008"))"""
            }
        )
    elif indicator == "累计季报":
        params.update(
            {"filter": f"""(SECUCODE="{symbol}")(DATE_TYPE_CODE in ("002","004"))"""}
        )
    else:
        raise ValueError("请输入正确的 indicator 参数")
    r = http.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    return temp_df


if __name__ == "__main__":
    stock_financial_us_analysis_indicator_em_df = (
        stock_financial_us_analysis_indicator_em(symbol="BABA", indicator="年报")
    )
    print(stock_financial_us_analysis_indicator_em_df)

    stock_financial_us_analysis_indicator_em_df = (
        stock_financial_us_analysis_indicator_em(symbol="BRK_A", indicator="单季报")
    )
    print(stock_financial_us_analysis_indicator_em_df)

    stock_financial_us_analysis_indicator_em_df = (
        stock_financial_us_analysis_indicator_em(symbol="TSLA", indicator="累计季报")
    )
    print(stock_financial_us_analysis_indicator_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="BRK", indicator="资产负债表", period="年报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="资产负债表", period="单季报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="资产负债表", period="累计季报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="综合损益表", period="年报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="综合损益表", period="单季报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="综合损益表", period="累计季报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="现金流量表", period="年报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="现金流量表", period="单季报"
    )
    print(stock_financial_us_report_em_df)

    stock_financial_us_report_em_df = stock_financial_us_report_em(
        symbol="TSLA", indicator="现金流量表", period="累计季报"
    )
    print(stock_financial_us_report_em_df)
