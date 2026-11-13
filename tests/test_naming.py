#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/13
Desc: 接口命名的基线测试

接口名是对外契约，用词要与金融含义一致，规则见 docs/contributing.md 的“接口命名规范”。
这里只检查能机械判断的三条：

- prefix：接口名以所属类目开头，如 index 类目的接口以 `index_` 开头；
- token：不使用已确认有歧义或用错的词，见 FORBIDDEN_TOKENS；
- source_position：数据源、交易所标记放在末尾，如 `futures_daily_dce`。
  名称已以数据源结尾时，中间的交易所标记视为市场限定词，
  如 `option_sse_daily_sina`，不算违规。

“用词是否符合金融含义”无法机械判断（如 spot 在期货类目只表示现货），仍需人工审查。

存量问题记录在 tests/naming_baseline.json 中，只许减少、不许新增：
- 新接口违反规则，或老接口新增一种违规时，测试失败；
- 基线中的接口已改名或已合规时也会失败，提示更新基线，使基线随改名逐步收紧。

数据来自 akshare/data/interfaces.json，全程不联网。

更新基线：python tests/test_naming.py --update
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "akshare" / "data" / "interfaces.json"
BASELINE = Path(__file__).resolve().parent / "naming_baseline.json"

# 数据源与交易所标记，应放在接口名末尾
SOURCES = frozenset(
    "em sina ths xq cninfo jsl tx lg baidu js sw futu cls eniu csindex cni".split()
)
EXCHANGES = frozenset("sse szse bse dce czce shfe cffex gfex ine sge sgx hkex".split())

# 类目 -> {禁用词：应改用的写法}；"*" 表示所有类目
FORBIDDEN_TOKENS = {
    "*": {
        "get": "数据接口不以动词开头",
        "comm": "手续费用 fee，商品用 commodity",
        "forex": "外汇统一用 fx",
    },
    "bond": {"cov": "可转债用 cb"},
    "macro": {
        "yearly": "年率（同比）用 yoy",
        "monthly": "月率（环比）用 mom",
        "quarterly": "季率用 qoq",
    },
}


def _violations(name: str, category: str) -> list[str]:
    found = []
    tokens = name.split("_")
    if not re.fullmatch(r"[a-z][a-z0-9]*(_[a-z0-9]+)*", name):
        found.append("snake_case")
    if name != category and not name.startswith(category + "_"):
        found.append("prefix")
    banned = FORBIDDEN_TOKENS["*"] | FORBIDDEN_TOKENS.get(category, {})
    if any(token in banned for token in tokens):
        found.append("token")
    middle = set(tokens[1:-1])
    if middle & SOURCES or (middle & EXCHANGES and tokens[-1] not in SOURCES):
        found.append("source_position")
    return found


def _scan() -> dict[str, list[str]]:
    interfaces = json.loads(REGISTRY.read_text(encoding="utf-8"))["interfaces"]
    result = {}
    for item in interfaces:
        found = _violations(item["name"], item["category"])
        if found:
            result[item["name"]] = found
    return dict(sorted(result.items()))


def test_violation_rules():
    assert _violations("index_zh_hist_em", "index") == []
    assert _violations("stock_zh_index_daily_em", "index") == ["prefix"]
    assert _violations("bond_zh_cov", "bond") == ["token"]
    assert _violations("macro_uk_cpi_yearly", "macro") == ["token"]
    assert _violations("movie_boxoffice_yearly", "alternative") == ["prefix"]
    assert _violations("futures_dce_position_rank", "futures") == ["source_position"]
    assert _violations("futures_daily_dce", "futures") == []
    assert _violations("option_sse_daily_sina", "option") == []
    assert _violations("crypto_js_spot", "crypto") == ["source_position"]
    assert _violations("stock_ZhA", "stock") == ["snake_case"]


def test_naming_violations_do_not_grow():
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    grown = {
        name: sorted(set(found) - set(baseline.get(name, [])))
        for name, found in _scan().items()
        if set(found) - set(baseline.get(name, []))
    }
    assert not grown, (
        f"以下接口名不符合 docs/contributing.md 的“接口命名规范”，请改名：{grown}"
    )


def test_naming_baseline_is_tight():
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    current = _scan()
    stale = {
        name: sorted(set(found) - set(current.get(name, [])))
        for name, found in baseline.items()
        if set(found) - set(current.get(name, []))
    }
    assert not stale, (
        "以下接口已改名或已合规，请运行 "
        f"python tests/test_naming.py --update 更新基线：{stale}"
    )


if __name__ == "__main__":
    if "--update" in sys.argv:
        scanned = _scan()
        BASELINE.write_text(
            json.dumps(scanned, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"基线已更新：{len(scanned)} 个接口")
    else:
        print(json.dumps(_scan(), ensure_ascii=False, indent=2))
