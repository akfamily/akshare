#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/3/30 15:59
Desc: REITs 行情及信息
https://quote.eastmoney.com/center/gridlist.html#fund_reits_all
https://www.jisilu.cn/data/cnreits/#CnReits
"""
import pandas as pd
import requests


def reits_realtime_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-REITs-沪深 REITs
    https://quote.eastmoney.com/center/gridlist.html#fund_reits_all
    :return: 沪深 REITs-实时行情
    :rtype: pandas.DataFrame
    """
    url = "http://95.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "20",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:1 t:9 e:97,m:0 t:10 e:97",
        "fields": "f2,f3,f4,f5,f6,f12,f14,f15,f16,f17,f18",
        "_": "1630048369992",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.rename(
        columns={
            "index": "序号",
            "f2": "最新价",
            "f3": "涨跌幅",
            "f4": "涨跌额",
            "f5": "成交量",
            "f6": "成交额",
            "f12": "代码",
            "f14": "名称",
            "f15": "最高价",
            "f16": "最低价",
            "f17": "开盘价",
            "f18": "昨收",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "成交量",
            "成交额",
            "开盘价",
            "最高价",
            "最低价",
            "昨收",
        ]
    ]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors="coerce")
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors="coerce")
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors="coerce")
    temp_df['开盘价'] = pd.to_numeric(temp_df['开盘价'], errors="coerce")
    temp_df['最高价'] = pd.to_numeric(temp_df['最高价'], errors="coerce")
    temp_df['最低价'] = pd.to_numeric(temp_df['最低价'], errors="coerce")
    temp_df['昨收'] = pd.to_numeric(temp_df['昨收'], errors="coerce")
    return temp_df


if __name__ == "__main__":
    reits_realtime_em_df = reits_realtime_em()
    print(reits_realtime_em_df)
