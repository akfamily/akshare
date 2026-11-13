#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/27
Desc: 接口检索层，提供接口发现与元数据查询能力
"""

import copy
import json
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

from akshare.datasets import get_registry_json
from akshare.exceptions import DataParsingError, InvalidParameterError
from akshare.utils.params import to_bool, to_int

_REGISTRY: Optional[Dict] = None

_TOKEN_SPLIT_RE = re.compile(r"[\s,，、;；/|]+")

WEIGHT_NAME_EXACT = 100.0
WEIGHT_NAME = 10.0
WEIGHT_DESC = 5.0
WEIGHT_CATEGORY = 3.0
WEIGHT_OUTPUT = 2.0
BONUS_ALL_TOKENS = 1.5
PENALTY_UNDOCUMENTED = 0.5

# 同义词组：查询词命中组内任意一个词时，按整组去匹配。接口描述沿用数据源网站的
# 栏目名，与用户的说法常常对不上——描述里写的是「日频率」「历史行情」，用户搜的是
# 「日线」；只做字面匹配时，「期货 日线」的前几名里没有一个是日线行情。
# 组内的英文词是接口名中以下划线分隔的片段，按整段匹配：us 只命中 stock_us_daily
# 这样的名字，不会命中 industry。含下划线的词（如 fund_flow）要求各段连续出现。
SYNONYM_GROUPS: Tuple[Tuple[str, ...], ...] = (
    ("日线", "日k", "日k线", "日频", "历史行情", "daily", "hist"),
    ("分时", "分钟", "分钟线", "minute", "min"),
    ("实时", "实时行情", "行情快照", "spot", "realtime"),
    ("a股", "沪深京a股", "沪深a股", "zh_a"),
    ("港股", "hk"),
    ("美股", "us"),
    ("股票", "个股", "stock"),
    ("指数", "index"),
    ("基金", "fund"),
    ("etf", "交易型开放式指数基金"),
    ("期货", "futures"),
    ("期权", "option"),
    ("债券", "bond"),
    ("可转债", "转债", "cov", "cb"),
    ("外汇", "汇率", "forex", "fx", "currency"),
    ("宏观", "macro"),
    ("资金流", "资金流向", "fund_flow"),
    ("龙虎榜", "lhb"),
    ("北向资金", "北向", "沪深港通", "hsgt"),
    ("财务报表", "财报", "资产负债表", "利润表", "现金流量表"),
    ("交易日历", "交易日", "trade_date"),
    ("行业板块", "board_industry"),
    ("概念板块", "board_concept"),
    ("涨停", "涨停板", "zt_pool"),
    ("分红", "派息", "分红派息", "dividend", "fh", "fhps", "fhpx"),
)

_ASCII_WORD_RE = re.compile(r"[a-z0-9_]+")


def _build_synonym_index() -> Dict[str, Tuple[str, ...]]:
    index: Dict[str, Tuple[str, ...]] = {}
    for group in SYNONYM_GROUPS:
        for word in group:
            index[word] = group
    return index


_SYNONYM_INDEX = _build_synonym_index()


def _synonyms(norm_token: str) -> Tuple[str, ...]:
    """
    返回查询词所在同义词组中的其余词，不区分大小写；不在任何组内时返回空元组。

    :param norm_token: 已压缩空白的查询词
    :return: 同组的其他词
    """
    key = norm_token.lower()
    group = _SYNONYM_INDEX.get(key, ())
    return tuple(word for word in group if word != key)


def _name_has_segments(name_segments: List[str], word: str) -> bool:
    """
    判断接口名中是否连续出现给定的片段，如 zh_a 命中 stock_zh_a_hist，
    但不命中 stock_zh_ah_spot。

    :param name_segments: 接口名按下划线切分后的片段
    :param word: 英文同义词，可含下划线
    :return: 是否命中
    """
    parts = word.split("_")
    size = len(parts)
    return any(
        name_segments[start : start + size] == parts
        for start in range(len(name_segments) - size + 1)
    )


def _load() -> Dict:
    """
    懒加载 registry 数据。import akshare 时不触发，仅首次检索时读取。

    :return: registry 数据
    :rtype: dict
    """
    global _REGISTRY
    if _REGISTRY is None:
        try:
            path = get_registry_json()
            _REGISTRY = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise DataParsingError(
                f"接口元数据加载失败，请重装 akshare 或运行 "
                f"python scripts/build_registry.py 重新生成: {e}"
            )
    return _REGISTRY


def _tokenize(query: str) -> List[str]:
    """
    按空白与常见标点切分查询词。

    :param query: 查询字符串
    :return: token 列表
    """
    return [token for token in _TOKEN_SPLIT_RE.split(query.strip()) if token]


def _normalize(text: str) -> str:
    """
    压缩字符串内的全部空白，用于消除源文档里 latin/数字与中日韩字符之间
    人工插入的排版空格（如「A 股」）对子串匹配造成的干扰。

    :param text: 原始字符串
    :return: 空白压缩后的字符串
    """
    # str.split() 认定的空白与正则 \s 完全一致，但对短字符串快得多；
    # 检索时每条记录、每个 token 都要调用这里。
    return "".join(text.split())


def _prepare(record: Dict) -> Tuple[str, str, str, str]:
    """
    归一化单条记录的待搜索字段。

    :param record: registry 中的一条接口记录
    :return: 归一化后的（接口名，描述，类目，输出列名）
    """
    # 用 "\x00" 而非空格拼接列名：归一化会压掉真正的空白分隔符，若仍用
    # 空格拼接，两个相邻列名会首尾相连产生跨列名的假匹配（例如列名
    # "市盈率" 与 "动态" 拼接后变成 "市盈率动态"，让查询词 "率动" 误命中）。
    # "\x00" 不会出现在真实列名里，归一化后依然保留分隔作用。
    columns = "\x00".join(
        column.get("name") or "" for column in record.get("outputs") or []
    )
    return (
        _normalize(record["name"]),
        _normalize(record.get("desc") or ""),
        _normalize(record.get("category") or ""),
        _normalize(columns),
    )


def _score(
    tokens: List[str],
    record: Dict,
    fields: Optional[Tuple[str, str, str, str]] = None,
) -> float:
    """
    对单条记录打分。

    :param tokens: 已切分的查询 token
    :param record: registry 中的一条接口记录
    :param fields: _prepare 的结果；为 None 时现场计算，传入可在多轮打分间复用
    :return: 匹配分，0 表示未命中
    """
    if not tokens:
        return 0.0
    if len(tokens) == 1 and tokens[0] == record["name"]:
        return WEIGHT_NAME_EXACT
    if fields is None:
        fields = _prepare(record)
    norm_name, norm_desc, norm_category, norm_columns = fields
    name_segments = norm_name.split("_")
    lower_desc = norm_desc.lower()
    total = 0.0
    hit_count = 0
    for token in tokens:
        norm_token = _normalize(token)
        # 同义词只用于接口名、描述与类目；输出列名是数据字段，不是对接口的描述，
        # 用同义词去匹配会把含「日线」类列名的无关接口带进来
        # 接口名全是小写，描述里的英文多为大写（ETF、LOF），比较时不区分大小写
        lower_token = norm_token.lower()
        in_name = lower_token in norm_name
        in_desc = lower_token in lower_desc
        in_category = norm_token in norm_category
        for word in _synonyms(norm_token):
            if _ASCII_WORD_RE.fullmatch(word):
                in_name = in_name or _name_has_segments(name_segments, word)
                in_category = in_category or word == norm_category
            else:
                in_desc = in_desc or word in lower_desc
        subtotal = 0.0
        if in_name:
            subtotal += WEIGHT_NAME
        if in_desc:
            subtotal += WEIGHT_DESC
        if in_category:
            subtotal += WEIGHT_CATEGORY
        if norm_token in norm_columns:
            subtotal += WEIGHT_OUTPUT
        if subtotal:
            hit_count += 1
        total += subtotal
    if total and hit_count == len(tokens):
        total *= BONUS_ALL_TOKENS
    if not record.get("documented", False):
        total *= PENALTY_UNDOCUMENTED
    return total


SEARCH_COLUMNS = ["接口名", "类目", "描述", "有无文档", "匹配分"]


def _bigrams(query: str) -> List[str]:
    """
    把查询压成连续字符 2-gram，用于用户未打空格时的降级召回。

    :param query: 查询字符串
    :return: 2-gram 列表
    """
    compact = re.sub(r"\s+", "", query)
    return [compact[i : i + 2] for i in range(len(compact) - 1)]


def _rank(query: str, records: List[Dict]) -> List[Dict]:
    """
    对候选记录打分排序。

    每条记录取「按空白/标点切分的主分」与「连续字符 2-gram 的降级分」两者中
    的较大值，作为召回与常规排序依据。但排序优先级不完全依赖分数大小：
    接口名与查询原文完全相等的记录一律置顶，不论其分数是否被 2-gram 降级
    分反超——因为 2-gram 分是按字符子串累加的，接口名越长该分数越容易超过
    精确命中的加成分，单纯比较数值大小无法保证精确匹配永远排第一。其余
    记录按分数降序，同分再按接口名字典序排列。

    :param query: 查询字符串
    :param records: 候选记录
    :return: 含 _score 键并按「精确名置顶、分数降序、名字典序」排列的记录列表
    """
    tokens = _tokenize(query)
    fallback_tokens = _bigrams(query)
    stripped = query.strip()
    scored = []
    for record in records:
        # 主分与降级分共用同一份归一化字段，每条记录只归一化一次。
        fields = _prepare(record)
        score = _score(tokens, record, fields)
        if fallback_tokens:
            score = max(score, _score(fallback_tokens, record, fields))
        if score > 0:
            # 与 _score 的精确名捷径判定保持一致：tokenize 会剥掉
            # ",，、;；/|" 等标点，若这里仍用未剥标点的原始 stripped 比较，
            # 带尾随标点的精确名查询（如 "stock_zh_a_hist,"）会被判定为
            # 非精确，从而失去置顶保证。
            is_exact = (len(tokens) == 1 and tokens[0] == record["name"]) or (
                record["name"] == stripped
            )
            scored.append((record, score, is_exact))
    scored.sort(key=lambda item: (not item[2], -item[1], item[0]["name"]))
    return [dict(record, _score=score) for record, score, _ in scored]


def search(
    query: str,
    limit: int = 20,
    category: Optional[str] = None,
    documented_only: bool = False,
) -> pd.DataFrame:
    """
    按自然语言检索 AKShare 接口。

    :param query: 查询词，如 "A股 历史行情"
    :param limit: 返回条数上限
    :param category: 限定类目，如 "stock"
    :param documented_only: 仅返回有文档的接口
    :return: 检索结果
    :rtype: pandas.DataFrame
    :raises InvalidParameterError: 当 limit 为负数时
    """
    limit = to_int(limit, "limit")
    documented_only = to_bool(documented_only, "documented_only")
    if limit < 0:
        raise InvalidParameterError(f"limit 不能为负数，收到 {limit}")
    if not query.strip():
        return pd.DataFrame(columns=SEARCH_COLUMNS)
    records = _load()["interfaces"]
    if category:
        records = [item for item in records if item["category"] == category]
    if documented_only:
        records = [item for item in records if item["documented"]]
    ranked = _rank(query, records)
    rows = [
        {
            "接口名": item["name"],
            "类目": item["category"],
            "描述": item["desc"],
            "有无文档": item["documented"],
            "匹配分": round(item["_score"], 2),
        }
        for item in ranked[:limit]
    ]
    return pd.DataFrame(rows, columns=SEARCH_COLUMNS)


def interface_info(name: str) -> Dict:
    """
    返回单个接口的完整元数据。

    :param name: 接口名，如 "stock_zh_a_hist"
    :return: 完整元数据
    :rtype: dict
    """
    records = _load()["interfaces"]
    for record in records:
        if record["name"] == name:
            return copy.deepcopy(record)
    candidates = [item["name"] for item in _rank(name, records)[:3]]
    hint = "、".join(candidates) if candidates else "无"
    raise InvalidParameterError(f"未知接口 {name}，最接近的候选: {hint}")


def list_categories() -> pd.DataFrame:
    """
    列出全部类目及其接口数量。

    :return: 类目统计
    :rtype: pandas.DataFrame
    """
    counter: Dict[str, int] = {}
    for record in _load()["interfaces"]:
        counter[record["category"]] = counter.get(record["category"], 0) + 1
    rows = [{"类目": key, "接口数": counter[key]} for key in sorted(counter)]
    return pd.DataFrame(rows, columns=["类目", "接口数"])
