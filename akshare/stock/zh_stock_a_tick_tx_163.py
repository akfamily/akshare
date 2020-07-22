# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/16 20:39
Desc: 腾讯-股票-实时行情-成交明细
下载成交明细-每个交易日16:00提供当日数据
该列表港股报价延时15分钟
"""
from io import StringIO, BytesIO

import pandas as pd
import requests


def stock_zh_a_tick_tx_js(code: str = "sz000001"):
    big_df = pd.DataFrame()
    page = 0
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
            temp_df = (
                pd.DataFrame(eval(text_data[text_data.find("[") :])[1].split("|"))
                .iloc[:, 0]
                .str.split("/", expand=True)
            )
            page += 1
            big_df = big_df.append(temp_df)
        except:
            break
    if not big_df.empty:
        big_df = big_df.iloc[:, 1:]
        big_df.columns = ["成交时间", "成交价", "价格变动", "成交量（手）", "成交额（元）", "性质"]
    return big_df


def stock_zh_a_tick_tx(
    code: str = "sh600848", trade_date: str = "20191011"
) -> pd.DataFrame:
    """
    http://gu.qq.com/sz000001/gp/detail
    成交明细-每个交易日16:00提供当日数据
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
    res = requests.get(url, params=params)
    res.encoding = "gbk"
    temp_df = pd.read_table(StringIO(res.text))
    return temp_df


def stock_zh_a_tick_163(
    code: str = "sh600848", trade_date: str = "20200410"
) -> pd.DataFrame:
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
    res = requests.get(url)
    res.encoding = "utf-8"
    try:
        temp_df = pd.read_excel(BytesIO(res.content))
        return temp_df
    except:
        return print("无当前交易日数据，请稍后再试")


if __name__ == "__main__":
    date_list = pd.date_range(start="20190801", end="20191111").tolist()
    date_list = pd.date_range(start="20200425", end="20200428").tolist()
    date_list = [item.strftime("%Y%m%d") for item in date_list]
    for item in date_list:
        print(item)
        data = stock_zh_a_tick_tx(code="sz000001", trade_date=f"{item}")
        if not data.empty:
            print(data)
    stock_zh_a_tick_163_df = stock_zh_a_tick_163(code="sh600848", trade_date="20200428")
    print(stock_zh_a_tick_163_df)

    stock_zh_a_tick_tx_js_df = stock_zh_a_tick_tx_js(code="sz000001")
    print(stock_zh_a_tick_tx_js_df)
