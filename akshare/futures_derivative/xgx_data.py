# coding=utf-8
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/15 18:27
desc: 西本新干线-指数数据
"""
import random
from io import BytesIO

from PIL import Image
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

from akshare.futures_derivative.cons import (xgx_short_headers,
                                             xgx_headers,
                                             xgx_code_url,
                                             xgx_main_url,
                                             symbol_dict)

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


def get_code_pic():
    payload = {
        "": round(random.random(), 16)
    }
    session = requests.session()
    res = session.get(xgx_code_url, params=payload, headers=xgx_short_headers)
    f = Image.open(BytesIO(res.content))
    f.show()
    return session


def xgx_data(symbol=67, plot=True):
    session = get_code_pic()
    value = input()
    payload = {
        "txtStartTime": "1992-10-01",
        "txtEndTime": "2019-10-27",
        "txtyzcode": value
    }
    res = session.post(xgx_main_url.format(symbol), data=payload, headers=xgx_headers)
    soup = BeautifulSoup(res.text, "lxml")

    table_df = pd.read_html(res.text)[0]
    table_df.index = pd.to_datetime(table_df["日期"])
    del table_df["日期"]
    if plot:
        table_df["值"].plot()
        plt.title(soup.find("div", attrs={"class": "commodity_right"}).find("h5").get_text())
        plt.xlabel("日期")
        plt.ylabel("值")
        plt.show()
        return table_df
    else:
        return table_df


if __name__ == "__main__":
    # 国内螺纹钢社会库存量 67
    # 国内线材社会库存量 68
    print(pd.DataFrame.from_dict(symbol_dict, orient="index"))
    df = xgx_data(symbol=161, plot=True)
    print(df)
