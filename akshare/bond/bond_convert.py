# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/8/6 16:24
Desc: 债券-可转债
集思录：https://app.jisilu.cn/data/cbnew/#cb
"""
import pandas as pd
import requests


def bond_cov_jsl() -> pd.DataFrame:
    """
    集思录可转债
    https://app.jisilu.cn/data/cbnew/#cb
    :return: 集思录可转债
    :rtype: pandas.DataFrame
    """
    url = "https://app.jisilu.cn/data/cbnew/cb_list/"
    params = {
        "___jsl": "LST___t = 1596700481780",
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
        "btype": "",
        "listed": "Y",
        "sw_cd": "",
        "bond_ids": "",
        "rp": "50",
    }
    r = requests.post(url, params=params, data=payload)
    temp_df = pd.DataFrame([item["cell"] for item in r.json()["rows"]])
    return temp_df


if __name__ == '__main__':
    bond_convert_jsl_df = bond_cov_jsl()
    print(bond_convert_jsl_df)
