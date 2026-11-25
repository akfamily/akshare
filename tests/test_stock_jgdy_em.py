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


class FakeSurveyServer:
    """
    模拟 datacenter-web 的 RPT_ORG_SURVEY：按 filter 里的调研日期范围筛选、每页 50 条，
    并像 2026-11-25 实测的那样拒绝第 50 页以后的请求。
    """

    def __init__(self, rows_per_day):
        self.rows = [
            {
                "SECUCODE": f"{code:06d}.SZ",
                "SECURITY_CODE": f"{code:06d}",
                "SECURITY_NAME_ABBR": f"公司{code}",
                "NOTICE_DATE": f"{day} 00:00:00",
                "RECEIVE_START_DATE": f"{day} 00:00:00",
                "RECEIVE_OBJECT": f"机构{code}",
                "RECEIVE_PLACE": "公司会议室",
                "RECEIVE_WAY_EXPLAIN": "特定对象调研",
                "INVESTIGATORS": "张三",
                "RECEPTIONIST": "李四",
                "ORG_TYPE": "基金公司",
                "CLOSE_PRICE": 10.0,
                "CHANGE_RATE": 1.0,
            }
            for day, count in rows_per_day.items()
            for code in range(1, count + 1)
        ]
        self.filters = []

    def get(self, url, params=None, **kwargs):
        import re

        flt = params["filter"]
        self.filters.append(flt)
        low = re.search(r"RECEIVE_START_DATE>'([\d-]+)'", flt).group(1)
        high = re.search(r"RECEIVE_START_DATE<='([\d-]+)'", flt)
        rows = [
            row
            for row in self.rows
            if row["RECEIVE_START_DATE"][:10] > low
            and (high is None or row["RECEIVE_START_DATE"][:10] <= high.group(1))
        ]
        rows.sort(key=lambda row: (row["NOTICE_DATE"], row["SECURITY_CODE"]))
        rows.reverse()
        page = int(params["pageNumber"])
        size = int(params["pageSize"])
        pages = -(-len(rows) // size)
        if not rows:
            payload = EMPTY_JSON
        elif page > 50:
            payload = BUSY_JSON
        else:
            payload = {
                "result": {
                    "pages": pages,
                    "count": len(rows),
                    "data": rows[(page - 1) * size : page * size],
                },
                "success": True,
            }
        return SimpleNamespace(json=lambda: payload)


def test_detail_splits_large_range_by_day(monkeypatch):
    # 4 天共 3400 条，不分段要翻 68 页，第 50 页以后会被拒；按天查询每天最多 24 页
    server = FakeSurveyServer(
        {"2026-11-13": 700, "2026-11-16": 1200, "2026-11-17": 900, "2026-11-20": 600}
    )
    monkeypatch.setattr(module.http, "get", server.get)
    monkeypatch.setattr(module, "_today", lambda: module.datetime.date(2026, 11, 25))
    df = module.stock_jgdy_detail_em(date="20261112")
    assert len(df) == 3400
    assert df["序号"].tolist() == list(range(1, 3401))
    # 结果仍按公告日期从新到旧排列
    assert df["公告日期"].is_monotonic_decreasing
    assert str(df["公告日期"].iloc[0]) == "2026-11-20"
    assert not df.drop(columns=["序号"]).duplicated().any()
    # 第一次请求不带上界（探测总页数），之后的请求都限定了调研日期的上下界
    assert "RECEIVE_START_DATE<=" not in server.filters[0]
    assert any("RECEIVE_START_DATE<='2026-11-16'" in flt for flt in server.filters)


def test_detail_keeps_single_query_for_small_range(monkeypatch):
    server = FakeSurveyServer({"2026-11-20": 120})
    monkeypatch.setattr(module.http, "get", server.get)
    df = module.stock_jgdy_detail_em(date="20261118")
    assert len(df) == 120
    assert all("RECEIVE_START_DATE<=" not in flt for flt in server.filters)
    assert len(server.filters) == 3  # 3 页各请求一次，第 1 页不重复请求
