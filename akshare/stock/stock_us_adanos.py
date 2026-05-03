#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/05/03
Desc: Adanos Market Sentiment API-美股市场情绪数据
https://api.adanos.org
"""

import os

import pandas as pd
import requests

ADANOS_BASE_URL = "https://api.adanos.org"
ADANOS_SOURCES = {"reddit", "x", "news", "polymarket"}
ADANOS_REQUEST_TIMEOUT = 30


def _normalize_symbol(symbol: str) -> str:
    """
    规范化单个美股代码
    :param symbol: 美股代码
    :type symbol: str
    :return: 规范化后的美股代码
    :rtype: str
    """
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("symbol must not be empty.")
    return symbol


def _normalize_symbols(symbols: str) -> str:
    """
    规范化多个美股代码
    :param symbols: 英文逗号分隔的美股代码
    :type symbols: str
    :return: 规范化后的美股代码
    :rtype: str
    """
    normalized_symbols = ",".join(
        symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()
    )
    if not normalized_symbols:
        raise ValueError("symbols must contain at least one symbol.")
    return normalized_symbols


def _get_adanos_api_key(api_key: str = "") -> str:
    """
    获取 Adanos API Key
    :param api_key: Adanos API Key
    :type api_key: str
    :return: Adanos API Key
    :rtype: str
    """
    adanos_api_key = (api_key or os.getenv("ADANOS_API_KEY", "")).strip()
    if not adanos_api_key:
        raise ValueError("Please provide api_key or set ADANOS_API_KEY.")
    return adanos_api_key


def _validate_source(source: str) -> str:
    """
    校验 Adanos 数据源
    :param source: 数据源
    :type source: str
    :return: 数据源
    :rtype: str
    """
    source = source.strip().lower()
    if source not in ADANOS_SOURCES:
        raise ValueError("source must be one of: reddit, x, news, polymarket")
    return source


def _request_adanos(
    path: str,
    params: dict,
    api_key: str,
    base_url: str,
    timeout: int,
) -> dict:
    """
    请求 Adanos API
    :param path: API 路径
    :type path: str
    :param params: 请求参数
    :type params: dict
    :param api_key: Adanos API Key
    :type api_key: str
    :param base_url: API 地址
    :type base_url: str
    :param timeout: 超时时间
    :type timeout: int
    :return: JSON 数据
    :rtype: dict
    """
    url = f"{base_url.rstrip('/')}{path}"
    headers = {"X-API-Key": api_key, "Accept": "application/json"}
    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _flatten_stock(item: dict, source: str) -> dict:
    """
    展平单个股票情绪数据
    :param item: API 返回数据
    :type item: dict
    :param source: 数据源
    :type source: str
    :return: 展平后的数据
    :rtype: dict
    """
    return {
        "source": source,
        "ticker": item.get("ticker"),
        "company_name": item.get("company_name"),
        "buzz_score": item.get("buzz_score"),
        "trend": item.get("trend"),
        "sentiment_score": item.get("sentiment_score"),
        "mentions": item.get("mentions"),
        "unique_tweets": item.get("unique_tweets"),
        "trade_count": item.get("trade_count"),
        "market_count": item.get("market_count"),
        "unique_traders": item.get("unique_traders"),
        "total_liquidity": item.get("total_liquidity"),
        "positive_count": item.get("positive_count"),
        "negative_count": item.get("negative_count"),
        "neutral_count": item.get("neutral_count"),
        "bullish_pct": item.get("bullish_pct"),
        "bearish_pct": item.get("bearish_pct"),
        "period_days": item.get("period_days"),
        "trend_history": item.get("trend_history"),
    }


def stock_us_adanos_sentiment(
    symbol: str = "TSLA",
    source: str = "reddit",
    days: int = 7,
    api_key: str = "",
    base_url: str = ADANOS_BASE_URL,
    timeout: int = ADANOS_REQUEST_TIMEOUT,
) -> pd.DataFrame:
    """
    Adanos Market Sentiment API-美股个股市场情绪数据
    https://api.adanos.org
    :param symbol: 美股代码, 如: "TSLA"; 不需要添加交易所前缀
    :type symbol: str
    :param source: 数据源, 可选值: "reddit", "x", "news", "polymarket"
    :type source: str
    :param days: 最近 N 天数据
    :type days: int
    :param api_key: Adanos API Key; 也可以设置环境变量 ADANOS_API_KEY
    :type api_key: str
    :param base_url: Adanos API 地址
    :type base_url: str
    :param timeout: 请求超时时间
    :type timeout: int
    :return: 美股个股市场情绪数据
    :rtype: pandas.DataFrame
    """
    source = _validate_source(source)
    data_json = _request_adanos(
        path=f"/{source}/stocks/v1/stock/{_normalize_symbol(symbol)}",
        params={"days": days},
        api_key=_get_adanos_api_key(api_key),
        base_url=base_url,
        timeout=timeout,
    )
    temp_df = pd.DataFrame([_flatten_stock(data_json, source)])
    return temp_df


def stock_us_adanos_compare(
    symbols: str = "TSLA,NVDA,AAPL",
    source: str = "reddit",
    days: int = 7,
    api_key: str = "",
    base_url: str = ADANOS_BASE_URL,
    timeout: int = ADANOS_REQUEST_TIMEOUT,
) -> pd.DataFrame:
    """
    Adanos Market Sentiment API-美股多股票市场情绪对比
    https://api.adanos.org
    :param symbols: 英文逗号分隔的美股代码, 如: "TSLA,NVDA,AAPL"
    :type symbols: str
    :param source: 数据源, 可选值: "reddit", "x", "news", "polymarket"
    :type source: str
    :param days: 最近 N 天数据
    :type days: int
    :param api_key: Adanos API Key; 也可以设置环境变量 ADANOS_API_KEY
    :type api_key: str
    :param base_url: Adanos API 地址
    :type base_url: str
    :param timeout: 请求超时时间
    :type timeout: int
    :return: 美股多股票市场情绪对比
    :rtype: pandas.DataFrame
    """
    source = _validate_source(source)
    data_json = _request_adanos(
        path=f"/{source}/stocks/v1/compare",
        params={"tickers": _normalize_symbols(symbols), "days": days},
        api_key=_get_adanos_api_key(api_key),
        base_url=base_url,
        timeout=timeout,
    )
    temp_df = pd.DataFrame(
        [_flatten_stock(item, source) for item in data_json.get("stocks", [])]
    )
    return temp_df


if __name__ == "__main__":
    adanos_api_key = os.getenv("ADANOS_API_KEY", "")
    stock_us_adanos_sentiment_df = stock_us_adanos_sentiment(
        symbol="TSLA", source="reddit", api_key=adanos_api_key
    )
    print(stock_us_adanos_sentiment_df)

    stock_us_adanos_compare_df = stock_us_adanos_compare(
        symbols="TSLA,NVDA,AAPL", source="reddit", api_key=adanos_api_key
    )
    print(stock_us_adanos_compare_df)
