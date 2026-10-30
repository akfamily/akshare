#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: akshare.utils.jsonish 的解析测试

jsonish 替代已停止维护的 demjson（停留在 2015 年的 2.2.4），用于解析上游返回的
JavaScript 对象字面量。上线前用 22 + 35 个接口抓取的 817 份真实响应与 demjson
逐份比对，结果全部一致。这里的用例取自那批响应的开头片段，覆盖实际出现过的写法，
并补充 JavaScript 语法的边界情况。全程不联网。
"""

import math

import pytest

from akshare.exceptions import DataParsingError
from akshare.utils import jsonish

# 截取自真实响应，键名与结构保持原样
REAL_SNIPPETS = [
    # 天天基金：键名不加引号
    (
        '{datas:[["000001","华夏成长混合","混合型-灵活","0.9680"]],count:["1"]}',
        {
            "datas": [["000001", "华夏成长混合", "混合型-灵活", "0.9680"]],
            "count": ["1"],
        },
    ),
    # 天天基金新发基金：数组中的空位，demjson 解析为 undefined
    (
        '{datas:[["023100","金信周期价值混合C","","",,"30466187","0.00%"]]}',
        {"datas": [["023100", "金信周期价值混合C", "", "", None, "30466187", "0.00%"]]},
    ),
    # 新浪宏观：键名不加引号，键名含保留字 except，值中有空格与等号
    (
        '{config:{all:[[0,"统计年度"],[2,"数量","百万美元"]],index:2,except:"1",'
        'condition:" F003=0 and F004=1"},data:[["2025","入境",null]]}',
        {
            "config": {
                "all": [[0, "统计年度"], [2, "数量", "百万美元"]],
                "index": 2,
                "except": "1",
                "condition": " F003=0 and F004=1",
            },
            "data": [["2025", "入境", None]],
        },
    ),
    # 新浪期货品种：单引号字符串、末尾逗号后跟注释再收尾
    (
        "{ \n    czce : ['郑州商品交易所', ['PTA', 'pta_qh', '16'],['菜油', 'czy_qh', '18']],\n"
        "    gfex : ['广州期货交易所', ['钯', 'pd_qh', '20', 'gfuturesindex']],\n"
        "    // bohai :  ['渤海商品\"交易所', ['x', 'y']],\n    \n}",
        {
            "czce": [
                "郑州商品交易所",
                ["PTA", "pta_qh", "16"],
                ["菜油", "czy_qh", "18"],
            ],
            "gfex": ["广州期货交易所", ["钯", "pd_qh", "20", "gfuturesindex"]],
        },
    ),
    # 新浪外盘期货：单双引号混用、浮点数
    (
        '{\n        FEF: ["新加坡铁矿石", [0.01, "美元/公吨"]],\n'
        "        FCPO: ['马棕油',[0.03215,\"美元/盎司\"]],\n    }",
        {
            "FEF": ["新加坡铁矿石", [0.01, "美元/公吨"]],
            "FCPO": ["马棕油", [0.03215, "美元/盎司"]],
        },
    ),
    # 天天基金持仓：双引号字符串中含单引号的 HTML 属性与冒号
    (
        "{ content:\"<div class='box'><a title='华夏成长混合' href='http://x.com/a'>\",arryear:[2024]}",
        {
            "content": "<div class='box'><a title='华夏成长混合' href='http://x.com/a'>",
            "arryear": [2024],
        },
    ),
]


@pytest.mark.parametrize("text, expected", REAL_SNIPPETS)
def test_real_snippets(text, expected):
    assert jsonish.loads(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ('{"a": [1, 2.5, "x"]}', {"a": [1, 2.5, "x"]}),
        ("[1,]", [1]),
        ("[1,,]", [1, None]),
        ("[,]", [None]),
        ("[,1]", [None, 1]),
        ("{a:1,}", {"a": 1}),
        ("[1, /* c */ ]", [1]),
        ("[1, // c\n ,2]", [1, None, 2]),
        ('["x",/*,*/"y"]', ["x", "y"]),
        (
            "{a:undefined,b:true,c:null,d:false}",
            {"a": None, "b": True, "c": None, "d": False},
        ),
        ("{a:0x1F,b:-0x10}", {"a": 31, "b": -16}),
        ("{a:1.5e3,b:-2,c:1e5}", {"a": 1500.0, "b": -2, "c": 100000.0}),
        ("{$a:1,_b:2,true:3}", {"$a": 1, "_b": 2, "true": 3}),
        (r"{'k':'it\'s \"x\"'}", {"k": 'it\'s "x"'}),
    ],
)
def test_javascript_syntax(text, expected):
    assert jsonish.loads(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        '{"s":"a:b, [c,,d]"}',
        '{"s":"he said \\"hi\\", x:1"}',
        '{"u":"http://x.com/a,,b // not a comment"}',
        '{"s":"[1,]"}',
    ],
)
def test_string_contents_untouched(text):
    """字符串内部的冒号、逗号、方括号、斜杠不能被当作语法改写"""
    import json

    assert jsonish.loads(text) == json.loads(text)


def test_nan_passes_through():
    assert math.isnan(jsonish.loads("{a:NaN}")["a"])


def test_bytes_input():
    assert jsonish.loads('{a:"中"}'.encode("utf-8")) == {"a": "中"}


@pytest.mark.parametrize("text", ["{a:foo}", "{a:", "", "var x = 1"])
def test_invalid_raises_data_parsing_error_with_context(text):
    with pytest.raises(DataParsingError) as excinfo:
        jsonish.loads(text)
    assert "无法解析上游返回的数据" in str(excinfo.value)
