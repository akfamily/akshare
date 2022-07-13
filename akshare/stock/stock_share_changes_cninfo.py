# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/7/11 16:44
Desc: 巨潮资讯-股本股东-公司股本变动
http://webapi.cninfo.com.cn/api/stock/p_stock2215
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


def stock_share_change_cninfo(
    symbol: str = "002594",
    start_date: str = "20091227",
    end_date: str = "20220713",
) -> pd.DataFrame:
    """
    巨潮资讯-股本股东-公司股本变动
    http://webapi.cninfo.com.cn/#/apiDoc
    查询 p_stock2215 接口
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始变动日期
    :type start_date: str
    :param end_date: 结束变动日期
    :type end_date: str
    :return: 公司股本变动
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/stock/p_stock2215"
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
        "SECCODE": "证券代码",
        "SECNAME": "证券简称",
        "ORGNAME": "机构名称",
        "DECLAREDATE": "公告日期",
        "VARYDATE": "变动日期",
        "F001V": "变动原因编码",
        "F002V": "变动原因",
        "F003N": "总股本",
        "F004N": "未流通股份",
        "F005N": "发起人股份",
        "F006N": "国家持股",
        "F007N": "国有法人持股",
        "F008N": "境内法人持股",
        "F009N": "境外法人持股",
        "F010N": "自然人持股",
        "F011N": "募集法人股",
        "F012N": "内部职工股",
        "F013N": "转配股",
        "F014N": "其他流通受限股份",
        "F015N": "优先股",
        "F016N": "其他未流通股",
        "F021N": "已流通股份",
        "F022N": "人民币普通股",
        "F023N": "境内上市外资股-B股",
        "F024N": "境外上市外资股-H股",
        "F025N": "高管股",
        "F026N": "其他流通股",
        "F028N": "流通受限股份",
        "F017N": "配售法人股",
        "F018N": "战略投资者持股",
        "F019N": "证券投资基金持股",
        "F020N": "一般法人持股",
        "F029N": "国家持股-受限",
        "F030N": "国有法人持股-受限",
        "F031N": "其他内资持股-受限",
        "F032N": "其中：境内法人持股",
        "F033N": "其中：境内自然人持股",
        "F034N": "外资持股-受限",
        "F035N": "其中：境外法人持股",
        "F036N": "其中：境外自然人持股",
        "F037N": "其中：限售高管股",
        "F038N": "其中：限售B股",
        "F040N": "其中：限售H股",
        "F027C": "最新记录标识",
        "F049N": "其他",
        "F050N": "控股股东、实际控制人",
    }
    ignore_cols = ["最新记录标识", "其他"]
    temp_df.rename(columns=cols_map, inplace=True)
    temp_df.fillna(np.nan, inplace=True)
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
    temp_df["变动日期"] = pd.to_datetime(temp_df["变动日期"]).dt.date
    data_df = temp_df[[c for c in temp_df.columns if c not in ignore_cols]]
    return data_df


if __name__ == "__main__":
    stock_share_change_cninfo_df = stock_share_change_cninfo(
        symbol="002594",
        start_date="20091227",
        end_date="20220713",
    )
    print(stock_share_change_cninfo_df)
