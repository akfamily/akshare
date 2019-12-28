# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/27 18:02
contact: jindaxiang@163.com
desc: 东方财富网-数据中心-特色数据-股权质押
东方财富网-数据中心-特色数据-股权质押-股权质押市场概况: http://data.eastmoney.com/jgdy/tj.html
东方财富网-数据中心-特色数据-股权质押-上市公司质押比例: http://data.eastmoney.com/gpzy/pledgeRatio.aspx
"""
import json

import requests
import demjson
import pandas as pd


# pd.set_option('display.max_columns', 500)


def _get_page_num_gpzy_market_profile():
    """
    东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
    http://data.eastmoney.com/jgdy/tj.html
    :return: int 获取 股权质押市场概况 的总页数
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "ZD_SUM",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "tdate",
        "sr": "-1",
        "p": "3",
        "ps": "5000",
        "js": "var zvxnZOnT={pages:(tp),data:(x),font:(font)}",
        "rt": "52583914",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
    return data_json["pages"]


def _get_page_num_gpzy_market_pledge_ratio():
    """
    东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
    http://data.eastmoney.com/gpzy/pledgeRatio.aspx
    :return: int 获取 机构调研详细 的总页数
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "ZD_QL_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "amtshareratio",
        "sr": "-1",
        "p": "2",
        'ps': '5000',
        'js': "var rlJqyOhv={pages:(tp),data:(x),font:(font)}",
        "filter": "(tdate='2019-12-27')",
        "rt": '52584436',
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
    return data_json["pages"]


def stock_em_gpzy_profile():
    """
    东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
    http://data.eastmoney.com/jgdy/tj.html
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_gpzy_market_profile()
    temp_df = pd.DataFrame()
    for page in range(1, page_num + 1):
        print(f"一共{page_num}页, 正在下载第{page}页")
        params = {
            "type": "ZD_SUM",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "cmd": "",
            "st": "tdate",
            "sr": "-1",
            "p": str(page),
            "ps": "5000",
            "js": "var zvxnZOnT={pages:(tp),data:(x),font:(font)}",
            "rt": "52583914",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        map_dict = dict(zip(pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                            pd.DataFrame(data_json["font"]["FontMapping"])["value"]))
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = ['交易日期', 'sc_zsz', '平均质押比例(%)', '涨跌幅', 'A股质押总比例(%)', '质押公司数量', '质押笔数', '质押总股数(股)', '质押总市值(元)',
                       '沪深300指数']
    temp_df = temp_df[['交易日期', '平均质押比例(%)', '涨跌幅', 'A股质押总比例(%)', '质押公司数量', '质押笔数', '质押总股数(股)', '质押总市值(元)', '沪深300指数']]
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    return temp_df


def stock_em_gpzy_pledge_ratio():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研详细
    http://data.eastmoney.com/jgdy/xx.html
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_gpzy_market_pledge_ratio()
    temp_df = pd.DataFrame()
    for page in range(1, page_num + 1):
        print(f"一共{page_num}页, 正在下载第{page}页")
        params = {
            "type": "ZD_QL_LB",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "cmd": "",
            "st": "amtshareratio",
            "sr": "-1",
            "p": str(page),
            'ps': '5000',
            'js': "var rlJqyOhv={pages:(tp),data:(x),font:(font)}",
            "filter": "(tdate='2019-12-27')",
            "rt": '52584436',
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        map_dict = dict(zip(pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                            pd.DataFrame(data_json["font"]["FontMapping"])["value"]))
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = ['股票代码', '股票简称', '交易日期', '所属行业', 'blfb', '质押比例(%)', '质押股数(股)', '质押市值(元)', '质押笔数', '无限售股质押数(股)', '限售股质押数(股)', '近一年涨跌幅(%)']
    temp_df = temp_df[['股票代码', '股票简称', '交易日期', '所属行业', '质押比例(%)', '质押股数(股)', '质押市值(元)', '质押笔数', '无限售股质押数(股)', '限售股质押数(股)', '近一年涨跌幅(%)']]
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    return temp_df


if __name__ == '__main__':
    # df_tj = stock_em_gpzy_profile()
    # print(df_tj)
    stock_em_gpzy_pledge_df = stock_em_gpzy_pledge_ratio()
    print(stock_em_gpzy_pledge_df)
    stock_em_gpzy_pledge_df.columns
