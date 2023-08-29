#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/8/27 20:20
Desc: 巨潮资讯-个股-上市相关
http://webapi.cninfo.com.cn/#/company
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


def stock_ipo_summary_cninfo(symbol: str = "600030") -> pd.DataFrame:
    """
    巨潮资讯-个股-上市相关
    http://webapi.cninfo.com.cn/#/company
    :param symbol: 股票代码
    :type symbol: str
    :return: 上市相关
    :rtype: pandas.DataFrame
    :raise: Exception，如果服务器返回的数据无法被解析
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1134"
    params = {
        "scode": symbol,
    }
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("cninfo.js")
    js_code.eval(js_content)
    mcode = js_code.call("getResCode1")
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Host": "webapi.cninfo.com.cn",
        "Accept-Enckey": mcode,
        "Origin": "http://webapi.cninfo.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://webapi.cninfo.com.cn/",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(url, params=params, headers=headers)
    data_json = r.json()
    columns = [
        "股票代码",
        "招股公告日期",
        "中签率公告日",
        "每股面值(元)",
        "总发行数量(万股)",
        "发行前每股净资产(元)",
        "摊薄发行市盈率",
        "募集资金净额(万元)",
        "上网发行日期",
        "上市日期",
        "发行价格(元)",
        "发行费用总额(万元)",
        "发行后每股净资产(元)",
        "上网发行中签率(%)",
        "主承销商",
    ]
    count = data_json["count"]
    if count == 1:
        # 有上市相关的
        redundant_json = data_json["records"][0]
        records_json = {}
        i = 0
        for k, v in redundant_json.items():
            if i == (len(redundant_json)):
                break
            records_json[k] = v
            i += 1
        del i
        temp_df = pd.Series(records_json).to_frame().T
        temp_df.columns = columns
    elif count == 0:
        # 没上市相关的
        temp_df = pd.DataFrame(columns=columns)
    else:
        raise Exception("数据错误！")
    return temp_df


if __name__ == "__main__":
    stock_ipo_summary_cninfo_df = stock_ipo_summary_cninfo(symbol="600030")
    print(stock_ipo_summary_cninfo_df)