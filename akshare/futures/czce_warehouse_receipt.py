# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/3 17:32
Desc: 郑州商品交易所-交易数据-仓单日报
http://www.czce.com.cn/cn/jysj/cdrb/H770310index_1.htm
"""
import re
from io import BytesIO

import pandas as pd
import requests


def futures_czce_warehouse_receipt(trade_date: str = "20200702") -> dict:

    url = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{trade_date[:4]}/{trade_date}/FutureDataWhsheet.xls"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    r = requests.get(url, verify=False, headers=headers)
    temp_df = pd.read_excel(BytesIO(r.content))
    index_list = temp_df[temp_df.iloc[:, 0].str.find("品种") == 0.0].index.to_list()
    index_list.append(len(temp_df))
    big_dict = {}
    for inner_index in range(len(index_list)-1):
        inner_df = temp_df[index_list[inner_index]: index_list[inner_index+1]]
        inner_key = re.findall(r"[a-zA-Z]+", inner_df.iloc[0, 0])[0]
        inner_df = inner_df.iloc[1:, :]
        inner_df.dropna(axis=0, how="all", inplace=True)
        inner_df.dropna(axis=1, how="all", inplace=True)
        inner_df.columns = inner_df.iloc[0, :].to_list()
        inner_df = inner_df.iloc[1:, :]
        inner_df.reset_index(inplace=True, drop=True)
        big_dict[inner_key] = inner_df
    return big_dict


if __name__ == '__main__':
    czce_warehouse_receipt_df = futures_czce_warehouse_receipt(trade_date="20200702")
    print(czce_warehouse_receipt_df)
