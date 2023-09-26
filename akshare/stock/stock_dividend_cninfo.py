# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/9/26 15:00
Desc: 巨潮资讯-个股-历史分红
http://webapi.cninfo.com.cn/#/company?companyid=600009
"""
import pandas as pd
import requests
from py_mini_racer import py_mini_racer

from akshare.datasets import get_ths_js


def _get_file_content_ths(file: str = "cninfo.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_ths_js(file)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def stock_dividend_cninfo(symbol: str = "600009") -> pd.DataFrame:
    """
    巨潮资讯-个股-历史分红
    http://webapi.cninfo.com.cn/#/company?companyid=600009
    :param symbol: 股票代码
    :type symbol: str
    :return: 历史分红
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1139"
    params = {"scode": symbol}
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("cninfo.js")
    js_code.eval(js_content)
    mcode = js_code.call("getResCode1")
    headers = {
        "Accept": "*/*",
        "Accept-Enckey": mcode,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Host": "webapi.cninfo.com.cn",
        "Origin": "http://webapi.cninfo.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://webapi.cninfo.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "实施方案公告日期",
        "送股比例",
        "转增比例",
        "派息比例",
        "股权登记日",
        "除权日",
        "派息日",
        "股份到账日",
        "实施方案分红说明",
        "分红类型",
        "报告时间",
    ]
    temp_df["实施方案公告日期"] = pd.to_datetime(temp_df["实施方案公告日期"]).dt.date
    temp_df["送股比例"] = pd.to_numeric(temp_df["送股比例"], errors="coerce")
    temp_df["转增比例"] = pd.to_numeric(temp_df["转增比例"], errors="coerce")
    temp_df["派息比例"] = pd.to_numeric(temp_df["派息比例"], errors="coerce")
    temp_df["股权登记日"] = pd.to_datetime(temp_df["股权登记日"], errors="coerce").dt.date
    temp_df["除权日"] = pd.to_datetime(temp_df["除权日"], errors="coerce").dt.date
    temp_df["派息日"] = pd.to_datetime(temp_df["派息日"], errors="coerce").dt.date
    temp_df.sort_values(by="实施方案公告日期", ignore_index=True, inplace=True)
    return temp_df


if __name__ == "__main__":
    stock_dividend_cninfo_df = stock_dividend_cninfo(symbol="600009")
    print(stock_dividend_cninfo_df)
