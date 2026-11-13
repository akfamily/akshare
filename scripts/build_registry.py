#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/12
Desc: 构建期脚本，解析 docs/data、akshare/__init__.py 与各接口源码生成接口元数据
"""

import argparse
import ast
import json
import pathlib
import re
from typing import Dict, List, Optional, Set, Tuple


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


# 冒号必须同时容错半角 ":" 与全角 "："。实测拆分前的 docs/data/stock/stock.md 中有 10 个
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


LABEL_RE = re.compile(r"^\(([A-Za-z0-9_]+)\)=\s*$", re.M)


def find_missing_labels(docs_dir: pathlib.Path) -> List[str]:
    """
    找出缺少 MyST 锚点标签的接口条目。

    中文标题生成的锚点是按顺序编号的 #idN，会随前面的标题增减而错位，因此
    每个接口都要在标题前写一行 "(接口名)="，以获得固定锚点 #接口名。

    :param docs_dir: docs/data 目录
    :return: 缺少标签的接口名，按字典序排列
    """
    names, labels = set(), set()
    for path in sorted(docs_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        names.update(match.group(1) for match in BLOCK_RE.finditer(text))
        labels.update(match.group(1) for match in LABEL_RE.finditer(text))
    return sorted(names - labels)


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
    "set_proxies",
    "get_proxies",
    "ProxyContext",
    "set_timeout",
    "get_timeout",
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


def collect_export_targets(init_path: pathlib.Path) -> Dict[str, Tuple[str, str]]:
    """
    静态解析 __init__.py，提取公开数据接口的定义位置。

    与 collect_exports 的区别是同时保留导入时的原名：__init__.py 中用 as
    改名导出的接口，在其模块里仍以原名定义，追踪源码时需要原名。

    :param init_path: akshare/__init__.py 路径
    :return: 接口名 -> (模块路径，模块中的函数名)
    """
    tree = ast.parse(init_path.read_text(encoding="utf-8"))
    targets: Dict[str, Tuple[str, str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if not node.module or not node.module.startswith("akshare."):
            continue
        for alias in node.names:
            name = alias.asname or alias.name
            if name in EXCLUDE:
                continue
            targets[name] = (node.module, alias.name)
    return targets


# 东方财富 push2 系行情服务器：push2、push2his、push2ex、push2delay 及 82.push2 等编号子域。
# 短时间内请求较多时会临时封禁来源 IP（实测约 5 页翻页即触发），而数据中心
# （datacenter-web）、基金、F10 等其他东方财富服务器不受影响。本脚本只依赖标准库、
# 不导入 akshare，因此这里复制 akshare/utils/http.py 中 _PUSH2_HOST 的规则，
# 由 tests/test_build_registry.py 校验两处一致。
PUSH2_HOST_PATTERN = r"(?:\d+\.)?push2(?:his|ex|delay)?\.eastmoney\.com"
# 在源码字符串中查找时，前面不能紧跟字母、数字或连字符，以免把 xpush2 一类的
# 其他主机名误判为 push2；f"https://{n}.push2.eastmoney.com" 这类 f-string
# 被拆出的 ".push2.eastmoney.com/..." 片段也能命中
PUSH2_IN_TEXT_RE = re.compile(rf"(?<![A-Za-z0-9-]){PUSH2_HOST_PATTERN}")
RATE_LIMIT_EASTMONEY_PUSH2 = "eastmoney_push2"
# 沿函数调用追踪辅助函数的最大层数
MAX_CALL_DEPTH = 3


def _module_path(package_parent: pathlib.Path, module: str) -> Optional[pathlib.Path]:
    """模块路径转为源文件路径，找不到时返回 None。"""
    base = package_parent.joinpath(*module.split("."))
    for path in (base.with_suffix(".py"), base / "__init__.py"):
        if path.exists():
            return path
    return None


def _resolve_relative(module: str, is_package: bool, level: int, target: str) -> str:
    """把模块内的相对导入（from .x import y）转为绝对模块路径。"""
    parts = module.split(".")
    if not is_package:
        parts = parts[:-1]
    if level > 1:
        parts = parts[: -(level - 1)]
    return ".".join(parts + ([target] if target else []))


def _strings_hit_push2(node: ast.AST) -> bool:
    """节点（含子节点）中的字符串常量是否含 push2 行情服务器地址。"""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            if PUSH2_IN_TEXT_RE.search(sub.value):
                return True
    return False


class ModuleIndex:
    """
    按需解析 akshare 的模块源码，供静态追踪接口实际请求的服务器。

    只解析源码、不执行任何代码，因此与本脚本其余部分一样只依赖标准库。
    """

    def __init__(self, package_parent: pathlib.Path):
        """
        :param package_parent: akshare 包所在的目录，即仓库根目录
        """
        self.package_parent = package_parent
        self._cache: Dict[str, Optional[Dict]] = {}

    def get(self, module: str) -> Optional[Dict]:
        """
        返回模块的函数定义、导入名与含 push2 地址的模块级常量。

        :param module: 模块路径，如 "akshare.stock.quote.stock_hist_em"
        :return: 含 functions/imports/push2_constants 三个键的 dict，模块不存在时为 None
        """
        if module in self._cache:
            return self._cache[module]
        path = _module_path(self.package_parent, module)
        if path is None:
            self._cache[module] = None
            return None
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        is_package = path.name == "__init__.py"
        functions: Dict[str, ast.AST] = {}
        imports: Dict[str, Tuple[str, str]] = {}
        push2_constants: Set[str] = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions[node.name] = node
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    source = _resolve_relative(
                        module, is_package, node.level, node.module or ""
                    )
                else:
                    source = node.module or ""
                if not source.startswith("akshare"):
                    continue
                for alias in node.names:
                    imports[alias.asname or alias.name] = (source, alias.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value:
                if isinstance(node, ast.Assign):
                    targets = node.targets
                else:
                    targets = [node.target]
                if _strings_hit_push2(node.value):
                    push2_constants.update(
                        t.id for t in targets if isinstance(t, ast.Name)
                    )
        info = {
            "functions": functions,
            "imports": imports,
            "push2_constants": push2_constants,
        }
        self._cache[module] = info
        return info


def _function_body(node: ast.AST) -> List[ast.stmt]:
    """去掉函数开头的文档字符串：文档里写的是网页地址，不是实际请求的地址。"""
    body = list(node.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    return body


def requests_push2(index: ModuleIndex, module: str, func_name: str) -> bool:
    """
    静态判断接口是否请求东方财富 push2 行情服务器。

    检查函数体（不含文档字符串）中的字符串常量与用到的模块级常量，并沿
    函数名调用追踪同模块或从 akshare 导入的辅助函数，最多 MAX_CALL_DEPTH 层。
    通过属性调用（如 obj.method()）发出的请求、运行时才拼出主机名的地址追踪不到。

    :param index: 模块源码索引
    :param module: 接口所在模块
    :param func_name: 模块中的函数名
    :return: 是否请求 push2 行情服务器
    """
    stack = [(module, func_name, 0)]
    seen: Set[Tuple[str, str]] = set()
    while stack:
        mod, name, depth = stack.pop()
        if (mod, name) in seen:
            continue
        seen.add((mod, name))
        info = index.get(mod)
        if info is None:
            continue
        node = info["functions"].get(name)
        if node is None:
            # 名字是从别的模块导入的（含包 __init__.py 的转导出），到定义处继续找
            if name in info["imports"]:
                stack.append((*info["imports"][name], depth))
            continue
        for stmt in _function_body(node):
            if _strings_hit_push2(stmt):
                return True
            for sub in ast.walk(stmt):
                if isinstance(sub, ast.Name) and sub.id in info["push2_constants"]:
                    return True
                if (
                    depth < MAX_CALL_DEPTH
                    and isinstance(sub, ast.Call)
                    and isinstance(sub.func, ast.Name)
                ):
                    stack.append((mod, sub.func.id, depth + 1))
    return False


def collect_rate_limits(repo_root: pathlib.Path) -> Dict[str, Optional[str]]:
    """
    给每个公开数据接口标注它会受到的访问限制。

    目前只识别东方财富 push2 行情服务器，值为 "eastmoney_push2"，其余为 None。

    :param repo_root: 仓库根目录
    :return: 接口名 -> 访问限制标识
    """
    index = ModuleIndex(repo_root)
    targets = collect_export_targets(repo_root / "akshare" / "__init__.py")
    return {
        name: (
            RATE_LIMIT_EASTMONEY_PUSH2
            if requests_push2(index, module, original)
            else None
        )
        for name, (module, original) in targets.items()
    }


ALTERNATIVES_RELPATH = pathlib.Path("scripts") / "registry_alternatives.json"


def resolve_alternatives(
    config: Dict, exports: Dict[str, str]
) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    把人工维护的同类接口对照表展开为「接口名 -> 同类接口列表」。

    对照表记录的是来自不同数据源、内容属于同一类的接口，例如 A 股日线的
    stock_zh_a_hist（东方财富）、stock_zh_a_daily（新浪财经）与
    stock_zh_a_hist_tx（腾讯）。它无法从源码或文档推断，只能人工维护：
    按名称与描述猜测时，会把 ST 股票列表配给日线、把 B 股配给科创板。

    groups 中同一组的接口互为同类；one_way 是单向关系，用于「分市场的实时行情
    可改用全市场接口再自行筛选」这类不对称的情形。同类接口的参数写法与返回列
    通常不同，调用方需要另行查看各自的说明。

    :param config: registry_alternatives.json 的内容，含 groups 与 one_way
    :param exports: 接口名 -> 模块路径，用于校验对照表中的接口名
    :return: (接口名 -> 同类接口列表，问题说明列表)；未导出的接口名不进入结果
    """
    mapping: Dict[str, List[str]] = {}
    problems: List[str] = []

    def add(name: str, others: List[str], where: str) -> None:
        for item in [name, *others]:
            if item not in exports and f"{where}:{item}" not in seen_unknown:
                seen_unknown.add(f"{where}:{item}")
                problems.append(
                    f"registry_alternatives.json 的 {where} 中的 {item} "
                    "不是已导出的接口，请更正或移除"
                )
        if name not in exports:
            return
        target = mapping.setdefault(name, [])
        for other in others:
            if other == name:
                problems.append(
                    f"registry_alternatives.json 的 {where} 中 {name} 不能把自己列为同类接口"
                )
            elif other in exports and other not in target:
                target.append(other)

    seen_unknown: Set[str] = set()
    for position, group in enumerate(config.get("groups", []), start=1):
        if len(group) < 2:
            problems.append(
                f"registry_alternatives.json 的 groups 第 {position} 组至少需要两个接口"
            )
        if len(set(group)) != len(group):
            problems.append(
                f"registry_alternatives.json 的 groups 第 {position} 组有重复的接口"
            )
        for name in dict.fromkeys(group):
            others = [item for item in dict.fromkeys(group) if item != name]
            add(name, others, f"groups 第 {position} 组")
    for name, others in config.get("one_way", {}).items():
        add(name, list(others), f"one_way[{name}]")
    return {name: items for name, items in mapping.items() if items}, problems


def load_alternatives(
    repo_root: pathlib.Path, exports: Dict[str, str]
) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    读取并展开同类接口对照表，文件不存在时视为空表。

    :param repo_root: 仓库根目录
    :param exports: 接口名 -> 模块路径
    :return: 同 resolve_alternatives
    """
    path = repo_root / ALTERNATIVES_RELPATH
    if not path.exists():
        return {}, []
    config = json.loads(path.read_text(encoding="utf-8"))
    return resolve_alternatives(config, exports)


SCHEMA_VERSION = 1


def merge_records(
    exports: Dict[str, str],
    docs: Dict[str, Dict],
    rate_limits: Optional[Dict[str, Optional[str]]] = None,
    alternatives: Optional[Dict[str, List[str]]] = None,
) -> List[Dict]:
    """
    以导出表为主键集合合并文档信息。

    不变量①：结果中的每个 name 都保证可通过 getattr(ak, name) 取到，
    因此文档中存在而代码未导出的条目会被丢弃。

    :param exports: 接口名 -> 模块路径
    :param docs: 接口名 -> 文档元数据
    :param rate_limits: 接口名 -> 访问限制标识，见 collect_rate_limits
    :param alternatives: 接口名 -> 同类接口列表，见 resolve_alternatives
    :return: 按 name 字典序排序的记录列表
    """
    rate_limits = rate_limits or {}
    alternatives = alternatives or {}
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
                "rate_limit": rate_limits.get(name),
                "alternatives": list(alternatives.get(name, [])),
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


def write_if_changed(path: pathlib.Path, text: str) -> bool:
    """
    仅在内容变化时写入，并沿用目标文件现有的行尾风格。

    本仓库在 Windows 上 core.autocrlf=true，工作区文件是 CRLF。若无条件地以 LF
    重写，内容未变的文件也会被 git 标为已修改；pre-commit 钩子每次提交都会运行
    本脚本，于是提交后工作区总残留一个只有行尾差异的 interfaces.json。

    :param path: 目标文件
    :param text: 以 LF 分行的新内容
    :return: 是否实际写入
    """
    if path.exists():
        raw = path.read_bytes()
        if raw.decode("utf-8").replace("\r\n", "\n") == text:
            return False
        newline = "\r\n" if b"\r\n" in raw else "\n"
    else:
        newline = "\n"
    path.write_text(text, encoding="utf-8", newline=newline)
    return True


def build(repo_root: pathlib.Path) -> str:
    """
    生成完整的 registry JSON 文本。

    :param repo_root: 仓库根目录
    :return: JSON 文本
    """
    exports = collect_exports(repo_root / "akshare" / "__init__.py")
    docs = collect_doc_records(repo_root / "docs" / "data")
    alternatives, _ = load_alternatives(repo_root, exports)
    return serialize(
        merge_records(exports, docs, collect_rate_limits(repo_root), alternatives)
    )


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
    # 对照表里出现已删除或写错的接口名时，写入模式也要失败：否则 pre-commit 会
    # 悄悄生成一份丢掉这些条目的 interfaces.json，过期的对照表永远不会被发现
    _, alternative_problems = load_alternatives(repo_root, collect_exports(init_path))
    if alternative_problems and not args.check:
        for problem in alternative_problems:
            print(f"[registry] {problem}")
        return 1
    if args.check:
        baseline_path = repo_root / BASELINE_RELPATH
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        exports = collect_exports(init_path)
        docs = collect_doc_records(repo_root / "docs" / "data")
        problems = diff_baseline(exports, docs, baseline)
        problems.extend(alternative_problems)
        for name in find_missing_labels(repo_root / "docs" / "data"):
            problems.append(
                f"接口 {name} 的文档条目缺少锚点标签，请在其标题前加一行 ({name})="
            )
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
    if write_if_changed(repo_root / OUTPUT_RELPATH, text):
        print(f"已写入 {OUTPUT_RELPATH}")
    else:
        print(f"{OUTPUT_RELPATH} 无变化")
    if write_if_changed(init_path, new_init_text):
        print(
            f"已更新 {init_path.name} 的 __all__（{len(collect_all_names(init_path))} 项）"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
