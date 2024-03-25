#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/10/15 18:00
Desc: 同花顺-板块-概念板块
https://q.10jqka.com.cn/gn/detail/code/301558/
"""

from datetime import datetime
from functools import lru_cache
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm

from akshare.datasets import get_ths_js
from akshare.utils import demjson


def stock_board_concept_graph_ths(symbol: str = "通用航空") -> pd.DataFrame:
    """
    同花顺-板块-概念板块-概念图谱
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 板块名称
    :type symbol: str
    :return: 概念图谱
    :rtype: pandas.DataFrame
    """
    stock_board_ths_map_df = stock_board_concept_name_ths()
    symbol = (
        stock_board_ths_map_df[stock_board_ths_map_df["概念名称"] == symbol]["网址"]
        .values[0]
        .split("/")[-2]
    )
    url = f"https://q.10jqka.com.cn/gn/detail/code/{symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    temp_df = pd.read_html(StringIO(r.text))[0]
    new_list = []
    for col in temp_df.columns:
        temp_list = temp_df[col].values[0].split("  ")
        for i, item in enumerate(temp_list):
            if i % 2 != 0:
                price_pct, pct = item.split(" ")
                price_pct = price_pct.strip("%").strip("+").strip("-")
                pct = pct.strip("-").strip("+")
                new_list.append([col, temp_list[i - 1], price_pct, pct])
    temp_df = pd.DataFrame(new_list, columns=["产业链", "名称", "涨跌幅", "现价"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["现价"] = pd.to_numeric(temp_df["现价"], errors="coerce")
    return temp_df


def _get_file_content_ths(file: str = "ths.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_ths_js(file)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


@lru_cache()
def stock_board_concept_name_ths() -> pd.DataFrame:
    """
    同花顺-板块-概念板块-概念
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :return: 所有概念板块的名称和链接
    :rtype: pandas.DataFrame
    """
    url = "https://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/1/ajax/1/"
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": f"v={v_code}",
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    total_page = soup.find(name="span", attrs={"class": "page_info"}).text.split("/")[1]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1), leave=False):
        url = f"https://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/{page}/ajax/1/"
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call("v")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.90 Safari/537.36",
            "Cookie": f"v={v_code}",
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, features="lxml")
        url_list = []
        for item in (
            soup.find(name="table", attrs={"class": "m-table m-pager-table"})
            .find("tbody")
            .find_all("tr")
        ):
            inner_url = item.find_all("td")[1].find("a")["href"]
            url_list.append(inner_url)
        temp_df = pd.read_html(StringIO(r.text))[0]
        temp_df["网址"] = url_list
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df = big_df[["日期", "概念名称", "成分股数量", "网址"]]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["成分股数量"] = pd.to_numeric(big_df["成分股数量"], errors="coerce")
    big_df["代码"] = big_df["网址"].str.split("/", expand=True).iloc[:, 6]
    big_df.drop_duplicates(keep="last", inplace=True)
    big_df.reset_index(inplace=True, drop=True)

    # 处理遗漏的板块
    url = "https://q.10jqka.com.cn/gn/detail/code/301558/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    need_list = [
        item.find_all("a") for item in soup.find_all(attrs={"class": "cate_group"})
    ]
    temp_list = []
    for item in need_list:
        temp_list.extend(item)
    temp_df = pd.DataFrame(
        [
            [item.text for item in temp_list],
            [item["href"] for item in temp_list],
        ]
    ).T
    temp_df.columns = ["概念名称", "网址"]
    temp_df["日期"] = None
    temp_df["成分股数量"] = None
    temp_df["代码"] = temp_df["网址"].str.split("/", expand=True).iloc[:, 6].tolist()
    temp_df = temp_df[["日期", "概念名称", "成分股数量", "网址", "代码"]]
    big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(subset=["概念名称"], keep="first", inplace=True)
    return big_df


def _stock_board_concept_code_ths() -> dict:
    """
    同花顺-板块-概念板块-概念
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :return: 所有概念板块的名称和链接
    :rtype: pandas.DataFrame
    """
    _stock_board_concept_name_ths_df = stock_board_concept_name_ths()
    name_list = _stock_board_concept_name_ths_df["概念名称"].tolist()
    url_list = [
        item.split("/")[-2]
        for item in _stock_board_concept_name_ths_df["网址"].tolist()
    ]
    temp_map = dict(zip(name_list, url_list))
    return temp_map


def stock_board_concept_cons_ths(symbol: str = "小米概念") -> pd.DataFrame:
    """
    同花顺-板块-概念板块-成份股
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 板块名称
    :type symbol: str
    :return: 成份股
    :rtype: pandas.DataFrame
    """
    stock_board_ths_map_df = stock_board_concept_name_ths()
    symbol = (
        stock_board_ths_map_df[stock_board_ths_map_df["概念名称"] == symbol]["网址"]
        .values[0]
        .split("/")[-2]
    )
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": f"v={v_code}",
    }
    url = f"https://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/1/ajax/1/code/{symbol}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    try:
        page_num = int(
            soup.find_all(name="a", attrs={"class": "changePage"})[-1]["page"]
        )
    except IndexError:
        page_num = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        v_code = js_code.call("v")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.90 Safari/537.36",
            "Cookie": f"v={v_code}",
        }
        url = f"https://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{page}/ajax/1/code/{symbol}"
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(StringIO(r.text))[0]
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.rename(
        mapper={
            "涨跌幅(%)": "涨跌幅",
            "涨速(%)": "涨速",
            "换手(%)": "换手",
            "振幅(%)": "振幅",
        },
        inplace=True,
        axis=1,
    )
    del big_df["加自选"]
    big_df["代码"] = big_df["代码"].astype(str).str.zfill(6)
    big_df = big_df[big_df["代码"] != "暂无成份股数据"]
    return big_df


def stock_board_concept_info_ths(symbol: str = "阿里巴巴概念") -> pd.DataFrame:
    """
    同花顺-板块-概念板块-板块简介
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 板块简介
    :type symbol: str
    :return: 板块简介
    :rtype: pandas.DataFrame
    """
    stock_board_ths_map_df = stock_board_concept_name_ths()
    symbol_code = (
        stock_board_ths_map_df[stock_board_ths_map_df["概念名称"] == symbol]["网址"]
        .values[0]
        .split("/")[-2]
    )
    url = f"https://q.10jqka.com.cn/gn/detail/code/{symbol_code}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    name_list = [
        item.text
        for item in soup.find(name="div", attrs={"class": "board-infos"}).find_all("dt")
    ]
    value_list = [
        item.text.strip().replace("\n", "/")
        for item in soup.find(name="div", attrs={"class": "board-infos"}).find_all("dd")
    ]
    temp_df = pd.DataFrame([name_list, value_list]).T
    temp_df.columns = ["项目", "值"]
    return temp_df


def stock_board_concept_hist_ths(
    start_year: str = "2000", symbol: str = "安防"
) -> pd.DataFrame:
    """
    同花顺-板块-概念板块-指数数据
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :param start_year: 开始年份; e.g., 2019
    :type start_year: str
    :param symbol: 板块简介
    :type symbol: str
    :return: 板块简介
    :rtype: pandas.DataFrame
    """
    code_map = _stock_board_concept_code_ths()
    symbol_url = f"https://q.10jqka.com.cn/gn/detail/code/{code_map[symbol]}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(symbol_url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    symbol_code = soup.find("div", attrs={"class": "board-hq"}).find("span").text
    big_df = pd.DataFrame()
    current_year = datetime.now().year
    for year in tqdm(range(int(start_year), current_year + 1), leave=False):
        url = f"https://d.10jqka.com.cn/v4/line/bk_{symbol_code}/01/{year}.js"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.90 Safari/537.36",
            "Referer": "https://q.10jqka.com.cn",
            "Host": "d.10jqka.com.cn",
        }
        r = requests.get(url, headers=headers)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find("{") : -1])
        except:  # noqa: E722
            continue
        temp_df = demjson.decode(data_text[data_text.find("{") : -1])
        temp_df = pd.DataFrame(temp_df["data"].split(";"))
        temp_df = temp_df.iloc[:, 0].str.split(",", expand=True)
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    if big_df.columns.shape[0] == 12:
        big_df.columns = [
            "日期",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "成交量",
            "成交额",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
    else:
        big_df.columns = [
            "日期",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "成交量",
            "成交额",
            "_",
            "_",
            "_",
            "_",
        ]
    big_df = big_df[
        [
            "日期",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "成交量",
            "成交额",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["开盘价"] = pd.to_numeric(big_df["开盘价"], errors="coerce")
    big_df["最高价"] = pd.to_numeric(big_df["最高价"], errors="coerce")
    big_df["最低价"] = pd.to_numeric(big_df["最低价"], errors="coerce")
    big_df["收盘价"] = pd.to_numeric(big_df["收盘价"], errors="coerce")
    big_df["成交量"] = pd.to_numeric(big_df["成交量"], errors="coerce")
    big_df["成交额"] = pd.to_numeric(big_df["成交额"], errors="coerce")
    return big_df


def stock_board_cons_ths(symbol: str = "301558") -> pd.DataFrame:
    """
    通过输入行业板块或者概念板块的代码获取成份股
    https://q.10jqka.com.cn/thshy/detail/code/881121/
    https://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 行业板块或者概念板块的代码
    :type symbol: str
    :return: 行业板块或者概念板块的成份股
    :rtype: pandas.DataFrame
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": f"v={v_code}",
    }
    url = f"https://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/1/ajax/1/code/{symbol}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    url_flag = "thshy"
    if soup.find("td", attrs={"colspan": "14"}):
        url = f"https://q.10jqka.com.cn/gn/detail/field/199112/order/desc/page/1/ajax/1/code/{symbol}"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        url_flag = "gn"
    try:
        page_num = int(soup.find_all("a", attrs={"class": "changePage"})[-1]["page"])
    except IndexError:
        page_num = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        v_code = js_code.call("v")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.90 Safari/537.36",
            "Cookie": f"v={v_code}",
        }
        url = f"https://q.10jqka.com.cn/{url_flag}/detail/field/199112/order/desc/page/{page}/ajax/1/code/{symbol}"
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(StringIO(r.text))[0]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.rename(
        {
            "涨跌幅(%)": "涨跌幅",
            "涨速(%)": "涨速",
            "换手(%)": "换手",
            "振幅(%)": "振幅",
        },
        inplace=True,
        axis=1,
    )
    del big_df["加自选"]
    big_df["代码"] = big_df["代码"].astype(str).str.zfill(6)
    return big_df


if __name__ == "__main__":
    stock_board_concept_graph_ths_df = stock_board_concept_graph_ths(symbol="通用航空")
    print(stock_board_concept_graph_ths_df)

    stock_board_concept_name_ths_df = stock_board_concept_name_ths()
    print(stock_board_concept_name_ths_df)

    stock_board_concept_cons_ths_df = stock_board_concept_cons_ths(symbol="小米概念")
    print(stock_board_concept_cons_ths_df)

    stock_board_concept_info_ths_df = stock_board_concept_info_ths(symbol="PVDF概念")
    print(stock_board_concept_info_ths_df)

    stock_board_concept_hist_ths_df = stock_board_concept_hist_ths(
        start_year="2024", symbol="新能源汽车"
    )
    print(stock_board_concept_hist_ths_df)

    stock_board_cons_ths_df = stock_board_cons_ths(symbol="881121")
    print(stock_board_cons_ths_df)
