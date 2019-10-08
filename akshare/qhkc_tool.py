# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc:
货可查指数目前已经收费, 特提供奇货可查-工具数据接口, 方便您调用
"""
import pandas as pd
import requests
from typing import AnyStr

from akshare.cons import (QHKC_TOOL_FOREIGN)


def get_qhkc_tool_foreign(url: AnyStr = QHKC_TOOL_FOREIGN):
    """
    奇货可查-工具-外盘比价
    实时更新数据, 暂不能查询历史数据
    :param url: 网址
    :return: pd.DataFrame
        name    base_time base_price latest_price   rate
         伦敦铜  10/08 01:00       5704       5746.5  0.745
         伦敦锌  10/08 01:00    2291.25      2305.75  0.633
         伦敦镍  10/08 01:00      17720      17372.5 -1.961
         伦敦铝  10/08 01:00     1743.5      1742.75 -0.043
         伦敦锡  10/07 15:00      16550        16290 -1.571
         伦敦铅  10/08 01:00    2181.25       2177.5 -0.172
        美原油1  10/08 02:30      52.81        53.05  0.454
        美原油2  10/07 23:00      53.94        53.05  -1.65
        布原油1  10/08 02:30      58.41        58.67  0.445
        布原油2  10/07 23:00      59.54        58.67 -1.461
         美燃油  10/07 23:00     1.9287       1.9102 -0.959
        CMX金  10/08 02:30     1495.9       1496.5   0.04
        CMX银  10/08 02:30     17.457       17.457      0
          美豆  10/07 23:00     916.12       915.88 -0.026
         美豆粕  10/07 23:00     302.75       302.65 -0.033
         美豆油  10/07 23:00      30.02        29.91 -0.366
         美玉米  10/07 23:00     386.38       387.88  0.388
          美糖  10/07 23:30      12.37        12.53  1.293
         美棉花  10/07 23:30      61.69        61.05 -1.037
    """
    payload_id = {
        "page": 1,
        "limit": 10
    }
    r = requests.post(url, data=payload_id)
    print("数据获取成功")
    json_data = r.json()
    name = []
    base_time = []
    base_price = []
    latest_price = []
    rate = []
    for item in json_data["data"]:
        name.append(item["name"])
        base_time.append(item["base_time"])
        base_price.append(item["base_price"])
        latest_price.append(item["latest_price"])
        rate.append(item["rate"])
    temp_df = pd.DataFrame([name, base_time, base_price, latest_price, rate]).T
    temp_df.columns = ["name", "base_time", "base_price", "latest_price", "rate"]
    return temp_df


if __name__ == "__main__":
    df = get_qhkc_tool_foreign()
    print(df)
