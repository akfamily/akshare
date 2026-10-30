#!/usr/bin/env python
"""
Date: 2026/10/30
Desc: 解析上游返回的 JSON 与 JavaScript 对象字面量，替代已停止维护的 demjson
新浪、天天基金、腾讯等数据源常返回 JavaScript 写法而非严格 JSON：键名不加引号、
单引号字符串、数组中的空位、undefined、末尾多余的逗号、十六进制数等。
先按严格 JSON 解析，失败时只改写字符串以外的部分，转成 JSON 后再交给 json.loads。
"""

import json
import re
from typing import Any

from akshare.exceptions import DataParsingError

# 依次匹配：双引号字符串、单引号字符串、数组空位、末尾多余的逗号、注释、十六进制数与裸词。
# 字符串整体匹配后原样保留（单引号字符串转成双引号），因此字符串内部的冒号、逗号、
# 方括号等不会被误改；匹配在正则引擎的 C 层完成，数 MB 的文本也只需零点几秒
_GAP = r"(?:\s|//[^\n]*|/\*.*?\*/)*"  # 空白与注释，判断逗号与空位时需要跳过
_TOKEN = re.compile(
    rf"""
    (?P<dq>"(?:[^"\\]|\\.)*")
  | (?P<sq>'(?:[^'\\]|\\.)*')
  | (?P<hole>(?<=[\[,]){_GAP}(?=,))
  | (?P<trailing>,{_GAP}(?=[\]}}]))
  | (?P<comment>//[^\n]*|/\*.*?\*/)
  | (?P<hex>(?<![\w.$])[-+]?0[xX][0-9a-fA-F]+(?![\w$]))
  | (?P<word>(?<![\w.$])[A-Za-z_$][\w$]*(?![\w$]))
    """,
    re.VERBOSE | re.DOTALL,
)
# 与 JavaScript 一致：只有后面紧跟逗号的位置才是空位，[1,,2] 与 [,1] 含空位，
# 而 [1,] 只是末尾多余的逗号；[1,,] 解析为 [1, None]
_KEY_AFTER = re.compile(r"\s*:")
_SQ_ESCAPE = re.compile(r"\\(.)|\"", re.DOTALL)
# 裸词中只需改写 undefined；true、false、null、NaN、Infinity 本身就能被 json.loads 解析，
# 其余裸词不是合法的值，原样保留，让 json.loads 报出准确位置
_LITERALS = {"undefined": "null"}


def _escape_for_double_quotes(m: re.Match) -> str:
    if m.group(0) == '"':
        return '\\"'
    # 单引号字符串里的 \' 在 JSON 中不是合法转义，还原为 '
    return "'" if m.group(1) == "'" else m.group(0)


def _single_to_double(text: str) -> str:
    return '"' + _SQ_ESCAPE.sub(_escape_for_double_quotes, text[1:-1]) + '"'


def _to_json(text: str) -> str:
    def replace(m: re.Match) -> str:
        kind = m.lastgroup
        value = m.group(0)
        if kind == "dq":
            return value
        if kind == "sq":
            return _single_to_double(value)
        if kind == "comment":
            return ""
        if kind == "hex":
            return str(int(value, 16))
        if kind == "word":
            if _KEY_AFTER.match(text, m.end()):
                return f'"{value}"'
            return _LITERALS.get(value, value)
        if kind == "hole":
            return "null"
        return ""  # trailing

    return _TOKEN.sub(replace, text)


def loads(text: str) -> Any:
    """
    解析 JSON 或 JavaScript 对象字面量
    :param text: 待解析文本
    :type text: str
    :return: 解析结果；undefined 与数组空位解析为 None
    :rtype: Any
    :raises DataParsingError: 无法解析时抛出，附出错位置附近的原文
    """
    if isinstance(text, (bytes, bytearray)):
        text = text.decode("utf-8")
    try:
        return json.loads(text)
    except ValueError:
        pass
    converted = _to_json(text.strip())
    try:
        return json.loads(converted)
    except ValueError as e:
        pos = getattr(e, "pos", 0) or 0
        snippet = converted[max(0, pos - 40) : pos + 40]
        raise DataParsingError(
            f"无法解析上游返回的数据：{e}；附近内容：{snippet!r}"
        ) from e
