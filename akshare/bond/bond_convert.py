#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/15 19:50
Desc: 债券-集思录-可转债
集思录：https://app.jisilu.cn/data/cbnew/#cb
"""
import pandas as pd
import requests


def bond_cov_jsl(cookie: str = None) -> pd.DataFrame:
    """
    集思录可转债
    https://app.jisilu.cn/data/cbnew/#cb
    :param cookie: 输入获取到的游览器 cookie
    :type cookie: str
    :return: 集思录可转债
    :rtype: pandas.DataFrame
    """
    url = "https://app.jisilu.cn/data/cbnew/cb_list/"
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-length': '220',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://app.jisilu.cn',
        'pragma': 'no-cache',
        'referer': 'https://app.jisilu.cn/data/cbnew/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    params = {
        "___jsl": "LST___t=1627021692978",
    }
    payload = {
        "fprice": "",
        "tprice": "",
        "curr_iss_amt": "",
        "volume": "",
        "svolume": "",
        "premium_rt": "",
        "ytm_rt": "",
        "market": "",
        "rating_cd": "",
        "is_search": "N",
        'market_cd[]': 'shmb',
        'market_cd[]': 'shkc',
        'market_cd[]': 'szmb',
        'market_cd[]': 'szcy',
        "btype": "",
        "listed": "Y",
        'qflag': 'N',
        "sw_cd": "",
        "bond_ids": "",
        "rp": "50",
    }
    r = requests.post(url, params=params, json=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame([item["cell"] for item in data_json["rows"]])
    return temp_df


def bond_conv_adj_logs_jsl(symbol: str = "128013") -> pd.DataFrame:
    """
    集思录-可转债转股价-调整记录
    https://app.jisilu.cn/data/cbnew/#cb
    :param symbol: 可转债代码
    :type symbol: str
    :return: 转股价调整记录
    :rtype: pandas.DataFrame
    """
    url = f"https://www.jisilu.cn/data/cbnew/adj_logs/?bond_id={symbol}"
    r = requests.get(url)
    data_text = r.text
    if '</table>' not in data_text:
        # 1. 该可转债没有转股价调整记录，服务端返回文本 '暂无数据'
        # 2. 无效可转债代码，服务端返回 {"timestamp":1639565628,"isError":1,"msg":"无效代码格式"}
        # 以上两种情况，返回空的 DataFrame
        return
    else:
        temp_df = pd.read_html(data_text, parse_dates=True)[0]
        temp_df['股东大会日'] = pd.to_datetime(temp_df['股东大会日']).dt.date
        temp_df['下修前转股价'] = pd.to_numeric(temp_df['下修前转股价'])
        temp_df['下修后转股价'] = pd.to_numeric(temp_df['下修后转股价'])
        temp_df['新转股价生效日期'] = pd.to_datetime(temp_df['新转股价生效日期']).dt.date
        temp_df['下修底价'] = pd.to_numeric(temp_df['下修底价'])
        return temp_df


if __name__ == '__main__':
    bond_convert_jsl_df = bond_cov_jsl(cookie='')
    print(bond_convert_jsl_df)

    bond_conv_adj_logs_jsl_df = bond_conv_adj_logs_jsl(symbol="128013")
    print(bond_conv_adj_logs_jsl_df)
