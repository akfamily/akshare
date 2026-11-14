import json
import pytest

from build_registry import (
    ALL_BEGIN,
    ALL_END,
    collect_all_names,
    collect_doc_records,
    collect_exports,
    diff_baseline,
    find_missing_labels,
    merge_records,
    parse_segment,
    parse_table,
    render_all_block,
    replace_all_block,
    serialize,
    write_if_changed,
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
        "接口：stock_news_cjzc_em\n\n描述: 全角冒号接口\n",
        encoding="utf-8",
    )
    records = collect_doc_records(tmp_path)
    assert "stock_news_cjzc_em" in records
    assert records["stock_news_cjzc_em"]["desc"] == "全角冒号接口"
    assert records["prev_iface"]["desc"] == "前一个接口"


def test_find_missing_labels_reports_entry_without_label(tmp_path):
    stock_dir = tmp_path / "stock"
    stock_dir.mkdir()
    (stock_dir / "a.md").write_text(
        "(labelled_iface)=\n### 有标签\n\n接口：labelled_iface\n\n"
        "### 无标签\n\n接口：bare_iface\n",
        encoding="utf-8",
    )
    assert find_missing_labels(tmp_path) == ["bare_iface"]


def test_find_missing_labels_accepts_label_before_entry_line(tmp_path):
    """同一标题下有两个接口时，第二个接口的标签写在其 "接口：" 行之前。"""
    bond_dir = tmp_path / "bond"
    bond_dir.mkdir()
    (bond_dir / "a.md").write_text(
        "(first_iface)=\n### 标题\n\n接口：first_iface\n\n"
        "(second_iface)=\n接口：second_iface\n",
        encoding="utf-8",
    )
    assert find_missing_labels(tmp_path) == []


FAKE_INIT = '''"""模块文档字符串"""

from akshare._version import __version__
from akshare.index.index_cni import index_all_cni, index_hist_cni
from akshare.pro.data_pro import pro_api
from akshare.utils.token_process import set_token, get_token
from akshare.registry import search, interface_info, list_categories
from .exceptions import APIError, NetworkError
from pandas import DataFrame

try:
    from akshare.optional.maybe_missing import optional_iface
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
    """
    三类名字都不得进入导出表，各自由不同规则拦下：

    - __version__/pro_api/set_token/search 等：可推断 category，靠 EXCLUDE 显式排除；
    - DataFrame：模块名不以 "akshare." 开头，第三方导入一律忽略；
    - optional_iface：嵌套在 try 内，collect_exports 只遍历 tree.body 顶层节点。
    """
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
        "search",
        "interface_info",
        "list_categories",
        "DataFrame",
        "optional_iface",
    ):
        assert name not in exports
    assert len(exports) == 2


def test_merge_uses_exports_as_primary_key():
    """文档孤儿不得进入结果；无文档的导出必须保留并标记。"""
    exports = {
        "index_all_cni": "akshare.index.index_cni",
        "no_doc_func": "akshare.stock.research.stock_info",
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
    exports = {"no_doc_func": "akshare.stock.research.stock_info"}
    records = merge_records(exports, {})
    assert records[0]["category"] == "stock"
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


def test_collect_all_names_includes_non_data_public_api(tmp_path):
    """__all__ 是数据接口与非数据公开 API 的并集，两类都不能漏。"""
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    names = collect_all_names(init_file)
    # 数据接口
    assert "index_all_cni" in names
    assert "index_hist_cni" in names
    # registry 排除、但仍属公开 API 的工具函数与异常类
    for name in ("pro_api", "set_token", "search", "APIError", "NetworkError"):
        assert name in names


def test_collect_all_names_excludes_dunder_and_third_party(tmp_path):
    """dunder 的可访问性与 __all__ 无关；第三方与条件导入不得进入。"""
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    names = collect_all_names(init_file)
    for name in ("__version__", "DataFrame", "optional_iface"):
        assert name not in names


def test_collect_all_names_is_sorted_and_unique(tmp_path):
    init_file = tmp_path / "__init__.py"
    init_file.write_text(FAKE_INIT, encoding="utf-8")
    names = collect_all_names(init_file)
    assert names == sorted(names)
    assert len(names) == len(set(names))


def test_render_all_block_is_valid_python_and_round_trips():
    """渲染结果必须能被 exec 出等价的 __all__，否则等于写坏了 __init__.py。"""
    block = render_all_block(["b_iface", "a_iface"])
    assert block.startswith(ALL_BEGIN)
    assert block.rstrip("\n").endswith(ALL_END)
    namespace = {}
    exec(block, namespace)
    assert namespace["__all__"] == ["b_iface", "a_iface"]


def test_replace_all_block_appends_when_marker_absent():
    text = '"""doc"""\nfrom akshare.x import y\n'
    block = render_all_block(["y"])
    result = replace_all_block(text, block)
    assert result.startswith('"""doc"""')
    assert result.count(ALL_BEGIN) == 1
    assert result.endswith(block)


def test_replace_all_block_replaces_in_place_and_is_idempotent():
    """重复生成不得堆叠出第二个块，这是 --check 能作为门禁的前提。"""
    text = '"""doc"""\nfrom akshare.x import y\n'
    once = replace_all_block(text, render_all_block(["y"]))
    twice = replace_all_block(once, render_all_block(["y"]))
    assert once == twice
    assert twice.count(ALL_BEGIN) == 1
    assert twice.count(ALL_END) == 1


def test_replace_all_block_updates_stale_content():
    text = '"""doc"""\nfrom akshare.x import y\n'
    stale = replace_all_block(text, render_all_block(["old_iface"]))
    fresh = replace_all_block(stale, render_all_block(["new_iface"]))
    assert "old_iface" not in fresh
    assert "new_iface" in fresh
    assert fresh.count(ALL_BEGIN) == 1


def test_write_if_changed_skips_identical_content(tmp_path):
    # 内容未变时不得写入：重写会改动 mtime 与行尾，让 git 把文件标为已修改
    target = tmp_path / "a.json"
    target.write_bytes(b"line1\r\nline2\r\n")
    before = target.stat().st_mtime_ns
    assert write_if_changed(target, "line1\nline2\n") is False
    assert target.read_bytes() == b"line1\r\nline2\r\n"
    assert target.stat().st_mtime_ns == before


def test_write_if_changed_preserves_crlf(tmp_path):
    # Windows 上 core.autocrlf=true 时工作区是 CRLF，写回时须沿用
    target = tmp_path / "a.json"
    target.write_bytes(b"old\r\n")
    assert write_if_changed(target, "new1\nnew2\n") is True
    assert target.read_bytes() == b"new1\r\nnew2\r\n"


def test_write_if_changed_preserves_lf(tmp_path):
    target = tmp_path / "a.json"
    target.write_bytes(b"old\n")
    assert write_if_changed(target, "new1\nnew2\n") is True
    assert target.read_bytes() == b"new1\nnew2\n"


def test_write_if_changed_creates_missing_file_with_lf(tmp_path):
    target = tmp_path / "a.json"
    assert write_if_changed(target, "new\n") is True
    assert target.read_bytes() == b"new\n"


# ---- rate_limit：静态识别请求东方财富 push2 行情服务器的接口 ----

from build_registry import (  # noqa: E402
    PUSH2_HOST_PATTERN,
    PUSH2_IN_TEXT_RE,
    RATE_LIMIT_EASTMONEY_PUSH2,
    ModuleIndex,
    collect_export_targets,
    collect_rate_limits,
    requests_push2,
)


def test_push2_pattern_matches_runtime_detection():
    # 构建脚本不能 import akshare，只能复制规则；两处不一致时，登记里的
    # rate_limit 与运行时抛出的 Push2RateLimitError 就会对不上
    from akshare.utils import http

    assert http._PUSH2_HOST.pattern == f"^{PUSH2_HOST_PATTERN}$"


@pytest.mark.parametrize(
    "text",
    [
        "https://push2.eastmoney.com/api/qt/clist/get",
        "https://push2his.eastmoney.com/api/qt/stock/kline/get",
        "https://push2ex.eastmoney.com/getTopicZTPool",
        "https://push2delay.eastmoney.com/api/qt/clist/get",
        "https://82.push2.eastmoney.com/api/qt/clist/get",
        ".push2his.eastmoney.com/api/qt/stock/kline/get",  # f-string 拆出的片段
    ],
)
def test_push2_in_text_matches_quote_servers(text):
    assert PUSH2_IN_TEXT_RE.search(text)


@pytest.mark.parametrize(
    "text",
    [
        "https://datacenter-web.eastmoney.com/api/data/v1/get",
        "https://data.eastmoney.com/cjsj/cpi.html",
        "https://fund.eastmoney.com/js/fundcode_search.js",
        "https://xpush2.eastmoney.com/api",
        "https://quote.eastmoney.com/center/gridlist.html",
    ],
)
def test_push2_in_text_ignores_other_servers(text):
    assert not PUSH2_IN_TEXT_RE.search(text)


PUSH2_FAKE_INIT = """
from akshare.quote.hist import quote_direct, quote_via_helper as quote_alias
from akshare.quote.hist import quote_via_constant, quote_docstring_only
from akshare.quote.hist import quote_via_relative_import, macro_datacenter
from akshare.quote.hist import quote_too_deep
"""

PUSH2_FAKE_HIST = '''
from .helpers import remote_helper

KLINE_URL = "https://push2his.eastmoney.com/api/qt/stock/kline/get"


def _helper():
    return "https://82.push2.eastmoney.com/api/qt/clist/get"


def _level3():
    return "https://push2.eastmoney.com/api"


def _level2():
    return _level3()


def _level1():
    return _level2()


def _level0():
    return _level1()


def quote_direct():
    """https://datacenter-web.eastmoney.com/ 文档里的地址不算"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    return url


def quote_via_helper():
    return _helper()


def quote_via_constant():
    return KLINE_URL


def quote_docstring_only():
    """
    https://push2.eastmoney.com/ 只出现在文档字符串里
    """
    return "https://datacenter-web.eastmoney.com/api/data/v1/get"


def quote_via_relative_import():
    return remote_helper()


def macro_datacenter():
    return "https://datacenter-web.eastmoney.com/api/data/v1/get"


def quote_too_deep():
    return _level0()
'''

PUSH2_FAKE_HELPERS = """
def remote_helper():
    return f"https://{82}.push2.eastmoney.com/api/qt/clist/get"
"""


@pytest.fixture
def push2_repo(tmp_path):
    package = tmp_path / "akshare"
    (package / "quote").mkdir(parents=True)
    (package / "__init__.py").write_text(PUSH2_FAKE_INIT, encoding="utf-8")
    (package / "quote" / "__init__.py").write_text("", encoding="utf-8")
    (package / "quote" / "hist.py").write_text(PUSH2_FAKE_HIST, encoding="utf-8")
    (package / "quote" / "helpers.py").write_text(PUSH2_FAKE_HELPERS, encoding="utf-8")
    return tmp_path


def test_collect_export_targets_keeps_original_name(push2_repo):
    targets = collect_export_targets(push2_repo / "akshare" / "__init__.py")
    assert targets["quote_alias"] == ("akshare.quote.hist", "quote_via_helper")
    assert targets["quote_direct"] == ("akshare.quote.hist", "quote_direct")


def test_collect_rate_limits_traces_requested_servers(push2_repo):
    limits = collect_rate_limits(push2_repo)
    assert limits == {
        "quote_direct": RATE_LIMIT_EASTMONEY_PUSH2,
        "quote_alias": RATE_LIMIT_EASTMONEY_PUSH2,  # 同模块辅助函数，as 改名导出
        "quote_via_constant": RATE_LIMIT_EASTMONEY_PUSH2,  # 模块级常量
        "quote_via_relative_import": RATE_LIMIT_EASTMONEY_PUSH2,  # 相对导入 + f-string
        "quote_docstring_only": None,  # 文档字符串里的地址不是请求地址
        "macro_datacenter": None,  # 东方财富数据中心不限流
        "quote_too_deep": None,  # 超过 MAX_CALL_DEPTH 层的调用不再追踪
    }


def test_requests_push2_handles_missing_module_and_function(push2_repo):
    index = ModuleIndex(push2_repo)
    assert requests_push2(index, "akshare.not_exist", "f") is False
    assert requests_push2(index, "akshare.quote.hist", "not_exist") is False


def test_merge_records_carries_rate_limit():
    exports = {"a_func": "akshare.stock.a", "b_func": "akshare.stock.b"}
    records = merge_records(exports, {}, {"a_func": RATE_LIMIT_EASTMONEY_PUSH2})
    assert {r["name"]: r["rate_limit"] for r in records} == {
        "a_func": RATE_LIMIT_EASTMONEY_PUSH2,
        "b_func": None,
    }
    # 不传 rate_limits 时字段仍然存在，值为 None
    assert merge_records(exports, {})[0]["rate_limit"] is None


def test_real_registry_marks_push2_interfaces():
    import akshare as ak

    assert ak.interface_info("stock_zh_a_hist_em")["rate_limit"] == "eastmoney_push2"
    assert ak.interface_info("stock_zh_a_spot_em")["rate_limit"] == "eastmoney_push2"
    # 东方财富数据中心（宏观、龙虎榜）与其他数据源不受 push2 限流影响
    assert ak.interface_info("macro_china_cpi")["rate_limit"] is None
    assert ak.interface_info("stock_lhb_detail_em")["rate_limit"] is None
    assert ak.interface_info("stock_zh_a_daily_sina")["rate_limit"] is None


# ---- alternatives：人工维护的同类接口对照表 ----

from build_registry import resolve_alternatives  # noqa: E402

ALT_EXPORTS = {name: "akshare.x" for name in ("a_em", "a_sina", "a_tx", "b_em", "c")}


def test_resolve_alternatives_groups_are_symmetric_and_keep_order():
    mapping, problems = resolve_alternatives(
        {"groups": [["a_em", "a_sina", "a_tx"]]}, ALT_EXPORTS
    )
    assert problems == []
    assert mapping == {
        "a_em": ["a_sina", "a_tx"],
        "a_sina": ["a_em", "a_tx"],
        "a_tx": ["a_em", "a_sina"],
    }


def test_resolve_alternatives_one_way_is_not_mirrored():
    mapping, problems = resolve_alternatives(
        {"groups": [["a_em", "a_sina"]], "one_way": {"b_em": ["a_sina"]}}, ALT_EXPORTS
    )
    assert problems == []
    assert mapping["b_em"] == ["a_sina"]
    assert mapping["a_sina"] == ["a_em"]


def test_resolve_alternatives_reports_unknown_names_and_drops_them():
    mapping, problems = resolve_alternatives(
        {"groups": [["a_em", "removed_func"]], "one_way": {"gone": ["c"]}}, ALT_EXPORTS
    )
    assert mapping == {}
    assert any("removed_func" in problem for problem in problems)
    assert any("gone" in problem for problem in problems)


def test_resolve_alternatives_rejects_self_duplicates_and_single_member():
    _, problems = resolve_alternatives(
        {"groups": [["a_em"], ["b_em", "b_em", "c"]], "one_way": {"c": ["c"]}},
        ALT_EXPORTS,
    )
    text = "\n".join(problems)
    assert "至少需要两个接口" in text
    assert "重复" in text
    assert "不能把自己列为同类接口" in text


def test_merge_records_carries_alternatives():
    exports = {"a_em": "akshare.stock.a", "c": "akshare.stock.c"}
    records = merge_records(exports, {}, None, {"a_em": ["c"]})
    assert {r["name"]: r["alternatives"] for r in records} == {"a_em": ["c"], "c": []}


def test_real_alternatives_table_is_valid_and_useful():
    import pathlib

    import build_registry

    repo_root = pathlib.Path(build_registry.__file__).resolve().parent.parent
    exports = collect_exports(repo_root / "akshare" / "__init__.py")
    mapping, problems = build_registry.load_alternatives(repo_root, exports)
    assert problems == []
    limits = collect_rate_limits(repo_root)
    # 对照表的主要用途是东方财富行情接口被限流时换源：每个登记了同类接口的
    # push2 接口，都至少要有一个不走 push2 的选择
    for name, others in mapping.items():
        if limits.get(name):
            assert any(not limits.get(other) for other in others), name
