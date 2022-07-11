# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/10/21 12:19
Desc: 巨潮资讯-数据中心-专题统计-基金报表
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


def fund_report_stock_cninfo(date: str = "20210630") -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-基金报表-基金重仓股
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param date: 报告时间; choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}
    :type date: str
    :return: 基金重仓股
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1112"
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
        "rdate": "-".join([date[:4], date[4:6], date[6:]]),
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.rename(
        columns={
            "F003N": "持股总市值",
            "F002N": "持股总数",
            "F001N": "基金覆盖家数",
            "SECNAME": "股票简称",
            "ID": "序号",
            "SECCODE": "股票代码",
            "ENDDATE": "报告期",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "报告期",
            "基金覆盖家数",
            "持股总数",
            "持股总市值",
        ]
    ]
    temp_df["报告期"] = pd.to_datetime(temp_df["报告期"]).dt.date
    temp_df["持股总数"] = pd.to_numeric(temp_df["持股总数"])
    temp_df["持股总市值"] = pd.to_numeric(temp_df["持股总市值"])
    temp_df["基金覆盖家数"] = pd.to_numeric(temp_df["基金覆盖家数"])
    return temp_df


def fund_report_industry_allocation_cninfo(date: str = "20210630") -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-基金报表-基金行业配置
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param date: 报告时间; choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}, 从 2017 年开始
    :type date: str
    :return: 基金行业配置
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1113"
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
        "rdate": "-".join([date[:4], date[4:6], date[6:]]),
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.rename(
        columns={
            'F004N': '行业规模',
            'F003N': '基金覆盖家数',
            'F002V': '证监会行业名称',
            'F001V': '行业编码',
            'ENDDATE': '报告期',
            'F005N': '占净资产比例'
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            '行业编码',
            '证监会行业名称',
            '报告期',
            '基金覆盖家数',
            '行业规模',
            '占净资产比例',
        ]
    ]
    temp_df["报告期"] = pd.to_datetime(temp_df["报告期"]).dt.date
    temp_df["基金覆盖家数"] = pd.to_numeric(temp_df["基金覆盖家数"])
    temp_df["行业规模"] = pd.to_numeric(temp_df["行业规模"])
    temp_df["占净资产比例"] = pd.to_numeric(temp_df["占净资产比例"])
    return temp_df


def fund_report_asset_allocation_cninfo() -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-基金报表-基金资产配置
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :return: 基金资产配置
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1114"
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
    r = requests.post(url, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.rename(
        columns={
            'F001N': '基金覆盖家数',
            'F008N': '现金货币类占净资产比例',
            'F007N': '债券固定收益类占净资产比例',
            'F006N': '股票权益类占净资产比例',
            'ENDDATE': '报告期',
            'F005N': '基金市场净资产规模'
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            '报告期',
            '基金覆盖家数',
            '股票权益类占净资产比例',
            '债券固定收益类占净资产比例',
            '现金货币类占净资产比例',
            '基金市场净资产规模',
        ]
    ]
    temp_df["报告期"] = pd.to_datetime(temp_df["报告期"]).dt.date
    temp_df["基金覆盖家数"] = pd.to_numeric(temp_df["基金覆盖家数"])
    temp_df["股票权益类占净资产比例"] = pd.to_numeric(temp_df["股票权益类占净资产比例"])
    temp_df["债券固定收益类占净资产比例"] = pd.to_numeric(temp_df["债券固定收益类占净资产比例"])
    temp_df["现金货币类占净资产比例"] = pd.to_numeric(temp_df["现金货币类占净资产比例"])
    temp_df["基金市场净资产规模"] = pd.to_numeric(temp_df["基金市场净资产规模"])
    return temp_df


if __name__ == "__main__":
    fund_report_stock_cninfo_df = fund_report_stock_cninfo(date="20210630")
    print(fund_report_stock_cninfo_df)

    fund_report_industry_allocation_cninfo_df = fund_report_industry_allocation_cninfo(date="20210930")
    print(fund_report_industry_allocation_cninfo_df)

    fund_report_asset_allocation_cninfo_df = fund_report_asset_allocation_cninfo()
    print(fund_report_asset_allocation_cninfo_df)
