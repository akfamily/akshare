#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/6/30 22:00
Desc: 中国-国家统计局-宏观数据
https://data.stats.gov.cn/dg/website/page.html
"""

import datetime
from functools import lru_cache
import re
from typing import Dict, List, Literal, Union

import pandas as pd
from curl_cffi import requests as curl_requests

_NBS_SESSION = None
_KIND_CONFIG: Dict[str, Dict[str, Union[int, str]]] = {
    "月度数据": {"code": 1, "route": "monthData"},
    "季度数据": {"code": 2, "route": "quarterData"},
    "年度数据": {"code": 3, "route": "yearData"},
    "分省月度数据": {"code": 4, "route": "fsMonthData"},
    "分省季度数据": {"code": 5, "route": "fsQuarterData"},
    "分省年度数据": {"code": 6, "route": "fsYearData"},
    "主要城市月度价格": {"code": 7, "route": "mainMonthData"},
    "主要城市年度数据": {"code": 8, "route": "mainYearData"},
    "港澳台月度数据": {"code": 9, "route": "monthData"},
    "港澳台年度数据": {"code": 10, "route": "yearData"},
}


def _get_nbs_headers(route: str) -> Dict[str, str]:
    """
    获取国家统计局新站请求头。

    :param route: 页面路由
    :type route: str
    :return: 请求头
    :rtype: Dict[str, str]
    """
    _ = route
    return {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/dg/website/page.html#/pc/national/monthData",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
    }


def _get_nbs_session() -> curl_requests.Session:
    """
    获取已预热的国家统计局会话。

    :return: 已预热会话
    :rtype: curl_requests.Session
    """
    global _NBS_SESSION
    if _NBS_SESSION is None:
        _NBS_SESSION = curl_requests.Session(impersonate="chrome")
        _NBS_SESSION.get(
            "https://data.stats.gov.cn/dg/website/page.html#/pc/national/monthData",
            headers=_get_nbs_headers("monthData"),
            timeout=30,
        )
    return _NBS_SESSION


def _normalize_nbs_text(text: str) -> str:
    """
    规范化国家统计局返回的文本。

    :param text: 原始文本
    :type text: str
    :return: 规范化后的文本
    :rtype: str
    """
    return re.sub(r"\s+", "", text or "")


def _get_nbs_granularity(kind: str) -> str:
    """
    根据数据类别返回时间粒度。

    :param kind: 数据类别
    :type kind: str
    :return: 时间粒度
    :rtype: str
    """
    if "月度" in kind:
        return "month"
    if "季度" in kind:
        return "quarter"
    return "year"


@lru_cache
def _get_nbs_tree(pid: str, code: int, route: str) -> List[Dict]:
    """
    获取国家统计局新站目录树节点。

    :param pid: 父节点 ID
    :type pid: str
    :param code: 数据类别编码
    :type code: int
    :param route: 页面路由
    :type route: str
    :return: 当前层级节点列表
    :rtype: List[Dict]
    """
    url = "https://data.stats.gov.cn/dg/website/publicrelease/web/external/new/queryIndexTreeAsync"
    r = _get_nbs_session().get(
        url,
        params={"pid": pid, "code": code},
        headers=_get_nbs_headers(route),
        timeout=30,
    )
    data_json = r.json()
    return data_json.get("data", [])


@lru_cache
def _get_nbs_root_id(code: int, route: str) -> str:
    """
    获取国家统计局新站某类数据的根节点 ID。

    :param code: 数据类别编码
    :type code: int
    :param route: 页面路由
    :type route: str
    :return: 根节点 ID
    :rtype: str
    """
    root_nodes = _get_nbs_tree("", code, route)
    if not root_nodes:
        raise ValueError("Failed to load the NBS root catalog.")
    return root_nodes[0]["_id"]


@lru_cache
def _get_nbs_indicators(cid: str, route: str) -> List[Dict]:
    """
    获取目录下的可选指标列表。

    :param cid: 目录叶子节点 ID
    :type cid: str
    :param route: 页面路由
    :type route: str
    :return: 指标列表
    :rtype: List[Dict]
    """
    url = "https://data.stats.gov.cn/dg/website/publicrelease/web/external/new/queryIndicatorsByCid"
    r = _get_nbs_session().get(
        url,
        params={"cid": cid, "dt": "", "name": ""},
        headers=_get_nbs_headers(route),
        timeout=30,
    )
    data_json = r.json()
    return data_json.get("data", {}).get("list", [])


@lru_cache
def _get_nbs_da_catalogs(cid: str, route: str) -> List[Dict]:
    """
    获取目录的地区维度分组。

    :param cid: 目录叶子节点 ID
    :type cid: str
    :param route: 页面路由
    :type route: str
    :return: 地区维度分组
    :rtype: List[Dict]
    """
    url = "https://data.stats.gov.cn/dg/website/publicrelease/web/external/getDaCatalogTreeByIndicatorCid"
    r = _get_nbs_session().get(
        url,
        params={"indicatorCid": cid},
        headers=_get_nbs_headers(route),
        timeout=30,
    )
    data_json = r.json()
    return data_json.get("data", [])


@lru_cache
def _get_nbs_da_members(da_cid: str, route: str) -> List[Dict]:
    """
    获取地区分组下的地区成员。

    :param da_cid: 地区分组 ID
    :type da_cid: str
    :param route: 页面路由
    :type route: str
    :return: 地区成员列表
    :rtype: List[Dict]
    """
    url = "https://data.stats.gov.cn/dg/website/publicrelease/web/external/getDasByDaCatalogId"
    r = _get_nbs_session().get(
        url,
        params={"daCid": da_cid},
        headers=_get_nbs_headers(route),
        timeout=30,
    )
    data_json = r.json()
    return data_json.get("data", [])


def _find_nbs_node_by_name(nodes: List[Dict], name: str) -> Dict:
    """
    根据名称查找目录节点。

    :param nodes: 节点列表
    :type nodes: List[Dict]
    :param name: 节点名称
    :type name: str
    :return: 匹配到的节点
    :rtype: Dict
    """
    target_name = _normalize_nbs_text(name)
    for item in nodes:
        if _normalize_nbs_text(item.get("name", item.get("_name", ""))) == target_name:
            return item
    raise ValueError("Please check if the data path or indicator is correct.")


def _format_nbs_indicator_name(item: Dict) -> str:
    """
    将新站指标名格式化为旧接口更稳定的风格。

    :param item: 指标信息
    :type item: Dict
    :return: 格式化后的指标名称
    :rtype: str
    """
    label = _normalize_nbs_text(item.get("i_showname", ""))
    if not label:
        label = _normalize_nbs_text(item.get("ek_dp_name", ""))
    if not label:
        label = _normalize_nbs_text(item.get("_name", ""))
    match = re.match(
        r"^(.*?)(累计值|当期值|本期值|期末值|平均值|同比增长率|同比增长|增长率|增速)(\([^)]*\))?$",
        label,
    )
    if match:
        prefix, suffix, unit = match.groups()
        return f"{prefix}_{suffix}{unit or ''}"
    return label


def _find_nbs_indicator(indicators: List[Dict], name: str) -> Dict:
    """
    根据名称查找具体指标。

    :param indicators: 指标列表
    :type indicators: List[Dict]
    :param name: 指标名称
    :type name: str
    :return: 指标信息
    :rtype: Dict
    """
    target_name = _normalize_nbs_text(name).replace("_", "")
    for item in indicators:
        candidates = {
            _normalize_nbs_text(item.get("i_showname", "")).replace("_", ""),
            _format_nbs_indicator_name(item).replace("_", ""),
            _normalize_nbs_text(item.get("ek_dp_name", "")).replace("_", ""),
            _normalize_nbs_text(item.get("_name", "")).replace("_", ""),
        }
        if target_name in candidates:
            return item
    raise ValueError("Please check if the data path or indicator is correct.")


def _resolve_nbs_catalog(kind: str, path: str) -> Dict[str, Union[str, int]]:
    """
    根据路径解析到最终目录节点。

    :param kind: 数据类别
    :type kind: str
    :param path: 数据路径
    :type path: str
    :return: 目录解析结果
    :rtype: Dict[str, Union[str, int]]
    """
    config = _KIND_CONFIG[kind]
    code = int(config["code"])
    route = str(config["route"])
    node_id = _get_nbs_root_id(code, route)
    for item in [part.strip() for part in path.split(">") if part.strip()]:
        nodes = _get_nbs_tree(node_id, code, route)
        target_node = _find_nbs_node_by_name(nodes, item)
        node_id = target_node["_id"]
    return {"cid": node_id, "root_id": _get_nbs_root_id(code, route), "route": route}


def _encode_nbs_period_token(token: str, granularity: str) -> str:
    """
    将旧接口时间格式转换为新站 dts 编码。

    :param token: 原始时间片段
    :type token: str
    :param granularity: 时间粒度
    :type granularity: str
    :return: 编码后的时间片段
    :rtype: str
    """
    token = token.strip().upper()
    if granularity == "year":
        if re.fullmatch(r"\d{4}(YY)?", token):
            return token if token.endswith("YY") else f"{token}YY"
    elif granularity == "month":
        if re.fullmatch(r"\d{6}MM", token):
            return token
        if re.fullmatch(r"\d{6}", token):
            return f"{token}MM"
    elif granularity == "quarter":
        if re.fullmatch(r"\d{6}SS", token):
            return token
        quarter_map = {"A": "01", "B": "02", "C": "03", "D": "04"}
        if re.fullmatch(r"\d{4}[ABCD]", token):
            return f"{token[:4]}{quarter_map[token[-1]]}SS"
        if re.fullmatch(r"\d{5}", token) and token[-1] in "1234":
            return f"{token[:4]}0{token[-1]}SS"
    raise ValueError("Please check if the period parameter is correct.")


def _get_last_completed_period(granularity: str) -> str:
    """
    获取最近一个完整统计周期。

    :param granularity: 时间粒度
    :type granularity: str
    :return: 最近完整周期编码
    :rtype: str
    """
    today = datetime.date.today()
    if granularity == "month":
        first_day = today.replace(day=1)
        last_month_day = first_day - datetime.timedelta(days=1)
        return f"{last_month_day.year}{last_month_day.month:02d}MM"
    if granularity == "quarter":
        quarter = (today.month - 1) // 3 + 1
        year = today.year
        quarter -= 1
        if quarter == 0:
            year -= 1
            quarter = 4
        return f"{year}0{quarter}SS"
    return f"{today.year - 1}YY"


def _shift_nbs_period(code: str, granularity: str, offset: int) -> str:
    """
    对周期编码做偏移计算。

    :param code: 周期编码
    :type code: str
    :param granularity: 时间粒度
    :type granularity: str
    :param offset: 偏移量
    :type offset: int
    :return: 偏移后的周期编码
    :rtype: str
    """
    if granularity == "month":
        year = int(code[:4])
        month = int(code[4:6])
        total = year * 12 + (month - 1) + offset
        new_year, new_month = divmod(total, 12)
        return f"{new_year}{new_month + 1:02d}MM"
    if granularity == "quarter":
        year = int(code[:4])
        quarter = int(code[4:6])
        total = year * 4 + (quarter - 1) + offset
        new_year, new_quarter = divmod(total, 4)
        return f"{new_year}0{new_quarter + 1}SS"
    year = int(code[:4]) + offset
    return f"{year}YY"


def _build_nbs_dts(period: str, granularity: str) -> List[str]:
    """
    构造新站接口使用的 dts 参数。

    :param period: 旧接口时间参数
    :type period: str
    :param granularity: 时间粒度
    :type granularity: str
    :return: dts 列表
    :rtype: List[str]
    """
    period = period.strip()
    if not period:
        return []
    if period.lower().startswith("last"):
        count = int(period[4:])
        end_code = _get_last_completed_period(granularity)
        start_code = _shift_nbs_period(end_code, granularity, -(count - 1))
        return [f"{start_code}-{end_code}"]
    if "-" in period:
        start_text, end_text = [item.strip() for item in period.split("-", maxsplit=1)]
        if granularity != "year" and re.fullmatch(r"\d{4}", start_text):
            start_text = (
                f"{start_text}01" if granularity == "month" else f"{start_text}A"
            )
        start_code = _encode_nbs_period_token(start_text, granularity)
        if not end_text:
            end_code = _get_last_completed_period(granularity)
        else:
            if granularity == "month" and re.fullmatch(r"\d{4}", end_text):
                end_text = f"{end_text}12"
            elif granularity == "quarter" and re.fullmatch(r"\d{4}", end_text):
                end_text = f"{end_text}D"
            end_code = _encode_nbs_period_token(end_text, granularity)
        return [f"{start_code}-{end_code}"]
    token_list = [item.strip() for item in period.split(",") if item.strip()]
    if len(token_list) == 1:
        token = token_list[0]
        if granularity == "month" and re.fullmatch(r"\d{4}", token):
            return [f"{token}01MM", f"{token}12MM"]
        if granularity == "quarter" and re.fullmatch(r"\d{4}", token):
            return [f"{token}01SS", f"{token}04SS"]
        return [_encode_nbs_period_token(token, granularity)]
    result = []
    for item in token_list:
        if granularity == "month" and re.fullmatch(r"\d{4}", item):
            result.extend([f"{item}01MM", f"{item}12MM"])
        elif granularity == "quarter" and re.fullmatch(r"\d{4}", item):
            result.extend([f"{item}01SS", f"{item}04SS"])
        else:
            result.append(_encode_nbs_period_token(item, granularity))
    return result


def _convert_nbs_value(value: str) -> Union[float, None]:
    """
    转换数值字符串。

    :param value: 原始值
    :type value: str
    :return: 转换后的值
    :rtype: Union[float, None]
    """
    if value in ("", None):
        return None
    return pd.to_numeric(value, errors="coerce")


def _format_nbs_period_name(name: str) -> str:
    """
    规范化返回的时间名称。

    :param name: 原始时间名称
    :type name: str
    :return: 规范化后的时间名称
    :rtype: str
    """
    return _normalize_nbs_text(name)


def _post_nbs_es_data(
    cid: str,
    root_id: str,
    route: str,
    indicator_ids: List[str],
    das: List[Dict[str, str]],
    show_type: Union[int, str],
    dts: List[str],
) -> List[Dict]:
    """
    请求国家统计局新站数据流接口。

    :param cid: 目录叶子节点 ID
    :type cid: str
    :param root_id: 根节点 ID
    :type root_id: str
    :param route: 页面路由
    :type route: str
    :param indicator_ids: 指标 ID 列表
    :type indicator_ids: List[str]
    :param das: 地区列表
    :type das: List[Dict[str, str]]
    :param show_type: 展示类型
    :type show_type: Union[int, str]
    :param dts: 时间参数列表
    :type dts: List[str]
    :return: 数据列表
    :rtype: List[Dict]
    """
    url = (
        "https://data.stats.gov.cn/dg/website/publicrelease/web/external/stream/esData"
    )
    payload = {
        "cid": cid,
        "indicatorIds": indicator_ids,
        "daCatalogId": "",
        "das": das,
        "showType": show_type,
        "rootId": root_id,
    }
    if dts:
        payload["dts"] = dts
    r = _get_nbs_session().post(
        url,
        json=payload,
        headers=_get_nbs_headers(route),
        timeout=30,
    )
    data_json = r.json()
    return data_json.get("data", [])


def macro_china_nbs_nation(
    kind: Literal["月度数据", "季度数据", "年度数据"], path: str, period: str = "LAST10"
) -> pd.DataFrame:
    """
    国家统计局全国数据通用接口
    https://data.stats.gov.cn/dg/website/page.html
    :param kind: 数据类别
    :param path: 数据路径
    :param period: 时间区间，例如'LAST10', '2016-2023', '2016-'等
    :return: 国家统计局统计数据
    :rtype: pandas.DataFrame
    """
    catalog_info = _resolve_nbs_catalog(kind=kind, path=path)
    cid = str(catalog_info["cid"])
    root_id = str(catalog_info["root_id"])
    route = str(catalog_info["route"])
    indicators = _get_nbs_indicators(cid, route)
    data_list = _post_nbs_es_data(
        cid=cid,
        root_id=root_id,
        route=route,
        indicator_ids=[item["_id"] for item in indicators],
        das=[{"text": "全国", "value": "000000000000"}],
        show_type="1",
        dts=_build_nbs_dts(period=period, granularity=_get_nbs_granularity(kind)),
    )
    if not data_list:
        return pd.DataFrame()
    period_names: List[str] = []
    indicator_order: List[str] = []
    data_dict: Dict[str, Dict[str, Union[float, None]]] = {}
    for period_item in data_list:
        period_name = _format_nbs_period_name(period_item["name"])
        period_names.append(period_name)
        for value_item in period_item["values"]:
            indicator_name = _format_nbs_indicator_name(value_item)
            if indicator_name not in indicator_order:
                indicator_order.append(indicator_name)
            data_dict.setdefault(indicator_name, {})[period_name] = _convert_nbs_value(
                value_item.get("value")
            )
    temp_df = pd.DataFrame.from_dict(data_dict, orient="index")
    temp_df = temp_df.reindex(index=indicator_order, columns=period_names)
    temp_df.dropna(axis=1, how="all", inplace=True)
    temp_df.index.name = None
    temp_df.columns.name = None
    return temp_df


def macro_china_nbs_region(
    kind: Literal[
        "分省月度数据",
        "分省季度数据",
        "分省年度数据",
        "主要城市月度价格",
        "主要城市年度数据",
        "港澳台月度数据",
        "港澳台年度数据",
    ],
    path: str,
    indicator: Union[str, None],
    region: Union[str, None] = None,
    period: str = "LAST10",
) -> pd.DataFrame:
    """
    国家统计局地区数据通用接口
    https://data.stats.gov.cn/dg/website/page.html
    :param kind: 数据类别
    :param path: 数据路径
    :param indicator: 指定指标
    :param region:  指定地区 当指定region时，将symbol设为None可以同时获得所有可选指标的值
    :param period: 时间区间，例如'LAST10', '2016-2023', '2016-'等
    :return: 国家统计局统计数据
    :rtype: pandas.DataFrame
    """
    if indicator is None and region is None:
        raise AssertionError("The indicator and region parameters cannot both be None.")
    catalog_info = _resolve_nbs_catalog(kind=kind, path=path)
    cid = str(catalog_info["cid"])
    root_id = str(catalog_info["root_id"])
    route = str(catalog_info["route"])
    indicators = _get_nbs_indicators(cid, route)
    da_catalogs = _get_nbs_da_catalogs(cid, route)
    default_da_catalog = next(
        (
            item
            for item in da_catalogs
            if _normalize_nbs_text(item.get("name", item.get("_name", "")))
            == "全部地区"
        ),
        da_catalogs[0],
    )
    da_members = _get_nbs_da_members(default_da_catalog["_id"], route)
    dts = _build_nbs_dts(period=period, granularity=_get_nbs_granularity(kind))

    if region is None:
        target_indicator = _find_nbs_indicator(indicators, indicator)
        data_list = _post_nbs_es_data(
            cid=cid,
            root_id=root_id,
            route=route,
            indicator_ids=[target_indicator["_id"]],
            das=[
                {"text": item["show_name"], "value": item["name_value"]}
                for item in da_members
            ],
            show_type=3,
            dts=dts,
        )
        if not data_list:
            return pd.DataFrame()
        period_names: List[str] = []
        region_order: List[str] = []
        data_dict: Dict[str, Dict[str, Union[float, None]]] = {}
        title_name = _format_nbs_indicator_name(target_indicator)
        for period_item in data_list:
            period_name = _format_nbs_period_name(period_item["name"])
            period_names.append(period_name)
            for value_item in period_item["values"]:
                region_name = value_item.get("area", value_item.get("da_name", ""))
                if region_name not in region_order:
                    region_order.append(region_name)
                data_dict.setdefault(region_name, {})[period_name] = _convert_nbs_value(
                    value_item.get("value")
                )
        temp_df = pd.DataFrame.from_dict(data_dict, orient="index")
        temp_df = temp_df.reindex(index=region_order, columns=period_names)
        temp_df.dropna(axis=1, how="all", inplace=True)
        temp_df.index.name = None
        temp_df.columns.name = title_name
        return temp_df

    region_item = next(
        (
            item
            for item in da_members
            if _normalize_nbs_text(item.get("show_name", ""))
            == _normalize_nbs_text(region)
        ),
        None,
    )
    if region_item is None:
        raise ValueError("Please check if the data path or indicator is correct.")
    indicator_ids = [item["_id"] for item in indicators]
    if indicator is not None:
        indicator_ids = [_find_nbs_indicator(indicators, indicator)["_id"]]
    data_list = _post_nbs_es_data(
        cid=cid,
        root_id=root_id,
        route=route,
        indicator_ids=indicator_ids,
        das=[{"text": region_item["show_name"], "value": region_item["name_value"]}],
        show_type="1",
        dts=dts,
    )
    if not data_list:
        return pd.DataFrame()
    period_names = []
    indicator_order: List[str] = []
    data_dict = {}
    for period_item in data_list:
        period_name = _format_nbs_period_name(period_item["name"])
        period_names.append(period_name)
        for value_item in period_item["values"]:
            indicator_name = _format_nbs_indicator_name(value_item)
            if indicator_name not in indicator_order:
                indicator_order.append(indicator_name)
            data_dict.setdefault(indicator_name, {})[period_name] = _convert_nbs_value(
                value_item.get("value")
            )
    temp_df = pd.DataFrame.from_dict(data_dict, orient="index")
    temp_df = temp_df.reindex(index=indicator_order, columns=period_names)
    temp_df.dropna(axis=1, how="all", inplace=True)
    temp_df.index.name = None
    temp_df.columns.name = region_item["show_name"]
    return temp_df


if __name__ == "__main__":
    macro_china_nbs_nation_df = macro_china_nbs_nation(
        kind="月度数据",
        path="工业 > 工业分大类行业出口交货值(2018-至今) > 废弃资源综合利用业",
        period="LAST5",
    )
    print(macro_china_nbs_nation_df)

    macro_china_nbs_region_df = macro_china_nbs_region(
        kind="分省季度数据",
        path="人民生活 > 居民人均可支配收入",
        period="2018-2022",
        indicator=None,
        region="北京市",
    )
    print(macro_china_nbs_region_df)

    macro_china_nbs_region_df = macro_china_nbs_region(
        kind="分省季度数据",
        path="国民经济核算 > 地区生产总值",
        period="2018-",
        indicator="地区生产总值_累计值(亿元)",
    )
    print(macro_china_nbs_region_df)
