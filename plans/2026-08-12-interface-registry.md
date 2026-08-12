# 接口检索层 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 AKShare 增加离线可用的接口检索能力，使 agent 能从自然语言定位到可调用接口，并建立 CI 门禁阻止文档与代码继续漂移。

**Architecture:** 构建期脚本解析 `docs/data/**/*.md` 与 `akshare/__init__.py`，交叉合并后生成确定性的 `akshare/data/interfaces.json` 并提交进 git；运行期 `akshare/registry.py` 懒加载该 JSON，用零依赖关键词打分提供 `ak.search()` / `ak.interface_info()` / `ak.list_categories()`。两侧仅通过 JSON Schema 通信，互不感知对方实现。

**Tech Stack:** Python 3.9+、pandas、pytest。构建期仅用标准库（`re` / `ast` / `json` / `pathlib` / `argparse`）。

设计依据：`specs/2026-08-12-interface-registry-design.md`

## Global Constraints

- **不引入任何第三方依赖。** 构建期脚本仅用标准库；运行期仅用已有的 `pandas`。
- **Python 下限 3.9。** 禁止 `match` 语句、禁止 `X | Y` 运行时注解（用 `typing.Optional` / `typing.List`）。`list[dict]` 这类 PEP 585 注解在 3.9 可用。
- **不修改任何现有数据接口的函数签名或运行时行为。** 本计划只新增文件，对 `akshare/__init__.py`、`akshare/datasets.py`、CI workflow 只做追加式修改。
- **Ruff 强制：** 88 字符行宽、双引号、4 空格缩进。提交前对**本任务改动的文件**跑 `ruff format <文件>` 与 `ruff check <文件> --fix`。**禁止跑全量 `ruff format .`**——当前 ruff 会格式化 Markdown 里的 Python 代码块，全量执行会改动 11 个与本次无关的 md 文件和 1 个存量 py 文件（`akshare/stock_feature/stock_margin_bse.py`），污染提交。注意 `akshare/__init__.py` 被 Ruff 排除，其余新文件不排除。
- **提交信息遵循 Conventional Commits**（`conventional-pre-commit` 在 `commit-msg` 钩子强制）。仓库惯例为英文 type/scope + 中文主题。
- **测试全程禁止联网。** 本计划所有测试均为纯本地，不得发起 HTTP 请求。
- **产物确定性三要素：** 按 `name` 字典序排序、`json.dumps(..., ensure_ascii=False, separators=(",", ":"), sort_keys=True)`、文件末尾单个换行。产物中禁止出现时间戳与版本号。

## File Structure

| 文件 | 职责 | 状态 |
|---|---|---|
| `scripts/build_registry.py` | 解析文档与导出表、合并、序列化、`--check` 校验 | 新建，约 250 行 |
| `scripts/registry_baseline.json` | 存量漂移豁免清单 | 新建（由 Task 5 生成） |
| `akshare/registry.py` | 懒加载、打分、三个公开 API、异常 | 新建，约 180 行 |
| `akshare/data/interfaces.json` | 数据契约产物，提交进 git | 新建（由 Task 4 生成，约 1.19 MB） |
| `akshare/datasets.py` | 追加 `get_registry_json()` | 修改 |
| `akshare/__init__.py` | 追加三个 API 的导出与版本记录行 | 修改 |
| `tests/conftest.py` | 将 `scripts/` 加入 `sys.path` 供测试导入 | 新建 |
| `tests/test_build_registry.py` | 构建期解析器单元测试 | 新建 |
| `tests/test_registry.py` | 运行期检索器单元测试（用假数据 fixture） | 新建 |
| `tests/test_registry_integration.py` | 不变量集成测试（用真实产物） | 新建 |
| `.github/workflows/main_dev_check.yml` | 追加独立的 registry-check job | 修改 |

测试拆成两个文件：构建期与运行期是解耦的两个组件，分开测才能各自独立演进。这是对 spec 交付物清单中单一 `tests/test_registry.py` 的细化。

---

### Task 1: 表格解析器

Markdown 参数表的提取。这是整个解析器最容易出错的地方——原型实现用「标题后固定字符数内的所有表格行」为界，会跨表抓取相邻的无关表格。必须先写出复现该缺陷的测试。

**Files:**
- Create: `scripts/build_registry.py`
- Create: `tests/conftest.py`
- Test: `tests/test_build_registry.py`

**Interfaces:**
- Consumes: 无
- Produces: `parse_table(segment: str, header: str) -> List[Dict[str, Optional[str]]]`，返回形如 `[{"name": "symbol", "type": "str", "desc": "..."}]` 的列表；表头不存在时返回 `[]`

- [ ] **Step 1: 创建 conftest 让测试能导入 scripts/**

`scripts/` 不是 Python 包，pytest 默认无法导入其中模块。

创建 `tests/conftest.py`：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
```

- [ ] **Step 2: 写失败的测试**

创建 `tests/test_build_registry.py`。第二个测试是跨表污染的回归用例，样本取自真实文档 `article_oman_rv`：输入参数表之后隔一个空行紧跟一张 4 列的无关数据表。

```python
from build_registry import parse_table

SIMPLE = """
输入参数

| 名称     | 类型  | 描述           |
|--------|-----|--------------|
| symbol | str | symbol="FTSE" |
| index  | str | index="rk_th2" |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
"""

CONTAMINATED = """
输入参数

| 名称     | 类型  | 描述           |
|--------|-----|--------------|
| symbol | str | symbol="FTSE" |

实现波动率指数一览表

| Symbol | Name      | Earliest Available | Latest Available |
|--------|-----------|--------------------|------------------|
| .AEX   | AEX index | January 03, 2000   | June 01, 2024    |
| .AORD  | All Ords  | January 04, 2000   | June 01, 2024    |
"""


def test_parse_table_reads_rows():
    rows = parse_table(SIMPLE, "输入参数")
    assert rows == [
        {"name": "symbol", "type": "str", "desc": 'symbol="FTSE"'},
        {"name": "index", "type": "str", "desc": 'index="rk_th2"'},
    ]


def test_parse_table_picks_correct_header():
    rows = parse_table(SIMPLE, "输出参数")
    assert rows == [{"name": "日期", "type": "object", "desc": "-"}]


def test_parse_table_stops_at_blank_line_not_next_table():
    """回归：不得把后续无关表格的行吸进输入参数。"""
    rows = parse_table(CONTAMINATED, "输入参数")
    assert len(rows) == 1
    assert rows[0]["name"] == "symbol"


def test_parse_table_missing_header_returns_empty():
    assert parse_table(SIMPLE, "不存在的标题") == []
```

- [ ] **Step 3: 运行测试确认失败**

Run: `pytest tests/test_build_registry.py -v`
Expected: FAIL，`ModuleNotFoundError: No module named 'build_registry'`

- [ ] **Step 4: 实现 parse_table**

创建 `scripts/build_registry.py`：

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 构建期脚本，解析 docs/data 与 akshare/__init__.py 生成接口元数据
"""

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
    lines = segment[match.end():].split("\n")
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
```

- [ ] **Step 5: 运行测试确认通过**

Run: `pytest tests/test_build_registry.py -v`
Expected: 4 passed

- [ ] **Step 6: 格式化并提交**

```bash
ruff format scripts/build_registry.py tests/
ruff check scripts/build_registry.py tests/ --fix
git add scripts/build_registry.py tests/conftest.py tests/test_build_registry.py
git commit -m "feat(registry): 新增文档表格解析器"
```

---

### Task 2: 接口条目解析

把 `docs/data/**/*.md` 切成一个个接口条目并抽取字段。

**Files:**
- Modify: `scripts/build_registry.py`
- Test: `tests/test_build_registry.py`

**Interfaces:**
- Consumes: `parse_table(segment, header)`（Task 1）
- Produces:
  - `parse_segment(segment: str) -> Dict`，返回含 `desc` / `url` / `limit_desc` / `params` / `outputs` / `example` 六个键的 dict
  - `collect_doc_records(docs_dir: Path) -> Dict[str, Dict]`，键为接口名，值在 `parse_segment` 结果上追加 `category`（取自所在目录名）

- [ ] **Step 1: 写失败的测试**

追加到 `tests/test_build_registry.py`：

```python
from build_registry import parse_segment

SEGMENT = """
目标地址: https://www.cnindex.com.cn/index.html

描述: 国证指数-最近交易日的所有指数

限量: 单次返回所有指数

输入参数

| 名称     | 类型  | 描述 |
|--------|-----|----|
| symbol | str | -  |

输出参数

| 名称     | 类型  | 描述 |
|--------|-----|----|
| 指数代码 | str | -  |

接口示例

```python
import akshare as ak

df = ak.index_all_cni()
print(df)
```

数据示例
"""


def test_parse_segment_extracts_fields():
    rec = parse_segment(SEGMENT)
    assert rec["url"] == "https://www.cnindex.com.cn/index.html"
    assert rec["desc"] == "国证指数-最近交易日的所有指数"
    assert rec["limit_desc"] == "单次返回所有指数"
    assert rec["params"] == [{"name": "symbol", "type": "str", "desc": "-"}]
    assert rec["outputs"] == [{"name": "指数代码", "type": "str", "desc": "-"}]
    assert rec["example"].startswith("import akshare as ak")
    assert "print(df)" in rec["example"]


def test_parse_segment_absent_limit_is_none():
    rec = parse_segment("描述: 某接口\n\n目标地址: https://x.com\n")
    assert rec["limit_desc"] is None
    assert rec["params"] == []
    assert rec["example"] is None
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_build_registry.py -v`
Expected: FAIL，`ImportError: cannot import name 'parse_segment'`

- [ ] **Step 3: 实现 parse_segment 与 collect_doc_records**

追加到 `scripts/build_registry.py`（`import re` 下方补充 `import pathlib`）：

```python
# 冒号必须同时容错半角 ":" 与全角 "："。实测 docs/data/stock/stock.md 中有 10 个
# 接口条目使用全角冒号（stock_info_global_em/sina/ths/futu/cls、stock_info_cjzc_em、
# stock_rank_cxg/cxd/lxsz/lxxd_ths），它们都是真实导出的接口。只匹配半角会让这些
# 条目不被识别为边界，其正文被并入前一条记录，接口本身则从 registry 中彻底消失。
BLOCK_RE = re.compile(r"^接口[:：]\s*(\S+)\s*$", re.M)
EXAMPLE_RE = re.compile(r"```python\n(.*?)```", re.S)


def _field(segment: str, key: str) -> Optional[str]:
    """抽取 "键: 值" 形式的单行字段，冒号半角全角均可。"""
    match = re.search(rf"^{re.escape(key)}[:：]\s*(.+?)\s*$", segment, re.M)
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
            record = parse_segment(text[match.end():end])
            record["category"] = path.parent.name
            records[name] = record
    return records
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_build_registry.py -v`
Expected: 6 passed

- [ ] **Step 5: 用真实文档冒烟验证**

Run:

```bash
python -c "
import sys, pathlib; sys.path.insert(0, 'scripts')
from build_registry import collect_doc_records
r = collect_doc_records(pathlib.Path('docs/data'))
print('records:', len(r))
print('with outputs:', sum(1 for v in r.values() if v['outputs']))
print('with example:', sum(1 for v in r.values() if v['example']))
"
```

Expected: `records: 1018`、`with outputs` 约 959、`with example: 1018`。**records 必须是 1018**，若不是则说明条目切分有误（最常见的原因是冒号未容错全角），先排查再继续；`with outputs` 是参考值，允许小幅出入。

- [ ] **Step 6: 格式化并提交**

```bash
ruff format scripts/build_registry.py tests/
ruff check scripts/build_registry.py tests/ --fix
git add scripts/build_registry.py tests/test_build_registry.py
git commit -m "feat(registry): 新增接口条目解析"
```

---

### Task 3: 导出表提取

从 `akshare/__init__.py` 静态解析出「接口名 → 模块路径」，并排除非数据接口。这是不变量①（主键集合以代码为准）的实现基础。

**Files:**
- Modify: `scripts/build_registry.py`
- Test: `tests/test_build_registry.py`

**Interfaces:**
- Consumes: 无
- Produces: `collect_exports(init_path: Path) -> Dict[str, str]`，键为接口名，值为模块路径如 `"akshare.index.index_cni"`；已排除非数据接口

- [ ] **Step 1: 写失败的测试**

追加到 `tests/test_build_registry.py`：

```python
import pathlib
from build_registry import collect_exports

FAKE_INIT = '''"""模块文档字符串"""

from akshare._version import __version__
from akshare.index.index_cni import index_all_cni, index_hist_cni
from akshare.pro.data_pro import pro_api
from akshare.utils.token_process import set_token, get_token
from .exceptions import APIError, NetworkError

try:
    from akqmt import xt_api
except ImportError:
    pass
'''


def test_collect_exports_maps_name_to_module(tmp_path):
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    exports = collect_exports(init_file)
    assert exports["index_all_cni"] == "akshare.index.index_cni"
    assert exports["index_hist_cni"] == "akshare.index.index_cni"


def test_collect_exports_drops_non_data_interfaces(tmp_path):
    """__version__/pro_api/set_token 等可推断 category，必须显式排除。"""
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    exports = collect_exports(init_file)
    for name in ("__version__", "pro_api", "set_token", "get_token",
                 "APIError", "NetworkError", "xt_api"):
        assert name not in exports
    assert len(exports) == 2
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_build_registry.py -v`
Expected: FAIL，`ImportError: cannot import name 'collect_exports'`

- [ ] **Step 3: 实现 collect_exports**

追加到 `scripts/build_registry.py`（顶部补充 `import ast`）：

```python
# 非数据接口，必须显式排除。不可依赖「category 能否推断」判定：
# 实测 1100 个顶层导出中 6 个不可推断 category，而这 6 个恰好只是异常类
# （相对导入 from .exceptions）；__version__ / pro_api / set_token / get_token
# 均可推断 category，若按「不可推断即排除」实现会被错误收录。
EXCLUDE = {
    "__version__",
    "pro_api",
    "set_token",
    "get_token",
    "xt_api",
    "AkshareException",
    "APIError",
    "DataParsingError",
    "InvalidParameterError",
    "NetworkError",
    "RateLimitError",
}


def collect_exports(init_path: pathlib.Path) -> Dict[str, str]:
    """
    静态解析 __init__.py，提取公开数据接口及其所属模块。

    :param init_path: akshare/__init__.py 路径
    :return: 接口名 -> 模块路径
    """
    tree = ast.parse(init_path.read_text(encoding="utf-8"))
    exports: Dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if not node.module or not node.module.startswith("akshare."):
            continue
        for alias in node.names:
            name = alias.asname or alias.name
            if name in EXCLUDE:
                continue
            exports[name] = node.module
    return exports
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_build_registry.py -v`
Expected: 8 passed

- [ ] **Step 5: 用真实文件冒烟验证**

Run:

```bash
python -c "
import sys, pathlib; sys.path.insert(0, 'scripts')
from build_registry import collect_exports
e = collect_exports(pathlib.Path('akshare/__init__.py'))
print('exports:', len(e))
print('excluded ok:', all(k not in e for k in ('__version__','pro_api','set_token')))
"
```

Expected: `exports: 1090`（1100 个顶层导出减去 6 个异常类与 4 个非数据接口）、`excluded ok: True`

- [ ] **Step 6: 格式化并提交**

```bash
ruff format scripts/build_registry.py tests/
ruff check scripts/build_registry.py tests/ --fix
git add scripts/build_registry.py tests/test_build_registry.py
git commit -m "feat(registry): 新增导出表静态解析"
```

---

### Task 4: 合并、确定性序列化与产物生成

把导出表与文档记录合并成最终 Schema，写出字节确定的 JSON，并生成真实产物提交进 git。

**Files:**
- Modify: `scripts/build_registry.py`
- Create: `akshare/data/interfaces.json`
- Test: `tests/test_build_registry.py`

**Interfaces:**
- Consumes: `collect_exports`（Task 3）、`collect_doc_records`（Task 2）
- Produces:
  - `merge_records(exports: Dict[str, str], docs: Dict[str, Dict]) -> List[Dict]`
  - `serialize(records: List[Dict]) -> str`
  - `build(repo_root: pathlib.Path) -> str`，返回序列化后的 JSON 文本
  - CLI：`python scripts/build_registry.py`（写入产物）

- [ ] **Step 1: 写失败的测试**

追加到 `tests/test_build_registry.py`：

```python
import json
from build_registry import merge_records, serialize


def test_merge_uses_exports_as_primary_key():
    """文档孤儿不得进入结果；无文档的导出必须保留并标记。"""
    exports = {"index_all_cni": "akshare.index.index_cni",
               "no_doc_func": "akshare.stock_feature.stock_info"}
    docs = {"index_all_cni": {"desc": "国证指数", "url": "https://x.com",
                              "limit_desc": None, "params": [], "outputs": [],
                              "example": None, "category": "index"},
            "orphan_func": {"desc": "已删除的接口", "url": None,
                            "limit_desc": None, "params": [], "outputs": [],
                            "example": None, "category": "stock"}}
    records = merge_records(exports, docs)
    names = [r["name"] for r in records]
    assert "orphan_func" not in names
    assert names == ["index_all_cni", "no_doc_func"]  # 已按字典序排序
    documented = {r["name"]: r["documented"] for r in records}
    assert documented == {"index_all_cni": True, "no_doc_func": False}


def test_merge_infers_category_from_module_when_undocumented():
    exports = {"no_doc_func": "akshare.stock_feature.stock_info"}
    records = merge_records(exports, {})
    assert records[0]["category"] == "stock_feature"
    assert records[0]["desc"] is None


def test_serialize_is_deterministic():
    exports = {"b_func": "akshare.stock.a", "a_func": "akshare.fund.b"}
    records = merge_records(exports, {})
    assert serialize(records) == serialize(records)


def test_serialize_has_no_timestamp_or_version():
    records = merge_records({"f": "akshare.stock.a"}, {})
    payload = json.loads(serialize(records))
    assert set(payload.keys()) == {"schema_version", "interfaces"}


def test_serialize_ends_with_single_newline():
    text = serialize(merge_records({"f": "akshare.stock.a"}, {}))
    assert text.endswith("}\n")
    assert not text.endswith("\n\n")
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_build_registry.py -v`
Expected: FAIL，`ImportError: cannot import name 'merge_records'`

- [ ] **Step 3: 实现合并与序列化**

追加到 `scripts/build_registry.py`（顶部补充 `import json`、`import argparse`）：

```python
SCHEMA_VERSION = 1


def merge_records(exports: Dict[str, str], docs: Dict[str, Dict]) -> List[Dict]:
    """
    以导出表为主键集合合并文档信息。

    不变量①：结果中的每个 name 都保证可通过 getattr(ak, name) 取到，
    因此文档中存在而代码未导出的条目会被丢弃。

    :param exports: 接口名 -> 模块路径
    :param docs: 接口名 -> 文档元数据
    :return: 按 name 字典序排序的记录列表
    """
    records = []
    for name in sorted(exports):
        module = exports[name]
        doc = docs.get(name)
        records.append(
            {
                "name": name,
                "module": module,
                "category": (doc or {}).get("category") or module.split(".")[1],
                "documented": doc is not None,
                "desc": (doc or {}).get("desc"),
                "url": (doc or {}).get("url"),
                "limit_desc": (doc or {}).get("limit_desc"),
                "params": (doc or {}).get("params") or [],
                "outputs": (doc or {}).get("outputs") or [],
                "example": (doc or {}).get("example"),
            }
        )
    return records


def serialize(records: List[Dict]) -> str:
    """
    确定性序列化。禁止写入时间戳与版本号，否则会污染 --check 的 diff 比对。

    :param records: 记录列表
    :return: JSON 文本，末尾带单个换行
    """
    payload = {"schema_version": SCHEMA_VERSION, "interfaces": records}
    return (
        json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )
        + "\n"
    )


def build(repo_root: pathlib.Path) -> str:
    """
    生成完整的 registry JSON 文本。

    :param repo_root: 仓库根目录
    :return: JSON 文本
    """
    exports = collect_exports(repo_root / "akshare" / "__init__.py")
    docs = collect_doc_records(repo_root / "docs" / "data")
    return serialize(merge_records(exports, docs))


OUTPUT_RELPATH = pathlib.Path("akshare") / "data" / "interfaces.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="生成接口元数据 registry")
    parser.add_argument(
        "--check", action="store_true", help="仅校验，不写入（供 CI 使用）"
    )
    args = parser.parse_args()
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    text = build(repo_root)
    if args.check:
        return 0  # Task 5 实现完整校验
    (repo_root / OUTPUT_RELPATH).write_text(text, encoding="utf-8", newline="\n")
    print(f"已写入 {OUTPUT_RELPATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

注意 `write_text(..., newline="\n")`：Windows 下默认会把 `\n` 转成 `\r\n`，导致跨平台生成的字节不同，`--check` 必然失败。

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_build_registry.py -v`
Expected: 13 passed

- [ ] **Step 5: 生成真实产物并验证确定性**

Run:

```bash
python scripts/build_registry.py
python -c "
import json, pathlib
p = pathlib.Path('akshare/data/interfaces.json')
d = json.loads(p.read_text(encoding='utf-8'))
print('size: %.2f MB' % (p.stat().st_size/1e6))
print('interfaces:', len(d['interfaces']))
print('documented:', sum(1 for i in d['interfaces'] if i['documented']))
"
cp akshare/data/interfaces.json /tmp/first.json
python scripts/build_registry.py
diff -q /tmp/first.json akshare/data/interfaces.json && echo "确定性 OK"
```

Expected: size 约 1.19 MB、interfaces 1090、documented 1015、输出「确定性 OK」

- [ ] **Step 6: 提交**

```bash
ruff format scripts/build_registry.py tests/
ruff check scripts/build_registry.py tests/ --fix
git add scripts/build_registry.py tests/test_build_registry.py akshare/data/interfaces.json
git commit -m "feat(registry): 生成接口元数据产物"
```

---

### Task 5: --check 校验与 baseline 棘轮

**Files:**
- Modify: `scripts/build_registry.py`
- Create: `scripts/registry_baseline.json`
- Test: `tests/test_build_registry.py`

**Interfaces:**
- Consumes: `build`（Task 4）、`collect_exports`、`collect_doc_records`
- Produces: `diff_baseline(exports, docs, baseline: Dict) -> List[str]`，返回违规说明列表，空列表代表通过

- [ ] **Step 1: 写失败的测试**

追加到 `tests/test_build_registry.py`：

```python
from build_registry import diff_baseline

BASE = {"undocumented": ["old_no_doc"], "orphaned": ["old_orphan"]}


def test_baseline_allows_known_gaps():
    exports = {"old_no_doc": "akshare.stock.a"}
    docs = {"old_orphan": {"category": "stock"}}
    assert diff_baseline(exports, docs, BASE) == []


def test_baseline_rejects_new_undocumented():
    exports = {"old_no_doc": "akshare.stock.a", "brand_new": "akshare.fund.b"}
    docs = {"old_orphan": {"category": "stock"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "brand_new" in problems[0]


def test_baseline_rejects_new_orphan():
    exports = {"old_no_doc": "akshare.stock.a"}
    docs = {"old_orphan": {"category": "stock"}, "new_orphan": {"category": "fund"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "new_orphan" in problems[0]


def test_baseline_rejects_stale_entry():
    """已修复的项必须从 baseline 移除，否则 baseline 会腐烂。"""
    exports = {"old_no_doc": "akshare.stock.a"}
    docs = {"old_no_doc": {"category": "stock"}, "old_orphan": {"category": "stock"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "old_no_doc" in problems[0]
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_build_registry.py -v`
Expected: FAIL，`ImportError: cannot import name 'diff_baseline'`

- [ ] **Step 3: 实现双向棘轮校验**

追加到 `scripts/build_registry.py`：

```python
BASELINE_RELPATH = pathlib.Path("scripts") / "registry_baseline.json"


def diff_baseline(
    exports: Dict[str, str], docs: Dict[str, Dict], baseline: Dict
) -> List[str]:
    """
    双向棘轮校验：缺口不得超出 baseline，baseline 中也不得残留已修复项。

    :param exports: 接口名 -> 模块路径
    :param docs: 接口名 -> 文档元数据
    :param baseline: 含 undocumented / orphaned 两个名单
    :return: 违规说明列表，空列表代表通过
    """
    undocumented = set(exports) - set(docs)
    orphaned = set(docs) - set(exports)
    known_undoc = set(baseline.get("undocumented", []))
    known_orphan = set(baseline.get("orphaned", []))
    problems = []
    for name in sorted(undocumented - known_undoc):
        problems.append(f"新增接口 {name} 缺少 docs/data 文档条目")
    for name in sorted(orphaned - known_orphan):
        problems.append(f"文档条目 {name} 在 __init__.py 中没有对应导出")
    for name in sorted(known_undoc - undocumented):
        problems.append(f"{name} 已补文档，请从 registry_baseline.json 移除")
    for name in sorted(known_orphan - orphaned):
        problems.append(f"{name} 的文档漂移已修复，请从 registry_baseline.json 移除")
    return problems
```

同时把 `main()` 中 `--check` 的占位实现替换为：

```python
    baseline_path = repo_root / BASELINE_RELPATH
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    exports = collect_exports(repo_root / "akshare" / "__init__.py")
    docs = collect_doc_records(repo_root / "docs" / "data")
    problems = diff_baseline(exports, docs, baseline)
    current = (repo_root / OUTPUT_RELPATH).read_text(encoding="utf-8")
    if current != text:
        problems.append(
            "interfaces.json 与源不同步，请运行 python scripts/build_registry.py"
        )
    if problems:
        for problem in problems:
            print(f"[registry] {problem}")
        return 1
    print("[registry] 校验通过")
    return 0
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_build_registry.py -v`
Expected: 17 passed

- [ ] **Step 5: 生成 baseline 并验证 --check 通过**

Run:

```bash
python -c "
import sys, json, pathlib; sys.path.insert(0, 'scripts')
from build_registry import collect_exports, collect_doc_records
e = collect_exports(pathlib.Path('akshare/__init__.py'))
d = collect_doc_records(pathlib.Path('docs/data'))
base = {'undocumented': sorted(set(e)-set(d)), 'orphaned': sorted(set(d)-set(e))}
pathlib.Path('scripts/registry_baseline.json').write_text(
    json.dumps(base, ensure_ascii=False, indent=2, sort_keys=True)+'\n',
    encoding='utf-8', newline='\n')
print('undocumented:', len(base['undocumented']))
print('orphaned:', base['orphaned'])
"
python scripts/build_registry.py --check
```

Expected: `undocumented: 75`、`orphaned` 为 `['fortune_rank', 'option_czce_hist', 'stock_zh_a_tick_tx']`、`--check` 输出「校验通过」且退出码 0

75 的推导：顶层导出共 1100 个，经 `EXCLUDE` 排除 6 个异常类与 4 个非数据接口后 `exports` 为 1090；文档条目在冒号容错后为 1018 条，与 exports 的交集为 1015，相减得 75。（早期基于半角冒号的统计为 85，其中 10 个接口实为全角冒号文档被漏读，不是真的缺文档。）

- [ ] **Step 6: 验证门禁真的会失败（两种模式都要验）**

门禁有两条独立的失败路径，必须分别确认，否则可能出现「校验永远通过」的假安全。

**模式一：产物与源不同步**

```bash
python -c "
import pathlib
p = pathlib.Path('akshare/data/interfaces.json')
p.write_text(p.read_text(encoding='utf-8').replace('\"schema_version\":1', '\"schema_version\":2'), encoding='utf-8', newline='\n')
"
python scripts/build_registry.py --check; echo "退出码: $?"
git checkout akshare/data/interfaces.json
```

Expected: 输出「interfaces.json 与源不同步」，退出码 1。

**模式二：文档条目丢失（对应 spec 验收标准第 5 条）**

把一个已有文档的接口条目改名，模拟「有人删了文档」与「文档里留下孤儿」同时发生：

```bash
python -c "
import pathlib
p = pathlib.Path('docs/data/index/index.md')
p.write_text(p.read_text(encoding='utf-8').replace(
    '接口: index_all_cni', '接口: index_all_cni_TEMP', 1), encoding='utf-8')
"
python scripts/build_registry.py --check; echo "退出码: $?"
git checkout docs/data/index/index.md
```

Expected: 同时报出两条违规——「新增接口 index_all_cni 缺少 docs/data 文档条目」与「文档条目 index_all_cni_TEMP 在 \_\_init\_\_.py 中没有对应导出」，退出码 1。

两种模式验完后务必确认工作区已恢复干净：

```bash
git status --short && python scripts/build_registry.py --check
```

Expected: 无未预期改动，`--check` 输出「校验通过」

- [ ] **Step 7: 提交**

```bash
ruff format scripts/build_registry.py tests/
ruff check scripts/build_registry.py tests/ --fix
git add scripts/build_registry.py scripts/registry_baseline.json tests/test_build_registry.py
git commit -m "feat(registry): 新增 --check 门禁与 baseline 棘轮"
```

---

### Task 6: 运行期数据加载与打分函数

**Files:**
- Create: `akshare/registry.py`
- Modify: `akshare/datasets.py`
- Test: `tests/test_registry.py`

**Interfaces:**
- Consumes: `akshare/data/interfaces.json`（Task 4 产物）
- Produces:
  - `akshare.datasets.get_registry_json(file: str = "interfaces.json") -> pathlib.Path`
  - `akshare.registry._tokenize(query: str) -> List[str]`
  - `akshare.registry._score(tokens: List[str], record: Dict) -> float`

- [ ] **Step 1: 写失败的测试**

创建 `tests/test_registry.py`：

```python
from akshare.registry import _tokenize, _score

RECORD = {
    "name": "stock_zh_a_hist",
    "category": "stock",
    "documented": True,
    "desc": "东方财富-沪深京 A 股历史行情数据",
    "outputs": [{"name": "市盈率", "type": "float64", "desc": "-"}],
}
UNDOC = dict(RECORD, name="stock_zh_a_other", documented=False)


def test_tokenize_splits_on_whitespace_and_punctuation():
    assert _tokenize("A股 历史行情") == ["A股", "历史行情"]
    assert _tokenize("stock,hist") == ["stock", "hist"]


def test_tokenize_drops_empty():
    assert _tokenize("   ") == []


def test_score_exact_name_match_dominates():
    assert _score(["stock_zh_a_hist"], RECORD) >= 100


def test_score_desc_hit_lower_than_name_hit():
    name_hit = _score(["hist"], RECORD)
    desc_hit = _score(["东方财富"], RECORD)
    assert name_hit > desc_hit > 0


def test_score_matches_output_column():
    assert _score(["市盈率"], RECORD) > 0


def test_score_all_tokens_hit_gets_bonus():
    both = _score(["hist", "东方财富"], RECORD)
    single = _score(["hist", "不存在的词"], RECORD)
    assert both > single


def test_score_undocumented_is_downweighted():
    assert _score(["历史行情"], UNDOC) < _score(["历史行情"], RECORD)


def test_score_no_hit_returns_zero():
    assert _score(["完全不相关"], RECORD) == 0
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_registry.py -v`
Expected: FAIL，`ModuleNotFoundError: No module named 'akshare.registry'`

- [ ] **Step 3: 在 datasets.py 追加产物路径解析**

追加到 `akshare/datasets.py` 末尾的 `if __name__` 之前：

```python
def get_registry_json(file: str = "interfaces.json") -> pathlib.Path:
    """
    get path to data "interfaces.json" file.
    :return: 文件路径
    :rtype: pathlib.Path
    """
    with resources.path("akshare.data", file) as f:
        data_file_path = f
        return data_file_path
```

- [ ] **Step 4: 实现 registry.py 的加载与打分**

创建 `akshare/registry.py`：

```python
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
```

- [ ] **Step 5: 运行测试确认通过**

Run: `pytest tests/test_registry.py -v`
Expected: 8 passed

- [ ] **Step 6: 验证懒加载未拖慢 import**

Run:

```bash
python -c "
import time, akshare
t = time.time(); import akshare.registry; print('registry import: %.4fs' % (time.time()-t))
import akshare.registry as r; print('data loaded before search:', r._REGISTRY is None)
"
```

Expected: `registry import` 远小于 0.01s，且 `data loaded before search: True`

- [ ] **Step 7: 提交**

```bash
ruff format akshare/registry.py akshare/datasets.py tests/
ruff check akshare/registry.py akshare/datasets.py tests/ --fix
git add akshare/registry.py akshare/datasets.py tests/test_registry.py
git commit -m "feat(registry): 新增运行期数据加载与打分函数"
```

---

### Task 7: 公开检索 API

**Files:**
- Modify: `akshare/registry.py`
- Test: `tests/test_registry.py`

**Interfaces:**
- Consumes: `_load`、`_tokenize`、`_score`（Task 6）
- Produces:
  - `search(query: str, limit: int = 20, category: Optional[str] = None, documented_only: bool = False) -> pd.DataFrame`，列为 `["接口名", "类目", "描述", "有无文档", "匹配分"]`
  - `interface_info(name: str) -> Dict`
  - `list_categories() -> pd.DataFrame`，列为 `["类目", "接口数"]`

- [ ] **Step 1: 写失败的测试**

追加到 `tests/test_registry.py`：

```python
import pandas as pd
import pytest

from akshare.exceptions import InvalidParameterError
from akshare import registry

FIXTURE = {
    "schema_version": 1,
    "interfaces": [
        {"name": "stock_zh_a_hist", "module": "akshare.stock.a", "category": "stock",
         "documented": True, "desc": "东方财富-沪深京 A 股历史行情数据", "url": None,
         "limit_desc": None, "params": [], "outputs": [], "example": None},
        {"name": "fund_open_fund_info_em", "module": "akshare.fund.b",
         "category": "fund", "documented": True, "desc": "东方财富-开放式基金净值",
         "url": None, "limit_desc": None, "params": [], "outputs": [],
         "example": None},
        {"name": "stock_no_doc", "module": "akshare.stock.c", "category": "stock",
         "documented": False, "desc": None, "url": None, "limit_desc": None,
         "params": [], "outputs": [], "example": None},
    ],
}


@pytest.fixture(autouse=True)
def _use_fixture(monkeypatch):
    monkeypatch.setattr(registry, "_REGISTRY", FIXTURE)
    yield
    monkeypatch.setattr(registry, "_REGISTRY", None)


def test_search_returns_dataframe_with_expected_columns():
    df = registry.search("历史行情")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["接口名", "类目", "描述", "有无文档", "匹配分"]
    assert df.iloc[0]["接口名"] == "stock_zh_a_hist"


def test_search_empty_result_keeps_columns():
    df = registry.search("完全不相关的词")
    assert df.empty
    assert list(df.columns) == ["接口名", "类目", "描述", "有无文档", "匹配分"]


def test_search_respects_limit():
    assert len(registry.search("东方财富", limit=1)) == 1


def test_search_filters_by_category():
    df = registry.search("东方财富", category="fund")
    assert set(df["类目"]) == {"fund"}


def test_search_documented_only_excludes_undocumented():
    df = registry.search("stock", documented_only=True)
    assert "stock_no_doc" not in set(df["接口名"])


def test_interface_info_returns_full_record():
    info = registry.interface_info("stock_zh_a_hist")
    assert info["module"] == "akshare.stock.a"
    assert info["desc"] == "东方财富-沪深京 A 股历史行情数据"


def test_interface_info_unknown_name_suggests_candidates():
    with pytest.raises(InvalidParameterError) as exc:
        registry.interface_info("stock_zh_a_hisr")
    assert "stock_zh_a_hist" in str(exc.value)


def test_list_categories_counts():
    df = registry.list_categories()
    assert list(df.columns) == ["类目", "接口数"]
    assert dict(zip(df["类目"], df["接口数"]))["stock"] == 2
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_registry.py -v`
Expected: FAIL，`AttributeError: module 'akshare.registry' has no attribute 'search'`

- [ ] **Step 3: 实现三个公开 API**

在 `akshare/registry.py` 顶部导入处补充 `import pandas as pd` 与 `from akshare.exceptions import InvalidParameterError`，然后追加：

```python
SEARCH_COLUMNS = ["接口名", "类目", "描述", "有无文档", "匹配分"]
MIN_HITS_BEFORE_FALLBACK = 3


def _bigrams(query: str) -> List[str]:
    """
    把查询压成连续字符 2-gram，用于用户未打空格时的降级召回。

    :param query: 查询字符串
    :return: 2-gram 列表
    """
    compact = re.sub(r"\s+", "", query)
    return [compact[i: i + 2] for i in range(len(compact) - 1)]


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
            scored = [
                (record, _score(fallback_tokens, record)) for record in records
            ]
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
    rows = [
        {"类目": key, "接口数": counter[key]} for key in sorted(counter)
    ]
    return pd.DataFrame(rows, columns=["类目", "接口数"])
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_registry.py -v`
Expected: 16 passed

- [ ] **Step 5: 提交**

```bash
ruff format akshare/registry.py tests/
ruff check akshare/registry.py tests/ --fix
git add akshare/registry.py tests/test_registry.py
git commit -m "feat(registry): 新增 search/interface_info/list_categories 接口"
```

---

### Task 8: 导出到公开 API 并验证不变量

**Files:**
- Modify: `akshare/__init__.py`
- Test: `tests/test_registry_integration.py`（新建）

集成测试必须放在**独立文件**，不能追加到 `tests/test_registry.py`：后者有一个 `autouse=True` 的 fixture 会给全文件注入假数据，而集成测试需要真实产物。同文件靠 `monkeypatch` 反转 autouse fixture 依赖执行顺序，脆弱且难读。

**Interfaces:**
- Consumes: `search`、`interface_info`、`list_categories`（Task 7）
- Produces: `ak.search`、`ak.interface_info`、`ak.list_categories`

- [ ] **Step 1: 写失败的集成测试**

创建 `tests/test_registry_integration.py`：

```python
import pytest

from akshare import registry


@pytest.fixture(autouse=True)
def _force_real_registry(monkeypatch):
    """确保从真实产物文件加载，不受其他测试文件注入的假数据影响。"""
    monkeypatch.setattr(registry, "_REGISTRY", None)


def test_public_api_is_exported():
    import akshare as ak

    assert callable(ak.search)
    assert callable(ak.interface_info)
    assert callable(ak.list_categories)


def test_real_search_returns_callable_interfaces():
    """不变量①：search 返回的每个接口名都必须真实可调用。"""
    import akshare as ak

    df = ak.search("A股 历史行情", limit=10)
    assert not df.empty
    for name in df["接口名"]:
        assert hasattr(ak, name), f"{name} 在 registry 中但无法从 akshare 取到"


def test_every_registry_entry_is_reachable():
    """全量校验不变量①，将来有人删函数忘删文档时会立即失败。"""
    import akshare as ak

    missing = [
        item["name"]
        for item in registry._load()["interfaces"]
        if not hasattr(ak, item["name"])
    ]
    assert missing == [], f"registry 中有 {len(missing)} 个接口无法取到: {missing[:5]}"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_registry.py -v`
Expected: FAIL，`AttributeError: module 'akshare' has no attribute 'search'`

- [ ] **Step 3: 追加导出**

在 `akshare/__init__.py` 末尾、`AKQMT 设置` 之前插入：

```python
"""
接口检索层
"""
from akshare.registry import search, interface_info, list_categories
```

同时在文件顶部版本记录 docstring 的末尾追加一行（紧跟当前最后一行 `1.18.84 fix: fix index_all_cni interface` 之后）：

```
1.18.85 feat: add interface registry search API
```

- [ ] **Step 4: 运行全部测试确认通过**

Run: `pytest -v`
Expected: 全部通过（含原有 2 个 `test_func.py` 测试）

- [ ] **Step 5: 手工冒烟**

Run:

```bash
python -c "
import akshare as ak
print(ak.search('A股 历史行情', limit=5).to_string())
print()
print(ak.search('A股历史行情', limit=3)['接口名'].tolist())  # 无空格，验证 2-gram 降级
print()
print(ak.list_categories().head().to_string())
print()
try:
    ak.interface_info('stock_zh_a_hisr')
except Exception as e:
    print('异常提示:', e)
"
```

Expected: 第一条返回相关接口；无空格查询仍有结果；类目统计非空；异常消息中含 `stock_zh_a_hist` 候选

- [ ] **Step 6: 提交**

```bash
ruff format tests/test_registry_integration.py
ruff check tests/test_registry_integration.py --fix
git add akshare/__init__.py tests/test_registry_integration.py
git commit -m "feat(registry): 导出检索接口至公开 API"
```

---

### Task 9: CI 门禁与发布约定同步

**Files:**
- Modify: `.github/workflows/main_dev_check.yml`
- Modify: `akshare/_version.py`
- Modify: `docs/changelog.md`
- Modify: `docs/introduction.md`

**Interfaces:**
- Consumes: `python scripts/build_registry.py --check`（Task 5）
- Produces: 无

- [ ] **Step 1: 追加独立的 registry-check job**

现有 workflow 是 3 OS × 4 Python 的 12 格矩阵，registry 校验与平台无关，必须独立成 job 只跑一次。在 `.github/workflows/main_dev_check.yml` 的 `jobs:` 下追加：

```yaml
  registry-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.13"

      - name: Check interface registry is in sync
        run: python scripts/build_registry.py --check
```

- [ ] **Step 2: 本地验证该命令**

Run: `python scripts/build_registry.py --check; echo "退出码: $?"`
Expected: 输出「校验通过」，退出码 0

- [ ] **Step 3: 按仓库发布约定同步版本与文档**

`akshare/_version.py` 改为：

```python
__version__ = "1.18.85"
```

`docs/changelog.md` 在 `## 更新说明详情` 下方最前面插入：

```
1.18.85 feat: add interface registry search API

    1. 新增 ak.search 接口检索功能，支持按自然语言定位接口
    2. 新增 ak.interface_info 接口元数据查询功能
    3. 新增 ak.list_categories 类目列表功能
    4. 新增 CI 门禁，校验文档与接口导出的一致性

```

`docs/introduction.md` 中的文档更新时间改为：

```
1. 本文档更新时间：**2026-08-12**；
```

（`akshare/__init__.py` 的版本记录行已在 Task 8 Step 3 追加，此处不重复。）

- [ ] **Step 4: 全量验收**

**不要跑 `ruff format .`**。当前 ruff 会格式化 Markdown 里的 Python 代码块，全量执行会改动 11 个与本次无关的 md 文件（`README.md`、多个 `docs/*.md`、本 plan 与 spec 自身）以及 1 个存量 py 文件 `akshare/stock_feature/stock_margin_bse.py`，污染提交。项目 CI 用的是修改模式的 `ruff format .` 而非 `--check`，所以这些存量不合规长期存在且不会导致 CI 失败——不属于本次范围。

只校验本次涉及的 Python 文件：

```bash
ruff format --check scripts/build_registry.py akshare/registry.py akshare/datasets.py tests/
ruff check scripts/build_registry.py akshare/registry.py akshare/datasets.py tests/
pytest -v
python scripts/build_registry.py --check
python -c "
import time
t = time.time(); import akshare as ak; print('import 耗时: %.2fs' % (time.time()-t))
import akshare.registry as r; print('检索前未加载数据:', r._REGISTRY is None)
print('检索可用:', not ak.search('基金 净值', limit=3).empty)
"
```

Expected: ruff 两条命令均无输出问题；pytest 全绿；`--check` 通过；import 耗时与实施前基线（约 1.95s）无可测量差异；`检索前未加载数据: True`

- [ ] **Step 5: 提交**

```bash
git add .github/workflows/main_dev_check.yml akshare/_version.py docs/changelog.md docs/introduction.md
git commit -m "ci(registry): 新增接口一致性门禁并同步版本文档"
```

---

## 遗留事项（不在本计划范围）

以下由 baseline 记录，各自单独提 PR 处理，详见 spec 第 12 节：

| 接口 | 状态 | 建议处置 |
|---|---|---|
| `fortune_rank` | 函数存在于 `akshare/fortune/fortune_500.py:40`，历史修复四次，当前未导出 | 补 `__init__.py` 导出 |
| `option_czce_hist` | 已于 1.17.68 更名为 `option_hist_yearly_czce`，文档未同步 | 删除过期文档条目 |
| `stock_zh_a_tick_tx` | 函数存在未导出 | 需维护者判断补导出还是正式下线 |
| 75 个无文档接口 | 见 `scripts/registry_baseline.json` | 逐步补文档，baseline 只减不增 |

### 本次实施中记录的延后项

以下问题在「检索质量最终修复轮」的实施与 review 过程中被发现，均已评估为
可延后、不阻塞本轮合并，按主题归档于此，避免随工作区清理而丢失，后续各自
单独提 PR 处理。

#### 检索质量

- **`parse_table` 在标题与表格之间夹了小标题时返回空表。**
  `scripts/build_registry.py` 的 `parse_table` 用「标题行之后跳过空行，
  遇到第一个非 `|` 开头的行立即终止」的规则定位表格，如果标题与表格之间
  插入了一行说明性小标题（而非直接是表格），该规则会在小标题处提前终止，
  返回空表。实测 10 个已文档接口的 `输出参数` 全部因此丢失：
  `article_oman_rv`、`article_rlab_rv`、`fx_spot_quote`、`fx_swap_quote`、
  `option_finance_board`、`option_hist_shfe`、`option_hist_dce`、
  `option_hist_czce`、`option_hist_gfex`、`option_vol_gfex`。它们在产物中
  `outputs: []`，与「文档本来就没有输出表」无法区分，导致输出列反查失效、
  `interface_info` 误报。修法需要有界前瞻——向后扫描，但一旦遇到下一个
  `输入参数` / `输出参数` / `接口:` 边界即停，不能无界扫描。**陷阱**：
  `article_oman_rv` 同时是 Task 1 跨表污染回归测试的 `CONTAMINATED` 样本
  来源，若简单放宽为「跳过文本直到首个表格」会重新破坏
  `test_parse_table_stops_at_blank_line_not_next_table`，修的时候要连带
  跑一遍该测试。
- **`匹配分` 列不可用作置信度信号。** spec 第 6 节承诺该列「供 agent 判断
  置信度」，但 2-gram 分是按接口名长度累加的，跨记录、跨查询不可比：实测
  两个同为精确匹配的接口 `fred_md` 得 100.0、`macro_china_cpi` 得 228.0。
  排序不受影响（精确名靠 `is_exact` 置顶），损害仅限于展示列的数值本身。
  同时 `akshare/registry.py` 的 `_score` 里，精确名捷径在
  `PENALTY_UNDOCUMENTED` 之前就 `return`，导致无文档接口精确命中反而拿满
  分 100，而其他命中路径都被打五折——这两个问题性质相关，应一并处理
  （归一化展示分，或从 spec 移除「置信度」这一承诺）。
- **2-gram 无条件参与打分带来噪声召回。** 实测 `search("今天天气怎么样")`
  返回 38 行、`search("A股 历史行情")` 有 194 个命中（本轮修复后的实测
  数字，见 final-fix-report）。已评估的两个缓解方向——per-token 取最大值、
  per-record fallback——经 12 查询 benchmark 实测均**更差**（top5 命中率从
  8/12 降到 6/12），不要采用；相对分数下限（丢弃低于最高分约 25% 的结果）
  是尚未验证的可选方向，留给后续单独评估。
- **空白归一化会把 `desc` 内部相邻的两个词融合，产生跨词假匹配。** 本轮
  为解决「`A 股` 带空格导致查询词 `A股` 匹配不上」而在 `_score` 里对被搜索
  字段做了空白压缩，副作用是 `desc` 中由合法空格分隔的两个词也会被压到
  一起，使得跨越原空格位置的子串变得可匹配。实测三例：`article_ff_crr` 的
  desc 含 "Current Research"，压缩后查询 `tRes` 命中并排第一；
  `macro_cons_gold` 含 "SPDR Gold"，查询 `RGo` 命中；`macro_cons_silver`
  含 "iShares Silver"，查询 `sSi` 命中。修复前这些都因字面空格而不匹配。
  这与 `columns` 拼接时的跨列名融合是同一类问题，但 `columns` 可以用
  `"\x00"` 作分隔符规避，`desc` 是单一字符串没有等价修法。**评估为可延后**：
  产物中仅 3/1090 条 desc 含 latin-latin 空格序列，且需要构造恰好跨越原
  空格位置的查询才会触发，不影响精确名保证、`is_exact` 判定与任何硬门槛，
  属排序噪声而非功能性错误。当前无测试覆盖该向量。若后续要修，方向是改用
  分词感知的匹配（而非裸子串），或仅在 CJK↔latin 边界处压缩空白而保留
  latin↔latin 之间的空格。

#### 构建期健壮性

- `main()`（`scripts/build_registry.py`）写产物非原子，中断可能留下截断的
  `interfaces.json`。已被 `--check` 与集成测试里的
  `len(interfaces) > 1000` 守卫兜底；改为写临时文件再 `os.replace` 是两行
  改动，不紧急。
- `scripts/registry_baseline.json` 缺失或 JSON 非法时抛裸 traceback，而非
  清晰的 `[registry]` 消息。仍会以非零退出码结束，CI 门禁不受影响，仅操作
  体验较差。
- `collect_doc_records` 用 `errors="replace"` 读取文档，编码问题会被静默
  替换并写进产物，而不是响亮失败。
- `--check` 中读取产物用 `read_text(encoding="utf-8")`，其 universal-newline
  转换是 Windows checkout 能通过校验的**载重逻辑**（git 工作区可能是
  CRLF，而 blob 是 LF）；代码里目前没有注释说明这一点，将来若有人为了
  「更严格」改成 `read_bytes()` 会破坏所有 Windows 检出，动手前务必先补
  这条注释。
- 仓库自己的 `ruff format .`（CI 的 `build` job 就在跑）会重排
  `docs/data` 下 20 个文件里 `接口示例` 代码块的引号风格（单引号改双
  引号），而这些代码块正是产物 `example` 字段的来源。当前 CI 能自洽仅因为
  `build` job 不提交格式化结果、`registry-check` job 用的是干净检出；一旦
  有人提交一次全量格式化清理的 PR，`registry-check` 会无关地变红（可
  自愈，报错消息里带重新生成命令）。建议在 `scripts/build_registry.py`
  的模块 docstring 里补一句提示，防止这个耦合被遗忘。
- `--check` 会把 `akshare/__init__.py` 与整个 `docs/data` 解析两遍
  （`build()` 内一次、`diff_baseline` 之前又一次）。**已评估无需处理**：
  实测总耗时 0.519s，优化收益不值得为此增加代码复杂度。
- `EXCLUDE`（`scripts/build_registry.py`）的注释未提示「将来若出现真名为
  `search` / `list_categories` 的数据接口会被静默丢弃且无报错」。鉴于仓库
  强制 `<domain>_<topic>_<source>` 命名惯例，撞名概率极低，暂不处理。

#### 运行期健壮性

- `search(None)` / `interface_info(None)` 会抛 `AttributeError` 而非
  `InvalidParameterError`；`search("stock", limit=1.5)` 会泄漏切片操作的
  `TypeError`。`akshare/registry.py` 已经对 `limit < 0` 做了校验，不校验
  类型是内部不一致，但不影响任何文档化的正常调用路径。
- `_load`（`akshare/registry.py`）中 `raise DataParsingError(...)` 未用
  `from e`，会丢失原始 traceback，排障时不够友好。
- `_REGISTRY` 的 check-then-load 无锁，并发首次调用可能重复解析一次
  1.07 MB 的 JSON 文件。仅浪费一次解析开销，不会导致数据损坏（GIL 保证
  模块级变量赋值是原子的），计划本身未要求线程安全。
- `merge_records` 重复七次 `(doc or {}).get(...)`，可以提前
  `doc = doc or {}` 简化。纯可读性问题，不影响行为。

#### 测试覆盖

以下缺口均被 `--check` 的字节级比对兜底：改动涉及的任一处都会让产物
字节变化并使 CI 变红，因此不是「静默漂移」风险，只是覆盖不够精确、定位
问题时不够直接。

- 全角冒号容错的回归测试只覆盖了 `BLOCK_RE`，未独立验证 `_field` 对全角
  `描述：` / `目标地址：` 的容错。实测 `docs/data` 中有 31 处使用全角
  冒号，说明这条容错确实是载重的，值得补一条独立断言。
- `EXCLUDE` 完整性测试只覆盖了 4 个真正依赖 `EXCLUDE` 才能被排除的名字，
  另外 7 个已经被前缀过滤器或 try 过滤器冗余拦截，测试没有区分「必须靠
  EXCLUDE」与「碰巧也被别的规则拦住」。

#### 文档笔误（仅设计文档侧）

- `specs/2026-08-12-interface-registry-design.md` 第 6 节称检索层覆盖
  「36 个类目」，实际为 27 个。
- 同文件第 3 / 第 5 节称产物大小约 1.19 MB，实际为 1,066,985 字节
  （约 1.07 MB）。

#### 存量问题（本次未触碰）

- `akshare/__init__.py` 存在重复导入：`macro_bank_brazil_interest_rate`
  在 5418、5419 两行各导入一次，`stock_margin_bse` 在 3301 与 4444 两行
  各导入一次。均为同符号同模块的重复导入，无害；修复它会违反本计划「只做
  追加式修改」的约束，留给专门清理 `__init__.py` 的 PR。
