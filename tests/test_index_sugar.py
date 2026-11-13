#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/13
Desc: 沐甜科技数据中心接口的列名映射测试

上游返回 {"category": [日期], "data": {指标名：[数值]}}。原实现按位置给列命名，
上游调整字段顺序后各列错位且不报错；现按指标名取列。全程不联网。
"""

from akshare.index import index_sugar


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def test_columns_follow_names_not_upstream_order(monkeypatch):
    payload = {
        "category": ["2023/1/30", "2023/1/31"],
        "data": {
            "巴西糖进口成本": ["6782", "6938"],
            "泰国糖进口成本": ["6808", "6964"],
            "日照现货价": ["6260", "6260"],
            "巴西糖进口利润空间": ["-548", "-704"],
            "泰国糖进口利润空间": ["-522", "-678"],
        },
    }
    monkeypatch.setattr(index_sugar.http, "get", lambda *a, **k: _Response(payload))
    df = index_sugar.index_outer_quota_sugar_msweet()
    assert list(df.columns) == [
        "日期",
        "巴西糖进口成本",
        "泰国糖进口利润空间",
        "巴西糖进口利润空间",
        "泰国糖进口成本",
        "日照现货价",
    ]
    assert df["泰国糖进口成本"].tolist() == [6808.0, 6964.0]
    assert df["泰国糖进口利润空间"].tolist() == [-522.0, -678.0]
    assert str(df["日期"].iloc[0]) == "2023-01-30"


def test_dirty_values_are_cleaned(monkeypatch):
    payload = {
        "category": ["2019-1-31", "2014-10-14"],
        "data": {
            "综合价格": ["5377", "5000"],
            "原糖价格": ["12..88", "4045.2 "],
            "现货价格": ["5071", ""],
        },
    }
    monkeypatch.setattr(index_sugar.http, "get", lambda *a, **k: _Response(payload))
    df = index_sugar.index_sugar_msweet()
    assert df["原糖价格"].tolist() == [12.88, 4045.2]
    assert df["现货价格"].isna().tolist() == [False, True]
    assert df["综合价格"].dtype == "float64"
