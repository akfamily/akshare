# coding=utf-8
#!/usr/bin/env python
"""
Date: 2020/4/19 14:27
Desc: 西本新干线-指数数据
http://nanjing.96369.net/
"""
import random
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image
from bs4 import BeautifulSoup

from akshare.futures_derivative.cons import (
    xgx_short_headers,
    xgx_headers,
    xgx_code_url,
    xgx_main_url,
    symbol_dict,
)

plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False


def _get_code_pic():
    payload = {"": round(random.random(), 16)}
    session = requests.session()
    res = session.get(xgx_code_url, params=payload, headers=xgx_short_headers)
    f = Image.open(BytesIO(res.content))
    f.show()
    return session


def futures_xgx_index(
    symbol: str = 67,
    start_date: str = "2000-10-01",
    end_date: str = "2020-04-17",
    plot: bool = True,
) -> pd.DataFrame:
    session = _get_code_pic()
    value = input()
    payload = {"txtStartTime": start_date, "txtEndTime": end_date, "txtyzcode": value}
    res = session.post(xgx_main_url.format(symbol), data=payload, headers=xgx_headers)
    soup = BeautifulSoup(res.text, "lxml")

    table_df = pd.read_html(res.text)[0]
    table_df.index = pd.to_datetime(table_df["日期"])
    del table_df["日期"]
    if plot:
        table_df["值"].plot()
        plt.title(
            soup.find("div", attrs={"class": "commodity_right"}).find("h5").get_text()
        )
        plt.xlabel("日期")
        plt.ylabel("值")
        plt.show()
        return table_df
    else:
        return table_df


if __name__ == "__main__":
    # 国内螺纹钢社会库存量 67
    # 国内线材社会库存量 68
    symbol_dict_df = pd.DataFrame.from_dict(symbol_dict, orient="index")
    print(symbol_dict_df)

    futures_xgx_index_df = futures_xgx_index(
        symbol=161, start_date="2000-10-01", end_date="2021-11-17", plot=True
    )
    print(futures_xgx_index_df)
