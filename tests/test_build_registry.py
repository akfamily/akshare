import json

from build_registry import (
    collect_doc_records,
    collect_exports,
    diff_baseline,
    merge_records,
    parse_segment,
    parse_table,
    serialize,
)

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


def test_collect_doc_records_keeps_first_occurrence_by_sorted_path(tmp_path):
    """同名条目以首次出现者为准，"首次"由 sorted(rglob) 后的路径顺序决定。"""
    first_dir = tmp_path / "aaa"
    second_dir = tmp_path / "bbb"
    first_dir.mkdir()
    second_dir.mkdir()
    (first_dir / "a.md").write_text(
        "接口: dup_iface\n\n描述: 来自 aaa 的描述\n\n目标地址: https://a.com\n",
        encoding="utf-8",
    )
    (second_dir / "a.md").write_text(
        "接口: dup_iface\n\n描述: 来自 bbb 的描述\n\n目标地址: https://b.com\n",
        encoding="utf-8",
    )
    records = collect_doc_records(tmp_path)
    assert records["dup_iface"]["desc"] == "来自 aaa 的描述"


def test_collect_doc_records_category_from_parent_dir_name(tmp_path):
    stock_dir = tmp_path / "stock"
    stock_dir.mkdir()
    (stock_dir / "a.md").write_text(
        "接口: stock_only_iface\n\n描述: 股票专属接口\n", encoding="utf-8"
    )
    records = collect_doc_records(tmp_path)
    assert records["stock_only_iface"]["category"] == "stock"


def test_collect_doc_records_supports_fullwidth_colon(tmp_path):
    """回归：接口边界冒号必须容错全角"："，否则该条目会被并入前一条记录。"""
    stock_dir = tmp_path / "stock"
    stock_dir.mkdir()
    (stock_dir / "a.md").write_text(
        "接口: prev_iface\n\n描述: 前一个接口\n\n"
        "接口：stock_info_cjzc_em\n\n描述: 全角冒号接口\n",
        encoding="utf-8",
    )
    records = collect_doc_records(tmp_path)
    assert "stock_info_cjzc_em" in records
    assert records["stock_info_cjzc_em"]["desc"] == "全角冒号接口"
    assert records["prev_iface"]["desc"] == "前一个接口"


FAKE_INIT = '''"""模块文档字符串"""

from akshare._version import __version__
from akshare.index.index_cni import index_all_cni, index_hist_cni
from akshare.pro.data_pro import pro_api
from akshare.utils.token_process import set_token, get_token
from akshare.registry import search, interface_info, list_categories
from .exceptions import APIError, NetworkError

try:
    from akqmt import xt_api
except ImportError:
    pass
'''


def test_collect_exports_maps_name_to_module(tmp_path):
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    exports = collect_exports(init_file)
    assert exports["index_all_cni"] == "akshare.index.index_cni"
    assert exports["index_hist_cni"] == "akshare.index.index_cni"


def test_collect_exports_drops_non_data_interfaces(tmp_path):
    """__version__/pro_api/set_token 等可推断 category，必须显式排除。"""
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    exports = collect_exports(init_file)
    for name in (
        "__version__",
        "pro_api",
        "set_token",
        "get_token",
        "APIError",
        "NetworkError",
        "xt_api",
        "search",
        "interface_info",
        "list_categories",
    ):
        assert name not in exports
    assert len(exports) == 2


def test_merge_uses_exports_as_primary_key():
    """文档孤儿不得进入结果；无文档的导出必须保留并标记。"""
    exports = {
        "index_all_cni": "akshare.index.index_cni",
        "no_doc_func": "akshare.stock_feature.stock_info",
    }
    docs = {
        "index_all_cni": {
            "desc": "国证指数",
            "url": "https://x.com",
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
            "category": "index",
        },
        "orphan_func": {
            "desc": "已删除的接口",
            "url": None,
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
            "category": "stock",
        },
    }
    records = merge_records(exports, docs)
    names = [r["name"] for r in records]
    assert "orphan_func" not in names
    assert names == ["index_all_cni", "no_doc_func"]  # 已按字典序排序
    documented = {r["name"]: r["documented"] for r in records}
    assert documented == {"index_all_cni": True, "no_doc_func": False}


def test_merge_infers_category_from_module_when_undocumented():
    exports = {"no_doc_func": "akshare.stock_feature.stock_info"}
    records = merge_records(exports, {})
    assert records[0]["category"] == "stock_feature"
    assert records[0]["desc"] is None


def test_serialize_is_deterministic():
    """
    回归：serialize 必须依赖 sort_keys=True 消除字典插入顺序的影响。

    两份 record 的键值完全相同，但插入顺序相反（构造方式不同，非同一对象），
    若 sort_keys=True 被删除，json.dumps 会按各自的插入顺序输出，
    两次 serialize 结果将逐字节不同，此断言即会失败。
    """
    record = {
        "name": "a_func",
        "module": "akshare.fund.b",
        "category": "fund",
        "documented": False,
        "desc": None,
        "url": None,
        "limit_desc": None,
        "params": [],
        "outputs": [],
        "example": None,
    }
    reordered_record = {key: record[key] for key in reversed(list(record))}
    assert list(record.keys()) != list(reordered_record.keys())
    assert record == reordered_record  # 内容相同，仅插入顺序不同
    assert serialize([record]) == serialize([reordered_record])


def test_serialize_has_no_timestamp_or_version():
    records = merge_records({"f": "akshare.stock.a"}, {})
    payload = json.loads(serialize(records))
    assert set(payload.keys()) == {"schema_version", "interfaces"}


def test_serialize_ends_with_single_newline():
    text = serialize(merge_records({"f": "akshare.stock.a"}, {}))
    assert text.endswith("}\n")
    assert not text.endswith("\n\n")


BASE = {"undocumented": ["old_no_doc"], "orphaned": ["old_orphan"]}


def test_baseline_allows_known_gaps():
    exports = {"old_no_doc": "akshare.stock.a"}
    docs = {"old_orphan": {"category": "stock"}}
    assert diff_baseline(exports, docs, BASE) == []


def test_baseline_rejects_new_undocumented():
    exports = {"old_no_doc": "akshare.stock.a", "brand_new": "akshare.fund.b"}
    docs = {"old_orphan": {"category": "stock"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "brand_new" in problems[0]


def test_baseline_rejects_new_orphan():
    exports = {"old_no_doc": "akshare.stock.a"}
    docs = {"old_orphan": {"category": "stock"}, "new_orphan": {"category": "fund"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "new_orphan" in problems[0]


def test_baseline_rejects_stale_entry():
    """已修复的项必须从 baseline 移除，否则 baseline 会腐烂。"""
    exports = {"old_no_doc": "akshare.stock.a"}
    docs = {"old_no_doc": {"category": "stock"}, "old_orphan": {"category": "stock"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "old_no_doc" in problems[0]


def test_baseline_rejects_fixed_orphan():
    """已修复的孤儿项（补上导出）必须从 baseline 移除，否则 baseline 会腐烂。"""
    exports = {"old_no_doc": "akshare.stock.a", "old_orphan": "akshare.stock.b"}
    docs = {"old_orphan": {"category": "stock"}}
    problems = diff_baseline(exports, docs, BASE)
    assert len(problems) == 1
    assert "old_orphan" in problems[0]
