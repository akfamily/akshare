#!/usr/bin/env python
"""
Date: 2026/10/30
Desc: 接口参数的类型转换
AKShare 的接口参数绝大多数是文本，如 date="20240101"、start_page="1"；少数参数要求数字或
布尔值，如 page、limit。经 HTTP、MCP 或配置文件调用时参数值往往只能是文本，这些接口
因此报错或得到错误结果：page="-1" 不等于 -1，"false" 作为布尔值为真。这里的函数让这些
参数同时接受原生类型与文本。超时统一由 ak.set_timeout 设置，接口不再提供 timeout 参数
"""

from typing import Any

from akshare.exceptions import InvalidParameterError

_TRUE = {"true", "1", "yes", "y", "on"}
_FALSE = {"false", "0", "no", "n", "off"}


def to_int(value: Any, name: str) -> int:
    """
    把整数或整数文本转为 int
    :param value: 参数值，如 5、"5"、"-1"
    :type value: int or str
    :param name: 参数名，用于报错
    :type name: str
    :return: 整数
    :rtype: int
    :raises InvalidParameterError: 值不是整数
    """
    if isinstance(value, bool):
        raise InvalidParameterError(f"参数 {name} 应为整数，收到 {value!r}")
    if isinstance(value, int):
        return value
    try:
        number = float(str(value).strip())
    except ValueError:
        raise InvalidParameterError(f"参数 {name} 应为整数，收到 {value!r}") from None
    if not number.is_integer():
        raise InvalidParameterError(f"参数 {name} 应为整数，收到 {value!r}")
    return int(number)


def to_bool(value: Any, name: str) -> bool:
    """
    把布尔值或 "true"、"false"、"1"、"0" 等文本转为 bool
    :param value: 参数值
    :type value: bool or str
    :param name: 参数名，用于报错
    :type name: str
    :return: 布尔值
    :rtype: bool
    :raises InvalidParameterError: 无法识别的值
    """
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in _TRUE:
        return True
    if text in _FALSE:
        return False
    raise InvalidParameterError(f"参数 {name} 应为 true 或 false，收到 {value!r}")
