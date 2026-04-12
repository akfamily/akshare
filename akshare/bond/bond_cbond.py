# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2026/4/10 19:00
Desc: 中国债券信息网-中债指数-中债指数族系-总指数-综合类指数
"""

import pandas as pd
import requests

from akshare.bond.cons import INDEX_MAPPING, PERIOD_MAPPING, INDICATOR_MAPPING


def bond_available_index_cbond():
    """
    中国债券信息网-中债指数-中债指数族系 当中， 非指定期限部分
    https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult
    :return: 可选项列表
    :rtype: list
    """
    temp_df = pd.DataFrame(list(INDEX_MAPPING.keys()))
    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df['index'] + 1
    temp_df.columns = ['index', 'value']
    return temp_df


def bond_index_general_cbond(
    index_category: str = "新综合指数", indicator: str = "全价", period: str = "总值"
):
    """
    中国债券信息网-中债指数-中债指数族系
    https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult
    :param index_category: see result of available_bond_index()
    :type index_category: str
    :param indicator: choice of {"全价", "净价", "财富", "平均市值法久期", "平均现金流法久期", "平均市值法凸性", "平均现金流法凸性", "平均现金流法到期收益率", "平均市值法到期收益率", "平均基点价值", "平均待偿期", "平均派息率", "指数上日总市值", "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅", "现券结算量"}
    :type indicator: str
    :param period: choice of {"总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上", "0-3个月", "3-6个月", "6-9个月", "9-12个月", "0-6个月", "6-12个月"}
    :type period: str
    :return: 指定指数的指定指标的指定期限分段数据
    :rtype: pandas.DataFrame
    """
    url = "https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult"
    params = {
        "indexid": INDEX_MAPPING[index_category],
        "qxlxt": PERIOD_MAPPING[period],
        "ltcslx": "",
        "zslxt": INDICATOR_MAPPING[indicator],
        "zslxt1": INDICATOR_MAPPING[indicator],
        "lx": "1",
        "locale": "zh_CN",
    }
    r = requests.post(url, params=params)
    raw_json = r.json()
    key_col_map = {f"{INDICATOR_MAPPING[indicator]}_{p_code}": freq_col for p_code, freq_col in
                   raw_json['dqcName'].items()}
    data_json = {key: raw_json[key] for key in key_col_map}
    temp_df = pd.DataFrame.from_dict(data_json, orient="columns")
    temp_df.index = pd.to_datetime(pd.to_numeric(temp_df.index), unit="ms", utc=True).tz_convert("Asia/Shanghai")
    temp_df.index.name = "date"
    temp_df.rename(columns=key_col_map, inplace=True)
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["date", "value"]
    temp_df['date'] = pd.to_datetime(temp_df['date'], errors="coerce").dt.date
    return temp_df


def bond_treasury_index_cbond(
    indicator: str = "财富", period: str = "5Y"
) -> pd.DataFrame:
    """
    中国债券信息网-中债指数-中债指数族系-总指数-综合类指数-中债-国债指数
    https://yield.chinabond.com.cn/cbweb-mn/indices/single_index_query
    :param indicator: choice of {"全价", "净价", "财富"}
    :type indicator: str
    :param period: choice of {'0-1Y', '0-3Y', '0-5Y', '0-10Y', '1-3Y', '1-5Y', '1-10Y',
    '3-5Y', '5Y', '7Y', '7-10Y', '10Y', '30Y'}
    :type period: str
    :return: 国债指数
    :rtype: pandas.DataFrame
    """
    mapping = {
        "0-1Y": "8a8b2cef70bc61380170be069828032b",
        "0-3Y": "61f69682dc3ec18fe9664ff59308314a",
        "0-5Y": "0beafb51867009998c2f4932bf22ede3",
        "0-10Y": "8a8b2cef7832f8920178350801470014",
        "1-3Y": "cc1cfe89b0cbd0800420a0e037026407",
        "1-5Y": "7c3110e5305f9301482517066427a554",
        "1-10Y": "a5d90802e3259978a027267de651106d",
        "3-5Y": "8a8b2ca04bf69582014c10b60f376c77",
        "5Y": "8a8b2ca03a3feea1013a44b98fc533f5",
        "7Y": "2c9081e50e8767dc010e87b6e26c0080",
        "7-10Y": "8a8b2c8f5a492a01015a4ac986480043",
        "10Y": "8a8b2ca04b666362014b723482bc4f49",
        "30Y": "8a8b2cef77b239980177b485d20a6379",
    }
    url = "https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQueryResult"
    params = {
        "indexid": mapping[period],
        "qxlxt": "00",
        "ltcslx": "",
        "zslxt": INDICATOR_MAPPING[indicator],
        "zslxt1": INDICATOR_MAPPING[indicator],
        "lx": "1",
        "locale": "zh_CN",
    }
    r = requests.post(url, params=params)
    raw_json = r.json()
    key_col_map = {f"{INDICATOR_MAPPING[indicator]}_{p_code}": freq_col for p_code, freq_col in
                   raw_json['dqcName'].items()}
    data_json = {key: raw_json[key] for key in key_col_map}
    temp_df = pd.DataFrame.from_dict(data_json, orient="columns")
    temp_df.index = pd.to_datetime(pd.to_numeric(temp_df.index), unit="ms", utc=True).tz_convert("Asia/Shanghai")
    temp_df.index.name = "date"
    temp_df.rename(columns=key_col_map, inplace=True)
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["date", "value"]
    temp_df['date'] = pd.to_datetime(temp_df['date'], errors="coerce").dt.date
    return temp_df


def bond_new_composite_index_cbond(
    indicator: str = "财富", period: str = "总值"
) -> pd.DataFrame:
    """
    中国债券信息网-中债指数-中债指数族系-总指数-综合类指数-中债-新综合指数
    https://yield.chinabond.com.cn/cbweb-mn/indices/single_index_query
    :param indicator: choice of {"全价", "净价", "财富", "平均市值法久期", "平均现金流法久期", "平均市值法凸性",
    "平均现金流法凸性", "平均现金流法到期收益率", "平均市值法到期收益率", "平均基点价值", "平均待偿期", "平均派息率",
    "指数上日总市值", "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅", "现券结算量"}
    :type indicator: str
    :param period: choice of {"总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上", "0-3个月",
    "3-6个月", "6-9个月", "9-12个月", "0-6个月", "6-12个月"}
    :type period: str
    :return: 新综合指数
    :rtype: pandas.DataFrame
    """
    indicator_map = {
        "全价": "QJZS",
        "净价": "JJZS",
        "财富": "CFZS",
        "平均市值法久期": "PJSZFJQ",
        "平均现金流法久期": "PJXJLFJQ",
        "平均市值法凸性": "PJSZFTX",
        "平均现金流法凸性": "PJXJLFTX",
        "平均现金流法到期收益率": "PJDQSYL",
        "平均市值法到期收益率": "PJSZFDQSYL",
        "平均基点价值": "PJJDJZ",
        "平均待偿期": "PJDCQ",
        "平均派息率": "PJPXL",
        "指数上日总市值": "ZSZSZ",
        "财富指数涨跌幅": "CFZSZDF",
        "全价指数涨跌幅": "QJZSZDF",
        "净价指数涨跌幅": "JJZSZDF",
        "现券结算量": "XQJSL",
    }
    period_map = {
        "总值": "00",
        "1年以下": "01",
        "1-3年": "02",
        "3-5年": "03",
        "5-7年": "04",
        "7-10年": "05",
        "10年以上": "06",
        "0-3个月": "07",
        "3-6个月": "08",
        "6-9个月": "09",
        "9-12个月": "10",
        "0-6个月": "11",
        "6-12个月": "12",
    }
    url = "https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQuery"
    params = {
        "indexid": "8a8b2ca0332abed20134ea76d8885831",
        "": "",  # noqa: F601
        "qxlxt": period_map[period],
        "": "",  # noqa: F601
        "ltcslx": "",
        "": "",  # noqa: F601
        "zslxt": indicator_map[indicator],  # noqa: F601
        "": "",  # noqa: F601
        "zslxt": indicator_map[indicator],  # noqa: F601
        "": "",  # noqa: F601
        "lx": "1",
        "": "",  # noqa: F601
        "locale": "",
    }
    r = requests.post(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame.from_dict(
        data_json[f"{indicator_map[indicator]}_{period_map[period]}"],
        orient="index",
    )
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["date", "value"]
    temp_df["date"] = temp_df["date"].astype(float)
    temp_df["date"] = (
        pd.to_datetime(temp_df["date"], unit="ms", errors="coerce", utc=True)
        .dt.tz_convert("Asia/Shanghai")
        .dt.date
    )
    temp_df["value"] = pd.to_numeric(temp_df["value"], errors="coerce")
    return temp_df


def bond_composite_index_cbond(
    indicator: str = "财富", period: str = "总值"
) -> pd.DataFrame:
    """
    中国债券信息网-中债指数-中债指数族系-总指数-综合类指数-中债-综合指数
    https://yield.chinabond.com.cn/cbweb-mn/indices/single_index_query
    :param indicator: choice of {"全价", "净价", "财富", "平均市值法久期", "平均现金流法久期", "平均市值法凸性",
    "平均现金流法凸性", "平均现金流法到期收益率", "平均市值法到期收益率", "平均基点价值", "平均待偿期", "平均派息率",
    "指数上日总市值", "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅", "现券结算量"}
    :type indicator: str
    :param period: choice of {"总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上", "0-3个月",
    "3-6个月", "6-9个月", "9-12个月", "0-6个月", "6-12个月"}
    :type period: str
    :return: 新综合指数
    :rtype: pandas.DataFrame
    """
    indicator_map = {
        "全价": "QJZS",
        "净价": "JJZS",
        "财富": "CFZS",
        "平均市值法久期": "PJSZFJQ",
        "平均现金流法久期": "PJXJLFJQ",
        "平均市值法凸性": "PJSZFTX",
        "平均现金流法凸性": "PJXJLFTX",
        "平均现金流法到期收益率": "PJDQSYL",
        "平均市值法到期收益率": "PJSZFDQSYL",
        "平均基点价值": "PJJDJZ",
        "平均待偿期": "PJDCQ",
        "平均派息率": "PJPXL",
        "指数上日总市值": "ZSZSZ",
        "财富指数涨跌幅": "CFZSZDF",
        "全价指数涨跌幅": "QJZSZDF",
        "净价指数涨跌幅": "JJZSZDF",
        "现券结算量": "XQJSL",
    }
    period_map = {
        "总值": "00",
        "1年以下": "01",
        "1-3年": "02",
        "3-5年": "03",
        "5-7年": "04",
        "7-10年": "05",
        "10年以上": "06",
        "0-3个月": "07",
        "3-6个月": "08",
        "6-9个月": "09",
        "9-12个月": "10",
        "0-6个月": "11",
        "6-12个月": "12",
    }
    url = "https://yield.chinabond.com.cn/cbweb-mn/indices/singleIndexQuery"
    params = {
        "indexid": "2c90818811afed8d0111c0c672b31578",
        "": "",  # noqa: F601
        "qxlxt": period_map[period],
        "": "",  # noqa: F601
        "zslxt": indicator_map[indicator],
        "": "",  # noqa: F601
        "lx": "1",
        "": "",  # noqa: F601
        "locale": "",
    }
    r = requests.post(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame.from_dict(
        data_json[f"{indicator_map[indicator]}_{period_map[period]}"],
        orient="index",
    )
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["date", "value"]
    temp_df["date"] = pd.to_datetime(temp_df["date"].astype(int), errors="coerce", unit="ms").dt.date
    temp_df["value"] = pd.to_numeric(temp_df["value"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    bond_new_composite_index_cbond_df = bond_new_composite_index_cbond(
        indicator="财富", period="总值"
    )
    print(bond_new_composite_index_cbond_df)

    bond_composite_index_cbond_df = bond_composite_index_cbond(
        indicator="财富", period="总值"
    )
    print(bond_composite_index_cbond_df)

    bond_index_general_cbond_df = bond_index_general_cbond(index_category="新综合指数", indicator="全价", period="总值")
    print(bond_index_general_cbond_df)

    bond_treasury_index_cbond_df = bond_treasury_index_cbond(indicator="财富", period="5Y")
    print(bond_treasury_index_cbond_df)
