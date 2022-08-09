#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/3/5 23:50
Desc: 国证指数
http://www.cnindex.com.cn/index.html
"""
import zipfile

import pandas as pd
import requests


def index_all_cni() -> pd.DataFrame:
    """
    国证指数-最近交易日的所有指数
    http://www.cnindex.com.cn/zh_indices/sese/index.html?act_menu=1&index_type=-1
    :return: 国证指数-所有指数
    :rtype: pandas.DataFrame
    """
    url = "http://www.cnindex.com.cn/index/indexList"
    params = {
        "channelCode": "-1",
        "rows": "2000",
        "pageNum": "1",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["rows"])
    temp_df.columns = [
        "_",
        "_",
        "指数代码",
        "_",
        "_",
        "_",
        "_",
        "_",
        "指数简称",
        "_",
        "_",
        "_",
        "样本数",
        "收盘点位",
        "涨跌幅",
        "_",
        "PE滚动",
        "_",
        "成交量",
        "成交额",
        "总市值",
        "自由流通市值",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "指数代码",
            "指数简称",
            "样本数",
            "收盘点位",
            "涨跌幅",
            "PE滚动",
            "成交量",
            "成交额",
            "总市值",
            "自由流通市值",
        ]
    ]
    temp_df['成交量'] = temp_df['成交量'] / 100000
    temp_df['成交额'] = temp_df['成交额'] / 100000000
    temp_df['总市值'] = temp_df['总市值'] / 100000000
    temp_df['自由流通市值'] = temp_df['自由流通市值'] / 100000000
    return temp_df


def index_hist_cni(symbol: str = "399001") -> pd.DataFrame:
    """
    指数历史行情数据
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param symbol: 指数代码
    :type symbol: str
    :return: 指数历史行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://hq.cnindex.com.cn/market/market/getIndexDailyDataWithDataFormat"
    params = {
        "indexCode": symbol,
        "startDate": "",
        "endDate": "",
        "frequency": "day",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["data"])
    temp_df.columns = [
        "日期",
        "_",
        "最高价",
        "开盘价",
        "最低价",
        "收盘价",
        "_",
        "涨跌幅",
        "成交额",
        "成交量",
        "_",
    ]
    temp_df = temp_df[
        [
            "日期",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "涨跌幅",
            "成交量",
            "成交额",
        ]
    ]
    temp_df["涨跌幅"] = temp_df["涨跌幅"].str.replace("%", "")
    temp_df["涨跌幅"] = temp_df["涨跌幅"].astype("float")
    temp_df["涨跌幅"] = temp_df["涨跌幅"] / 100
    return temp_df


def index_detail_cni(symbol: str = '399005', date: str = '202011') -> pd.DataFrame:
    """
    国证指数-样本详情-指定日期的样本成份
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param symbol: 指数代码
    :type symbol: str
    :param date: 指定月份
    :type date: str
    :return: 指定日期的样本成份
    :rtype: pandas.DataFrame
    """
    url = 'http://www.cnindex.com.cn/sample-detail/download'
    params = {
        'indexcode': symbol,
        'dateStr': '-'.join([date[:4], date[4:]])
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(r.content)
    temp_df['样本代码'] = temp_df['样本代码'].astype(str).str.zfill(6)
    temp_df.columns = [
        '日期',
        '样本代码',
        '样本简称',
        '所属行业',
        '自由流通市值',
        '总市值',
        '权重',
    ]
    temp_df['自由流通市值'] = pd.to_numeric(temp_df['自由流通市值'])
    temp_df['总市值'] = pd.to_numeric(temp_df['总市值'])
    temp_df['权重'] = pd.to_numeric(temp_df['权重'])
    return temp_df


def index_detail_hist_cni(symbol: str = '399001', date: str = "") -> pd.DataFrame:
    """
    国证指数-样本详情-历史样本
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param date: 指数代码
    :type date: str
    :param symbol: 指数代码
    :type symbol: str
    :return: 历史样本
    :rtype: pandas.DataFrame
    """
    if date:
        url = 'http://www.cnindex.com.cn/sample-detail/detail'
        params = {
            'indexcode': symbol,
            'dateStr': '-'.join([date[:4], date[4:]]),
            'pageNum': '1',
            'rows': '50000',
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['data']['rows'])
        temp_df.columns = [
            '-',
            '-',
            '日期',
            '样本代码',
            '样本简称',
            '所属行业',
            '-',
            '自由流通市值',
            '总市值',
            '权重',
            '-',
        ]
        temp_df = temp_df[[
            '日期',
            '样本代码',
            '样本简称',
            '所属行业',
            '自由流通市值',
            '总市值',
            '权重',
        ]]
    else:
        url = 'http://www.cnindex.com.cn/sample-detail/download-history'
        params = {
            'indexcode': symbol
        }
        r = requests.get(url, params=params)
        temp_df = pd.read_excel(r.content)
    temp_df['样本代码'] = temp_df['样本代码'].astype(str).str.zfill(6)
    temp_df.columns = [
        '日期',
        '样本代码',
        '样本简称',
        '所属行业',
        '自由流通市值',
        '总市值',
        '权重',
    ]
    temp_df['自由流通市值'] = pd.to_numeric(temp_df['自由流通市值'])
    temp_df['总市值'] = pd.to_numeric(temp_df['总市值'])
    temp_df['权重'] = pd.to_numeric(temp_df['权重'])
    return temp_df


def index_detail_hist_adjust_cni(symbol: str = '399005') -> pd.DataFrame:
    """
    国证指数-样本详情-历史调样
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399005
    :param symbol: 指数代码
    :type symbol: str
    :return: 历史调样
    :rtype: pandas.DataFrame
    """
    url = 'http://www.cnindex.com.cn/sample-detail/download-adjustment'
    params = {
        'indexcode': symbol
    }
    r = requests.get(url, params=params)
    try:
        temp_df = pd.read_excel(r.content, engine="openpyxl")
    except zipfile.BadZipFile as e:
        return pd.DataFrame()
    temp_df['样本代码'] = temp_df['样本代码'].astype(str).str.zfill(6)
    return temp_df


if __name__ == "__main__":
    index_all_cni_df = index_all_cni()
    print(index_all_cni_df)

    index_hist_cni_df = index_hist_cni(symbol="399303")
    print(index_hist_cni_df)

    index_detail_cni_df = index_detail_cni(symbol='399303', date='202011')
    print(index_detail_cni_df)

    index_detail_hist_cni_df = index_detail_hist_cni(symbol='399303', date='202201')
    print(index_detail_hist_cni_df)

    index_detail_hist_adjust_cni_df = index_detail_hist_adjust_cni(symbol='399005')
    print(index_detail_hist_adjust_cni_df)
