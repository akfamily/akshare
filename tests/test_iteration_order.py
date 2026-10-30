#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 禁止遍历 set 产生结果顺序的测试

Python 对字符串的哈希每个进程随机，遍历 set(...) 的顺序因此每次运行都不同：
get_shfe_rank_table 返回的字典、get_rank_sum 返回的行，同一份上游数据每次顺序都不一样，
结果无法复现。去重请用 dict.fromkeys(...)，它保留首次出现的顺序。全程不联网。
"""

import ast
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _is_set(node: ast.AST) -> bool:
    if isinstance(node, (ast.Set, ast.SetComp)):
        return True
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in ("set", "frozenset")
    )


def test_no_iteration_over_set():
    offenders = []
    for path in sorted((ROOT / "akshare").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            target = None
            if isinstance(node, (ast.For, ast.comprehension)):
                target = node.iter
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in ("list", "tuple", "enumerate")
                and node.args
            ):
                target = node.args[0]
            if target is not None and _is_set(target):
                offenders.append(f"{path.relative_to(ROOT).as_posix()}:{target.lineno}")
    assert not offenders, (
        f"以下位置遍历了 set，顺序每次运行都不同，请改用 dict.fromkeys：{offenders}"
    )


def test_dict_fromkeys_keeps_first_seen_order():
    assert list(dict.fromkeys(["cu2612", "cu2611", "cu2612", "al2701"])) == [
        "cu2612",
        "cu2611",
        "al2701",
    ]
