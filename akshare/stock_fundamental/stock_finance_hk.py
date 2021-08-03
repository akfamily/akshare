# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/8/3 10:15
Desc: 香港股票基本面数据
新浪财经-财务分析-财务指标
http://stock.finance.sina.com.cn/hkstock/finance/00700.html#a1
"""
from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def stock_financial_hk_report_eastmoney(
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
        raise Exception("非法的关键字!", indicator)

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
    temp_df.index = pd.to_datetime(temp_df.loc[:, "截止日期"].values, format="%y-%m-%d")
    temp_df = temp_df.drop("截止日期", axis=1)
    temp_df
    return temp_df


def stock_financial_hk_analysis_indicator(
    stock: str = "00700", indicator: str = "年度"
) -> pd.DataFrame:
    """
    东方财富-港股-财务分析-主要指标
    https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/600004/ctrl/2019/displaytype/4.phtml
    :param stock: 股票代码
    :type stock: str    
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

    url = f"http://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/GetZYZB?code={stock}&color=b"
    r = requests.get(url)
    temp_df = pd.DataFrame.from_records(eval(r.text)["data"][key])
    temp_df.columns = temp_df.loc[0]
    temp_df = temp_df.drop(0, axis=0)
    temp_df.index = pd.to_datetime(temp_df.loc[:, "每股指标"].values, format="%y-%m-%d")
    temp_df = temp_df.drop("每股指标", axis=1)
    return temp_df


if __name__ == "__main__":
    stock_financial_analysis_indicator_df = stock_financial_hk_analysis_indicator(
        stock="00700", indicator="年度"
    )
    print(stock_financial_analysis_indicator_df)

    stock_financial_analysis_indicator_df = stock_financial_hk_analysis_indicator(
        stock="00700", indicator="报告期"
    )
    print(stock_financial_analysis_indicator_df)

    stock_financial_report_eastmoney_df = stock_financial_hk_report_eastmoney(
        stock="00700", symbol="资产负债表", indicator="年度"
    )
    print(stock_financial_report_eastmoney_df)

    stock_financial_report_eastmoney_df = stock_financial_hk_report_eastmoney(
        stock="00700", symbol="资产负债表", indicator="报告期"
    )
    print(stock_financial_report_eastmoney_df)

    stock_financial_report_eastmoney_df = stock_financial_hk_report_eastmoney(
        stock="00700", symbol="利润表", indicator="年度"
    )
    print(stock_financial_report_eastmoney_df)

    stock_financial_report_eastmoney_df = stock_financial_hk_report_eastmoney(
        stock="00700", symbol="利润表", indicator="报告期"
    )
    print(stock_financial_report_eastmoney_df)

    stock_financial_report_eastmoney_df = stock_financial_hk_report_eastmoney(
        stock="00700", symbol="现金流量表", indicator="年度"
    )
    print(stock_financial_report_eastmoney_df)

    stock_financial_report_eastmoney_df = stock_financial_hk_report_eastmoney(
        stock="00700", symbol="现金流量表", indicator="报告期"
    )
    print(stock_financial_report_eastmoney_df)
