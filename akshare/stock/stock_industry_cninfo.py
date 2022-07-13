# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/7/13 15:34
Desc: 巨潮资讯-行业分类数据
http://webapi.cninfo.com.cn/#/apiDoc
http://webapi.cninfo.com.cn/api/stock/p_stock2110
"""
import time

import numpy as np
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


def stock_industry_category_cninfo(symbol: str = "巨潮行业分类标准") -> pd.DataFrame:
    """
    巨潮资讯-行业分类数据
    http://webapi.cninfo.com.cn/#/apiDoc
    查询 p_public0002 接口
    :param symbol: 行业类型; choice of {"证监会行业分类标准", "巨潮行业分类标准", "申银万国行业分类标准", "新财富行业分类标准", "国资委行业分类标准", "巨潮产业细分标准", "天相行业分类标准", "全球行业分类标准"}
    :type symbol: str
    :return: 行业分类数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "证监会行业分类标准": "008001",
        "巨潮行业分类标准": "008002",
        "申银万国行业分类标准": "008003",
        "新财富行业分类标准": "008004",
        "国资委行业分类标准": "008005",
        "巨潮产业细分标准": "008006",
        "天相行业分类标准": "008007",
        "全球行业分类标准": "008008",
    }
    url = "http://webapi.cninfo.com.cn/api/stock/p_public0002"
    params = {"indcode": "", "indtype": symbol_map[symbol]}
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
        "F001V": "类目名称英文",
        "F002D": "终止日期",
        "F003V": "行业类型编码",
        "F004V": "行业类型",
    }
    temp_df.rename(columns=cols_map, inplace=True)
    # 行业按分级排序
    tmp = temp_df[["类目编码"]].copy()
    tmp["len"] = temp_df["类目编码"].str.len()
    tmp["Level"] = 0
    g = tmp.groupby("len")
    level = 0
    for k in g.groups.keys():
        temp_df.loc[
            temp_df["类目编码"].isin(g.get_group(k)["类目编码"]), "Level"
        ] = level
        level += 1
    temp_df["Level"] = temp_df["Level"].astype(int)
    temp_df.rename(columns={"Level": "分级"}, inplace=True)
    temp_df["终止日期"] = pd.to_datetime(temp_df["终止日期"]).dt.date
    return temp_df


def stock_industry_change_cninfo(
    symbol: str = "002594",
    start_date: str = "20091227",
    end_date: str = "20220713",
) -> pd.DataFrame:
    """
    巨潮资讯-上市公司行业归属的变动情况
    http://webapi.cninfo.com.cn/#/apiDoc
    查询 p_stock2110 接口
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始变动日期
    :type start_date: str
    :param end_date: 结束变动日期
    :type end_date: str
    :return: 行业归属的变动情况
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/stock/p_stock2110"
    params = {
        "scode": symbol,
        "sdate": "-".join([start_date[:4], start_date[4:6], start_date[6:]]),
        "edate": "-".join([end_date[:4], end_date[4:6], end_date[6:]]),
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
    data_df = temp_df[[c for c in temp_df.columns if c not in ignore_cols]]
    return data_df


if __name__ == "__main__":
    stock_industry_category_cninfo_df = stock_industry_category_cninfo(
        symbol="巨潮行业分类标准"
    )
    print(stock_industry_category_cninfo_df)

    stock_industry_change_cninfo_df = stock_industry_change_cninfo(
        symbol="002594", start_date="20091227", end_date="20220708"
    )
    print(stock_industry_change_cninfo_df)
