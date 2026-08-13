#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/8/13
Desc: 中英文标点规范检查与修复工具

规范：中文正文统一使用全角标点（，。；：？！（）“”、）；纯英文语境保持半角。

可修改范围经过严格限定，这是本脚本的核心设计：
    - .py 只处理 docstring 与 # 注释，其余字符串常量一律跳过。原因是中文列名
      （"持股数（万股）"）、用户可传参数值（indicator="申购费率（前端）"）以及
      解析上游文本的字面量（如 .split 的分隔符）里的标点属于数据或对外契约，改动会
      直接破坏接口与用户代码。
    - .md 跳过围栏代码块（接口示例 / 数据示例）、行内代码、链接与图片、HTML
      标签、裸 URL，这些位置的内容是真实输出或代码，不是正文。
    - 引号内的内容一并保护，避免改坏注释里引用的正则与字段名。

用法：
    python scripts/check_punctuation.py                 # 检查全仓库，只报告
    python scripts/check_punctuation.py --fix           # 就地修复
    python scripts/check_punctuation.py --selftest      # 运行内置用例
    python scripts/check_punctuation.py a.py docs/b.md  # 只处理指定文件

注意：修改 docs/data 下的文档后必须重新生成接口元数据，否则 CI 的 registry-check
会因 interfaces.json 不同步而失败：
    python scripts/build_registry.py
"""

import argparse
import ast
import io
import pathlib
import re
import tokenize
from typing import List, Optional, Tuple

# ---------------------------------------------------------------- 字符类定义

# 中日韩统一表意文字，用于判定「左邻是否为中文」
CJK = "一-鿿㐀-䶿豈-﫿"
# 中文语境标志：汉字加已有的全角标点，全角标点右侧同样属于中文语境
CTX = CJK + "，。；：？！、（）【】“”‘’《》…—"

# 半角 -> 全角映射
SIMPLE_MAP = {",": "，", ";": "；", ":": "：", "!": "！", "?": "？"}

# 该行是否含汉字，用于判定「这行是不是中文正文」
HAS_CJK_RE = re.compile(rf"[{CJK}]")
# 不含汉字却出现中文标点，属于英文语境误用。只报告不自动改：极少数情况下，
# 中文段落折行后某一行可能确实只剩标点与英文，需要人工判断。
CJK_PUNCT_IN_ASCII_RE = re.compile(r"[，。；、？！]")

# 左邻为中文语境的半角标点，连同其后的空白一起吃掉
SIMPLE_RE = re.compile(rf"(?<=[{CTX}])([,;:!?])[ \t]*")
# 右邻为汉字时也应转换，覆盖 "0.5, 小于 1" 这类左邻是数字或引号的情况。
# 只对 "," 与 ";" 生效：若放开到 ":"，会把 ":param x: 股票代码" 的 RST 字段
# 冒号一并改成全角，直接破坏 docstring 语法。
RIGHT_CJK_RE = re.compile(rf"([,;])[ \t]*(?=[{CJK}])")
# 句末点号：左邻必须是汉字，右侧必须是空白或行尾，避免误伤 1.18.85 / ak.func / U.S.
PERIOD_RE = re.compile(rf"(?<=[{CJK}])\.(?=[ \t]|$)")
# 中文括号：左邻为中文语境，括号内至少含一个汉字且不嵌套
PAREN_RE = re.compile(rf"(?<=[{CTX}])\(([^()\n]*[{CJK}][^()\n]*)\)")
# 全角标点后的多余空白，表格右侧的对齐填充不动
TRAILING_SPACE_RE = re.compile(r"([，。；：！？、])[ \t]+(?=[^\s|])")
# 方向错误的中文引号：”内容” 应为 “内容”。汉字属于 \w，因此不能用 (?<!\w)
# 做守卫，改为只在整行不含左引号时才修，避免误伤 “公司”或“本公司” 这类正确文本。
WRONG_QUOTE_RE = re.compile(r"”([^”“\n]{1,60})”")
# ASCII 两侧夹着的全角冒号属于英文语境误用，例如 format: YYYY-MM-DD。
# 允许中间有空白，否则 "format： YYYYMMDD" 这类写法在本轮匹配不上，要等空白被
# TRAILING_SPACE_RE 压掉后的下一轮才命中。
ASCII_COLON_RE = re.compile(r"(?<=[A-Za-z0-9])：[ \t]*(?=[A-Za-z0-9\"'/])")
# 括号左右全角半角不配对，只报告不自动修复，需人工判断
MISMATCH_PAREN_RE = re.compile(r"（[^（）\n]*\)|\([^()\n]*）")

# 需要保护的片段，顺序敏感：先行内代码，再链接，再标签，最后裸 URL 与引号
PROTECT_MD = [
    re.compile(r"`[^`\n]*`"),
    re.compile(r"!?\[[^\]\n]*\]\([^)\n]*\)"),
    re.compile(r"<[^>\n]+>"),
    re.compile(r"https?://\S+"),
    re.compile(r"\"[^\"\n]*\""),
]
PROTECT_PY = [
    re.compile(r"https?://\S+"),
    re.compile(r"\"[^\"\n]*\""),
    # 前后不得紧邻字母，否则英文撇号（Institute's / don't）会被当成引号起点，
    # 把后面整段正文都掩掉，导致该段标点被静默跳过。
    re.compile(r"(?<![A-Za-z])'[^'\n]*'(?![A-Za-z])"),
]

# 单行迭代到不动点的最大轮数，正常两三轮即收敛，这里只作为死循环的兜底
MAX_PASSES = 8

FENCE_RE = re.compile(r"^\s*(```|~~~)")
# 拆出字符串常量的前缀、引号分隔符与正文。必须把分隔符排除在转换范围外，否则
# 单行 docstring 的 \"\"\" 会被引号保护规则自己配成一对，把整段正文掩掉不做转换。
STRING_SPLIT_RE = re.compile(r"^([A-Za-z]*)('''|\"\"\"|'|\")(.*)\2$", re.S)


# ---------------------------------------------------------------- 掩码与转换


def _mask(text: str, patterns: List[re.Pattern]) -> Tuple[str, List[str]]:
    """
    把受保护片段替换为占位符，使其不参与标点转换。

    :param text: 单行文本
    :param patterns: 受保护片段的正则列表
    :return: 掩码后的文本与被抽出的原文列表
    """
    store: List[str] = []

    def repl(match: re.Match) -> str:
        store.append(match.group())
        return f"\x00{len(store) - 1}\x00"

    for pattern in patterns:
        text = pattern.sub(repl, text)
    return text, store


def _unmask(text: str, store: List[str]) -> str:
    """
    还原被掩码的片段。

    :param text: 掩码后的文本
    :param store: 被抽出的原文列表
    :return: 还原后的文本
    """
    # 必须逆序还原。后一个 pattern 可能掩掉一段本身已含前一个占位符的文本
    # （例如 [`code`](url) 先掩行内代码，再整体掩链接），顺序还原会让内层占位符
    # 永久留在结果里，把 NUL 字节写进源文件。
    for index in range(len(store) - 1, -1, -1):
        text = text.replace(f"\x00{index}\x00", store[index])
    return text


def _apply_rules(line: str) -> str:
    """
    对已掩码的单行文本套用一轮标点规则。

    :param line: 已掩码的单行文本
    :return: 套用一轮后的文本
    """
    line = line.replace("　", " ")
    if "“" not in line:
        line = WRONG_QUOTE_RE.sub(r"“\1”", line)
    # 这条是全角改半角，对纯英文行同样要生效，因此不受下面的中文行闸门约束
    line = ASCII_COLON_RE.sub(": ", line)
    # 半角改全角的规则只对含汉字的行生效。CTX 里包含 “”，而英文同样使用弯引号，
    # 不设这道闸门就会把英文参考文献的 '”, by Rui Da' 改成 '”，by Rui Da'。
    # PERIOD_RE / PAREN_RE / RIGHT_CJK_RE 自身已要求汉字相邻，一并放在闸门内更清晰。
    if HAS_CJK_RE.search(line):
        line = SIMPLE_RE.sub(lambda m: SIMPLE_MAP[m.group(1)], line)
        line = RIGHT_CJK_RE.sub(lambda m: SIMPLE_MAP[m.group(1)], line)
        line = PERIOD_RE.sub("。", line)
        line = PAREN_RE.sub(r"（\1）", line)
    return TRAILING_SPACE_RE.sub(r"\1", line)


def convert_line(line: str, markdown: bool = False) -> str:
    """
    转换单行正文的标点。

    :param line: 单行文本，不含换行符
    :param markdown: 是否按 Markdown 规则保护片段
    :return: 转换后的文本
    """
    # CRLF 文件按 "\n" 切分后每行尾部残留 "\r"，会让 PERIOD_RE 的行尾断言失效，
    # 句末点号被静默跳过。先摘掉再原样接回，保持原有行尾风格不变。
    suffix = ""
    if line.endswith("\r"):
        line, suffix = line[:-1], "\r"
    line, store = _mask(line, PROTECT_MD if markdown else PROTECT_PY)
    # 迭代到不动点。规则之间存在依赖：括号规则先把 "(元/份)" 变成 "（元/份）",
    # 其后的逗号才满足「左邻是中文语境」的条件，而逗号规则本轮已经跑过了。单轮
    # 处理会留下一批需要再跑一次才收敛的残留，也就是工具本身不幂等。
    for _ in range(MAX_PASSES):
        updated = _apply_rules(line)
        if updated == line:
            break
        line = updated
    return _unmask(line, store) + suffix


def convert_block(text: str, markdown: bool = False) -> str:
    """
    逐行转换一段文本，保留原有换行。

    :param text: 可含换行的文本
    :param markdown: 是否按 Markdown 规则保护片段
    :return: 转换后的文本
    """
    return "\n".join(convert_line(line, markdown) for line in text.split("\n"))


# ---------------------------------------------------------------- Python 文件


def editable_spans(source: str) -> List[Tuple[int, int, bool]]:
    """
    定位 .py 中允许修改的字符区间，即 docstring 与 # 注释。

    :param source: 源码文本
    :return: 按起点升序排列的 (start, end, is_string) 三元组列表
    """
    # 按 "\n" 切分而非 splitlines(): 后者还会在 \x0b \x0c   等处断行，与
    # tokenize 只按 \n 计行的口径不一致，一旦正文里出现这些字符就会整体错位。
    offsets = [0]
    for part in source.split("\n"):
        offsets.append(offsets[-1] + len(part) + 1)

    def pos(lineno: int, col: int) -> int:
        return offsets[lineno - 1] + col

    spans: List[Tuple[int, int, bool]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    # 只从 ast 取 docstring 的起始行号。ast 的 col_offset 是 UTF-8 字节偏移，
    # 而 tokenize 给的是字符偏移，两者混用会让含中文的单行 docstring
    # （"""中文说明"""）算出错误的结束位置并截断源码，因此精确区间一律取自 tokenize。
    doc_rows = set()
    for node in ast.walk(tree):
        if not isinstance(
            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            continue
        if ast.get_docstring(node, clean=False) is None:
            continue
        # 同时登记 Expr 与其字符串常量的行号。docstring 被括号包起来时
        # （akshare/cal/rv.py 就是这样写的），Expr 的行号指向 "(" 所在行，而
        # tokenize 的字符串 token 在下一行，只登记前者会让整个 docstring 漏掉。
        doc_rows.add(node.body[0].lineno)
        doc_rows.add(node.body[0].value.lineno)
    try:
        for token in tokenize.generate_tokens(io.StringIO(source, newline="").readline):
            if token.type == tokenize.COMMENT or (
                token.type == tokenize.STRING and token.start[0] in doc_rows
            ):
                spans.append(
                    (
                        pos(token.start[0], token.start[1]),
                        pos(token.end[0], token.end[1]),
                        token.type == tokenize.STRING,
                    )
                )
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return []
    return sorted(spans)


def process_python(source: str) -> str:
    """
    只在 docstring 与注释区间内做标点转换。

    :param source: 源码文本
    :return: 转换后的源码
    """
    spans = editable_spans(source)
    for start, end, is_string in reversed(spans):
        chunk = source[start:end]
        match = STRING_SPLIT_RE.match(chunk) if is_string else None
        if match:
            prefix, quote, body = match.group(1), match.group(2), match.group(3)
            chunk = prefix + quote + convert_block(body) + quote
        else:
            chunk = convert_block(chunk)
        source = source[:start] + chunk + source[end:]
    return source


# ---------------------------------------------------------------- Markdown


def process_markdown(text: str) -> str:
    """
    转换 Markdown 正文，跳过围栏代码块。

    :param text: 文档文本
    :return: 转换后的文本
    """
    out: List[str] = []
    fence: Optional[str] = None
    for line in text.split("\n"):
        marker = FENCE_RE.match(line)
        if fence is None and marker:
            fence = marker.group(1)
            out.append(line)
            continue
        if fence is not None:
            out.append(line)
            if marker and marker.group(1) == fence:
                fence = None
            continue
        out.append(convert_line(line, markdown=True))
    return "\n".join(out)


# ---------------------------------------------------------------- 报告与入口


def _ascii_line_warnings(label: str, lineno: int, raw: str) -> List[str]:
    """
    报告不含汉字却使用了中文标点的行，属于英文语境误用。

    是否算中文行必须看未掩码的原文：表格里 symbol="上证系列指数"；choice of {...}
    这类写法的汉字全在引号内，掩码后整行看起来就是纯英文，会被误判。而标点则要在
    掩码后的文本里找，避免把行内代码与 URL 里的字符算进来。

    :param label: 用于展示的文件名
    :param lineno: 行号
    :param raw: 未掩码的单行原文
    :return: 告警文本列表
    """
    if HAS_CJK_RE.search(raw):
        return []
    masked, _ = _mask(raw, PROTECT_MD)
    hits = CJK_PUNCT_IN_ASCII_RE.findall(masked)
    if not hits:
        return []
    return [f"{label}:{lineno}: 英文语境使用了中文标点 {''.join(sorted(set(hits)))}"]


def warnings_for(label: str, text: str, markdown: bool) -> List[str]:
    """
    收集不自动修复但需人工确认的问题。

    检查必须按区间进行，否则会把 Python 语法的 "(" 与字符串内的 "）" 配成一对，
    产出大量误报；Markdown 侧同理必须跳过围栏块，那里的不配对来自上游真实输出。

    :param label: 用于展示的文件名
    :param text: 文件文本
    :param markdown: 是否为 Markdown
    :return: 告警文本列表
    """
    found: List[str] = []
    prose: List[str] = []
    if markdown:
        fence: Optional[str] = None
        for lineno, line in enumerate(text.split("\n"), 1):
            marker = FENCE_RE.match(line)
            if fence is None and marker:
                fence = marker.group(1)
                continue
            if fence is not None:
                if marker and marker.group(1) == fence:
                    fence = None
                continue
            prose.append(line)
            # 先掩掉行内代码与链接，否则正文里的 `f(indicator="费率（前端）")`
            # 会被把 Python 的 "(" 和字符串内的 "）" 配成一对而误报。
            masked, _ = _mask(line, PROTECT_MD)
            for match in MISMATCH_PAREN_RE.finditer(masked):
                found.append(f"{label}:{lineno}: 括号全角半角不配对 -> {match.group()}")
            found.extend(_ascii_line_warnings(label, lineno, line))
    else:
        # 逐个 token 检查，每个字符串常量与注释各自独立成为一个检查单元
        try:
            for token in tokenize.generate_tokens(io.StringIO(text).readline):
                if token.type not in (tokenize.STRING, tokenize.COMMENT):
                    continue
                prose.append(token.string)
                for match in MISMATCH_PAREN_RE.finditer(token.string):
                    found.append(
                        f"{label}:{token.start[0]}: 括号全角半角不配对 -> {match.group()}"
                    )
        except (tokenize.TokenError, IndentationError, SyntaxError):
            return found
        # 英文语境误用只在 docstring 与注释里报。代码字符串里的中文标点通常是数据，
        # 例如 registry.py 的 re.compile(r"[\s,，、;；/|]+") 与 "、".join(...),
        # 以及各模块用来解析上游文本的 .strip("。）")，报出来只会是噪声。
        lines = text.split("\n")
        offsets = [0]
        for part in lines:
            offsets.append(offsets[-1] + len(part) + 1)
        for start, end, _ in editable_spans(text):
            first = next(i for i in range(len(lines)) if offsets[i + 1] > start)
            for extra, part in enumerate(text[start:end].split("\n")):
                found.extend(_ascii_line_warnings(label, first + 1 + extra, part))
    body = "\n".join(prose)
    if body.count("“") != body.count("”"):
        found.append(
            f"{label}: 中文引号数量不配平 “={body.count('“')} ”={body.count('”')}"
        )
    return found


def iter_targets(paths: List[str]) -> List[pathlib.Path]:
    """
    展开待处理的文件列表。

    :param paths: 命令行给出的路径，为空则扫描 akshare 与 docs
    :return: 文件路径列表
    """
    root = pathlib.Path(__file__).resolve().parent.parent
    candidates: List[pathlib.Path] = []
    if paths:
        for item in paths:
            target = pathlib.Path(item)
            if target.is_dir():
                candidates.extend(sorted(target.rglob("*.py")))
                candidates.extend(sorted(target.rglob("*.md")))
            else:
                candidates.append(target)
    else:
        candidates = sorted((root / "akshare").rglob("*.py")) + sorted(
            (root / "docs").rglob("*.md")
        )
    result = []
    for item in candidates:
        if item.suffix not in {".py", ".md"}:
            continue
        result.append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="中英文标点规范检查与修复")
    parser.add_argument("paths", nargs="*", help="待处理文件, 缺省为 akshare 与 docs")
    parser.add_argument("--fix", action="store_true", help="就地修复")
    parser.add_argument("--selftest", action="store_true", help="运行内置用例")
    parser.add_argument("--quiet", action="store_true", help="只输出汇总")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    root = pathlib.Path(__file__).resolve().parent.parent
    changed: List[pathlib.Path] = []
    warns: List[str] = []
    touched_doc_data = False
    for path in iter_targets(args.paths):
        try:
            label = path.resolve().relative_to(root).as_posix()
        except ValueError:
            label = path.as_posix()
        # 必须用 newline="" 读写。默认的通用换行会把 CRLF 读成 LF，写回时便把
        # 整个文件的行尾从 CRLF 改成 LF（本仓库 core.autocrlf=true，工作区是
        # CRLF），造成与标点无关的全文件改动。这里用 open() 而非 Path.read_text
        # 的 newline 参数，后者要到 Python 3.13 才有，本仓库下限是 3.9。
        with open(path, encoding="utf-8", newline="") as handle:
            original = handle.read()
        markdown = path.suffix == ".md"
        updated = process_markdown(original) if markdown else process_python(original)
        warns.extend(warnings_for(label, updated, markdown))
        if updated == original:
            continue
        changed.append(path)
        if label.startswith("docs/data/"):
            touched_doc_data = True
        if args.fix:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(updated)
        elif not args.quiet:
            for lineno, (before, after) in enumerate(
                zip(original.split("\n"), updated.split("\n")), 1
            ):
                if before != after:
                    print(
                        f"{label}:{lineno}:\n  - {before.strip()}\n  + {after.strip()}"
                    )

    for item in warns:
        print(f"[warn] {item}")
    verb = "已修复" if args.fix else "待修复"
    print(f"[punct] {verb} {len(changed)} 个文件, 另有 {len(warns)} 条告警")
    if touched_doc_data:
        # docs/data 的正文会被 build_registry.py 逐字写进 akshare/data/interfaces.json,
        # 不重新生成会让 CI 的 registry-check 因字节比对失败。
        print("[punct] docs/data 有改动, 请运行 python scripts/build_registry.py")
    if changed and not args.fix:
        return 1
    return 0


# ---------------------------------------------------------------- 内置用例

# (说明，输入，期望输出，是否 Markdown)
CASES: List[Tuple[str, str, str, bool]] = [
    # --- 应当转换 ---
    ("中文逗号", "日频率更新, 新上的标的", "日频率更新，新上的标的", False),
    ("中文冒号", "描述: 东方财富", "描述：东方财富", True),
    ("中文分号", "分时行情; 该接口", "分时行情；该接口", True),
    ("中文句号", "优先股股票等.", "优先股股票等。", True),
    ("中文括号", "空气质量级别(优、良等)", "空气质量级别（优、良等）", True),
    ("全角空格", "注意　单位", "注意 单位", True),
    ("引号方向", "进行了”平滑”处理", "进行了“平滑”处理", True),
    ("英文语境冒号", "日期 format：YYYY-MM-DD", "日期 format: YYYY-MM-DD", False),
    ("多余空白", "结束日期,   格式", "结束日期，格式", True),
    # --- 必须保持原样 ---
    ("RST 字段", ":param symbol: 股票代码", ":param symbol: 股票代码", False),
    ("RST 返回", ":rtype: pandas.DataFrame", ":rtype: pandas.DataFrame", False),
    ("版本号", "1.18.85 fix: 修复接口", "1.18.85 fix: 修复接口", False),
    ("模块头键", "Desc: 国证指数", "Desc: 国证指数", False),
    (
        "函数调用",
        "请使用 ak.futures_dce_position_rank() 接口",
        "请使用 ak.futures_dce_position_rank() 接口",
        False,
    ),
    ("小数", "百分比大于 0.5, 小于 1", "百分比大于 0.5，小于 1", False),
    ("时间", "每日 10:30 更新", "每日 10:30 更新", True),
    ("数字列表", "可以获取 1, 5, 15 分钟", "可以获取 1, 5, 15 分钟", True),
    (
        "RST 字段后接中文",
        ":param date: 日期 format: YYYY-MM-DD 或 YYYYMMDD",
        ":param date: 日期 format: YYYY-MM-DD 或 YYYYMMDD",
        False,
    ),
    (
        "枚举取值",
        ':param symbol: choice of {"沪深A股", "港股"}',
        ':param symbol: choice of {"沪深A股", "港股"}',
        False,
    ),
    ("正确的成对引号", "称为“展期”或“换仓”。", "称为“展期”或“换仓”。", True),
    # 以下三条是已修 bug 的回归用例
    (
        "嵌套占位符不得泄漏",
        "见 [`ak`](https://a.com) 文档, 说明如下",
        "见 [`ak`](https://a.com) 文档，说明如下",
        True,
    ),
    ("CRLF 行尾句末点号", "优先股股票等.\r", "优先股股票等。\r", True),
    (
        "英文撇号不应掩掉后文",
        "The Institute's 报告收录数据, 说明如下",
        "The Institute's 报告收录数据，说明如下",
        False,
    ),
    (
        "单引号内取值",
        "格式为 '%Y-%m-%d', 默认当天",
        "格式为 '%Y-%m-%d'，默认当天",
        False,
    ),
    # 以下两条依赖别的规则先执行，单轮处理会漏掉
    (
        "括号转换后逗号才成立",
        '分红(元/份), "FFR": 分红发放日',
        '分红（元/份），"FFR": 分红发放日',
        False,
    ),
    (
        "空白压缩后英文冒号才成立",
        "日期 format： YYYYMMDD",
        "日期 format: YYYYMMDD",
        False,
    ),
    # 回归用例：CTX 里含弯引号，缺了中文行闸门就会把英文参考文献的
    # '”, by Rui Da' 改成 '”，by Rui Da'
    (
        "纯英文行不得改动",
        "1. “Uniform Inference on Volatility”, by Rui Da. 2017.",
        "1. “Uniform Inference on Volatility”, by Rui Da. 2017.",
        False,
    ),
    (
        "中英混排行仍需转换",
        "参见 “已实现波动率”, 由 Rui Da 提出",
        "参见 “已实现波动率”，由 Rui Da 提出",
        False,
    ),
    ("有序列表", "1. 在 Terminal 中运行", "1. 在 Terminal 中运行", True),
    (
        "Markdown 链接",
        "在 [currencyscoop](https://currencyscoop.com/) 注册",
        "在 [currencyscoop](https://currencyscoop.com/) 注册",
        True,
    ),
    (
        "行内代码",
        "运行 `python -m akshare` 即可",
        "运行 `python -m akshare` 即可",
        True,
    ),
    (
        "裸 URL",
        "见 https://a.com/x?a=1,b=2 页面",
        "见 https://a.com/x?a=1,b=2 页面",
        True,
    ),
    ("引号内正则", '剥掉 ",，、;；/|" 等标点', '剥掉 ",，、;；/|" 等标点', False),
    ("引号内取值", '格式 "YYYYMMDD", 为空', '格式 "YYYYMMDD"，为空', True),
    ("表格对齐", "| 注意单位: 亿元   |", "| 注意单位：亿元   |", True),
    ("英文句子", "Today is not trading day: x", "Today is not trading day: x", False),
    ("省略号", "返回数据...稍后重试", "返回数据...稍后重试", False),
    ("已是全角", "日频率更新，新上的标的", "日频率更新，新上的标的", False),
]

# 整文件级用例：.py 中的数据字符串绝对不能被改动
PY_CASE = '''#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/1/12
Desc: 国证指数, 含成份股
"""


def demo() -> None:
    """
    某接口-数据, 说明如下
    :param x: 参数, 例如 "600000"
    :return: 数据
    """
    columns = {"lastWbillQty": "昨日仓单量（手）", "diff": "增减（手）"}
    label = "其中：境内法人持股"
    parsed = label.split("：")[0]
    check = "暂时没有数据！"
    fee = "申购费率（前端）"
    # 中文注释, 也要统一
    return columns, parsed, check, fee
'''

PY_EXPECT = '''#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/1/12
Desc: 国证指数，含成份股
"""


def demo() -> None:
    """
    某接口-数据，说明如下
    :param x: 参数，例如 "600000"
    :return: 数据
    """
    columns = {"lastWbillQty": "昨日仓单量（手）", "diff": "增减（手）"}
    label = "其中：境内法人持股"
    parsed = label.split("：")[0]
    check = "暂时没有数据！"
    fee = "申购费率（前端）"
    # 中文注释，也要统一
    return columns, parsed, check, fee
'''

MD_CASE = """#### 标题

描述: 东方财富-数据, 含明细

数据示例

```
名称, 数值
中文, 1.5
```

限量: 单次返回所有数据, 注意单位: 亿元
"""

MD_EXPECT = """#### 标题

描述：东方财富-数据，含明细

数据示例

```
名称, 数值
中文, 1.5
```

限量：单次返回所有数据，注意单位：亿元
"""


# 单行中文 docstring 与 CRLF 行尾的整文件回归用例
PY_CRLF_CASE = (
    "#!/usr/bin/env python\r\n"
    '"""\r\n'
    "Desc: 模块说明, 含中文\r\n"
    '"""\r\n'
    "\r\n"
    "\r\n"
    "def demo() -> None:\r\n"
    '    """某接口-数据, 说明"""\r\n'
    '    label = "其中：境内法人持股"\r\n'
    "    return label  # 尾注, 也要统一\r\n"
)

PY_CRLF_EXPECT = (
    "#!/usr/bin/env python\r\n"
    '"""\r\n'
    "Desc: 模块说明，含中文\r\n"
    '"""\r\n'
    "\r\n"
    "\r\n"
    "def demo() -> None:\r\n"
    '    """某接口-数据，说明"""\r\n'
    '    label = "其中：境内法人持股"\r\n'
    "    return label  # 尾注，也要统一\r\n"
)


def selftest() -> int:
    """
    运行内置用例，覆盖易误伤场景。

    :return: 进程退出码
    """
    failed = 0
    for name, source, expect, markdown in CASES:
        actual = convert_line(source, markdown=markdown)
        if actual != expect:
            failed += 1
            print(
                f"[FAIL] {name}\n  输入: {source}\n  期望: {expect}\n  实际: {actual}"
            )
        if "\x00" in actual:
            failed += 1
            print(f"[FAIL] {name}: 输出残留 NUL 占位符 -> {actual!r}")
        # 幂等性：再跑一遍必须不再变化，否则 --fix 后 --check 仍会报待修复
        again = convert_line(actual, markdown=markdown)
        if again != actual:
            failed += 1
            print(f"[FAIL] {name}: 不幂等\n  一次: {actual}\n  两次: {again}")
    py_actual = process_python(PY_CASE)
    if py_actual != PY_EXPECT:
        failed += 1
        print("[FAIL] 整文件 .py 用例")
        for a, b in zip(PY_EXPECT.split("\n"), py_actual.split("\n")):
            if a != b:
                print(f"  期望: {a}\n  实际: {b}")
    crlf_actual = process_python(PY_CRLF_CASE)
    if crlf_actual != PY_CRLF_EXPECT:
        failed += 1
        print("[FAIL] 单行 docstring 与 CRLF 用例")
        for a, b in zip(PY_CRLF_EXPECT.split("\n"), crlf_actual.split("\n")):
            if a != b:
                print(f"  期望: {a!r}\n  实际: {b!r}")
    md_actual = process_markdown(MD_CASE)
    if md_actual != MD_EXPECT:
        failed += 1
        print("[FAIL] 整文件 .md 用例")
        for a, b in zip(MD_EXPECT.split("\n"), md_actual.split("\n")):
            if a != b:
                print(f"  期望: {a}\n  实际: {b}")
    total = len(CASES) + 3
    print(f"[selftest] {total - failed}/{total} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
