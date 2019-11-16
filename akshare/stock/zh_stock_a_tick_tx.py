# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/16 20:39
contact: jindaxiang@163.com
desc: 腾讯-股票-实时行情-成交明细
"""
import requests
import pandas as pd
from io import StringIO


def stock_zh_a_tick(code="sh600848", trade_date="20191011"):
    url = f"http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c={code}&d={trade_date}"
    res = requests.get(url)
    res.encoding = "gbk"
    df = pd.read_table(StringIO(res.text))
    return df


if __name__ == "__main__":
    date_list = pd.date_range(start="20180801", end="20191111").tolist()
    date_list = [item.strftime("%Y%m%d") for item in date_list]
    for item in date_list:
        data = stock_zh_a_tick(code="sh601872", trade_date=f"{item}")
        if not data.empty:
            print(data)

