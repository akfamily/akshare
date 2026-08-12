#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 接口检索层，提供接口发现与元数据查询能力
"""

import json
import re
from typing import Dict, List, Optional

from akshare.datasets import get_registry_json
from akshare.exceptions import DataParsingError

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
