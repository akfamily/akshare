#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14
Desc: 旧接口名的去向提示

接口改名或移除后，调用旧名称应当告诉用户新名称或移除的版本，而不是只报
“没有这个属性”。对照数据 akshare/data/renames.json 由 scripts/build_registry.py
根据更新日志的接口更名一览表与 scripts/registry_removed.json 生成，全程不联网。
"""

import pytest
from build_registry import build_renames

import akshare as ak
from akshare import registry
from akshare.exceptions import InvalidParameterError

TABLE = """
| 1.20.46      | stock_zh_a_hist   | stock_zh_a_hist_em | 20261114 |
| 1.20.31      | get_a             | futures_a          | 20261105 |
| 1.20.44      | futures_a         | futures_a_sina     | 20261114 |
| 1.20.48      | currency_latest   | fx_latest_scoop    | 20261114 |
| 1.4.86       | very_old          | long_gone          | 20200101 |
"""
EXPORTS = {"stock_zh_a_hist_em": "m", "futures_a_sina": "m"}
REMOVED = {"fx_latest_scoop": "1.20.52", "index_yw": "1.20.54"}


def test_build_renames_follows_chain_to_final_name():
    data, problems = build_renames(TABLE, REMOVED, EXPORTS)
    assert problems == []
    assert data["renamed"]["stock_zh_a_hist"] == ["stock_zh_a_hist_em", "1.20.46"]
    # 两次改名的旧名指向最终名称，版本取它自己被改名的那一版
    assert data["renamed"]["get_a"] == ["futures_a_sina", "1.20.31"]
    assert data["renamed"]["futures_a"] == ["futures_a_sina", "1.20.44"]


def test_build_renames_treats_renamed_then_removed_as_removed():
    data, _ = build_renames(TABLE, REMOVED, EXPORTS)
    assert "currency_latest" not in data["renamed"]
    assert data["removed"]["currency_latest"] == "1.20.52"
    assert data["removed"]["index_yw"] == "1.20.54"


def test_build_renames_skips_history_whose_target_is_unknown():
    # 新名称既不存在也不在已移除名单里，说不清去向，不给提示
    data, _ = build_renames(TABLE, REMOVED, EXPORTS)
    assert "very_old" not in data["renamed"]
    assert "very_old" not in data["removed"]


def test_build_renames_rejects_removed_name_that_still_exists():
    _, problems = build_renames(TABLE, {"futures_a_sina": "1.20.50"}, EXPORTS)
    assert problems and "futures_a_sina" in problems[0]


def test_old_name_tells_the_new_name():
    with pytest.raises(AttributeError) as error:
        ak.stock_zh_a_hist
    message = str(error.value)
    assert "stock_zh_a_hist_em" in message
    assert "1.20.46" in message


def test_removed_name_tells_the_version():
    with pytest.raises(AttributeError) as error:
        ak.index_yw
    assert "1.20.54" in str(error.value)
    assert "移除" in str(error.value)


def test_typo_suggests_close_names():
    with pytest.raises(AttributeError) as error:
        ak.stock_zh_a_hist_emm
    assert "stock_zh_a_hist_em" in str(error.value)


def test_hasattr_and_private_names_keep_working():
    assert not hasattr(ak, "stock_zh_a_hist")
    assert not hasattr(ak, "__wrapped__")
    assert hasattr(ak, "stock_zh_a_hist_em")


def test_interface_info_reports_rename():
    with pytest.raises(InvalidParameterError) as error:
        ak.interface_info("stock_zh_a_daily")
    assert "stock_zh_a_hist_sina" in str(error.value)


def test_every_rename_target_is_a_real_interface():
    registry.renamed_hint("x")
    names = {item["name"] for item in registry._load()["interfaces"]}
    renamed = registry._RENAMES["renamed"]
    assert len(renamed) > 300
    assert all(new in names for new, _ in renamed.values())
    assert not set(renamed) & names
    assert not set(registry._RENAMES["removed"]) & names


def test_renamed_info_returns_structured_data():
    info = ak.renamed_info("stock_zh_a_hist")
    assert info == {
        "name": "stock_zh_a_hist",
        "status": "renamed",
        "new_name": "stock_zh_a_hist_em",
        "version": "1.20.46",
        "url": registry.RENAME_TABLE_URL,
    }
    removed = ak.renamed_info("index_yw")
    assert removed["status"] == "removed" and removed["version"] == "1.20.54"
    assert removed["url"].endswith("#v1-20-54") and "new_name" not in removed
    assert ak.renamed_info("stock_zh_a_hist_em") is None


def test_search_puts_the_new_name_first_for_an_old_name():
    assert list(ak.search("stock_zh_a_hist", limit=1)["接口名"]) == [
        "stock_zh_a_hist_em"
    ]
    # 旧名称与其他词一起出现时同样置顶
    assert list(ak.search("stock_zh_a_daily 复权", limit=1)["接口名"]) == [
        "stock_zh_a_hist_sina"
    ]
    # 新名称与旧名称没有共同片段时也能找到
    assert list(ak.search("macro_china_shibor_all", limit=1)["接口名"]) == [
        "interest_rate_shibor_js"
    ]


def test_search_respects_category_filter_for_an_old_name():
    result = ak.search("stock_zh_a_hist", category="futures", limit=5)
    assert "stock_zh_a_hist_em" not in list(result["接口名"])
