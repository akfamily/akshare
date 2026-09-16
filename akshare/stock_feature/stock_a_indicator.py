#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/30 20:24
Desc: 市盈率，市净率和股息率查询
https://www.legulegu.com/stocklist
https://www.legulegu.com/s/000001
"""

from datetime import datetime
from hashlib import md5

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.exceptions import APIError, DataParsingError
from akshare.utils.cons import headers


def get_cookie_csrf(url: str = "") -> dict:
    """
    从乐咕乐股页面取出 CSRF 令牌与 cookie，供该数据源的各接口带在后续请求上
    https://legulegu.com/stockdata/shanghaiPE
    :param url: 乐咕乐股的页面地址
    :type url: str
    :return: 含 cookies 与 headers 两个键，可直接展开传给 requests
    :rtype: dict
    :raises APIError: 上游返回非 2xx（被拒绝时为 nginx 403）或请求本身失败
    :raises DataParsingError: 页面取回成功但其中没有 _csrf 标签
    """
    # 创建独立的 session，避免污染全局状态
    session = requests.Session()
    session.headers.update(headers)
    # 必须先校验状态码：上游拒绝请求时返回的 nginx 403 错误页里没有 _csrf 标签，
    # 若直接交给下面的解析流程，就会在 None 上取 .attrs，而抛出的
    # AttributeError: 'NoneType' object has no attribute 'attrs' 既不含状态码
    # 也不提上游，用户无从判断是自己被挡了。同一报错自 2024 年起已复发多次，
    # 见 #4680、#7237、#7417。
    try:
        r = session.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise APIError(
            f"legulegu 请求失败，请确认该站点在当前网络下可正常访问：{err}",
            status_code=getattr(err.response, "status_code", None),
        ) from err
    soup = BeautifulSoup(r.text, features="lxml")
    csrf_tag = soup.find(name="meta", attrs={"name": "_csrf"})
    # 状态码正常却没有令牌，通常是上游改版或返回了 200 的拦截页。
    if csrf_tag is None:
        raise DataParsingError(
            f"legulegu 页面中未找到 _csrf 令牌，上游可能已改版或拦截了本次请求：{url}"
        )
    csrf_token = csrf_tag.attrs["content"]
    # 创建新的 headers
    local_headers = headers.copy()
    local_headers.update({"X-CSRF-Token": csrf_token})
    return {"cookies": r.cookies, "headers": local_headers}


def get_token_lg() -> str:
    """
    生成乐咕的 token
    https://legulegu.com/s/002488
    :return: token
    :rtype: str
    """
    current_date_str = datetime.now().date().isoformat()
    obj = md5()
    obj.update(current_date_str.encode("utf-8"))
    token = obj.hexdigest()
    return token


def stock_hk_indicator_eniu(
    symbol: str = "hk01093", indicator: str = "市盈率"
) -> pd.DataFrame:
    """
    亿牛网-港股指标
    https://eniu.com/gu/hk01093/roe
    :param symbol: 港股代码
    :type symbol: str
    :param indicator: 需要获取的指标，choice of {"港股", "市盈率", "市净率", "股息率", "ROE", "市值"}
    :type indicator: str
    :return: 指定 symbol 和 indicator 的数据
    :rtype: pandas.DataFrame
    """
    if indicator == "港股":
        url = "https://eniu.com/static/data/stock_list.json"
        r = requests.get(url, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df = temp_df[temp_df["stock_id"].str.contains("hk")]
        temp_df.reset_index(inplace=True, drop=True)
        return temp_df
    if indicator == "市盈率":
        url = f"https://eniu.com/chart/peh/{symbol}"
    elif indicator == "市净率":
        url = f"https://eniu.com/chart/pbh/{symbol}"
    elif indicator == "股息率":
        url = f"https://eniu.com/chart/dvh/{symbol}"
    elif indicator == "ROE":
        url = f"https://eniu.com/chart/roeh/{symbol}"
    else:
        url = f"https://eniu.com/chart/marketvalueh/{symbol}"
    r = requests.get(url, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    return temp_df


if __name__ == "__main__":
    stock_hk_indicator_eniu_df = stock_hk_indicator_eniu(
        symbol="hk01093", indicator="市盈率"
    )
    print(stock_hk_indicator_eniu_df)
