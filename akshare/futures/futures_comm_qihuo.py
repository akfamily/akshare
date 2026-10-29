#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/11 17:00
Desc: 九期网-期货手续费
https://www.9qihuo.com/qihuoshouxufei
"""

from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup

from akshare.exceptions import APIError, DataParsingError, RateLimitError
from akshare.utils import http

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.9qihuo.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


def _futures_comm_qihuo_page() -> str:
    """
    取回九期网期货手续费页面
    https://www.9qihuo.com/qihuoshouxufei
    :return: 页面 HTML
    :rtype: str
    :raises RateLimitError: 上游返回 429，访问过于频繁
    :raises APIError: 上游返回其他非 2xx 状态码
    """
    # 该站点限流较严：先访问首页取得 Cookie，再取手续费页，整个接口只发这两个请求。
    # 早先每处理一个交易所就重新取一次页面，symbol="所有" 时共发 14 个请求，
    # 自身就会触发 429，而 429 页面里没有表格，最终报出与限流无关的
    # ValueError: No tables found 或 AttributeError: 'NoneType' object has no attribute 'previous'
    session = http.Session()
    session.get("https://www.9qihuo.com/", headers=_HEADERS, timeout=10)
    r = session.get(
        "https://www.9qihuo.com/qihuoshouxufei", headers=_HEADERS, timeout=10
    )
    if r.status_code == 429:
        raise RateLimitError("9qihuo 返回 429，访问过于频繁，请稍后再试")
    if not r.ok:
        raise APIError("9qihuo 请求失败", status_code=r.status_code)
    return r.text


def _futures_comm_qihuo_update_time(html: str) -> tuple:
    """
    从页面中解析手续费与价格的更新时间
    :param html: 页面 HTML
    :type html: str
    :return: 由手续费更新时间与价格更新时间组成的二元组
    :rtype: tuple
    :raises DataParsingError: 页面中没有更新时间
    """
    soup = BeautifulSoup(html, features="lxml")
    dlink = soup.find(name="a", attrs={"id": "dlink"})
    if dlink is None:
        raise DataParsingError("9qihuo 页面中未找到更新时间，上游可能已改版")
    raw_date_text = dlink.previous
    comm_update_time = raw_date_text.split("，")[0].strip("（手续费更新时间：")
    price_update_time = (
        raw_date_text.split("，")[1].strip("价格更新时间：").strip("。）")
    )
    return comm_update_time, price_update_time


def _futures_comm_qihuo_process(
    df: pd.DataFrame, name: str, update_time: tuple
) -> pd.DataFrame:
    """
    期货手续费数据细节处理函数
    https://www.9qihuo.com/qihuoshouxufei
    :param df: 获取到的 pandas.DataFrame 数据
    :type df: pandas.DataFrame
    :param name: 交易所名称
    :type name: str
    :param update_time: 由手续费更新时间与价格更新时间组成的二元组
    :type update_time: tuple
    :return: 处理后的数据
    :rtype: pandas.DataFrame
    """
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    common_temp_df = df.copy()
    common_temp_df["合约名称"] = (
        common_temp_df["合约品种"].str.split("(", expand=True).iloc[:, 0].str.strip()
    )
    common_temp_df["合约代码"] = (
        common_temp_df["合约品种"].str.split("(", expand=True).iloc[:, 1].str.strip(")")
    )
    common_temp_df["涨停板"] = (
        common_temp_df["涨/跌停板"].str.split("/", expand=True).iloc[:, 0].str.strip()
    )
    common_temp_df["跌停板"] = (
        common_temp_df["涨/跌停板"].str.split("/", expand=True).iloc[:, 1].str.strip()
    )
    common_temp_df["保证金-买开"] = common_temp_df["保证金-买开"].str.strip("%")
    common_temp_df["保证金-卖开"] = common_temp_df["保证金-卖开"].str.strip("%")
    common_temp_df["保证金-每手"] = common_temp_df["保证金-保证金/每手"].str.strip("元")
    common_temp_df["手续费"] = common_temp_df["手续费(开+平)"].str.strip("元")
    try:
        temp_df_ratio = (
            common_temp_df["手续费标准-开仓"][
                common_temp_df["手续费标准-开仓"].str.contains("万分之")
            ]
            .str.split("/", expand=True)
            .iloc[:, 0]
            .astype(float)
            / 10000
        )
    except IndexError:
        temp_df_ratio = pd.NA
    temp_df_yuan = common_temp_df["手续费标准-开仓"][
        common_temp_df["手续费标准-开仓"].str.contains("元")
    ]
    common_temp_df["手续费标准-开仓-万分之"] = temp_df_ratio
    common_temp_df["手续费标准-开仓-元"] = temp_df_yuan.str.strip("元")
    try:
        temp_df_ratio = (
            common_temp_df["手续费标准-平昨"][
                common_temp_df["手续费标准-平昨"].str.contains("万分之")
            ]
            .str.split("/", expand=True)
            .iloc[:, 0]
            .astype(float)
            / 10000
        )
    except IndexError:
        temp_df_ratio = pd.NA
    temp_df_yuan = common_temp_df["手续费标准-平昨"][
        common_temp_df["手续费标准-平昨"].str.contains("元")
    ]
    common_temp_df["手续费标准-平昨-万分之"] = temp_df_ratio
    common_temp_df["手续费标准-平昨-元"] = temp_df_yuan.str.strip("元")
    try:
        temp_df_ratio = (
            common_temp_df["手续费标准-平今"][
                common_temp_df["手续费标准-平今"].str.contains("万分之")
            ]
            .str.split("/", expand=True)
            .iloc[:, 0]
            .astype(float)
            / 10000
        )
    except IndexError:
        temp_df_ratio = pd.NA
    temp_df_yuan = common_temp_df["手续费标准-平今"][
        common_temp_df["手续费标准-平今"].str.contains("元")
    ]
    common_temp_df["手续费标准-平今-万分之"] = temp_df_ratio
    common_temp_df["手续费标准-平今-元"] = temp_df_yuan.str.strip("元")
    del common_temp_df["手续费标准-开仓"]
    del common_temp_df["手续费标准-平昨"]
    del common_temp_df["手续费标准-平今"]
    del common_temp_df["合约品种"]
    del common_temp_df["涨/跌停板"]
    del common_temp_df["手续费(开+平)"]
    del common_temp_df["保证金-保证金/每手"]
    common_temp_df["交易所名称"] = name
    common_temp_df = common_temp_df[
        [
            "交易所名称",
            "合约名称",
            "合约代码",
            "现价",
            "涨停板",
            "跌停板",
            "保证金-买开",
            "保证金-卖开",
            "保证金-每手",
            "手续费标准-开仓-万分之",
            "手续费标准-开仓-元",
            "手续费标准-平昨-万分之",
            "手续费标准-平昨-元",
            "手续费标准-平今-万分之",
            "手续费标准-平今-元",
            "每跳毛利",
            "手续费",
            "每跳净利",
            "备注",
        ]
    ]
    common_temp_df["现价"] = pd.to_numeric(common_temp_df["现价"])
    common_temp_df["涨停板"] = pd.to_numeric(common_temp_df["涨停板"])
    common_temp_df["跌停板"] = pd.to_numeric(common_temp_df["跌停板"])
    common_temp_df["保证金-买开"] = pd.to_numeric(common_temp_df["保证金-买开"])
    common_temp_df["保证金-卖开"] = pd.to_numeric(common_temp_df["保证金-卖开"])
    common_temp_df["保证金-每手"] = pd.to_numeric(common_temp_df["保证金-每手"])
    # common_temp_df["手续费标准-开仓-元"] = pd.to_numeric(common_temp_df["手续费标准-开仓-元"])
    # common_temp_df["手续费标准-平昨-元"] = pd.to_numeric(common_temp_df["手续费标准-平昨-元"])
    # common_temp_df["手续费标准-平今-元"] = pd.to_numeric(common_temp_df["手续费标准-平今-元"])
    common_temp_df["每跳毛利"] = pd.to_numeric(common_temp_df["每跳毛利"])
    common_temp_df["手续费"] = pd.to_numeric(common_temp_df["手续费"])
    common_temp_df["每跳净利"] = pd.to_numeric(common_temp_df["每跳净利"])
    comm_update_time, price_update_time = update_time
    common_temp_df["手续费更新时间"] = comm_update_time
    common_temp_df["价格更新时间"] = price_update_time
    return common_temp_df


def futures_comm_info(symbol: str = "所有") -> pd.DataFrame:
    """
    九期网-期货手续费
    https://www.9qihuo.com/qihuoshouxufei
    :param symbol: choice of {"所有", "上海期货交易所", "大连商品交易所", "郑州商品交易所", "上海国际能源交易中心", "中国金融期货交易所", "广州期货交易所"}
    :type symbol: str
    :return: 期货手续费
    :rtype: pandas.DataFrame
    """
    html = _futures_comm_qihuo_page()
    update_time = _futures_comm_qihuo_update_time(html)
    try:
        temp_df = pd.read_html(StringIO(html))[0]
    except ValueError as err:
        raise DataParsingError("9qihuo 页面中未找到手续费表格，上游可能已改版") from err
    temp_df.columns = [
        "合约品种",
        "现价",
        "涨/跌停板",
        "保证金-买开",
        "保证金-卖开",
        "保证金-保证金/每手",
        "手续费标准-开仓",
        "手续费标准-平昨",
        "手续费标准-平今",
        "每跳毛利",
        "手续费(开+平)",
        "每跳净利",
        "备注",
        "-",
        "-",
    ]
    df_0 = temp_df[temp_df["合约品种"].str.contains("上海期货交易所")].index.values[0]
    df_1 = temp_df[temp_df["合约品种"].str.contains("大连商品交易所")].index.values[0]
    df_2 = temp_df[temp_df["合约品种"].str.contains("郑州商品交易所")].index.values[0]
    df_3 = temp_df[
        temp_df["合约品种"].str.contains("上海国际能源交易中心")
    ].index.values[0]
    df_4 = temp_df[temp_df["合约品种"].str.contains("广州期货交易所")].index.values[0]
    df_5 = temp_df[temp_df["合约品种"].str.contains("中国金融期货交易所")].index.values[
        0
    ]
    shfe_df = temp_df.iloc[df_0 + 3 : df_1, :].reset_index(drop=True)
    dce_df = temp_df.iloc[df_1 + 3 : df_2, :].reset_index(drop=True)
    czce_df = temp_df.iloc[df_2 + 3 : df_3, :].reset_index(drop=True)
    ine_df = temp_df.iloc[df_3 + 3 : df_4, :].reset_index(drop=True)
    gfex_df = temp_df.iloc[df_4 + 3 : df_5, :].reset_index(drop=True)
    cffex_df = temp_df.iloc[df_5 + 3 :, :].reset_index(drop=True)
    if symbol == "上海期货交易所":
        return _futures_comm_qihuo_process(
            shfe_df, name="上海期货交易所", update_time=update_time
        )
    elif symbol == "大连商品交易所":
        return _futures_comm_qihuo_process(
            dce_df, name="大连商品交易所", update_time=update_time
        )
    elif symbol == "郑州商品交易所":
        return _futures_comm_qihuo_process(
            czce_df, name="郑州商品交易所", update_time=update_time
        )
    elif symbol == "上海国际能源交易中心":
        return _futures_comm_qihuo_process(
            ine_df, name="上海国际能源交易中心", update_time=update_time
        )
    elif symbol == "广州期货交易所":
        return _futures_comm_qihuo_process(
            gfex_df, name="广州期货交易所", update_time=update_time
        )
    elif symbol == "中国金融期货交易所":
        return _futures_comm_qihuo_process(
            cffex_df, name="中国金融期货交易所", update_time=update_time
        )
    else:
        big_df = pd.DataFrame()
        big_df = pd.concat(
            objs=[
                big_df,
                _futures_comm_qihuo_process(
                    shfe_df, name="上海期货交易所", update_time=update_time
                ),
            ],
            ignore_index=True,
        )
        big_df = pd.concat(
            objs=[
                big_df,
                _futures_comm_qihuo_process(
                    dce_df, name="大连商品交易所", update_time=update_time
                ),
            ],
            ignore_index=True,
        )
        big_df = pd.concat(
            objs=[
                big_df,
                _futures_comm_qihuo_process(
                    czce_df, name="郑州商品交易所", update_time=update_time
                ),
            ],
            ignore_index=True,
        )
        big_df = pd.concat(
            objs=[
                big_df,
                _futures_comm_qihuo_process(
                    ine_df, name="上海国际能源交易中心", update_time=update_time
                ),
            ],
            ignore_index=True,
        )
        big_df = pd.concat(
            objs=[
                big_df,
                _futures_comm_qihuo_process(
                    gfex_df, name="广州期货交易所", update_time=update_time
                ),
            ],
            ignore_index=True,
        )
        big_df = pd.concat(
            objs=[
                big_df,
                _futures_comm_qihuo_process(
                    cffex_df, name="中国金融期货交易所", update_time=update_time
                ),
            ],
            ignore_index=True,
        )
        return big_df


if __name__ == "__main__":
    futures_comm_info_df = futures_comm_info(symbol="所有")
    print(futures_comm_info_df)
