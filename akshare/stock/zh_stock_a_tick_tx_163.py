# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/6/14 11:08
Desc: 腾讯-网易-股票-实时行情-成交明细
成交明细-每个交易日 16:00 提供当日数据
港股报价延时 15 分钟
"""
from io import StringIO, BytesIO
from tqdm import tqdm

import pandas as pd
import requests
import warnings


def stock_zh_a_tick_tx_js(code: str = "sz000001") -> pd.DataFrame:
    """
    腾讯财经-历史分笔数据
    http://gu.qq.com/sz300494/gp/detail
    :param code: 股票代码
    :type code: str
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
                "c": code,
                "p": page,
            }
            r = requests.get(url, params=params)
            text_data = r.text
            temp_df = pd.DataFrame(eval(text_data[text_data.find("["):])[1].split("|")).iloc[:, 0].str.split("/", expand=True)
            page += 1
            big_df = big_df.append(temp_df)
        except:
            break
    if not big_df.empty:
        big_df = big_df.iloc[:, 1:]
        big_df.columns = ["成交时间", "成交价", "价格变动", "成交量", "成交额", "性质"]
    return big_df


def stock_zh_a_tick_tx(code: str = "sz000001", trade_date: str = "20210610") -> pd.DataFrame:
    """
    http://gu.qq.com/sz000001/gp/detail
    成交明细-每个交易日 16:00 提供当日数据
    :param code: 带市场标识的股票代码
    :type code: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    url = "http://stock.gtimg.cn/data/index.php"
    params = {
        "appn": "detail",
        "action": "download",
        "c": code,
        "d": trade_date,
    }
    r = requests.get(url, params=params)
    r.encoding = "gbk"
    temp_df = pd.read_table(StringIO(r.text))
    return temp_df


def stock_zh_a_tick_163(code: str = "sz002352", trade_date: str = "20210608") -> pd.DataFrame:
    """
    成交明细-每个交易日 22:00 提供当日数据
    http://quotes.money.163.com/trade/cjmx_000001.html#01b05
    :param code: 带市场标识的股票代码
    :type code: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    name_code_map = {"sh": "0", "sz": 1}
    url = f"http://quotes.money.163.com/cjmx/{trade_date[:4]}/{trade_date}/{name_code_map[code[:2]]}{code[2:]}.xls"
    r = requests.get(url)
    r.encoding = "utf-8"
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df.columns = [
        "成交时间",
        "成交价",
        "价格变动",
        "成交量",
        "成交额",
        "性质",
    ]
    return temp_df


def stock_zh_a_tick_163_now(code: str = "000001") -> pd.DataFrame:
    """
    成交明细-收盘后获取, 补充 stock_zh_a_tick_163 接口, 用来尽快获取数据
    http://quotes.money.163.com/trade/cjmx_000001.html#01b05
    :param code: 带市场标识的股票代码
    :type code: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    time_list_one = [item.isoformat().split("T")[1] for item in pd.date_range('09:30:00', '11:30:00', freq='5min').tolist()][1:]
    time_list_two = [item.isoformat().split("T")[1] for item in pd.date_range('13:00:00', '15:00:00', freq='5min').tolist()][1:]
    time_list_one.extend(time_list_two)
    big_df = pd.DataFrame()
    for item in tqdm(time_list_one):
        url = "http://quotes.money.163.com/service/zhubi_ajax.html"
        params = {
            "symbol": code,
            "end": item
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["zhubi_list"])
        del temp_df["_id"]
        del temp_df["TRADE_TYPE"]
        del temp_df["DATE"]
        temp_df.reset_index(inplace=True)
        temp_df.sort_values(by="index", ascending=False, ignore_index=True, inplace=True)
        big_df = big_df.append(temp_df)
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
    big_df = big_df[[
        "成交时间",
        "成交价",
        "价格变动",
        "成交量",
        "成交额",
        "性质",
    ]]
    big_df["成交量"] = big_df["成交量"] / 100
    return big_df


if __name__ == "__main__":
    stock_zh_a_tick_163_df = stock_zh_a_tick_163(code="sz002352", trade_date="20210608")
    print(stock_zh_a_tick_163_df)

    stock_zh_a_tick_tx_js_df = stock_zh_a_tick_tx_js(code="sz000001")
    print(stock_zh_a_tick_tx_js_df)

    date_list = pd.date_range(start="20210601", end="20210613").tolist()
    date_list = [item.strftime("%Y%m%d") for item in date_list]
    for item in date_list:
        print(item)
        data = stock_zh_a_tick_tx(code="sh601699", trade_date=f"{item}")
        if not data.empty:
            print(data)

    stock_zh_a_tick_163_now_df = stock_zh_a_tick_163_now(code="000001")
    print(stock_zh_a_tick_163_now_df)
