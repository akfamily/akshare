# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/9/16 17:29
Desc: 巨潮资讯-个股-历史分红
http://webapi.cninfo.com.cn/#/company?companyid=600009
"""
import time
from py_mini_racer import py_mini_racer
import requests
import pandas as pd


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


def stock_dividents_cninfo(symbol: str = "600009") -> pd.DataFrame:
    """
    巨潮资讯-个股-历史分红
    http://webapi.cninfo.com.cn/#/company?companyid=600009
    :param symbol: 股票代码
    :type symbol: str
    :return: 历史分红
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1139"
    params = {
        'scode': symbol
              }
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
    return temp_df


if __name__ == "__main__":
    stock_dividents_cninfo_df = stock_dividents_cninfo(symbol="600009")
    print(stock_dividents_cninfo_df)
