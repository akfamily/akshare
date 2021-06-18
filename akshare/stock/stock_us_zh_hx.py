# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/19 10:34
Desc: 从和讯网获取美股-中概股实时行情数据和历史行情数据(日)
http://quote.hexun.com/default.html#ustock_0
注意: 由于涉及到复权问题, 建议使用新浪的接口来获取历史行情数据(日)
"""
import json

import requests
import pandas as pd


def stock_us_zh_spot() -> pd.DataFrame:
    """
    美股-中概股的实时行情数据
    http://quote.hexun.com/default.htm#ustock_3
    :return: 中概股的实时行情数据
    :return: pandas.DataFrame
    """
    url = "http://quote.hexun.com/usastock/data/getdjstock.aspx"
    params = {
        "type": "1",
        "market": "3",
        "sorttype": "4",
        "updown": "up",
        "page": "1",
        'count': "200",
        "time": "203450"
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "quote.hexun.com",
        "Pragma": "no-cache",
        "Referer": "http://quote.hexun.com/usastock/xqstock.aspx?market=3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    r = requests.get(url, params=params, headers=headers)
    data_list = eval(r.text.split("=")[1].strip().rsplit(";")[0])  # eval 出列表
    data_df = pd.DataFrame(
        data_list,
        columns=[
            "代码",
            "名称",
            "最新价(美元)",
            "涨跌幅",
            "d_1",
            "d_2",
            "最高",
            "最低",
            "昨收",
            "d_3",
            "成交量",
            "d_4",
        ],
    )
    temp_df = data_df[["代码", "名称", "最新价(美元)", "涨跌幅", "最高", "最低", "昨收", "成交量"]]
    temp_df = temp_df.rename({"最新价(美元)": "最新价"}, axis=1)
    return temp_df


def stock_us_zh_daily(symbol: str = 'BABA') -> pd.DataFrame:
    """
    美股-中概股的日频率历史行情数据
    http://stockdata.stock.hexun.com/us/BABA.shtml
    :return: 中概股的日频率历史行情数据
    :return: pandas.DataFrame
    """
    url = "http://webusstock.hermes.hexun.com/usa/kline"
    params = {
        "code": f"NYSE{symbol}",
        "start": "20201218223000",
        "number": "-1000",
        "type": "5",
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "UM_distinctid=1758d5cddd49c-0fc7e2c2612624-303464-1fa400-1758d5cddd592f; ADVC=38ffe1fbf97465; cn_1263247791_dplus=%7B%22distinct_id%22%3A%20%221758d5cddd49c-0fc7e2c2612624-303464-1fa400-1758d5cddd592f%22%2C%22userFirstDate%22%3A%20%2220201103%22%2C%22userID%22%3A%20%220%22%2C%22userName%22%3A%20%22%22%2C%22userType%22%3A%20%22loginuser%22%2C%22userLoginDate%22%3A%20%2220201103%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201604394498%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201604394498%2C%22initial_view_time%22%3A%20%221604392649%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRaFkqqESxpi2iDV4Q7Men69HaM9QOkW5KKUtQakjQzkfkygaOuGzJBFcHSg35wmfSKFA26xUDad7jHwCCv1ksa%26wd%3D%26eqid%3Da38e871500004846000000065fa11d78%22%2C%22initial_referrer_domain%22%3A%20%22www.baidu.com%22%2C%22%24recent_outside_referrer%22%3A%20%22www.baidu.com%22%7D; HexunTrack=SID=20200722150527074dded739ba5e24fd2915f1f692d4ad9c7&CITY=51&TOWN=510100; ADVS=392342a9ca40f5; ASL=18614,00rzr,abdfc0a27d461d18b68a5530; __jsluid_h=35f649169d5fb027d0e857b8ecd24d5b",
        "Host": "webusstock.hermes.hexun.com",
        "Pragma": "no-cache",
        "Referer": "http://stockdata.stock.hexun.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "X-Requested-With": "ShockwaveFlash/33.0.0.432",
    }
    r = requests.get(url, params=params, headers=headers)
    r.encoding = "utf-8"
    data_dict = json.loads(r.text[1:-2])
    data_df = pd.DataFrame(
        data_dict["Data"][0],
        columns=[list(item.values())[0] for item in data_dict["KLine"]],
    )
    data_df['时间'] = data_df['时间'].astype(str).str.slice(0, 8)
    data_df['前收盘价'] = round(data_df['前收盘价'] / 100, 2)
    data_df['开盘价'] = round(data_df['开盘价'] / 100, 2)
    data_df['收盘价'] = round(data_df['收盘价'] / 100, 2)
    data_df['最高价'] = round(data_df['最高价'] / 100, 2)
    data_df['最低价'] = round(data_df['最低价'] / 100, 2)
    del data_df['成交额']
    return data_df


if __name__ == "__main__":
    stock_us_zh_spot_df = stock_us_zh_spot()
    print(stock_us_zh_spot_df)
    stock_us_zh_daily_df = stock_us_zh_daily(symbol="BABA")
    print(stock_us_zh_daily_df)
