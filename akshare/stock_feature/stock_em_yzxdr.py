# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/6 23:24
Desc: 东方财富网-数据中心-特色数据-一致行动人
http://data.eastmoney.com/yzxdr/
"""
import requests
import pandas as pd
import demjson


def stock_em_yzxdr(date: str = "2020-09-30") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-一致行动人
    http://data.eastmoney.com/yzxdr/
    :param date: 每年的季度末时间点
    :type date: str
    :return: 一致行动人
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPTA_WEB_YZXDRINDEX",
        "sty": "ALL",
        "source": "WEB",
        "p": "1",
        "ps": "50000",
        "st": "noticedate",
        "sr": "-1",
        "var": "mwUyirVm",
        "filter": f"(enddate='{date}')",
        "rt": "53575609",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "一致行动人",
        "股票代码",
        "股东排名",
        "公告日期",
        "股票简称",
        "持股数量",
        "持股比例",
        "_",
        "_",
        "行业",
        "_",
        "_",
        "数据日期",
        "股票市场",
    ]
    temp_df = temp_df[
        [
            "序号",
            "一致行动人",
            "股票代码",
            "股东排名",
            "公告日期",
            "股票简称",
            "持股数量",
            "持股比例",
            "行业",
            "数据日期",
            "股票市场",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_em_yzxdr_df = stock_em_yzxdr(date="2020-09-30")
    print(stock_em_yzxdr_df)
