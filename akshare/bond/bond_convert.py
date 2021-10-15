# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/23 14:24
Desc: 债券-集思录-可转债
集思录：https://app.jisilu.cn/data/cbnew/#cb
"""
import pandas as pd
import requests


def bond_cov_jsl(cookie: None = '') -> pd.DataFrame:
    """
    集思录可转债
    https://app.jisilu.cn/data/cbnew/#cb
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


if __name__ == '__main__':
    bond_convert_jsl_df = bond_cov_jsl(cookie='')
    print(bond_convert_jsl_df)
