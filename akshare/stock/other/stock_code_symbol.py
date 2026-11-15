#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 18:00
Desc: 股票代码工具-为沪深股票代码加上市场前缀
"""


def stock_a_code_to_symbol(symbol: str = "000300") -> str:
    """
    按股票代码的开头判断所属市场，返回带市场标识的代码；本地计算，不联网
    :param symbol: 股票代码
    :type symbol: str
    :return: 带市场标识的代码，如 sh600000
    :rtype: str
    """
    if symbol.startswith("6") or symbol.startswith("900"):
        market = "sh"
    elif symbol.startswith(("4", "8", "92")):
        market = "bj"
    else:
        market = "sz"
    return f"{market}{symbol}"


if __name__ == "__main__":
    stock_a_code_to_symbol_str = stock_a_code_to_symbol(symbol="000300")
    print(stock_a_code_to_symbol_str)
