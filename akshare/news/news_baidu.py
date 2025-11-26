# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2025/11/14 20:30
Desc: 百度股市通-经济数据
https://gushitong.baidu.com/calendar
"""
import math

import pandas as pd
import requests


def _baidu_finance_calendar(
    date: str,
    cate: str,
    process_func,
    cookie: str = None
) -> pd.DataFrame:
    """
    百度股市通日历数据基础函数（支持分页）
    :param date: 查询日期 (格式: YYYYMMDD)
    :param cate: 数据类别 ("economic_data" 或 "notify_suspend")
    :param process_func: 数据处理函数
    :param cookie: cookie
    :return: 处理后的DataFrame
    """
    # 日期格式转换
    formatted_date = "-".join([date[:4], date[4:6], date[6:]])

    # 构建请求参数
    base_params = {
        "start_date": formatted_date,
        "end_date": formatted_date,
        "pn": "0",
        "rn": "100",  # 每页100条
        "cate": cate,
        "finClientType": "pc",
    }

    # 构建请求头
    headers = {
        "accept": "application/vnd.finance-web.v1+json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://gushitong.baidu.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://gushitong.baidu.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/142.0.0.0 Safari/537.36"
    }

    # 默认cookie
    if cookie is None:
        cookie = ("BAIDUID=2FFEC7A2DFDD58623592821064EA5BA7:FG=1; BAIDUID_BFESS=2FFEC7A2DFDD58623592821064EA5BA7"
                  ":FG=1; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIe"
                  "AeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGnsqk"
                  "Zri/4OJbm7r4CyJIowGEimjy3MrXEpSuItnI4KD2oamHIjD/NFFeJepWnxVEaTDvh37imFnz2JusPfLg+20CMlRn+O+PSm"
                  "Ijl1iaxOt9JGgA1IWuwdWQ6HGpfvkACrc6cZOQiWpdWZFfM9cCLuTBuECl+tiP++NCHKpXEMdWH1SPBXDyoMbf9Ga3EX3J"
                  "C70/lU+rOcT92RpNAO3HyuQbeCqJ91LNPfk1CUv8oZVl7/rim5dFAQ7oqBps3g3+aZ9KUZywDhnDu1Pi1I0y9keBGRJ+oo"
                  "8Kes3TzdoZP/mCoPKvyITQOchTYjURqFqbrHZFO3SaB4GS7zlBrG2cLm8lTRl19JYcYcqvy3P/50mxpWDwUUC4pvKOF9e+p"
                  "wNq7l6HzKEZyCMUDd+W6AiaksYiu+4AAz72OnMQfgAyNUbW3IyzL5c+UBht87WUigOY9alcIuR+n1gwn+Dmf3unATYGtv0z"
                  "KmAog3Ny9wFYiQ/gdKSrR9D25HSwrLQyIe5QKTkKSlY6nVev8MhaT3AUPwNqYIvWCQZXWkhuuU0ZXLMYAKJSeHY7mTrwwSS"
                  "KC3ZaI47CoFrvl4EuqobWGxpsF3vJDYM3XW3DNljsFR9IuqbVM9CtZEazJl9vJpqbMvL7R91rSPWb2eeCt263/A+EJVR/A8"
                  "+3BQ92SIDoXabq8Wb8ZGN9BAsC9g5OdjE6lhwzTadptHqT7mZN901gDzA4lMYEG/kekC+0J5/N5yVy+eizEguGAhOCNLy27"
                  "Y07ekeZ4evBBG6uKiyECyim8GsWrtEdf1YjB/qEZ70NLAIoAhusD05kuRm4sFZh/o1XJ6o5ZazU62XvOvycqQeNHJHilKXv"
                  "+Y0q7CT6wHNqzprY+XMxDln8dKB7nefcEun8dlqoZs4uNOo+pkpyckwWP4VbWloC92vUUtZ2lVqKiGsvJKvLgaUA9sPnxLH"
                  "pdf4XomqPKDKx4eFPQw2Q1jzqxFibbX6o8w3MlwZxJhxBabUW5sicyie973hz6nxWLbBzvYx9HPb4mEvyTKCvOi6/oFz+ZBS"
                  "s/kEn2kikYfHcMOTvlvvsfnWwwTasVNneN3K++VbMkJcXe6HpWGsfMtkPHUjgkj; ab_sr=1.0.1_MThjZTllNjUzYjk4Mz"
                  "Q4ZDcxZTc3ZDIxY2ZiZDYyODdkOTZmMDUxYzU1MWE4NTY2N2I5NjExZjk1ZjRiMTU4M2Q4N2MyMDYxZGRiMDFjOTg5NDJjO"
                  "DM5Zjk2Y2JhMDI1NzU5YjFmYWZlYjgyYjEyNzYxMTQ0YTVjYjVhNDc0ZTQwMWUzZDI2YjQ3OGVkYjI0Mzk5ZmQyNWYwZjBh"
                  "M2U3YmQzNTI5YWUyNGRlZDNhOTIxNjMyODljN2I1YzYyYzA0OTE4NjI0NWVkYzVhZWFkMDc2YWEwZjQxZDRiZDY0MmE=")
    headers["cookie"] = cookie

    url = "https://finance.pae.baidu.com/sapi/v1/financecalendar"
    big_df = pd.DataFrame()

    # 获取指定日期的总记录数
    target_date = formatted_date
    total_records = 0

    # 第一次请求
    params = base_params.copy()
    response = requests.get(url=url, params=params, headers=headers)
    response.raise_for_status()
    data_json = response.json()

    # 从JSON中提取指定日期的总记录数
    if "Result" in data_json and "calendarInfo" in data_json["Result"]:
        calendar_info = data_json["Result"]["calendarInfo"]

        # 查找目标日期的记录
        for item in calendar_info:
            if item.get("date") == target_date:
                total_records = item.get("total", 0)
                break

    # 计算总页数 (每页100条)
    total_pages = math.ceil(total_records / 100) if total_records > 0 else 1

    # 处理所有页码
    for page in range(total_pages):
        if page > 0:  # 第一页已在前面获取
            params = base_params.copy()
            params["pn"] = str(page)
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            data_json = response.json()

        # 提取并处理指定日期的数据
        if "Result" in data_json and "calendarInfo" in data_json["Result"]:
            for item in data_json["Result"]["calendarInfo"]:
                if item.get("date") == target_date and item.get("list"):
                    processed_df = process_func(item["list"])
                    big_df = pd.concat([big_df, processed_df], ignore_index=True)

    return big_df


def _process_economic_data(data_list: list) -> pd.DataFrame:
    """处理经济数据"""
    if not data_list:
        return pd.DataFrame()

    temp_df = pd.DataFrame(data_list)
    rename_dict = {
        "date": "日期",
        "time": "时间",
        "title": "事件",
        "star": "重要性",
        "formerVal": "前值",
        "pubVal": "公布",
        "region": "地区",
        "indicateVal": "预期",
        "country": "国家",
        "timePeriod": "统计周期"
    }
    temp_df.rename(columns=rename_dict, inplace=True)

    # 确保必要列存在
    required_cols = ["公布", "预期", "前值", "重要性"]
    for col in required_cols:
        if col not in temp_df.columns:
            temp_df[col] = None

    # 选择并排序列 (根据实际存在的列)
    available_cols = []
    for col in ["日期", "时间", "国家", "地区", "事件", "统计周期", "公布", "预期", "前值", "重要性"]:
        if col in temp_df.columns:
            available_cols.append(col)

    if available_cols:
        temp_df = temp_df[available_cols]

    # 类型转换
    for col in ["公布", "预期", "前值", "重要性"]:
        if col in temp_df.columns:
            temp_df[col] = pd.to_numeric(temp_df[col], errors="coerce")

    if "日期" in temp_df.columns:
        temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date

    return temp_df


def _process_suspend_data(data_list: list) -> pd.DataFrame:
    """处理停复牌数据 - 根据实际JSON结构精确修正"""
    if not data_list:
        return pd.DataFrame()

    # 创建DataFrame
    temp_df = pd.DataFrame(data_list)

    # 精确字段映射 (根据实际JSON结构)
    rename_dict = {
        "code": "股票代码",
        "name": "股票简称",
        "exchange": "交易所代码",
        "start": "停牌时间",  # 实际停牌开始时间字段
        "reason": "停牌事项说明",
        "marketValue": "市值",  # 使用marketValue而非capitalization
        "date": "公告日期",
        "time": "公告时间",
        "type": "证券类型",
        "market": "市场类型",
        "isSkip": "是否跳过",
        "end": "复牌时间"
    }
    temp_df.rename(columns=rename_dict, inplace=True)
    if "复牌时间" not in temp_df.columns:
        temp_df['复牌时间'] = '-'
    temp_df = temp_df[[
        "股票代码",
        "股票简称",
        "交易所代码",
        "停牌时间",  # 实际停牌开始时间字段
        "复牌时间",  # 实际停牌开始时间字段
        "停牌事项说明",
        "市值",  # 使用marketValue而非capitalization
        "公告日期",
        "公告时间",
        "证券类型",
        "市场类型",
        "是否跳过"
    ]]
    return temp_df


def news_economic_baidu(date: str = "20251126", cookie: str = None) -> pd.DataFrame:
    """
    百度股市通-经济数据
    https://gushitong.baidu.com/calendar
    :param date: 查询日期 (格式: YYYYMMDD)
    :param cookie: cookie
    :return: 经济数据DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="economic_data",
        process_func=_process_economic_data,
        cookie=cookie
    )


def news_trade_notify_suspend_baidu(date: str = "20251126", cookie: str = None) -> pd.DataFrame:
    """
    百度股市通-交易提醒-停复牌
    https://gushitong.baidu.com/calendar
    :param date: 查询日期 (格式: YYYYMMDD)
    :param cookie: cookie
    :return: 停复牌数据DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="notify_suspend",
        process_func=_process_suspend_data,
        cookie=cookie
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
    temp_df.rename(columns=rename_dict, inplace=True)

    # 确保必要列存在
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


def news_trade_notify_dividend_baidu(date: str = "20251126", cookie: str = None) -> pd.DataFrame:
    """
    百度股市通-交易提醒-分红派息
    https://gushitong.baidu.com/calendar
    :param date: 查询日期 (格式: YYYYMMDD)
    :param cookie: cookie
    :return: 交易提醒-分红派息DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="notify_divide",
        process_func=_process_dividend_data,
        cookie=cookie
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
        "date": "发布日期"
    }
    temp_df.rename(columns=rename_dict, inplace=True)

    # 确保必要列存在
    if "财报类型" not in temp_df.columns:
        temp_df["财报类型"] = "-"
    if "发布时间" not in temp_df.columns:
        temp_df["发布时间"] = "-"
    if "市值" not in temp_df.columns and "总市值" in temp_df.columns:
        temp_df["市值"] = temp_df["总市值"]

    # 选择并排序列
    available_cols = []
    for col in ["股票代码", "股票简称", "交易所", "财报类型", "发布时间", "市值", "发布日期"]:
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
        temp_df["发布日期"] = pd.to_datetime(temp_df["发布日期"], errors="coerce").dt.date

    return temp_df


def news_report_time_baidu(date: str = "20251126", cookie: str = None) -> pd.DataFrame:
    """
    百度股市通-财报发行
    https://gushitong.baidu.com/calendar
    :param date: 查询日期 (格式: YYYYMMDD)
    :param cookie: cookie
    :return: 财报发行DataFrame
    """
    return _baidu_finance_calendar(
        date=date,
        cate="report_time",
        process_func=_process_report_data,
        cookie=cookie
    )


if __name__ == "__main__":
    news_economic_baidu_df = news_economic_baidu(date="20251126")
    print(news_economic_baidu_df)

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
