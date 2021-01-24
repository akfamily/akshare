# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/24 20:54
Desc: 中国外汇交易中心暨全国银行间同业拆借中心
中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场做市报价
中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
http://www.chinamoney.com.cn/chinese/mkdatabond/
"""
import pandas as pd
import requests


def bond_spot_quote() -> pd.DataFrame:
    """
    处理中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场做市报价
    http://www.chinamoney.com.cn/chinese/mkdatabond/
    """
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbMktMakQuot"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }
    payload = {
        "flag": "1",
        "lang": "cn",
    }
    r = requests.post(url=url, data=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "_",
        "买入/卖出净价",
        "_",
        "_",
        "_",
        "_",
        "债券简称",
        "_",
        "_",
        "_",
        "报价机构",
        "_",
        "_",
        "_",
        "买入/卖出收益率",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "报价机构",
            "债券简称",
            "买入/卖出净价",
            "买入/卖出收益率",
        ]
    ]
    temp_df["买入净价"] = temp_df["买入/卖出净价"].str.split("/", expand=True).iloc[:, 0]
    temp_df["卖出净价"] = temp_df["买入/卖出净价"].str.split("/", expand=True).iloc[:, 1]
    temp_df["买入收益率"] = temp_df["买入/卖出收益率"].str.split("/", expand=True).iloc[:, 0]
    temp_df["卖出收益率"] = temp_df["买入/卖出收益率"].str.split("/", expand=True).iloc[:, 1]
    del temp_df["买入/卖出净价"]
    del temp_df["买入/卖出收益率"]
    return temp_df


def bond_spot_deal() -> pd.DataFrame:
    """
    中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
    http://www.chinamoney.com.cn/chinese/mkdatabond/
    """
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbtPri"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }
    payload = {
        "flag": "1",
        "lang": "cn",
        "bondName": "",
    }
    r = requests.post(url=url, data=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "_",
        "成交净价",
        "涨跌",
        "_",
        "债券简称",
        "_",
        "_",
        "交易量",
        "_",
        "最新收益率",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "加权收益率",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "债券简称",
            "成交净价",
            "最新收益率",
            "涨跌",
            "加权收益率",
            "交易量",
        ]
    ]
    return temp_df


def bond_china_yield(
    start_date: str = "2020-02-04", end_date: str = "2021-01-24"
) -> pd.DataFrame:
    """
    中国债券信息网-国债及其他债券收益率曲线
    https://www.chinabond.com.cn/
    http://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery?startDate=2019-02-07&endDate=2020-02-04&gjqx=0&qxId=ycqx&locale=cn_ZH
    注意: end_date - start_date 应该小于一年
    :param start_date: 需要查询的日期, 返回在该日期之后一年内的数据
    :type start_date: str
    :param end_date: 需要查询的日期, 返回在该日期之前一年内的数据
    :type end_date: str
    :return: 返回在指定日期之间之前一年内的数据
    :rtype: pandas.DataFrame
    """
    url = "http://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery"
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "gjqx": "0",
        "qxId": "ycqx",
        "locale": "cn_ZH",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    res = requests.get(url, params=params, headers=headers)
    data_text = res.text.replace("&nbsp", "")
    data_df = pd.read_html(data_text, header=0)[1]
    return data_df


if __name__ == "__main__":
    bond_spot_quote_df = bond_spot_quote()
    print(bond_spot_quote_df)
    bond_spot_deal_df = bond_spot_deal()
    print(bond_spot_deal_df)
    bond_china_yield_df = bond_china_yield(
        start_date="2020-02-01", end_date="2021-01-24"
    )
    print(bond_china_yield_df)
