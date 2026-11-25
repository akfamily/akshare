"""QVIX 分时接口：上游 CSV 里混入 Excel 错误值时仍应返回数值列。"""

from io import BytesIO

import pandas as pd
import pytest

from akshare.index import index_option_qvix

# 2026-11-25 抓到的 vix100.csv 开头几行：第一行的 Max/Min 是 "#NUM!"，
# pandas 3 因此把整列读成文本，往文本列里写数值会抛 TypeError
CSV_WITH_EXCEL_ERROR = (
    "Time,QVIX(100ETF),Pre,Max,Min\n"
    "9:30:00,#NUM!,46.97,#NUM!,#NUM!\n"
    "9:31:24,24.69,,,\n"
    "9:32:28,24.18,,,\n"
).encode("utf-8")

MIN_FUNCTIONS = [
    name
    for name in dir(index_option_qvix)
    if name.startswith("index_option_") and name.endswith("_min_qvix")
]


def test_all_min_functions_are_covered():
    # 3 个股指期权的分时接口在 1.20.70 移除（上游文件里不再有数据）
    assert len(MIN_FUNCTIONS) == 6


@pytest.mark.parametrize("name", MIN_FUNCTIONS)
def test_min_qvix_coerces_excel_error_to_nan(monkeypatch, name):
    monkeypatch.setattr(
        index_option_qvix.http,
        "get_buffer",
        lambda url, **kwargs: BytesIO(CSV_WITH_EXCEL_ERROR),
    )
    df = getattr(index_option_qvix, name)()
    assert list(df.columns) == ["time", "qvix"]
    assert pd.api.types.is_float_dtype(df["qvix"])
    assert pd.isna(df["qvix"].iloc[0])
    assert df["qvix"].iloc[1:].tolist() == [24.69, 24.18]
