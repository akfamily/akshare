# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/14 15:35
Desc: 新浪财经-财务报表-财务摘要
https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/600004.phtml
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def stock_financial_abstract(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-财务报表-财务摘要
    https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-财务报表-财务摘要
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[13].iloc[:, :2]
    big_df = pd.DataFrame()
    for i in range(0, len(temp_df), 12):
        truncated_df = temp_df.iloc[i: i + 11, 1]
        big_df = pd.concat([big_df, truncated_df.reset_index(drop=True)], axis=1, ignore_index=True)
    data_df = big_df.T
    data_df.columns = temp_df.iloc[:11, 0].tolist()
    return data_df


def stock_financial_analysis_indicator(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-财务分析-财务指标
    https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/600004/ctrl/2019/displaytype/4.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-财务分析-财务指标
    :rtype: pandas.DataFrame
    """
    url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{stock}/ctrl/2020/displaytype/4.phtml"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    year_context = soup.find(attrs={"id": "con02-1"}).find("table").find_all("a")
    year_list = [item.text for item in year_context]
    out_df = pd.DataFrame()
    for year_item in tqdm(year_list):
        url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{stock}/ctrl/{year_item}/displaytype/4.phtml"
        r = requests.get(url)
        temp_df = pd.read_html(r.text)[12].iloc[:, :-1]
        temp_df.columns = temp_df.iloc[0, :]
        temp_df = temp_df.iloc[1:, :]
        big_df = pd.DataFrame()
        indicator_list = ["每股指标", "盈利能力", "成长能力", "营运能力", "偿债及资本结构", "现金流量", "其他指标"]
        for i in range(len(indicator_list)):
            if i == 6:
                inner_df = temp_df[temp_df.loc[temp_df.iloc[:, 0].str.find(indicator_list[i]) == 0, :].index[0]:].T
            else:
                inner_df = temp_df[temp_df.loc[temp_df.iloc[:, 0].str.find(indicator_list[i]) == 0, :].index[0]: temp_df.loc[temp_df.iloc[:, 0].str.find(indicator_list[i+1]) == 0, :].index[0]-1].T
            inner_df = inner_df.reset_index(drop=True)
            big_df = pd.concat([big_df, inner_df], axis=1)
        big_df.columns = big_df.iloc[0, :].tolist()
        big_df = big_df.iloc[1:, :]
        big_df.index = temp_df.columns.tolist()[1:]
        out_df = out_df.append(big_df)
    out_df.dropna(inplace=True)
    return out_df


if __name__ == '__main__':
    stock_financial_abstract_df = stock_financial_abstract(stock="600004")
    print(stock_financial_abstract_df)
    stock_financial_analysis_indicator_df = stock_financial_analysis_indicator(stock="600004")
    print(stock_financial_analysis_indicator_df)
