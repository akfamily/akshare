# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/6 0:17
contact: jindaxiang@163.com
desc: 交易法门-数据-农产品-白糖
"""
from io import BytesIO

from PIL import Image

import requests
import pandas as pd
import execjs

from akshare.futures_derivative import jymf_js


from akshare.futures_derivative.cons import (
    jyfm_init_headers,
    jyfm_login_url,
)


def jyfm_login(account="", password=""):
    try:
        pic_url = f"https://www.jiaoyifamen.com/captcha/login?needCaptcha=1571976133484&t={execjs.eval('Math.random()')}"
        res = requests.get(pic_url)
        f = Image.open(BytesIO(res.content))
        f.show()
        code = input()
        c_func = execjs.compile(jymf_js.c.replace(r"\n", ""))
        en_psw = c_func.call("e", password)
        payload = {"nameOrEmail": account, "userPassword": en_psw, "captcha": code}
    except:
        c_func = execjs.compile(jymf_js.c.replace(r"\n", ""))
        en_psw = c_func.call("e", password)
        payload = {"nameOrEmail": account, "userPassword": en_psw}
    res = requests.post(jyfm_login_url, json=payload, headers=jyfm_init_headers)
    copy_jyfm_init_headers = jyfm_init_headers.copy()
    copy_jyfm_init_headers["cookie"] = (
        list(dict(res.cookies).keys())[0]
        + "="
        + list(dict(res.cookies).values())[0]
        + "; "
        + list(dict(res.cookies).keys())[1]
        + "="
        + list(dict(res.cookies).values())[1]
    )
    return copy_jyfm_init_headers


def sugar_month_data_produce_2(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-month-data/produce?category=2",
        headers=headers,
    )
    return res.json()


def sugar_month_data_produce_1(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-month-data/produce?category=1",
        headers=headers,
    )
    return res.json()


def sugar_month_data_trade(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-month-trade/trade", headers=headers
    )
    return res.json()


def sugar_month_data_stock(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-month-stock/stock", headers=headers
    )
    return res.json()


def sugar_year_data_grow_area(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-year-grow-area/grow", headers=headers
    )
    return res.json()


def sugar_year_data_yield(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-year-yield/yield", headers=headers
    )
    return res.json()


def sugar_year_data_produce(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-year-data/produce", headers=headers
    )
    return res.json()


def sugar_year_data_trade(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-year-data/trade", headers=headers
    )
    return res.json()


def sugar_year_data_gap(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-year-data/gap", headers=headers
    )
    return res.json()


def sugar_year_data_stock(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/sugar-year-stock/stock", headers=headers
    )
    return res.json()


if __name__ == "__main__":
    headers = jyfm_login(account="", password="")
    df = sugar_year_data_stock(headers=headers)
    temp_df = pd.DataFrame(df)
    print(temp_df)
