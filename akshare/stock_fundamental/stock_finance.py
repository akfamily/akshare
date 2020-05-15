# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/15 15:35
Desc: 股票基本面数据
新浪财经-财务报表-财务摘要
https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/600004.phtml
新浪财经-财务分析-财务指标
https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/600004/displaytype/4.phtml
新浪财经-发行与分配
http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/600004.phtml
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


def stock_history_dividend() -> pd.DataFrame:
    """
    新浪财经-发行与分配-历史分红
    http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml?p=1&num=5000
    :return: 所有股票的历史分红数据
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml"
    params = {
        "p": "1",
        "num": "5000"
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    temp_df["代码"] = temp_df["代码"].astype(str)
    temp_df["代码"] = temp_df["代码"].str.zfill(6)
    return temp_df


def stock_history_dividend_detail(indicator: str = "分红", stock: str = "000541", date: str = "1994-12-24") -> pd.DataFrame:
    """
    新浪财经-发行与分配-分红配股详情
    https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/300670.phtml
    :param indicator: choice of {"分红", "配股"}
    :type indicator: str
    :param stock: 股票代码
    :type stock: str
    :param date: 分红配股的具体日期, e.g., "1994-12-24"
    :type date: str
    :return: 指定 indicator, stock, date 的数据
    :rtype: pandas.DataFrame
    """
    if indicator == "分红":
        url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/{stock}.phtml"
        r = requests.get(url)
        temp_df = pd.read_html(r.text)[12]
        temp_df.columns = [item[2] for item in temp_df.columns.tolist()]
        if date:
            url = "https://vip.stock.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php"
            params = {
                "stockid": stock,
                "type": "1",
                "end_date": date,
            }
            r = requests.get(url, params=params)
            temp_df = pd.read_html(r.text)[12]
            temp_df.columns = ["item", "value"]
            return temp_df
        else:
            return temp_df
    else:
        url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/{stock}.phtml"
        r = requests.get(url)
        temp_df = pd.read_html(r.text)[13]
        temp_df.columns = [item[1] for item in temp_df.columns.tolist()]
        if date:
            url = "https://vip.stock.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php"
            params = {
                "stockid": stock,
                "type": "2",
                "end_date": date,
            }
            r = requests.get(url, params=params)
            temp_df = pd.read_html(r.text)[12]
            temp_df.columns = ["item", "value"]
            return temp_df
        else:
            return temp_df


def stock_ipo_info(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-发行与分配-新股发行
    https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_NewStock/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 返回新股发行详情
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_NewStock/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[12]
    temp_df.columns = ["item", "value"]
    return temp_df


def stock_add_stock(stock: str = "688166") -> pd.DataFrame:
    """
    新浪财经-发行与分配-增发
    https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 返回增发详情
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[12]
    if temp_df.at[0, 0] == '对不起，暂时没有相关增发记录':
        return f"股票 {stock} 无增发记录"
    big_df = pd.DataFrame()
    for i in range(int(len(temp_df.at[0, 1]) / 10)):
        temp_df = pd.read_html(r.text)[13+i].iloc[:, 1]
        big_df[temp_df.name.split(" ")[1].split("：")[1][:10]] = temp_df
    big_df = big_df.T
    big_df.columns = ["发行方式", "发行价格", "实际公司募集资金总额", "发行费用总额", "实际发行数量"]
    return big_df


if __name__ == '__main__':
    stock_financial_abstract_df = stock_financial_abstract(stock="600004")
    print(stock_financial_abstract_df)
    stock_financial_analysis_indicator_df = stock_financial_analysis_indicator(stock="600004")
    print(stock_financial_analysis_indicator_df)

    stock_history_dividend_df = stock_history_dividend()
    print(stock_history_dividend_df)
    stock_history_dividend_detail_df = stock_history_dividend_detail(indicator="分红", stock="600012", date="")
    print(stock_history_dividend_detail_df)

    stock_history_dividend_detail_df = stock_history_dividend_detail(indicator="分红", stock="600012", date="2019-07-08")
    print(stock_history_dividend_detail_df)

    stock_history_dividend_detail_df = stock_history_dividend_detail(indicator="配股", stock="000002", date="1999-12-22")
    print(stock_history_dividend_detail_df)

    stock_ipo_info_df = stock_ipo_info(stock="600004")
    print(stock_ipo_info_df)
    stock_add_stock_df = stock_add_stock(stock="600004")
    print(stock_add_stock_df)
