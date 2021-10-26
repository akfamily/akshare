#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/6/16 15:18
Desc: 国证指数
http://www.cnindex.com.cn/index.html
"""
import zipfile

import pandas as pd
import requests


def index_cni_all() -> pd.DataFrame:
    """
    国证指数-所有指数
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
    return temp_df


def index_cni_hist(index: str = "399001") -> pd.DataFrame:
    """
    指数历史行情数据
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param index: 指数代码
    :type index: str
    :return: 指数历史行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://hq.cnindex.com.cn/market/market/getIndexDailyDataWithDataFormat"
    params = {
        "indexCode": index,
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


def index_cni_detail(index: str = '399005', date: str = '2020-11') -> pd.DataFrame:
    """
    国证指数-样本详情-指定日期的样本成份
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param index: 指数代码
    :type index: str
    :param date: 指定月份
    :type date: str
    :return: 指定日期的样本成份
    :rtype: pandas.DataFrame
    """
    url = 'http://www.cnindex.com.cn/sample-detail/download'
    params = {
        'indexcode': index,
        'dateStr': date
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
    return temp_df


def index_cni_detail_hist(index: str = '399005') -> pd.DataFrame:
    """
    国证指数-样本详情-历史样本
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param index: 指数代码
    :type index: str
    :return: 历史样本
    :rtype: pandas.DataFrame
    """
    url = 'http://www.cnindex.com.cn/sample-detail/download-history'
    params = {
        'indexcode': index
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
    return temp_df


def index_cni_detail_hist_adjust(index: str = '399231') -> pd.DataFrame:
    """
    国证指数-样本详情-历史调样
    http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
    :param index: 指数代码
    :type index: str
    :return: 历史调样
    :rtype: pandas.DataFrame
    """
    url = 'http://www.cnindex.com.cn/sample-detail/download-adjustment'
    params = {
        'indexcode': index
    }
    r = requests.get(url, params=params)
    try:
        temp_df = pd.read_excel(r.content, engine="openpyxl")
    except zipfile.BadZipFile as e:
        return
    temp_df['样本代码'] = temp_df['样本代码'].astype(str).str.zfill(6)
    return temp_df


if __name__ == "__main__":
    index_cni_all_df = index_cni_all()
    print(index_cni_all_df)

    index_cni_hist_df = index_cni_hist(index="399005")
    print(index_cni_hist_df)

    index_cni_detail_df = index_cni_detail(index='399005', date='2020-11')
    print(index_cni_detail_df)

    index_cni_detail_hist_df = index_cni_detail_hist(index='399005')
    print(index_cni_detail_hist_df)

    index_cni_detail_hist_adjust_df = index_cni_detail_hist_adjust(index='399005')
    print(index_cni_detail_hist_adjust_df)
