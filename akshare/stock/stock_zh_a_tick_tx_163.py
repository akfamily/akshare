#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/10/22 11:08
Desc: 腾讯-网易-股票-实时行情-成交明细
成交明细-每个交易日 16:00 提供当日数据
港股报价延时 15 分钟
"""
from io import StringIO, BytesIO
from tqdm import tqdm

import pandas as pd
import requests
import warnings


def stock_zh_a_tick_tx_js(symbol: str = "sz000001") -> pd.DataFrame:
    """
    腾讯财经-历史分笔数据
    http://gu.qq.com/sz300494/gp/detail
    :param symbol: 股票代码
    :type symbol: str
    :return: 股票代码
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page = 0
    warnings.warn("正在下载数据，请稍等")
    while True:
        try:
            url = "http://stock.gtimg.cn/data/index.php"
            params = {
                "appn": "detail",
                "action": "data",
                "c": symbol,
                "p": page,
            }
            r = requests.get(url, params=params)
            text_data = r.text
            temp_df = (
                pd.DataFrame(eval(text_data[text_data.find("[") :])[1].split("|"))
                .iloc[:, 0]
                .str.split("/", expand=True)
            )
            page += 1
            big_df = pd.concat([big_df, temp_df], ignore_index=True)

        except:
            break
    if not big_df.empty:
        big_df = big_df.iloc[:, 1:]
        big_df.columns = ["成交时间", "成交价格", "价格变动", "成交量", "成交金额", "性质"]
        big_df.reset_index(drop=True, inplace=True)
        property_map = {
            "S": "卖盘",
            "B": "买盘",
            "M": "中性盘",
        }
        big_df["性质"] = big_df["性质"].map(property_map)
        big_df = big_df.astype({
            '成交时间': str,
            '成交价格': float,
            '价格变动': float,
            '成交量': int,
            '成交金额': int,
            '性质': str,
        })
    return big_df


def stock_zh_a_tick_tx(
    symbol: str = "sz000001", trade_date: str = "20210316"
) -> pd.DataFrame:
    """
    http://gu.qq.com/sz000001/gp/detail
    成交明细-每个交易日 16:00 提供当日数据
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    url = "http://stock.gtimg.cn/data/index.php"
    params = {
        "appn": "detail",
        "action": "download",
        "c": symbol,
        "d": trade_date,
    }
    r = requests.get(url, params=params)
    r.encoding = "gbk"
    temp_df = pd.read_table(StringIO(r.text))
    return temp_df


def stock_zh_a_tick_163(
    symbol: str = "sz000001", trade_date: str = "20220429"
) -> pd.DataFrame:
    """
    成交明细-每个交易日 22:00 提供当日数据; 该接口目前还不支持北交所的股票
    http://quotes.money.163.com/trade/cjmx_000001.html#01b05
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    name_code_map = {"sh": "0", "sz": "1"}
    url = f"http://quotes.money.163.com/cjmx/{trade_date[:4]}/{trade_date}/{name_code_map[symbol[:2]]}{symbol[2:]}.xls"
    r = requests.get(url)
    r.encoding = "utf-8"
    temp_df = pd.read_excel(BytesIO(r.content), engine="xlrd")
    temp_df.columns = [
        "时间",
        "成交价",
        "价格变动",
        "成交量",
        "成交额",
        "性质",
    ]
    temp_df['成交价'] = pd.to_numeric(temp_df['成交价'])
    temp_df['价格变动'] = pd.to_numeric(temp_df['价格变动'])
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'])
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'])
    return temp_df


def stock_zh_a_tick_163_now(symbol: str = "000001") -> pd.DataFrame:
    """
    成交明细-收盘后获取, 补充 stock_zh_a_tick_163 接口, 用来尽快获取数据
    http://quotes.money.163.com/trade/cjmx_000001.html#01b05
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    time_list_one = [
        item.isoformat().split("T")[1]
        for item in pd.date_range("09:30:00", "11:30:00", freq="5min").tolist()
    ][1:]
    time_list_two = [
        item.isoformat().split("T")[1]
        for item in pd.date_range("13:00:00", "15:00:00", freq="5min").tolist()
    ][1:]
    time_list_one.extend(time_list_two)
    big_df = pd.DataFrame()
    for item in tqdm(time_list_one):
        url = "http://quotes.money.163.com/service/zhubi_ajax.html"
        params = {"symbol": symbol, "end": item}
        r = requests.get(url, params=params)
        data_json = r.json()
        if not data_json['zhubi_list']:
            break
        temp_df = pd.DataFrame(data_json["zhubi_list"])
        del temp_df["_id"]
        del temp_df["TRADE_TYPE"]
        del temp_df["DATE"]
        temp_df.reset_index(inplace=True)
        temp_df.sort_values(
            by="index", ascending=False, ignore_index=True, inplace=True
        )
        big_df = pd.concat([big_df,temp_df], ignore_index=True)

    del big_df["index"]
    big_df.columns = [
        "_",
        "成交量",
        "成交价",
        "成交额",
        "价格变动",
        "成交时间",
        "性质",
    ]
    big_df = big_df[
        [
            "成交时间",
            "成交价",
            "价格变动",
            "成交量",
            "成交额",
            "性质",
        ]
    ]
    big_df["成交量"] = big_df["成交量"] / 100
    return big_df


if __name__ == "__main__":
    stock_zh_a_tick_163_df = stock_zh_a_tick_163(symbol="sz000001", trade_date="20220427")
    print(stock_zh_a_tick_163_df)

    stock_zh_a_tick_tx_js_df = stock_zh_a_tick_tx_js(symbol="sz000001")
    print(stock_zh_a_tick_tx_js_df)

    stock_zh_a_tick_tx_df = stock_zh_a_tick_tx(symbol="sh600848", trade_date="20210514")
    print(stock_zh_a_tick_tx_df)

    date_list = pd.date_range(start="20210601", end="20210613").tolist()
    date_list = [item.strftime("%Y%m%d") for item in date_list]
    for item in date_list:
        print(item)
        data = stock_zh_a_tick_tx(symbol="sh601699", trade_date=f"{item}")
        if not data.empty:
            print(data)

    stock_zh_a_tick_163_now_df = stock_zh_a_tick_163_now(symbol="000001")
    print(stock_zh_a_tick_163_now_df)
