# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/16 18:25
Desc: 平均持仓
https://www.legulegu.com/stockdata/averageposition
"""
import pandas as pd
import requests


def stock_legu_average_position():
    """
    平均持仓
    https://www.legulegu.com/stockdata/averageposition
    :return: 赚钱效应分析
    :rtype: pandas.DataFrame
    """
    url = "https://www.legulegu.com/stockdata/averageposition/getaverageposition"
    params = {"token": "ac237e85cf6c0a79e2a5299459827f02"}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    del temp_df["id"]
    temp_df.columns = [
        "满仓+融资",
        "80%~99%",
        "60%~79%",
        "40%~59%",
        "20%~39%",
        "0%~19%",
        "平均持仓",
        "上证指数",
        "日期",
    ]
    temp_df = temp_df[
        [
            "日期",
            "上证指数",
            "满仓+融资",
            "80%~99%",
            "60%~79%",
            "40%~59%",
            "20%~39%",
            "0%~19%",
            "平均持仓",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_legu_average_position_df = stock_legu_average_position()
    print(stock_legu_average_position_df)
