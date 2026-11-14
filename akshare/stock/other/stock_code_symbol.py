#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 18:00
Desc: 股票代码工具-为沪深股票代码加上市场前缀
"""


def stock_a_code_to_symbol(symbol: str = "000300") -> str:
    """
    输入股票代码判断股票市场
    :param symbol: 股票代码
    :type symbol: str
    :return: 股票市场
    :rtype: str
    """
    if symbol.startswith("6") or symbol.startswith("900"):
        return f"sh{symbol}"
    else:
        return f"sz{symbol}"


if __name__ == "__main__":
    stock_a_code_to_symbol_str = stock_a_code_to_symbol(symbol="000300")
    print(stock_a_code_to_symbol_str)
