# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/8/17 12:08
Desc: 金十数据-数据中心-中国-中国宏观
https://datacenter.jin10.com/economic
首页-价格指数-中价-价格指数-中国电煤价格指数(CTCI)
http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
输出数据格式为 float64
"""
import json
import re
import time

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


# pd.set_option('display.max_rows', 10)  # just for debug


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
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
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
    params = {
        "_": t
    }
    res = requests.get("https://cdn.jin10.com/data_center/reports/il_1.json", params=params)
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
    params = {
        "_": t
    }
    res = requests.get("https://cdn.jin10.com/data_center/reports/il_2.json", params=params)
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
    params = {
        "_": t
    }
    res = requests.get("https://cdn.jin10.com/data_center/reports/exchange_rate.json", params=params)
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
    params = {
        "_": t
    }
    res = requests.get("https://cdn.jin10.com/data_center/reports/fs_2.json", params=params)
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
    上海融资融券报告, 数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sse
    :return: pandas.DataFrame
                        融资买入额(元)      融资余额(元)    融券卖出量(股)      融券余量(股)    融券余额(元)  \
    2010-03-31       5824813      5866316        2900        24142       3100
    2010-04-01       6842114      1054024        2200        17325          0
    2010-04-02       6762781       207516        1500        11929          0
    2010-04-06      10091243      3329461        1400        10267          0
    2010-04-07      25086826     15141395        2800        38418       1400
                      ...          ...         ...          ...        ...
    2019-12-12  544762356034  15711214718  1449227888  10838303677   87173923
    2019-12-13  544431163367  23244118842  1444631533  10983715047  125984881
    2019-12-16  548288053609  27740021378  1453192249  10964588638  113223026
    2019-12-17  551516610507  35126663542  1457433748  11152939293  152548014
    2019-12-18  554466188124  29684776793  1413650473  11107457966  122335778
                   融资融券余额(元)
    2010-03-31       5848955
    2010-04-01       6859439
    2010-04-02       6774710
    2010-04-06      10101510
    2010-04-07      25125244
                      ...
    2019-12-12  555600659711
    2019-12-13  555414878414
    2019-12-16  559252642247
    2019-12-17  562669549800
    2019-12-18  565573646090
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
        "融资余额(元)",
        "融资买入额(元)",
        "融券余量(股)",
        "融券余量金额(元)",
        "融券卖出量(股)",
        "融资融券余额(元)",
    ]
    value_df.index = pd.to_datetime(date_list)
    value_df.name = "market_margin_sh"
    value_df.index = pd.to_datetime(value_df.index)
    value_df = value_df.astype(float)
    return value_df


# 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
def macro_china_au_report():
    """
    上海黄金交易所报告, 数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_sge_report
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {
        "_": t
    }
    res = requests.get("https://cdn.jin10.com/data_center/reports/sge.json", params=params)
    json_data = res.json()
    big_df = pd.DataFrame()
    for item in json_data["values"].keys():
        temp_df = pd.DataFrame(json_data["values"][item])
        temp_df["date"] = item
        temp_df.columns = ['商品', '开盘价', '最高价', '最低价', '收盘价', '涨跌', '涨跌幅', '加权平均价', '成交量', '成交金额', '持仓量', '交收方向', '交收量', "日期"]
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


# 中国-货币-货币供应量
def macro_china_money_supply():
    """
    http://data.eastmoney.com/cjsj/moneysupply.aspx?p=3
    中国货币供应量
    :return: 中国货币供应量
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/moneysupply.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "p": 1,
    }
    r = requests.get(url, params=params, headers=headers)
    page_num = int(re.findall(r"\d", pd.read_html(r.text)[0].iloc[-1, 0])[0]) + 1
    big_df = pd.DataFrame()
    for page in range(1, page_num):
        params = {
            "p": page,
        }
        r = requests.get(url, params=params, headers=headers)
        text_data = r.text
        temp_df = pd.read_html(text_data)[0].iloc[:-1, :-3]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ["月份", "M2-数量", "M2-同比增长", "M2-环比增长", "M1-数量", "M1-同比增长", "M1-环比增长", "M0-数量", "M0-同比增长", "M0-环比增长"]
    return big_df


# 中国-新房价指数
def macro_china_new_house_price():
    """
    http://data.eastmoney.com/cjsj/newhouse.html
    中国-新房价指数
    :return: 新房价指数
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/newhousepriceindex.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "p": 1,
    }
    r = requests.get(url, params=params, headers=headers)
    page_num = int(re.findall(r"\d", pd.read_html(r.text)[0].iloc[-1, 0])[0]) + 1
    big_df = pd.DataFrame()
    for page in range(1, page_num):
        params = {
            "p": page,
        }
        r = requests.get(url, params=params, headers=headers)
        r.encoding = "gb2312"
        text_data = r.text
        temp_df = pd.read_html(text_data)[0].iloc[:-1, :-3]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ["日期", "城市", "新建住宅价格指数-环比", "新建住宅价格指数-同比", "新建住宅价格指数-定基",
                      "新建商品住宅价格指数-环比", "新建商品住宅价格指数-同比", "新建商品住宅价格指数-定基",
                      "二手住宅价格指数-环比", "二手住宅价格指数-同比"]
    return big_df


# 中国-企业景气及企业家信心指数
def macro_china_enterprise_boom_index():
    """
    http://data.eastmoney.com/cjsj/qyjqzs.html
    中国-企业景气及企业家信心指数
    :return: 企业景气及企业家信心指数
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/enterpriseboomindex.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "p": 1,
    }
    r = requests.get(url, params=params, headers=headers)
    page_num = int(re.findall(r"\d", pd.read_html(r.text)[0].iloc[-1, 0])[0]) + 1
    big_df = pd.DataFrame()
    for page in range(1, page_num):
        params = {
            "p": page,
        }
        r = requests.get(url, params=params, headers=headers)
        r.encoding = "gb2312"
        text_data = r.text
        temp_df = pd.read_html(text_data)[0].iloc[:-1, :-6]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ["季度", "企业景气指数-指数", "企业景气指数-同比", "企业景气指数-环比", "企业家信心指数-指数",
                      "企业家信心指数-同比", "企业家信心指数-环比"]
    return big_df


# 中国-全国税收收入
def macro_china_national_tax_receipts() -> pd.DataFrame:
    """
    http://data.eastmoney.com/cjsj/nationaltaxreceipts.aspx
    中国-全国税收收入
    :return: 全国税收收入
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/nationaltaxreceipts.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "p": 1,
    }
    r = requests.get(url, params=params, headers=headers)
    page_num = int(re.findall(r"\d", pd.read_html(r.text)[0].iloc[-1, 0])[0]) + 1
    big_df = pd.DataFrame()
    for page in range(1, page_num):
        params = {
            "p": page,
        }
        r = requests.get(url, params=params, headers=headers)
        r.encoding = "gb2312"
        text_data = r.text
        temp_df = pd.read_html(text_data)[0].iloc[:-1, :-9]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ["季度", "税收收入合计", "较上年同期", "季度环比"]
    return big_df


def macro_china_new_financial_credit() -> pd.DataFrame:
    """
    中国-新增信贷数据
    http://data.eastmoney.com/cjsj/xzxd.html
    :return: 新增信贷数据
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/newfinancialcredit.aspx"
    params = {
        "p": "1",
    }
    r = requests.get(url, params=params)
    raw_total_page_num = pd.read_html(r.text)[-1].dropna(axis=1).iloc[-1, 0]
    total_page_num = int(re.compile(r"\d+").findall(raw_total_page_num)[0])
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page_num+1)):
        params = {
            "p": page,
        }
        r = requests.get(url, params=params)
        temp_df = pd.read_html(r.text)[-1].dropna(axis=1).iloc[:-1, :]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ["月份", "当月", "当月-同比增长", "当月-环比增长", "累计", "累计-同比增长"]
    big_df["当月-同比增长"] = big_df["当月-同比增长"].str.replace("%", "")
    big_df["当月-环比增长"] = big_df["当月-环比增长"].str.replace("%", "")
    big_df["累计-同比增长"] = big_df["累计-同比增长"].str.replace("%", "")
    return big_df


def macro_china_fx_gold() -> pd.DataFrame:
    """
    东方财富-外汇和黄金储备
    http://data.eastmoney.com/cjsj/hjwh.html
    :return: 外汇和黄金储备
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/DataCenter_V3/Chart/cjsj/goldforexreserve.ashx"
    params = {
        "mkt": "99",
        "stat": "17",
        "r": "0.11885134457023705",
        "isxml": "false",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    data_df = pd.DataFrame([data_json["X"].split(","), data_json["Y"][0].split(","), data_json["Y"][1].split(",")]).T
    data_df.columns = ["date", "foreign_exchange_reserve", "gold_reserves"]
    return data_df


def macro_china_cpi():
    """
    东方财富-中国居民消费价格指数
    http://data.eastmoney.com/cjsj/cpi.html
    :return: 东方财富中国居民消费价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/consumerpriceindex.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=2)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/consumerpriceindex.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=2)[-1].iloc[:-1, :])
    big_df.columns = ["月份",
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
    return big_df


def macro_china_gdp():
    """
    东方财富-中国国内生产总值
    http://data.eastmoney.com/cjsj/gdp.html
    :return: 东方财富中国国内生产总值
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/grossdomesticproduct.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=1)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/grossdomesticproduct.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=1)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :9]
    big_df.columns = ["季度",
                      "国内生产总值-绝对值",
                      "国内生产总值-同比增长",
                      "第一产业-绝对值",
                      "第一产业-同比增长",
                      "第二产业-绝对值",
                      "第二产业-同比增长",
                      "第三产业-绝对值",
                      "第三产业-同比增长",
                      ]
    return big_df


def macro_china_ppi():
    """
    东方财富-中国工业品出厂价格指数
    http://data.eastmoney.com/cjsj/ppi.html
    :return: 东方财富中国工业品出厂价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/productpricesindex.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=0)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/productpricesindex.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=0)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :4]
    return big_df


def macro_china_pmi():
    """
    东方财富-中国采购经理人指数
    http://data.eastmoney.com/cjsj/pmi.html
    :return: 东方财富中国采购经理人指数
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/purchasingmanagerindex.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=1)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/purchasingmanagerindex.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=1)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :5]
    big_df.columns = [
        "月份",
        "制造业-指数",
        "制造业-同比增长",
        "非制造业-指数",
        "非制造业-同比增长",
    ]
    return big_df


def macro_china_gdzctz():
    """
    东方财富-中国城镇固定资产投资
    http://data.eastmoney.com/cjsj/gdzctz.html
    :return: 东方财富中国城镇固定资产投资
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/townassetsinvest.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=0)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/townassetsinvest.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=0)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :5]
    big_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "自年初累计",
    ]
    return big_df


def macro_china_hgjck():
    """
    东方财富-海关进出口增减情况一览表
    http://data.eastmoney.com/cjsj/hgjck.html
    :return: 东方财富-海关进出口增减情况一览表
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/importandexport.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=1)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/importandexport.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=1)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :11]
    big_df.columns = [
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
    return big_df


def macro_china_czsr():
    """
    东方财富-财政收入
    http://data.eastmoney.com/cjsj/czsr.html
    :return: 东方财富-财政收入
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/staterevenue.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=0)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/staterevenue.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=0)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :6]
    big_df.columns = [
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长",
    ]
    return big_df


def macro_china_whxd():
    """
    东方财富-外汇贷款数据
    http://data.eastmoney.com/cjsj/whxd.html
    :return: 东方财富-外汇贷款数据
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/foreignexchangeloan.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=0)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/foreignexchangeloan.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=0)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :5]
    big_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    return big_df


def macro_china_wbck():
    """
    东方财富-本外币存款
    http://data.eastmoney.com/cjsj/wbck.html
    :return: 东方财富-本外币存款
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/cjsj/foreigncurrencydeposit.aspx?p=1"
    page_num = int(re.findall(r'\d', pd.read_html(url, header=2)[-1].iloc[-1, 1])[0])
    big_df = pd.read_html(url, header=0)[-1].iloc[:-1, :]
    for page in range(2, page_num+1):
        url = f"http://data.eastmoney.com/cjsj/foreigncurrencydeposit.aspx?p={page}"
        big_df = big_df.append(pd.read_html(url, header=0)[-1].iloc[:-1, :])
    big_df = big_df.iloc[:, :5]
    big_df.columns = [
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    return big_df


if __name__ == "__main__":
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

    # 中国-货币-货币供应量
    macro_china_money_supply_df = macro_china_money_supply()
    print(macro_china_money_supply_df)

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
