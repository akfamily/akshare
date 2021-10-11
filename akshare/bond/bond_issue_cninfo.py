# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/10/11 12:19
Desc: 巨潮资讯-数据中心-专题统计-债券报表-债券发行
http://webapi.cninfo.com.cn/#/thematicStatistics
"""
import time

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

js_str = """
    function mcode(input) {  
                var keyStr = "ABCDEFGHIJKLMNOP" + "QRSTUVWXYZabcdef" + "ghijklmnopqrstuv"   + "wxyz0123456789+/" + "=";  
                var output = "";  
                var chr1, chr2, chr3 = "";  
                var enc1, enc2, enc3, enc4 = "";  
                var i = 0;  
                do {  
                    chr1 = input.charCodeAt(i++);  
                    chr2 = input.charCodeAt(i++);  
                    chr3 = input.charCodeAt(i++);  
                    enc1 = chr1 >> 2;  
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);  
                    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);  
                    enc4 = chr3 & 63;  
                    if (isNaN(chr2)) {  
                        enc3 = enc4 = 64;  
                    } else if (isNaN(chr3)) {  
                        enc4 = 64;  
                    }  
                    output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2)  
                            + keyStr.charAt(enc3) + keyStr.charAt(enc4);  
                    chr1 = chr2 = chr3 = "";  
                    enc1 = enc2 = enc3 = enc4 = "";  
                } while (i < input.length);  
          
                return output;  
            }  
"""


def bond_treasure_issue_cninfo(
        start_date: str = "20210910", end_date: str = "20211109"
) -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-债券报表-债券发行-国债发行
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param start_date: 开始统计时间
    :type start_date: str
    :param end_date: 开始统计时间
    :type end_date: str
    :return: 国债发行
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1120"
    random_time_str = str(int(time.time()))
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(js_str)
    mcode = js_code.call("mcode", random_time_str)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Host": "webapi.cninfo.com.cn",
        "mcode": mcode,
        "Origin": "http://webapi.cninfo.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://webapi.cninfo.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    params = {
        "sdate": "-".join([start_date[:4], start_date[4:6], start_date[6:]]),
        "edate": "-".join([end_date[:4], end_date[4:6], end_date[6:]]),
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.rename(
        columns={
            "F009D": "缴款日",
            "SECNAME": "债券简称",
            "DECLAREDATE": "公告日期",
            "F004D": "发行起始日",
            "F003D": "发行终止日",
            "F008N": "单位面值",
            "SECCODE": "债券代码",
            "F007N": "发行价格",
            "F006N": "计划发行总量",
            "F005N": "实际发行总量",
            "F028N": "增发次数",
            "BONDNAME": "债券名称",
            "F014V": "发行对象",
            "F002V": "交易市场",
            "F013V": "发行方式",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "债券代码",
            "债券简称",
            "发行起始日",
            "发行终止日",
            "计划发行总量",
            "实际发行总量",
            "发行价格",
            "单位面值",
            "缴款日",
            "增发次数",
            "交易市场",
            "发行方式",
            "发行对象",
            "公告日期",
            "债券名称",
        ]
    ]
    temp_df["发行起始日"] = pd.to_datetime(temp_df["发行起始日"]).dt.date
    temp_df["发行终止日"] = pd.to_datetime(temp_df["发行终止日"]).dt.date
    temp_df["缴款日"] = pd.to_datetime(temp_df["缴款日"]).dt.date
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
    temp_df["计划发行总量"] = pd.to_numeric(temp_df["计划发行总量"])
    temp_df["实际发行总量"] = pd.to_numeric(temp_df["实际发行总量"])
    temp_df["发行价格"] = pd.to_numeric(temp_df["发行价格"])
    temp_df["单位面值"] = pd.to_numeric(temp_df["单位面值"])
    temp_df["增发次数"] = pd.to_numeric(temp_df["增发次数"])
    return temp_df


def bond_local_government_issue_cninfo(
        start_date: str = "20210911", end_date: str = "20211110"
) -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-债券报表-债券发行-地方债发行
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param start_date: 开始统计时间
    :type start_date: str
    :param end_date: 开始统计时间
    :type end_date: str
    :return: 地方债发行
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1121"
    random_time_str = str(int(time.time()))
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(js_str)
    mcode = js_code.call("mcode", random_time_str)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Host": "webapi.cninfo.com.cn",
        "mcode": mcode,
        "Origin": "http://webapi.cninfo.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://webapi.cninfo.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    params = {
        "sdate": "-".join([start_date[:4], start_date[4:6], start_date[6:]]),
        "edate": "-".join([end_date[:4], end_date[4:6], end_date[6:]]),
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.rename(
        columns={
            "F009D": "缴款日",
            "SECNAME": "债券简称",
            "DECLAREDATE": "公告日期",
            "F004D": "发行起始日",
            "F003D": "发行终止日",
            "F008N": "单位面值",
            "SECCODE": "债券代码",
            "F007N": "发行价格",
            "F006N": "计划发行总量",
            "F005N": "实际发行总量",
            "F028N": "增发次数",
            "BONDNAME": "债券名称",
            "F014V": "发行对象",
            "F002V": "交易市场",
            "F013V": "发行方式",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "债券代码",
            "债券简称",
            "发行起始日",
            "发行终止日",
            "计划发行总量",
            "实际发行总量",
            "发行价格",
            "单位面值",
            "缴款日",
            "增发次数",
            "交易市场",
            "发行方式",
            "发行对象",
            "公告日期",
            "债券名称",
        ]
    ]
    temp_df["发行起始日"] = pd.to_datetime(temp_df["发行起始日"]).dt.date
    temp_df["发行终止日"] = pd.to_datetime(temp_df["发行终止日"]).dt.date
    temp_df["缴款日"] = pd.to_datetime(temp_df["缴款日"]).dt.date
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
    temp_df["计划发行总量"] = pd.to_numeric(temp_df["计划发行总量"])
    temp_df["实际发行总量"] = pd.to_numeric(temp_df["实际发行总量"])
    temp_df["发行价格"] = pd.to_numeric(temp_df["发行价格"])
    temp_df["单位面值"] = pd.to_numeric(temp_df["单位面值"])
    temp_df["增发次数"] = pd.to_numeric(temp_df["增发次数"])
    return temp_df


if __name__ == "__main__":
    bond_treasure_issue_cninfo_df = bond_treasure_issue_cninfo(
        start_date="20210910", end_date="20211109"
    )
    print(bond_treasure_issue_cninfo_df)

    bond_local_government_issue_cninfo_df = bond_local_government_issue_cninfo(start_date="20210911", end_date="20211110")
    print(bond_local_government_issue_cninfo_df)
