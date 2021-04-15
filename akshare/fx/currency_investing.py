# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/9 14:56
Desc: 英为财情-外汇-货币对历史数据
https://cn.investing.com/currencies/
https://cn.investing.com/currencies/eur-usd-historical-data
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.index.cons import short_headers, long_headers


def _currency_name_url() -> dict:
    """
    货币键值对
    :return: 货币键值对
    :rtype: dict
    """
    url = "https://hk.investing.com/currencies/"
    r = requests.get(url, headers=short_headers)
    data_table = pd.read_html(r.text)[0].iloc[:, 1:]  # 实时货币行情
    data_table.columns = ["中文名称", "英文名称", "最新", "最高", "最低", "涨跌额", "涨跌幅", "时间"]
    name_code_dict = dict(
        zip(
            data_table["中文名称"].tolist(),
            [item.lower().replace("/", "-") for item in data_table["英文名称"].tolist()],
        )
    )
    return name_code_dict


def currency_hist(
    symbol: str = "usd-jpy", start_date: str = "20030101", end_date: str = "20200717"
) -> pd.DataFrame:
    """
    外汇历史数据, 注意获取数据区间的长短, 输入任意货币对, 具体能否获取, 通过 currency_name_code_dict 查询
    :param symbol: 货币对
    :type symbol: str
    :param start_date: 日期
    :type start_date: str
    :param end_date: 日期
    :type end_date: str
    :return: 货币对历史数据
    :rtype: pandas.DataFrame
    """
    start_date = "/".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "/".join([end_date[:4], end_date[4:6], end_date[6:]])
    temp_url = f"https://hk.investing.com/currencies/{symbol.lower().replace('/', '-')}-historical-data"
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find_all(text=re.compile("window.histDataExcessInfo"))[0].strip()
    para_data = re.findall(r"\d+", data)
    payload = {
        "curr_id": para_data[0],
        "smlID": para_data[1],
        "header": title,
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    url = "https://hk.investing.com/instruments/HistoricalDataAjax"
    res = requests.post(url, data=payload, headers=long_headers)
    soup = BeautifulSoup(res.text, "lxml")
    # vest_list = [item.get_text().strip() for item in soup.find_all("tr")]
    vest_list = [
        item.get_text().strip().replace(" ", "\n").split("\n")
        for item in soup.find_all("tr")
    ]
    # vest_list = [item.get_text().strip().split("\n") for item in soup.find_all("tr")]
    raw_df = pd.DataFrame(vest_list)
    df_data = pd.DataFrame(vest_list, columns=raw_df.iloc[0, :].tolist()).iloc[1:-1, :]
    df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    if '成交量' in df_data.columns:
        df_data.columns = [
            '日期',
            '收盘',
            '开盘',
            '高',
            '低',
            '交易量',
            '涨跌幅',
            '_',
            '_',
            '_',
        ]
    else:
        df_data.columns = [
            '日期',
            '收盘',
            '开盘',
            '高',
            '低',
            '涨跌幅',
            '_',
            '_',
            '_',
            '_',
        ]
    df_data["涨跌幅"] = pd.DataFrame(
        round(
            df_data["涨跌幅"].str.replace(",", "").str.replace("%", "").astype(float)
            / 100,
            6,
        )
    )

    if "交易量" in df_data.columns:
        if any(df_data["交易量"].astype(str).str.contains("-")):
            df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][
                df_data["交易量"].str.contains("-")
            ].replace("-", 0)

        if any(df_data["交易量"].astype(str).str.contains("B")):
            df_data["交易量"] = (
                df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)]
                .str.replace("B", "")
                .str.replace(",", "")
                .astype(float)
                * 1000000000
            )
        if any(df_data["交易量"].astype(str).str.contains("M")):
            df_data["交易量"] = (
                df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)]
                .str.replace("M", "")
                .str.replace(",", "")
                .astype(float)
                * 1000000
            )
        if any(df_data["交易量"].astype(str).str.contains("K")):
            df_data["交易量"] = (
                df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)]
                .str.replace("K", "")
                .str.replace(",", "")
                .astype(float)
                * 1000
            )
        # df_data["交易量"] = df_data["交易量"].astype(float)

    del df_data["日期"]
    try:
        df_data.iloc[:, :-1] = df_data.iloc[:, :-1].applymap(
            lambda x: x.replace(",", "")
        )
    except:
        pass
    df_data = df_data.astype(float)
    df_data.dropna(how="all", axis=1, inplace=True)
    return df_data


def _currency_single() -> pd.DataFrame:
    """
    英为财情-外汇-单种货币兑换汇率-单种货币列表
    :return: 单种货币列表
    :rtype: pandas.DataFrame
    """
    url = "https://hk.investing.com/currencies/single-currency-crosses"
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
    url = "https://hk.investing.com/currencies/Service/ChangeCurrency"
    params = {
        "session_uniq_id": "53bee677662a2336ec07b40738753fc1",
        "currencies": currency_df[currency_df["short_name"] == symbol.split("/")[0]][
            "code"
        ].values[0],
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "hk.investing.com",
        "Pragma": "no-cache",
        "Referer": "https://hk.investing.com/currencies/single-currency-crosses",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.read_html(r.json()["HTML"])[0].iloc[:, 1:]
    temp_df.rename(columns={"名稱.1": "简称"}, inplace=True)
    temp_df["pids"] = [item[:-1] for item in r.json()["pids"]]
    name_code_dict_one = dict(
        zip(
            temp_df["名稱"].tolist(),
            [item.lower().replace("/", "-") for item in temp_df["貨幣對"].tolist()],
        )
    )
    params = {
        "session_uniq_id": "53bee677662a2336ec07b40738753fc1",
        "currencies": currency_df[currency_df["short_name"] == symbol.split("/")[1]][
            "code"
        ].values[0],
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "hk.investing.com",
        "Pragma": "no-cache",
        "Referer": "https://hk.investing.com/currencies/single-currency-crosses",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.read_html(r.json()["HTML"])[0].iloc[:, 1:]
    temp_df.rename(columns={"名稱.1": "简称"}, inplace=True)
    temp_df["pids"] = [item[:-1] for item in r.json()["pids"]]
    name_code_dict_two = dict(
        zip(
            temp_df["名稱"].tolist(),
            [item.lower().replace("/", "-") for item in temp_df["貨幣對"].tolist()],
        )
    )
    name_code_dict_one.update(name_code_dict_two)
    temp_df = pd.DataFrame.from_dict(name_code_dict_one, orient="index").reset_index()
    temp_df.columns = ["name", "code"]
    return temp_df


def currency_pair_map(symbol: str = "人民币") -> pd.DataFrame:
    """
    指定货币的所有可获取货币对的数据
    https://hk.investing.com/currencies/cny-jmd
    :param symbol: 指定货币
    :type symbol: str
    :return: 指定货币的所有可获取货币对的数据
    :rtype: pandas.DataFrame
    """
    region_code = []
    region_name = []
    from zhconv import convert
    symbol = convert(symbol, 'zh-hk')

    def has_data_sml_id_but_no_id(tag):
        return tag.has_attr("data-sml-id") and not tag.has_attr("title")

    for region_id in tqdm(["4", "1", "8", "7", "6"]):
        url = "https://hk.investing.com/currencies/Service/region"
        params = {"region_ID": region_id, "currency_ID": "false"}
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "hk.investing.com",
            "Pragma": "no-cache",
            "Referer": "https://hk.investing.com/currencies/single-currency-crosses",
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
            [item.find("i").text for item in soup.find_all(has_data_sml_id_but_no_id)]
        )

    name_id_map = dict(zip(region_name, region_code))
    url = "https://hk.investing.com/currencies/Service/currency"
    params = {
        "region_ID": name_id_map[symbol].split("-")[1],
        "currency_ID": name_id_map[symbol].split("-")[0],
    }
    r = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    temp_code = [item["href"].split("/")[-1] for item in soup.find_all("a")]  # need
    temp_name = [item["title"].replace(" ", "-") for item in soup.find_all("a")]
    temp_df = pd.DataFrame([temp_name, temp_code], index=["name", "code"]).T
    return temp_df


if __name__ == "__main__":
    currency_pair_map_df = currency_pair_map(symbol="澳大利亚元")
    print(currency_pair_map_df)

    currency_name_code_df = currency_name_code(symbol="usd/jpy")
    print(currency_name_code_df)

    currency_hist_df = currency_hist(
        symbol="us-dollar-index", start_date="20050907", end_date="20201125"
    )
    print(currency_hist_df)

    currency_hist_df = currency_hist(
        symbol="usd-jpy", start_date="20050907", end_date="20201125"
    )
    print(currency_hist_df)

    for i_item in currency_pair_map_df["code"].to_list():
        print(i_item)
        currency_hist_df = currency_hist(
            symbol=i_item, start_date="20000101", end_date="20201109"
        )
        print(currency_hist_df)
