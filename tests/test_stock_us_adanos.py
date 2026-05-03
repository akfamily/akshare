#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/05/03
Desc: test stock_us_adanos.py
"""

from unittest.mock import Mock, patch

import pandas as pd
import pytest

from akshare.stock.stock_us_adanos import (
    stock_us_adanos_compare,
    stock_us_adanos_sentiment,
)


def test_stock_us_adanos_sentiment():
    """
    test stock_us_adanos_sentiment
    :return: None
    :rtype: None
    """
    mock_response = Mock()
    mock_response.json.return_value = {
        "ticker": "TSLA",
        "company_name": "Tesla Inc.",
        "buzz_score": 72.4,
        "trend": "rising",
        "sentiment_score": 0.31,
        "mentions": 128,
        "trend_history": [61.0, 66.0, 72.4],
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "akshare.stock.stock_us_adanos.requests.get", return_value=mock_response
    ) as mock_get:
        temp_df = stock_us_adanos_sentiment(
            symbol="tsla", source="reddit", days=3, api_key="test-key"
        )

    assert isinstance(temp_df, pd.DataFrame)
    assert temp_df.loc[0, "source"] == "reddit"
    assert temp_df.loc[0, "ticker"] == "TSLA"
    assert temp_df.loc[0, "buzz_score"] == 72.4
    assert temp_df.loc[0, "trend_history"] == [61.0, 66.0, 72.4]

    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {"days": 3}
    assert kwargs["headers"]["X-API-Key"] == "test-key"
    assert kwargs["timeout"] == 30


def test_stock_us_adanos_compare():
    """
    test stock_us_adanos_compare
    :return: None
    :rtype: None
    """
    mock_response = Mock()
    mock_response.json.return_value = {
        "stocks": [
            {
                "ticker": "TSLA",
                "company_name": "Tesla Inc.",
                "buzz_score": 72.4,
                "trend": "rising",
            },
            {
                "ticker": "NVDA",
                "company_name": "NVIDIA Corporation",
                "buzz_score": 68.2,
                "trend": "stable",
            },
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "akshare.stock.stock_us_adanos.requests.get", return_value=mock_response
    ) as mock_get:
        temp_df = stock_us_adanos_compare(
            symbols="tsla,nvda", source="news", days=7, api_key="test-key"
        )

    assert list(temp_df["ticker"]) == ["TSLA", "NVDA"]
    assert list(temp_df["source"]) == ["news", "news"]

    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {"tickers": "TSLA,NVDA", "days": 7}


def test_stock_us_adanos_invalid_source():
    """
    test stock_us_adanos invalid source
    :return: None
    :rtype: None
    """
    with pytest.raises(ValueError, match="source must be one of"):
        stock_us_adanos_sentiment(source="invalid", api_key="test-key")


def test_stock_us_adanos_requires_api_key(monkeypatch):
    """
    test stock_us_adanos requires api key
    :return: None
    :rtype: None
    """
    monkeypatch.delenv("ADANOS_API_KEY", raising=False)
    with pytest.raises(ValueError, match="Please provide api_key"):
        stock_us_adanos_compare(api_key="")


def test_stock_us_adanos_env_api_key(monkeypatch):
    """
    test stock_us_adanos uses environment api key
    :return: None
    :rtype: None
    """
    mock_response = Mock()
    mock_response.json.return_value = {"stocks": []}
    mock_response.raise_for_status.return_value = None
    monkeypatch.setenv("ADANOS_API_KEY", "env-key")

    with patch(
        "akshare.stock.stock_us_adanos.requests.get", return_value=mock_response
    ) as mock_get:
        stock_us_adanos_compare(api_key="")

    _, kwargs = mock_get.call_args
    assert kwargs["headers"]["X-API-Key"] == "env-key"
