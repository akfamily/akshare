# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/21 12:08
contact: jindaxiang@163.com
desc: 获取金十数据-数据中心-欧洲-宏观经济
后续修改为类 --> 去除冗余代码
"""
import json
import time

import pandas as pd
import requests

from akshare.economic.cons import JS_EURO_RATE_DECISION_URL


def get_euro_interest_rate():
    """
    获取欧洲央行决议报告, 数据区间从19990101-至今
    :return: pandas.Series
    1999-01-01      3
    1999-02-01      3
    1999-03-01      3
    1999-04-01      3
    1999-05-01    2.5
                 ...
    2019-04-10      0
    2019-06-06      0
    2019-07-25      0
    2019-09-12      0
    2019-10-24      0
    """
    t = time.time()
    res = requests.get(
        JS_EURO_RATE_DECISION_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区利率决议"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "interest_rate"
    return temp_df


if __name__ == "__main__":
    df = get_euro_interest_rate()
    print(df)
