#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/08 18:11
Desc: 巨潮资讯-数据浏览器-筹资指标-公司配股实施方案
http://webapi.cninfo.com.cn/#/dataBrowse
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


def stock_allotment_cninfo(
    symbol: str = "600030", start_date: str = "19700101", end_date: str = "22220222"
) -> pd.DataFrame:
    """
    巨潮资讯-个股-配股实施方案
    http://webapi.cninfo.com.cn/#/dataBrowse
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始查询的日期
    :type symbol: str
    :param end_date: 结束查询的日期
    :type symbol: str
    :return: 配股实施方案
    :rtype: pandas.DataFrame
    """
    url = "http://webapi.cninfo.com.cn/api/stock/p_stock2232"
    params = {
        "scode": symbol,
        "sdate": start_date
        if not start_date
        else f"{start_date[0:4]}-{start_date[4:6]}-{start_date[6:8]}",
        "edate": end_date
        if not end_date
        else f"{end_date[0:4]}-{end_date[4:6]}-{end_date[6:8]}",
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
        "记录标识",
        "证券简称",
        "停牌起始日",
        "上市公告日期",
        "配股缴款起始日",
        "可转配股数量",
        "停牌截止日",
        "实际配股数量",
        "配股价格",
        "配股比例",
        "配股前总股本",
        "每股配权转让费(元)",
        "法人股实配数量",
        "实际募资净额",
        "大股东认购方式",
        "其他配售简称",
        "发行方式",
        "配股失败，退还申购款日期",
        "除权基准日",
        "预计发行费用",
        "配股发行结果公告日",
        "证券代码",
        "配股权证交易截止日",
        "其他股份实配数量",
        "国家股实配数量",
        "委托单位",
        "公众获转配数量",
        "其他配售代码",
        "配售对象",
        "配股权证交易起始日",
        "资金到账日",
        "机构名称",
        "股权登记日",
        "实际募资总额",
        "预计募集资金",
        "大股东认购数量",
        "公众股实配数量",
        "转配股实配数量",
        "承销费用",
        "法人获转配数量",
        "配股后流通股本",
        "股票类别",
        "公众配售简称",
        "发行方式编码",
        "承销方式",
        "公告日期",
        "配股上市日",
        "配股缴款截止日",
        "承销余额(股)",
        "预计配股数量",
        "配股后总股本",
        "职工股实配数量",
        "承销方式编码",
        "发行费用总额",
        "配股前流通股本",
        "股票类别编码",
        "公众配售代码",
    ]
    if data_json["records"]:
        # 有配股记录
        temp_df = pd.DataFrame(data_json["records"])
        temp_df.columns = columns
        dates = (
            "停牌起始日",
            "上市公告日期",
            "配股失败，退还申购款日期",
            "配股缴款起始日",
            "停牌截止日",
            "除权基准日",
            "配股发行结果公告日",
            "配股权证交易截止日",
            "配股权证交易起始日",
            "资金到账日",
            "股权登记日",
            "公告日期",
            "配股上市日",
            "配股缴款截止日",
        )
        for s in dates:
            temp_df[s] = pd.to_datetime(temp_df[s], errors="coerce").dt.date
        nums = (
            "可转配股数量",
            "实际配股数量",
            "配股价格",
            "配股比例",
            "配股前总股本",
            "每股配权转让费(元)",
            "法人股实配数量",
            "实际募资净额",
            "预计发行费用",
            "其他股份实配数量",
            "国家股实配数量",
            "公众获转配数量",
            "实际募资总额",
            "预计募集资金",
            "大股东认购数量",
            "公众股实配数量",
            "转配股实配数量",
            "承销费用",
            "法人获转配数量",
            "配股后流通股本",
            "承销余额(股)",
            "预计配股数量",
            "配股后总股本",
            "职工股实配数量",
            "发行费用总额",
            "配股前流通股本",
        )
        for s in nums:
            temp_df[s] = pd.to_numeric(temp_df[s], errors="coerce")
    else:
        # 没有配股数据
        temp_df = pd.DataFrame(columns=columns)

    return temp_df


if __name__ == "__main__":
    stock_allotment_cninfo_df = stock_allotment_cninfo(symbol="600030", start_date="19900101", end_date="20221008")
    print(stock_allotment_cninfo_df)
