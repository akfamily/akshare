# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2026/04/30 12:00
Desc: 巨潮资讯-港股-重要指标-分红派息表
https://webapi.cninfo.com.cn/#/apiDoc
"""

import pandas as pd
import py_mini_racer
import requests

from akshare.datasets import get_ths_js


def _get_file_content_cninfo(file: str = "cninfo.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_ths_js(file)
    with open(setting_file_path, encoding="utf-8") as f:
        file_data = f.read()
    return file_data


def stock_hk_dividend_cninfo(
    symbol: str = "00700",
    start_date: str = "19000101",
    end_date: str = "21000101",
    state: str = "1",
) -> pd.DataFrame:
    """
    巨潮资讯-港股-重要指标-分红派息表
    https://webapi.cninfo.com.cn/#/apiDoc
    查询 p_hk4018 接口
    :param symbol: 港股代码
    :type symbol: str
    :param start_date: 开始查询时间
    :type start_date: str
    :param end_date: 结束查询时间
    :type end_date: str
    :param state: 查询状态; 1: 历史所有数据; 2: 最近一次数据
    :type state: str
    :return: 分红派息表
    :rtype: pandas.DataFrame
    """
    symbol = symbol.zfill(5)
    url = "https://webapi.cninfo.com.cn/api/hk/p_hk4018"
    params = {
        "scode": symbol,
        "sdate": "-".join([start_date[:4], start_date[4:6], start_date[6:]]),
        "edate": "-".join([end_date[:4], end_date[4:6], end_date[6:]]),
        "state": state,
    }
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_cninfo("cninfo.js")
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
        "Origin": "https://webapi.cninfo.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "https://webapi.cninfo.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/93.0.4577.63 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json.get("records", []))
    if temp_df.empty:
        return temp_df
    temp_df.rename(
        columns={
            "SECCODE": "证券代码",
            "SECNAME": "证券简称",
            "F001D": "公告日期",
            "F002D": "分红年度",
            "F003V": "事项类型",
            "F004V": "事项",
            "F005D": "股权登记日",
            "F006D": "除净日",
            "F007D": "开始截止过户日期",
            "F008D": "最后截止过户日期",
            "F009D": "派息日",
            "F010N": "每股派息",
            "F011V": "每股派息币种",
            "F012N": "派息比例",
            "F013N": "派息比例值",
            "F015V": "币种",
            "F044V": "实物分派说明",
            "F046V": "派息方式",
            "MEMO": "备注",
        },
        inplace=True,
    )
    date_cols = [
        "公告日期",
        "分红年度",
        "股权登记日",
        "除净日",
        "开始截止过户日期",
        "最后截止过户日期",
        "派息日",
    ]
    for item in date_cols:
        temp_df[item] = pd.to_datetime(temp_df[item], errors="coerce").dt.date
    numeric_cols = ["每股派息", "派息比例", "派息比例值"]
    for item in numeric_cols:
        temp_df[item] = pd.to_numeric(temp_df[item], errors="coerce")
    temp_df = temp_df[
        [
            "证券代码",
            "证券简称",
            "公告日期",
            "分红年度",
            "事项类型",
            "事项",
            "股权登记日",
            "除净日",
            "开始截止过户日期",
            "最后截止过户日期",
            "派息日",
            "每股派息",
            "每股派息币种",
            "派息比例",
            "派息比例值",
            "币种",
            "派息方式",
            "实物分派说明",
            "备注",
        ]
    ]
    temp_df.sort_values(by="公告日期", ignore_index=True, inplace=True)
    return temp_df


if __name__ == "__main__":
    stock_hk_dividend_cninfo_df = stock_hk_dividend_cninfo(
        symbol="00700",
        start_date="20200101",
        end_date="20260101",
    )
    print(stock_hk_dividend_cninfo_df)
