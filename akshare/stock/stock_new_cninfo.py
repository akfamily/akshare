# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/9/16 19:29
Desc: 巨潮资讯-数据中心-新股数据
http://webapi.cninfo.com.cn/#/xinguList
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


def stock_new_gh_cninfo() -> pd.DataFrame:
    """
    巨潮资讯-数据中心-新股数据
    http://webapi.cninfo.com.cn/#/xinguList
    :param symbol: choice of {"证监会行业分类", "国证行业分类"}
    :type symbol: str
    :param date: 查询日期
    :type date: str
    :return: 行业市盈率
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


if __name__ == "__main__":
    stock_new_gh_cninfo_df = stock_new_gh_cninfo()
    print(stock_new_gh_cninfo_df)
