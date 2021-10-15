# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/9/11 22:25
Desc: 乐咕乐股网-调查平均持仓数据
https://www.legulegu.com/stockdata/averageposition
"""
import pandas as pd
import requests


def stock_average_position_legu() -> pd.DataFrame:
    """
    乐咕乐股网-调查平均持仓数据
    https://www.legulegu.com/stockdata/averageposition
    :return: 调查平均持仓数据
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
    stock_average_position_legu_df = stock_average_position_legu()
    print(stock_average_position_legu_df)
