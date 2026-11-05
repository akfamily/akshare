#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/5
Desc: 按位置赋列名的基线测试

`temp_df.columns = ["_", "日期", ...]` 按位置给列命名，上游一加字段就报
`Length mismatch`，是接口失效最常见的原因。应改为按上游字段名映射：
`temp_df.rename(columns={"REPORT_DATE": "日期", ...})`，再显式选列。

存量写法记录在 tests/positional_columns_baseline.json 中，只许减少、不许新增：
- 某个文件的处数超过基线（或新文件出现这种写法）时测试失败；
- 某个文件的处数低于基线时也会失败，提示更新基线，使基线随修复逐步收紧。

只统计赋值右侧是列表字面量的情况；`[item[1] for item in ...]` 这类从上游
返回结果推导列名的写法不计入。上游返回的是无字段名的二维数组时只能按位置命名，
这类写法保留在基线中即可。全程不联网。

更新基线：python tests/test_positional_columns.py --update
"""

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "positional_columns_baseline.json"


def _count(path: Path) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    n = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.List):
            continue
        for target in node.targets:
            if isinstance(target, ast.Attribute) and target.attr == "columns":
                n += 1
    return n


def _scan() -> dict[str, int]:
    counts = {}
    for path in sorted((ROOT / "akshare").rglob("*.py")):
        n = _count(path)
        if n:
            counts[path.relative_to(ROOT).as_posix()] = n
    return counts


def test_positional_columns_do_not_grow():
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    current = _scan()
    grown = {
        f: f"{baseline.get(f, 0)} -> {n}"
        for f, n in current.items()
        if n > baseline.get(f, 0)
    }
    assert not grown, (
        "以下文件新增了按位置赋列名的写法，请改用 rename(columns={上游字段: 中文列名})："
        f"{grown}"
    )


def test_positional_columns_baseline_is_tight():
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    current = _scan()
    shrunk = {
        f: f"{n} -> {current.get(f, 0)}"
        for f, n in baseline.items()
        if current.get(f, 0) < n
    }
    assert not shrunk, (
        "以下文件按位置赋列名的处数已减少，请运行 "
        f"python tests/test_positional_columns.py --update 更新基线：{shrunk}"
    )


if __name__ == "__main__":
    if "--update" in sys.argv:
        data = _scan()
        BASELINE.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        print(f"{len(data)} 个文件，共 {sum(data.values())} 处")
