#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/08 19:20
Desc: 巨潮资讯-个股-公司概况
http://webapi.cninfo.com.cn/#/company
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


def stock_profile_cninfo(symbol: str = "600030") -> pd.DataFrame:
    """
    巨潮资讯-个股-公司概况
    http://webapi.cninfo.com.cn/#/company
    :param symbol: 股票代码
    :type symbol: str
    :return: 公司概况
    :rtype: pandas.DataFrame
    :raise: Exception，如果服务器返回的数据无法被解析
    """
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1133"
    params = {
        "scode": symbol,
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
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(url, params=params, headers=headers)
    data_json = r.json()
    columns = [
        "公司名称",
        "英文名称",
        "曾用简称",
        "A股代码",
        "A股简称",
        "B股代码",
        "B股简称",
        "H股代码",
        "H股简称",
        "入选指数",
        "所属市场",
        "所属行业",
        "法人代表",
        "注册资金",
        "成立日期",
        "上市日期",
        "官方网站",
        "电子邮箱",
        "联系电话",
        "传真",
        "注册地址",
        "办公地址",
        "邮政编码",
        "主营业务",
        "经营范围",
        "机构简介",
    ]
    count = data_json["count"]
    if count == 1:
        # 有公司概况的
        redundant_json = data_json["records"][0]
        records_json = {}
        i = 0
        for k, v in redundant_json.items():
            if i == (len(redundant_json) - 4):
                break
            records_json[k] = v
            i += 1
        del i
        temp_df = pd.Series(records_json).to_frame().T
        temp_df.columns = columns
    elif count == 0:
        # 没公司概况的
        temp_df = pd.DataFrame(columns=columns)
    else:
        raise Exception("数据错误！")
    return temp_df


if __name__ == "__main__":
    stock_profile_cninfo_df = stock_profile_cninfo(symbol="600030")
    print(stock_profile_cninfo_df)
