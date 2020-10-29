# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/29 11:48
Desc: 腾讯-债券-质押式回购-实时行情-成交明细
下载成交明细-每个交易日16:00提供当日数据
http://stockhtm.finance.qq.com/sstock/ggcx/131802.shtml
"""
from io import StringIO

import pandas as pd
import requests


def bond_repo_zh_tick(code="sz131802", trade_date="20201028"):
    """
    成交明细-每个交易日16:00提供当日数据
    http://stockhtm.finance.qq.com/sstock/ggcx/131802.shtml
    :param code: 带市场标识的债券-质押式回购代码
    :type code: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回指定交易日债券-质押式回购成交明细的数据
    :rtype: pandas.DataFrame
    """
    url = "http://stock.gtimg.cn/data/index.php"
    params = {
        "appn": "detail",
        "action": "download",
        "c": code,
        "d": trade_date,
    }
    r = requests.get(url, params=params)
    r.encoding = "gbk"
    temp_df = pd.read_table(StringIO(r.text))
    return temp_df


if __name__ == "__main__":
    date_list = pd.date_range(start="20201001", end="20201028").tolist()
    date_list = [item.strftime("%Y%m%d") for item in date_list]
    for item in date_list:
        data = bond_repo_zh_tick(code="sz131802", trade_date=f"{item}")
        if not data.empty:
            print(data)
