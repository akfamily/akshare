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
    # 1090 条，用下界而非硬编码具体数字，避免接口数增长时反而要改测试。
    assert len(interfaces) > 1000, (
        f"registry 加载到的接口数异常偏少: {len(interfaces)} 条，"
        "怀疑产物未正确加载（路径错误/JSON 被截断/_load 返回残缺数据）"
    )
    missing = [item["name"] for item in interfaces if not hasattr(ak, item["name"])]
    assert missing == [], f"registry 中有 {len(missing)} 个接口无法取到: {missing[:5]}"
