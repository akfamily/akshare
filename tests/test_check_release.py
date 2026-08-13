import pytest

from check_release import (
    collect_problems,
    has_version_entry,
    parse_tag,
    read_version,
)


def make_repo(tmp_path, version="1.18.91", init_version=None, changelog_version=None):
    """
    造一个只含发布校验所需三个文件的最小仓库。

    :param tmp_path: pytest 提供的临时目录
    :param version: 写入 _version.py 的版本号
    :param init_version: 写入 __init__.py 版本历史的版本号，默认与 version 相同
    :param changelog_version: 写入 changelog 的版本号，默认与 version 相同
    :return: 仓库根目录
    """
    init_version = version if init_version is None else init_version
    changelog_version = version if changelog_version is None else changelog_version
    (tmp_path / "akshare").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "akshare" / "_version.py").write_text(
        f'__version__ = "{version}"\n', encoding="utf-8"
    )
    (tmp_path / "akshare" / "__init__.py").write_text(
        f'"""\n{init_version} fix: fix some interface\n"""\n', encoding="utf-8"
    )
    (tmp_path / "docs" / "changelog.md").write_text(
        f"## 更新说明详情\n\n{changelog_version} fix: fix some interface\n\n"
        "    1. 修复某个接口\n",
        encoding="utf-8",
    )
    return tmp_path


def test_parse_tag_extracts_version():
    assert parse_tag("release-v1.18.91") == "1.18.91"


@pytest.mark.parametrize(
    "tag",
    ["v1.18.91", "release-v1.18", "release-1.18.91", "release-v1.18.91-rc1", ""],
)
def test_parse_tag_rejects_malformed(tag):
    """tag 格式必须严格，否则版本号可能被截取成意料之外的值。"""
    with pytest.raises(ValueError):
        parse_tag(tag)


def test_read_version(tmp_path):
    path = tmp_path / "_version.py"
    path.write_text('__version__ = "1.2.3"\n', encoding="utf-8")
    assert read_version(path) == "1.2.3"


def test_read_version_without_declaration_raises(tmp_path):
    path = tmp_path / "_version.py"
    path.write_text("# 没有版本声明\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_version(path)


def test_has_version_entry_requires_line_start():
    """必须锚定行首，否则 1.18.9 会被 1.18.91 的条目误判为存在。"""
    text = "1.18.91 fix: something\n"
    assert has_version_entry(text, "1.18.91")
    assert not has_version_entry(text, "1.18.9")
    assert not has_version_entry("见 1.18.91 的说明\n", "1.18.91")


def test_collect_problems_passes_when_all_aligned(tmp_path):
    repo = make_repo(tmp_path)
    assert collect_problems(repo, "release-v1.18.91") == []


def test_collect_problems_detects_tag_version_mismatch(tmp_path):
    repo = make_repo(tmp_path, version="1.18.91")
    problems = collect_problems(repo, "release-v1.18.99")
    assert len(problems) == 1
    assert "不一致" in problems[0]


def test_collect_problems_detects_missing_changelog_entry(tmp_path):
    repo = make_repo(tmp_path, version="1.18.91", changelog_version="1.18.90")
    problems = collect_problems(repo, "release-v1.18.91")
    assert any("changelog" in p for p in problems)


def test_collect_problems_detects_missing_init_history(tmp_path):
    repo = make_repo(tmp_path, version="1.18.91", init_version="1.18.90")
    problems = collect_problems(repo, "release-v1.18.91")
    assert any("__init__.py" in p for p in problems)


def test_collect_problems_reports_every_problem_at_once(tmp_path):
    """一次报全，避免修一个再跑一次 CI 才发现下一个。"""
    repo = make_repo(
        tmp_path, version="1.18.91", init_version="1.18.90", changelog_version="1.18.89"
    )
    problems = collect_problems(repo, "release-v1.18.99")
    assert len(problems) == 3
