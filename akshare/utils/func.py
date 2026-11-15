# !/usr/bin/env python
"""
Date: 2025/3/10 18:00
Desc: 通用帮助函数
"""

import math
import random
import time
from typing import List, Dict

import pandas as pd

from akshare.exceptions import InvalidParameterError
from akshare.utils import http
from akshare.utils.tqdm import get_tqdm


def _get_page(url: str, params: Dict):
    """
    取一页东方财富分页数据；每次新建连接，失败时按 http.request_with_retry 的策略重试
    :return: 响应对象
    :rtype: requests.Response
    """
    r = http.request_with_retry("get", url, params=params, fresh_session=True)
    r.raise_for_status()
    return r


def fetch_paginated_data(url: str, base_params: Dict):
    """
    东方财富-分页获取数据并合并结果
    https://quote.eastmoney.com/f1.html?newcode=0.000001
    :param url: 股票代码
    :type url: str
    :param base_params: 基础请求参数
    :type base_params: dict
    :return: 合并后的数据
    :rtype: pandas.DataFrame
    """
    # 复制参数以避免修改原始参数
    params = base_params.copy()
    # 获取第一页数据，用于确定分页信息
    r = _get_page(url, params)
    data_json = r.json()
    # 计算分页信息
    per_page_num = len(data_json["data"]["diff"])
    total_page = math.ceil(data_json["data"]["total"] / per_page_num)
    # 存储所有页面数据
    temp_list = []
    # 添加第一页数据
    temp_list.append(pd.DataFrame(data_json["data"]["diff"]))
    # 获取进度条
    tqdm = get_tqdm()
    # 获取剩余页面数据
    for page in tqdm(range(2, total_page + 1), leave=False):
        params.update({"pn": page})
        # 添加随机延迟，避免请求过于频繁
        time.sleep(random.uniform(0.5, 1.5))
        r = _get_page(url, params)
        data_json = r.json()
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df = temp_df.sort_values(by=["f3"], ascending=False, ignore_index=True)
    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df["index"].astype(int) + 1
    return temp_df


def ffill_to_index(df: pd.DataFrame, index: pd.Index) -> pd.DataFrame:
    """
    把按变动日期记录的数据（股本、复权因子等）对齐到指定日期：每个日期取不晚于它的最近一条记录
    先在两组日期的并集上前向填充，再只保留指定日期，因此变动日不是交易日时也能取到正确的值，
    且不会多出非交易日的行。早于第一条记录的日期为 NaN；同一日期有多条记录时取最后一条
    :param df: 以 DatetimeIndex 为索引的变动记录，可以无序
    :type df: pandas.DataFrame
    :param index: 需要对齐到的日期，通常是交易日
    :type index: pandas.Index
    :return: 以 index 为索引、列与 df 相同的数据
    :rtype: pandas.DataFrame
    """
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df.reindex(df.index.union(index)).ffill().reindex(index)


# K 线周期 -> pandas 的周期频率；周线按自然周（周一至周日），月线按自然月
KLINE_PERIODS = {"daily": None, "weekly": "W", "monthly": "M"}
# 合成周线、月线时各列的取法，未列出的列（如 outstanding_share）取周期内最后一个交易日的值
_KLINE_FIRST = {"open", "prevclose"}
_KLINE_MAX = {"high"}
_KLINE_MIN = {"low"}
_KLINE_SUM = {
    "volume",
    "amount",
    "turnover",
    "after_volume",
    "after_amount",
    "postVol",
    "postAmt",
}


def check_kline_period(period: str, adjust: str = "") -> None:
    """
    检查 K 线周期；复权因子不是行情，不能与周线、月线一起使用
    :param period: daily、weekly 或 monthly
    :type period: str
    :param adjust: 复权方式
    :type adjust: str
    """
    if period not in KLINE_PERIODS:
        raise InvalidParameterError(
            f"period 不能是 {period}，可选值：{'、'.join(KLINE_PERIODS)}"
        )
    if period != "daily" and adjust.endswith("-factor"):
        raise InvalidParameterError(
            f'adjust="{adjust}" 返回的是复权因子，只能与 period="daily" 一起使用'
        )


def resample_kline(
    df: pd.DataFrame, period: str, start_date: str = "", end_date: str = ""
) -> pd.DataFrame:
    """
    把日线合成为周线或月线：开盘取第一个交易日，最高、最低取极值，收盘取最后一个交易日，
    成交量、成交额、换手率求和，其余列取最后一个交易日的值；日期为周期内最后一个交易日。
    应传入完整的日线再用 start_date、end_date 筛选，这样首尾两根 K 线不会因为日期范围
    从周期中间开始而只含部分交易日
    :param df: 含 date 列、按日期升序的日线
    :type df: pandas.DataFrame
    :param period: daily、weekly 或 monthly；daily 时原样返回
    :type period: str
    :param start_date: 开始日期，按合成后的日期筛选，为空时不筛选
    :type start_date: str
    :param end_date: 结束日期，按合成后的日期筛选，为空时不筛选
    :type end_date: str
    :return: 列与 df 相同的周线或月线
    :rtype: pandas.DataFrame
    """
    freq = KLINE_PERIODS[period]
    if freq is None or df.empty:
        return df
    dates = pd.to_datetime(df["date"])
    df = df.iloc[dates.argsort(kind="stable").to_numpy()]
    key = pd.to_datetime(df["date"]).dt.to_period(freq).rename(None)
    how = {}
    for col in df.columns:
        if col in _KLINE_FIRST:
            how[col] = "first"
        elif col in _KLINE_MAX:
            how[col] = "max"
        elif col in _KLINE_MIN:
            how[col] = "min"
        elif col in _KLINE_SUM:
            # 整个周期都没有数据时保持为空，而不是 0
            how[col] = lambda x: x.sum(min_count=1)
        else:
            how[col] = "last"
    temp_df = df.groupby(key, sort=True).agg(how).reset_index(drop=True)
    temp_df = temp_df[list(df.columns)]
    bar_dates = pd.to_datetime(temp_df["date"])
    mask = pd.Series(True, index=temp_df.index)
    if start_date:
        mask &= bar_dates >= pd.to_datetime(start_date)
    if end_date:
        mask &= bar_dates <= pd.to_datetime(end_date)
    return temp_df[mask].reset_index(drop=True)


def set_df_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    设置 pandas.DataFrame 为空的情况
    :param df: 需要设置命名的数据框
    :type df: pandas.DataFrame
    :param cols: 字段的列表
    :type cols: list
    :return: 重新设置后的数据
    :rtype: pandas.DataFrame
    """
    if df.shape == (0, 0):
        return pd.DataFrame(data=[], columns=cols)
    else:
        df.columns = cols
        return df
