# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/15 18:02
Desc: 东方财富网-数据中心-新股数据-打新收益率
东方财富网-数据中心-新股数据-打新收益率
http://data.eastmoney.com/xg/xg/dxsyl.html
"""
import demjson
import pandas as pd
import requests
from tqdm import tqdm


# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 500)


def _get_page_num_dxsyl(market: str = "上海主板") -> int:
    """
    东方财富网-数据中心-新股数据-打新收益率-总页数
    http://data.eastmoney.com/xg/xg/dxsyl.html
    :param market: choice of {"上海主板", "中小板", "创业板"}
    :type market: str
    :return: 总页数
    :rtype: int
    """
    market_map = {"上海主板": "2", "创业板": "3", "中小板": "4"}
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "NS",
        "sty": "NSDXSYL",
        "st": "16",
        "sr": "-1",
        "p": "1",
        "ps": "50",
        "js": "var oyfyNYmO={pages:(pc),data:[(x)]}",
        "stat": market_map[market],
        "rt": "52898446",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
    return data_json["pages"]


def stock_em_dxsyl(market: str = "上海主板") -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-打新收益率
    http://data.eastmoney.com/xg/xg/dxsyl.html
    :param market: choice of {"上海主板", "中小板", "创业板"}
    :type market: str
    :return: 指定市场的打新收益率数据
    :rtype: pandas.DataFrame
    """
    market_map = {"上海主板": "2", "创业板": "3", "中小板": "4"}
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    page_num = _get_page_num_dxsyl(market=market)
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "NS",
            "sty": "NSDXSYL",
            "st": "16",
            "sr": "-1",
            "p": str(page),
            "ps": "50",
            "js": "var oyfyNYmO={pages:(pc),data:[(x)]}",
            "stat": market_map[market],
            "rt": "52898446",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df = temp_df.iloc[:, 0].str.split(",", expand=True)
    temp_df.columns = [
        "股票代码",
        "股票简称",
        "发行价",
        "最新价",
        "网上发行中签率",
        "网上有效申购股数",
        "网上有效申购户数",
        "网上超额认购倍数",
        "网下配售中签率",
        "网下有效申购股数",
        "网下有效申购户数",
        "网下配售认购倍数",
        "总发行数量",
        "开盘溢价",
        "首日涨幅",
        "打新收益",
        "上市日期",
        "市场",
    ]
    return temp_df


if __name__ == "__main__":
    stock_em_dxsyl_df = stock_em_dxsyl(market="上海主板")
    print(stock_em_dxsyl_df)
