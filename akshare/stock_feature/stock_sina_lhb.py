# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/30 22:17
Desc: 新浪财经-龙虎榜
http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhb/index.phtml
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def stock_sina_lhb_detail_daily(trade_date: str = "20200729", symbol: str = "涨幅偏离值达7%的证券") -> pd.DataFrame:
    """
    龙虎榜-每日详情
    http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhb/index.phtml
    :param trade_date: 交易日, e.g., trade_date="20200729"
    :type trade_date: str
    :param symbol: 指定标题
    :type symbol: str
    :return: 龙虎榜-每日详情
    :rtype: pandas.DataFrame
    """
    trade_date = "-".join([trade_date[:4], trade_date[4:6], trade_date[6:]])
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhb/index.phtml"
    params = {
        "tradedate": trade_date
    }
    r = requests.get(url, params=params)
    if symbol == "涨幅偏离值达7%的证券":
        temp_df = pd.read_html(r.text, header=1)[0].iloc[0:, :]
    elif symbol == "跌幅偏离值达7%的证券":
        temp_df = pd.read_html(r.text, header=1)[1].iloc[0:, :]
    elif symbol == "振幅值达15%的证券":
        temp_df = pd.read_html(r.text, header=1)[2].iloc[0:, :]
    elif symbol == "换手率达20%的证券":
        temp_df = pd.read_html(r.text, header=1)[3].iloc[0:, :]
    elif symbol == "连续三个交易日内，涨幅偏离值累计达20%的证券":
        temp_df = pd.read_html(r.text, header=1)[4].iloc[0:, :]
    elif symbol == "退市整理的证券":
        temp_df = pd.read_html(r.text, header=1)[5].iloc[0:, :]
    elif symbol == "连续三个交易日内，日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20%的股票":
        temp_df = pd.read_html(r.text, header=1)[6].iloc[0:, :]
    elif symbol == "连续三个交易日内，跌幅偏离值累计达到12%的ST证券":
        temp_df = pd.read_html(r.text, header=1)[7].iloc[0:, :]
    elif symbol == "*ST证券":
        temp_df = pd.read_html(r.text, header=1)[8].iloc[0:, :]
    elif symbol == "未完成股改证券":
        temp_df = pd.read_html(r.text, header=1)[9].iloc[0:, :]
    temp_df["股票代码"] = temp_df["股票代码"].astype(str).str.zfill(6)
    del temp_df["查看详情"]
    temp_df.columns = ["序号", "股票代码", "股票名称", "收盘价", "对应值", "成交量", "成交额"]
    return temp_df


def stock_sina_lhb_ggtj(recent_day: str = "5") -> pd.DataFrame:
    """
    龙虎榜-个股上榜统计
    http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml
    :param recent_day: choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;}
    :type recent_day: str
    :return: 龙虎榜-每日详情
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml"
    params = {
        "last": recent_day,
        "p": "1",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    last_page_num = int(soup.find_all(attrs={"class": "page"})[-2].text)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, last_page_num+1)):
        params = {
            "last": "5",
            "p": page,
        }
        r = requests.get(url, params=params)
        temp_df = pd.read_html(r.text)[0].iloc[0:, :]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df["股票代码"] = big_df["股票代码"].astype(str).str.zfill(6)
    big_df.columns = ["股票代码", "股票名称", "上榜次数", "累积购买额", "累积卖出额", "净额", "买入席位数", "卖出席位数"]
    return big_df


def stock_sina_lhb_yytj(recent_day: str = "5") -> pd.DataFrame:
    """
    龙虎榜-营业部上榜统计
    http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/yytj/index.phtml
    :param recent_day: choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;}
    :type recent_day: str
    :return: 龙虎榜-营业部上榜统计
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/yytj/index.phtml"
    params = {
        "last": recent_day,
        "p": "1",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    last_page_num = int(soup.find_all(attrs={"class": "page"})[-2].text)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, last_page_num+1)):
        params = {
            "last": "5",
            "p": page,
        }
        r = requests.get(url, params=params)
        temp_df = pd.read_html(r.text)[0].iloc[0:, :]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ['营业部名称', '上榜次数', '累积购买额', '买入席位数', '累积卖出额', '卖出席位数', '买入前三股票']
    return big_df


def stock_sina_lhb_jgzz(recent_day: str = "5") -> pd.DataFrame:
    """
    龙虎榜-机构席位追踪
    http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml
    :param recent_day: choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;}
    :type recent_day: str
    :return: 龙虎榜-机构席位追踪
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml"
    params = {
        "last": recent_day,
        "p": "1",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    last_page_num = int(soup.find_all(attrs={"class": "page"})[-2].text)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, last_page_num+1)):
        params = {
            "last": "5",
            "p": page,
        }
        r = requests.get(url, params=params)
        temp_df = pd.read_html(r.text)[0].iloc[0:, :]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df["股票代码"] = big_df["股票代码"].astype(str).str.zfill(6)
    del big_df["当前价"]
    del big_df["涨跌幅"]
    big_df.columns = ['股票代码', '股票名称', '累积买入额', '买入次数', '累积卖出额', '卖出次数', '净额']
    return big_df


def stock_sina_lhb_jgmx() -> pd.DataFrame:
    """
    龙虎榜-机构席位成交明细
    http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgzz/index.phtml
    :return: 龙虎榜-机构席位成交明细
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgmx/index.phtml"
    params = {
        "p": "1",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    last_page_num = int(soup.find_all(attrs={"class": "page"})[-2].text)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, last_page_num+1)):
        params = {
            "p": page,
        }
        r = requests.get(url, params=params)
        temp_df = pd.read_html(r.text)[0].iloc[0:, :]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df["股票代码"] = big_df["股票代码"].astype(str).str.zfill(6)
    return big_df


if __name__ == '__main__':
    stock_sina_lhb_detail_daily_df = stock_sina_lhb_detail_daily(trade_date="20200729", symbol="涨幅偏离值达7%的证券")
    print(stock_sina_lhb_detail_daily_df)

    stock_sina_lhb_ggtj_df = stock_sina_lhb_ggtj(recent_day="5")
    print(stock_sina_lhb_ggtj_df)

    stock_sina_lhb_yytj_df = stock_sina_lhb_yytj(recent_day="5")
    print(stock_sina_lhb_yytj_df)

    stock_sina_lhb_jgzz_df = stock_sina_lhb_jgzz(recent_day="5")
    print(stock_sina_lhb_jgzz_df)

    stock_sina_lhb_jgmx_df = stock_sina_lhb_jgmx()
    print(stock_sina_lhb_jgmx_df)
