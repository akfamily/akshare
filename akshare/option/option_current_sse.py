# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2025/9/8 16:20
Desc: 上海证券交易所-产品-股票期权-信息披露-当日合约
http://www.sse.com.cn/assortment/options/disclo/preinfo/
"""

import pandas as pd
import requests


def option_current_day_sse() -> pd.DataFrame:
    """
    上海证券交易所-产品-股票期权-信息披露-当日合约
    http://www.sse.com.cn/assortment/options/disclo/preinfo/
    :return: 上交所期权当日合约
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/commonQuery.do"
    params = {
        "isPagination": "false",
        "expireDate": "",
        "securityId": "",
        "sqlId": "SSE_ZQPZ_YSP_GGQQZSXT_XXPL_DRHY_SEARCH_L",
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/101.0.4951.67 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"])
    dict_df = {
        "SECURITY_ID": "合约编码",
        "CONTRACT_ID": "合约交易代码",
        "CONTRACT_SYMBOL": "合约简称",
        "SECURITYNAMEBYID": "标的券名称及代码",
        "CALL_OR_PUT": "类型",
        "EXERCISE_PRICE": "行权价",
        "CONTRACT_UNIT": "合约单位",
        "END_DATE": "期权行权日",
        "DELIVERY_DATE": "行权交收日",
        "EXPIRE_DATE": "到期日",
        "START_DATE": "开始日期",
    }
    temp_df = temp_df[dict_df.keys()].rename(columns=dict_df)
    return temp_df


if __name__ == "__main__":
    option_current_day_sse_df = option_current_day_sse()
    print(option_current_day_sse_df)
