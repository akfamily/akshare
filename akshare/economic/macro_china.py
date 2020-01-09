# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/21 12:08
contact: jindaxiang@163.com
desc: 获取金十数据-数据中心-中国-中国宏观
首页-价格指数-中价-价格指数-中国电煤价格指数(CTCI)
http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
"""
import json
import time

import pandas as pd
import requests

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
    JS_CHINA_RMB_DAILY_URL,
    JS_CHINA_CX_SERVICE_PMI_YEARLY_URL,
    JS_CHINA_MARKET_MARGIN_SZ_URL,
    JS_CHINA_MARKET_MARGIN_SH_URL,
    JS_CHINA_REPORT_URL,
)


def macro_china_yearly_cpi():
    """
    获取中国年度CPI数据, 数据区间从19860201-至今
    :return: pandas.Series
    1986-02-01    7.1
    1986-03-01    7.1
    1986-04-01    7.1
    1986-05-01    7.1
    1986-06-01    7.1
                 ...
    2019-07-10    2.7
    2019-08-09    2.8
    2019-09-10    2.8
    2019-10-15      3
    2019-11-09      0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CPI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi"
    return temp_df


def macro_china_monthly_cpi():
    """
    获取中国月度CPI数据, 数据区间从19960201-至今
    :return: pandas.Series
    1996-02-01     2.1
    1996-03-01     2.3
    1996-04-01     0.6
    1996-05-01     0.7
    1996-06-01    -0.5
                  ...
    2019-07-10    -0.1
    2019-08-09     0.4
    2019-09-10     0.7
    2019-10-15     0.9
    2019-11-09       0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CPI_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi"
    return temp_df


def macro_china_yearly_m2():
    """
    获取中国年度M2数据, 数据区间从19980201-至今
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
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国M2货币供应年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "m2"
    return temp_df


def macro_china_yearly_ppi():
    """
    获取中国年度PPI数据, 数据区间从19950801-至今
    :return: pandas.Series
    1995-08-01    13.5
    1995-09-01      13
    1995-10-01    12.9
    1995-11-01    12.5
    1995-12-01    11.1
                  ... 
    2019-07-10       0
    2019-08-09    -0.3
    2019-09-10    -0.8
    2019-10-15    -1.2
    2019-11-09       0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_PPI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国PPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "ppi"
    return temp_df


def macro_china_yearly_pmi():
    """
    获取中国年度PMI数据, 数据区间从20050201-至今
    :return: pandas.Series
    2005-02-01    54.7
    2005-03-01    54.5
    2005-04-01    57.9
    2005-05-01    56.7
    2005-06-01    52.9
                  ...
    2019-06-30    49.4
    2019-07-31    49.7
    2019-08-31    49.5
    2019-09-30    49.5
    2019-10-31       0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国官方制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "pmi"
    return temp_df


def macro_china_yearly_gdp():
    """
    获取中国年度GDP数据, 数据区间从20110120-至今
    :return: pandas.Series
    2011-01-20    9.8
    2011-04-15    9.7
    2011-07-13    9.5
    2011-10-18    9.1
    2012-01-17    8.9
    2012-04-13    8.1
    2012-07-13    7.6
    2012-10-18    7.4
    2013-01-18    7.9
    2013-04-15    7.7
    2013-07-15    7.5
    2013-10-18    7.8
    2014-01-20    7.7
    2014-04-16    7.4
    2014-07-16    7.5
    2014-10-21    7.3
    2015-01-20    7.3
    2015-04-15      7
    2015-07-15      7
    2015-10-19    6.9
    2016-01-19    6.8
    2016-04-15    6.7
    2016-07-15    6.7
    2016-10-19    6.7
    2017-01-20    6.8
    2017-04-17    6.9
    2017-07-17    6.9
    2017-10-19    6.8
    2018-01-18    6.8
    2018-04-17    6.8
    2018-07-16    6.7
    2018-10-19    6.5
    2019-01-21    6.4
    2019-04-17    6.4
    2019-07-15    6.2
    2019-10-18      6
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
    return temp_df


def macro_china_yearly_cx_pmi():
    """
    获取中国年度财新PMI数据, 数据区间从20120120-至今
    :return: pandas.Series
    2012-01-20    48.8
    2012-02-22    49.6
    2012-03-22    48.3
    2012-04-23    49.1
    2012-05-02    49.3
                  ...
    2019-07-01    49.4
    2019-08-01    49.9
    2019-09-02    50.4
    2019-09-30    51.4
    2019-11-01       0
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CX_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国财新制造业PMI终值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "cx_pmi"
    return temp_df


def macro_china_yearly_cx_services_pmi():
    """
    获取中国财新服务业PMI报告, 数据区间从20120405-至今
    :return: pandas.Series
    2012-04-05    53.3
    2012-05-04    54.1
    2012-06-05    54.7
    2012-07-04    52.3
    2012-08-03    53.1
                  ...
    2019-08-05    51.6
    2019-09-04    52.1
    2019-10-08    51.3
    2019-11-05    51.1
    2019-12-04    53.5
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_CX_SERVICE_PMI_YEARLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国财新服务业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "cx_services_pmi"
    return temp_df


def macro_china_yearly_fx_reserves():
    """
    获取中国年度外汇储备数据, 数据区间从20140115-至今
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
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国外汇储备报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    temp_df.name = "fx_reserves"
    return temp_df


def macro_china_daily_energy():
    """
    获取中国日度沿海六大电库存数据, 数据区间从20160101-至今
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
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["沿海六大电厂库存动态报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df[["沿海六大电库存", "日耗", "存煤可用天数"]]
    temp_df.name = "energy"
    return temp_df


def macro_china_non_man_pmi():
    """
    获取中国官方非制造业PMI, 数据区间从20160101-至今
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
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国官方非制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "non_pmi"
    return temp_df


def macro_china_rmb():
    """
    获取中国人民币汇率中间价报告, 数据区间从20170103-至今
    :return: pandas.Series
                         美元/人民币            欧元/人民币         100日元/人民币  \
    2017-03-01  [6.8798, 48.00]  [7.2648, 126.00]   [6.0913, 73.00]
    2017-03-02  [6.8798, 48.00]  [7.2648, 126.00]   [6.0913, 73.00]
    2017-03-03  [6.8809, 11.00]  [7.2536, 112.00]  [6.0381, 532.00]
    2017-03-04  [6.8896, 87.00]  [7.2334, 202.00]  [6.0253, 128.00]
    2017-03-05  [6.8896, 87.00]  [7.2334, 202.00]  [6.0253, 128.00]
                         ...               ...               ...
    2019-10-16  [7.0746, 38.00]  [7.8052, 132.00]  [6.5010, 185.00]
    2019-10-17  [7.0789, 43.00]  [7.8405, 353.00]  [6.5111, 101.00]
    2019-10-18  [7.0690, 99.00]  [7.8625, 220.00]   [6.5081, 30.00]
    2019-10-21  [7.0680, 10.00]  [7.8843, 218.00]  [6.5201, 120.00]
    2019-10-22  [7.0668, 12.00]   [7.8802, 41.00]  [6.5055, 146.00]
                          港元/人民币             英镑/人民币            澳元/人民币  \
    2017-03-01   [0.88629, 4.90]   [8.5090, 377.00]  [5.2629, 129.00]
    2017-03-02   [0.88629, 4.90]   [8.5090, 377.00]  [5.2629, 129.00]
    2017-03-03   [0.88638, 0.90]   [8.4521, 569.00]   [5.2723, 94.00]
    2017-03-04  [0.88758, 12.00]    [8.4464, 57.00]  [5.2173, 550.00]
    2017-03-05  [0.88758, 12.00]    [8.4464, 57.00]  [5.2173, 550.00]
                          ...                ...               ...
    2019-10-16   [0.90173, 4.00]  [9.0250, 1141.00]  [4.7759, 114.00]
    2019-10-17   [0.90248, 7.50]   [9.0771, 521.00]   [4.7855, 96.00]
    2019-10-18  [0.90136, 11.20]   [9.0952, 181.00]  [4.8238, 383.00]
    2019-10-21   [0.90136, 0.00]   [9.1193, 241.00]  [4.8416, 178.00]
    2019-10-22   [0.90111, 2.50]   [9.1627, 434.00]  [4.8536, 120.00]
                        新西兰元/人民币
    2017-03-01   [4.9320, 66.00]
    2017-03-02   [4.9320, 66.00]
    2017-03-03  [4.9076, 244.00]
    2017-03-04  [4.8647, 429.00]
    2017-03-05  [4.8647, 429.00]
                          ...
    2019-10-16    [4.4529, 4.00]
    2019-10-17   [4.4539, 10.00]
    2019-10-18  [4.4885, 346.00]
    2019-10-21  [4.5140, 255.00]
    2019-10-22  [4.5305, 165.00]
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_RMB_DAILY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list_1 = [item["datas"]["美元/人民币"] for item in json_data["list"]]
    value_list_2 = [item["datas"]["欧元/人民币"] for item in json_data["list"]]
    value_list_3 = [item["datas"]["100日元/人民币"] for item in json_data["list"]]
    value_list_4 = [item["datas"]["港元/人民币"] for item in json_data["list"]]
    value_list_5 = [item["datas"]["英镑/人民币"] for item in json_data["list"]]
    value_list_6 = [item["datas"]["澳元/人民币"] for item in json_data["list"]]
    value_list_7 = [item["datas"]["新西兰元/人民币"] for item in json_data["list"]]
    value_df = pd.DataFrame(
        [
            value_list_1,
            value_list_2,
            value_list_3,
            value_list_4,
            value_list_5,
            value_list_6,
            value_list_7,
        ]
    ).T
    value_df.columns = [
        "美元/人民币",
        "欧元/人民币",
        "100日元/人民币",
        "港元/人民币",
        "英镑/人民币",
        "澳元/人民币",
        "新西兰元/人民币",
    ]
    value_df.index = pd.to_datetime(date_list)
    value_df.name = "currency"
    return value_df


def macro_market_margin_sz():
    """
    获取深圳融资融券报告, 数据区间从20100331-至今
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
    res = requests.get(
        JS_CHINA_MARKET_MARGIN_SZ_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
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
    value_df.name = "market_margin_sz"
    return value_df


def macro_market_margin_sh():
    """
    获取上海融资融券报告, 数据区间从20100331-至今
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
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
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
    return value_df


def au_report():
    """
    获取上海黄金交易所报告, 数据区间从20100331-至今
    :return: pandas.DataFrame
    格式暂未处理
    """
    t = time.time()
    res = requests.get(
        JS_CHINA_REPORT_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list_1 = pd.DataFrame([item["datas"] for item in json_data["list"]])
    value_list_1.index = pd.to_datetime(date_list)
    return value_list_1


# 发改委
def macro_china_ctci():
    """
    中国电煤价格指数-全国综合电煤价格指数
    http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741
    :return: 20140101-至今的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = "http://59.252.41.60/portal//out/dm?t=1578298533594"
    res = requests.get(url)
    return pd.DataFrame({"date": res.json()["periods"], "value": res.json()["data"][0]})


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
    return data_df[["环比", "上期", "同比", "本期"]]


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
    return data_df


if __name__ == "__main__":
    df = macro_china_yearly_cpi()
    print(df)
    df = macro_china_monthly_cpi()
    print(df)
    df = macro_china_yearly_m2()
    print(df)
    df = macro_china_yearly_ppi()
    print(df)
    df = macro_china_yearly_pmi()
    print(df)
    df = macro_china_yearly_gdp()
    print(df)
    df = macro_china_yearly_cx_pmi()
    print(df)
    df = macro_china_yearly_fx_reserves()
    print(df)
    # 发改委
    macro_china_ctci_df = macro_china_ctci()
    print(macro_china_ctci_df)
    macro_china_ctci_detail_df = macro_china_ctci_detail()
    print(macro_china_ctci_detail_df)
    macro_china_ctci_detail_hist_df = macro_china_ctci_detail_hist()
    print(macro_china_ctci_detail_hist_df)

