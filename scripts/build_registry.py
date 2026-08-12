#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 构建期脚本，解析 docs/data 与 akshare/__init__.py 生成接口元数据
"""

import pathlib
import re
from typing import Dict, List, Optional


def parse_table(segment: str, header: str) -> List[Dict[str, Optional[str]]]:
    """
    提取指定标题下紧邻的一张 Markdown 表格。

    表格边界规则：标题行之后跳过空行，随后连续收集以 "|" 开头的行，
    遇到第一个非 "|" 开头的行（含空行）立即终止。文档中相邻表格之间
    必有空行或文本行分隔，因此该规则可避免跨表抓取。

    :param segment: 单个接口条目的文本片段
    :param header: 表格上方的标题，如 "输入参数"
    :return: 每行一个 dict，含 name/type/desc 三个键
    """
    match = re.search(rf"^{re.escape(header)}\s*$", segment, re.M)
    if not match:
        return []
    lines = segment[match.end() :].split("\n")
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    raw_rows = []
    while index < len(lines) and lines[index].startswith("|"):
        raw_rows.append(lines[index])
        index += 1
    # 前两行分别是表头与分隔行，数据行从第三行开始
    result = []
    for row in raw_rows[2:]:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        # 实测数据行以 3 列为主，另有极少数 2 列或 4 列，统一取前 3 列并补齐
        cells = (cells + [None, None, None])[:3]
        if not cells[0]:
            continue
        result.append({"name": cells[0], "type": cells[1], "desc": cells[2]})
    return result


BLOCK_RE = re.compile(r"^接口:\s*(\S+)\s*$", re.M)
EXAMPLE_RE = re.compile(r"```python\n(.*?)```", re.S)


def _field(segment: str, key: str) -> Optional[str]:
    """抽取 "键: 值" 形式的单行字段。"""
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", segment, re.M)
    return match.group(1) if match else None


def parse_segment(segment: str) -> Dict:
    """
    解析单个接口条目的正文。

    :param segment: 从 "接口: xxx" 之后到下一个接口条目之前的文本
    :return: 接口元数据 dict
    """
    example_match = EXAMPLE_RE.search(segment)
    return {
        "desc": _field(segment, "描述"),
        "url": _field(segment, "目标地址"),
        "limit_desc": _field(segment, "限量"),
        "params": parse_table(segment, "输入参数"),
        "outputs": parse_table(segment, "输出参数"),
        "example": example_match.group(1).strip() if example_match else None,
    }


def collect_doc_records(docs_dir: pathlib.Path) -> Dict[str, Dict]:
    """
    遍历 docs/data 下所有 Markdown，收集接口条目。

    同名条目以首次出现者为准。

    :param docs_dir: docs/data 目录
    :return: 接口名 -> 元数据
    """
    records: Dict[str, Dict] = {}
    for path in sorted(docs_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = list(BLOCK_RE.finditer(text))
        for position, match in enumerate(hits):
            end = hits[position + 1].start() if position + 1 < len(hits) else len(text)
            name = match.group(1)
            if name in records:
                continue
            record = parse_segment(text[match.end() : end])
            record["category"] = path.parent.name
            records[name] = record
    return records
