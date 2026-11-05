#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/5 18:00
Desc: 乘联会
http://data.cpcadata.com/FuelMarket
"""

import re

import pandas as pd

from akshare.utils import http

# 年份字段形如 "2026年"、"2026年9月"、"2026年 1-9月"，与 "同比" 等字段区分
_YEAR_FIELD = re.compile(r"^\d{4}年")


def _cpca_chart(charttype: str, api: str = "chartlist") -> list:
    """
    乘联会-统计数据-图表数据
    http://data.cpcadata.com/api/chartlist
    :param charttype: 图表类型
    :type charttype: str
    :param api: 接口名；厂商排名的零售数据在 chartlist_2，其余在 chartlist
    :type api: str
    :return: 上游返回的图表列表，每个元素含 category 和 dataList
    :rtype: list
    """
    url = f"http://data.cpcadata.com/api/{api}"
    params = {"charttype": charttype}
    r = http.get(url, params=params)
    return r.json()


def _cpca_table(
    rows: list, key: str, fields: list, value_index: int, label: str
) -> pd.DataFrame:
    """
    把乘联会的 dataList 整理为表格
    :param rows: 上游 dataList，每条记录形如 {"month": "1月", "2026年": [...], ...}
    :type rows: list
    :param key: 行标签字段名，如 "month"、"厂商"、"月份"
    :type key: str
    :param fields: 要输出的数值字段名，按输出顺序排列
    :type fields: list
    :param value_index: 每个字段的数值列表中要取的位置
    :type value_index: int
    :param label: 行标签列在结果中的列名
    :type label: str
    :return: 整理后的表格；记录中缺少的字段（如当年尚未公布的月份）为 NaN
    :rtype: pandas.DataFrame
    """
    data = {label: [row[key] for row in rows]}
    for field in fields:
        data[field] = [
            row[field][value_index] if field in row else None for row in rows
        ]
    temp_df = pd.DataFrame(data)
    temp_df[fields] = temp_df[fields].astype("float64")
    return temp_df


def _cpca_year_table(
    rows: list, key: str, value_index: int, label: str
) -> pd.DataFrame:
    """
    把按年份分列的 dataList 整理为表格，年份列按从早到晚排列
    :param rows: 上游 dataList
    :type rows: list
    :param key: 行标签字段名
    :type key: str
    :param value_index: 每个年份的数值列表中要取的位置
    :type value_index: int
    :param label: 行标签列在结果中的列名
    :type label: str
    :return: 行标签列加各年份列
    :rtype: pandas.DataFrame
    """
    years = sorted({field for row in rows for field in row if _YEAR_FIELD.match(field)})
    return _cpca_table(rows, key, years, value_index, label)


def car_market_total_cpca(
    symbol: str = "狭义乘用车", indicator: str = "产量"
) -> pd.DataFrame:
    """
    乘联会-统计数据-总体市场
    http://data.cpcadata.com/TotalMarket
    :param symbol: choice of {"狭义乘用车", "广义乘用车"}
    :type symbol: str
    :param indicator: choice of {"产量", "批发", "零售", "出口"}
    :type indicator: str
    :return: 统计数据-总体市场
    :rtype: pandas.DataFrame
    """
    indicator_map = {"产量": 0, "批发": 1, "零售": 2, "出口": 3}
    if indicator not in indicator_map:
        return pd.DataFrame()
    data_json = _cpca_chart("1")
    block = 0 if symbol == "狭义乘用车" else 1
    return _cpca_year_table(
        data_json[block]["dataList"],
        key="month",
        value_index=indicator_map[indicator],
        label="月份",
    )


def car_market_man_rank_cpca(
    symbol: str = "狭义乘用车-累计", indicator: str = "批发"
) -> pd.DataFrame:
    """
    乘联会-统计数据-厂商排名
    http://data.cpcadata.com/ManRank
    :param symbol: choice of {"狭义乘用车-单月", "狭义乘用车-累计", "广义乘用车-单月", "广义乘用车-累计"}
    :type symbol: str
    :param indicator: choice of {"批发", "零售"}
    :type indicator: str
    :return: 统计数据-厂商排名
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "狭义乘用车-累计": 0,
        "狭义乘用车-单月": 1,
        "广义乘用车-累计": 2,
        "广义乘用车-单月": 3,
    }
    if symbol not in symbol_map:
        return pd.DataFrame()
    if indicator == "批发":
        data_json = _cpca_chart("2")
        value_index = 0
    else:
        data_json = _cpca_chart("2", api="chartlist_2")
        value_index = 1
    return _cpca_year_table(
        data_json[symbol_map[symbol]]["dataList"],
        key="厂商",
        value_index=value_index,
        label="厂商",
    )


def car_market_cate_cpca(symbol: str = "轿车", indicator: str = "批发") -> pd.DataFrame:
    """
    乘联会-统计数据-车型大类
    http://data.cpcadata.com/CategoryMarket
    :param symbol: choice of {"轿车", "MPV", "SUV", "占比"}
    :type symbol: str
    :param indicator: choice of {"批发", "零售"}
    :type indicator: str
    :return: 统计数据-车型大类
    :rtype: pandas.DataFrame
    """
    symbol_map = {"MPV": 0, "SUV": 1, "轿车": 2, "占比": 3}
    if symbol not in symbol_map:
        return pd.DataFrame()
    data_json = _cpca_chart("3")
    rows = data_json[symbol_map[symbol]]["dataList"]
    if symbol == "占比":
        return _cpca_table(
            rows,
            key="月份",
            fields=["MPV", "SUV", "轿车"],
            value_index=2 if indicator == "批发" else 3,
            label="月份",
        )
    return _cpca_year_table(
        rows, key="month", value_index=1 if indicator == "批发" else 2, label="月份"
    )


def car_market_country_cpca() -> pd.DataFrame:
    """
    乘联会-统计数据-国别细分市场
    http://data.cpcadata.com/CountryMarket
    :return: 统计数据-车型大类
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcadata.com/api/chartlist"
    params = {"charttype": "4"}
    r = http.get(url=url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json[0]["dataList"])
    for item in temp_df.columns[1:]:
        temp_list = []
        for item_list in temp_df[item]:
            temp_list.append(item_list[2])
        temp_df[item] = pd.to_numeric(temp_list, errors="coerce")
    return temp_df


def car_market_segment_cpca(symbol: str = "轿车") -> pd.DataFrame:
    """
    乘联会-统计数据-级别细分市场
    http://data.cpcadata.com/SegmentMarket
    :param symbol: choice of {"轿车", "MPV", "SUV"}
    :type symbol: str
    :return: 统计数据-车型大类
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcadata.com/api/chartlist"
    params = {"charttype": "5"}
    r = http.get(url=url, params=params)
    data_json = r.json()
    if symbol == "MPV":
        temp_df = pd.DataFrame(data_json[0]["dataList"])
        for item in temp_df.columns[1:]:
            temp_list = []
            for item_list in temp_df[item]:
                temp_list.append(item_list[2])
            temp_df[item] = pd.to_numeric(temp_list, errors="coerce")
    elif symbol == "SUV":
        temp_df = pd.DataFrame(data_json[1]["dataList"])
        for item in temp_df.columns[1:]:
            temp_list = []
            for item_list in temp_df[item]:
                temp_list.append(item_list[2])
            temp_df[item] = pd.to_numeric(temp_list, errors="coerce")
    else:
        temp_df = pd.DataFrame(data_json[2]["dataList"])
        for item in temp_df.columns[1:]:
            temp_list = []
            for item_list in temp_df[item]:
                temp_list.append(item_list[2])
            temp_df[item] = pd.to_numeric(temp_list, errors="coerce")
    return temp_df


def car_market_fuel_cpca(symbol: str = "整体市场") -> pd.DataFrame:
    """
    乘联会-统计数据-新能源细分市场
    :param symbol: choice of {"整体市场", "销量占比-PHEV-BEV", "销量占比-ICE-NEV"}
    :type symbol: str
    https://data.cpcadata.com/FuelMarket
    :return: 新能源细分市场
    :rtype: pandas.DataFrame
    """
    data_json = _cpca_chart("6")
    if symbol == "整体市场":
        return _cpca_year_table(
            data_json[0]["dataList"], key="month", value_index=2, label="月份"
        )
    if symbol == "销量占比-PHEV-BEV":
        return _cpca_table(
            data_json[1]["dataList"],
            key="月份",
            fields=["PHEV", "BEV"],
            value_index=2,
            label="月份",
        )
    return _cpca_table(
        data_json[2]["dataList"],
        key="月份",
        fields=["NEV", "ICE"],
        value_index=2,
        label="月份",
    )


if __name__ == "__main__":
    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="产量"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="产量"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="批发"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="批发"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="零售"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="零售"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="出口"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="出口"
    )
    print(car_market_total_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-单月", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-累计", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-单月", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-累计", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-单月", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-累计", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-单月", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-累计", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="轿车", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="MPV", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="SUV", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="占比", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="轿车", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="MPV", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="SUV", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="占比", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_country_cpca_df = car_market_country_cpca()
    print(car_market_country_cpca_df)

    car_market_segment_cpca_df = car_market_segment_cpca(symbol="轿车")
    print(car_market_segment_cpca_df)

    car_market_segment_cpca_df = car_market_segment_cpca(symbol="MPV")
    print(car_market_segment_cpca_df)

    car_market_segment_cpca_df = car_market_segment_cpca(symbol="SUV")
    print(car_market_segment_cpca_df)

    car_market_fuel_cpca_df = car_market_fuel_cpca(symbol="整体市场")
    print(car_market_fuel_cpca_df)

    car_market_fuel_cpca_df = car_market_fuel_cpca(symbol="销量占比-PHEV-BEV")
    print(car_market_fuel_cpca_df)

    car_market_fuel_cpca_df = car_market_fuel_cpca(symbol="销量占比-ICE-NEV")
    print(car_market_fuel_cpca_df)
