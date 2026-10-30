#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/28
Desc: 百度股市通-财经日历的公共请求函数
https://finance.baidu.com/calendar
"""

import math
import re
import pandas as pd
from curl_cffi import requests

from akshare.utils import http


def _get_baidu_cookie(headers: dict) -> str:
    """
    安全获取百度股市通所需的 Cookie
    :param headers: 基础请求头
    :return: 格式化的 Cookie字符串
    :raises ValueError: 当无法获取必要Cookie时
    :raises ConnectionError: 网络请求失败时
    """
    try:
        # 使用Session保持Cookie上下文
        with http.CurlSession() as session:
            session.headers.update(headers)

            # 第一步：获取基础Cookie (BAIDUID系列)
            resp1 = session.get(
                "https://finance.baidu.com/calendar",
                impersonate="chrome110",
            )
            resp1.raise_for_status()

            # 验证必要Cookie
            baiduid = resp1.cookies.get("BAIDUID")
            baiduid_bfess = resp1.cookies.get("BAIDUID_BFESS")
            if not all([baiduid, baiduid_bfess]):
                raise ValueError("Missing BAIDUID cookies in first response")

            # 第二步：提取并请求hm.js
            hm_pattern = r"https://hm\.baidu\.com/hm\.js\?\w+"
            hm_match = re.search(hm_pattern, resp1.text)
            if not hm_match:
                # 尝试备用正则模式
                hm_match = re.search(r"//hm\.baidu\.com/hm\.js\?\w+", resp1.text)
                if not hm_match:
                    raise ValueError("Failed to extract hm.js URL from response")

            hm_url = (
                "https:" + hm_match.group()
                if hm_match.group().startswith("//")
                else hm_match.group()
            )

            # 第二步请求 (自动携带第一步的Cookie)
            resp2 = session.get(hm_url, impersonate="chrome110")
            resp2.raise_for_status()

            # 验证必要Cookie
            hmac_count = resp2.cookies.get("HMACCOUNT")
            hmac_count_bfess = resp2.cookies.get("HMACCOUNT_BFESS")
            if not all([hmac_count, hmac_count_bfess]):
                raise ValueError("Missing HMACCOUNT cookies in second response")

            # 安全拼接Cookie
            return (
                f"BAIDUID={baiduid}; "
                f"BAIDUID_BFESS={baiduid_bfess}; "
                f"HMACCOUNT={hmac_count}; "
                f"HMACCOUNT_BFESS={hmac_count_bfess}"
            )

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network request failed: {str(e)}") from e
    except re.error as e:
        raise ValueError(f"Regex pattern error: {str(e)}") from e


def _baidu_finance_calendar(
    date: str, cate: str, process_func, cookie: str = None
) -> pd.DataFrame:
    """
    百度股市通日历数据基础函数（支持分页）
    :param date: 查询日期 (格式：YYYYMMDD)
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
        "origin": "https://finance.baidu.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://finance.baidu.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36",
    }

    # 在_baidu_finance_calendar函数中替换原代码块
    if cookie is None:
        try:
            cookie = _get_baidu_cookie(headers.copy())  # 保护原始headers
        except Exception as e:
            # 可降级处理或保留原始行为
            raise RuntimeError(f"Failed to obtain Baidu cookies: {str(e)}") from e
    headers["cookie"] = cookie

    url = "https://finance.pae.baidu.com/sapi/v1/financecalendar"
    big_df = pd.DataFrame()

    # 获取指定日期的总记录数
    target_date = formatted_date
    total_records = 0

    # 第一次请求
    params = base_params.copy()
    response = http.curl_get(
        url=url, params=params, headers=headers, impersonate="chrome110"
    )
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
            response = http.curl_get(url=url, params=params, headers=headers)
            response.raise_for_status()
            data_json = response.json()

        # 提取并处理指定日期的数据
        if "Result" in data_json and "calendarInfo" in data_json["Result"]:
            for item in data_json["Result"]["calendarInfo"]:
                if item.get("date") == target_date and item.get("list"):
                    processed_df = process_func(item["list"])
                    big_df = pd.concat([big_df, processed_df], ignore_index=True)

    return big_df
