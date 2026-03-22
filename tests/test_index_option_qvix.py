#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/03/22
Desc: index option QVIX daily functions unit tests
"""

import pandas as pd
import pytest

import akshare as ak


@pytest.fixture(params=[
    ("50ETF", ak.index_option_50etf_qvix),
    ("300ETF", ak.index_option_300etf_qvix),
    ("500ETF", ak.index_option_500etf_qvix),
    ("创业板", ak.index_option_cyb_qvix),
    ("科创板", ak.index_option_kcb_qvix),
    ("100ETF", ak.index_option_100etf_qvix),
    ("中证300", ak.index_option_300index_qvix),
    ("中证1000", ak.index_option_1000index_qvix),
    ("上证50", ak.index_option_50index_qvix),
])
def qvix_func(request):
    return request.param


def test_qvix_returns_dataframe(qvix_func):
    """Test that QVIX function returns a pandas DataFrame."""
    name, fn = qvix_func
    result = fn()
    assert isinstance(result, pd.DataFrame)


def test_qvix_has_expected_columns(qvix_func):
    """Test that QVIX DataFrame has expected columns."""
    name, fn = qvix_func
    result = fn()
    expected_columns = {"date", "open", "high", "low", "close"}
    assert set(result.columns) == expected_columns


def test_qvix_date_column_is_datetime(qvix_func):
    """Test that date column is datetime type (not datetime.date object)."""
    name, fn = qvix_func
    result = fn()
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_qvix_numeric_columns_are_float(qvix_func):
    """Test that open/high/low/close columns are numeric."""
    name, fn = qvix_func
    result = fn()
    for col in ["open", "high", "low", "close"]:
        assert pd.api.types.is_numeric_dtype(result[col])


def test_qvix_dataframe_not_empty(qvix_func):
    """Test that QVIX DataFrame is not empty."""
    name, fn = qvix_func
    result = fn()
    assert len(result) > 0


def test_qvix_close_is_valid_float(qvix_func):
    """Test that close column contains valid float values."""
    name, fn = qvix_func
    result = fn()
    assert result["close"].notna().any()
