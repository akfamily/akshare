#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/1/6 15:15
Desc: 港股-基本面数据
新浪财经-财务分析-财务指标
http://stock.finance.sina.com.cn/hkstock/finance/00700.html#a1
"""
import pandas as pd
import requests


def stock_financial_hk_report_em(
    stock: str = "00700", symbol: str = "现金流量表", indicator: str = "年度"
) -> pd.DataFrame:
    """
    东方财富-港股-财务报表-三大报表
    https://emweb.securities.eastmoney.com/PC_HKF10/FinancialAnalysis/index?type=web&code=00700
    :param stock: 股票代码
    :type stock: str
    :param symbol: choice of {"资产负债表", "利润表", "现金流量表"}
    :type symbol:
    :param indicator: choice of {"年度", "报告期"}
    :type indicator:
    :return: 东方财富-港股-财务报表-三大报表
    :rtype: pandas.DataFrame
    """
    if indicator == "年度":
        rtype = 6
    elif indicator == "报告期":
        rtype = 0
    else:
        raise Exception("请输入正确的 indicator !", indicator)
    if symbol == "资产负债表":
        url = f"https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/GetZCFZB?code={stock}&startdate=&ctype=4&rtype={rtype}"  # 资产负债表
    elif symbol == "利润表":
        url = f"https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/GetLRB?code={stock}&startdate=&ctype=4&rtype={rtype}"  # 利润表
    elif symbol == "现金流量表":
        url = f"https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/GetXJLLB?code={stock}&startdate=&rtype={rtype}"  # 现金流量表
    r = requests.get(url)
    temp_df = pd.DataFrame(eval(r.text)["data"])
    temp_df.columns = temp_df.loc[0]
    temp_df = temp_df.drop(0, axis=0)
    temp_df['截止日期'] = pd.to_datetime(temp_df["截止日期"], format="%y-%m-%d").dt.date
    temp_df.reset_index(drop=True, inplace=True)
    temp_df.columns.name = None
    return temp_df


def stock_financial_hk_analysis_indicator_em(
    symbol: str = "00700", indicator: str = "年度"
) -> pd.DataFrame:
    """
    东方财富-港股-财务分析-主要指标
    https://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/index?type=web&code=00700
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: choice of {"年度", "报告期"}
    :type indicator: str
    :return: 新浪财经-港股-财务分析-主要指标
    :rtype: pandas.DataFrame
    """
    if indicator == "年度":
        key = "zyzb_an"
    elif indicator == "报告期":
        key = "zyzb_abgq"
    else:
        raise Exception("非法的关键字!", indicator)
    url = f"http://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/GetZYZB?code={symbol}"
    r = requests.get(url)
    temp_df = pd.DataFrame.from_records(eval(r.text)["data"][key])
    temp_df.columns = temp_df.loc[0]
    temp_df = temp_df.drop(0, axis=0)
    temp_df["周期"] = pd.to_datetime(temp_df["每股指标"], format="%y-%m-%d").dt.date
    temp_df = temp_df.drop("每股指标", axis=1)
    temp_df = temp_df[
        [
            "周期",
            "基本每股收益(元)",
            "稀释每股收益(元)",
            "TTM每股收益(元)",
            "每股净资产(元)",
            "每股经营现金流(元)",
            "每股营业收入(元)",
            "成长能力指标",
            "营业总收入(元)",
            "毛利润",
            "归母净利润",
            "营业总收入同比增长(%)",
            "毛利润同比增长(%)",
            "归母净利润同比增长(%)",
            "营业总收入滚动环比增长(%)",
            "毛利润滚动环比增长(%)",
            "归母净利润滚动环比增长(%)",
            "盈利能力指标",
            "平均净资产收益率(%)",
            "年化净资产收益率(%)",
            "总资产净利率(%)",
            "毛利率(%)",
            "净利率(%)",
            "年化投资回报率(%)",
            "盈利质量指标",
            "所得税/利润总额(%)",
            "经营现金流/营业收入(%)",
            "财务风险指标",
            "资产负债率(%)",
            "流动负债/总负债(%)",
            "流动比率",
        ]
    ]
    temp_df.reset_index(drop=True, inplace=True)
    temp_df.columns.name = None
    temp_df['周期'] = pd.to_datetime(temp_df['周期']).dt.date
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
        stock="00700", symbol="资产负债表", indicator="年度"
    )
    print(stock_financial_hk_report_em_df)

    stock_financial_hk_report_em_df = stock_financial_hk_report_em(
        stock="00700", symbol="资产负债表", indicator="报告期"
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
