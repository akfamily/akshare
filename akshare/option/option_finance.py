# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 获取金融期权数据
"""
import requests
import pandas as pd

from akshare.option.cons import (SH_OPTION_URL,
                                 SH_OPTION_PAYLOAD,
                                 SH_OPTION_PAYLOAD_OTHER,
                                 SH_OPTION_URL_KING)


def get_finance_option_current():
    res = requests.get(SH_OPTION_URL, params=SH_OPTION_PAYLOAD)
    data_json = res.json()
    raw_data = pd.DataFrame(data_json["list"])
    raw_data.at[0, 0] = "510050"
    raw_data.at[0, 8] = pd.to_datetime(str(data_json["date"]) + str(data_json["time"]), format="%Y%m%d%H%M%S")
    raw_data.columns = ["代码", "名称", "当前价", "涨跌", "涨跌幅", "振幅", "成交量(手)", "成交额(万元)", "更新日期"]
    return raw_data


def get_finance_option(symbol="03"):
    res = requests.get(SH_OPTION_URL_KING.format(symbol), params=SH_OPTION_PAYLOAD_OTHER)
    data_json = res.json()
    raw_data = pd.DataFrame(data_json["list"])
    raw_data.index = [str(data_json["date"]) + str(data_json["time"])] * data_json["total"]
    raw_data.columns = ["合约交易代码", "当前价", "涨跌幅", "前结价", "行权价"]
    raw_data["数量"] = [data_json["total"]] * data_json["total"]
    return raw_data


if __name__ == "__main__":
    df = get_finance_option_current()
    print(df)
    df = get_finance_option(symbol="03")
    print(df)
