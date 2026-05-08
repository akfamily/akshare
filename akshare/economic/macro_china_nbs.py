#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/5/8 10:00
Desc: 中国-国家统计局-宏观数据
https://data.stats.gov.cn/dg/website/

NBS 在 2026 年改版后, 老 easyquery.htm 端点被 WAF 拉黑名单 (reason:UrlACL),
本模块改走新版 /dg/website/publicrelease/web/external/* GUID 体系直连.

对外签名 (macro_china_nbs_nation / macro_china_nbs_region) 与旧版兼容.
内部解析 path 中文名到 GUID, 并支持 leaf 节点的多时间切片 fallback.

修复 issues: #7180 #7211 #7216
"""

import json
import re
from functools import lru_cache
from typing import Dict, List, Literal, Optional, Tuple, Union

import pandas as pd
import requests

# ============ 常量 ============

NBS_BASE = "https://data.stats.gov.cn/dg/website/publicrelease/web/external"

# 12 个 dataset 根节点 (探测得到, 老版只暴露 10 种 kind)
_DATASETS: Dict[str, Dict[str, str]] = {
    "1": {"name": "月度数据", "root_id": "fc982599aa684be7969d7b90b1bd0e84"},
    "2": {"name": "季度数据", "root_id": "a94b8b7365a94874968cabbe392cf679"},
    "3": {"name": "年度数据", "root_id": "884c062607104a91967b22742537f44f"},
    "4": {"name": "分省月度数据", "root_id": "f4c6cd795fea436c807163397dd36b98"},
    "5": {"name": "分省季度数据", "root_id": "854f819b04104191a5ae2f2cba270e6c"},
    "6": {"name": "分省年度数据", "root_id": "c4d82af16c3d4f0cb4f09d4af7d5888e"},
    "7": {"name": "主要城市月度价格", "root_id": "327ecbb2e6b14c669da1e99e39faa24c"},
    "8": {"name": "主要城市年度数据", "root_id": "2d06bab01494417e9052ef0f8d93e23e"},
    "9": {"name": "港澳台月度数据", "root_id": "bbf7c2c592a140e295423bc2e7f5cd36"},
    "10": {"name": "港澳台年度数据", "root_id": "df5df037aa03435888766cde0aa303dd"},
}
_KIND_TO_CODE: Dict[str, str] = {m["name"]: c for c, m in _DATASETS.items()}

# kind → period 后缀 (月度 MM / 季度 SS 序号 01-04 / 年度 YY)
_KIND_TO_SUFFIX: Dict[str, str] = {
    "月度数据": "MM",
    "分省月度数据": "MM",
    "季度数据": "SS",
    "分省季度数据": "SS",
    "年度数据": "YY",
    "分省年度数据": "YY",
    "主要城市月度价格": "MM",
    "主要城市年度数据": "YY",
    "港澳台月度数据": "MM",
    "港澳台年度数据": "YY",
}

_HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://data.stats.gov.cn",
    "Referer": "https://data.stats.gov.cn/dg/website/page.html",
}

_session: Optional[requests.Session] = None


def _get_session() -> requests.Session:
    """Lazy 持久 Session — 必须 lazy, 绝不 import-time 网络请求.

    NBS WAF 偶发会 307 + Set-Cookie (wzws_cid) challenge, 持久 Session
    自动 carry cookie 跟随 redirect.
    """
    global _session
    if _session is None:
        s = requests.Session()
        s.headers.update(_HTTP_HEADERS)
        try:
            s.get("https://data.stats.gov.cn/dg/website/page.html", timeout=15)
        except requests.RequestException:
            pass
        _session = s
    return _session


def _request_json(method: str, url: str, **kwargs) -> Union[dict, list]:
    """统一 HTTP 请求 + JSON 解析 + WAF 检测.

    NBS WAF 在错误请求 (例 dts 字符串形态而非 list) 时返 200 + HTML 而不是 JSON,
    必须显式检查 Content-Type.
    """
    s = _get_session()
    kwargs.setdefault("timeout", 30)
    resp = s.request(method, url, **kwargs)
    resp.raise_for_status()
    ctype = resp.headers.get("Content-Type", "").lower()
    if "html" in ctype or resp.text.lstrip().startswith("<"):
        raise RuntimeError(
            "NBS WAF 拦截 (返 HTML 而非 JSON), 请检查请求参数 (例 dts 必须是 list)"
        )
    return resp.json()


# ============ 名字归一 + leaf 时间切片解析 ============


def _normalize(name: Optional[str]) -> str:
    """归一 NBS 节点名用于比较.

    NBS 改版后 catalog name 加了空格 (例 '居民消费价格分类指数 (上年同月=100) ');
    老版用户传值习惯 '居民消费价格分类指数(上年同月=100)' 或 '地区生产总值_累计值(亿元)'.
    比较时双方都 normalize 才能稳定匹配.
    """
    if not name:
        return ""
    n = name.replace(" ", "").replace("　", "")
    n = n.replace("（", "(").replace("）", ")").replace("：", ":")
    n = n.replace("_", "")
    return n


_PERIOD_TAIL = re.compile(r"\s*[\(（]\s*(\d{4})?\s*[-—]\s*(\d{4}|至今)?\s*[\)）]\s*$")


def _strip_period_tail(name: str) -> str:
    """去掉末尾时间切片括号. 输入应已 normalized."""
    return _PERIOD_TAIL.sub("", name).strip()


def _parse_slice_range(name: str) -> Optional[Tuple[Optional[int], Optional[int]]]:
    """从 leaf 名末尾切片括号解析时间范围, 返 (start, end) 或 None."""
    m = _PERIOD_TAIL.search(name)
    if not m:
        return None
    s, e = m.group(1), m.group(2)
    start = int(s) if s else None
    end = int(e) if (e and e != "至今") else None
    return (start, end)


# ============ Period 解析 (老版兼容) ============

# 老版文档支持: last10 (大小写) / 201201,201205 / 2012A-D / 2012,2013 / 2013-
_RE_LAST = re.compile(r"^last(\d+)$", re.IGNORECASE)
_RE_RANGE_DASH = re.compile(r"^(\d{4})-(\d{4})?$")
_RE_SINGLE_YEAR = re.compile(r"^(\d{4})$")
_RE_MONTH_TOKEN = re.compile(r"^(\d{4})(\d{2})$")
_RE_QUARTER_TOKEN = re.compile(r"^(\d{4})([ABCD])$", re.IGNORECASE)
_QUARTER_LETTER_TO_IDX = {"A": 1, "B": 2, "C": 3, "D": 4}


def _parse_user_period(period: Optional[str]) -> Dict[str, object]:
    """解析用户 period 字符串成结构化字典.

    支持格式 (与老版 docstring 对齐):
        None / 'last10' / 'LAST10'    → {kind: LATEST, n}
        '2018-2023'                    → {kind: RANGE, start, end}
        '2018-'                        → {kind: OPEN_RANGE, start}
        '2018'                         → {kind: SINGLE, year}
        '201201,201205'  (月度逗号)    → {kind: DISCRETE_MONTH, codes}
        '2012A,2012B'    (季度逗号)    → {kind: DISCRETE_QUARTER, codes}
        '2012,2013'      (年度逗号)    → {kind: DISCRETE_YEAR, codes}
    """
    if period is None or not period.strip():
        return {"kind": "LATEST", "n": 13}
    p = period.strip()

    m = _RE_LAST.match(p)
    if m:
        n = int(m.group(1))
        if n < 1:
            raise ValueError(f"last_N 必须 >= 1, 得到 {period!r}")
        return {"kind": "LATEST", "n": n}

    if "," in p:
        tokens = [t.strip() for t in p.split(",") if t.strip()]
        if all(_RE_MONTH_TOKEN.match(t) for t in tokens):
            codes = [
                (
                    int(_RE_MONTH_TOKEN.match(t).group(1)),
                    int(_RE_MONTH_TOKEN.match(t).group(2)),
                )
                for t in tokens
            ]
            invalid_months = [(y, m) for y, m in codes if not 1 <= m <= 12]
            if invalid_months:
                raise ValueError(
                    f"period 月度离散值含非法月份 {invalid_months}, 月份必须 1-12"
                )
            return {"kind": "DISCRETE_MONTH", "codes": codes}
        if all(_RE_QUARTER_TOKEN.match(t) for t in tokens):
            codes = [
                (
                    int(_RE_QUARTER_TOKEN.match(t).group(1)),
                    _QUARTER_LETTER_TO_IDX[_RE_QUARTER_TOKEN.match(t).group(2).upper()],
                )
                for t in tokens
            ]
            return {"kind": "DISCRETE_QUARTER", "codes": codes}
        if all(_RE_SINGLE_YEAR.match(t) for t in tokens):
            return {"kind": "DISCRETE_YEAR", "codes": [int(t) for t in tokens]}
        raise ValueError(f"period {period!r} 中逗号离散值类型不一致或格式不识别")

    m = _RE_RANGE_DASH.match(p)
    if m:
        start = int(m.group(1))
        end = m.group(2)
        if end is None:
            return {"kind": "OPEN_RANGE", "start": start}
        return {"kind": "RANGE", "start": start, "end": int(end)}

    m = _RE_SINGLE_YEAR.match(p)
    if m:
        return {"kind": "SINGLE", "year": int(m.group(1))}

    raise ValueError(f"无法识别的 period 格式: {period!r}")


# ============ NBS period code 转换 ============


def _parse_nbs_code(code: str) -> Tuple[int, int, str]:
    """NBS code → (year, sub_index, suffix). 例: 202604MM → (2026, 4, MM)."""
    m = re.match(r"^(\d{4})(\d{2})(MM|SS)$", code)
    if m:
        return int(m.group(1)), int(m.group(2)), m.group(3)
    m = re.match(r"^(\d{4})YY$", code)
    if m:
        return int(m.group(1)), 0, "YY"
    raise ValueError(f"无法解析 NBS period code: {code!r}")


def _shift_period(year: int, sub: int, suffix: str, n_back: int) -> Tuple[int, int]:
    """从 (year, sub) 往前推 n_back 期."""
    if suffix == "YY":
        return (year - n_back, 0)
    units = 12 if suffix == "MM" else 4
    total = year * units + (sub - 1) - n_back
    return (total // units, total % units + 1)


def _fmt_nbs_code(year: int, sub: int, suffix: str) -> str:
    if suffix == "YY":
        return f"{year}YY"
    return f"{year:04d}{sub:02d}{suffix}"


def _is_period_after(a: Tuple[int, int], b: Tuple[int, int], suffix: str) -> bool:
    if suffix == "YY":
        return a[0] > b[0]
    return (a[0], a[1]) > (b[0], b[1])


def _period_to_dts(
    kind: str, user_period: Dict[str, object], latest_code: str
) -> List[str]:
    """老 period → 新版 dts list. 含越界 clamp + start>latest fail-fast.

    新版后端能服务端过滤 dts list (字符串形态被 WAF 拒).
    右端超过 latest 会被 clamp 到 latest (避免拉到未发布的空期).
    start > latest / start > end 直接 fail-fast.
    """
    suffix = _KIND_TO_SUFFIX[kind]
    ey, es, _ = _parse_nbs_code(latest_code)
    pkind = user_period["kind"]

    # 离散 period 必须跟 kind 后缀一致 (例 月度 kind 不能用 '2012,2013' 年度逗号)
    _DISCRETE_REQUIRED_SUFFIX = {
        "DISCRETE_YEAR": "YY",
        "DISCRETE_MONTH": "MM",
        "DISCRETE_QUARTER": "SS",
    }
    if pkind in _DISCRETE_REQUIRED_SUFFIX:
        required = _DISCRETE_REQUIRED_SUFFIX[pkind]
        if required != suffix:
            kind_label = {"YY": "年度", "MM": "月度", "SS": "季度"}[required]
            raise ValueError(
                f"period 离散值是 {kind_label} 格式, 不匹配 kind={kind!r} (期望 {suffix})"
            )

    def _clamp_end(year: int, sub: int) -> Tuple[int, int]:
        if suffix == "YY":
            return (min(year, ey), 0)
        if _is_period_after((year, sub), (ey, es), suffix):
            return (ey, es)
        return (year, sub)

    def _check_start_le(year: int, sub: int):
        if suffix == "YY":
            if year > ey:
                raise ValueError(f"period 起点 {year} 晚于最新有数据期 {latest_code}")
            return
        if _is_period_after((year, sub), (ey, es), suffix):
            raise ValueError(f"period 起点 {year}-{sub} 晚于最新有数据期 {latest_code}")

    if pkind == "LATEST":
        n = int(user_period["n"])
        sy, ss = _shift_period(ey, es, suffix, n - 1)
        if suffix == "YY":
            return [f"{sy}YY-{ey}YY"]
        return [f"{_fmt_nbs_code(sy, ss, suffix)}-{_fmt_nbs_code(ey, es, suffix)}"]

    if pkind == "RANGE":
        sy = int(user_period["start"])
        eyy = int(user_period["end"])
        if sy > eyy:
            raise ValueError(f"period 起点 {sy} 晚于终点 {eyy}, 区间无效")
        if suffix == "YY":
            _check_start_le(sy, 0)
            ce_y, _ = _clamp_end(eyy, 0)
            return [f"{sy}YY-{ce_y}YY"]
        if suffix == "MM":
            _check_start_le(sy, 1)
            ce_y, ce_s = _clamp_end(eyy, 12)
            return [f"{sy}01MM-{_fmt_nbs_code(ce_y, ce_s, 'MM')}"]
        _check_start_le(sy, 1)
        ce_y, ce_s = _clamp_end(eyy, 4)
        return [f"{sy}01SS-{_fmt_nbs_code(ce_y, ce_s, 'SS')}"]

    if pkind == "OPEN_RANGE":
        sy = int(user_period["start"])
        if suffix == "YY":
            _check_start_le(sy, 0)
            return [f"{sy}YY-{ey}YY"]
        if suffix == "MM":
            _check_start_le(sy, 1)
            return [f"{sy}01MM-{_fmt_nbs_code(ey, es, 'MM')}"]
        _check_start_le(sy, 1)
        return [f"{sy}01SS-{_fmt_nbs_code(ey, es, 'SS')}"]

    if pkind == "SINGLE":
        y = int(user_period["year"])
        # 单年起点不能晚于 latest 起点; 当前年终点 clamp 到 latest 防生成未来 dts
        if y > ey:
            raise ValueError(
                f"period 单年 {y} 晚于最新有数据期 {latest_code}, 无可拉数据"
            )
        if suffix == "YY":
            return [f"{y}YY-{y}YY"]
        if suffix == "MM":
            ce_y, ce_s = _clamp_end(y, 12)
            return [f"{y}01MM-{_fmt_nbs_code(ce_y, ce_s, 'MM')}"]
        ce_y, ce_s = _clamp_end(y, 4)
        return [f"{y}01SS-{_fmt_nbs_code(ce_y, ce_s, 'SS')}"]

    if pkind == "DISCRETE_YEAR":
        codes = sorted(set(user_period["codes"]))
        # 离散值任何一个晚于 latest 都 fail-fast (而不是静默返未来空 dts)
        future = [y for y in codes if y > ey]
        if future:
            raise ValueError(
                f"period 离散年 {future} 晚于最新有数据期 {latest_code}, 无可拉数据"
            )
        return [f"{y}YY-{y}YY" for y in codes]

    if pkind == "DISCRETE_MONTH":
        codes = sorted(set(user_period["codes"]))
        future = [(y, m) for y, m in codes if _is_period_after((y, m), (ey, es), "MM")]
        if future:
            raise ValueError(
                f"period 离散月 {future} 晚于最新有数据期 {latest_code}, 无可拉数据"
            )
        return [
            f"{_fmt_nbs_code(y, m, 'MM')}-{_fmt_nbs_code(y, m, 'MM')}" for y, m in codes
        ]

    if pkind == "DISCRETE_QUARTER":
        codes = sorted(set(user_period["codes"]))
        future = [(y, q) for y, q in codes if _is_period_after((y, q), (ey, es), "SS")]
        if future:
            raise ValueError(
                f"period 离散季 {future} 晚于最新有数据期 {latest_code}, 无可拉数据"
            )
        return [
            f"{_fmt_nbs_code(y, q, 'SS')}-{_fmt_nbs_code(y, q, 'SS')}" for y, q in codes
        ]

    raise ValueError(f"未实现的 period kind: {pkind}")


def _validate_dts_within_slice(
    dts: List[str],
    leaf_slice: Optional[Tuple[Optional[int], Optional[int]]],
    leaf_name_for_error: Optional[str] = None,
) -> None:
    """校验 dts 全部端点都落在 leaf 切片年份范围内. 不覆盖时 fail-fast.

    PR1 不做跨切片 stitching, 否则会让 LAST_N 跨切片时静默返 NaN 列.
    leaf_slice=None 表示 leaf 无切片标记 (单切片 catalog), 不做限制.
    """
    if leaf_slice is None:
        return
    slc_start, slc_end = leaf_slice
    for span in dts:
        if "-" not in span:
            continue
        a, b = span.split("-", 1)
        sy, _, _ = _parse_nbs_code(a)
        ey, _, _ = _parse_nbs_code(b)
        if slc_start is not None and sy < slc_start:
            raise ValueError(
                f"period 起点年 {sy} 早于 leaf 切片起点 {slc_start}"
                f"{' (' + leaf_name_for_error + ')' if leaf_name_for_error else ''}; "
                f"PR1 不做跨切片拼接, 请在 path 末段切换到包含起点年的切片"
            )
        if slc_end is not None and ey > slc_end:
            raise ValueError(
                f"period 终点年 {ey} 晚于 leaf 切片终点 {slc_end}"
                f"{' (' + leaf_name_for_error + ')' if leaf_name_for_error else ''}; "
                f"PR1 不做跨切片拼接, 请切换到包含终点年的切片"
            )


def _expand_dts_to_codes(dts: List[str], suffix: str) -> List[str]:
    """从 dts list 算出期望 period code 列表 (升序)."""
    out = []
    for span in dts:
        if "-" not in span:
            continue
        a, b = span.split("-", 1)
        sy, ss, _ = _parse_nbs_code(a)
        ey, es, _ = _parse_nbs_code(b)
        if suffix == "YY":
            out.extend(f"{y}YY" for y in range(sy, ey + 1))
        else:
            units = 12 if suffix == "MM" else 4
            si = sy * units + (ss - 1)
            ei = ey * units + (es - 1)
            for idx in range(si, ei + 1):
                out.append(f"{idx // units:04d}{idx % units + 1:02d}{suffix}")
    return out


# ============ NBS Tree / Indicators / Da catalog (lazy lru_cache) ============


@lru_cache(maxsize=2048)
def _query_tree(pid: str, code: str) -> Tuple[Tuple[str, str, bool], ...]:
    """获取 catalog 树某层节点. 返回 immutable tuple of (name, _id, isLeaf)."""
    raw = _request_json(
        "GET",
        f"{NBS_BASE}/new/queryIndexTreeAsync",
        params={"pid": pid, "code": code},
    )
    nodes = raw.get("data") or []
    return tuple((n["_name"], n["_id"], n.get("isLeaf") is True) for n in nodes)


@lru_cache(maxsize=512)
def _query_indicators_cached(cid: str) -> Tuple[Tuple[Tuple[str, object], ...], ...]:
    """指标元信息列表. 用 frozen tuple of items 做哈希."""
    raw = _request_json(
        "GET",
        f"{NBS_BASE}/new/queryIndicatorsByCid",
        params={"cid": cid, "dt": "", "name": ""},
    )
    data = raw.get("data") or {}
    items = data.get("list") if isinstance(data, dict) else None
    items = items or []
    return tuple(tuple(it.items()) for it in items)


def _query_indicators(cid: str) -> List[Dict[str, str]]:
    return [dict(it) for it in _query_indicators_cached(cid)]


@lru_cache(maxsize=256)
def _resolve_da_catalog_cached(cid: str) -> Tuple[Tuple[str, str], ...]:
    """拿地区列表 (name_text, name_value), fail-fast 当地区列表为空.

    NBS 改版后某些 leaf 切片 (例 主要城市月度价格 (2026-)) 有 da_tree 但
    getDasByDaCatalogId 返 0 个地区, 必须 fail-fast 不能继续 Mode A/B/C.
    """
    cats = (
        _request_json(
            "GET",
            f"{NBS_BASE}/getDaCatalogTreeByIndicatorCid",
            params={"indicatorCid": cid},
        ).get("data")
        or []
    )
    if not cats:
        raise ValueError(f"catalog {cid} 无地区维度 (da_catalog 为空)")
    da_cat_id = cats[0].get("_id") or cats[0].get("publicrelease_web_dacatalog_id")
    raw = (
        _request_json(
            "GET",
            f"{NBS_BASE}/getDasByDaCatalogId",
            params={"daCid": da_cat_id},
        ).get("data")
        or []
    )
    if not raw:
        raise ValueError(
            f"catalog {cid} 地区列表为空, "
            f"该 catalog 没有可枚举地区, 请改用更早期的时间切片或检查 NBS 是否未发布"
        )
    return tuple((d["name_text"], d["name_value"]) for d in raw)


def _resolve_da_catalog(cid: str) -> List[Dict[str, str]]:
    return [{"text": t, "value": v} for t, v in _resolve_da_catalog_cached(cid)]


# ============ Path resolver ============


def _select_leaf_by_period(
    candidates: List[Tuple[str, str, bool]],
    user_period: Dict[str, object],
    path_for_error: str,
) -> str:
    """多 leaf 候选时按 period 选, 否则 fail-fast.

    绝不"取最新候选" (用户传 (2021-2025) 但拿到 (2026-) 是静默错数据).
    """
    if len(candidates) == 1:
        return candidates[0][1]

    parsed = [(name, _id, _parse_slice_range(name)) for name, _id, _leaf in candidates]
    pkind = user_period["kind"]

    def _slice_contains(slc, year):
        s, e = slc
        if s is not None and year < s:
            return False
        if e is not None and year > e:
            return False
        return True

    def _slice_covers_range(slc, start, end):
        s, e = slc
        if s is not None and start < s:
            return False
        if e is not None and end > e:
            return False
        return True

    def _fail(reason: str):
        raise ValueError(
            f"path {path_for_error!r} {reason}. 请在 path 末段写出明确的时间切片. "
            f"候选: " + " / ".join(n for n, _, _ in parsed)
        )

    if pkind == "LATEST":
        open_right = [(n, i) for n, i, slc in parsed if slc and slc[1] is None]
        if len(open_right) == 1:
            return open_right[0][1]
        _fail("多个候选切片, period 未指定具体范围无法唯一判断")

    if pkind == "SINGLE":
        year = int(user_period["year"])
        hits = [(n, i) for n, i, slc in parsed if slc and _slice_contains(slc, year)]
        if len(hits) == 1:
            return hits[0][1]
        _fail(f"单年 {year} 落在 {len(hits)} 个时间切片内")

    if pkind == "RANGE":
        s = int(user_period["start"])
        e = int(user_period["end"])
        hits = [
            (n, i) for n, i, slc in parsed if slc and _slice_covers_range(slc, s, e)
        ]
        if len(hits) == 1:
            return hits[0][1]
        _fail(f"区间 {s}-{e} 跨多个或无完全覆盖切片")

    if pkind == "OPEN_RANGE":
        s = int(user_period["start"])
        hits = [
            (n, i)
            for n, i, slc in parsed
            if slc and slc[1] is None and (slc[0] is None or slc[0] <= s)
        ]
        if len(hits) == 1:
            return hits[0][1]
        _fail(f"开放区间 {s}- 跨多个或无适配切片")

    if pkind in ("DISCRETE_YEAR", "DISCRETE_MONTH", "DISCRETE_QUARTER"):
        years = []
        for code in user_period["codes"]:
            years.append(code if isinstance(code, int) else code[0])
        ymin, ymax = min(years), max(years)
        hits = [
            (n, i)
            for n, i, slc in parsed
            if slc and _slice_covers_range(slc, ymin, ymax)
        ]
        if len(hits) == 1:
            return hits[0][1]
        _fail(f"离散值跨年范围 {ymin}-{ymax} 跨多个或无适配切片")

    raise ValueError(f"未实现 leaf 选择: {pkind}")


def _resolve_path(
    kind: str, path: str, user_period: Dict[str, object]
) -> Tuple[str, Optional[Tuple[Optional[int], Optional[int]]]]:
    """path 字符串 → (leaf cid, leaf 切片 (start_year, end_year)).

    切片为 None 表示 leaf name 没有时间区间标记 (例 `国内生产总值` 单切片 catalog).
    含 leaf period-aware fallback.
    """
    if kind not in _KIND_TO_CODE:
        raise ValueError(f"未知 kind: {kind!r}, 可选: {list(_KIND_TO_CODE.keys())}")
    code = _KIND_TO_CODE[kind]
    pid = _DATASETS[code]["root_id"]

    parts_raw = [p.strip() for p in path.split(">") if p.strip()]
    if not parts_raw:
        raise ValueError(f"path 为空: {path!r}")
    parts = [_normalize(p) for p in parts_raw]

    chosen_leaf_name: Optional[str] = None
    for i, part in enumerate(parts):
        is_last = i == len(parts) - 1
        nodes = _query_tree(pid, code)
        if not nodes:
            raise ValueError(
                f"path 第 {i + 1} 段 {parts_raw[i]!r} 下无子节点 (parent_id={pid})"
            )

        # 1) 精确匹配 (双方 normalize)
        exact = [(n, _id, leaf) for n, _id, leaf in nodes if _normalize(n) == part]
        if exact:
            if len(exact) > 1:
                raise ValueError(
                    f"path 第 {i + 1} 段 {parts_raw[i]!r} 精确匹配到多个同名节点: "
                    f"{[(n, _id) for n, _id, _ in exact]}"
                )
            chosen_name, chosen_id, chosen_leaf = exact[0]
            if is_last and not chosen_leaf:
                next_layer = _query_tree(chosen_id, code)
                raise ValueError(
                    f"path 末段 {parts_raw[i]!r} 命中 catalog (非 leaf), "
                    f"NBS 改版后该层级多了子层, 请加一段 path. "
                    f"可选: {[n for n, _, _ in next_layer][:15]}"
                )
            pid = chosen_id
            if is_last:
                chosen_leaf_name = chosen_name
            continue

        if not is_last:
            raise ValueError(
                f"path 第 {i + 1} 段 {parts_raw[i]!r} 找不到 (parent_id={pid}); "
                f"可选: {[n for n, _, _ in nodes][:10]}"
            )

        # 2) Leaf base-name fallback (仅 isLeaf=True 候选)
        base = _strip_period_tail(part)
        candidates = [
            (n, _id, leaf)
            for n, _id, leaf in nodes
            if _strip_period_tail(_normalize(n)) == base and leaf
        ]
        if not candidates:
            same_base_catalogs = [
                n
                for n, _, leaf in nodes
                if _strip_period_tail(_normalize(n)) == base and not leaf
            ]
            if same_base_catalogs:
                raise ValueError(
                    f"path leaf {parts_raw[i]!r} 同 base name 仅匹配到 catalog 不是 leaf, "
                    f"需要加一段 path. 匹配的 catalog: {same_base_catalogs}"
                )
            raise ValueError(
                f"path leaf {parts_raw[i]!r} 找不到; "
                f"可选: {[n for n, _, _ in nodes][:10]}"
            )

        pid = _select_leaf_by_period(candidates, user_period, path)
        chosen_leaf_name = next(n for n, _id, _ in candidates if _id == pid)

    leaf_slice = (
        _parse_slice_range(_normalize(chosen_leaf_name)) if chosen_leaf_name else None
    )
    return pid, leaf_slice


# ============ Indicator name → _id ============


def _indicator_candidate_labels(meta: Dict[str, str]) -> List[str]:
    """生成一个 indicator 的所有匹配候选 label, 用于多字段 normalize 比较."""
    out = []
    for k in ("i_showname", "_name", "ek_dp_name", "ek_name"):
        v = meta.get(k)
        if v:
            out.append(v)
    name = meta.get("_name", "")
    dp = meta.get("dp_name", "")
    du = meta.get("du_name", "")
    kj1 = meta.get("kj1_name", "")
    if name and du:
        out.append(f"{name}({du})")
        if dp:
            out.append(f"{name}_{dp}({du})")
    if name and kj1:
        out.append(f"{name}({kj1})")
        if dp and du:
            out.append(f"{name}({kj1})_{dp}({du})")
    return out


def _match_indicator(user_indicator: str, metas: List[Dict[str, str]]) -> str:
    """用户传的 indicator 名 → indicator _id. 二义性 fail-fast."""
    if not user_indicator:
        raise ValueError("indicator 名为空")
    target = _normalize(user_indicator)
    matched = []
    for m in metas:
        for cand in _indicator_candidate_labels(m):
            if _normalize(cand) == target:
                matched.append(m)
                break
    if not matched:
        choices = [m.get("i_showname") or m.get("_name") for m in metas]
        raise ValueError(
            f"indicator {user_indicator!r} 在 catalog 下无匹配, 可选: {choices}"
        )
    if len(matched) > 1:
        choices = [m.get("i_showname") or m.get("_name") for m in matched]
        raise ValueError(
            f"indicator {user_indicator!r} 匹配到多个候选 (normalize 二义性): {choices}"
        )
    return matched[0]["_id"]


def _legacy_indicator_label(meta: Dict[str, str]) -> str:
    """生成跟老版输出最接近的 row label.

    新版 i_showname '地区生产总值累计值 (亿元) ', 老版输出 '地区生产总值_累计值(亿元)'.
    我们去多余空格但**不强行加下划线** (NBS 字段无可靠还原).
    """
    showname = (meta.get("i_showname") or meta.get("_name") or "").strip()
    return re.sub(r"\s+", "", showname)


# ============ detect_latest_period ============


@lru_cache(maxsize=512)
def _detect_latest_cached(
    cid: str, ids_key: Tuple[str, ...], root_id: str, das_key: str
) -> Optional[str]:
    """daCatalogId 永远 ""; 各 dataset 默认期数不同; 倒序找第一个 non-empty."""
    payload = {
        "cid": cid,
        "indicatorIds": list(ids_key),
        "daCatalogId": "",
        "das": json.loads(das_key),
        "showType": "1",
        "dts": "",
        "rootId": root_id,
    }
    raw = _request_json(
        "POST",
        f"{NBS_BASE}/getEsDataByCidAndDt",
        json=payload,
        headers={"Content-Type": "application/json;charset=UTF-8"},
    )
    rows = raw.get("data") or []
    # 显式按 code 倒序排 (NBS 默认顺序未保证)
    try:
        rows = sorted(rows, key=lambda r: r.get("code") or "", reverse=True)
    except TypeError:
        pass
    for row in rows:
        for v in row.get("values") or []:
            if v.get("value") not in ("", None):
                return row.get("code")
    return None


def _detect_latest_period(
    cid: str, ids: List[str], root_id: str, das: Optional[List[Dict[str, str]]] = None
) -> Optional[str]:
    if das is None:
        das = [{"text": "全国", "value": "000000000000"}]
    return _detect_latest_cached(
        cid,
        tuple(sorted(ids)),
        root_id,
        json.dumps(das, sort_keys=True, ensure_ascii=False),
    )


# ============ Fetch data (daCatalogId="") ============


def _fetch_data(
    cid: str, ids: List[str], root_id: str, das: List[Dict[str, str]], dts: List[str]
) -> List[dict]:
    """所有 fetch 一律 daCatalogId="" (否则 NBS 忽略 das 走默认地区)."""
    payload = {
        "cid": cid,
        "indicatorIds": ids,
        "daCatalogId": "",
        "das": das,
        "showType": "1",
        "dts": dts,
        "rootId": root_id,
    }
    raw = _request_json(
        "POST",
        f"{NBS_BASE}/getEsDataByCidAndDt",
        json=payload,
        headers={"Content-Type": "application/json;charset=UTF-8"},
    )
    return raw.get("data") or []


def _row_first_value(row: dict) -> Optional[str]:
    """row.values[0].value, 防 IndexError."""
    vals = row.get("values") or []
    if not vals:
        return None
    return vals[0].get("value")


# ============ 公开函数 ============


def macro_china_nbs_nation(
    kind: Literal["月度数据", "季度数据", "年度数据"],
    path: str,
    period: str = "LAST10",
) -> pd.DataFrame:
    """
    国家统计局全国数据通用接口
    https://data.stats.gov.cn/dg/website/

    NBS 2026 改版后老 easyquery.htm 端点失效, 本接口直连新版 GUID API.
    对外签名与旧版兼容; path 解析支持 leaf 节点的多时间切片 fallback.

    :param kind: 数据类别, 月度/季度/年度
    :param path: 数据路径, 多层级用 ' > ' 连接, 例如 '价格指数 > 居民消费价格指数(上年同月=100)'
        NBS 改版后某些 catalog 多了一层 (例 CPI 多了"全国/城市/农村"维度);
        路径不到 leaf 时函数会 fail-fast 列出可选子项.
    :param period: 时间区间, 支持以下格式:
        - 'last10' / 'LAST10' (大小写均可)
        - 月度逗号离散: '201201,201205'
        - 季度逗号离散: '2012A,2012B,2012C,2012D' (A-D 表 Q1-Q4)
        - 年度逗号离散: '2012,2013'
        - 区间: '2018-2023'
        - 至今: '2013-'
        - 单年: '2018'
    :return: 国家统计局统计数据
    :rtype: pandas.DataFrame
    """
    if kind not in {"月度数据", "季度数据", "年度数据"}:
        raise ValueError(f"nation 接口 kind 必须是月度/季度/年度, 得到 {kind!r}")
    user_period = _parse_user_period(period)
    cid, leaf_slice = _resolve_path(kind, path, user_period)

    metas = _query_indicators(cid)
    if not metas:
        raise ValueError(f"catalog {cid} 无 indicators (path 可能未到 leaf)")
    ind_ids = [m["_id"] for m in metas]

    code = _KIND_TO_CODE[kind]
    root_id = _DATASETS[code]["root_id"]
    suffix = _KIND_TO_SUFFIX[kind]

    latest = _detect_latest_period(cid, ind_ids, root_id)
    if latest is None:
        raise ValueError("探测最新有数据期失败 (catalog 可能无数据)")
    dts = _period_to_dts(kind, user_period, latest)
    _validate_dts_within_slice(dts, leaf_slice)
    expected_codes = _expand_dts_to_codes(dts, suffix)

    rows = _fetch_data(
        cid,
        ind_ids,
        root_id,
        das=[{"text": "全国", "value": "000000000000"}],
        dts=dts,
    )
    code_to_name = {
        r["code"]: r["name"] for r in rows if r.get("code") and r.get("name")
    }

    row_labels = [_legacy_indicator_label(m) for m in metas]
    ind_id_to_label = {m["_id"]: _legacy_indicator_label(m) for m in metas}

    # 列降序 (老版示例最新在前)
    col_codes = sorted(expected_codes, reverse=True)
    col_labels = [code_to_name.get(c, c) for c in col_codes]

    data: Dict[str, Dict[str, object]] = {label: {} for label in row_labels}
    for row in rows:
        col = code_to_name.get(row.get("code"), row.get("code"))
        for v in row.get("values") or []:
            ind_id = v.get("_id")
            if ind_id in ind_id_to_label:
                val = v.get("value")
                data[ind_id_to_label[ind_id]][col] = (
                    val if val not in ("", None) else None
                )

    df = pd.DataFrame(
        [[data[r].get(c) for c in col_labels] for r in row_labels],
        index=row_labels,
        columns=col_labels,
    ).apply(pd.to_numeric, errors="coerce")
    df.index.name = None
    df.columns.name = None
    return df


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
    indicator: Union[str, None] = None,
    region: Union[str, None] = None,
    period: str = "LAST10",
) -> pd.DataFrame:
    """
    国家统计局地区数据通用接口
    https://data.stats.gov.cn/dg/website/

    支持三种模式:
    - region=None + indicator: 行=地区, 列=时期 (循环各地区串行 fetch)
    - region + indicator=None: 行=指标, 列=时期 (该地区下所有指标)
    - region + indicator: 行=单指标, 列=时期

    :param kind: 数据类别 (分省/主要城市/港澳台 × 月/季/年)
    :param path: 数据路径
    :param indicator: 指定指标 (region 给定时可为 None 拿全部)
    :param region: 指定地区 (indicator 给定时可为 None 拿所有地区)
    :param period: 时间区间, 格式同 nation 接口
    :return: 国家统计局地区数据
    :rtype: pandas.DataFrame
    """
    if indicator is None and region is None:
        raise ValueError("indicator 和 region 不能同时为 None")
    valid_kinds = {
        "分省月度数据",
        "分省季度数据",
        "分省年度数据",
        "主要城市月度价格",
        "主要城市年度数据",
        "港澳台月度数据",
        "港澳台年度数据",
    }
    if kind not in valid_kinds:
        raise ValueError(f"region 接口 kind 不在 {valid_kinds}, 得到 {kind!r}")

    user_period = _parse_user_period(period)
    cid, leaf_slice = _resolve_path(kind, path, user_period)

    metas = _query_indicators(cid)
    if not metas:
        raise ValueError(f"catalog {cid} 无 indicators (path 可能未到 leaf)")
    das_list = _resolve_da_catalog(cid)  # 空地区在此 fail-fast

    code = _KIND_TO_CODE[kind]
    root_id = _DATASETS[code]["root_id"]
    suffix = _KIND_TO_SUFFIX[kind]

    # ===== Mode A: region=None + indicator =====
    if region is None:
        ind_id = _match_indicator(indicator, metas)
        ind_meta = next(m for m in metas if m["_id"] == ind_id)
        ind_label = _legacy_indicator_label(ind_meta)

        latest = _detect_latest_period(cid, [ind_id], root_id, das=[das_list[0]])
        if latest is None:
            raise ValueError("探测最新期失败")
        dts = _period_to_dts(kind, user_period, latest)
        _validate_dts_within_slice(dts, leaf_slice)
        expected = _expand_dts_to_codes(dts, suffix)

        # 循环各地区串行 fetch (das 多地区不工作, 只能逐个调)
        per_region: Dict[str, Dict[str, object]] = {}
        col_name_map: Dict[str, str] = {}
        for da in das_list:
            rows = _fetch_data(cid, [ind_id], root_id, das=[da], dts=dts)
            for r in rows:
                if r.get("code") and r.get("name"):
                    col_name_map[r["code"]] = r["name"]
            per_region[da["text"]] = {
                r["code"]: (
                    _row_first_value(r)
                    if _row_first_value(r) not in ("", None)
                    else None
                )
                for r in rows
                if r.get("code")
            }

        col_codes = sorted(expected, reverse=True)
        col_labels = [col_name_map.get(c, c) for c in col_codes]
        row_labels = [d["text"] for d in das_list]

        df = pd.DataFrame(
            [[per_region[r].get(c) for c in col_codes] for r in row_labels],
            index=row_labels,
            columns=col_labels,
        ).apply(pd.to_numeric, errors="coerce")
        df = df.dropna(axis=1, how="all")
        df.index.name = None
        df.columns.name = ind_label
        return df

    # ===== Mode B/C: region != None =====
    target_das = [d for d in das_list if d["text"] == region]
    if not target_das:
        raise ValueError(
            f"region {region!r} 不在 das_list 中, "
            f"可选: {[d['text'] for d in das_list][:10]}..."
        )

    if indicator is None:
        # Mode B: 单地区 + 全部 indicator (单请求多 indicatorIds)
        ind_ids = [m["_id"] for m in metas]
        ind_labels = [_legacy_indicator_label(m) for m in metas]
        ind_id_to_label = {m["_id"]: _legacy_indicator_label(m) for m in metas}
        latest = _detect_latest_period(cid, ind_ids, root_id, das=target_das)
    else:
        # Mode C: 单地区 + 单 indicator
        ind_id = _match_indicator(indicator, metas)
        ind_ids = [ind_id]
        ind_meta = next(m for m in metas if m["_id"] == ind_id)
        ind_labels = [_legacy_indicator_label(ind_meta)]
        ind_id_to_label = {ind_id: ind_labels[0]}
        latest = _detect_latest_period(cid, ind_ids, root_id, das=target_das)

    if latest is None:
        raise ValueError(f"region={region} 探测最新期失败")
    dts = _period_to_dts(kind, user_period, latest)
    _validate_dts_within_slice(dts, leaf_slice)
    expected = _expand_dts_to_codes(dts, suffix)

    rows = _fetch_data(cid, ind_ids, root_id, das=target_das, dts=dts)
    code_to_name = {
        r["code"]: r["name"] for r in rows if r.get("code") and r.get("name")
    }

    data: Dict[str, Dict[str, object]] = {label: {} for label in ind_labels}
    for row in rows:
        for v in row.get("values") or []:
            ind_id_v = v.get("_id")
            if ind_id_v in ind_id_to_label:
                val = v.get("value")
                data[ind_id_to_label[ind_id_v]][row["code"]] = (
                    val if val not in ("", None) else None
                )

    col_codes = sorted(expected, reverse=True)
    col_labels = [code_to_name.get(c, c) for c in col_codes]

    df = pd.DataFrame(
        [[data[r].get(c) for c in col_codes] for r in ind_labels],
        index=ind_labels,
        columns=col_labels,
    ).apply(pd.to_numeric, errors="coerce")
    df.index.name = None
    df.columns.name = region
    return df


if __name__ == "__main__":
    macro_china_nbs_nation_df = macro_china_nbs_nation(
        kind="年度数据",
        path="国民经济核算 > 国内生产总值",
        period="LAST5",
    )
    print(macro_china_nbs_nation_df)

    macro_china_nbs_region_df = macro_china_nbs_region(
        kind="分省季度数据",
        path="国民经济核算 > 地区生产总值",
        indicator="地区生产总值累计值(亿元)",
        period="LAST3",
    )
    print(macro_china_nbs_region_df)

    macro_china_nbs_region_df = macro_china_nbs_region(
        kind="分省季度数据",
        path="国民经济核算 > 地区生产总值",
        period="last3",
        indicator=None,
        region="河北省",
    )
    print(macro_china_nbs_region_df)
