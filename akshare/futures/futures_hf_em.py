#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/11/28 22:00
Desc: 东方财富网-行情中心-期货市场-国际期货
https://quote.eastmoney.com/center/gridlist.html#futures_global
"""

import math

import pandas as pd
import requests

from akshare.utils.tqdm import get_tqdm


def futures_global_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-期货市场-国际期货
    https://quote.eastmoney.com/center/gridlist.html#futures_global
    :return: 行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://futsseapi.eastmoney.com/list/COMEX,NYMEX,COBOT,SGX,NYBOT,LME,MDEX,TOCOM,IPE"
    params = {
        "orderBy": "zdf",
        "sort": "desc",
        "pageSize": "20",
        "pageIndex": "0",
        "token": "58b2fa8f54638b60b87d69b31969089c",
        "field": "dm,sc,name,p,zsjd,zde,zdf,f152,o,h,l,zjsj,vol,wp,np,ccl",
        "blockName": "callback",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_num = data_json["total"]
    total_page = math.ceil(total_num / 20) - 1
    tqdm = get_tqdm()
    big_df = pd.DataFrame()
    for page in tqdm(range(total_page), leave=False):
        params.update({"pageIndex": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["list"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df["index"] + 1
    big_df.rename(
        columns={
            "index": "序号",
            "np": "卖盘",
            "h": "最高",
            "dm": "代码",
            "zsjd": "-",
            "l": "最低",
            "ccl": "持仓量",
            "o": "今开",
            "p": "最新价",
            "sc": "-",
            "vol": "成交量",
            "name": "名称",
            "wp": "买盘",
            "zde": "涨跌额",
            "zdf": "涨跌幅",
            "zjsj": "昨结",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "今开",
            "最高",
            "最低",
            "昨结",
            "成交量",
            "买盘",
            "卖盘",
            "持仓量",
        ]
    ]
    big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
    big_df["涨跌额"] = pd.to_numeric(big_df["涨跌额"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["今开"] = pd.to_numeric(big_df["今开"], errors="coerce")
    big_df["最高"] = pd.to_numeric(big_df["最高"], errors="coerce")
    big_df["最低"] = pd.to_numeric(big_df["最低"], errors="coerce")
    big_df["昨结"] = pd.to_numeric(big_df["昨结"], errors="coerce")
    big_df["成交量"] = pd.to_numeric(big_df["成交量"], errors="coerce")
    big_df["买盘"] = pd.to_numeric(big_df["买盘"], errors="coerce")
    big_df["卖盘"] = pd.to_numeric(big_df["卖盘"], errors="coerce")
    big_df["持仓量"] = pd.to_numeric(big_df["持仓量"], errors="coerce")
    return big_df


if __name__ == "__main__":
    futures_global_em_df = futures_global_em()
    print(futures_global_em_df)
