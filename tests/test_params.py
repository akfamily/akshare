#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 接口参数类型转换测试

经 HTTP（AKTools 的 /api/public）、MCP 或配置文件调用时，参数值往往只能是文本。少数
接口的参数要求数字或布尔值：fund_fh_em(page="-1") 不等于 -1，
search(documented_only="false") 作为布尔值为真。这些参数现在同时接受原生类型与文本。

原先 13 个接口另有 timeout 参数，stock_zh_a_hist?timeout=5 会报
Timeout value … must be an int, float or None，且默认 None 等于不设超时、绕过
ak.set_timeout。1.20.13 起删除这些参数，超时统一由 ak.set_timeout 设置。全程不联网。
"""

import inspect
import pathlib
import typing

import pytest
import requests

import akshare as ak
from akshare.exceptions import InvalidParameterError
from akshare.utils.context import DEFAULT_TIMEOUT, config
from akshare.utils.params import to_bool, to_int

ROOT = pathlib.Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "value, expected", [(5, 5), ("5", 5), (" -1 ", -1), ("3.0", 3), (2.0, 2)]
)
def test_to_int(value, expected):
    assert to_int(value, "page") == expected


@pytest.mark.parametrize("value", ["abc", "1.5", "", True, None])
def test_to_int_rejects(value):
    with pytest.raises(InvalidParameterError, match="page"):
        to_int(value, "page")


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, True),
        (False, False),
        ("true", True),
        ("False", False),
        ("1", True),
        ("0", False),
        ("yes", True),
    ],
)
def test_to_bool(value, expected):
    assert to_bool(value, "flag") is expected


def test_to_bool_rejects():
    with pytest.raises(InvalidParameterError, match="flag"):
        to_bool("maybe", "flag")


@pytest.fixture
def sent(monkeypatch):
    """记录交给传输层的 timeout，并返回一个空响应，不联网"""
    calls = []
    monkeypatch.setattr(requests.sessions, "get_environ_proxies", lambda *a, **k: {})
    monkeypatch.setattr(config, "timeout", DEFAULT_TIMEOUT)

    def fake_send(self, request, **kwargs):
        calls.append(kwargs["timeout"])
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"data": null}'
        response.request = request
        return response

    monkeypatch.setattr(requests.Session, "send", fake_send)
    return calls


def test_stock_zh_a_hist_uses_global_timeout(sent, monkeypatch):
    """接口不再提供 timeout 参数，请求使用 ak.set_timeout 设置的全局超时"""
    ak.stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20240110")
    monkeypatch.setattr(config, "timeout", 7)
    ak.stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20240110")
    assert sent == [DEFAULT_TIMEOUT, 7]


def test_interfaces_have_no_timeout_param():
    """超时统一由 ak.set_timeout 设置，公开接口不再提供 timeout 参数"""
    offenders = [
        name
        for name in ak.__all__
        if inspect.isfunction(getattr(ak, name))
        and "timeout" in inspect.signature(getattr(ak, name)).parameters
        and name not in {"set_timeout"}
    ]
    assert not offenders, offenders


def test_search_accepts_text_params():
    assert len(ak.search("历史行情", limit="3")) <= 3
    documented = ak.search("历史行情", limit="50", documented_only="true")
    assert documented.equals(ak.search("历史行情", limit=50, documented_only=True))
    undocumented = ak.search("历史行情", limit="50", documented_only="false")
    assert undocumented.equals(ak.search("历史行情", limit=50))


def _numeric_params():
    """公开接口中要求整数、小数或布尔值的参数：按类型注解判断，没有注解时按默认值判断"""
    for name in ak.__all__:
        func = getattr(ak, name)
        if not inspect.isfunction(func):
            continue
        for param in inspect.signature(func).parameters.values():
            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                if isinstance(param.default, (bool, int, float)):
                    yield name, param.name
                continue
            members = typing.get_args(annotation) or (annotation,)
            if str not in members and any(t in members for t in (bool, int, float)):
                yield name, param.name


def test_numeric_params_accept_text():
    """新增数字或布尔参数时，必须在模块里经 to_int、to_bool 或 int()、float() 转换"""
    params = list(_numeric_params())
    assert len(params) >= 5
    missing = []
    for name, param in params:
        source = pathlib.Path(inspect.getsourcefile(getattr(ak, name))).read_text(
            encoding="utf-8"
        )
        patterns = (
            f"to_int({param}",
            f"to_bool({param}",
            f"int({param})",
            f"float({param})",
        )
        if not any(p in source for p in patterns):
            missing.append(f"{name}.{param}")
    assert not missing, f"以下参数没有转换文本输入：{missing}"


# 有意保留的固定超时：FRED 历史压缩包达数十 MB，需放宽总时长；pro 客户端的超时由用户传入；
# multi_decrypt 的超时限制的是 JS 执行时间而非 HTTP 请求
_ALLOWED_TIMEOUTS = {
    "akshare/research/research_fred_md.py",
    "akshare/pro/client.py",
    "akshare/utils/multi_decrypt.py",
}


def test_no_hardcoded_request_timeout():
    """请求超时统一由 ak.set_timeout 设置，接口代码不应再写死 timeout=15 之类的值"""
    import ast

    offenders = []
    for path in sorted((ROOT / "akshare").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in _ALLOWED_TIMEOUTS:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for kw in node.keywords:
                    if kw.arg == "timeout":
                        offenders.append(f"{rel}:{node.lineno}")
    assert not offenders, (
        f"以下请求写死了 timeout，请删去，改由 ak.set_timeout 控制：{offenders}"
    )
