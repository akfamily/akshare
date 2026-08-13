import pandas as pd
import pytest

from akshare.exceptions import InvalidParameterError
from akshare import registry
from akshare.registry import _bigrams, _tokenize, _score

RECORD = {
    "name": "stock_zh_a_hist",
    "category": "stock",
    "documented": True,
    "desc": "东方财富-沪深京 A 股历史行情数据",
    "outputs": [{"name": "市盈率", "type": "float64", "desc": "-"}],
}
UNDOC = dict(RECORD, name="stock_zh_a_other", documented=False)


def test_tokenize_splits_on_whitespace_and_punctuation():
    assert _tokenize("A股 历史行情") == ["A股", "历史行情"]
    assert _tokenize("stock,hist") == ["stock", "hist"]


def test_tokenize_drops_empty():
    assert _tokenize("   ") == []


def test_score_exact_name_match_dominates():
    assert _score(["stock_zh_a_hist"], RECORD) >= 100


def test_score_desc_hit_lower_than_name_hit():
    name_hit = _score(["hist"], RECORD)
    desc_hit = _score(["东方财富"], RECORD)
    assert name_hit > desc_hit > 0


def test_score_matches_output_column():
    assert _score(["市盈率"], RECORD) > 0


def test_score_all_tokens_hit_gets_bonus():
    both = _score(["hist", "东方财富"], RECORD)
    single = _score(["hist", "不存在的词"], RECORD)
    assert both > single


def test_score_undocumented_is_downweighted():
    assert _score(["历史行情"], UNDOC) < _score(["历史行情"], RECORD)


def test_score_no_hit_returns_zero():
    assert _score(["完全不相关"], RECORD) == 0


# desc 中 "A" 与 "股" 之间夹了一个源文档常见的排版空格，用于验证 _score 在
# 匹配前会先压缩查询 token 与被搜索字段的空白，否则连写查询词 "A股" 匹配不
# 到带空格的 "A 股" 子串。
WHITESPACE_RECORD = {
    "name": "quant_whitespace_probe",
    "category": "probe",
    "documented": True,
    "desc": "东方财富-A 股专题历史行情",
    "outputs": [],
}


def test_score_normalizes_whitespace_between_latin_and_cjk():
    assert _score(["A股"], WHITESPACE_RECORD) > 0


# "市盈率" 与 "动态" 是两个相邻列名。拼接列名时如果仍用空格分隔，归一化会把
# 分隔空格一并压掉，两个列名会首尾相连成 "市盈率动态"，让跨列名边界的伪造
# 查询词 "率动" 产生假匹配。分隔符换成不会出现在真实列名里的字符后，归一化
# 不应消除这个分隔，因此该查询词不应命中。
COLUMN_BOUNDARY_RECORD = {
    "name": "quant_column_boundary_probe",
    "category": "probe",
    "documented": True,
    "desc": "-",
    "outputs": [
        {"name": "市盈率", "type": "float64", "desc": "-"},
        {"name": "动态", "type": "float64", "desc": "-"},
    ],
}


def test_score_does_not_match_across_adjacent_column_boundary():
    assert _score(["率动"], COLUMN_BOUNDARY_RECORD) == 0


# name / category / desc / outputs 四个字段互不重叠子串，
# 便于构造「只命中单一字段」的查询，以钉住各权重常量的相对次序。
FIELD_RECORD = {
    "name": "quant_alpha_beta",
    "category": "kappa",
    "documented": True,
    "desc": "delta_desc_text",
    "outputs": [{"name": "epsilon_col", "type": "float64", "desc": "-"}],
}


def test_score_category_only_hit_is_positive():
    assert _score(["kappa"], FIELD_RECORD) > 0


def test_score_desc_gt_category_gt_output_when_each_hits_alone():
    desc_only = _score(["delta"], FIELD_RECORD)
    category_only = _score(["kappa"], FIELD_RECORD)
    output_only = _score(["epsilon"], FIELD_RECORD)
    assert desc_only > category_only > output_only > 0


FIXTURE = {
    "schema_version": 1,
    "interfaces": [
        {
            "name": "stock_zh_a_hist",
            "module": "akshare.stock.a",
            "category": "stock",
            "documented": True,
            "desc": "东方财富-沪深京 A 股历史行情数据",
            "url": None,
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
        },
        {
            "name": "fund_open_fund_info_em",
            "module": "akshare.fund.b",
            "category": "fund",
            "documented": True,
            "desc": "东方财富-开放式基金净值",
            "url": None,
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
        },
        {
            "name": "stock_no_doc",
            "module": "akshare.stock.c",
            "category": "stock",
            "documented": False,
            "desc": None,
            "url": None,
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
        },
        {
            "name": "bond_zh_hs_daily",
            "module": "akshare.bond.a",
            "category": "bond",
            "documented": True,
            "desc": "沪深债券日行情",
            "url": None,
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
        },
        {
            "name": "bond_zh_hs_cov_daily",
            "module": "akshare.bond.b",
            "category": "bond",
            "documented": True,
            "desc": "沪深可转债日行情",
            "url": None,
            "limit_desc": None,
            "params": [],
            "outputs": [],
            "example": None,
        },
    ],
}


@pytest.fixture(autouse=True)
def _use_fixture(monkeypatch):
    monkeypatch.setattr(registry, "_REGISTRY", FIXTURE)
    yield
    monkeypatch.setattr(registry, "_REGISTRY", None)


def test_search_returns_dataframe_with_expected_columns():
    df = registry.search("历史行情")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["接口名", "类目", "描述", "有无文档", "匹配分"]
    assert df.iloc[0]["接口名"] == "stock_zh_a_hist"


def test_search_empty_result_keeps_columns():
    df = registry.search("完全不相关的词")
    assert df.empty
    assert list(df.columns) == ["接口名", "类目", "描述", "有无文档", "匹配分"]


def test_search_respects_limit():
    assert len(registry.search("东方财富", limit=1)) == 1


def test_search_filters_by_category():
    df = registry.search("东方财富", category="fund")
    assert set(df["类目"]) == {"fund"}


def test_search_documented_only_excludes_undocumented():
    df = registry.search("stock", documented_only=True)
    assert "stock_no_doc" not in set(df["接口名"])
    assert "stock_zh_a_hist" in set(df["接口名"])


def test_interface_info_returns_full_record():
    info = registry.interface_info("stock_zh_a_hist")
    assert info["module"] == "akshare.stock.a"
    assert info["desc"] == "东方财富-沪深京 A 股历史行情数据"


def test_interface_info_unknown_name_suggests_candidates():
    with pytest.raises(InvalidParameterError) as exc:
        registry.interface_info("stock_zh_a_hisr")
    assert "stock_zh_a_hist" in str(exc.value)


def test_interface_info_deepcopy_isolates_nested_structures(monkeypatch):
    # 局部注入一份独立的 registry 数据（不改动模块级 FIXTURE），预置非空
    # outputs/params，用来验证 interface_info 返回的是深拷贝而不是缓存里
    # 那个 list 对象的引用——否则用户对返回值做 append 会真的污染进程级
    # 缓存，且此后所有 search/interface_info 都会被污染。
    local_registry = {
        "schema_version": 1,
        "interfaces": [
            {
                "name": "isolated_probe",
                "module": "akshare.probe.a",
                "category": "probe",
                "documented": True,
                "desc": "用于验证 interface_info 深拷贝隔离的探测记录",
                "url": None,
                "limit_desc": None,
                "params": [{"name": "symbol", "type": "str", "desc": "-"}],
                "outputs": [{"name": "close", "type": "float64", "desc": "-"}],
                "example": None,
            },
        ],
    }
    monkeypatch.setattr(registry, "_REGISTRY", local_registry)
    cached_record = local_registry["interfaces"][0]

    info = registry.interface_info("isolated_probe")

    # 结构断言：返回值的嵌套 list 不是缓存里的同一个对象。
    assert info["outputs"] is not cached_record["outputs"]
    assert info["params"] is not cached_record["params"]

    # 行为断言：对返回值追加元素后，缓存中的记录不受影响。
    info["outputs"].append({"name": "polluted", "type": "float64", "desc": "-"})
    info["params"].append({"name": "polluted", "type": "str", "desc": "-"})
    assert len(cached_record["outputs"]) == 1
    assert len(cached_record["params"]) == 1


def test_list_categories_counts():
    df = registry.list_categories()
    assert list(df.columns) == ["类目", "接口数"]
    assert dict(zip(df["类目"], df["接口数"]))["stock"] == 2


def test_bigrams_single_char_returns_empty():
    assert _bigrams("a") == []


def test_bigrams_compresses_whitespace_before_splitting():
    assert _bigrams("a b") == ["ab"]


def test_search_exact_name_is_ranked_first():
    # bond_zh_hs_daily 与 bond_zh_hs_cov_daily 是近似名字（后者是前者插入了
    # "cov_"），2-gram 降级分几乎相同，字典序上 cov 版本更靠前。如果降级路径
    # 覆盖了精确命中接口名的主分（而不是与主分取最大值），精确查询就会被
    # 挤到第二位，这条测试用来钉住这个回归。
    df = registry.search("bond_zh_hs_daily")
    assert df.iloc[0]["接口名"] == "bond_zh_hs_daily"


# decoy 与目标共享目标接口名作为前缀，且额外的输出列名把目标全部命中的
# 2-gram 又在 "outputs" 字段里重复命中了一遍，2-gram 降级分因此反超目标的
# 精确命中分（100）。如果 is_exact 判定仍使用未剥标点的原始 query 与
# record["name"] 比较（旧实现），两者的 is_exact 都是 False，纯按分数排序
# 会让 decoy 反而排到目标前面；is_exact 判定与 _score 的精确名捷径口径一致
# 后，目标应该无条件置顶，不受分数大小影响。
EXACT_PUNCTUATION_TARGET = {
    "name": "stock_zh_a_hist",
    "category": "stock",
    "documented": True,
    "desc": "东方财富-沪深京 A 股历史行情数据",
    "outputs": [],
}
EXACT_PUNCTUATION_DECOY = {
    "name": "stock_zh_a_hist_min_em",
    "category": "stock",
    "documented": True,
    "desc": "东方财富-沪深京 A 股历史行情数据",
    "outputs": [{"name": "stock_zh_a_hist_extra_col", "type": "float64", "desc": "-"}],
}
EXACT_PUNCTUATION_FIXTURE = {
    "schema_version": 1,
    "interfaces": [EXACT_PUNCTUATION_TARGET, EXACT_PUNCTUATION_DECOY],
}


@pytest.mark.parametrize("suffix", [",", "，", "、"])
def test_search_exact_name_survives_trailing_punctuation(suffix, monkeypatch):
    monkeypatch.setattr(registry, "_REGISTRY", EXACT_PUNCTUATION_FIXTURE)
    df = registry.search("stock_zh_a_hist" + suffix)
    assert df.iloc[0]["接口名"] == "stock_zh_a_hist"


def test_search_unspaced_query_recalls_via_bigram_fallback():
    # "行情历史" 整体不是 desc 里的连续子串（desc 里是"历史行情"，顺序相反），
    # 主分为 0，只有降级为 2-gram（"行情"/"情历"/"历史"）后才能命中 desc，
    # 用来验证 2-gram 降级召回在 search 上确实生效，而不只是在
    # interface_info 的错名提示路径里被间接测到。
    df = registry.search("行情历史")
    assert "stock_zh_a_hist" in set(df["接口名"])


def test_search_negative_limit_raises():
    with pytest.raises(InvalidParameterError):
        registry.search("stock", limit=-1)


def test_search_empty_query_returns_empty_with_columns():
    df = registry.search("")
    assert df.empty
    assert list(df.columns) == ["接口名", "类目", "描述", "有无文档", "匹配分"]
