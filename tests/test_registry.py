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
