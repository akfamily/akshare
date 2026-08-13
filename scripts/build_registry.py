#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 构建期脚本，解析 docs/data 与 akshare/__init__.py 生成接口元数据
"""

import argparse
import ast
import json
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
            record = parse_segment(text[match.end() : end])
            record["category"] = path.parent.name
            records[name] = record
    return records


# 非数据接口，必须显式排除。不可依赖「category 能否推断」判定：
# 实测 1100 个顶层导出中 6 个不可推断 category，而这 6 个恰好只是异常类
# （相对导入 from .exceptions）；__version__ / pro_api / set_token / get_token
# 均可推断 category，若按「不可推断即排除」实现会被错误收录。
#
# 检索层（akshare/registry.py）自身对外暴露的 search / interface_info /
# list_categories 同样是工具函数：查的是接口元数据本身，不属于 docs/data
# 下任何资产类目，因此必须显式排除，否则它们会被本脚本当成新增数据接口
# 收录进产物，进而因缺少 docs/data 文档条目触发 --check 门禁误报（检索层
# 收录了自己）。后续新增面向工具/元数据的公开 API（而非某个资产类目的
# 数据接口）时，同样应加入这里，而不是指望 category 推断把它们过滤掉。
EXCLUDE = {
    "__version__",
    "pro_api",
    "set_token",
    "get_token",
    "AkshareException",
    "APIError",
    "DataParsingError",
    "InvalidParameterError",
    "NetworkError",
    "RateLimitError",
    "search",
    "interface_info",
    "list_categories",
}

# EXCLUDE 的成员被排除在 registry 之外，但除 dunder 以外它们仍是公开 API，
# 因此必须出现在 __all__ 里。dunder 不需要：ak.__version__ 的可访问性与
# __all__ 无关，而 __all__ 只影响 from akshare import * 导出哪些名字。
DUNDER_EXPORTS = {"__version__"}

ALL_BEGIN = "# === __all__ 开始：由 scripts/build_registry.py 生成，请勿手工编辑 ==="
ALL_END = "# === __all__ 结束 ==="


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


def collect_all_names(init_path: pathlib.Path) -> List[str]:
    """
    计算 __init__.py 应当声明的 __all__ 名单。

    构成为「数据接口导出表」并上「EXCLUDE 中的非 dunder 公开 API」。
    刻意不含子模块名（air、bond、cal 等）：它们只是 import 的副产物，
    缺少 __all__ 时 from akshare import * 会把它们一并倒进用户命名空间，
    其中 cal、event、bank 一类通用词很容易静默覆盖用户自己的变量。

    :param init_path: akshare/__init__.py 路径
    :return: 按字典序排序的公开名称列表
    """
    exports = collect_exports(init_path)
    return sorted(set(exports) | (EXCLUDE - DUNDER_EXPORTS))


def render_all_block(names: List[str]) -> str:
    """
    渲染带首尾标记的 __all__ 代码块。

    :param names: 公开名称列表
    :return: 可写入 __init__.py 的文本，以换行结尾
    """
    lines = [ALL_BEGIN, "__all__ = ["]
    lines.extend(f'    "{name}",' for name in names)
    lines.extend(["]", ALL_END, ""])
    return "\n".join(lines)


def replace_all_block(text: str, block: str) -> str:
    """
    用新块替换 __init__.py 中的 __all__ 块，标记不存在时追加到文件末尾。

    :param text: __init__.py 原文
    :param block: render_all_block 的输出
    :return: 替换后的全文
    """
    if ALL_BEGIN in text:
        head, _, rest = text.partition(ALL_BEGIN)
        _, _, tail = rest.partition(ALL_END)
        return head + block + tail.lstrip("\n")
    return text.rstrip("\n") + "\n\n" + block


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
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
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


def main() -> int:
    parser = argparse.ArgumentParser(description="生成接口元数据 registry")
    parser.add_argument(
        "--check", action="store_true", help="仅校验，不写入（供 CI 使用）"
    )
    args = parser.parse_args()
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    init_path = repo_root / "akshare" / "__init__.py"
    text = build(repo_root)
    init_text = init_path.read_text(encoding="utf-8")
    all_block = render_all_block(collect_all_names(init_path))
    new_init_text = replace_all_block(init_text, all_block)
    if args.check:
        baseline_path = repo_root / BASELINE_RELPATH
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        exports = collect_exports(init_path)
        docs = collect_doc_records(repo_root / "docs" / "data")
        problems = diff_baseline(exports, docs, baseline)
        current = (repo_root / OUTPUT_RELPATH).read_text(encoding="utf-8")
        if current != text:
            problems.append(
                "interfaces.json 与源不同步，请运行 python scripts/build_registry.py"
            )
        if new_init_text != init_text:
            problems.append(
                "__init__.py 的 __all__ 与导入表不同步，"
                "请运行 python scripts/build_registry.py"
            )
        if problems:
            for problem in problems:
                print(f"[registry] {problem}")
            return 1
        print("[registry] 校验通过")
        return 0
    (repo_root / OUTPUT_RELPATH).write_text(text, encoding="utf-8", newline="\n")
    print(f"已写入 {OUTPUT_RELPATH}")
    if new_init_text != init_text:
        init_path.write_text(new_init_text, encoding="utf-8", newline="\n")
        print(
            f"已更新 {init_path.name} 的 __all__（{len(collect_all_names(init_path))} 项）"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
