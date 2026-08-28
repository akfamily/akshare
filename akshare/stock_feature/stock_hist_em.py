#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/3/10 18:00
Desc: 东方财富网-行情首页-沪深京 A 股
https://quote.eastmoney.com/
"""

import math
import random
import threading
import time
from typing import Optional, Sequence, Tuple

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from akshare.utils.func import fetch_paginated_data
from akshare.utils.tqdm import get_tqdm


_ZH_A_SPOT_URL = "https://82.push2.eastmoney.com/api/qt/clist/get"
_ZH_A_SPOT_BATCH_URL = "https://82.push2.eastmoney.com/api/qt/ulist.np/get"
_ZH_A_SPOT_FIELDS = (
    "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,"
    "f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152"
)
_ZH_A_SPOT_BATCH_SIZE = 500
_ZH_A_SPOT_CACHE_TTL = 60 * 60
_ZH_A_SPOT_TIMEOUT = 15
_ZH_A_SPOT_CACHE_LOCK = threading.Lock()
_ZH_A_SPOT_CACHED_SECIDS: Tuple[str, ...] = ()
_ZH_A_SPOT_CACHE_EXPIRES_AT = 0.0
_ZH_A_SPOT_CACHE_VERSION = 0

_ZH_A_SPOT_COLUMN_MAP = {
    "f12": "代码",
    "f14": "名称",
    "f2": "最新价",
    "f3": "涨跌幅",
    "f4": "涨跌额",
    "f5": "成交量",
    "f6": "成交额",
    "f7": "振幅",
    "f15": "最高",
    "f16": "最低",
    "f17": "今开",
    "f18": "昨收",
    "f10": "量比",
    "f8": "换手率",
    "f9": "市盈率-动态",
    "f23": "市净率",
    "f20": "总市值",
    "f21": "流通市值",
    "f22": "涨速",
    "f11": "5分钟涨跌",
    "f24": "60日涨跌幅",
    "f25": "年初至今涨跌幅",
}
_ZH_A_SPOT_COLUMNS = ["序号", *_ZH_A_SPOT_COLUMN_MAP.values()]
_ZH_A_SPOT_NUMERIC_COLUMNS = _ZH_A_SPOT_COLUMNS[3:]


class _StockZhASpotCodeCacheStale(ValueError):
    pass


def _create_stock_zh_a_spot_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
            "Referer": "https://quote.eastmoney.com/",
        }
    )
    retry = Retry(
        total=3,
        connect=3,
        read=2,
        status=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=1,
        pool_maxsize=1,
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _request_stock_zh_a_spot_data(
    session: requests.Session, url: str, params: dict
) -> dict:
    response = session.get(url, params=params, timeout=_ZH_A_SPOT_TIMEOUT)
    response.raise_for_status()
    data_json = response.json()
    if not isinstance(data_json, dict):
        raise ValueError("东方财富行情接口未返回有效的 JSON 对象")
    data = data_json.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("diff"), list):
        raise ValueError("东方财富行情接口未返回有效的 data.diff 数据")
    return data


def _stock_zh_a_spot_params() -> dict:
    return {
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fields": _ZH_A_SPOT_FIELDS,
    }


def _stock_zh_a_spot_secids(rows: Sequence[dict]) -> Tuple[str, ...]:
    try:
        secids = tuple(f"{item['f13']}.{item['f12']}" for item in rows)
    except (KeyError, TypeError) as err:
        raise ValueError("东方财富行情结果缺少证券代码或市场标识") from err
    if len(secids) != len(set(secids)):
        raise ValueError("东方财富行情结果包含重复证券代码")
    return secids


def _fetch_stock_zh_a_spot_clist(
    session: requests.Session,
) -> Tuple[list, Tuple[str, ...]]:
    params = {
        **_stock_zh_a_spot_params(),
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
    }
    first_data = _request_stock_zh_a_spot_data(session, _ZH_A_SPOT_URL, params)
    first_page = first_data["diff"]
    if not first_page:
        raise ValueError("东方财富行情接口返回了空的第一页数据")
    try:
        total = int(first_data["total"])
    except (KeyError, TypeError, ValueError) as err:
        raise ValueError("东方财富行情接口未返回有效的数据总量") from err

    total_page = math.ceil(total / len(first_page))
    rows = list(first_page)
    tqdm = get_tqdm()
    for page in tqdm(range(2, total_page + 1), leave=False):
        time.sleep(random.uniform(0.5, 1.5))
        params["pn"] = str(page)
        page_data = _request_stock_zh_a_spot_data(session, _ZH_A_SPOT_URL, params)
        rows.extend(page_data["diff"])

    secids = _stock_zh_a_spot_secids(rows)
    if len(secids) != total:
        raise ValueError(
            f"东方财富行情接口返回数量不完整: 预期 {total}, 实际 {len(secids)}"
        )
    return rows, secids


def _fetch_stock_zh_a_spot_batches(
    session: requests.Session, secids: Sequence[str]
) -> list:
    rows = []
    for start in range(0, len(secids), _ZH_A_SPOT_BATCH_SIZE):
        batch = tuple(secids[start : start + _ZH_A_SPOT_BATCH_SIZE])
        params = {
            **_stock_zh_a_spot_params(),
            "secids": ",".join(batch),
        }
        data = _request_stock_zh_a_spot_data(session, _ZH_A_SPOT_BATCH_URL, params)
        batch_rows = data["diff"]
        try:
            returned_secids = _stock_zh_a_spot_secids(batch_rows)
        except ValueError as err:
            raise _StockZhASpotCodeCacheStale(str(err)) from err
        if len(returned_secids) != len(batch) or set(returned_secids) != set(batch):
            raise _StockZhASpotCodeCacheStale(
                "东方财富批量行情结果与缓存的证券代码清单不一致"
            )
        rows.extend(batch_rows)
        if start + _ZH_A_SPOT_BATCH_SIZE < len(secids):
            time.sleep(random.uniform(0.2, 0.4))

    returned_secids = _stock_zh_a_spot_secids(rows)
    if len(returned_secids) != len(secids) or set(returned_secids) != set(secids):
        raise _StockZhASpotCodeCacheStale(
            "东方财富批量行情结果未覆盖完整的证券代码清单"
        )
    return rows


def _read_stock_zh_a_spot_cache() -> Tuple[Tuple[str, ...], int]:
    with _ZH_A_SPOT_CACHE_LOCK:
        if _ZH_A_SPOT_CACHED_SECIDS and time.monotonic() < _ZH_A_SPOT_CACHE_EXPIRES_AT:
            return _ZH_A_SPOT_CACHED_SECIDS, _ZH_A_SPOT_CACHE_VERSION
    return (), _ZH_A_SPOT_CACHE_VERSION


def _refresh_stock_zh_a_spot_cache(
    session: requests.Session, expected_version: Optional[int] = None
) -> Tuple[Optional[list], Tuple[str, ...], int]:
    global _ZH_A_SPOT_CACHED_SECIDS
    global _ZH_A_SPOT_CACHE_EXPIRES_AT
    global _ZH_A_SPOT_CACHE_VERSION

    with _ZH_A_SPOT_CACHE_LOCK:
        cache_is_valid = (
            _ZH_A_SPOT_CACHED_SECIDS and time.monotonic() < _ZH_A_SPOT_CACHE_EXPIRES_AT
        )
        if cache_is_valid and (
            expected_version is None or _ZH_A_SPOT_CACHE_VERSION != expected_version
        ):
            return None, _ZH_A_SPOT_CACHED_SECIDS, _ZH_A_SPOT_CACHE_VERSION

        rows, secids = _fetch_stock_zh_a_spot_clist(session)
        _ZH_A_SPOT_CACHED_SECIDS = secids
        _ZH_A_SPOT_CACHE_EXPIRES_AT = time.monotonic() + _ZH_A_SPOT_CACHE_TTL
        _ZH_A_SPOT_CACHE_VERSION += 1
        return rows, secids, _ZH_A_SPOT_CACHE_VERSION


def _format_stock_zh_a_spot(rows: Sequence[dict]) -> pd.DataFrame:
    temp_df = pd.DataFrame(rows)
    missing_fields = set(_ZH_A_SPOT_COLUMN_MAP).difference(temp_df.columns)
    if missing_fields:
        raise ValueError(
            "东方财富行情结果缺少字段: " + ", ".join(sorted(missing_fields))
        )
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
    temp_df.rename(columns=_ZH_A_SPOT_COLUMN_MAP, inplace=True)
    temp_df.insert(0, "序号", range(1, len(temp_df) + 1))
    temp_df = temp_df[_ZH_A_SPOT_COLUMNS]
    for column in _ZH_A_SPOT_NUMERIC_COLUMNS:
        temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce")
    return temp_df


def stock_zh_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-沪深京 A 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    with _create_stock_zh_a_spot_session() as session:
        secids, cache_version = _read_stock_zh_a_spot_cache()
        if not secids:
            rows, secids, cache_version = _refresh_stock_zh_a_spot_cache(session)
            if rows is not None:
                return _format_stock_zh_a_spot(rows)

        try:
            rows = _fetch_stock_zh_a_spot_batches(session, secids)
        except _StockZhASpotCodeCacheStale:
            rows, secids, cache_version = _refresh_stock_zh_a_spot_cache(
                session, expected_version=cache_version
            )
            if rows is None:
                rows = _fetch_stock_zh_a_spot_batches(session, secids)
        return _format_stock_zh_a_spot(rows)


def stock_sh_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-沪 A 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:1 t:2,m:1 t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,"
        "f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )
    return temp_df


def stock_sz_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-深 A 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:0 t:6,m:0 t:80",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,"
        "f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )
    return temp_df


def stock_bj_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-京 A 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:0 t:81 s:2048",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24"
        ",f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )
    return temp_df


def stock_new_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-新股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#newshares
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "wbp2u": "|0|0|0|web",
        "fid": "f26",
        "fs": "m:0 f:8,m:1 f:8",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,"
        "f25,f26,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "上市日期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "上市日期",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )

    temp_df["上市日期"] = pd.to_datetime(temp_df["上市日期"], format="%Y%m%d").dt.date
    return temp_df


def stock_cy_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-创业板-实时行情
    https://quote.eastmoney.com/center/gridlist.html#gem_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://7.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "wbp2u": "|0|0|0|web",
        "fid": "f12",
        "fs": "m:0 t:80",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,"
        "f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )
    return temp_df


def stock_kc_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-科创板-实时行情
    https://quote.eastmoney.com/center/gridlist.html#kcb_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://7.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "wbp2u": "|0|0|0|web",
        "fid": "f12",
        "fs": "m:1 t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,"
        "f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )
    return temp_df


def stock_zh_ab_comparison_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价
    https://quote.eastmoney.com/center/gridlist.html#ab_comparison
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "np": "1",
        "fltt": "1",
        "invt": "2",
        "fs": "m:1+b:BK0498,m:0+b:BK0498",
        "fields": "f201,f202,f203,f196,f200,f197,f152,f12,f13,f14,f1,f2,f4,f3,f199",
        "fid": "f199",
        "pn": "1",
        "pz": "100",
        "po": "1",
        "dect": "1",
        "wbp2u": "|0|0|0|web",
    }
    columns_map = {
        "index": "序号",
        "f1": "-",
        "f2": "最新价B",
        "f3": "涨跌幅B",
        "f4": "-",
        "f12": "A股代码",
        "f13": "-",
        "f14": "A股名称",
        "f152": "-",
        "f196": "最新价A",
        "f197": "涨跌幅A",
        "f199": "比价",
        "f200": "-",
        "f201": "B股代码",
        "f202": "-",
        "f203": "B股名称",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df = temp_df.rename(columns=columns_map)
    list_name = [value for key, value in columns_map.items() if value != "_"]
    temp_df = temp_df[list_name]
    temp_df = temp_df[
        [
            "序号",
            "B股代码",
            "B股名称",
            "最新价B",
            "涨跌幅B",
            "A股代码",
            "A股名称",
            "最新价A",
            "涨跌幅A",
            "比价",
        ]
    ]
    temp_df["最新价B"] = pd.to_numeric(temp_df["最新价B"], errors="coerce") / 100
    temp_df["涨跌幅B"] = pd.to_numeric(temp_df["涨跌幅B"], errors="coerce") / 100
    temp_df["最新价A"] = pd.to_numeric(temp_df["最新价A"], errors="coerce") / 100
    temp_df["涨跌幅A"] = pd.to_numeric(temp_df["涨跌幅A"], errors="coerce") / 100
    temp_df["比价"] = pd.to_numeric(temp_df["比价"], errors="coerce") / 100
    return temp_df


def stock_zh_b_spot_em() -> pd.DataFrame:
    """
    东方财富网- B 股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://28.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:0 t:7,m:1 t:3",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20"
        ",f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "5分钟涨跌",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "涨速",
        "市净率",
        "60日涨跌幅",
        "年初至今涨跌幅",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
            "总市值",
            "流通市值",
            "涨速",
            "5分钟涨跌",
            "60日涨跌幅",
            "年初至今涨跌幅",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df["涨速"] = pd.to_numeric(temp_df["涨速"], errors="coerce")
    temp_df["5分钟涨跌"] = pd.to_numeric(temp_df["5分钟涨跌"], errors="coerce")
    temp_df["60日涨跌幅"] = pd.to_numeric(temp_df["60日涨跌幅"], errors="coerce")
    temp_df["年初至今涨跌幅"] = pd.to_numeric(
        temp_df["年初至今涨跌幅"], errors="coerce"
    )
    return temp_df


def stock_zh_a_hist(
    symbol: str = "000001",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "20500101",
    adjust: str = "",
    timeout: float = None,
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日行情
    https://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
    :type adjust: str
    :param timeout: choice of None or a positive float number
    :type timeout: float
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    market_code = 1 if symbol.startswith("6") else 0
    adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
    period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "klt": period_dict[period],
        "fqt": adjust_dict[adjust],
        "secid": f"{market_code}.{symbol}",
        "beg": start_date,
        "end": end_date,
    }
    r = requests.get(url, params=params, timeout=timeout)
    data_json = r.json()
    if not (data_json["data"] and data_json["data"]["klines"]):
        return pd.DataFrame()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df["股票代码"] = symbol
    temp_df.columns = [
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "振幅",
        "涨跌幅",
        "涨跌额",
        "换手率",
        "股票代码",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df = temp_df[
        [
            "日期",
            "股票代码",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
    ]
    return temp_df


def stock_zh_a_hist_min_em(
    symbol: str = "000001",
    start_date: str = "1979-09-01 09:32:00",
    end_date: str = "2222-01-01 09:32:00",
    period: str = "5",
    adjust: str = "",
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日分时行情
    https://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param period: choice of {'1', '5', '15', '30', '60'}
    :type period: str
    :param adjust: choice of {'', 'qfq', 'hfq'}
    :type adjust: str
    :return: 每日分时行情
    :rtype: pandas.DataFrame
    """
    market_code = 1 if symbol.startswith("6") else 0
    adjust_map = {
        "": "0",
        "qfq": "1",
        "hfq": "2",
    }
    if period == "1":
        url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "ndays": "5",
            "iscr": "0",
            "secid": f"{market_code}.{symbol}",
        }
        r = requests.get(url, timeout=15, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["trends"]]
        )
        temp_df.columns = [
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "均价",
        ]
        temp_df.index = pd.to_datetime(temp_df["时间"])
        temp_df = temp_df[start_date:end_date]
        temp_df.reset_index(drop=True, inplace=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["均价"] = pd.to_numeric(temp_df["均价"], errors="coerce")
        temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
        return temp_df
    else:
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "klt": period,
            "fqt": adjust_map[adjust],
            "secid": f"{market_code}.{symbol}",
            "beg": "0",
            "end": "20500000",
        }
        r = requests.get(url, timeout=15, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["klines"]]
        )
        temp_df.columns = [
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["时间"])
        temp_df = temp_df[start_date:end_date]
        temp_df.reset_index(drop=True, inplace=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
        temp_df = temp_df[
            [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "涨跌幅",
                "涨跌额",
                "成交量",
                "成交额",
                "振幅",
                "换手率",
            ]
        ]
        return temp_df


def stock_zh_a_hist_pre_min_em(
    symbol: str = "000001",
    start_time: str = "09:00:00",
    end_time: str = "15:50:00",
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日分时行情包含盘前数据
    https://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param start_time: 开始时间
    :type start_time: str
    :param end_time: 结束时间
    :type end_time: str
    :return: 每日分时行情包含盘前数据
    :rtype: pandas.DataFrame
    """
    market_code = 1 if symbol.startswith("6") else 0
    url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "ndays": "1",
        "iscr": "1",
        "iscca": "0",
        "secid": f"{market_code}.{symbol}",
    }
    r = requests.get(url, timeout=15, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["trends"]])
    temp_df.columns = [
        "时间",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "最新价",
    ]
    temp_df.index = pd.to_datetime(temp_df["时间"])
    date_format = temp_df.index[0].date().isoformat()
    temp_df = temp_df[date_format + " " + start_time : date_format + " " + end_time]
    temp_df.reset_index(drop=True, inplace=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
    return temp_df


def stock_hk_spot_em() -> pd.DataFrame:
    """
    东方财富网-港股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hk_stocks
    :return: 港股-实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://72.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:128 t:3,m:128 t:4,m:128 t:1,m:128 t:2",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,"
        "f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "_",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "_",
        "_",
        "_",
        "市净率",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "今开",
            "最高",
            "最低",
            "昨收",
            "成交量",
            "成交额",
        ]
    ]
    temp_df["序号"] = pd.to_numeric(temp_df["序号"], errors="coerce")
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    return temp_df


def stock_hk_main_board_spot_em() -> pd.DataFrame:
    """
    东方财富网-港股-主板-实时行情
    https://quote.eastmoney.com/center/gridlist.html#hk_mainboard
    :return: 港股-主板-实时行情
    :rtype: pandas.DataFrame
    """
    url = "https://81.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:128 t:3",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,"
        "f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "_",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "_",
        "_",
        "_",
        "市净率",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "今开",
            "最高",
            "最低",
            "昨收",
            "成交量",
            "成交额",
        ]
    ]
    temp_df["序号"] = pd.to_numeric(temp_df["序号"], errors="coerce")
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    return temp_df


def stock_hk_hist(
    symbol: str = "00593",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "22220101",
    adjust: str = "",
) -> pd.DataFrame:
    """
    东方财富网-行情-港股-每日行情
    https://quote.eastmoney.com/hk/08367.html
    :param symbol: 港股-每日行情
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "1", "hfq": "2", "": "不复权"}
    :type adjust: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
    period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
    url = "https://33.push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "secid": f"116.{symbol}",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": period_dict[period],
        "fqt": adjust_dict[adjust],
        "end": "20500000",
        "lmt": "1000000",
    }
    r = requests.get(url, timeout=15, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    if temp_df.empty:
        return pd.DataFrame()
    temp_df.columns = [
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "振幅",
        "涨跌幅",
        "涨跌额",
        "换手率",
    ]
    temp_df.index = pd.to_datetime(temp_df["日期"], errors="coerce")
    temp_df = temp_df[start_date:end_date]
    if temp_df.empty:
        return pd.DataFrame()
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    return temp_df


def stock_hk_hist_min_em(
    symbol: str = "01611",
    period: str = "1",
    adjust: str = "",
    start_date: str = "1979-09-01 09:32:00",
    end_date: str = "2222-01-01 09:32:00",
) -> pd.DataFrame:
    """
    东方财富网-行情-港股-每日分时行情
    https://quote.eastmoney.com/hk/00948.html
    :param symbol: 股票代码
    :type symbol: str
    :param period: choice of {'1', '5', '15', '30', '60'}
    :type period: str
    :param adjust: choice of {'', 'qfq', 'hfq'}
    :type adjust: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日分时行情
    :rtype: pandas.DataFrame
    """
    adjust_map = {
        "": "0",
        "qfq": "1",
        "hfq": "2",
    }
    if period == "1":
        url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "iscr": "0",
            "ndays": "5",
            "secid": f"116.{symbol}",
        }
        r = requests.get(url, timeout=15, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["trends"]]
        )
        temp_df.columns = [
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "最新价",
        ]
        temp_df.index = pd.to_datetime(temp_df["时间"])
        temp_df = temp_df[start_date:end_date]
        temp_df.reset_index(drop=True, inplace=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
        return temp_df
    else:
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "klt": period,
            "fqt": adjust_map[adjust],
            "secid": f"116.{symbol}",
            "beg": "0",
            "end": "20500000",
        }
        r = requests.get(url, timeout=15, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["klines"]]
        )
        temp_df.columns = [
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["时间"])
        temp_df = temp_df[start_date:end_date]
        temp_df.reset_index(drop=True, inplace=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
        temp_df = temp_df[
            [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "涨跌幅",
                "涨跌额",
                "成交量",
                "成交额",
                "振幅",
                "换手率",
            ]
        ]
    return temp_df


def stock_us_spot_em() -> pd.DataFrame:
    """
    东方财富网-美股-实时行情
    https://quote.eastmoney.com/center/gridlist.html#us_stocks
    :return: 美股-实时行情；延迟 15 min
    :rtype: pandas.DataFrame
    """
    url = "https://72.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f12",
        "fs": "m:105,m:106,m:107",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,"
        "f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152",
    }
    temp_df = fetch_paginated_data(url, params)
    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "_",
        "_",
        "_",
        "简称",
        "编码",
        "名称",
        "最高价",
        "最低价",
        "开盘价",
        "昨收价",
        "总市值",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "市盈率",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df["代码"] = temp_df["编码"].astype(str) + "." + temp_df["简称"]
    temp_df = temp_df[
        [
            "序号",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "开盘价",
            "最高价",
            "最低价",
            "昨收价",
            "总市值",
            "市盈率",
            "成交量",
            "成交额",
            "振幅",
            "换手率",
            "代码",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
    temp_df["昨收价"] = pd.to_numeric(temp_df["昨收价"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["市盈率"] = pd.to_numeric(temp_df["市盈率"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    return temp_df


def stock_us_hist(
    symbol: str = "105.MSFT",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "22220101",
    adjust: str = "",
) -> pd.DataFrame:
    """
    东方财富网-行情-美股-每日行情
    https://quote.eastmoney.com/us/ENTX.html#fullScreenChart
    :param symbol: 股票代码；此股票代码需要通过调用 ak.stock_us_spot_em() 的 `代码` 字段获取
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "1", "hfq": "2", "": "不复权"}
    :type adjust: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
    adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
    url = "https://63.push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "secid": f"{symbol}",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": period_dict[period],
        "fqt": adjust_dict[adjust],
        "end": "20500000",
        "lmt": "1000000",
    }
    r = requests.get(url, timeout=15, params=params)
    data_json = r.json()
    if not data_json["data"]["klines"]:
        return pd.DataFrame()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = [
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "振幅",
        "涨跌幅",
        "涨跌额",
        "换手率",
    ]
    temp_df.index = pd.to_datetime(temp_df["日期"], errors="coerce")
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df.sort_values(["日期"], inplace=True, ignore_index=True)
    return temp_df


def stock_us_hist_min_em(
    symbol: str = "105.ATER",
    start_date: str = "1979-09-01 09:32:00",
    end_date: str = "2222-01-01 09:32:00",
) -> pd.DataFrame:
    """
    东方财富网-行情首页-美股-每日分时行情
    https://quote.eastmoney.com/us/ATER.html
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日分时行情
    :rtype: pandas.DataFrame
    """
    url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "iscr": "0",
        "ndays": "5",
        "secid": f"{symbol.split('.')[0]}.{symbol.split('.')[1]}",
    }
    r = requests.get(url, params=params, timeout=15)
    data_json = r.json()
    if not data_json["data"]["trends"]:
        return pd.DataFrame()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["trends"]])
    temp_df.columns = [
        "时间",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "最新价",
    ]
    temp_df.index = pd.to_datetime(temp_df["时间"], errors="coerce")
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(drop=True, inplace=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["时间"] = pd.to_datetime(temp_df["时间"], errors="coerce").astype(str)
    return temp_df


if __name__ == "__main__":
    stock_zh_a_spot_em_df = stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)

    stock_sh_a_spot_em_df = stock_sh_a_spot_em()
    print(stock_sh_a_spot_em_df)

    stock_sz_a_spot_em_df = stock_sz_a_spot_em()
    print(stock_sz_a_spot_em_df)

    stock_bj_a_spot_em_df = stock_bj_a_spot_em()
    print(stock_bj_a_spot_em_df)

    stock_new_a_spot_em_df = stock_new_a_spot_em()
    print(stock_new_a_spot_em_df)

    stock_cy_a_spot_em_df = stock_cy_a_spot_em()
    print(stock_cy_a_spot_em_df)

    stock_kc_a_spot_em_df = stock_kc_a_spot_em()
    print(stock_kc_a_spot_em_df)

    stock_zh_b_spot_em_df = stock_zh_b_spot_em()
    print(stock_zh_b_spot_em_df)

    stock_hk_spot_em_df = stock_hk_spot_em()
    print(stock_hk_spot_em_df)

    stock_hk_main_board_spot_em_df = stock_hk_main_board_spot_em()
    print(stock_hk_main_board_spot_em_df)

    stock_zh_a_hist_df = stock_zh_a_hist(
        symbol="600734",
        period="daily",
        start_date="20050501",
        end_date="20250304",
        adjust="hfq",
    )
    print(stock_zh_a_hist_df)

    stock_zh_a_hist_min_em_df = stock_zh_a_hist_min_em(symbol="603777", period="1")
    print(stock_zh_a_hist_min_em_df)

    stock_zh_a_hist_pre_min_em_df = stock_zh_a_hist_pre_min_em(symbol="000001")
    print(stock_zh_a_hist_pre_min_em_df)

    stock_hk_hist_df = stock_hk_hist(
        symbol="00593",
        period="daily",
        start_date="19700101",
        end_date="22220101",
        adjust="",
    )
    print(stock_hk_hist_df)

    stock_hk_hist_qfq_df = stock_hk_hist(
        symbol="00593",
        period="daily",
        start_date="19700101",
        end_date="22220101",
        adjust="qfq",
    )
    print(stock_hk_hist_qfq_df)

    stock_hk_hist_hfq_df = stock_hk_hist(
        symbol="00593",
        period="daily",
        start_date="19700101",
        end_date="22220101",
        adjust="hfq",
    )
    print(stock_hk_hist_hfq_df)

    stock_us_spot_em_df = stock_us_spot_em()
    print(stock_us_spot_em_df)

    stock_us_hist_df = stock_us_hist(
        symbol="106.TTE",
        period="daily",
        start_date="20200101",
        end_date="20240414",
        adjust="qfq",
    )
    print(stock_us_hist_df)

    stock_zh_a_spot_em_df = stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)

    stock_hk_hist_min_em_df = stock_hk_hist_min_em(symbol="01611")
    print(stock_hk_hist_min_em_df)

    stock_us_spot_em_df = stock_us_spot_em()
    print(stock_us_spot_em_df)

    stock_us_hist_min_em_df = stock_us_hist_min_em(symbol="106.TTE")
    print(stock_us_hist_min_em_df)

    stock_us_hist_min_em_df = stock_us_hist_min_em(symbol="105.ATER")
    print(stock_us_hist_min_em_df)

    stock_zh_a_hist_min_em_df = stock_zh_a_hist_min_em(
        symbol="300364",
        start_date="2025-03-07 09:30:00",
        end_date="2025-03-07 15:00:00",
        period="5",
        adjust="hfq",
    )
    print(stock_zh_a_hist_min_em_df)

    stock_zh_a_hist_df = stock_zh_a_hist(
        symbol="833454",
        period="daily",
        start_date="20170301",
        end_date="20241115",
        adjust="hfq",
    )
    print(stock_zh_a_hist_df)

    stock_hk_hist_min_em_df = stock_hk_hist_min_em(
        symbol="01611",
        period="1",
        adjust="",
        start_date="2025-03-07 09:30:00",
        end_date="2025-03-07 18:32:00",
    )
    print(stock_hk_hist_min_em_df)

    stock_zh_b_spot_em_df = stock_zh_b_spot_em()
    print(stock_zh_b_spot_em_df)
