#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/8/28 15:00
Desc: To test intention, just write test code here!
"""

import pathlib

import akshare as ak
from akshare.datasets import get_ths_js, get_crypto_info_csv
from akshare.utils.db import save_to_mysql


def test_cost_living():
    """
    just for test aim
    :return: assert result
    :rtype: assert
    """
    pass


def test_path_func():
    """
    test path func
    :return: path of file
    :rtype: pathlib.Path
    """
    temp_path = get_ths_js("ths.js")
    assert isinstance(temp_path, pathlib.Path)


def test_zipfile_func():
    """
    test path func
    :return: path of file
    :rtype: pathlib.Path
    """
    temp_path = get_crypto_info_csv("crypto_info.zip")
    assert isinstance(temp_path, pathlib.Path)


def test_demo():
    """
    获取指定股票的历史估值数据
    """

    stock_value_em_df = ak.stock_value_em(symbol="601398")
    print(stock_value_em_df)
    # 保存到 MySQL 数据库
    success = save_to_mysql(
        df=stock_value_em_df,
        table_name="stock_000001_daily",
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="akshare",
        column_mapping=filed(),
        column_comments=comment(),
    )

    if success:
        print("数据保存成功")
    else:
        print("数据保存失败")


def test_stock_zh_a_hist():
    stock_hfq_df = ak.stock_zh_a_hist(symbol="601398", adjust="").iloc[:, :7]
    del stock_hfq_df['股票代码']

if __name__ == "__main__":
    # test_cost_living()
    # test_path_func()
    # test_zipfile_func()
    test_demo()
    test_stock_zh_a_hist()


def filed():
    # 原始字典（字段映射）
    field_mapping = {
        "TRADE_DATE": "数据日期",
        "CLOSE_PRICE": "当日收盘价",
        "CHANGE_RATE": "当日涨跌幅",
        "TOTAL_MARKET_CAP": "总市值",
        "NOTLIMITED_MARKETCAP_A": "流通市值",
        "TOTAL_SHARES": "总股本",
        "FREE_SHARES_A": "流通股本",
        "PE_TTM": "PE(TTM)",
        "PE_LAR": "PE(静)",
        "PB_MRQ": "市净率",
        "PEG_CAR": "PEG值",
        "PCF_OCF_TTM": "市现率",
        "PS_TTM": "市销率",
    }
    # 键值互换后的字典（反向字段映射）
    reverse_field_mapping = {v: k for k, v in field_mapping.items()}
    return reverse_field_mapping


def comment():
    # 原始字典（字段映射）
    field_mapping = {
        "TRADE_DATE": "数据日期",
        "CLOSE_PRICE": "当日收盘价",
        "CHANGE_RATE": "当日涨跌幅",
        "TOTAL_MARKET_CAP": "总市值",
        "NOTLIMITED_MARKETCAP_A": "流通市值",
        "TOTAL_SHARES": "总股本",
        "FREE_SHARES_A": "流通股本",
        "PE_TTM": "PE(TTM)",
        "PE_LAR": "PE(静)",
        "PB_MRQ": "市净率",
        "PEG_CAR": "PEG值",
        "PCF_OCF_TTM": "市现率",
        "PS_TTM": "市销率",
    }
    return field_mapping
