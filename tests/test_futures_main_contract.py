"""match_main_contract 的主力合约判定（离线）"""

import pandas as pd

from akshare.futures.futures_zh_sina import _pick_main_contract


def _frame(rows):
    columns = ["symbol", "exchange", "name", "trade", "position", "ticktime"]
    return pd.DataFrame(rows, columns=columns)


def test_pick_follows_continuous_row_not_largest_position():
    data_df = _frame(
        [
            ["PG2701", "dce", "液化石油气2701", "4300", "63686", "13:31:30"],
            ["PG0", "dce", "液化石油气连续", "4400", "63294", "13:31:30"],
            ["PG2612", "dce", "液化石油气2612", "4400", "63294", "13:31:30"],
        ]
    )
    assert _pick_main_contract(data_df) == "PG2612"


def test_pick_tolerates_field_out_of_sync_with_continuous_row():
    data_df = _frame(
        [
            ["PS0", "gfex", "多晶硅连续", "34110", "55925", "11:29:55"],
            ["PS2701", "gfex", "多晶硅2701", "34110", "55925", "11:29:56"],
            ["PS2612", "gfex", "多晶硅2612", "34750", "30897", "11:29:56"],
        ]
    )
    assert _pick_main_contract(data_df) == "PS2701"


def test_pick_largest_position_without_continuous_row():
    data_df = _frame(
        [
            ["T2703", "cffex", "10年期国债期货2703", "110", "101823", "13:30:58"],
            ["T2612", "cffex", "10年期国债期货2612", "110", "361798", "13:30:58"],
        ]
    )
    assert _pick_main_contract(data_df) == "T2612"


def test_pick_returns_none_when_only_continuous_row():
    data_df = _frame([["WH0", "czce", "强麦连续", "0", "0", "15:00:00"]])
    assert _pick_main_contract(data_df) is None
