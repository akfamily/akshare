# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/26 20:34
Desc: 从和讯网获取美股-中概股实时行情数据和历史行情数据(日)
注意: 由于涉及到复权问题, 建议使用新浪的接口来获取历史行情数据(日)
"""
import datetime as dt
import json

import requests
import pandas as pd
from bs4 import BeautifulSoup

from akshare.stock.cons import (url_usa,
                                payload_usa,
                                headers_usa,
                                url_usa_daily,
                                payload_usa_daily)


def stock_us_zh_spot(flag=False):
    """
    获取美股-中概股实时行情数据
    :return: pd.DataFrame
               代码                           名称 最新价(美元)   涨跌幅      最高      最低      昨收  \
    0    NTES                           网易  281.16  0.00  285.80  279.90  282.88
    1    BABA                       阿里巴巴集团  174.30  1.75  175.81  170.88  172.55
    2     CEO                          中海油  155.10  0.03  155.39  153.87  155.07
    3     EDU                          新东方  120.88  0.65  121.98  118.60  120.23
    4    CBPO                         泰邦生物  114.21  0.00  115.00  113.15  114.77
    ..    ...                          ...     ...   ...     ...     ...     ...
    185  SGOC                         上为集团    0.00  0.00    0.00    0.00    1.00
    186  BSPM  Biostar Pharmaceuticals Inc    0.00  0.00    0.00    0.00    0.00
    187  CNTF                         德信无线    0.00  0.00    0.00    0.00    0.22
    188   SPU                         天人果汁    0.00  0.00    0.00    0.00    0.00
    189  ABAC                         奥信天力    0.00  0.00    0.00    0.00    0.00
                成交量
    0     652214.00
    1    8862746.00
    2      70954.00
    3     941155.00
    4      65449.00
    ..          ...
    185        0.00
    186        0.00
    187        0.00
    188        0.00
    189        0.00
    """
    payload_usa_copy = payload_usa.copy()
    payload_usa_copy.update({"time": dt.datetime.now().time().strftime("%H%I%M")})  # 每次更新时间
    res = requests.get(url_usa, params=payload_usa_copy, headers=headers_usa)  # 上传指定参数, 伪装游览器
    data_list = eval(res.text.split("=")[1].strip().rsplit(";")[0])  # eval 出列表
    data_df = pd.DataFrame(data_list,
                           columns=["代码", "名称", "最新价(美元)", "涨跌幅", "d_1", "d_2", "最高", "最低", "昨收", "d_3", "成交量", "d_4"])
    if flag:
        return dict(zip(data_df["名称"], data_df["代码"]))
    return data_df[["代码", "名称", "最新价(美元)", "涨跌幅", "最高", "最低", "昨收", "成交量"]]


def stock_us_zh_daily(code="NTES"):
    """
    获取美股-中概股历史行情数据(日)
    :param code: 参见代码表
    :return: pd.DataFrame
                    时间    前收盘价     开盘价     收盘价     最高价     最低价     成交量
    0   2015-10-28  111.29  111.48  115.00  115.41  111.30   83029
    1   2015-10-29  114.02  113.88  115.47  115.70  113.44  192211
    2   2015-10-30  115.53  112.77  113.67  114.34  111.95  228277
    3   2015-11-02  113.68  111.27  112.77  113.02  110.86  164664
    4   2015-11-03  112.76  114.05  116.26  117.29  114.00  197460
    ..         ...     ...     ...     ...     ...     ...     ...
    995 2019-10-21  150.06  152.70  152.36  153.10  151.95   58136
    996 2019-10-22  152.30  152.35  152.30  153.52  152.14   60558
    997 2019-10-23  152.30  151.25  154.27  154.40  151.25   57467
    998 2019-10-24  154.16  155.56  154.98  156.93  153.96   69055
    999 2019-10-25  155.07  153.91  155.10  155.39  153.87   70954
    """
    hist_headers_usa = headers_usa.copy()  # 复制伪装游览器数据
    hist_headers_usa.update({"Upgrade-Insecure-Requests": "1"})  # 更新游览器头
    hist_headers_usa.update({"Host": "stockdata.stock.hexun.com"})  # 更新游览器头
    res = requests.get("http://stockdata.stock.hexun.com/us/{}.shtml".format(code), headers=hist_headers_usa)
    soup = BeautifulSoup(res.text, "lxml")
    temp_code = soup.find("dl", attrs={"class": "dlDataTit"}).find("small").get_text().split("(")[1].split(")")[
        0].replace(":", "")
    payload_usa_daily.update({"code": temp_code})  # 更新股票代码, e.g., NYSEBABA
    payload_usa_daily.update({"start": dt.datetime.now().strftime("%Y%m%d" + "213000")})  # 更新时间
    res = requests.get(url_usa_daily, params=payload_usa_daily)
    res.encoding = "utf-8"  # 设置编码格式
    data_dict = json.loads(res.text[1:-2])  # 加载非规范 json 数据
    data_df = pd.DataFrame(data_dict["Data"][0],
                           columns=[list(item.values())[0] for item in data_dict["KLine"]])  # 设置数据框
    data_df["时间"] = pd.to_datetime(data_df["时间"].astype(str).str.slice(0, 8))  # 规范化时间
    data_df["前收盘价"] = data_df["前收盘价"] / 100  # 规范化数据
    data_df["开盘价"] = data_df["开盘价"] / 100  # 规范化数据
    data_df["收盘价"] = data_df["收盘价"] / 100  # 规范化数据
    data_df["最高价"] = data_df["最高价"] / 100  # 规范化数据
    data_df["最低价"] = data_df["最低价"] / 100  # 规范化数据
    del data_df["成交额"]  # 删除为空的值
    return data_df


if __name__ == "__main__":
    stock_us_zh_spot_df = stock_us_zh_spot(flag=False)
    print(stock_us_zh_spot_df)
    stock_us_zh_daily_df = stock_us_zh_daily(code="CEO")
    print(stock_us_zh_daily_df)
