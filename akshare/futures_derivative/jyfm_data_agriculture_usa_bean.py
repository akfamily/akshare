# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/6 0:17
contact: jindaxiang@163.com
desc: 交易法门-数据-农产品-美豆
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


def usa_bean_grow(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/usa-bean-grow/grow", headers=headers
    )
    return res.json()


def usa_bean_emergence_ratio(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/usa-bean-emergence/ratio", headers=headers
    )
    return res.json()


def usa_bean_flower_ratio(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/usa-bean-flower/ratio", headers=headers
    )
    return res.json()


def usa_bean_good_ratio(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/usa-bean-good/ratio", headers=headers
    )
    return res.json()


def usa_bean_harvest_ratio(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/usa-bean-harvest/ratio", headers=headers
    )
    return res.json()


def usa_bean_export_ratio(headers=""):
    res = requests.get(
        "https://www.jiaoyifamen.com/data/usa-bean-export/ratio", headers=headers
    )
    return res.json()


if __name__ == "__main__":
    headers = jyfm_login(account="", password="")
    df = usa_bean_export_ratio(headers=headers)
    temp_df = pd.DataFrame(df)
    print(temp_df)
