# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/10/16 15:00
Desc: 中证指数-所有指数-历史行情数据
http://www.csindex.com.cn/zh-CN/indices/index-detail/H30374
"""
import pandas as pd
import requests


def stock_zh_index_hist_csindex(
    symbol: str = "H30374", start_date: str = "20160101", end_date: str = "20211015"
) -> pd.DataFrame:
    """
    中证指数获取某个指数的 5 年历史行情数据
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


if __name__ == "__main__":
    stock_zh_index_hist_csindex_df = stock_zh_index_hist_csindex(
        symbol="H30374", start_date="20100101", end_date="20211015"
    )
    print(stock_zh_index_hist_csindex_df)
