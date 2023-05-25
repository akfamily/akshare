# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/05/25 14:05
Desc: 中证指数-所有指数-历史行情数据
https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/list?index_series=1
"""
from functools import lru_cache

import pandas as pd
import requests


def stock_zh_index_hist_csindex(
    symbol: str = "H30374",
    start_date: str = "20160101",
    end_date: str = "20211015",
) -> pd.DataFrame:
    """
    中证指数-具体指数-历史行情数据
    P.S. 只有收盘价，正常情况下不应使用该接口，除非指数只有中证网站有
    https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/detail?indexCode=H30374
    :param symbol: 指数代码; e.g., H30374
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 包含日期和收盘价的指数数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.csindex.com.cn/csindex-home/perf/index-perf"
    params = {
        "indexCode": symbol,
        "startDate": start_date,
        "endDate": end_date,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    del temp_df["peg"]
    temp_df.columns = [
        "日期",
        "指数代码",
        "指数中文全称",
        "指数中文简称",
        "指数英文全称",
        "指数英文简称",
        "开盘",
        "最高",
        "最低",
        "收盘",
        "涨跌",
        "涨跌幅",
        "成交量",
        "成交金额",
        "样本数量",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
    temp_df["最高"] = pd.to_numeric(temp_df["最高"])
    temp_df["最低"] = pd.to_numeric(temp_df["最低"])
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    temp_df["成交金额"] = pd.to_numeric(temp_df["成交金额"])
    temp_df["样本数量"] = pd.to_numeric(temp_df["样本数量"])
    return temp_df


def stock_zh_index_value_csindex(symbol: str = "H30374") -> pd.DataFrame:
    """
    中证指数-指数估值数据
    https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/detail?indexCode=H30374
    :param symbol: 指数代码; e.g., H30374
    :type symbol: str
    :return: 指数估值数据
    :rtype: pandas.DataFrame
    """
    url = f"https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/indicator/{symbol}indicator.xls"
    temp_df = pd.read_excel(url)
    temp_df.columns = [
        "日期",
        "指数代码",
        "指数中文全称",
        "指数中文简称",
        "指数英文全称",
        "指数英文简称",
        "市盈率1",
        "市盈率2",
        "股息率1",
        "股息率2",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], format="%Y%m%d").dt.date
    temp_df["市盈率1"] = pd.to_numeric(temp_df["市盈率1"])
    temp_df["市盈率2"] = pd.to_numeric(temp_df["市盈率2"])
    temp_df["股息率1"] = pd.to_numeric(temp_df["股息率1"])
    temp_df["股息率2"] = pd.to_numeric(temp_df["股息率2"])
    return temp_df


@lru_cache()
def index_value_name_funddb() -> pd.DataFrame:
    """
    funddb-指数估值-指数代码
    https://funddb.cn/site/index
    :return: pandas.DataFrame
    :rtype: 指数代码
    """
    url = "https://api.jiucaishuo.com/v2/guzhi/showcategory"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["right_list"])
    temp_df.columns = [
        "指数开始时间",
        "-",
        "指数名称",
        "指数代码",
        "最新PE",
        "最新PB",
        "PE分位",
        "PB分位",
        "股息率",
        "-",
        "-",
        "-",
        "更新时间",
        "股息率分位",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "指数名称",
            "最新PE",
            "PE分位",
            "最新PB",
            "PB分位",
            "股息率",
            "股息率分位",
            "指数代码",
            "指数开始时间",
            "更新时间",
        ]
    ]
    temp_df["指数开始时间"] = pd.to_datetime(temp_df["指数开始时间"]).dt.date
    temp_df["最新PE"] = pd.to_numeric(temp_df["最新PE"], errors="coerce")
    temp_df["PE分位"] = pd.to_numeric(temp_df["PE分位"], errors="coerce")
    temp_df["最新PB"] = pd.to_numeric(temp_df["最新PB"], errors="coerce")
    temp_df["PB分位"] = pd.to_numeric(temp_df["PB分位"], errors="coerce")
    temp_df["股息率"] = pd.to_numeric(temp_df["股息率"], errors="coerce")
    temp_df["股息率分位"] = pd.to_numeric(temp_df["股息率分位"], errors="coerce")
    return temp_df


def index_value_hist_funddb(
    symbol: str = "大盘成长", indicator: str = "市盈率"
) -> pd.DataFrame:
    """
    funddb-指数估值-估值信息
    https://funddb.cn/site/index
    :param symbol: 指数名称; 通过调用 ak.index_value_name_funddb() 来获取
    :type symbol: str
    :param indicator: choice of {'市盈率', '市净率', '股息率'}
    :type indicator: str
    :return: 估值信息
    :rtype: pandas.DataFrame
    """
    indicator_map = {
        "市盈率": "pe",
        "市净率": "pb",
        "股息率": "xilv",
        "风险溢价": "fed",
    }
    index_value_name_funddb_df = index_value_name_funddb()
    name_code_map = dict(
        zip(
            index_value_name_funddb_df["指数名称"],
            index_value_name_funddb_df["指数代码"],
        )
    )
    url = "https://api.jiucaishuo.com/v2/guzhi/newtubiaolinedata"
    payload = {
        "gu_code": name_code_map[symbol],
        "pe_category": indicator_map[indicator],
        "year": -1,
    }
    r = requests.post(url, json=payload)
    data_json = r.json()
    big_df = pd.DataFrame()
    temp_df = pd.DataFrame(
        data_json["data"]["tubiao"]["series"][0]["data"],
        columns=["timestamp", "value"],
    )
    big_df["日期"] = (
        pd.to_datetime(temp_df["timestamp"], unit="ms", utc=True)
        .dt.tz_convert("Asia/Shanghai")
        .dt.date
    )
    big_df["平均值"] = pd.to_numeric(temp_df["value"])
    big_df[indicator] = pd.to_numeric(
        [item[1] for item in data_json["data"]["tubiao"]["series"][1]["data"]]
    )
    big_df["最低30"] = pd.to_numeric(
        [item[1] for item in data_json["data"]["tubiao"]["series"][2]["data"]]
    )
    big_df["最低10"] = pd.to_numeric(
        [item[1] for item in data_json["data"]["tubiao"]["series"][3]["data"]]
    )
    big_df["最高30"] = pd.to_numeric(
        [item[1] for item in data_json["data"]["tubiao"]["series"][4]["data"]]
    )
    big_df["最高10"] = pd.to_numeric(
        [item[1] for item in data_json["data"]["tubiao"]["series"][5]["data"]]
    )
    return big_df


def get_csindex_pettm(symbol="000928", startDate="20041231", endDate="2100") -> pd.DataFrame:
    """
    中证指数 - 滚动市盈率
    https://www.csindex.com.cn/
    :param symbol: 指数名称;
    :type symbol: str
    :param startDate: 开始日期;
    :type startDate: str
    :param endDate: 结束日期;
    :type endDate: str
    :return: 滚动市盈率
    :rtype: pandas.DataFrame
    """
    params = {
        "indexCode":symbol,
        "startDate":startDate,
        "endDate":endDate
    }
    url = "https://www.csindex.com.cn/csindex-home/perf/indexCsiDsPe"
    rs = requests.get(url=url, params=params)
    if rs.status_code == 200:
        rs =  pd.DataFrame(rs.json()["data"])
        rs.rename(columns={
            "tradeDate":"交易日",
            "indexName":"指数中文简称",
            "indexNameEn":"指数英文简称",
            "peg":"滚动市盈率",
        },
        inplace=True)
        rs["交易日"] = pd.to_datetime(rs["交易日"]).dt.date
        rs["滚动市盈率"] = pd.to_numeric(rs["滚动市盈率"])
        return rs
    return pd.DataFrame()

def get_csindex(symbol:str ="000928", startDate:str ="20041231", endDate:str ="2100") -> pd.DataFrame:
    """
    中证指数 - 指数历史行情和估值
    https://www.csindex.com.cn/
    :param symbol: 指数名称;
    :type symbol: str
    :param startDate: 开始日期;
    :type startDate: str
    :param endDate: 结束日期;
    :type endDate: str
    :return: 滚动市盈率
    :rtype: pandas.DataFrame
    """
    params = {
        "indexCode":symbol,
        "startDate":startDate,
        "endDate":endDate
    }
    url = "https://www.csindex.com.cn/csindex-home/perf/index-perf"
    rs = requests.get(url=url, params=params)
    if rs.status_code == 200:
        rs = pd.DataFrame(rs.json()["data"])
        rs.rename(columns={
            "tradeDate":"交易日",
            "indexCode":"指数代码",
            "indexNameCnAll":"指数中文名称",
            "indexNameCn":"指数中文简称",
            "indexNameEnAll":"指数英文名称",
            "indexNameEn":"指数英文简称",
            "open":"开盘价",
            "high":"最高价",
            "low":"最低价",
            "close":"收盘价",
            "change":"涨跌",
            "changePct":"涨跌幅",
            "tradingValue":"交易量(万手)",
            "consNumber":"交易额(亿元)",
            "peg":"滚动市盈率",
        },
        inplace=True)
        rs["交易日"] = pd.to_datetime(rs["交易日"]).dt.date
        rs["开盘价"] = pd.to_numeric(rs["开盘价"])
        rs["最高价"] = pd.to_numeric(rs["最高价"])
        rs["最低价"] = pd.to_numeric(rs["最低价"])
        rs["收盘价"] = pd.to_numeric(rs["收盘价"])
        rs["涨跌"] = pd.to_numeric(rs["涨跌"])
        rs["涨跌"] = pd.to_numeric(rs["涨跌"])
        rs["涨跌"] = pd.to_numeric(rs["涨跌"])
        rs["涨跌幅"] = pd.to_numeric(rs["涨跌幅"])
        rs["交易量(万手)"] = pd.to_numeric(rs["交易量(万手)"])
        rs["交易额(亿元)"] = pd.to_numeric(rs["交易额(亿元)"])
        rs["滚动市盈率"] = pd.to_numeric(rs["滚动市盈率"])
        return rs
    return pd.DataFrame()

if __name__ == "__main__":
    stock_zh_index_hist_csindex_df = stock_zh_index_hist_csindex(
        symbol="000832", start_date="20221122", end_date="20221123"
    )
    print(stock_zh_index_hist_csindex_df)

    stock_zh_index_value_csindex_df = stock_zh_index_value_csindex(symbol="H30374")
    print(stock_zh_index_value_csindex_df)

    index_value_hist_funddb_df = index_value_hist_funddb(symbol="大盘成长", indicator="风险溢价")
    print(index_value_hist_funddb_df)

    index_value_name_funddb_df = index_value_name_funddb()
    print(index_value_name_funddb_df)

    pettm = get_csindex_pettm()
    print(pettm)
    csindex = get_csindex()
    print(csindex)
