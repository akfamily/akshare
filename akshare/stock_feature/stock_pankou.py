#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/20 21:39
Desc: 东方财富-行情中心-盘口异动
http://quote.eastmoney.com/changes/
"""
import pandas as pd
import requests


def stock_changes_em(symbol: str = "大笔买入") -> pd.DataFrame:
    """
    东方财富-行情中心-盘口异动
    http://quote.eastmoney.com/changes/
    :param symbol: choice of {'火箭发射', '快速反弹', '大笔买入', '封涨停板', '打开跌停板', '有大买盘', '竞价上涨', '高开5日线', '向上缺口', '60日新高', '60日大幅上涨', '加速下跌', '高台跳水', '大笔卖出', '封跌停板', '打开涨停板', '有大卖盘', '竞价下跌', '低开5日线', '向下缺口', '60日新低', '60日大幅下跌'}
    :type symbol: str
    :return: 盘口异动
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getAllStockChanges"
    symbol_map = {
        "火箭发射": "8201",
        "快速反弹": "8202",
        "大笔买入": "8193",
        "封涨停板": "4",
        "打开跌停板": "32",
        "有大买盘": "64",
        "竞价上涨": "8207",
        "高开5日线": "8209",
        "向上缺口": "8211",
        "60日新高": "8213",
        "60日大幅上涨": "8215",
        "加速下跌": "8204",
        "高台跳水": "8203",
        "大笔卖出": "8194",
        "封跌停板": "8",
        "打开涨停板": "16",
        "有大卖盘": "128",
        "竞价下跌": "8208",
        "低开5日线": "8210",
        "向下缺口": "8212",
        "60日新低": "8214",
        "60日大幅下跌": "8216",
    }
    reversed_symbol_map = {v: k for k, v in symbol_map.items()}
    params = {
        "type": symbol_map[symbol],
        "pageindex": "0",
        "pagesize": "5000",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wzchanges",
        "_": "1624005264245",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["allstock"])
    temp_df["tm"] = pd.to_datetime(temp_df["tm"], format="%H%M%S").dt.time
    temp_df.columns = [
        "时间",
        "代码",
        "_",
        "名称",
        "板块",
        "相关信息",
    ]
    temp_df = temp_df[
        [
            "时间",
            "代码",
            "名称",
            "板块",
            "相关信息",
        ]
    ]
    temp_df["板块"] = temp_df["板块"].astype(str)
    temp_df["板块"] = temp_df["板块"].map(reversed_symbol_map)
    return temp_df


if __name__ == "__main__":
    stock_changes_em_df = stock_changes_em(symbol='火箭发射')
    print(stock_changes_em_df)

    for item in {'火箭发射', '快速反弹', '大笔买入', '封涨停板', '打开跌停板', '有大买盘', '竞价上涨', '高开5日线', '向上缺口', '60日新高', '60日大幅上涨', '加速下跌', '高台跳水', '大笔卖出', '封跌停板', '打开涨停板', '有大卖盘', '竞价下跌', '低开5日线', '向下缺口', '60日新低', '60日大幅下跌'}:
        stock_changes_em_df = stock_changes_em(symbol=item)
        print(stock_changes_em_df)
