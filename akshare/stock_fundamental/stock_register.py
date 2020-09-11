# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/9/10 16:19
Desc: 东方财富网-数据中心-新股数据-注册制审核
http://data.eastmoney.com/kcb/?type=nsb
"""
import demjson
import pandas as pd
import requests


def stock_register_kcb():
    """
    东方财富网-数据中心-新股数据-注册制审核-科创板
    http://data.eastmoney.com/kcb/?type=nsb
    :return: 科创板注册制审核结果
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "KCB_YSB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "update_date",
        "sr": "-1",
        "p": "1",
        "ps": "500",
        "js": "var CuzkGWQs={pages:(tp),data:(x),font:(font)}",
        "rt": "53324195",
    }

    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") :])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.columns = [
        "_",
        "受理日期",
        "更新日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "发行人全称",
        "_",
        "_",
        "审核状态",
        "注册地",
        "证监会行业",
        "保荐机构",
        "律师事务所",
        "会计师事务所",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        ["发行人全称", "审核状态", "注册地", "证监会行业", "保荐机构", "律师事务所", "会计师事务所", "更新日期", "受理日期"]
    ]
    return temp_df


def stock_register_cyb():
    """
    东方财富网-数据中心-新股数据-注册制审核-创业板
    http://data.eastmoney.com/xg/cyb/
    :return: 创业板注册制审核结果
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPT_GEM_REGIPO_BASICINFO",
        "sty": "ORG_CODE,SECURITY_CODE,ISSUER_NAME,CHECK_STATUS,REG_ADDRESS,CSRC_INDUSTRY,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,UPDATE_DATE,ACCEPT_DATE,NUM",
        "token": "894050c76af8597a853f5b408b759f5d",
        "source": "GEMREG",
        "client": "WEB",
        "p": "1",
        "ps": "5000",
        "st": "UPDATE_DATE,ORG_CODE",
        "sr": "-1,-1",
        "var": "mmTmEhWD",
        "rt": "53326609",
    }

    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "_",
        "_",
        "发行人全称",
        "审核状态",
        "注册地",
        "证监会行业",
        "保荐机构",
        "律师事务所",
        "会计师事务所",
        "更新日期",
        "受理日期",
        "_",
    ]
    temp_df = temp_df[
        [
            "发行人全称",
            "审核状态",
            "注册地",
            "证监会行业",
            "保荐机构",
            "律师事务所",
            "会计师事务所",
            "更新日期",
            "受理日期",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_register_kcb_df = stock_register_kcb()
    print(stock_register_kcb_df)

    stock_register_cyb_df = stock_register_cyb()
    print(stock_register_cyb_df)
