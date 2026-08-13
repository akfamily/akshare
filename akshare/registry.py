#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 接口检索层，提供接口发现与元数据查询能力
"""

import copy
import json
import re
from typing import Dict, List, Optional

import pandas as pd

from akshare.datasets import get_registry_json
from akshare.exceptions import DataParsingError, InvalidParameterError

_REGISTRY: Optional[Dict] = None

_TOKEN_SPLIT_RE = re.compile(r"[\s,，、;；/|]+")

WEIGHT_NAME_EXACT = 100.0
WEIGHT_NAME = 10.0
WEIGHT_DESC = 5.0
WEIGHT_CATEGORY = 3.0
WEIGHT_OUTPUT = 2.0
BONUS_ALL_TOKENS = 1.5
PENALTY_UNDOCUMENTED = 0.5


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


_WHITESPACE_RE = re.compile(r"\s+")


def _normalize(text: str) -> str:
    """
    压缩字符串内的全部空白，用于消除源文档里 latin/数字与中日韩字符之间
    人工插入的排版空格（如「A 股」）对子串匹配造成的干扰。

    :param text: 原始字符串
    :return: 空白压缩后的字符串
    """
    return _WHITESPACE_RE.sub("", text)


def _score(tokens: List[str], record: Dict) -> float:
    """
    对单条记录打分。

    :param tokens: 已切分的查询 token
    :param record: registry 中的一条接口记录
    :return: 匹配分，0 表示未命中
    """
    if not tokens:
        return 0.0
    name = record["name"]
    if len(tokens) == 1 and tokens[0] == name:
        return WEIGHT_NAME_EXACT
    desc = record.get("desc") or ""
    category = record.get("category") or ""
    # 用 "\x00" 而非空格拼接列名：归一化会压掉真正的空白分隔符，若仍用
    # 空格拼接，两个相邻列名会首尾相连产生跨列名的假匹配（例如列名
    # "市盈率" 与 "动态" 拼接后变成 "市盈率动态"，让查询词 "率动" 误命中）。
    # "\x00" 不会出现在真实列名里，归一化后依然保留分隔作用。
    columns = "\x00".join(
        column.get("name") or "" for column in record.get("outputs") or []
    )
    # 每条记录只归一化一次待搜索字段，避免在下方 token 循环里重复计算。
    norm_name = _normalize(name)
    norm_desc = _normalize(desc)
    norm_category = _normalize(category)
    norm_columns = _normalize(columns)
    total = 0.0
    hit_count = 0
    for token in tokens:
        norm_token = _normalize(token)
        subtotal = 0.0
        if norm_token in norm_name:
            subtotal += WEIGHT_NAME
        if norm_token in norm_desc:
            subtotal += WEIGHT_DESC
        if norm_token in norm_category:
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
        score = _score(tokens, record)
        if fallback_tokens:
            score = max(score, _score(fallback_tokens, record))
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
