#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/1/14 17:00
Desc: 新浪财经-美股实时行情数据和历史行情数据
https://finance.sina.com.cn/stock/usstock/sector.shtml
"""

import ast
import json
import math
from functools import lru_cache

import pandas as pd
import py_mini_racer
from tqdm import tqdm

from akshare.stock.cons import (
    js_hash_text,
    zh_js_decode,
    us_sina_stock_list_url,
    us_sina_stock_dict_payload,
    us_sina_stock_hist_qfq_url,
)
from akshare.exceptions import APIError
from akshare.utils import http


def _us_list_error(response) -> bool:
    """
    判断新浪美股列表接口是否返回了错误；新浪偶发以 200 状态码返回后端数据库错误，
    如 {"__ERROR":"HY000","__ERRORMSG":"... MySQL server has gone away"}，重试同一页即可恢复
    :param response: 响应对象
    :type response: requests.Response
    :return: 是否为错误响应
    :rtype: bool
    """
    return '"__ERROR"' in response.text or '"data"' not in response.text


def _us_list_page(js_code, page: int) -> dict:
    """
    新浪财经-美股-列表的单页数据，遇到新浪偶发的后端错误时重试
    https://finance.sina.com.cn/stock/usstock/sector.shtml
    :param js_code: 已加载签名脚本的 JS 引擎
    :type js_code: py_mini_racer.MiniRacer
    :param page: 页码，从 1 开始
    :type page: int
    :return: 上游返回的 JSON，含 count（股票总数）与 data（当页数据）
    :rtype: dict
    :raises APIError: 重试后仍返回错误
    """
    us_js_decode = (
        f"US_CategoryService.getList?page={page}&num=20&sort=&asc=0&market=&id="
    )
    dict_list = js_code.call("d", us_js_decode)  # 执行 js 解密代码
    params = dict(us_sina_stock_dict_payload, page=str(page))
    res = http.request_with_retry(
        "GET",
        us_sina_stock_list_url.format(dict_list),
        params=params,
        retry_if=_us_list_error,
    )
    text = res.text[res.text.find("({") + 1 : res.text.rfind(");")]
    try:
        data_json = json.loads(text)
    except ValueError:
        data_json = {}
    if "data" not in data_json:
        raise APIError(
            f"新浪财经美股列表第 {page} 页重试后仍返回错误："
            f"{data_json.get('__ERRORMSG') or res.text[:200]}",
            status_code=res.status_code,
        )
    return data_json


def _us_list_js_code():
    """
    创建加载了新浪签名脚本的 JS 引擎，翻页时复用同一个实例
    :return: JS 引擎
    :rtype: py_mini_racer.MiniRacer
    """
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(js_hash_text)
    return js_code


@lru_cache()
def __get_us_page_count() -> int:
    """
    新浪财经-美股-总页数
    https://finance.sina.com.cn/stock/usstock/sector.shtml
    :return: 美股总页数
    :rtype: int
    """
    data_json = _us_list_page(_us_list_js_code(), 1)
    return math.ceil(int(data_json["count"]) / 20)


def _us_list_all() -> pd.DataFrame:
    """
    新浪财经-美股-列表的全部数据
    https://finance.sina.com.cn/stock/usstock/sector.shtml
    :return: 全部美股的列表数据
    :rtype: pandas.DataFrame
    """
    js_code = _us_list_js_code()
    frames = [
        pd.DataFrame(_us_list_page(js_code, page)["data"])
        for page in tqdm(range(1, __get_us_page_count() + 1), leave=False)
    ]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def stock_us_name_sina() -> pd.DataFrame:
    """
    u.s. stock's english name, chinese name and symbol
    you should use symbol to get apply into the next function
    https://finance.sina.com.cn/stock/usstock/sector.shtml
    :return: stock's english name, chinese name and symbol
    :rtype: pandas.DataFrame
    """
    big_df = _us_list_all()
    return big_df[["name", "cname", "symbol"]]


def stock_us_spot_sina() -> pd.DataFrame:
    """
    新浪财经-所有美股的数据，注意延迟 15 分钟
    https://finance.sina.com.cn/stock/usstock/sector.shtml
    :return: 美股所有股票实时行情
    :rtype: pandas.DataFrame
    """
    return _us_list_all()


def stock_us_daily_sina(symbol: str = "FB", adjust: str = "") -> pd.DataFrame:
    """
    新浪财经-美股
    https://finance.sina.com.cn/stock/usstock/sector.shtml
    备注：
    1. CIEN 新浪复权因子错误
    2. AI 新浪复权因子错误，该股票刚上市未发生复权，但是返回复权因子
    :param symbol: 可以使用 stock_us_name_sina 获取
    :type symbol: str
    :param adjust: "": 返回未复权的数据 ; qfq: 返回前复权后的数据；qfq-factor: 返回前复权因子和调整；
    :type adjust: str
    :return: 指定 adjust 的数据
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/staticdata/us/{symbol}"
    res = http.get(url)
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(zh_js_decode)
    dict_list = js_code.call("d", res.text.split("=")[1].split(";")[0].replace('"', ""))
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["amount"]
    del data_df["date"]
    data_df = data_df.astype("float")
    url = us_sina_stock_hist_qfq_url.format(symbol)
    res = http.get(url)
    qfq_factor_df = pd.DataFrame(
        ast.literal_eval(res.text.split("=")[1].split("\n")[0])["data"]
    )
    qfq_factor_df = qfq_factor_df.rename(
        columns={
            "c": "adjust",
            "d": "date",
            "f": "qfq_factor",
        },
    )
    qfq_factor_df.index = pd.to_datetime(qfq_factor_df["date"])
    del qfq_factor_df["date"]

    # 处理复权因子
    temp_date_range = pd.date_range("1900-01-01", qfq_factor_df.index[0].isoformat())
    temp_df = pd.DataFrame(range(len(temp_date_range)), temp_date_range)
    new_range = pd.merge(
        temp_df, qfq_factor_df, left_index=True, right_index=True, how="left"
    )
    new_range = new_range.ffill()
    new_range = new_range.iloc[:, [1, 2]]

    if adjust == "qfq":
        if len(new_range) == 1:
            new_range.index = [pd.to_datetime(str(data_df.index.date[0]))]
        temp_df = pd.merge(
            data_df, new_range, left_index=True, right_index=True, how="left"
        )
        temp_df = temp_df.ffill()
        temp_df = temp_df.bfill()

        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df["high"] = temp_df["high"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df["close"] = temp_df["close"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df["low"] = temp_df["low"] * temp_df["qfq_factor"] + temp_df["adjust"]
        temp_df = temp_df.apply(lambda x: round(x, 4))
        temp_df = temp_df.astype("float")
        # 处理复权因子错误的情况-开始
        check_df = temp_df[["open", "high", "low", "close"]].copy()
        check_df = check_df.dropna()
        if check_df.empty:
            data_df = data_df.reset_index()
            return data_df
        # 处理复权因子错误的情况-结束
        result_data = temp_df.iloc[:, :-2]
        result_data = result_data.reset_index()
        return result_data

    if adjust == "qfq-factor":
        qfq_factor_df = qfq_factor_df.reset_index()
        return qfq_factor_df

    if adjust == "":
        data_df = data_df.reset_index()
        return data_df


if __name__ == "__main__":
    stock_us_stock_name_df = stock_us_name_sina()
    print(stock_us_stock_name_df)

    stock_us_spot_sina_df = stock_us_spot_sina()
    print(stock_us_spot_sina_df)

    stock_us_daily_sina_df = stock_us_daily_sina(symbol=".DJI", adjust="")
    print(stock_us_daily_sina_df)

    stock_us_daily_qfq_df = stock_us_daily_sina(symbol="WOLF", adjust="qfq")
    print(stock_us_daily_qfq_df)

    stock_us_daily_qfq_factor_df = stock_us_daily_sina(
        symbol="AAPL", adjust="qfq-factor"
    )
    print(stock_us_daily_qfq_factor_df)
