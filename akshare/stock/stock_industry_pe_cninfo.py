#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/9/14 16:29
Desc: 巨潮资讯-数据中心-行业分析-行业市盈率
http://webapi.cninfo.com.cn/#/thematicStatistics?name=%E6%8A%95%E8%B5%84%E8%AF%84%E7%BA%A7
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


def stock_industry_pe_ratio_cninfo(symbol: str = "证监会行业分类", date: str = "20210910") -> pd.DataFrame:
    """
    巨潮资讯-数据中心-行业分析-行业市盈率
    http://webapi.cninfo.com.cn/#/thematicStatistics
    :param symbol: choice of {"证监会行业分类", "国证行业分类"}
    :type symbol: str
    :param date: 查询日期
    :type date: str
    :return: 行业市盈率
    :rtype: pandas.DataFrame
    """
    sort_code_map = {
        "证监会行业分类": "008001",
        "国证行业分类": "008200"
    }
    url = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1087"
    params = {"tdate": "-".join([date[:4], date[4:6], date[6:]]),
              "sortcode": sort_code_map[symbol],
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
        "行业层级",
        "静态市盈率-算术平均",
        "静态市盈率-中位数",
        "静态市盈率-加权平均",
        "净利润-静态",
        "行业名称",
        "行业编码",
        "行业分类",
        "总市值-静态",
        "纳入计算公司数量",
        "变动日期",
        "公司数量",
    ]
    temp_df = temp_df[[
        "变动日期",
        "行业分类",
        "行业层级",
        "行业编码",
        "行业名称",
        "公司数量",
        "纳入计算公司数量",
        "总市值-静态",
        "净利润-静态",
        "静态市盈率-加权平均",
        "静态市盈率-中位数",
        "静态市盈率-算术平均",
    ]]
    temp_df["行业层级"] = pd.to_numeric(temp_df["行业层级"], errors="coerce")
    temp_df["公司数量"] = pd.to_numeric(temp_df["公司数量"], errors="coerce")
    temp_df["纳入计算公司数量"] = pd.to_numeric(temp_df["纳入计算公司数量"], errors="coerce")
    temp_df["总市值-静态"] = pd.to_numeric(temp_df["总市值-静态"], errors="coerce")
    temp_df["净利润-静态"] = pd.to_numeric(temp_df["净利润-静态"], errors="coerce")
    temp_df["静态市盈率-加权平均"] = pd.to_numeric(temp_df["静态市盈率-加权平均"], errors="coerce")
    temp_df["静态市盈率-中位数"] = pd.to_numeric(temp_df["静态市盈率-中位数"], errors="coerce")
    temp_df["静态市盈率-算术平均"] = pd.to_numeric(temp_df["静态市盈率-算术平均"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_industry_pe_ratio_cninfo_df = stock_industry_pe_ratio_cninfo(symbol="国证行业分类", date="20210907")
    print(stock_industry_pe_ratio_cninfo_df)
