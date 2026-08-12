#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 接口检索层，提供接口发现与元数据查询能力
"""

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
    columns = " ".join(
        column.get("name") or "" for column in record.get("outputs") or []
    )
    total = 0.0
    hit_count = 0
    for token in tokens:
        subtotal = 0.0
        if token in name:
            subtotal += WEIGHT_NAME
        if token in desc:
            subtotal += WEIGHT_DESC
        if token in category:
            subtotal += WEIGHT_CATEGORY
        if token in columns:
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
MIN_HITS_BEFORE_FALLBACK = 3


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
    对候选记录打分排序，命中不足时降级为 2-gram 重试。

    :param query: 查询字符串
    :param records: 候选记录
    :return: 含 _score 键并按分数降序的记录列表
    """
    tokens = _tokenize(query)
    scored = [(record, _score(tokens, record)) for record in records]
    hits = [item for item in scored if item[1] > 0]
    if len(hits) < MIN_HITS_BEFORE_FALLBACK:
        fallback_tokens = _bigrams(query)
        if fallback_tokens:
            scored = [(record, _score(fallback_tokens, record)) for record in records]
            hits = [item for item in scored if item[1] > 0]
    hits.sort(key=lambda item: (-item[1], item[0]["name"]))
    return [dict(record, _score=score) for record, score in hits]


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
    """
    records = _load()["interfaces"]
    if category:
        records = [item for item in records if item["category"] == category]
    if documented_only:
        records = [item for item in records if item["documented"]]
    if not query.strip():
        ranked = [dict(item, _score=0.0) for item in records]
    else:
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
            return {key: value for key, value in record.items()}
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
