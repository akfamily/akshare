#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2019/10/25 15:56
Desc: 和讯财经-上市公司社会责任报告数据, http://stockdata.stock.hexun.com/zrbg/
"""
from akshare.utils import demjson
import requests
import pandas as pd
from tqdm import tqdm

from akshare.stock.cons import (hx_headers,
                                hx_params,
                                hx_url)


def stock_zh_a_scr_report(report_year=2018, page=1):
    """
    获取和讯财经-上市公司社会责任报告数据, 从2010年至今(年度)
    因为股票数量大, 所以获取某年需要遍历所有页
    :param report_year: int 年份
    :param page: int 具体某页
    :return: pandas.DataFrame
            股票名称   股东责任    总得分 等级  员工责任  环境责任   社会责任 供应商、客户和消费者权益责任
    0    陆家嘴(600663)  23.97  42.97  C  4.00  0.00  15.00           0.00
    1   世荣兆业(002016)  24.61  42.44  C  2.83  0.00  15.00           0.00
    2    万科A(000002)  23.18  42.18  C  4.00  0.00  15.00           0.00
    3   华夏幸福(600340)  22.76  41.76  C  4.00  0.00  15.00           0.00
    4   万业企业(600641)  22.03  41.03  C  4.00  0.00  15.00           0.00
    5   华联控股(000036)  24.96  40.98  C  1.02  0.00  15.00           0.00
    6   中国国贸(600007)  22.43  40.98  C  3.55  0.00  15.00           0.00
    7    新黄浦(600638)  22.25  40.92  C  3.67  0.00  15.00           0.00
    8   金科股份(000656)  22.47  40.62  C  4.00  0.00  14.15           0.00
    9   中华企业(600675)  21.44  40.44  C  4.00  0.00  15.00           0.00
    10  京投发展(600683)  21.39  40.39  C  4.00  0.00  15.00           0.00
    11  浦东金桥(600639)  21.32  40.32  C  4.00  0.00  15.00           0.00
    12  中航善达(000043)  22.80  40.06  C  2.26  0.00  15.00           0.00
    13   新华联(000620)  21.00  40.00  D  4.00  0.00  15.00           0.00
    14  首开股份(600376)  20.77  39.77  D  4.00  0.00  15.00           0.00
    15  深物业A(000011)  23.49  39.73  D  1.50  0.00  14.74           0.00
    16  江苏租赁(600901)  20.62  39.62  D  4.00  0.00  15.00           0.00
    17  中国太保(601601)  20.61  39.61  D  4.00  0.00  15.00           0.00
    18  中国平安(601318)  20.59  39.59  D  4.00  0.00  15.00           0.00
    19  深深房A(000029)  22.45  39.47  D  2.02  0.00  15.00           0.00
    """
    hx_params_copy = hx_params.copy()
    hx_params_copy.update({"date": "{}-12-31".format(str(report_year))})
    hx_params_copy.update({"page": page})
    res = requests.get(hx_url, headers=hx_headers, params=hx_params_copy)
    temp_df = res.text[res.text.find("(") + 1:res.text.rfind(")")]
    py_obj = demjson.decode(temp_df)
    industry = [item["industry"] for item in py_obj["list"]]
    stock_number = [item["stockNumber"] for item in py_obj["list"]]
    industry_rate = [item["industryrate"] for item in py_obj["list"]]
    price_limit = [item["Pricelimit"] for item in py_obj["list"]]
    looting_chips = [item["lootingchips"] for item in py_obj["list"]]
    r_scramble = [item["rscramble"] for item in py_obj["list"]]
    strong_stock = [item["Strongstock"] for item in py_obj["list"]]
    s_cramble = [item["Scramble"] for item in py_obj["list"]]
    return pd.DataFrame([industry, stock_number, industry_rate, price_limit, looting_chips, r_scramble, strong_stock, s_cramble],
                        index=["股票名称", "股东责任", "总得分", "等级", "员工责任", "环境责任", "社会责任", "供应商、客户和消费者权益责任"]).T


if __name__ == "__main__":
    for i_page in tqdm(range(1, 100)):
        df = stock_zh_a_scr_report(report_year=2018, page=i_page)
        # print(df)
