# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/10/1 19:19
Desc: 巨潮资讯-数据中心-专题统计-公司治理-股权质押
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


def stock_cg_equity_mortgage_cninfo(date: str = "20210930") -> pd.DataFrame:
    """
    巨潮资讯-数据中心-专题统计-公司治理-股权质押
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param date: 开始统计时间
    :type date: str
    :return: 股权质押
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1094"
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
        "tdate": "-".join([date[:4], date[4:6], date[6:]]),
    }
    r = requests.post(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "质押解除数量",
        "股票简称",
        "公告日期",
        "质押事项",
        "质权人",
        "出质人",
        "股票代码",
        "占总股本比例",
        "累计质押占总股本比例",
        "质押数量",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "公告日期",
            "出质人",
            "质权人",
            "质押数量",
            "占总股本比例",
            "质押解除数量",
            "质押事项",
            "累计质押占总股本比例",
        ]
    ]
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
    temp_df["质押数量"] = pd.to_numeric(temp_df["质押数量"])
    temp_df["占总股本比例"] = pd.to_numeric(temp_df["占总股本比例"])
    temp_df["质押解除数量"] = pd.to_numeric(temp_df["质押解除数量"])
    temp_df["累计质押占总股本比例"] = pd.to_numeric(temp_df["累计质押占总股本比例"])
    return temp_df


if __name__ == "__main__":
    pd.set_option('display.max_columns', 4)
    stock_cg_equity_mortgage_cninfo_df = stock_cg_equity_mortgage_cninfo(date="20210930")
    print(stock_cg_equity_mortgage_cninfo_df)
