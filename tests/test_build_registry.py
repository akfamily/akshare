from build_registry import parse_table

SIMPLE = """
输入参数

| 名称     | 类型  | 描述           |
|--------|-----|--------------|
| symbol | str | symbol="FTSE" |
| index  | str | index="rk_th2" |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期   | object  | -  |
"""

CONTAMINATED = """
输入参数

| 名称     | 类型  | 描述           |
|--------|-----|--------------|
| symbol | str | symbol="FTSE" |

实现波动率指数一览表

| Symbol | Name      | Earliest Available | Latest Available |
|--------|-----------|--------------------|------------------|
| .AEX   | AEX index | January 03, 2000   | June 01, 2024    |
| .AORD  | All Ords  | January 04, 2000   | June 01, 2024    |
"""


def test_parse_table_reads_rows():
    rows = parse_table(SIMPLE, "输入参数")
    assert rows == [
        {"name": "symbol", "type": "str", "desc": 'symbol="FTSE"'},
        {"name": "index", "type": "str", "desc": 'index="rk_th2"'},
    ]


def test_parse_table_picks_correct_header():
    rows = parse_table(SIMPLE, "输出参数")
    assert rows == [{"name": "日期", "type": "object", "desc": "-"}]


def test_parse_table_stops_at_blank_line_not_next_table():
    """回归：不得把后续无关表格的行吸进输入参数。"""
    rows = parse_table(CONTAMINATED, "输入参数")
    assert len(rows) == 1
    assert rows[0]["name"] == "symbol"


def test_parse_table_missing_header_returns_empty():
    assert parse_table(SIMPLE, "不存在的标题") == []
