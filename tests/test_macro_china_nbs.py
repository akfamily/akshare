#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/5/8 10:00
Desc: 国家统计局 NBS 接口测试 (issues #7180 #7211 #7216 修复后)

纯单元测试默认运行; 联网 smoke 默认 skip, 设环境变量 AKSHARE_NETWORK_TESTS=1 启用.
"""

import os

import pandas as pd
import pytest

from akshare.economic.macro_china_nbs import (
    _parse_user_period,
    _normalize,
    _strip_period_tail,
    _parse_slice_range,
    _parse_nbs_code,
    _shift_period,
    _fmt_nbs_code,
    _period_to_dts,
    _expand_dts_to_codes,
    _validate_dts_within_slice,
    macro_china_nbs_nation,
    macro_china_nbs_region,
)

_RUN_NETWORK = os.environ.get("AKSHARE_NETWORK_TESTS") == "1"


# ============ 纯单元测试 (不联网) ============


class TestNormalize:
    def test_basic_strip(self):
        assert _normalize("foo bar") == "foobar"
        assert _normalize("foo　bar") == "foobar"  # 全角空格

    def test_full_width_punctuation(self):
        assert _normalize("foo（bar）") == "foo(bar)"
        assert _normalize("foo：bar") == "foo:bar"

    def test_underscore_removed(self):
        assert _normalize("a_b_c") == "abc"

    def test_nbs_real_name(self):
        # NBS 改版后 catalog name 加了空格
        nbs = "居民消费价格分类指数 (上年同月=100) "
        user = "居民消费价格分类指数(上年同月=100)"
        assert _normalize(nbs) == _normalize(user)

    def test_underscore_label(self):
        # 老版用户传带下划线
        old = "地区生产总值_累计值(亿元)"
        new = "地区生产总值累计值 (亿元) "
        assert _normalize(old) == _normalize(new)

    def test_empty_and_none(self):
        assert _normalize(None) == ""
        assert _normalize("") == ""


class TestStripPeriodTail:
    def test_strip_basic(self):
        assert _strip_period_tail("xxx(2018-2025)") == "xxx"
        assert _strip_period_tail("xxx(2026-)") == "xxx"
        assert _strip_period_tail("xxx(-2015)") == "xxx"
        assert _strip_period_tail("xxx(2018-至今)") == "xxx"

    def test_no_tail(self):
        assert _strip_period_tail("xxx") == "xxx"


class TestParseSliceRange:
    def test_closed(self):
        assert _parse_slice_range("xxx(2018-2025)") == (2018, 2025)

    def test_open_right(self):
        assert _parse_slice_range("xxx(2026-)") == (2026, None)
        assert _parse_slice_range("xxx(2018-至今)") == (2018, None)

    def test_open_left(self):
        assert _parse_slice_range("xxx(-2015)") == (None, 2015)

    def test_no_tail(self):
        assert _parse_slice_range("xxx") is None


class TestParseUserPeriod:
    def test_last_lower_and_upper(self):
        assert _parse_user_period("last10") == {"kind": "LATEST", "n": 10}
        assert _parse_user_period("LAST10") == {"kind": "LATEST", "n": 10}
        assert _parse_user_period("LaSt5") == {"kind": "LATEST", "n": 5}

    def test_none_and_empty(self):
        assert _parse_user_period(None)["kind"] == "LATEST"
        assert _parse_user_period("")["kind"] == "LATEST"
        assert _parse_user_period("  ")["kind"] == "LATEST"

    def test_range(self):
        assert _parse_user_period("2018-2023") == {
            "kind": "RANGE",
            "start": 2018,
            "end": 2023,
        }

    def test_open_range(self):
        assert _parse_user_period("2018-") == {"kind": "OPEN_RANGE", "start": 2018}

    def test_single_year(self):
        assert _parse_user_period("2022") == {"kind": "SINGLE", "year": 2022}

    def test_discrete_month(self):
        r = _parse_user_period("201201,201205")
        assert r["kind"] == "DISCRETE_MONTH"
        assert r["codes"] == [(2012, 1), (2012, 5)]

    def test_discrete_quarter(self):
        r = _parse_user_period("2012A,2012B,2012C,2012D")
        assert r["kind"] == "DISCRETE_QUARTER"
        assert r["codes"] == [(2012, 1), (2012, 2), (2012, 3), (2012, 4)]

    def test_discrete_year(self):
        r = _parse_user_period("2012,2013")
        assert r["kind"] == "DISCRETE_YEAR"
        assert r["codes"] == [2012, 2013]

    def test_invalid(self):
        with pytest.raises(ValueError):
            _parse_user_period("abc")
        with pytest.raises(ValueError):
            _parse_user_period("2012,201205")  # 类型不一致

    def test_last_zero_rejected(self):
        with pytest.raises(ValueError):
            _parse_user_period("last0")

    def test_discrete_month_invalid_month_fails(self):
        # 月份必须 1-12, '201213' 这种应 fail-fast
        with pytest.raises(ValueError, match="非法月份"):
            _parse_user_period("201213,201214")


class TestNbsCode:
    def test_parse(self):
        assert _parse_nbs_code("202604MM") == (2026, 4, "MM")
        assert _parse_nbs_code("202404SS") == (2024, 4, "SS")
        assert _parse_nbs_code("2025YY") == (2025, 0, "YY")

    def test_fmt(self):
        assert _fmt_nbs_code(2026, 4, "MM") == "202604MM"
        assert _fmt_nbs_code(2024, 4, "SS") == "202404SS"
        assert _fmt_nbs_code(2025, 0, "YY") == "2025YY"

    def test_shift(self):
        assert _shift_period(2026, 4, "MM", 1) == (2026, 3)
        assert _shift_period(2026, 1, "MM", 1) == (2025, 12)  # 跨年
        assert _shift_period(2026, 1, "SS", 1) == (2025, 4)
        assert _shift_period(2025, 0, "YY", 5) == (2020, 0)


class TestPeriodToDts:
    def test_last_n_month(self):
        # latest = 202604MM, LAST5 应该是 202512MM-202604MM
        dts = _period_to_dts("月度数据", {"kind": "LATEST", "n": 5}, "202604MM")
        assert dts == ["202512MM-202604MM"]

    def test_last_n_quarter(self):
        # latest = 202601SS, LAST5 应该是 202501SS-202601SS (5 个季度)
        dts = _period_to_dts("季度数据", {"kind": "LATEST", "n": 5}, "202601SS")
        assert dts == ["202501SS-202601SS"]

    def test_last_n_year(self):
        dts = _period_to_dts("年度数据", {"kind": "LATEST", "n": 5}, "2025YY")
        assert dts == ["2021YY-2025YY"]

    def test_range_year(self):
        dts = _period_to_dts(
            "年度数据", {"kind": "RANGE", "start": 2018, "end": 2023}, "2025YY"
        )
        assert dts == ["2018YY-2023YY"]

    def test_range_month(self):
        dts = _period_to_dts(
            "月度数据", {"kind": "RANGE", "start": 2020, "end": 2022}, "202604MM"
        )
        assert dts == ["202001MM-202212MM"]

    def test_range_quarter(self):
        dts = _period_to_dts(
            "季度数据", {"kind": "RANGE", "start": 2020, "end": 2022}, "202601SS"
        )
        assert dts == ["202001SS-202204SS"]

    def test_range_clamp_end(self):
        # end 2030 超过 latest 2025, 应 clamp 到 latest
        dts = _period_to_dts(
            "年度数据", {"kind": "RANGE", "start": 2020, "end": 2030}, "2025YY"
        )
        assert dts == ["2020YY-2025YY"]

    def test_range_start_after_latest_fails(self):
        # start 2026 晚于 latest 2025, 应 fail-fast
        with pytest.raises(ValueError):
            _period_to_dts(
                "年度数据", {"kind": "RANGE", "start": 2026, "end": 2030}, "2025YY"
            )

    def test_range_start_after_end_fails(self):
        with pytest.raises(ValueError):
            _period_to_dts(
                "年度数据", {"kind": "RANGE", "start": 2025, "end": 2018}, "2025YY"
            )

    def test_single_year_clamp_current_year(self):
        # period="2026" + latest 202604MM, 单年 2026 终点应 clamp 到 4 月不是 12 月
        dts = _period_to_dts("月度数据", {"kind": "SINGLE", "year": 2026}, "202604MM")
        assert dts == ["202601MM-202604MM"]

    def test_single_year_future_fails(self):
        # period="2030" + latest 2025YY, 应 fail-fast
        with pytest.raises(ValueError):
            _period_to_dts("年度数据", {"kind": "SINGLE", "year": 2030}, "2025YY")

    def test_discrete_year_future_fails(self):
        with pytest.raises(ValueError):
            _period_to_dts(
                "年度数据",
                {"kind": "DISCRETE_YEAR", "codes": [2024, 2030]},
                "2025YY",
            )

    def test_discrete_month_future_fails(self):
        with pytest.raises(ValueError):
            _period_to_dts(
                "月度数据",
                {"kind": "DISCRETE_MONTH", "codes": [(2026, 12), (2027, 1)]},
                "202604MM",
            )

    def test_discrete_kind_mismatch_fails(self):
        # 月度 kind 用年度逗号 → fail-fast
        with pytest.raises(ValueError, match="不匹配"):
            _period_to_dts(
                "月度数据",
                {"kind": "DISCRETE_YEAR", "codes": [2012, 2013]},
                "202604MM",
            )
        # 年度 kind 用月度逗号 → fail-fast
        with pytest.raises(ValueError, match="不匹配"):
            _period_to_dts(
                "年度数据",
                {"kind": "DISCRETE_MONTH", "codes": [(2012, 1)]},
                "2025YY",
            )

    def test_open_range(self):
        dts = _period_to_dts(
            "年度数据", {"kind": "OPEN_RANGE", "start": 2018}, "2025YY"
        )
        assert dts == ["2018YY-2025YY"]

    def test_single_year(self):
        dts = _period_to_dts("月度数据", {"kind": "SINGLE", "year": 2022}, "202604MM")
        assert dts == ["202201MM-202212MM"]

    def test_discrete_month(self):
        dts = _period_to_dts(
            "月度数据",
            {"kind": "DISCRETE_MONTH", "codes": [(2012, 1), (2012, 5)]},
            "202604MM",
        )
        assert dts == ["201201MM-201201MM", "201205MM-201205MM"]

    def test_discrete_quarter(self):
        dts = _period_to_dts(
            "季度数据",
            {"kind": "DISCRETE_QUARTER", "codes": [(2012, 1), (2012, 4)]},
            "202601SS",
        )
        assert dts == ["201201SS-201201SS", "201204SS-201204SS"]


class TestValidateDtsWithinSlice:
    """跨切片 fail-fast — PR1 不做跨切片 stitching."""

    def test_no_slice_passes(self):
        # leaf 无切片标记, 不限制
        _validate_dts_within_slice(["2018YY-2025YY"], None)

    def test_within_closed_slice(self):
        _validate_dts_within_slice(["2022YY-2024YY"], (2021, 2025))

    def test_below_start_fails(self):
        with pytest.raises(ValueError, match="早于"):
            _validate_dts_within_slice(["2018YY-2024YY"], (2021, 2025))

    def test_above_end_fails(self):
        with pytest.raises(ValueError, match="晚于"):
            _validate_dts_within_slice(["2022YY-2026YY"], (2021, 2025))

    def test_open_right_slice(self):
        _validate_dts_within_slice(["2027YY-2030YY"], (2026, None))
        with pytest.raises(ValueError, match="早于"):
            _validate_dts_within_slice(["2025YY-2027YY"], (2026, None))

    def test_open_left_slice(self):
        _validate_dts_within_slice(["2010YY-2015YY"], (None, 2015))
        with pytest.raises(ValueError, match="晚于"):
            _validate_dts_within_slice(["2010YY-2016YY"], (None, 2015))


class TestExpandDtsToCodes:
    def test_year(self):
        assert _expand_dts_to_codes(["2018YY-2020YY"], "YY") == [
            "2018YY",
            "2019YY",
            "2020YY",
        ]

    def test_month(self):
        codes = _expand_dts_to_codes(["202401MM-202403MM"], "MM")
        assert codes == ["202401MM", "202402MM", "202403MM"]

    def test_quarter(self):
        codes = _expand_dts_to_codes(["202301SS-202304SS"], "SS")
        assert codes == ["202301SS", "202302SS", "202303SS", "202304SS"]

    def test_multi_span(self):
        codes = _expand_dts_to_codes(["2018YY-2018YY", "2020YY-2020YY"], "YY")
        assert codes == ["2018YY", "2020YY"]


# ============ 联网 smoke (走 NBS HTTP, 数据可能变) ============


@pytest.mark.skipif(
    not _RUN_NETWORK,
    reason="联网 smoke 默认跳过, 设 AKSHARE_NETWORK_TESTS=1 启用",
)
class TestNbsSmokeNetwork:
    """NBS 联网测试. 验证基本 shape/dtype/schema, 不测固定值 (NBS 数据会更新)."""

    def test_nation_yearly_gdp(self):
        df = macro_china_nbs_nation(
            kind="年度数据",
            path="国民经济核算 > 国内生产总值",
            period="LAST5",
        )
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] >= 3  # GDP catalog 下指标数
        assert df.shape[1] == 5
        # 列降序 (最新在前)
        col_years = [int(c.replace("年", "")) for c in df.columns]
        assert col_years == sorted(col_years, reverse=True)
        assert df.values.dtype.kind in "fi"  # numeric

    def test_region_mode_a_loop_provinces(self):
        df = macro_china_nbs_region(
            kind="分省季度数据",
            path="国民经济核算 > 地区生产总值",
            indicator="地区生产总值累计值(亿元)",
            period="LAST3",
        )
        assert df.shape[0] >= 30  # 31 省级单位
        assert df.shape[1] >= 1
        assert df.columns.name == "地区生产总值累计值(亿元)"
        # 含非北京地区
        assert "天津市" in df.index
        assert "广东省" in df.index

    def test_region_mode_b_all_indicators(self):
        df = macro_china_nbs_region(
            kind="分省季度数据",
            path="国民经济核算 > 地区生产总值",
            region="河北省",
            period="LAST3",
        )
        assert df.shape[0] >= 1
        assert df.columns.name == "河北省"

    def test_region_mode_c_single(self):
        df = macro_china_nbs_region(
            kind="分省季度数据",
            path="国民经济核算 > 地区生产总值",
            indicator="地区生产总值累计值(亿元)",
            region="天津市",
            period="LAST3",
        )
        assert df.shape == (1, 3)
        assert df.columns.name == "天津市"

    def test_region_invalid_both_none(self):
        with pytest.raises(ValueError, match="不能同时为 None"):
            macro_china_nbs_region(
                kind="分省季度数据",
                path="国民经济核算 > 地区生产总值",
                period="LAST3",
            )

    def test_path_invalid_middle_node(self):
        with pytest.raises(ValueError, match="找不到"):
            macro_china_nbs_nation(
                kind="月度数据",
                path="不存在分类 > 不存在指标",
                period="LAST5",
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
