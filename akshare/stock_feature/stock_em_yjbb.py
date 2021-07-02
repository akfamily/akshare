# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/3 10:27
Desc: 东方财富-数据中心-年报季报
东方财富-数据中心-年报季报-业绩快报-业绩报表
http://data.eastmoney.com/bbsj/202003/yjbb.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_em_yjbb(date: str = "20200331") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩快报-业绩报表
    http://data.eastmoney.com/bbsj/202003/yjbb.html
    :param date: "20200331", "20200630", "20200930", "20201231"; 从 20100331 开始
    :type date: str
    :return: 业绩报表
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "st": "UPDATE_DATE,SECURITY_CODE",
        "sr": "-1,-1",
        "ps": "5000",
        "p": "1",
        "type": "RPT_LICO_FN_CPD",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "filter": f"(REPORTDATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params = {
            "st": "UPDATE_DATE,SECURITY_CODE",
            "sr": "-1,-1",
            "ps": "500",
            "p": page,
            "type": "RPT_LICO_FN_CPD",
            "sty": "ALL",
            "token": "894050c76af8597a853f5b408b759f5d",
            "filter": f"(REPORTDATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "股票代码",
        "股票简称",
        "_",
        "_",
        "_",
        "_",
        "最新公告日期",
        "_",
        "每股收益",
        "_",
        "营业收入-营业收入",
        "净利润-净利润",
        "净资产收益率",
        "营业收入-同比增长",
        "净利润-同比增长",
        "每股净资产",
        "每股经营现金流量",
        "销售毛利率",
        "营业收入-季度环比增长",
        "净利润-季度环比增长",
        "_",
        "_",
        "所处行业",
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
    ]
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "每股收益",
            "营业收入-营业收入",
            "营业收入-同比增长",
            "营业收入-季度环比增长",
            "净利润-净利润",
            "净利润-同比增长",
            "净利润-季度环比增长",
            "每股净资产",
            "净资产收益率",
            "每股经营现金流量",
            "销售毛利率",
            "所处行业",
            "最新公告日期",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_em_yjbb_df = stock_em_yjbb(date="20200331")
    print(stock_em_yjbb_df)
