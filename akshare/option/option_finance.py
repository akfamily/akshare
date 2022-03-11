#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/1/26 10:58
Desc: 金融期权数据
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
    CFFEX_OPTION_URL_300,
)


def option_finance_underlying(symbol: str = "50ETF") -> pd.DataFrame:
    """
    期权标的当日行情, 目前只有 华夏上证 50 ETF, 华泰柏瑞沪深 300 ETF 两个产品
    http://www.sse.com.cn/assortment/options/price/
    :param symbol: 50ETF 或 300ETF
    :type symbol: str
    :return: 期权标的当日行情
    :rtype: pandas.DataFrame
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


def option_finance_board(symbol: str = "嘉实沪深300ETF期权", end_month: str = "2103") -> pd.DataFrame:
    """
    期权的当日具体的行情数据, 主要为三个: 华夏上证50ETF期权, 华泰柏瑞沪深300ETF期权, 嘉实沪深300ETF期权, 沪深300股指期权
    http://www.sse.com.cn/assortment/options/price/
    http://www.szse.cn/market/product/option/index.html
    http://www.cffex.com.cn/hs300gzqq/
    :param symbol: 华夏上证50ETF期权 or 华泰柏瑞沪深300ETF期权 or 嘉实沪深300ETF期权 or 沪深300股指期权
    :type symbol: str
    :param end_month: 2003; 2020年3月到期的期权
    :type end_month: str
    :return: 当日行情
    :rtype: pandas.DataFrame
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
        url = "http://www.szse.cn/api/report/ShowReport/data"
        params = {
            "SHOWTYPE": "JSON",
            "CATALOGID": "ysplbrb",
            "TABKEY": "tab1",
            "PAGENO": "1",
            "random": "0.10642298535346595",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        page_num = data_json[0]["metadata"]["pagecount"]
        big_df = pd.DataFrame()
        for page in range(1, page_num+1):
            params = {
                "SHOWTYPE": "JSON",
                "CATALOGID": "ysplbrb",
                "TABKEY": "tab1",
                "PAGENO": page,
                "random": "0.10642298535346595",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json[0]["data"])
            big_df = big_df.append(temp_df, ignore_index=True)
        big_df.columns = [
            "合约编码",
            "合约简称",
            "标的名称",
            "类型",
            "行权价",
            "合约单位",
            "期权行权日",
            "行权交收日",
        ]
        big_df["期权行权日"] = pd.to_datetime(big_df["期权行权日"])
        big_df["end_month"] = big_df["期权行权日"].dt.month.astype(str).str.zfill(2)
        big_df = big_df[big_df["end_month"] == end_month]
        del big_df["end_month"]
        return big_df
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

    option_finance_board_df = option_finance_board(symbol="华夏上证50ETF期权", end_month="2003")
    print(option_finance_board_df)

    option_finance_board_df = option_finance_board(symbol="嘉实沪深300ETF期权", end_month="2103")
    print(option_finance_board_df)

    option_finance_board_df = option_finance_board(symbol="华泰柏瑞沪深300ETF期权", end_month="2103")
    print(option_finance_board_df.info())

    option_finance_board_df = option_finance_board(symbol="沪深300股指期权", end_month="2003")
    print(option_finance_board_df)
