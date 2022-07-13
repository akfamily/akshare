# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/7/11 16:44
Desc: 巨潮资讯-行业分类数据
http://webapi.cninfo.com.cn/api/stock/p_public0002
http://webapi.cninfo.com.cn/api/stock/p_stock2110
"""
import time
from py_mini_racer import py_mini_racer
import requests
import pandas as pd
import numpy as np


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


def stock_industry_category_cninfo(indtype: str="008003") -> pd.DataFrame:
    """
    巨潮资讯-行业分类数据
    http://webapi.cninfo.com.cn/api/stock/p_public0002
    :param indtype: 行业类型
    :type indtype: str
    "008001" : "证监会行业分类标准"
    "008002" : "巨潮行业分类标准"
    "008003" : "申银万国行业分类标准"
    "008004" : "新财富行业分类标准"
    "008005" : "国资委行业分类标准"
    "008006" : "巨潮产业细分标准"
    "008007" : "天相行业分类标准"
    "008008" : "全球行业分类标准（GICS）"
    :return: 行业分类数据
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/stock/p_public0002"
    params = {
        'indcode': "",
        'indtype': indtype
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
    cols_map = {
        "PARENTCODE": "父类编码",
        "SORTCODE": "类目编码",
        "SORTNAME": "类目名称",
        "F001V": "类目名称（英文）",
        "F002D": "终止日期",
        "F003V": "行业类型编码",
        "F004V": "行业类型"
    }
    temp_df.rename(columns=cols_map, inplace=True)
    temp_df.fillna(np.nan, inplace=True)
    temp_df["终止日期"] = pd.to_datetime(temp_df["终止日期"]).dt.date

    tmp = temp_df[["类目编码"]].copy()
    tmp["len"] = temp_df["类目编码"].str.len()
    tmp["Level"] = 0
    g = tmp.groupby("len")
    level = 0
    for k in g.groups.keys():
        temp_df.loc[temp_df["类目编码"].isin(g.get_group(k)["类目编码"]), "Level"] = level
        level += 1

    return temp_df

def stock_industry_cninfo(symbol: str = "002594", sdate: str="2009-12-27", edate: str="2022-07-08") -> pd.DataFrame:
    """
    巨潮资讯-上市公司行业归属的变动情况
    http://webapi.cninfo.com.cn/api/stock/p_stock2110
    :param symbol: 股票代码
    :type symbol: str
    :param sdate: 开始变动日期
    :type sdate: str
    :param edate: 结束变动日期
    :type edate: str
    :return: 行业归属的变动情况
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/stock/p_stock2110"
    params = {
        'scode': symbol,
        'sdate': sdate,
        'edate': edate
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
    cols_map = {
        "ORGNAME": "机构名称",
        "SECCODE": "证券代码",
        "SECNAME": "新证券简称",
        "VARYDATE": "变更日期",
        "F001V": "分类标准编码",
        "F002V": "分类标准",
        "F003V": "行业编码",
        "F004V": "行业门类",
        "F005V": "行业次类",
        "F006V": "行业大类",
        "F007V": "行业中类",
        "F008C": "最新记录标识",
    }
    ignore_cols = ["最新记录标识"]
    temp_df.rename(columns=cols_map, inplace=True)
    temp_df.fillna(np.nan, inplace=True)
    temp_df["变更日期"] = pd.to_datetime(temp_df["变更日期"]).dt.date
    return temp_df[[c for c in temp_df.columns if c not in ignore_cols]]


if __name__ == "__main__":
    stock_industry_category_cninfo_df = stock_industry_category_cninfo()
    print(stock_industry_category_cninfo_df)
    stock_industry_cninfo_df = stock_industry_cninfo()
    print(stock_industry_cninfo_df)
