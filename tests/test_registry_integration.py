import pytest

from akshare import registry


@pytest.fixture(autouse=True)
def _force_real_registry(monkeypatch):
    """确保从真实产物文件加载，不受其他测试文件注入的假数据影响。"""
    monkeypatch.setattr(registry, "_REGISTRY", None)


def test_public_api_is_exported():
    import akshare as ak

    assert callable(ak.search)
    assert callable(ak.interface_info)
    assert callable(ak.list_categories)


def test_real_search_returns_callable_interfaces():
    """不变量①：search 返回的每个接口名都必须真实可调用。"""
    import akshare as ak

    df = ak.search("A股 历史行情", limit=10)
    assert not df.empty
    for name in df["接口名"]:
        assert hasattr(ak, name), f"{name} 在 registry 中但无法从 akshare 取到"


def test_every_registry_entry_is_reachable():
    """全量校验不变量①，将来有人删函数忘删文档时会立即失败。"""
    import akshare as ak

    interfaces = registry._load()["interfaces"]
    # 先确认确实加载到了完整产物，否则空/残缺列表会让下面的遍历空集通过，
    # 静默放行「产物路径解析出错」「JSON 被截断」等问题。真实产物当前
    # 约 980 条，用下界而非硬编码具体数字，避免接口数增长时反而要改测试。
    assert len(interfaces) > 900, (
        f"registry 加载到的接口数异常偏少: {len(interfaces)} 条，"
        "怀疑产物未正确加载（路径错误/JSON 被截断/_load 返回残缺数据）"
    )
    missing = [item["name"] for item in interfaces if not hasattr(ak, item["name"])]
    assert missing == [], f"registry 中有 {len(missing)} 个接口无法取到: {missing[:5]}"


# ---- 同义词检索与同类接口对照表（真实登记数据） ----


def _names(query, limit=5):
    return list(registry.search(query, limit=limit)["接口名"])


def test_search_daily_bars_rank_first_for_colloquial_query():
    """「日线」是用户的说法，接口描述写的是「日频率」「历史行情」"""
    assert set(_names("A股 日线", 4)) >= {
        "stock_zh_a_hist",
        "stock_zh_a_daily",
        "stock_zh_a_hist_tx",
    }
    # 港股指数的日线接口（index_hk_daily_sina）与个股日线同分，取前三
    assert set(_names("港股 日线", 3)) >= {"stock_hk_daily", "stock_hk_hist"}
    assert set(_names("期货 日线", 5)) >= {"futures_zh_daily_sina", "futures_hist_em"}
    assert _names("期货 分钟", 1) == ["futures_zh_min_sina"]
    assert set(_names("A股 实时行情", 2)) == {"stock_zh_a_spot_em", "stock_zh_a_spot"}


def test_search_unknown_word_still_returns_matches_for_known_word():
    # 证券名称不是接口的属性，不应让整个查询落空
    assert len(registry.search("贵州茅台 日线")) > 0


def test_interface_info_carries_alternatives():
    info = registry.interface_info("stock_zh_a_hist")
    assert info["alternatives"] == ["stock_zh_a_daily", "stock_zh_a_hist_tx"]
    # 单向关系：分市场的实时行情可改用全市场接口，反过来不成立
    assert registry.interface_info("stock_sh_a_spot_em")["alternatives"] == [
        "stock_zh_a_spot"
    ]
    assert (
        "stock_sh_a_spot_em"
        not in registry.interface_info("stock_zh_a_spot")["alternatives"]
    )
    assert registry.interface_info("macro_china_cpi")["alternatives"] == []
