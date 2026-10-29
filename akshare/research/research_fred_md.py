#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: Economic Research from Federal Reserve Bank of St. Louis
https://research.stlouisfed.org/econ/mccracken/fred-databases/
FRED-MD and FRED-QD are large macroeconomic databases designed for the empirical analysis of “big data.” The datasets of monthly and quarterly observations mimic the coverage of datasets already used in the literature, but they add three appealing features. They are updated in real-time through the FRED database. They are publicly accessible, facilitating the replication of empirical work. And they relieve the researcher of the task of incorporating data changes and revisions (a task accomplished by the data desk at the Federal Reserve Bank of St. Louis).
"""

import io
import re
import zipfile
from functools import lru_cache
from typing import Dict

import pandas as pd

from akshare.exceptions import DataParsingError, InvalidParameterError
from akshare.utils import http

_PAGE_URL = "https://research.stlouisfed.org/econ/mccracken/fred-databases/"
_BASE_URL = "https://www.stlouisfed.org"

# 原 s3.amazonaws.com/files.fred.stlouisfed.org 地址已返回 403。数据迁至
# www.stlouisfed.org，该站按 TLS 指纹拦截非浏览器客户端，requests 会一直无响应，
# 因此经 curl_cffi 模拟浏览器访问；无需翻墙。
# 当年以前的各期打包在一个历史 zip 中，当年的各期是单独的 CSV。两处文件名都不统一：
# 有 2020-01.csv、FRED-MD-2025m08.csv、FRED-MD_2025m12.csv、FRED-QD_2019m1.csv，
# 以及 2026-01-md.csv、2026-rev-08-md.csv 等写法，一律按其中的年份与月份识别
_VINTAGE_PATTERN = re.compile(r"(\d{4})(?:-rev-|-|m)(\d{1,2})\D*\.csv$")


def _vintage_key(name: str):
    """
    从文件名中识别数据所属的年月
    :param name: 文件名或链接
    :type name: str
    :return: 形如 "2020-01" 的年月；无法识别时为 None
    :rtype: str
    """
    match = _VINTAGE_PATTERN.search(name)
    if match is None:
        return None
    return f"{match.group(1)}-{int(match.group(2)):02d}"


def _fred_links(kind: str) -> Dict[str, str]:
    """
    从数据库主页解析当年各期 CSV 与历史 zip 的下载地址
    :param kind: "md" 或 "qd"
    :type kind: str
    :return: 以年月为键的各期 CSV 地址，另以 zip 为键存放历史压缩包地址
    :rtype: dict
    """
    r = http.curl_get(_PAGE_URL, impersonate="chrome")
    r.raise_for_status()
    folder = "monthly" if kind == "md" else "quarterly"
    links = {}
    for href in re.findall(r'href="([^"]+)"', r.text):
        href = href.replace("&amp;", "&")
        path = href.split("?")[0]
        if path.endswith(f"/fred-md/{folder}/{path.rsplit('/', 1)[-1]}"):
            key = _vintage_key(path)
            if key is not None:
                links[key] = _BASE_URL + path
        elif re.search(rf"historical-vintages-of-fred-{kind}-[^/]+\.zip$", path):
            links["zip"] = _BASE_URL + path
    return links


@lru_cache(maxsize=2)
def _fred_zip(url: str) -> Dict[str, bytes]:
    """
    下载历史 zip 并按年月索引其中的 CSV；地址中含截止年月，上游更新后地址随之变化
    :param url: 历史 zip 地址
    :type url: str
    :return: 以年月为键的各期 CSV 内容
    :rtype: dict
    """
    # 历史 zip 约 20～40 MB，curl_cffi 把超时当作总时长上限，默认值对慢速网络偏紧
    r = http.curl_get(url, impersonate="chrome", timeout=(10, 600))
    r.raise_for_status()
    archive = zipfile.ZipFile(io.BytesIO(r.content))
    return {
        _vintage_key(name): archive.read(name)
        for name in archive.namelist()
        if _vintage_key(name) is not None
    }


def _fred_vintage(kind: str, date: str) -> pd.DataFrame:
    """
    获取指定一期的 FRED-MD 或 FRED-QD 数据
    :param kind: "md" 或 "qd"
    :type kind: str
    :param date: 年月，如 "2020-01"
    :type date: str
    :return: 该期数据
    :rtype: pandas.DataFrame
    """
    key = _vintage_key(f"{date}.csv")
    if key is None:
        raise InvalidParameterError(f"date 应为 YYYY-MM 格式，如 2020-01，收到：{date}")
    links = _fred_links(kind)
    if key in links:
        r = http.curl_get(links[key], impersonate="chrome")
        r.raise_for_status()
        return pd.read_csv(io.BytesIO(r.content))
    if "zip" not in links:
        raise DataParsingError(
            f"FRED 数据库主页中未找到历史数据压缩包，上游可能已改版：{_PAGE_URL}"
        )
    vintages = _fred_zip(links["zip"])
    if key in vintages:
        return pd.read_csv(io.BytesIO(vintages[key]))
    available = sorted(set(vintages) | (set(links) - {"zip"}))
    raise InvalidParameterError(
        f"FRED-{kind.upper()} 没有 {key} 这一期，可选范围为 {available[0]} 至 {available[-1]}"
    )


def fred_md(date: str = "2020-01") -> pd.DataFrame:
    """
    The accompanying paper shows that factors extracted from the FRED-MD dataset share the same predictive content as those based on the various vintages of the so-called Stock-Watson data. In addition, it suggests that diffusion indexes constructed as the partial sum of the factor estimates can potentially be useful for the study of business cycle chronology.
    首次获取当年以前的数据需下载约 36 MB 的历史压缩包，同一进程内再次调用不重复下载
    :param date: e.g., "2020-03"; from "2015-01" to now
    :type date: str
    :return: Monthly Data
    :rtype: pandas.DataFrame
    """
    return _fred_vintage(kind="md", date=date)


def fred_qd(date: str = "2020-01") -> pd.DataFrame:
    """
    FRED-QD is a quarterly frequency companion to FRED-MD. It is designed to emulate the dataset used in "Disentangling the Channels of the 2007-2009 Recession" by Stock and Watson (2012, NBER WP No. 18094) but also contains several additional series. Comments or suggestions are welcome.
    首次获取当年以前的数据需下载约 20 MB 的历史压缩包，同一进程内再次调用不重复下载
    :param date: e.g., "2020-03"; from "2018-05" to now
    :type date: str
    :return: Quarterly Data
    :rtype: pandas.DataFrame
    """
    return _fred_vintage(kind="qd", date=date)


if __name__ == "__main__":
    fred_md_df = fred_md(date="2023-03")
    print(fred_md_df)

    fred_qd_df = fred_qd(date="2023-03")
    print(fred_qd_df)
