#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/15
Desc: 所有数据接口都返回 pandas.DataFrame 的守卫测试

AKTools 的 HTTP 与 MCP 服务把接口的返回值当作表格处理；1.20.65 之前有 13 个接口返回字符串、
列表、元组或字典，另有 4 个在非交易日返回 None。全程不联网。
"""

import ast
import inspect
import textwrap

import pandas as pd
import pytest

import akshare as ak
from akshare import registry
from akshare.exceptions import APIError
from akshare.futures import futures_cot, futures_roll_yield, futures_zh_sina
from akshare.index import index_zh_em
from akshare.option import option_commodity

INTERFACES = sorted(item["name"] for item in registry._load()["interfaces"])
# 不属于表格的 return：没有返回值、常量、字典、列表、元组、集合、f-string
_NOT_A_TABLE = (ast.Constant, ast.Dict, ast.List, ast.Tuple, ast.Set, ast.JoinedStr)


def _bad_returns(func) -> list:
    """函数体里明显不是表格的 return 语句，嵌套函数不算"""
    tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
    found = []

    def visit(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                continue
            if isinstance(child, ast.Return) and (
                child.value is None or isinstance(child.value, _NOT_A_TABLE)
            ):
                found.append(ast.unparse(child))
            visit(child)

    visit(tree.body[0])
    return found


def test_every_interface_is_annotated_as_dataframe():
    wrong = [
        name
        for name in INTERFACES
        if inspect.signature(getattr(ak, name)).return_annotation is not pd.DataFrame
    ]
    assert wrong == [], f"返回值注解不是 pd.DataFrame 的接口: {wrong}"


def test_no_interface_returns_a_literal():
    wrong = {
        name: bad
        for name in INTERFACES
        if (bad := _bad_returns(inspect.unwrap(getattr(ak, name))))
    }
    assert wrong == {}, f"函数体里返回了非表格的值: {wrong}"


def test_stock_a_code_to_symbol():
    """工具函数，仍返回字符串（常用于 Series.apply），因此不登记为数据接口"""
    assert ak.stock_a_code_to_symbol("600000") == "sh600000"
    assert ak.stock_a_code_to_symbol("000001") == "sz000001"
    assert ak.stock_a_code_to_symbol("920000") == "bj920000"
    assert ak.stock_a_code_to_symbol("830001") == "bj830001"
    assert "stock_a_code_to_symbol" not in INTERFACES
    assert "stock_a_code_to_symbol" in ak.__all__


def test_futures_main_contract_sina_splits_the_text(monkeypatch):
    monkeypatch.setattr(
        futures_zh_sina, "_futures_main_contract_text", lambda symbol: "IF2612,IC2612"
    )
    df = ak.futures_main_contract_sina(symbol="cffex")
    assert df["合约"].tolist() == ["IF2612", "IC2612"]
    monkeypatch.setattr(
        futures_zh_sina, "_futures_main_contract_text", lambda symbol: ""
    )
    empty = ak.futures_main_contract_sina(symbol="cffex")
    assert empty.empty and list(empty.columns) == ["合约"]


def test_index_code_id_map_em(monkeypatch):
    monkeypatch.setattr(
        index_zh_em, "_index_code_id_map", lambda: {"000001": 0, "600000": 1}
    )
    df = ak.index_code_id_map_em()
    assert df.to_dict("list") == {"代码": ["000001", "600000"], "市场代码": [0, 1]}


@pytest.mark.parametrize("result", [None, False])
def test_futures_roll_yield_without_data_is_an_empty_frame(monkeypatch, result):
    monkeypatch.setattr(
        futures_roll_yield, "_futures_roll_yield", lambda **kwargs: result
    )
    df = ak.futures_roll_yield(date="20261114", symbol="RB")
    assert df.empty and list(df.columns) == ["roll_yield", "near_by", "deferred"]


def test_futures_roll_yield_row(monkeypatch):
    monkeypatch.setattr(
        futures_roll_yield,
        "_futures_roll_yield",
        lambda **kwargs: (-0.002, "RB2701", "RB2705"),
    )
    df = ak.futures_roll_yield(date="20261113", symbol="RB")
    assert df.iloc[0].tolist() == [-0.002, "RB2701", "RB2705"]


def test_futures_rank_sum_non_trading_day_and_failure(monkeypatch):
    monkeypatch.setattr(futures_cot, "_futures_rank_sum", lambda **kwargs: None)
    df = ak.futures_rank_sum(date="20261114", symbols="RB")
    assert df.empty and list(df.columns) == futures_cot.RANK_SUM_COLUMNS
    assert len(futures_cot.RANK_SUM_COLUMNS) == 27
    monkeypatch.setattr(futures_cot, "_futures_rank_sum", lambda **kwargs: False)
    with pytest.raises(APIError):
        ak.futures_rank_sum(date="20261113", symbols="RB")


def test_non_trading_day_returns_an_empty_frame(monkeypatch):
    """非交易日在发出任何请求之前就返回空表"""

    def no_network(*args, **kwargs):
        raise AssertionError("不应发出请求")

    monkeypatch.setattr(option_commodity.http, "post", no_network)
    with pytest.warns(UserWarning, match="非交易日"):
        vol = ak.option_vol_gfex(symbol="碳酸锂", date="20261114")
    assert vol.empty and list(vol.columns) == ["合约系列", "隐含波动率"]
    monkeypatch.setattr(futures_cot.http, "post", no_network)
    with pytest.warns(UserWarning, match="非交易日"):
        rank = ak.futures_position_rank_other_dce(date="20261114")
    assert rank.empty and list(rank.columns) == futures_cot.cons.RANK_TABLE_COLUMNS
