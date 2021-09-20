# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/9/18 16:29
Desc: 巨潮资讯-数据中心-新股数据
http://webapi.cninfo.com.cn/#/xinguList
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


def stock_new_gh_cninfo() -> pd.DataFrame:
    """
    巨潮资讯-数据中心-新股数据-新股过会
    http://webapi.cninfo.com.cn/#/xinguList
    :return: 新股过会
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1098"
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
    temp_df.columns = [
        "公司名称",
        "上会日期",
        "审核类型",
        "审议内容",
        "审核结果",
        "审核公告日",
    ]
    temp_df["上会日期"] = pd.to_datetime(temp_df["上会日期"]).dt.date
    temp_df["审核公告日"] = pd.to_datetime(temp_df["审核公告日"]).dt.date
    return temp_df


def stock_new_ipo_cninfo() -> pd.DataFrame:
    """
    巨潮资讯-数据中心-新股数据-新股发行
    http://webapi.cninfo.com.cn/#/xinguList
    :return: 新股发行
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1097"
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
        "timetype": "36",
        "market": "ALL",
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "摇号结果公告日",
        "中签公告日",
        "证券简称",
        "上市日期",
        "中签缴款日",
        "申购日期",
        "发行价",
        "证劵代码",
        "上网发行中签率",
        "总发行数量",
        "发行市盈率",
        "上网发行数量",
        "网上申购上限",
    ]
    temp_df = temp_df[
        [
            "证劵代码",
            "证券简称",
            "上市日期",
            "申购日期",
            "发行价",
            "总发行数量",
            "发行市盈率",
            "上网发行中签率",
            "摇号结果公告日",
            "中签公告日",
            "中签缴款日",
            "网上申购上限",
            "上网发行数量",
        ]
    ]
    temp_df["摇号结果公告日"] = pd.to_datetime(temp_df["摇号结果公告日"]).dt.date
    temp_df["中签公告日"] = pd.to_datetime(temp_df["中签公告日"]).dt.date
    temp_df["上市日期"] = pd.to_datetime(temp_df["上市日期"]).dt.date
    temp_df["中签缴款日"] = pd.to_datetime(temp_df["中签缴款日"]).dt.date
    temp_df["申购日期"] = pd.to_datetime(temp_df["申购日期"]).dt.date
    temp_df["发行价"] = pd.to_numeric(temp_df["发行价"])
    temp_df["上网发行中签率"] = pd.to_numeric(temp_df["上网发行中签率"])
    temp_df["总发行数量"] = pd.to_numeric(temp_df["总发行数量"])
    temp_df["发行市盈率"] = pd.to_numeric(temp_df["发行市盈率"])
    temp_df["上网发行数量"] = pd.to_numeric(temp_df["上网发行数量"])
    temp_df["网上申购上限"] = pd.to_numeric(temp_df["网上申购上限"])
    return temp_df


if __name__ == "__main__":
    stock_new_gh_cninfo_df = stock_new_gh_cninfo()
    print(stock_new_gh_cninfo_df)

    stock_new_ipo_cninfo_df = stock_new_ipo_cninfo()
    print(stock_new_ipo_cninfo_df)
