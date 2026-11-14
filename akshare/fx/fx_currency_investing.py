#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/6/26 15:33
Desc: 英为财情-外汇-货币对历史数据
https://cn.investing.com/currencies/
https://cn.investing.com/currencies/eur-usd-historical-data
"""

import pandas as pd
from bs4 import BeautifulSoup

from akshare.exceptions import InvalidParameterError
from akshare.utils import http
from akshare.utils.tqdm import get_tqdm


def fx_pair_map_investing(symbol: str = "美元") -> pd.DataFrame:
    """
    指定货币的所有可获取货币对的数据
    https://cn.investing.com/currencies/cny-jmd
    :param symbol: 指定货币
    :type symbol: str
    :return: 指定货币的所有可获取货币对的数据
    :rtype: pandas.DataFrame
    """
    region_code = []
    region_name = []
    # 英为财情按 TLS 指纹拦截程序访问，requests 与 Chrome 指纹均返回 403，
    # 因此经 curl_cffi 以 Safari 指纹请求，且不自行设置 User-Agent
    headers = {
        "Referer": "https://cn.investing.com/currencies/single-currency-crosses",
        "X-Requested-With": "XMLHttpRequest",
    }

    def has_data_sml_id_but_no_id(tag):
        return tag.has_attr("data-sml-id") and not tag.has_attr("title")

    tqdm = get_tqdm()
    for region_id in tqdm(["4", "1", "8", "7", "6"], leave=False):
        url = "https://cn.investing.com/currencies/Service/region"
        params = {"region_ID": region_id, "currency_ID": "false"}

        r = http.curl_get(url, params=params, headers=headers, impersonate="safari")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, features="lxml")
        region_code.extend(
            [
                item["continentid"] + "-" + region_id
                for item in soup.find_all(has_data_sml_id_but_no_id)
            ]
        )
        region_name.extend(
            [item.find("i").text for item in soup.find_all(has_data_sml_id_but_no_id)]
        )

    name_id_map = dict(zip(region_name, region_code))
    if symbol not in name_id_map:
        raise InvalidParameterError(
            f"英为财情没有币种 {symbol}，请使用网页上的中文币种名称，如 人民币、美元"
        )
    url = "https://cn.investing.com/currencies/Service/currency"
    params = {
        "region_ID": name_id_map[symbol].split("-")[1],
        "currency_ID": name_id_map[symbol].split("-")[0],
    }
    r = http.curl_get(url, params=params, headers=headers, impersonate="safari")
    r.raise_for_status()
    soup = BeautifulSoup(r.text, features="lxml")

    temp_code = [item["href"].split("/")[-1] for item in soup.find_all("a")]  # need
    temp_name = [item["title"].replace(" ", "-") for item in soup.find_all("a")]
    temp_df = pd.DataFrame(data=[temp_name, temp_code], index=["name", "code"]).T
    return temp_df


if __name__ == "__main__":
    fx_pair_map_investing_df = fx_pair_map_investing(symbol="人民币")
    print(fx_pair_map_investing_df)
