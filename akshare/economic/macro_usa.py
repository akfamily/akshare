# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/21 12:08
contact: jindaxiang@163.com
desc: 获取金十数据-数据中心-美国-宏观经济
后续修改为类 --> 去除冗余代码
"""
import json
import time

import pandas as pd
import requests

from akshare.economic.cons import (JS_USA_INTEREST_RATE_URL,
                                   JS_USA_NON_FARM_URL,
                                   JS_USA_UNEMPLOYMENT_RATE_URL,
                                   JS_USA_EIA_CRUDE_URL,
                                   JS_USA_INITIAL_JOBLESS_URL,
                                   JS_USA_CORE_PCE_PRICE_URL,
                                   JS_USA_CPI_MONTHLY_URL,
                                   JS_USA_LMCI_URL,
                                   JS_USA_ADP_NONFARM_URL,
                                   JS_USA_GDP_MONTHLY_URL,
                                   JS_USA_EIA_CRUDE_PRODUCE_URL)


def get_usa_interest_rate():
    """
    获取美联储利率决议报告, 数据区间从19820927-至今
    :return: pandas.Series
    1982-09-27    10.25
    1982-10-01       10
    1982-10-07      9.5
    1982-11-19        9
    1982-12-14      8.5
                  ...
    2019-06-20      2.5
    2019-08-01     2.25
    2019-09-19        2
    2019-10-31        0
    2019-12-12        0
    """
    t = time.time()
    res = requests.get(JS_USA_INTEREST_RATE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国利率决议"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "interest_rate"
    return temp_df


def get_usa_non_farm():
    """
    获取美国非农就业人数报告, 数据区间从19700102-至今
    :return: pandas.Series
    1970-01-02    15.3
    1970-02-06    -6.4
    1970-03-06    12.8
    1970-04-03    14.8
    1970-05-01   -10.4
                  ...
    2019-07-05    19.3
    2019-08-02    15.9
    2019-09-06    16.8
    2019-10-04    13.6
    2019-11-01       0
    """
    t = time.time()
    res = requests.get(JS_USA_NON_FARM_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国非农就业人数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    temp_df.name = "non_farm"
    return temp_df


def get_usa_unemployment_rate():
    """
    获取美国失业率报告, 数据区间从19700101-至今
    :return: pandas.Series
    1970-01-01    3.5
    1970-02-01    3.9
    1970-03-01    4.2
    1970-04-01    4.4
    1970-05-01    4.6
                 ...
    2019-07-05    3.7
    2019-08-02    3.7
    2019-09-06    3.7
    2019-10-04    3.5
    2019-11-01      0
    """
    t = time.time()
    res = requests.get(JS_USA_UNEMPLOYMENT_RATE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国失业率"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "unemployment_rate"
    return temp_df


def get_usa_eia_crude_rate():
    """
    获取美国EIA原油库存报告, 数据区间从19950801-至今
    :return: pandas.Series
    1982-09-01   -262.6
    1982-10-01       -8
    1982-11-01    -41.3
    1982-12-01    -87.6
    1983-01-01     51.3
                  ...
    2019-10-02      310
    2019-10-09    292.7
    2019-10-16        0
    2019-10-17    928.1
    2019-10-23        0
    """
    t = time.time()
    res = requests.get(JS_USA_EIA_CRUDE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国EIA原油库存(万桶)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万桶)"]
    temp_df.name = "eia_crude_rate"
    return temp_df


def get_usa_initial_jobless():
    """
    获取美国初请失业金人数报告, 数据区间从19700101-至今
    :return: pandas.Series
    1970-01-01    22.1087
    1970-02-01    24.9318
    1970-03-01      25.85
    1970-04-01    26.8682
    1970-05-01    33.1591
                   ...
    2019-09-26       21.5
    2019-10-03         22
    2019-10-10         21
    2019-10-17       21.4
    2019-10-24          0
    """
    t = time.time()
    res = requests.get(JS_USA_INITIAL_JOBLESS_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国初请失业金人数(万人)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    temp_df.name = "initial_jobless"
    return temp_df


def get_usa_core_pce_price():
    """
    获取美国核心PCE物价指数年率报告, 数据区间从19700101-至今
    :return: pandas.Series
    1970-01-01    4.8
    1970-02-01    4.7
    1970-03-01    4.8
    1970-04-01    4.7
    1970-05-01    4.7
                 ...
    2019-06-28    1.5
    2019-07-30    1.6
    2019-08-30    1.7
    2019-09-27    1.8
    2019-10-31      0
    """
    t = time.time()
    res = requests.get(JS_USA_CORE_PCE_PRICE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国核心PCE物价指数年率"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "core_pce_price"
    return temp_df


def get_usa_cpi_monthly():
    """
    获取美国CPI月率报告, 数据区间从19700101-至今
    :return: pandas.Series
    1970-01-01    0.5
    1970-02-01    0.5
    1970-03-01    0.5
    1970-04-01    0.5
    1970-05-01    0.5
                 ...
    2019-07-11    0.1
    2019-08-13    0.3
    2019-09-12    0.1
    2019-10-10    0.1
    2019-11-13      0
    """
    t = time.time()
    res = requests.get(JS_USA_CPI_MONTHLY_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国居民消费价格指数(CPI)(月环比)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi_monthly"
    return temp_df


def get_usa_lmci():
    """
    获取美联储劳动力市场状况指数报告, 数据区间从20141006-至今
    :return: pandas.Series
    2014-10-06      4
    2014-11-10    3.9
    2014-12-08    5.5
    2015-01-12    7.3
    2015-02-09    4.9
    2015-03-09      2
    2015-04-06   -1.8
    2015-05-11   -0.5
    2015-06-08    0.9
    2015-07-06    1.4
    2015-08-10    1.8
    2015-09-08    1.2
    2015-10-05    1.3
    2015-11-09    2.2
    2015-12-07    2.7
    2016-01-11    2.3
    2016-02-08   -0.8
    2016-03-07   -2.5
    2016-04-04   -2.1
    2016-05-09   -3.4
    2016-06-06   -3.6
    2016-07-11   -0.1
    2016-08-08      1
    2016-09-06   -1.3
    2016-10-11   -0.1
    2016-11-07    1.4
    2016-12-05    2.1
    2017-01-09    0.6
    2017-02-06    1.3
    2017-03-17    1.5
    2017-04-10    3.6
    2017-05-08    3.5
    2017-06-05      0
    2017-06-16    3.3
    2017-07-10    1.5
    2017-08-07      0
    """
    t = time.time()
    res = requests.get(JS_USA_LMCI_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美联储劳动力市场状况指数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "lmci"
    return temp_df


def get_usa_adp_employment():
    """
    获取美国ADP就业人数报告, 数据区间从20010601-至今
    :return: pandas.Series
    2001-06-01   -17.5
    2001-07-01     -23
    2001-08-01   -20.3
    2001-09-01   -24.6
    2001-10-01   -26.1
                  ...
    2019-07-03    11.2
    2019-07-31    14.2
    2019-09-05    15.7
    2019-10-02    13.5
    2019-10-30       0
    """
    t = time.time()
    res = requests.get(JS_USA_ADP_NONFARM_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国ADP就业人数(万人)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    temp_df.name = "adp"
    return temp_df


def get_usa_gdp_monthly():
    """
    获取美国国内生产总值(GDP)报告, 数据区间从20080228-至今
    :return: pandas.Series
    2008-02-28    0.6
    2008-03-27    0.6
    2008-04-30    0.9
    2008-06-26      1
    2008-07-31    1.9
                 ...
    2019-06-27    3.1
    2019-07-26    2.1
    2019-08-29      2
    2019-09-26      2
    2019-10-30      0
    """
    t = time.time()
    res = requests.get(JS_USA_GDP_MONTHLY_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国国内生产总值(GDP)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "gdp"
    return temp_df


def get_usa_crude_inner():
    """
    获取美国原油产量报告, 数据区间从19830107-至今
    :return: pandas.Series
    1983-01-07     863.40
    1983-01-14     863.40
    1983-01-21     863.40
    1983-01-28     863.40
    1983-02-04     866.00
                   ...
    2019-09-20    1250.00
    2019-09-27    1240.00
    2019-10-04    1260.00
    2019-10-11    1260.00
    2019-10-18    1260.00
    """
    t = time.time()
    res = requests.get(JS_USA_EIA_CRUDE_PRODUCE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国国内原油总量"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["产量(万桶/日)"]
    temp_df.name = "crude_inner"
    return temp_df


def get_usa_crude_state():
    """
    获取美国本土48州原油产量, 数据区间从19830107-至今
    :return: pandas.Series
    1983-01-07       0.00
    1983-01-14       0.00
    1983-01-21       0.00
    1983-01-28       0.00
    1983-02-04       0.00
                   ...
    2019-09-20    1200.00
    2019-09-27    1190.00
    2019-10-04    1210.00
    2019-10-11    1210.00
    2019-10-18    1210.00
    """
    t = time.time()
    res = requests.get(JS_USA_EIA_CRUDE_PRODUCE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国本土48州原油产量"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["产量(万桶/日)"]
    temp_df.name = "crude_state"
    return temp_df


def get_usa_crude_alaska():
    """
    获取美国阿拉斯加州原油产量, 数据区间从19830107-至今
    :return: pandas.Series
    1983-01-07     0.00
    1983-01-14     0.00
    1983-01-21     0.00
    1983-01-28     0.00
    1983-02-04     0.00
                  ...
    2019-09-20    47.20
    2019-09-27    48.00
    2019-10-04    47.30
    2019-10-11    48.50
    2019-10-18    48.50
    """
    t = time.time()
    res = requests.get(JS_USA_EIA_CRUDE_PRODUCE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国阿拉斯加州原油产量"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["产量(万桶/日)"]
    temp_df.name = "crude_alaska"
    return temp_df


if __name__ == "__main__":
    df = get_usa_interest_rate()
    print(df)
    df = get_usa_non_farm()
    print(df)
    df = get_usa_unemployment_rate()
    print(df)
    df = get_usa_eia_crude_rate()
    print(df)


