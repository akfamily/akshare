#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/3/4 17:00
Desc: 港股-基本面数据
https://emweb.securities.eastmoney.com/PC_HKF10/FinancialAnalysis/index?type=web&code=00700
"""

from typing import Dict

import pandas as pd
import requests

from akshare.exceptions import APIError


def _get_hk_financial_report_list(stock: str) -> pd.DataFrame:
    """
    获取东方财富港股财务报告摘要列表。

    :param stock: 股票代码
    :type stock: str
    :return: 财务报告摘要列表
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_CUSTOM_HKSK_APPFN_CASHFLOW_SUMMARY",
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,START_DATE,REPORT_DATE,FISCAL_YEAR,"
        "CURRENCY,ACCOUNT_STANDARD,REPORT_TYPE",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{stock}.HK")',
        "source": "F10",
        "client": "PC",
        "v": "02092616586970355",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    result_data = data_json.get("result", {}).get("data", [])
    if not result_data:
        raise APIError(f"东方财富港股财务摘要接口未返回有效数据: {stock}")
    report_list = result_data[0].get("REPORT_LIST", [])
    if not isinstance(report_list, list):
        raise APIError(f"东方财富港股财务摘要接口返回格式异常: {stock}")
    return pd.DataFrame(report_list)


def _get_hk_financial_currency_map(stock: str) -> Dict[pd.Timestamp, str]:
    """
    获取港股财务报告日期到币种的映射表。

    :param stock: 股票代码
    :type stock: str
    :return: 报告日期到币种的映射
    :rtype: dict
    """
    report_df = _get_hk_financial_report_list(stock=stock)
    if report_df.empty or "REPORT_DATE" not in report_df.columns:
        return {}
    currency_df = report_df.loc[:, ["REPORT_DATE", "CURRENCY"]].copy()
    currency_df["REPORT_DATE_KEY"] = pd.to_datetime(
        currency_df["REPORT_DATE"], errors="coerce"
    )
    currency_df = currency_df.dropna(subset=["REPORT_DATE_KEY"])
    currency_df = currency_df.drop_duplicates(subset=["REPORT_DATE_KEY"], keep="first")
    return dict(zip(currency_df["REPORT_DATE_KEY"], currency_df["CURRENCY"]))


def stock_financial_hk_report_em(
    stock: str = "00700", symbol: str = "资产负债表", indicator: str = "年度"
) -> pd.DataFrame:
    """
    东方财富-港股-财务报表-三大报表
    https://emweb.securities.eastmoney.com/PC_HKF10/FinancialAnalysis/index?type=web&code=00700
    :param stock: 股票代码
    :type stock: str
    :param symbol: choice of {"资产负债表", "利润表", "现金流量表"}
    :type symbol: str
    :param indicator: choice of {"年度", "报告期"}
    :type indicator: str
    :return: 东方财富-港股-财务报表-三大报表
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    temp_df = _get_hk_financial_report_list(stock=stock)
    if indicator == "年度":
        temp_df = temp_df[temp_df["REPORT_TYPE"] == "年报"]
    else:
        temp_df = temp_df
    year_list = [item.split(" ")[0] for item in temp_df["REPORT_DATE"]]
    if symbol == "资产负债表":
        params = {
            "reportName": "RPT_HKF10_FN_BALANCE_PC",
            "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,REPORT_DATE,DATE_TYPE_CODE,"
            "FISCAL_YEAR,STD_ITEM_CODE,STD_ITEM_NAME,AMOUNT,STD_REPORT_DATE",
            "quoteColumns": "",
            "filter": f"""(SECUCODE="{stock}.HK")(REPORT_DATE in ({"'" + "','".join(year_list) + "'"}))""",
            "pageNumber": "1",
            "pageSize": "",
            "sortTypes": "-1,1",
            "sortColumns": "REPORT_DATE,STD_ITEM_CODE",
            "source": "F10",
            "client": "PC",
            "v": "01975982096513973",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        return temp_df
    elif symbol == "利润表":
        params = {
            "reportName": "RPT_HKF10_FN_INCOME_PC",
            "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,REPORT_DATE,DATE_TYPE_CODE,"
            "FISCAL_YEAR,START_DATE,STD_ITEM_CODE,STD_ITEM_NAME,AMOUNT",
            "quoteColumns": "",
            "filter": f"""(SECUCODE="{stock}.HK")(REPORT_DATE in ({"'" + "','".join(year_list) + "'"}))""",
            "pageNumber": "1",
            "pageSize": "",
            "sortTypes": "-1,1",
            "sortColumns": "REPORT_DATE,STD_ITEM_CODE",
            "source": "F10",
            "client": "PC",
            "v": "01975982096513973",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        return temp_df
    elif symbol == "现金流量表":
        params = {
            "reportName": "RPT_HKF10_FN_CASHFLOW_PC",
            "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,REPORT_DATE,DATE_TYPE_CODE,"
            "FISCAL_YEAR,START_DATE,STD_ITEM_CODE,STD_ITEM_NAME,AMOUNT",
            "quoteColumns": "",
            "filter": f"""(SECUCODE="{stock}.HK")(REPORT_DATE in ({"'" + "','".join(year_list) + "'"}))""",
            "pageNumber": "1",
            "pageSize": "",
            "sortTypes": "-1,1",
            "sortColumns": "REPORT_DATE,STD_ITEM_CODE",
            "source": "F10",
            "client": "PC",
            "v": "01975982096513973",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        return temp_df
    else:
        return pd.DataFrame()


def stock_financial_hk_analysis_indicator_em(
    symbol: str = "00853", indicator: str = "年度"
) -> pd.DataFrame:
    """
    东方财富-港股-财务分析-主要指标
    https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/index?type=web&code=00700
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"年度", "报告期"}
    :type indicator: str
    :return: 东方财富-港股-财务分析-主要指标
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_HKF10_FN_MAININDICATOR",
        "columns": "HKF10_FN_MAININDICATOR",
        "quoteColumns": "",
        "pageNumber": "1",
        "pageSize": "9",
        "sortTypes": "-1",
        "sortColumns": "STD_REPORT_DATE",
        "source": "F10",
        "client": "PC",
        "v": "01975982096513973",
    }
    if indicator == "年度":
        params.update({"filter": f"""(SECUCODE="{symbol}.HK")(DATE_TYPE_CODE="001")"""})
    else:
        params.update({"filter": f"""(SECUCODE="{symbol}.HK")"""})
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    if (
        not temp_df.empty
        and "REPORT_DATE" in temp_df.columns
        and "CURRENCY" in temp_df.columns
    ):
        currency_map = _get_hk_financial_currency_map(stock=symbol)
        if currency_map:
            temp_df["REPORT_DATE_KEY"] = pd.to_datetime(
                temp_df["REPORT_DATE"], errors="coerce"
            )
            temp_df["CURRENCY"] = (
                temp_df["REPORT_DATE_KEY"].map(currency_map).fillna(temp_df["CURRENCY"])
            )
            temp_df.drop(columns=["REPORT_DATE_KEY"], inplace=True)
    return temp_df


if __name__ == "__main__":
    stock_financial_hk_analysis_indicator_em_df = (
        stock_financial_hk_analysis_indicator_em(symbol="00700", indicator="年度")
    )
    print(stock_financial_hk_analysis_indicator_em_df)

    stock_financial_hk_analysis_indicator_em_df = (
        stock_financial_hk_analysis_indicator_em(symbol="00700", indicator="报告期")
    )
    print(stock_financial_hk_analysis_indicator_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="01742", symbol="资产负债表", indicator="年度"
    )
    print(stock_financial_hk_report_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="01742", symbol="资产负债表", indicator="报告期"
    )
    print(stock_financial_hk_report_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="00700", symbol="利润表", indicator="年度"
    )
    print(stock_financial_hk_report_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="00700", symbol="利润表", indicator="报告期"
    )
    print(stock_financial_hk_report_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="00700", symbol="现金流量表", indicator="年度"
    )
    print(stock_financial_hk_report_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="00700", symbol="现金流量表", indicator="报告期"
    )
    print(stock_financial_hk_report_em_df)
