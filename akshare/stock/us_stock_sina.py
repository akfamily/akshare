# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/8/27 12:47
Desc: 新浪财经-美股实时行情数据和历史行情数据
http://finance.sina.com.cn/stock/usstock/sector.shtml
"""
import json

import execjs
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.stock.cons import (
    js_hash_text,
    zh_js_decode,
    us_sina_stock_list_url,
    us_sina_stock_dict_payload,
    us_sina_stock_hist_qfq_url,
)


def get_us_page_count() -> int:
    """
    新浪财经-美股-总页数
    :return: 美股总页数
    :rtype: int
    """
    page = "1"
    us_js_decode = f"US_CategoryService.getList?page={page}&num=20&sort=&asc=0&market=&id="
    js_code = execjs.compile(js_hash_text)
    dict_list = js_code.call("d", us_js_decode)  # 执行js解密代码
    us_sina_stock_dict_payload.update({"page": "{}".format(page)})
    res = requests.get(
        us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload
    )
    data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
    if not isinstance(int(data_json["count"]) / 20, int):
        page_count = int(int(data_json["count"]) / 20) + 1
    else:
        page_count = int(int(data_json["count"]) / 20)
    return page_count


def get_us_stock_name() -> pd.DataFrame:
    """
    u.s. stock's english name, chinese name and symbol
    you should use symbol to get apply into the next function
    :return: stock's english name, chinese name and symbol
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_us_page_count()
    for page in tqdm(range(1, page_count + 1)):
        # page = "1"
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(
            page
        )
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call("d", us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        res = requests.get(
            us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload
        )
        data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df[["name", "cname", "symbol"]]


def stock_us_spot() -> pd.DataFrame:
    """
    新浪财经-所有美股的数据, 注意延迟 15 分钟
    :return: 美股所有股票实时行情
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_us_page_count()
    for page in tqdm(range(1, page_count + 1)):
        # page = "1"
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(
            page
        )
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call("d", us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        res = requests.get(
            us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload
        )
        data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df


def stock_us_daily(symbol: str = "AAPL", adjust: str = "") -> pd.DataFrame:
    """
    新浪财经-美股-个股的历史行情数据
    :param symbol: 可以使用 get_us_stock_name 获取
    :type symbol: str
    :param adjust: "": 返回未复权的数据 ; qfq: 返回前复权后的数据; qfq-factor: 返回前复权因子和调整;
    :type adjust: str
    :return: 指定 adjust 的数据
    :rtype: pandas.DataFrame
    """
    res = requests.get(f"https://finance.sina.com.cn/staticdata/us/{symbol}")
    js_code = execjs.compile(zh_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df = data_df.astype("float")
    res = requests.get(us_sina_stock_hist_qfq_url.format(symbol))
    qfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])["data"])
    qfq_factor_df.rename(columns={"c": "adjust", "d": "date", "f": "qfq_factor", }, inplace=True)
    qfq_factor_df.index = pd.to_datetime(qfq_factor_df["date"])
    del qfq_factor_df["date"]

    # 处理复权因子
    temp_date_range = pd.date_range("1900-01-01", qfq_factor_df.index[0].isoformat())
    temp_df = pd.DataFrame(range(len(temp_date_range)), temp_date_range)
    new_range = pd.merge(
            temp_df, qfq_factor_df, left_index=True, right_index=True, how="left"
        )
    new_range = new_range.fillna(method="ffill")
    new_range = new_range.iloc[:, [1, 2]]

    if adjust == "qfq":
        if len(new_range) == 1:
            new_range.index.values[0] = pd.to_datetime(str(data_df.index.date[0]))
        temp_df = pd.merge(
            data_df, new_range, left_index=True, right_index=True, how="left"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df.fillna(method="bfill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df["high"] = temp_df["high"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df["close"] = temp_df["close"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df["low"] = temp_df["low"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df = temp_df.apply(lambda x: round(x, 4))
        temp_df = temp_df.astype("float")
        return temp_df.iloc[:, :-2]

    if adjust == "qfq-factor":
        return qfq_factor_df

    if adjust == "":
        return data_df


def stock_us_fundamental(stock="GOOGL", symbol="info"):
    """
    美股财务指标
    https://www.macrotrends.net/stocks/charts/AAPL/apple/pe-ratio
    :return: 指定股票的财务数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.macrotrends.net/stocks/stock-screener"
    r = requests.get(url)
    temp_text = r.text[r.text.find("originalData")+15:r.text.find("filterArray")-8]
    data_json = json.loads(temp_text)
    temp_df = pd.DataFrame(data_json)
    if symbol == "info":
        del temp_df["name_link"]
        return temp_df
    else:
        need_df = temp_df[temp_df["ticker"] == stock]
        soup = BeautifulSoup(need_df["name_link"].values[0], "lxml")
        base_url = "https://www.macrotrends.net" + soup.find("a")["href"]
        if symbol == "PE":
            url = base_url.rsplit("/", maxsplit=1)[0] + "/pe-ratio"
            temp_df = pd.read_html(url)[0]
            temp_df.columns = ["date", "stock_price", "ttm_net_eps", "pe_ratio"]
            return temp_df
        elif symbol == "PB":
            url = base_url.rsplit("/", maxsplit=1)[0] + "/price-book"
            temp_df = pd.read_html(url)[0]
            temp_df.columns = ["date", "stock_price", "book_value_per_share", "price_to_book_ratio"]
            return temp_df


if __name__ == "__main__":
    stock_us_stock_name_df = get_us_stock_name()
    print(stock_us_stock_name_df)
    stock_us_spot_df = stock_us_spot()
    print(stock_us_spot_df)
    stock_us_daily_df = stock_us_daily(symbol="AAPL", adjust="")
    print(stock_us_daily_df)
    stock_us_daily_qfq_df = stock_us_daily(symbol="AAPL", adjust="qfq")
    print(stock_us_daily_qfq_df)
    stock_us_daily_qfq_factor_df = stock_us_daily(symbol="AAPL", adjust="qfq-factor")
    print(stock_us_daily_qfq_factor_df)

    stock_us_fundamental_df = stock_us_fundamental(stock="GOOGL", symbol="PB")
    print(stock_us_fundamental_df)
