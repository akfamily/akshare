import sys
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

AKSHARE_DIR = str(ROOT / "akshare")


@pytest.fixture(autouse=True)
def _fail_on_akshare_deprecations():
    """
    akshare 自身代码触发的 DeprecationWarning、FutureWarning 一律视为测试失败
    pandas 会把警告的来源标记为调用它的 akshare 模块，因此按警告记录的文件路径判断。
    第三方库自己触发的弃用警告（如 Python 3.14 起 py_mini_racer 导入时的 ctypes 警告）
    不在 akshare 中，无法在这里修复，不视为失败。不用 pyproject.toml 的 filterwarnings：
    它只能按警告类别或模块名匹配，前者会误伤第三方库，后者匹配不到 pandas 的警告
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        yield
    ours = [
        w
        for w in caught
        if issubclass(w.category, (DeprecationWarning, FutureWarning))
        and str(Path(w.filename).resolve()).startswith(AKSHARE_DIR)
    ]
    if ours:
        lines = [
            f"{Path(w.filename).relative_to(ROOT)}:{w.lineno} {w.category.__name__}: {w.message}"
            for w in ours
        ]
        pytest.fail("akshare 代码触发了弃用警告：\n" + "\n".join(lines))
