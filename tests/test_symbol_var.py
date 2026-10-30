#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: chinese_to_english 品种映射与上期所仓单解析测试

chinese_to_english 由两个按位置一一对应的列表组成，只能在末尾成对追加；
2026-10 上期所仓单页面新增了 20 号胶的仓库与厂库两张表，映射里没有这两个名称，
get_receipt 因此对所有含上期所品种的调用报 ValueError: list.index(x): x not in list。
全程不联网。
"""

import ast
import pathlib
import warnings

import pandas as pd
import pytest

from akshare.futures.symbol_var import chinese_to_english

SYMBOL_VAR = (
    pathlib.Path(__file__).resolve().parent.parent
    / "akshare"
    / "futures"
    / "symbol_var.py"
)


def _lists():
    tree = ast.parse(SYMBOL_VAR.read_text(encoding="utf-8"))
    func = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "chinese_to_english"
    )
    return {
        n.targets[0].id: [ast.literal_eval(e) for e in n.value.elts]
        for n in ast.walk(func)
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.List)
    }


def test_lists_stay_aligned():
    lists = _lists()
    assert len(lists["chinese_list"]) == len(lists["english_list"])


@pytest.mark.parametrize(
    "name, code",
    [
        ("20号胶(仓库)", "NR"),
        ("20号胶(厂库)", "NR"),
        ("20号胶", "NR"),
        ("铜", "CU"),
        ("丁二烯橡胶(厂库)", "BR"),
    ],
)
def test_known_names(name, code):
    assert chinese_to_english(name) == code


def _table(name: str, total: int) -> pd.DataFrame:
    return pd.DataFrame([["地区", name, "", ""], ["总计", "总计", total, 0]])


def test_shfe_receipt_skips_unknown_variety(monkeypatch):
    from akshare.futures import futures_receipt

    tables = [
        pd.DataFrame(),
        _table("铜", 100),
        _table("某新品种", 5),
        _table("20号胶(仓库)", 7),
    ]

    class FakeResponse:
        text = ""

    monkeypatch.setattr(futures_receipt.http, "get", lambda *a, **k: FakeResponse())
    monkeypatch.setattr(futures_receipt.pd, "read_html", lambda *a, **k: tables)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        df = futures_receipt.get_shfe_receipt_3(date="20261028", vars_list=["CU", "NR"])
    assert dict(zip(df["var"], df["receipt"])) == {"CU": 100, "NR": 7}
    assert any("某新品种" in str(w.message) for w in caught)


def test_option_comm_info_parses_update_times(monkeypatch):
    """九期网把“手续费更新时间”改为“期权手续费更新时间”后，原先用 strip 去前缀会残留文字"""
    from akshare.option import option_comm_qihuo

    html = (
        "<div>（期权手续费更新时间：2026-10-30 00:50:17.461，"
        "价格更新时间：2026-10-30 15:00:06.774。）<a id='dlink'></a></div>"
        "<table><tr><td>广州期货交易所</td></tr><tr><td>期权品种</td></tr>"
        "<tr><td>期权品种</td><td>现价</td><td>成交量</td><td>每跳毛利/元</td><td>每跳净利/元</td></tr>"
        "<tr><td>工业硅期权</td><td>1</td><td>114</td><td>5</td><td>2.9</td></tr></table>"
    )
    symbols = pd.DataFrame({"品种名称": ["工业硅期权"], "品种代码": ["si_o"]})
    monkeypatch.setattr(option_comm_qihuo, "option_comm_symbol", lambda: symbols)
    monkeypatch.setattr(
        option_comm_qihuo, "_option_comm_page", lambda params=None: html
    )
    df = option_comm_qihuo.option_comm_info(symbol="工业硅期权")
    assert df["手续费更新时间"].iloc[0] == "2026-10-30 00:50:17.461"
    assert df["价格更新时间"].iloc[0] == "2026-10-30 15:00:06.774"
    assert df["交易所"].iloc[0] == "广州期货交易所"
