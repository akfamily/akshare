"""机构调研：没有数据与服务器繁忙要报成不同的错误，翻页中途失败不能抛 TypeError。"""

from types import SimpleNamespace

import pytest

from akshare.exceptions import APIError, InvalidParameterError
from akshare.stock.holder import stock_jgdy_em as module

# 2026-11-25 实测 datacenter-web 的两种失败返回
EMPTY_JSON = {"result": None, "success": False, "message": "返回数据为空", "code": 9201}
BUSY_JSON = {"result": None, "success": False, "message": "服务器繁忙", "code": 9701}

FUNCTIONS = [module.stock_jgdy_tj_em, module.stock_jgdy_detail_em]


def _serve(monkeypatch, responses):
    """按请求顺序依次返回 responses 中的 JSON，并记录每次请求的参数。"""
    calls = []
    queue = list(responses)

    def fake_get(url, params=None, **kwargs):
        calls.append(dict(params))
        payload = queue.pop(0)
        return SimpleNamespace(json=lambda: payload)

    monkeypatch.setattr(module.http, "get", fake_get)
    return calls


@pytest.mark.parametrize("func", FUNCTIONS)
def test_empty_first_page_is_invalid_parameter(monkeypatch, func):
    _serve(monkeypatch, [EMPTY_JSON])
    with pytest.raises(InvalidParameterError, match="返回数据为空"):
        func(date="20180928")


@pytest.mark.parametrize("func", FUNCTIONS)
def test_busy_first_page_is_not_reported_as_missing_data(monkeypatch, func):
    # 服务器繁忙时首页也是 result=None；过去一律报“没有该日期以来的数据”
    _serve(monkeypatch, [BUSY_JSON])
    with pytest.raises(APIError, match="服务器繁忙"):
        func(date="20261112")


@pytest.mark.parametrize("func", FUNCTIONS)
def test_busy_page_during_paging_is_api_error(monkeypatch, func):
    # 实测翻到约第 50 页以后上游时常返回“服务器繁忙”，过去在这里抛
    # TypeError: 'NoneType' object is not subscriptable
    first = {"result": {"pages": 3, "data": []}, "success": True}
    _serve(monkeypatch, [first, first, BUSY_JSON])
    with pytest.raises(APIError, match="服务器繁忙"):
        func(date="20261112")


def test_detail_keeps_page_size_50(monkeypatch):
    # 2026-11-25 实测：RPT_ORG_SURVEY 每页超过 50 条（100、200、500 都试过）时
    # 上游直接返回“服务器繁忙”，不能靠加大每页条数来减少翻页
    calls = _serve(monkeypatch, [EMPTY_JSON])
    with pytest.raises(InvalidParameterError):
        module.stock_jgdy_detail_em(date="20261112")
    assert calls[0]["pageSize"] == "50"
