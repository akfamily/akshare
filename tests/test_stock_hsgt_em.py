"""沪深港通持股：上游对查询范围没有数据时应给出明确的报错。"""

from types import SimpleNamespace

import pytest

from akshare.exceptions import APIError
from akshare.stock.flow import stock_hsgt_em as module

# 2026-11-25 实测：查询范围内没有数据时 datacenter-web 返回的内容
EMPTY_JSON = {
    "version": None,
    "result": None,
    "success": False,
    "message": "返回数据为空",
    "code": 9201,
}


@pytest.fixture
def empty_upstream(monkeypatch):
    monkeypatch.setattr(
        module.http,
        "get",
        lambda url, **kwargs: SimpleNamespace(json=lambda: EMPTY_JSON),
    )


@pytest.mark.parametrize("market", ["北向持股", "南向持股", "沪股通持股", "深股通持股"])
def test_institution_statistics_reports_empty_range(empty_upstream, market):
    with pytest.raises(APIError, match="返回数据为空"):
        module.stock_hsgt_institution_statistics_em(
            market=market, start_date="20201218", end_date="20201218"
        )


def test_individual_detail_reports_empty_range(empty_upstream):
    with pytest.raises(APIError, match="返回数据为空"):
        module.stock_hsgt_individual_detail_em(
            symbol="002008", start_date="20210830", end_date="20211026"
        )
