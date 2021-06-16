# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/6/15 22:26
Desc: 东方财富网-行情首页-上证A股-每日行情
"""
import requests
import pandas as pd


def stock_zh_a_spot_em():
    """
    东方财富-股票和市场代码
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 股票和市场代码
    :rtype: dict
    """
    url = "http://35.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.columns = ["_",
                       "最新价",
                       "涨跌幅",
                       "涨跌额",
                       "成交量",
                       "成交额",
                       "振幅",
                       "换手率",
                       "市盈率-动态",
                       "量比",
                       "_",
                       "代码",
                       "_",
                       "名称",
                       "最高",
                       "最低",
                       "今开",
                       "昨收",
                       "_",
                       "_",
                       "_",
                       "市净率",
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
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.rename(columns={'index': "序号"}, inplace=True)
    temp_df = temp_df[[
        "序号",
        "代码",
        "名称",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "最高",
        "最低",
        "今开",
        "昨收",
        "量比",
        "换手率",
        "市盈率-动态",
        "市净率",
    ]]
    return temp_df


def _code_id_map():
    """
    东方财富-股票和市场代码
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 股票和市场代码
    :rtype: dict
    """
    url = "http://35.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:1 t:2,m:1 t:23",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df["market_id"] = 1
    temp_df.columns = ["sh_code", "sh_id"]
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df["sz_code"] = pd.DataFrame(data_json["data"]["diff"])
    temp_df["sz_id"] = 0
    code_id_dict = dict(zip(temp_df["sh_code"], temp_df["sh_id"]))
    code_id_dict.update(dict(zip(temp_df["sz_code"], temp_df["sz_id"])))
    return code_id_dict


def stock_zh_a_hist(
    symbol: str = "601568",
    start_date: str = "20210601",
    end_date: str = "20210616",
    adjust: str = "",
) -> pd.DataFrame:
    """
    东方财富网-行情首页-上证A股-每日行情
    http://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "1", "hfq": "2", "": "不复权"}
    :type adjust: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    code_id_dict = _code_id_map()
    adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "klt": "101",
        "fqt": adjust_dict[adjust],
        "secid": f"{code_id_dict[symbol]}.{symbol}",
        "beg": "0",
        "end": "20500000",
        "_": "1623766962675",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = [
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "振幅",
        "涨跌幅",
        "涨跌额",
        "换手率",
    ]
    temp_df.index = pd.to_datetime(temp_df["日期"])
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(inplace=True, drop=True)
    temp_df = temp_df.astype(
        {
            "开盘": float,
            "收盘": float,
            "最高": float,
            "最低": float,
            "成交量": int,
            "成交额": float,
            "振幅": float,
            "涨跌幅": float,
            "涨跌额": float,
            "换手率": float,
        }
    )
    return temp_df


if __name__ == "__main__":
    stock_zh_a_spot_em_df = stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)

    stock_zh_a_hist_df = stock_zh_a_hist(
        symbol="603777", start_date="20210301", end_date="20210616", adjust="hfq"
    )
    print(stock_zh_a_hist_df)
