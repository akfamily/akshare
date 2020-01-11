# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/4 16:36
contact: jindaxiang@163.com
desc: 获取金十数据-其他-加密货币实时行情
"""
import json
import time

import pandas as pd
import requests

from akshare.economic.cons import bitcoin_url, bitcoin_payload


def get_js_dc_current():
    """
    主流数字货币的实时行情数据, 一次请求返回具体某一时刻行情数据
    :return: pandas.DataFrame
    """
    bit_payload = bitcoin_payload.copy()
    bit_payload.update({"_": int(time.time() * 1000)})
    bit_payload.update(
        {
            "jsonpCallback": bitcoin_payload["jsonpCallback"].format(
                int(time.time() * 1000)
            )
        }
    )
    res = requests.get(bitcoin_url, params=bit_payload)
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    data_df = pd.DataFrame(json_data["data"])
    data_df.set_index("update", drop=True, inplace=True)
    data_df.index = pd.to_datetime(data_df.index)
    return data_df.iloc[:, :-4]


if __name__ == "__main__":
    df = get_js_dc_current()
    print(df)
