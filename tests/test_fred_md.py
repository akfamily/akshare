#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: fred_md、fred_qd 的文件名识别测试

上游历史压缩包与当年各期 CSV 的文件名写法不统一，以下用例均取自真实文件名；
识别错误会让对应年月的数据取不到，或被误报为“没有这一期”。全程不联网。
"""

import pytest

from akshare.research.research_fred_md import _vintage_key


@pytest.mark.parametrize(
    "name, key",
    [
        ("2020-01.csv", "2020-01"),
        ("FRED-MD-2025m08.csv", "2025-08"),
        ("FRED-MD_2025m12.csv", "2025-12"),
        ("FRED-QD_2019m1.csv", "2019-01"),
        ("FRED-QD_2018m05.csv", "2018-05"),
        ("2026-01-md.csv", "2026-01"),
        ("2026-09-qd.csv", "2026-09"),
        ("2026-rev-08-md.csv", "2026-08"),
        (
            "/-/media/project/frbstl/stlouisfed/research/fred-md/monthly/2026-09-md.csv",
            "2026-09",
        ),
    ],
)
def test_vintage_key(name, key):
    assert _vintage_key(name) == key


@pytest.mark.parametrize(
    "name",
    [
        "historical-vintages-of-fred-md-2015-01-to-2025-12.zip",
        "fred-md_appendix0324.zip",
        "README.txt",
    ],
)
def test_non_vintage_names_ignored(name):
    assert _vintage_key(name) is None
