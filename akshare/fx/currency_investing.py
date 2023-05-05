#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/8/8 20:33
Desc: 英为财情-外汇-货币对历史数据
https://cn.investing.com/currencies/
https://cn.investing.com/currencies/eur-usd-historical-data
"""
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.index.cons import short_headers


def _currency_name_url() -> dict:
    """
    货币键值对
    :return: 货币键值对
    :rtype: dict
    """
    url = "https://cn.investing.com/currencies/"
    res = requests.post(url, headers=short_headers)
    data_table = pd.read_html(res.text)[0].iloc[:, 1:]  # 实时货币行情
    data_table.columns = ["中文名称", "英文名称", "最新", "最高", "最低", "涨跌额", "涨跌幅", "时间"]
    name_code_dict = dict(
        zip(
            data_table["中文名称"].tolist(),
            [
                item.lower().replace("/", "-")
                for item in data_table["英文名称"].tolist()
            ],
        )
    )
    return name_code_dict


def currency_hist_area_index_name_code(symbol: str = "usd-jpy") -> dict:
    """
    指定 symbol 的所有指数和代码
    https://cn.investing.com/indices/
    :param symbol: 指定的国家或地区；ak._get_global_country_name_url() 函数返回的国家或地区的名称
    :type symbol: str
    :return: 指定 area 的所有指数和代码
    :rtype: dict
    """
    pd.set_option("mode.chained_assignment", None)
    url = f"https://cn.investing.com/currencies/{symbol}-historical-data"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("script", attrs={"id": "__NEXT_DATA__"}).text
    data_json = json.loads(data_text)
    code = json.loads(data_json["props"]["pageProps"]["state"])["dataStore"][
        "pageInfoStore"
    ]["identifiers"]["instrument_id"]
    return code


def currency_hist(
    symbol: str = "usd-jpy",
    period: str = "每日",
    start_date: str = "20030101",
    end_date: str = "20220808",
) -> pd.DataFrame:
    """
    外汇历史数据, 注意获取数据区间的长短, 输入任意货币对, 具体能否获取, 通过 currency_name_code_dict 查询
    https://www.investing.com/
    :param symbol: 货币对
    :type symbol: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: 日期
    :type start_date: str
    :param end_date: 日期
    :type end_date: str
    :return: 货币对历史数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    code = currency_hist_area_index_name_code(symbol)
    url = f"https://api.investing.com/api/financialdata/historical/{code}"
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    params = {
        "start-date": start_date,
        "end-date": end_date,
        "time-frame": period_map[period],
        "add-missing-rows": "false",
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "domain-id": "cn",
        "origin": "https://cn.investing.com",
        "pragma": "no-cache",
        "referer": "https://cn.investing.com/",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": '"?0"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    df_data = pd.DataFrame(data_json["data"])
    df_data.columns = [
        "-",
        "-",
        "-",
        "日期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "交易量",
        "-",
        "收盘",
        "开盘",
        "高",
        "低",
        "涨跌幅",
    ]
    df_data = df_data[["日期", "收盘", "开盘", "高", "低", "交易量", "涨跌幅"]]
    df_data["日期"] = pd.to_datetime(df_data["日期"]).dt.date
    df_data["收盘"] = pd.to_numeric(df_data["收盘"])
    df_data["开盘"] = pd.to_numeric(df_data["开盘"])
    df_data["高"] = pd.to_numeric(df_data["高"])
    df_data["低"] = pd.to_numeric(df_data["低"])
    df_data["交易量"] = pd.to_numeric(df_data["交易量"])
    df_data["涨跌幅"] = pd.to_numeric(df_data["涨跌幅"])
    df_data.sort_values("日期", inplace=True)
    df_data.reset_index(inplace=True, drop=True)
    return df_data


def _currency_single() -> pd.DataFrame:
    """
    英为财情-外汇-单种货币兑换汇率-单种货币列表
    :return: 单种货币列表
    :rtype: pandas.DataFrame
    """
    url = "https://cn.investing.com/currencies/single-currency-crosses"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    name_url_option_list = soup.find(
        "select", attrs={"class": "newInput selectBox"}
    ).find_all("option")
    temp_df = pd.DataFrame(
        [item.get_text().split("-", 1) for item in name_url_option_list]
    )
    temp_df.columns = ["short_name", "name"]
    temp_df["short_name"] = temp_df["short_name"].str.strip()
    temp_df["name"] = temp_df["name"].str.strip()
    temp_df["code"] = [item["value"] for item in name_url_option_list]
    return temp_df


def currency_name_code(symbol: str = "usd/jpy") -> pd.DataFrame:
    """
    当前所有可兑换货币对
    :param symbol: "usd/jpy"
    :type symbol: str
    :return: 中英文货币对
    :rtype: pandas.DataFrame
                  name     code
    0        欧元/美元  eur-usd
    1        英镑/美元  gbp-usd
    2        美元/日元  usd-jpy
    3      美元/瑞士法郎  usd-chf
    4     澳大利亚元/美元  aud-usd
    ..         ...      ...
    268    日元/新加坡元  jpy-sgd
    269  科威特第纳尔/日元  kwd-jpy
    270  日元/白俄罗斯卢布  jpy-byn
    271  日元/乌克兰赫里纳  jpy-uah
    272   日元/土耳其里拉  jpy-try
    """
    symbol = symbol.upper()
    currency_df = _currency_single()
    url = "https://cn.investing.com/currencies/Service/ChangeCurrency"
    params = {
        "session_uniq_id": "53bee677662a2336ec07b40738753fc1",
        "currencies": currency_df[
            currency_df["short_name"] == symbol.split("/")[0]
        ]["code"].values[0],
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "cn.investing.com",
        "Pragma": "no-cache",
        "Referer": "https://cn.investing.com/currencies/single-currency-crosses",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.read_html(r.json()["HTML"])[0].iloc[:, 1:]
    temp_df.rename(columns={"名称.1": "简称"}, inplace=True)
    temp_df["pids"] = [item[:-1] for item in r.json()["pids"]]
    name_code_dict_one = dict(
        zip(
            temp_df["名称"].tolist(),
            [
                item.lower().replace("/", "-")
                for item in temp_df["简称"].tolist()
            ],
        )
    )
    params = {
        "session_uniq_id": "53bee677662a2336ec07b40738753fc1",
        "currencies": currency_df[
            currency_df["short_name"] == symbol.split("/")[1]
        ]["code"].values[0],
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "cn.investing.com",
        "Pragma": "no-cache",
        "Referer": "https://cn.investing.com/currencies/single-currency-crosses",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.read_html(r.json()["HTML"])[0].iloc[:, 1:]
    temp_df.rename(columns={"名称.1": "简称"}, inplace=True)
    temp_df["pids"] = [item[:-1] for item in r.json()["pids"]]
    name_code_dict_two = dict(
        zip(
            temp_df["名称"].tolist(),
            [
                item.lower().replace("/", "-")
                for item in temp_df["简称"].tolist()
            ],
        )
    )
    name_code_dict_one.update(name_code_dict_two)
    temp_df = pd.DataFrame.from_dict(
        name_code_dict_one, orient="index"
    ).reset_index()
    temp_df.columns = ["name", "code"]
    return temp_df


def currency_pair_map(symbol: str = "美元") -> pd.DataFrame:
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

    def has_data_sml_id_but_no_id(tag):
        return tag.has_attr("data-sml-id") and not tag.has_attr("title")

    for region_id in tqdm(["4", "1", "8", "7", "6"], leave=False):
        url = "https://cn.investing.com/currencies/Service/region"
        params = {"region_ID": region_id, "currency_ID": "false"}
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "cn.investing.com",
            "Pragma": "no-cache",
            "Referer": "https://cn.investing.com/currencies/single-currency-crosses",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        r = requests.get(url, params=params, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        region_code.extend(
            [
                item["continentid"] + "-" + region_id
                for item in soup.find_all(has_data_sml_id_but_no_id)
            ]
        )
        region_name.extend(
            [
                item.find("i").text
                for item in soup.find_all(has_data_sml_id_but_no_id)
            ]
        )

    name_id_map = dict(zip(region_name, region_code))
    url = "https://cn.investing.com/currencies/Service/currency"
    params = {
        "region_ID": name_id_map[symbol].split("-")[1],
        "currency_ID": name_id_map[symbol].split("-")[0],
    }
    r = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    temp_code = [
        item["href"].split("/")[-1] for item in soup.find_all("a")
    ]  # need
    temp_name = [
        item["title"].replace(" ", "-") for item in soup.find_all("a")
    ]
    temp_df = pd.DataFrame([temp_name, temp_code], index=["name", "code"]).T
    return temp_df


if __name__ == "__main__":
    currency_hist_area_index_name_code_df = currency_hist_area_index_name_code(
        symbol="usd-jpy"
    )
    print(currency_hist_area_index_name_code_df)

    currency_pair_map_df = currency_pair_map(symbol="人民币")
    print(currency_pair_map_df)

    currency_name_code_df = currency_name_code(symbol="cny/dkk")
    print(currency_name_code_df)

    currency_hist_df = currency_hist(
        symbol="usd-jpy",
        period="每日",
        start_date="20050101",
        end_date="20220808",
    )
    print(currency_hist_df)
