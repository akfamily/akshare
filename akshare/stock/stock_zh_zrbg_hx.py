#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/28 15:55
Desc: 和讯财经-上市公司社会责任报告数据
http://stockdata.stock.hexun.com/zrbg/Plate.aspx#
"""
import pandas as pd
import requests
from tqdm import tqdm

from akshare.stock.cons import hx_headers, hx_params, hx_url
from akshare.utils import demjson


def stock_zh_a_scr_report(year: str = "2018", need_page: str = "1") -> pd.DataFrame:
    """
    和讯财经-上市公司社会责任报告, 从 2010- 年至今
    因为股票数量大, 所以获取某年需要遍历所有页
    http://stockdata.stock.hexun.com/zrbg/Plate.aspx#
    :param year: 报告年份
    :type year: str
    :param need_page: 需要获取的天数
    :type need_page: str
    :return: 上市公司社会责任报告数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(need_page)+1)):
        hx_params_copy = hx_params.copy()
        hx_params_copy.update({"date": "{}-12-31".format(year)})
        hx_params_copy.update({"page": page})
        r = requests.get(hx_url, headers=hx_headers, params=hx_params_copy)
        data_text = r.text
        temp_df = data_text[data_text.find("(") + 1: data_text.rfind(")")]
        py_obj = demjson.decode(temp_df)
        industry = [item["industry"] for item in py_obj["list"]]
        stock_number = [item["stockNumber"] for item in py_obj["list"]]
        industry_rate = [item["industryrate"] for item in py_obj["list"]]
        price_limit = [item["Pricelimit"] for item in py_obj["list"]]
        looting_chips = [item["lootingchips"] for item in py_obj["list"]]
        r_scramble = [item["rscramble"] for item in py_obj["list"]]
        strong_stock = [item["Strongstock"] for item in py_obj["list"]]
        s_cramble = [item["Scramble"] for item in py_obj["list"]]
        temp_df = pd.DataFrame(
            [
                industry,
                stock_number,
                industry_rate,
                price_limit,
                looting_chips,
                r_scramble,
                strong_stock,
                s_cramble,
            ],
            index=["股票名称", "股东责任", "总得分", "等级", "员工责任", "环境责任", "社会责任", "供应商、客户和消费者权益责任"],
        ).T
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.rename({"index": "序号"}, axis="columns", inplace=True)
    big_df["股票代码"] = (
        big_df["股票名称"].str.split("(", expand=True).iloc[:, 1].str.strip(")")
    )
    big_df["股票名称"] = big_df["股票名称"].str.split("(", expand=True).iloc[:, 0]
    big_df["股东责任"] = pd.to_numeric(big_df["股东责任"])
    big_df["总得分"] = pd.to_numeric(big_df["总得分"])
    big_df["员工责任"] = pd.to_numeric(big_df["员工责任"])
    big_df["环境责任"] = pd.to_numeric(big_df["环境责任"])
    big_df["社会责任"] = pd.to_numeric(big_df["社会责任"])
    big_df["供应商、客户和消费者权益责任"] = pd.to_numeric(big_df["供应商、客户和消费者权益责任"])
    big_df = big_df[
        [
            "序号",
            "股票名称",
            "股票代码",
            "总得分",
            "等级",
            "股东责任",
            "员工责任",
            "供应商、客户和消费者权益责任",
            "环境责任",
            "社会责任",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_zh_a_scr_report_df = stock_zh_a_scr_report(year="2018", need_page="10")
    print(stock_zh_a_scr_report_df)
