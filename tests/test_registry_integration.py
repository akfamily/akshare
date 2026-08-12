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

    missing = [
        item["name"]
        for item in registry._load()["interfaces"]
        if not hasattr(ak, item["name"])
    ]
    assert missing == [], f"registry 中有 {len(missing)} 个接口无法取到: {missing[:5]}"
