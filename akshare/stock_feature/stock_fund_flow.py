# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/24 21:13
Desc: 同花顺-数据中心-资金流向
同花顺-数据中心-资金流向-行业资金流
http://data.10jqka.com.cn/funds/hyzjl/#refCountId=data_55f13c2c_254
同花顺-数据中心-资金流向-概念资金流
http://data.10jqka.com.cn/funds/gnzjl/#refCountId=data_55f13c2c_254
"""
import os

import pandas as pd
import requests
from py_mini_racer import py_mini_racer
from tqdm import tqdm


def _get_js_path_ths(name: str = None, module_file: str = None) -> str:
    """
    获取 JS 文件的路径(从模块所在目录查找)
    :param name: 文件名
    :type name: str
    :param module_file: 模块路径
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_folder = os.path.abspath(os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "stock_feature", name)
    return module_json_path


def _get_file_content_ths(file_name: str = "ase.min.js") -> str:
    """
    获取 JS 文件的内容
    :param file_name:  JS 文件名
    :type file_name: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path_ths(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def stock_fund_flow_industry(symbol: str = "即时") -> pd.DataFrame:
    """
    同花顺-数据中心-资金流向-行业资金流
    http://data.10jqka.com.cn/funds/hyzjl/#refCountId=data_55f13c2c_254
    :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
    :type symbol: str
    :return: 行业资金流
    :rtype: pandas.DataFrame
    """
    if symbol == "3日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/3/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "5日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/5/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "10日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/10/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "20日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/20/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    else:
        url = "http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    big_df = pd.DataFrame()
    for page in tqdm(range(1, 3)):
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call("v")
        headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "hexin-v": v_code,
            "Host": "data.10jqka.com.cn",
            "Pragma": "no-cache",
            "Referer": "http://data.10jqka.com.cn/funds/hyzjl/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        r = requests.get(url.format(page), headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    del big_df["序号"]
    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    if symbol == "即时":
        big_df.columns = [
            "序号",
            "行业",
            "行业指数",
            "涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
            "公司家数",
            "领涨股",
            "涨跌幅",
            "当前价",
        ]
    else:
        big_df.columns = [
            "序号",
            "行业",
            "公司家数",
            "行业指数",
            "阶段涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
        ]
    return big_df


def stock_fund_flow_concept(symbol: str = "即时") -> pd.DataFrame:
    """
    同花顺-数据中心-资金流向-概念资金流
    http://data.10jqka.com.cn/funds/gnzjl/#refCountId=data_55f13c2c_254
    :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
    :type symbol: str
    :return: 概念资金流
    :rtype: pandas.DataFrame
    """
    if symbol == "3日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/3/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "5日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/5/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "10日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/10/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "20日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/20/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    else:
        url = "http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"

    big_df = pd.DataFrame()
    for page in tqdm(range(1, 7)):
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call("v")
        headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "hexin-v": v_code,
            "Host": "data.10jqka.com.cn",
            "Pragma": "no-cache",
            "Referer": "http://data.10jqka.com.cn/funds/gnzjl/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        r = requests.get(url.format(page), headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    del big_df["序号"]
    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    if symbol == "即时":
        big_df.columns = [
            "序号",
            "行业",
            "行业指数",
            "涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
            "公司家数",
            "领涨股",
            "涨跌幅",
            "当前价",
        ]
    else:
        big_df.columns = [
            "序号",
            "行业",
            "公司家数",
            "行业指数",
            "阶段涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
        ]
    return big_df


if __name__ == "__main__":
    stock_fund_flow_industry_df = stock_fund_flow_industry(symbol="即时")
    print(stock_fund_flow_industry_df)

    stock_fund_flow_industry_df = stock_fund_flow_industry(symbol="3日排行")
    print(stock_fund_flow_industry_df)

    stock_fund_flow_industry_df = stock_fund_flow_industry(symbol="5日排行")
    print(stock_fund_flow_industry_df)

    stock_fund_flow_industry_df = stock_fund_flow_industry(symbol="10日排行")
    print(stock_fund_flow_industry_df)

    stock_fund_flow_industry_df = stock_fund_flow_industry(symbol="20日排行")
    print(stock_fund_flow_industry_df)

    stock_fund_flow_concept_df = stock_fund_flow_concept(symbol="即时")
    print(stock_fund_flow_concept_df)

    stock_fund_flow_concept_df = stock_fund_flow_concept(symbol="3日排行")
    print(stock_fund_flow_concept_df)

    stock_fund_flow_concept_df = stock_fund_flow_concept(symbol="5日排行")
    print(stock_fund_flow_concept_df)

    stock_fund_flow_concept_df = stock_fund_flow_concept(symbol="10日排行")
    print(stock_fund_flow_concept_df)

    stock_fund_flow_concept_df = stock_fund_flow_concept(symbol="20日排行")
    print(stock_fund_flow_concept_df)
