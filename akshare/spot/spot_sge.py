# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/12/7 17:00
Desc: 上海黄金交易所-数据资讯-行情走势
https://www.sge.com.cn/sjzx/mrhq
上海黄金交易所-数据资讯-上海金基准价-历史数据
上海黄金交易所-数据资讯-上海银基准价-历史数据
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def spot_symbol_table_sge() -> pd.DataFrame:
    """
    上海黄金交易所-数据资讯-行情走势-品种表
    https://www.sge.com.cn/sjzx/mrhq
    :return: 品种表
    :rtype: pandas.DataFrame
    """
    url = "https://www.sge.com.cn/sjzx/mrhq"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    value_item = soup.find(attrs={"id": "instidsle"}).find_all("option")
    symbol_list = [item.text for item in value_item]
    temp_df = pd.DataFrame(symbol_list)
    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df.index + 1
    temp_df.columns = ['序号', '品种']
    return temp_df


def spot_hist_sge(symbol: str = "Au99.99") -> pd.DataFrame:
    """
    上海黄金交易所-数据资讯-行情走势-历史数据
    https://www.sge.com.cn/sjzx/mrhq
    :param symbol: choice of {'Au99.99', 'Au99.95', 'Au100g', 'Pt99.95', 'Ag(T+D)', 'Au(T+D)', 'mAu(T+D)', 'Au(T+N1)', 'Au(T+N2)', 'Ag99.99', 'iAu99.99', 'Au99.5', 'iAu100g', 'iAu99.5', 'PGC30g', 'NYAuTN06', 'NYAuTN12'}; 可以通过 ak.spot_symbol_table_sge() 获取品种表
    :type symbol: str
    :return: 历史数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.sge.com.cn/graph/Dailyhq"
    payload = {"instid": symbol}
    r = requests.post(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["time"])
    temp_df.columns = [
        "date",
        "open",
        "close",
        "high",
        "low",
    ]
    return temp_df


def spot_golden_benchmark_sge() -> pd.DataFrame:
    """
    上海黄金交易所-数据资讯-上海金基准价-历史数据
    https://www.sge.com.cn/sjzx/jzj
    :return: 历史数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.sge.com.cn/graph/DayilyJzj"
    payload = {}
    r = requests.post(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["wp"])
    temp_df.columns = [
        "交易时间",
        "晚盘价",
    ]
    temp_df["交易时间"] = pd.to_datetime(temp_df["交易时间"], unit="ms").dt.date
    temp_zp_df = pd.DataFrame(data_json["zp"])
    temp_zp_df.columns = [
        "交易时间",
        "早盘价",
    ]
    temp_zp_df["交易时间"] = pd.to_datetime(temp_zp_df["交易时间"], unit="ms").dt.date
    temp_df["早盘价"] = temp_zp_df["早盘价"]
    return temp_df


def spot_silver_benchmark_sge() -> pd.DataFrame:
    """
    上海黄金交易所-数据资讯-上海银基准价-历史数据
    https://www.sge.com.cn/sjzx/mrhq
    :return: 历史数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.sge.com.cn/graph/DayilyShsilverJzj"
    payload = {}
    r = requests.post(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["wp"])
    temp_df.columns = [
        "交易时间",
        "晚盘价",
    ]
    temp_df["交易时间"] = pd.to_datetime(temp_df["交易时间"], unit="ms").dt.date
    temp_zp_df = pd.DataFrame(data_json["zp"])
    temp_zp_df.columns = [
        "交易时间",
        "早盘价",
    ]
    temp_zp_df["交易时间"] = pd.to_datetime(temp_zp_df["交易时间"], unit="ms").dt.date
    temp_df["早盘价"] = temp_zp_df["早盘价"]
    return temp_df


if __name__ == "__main__":
    spot_symbol_table_sge_df = spot_symbol_table_sge()
    print(spot_symbol_table_sge_df)

    spot_hist_sge_df = spot_hist_sge(symbol="Au99.99")
    print(spot_hist_sge_df)

    spot_golden_benchmark_sge_df = spot_golden_benchmark_sge()
    print(spot_golden_benchmark_sge_df)

    spot_silver_benchmark_sge_df = spot_silver_benchmark_sge()
    print(spot_silver_benchmark_sge_df)

    for spot in spot_symbol_table_sge_df['品种'].tolist():
        spot_hist_sge_df = spot_hist_sge(symbol=spot)
        print(spot_hist_sge_df)
