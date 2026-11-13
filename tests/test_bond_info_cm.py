#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/5
Desc: 中国货币网债券信息查询的债券类型处理测试

2026-11 起中国货币网要求查询时必须指定债券类型，否则返回 {"errorMsg": "债券类型必选"}，
原先只按简称查询的 bond_info_cm 与依赖它的 bond_info_detail_cm 报 KeyError: 'pageTotal'。
现在只给简称或代码时依次按各债券类型查询，查到即停；什么条件都不给时抛出 APIError。

本测试全程不联网：顶替上游请求函数，按债券类型返回预设结果。
"""

import pandas as pd
import pytest

from akshare.bond import bond_info_cm as m
from akshare.exceptions import APIError

TYPES = pd.DataFrame(
    {"name": ["国债", "政策性金融债", "同业存单"], "code": ["1", "3", "41"]}
)
ROW = {
    "bondDefinedCode": "beced3rkhi",
    "bondName": "24国开10",
    "bondCode": "240210",
    "issueStartDate": "2024-04-30",
    "bondType": "政策性金融债",
    "entyFullName": "国家开发银行",
    "debtRtng": "---",
}


@pytest.fixture
def upstream(monkeypatch):
    calls = []

    def fake_post(url, payload):
        calls.append(payload["bondType"])
        if not payload["bondType"]:
            return {"total": 0, "errorMsg": "债券类型必选"}
        if payload["bondType"] == "3" and payload["bondName"] == "24国开10":
            return {"total": 1, "pageTotal": 1, "resultList": [ROW]}
        return {"total": 0, "pageTotal": 0, "resultList": []}

    monkeypatch.setattr(m, "_bond_info_cm_post", fake_post)
    monkeypatch.setattr(m, "bond_info_cm_query", lambda symbol: TYPES)
    monkeypatch.setattr(m, "bond_zh_close_yield_map_cm", lambda: None)
    monkeypatch.setattr(m.time, "sleep", lambda s: None)
    m.bond_info_cm.cache_clear()
    yield calls
    m.bond_info_cm.cache_clear()


def test_name_only_tries_types_until_found(upstream):
    df = m.bond_info_cm(bond_name="24国开10")
    assert df["债券代码"].tolist() == ["240210"]
    assert upstream == ["1", "3"]


def test_name_not_found_returns_empty_with_columns(upstream):
    df = m.bond_info_cm(bond_name="不存在")
    assert df.empty and "债券简称" in df.columns
    assert upstream == ["1", "3", "41"]


def test_no_condition_raises_clear_error(upstream):
    with pytest.raises(APIError, match="必须指定债券类型"):
        m.bond_info_cm()
    assert upstream == []
