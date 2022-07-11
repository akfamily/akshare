# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/5/2 15:58
Desc: 东方财富-股票-财务分析
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_balance_sheet_by_report_em(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富-股票-财务分析-资产负债表-按报告期
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 资产负债表-按报告期
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "0",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "0",
            "reportType": "1",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_balance_sheet_by_yearly_em(symbol: str = "SZ000001") -> pd.DataFrame:
    """
    东方财富-股票-财务分析-资产负债表-按年度
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 资产负债表-按年度
    :rtype: pandas.DataFrame
    """
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbDateAjaxNew"
    company_type = 3 if symbol[:2] == "SZ" else 4
    params = {
        "companyType": company_type,
        "reportDateType": "1",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "1",
            "reportType": "1",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_profit_sheet_by_report_em(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富-股票-财务分析-利润表-报告期
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 利润表-报告期
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "0",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "0",
            "reportType": "1",
            "code": symbol,
            "dates": item,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_profit_sheet_by_yearly_em(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富-股票-财务分析-利润表-按年度
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 利润表-按年度
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "1",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "1",
            "reportType": "1",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_profit_sheet_by_quarterly_em(
    symbol: str = "SH600519",
) -> pd.DataFrame:
    """
    东方财富-股票-财务分析-利润表-按单季度
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 利润表-按单季度
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "2",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "0",
            "reportType": "2",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_cash_flow_sheet_by_report_em(
    symbol: str = "SH600519",
) -> pd.DataFrame:
    """
    东方财富-股票-财务分析-现金流量表-按报告期
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 现金流量表-按报告期
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "0",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "0",
            "reportType": "1",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_cash_flow_sheet_by_yearly_em(
    symbol: str = "SH600519",
) -> pd.DataFrame:
    """
    东方财富-股票-财务分析-现金流量表-按年度
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 现金流量表-按年度
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "1",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "1",
            "reportType": "1",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


def stock_cash_flow_sheet_by_quarterly_em(
    symbol: str = "SH600519",
) -> pd.DataFrame:
    """
    东方财富-股票-财务分析-现金流量表-按单季度
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 现金流量表-按单季度
    :rtype: pandas.DataFrame
    """
    company_type = 3 if symbol[:2] == "SZ" else 4
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "2",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/xjllbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "0",
            "reportType": "2",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


if __name__ == "__main__":
    stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em(
        symbol="SH600519"
    )
    print(stock_balance_sheet_by_report_em_df)

    stock_balance_sheet_by_yearly_em_df = stock_balance_sheet_by_yearly_em(
        symbol="SH600519"
    )
    print(stock_balance_sheet_by_yearly_em_df)

    stock_profit_sheet_by_report_em_df = stock_profit_sheet_by_report_em(
        symbol="SH600519"
    )
    print(stock_profit_sheet_by_report_em_df)

    stock_profit_sheet_by_yearly_em_df = stock_profit_sheet_by_yearly_em(
        symbol="SH600519"
    )
    print(stock_profit_sheet_by_yearly_em_df)

    stock_profit_sheet_by_quarterly_em_df = stock_profit_sheet_by_quarterly_em(
        symbol="SH600519"
    )
    print(stock_profit_sheet_by_quarterly_em_df)

    stock_cash_flow_sheet_by_report_em_df = stock_cash_flow_sheet_by_report_em(
        symbol="SH600519"
    )
    print(stock_cash_flow_sheet_by_report_em_df)

    stock_cash_flow_sheet_by_yearly_em_df = stock_cash_flow_sheet_by_yearly_em(
        symbol="SH600519"
    )
    print(stock_cash_flow_sheet_by_yearly_em_df)

    stock_cash_flow_sheet_by_quarterly_em_df = (
        stock_cash_flow_sheet_by_quarterly_em(symbol="SH600519")
    )
    print(stock_cash_flow_sheet_by_quarterly_em_df)
