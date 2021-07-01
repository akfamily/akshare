# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/22 13:28
Desc: 新浪财经-债券-沪深可转债-实时行情数据和历史行情数据
http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
"""
import datetime
import re

import demjson
from py_mini_racer import py_mini_racer
import pandas as pd
import requests
from tqdm import tqdm

from akshare.bond.cons import (
    zh_sina_bond_hs_cov_count_url,
    zh_sina_bond_hs_cov_payload,
    zh_sina_bond_hs_cov_url,
    zh_sina_bond_hs_cov_hist_url,
)
from akshare.stock.cons import hk_js_decode


def _get_zh_bond_hs_cov_page_count() -> int:
    """
    行情中心首页-债券-沪深可转债的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 总页数
    :rtype: int
    """
    params = {
        "node": "hskzz_z",
    }
    res = requests.get(zh_sina_bond_hs_cov_count_url, params=params)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def bond_zh_hs_cov_spot() -> pd.DataFrame:
    """
    新浪财经-债券-沪深可转债的实时行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 所有沪深可转债在当前时刻的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_bond_hs_cov_page_count()
    zh_sina_bond_hs_payload_copy = zh_sina_bond_hs_cov_payload.copy()
    for page in tqdm(range(1, page_count + 1), leave=False):
        zh_sina_bond_hs_payload_copy.update({"page": page})
        res = requests.get(zh_sina_bond_hs_cov_url, params=zh_sina_bond_hs_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    return big_df


def bond_zh_hs_cov_daily(symbol: str = "sh113542") -> pd.DataFrame:
    """
    新浪财经-债券-沪深可转债的历史行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :param symbol: 沪深可转债代码; e.g., sh010107
    :type symbol: str
    :return: 指定沪深可转债代码的日 K 线数据
    :rtype: pandas.DataFrame
    """
    res = requests.get(
        zh_sina_bond_hs_cov_hist_url.format(
            symbol, datetime.datetime.now().strftime("%Y_%m_%d")
        )
    )
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df = data_df.astype("float")
    return data_df


def bond_zh_cov() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-可转债数据
    http://data.eastmoney.com/kzz/default.html
    :return: 可转债数据
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "KZZ_LB2.0",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "STARTDATE",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var {jsname}={pages:(tp),data:(x),font:(font)}",
        "rt": "53603537",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = demjson.decode(text_data[text_data.find("=") + 1:])
    temp_df = pd.DataFrame(json_data["data"])
    map_dict = {
        item["code"]: item["value"] for item in json_data["font"]["FontMapping"]
    }
    for key, value in map_dict.items():
        for i in range(1, 9):
            temp_df.iloc[:, -i] = temp_df.iloc[:, -i].apply(
                lambda x: x.replace(key, str(value))
            )
    temp_df.columns = [
        "债券代码",
        "交易场所",
        "_",
        "债券简称",
        "申购日期",
        "申购代码",
        "_",
        "正股代码",
        "正股简称",
        "债券面值",
        "发行价格",
        "_",
        "中签号发布日",
        "中签率",
        "上市时间",
        "_",
        "备忘录",
        "正股价",
        "市场类型",
        "_",
        "_",
        "_",
        "股权登记日",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "申购上限",
        "_",
        "转股价",
        "转股价值",
        "债现价",
        "转股溢价率",
        "每股配售额",
        "发行规模",
    ]
    temp_df = temp_df[
        [
            "债券代码",
            "交易场所",
            "债券简称",
            "申购日期",
            "申购代码",
            "正股代码",
            "正股简称",
            "债券面值",
            "发行价格",
            "转股价",
            "中签号发布日",
            "中签率",
            "上市时间",
            "备忘录",
            "正股价",
            "市场类型",
            "股权登记日",
            "申购上限",
            "转股价值",
            "债现价",
            "转股溢价率",
            "每股配售额",
            "发行规模",
        ]
    ]
    return temp_df


def bond_cov_comparison() -> pd.DataFrame:
    """
    东方财富网-行情中心-债券市场-可转债比价表
    http://quote.eastmoney.com/center/fullscreenlist.html#convertible_comparison
    :return: 可转债比价表数据
    :rtype: pandas.DataFrame
    """
    url = "http://16.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f243",
        "fs": "b:MK0354",
        "fields": "f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243",
        "_": "1590386857527",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = demjson.decode(text_data)
    temp_df = pd.DataFrame(json_data["data"]["diff"])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "_",
        "转债最新价",
        "转债涨跌幅",
        "转债代码",
        "_",
        "转债名称",
        "上市日期",
        "_",
        "纯债价值",
        "_",
        "正股最新价",
        "正股涨跌幅",
        "_",
        "正股代码",
        "_",
        "正股名称",
        "转股价",
        "转股价值",
        "转股溢价率",
        "纯债溢价率",
        "回售触发价",
        "强赎触发价",
        "到期赎回价",
        "开始转股日",
        "申购日期",
    ]
    temp_df = temp_df[
        [
            "序号",
            "转债代码",
            "转债名称",
            "转债最新价",
            "转债涨跌幅",
            "正股代码",
            "正股名称",
            "正股最新价",
            "正股涨跌幅",
            "转股价",
            "转股价值",
            "转股溢价率",
            "纯债溢价率",
            "回售触发价",
            "强赎触发价",
            "到期赎回价",
            "纯债价值",
            "开始转股日",
            "上市日期",
            "申购日期",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    bond_zh_hs_cov_daily_df = bond_zh_hs_cov_daily(symbol="sh113542")
    print(bond_zh_hs_cov_daily_df)
    bond_zh_hs_cov_spot_df = bond_zh_hs_cov_spot()
    print(bond_zh_hs_cov_spot_df)

    bond_zh_cov_df = bond_zh_cov()
    print(bond_zh_cov_df)

    bond_cov_comparison_df = bond_cov_comparison()
    print(bond_cov_comparison_df)
