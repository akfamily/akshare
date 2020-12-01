# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/1 10:59
Desc: 国证指数
http://www.cnindex.com.cn/index.html
"""
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


if __name__ == "__main__":
    index_cni_all_df = index_cni_all()
    print(index_cni_all_df)
    index_cni_hist_df = index_cni_hist(index="399005")
    print(index_cni_hist_df)
