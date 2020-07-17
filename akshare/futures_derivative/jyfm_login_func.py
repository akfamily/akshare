# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/9 14:23
Desc: 交易法门-登录函数
"""
from io import BytesIO

from PIL import Image
import requests
import execjs

from akshare.futures_derivative import jymf_js

from akshare.futures_derivative.cons import (
    jyfm_init_headers,
    jyfm_login_url,
)


def jyfm_login(account="", password=""):
    """
    交易法门网站登录函数
    :param account: user account
    :type account: str
    :param password: user password
    :type password: str
    :return: headers with cookies
    :rtype: dict
    """
    try:
        pic_url = f"https://www.jiaoyifamen.com/captcha"
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
