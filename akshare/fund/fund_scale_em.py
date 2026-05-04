# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/10/27 20:30
Desc: 天天基金网-基金数据-规模份额
https://fund.eastmoney.com/data/cyrjglist.html
"""

from io import StringIO

import pandas as pd
import requests

from akshare.utils import demjson
from akshare.tool.latest_quarter import latest_quarter


def fund_scale_change_em() -> pd.DataFrame:
    """
    天天基金网-基金数据-规模份额-规模变动
    https://fund.eastmoney.com/data/gmbdlist.html
    :return: 规模变动
    :rtype: pandas.DataFrame
    """
    url = "https://fund.eastmoney.com/data/FundDataPortfolio_Interface.aspx"
    params = {
        "dt": "9",
        "pi": "1",
        "pn": "50",
        "mc": "hypzDetail",
        "st": "desc",
        "sc": "reportdate",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    total_page = data_json["pages"]
    big_df = pd.DataFrame()
    for page in range(1, int(total_page) + 1):
        params.update({"pi": page})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -1])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df["index"] + 1
    big_df.columns = [
        "序号",
        "截止日期",
        "基金家数",
        "期间申购",
        "期间赎回",
        "期末总份额",
        "期末净资产",
    ]
    big_df["截止日期"] = pd.to_datetime(big_df["截止日期"], errors="coerce").dt.date
    big_df["基金家数"] = pd.to_numeric(big_df["基金家数"], errors="coerce")
    big_df["期间申购"] = pd.to_numeric(
        big_df["期间申购"].str.replace(",", ""), errors="coerce"
    )
    big_df["期间赎回"] = pd.to_numeric(
        big_df["期间赎回"].str.replace(",", ""), errors="coerce"
    )
    big_df["期末总份额"] = pd.to_numeric(
        big_df["期末总份额"].str.replace(",", ""), errors="coerce"
    )
    big_df["期末净资产"] = pd.to_numeric(
        big_df["期末净资产"].str.replace(",", ""), errors="coerce"
    )
    return big_df

def fund_scale_change_detail_all_em(date: str = "", qmjzc_minimum_value: int = 0) -> pd.DataFrame:
    """
    天天基金网-基金数据-规模份额-规模变动-基金明细
    https://fund.eastmoney.com/data/gmbddetail.html
    :param date: 季度日期，格式 "YYYY_Q"，如"2026_1"，为空则为当前最新季度
    :type date: str
    :param qmjzc_minimum_value: 期末净资产（亿元）最小值，设置则输出大于最小值的所有基金规模明细，留空则默认输出全部（数据量较大）
    :type qmjzc_minimum_value: int
    :return: 基金规模明细
    :rtype: pandas.DataFrame
    """
    if not date:
        date = latest_quarter()
    url = "https://fund.eastmoney.com/data/FundDataPortfolio_Interface.aspx"
    params = {
        "dt": "8",
        "t": date,
        "pi": "1",
        "pn": "150",
        "mc": "returnJson",
        "st": "desc",
        "sc": "qmjzc",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    total_page = data_json["pages"]
    big_df = pd.DataFrame()
    for page in range(1, int(total_page) + 1):
        params.update({"pi": page})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -1])
        temp_df = pd.DataFrame(data_json["data"])
        temp_df.columns = [
            "基金代码",
            "基金简称",
            "期间申购（亿份）",
            "期间赎回（亿份）",
            "期末总份额（亿份）",
            "期末净资产（亿元）",
        ]
        temp_df["期末净资产（亿元）"] = pd.to_numeric(
            temp_df["期末净资产（亿元）"].str.replace(",", ""), errors="coerce"
        )
        original_count = len(temp_df)
        temp_df = temp_df[temp_df["期末净资产（亿元）"] >= qmjzc_minimum_value]
        if len(temp_df) == 0:
            break
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
        if len(temp_df) < original_count:
            break
    if len(big_df) == 0:
        big_df = pd.DataFrame(columns=[
            "基金代码",
            "基金简称",
            "期间申购（亿份）",
            "期间赎回（亿份）",
            "期末总份额（亿份）",
            "期末净资产（亿元）",
        ])
        return big_df
    big_df["期间申购（亿份）"] = pd.to_numeric(
        big_df["期间申购（亿份）"].str.replace(",", ""), errors="coerce"
    )
    big_df["期间赎回（亿份）"] = pd.to_numeric(
        big_df["期间赎回（亿份）"].str.replace(",", ""), errors="coerce"
    )
    big_df["期末总份额（亿份）"] = pd.to_numeric(
        big_df["期末总份额（亿份）"].str.replace(",", ""), errors="coerce"
    )
    return big_df

def fund_scale_single_em(symbol: str = "000001") -> pd.DataFrame:
    """
    天天基金网-基金数据-规模份额-单只基金规模变动
    https://fundf10.eastmoney.com/gmbd_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :return: 单只基金规模变动
    :rtype: pandas.DataFrame
    """
    url = "https://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "gmbd",
        "mode": "0",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.read_html(StringIO(data_json["content"]))[0]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["期间申购（亿份）"] = pd.to_numeric(temp_df["期间申购（亿份）"], errors="coerce")
    temp_df["期间赎回（亿份）"] = pd.to_numeric(temp_df["期间赎回（亿份）"], errors="coerce")
    temp_df["期末总份额（亿份）"] = pd.to_numeric(temp_df["期末总份额（亿份）"], errors="coerce")
    temp_df["期末净资产（亿元）"] = pd.to_numeric(temp_df["期末净资产（亿元）"], errors="coerce")
    temp_df["净资产变动率"] = temp_df["净资产变动率"].str.replace("%", "", regex=False)
    temp_df["净资产变动率"] = pd.to_numeric(temp_df["净资产变动率"], errors="coerce")
    return temp_df


def fund_hold_structure_em() -> pd.DataFrame:
    """
    天天基金网-基金数据-规模份额-持有人结构
    https://fund.eastmoney.com/data/cyrjglist.html
    :return: 持有人结构
    :rtype: pandas.DataFrame
    """
    url = "https://fund.eastmoney.com/data/FundDataPortfolio_Interface.aspx"
    params = {
        "dt": "11",
        "pi": "1",
        "pn": "50",
        "mc": "hypzDetail",
        "st": "desc",
        "sc": "reportdate",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    total_page = data_json["pages"]
    big_df = pd.DataFrame()
    for page in range(1, int(total_page) + 1):
        params.update({"pi": page})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -1])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df["index"] + 1
    big_df.columns = [
        "序号",
        "截止日期",
        "基金家数",
        "机构持有比列",
        "个人持有比列",
        "内部持有比列",
        "总份额",
    ]
    big_df["截止日期"] = pd.to_datetime(big_df["截止日期"], errors="coerce").dt.date
    big_df["基金家数"] = pd.to_numeric(big_df["基金家数"], errors="coerce")
    big_df["机构持有比列"] = pd.to_numeric(big_df["机构持有比列"], errors="coerce")
    big_df["个人持有比列"] = pd.to_numeric(big_df["个人持有比列"], errors="coerce")
    big_df["内部持有比列"] = pd.to_numeric(big_df["内部持有比列"], errors="coerce")
    big_df["总份额"] = pd.to_numeric(
        big_df["总份额"].str.replace(",", ""), errors="coerce"
    )
    return big_df



if __name__ == "__main__":
    fund_scale_change_em_df = fund_scale_change_em()
    print(fund_scale_change_em_df)

    fund_scale_change_detail_em_df = fund_scale_change_detail_all_em()
    print(fund_scale_change_detail_em_df)

    fund_scale_single_em_df = fund_scale_single_em(symbol="000001")
    print(fund_scale_single_em_df)

    fund_hold_structure_em_df = fund_hold_structure_em()
    print(fund_hold_structure_em_df)
    
