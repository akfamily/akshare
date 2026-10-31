#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/28
Desc: 百度股市通-停复牌、分红派息与财报发行
https://finance.baidu.com/calendar
"""

import pandas as pd
from akshare.utils.baidu_finance import _baidu_finance_calendar


def _process_suspend_data(data_list: list) -> pd.DataFrame:
    """处理停复牌数据 - 根据实际JSON结构精确修正"""
    if not data_list:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_list)
    rename_dict = {
        "code": "股票代码",
        "name": "股票简称",
        "exchange": "交易所代码",
        "start": "停牌时间",
        "reason": "停牌事项说明",
        "marketValue": "市值",
        "date": "公告日期",
        "time": "公告时间",
        "type": "证券类型",
        "market": "市场类型",
        "isSkip": "是否跳过",
        "end": "复牌时间",
    }
    temp_df = temp_df.rename(columns=rename_dict)
    if "复牌时间" not in temp_df.columns:
        temp_df["复牌时间"] = "-"
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "交易所代码",
            "停牌时间",
            "复牌时间",
            "停牌事项说明",
            "市值",
            "公告日期",
            "公告时间",
            "证券类型",
            "市场类型",
            "是否跳过",
        ]
    ]
    return temp_df


def news_trade_notify_suspend_baidu(
    date: str = "20251126", cookie: str = None
) -> pd.DataFrame:
    """
    百度股市通-交易提醒-停复牌
    https://finance.baidu.com/calendar
    :param date: 查询日期 (格式：YYYYMMDD)
    :param cookie: cookie
    :return: 停复牌数据DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="notify_suspend",
        process_func=_process_suspend_data,
        cookie=cookie,
    )


def _process_dividend_data(data_list: list) -> pd.DataFrame:
    """处理分红派息数据"""
    if not data_list:
        return pd.DataFrame()

    temp_df = pd.DataFrame(data_list)

    # 字段映射
    rename_dict = {
        "code": "股票代码",
        "market": "-",  # 这个字段在最终结果中会被删除
        "exchange": "交易所",
        "name": "股票简称",
        "diviDate": "除权日",
        "date": "报告期",
        "diviCash": "分红",
        "shareDivide": "送股",
        "transfer": "转增",
        "physical": "实物",
    }
    temp_df = temp_df.rename(columns=rename_dict)

    # 确保必要列存在
    if "分红" not in temp_df.columns:
        temp_df["分红"] = "-"
    if "实物" not in temp_df.columns:
        temp_df["实物"] = "-"
    if "送股" not in temp_df.columns:
        temp_df["送股"] = "-"
    if "转增" not in temp_df.columns:
        temp_df["转增"] = "-"

    # 选择需要的列
    temp_df = temp_df[
        [
            "股票代码",
            "除权日",
            "分红",
            "送股",
            "转增",
            "实物",
            "交易所",
            "股票简称",
            "报告期",
        ]
    ]

    # 日期格式转换
    if "除权日" in temp_df.columns:
        temp_df["除权日"] = pd.to_datetime(temp_df["除权日"], errors="coerce").dt.date
    if "报告期" in temp_df.columns:
        temp_df["报告期"] = pd.to_datetime(temp_df["报告期"], errors="coerce").dt.date

    return temp_df


def news_trade_notify_dividend_baidu(
    date: str = "20251126", cookie: str = None
) -> pd.DataFrame:
    """
    百度股市通-交易提醒-分红派息
    https://finance.baidu.com/calendar
    :param date: 查询日期 (格式：YYYYMMDD)
    :param cookie: cookie
    :return: 交易提醒-分红派息DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="notify_divide",
        process_func=_process_dividend_data,
        cookie=cookie,
    )


def _process_report_data(data_list: list) -> pd.DataFrame:
    """处理财报发行数据 - 根据实际JSON结构精确修正"""
    if not data_list:
        return pd.DataFrame()

    # 创建DataFrame
    temp_df = pd.DataFrame(data_list)

    # 精确字段映射 (根据提供的JSON结构)
    rename_dict = {
        "code": "股票代码",
        "name": "股票简称",
        "exchange": "交易所",
        "reportType": "财报类型",
        "time": "发布时间",
        "marketValue": "市值",
        "capitalization": "总市值",
        "date": "发布日期",
    }
    temp_df = temp_df.rename(columns=rename_dict)

    # 确保必要列存在
    if "财报类型" not in temp_df.columns:
        temp_df["财报类型"] = "-"
    if "发布时间" not in temp_df.columns:
        temp_df["发布时间"] = "-"
    if "市值" not in temp_df.columns and "总市值" in temp_df.columns:
        temp_df["市值"] = temp_df["总市值"]

    # 选择并排序列
    available_cols = []
    for col in [
        "股票代码",
        "股票简称",
        "交易所",
        "财报类型",
        "发布时间",
        "市值",
        "发布日期",
    ]:
        if col in temp_df.columns:
            available_cols.append(col)

    if available_cols:
        temp_df = temp_df[available_cols]
    else:
        # 如果没有匹配的列，返回空DataFrame
        return pd.DataFrame()

    # 类型转换
    if "市值" in temp_df.columns:
        temp_df["市值"] = pd.to_numeric(temp_df["市值"], errors="coerce")

    if "发布日期" in temp_df.columns:
        temp_df["发布日期"] = pd.to_datetime(
            temp_df["发布日期"], errors="coerce"
        ).dt.date

    return temp_df


def news_report_time_baidu(date: str = "20251126", cookie: str = None) -> pd.DataFrame:
    """
    百度股市通-财报发行
    https://finance.baidu.com/calendar
    :param date: 查询日期 (格式：YYYYMMDD)
    :param cookie: cookie
    :return: 财报发行DataFrame
    """
    return _baidu_finance_calendar(
        date=date, cate="report_time", process_func=_process_report_data, cookie=cookie
    )


if __name__ == "__main__":
    news_trade_notify_suspend_baidu_df = news_trade_notify_suspend_baidu(
        date="20251126"
    )
    print(news_trade_notify_suspend_baidu_df)

    news_trade_notify_dividend_baidu_df = news_trade_notify_dividend_baidu(
        date="20251126"
    )
    print(news_trade_notify_dividend_baidu_df)

    news_report_time_baidu_df = news_report_time_baidu(date="20251126")
    print(news_report_time_baidu_df)
