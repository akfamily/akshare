#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/3/4 20:00
Desc: Tests for ETF support in stock_zh_a_daily (stock_zh_a_sina.py)

Fixes verified:
1. ETF with null outstanding_share no longer crashes (fallback to 0.0)
2. Division-by-zero in turnover calculation is handled for ETFs
3. Extra columns (s, u) in ETF qfq/hfq factor data no longer cause column mismatch

Note: These tests make real network requests to the Sina Finance API.
      Run in a networked environment.
"""

import pandas as pd
import pytest

from akshare.stock.stock_zh_a_sina import stock_zh_a_daily

# ETF symbol that previously triggered all three bugs
ETF_SYMBOL = "sh512400"
# A normal A-share stock for regression testing
NORMAL_SYMBOL = "sh600000"


class TestETFNoAdjust:
    """ETF data without adjustment — verifies null outstanding_share fix."""

    def test_returns_dataframe(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="")
        assert isinstance(df, pd.DataFrame), "Should return a DataFrame"
        assert not df.empty, "DataFrame should not be empty"

    def test_has_required_columns(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="")
        required = {
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "outstanding_share",
            "turnover",
        }
        assert required.issubset(df.columns), (
            f"Missing columns: {required - set(df.columns)}"
        )

    def test_turnover_is_zero_for_etf(self):
        """ETFs have no outstanding_share, so turnover must be 0.0 (not NaN or inf)."""
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="")
        assert (df["turnover"] == 0.0).all(), (
            "ETF turnover should be 0.0 when outstanding_share is unavailable"
        )

    def test_no_inf_or_nan_in_numeric_columns(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="")
        numeric_cols = df.select_dtypes(include="number").columns
        assert not df[numeric_cols].isin([float("inf"), float("-inf")]).any().any(), (
            "No infinite values allowed"
        )
        # outstanding_share and turnover may be 0 but not NaN
        assert df["turnover"].notna().all(), "turnover should not contain NaN"


class TestETFHfq:
    """ETF with back-adjustment (hfq) — verifies extra-column fix for hfq factor data."""

    def test_does_not_crash(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="hfq")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_has_close_column(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="hfq")
        assert "close" in df.columns

    def test_close_is_numeric(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="hfq")
        assert pd.api.types.is_float_dtype(df["close"]), "close should be float"


class TestETFQfq:
    """ETF with forward-adjustment (qfq) — verifies extra-column fix for qfq factor data."""

    def test_does_not_crash(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="qfq")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_has_close_column(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="qfq")
        assert "close" in df.columns

    def test_close_is_numeric(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="qfq")
        assert pd.api.types.is_float_dtype(df["close"]), "close should be float"


class TestETFFactorOnly:
    """ETF factor-only modes — verifies column fix inside _fq_factor()."""

    def test_hfq_factor_returns_dataframe(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="hfq-factor")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_hfq_factor_has_correct_columns(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="hfq-factor")
        assert "hfq_factor" in df.columns
        assert "date" in df.columns

    def test_qfq_factor_returns_dataframe(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="qfq-factor")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_qfq_factor_has_correct_columns(self):
        df = stock_zh_a_daily(symbol=ETF_SYMBOL, adjust="qfq-factor")
        assert "qfq_factor" in df.columns
        assert "date" in df.columns


class TestNormalStockRegression:
    """Regression: normal A-share stocks should still work correctly."""

    def test_no_adjust_returns_data(self):
        df = stock_zh_a_daily(symbol=NORMAL_SYMBOL, adjust="")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_qfq_returns_data(self):
        df = stock_zh_a_daily(symbol=NORMAL_SYMBOL, adjust="qfq")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_hfq_returns_data(self):
        df = stock_zh_a_daily(symbol=NORMAL_SYMBOL, adjust="hfq")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_normal_stock_has_nonzero_turnover(self):
        """Normal stocks should have non-zero turnover rates."""
        df = stock_zh_a_daily(symbol=NORMAL_SYMBOL, adjust="")
        # At least some rows should have positive turnover
        assert (df["turnover"] > 0).any(), (
            "Normal stock should have positive turnover for at least some days"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
