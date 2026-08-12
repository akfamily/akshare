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
