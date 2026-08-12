import pandas as pd
import pytest

from akshare.exceptions import InvalidParameterError
from akshare import registry
from akshare.registry import _tokenize, _score

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


def test_interface_info_returns_full_record():
    info = registry.interface_info("stock_zh_a_hist")
    assert info["module"] == "akshare.stock.a"
    assert info["desc"] == "东方财富-沪深京 A 股历史行情数据"


def test_interface_info_unknown_name_suggests_candidates():
    with pytest.raises(InvalidParameterError) as exc:
        registry.interface_info("stock_zh_a_hisr")
    assert "stock_zh_a_hist" in str(exc.value)


def test_list_categories_counts():
    df = registry.list_categories()
    assert list(df.columns) == ["类目", "接口数"]
    assert dict(zip(df["类目"], df["接口数"]))["stock"] == 2
