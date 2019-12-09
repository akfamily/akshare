# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/9 14:23
contact: jindaxiang@163.com
desc: 交易法门-登录函数
"""
from io import BytesIO
import time

from PIL import Image
import requests
import execjs

from akshare.futures_derivative import jymf_js

from akshare.futures_derivative.cons import (
    jyfm_init_headers,
    jyfm_login_url,
)


def jyfm_login(account="", password=""):
    try:
        pic_url = f"https://www.jiaoyifamen.com/captcha/login?needCaptcha={round(time.time() * 1000)}&t={execjs.eval('Math.random()')}"
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


if __name__ == "__main__":
    headers = jyfm_login(account="", password="")
    print(headers)
