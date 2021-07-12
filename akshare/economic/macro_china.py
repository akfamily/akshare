# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/9 16:08
Desc: 金十数据-数据中心-中国-中国宏观
https://datacenter.jin10.com/economic
首页-价格指数-中价-价格指数-中国电煤价格指数(CTCI)
http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
"""
import json
import math
import time
from datetime import datetime

import demjson
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

from akshare.economic.cons import (
    JS_CHINA_CPI_YEARLY_URL,
    JS_CHINA_CPI_MONTHLY_URL,
    JS_CHINA_M2_YEARLY_URL,
    JS_CHINA_PPI_YEARLY_URL,
    JS_CHINA_PMI_YEARLY_URL,
    JS_CHINA_GDP_YEARLY_URL,
    JS_CHINA_CX_PMI_YEARLY_URL,
    JS_CHINA_FX_RESERVES_YEARLY_URL,
    JS_CHINA_ENERGY_DAILY_URL,
    JS_CHINA_NON_MAN_PMI_MONTHLY_URL,
    JS_CHINA_CX_SERVICE_PMI_YEARLY_URL,
    JS_CHINA_MARKET_MARGIN_SH_URL,
)


# 企业商品价格指数
def macro_china_qyspjg() -> pd.DataFrame:
    """
    企业商品价格指数
    http://data.eastmoney.com/cjsj/qyspjg.html
    :return: 企业商品价格指数
    :rtype: pandas.DataFrame
    """
    url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx'
    params = {
        'type': 'GJZB',
        'sty': 'ZGZB',
        'js': '({data:[(x)],pages:(pc)})',
        'p': '1',
        'ps': '2000',
        'mkt': '9',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1625474966006'
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(',') for item in data_json['data']])
    temp_df.columns = [
        '月份',
        '总指数-指数值',
        '总指数-同比增长',
        '总指数-环比增长',
        '农产品-指数值',
        '农产品-同比增长',
        '农产品-环比增长',
        '矿产品-指数值',
        '矿产品-同比增长',
        '矿产品-环比增长',
        '煤油电-指数值',
        '煤油电-同比增长',
        '煤油电-环比增长',
    ]
    temp_df['总指数-指数值'] = pd.to_numeric(temp_df['总指数-指数值'])
    temp_df['总指数-同比增长'] = pd.to_numeric(temp_df['总指数-同比增长'])
    temp_df['总指数-环比增长'] = pd.to_numeric(temp_df['总指数-环比增长'])
    temp_df['农产品-指数值'] = pd.to_numeric(temp_df['农产品-指数值'])
    temp_df['农产品-同比增长'] = pd.to_numeric(temp_df['农产品-同比增长'])
    temp_df['农产品-环比增长'] = pd.to_numeric(temp_df['农产品-环比增长'])
    temp_df['矿产品-指数值'] = pd.to_numeric(temp_df['矿产品-指数值'])
    temp_df['矿产品-同比增长'] = pd.to_numeric(temp_df['矿产品-同比增长'])
    temp_df['矿产品-环比增长'] = pd.to_numeric(temp_df['矿产品-环比增长'])
    temp_df['煤油电-指数值'] = pd.to_numeric(temp_df['煤油电-指数值'])
    temp_df['煤油电-同比增长'] = pd.to_numeric(temp_df['煤油电-同比增长'])
    temp_df['煤油电-环比增长'] = pd.to_numeric(temp_df['煤油电-环比增长'])
    return temp_df


# 外商直接投资数据
def macro_china_fdi() -> pd.DataFrame:
    """
    外商直接投资数据
    http://data.eastmoney.com/cjsj/fdi.html
    :return: 外商直接投资数据
    :rtype: pandas.DataFrame
    """
    url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx'
    params = {
        'type': 'GJZB',
        'sty': 'ZGZB',
        'js': '({data:[(x)],pages:(pc)})',
        'p': '1',
        'ps': '2000',
        'mkt': '15',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1625474966006'
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(',') for item in data_json['data']])
    temp_df.columns = [
        '月份',
        '当月',
        '当月-同比增长',
        '当月-环比增长',
        '累计',
        '累计-同比增长',
    ]
    temp_df['当月'] = pd.to_numeric(temp_df['当月'])
    temp_df['当月-同比增长'] = pd.to_numeric(temp_df['当月-同比增长'])
    temp_df['当月-环比增长'] = pd.to_numeric(temp_df['当月-环比增长'])
    temp_df['累计'] = pd.to_numeric(temp_df['累计'])
    temp_df['累计-同比增长'] = pd.to_numeric(temp_df['累计-同比增长'])
    return temp_df


# 中国社会融资规模数据
def macro_china_shrzgm() -> pd.DataFrame:
    """
    社会融资规模增量统计
    http://data.mofcom.gov.cn/gnmy/shrzgm.shtml
    :return: 社会融资规模增量统计
    :rtype: pandas.DataFrame
    """
    url = "http://data.mofcom.gov.cn/datamofcom/front/gnmy/shrzgmQuery"
    r = requests.post(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df.columns = [
        "月份",
        "其中-未贴现银行承兑汇票",
        "其中-委托贷款",
        "其中-委托贷款外币贷款(折合人民币)",
        "其中-人民币贷款",
        "其中-企业债券",
        "社会融资规模增量",
        "其中-非金融企业境内股票融资",
        "其中-信托贷款",
    ]
    temp_df = temp_df[[
        "月份",
        "社会融资规模增量",
        "其中-人民币贷款",
        "其中-委托贷款外币贷款(折合人民币)",
        "其中-委托贷款",
        "其中-信托贷款",
        "其中-未贴现银行承兑汇票",
        "其中-企业债券",
        "其中-非金融企业境内股票融资",
    ]]
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
def macro_china_gdp_yearly():
    """
    中国年度GDP数据, 数据区间从20110120-至今
    https://datacenter.jin10.com/reportType/dc_chinese_gdp_yoy
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_GDP_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国GDP年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "gdp"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
def macro_china_cpi_yearly():
    """
    中国年度CPI数据, 数据区间从19860201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_cpi_yoy
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CPI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI月率报告
def macro_china_cpi_monthly():
    """
    中国月度CPI数据, 数据区间从19960201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_cpi_mom
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CPI_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
def macro_china_ppi_yearly():
    """
    中国年度PPI数据, 数据区间从19950801-至今
    https://datacenter.jin10.com/reportType/dc_chinese_ppi_yoy
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_PPI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国PPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "ppi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
def macro_china_exports_yoy():
    """
    中国以美元计算出口年率报告, 数据区间从19820201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_exports_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_exports_yoy_all.js?v=1578754453
    :return: 中国以美元计算出口年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_exports_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国以美元计算出口年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "china_exports_yoy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
def macro_china_imports_yoy():
    """
    中国以美元计算进口年率报告, 数据区间从19960201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_imports_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_imports_yoy_all.js?v=1578754588
    :return: 中国以美元计算进口年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_imports_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国以美元计算进口年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "china_imports_yoy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-贸易状况-以美元计算贸易帐(亿美元)
def macro_china_trade_balance():
    """
    中国以美元计算贸易帐报告, 数据区间从19810201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_trade_balance
    https://cdn.jin10.com/dc/reports/dc_chinese_trade_balance_all.js?v=1578754677
    :return: 中国以美元计算贸易帐报告-今值(亿美元)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_trade_balance_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国以美元计算贸易帐报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    temp_df.name = "china_trade_balance"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-规模以上工业增加值年率
def macro_china_industrial_production_yoy():
    """
    中国规模以上工业增加值年率报告, 数据区间从19900301-至今
    https://datacenter.jin10.com/reportType/dc_chinese_industrial_production_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_industrial_production_yoy_all.js?v=1578754779
    :return: 中国规模以上工业增加值年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_chinese_industrial_production_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国规模以上工业增加值年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "china_industrial_production_yoy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-官方制造业PMI
def macro_china_pmi_yearly():
    """
    中国年度PMI数据, 数据区间从20050201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_manufacturing_pmi_all.js?v=1578817858
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国官方制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-财新制造业PMI终值
def macro_china_cx_pmi_yearly():
    """
    中国年度财新PMI数据, 数据区间从20120120-至今
    https://datacenter.jin10.com/reportType/dc_chinese_caixin_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_caixin_manufacturing_pmi_all.js?v=1578818009
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CX_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国财新制造业PMI终值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "cx_pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-财新服务业PMI
def macro_china_cx_services_pmi_yearly():
    """
    中国财新服务业PMI报告, 数据区间从20120405-至今
    https://datacenter.jin10.com/reportType/dc_chinese_caixin_services_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_caixin_services_pmi_all.js?v=1578818109
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CX_SERVICE_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国财新服务业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "cx_services_pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-产业指标-中国官方非制造业PMI
def macro_china_non_man_pmi():
    """
    中国官方非制造业PMI, 数据区间从20160101-至今
    https://datacenter.jin10.com/reportType/dc_chinese_non_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_chinese_non_manufacturing_pmi_all.js?v=1578818248
    :return: pandas.Series
    2007-02-01    60.4
    2007-03-01    60.6
    2007-04-01    58.2
    2007-05-01    60.4
    2007-06-01    62.2
                  ...
    2019-06-30    54.2
    2019-07-31    53.7
    2019-08-31    53.8
    2019-09-30    53.7
    2019-10-31       0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_NON_MAN_PMI_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国官方非制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "non_pmi"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-金融指标-外汇储备(亿美元)
def macro_china_fx_reserves_yearly():
    """
    中国年度外汇储备数据, 数据区间从20140115-至今
    https://datacenter.jin10.com/reportType/dc_chinese_fx_reserves
    https://cdn.jin10.com/dc/reports/dc_chinese_fx_reserves_all.js?v=1578818365
    :return: pandas.Series
    2014-01-15    39500
    2014-07-15    39900
    2015-01-15    32300
    2016-03-07    32020
    2016-04-07    32100
    2016-06-07    31900
    2016-07-07    32100
    2016-08-07    32010
    2016-09-07    31820
    2016-10-07    31660
    2016-11-07    31210
    2016-12-07    30520
    2017-01-07    30110
    2017-02-07    29980
    2017-03-07    30050
    2017-04-07    30090
    2017-05-07    30300
    2017-06-07    30540
    2017-07-07    30570
    2017-08-07    30810
    2017-09-07    30920
    2017-10-09    31080
    2017-11-07    31090
    2017-12-07    31190
    2017-12-08        0
    2018-01-07    31390
    2018-02-07    31620
    2018-02-08        0
    2018-03-07    31340
    2018-04-08    31430
    2018-05-07    31250
    2018-06-07    31110
    2018-07-09    31120
    2018-08-07    31180
    2018-09-07    31100
    2018-10-07    30870
    2018-11-07    30500
    2018-12-07    30600
    2019-01-07    30700
    2019-02-11    30700
    2019-03-07    30900
    2019-04-07    30990
    2019-05-07        0
    2019-05-08    31010
    2019-06-07        0
    2019-07-07        0
    2019-07-08    31190
    2019-08-07    31040
    2019-09-07    31070
    2019-10-08    30920
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_FX_RESERVES_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国外汇储备报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    temp_df.name = "fx_reserves"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-金融指标-M2货币供应年率
def macro_china_m2_yearly():
    """
    中国年度M2数据, 数据区间从19980201-至今
    https://datacenter.jin10.com/reportType/dc_chinese_m2_money_supply_yoy
    https://cdn.jin10.com/dc/reports/dc_chinese_m2_money_supply_yoy_all.js?v=1578818474
    :return: pandas.Series
    1998-02-01    17.4
    1998-03-01    16.7
    1998-04-01    15.4
    1998-05-01    14.6
    1998-06-01    15.5
                  ...
    2019-09-11     8.2
    2019-09-13       0
    2019-10-14       0
    2019-10-15     8.4
    2019-10-17       0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_M2_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国M2货币供应年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "m2"
    temp_df = temp_df[temp_df != 0]
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-金融指标-上海银行业同业拆借报告
def macro_china_shibor_all():
    """
    上海银行业同业拆借报告, 数据区间从20170317-至今
    https://datacenter.jin10.com/reportType/dc_shibor
    https://cdn.jin10.com/dc/reports/dc_shibor_all.js?v=1578755058
    :return: 上海银行业同业拆借报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/il_1.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    big_df["O/N_定价"] = temp_df["O/N"].apply(lambda x: x[0])
    big_df["O/N_涨跌幅"] = temp_df["O/N"].apply(lambda x: x[1])
    big_df["1W_定价"] = temp_df["1W"].apply(lambda x: x[0])
    big_df["1W_涨跌幅"] = temp_df["1W"].apply(lambda x: x[1])
    big_df["2W_定价"] = temp_df["2W"].apply(lambda x: x[0])
    big_df["2W_涨跌幅"] = temp_df["2W"].apply(lambda x: x[1])
    big_df["1M_定价"] = temp_df["1M"].apply(lambda x: x[0])
    big_df["1M_涨跌幅"] = temp_df["1M"].apply(lambda x: x[1])
    big_df["3M_定价"] = temp_df["3M"].apply(lambda x: x[0])
    big_df["3M_涨跌幅"] = temp_df["3M"].apply(lambda x: x[1])
    big_df["6M_定价"] = temp_df["6M"].apply(lambda x: x[0])
    big_df["6M_涨跌幅"] = temp_df["6M"].apply(lambda x: x[1])
    big_df["9M_定价"] = temp_df["9M"].apply(lambda x: x[0])
    big_df["9M_涨跌幅"] = temp_df["9M"].apply(lambda x: x[1])
    big_df["1Y_定价"] = temp_df["1Y"].apply(lambda x: x[0])
    big_df["1Y_涨跌幅"] = temp_df["1Y"].apply(lambda x: x[1])
    # big_df["ON_定价"] = temp_df["ON"].apply(lambda x: x[0])
    # big_df["ON_涨跌幅"] = temp_df["ON"].apply(lambda x: x[1])
    # big_df["2M_定价"] = temp_df["2M"].apply(lambda x: x[0])
    # big_df["2M_涨跌幅"] = temp_df["2M"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", np.nan))
    big_df = big_df.apply(lambda x: x.replace([None], np.nan))
    big_df.sort_index(inplace=True)
    big_df = big_df.astype("float")
    return big_df


# 金十数据中心-经济指标-中国-金融指标-人民币香港银行同业拆息
def macro_china_hk_market_info():
    """
    香港同业拆借报告, 数据区间从20170320-至今
    https://datacenter.jin10.com/reportType/dc_hk_market_info
    https://cdn.jin10.com/dc/reports/dc_hk_market_info_all.js?v=1578755471
    :return: 香港同业拆借报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/il_2.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    # big_df["O/N_定价"] = temp_df["O/N"].apply(lambda x: x[0])
    # big_df["O/N_涨跌幅"] = temp_df["O/N"].apply(lambda x: x[1])
    big_df["1W_定价"] = temp_df["1W"].apply(lambda x: x[0])
    big_df["1W_涨跌幅"] = temp_df["1W"].apply(lambda x: x[1])
    big_df["2W_定价"] = temp_df["2W"].apply(lambda x: x[0])
    big_df["2W_涨跌幅"] = temp_df["2W"].apply(lambda x: x[1])
    big_df["1M_定价"] = temp_df["1M"].apply(lambda x: x[0])
    big_df["1M_涨跌幅"] = temp_df["1M"].apply(lambda x: x[1])
    big_df["3M_定价"] = temp_df["3M"].apply(lambda x: x[0])
    big_df["3M_涨跌幅"] = temp_df["3M"].apply(lambda x: x[1])
    big_df["6M_定价"] = temp_df["6M"].apply(lambda x: x[0])
    big_df["6M_涨跌幅"] = temp_df["6M"].apply(lambda x: x[1])
    # big_df["9M_定价"] = temp_df["9M"].apply(lambda x: x[0])
    # big_df["9M_涨跌幅"] = temp_df["9M"].apply(lambda x: x[1])
    big_df["1Y_定价"] = temp_df["1Y"].apply(lambda x: x[0])
    big_df["1Y_涨跌幅"] = temp_df["1Y"].apply(lambda x: x[1])
    big_df["ON_定价"] = temp_df["ON"].apply(lambda x: x[0])
    big_df["ON_涨跌幅"] = temp_df["ON"].apply(lambda x: x[1])
    big_df["2M_定价"] = temp_df["2M"].apply(lambda x: x[0])
    big_df["2M_涨跌幅"] = temp_df["2M"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", np.nan))
    big_df = big_df.apply(lambda x: x.replace([None], np.nan))
    big_df.sort_index(inplace=True)
    big_df = big_df.astype("float")
    return big_df


# 金十数据中心-经济指标-中国-其他-中国日度沿海六大电库存数据
def macro_china_daily_energy():
    """
    中国日度沿海六大电库存数据, 数据区间从20160101-至今
    https://datacenter.jin10.com/reportType/dc_qihuo_energy_report
    https://cdn.jin10.com/dc/reports/dc_qihuo_energy_report_all.js?v=1578819100
    :return: pandas.Series
                 沿海六大电库存      日耗 存煤可用天数
    2016-01-01  1167.60   64.20   18.19
    2016-01-02  1162.90   63.40   18.34
    2016-01-03  1160.80   62.60   18.54
    2016-01-04  1185.30   57.60   20.58
    2016-01-05  1150.20   57.20   20.11
                  ...     ...    ...
    2019-05-17   1639.47   61.71  26.56
    2019-05-21   1591.92   62.67  25.40
    2019-05-22   1578.63   59.54  26.51
    2019-05-24   1671.83   60.65  27.56
    2019-06-21   1786.64   66.57  26.84
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_ENERGY_DAILY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["沿海六大电厂库存动态报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df[["沿海六大电库存", "日耗", "存煤可用天数"]]
    temp_df.name = "energy"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-中国-其他-中国人民币汇率中间价报告
def macro_china_rmb():
    """
    中国人民币汇率中间价报告, 数据区间从20170103-至今
    https://datacenter.jin10.com/reportType/dc_rmb_data
    :return: pandas.Series
                美元/人民币_中间价  美元/人民币_涨跌幅  ...  人民币/泰铢_定价  人民币/泰铢_涨跌幅
    2018-02-06      6.3072         NaN  ...     5.0191         NaN
    2018-02-07      6.2882      -190.0  ...     5.0178       -13.0
    2018-02-08      6.2822       -60.0  ...     5.0429       251.0
    2018-02-09      6.3194       372.0  ...     5.0406       -23.0
    2018-02-12      6.3001      -193.0  ...     5.0310       -96.0
                    ...         ...  ...        ...         ...
    2020-04-16      7.0714       312.0  ...     4.6260      -156.0
    2020-04-17      7.0718         4.0  ...     4.6083      -177.0
    2020-04-20      7.0657       -61.0  ...     4.5977      -106.0
    2020-04-21      7.0752        95.0  ...     4.5929       -48.0
    2020-04-22      7.0903       151.0  ...     4.5843       -86.0
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/exchange_rate.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    big_df["美元/人民币_中间价"] = temp_df["美元/人民币"].apply(lambda x: x[0])
    big_df["美元/人民币_涨跌幅"] = temp_df["美元/人民币"].apply(lambda x: x[1])
    big_df["欧元/人民币_中间价"] = temp_df["欧元/人民币"].apply(lambda x: x[0])
    big_df["欧元/人民币_涨跌幅"] = temp_df["欧元/人民币"].apply(lambda x: x[1])
    big_df["100日元/人民币_中间价"] = temp_df["100日元/人民币"].apply(lambda x: x[0])
    big_df["100日元/人民币_涨跌幅"] = temp_df["100日元/人民币"].apply(lambda x: x[1])
    big_df["港元/人民币_中间价"] = temp_df["港元/人民币"].apply(lambda x: x[0])
    big_df["港元/人民币_涨跌幅"] = temp_df["港元/人民币"].apply(lambda x: x[1])
    big_df["英镑/人民币_中间价"] = temp_df["英镑/人民币"].apply(lambda x: x[0])
    big_df["英镑/人民币_涨跌幅"] = temp_df["英镑/人民币"].apply(lambda x: x[1])
    big_df["澳元/人民币_中间价"] = temp_df["澳元/人民币"].apply(lambda x: x[0])
    big_df["澳元/人民币_涨跌幅"] = temp_df["澳元/人民币"].apply(lambda x: x[1])
    big_df["新西兰元/人民币_中间价"] = temp_df["新西兰元/人民币"].apply(lambda x: x[0])
    big_df["新西兰元/人民币_涨跌幅"] = temp_df["新西兰元/人民币"].apply(lambda x: x[1])
    big_df["新加坡元/人民币_中间价"] = temp_df["新加坡元/人民币"].apply(lambda x: x[0])
    big_df["新加坡元/人民币_涨跌幅"] = temp_df["新加坡元/人民币"].apply(lambda x: x[1])
    big_df["瑞郎/人民币_中间价"] = temp_df["瑞郎/人民币"].apply(lambda x: x[0])
    big_df["瑞郎/人民币_涨跌幅"] = temp_df["瑞郎/人民币"].apply(lambda x: x[1])
    big_df["加元/人民币_中间价"] = temp_df["加元/人民币"].apply(lambda x: x[0])
    big_df["加元/人民币_涨跌幅"] = temp_df["加元/人民币"].apply(lambda x: x[1])
    big_df["人民币/马来西亚林吉特_中间价"] = temp_df["人民币/马来西亚林吉特"].apply(lambda x: x[0])
    big_df["人民币/马来西亚林吉特_涨跌幅"] = temp_df["人民币/马来西亚林吉特"].apply(lambda x: x[1])
    big_df["人民币/俄罗斯卢布_中间价"] = temp_df["人民币/俄罗斯卢布"].apply(lambda x: x[0])
    big_df["人民币/俄罗斯卢布_涨跌幅"] = temp_df["人民币/俄罗斯卢布"].apply(lambda x: x[1])
    big_df["人民币/南非兰特_中间价"] = temp_df["人民币/南非兰特"].apply(lambda x: x[0])
    big_df["人民币/南非兰特_涨跌幅"] = temp_df["人民币/南非兰特"].apply(lambda x: x[1])
    big_df["人民币/韩元_中间价"] = temp_df["人民币/韩元"].apply(lambda x: x[0])
    big_df["人民币/韩元_涨跌幅"] = temp_df["人民币/韩元"].apply(lambda x: x[1])
    big_df["人民币/阿联酋迪拉姆_中间价"] = temp_df["人民币/阿联酋迪拉姆"].apply(lambda x: x[0])
    big_df["人民币/阿联酋迪拉姆_涨跌幅"] = temp_df["人民币/阿联酋迪拉姆"].apply(lambda x: x[1])
    big_df["人民币/沙特里亚尔_中间价"] = temp_df["人民币/沙特里亚尔"].apply(lambda x: x[0])
    big_df["人民币/沙特里亚尔_涨跌幅"] = temp_df["人民币/沙特里亚尔"].apply(lambda x: x[1])
    big_df["人民币/匈牙利福林_中间价"] = temp_df["人民币/匈牙利福林"].apply(lambda x: x[0])
    big_df["人民币/匈牙利福林_涨跌幅"] = temp_df["人民币/匈牙利福林"].apply(lambda x: x[1])
    big_df["人民币/波兰兹罗提_中间价"] = temp_df["人民币/波兰兹罗提"].apply(lambda x: x[0])
    big_df["人民币/波兰兹罗提_涨跌幅"] = temp_df["人民币/波兰兹罗提"].apply(lambda x: x[1])
    big_df["人民币/丹麦克朗_中间价"] = temp_df["人民币/丹麦克朗"].apply(lambda x: x[0])
    big_df["人民币/丹麦克朗_涨跌幅"] = temp_df["人民币/丹麦克朗"].apply(lambda x: x[1])
    big_df["人民币/瑞典克朗_中间价"] = temp_df["人民币/瑞典克朗"].apply(lambda x: x[0])
    big_df["人民币/瑞典克朗_涨跌幅"] = temp_df["人民币/瑞典克朗"].apply(lambda x: x[1])
    big_df["人民币/挪威克朗_中间价"] = temp_df["人民币/挪威克朗"].apply(lambda x: x[0])
    big_df["人民币/挪威克朗_涨跌幅"] = temp_df["人民币/挪威克朗"].apply(lambda x: x[1])
    big_df["人民币/土耳其里拉_中间价"] = temp_df["人民币/土耳其里拉"].apply(lambda x: x[0])
    big_df["人民币/土耳其里拉_涨跌幅"] = temp_df["人民币/土耳其里拉"].apply(lambda x: x[1])
    big_df["人民币/墨西哥比索_中间价"] = temp_df["人民币/墨西哥比索"].apply(lambda x: x[0])
    big_df["人民币/墨西哥比索_涨跌幅"] = temp_df["人民币/墨西哥比索"].apply(lambda x: x[1])
    big_df["人民币/泰铢_定价"] = temp_df["人民币/泰铢"].apply(lambda x: x[0])
    big_df["人民币/泰铢_涨跌幅"] = temp_df["人民币/泰铢"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", np.nan))
    big_df = big_df.apply(lambda x: x.replace([None], np.nan))
    big_df.sort_index(inplace=True)
    big_df = big_df.astype("float")
    return big_df


# 金十数据中心-经济指标-中国-其他-深圳融资融券报告
def macro_china_market_margin_sz():
    """
    深圳融资融券报告, 数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sz
    :return: pandas.DataFrame
                   融资买入额(元)       融资余额(元)  融券卖出量(股)    融券余量(股)     融券余额(元)  \
    2010-03-31       684569        670796      4000       3900       70895
    2010-04-08      6713260      14467758      2100       3100       56023
    2010-04-09      9357095      19732998      6700       5400      108362
    2010-04-12     10406563      24813027      2200       1000        8100
    2010-04-15     16607172      47980287      4200       5200       97676
                     ...           ...       ...        ...         ...
    2019-12-12  25190412075  423457288662  29769255  209557883  2504593151
    2019-12-13  29636811209  423422868505  32820867  206092170  2509424768
    2019-12-16  39166060634  428851154451  44000215  217123568  2647520178
    2019-12-17  46930557203  433966722200  40492711  220945538  2750371397
    2019-12-18  41043515833  438511398249  39150376  224554586  2761303194
                   融资融券余额(元)
    2010-03-31        741691
    2010-04-08      14523781
    2010-04-09      19841360
    2010-04-12      24821127
    2010-04-15      48077963
                      ...
    2019-12-12  425961881813
    2019-12-13  425932293273
    2019-12-16  431498674629
    2019-12-17  436717093597
    2019-12-18  441272701443
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/fs_2.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.columns = ["融资买入额", "融资余额", "融券卖出量", "融券余量", "融券余额", "融资融券余额"]
    temp_df.sort_index(inplace=True)
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-中国-其他-上海融资融券报告
def macro_china_market_margin_sh():
    """
    上海融资融券报告, 数据区间从 20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sse
    :return: pandas.DataFrame
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_MARKET_MARGIN_SH_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list_1 = [item["datas"]["总量"][0] for item in json_data["list"]]
    value_list_2 = [item["datas"]["总量"][1] for item in json_data["list"]]
    value_list_3 = [item["datas"]["总量"][2] for item in json_data["list"]]
    value_list_4 = [item["datas"]["总量"][3] for item in json_data["list"]]
    value_list_5 = [item["datas"]["总量"][4] for item in json_data["list"]]
    value_list_6 = [item["datas"]["总量"][5] for item in json_data["list"]]
    value_df = pd.DataFrame(
        [
            value_list_1,
            value_list_2,
            value_list_3,
            value_list_4,
            value_list_5,
            value_list_6,
        ]
    ).T
    value_df.columns = [
        "融资余额",
        "融资买入额",
        "融券余量",
        "融券余额",
        "融券卖出量",
        "融资融券余额",
    ]
    value_df.index = pd.to_datetime(date_list)
    value_df.name = "market_margin_sh"
    value_df.index = pd.to_datetime(value_df.index)
    value_df = value_df.astype(float)

    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "fs",
        "attr_id": "1",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_market_margin_sse",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.DataFrame(r.json()["data"]["values"])
    temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
    temp_df = temp_df.iloc[:, 1:]
    temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][1:]

    for_times = math.ceil(
        int(str((temp_df.index[-1] - value_df.index[-1])).split(" ")[0]) / 20
    )
    big_df = temp_df
    for i in tqdm(range(for_times)):
        params = {
            "max_date": temp_df.index[-1],
            "category": "fs",
            "attr_id": "1",
            "_": str(int(round(t * 1000))),
        }
        r = requests.get(url, params=params, headers=headers)
        temp_df = pd.DataFrame(r.json()["data"]["values"])
        temp_df.index = pd.to_datetime(temp_df.iloc[:, 0])
        temp_df = temp_df.iloc[:, 1:]
        temp_df.columns = [item["name"] for item in r.json()["data"]["keys"]][1:]
        big_df = big_df.append(temp_df)

    value_df = value_df.append(big_df)
    value_df.drop_duplicates(inplace=True)
    value_df.sort_index(inplace=True)
    return value_df


# 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
def macro_china_au_report():
    """
    上海黄金交易所报告, 数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_sge_report
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        "https://cdn.jin10.com/data_center/reports/sge.json", params=params
    )
    json_data = res.json()
    big_df = pd.DataFrame()
    for item in json_data["values"].keys():
        temp_df = pd.DataFrame(json_data["values"][item])
        temp_df["date"] = item
        temp_df.columns = [
            "商品",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "涨跌",
            "涨跌幅",
            "加权平均价",
            "成交量",
            "成交金额",
            "持仓量",
            "交收方向",
            "交收量",
            "日期",
        ]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.index = pd.to_datetime(big_df["日期"])
    del big_df["日期"]
    big_df.sort_index(inplace=True)
    return big_df


# 发改委-中国电煤价格指数-全国综合电煤价格指数
def macro_china_ctci():
    """
    中国电煤价格指数-全国综合电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :return: 20140101-至今的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = "http://59.252.41.60/portal//out/dm?t=1578298533594"
    r = requests.get(url)
    temp_df = pd.Series(r.json()["data"][0])
    temp_df.index = pd.to_datetime(r.json()["periods"])
    temp_df = temp_df.astype(float)
    return temp_df


# 发改委-中国电煤价格指数-各价区电煤价格指数
def macro_china_ctci_detail():
    """
    2019年11月各价区电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :return:
    :rtype:
    """
    url = "http://59.252.41.60/portal//out/dm/list/cebdf627f9c24c22a507e2f2e25e2b43?t=1578298533161"
    res = requests.get(url)
    data_df = pd.DataFrame(res.json()["data"])
    data_df.index = res.json()["names"]
    data_df.columns = ["-", "环比", "上期", "同比", "本期"]
    temp = data_df[["环比", "上期", "同比", "本期"]]
    temp = temp.astype(float)
    return temp


# 发改委-中国电煤价格指数-历史电煤价格指数
def macro_china_ctci_detail_hist(year="2018"):
    """
    历史电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :param year: 2014-2019 年
    :type year: str
    :return: 制定年份的中国电煤价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://59.252.41.60/portal//out/dm/listAll?t=1578299685398"
    params = {
        "CONF_ID": "cebdf627f9c24c22a507e2f2e25e2b43",
        "year": f"{year}",
    }
    res = requests.post(url, data=params)
    data_df = pd.DataFrame(res.json()["data"])
    data_df.columns = res.json()["names"]
    data_df.index = data_df["地区"]
    del data_df["地区"]
    temp_df = data_df
    temp_df = temp_df.astype(float)
    return temp_df


# 中国-利率-贷款报价利率
def macro_china_lpr():
    """
    http://data.eastmoney.com/cjsj/globalRateLPR.html
    LPR品种详细数据
    :return: LPR品种详细数据
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPTA_WEB_RATE",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "p": "1",
        "ps": "2000",
        "st": "TRADE_DATE",
        "sr": "-1",
        "var": "WPuRCBoA",
        "rt": "52826782",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text.strip("var WPuRCBoA=")[:-1])
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.index = pd.to_datetime(temp_df["TRADE_DATE"])
    del temp_df["TRADE_DATE"]
    temp_df = temp_df.astype(float)
    return temp_df


# 中国-新房价指数
def macro_china_new_house_price():
    """
    中国-新房价指数
    http://data.eastmoney.com/cjsj/newhouse.html
    :return: 新房价指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable6451982",
        "type": "GJZB",
        "sty": "XFJLB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "19",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "日期",
        "城市",
        "新建住宅价格指数-环比",
        "新建住宅价格指数-同比",
        "新建住宅价格指数-定基",
        "新建商品住宅价格指数-环比",
        "新建商品住宅价格指数-同比",
        "新建商品住宅价格指数-定基",
        "二手住宅价格指数-环比",
        "二手住宅价格指数-同比",
        "二手住宅价格指数-定基",
    ]
    return temp_df


# 中国-企业景气及企业家信心指数
def macro_china_enterprise_boom_index():
    """
    http://data.eastmoney.com/cjsj/qyjqzs.html
    中国-企业景气及企业家信心指数
    :return: 企业景气及企业家信心指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable6607710",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "季度",
        "企业景气指数-指数",
        "企业景气指数-同比",
        "企业景气指数-环比",
        "企业家信心指数-指数",
        "企业家信心指数-同比",
        "企业家信心指数-环比",
    ]
    return temp_df


# 中国-全国税收收入
def macro_china_national_tax_receipts() -> pd.DataFrame:
    """
    http://data.eastmoney.com/cjsj/nationaltaxreceipts.aspx
    中国-全国税收收入
    :return: 全国税收收入
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable8330863",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = ["季度", "税收收入合计", "较上年同期", "季度环比"]
    return temp_df


def macro_china_new_financial_credit() -> pd.DataFrame:
    """
    中国-新增信贷数据
    http://data.eastmoney.com/cjsj/xzxd.html
    :return: 新增信贷数据
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable4364401",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "7",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = ["月份", "当月", "当月-同比增长", "当月-环比增长", "累计", "累计-同比增长"]
    temp_df["当月-同比增长"] = temp_df["当月-同比增长"].str.replace("%", "")
    temp_df["当月-环比增长"] = temp_df["当月-环比增长"].str.replace("%", "")
    temp_df["累计-同比增长"] = temp_df["累计-同比增长"].str.replace("%", "")
    return temp_df


def macro_china_fx_gold() -> pd.DataFrame:
    """
    东方财富-外汇和黄金储备
    http://data.eastmoney.com/cjsj/hjwh.html
    :return: 外汇和黄金储备
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable3314825",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "16",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "国家外汇储备-数值",
        "国家外汇储备-同比",
        "国家外汇储备-环比",
        "黄金储备-数值",
        "黄金储备-同比",
        "黄金储备-环比",
    ]
    return temp_df


def macro_china_stock_market_cap():
    """
    东方财富-全国股票交易统计表
    http://data.eastmoney.com/cjsj/gpjytj.html
    :return: 全国股票交易统计表
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "2",
        "_": "1608999482942",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "数据日期",
        "发行总股本-上海",
        "发行总股本-深圳",
        "市价总值-上海",
        "市价总值-深圳",
        "成交金额-上海",
        "成交金额-深圳",
        "成交量-上海",
        "成交量-深圳",
        "A股最高综合股价指数-上海",
        "A股最高综合股价指数-深圳",
        "A股最低综合股价指数-上海",
        "A股最低综合股价指数-深圳",
    ]
    
    return temp_df


def macro_china_money_supply():
    """
    东方财富-货币供应量
    http://data.eastmoney.com/cjsj/hbgyl.html
    :return: 货币供应量
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {"type": "GJZB", "sty": "ZGZB", "p": "1", "ps": "200", "mkt": "11"}
    r = requests.get(url=url, params=params)
    data_text = r.text
    tmp_list = data_text[data_text.find("[") + 2 : -3]
    tmp_list = tmp_list.split('","')
    res_list = []
    for li in tmp_list:
        res_list.append(li.split(","))
    columns = [
        "月份",
        "货币和准货币(M2)数量(亿元)",
        "货币和准货币(M2)同比增长",
        "货币和准货币(M2)环比增长",
        "货币(M1)数量(亿元)",
        "货币(M1)同比增长",
        "货币(M1)环比增长",
        "流通中的现金(M0)数量(亿元)",
        "流通中的现金(M0)同比增长",
        "流通中的现金(M0)环比增长",
    ]
    data_df = pd.DataFrame(res_list, columns=columns)
    data_df['货币和准货币(M2)数量(亿元)'] = pd.to_numeric(data_df['货币和准货币(M2)数量(亿元)'])
    data_df['货币和准货币(M2)同比增长'] = pd.to_numeric(data_df['货币和准货币(M2)同比增长'])
    data_df['货币和准货币(M2)环比增长'] = pd.to_numeric(data_df['货币和准货币(M2)环比增长'])
    data_df['货币(M1)数量(亿元)'] = pd.to_numeric(data_df['货币(M1)数量(亿元)'])
    data_df['货币(M1)同比增长'] = pd.to_numeric(data_df['货币(M1)同比增长'])
    data_df['货币(M1)环比增长'] = pd.to_numeric(data_df['货币(M1)环比增长'])
    data_df['流通中的现金(M0)数量(亿元)'] = pd.to_numeric(data_df['流通中的现金(M0)数量(亿元)'])
    data_df['流通中的现金(M0)同比增长'] = pd.to_numeric(data_df['流通中的现金(M0)同比增长'])
    data_df['流通中的现金(M0)环比增长'] = pd.to_numeric(data_df['流通中的现金(M0)环比增长'])
    return data_df


def macro_china_cpi():
    """
    东方财富-中国居民消费价格指数
    http://data.eastmoney.com/cjsj/cpi.html
    :return: 东方财富-中国居民消费价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "19",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "全国-当月",
        "全国-同比增长",
        "全国-环比增长",
        "全国-累计",
        "城市-当月",
        "城市-同比增长",
        "城市-环比增长",
        "城市-累计",
        "农村-当月",
        "农村-同比增长",
        "农村-环比增长",
        "农村-累计",
    ]
    temp_df['全国-当月'] = pd.to_numeric(temp_df['全国-当月'])
    temp_df['全国-同比增长'] = pd.to_numeric(temp_df['全国-同比增长'])
    temp_df['全国-环比增长'] = pd.to_numeric(temp_df['全国-环比增长'])
    temp_df['全国-累计'] = pd.to_numeric(temp_df['全国-累计'])
    temp_df['城市-当月'] = pd.to_numeric(temp_df['城市-当月'])
    temp_df['城市-同比增长'] = pd.to_numeric(temp_df['城市-同比增长'])
    temp_df['城市-环比增长'] = pd.to_numeric(temp_df['城市-环比增长'])
    temp_df['城市-累计'] = pd.to_numeric(temp_df['城市-累计'])
    temp_df['农村-当月'] = pd.to_numeric(temp_df['农村-当月'])
    temp_df['农村-同比增长'] = pd.to_numeric(temp_df['农村-同比增长'])
    temp_df['农村-环比增长'] = pd.to_numeric(temp_df['农村-环比增长'])
    temp_df['农村-累计'] = pd.to_numeric(temp_df['农村-累计'])
    return temp_df


def macro_china_gdp():
    """
    东方财富-中国国内生产总值
    http://data.eastmoney.com/cjsj/gdp.html
    :return: 东方财富中国国内生产总值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "20",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "季度",
        "国内生产总值-绝对值",
        "国内生产总值-同比增长",
        "第一产业-绝对值",
        "第一产业-同比增长",
        "第二产业-绝对值",
        "第二产业-同比增长",
        "第三产业-绝对值",
        "第三产业-同比增长",
    ]
    temp_df['国内生产总值-绝对值'] = pd.to_numeric(temp_df['国内生产总值-绝对值'])
    temp_df['国内生产总值-同比增长'] = pd.to_numeric(temp_df['国内生产总值-同比增长'])
    temp_df['第一产业-绝对值'] = pd.to_numeric(temp_df['第一产业-绝对值'])
    temp_df['第一产业-同比增长'] = pd.to_numeric(temp_df['第一产业-同比增长'])
    temp_df['第二产业-绝对值'] = pd.to_numeric(temp_df['第二产业-绝对值'])
    temp_df['第二产业-同比增长'] = pd.to_numeric(temp_df['第二产业-同比增长'])
    temp_df['第三产业-绝对值'] = pd.to_numeric(temp_df['第三产业-绝对值'])
    temp_df['第三产业-同比增长'] = pd.to_numeric(temp_df['第三产业-同比增长'])
    return temp_df


def macro_china_ppi():
    """
    东方财富-中国工业品出厂价格指数
    http://data.eastmoney.com/cjsj/ppi.html
    :return: 东方财富中国工业品出厂价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable6912149",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "22",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = ["月份", "当月", "当月同比增长", "累计"]
    return temp_df


def macro_china_pmi():
    """
    东方财富-中国采购经理人指数
    http://data.eastmoney.com/cjsj/pmi.html
    :return: 东方财富中国采购经理人指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "21",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "制造业-指数",
        "制造业-同比增长",
        "非制造业-指数",
        "非制造业-同比增长",
    ]
    temp_df['制造业-指数'] = pd.to_numeric(temp_df['制造业-指数'])
    temp_df['制造业-同比增长'] = pd.to_numeric(temp_df['制造业-同比增长'])
    temp_df['非制造业-指数'] = pd.to_numeric(temp_df['非制造业-指数'])
    temp_df['非制造业-同比增长'] = pd.to_numeric(temp_df['非制造业-同比增长'])
    return temp_df


def macro_china_gdzctz():
    """
    东方财富-中国城镇固定资产投资
    http://data.eastmoney.com/cjsj/gdzctz.html
    :return: 东方财富中国城镇固定资产投资
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable1891672",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "12",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "自年初累计",
    ]
    return temp_df


def macro_china_hgjck():
    """
    东方财富-海关进出口增减情况一览表
    http://data.eastmoney.com/cjsj/hgjck.html
    :return: 东方财富-海关进出口增减情况一览表
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable938186",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月出口额-金额",
        "当月出口额-同比增长",
        "当月出口额-环比增长",
        "当月进口额-金额",
        "当月进口额-同比增长",
        "当月进口额-环比增长",
        "累计出口额-金额",
        "累计出口额-同比增长",
        "累计进口额-金额",
        "累计进口额-同比增长",
    ]
    return temp_df


def macro_china_czsr():
    """
    东方财富-财政收入
    http://data.eastmoney.com/cjsj/czsr.html
    :return: 东方财富-财政收入
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable5011006",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "14",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长",
    ]
    return temp_df


def macro_china_whxd():
    """
    东方财富-外汇贷款数据
    http://data.eastmoney.com/cjsj/whxd.html
    :return: 东方财富-外汇贷款数据
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable8618737",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "17",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    return temp_df


def macro_china_wbck():
    """
    东方财富-本外币存款
    http://data.eastmoney.com/cjsj/wbck.html
    :return: 东方财富-本外币存款
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "cb": "datatable3653904",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "18",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    return temp_df


def macro_china_hb():
    """
    中国-货币净投放与净回笼
    http://www.chinamoney.com.cn/chinese/hb/
    :return: 货币净投放与净回笼
    :rtype: pandas.DataFrame
    """
    current_year = datetime.today().year
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bond-publish/TicketPutAndBackStatByWeek"
    params = {
        "t": "1597986289666",
        "t": "1597986289666",
    }
    big_df = pd.DataFrame()
    for year in tqdm(range(1997, current_year + 1)):
        payload = {
            "startWeek": f"{year}-01",
            "endWeek": f"{year}-52",
            "pageSize": "5000",
            "pageNo": "1",
        }
        r = requests.post(url, params=params, data=payload)
        page_num = r.json()["data"]["pageTotal"]
        for page in range(1, page_num + 1):
            payload = {
                "startWeek": f"{year}-01",
                "endWeek": f"{year}-52",
                "pageSize": "5000",
                "pageNo": str(page),
            }
            r = requests.post(url, params=params, data=payload)
            temp_df = pd.DataFrame(r.json()["data"]["resultList"])
            big_df = big_df.append(temp_df, ignore_index=True)
            # print(big_df)
    big_df = big_df.sort_values(by=["startDate"])
    big_df.reset_index(inplace=True, drop=True)
    big_df.columns = ["start_date", "net_put_in", "back", "end_date", "put_in", "date"]
    return big_df


def macro_china_gksccz():
    """
    中国-央行公开市场操作
    http://www.chinamoney.com.cn/chinese/yhgkscczh/
    :return: 央行公开市场操作
    :rtype: pandas.DataFrame
    """
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bond-publish/TicketHandle"
    params = {
        "t": "1597986289666",
        "t": "1597986289666",
    }
    big_df = pd.DataFrame()
    payload = {
        "pageSize": "1000",
        "pageNo": "1",
    }
    r = requests.post(url, params=params, data=payload)
    page_num = r.json()["data"]["pageTotal"]
    for page in tqdm(range(1, page_num + 1)):
        payload = {
            "pageSize": "1000",
            "pageNo": str(page),
        }
        r = requests.post(url, params=params, data=payload)
        temp_df = pd.DataFrame(r.json()["data"]["resultList"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df = big_df.sort_values(by=["operationFromDate"])
    big_df.reset_index(inplace=True, drop=True)
    big_df.columns = [
        "rate",
        "trading_method",
        "deal_amount",
        "period",
        "operation_from_date",
    ]
    return big_df


def macro_china_bond_public():
    """
    中国-债券信息披露-债券发行
    http://www.chinamoney.com.cn/chinese/xzjfx/
    :return: 债券发行
    :rtype: pandas.DataFrame
    """
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bond-an/bnBondEmit"
    payload = {
        "enty": "",
        "bondType": "",
        "bondNameCode": "",
        "leadUnderwriter": "",
        "pageNo": "1",
        "pageSize": "1000",
        "limit": "1",
    }
    r = requests.post(url, data=payload)
    big_df = pd.DataFrame(r.json()["records"])
    big_df.columns = [
        "issue_price",
        "emit_enty",
        "coupon_type",
        "plnd_issue_vlmn_str",
        "issue_price_str",
        "issue_date",
        "bond_type",
        "plnd_issue_vlmn",
        "bond_name",
        "bond_code",
        "rtng_shrt",
        "bond_period",
        "defined_code",
    ]
    return big_df


def macro_china_xfzxx():
    """
    消费者信心指数
    https://data.eastmoney.com/cjsj/xfzxx.html
    :return: 消费者信心指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        'type': 'GJZB',
        'sty': 'ZGZB',
        'js': '({data:[(x)],pages:(pc)})',
        'p': '1',
        'ps': '2000',
        'mkt': '4',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1625824314514',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(',') for item in data_json['data']])
    temp_df.columns = [
        '月份',
        '消费者信心指数-指数值',
        '消费者信心指数-同比增长',
        '消费者信心指数-环比增长',
        '消费者满意指数-指数值',
        '消费者满意指数-同比增长',
        '消费者满意指数-环比增长',
        '消费者预期指数-指数值',
        '消费者预期指数-同比增长',
        '消费者预期指数-环比增长',
    ]
    temp_df['消费者信心指数-指数值'] = pd.to_numeric(temp_df['消费者信心指数-指数值'])
    temp_df['消费者信心指数-同比增长'] = pd.to_numeric(temp_df['消费者信心指数-同比增长'])
    temp_df['消费者信心指数-环比增长'] = pd.to_numeric(temp_df['消费者信心指数-环比增长'])
    temp_df['消费者满意指数-指数值'] = pd.to_numeric(temp_df['消费者满意指数-指数值'])
    temp_df['消费者满意指数-同比增长'] = pd.to_numeric(temp_df['消费者满意指数-同比增长'])
    temp_df['消费者满意指数-环比增长'] = pd.to_numeric(temp_df['消费者满意指数-环比增长'])
    temp_df['消费者预期指数-指数值'] = pd.to_numeric(temp_df['消费者满意指数-指数值'])
    temp_df['消费者预期指数-同比增长'] = pd.to_numeric(temp_df['消费者预期指数-同比增长'])
    temp_df['消费者预期指数-环比增长'] = pd.to_numeric(temp_df['消费者预期指数-环比增长'])
    return temp_df


def macro_china_gyzjz():
    """
    工业增加值增长
    https://data.eastmoney.com/cjsj/gyzjz.html
    :return: 工业增加值增长
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        'type': 'GJZB',
        'sty': 'ZGZB',
        'js': '({data:[(x)],pages:(pc)})',
        'p': '1',
        'ps': '2000',
        'mkt': '0',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1625824314514',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(',') for item in data_json['data']])
    temp_df.columns = [
        '月份',
        '同比增长',
        '累计增长',
    ]
    temp_df['同比增长'] = pd.to_numeric(temp_df['同比增长'])
    temp_df['累计增长'] = pd.to_numeric(temp_df['累计增长'])
    return temp_df


def macro_china_reserve_requirement_ratio():
    """
    存款准备金率
    https://data.eastmoney.com/cjsj/ckzbj.html
    :return: 存款准备金率
    :rtype: pandas.DataFrame
    """
    url = "https://data.eastmoney.com/DataCenter_V3/Chart/cjsj/reserverequirementratio.ashx"
    params = {
        "r": "0.12301106148653584",
        "isxml": "false",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        [
            ["20" + item for item in data_json["X"].split(",")],
            [item for item in data_json["Y"][0].split(",")],
            [item for item in data_json["Y"][1].split(",")],
        ]
    ).T
    temp_df.columns = ["月份", "大型金融机构-调整后", "中小金融机构-调整后"]
    temp_df = temp_df.astype(
        {
            "大型金融机构-调整后": float,
            "中小金融机构-调整后": float,
        }
    )
    return temp_df


def macro_china_consumer_goods_retail():
    """
    社会消费品零售总额
    http://data.eastmoney.com/cjsj/xfp.html
    :return: 社会消费品零售总额
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        'type': 'GJZB',
        'sty': 'ZGZB',
        'js': '({data:[(x)],pages:(pc)})',
        'p': '1',
        'ps': '2000',
        'mkt': '5',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1625822628225',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(',') for item in data_json['data']])
    temp_df.columns = [
        '月份',
        '当月',
        '同比增长',
        '环比增长',
        '累计',
        '累计-同比增长',
    ]
    temp_df['当月'] = pd.to_numeric(temp_df['当月'])
    temp_df['同比增长'] = pd.to_numeric(temp_df['同比增长'])
    temp_df['环比增长'] = pd.to_numeric(temp_df['环比增长'])
    temp_df['累计'] = pd.to_numeric(temp_df['累计'])
    temp_df['累计-同比增长'] = pd.to_numeric(temp_df['累计-同比增长'])
    return temp_df


def macro_china_society_electricity():
    """
    全社会用电分类情况表
    http://finance.sina.com.cn/mac/#industry-6-0-31-1
    :return: 全社会用电分类情况表
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601557771972/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "6",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601557771972",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in range(1, page_num):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.columns = [
        "统计时间",
        "全社会用电量",
        "全社会用电量同比",
        "各行业用电量合计",
        "各行业用电量合计同比",
        "第一产业用电量",
        "第一产业用电量同比",
        "第二产业用电量",
        "第二产业用电量同比",
        "第三产业用电量",
        "第三产业用电量同比",
        "城乡居民生活用电量合计",
        "城乡居民生活用电量合计同比",
        "城镇居民用电量",
        "城镇居民用电量同比",
        "乡村居民用电量",
        "乡村居民用电量同比",
    ]
    return big_df


def macro_china_society_traffic_volume():
    """
    全社会客货运输量
    http://finance.sina.com.cn/mac/#industry-10-0-31-1
    :return: 全社会客货运输量
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601559094538/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "10",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601557771972",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"]["非累计"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"]["非累计"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_postal_telecommunicational():
    """
    邮电业务基本情况
    http://finance.sina.com.cn/mac/#industry-11-0-31-1
    :return: 邮电业务基本情况
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601624495046/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "11",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"]["非累计"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"]["非累计"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_international_tourism_fx():
    """
    国际旅游外汇收入构成
    http://finance.sina.com.cn/mac/#industry-15-0-31-3
    :return: 国际旅游外汇收入构成
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "15",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_passenger_load_factor():
    """
    民航客座率及载运率
    http://finance.sina.com.cn/mac/#industry-20-0-31-1
    :return: 民航客座率及载运率
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "20",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_freight_index():
    """
    航贸运价指数
    http://finance.sina.com.cn/mac/#industry-22-0-31-2
    :return: 航贸运价指数
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "industry",
        "event": "22",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_central_bank_balance():
    """
    央行货币当局资产负债
    http://finance.sina.com.cn/mac/#fininfo-8-0-31-2
    :return: 央行货币当局资产负债
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "8",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_insurance():
    """
    保险业经营情况
    http://finance.sina.com.cn/mac/#fininfo-19-0-31-3
    :return: 保险业经营情况
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "19",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_supply_of_money():
    """
    货币供应量
    http://finance.sina.com.cn/mac/#fininfo-1-0-31-1
    :return: 货币供应量
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "1",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_swap_rate(
    start_date: str = "2020-09-06", end_date: str = "2020-10-06"
) -> pd.DataFrame:
    """
    FR007利率互换曲线历史数据
    http://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007
    :param start_date: 开始日期, 开始和结束日期不得超过一个月
    :type start_date: str
    :param end_date: 结束日期, 开始和结束日期不得超过一个月
    :type end_date: str
    :return: FR007利率互换曲线历史数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bk-shibor/IfccHis"
    params = {
        "cfgItemType": "72",
        "interestRateType": "0",
        "startDate": start_date,
        "endDate": end_date,
        "bidAskType": "",
        "lang": "CN",
        "quoteTime": "全部",
        "pageSize": "5000",
        "pageNum": "1",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "_",
        "_",
        "_",
        "曲线名称",
        "时刻",
        "data",
        "日期",
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
        "价格类型",
    ]
    temp_df = temp_df[
        [
            "日期",
            "曲线名称",
            "时刻",
            "价格类型",
            "data",
        ]
    ]
    inner_df = pd.DataFrame([item for item in temp_df["data"]])
    inner_df.columns = data_json["data"]["bigthRowName"]
    big_df = pd.concat([temp_df, inner_df], axis=1)
    del big_df["data"]
    return big_df


def macro_china_foreign_exchange_gold():
    """
    央行黄金和外汇储备
    http://finance.sina.com.cn/mac/#fininfo-5-0-31-2
    :return: 央行黄金和外汇储备
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "fininfo",
        "event": "5",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_retail_price_index():
    """
    商品零售价格指数
    http://finance.sina.com.cn/mac/#price-12-0-31-1
    :return: 商品零售价格指数
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/mac/api/jsonp_v3.php/SINAREMOTECALLCALLBACK1601651495761/MacPage_Service.get_pagedata"
    params = {
        "cate": "price",
        "event": "12",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df


def macro_china_real_estate():
    """
    国房景气指数
    http://data.eastmoney.com/cjsj/hyzs_list_EMM00121987.html
    :return: 国房景气指数
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "callback": "jQuery1123007722026081503319_1603084293192",
        "st": "DATADATE",
        "sr": "-1",
        "ps": "1000",
        "p": "1",
        "type": "HYZS_All",
        "js": '({data:dataDistinc((x),"DATADATE"),pages:(tp)})',
        "filter": "(ID='EMM00121987')",
        "token": "894050c76af8597a853f5b408b759f5d",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("[") : data_text.rfind("]") + 1])
    temp_df = pd.DataFrame([item for item in data_json])
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
        "_",
        "_",
        "_",
        "_",
        "地区",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "日期",
            "最新值",
            "涨跌幅",
            "近3月涨跌幅",
            "近6月涨跌幅",
            "近1年涨跌幅",
            "近2年涨跌幅",
            "近3年涨跌幅",
            "地区",
        ]
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"])
    return temp_df


if __name__ == "__main__":
    # 企业商品价格指数
    macro_china_qyspjg_df = macro_china_qyspjg()
    print(macro_china_qyspjg_df)
    # 外商直接投资数据
    macro_china_fdi_df = macro_china_fdi()
    print(macro_china_fdi_df)
    # 社会融资规模增量
    macro_china_shrzgm_df = macro_china_shrzgm()
    print(macro_china_shrzgm_df)
    # 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
    macro_china_gdp_yearly_df = macro_china_gdp_yearly()
    print(macro_china_gdp_yearly_df)
    # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
    macro_china_cpi_yearly_df = macro_china_cpi_yearly()
    print(macro_china_cpi_yearly_df)
    # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI月率报告
    macro_china_cpi_monthly_df = macro_china_cpi_monthly()
    print(macro_china_cpi_monthly_df)
    # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
    macro_china_ppi_yearly_df = macro_china_ppi_yearly()
    print(macro_china_ppi_yearly_df)
    # 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
    macro_china_exports_yoy_df = macro_china_exports_yoy()
    print(macro_china_exports_yoy_df)
    # 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
    macro_china_imports_yoy_df = macro_china_imports_yoy()
    print(macro_china_imports_yoy_df)
    # 金十数据中心-经济指标-中国-贸易状况-以美元计算贸易帐(亿美元)
    macro_china_trade_balance_df = macro_china_trade_balance()
    print(macro_china_trade_balance_df)
    # 金十数据中心-经济指标-中国-产业指标-规模以上工业增加值年率
    macro_china_industrial_production_yoy_df = macro_china_industrial_production_yoy()
    print(macro_china_industrial_production_yoy_df)
    # 金十数据中心-经济指标-中国-产业指标-官方制造业PMI
    macro_china_pmi_yearly_df = macro_china_pmi_yearly()
    print(macro_china_pmi_yearly_df)
    # 金十数据中心-经济指标-中国-产业指标-财新制造业PMI终值
    macro_china_cx_pmi_yearly_df = macro_china_cx_pmi_yearly()
    print(macro_china_cx_pmi_yearly_df)
    # 金十数据中心-经济指标-中国-产业指标-财新服务业PMI
    macro_china_cx_services_pmi_yearly_df = macro_china_cx_services_pmi_yearly()
    print(macro_china_cx_services_pmi_yearly_df)
    # 金十数据中心-经济指标-中国-产业指标-中国官方非制造业PMI
    macro_china_non_man_pmi_df = macro_china_non_man_pmi()
    print(macro_china_non_man_pmi_df)
    # 金十数据中心-经济指标-中国-金融指标-外汇储备(亿美元)
    macro_china_fx_reserves_yearly_df = macro_china_fx_reserves_yearly()
    print(macro_china_fx_reserves_yearly_df)
    # 金十数据中心-经济指标-中国-金融指标-M2货币供应年率
    macro_china_m2_yearly_df = macro_china_m2_yearly()
    print(macro_china_m2_yearly_df)
    # 金十数据中心-经济指标-中国-金融指标-上海银行业同业拆借报告
    macro_china_shibor_all_df = macro_china_shibor_all()
    print(macro_china_shibor_all_df)
    # 金十数据中心-经济指标-中国-金融指标-人民币香港银行同业拆息
    macro_china_hk_market_info_df = macro_china_hk_market_info()
    print(macro_china_hk_market_info_df)
    # 金十数据中心-经济指标-中国-其他-中国日度沿海六大电库存数据
    macro_china_daily_energy_df = macro_china_daily_energy()
    print(macro_china_daily_energy_df)
    # 金十数据中心-经济指标-中国-其他-中国人民币汇率中间价报告
    macro_china_rmb_df = macro_china_rmb()
    print(macro_china_rmb_df)
    # 金十数据中心-经济指标-中国-其他-深圳融资融券报告
    macro_china_market_margin_sz_df = macro_china_market_margin_sz()
    print(macro_china_market_margin_sz_df)
    # 金十数据中心-经济指标-中国-其他-上海融资融券报告
    macro_china_market_margin_sh_df = macro_china_market_margin_sh()
    print(macro_china_market_margin_sh_df)
    # 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
    macro_china_au_report_df = macro_china_au_report()
    print(macro_china_au_report_df)

    # 发改委-中国电煤价格指数-全国综合电煤价格指数
    macro_china_ctci_df = macro_china_ctci()
    print(macro_china_ctci_df)
    # 发改委-中国电煤价格指数-各价区电煤价格指数
    macro_china_ctci_detail_df = macro_china_ctci_detail()
    print(macro_china_ctci_detail_df)
    # 发改委-中国电煤价格指数-历史电煤价格指数
    macro_china_ctci_detail_hist_df = macro_china_ctci_detail_hist()
    print(macro_china_ctci_detail_hist_df)

    # 中国-新房价指数
    macro_china_new_house_price_df = macro_china_new_house_price()
    print(macro_china_new_house_price_df)

    # 中国-企业景气及企业家信心指数
    macro_china_enterprise_boom_index_df = macro_china_enterprise_boom_index()
    print(macro_china_enterprise_boom_index_df)

    # 中国-全国税收收入
    macro_china_national_tax_receipts_df = macro_china_national_tax_receipts()
    print(macro_china_national_tax_receipts_df)

    # 中国-新增信贷数据
    macro_china_new_financial_credit_df = macro_china_new_financial_credit()
    print(macro_china_new_financial_credit_df)

    # 中国-外汇和黄金储备
    macro_china_fx_gold_df = macro_china_fx_gold()
    print(macro_china_fx_gold_df)

    macro_china_stock_market_cap_df = macro_china_stock_market_cap()
    print(macro_china_stock_market_cap_df)

    macro_china_money_supply_df = macro_china_money_supply()
    print(macro_china_money_supply_df)

    macro_china_cpi_df = macro_china_cpi()
    print(macro_china_cpi_df)

    macro_china_gdp_df = macro_china_gdp()
    print(macro_china_gdp_df)

    macro_china_ppi_df = macro_china_ppi()
    print(macro_china_ppi_df)

    macro_china_pmi_df = macro_china_pmi()
    print(macro_china_pmi_df)

    macro_china_gdzctz_df = macro_china_gdzctz()
    print(macro_china_gdzctz_df)

    macro_china_hgjck_df = macro_china_hgjck()
    print(macro_china_hgjck_df)

    macro_china_czsr_df = macro_china_czsr()
    print(macro_china_czsr_df)

    macro_china_whxd_df = macro_china_whxd()
    print(macro_china_whxd_df)

    macro_china_wbck_df = macro_china_wbck()
    print(macro_china_wbck_df)

    macro_china_hb_df = macro_china_hb()
    print(macro_china_hb_df)

    macro_china_gksccz_df = macro_china_gksccz()
    print(macro_china_gksccz_df)

    macro_china_bond_public_df = macro_china_bond_public()
    print(macro_china_bond_public_df)

    macro_china_xfzxx_df = macro_china_xfzxx()
    print(macro_china_xfzxx_df)

    macro_china_gyzjz_df = macro_china_gyzjz
    print(macro_china_gyzjz_df)

    macro_china_reserve_requirement_ratio_df = macro_china_reserve_requirement_ratio()
    print(macro_china_reserve_requirement_ratio_df)

    macro_china_consumer_goods_retail_df = macro_china_consumer_goods_retail()
    print(macro_china_consumer_goods_retail_df)

    macro_china_society_electricity_df = macro_china_society_electricity()
    print(macro_china_society_electricity_df)

    macro_china_society_traffic_volume_df = macro_china_society_traffic_volume()
    print(macro_china_society_traffic_volume_df)

    macro_china_postal_telecommunicational_df = macro_china_postal_telecommunicational()
    print(macro_china_postal_telecommunicational_df)

    macro_china_international_tourism_fx_df = macro_china_international_tourism_fx()
    print(macro_china_international_tourism_fx_df)

    macro_china_passenger_load_factor_df = macro_china_passenger_load_factor()
    print(macro_china_passenger_load_factor_df)

    macro_china_freight_index_df = macro_china_freight_index()
    print(macro_china_freight_index_df)

    macro_china_central_bank_balance_df = macro_china_central_bank_balance()
    print(macro_china_central_bank_balance_df)

    macro_china_insurance_df = macro_china_insurance()
    print(macro_china_insurance_df)

    macro_china_supply_of_money_df = macro_china_supply_of_money()
    print(macro_china_supply_of_money_df)

    macro_china_swap_rate_df = macro_china_swap_rate(
        start_date="2020-09-06", end_date="2020-10-06"
    )
    print(macro_china_swap_rate_df)

    macro_china_foreign_exchange_gold_df = macro_china_foreign_exchange_gold()
    print(macro_china_foreign_exchange_gold_df)

    macro_china_retail_price_index_df = macro_china_retail_price_index()
    print(macro_china_retail_price_index_df)

    macro_china_real_estate_df = macro_china_real_estate()
    print(macro_china_real_estate_df)
