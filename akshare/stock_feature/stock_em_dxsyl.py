# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/9/21 12:02
Desc: 东方财富网-数据中心-新股数据-打新收益率
东方财富网-数据中心-新股数据-打新收益率
http://data.eastmoney.com/xg/xg/dxsyl.html
东方财富网-数据中心-新股数据-新股申购与中签查询
http://data.eastmoney.com/xg/xg/default_2.html
"""
import demjson
import pandas as pd
import requests
from tqdm import tqdm


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
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
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
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
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


def stock_em_xgsglb(market: str = "上海主板"):
    """
    新股申购与中签查询
    http://data.eastmoney.com/xg/xg/default_2.html
    :param market: choice of {"上海主板", "创业板", "中小板", "科创板"}
    :type market: str
    :return: 新股申购与中签数据
    :rtype: pandas.DataFrame
    """
    market_map = {
        "上海主板": "sh",
        "创业板": "cyb",
        "中小板": "zxb",
        "科创板": "kcb",
    }
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "XGSG_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "purchasedate,securitycode",
        "sr": "-1",
        "p": "1",
        "ps": "3000",
        "js": "var qnnaUGTA={pages:(tp),data:(x)}",
        "rt": "53355447",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") :])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.columns = [
        "_",
        "_",
        "股票简称",
        "股票代码",
        "申购代码",
        "发行总数",
        "网上发行",
        "申购上限",
        "_",
        "发行价格",
        "申购日期",
        "中签号公布日",
        "上市日期",
        "发行市盈率",
        "中签率",
        "询价累计报价倍数",
        "板块",
        "_",
        "_",
        "顶格申购需配市值",
        "_",
        "连续一字板数量",
        "涨幅",
        "_",
        "每中一签获利",
        "配售对象报价家数",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "最新价",
        "_",
        "_",
        "_",
        "行业市盈率",
        "首日收盘价",
        "中签缴款日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "申购代码",
            "发行总数",
            "网上发行",
            "顶格申购需配市值",
            "申购上限",
            "发行价格",
            "最新价",
            "首日收盘价",
            "申购日期",
            "中签号公布日",
            "中签缴款日期",
            "上市日期",
            "发行市盈率",
            "行业市盈率",
            "中签率",
            "询价累计报价倍数",
            "配售对象报价家数",
            "连续一字板数量",
            "涨幅",
            "每中一签获利",
            "板块",
        ]
    ]
    temp_df = temp_df[temp_df["板块"] == market_map[market]]
    del temp_df["板块"]
    return temp_df


if __name__ == "__main__":
    stock_em_dxsyl_df = stock_em_dxsyl(market="上海主板")
    print(stock_em_dxsyl_df)

    stock_em_xgsglb_df = stock_em_xgsglb(market="科创板")
    print(stock_em_xgsglb_df)
