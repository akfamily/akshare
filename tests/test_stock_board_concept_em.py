import pandas as pd
import pytest

import akshare.stock.stock_board_concept_em as concept_em


EXPECTED_HIST_COLUMNS = [
    "日期",
    "开盘",
    "收盘",
    "最高",
    "最低",
    "涨跌幅",
    "涨跌额",
    "成交量",
    "成交额",
    "振幅",
    "换手率",
]


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


def test_board_code_does_not_require_name_lookup(monkeypatch):
    monkeypatch.setattr(
        concept_em,
        "__stock_board_concept_name_em",
        lambda: pytest.fail("board codes should bypass the name lookup"),
    )
    monkeypatch.setattr(
        concept_em.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(
            {
                "data": {
                    "klines": [
                        "2025-01-01,1,2,3,0,10,20,4,5,1,0.1",
                    ]
                }
            }
        ),
    )

    result = concept_em.stock_board_concept_hist_em(symbol="BK1676")

    assert list(result.columns) == EXPECTED_HIST_COLUMNS
    assert result.loc[0, "收盘"] == 2


@pytest.mark.parametrize(
    "payload",
    [
        {"data": None},
        {},
        {"data": {}},
        {"data": {"klines": None}},
        {"data": {"klines": []}},
    ],
)
def test_empty_or_invalid_response_returns_schema(monkeypatch, payload):
    monkeypatch.setattr(
        concept_em.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(payload),
    )

    result = concept_em.stock_board_concept_hist_em(symbol="BK1676")

    assert isinstance(result, pd.DataFrame)
    assert result.empty
    assert list(result.columns) == EXPECTED_HIST_COLUMNS
