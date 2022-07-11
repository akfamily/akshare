#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/9/21 16:19
Desc: 巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度
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


def stock_hold_num_cninfo(date: str = "20210630") -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param date: choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}; 从 20170331 开始
    :type date: str
    :return: 股东人数及持股集中度
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1034"
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
        "rdate": date,
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "本期人均持股数量",
        "股东人数增幅",
        "上期股东人数",
        "本期股东人数",
        "证券简称",
        "证券代码",
        "人均持股数量增幅",
        "变动日期",
        "上期人均持股数量",
    ]
    temp_df = temp_df[
        [
            "证券代码",
            "证券简称",
            "变动日期",
            "本期股东人数",
            "上期股东人数",
            "股东人数增幅",
            "本期人均持股数量",
            "上期人均持股数量",
            "人均持股数量增幅",
        ]
    ]
    temp_df["变动日期"] = pd.to_datetime(temp_df["变动日期"]).dt.date
    temp_df["本期人均持股数量"] = pd.to_numeric(temp_df["本期人均持股数量"])
    temp_df["股东人数增幅"] = pd.to_numeric(temp_df["股东人数增幅"])
    temp_df["上期股东人数"] = pd.to_numeric(temp_df["上期股东人数"])
    temp_df["本期股东人数"] = pd.to_numeric(temp_df["本期股东人数"])
    temp_df["人均持股数量增幅"] = pd.to_numeric(temp_df["人均持股数量增幅"])
    temp_df["上期人均持股数量"] = pd.to_numeric(temp_df["上期人均持股数量"])
    return temp_df


if __name__ == "__main__":
    stock_hold_num_cninfo_df = stock_hold_num_cninfo(date="20211130")
    print(stock_hold_num_cninfo_df)
