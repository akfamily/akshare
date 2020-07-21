# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/9/30 13:58
Desc: 获取金融期权数据
http://www.sse.com.cn/assortment/options/price/
"""
import pandas as pd
import requests

from akshare.option.cons import (
    SH_OPTION_URL_50,
    SH_OPTION_PAYLOAD,
    SH_OPTION_PAYLOAD_OTHER,
    SH_OPTION_URL_KING_50,
    SH_OPTION_URL_300,
    SH_OPTION_URL_KING_300,
    SZ_OPTION_URL_300,
    CFFEX_OPTION_URL_300,
)


def option_finance_underlying(symbol="50ETF"):
    """
    获取期权标的当日行情, 目前只有 华夏上证50ETF, 华泰柏瑞沪深300ETF 两个产品
    http://www.sse.com.cn/assortment/options/price/
    :param symbol: 50ETF 或 300ETF
    :return: pandas.DataFrame
    """
    if symbol == "50ETF":
        res = requests.get(SH_OPTION_URL_50, params=SH_OPTION_PAYLOAD)
        data_json = res.json()
        raw_data = pd.DataFrame(data_json["list"])
        raw_data.at[0, 0] = "510050"
        raw_data.at[0, 8] = pd.to_datetime(
            str(data_json["date"]) + str(data_json["time"]), format="%Y%m%d%H%M%S"
        )
        raw_data.columns = [
            "代码",
            "名称",
            "当前价",
            "涨跌",
            "涨跌幅",
            "振幅",
            "成交量(手)",
            "成交额(万元)",
            "更新日期",
        ]
        return raw_data
    else:
        res = requests.get(SH_OPTION_URL_300, params=SH_OPTION_PAYLOAD)
        data_json = res.json()
        raw_data = pd.DataFrame(data_json["list"])
        raw_data.at[0, 0] = "510300"
        raw_data.at[0, 8] = pd.to_datetime(
            str(data_json["date"]) + str(data_json["time"]), format="%Y%m%d%H%M%S"
        )
        raw_data.columns = [
            "代码",
            "名称",
            "当前价",
            "涨跌",
            "涨跌幅",
            "振幅",
            "成交量(手)",
            "成交额(万元)",
            "更新日期",
        ]
        return raw_data


def option_finance_board(symbol="华泰柏瑞沪深300ETF期权", end_month="2003"):
    """
    获取期权的当日具体的行情数据, 主要为三个: 华夏上证50ETF期权, 华泰柏瑞沪深300ETF期权, 嘉实沪深300ETF期权, 沪深300股指期权
    http://www.sse.com.cn/assortment/options/price/
    http://www.szse.cn/market/derivative/derivative_list/index.html
    http://www.cffex.com.cn/hs300gzqq/
    :param symbol: 华夏上证50ETF期权 or 华泰柏瑞沪深300ETF期权 or 嘉实沪深300ETF期权 or 沪深300股指期权
    :param end_month: 2003 2020年3月到期的期权
    :return: pandas.DataFrame
    """
    end_month = end_month[-2:]
    if symbol == "华夏上证50ETF期权":
        res = requests.get(
            SH_OPTION_URL_KING_50.format(end_month), params=SH_OPTION_PAYLOAD_OTHER
        )
        data_json = res.json()
        raw_data = pd.DataFrame(data_json["list"])
        raw_data.index = [str(data_json["date"]) + str(data_json["time"])] * data_json[
            "total"
        ]
        raw_data.columns = ["合约交易代码", "当前价", "涨跌幅", "前结价", "行权价"]
        raw_data["数量"] = [data_json["total"]] * data_json["total"]
        return raw_data
    elif symbol == "华泰柏瑞沪深300ETF期权":
        res = requests.get(
            SH_OPTION_URL_KING_300.format(end_month), params=SH_OPTION_PAYLOAD_OTHER
        )
        data_json = res.json()
        raw_data = pd.DataFrame(data_json["list"])
        raw_data.index = [str(data_json["date"]) + str(data_json["time"])] * data_json[
            "total"
        ]
        raw_data.columns = ["合约交易代码", "当前价", "涨跌幅", "前结价", "行权价"]
        raw_data["数量"] = [data_json["total"]] * data_json["total"]
        return raw_data
    elif symbol == "嘉实沪深300ETF期权":
        raw_df = pd.read_excel(SZ_OPTION_URL_300)
        raw_df["期权行权日"] = pd.to_datetime(raw_df["期权行权日"])
        raw_df["end_month"] = raw_df["期权行权日"].dt.month.astype(str).str.zfill(2)
        raw_df = raw_df[raw_df["end_month"] == end_month]
        del raw_df["end_month"]
        return raw_df
    elif symbol == "沪深300股指期权":
        raw_df = pd.read_table(CFFEX_OPTION_URL_300, sep=",")
        raw_df["end_month"] = (
            raw_df["instrument"].str.split("-", expand=True).iloc[:, 0].str.slice(4,)
        )
        raw_df = raw_df[raw_df["end_month"] == end_month]
        del raw_df["end_month"]
        return raw_df


if __name__ == "__main__":
    option_finance_underlying_df = option_finance_underlying(symbol="300ETF")
    print(option_finance_underlying_df)
    option_finance_board_df = option_finance_board(symbol="沪深300股指期权", end_month="2003")
    print(option_finance_board_df)
