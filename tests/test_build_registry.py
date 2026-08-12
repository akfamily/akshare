from build_registry import parse_segment, parse_table

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

TWO_COLUMN = """
输入参数

| 名称     | 类型  |
|--------|-----|
| symbol | str |
"""

FOUR_COLUMN = """
输入参数

| 名称     | 类型  | 描述           | 备注    |
|--------|-----|--------------|-------|
| symbol | str | symbol="FTSE" | extra |
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


def test_parse_table_pads_missing_desc_when_row_has_two_cells():
    """回归：数据行只有 2 列时，缺失的 desc 应补齐为 None。"""
    rows = parse_table(TWO_COLUMN, "输入参数")
    assert rows == [{"name": "symbol", "type": "str", "desc": None}]


def test_parse_table_truncates_extra_column_when_row_has_four_cells():
    """回归：数据行有 4 列时，只保留前 3 列，第 4 列被丢弃。"""
    rows = parse_table(FOUR_COLUMN, "输入参数")
    assert rows == [{"name": "symbol", "type": "str", "desc": 'symbol="FTSE"'}]


SEGMENT = """
目标地址: https://www.cnindex.com.cn/index.html

描述: 国证指数-最近交易日的所有指数

限量: 单次返回所有指数

输入参数

| 名称     | 类型  | 描述 |
|--------|-----|----|
| symbol | str | -  |

输出参数

| 名称     | 类型  | 描述 |
|--------|-----|----|
| 指数代码 | str | -  |

接口示例

```python
import akshare as ak

df = ak.index_all_cni()
print(df)
```

数据示例
"""


def test_parse_segment_extracts_fields():
    rec = parse_segment(SEGMENT)
    assert rec["url"] == "https://www.cnindex.com.cn/index.html"
    assert rec["desc"] == "国证指数-最近交易日的所有指数"
    assert rec["limit_desc"] == "单次返回所有指数"
    assert rec["params"] == [{"name": "symbol", "type": "str", "desc": "-"}]
    assert rec["outputs"] == [{"name": "指数代码", "type": "str", "desc": "-"}]
    assert rec["example"].startswith("import akshare as ak")
    assert "print(df)" in rec["example"]


def test_parse_segment_absent_limit_is_none():
    rec = parse_segment("描述: 某接口\n\n目标地址: https://x.com\n")
    assert rec["limit_desc"] is None
    assert rec["params"] == []
    assert rec["example"] is None
