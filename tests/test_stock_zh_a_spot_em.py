#!/usr/bin/env python
# -*- coding:utf-8 -*-

import inspect
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import pytest
import requests

from akshare.stock_feature import stock_hist_em


class _FakeResponse:
    def __init__(self, payload=None, error=None):
        self._payload = payload
        self._error = error

    def raise_for_status(self):
        if self._error is not None:
            raise self._error

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


class _FakeSession:
    def __init__(self, handler):
        self._handler = handler
        self.calls = []
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.closed = True

    def get(self, url, params, timeout):
        self.calls.append((url, params.copy(), timeout))
        return self._handler(url, params)


def _make_row(code, market=0, pct_chg=0.0):
    return {
        "f1": 2,
        "f2": "10.20",
        "f3": str(pct_chg),
        "f4": "0.20",
        "f5": "1000",
        "f6": "10200",
        "f7": "2.50",
        "f8": "1.20",
        "f9": "12.30",
        "f10": "1.10",
        "f11": "0.30",
        "f12": code,
        "f13": market,
        "f14": f"股票{code}",
        "f15": "10.50",
        "f16": "9.90",
        "f17": "10.00",
        "f18": "10.00",
        "f20": "1000000",
        "f21": "800000",
        "f22": "0.10",
        "f23": "1.50",
        "f24": "5.20",
        "f25": "8.30",
    }


@pytest.fixture(autouse=True)
def _reset_stock_zh_a_spot_cache(monkeypatch):
    for market in stock_hist_em._ZH_A_SPOT_MARKET_FS:
        monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHED_SECIDS, market, ())
        monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHE_EXPIRES_AT, market, 0.0)
        monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHE_VERSION, market, 0)
    monkeypatch.setattr(stock_hist_em.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(
        stock_hist_em,
        "get_tqdm",
        lambda: lambda iterable, **_kwargs: iterable,
    )


def _set_valid_cache(monkeypatch, secids, version=1, market="zh"):
    monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHED_SECIDS, market, tuple(secids))
    monkeypatch.setitem(
        stock_hist_em._ZH_A_SPOT_CACHE_EXPIRES_AT,
        market,
        time.monotonic() + 3600,
    )
    monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHE_VERSION, market, version)


@pytest.mark.parametrize(
    "interface",
    [
        stock_hist_em.stock_zh_a_spot_em,
        stock_hist_em.stock_sh_a_spot_em,
        stock_hist_em.stock_sz_a_spot_em,
        stock_hist_em.stock_bj_a_spot_em,
    ],
)
def test_stock_a_spot_em_keeps_public_signature(interface):
    signature = inspect.signature(interface)
    assert not signature.parameters
    assert signature.return_annotation is pd.DataFrame


@pytest.mark.parametrize(
    ("interface", "market", "code", "market_id"),
    [
        (stock_hist_em.stock_sh_a_spot_em, "sh", "600000", 1),
        (stock_hist_em.stock_sz_a_spot_em, "sz", "000001", 0),
        (stock_hist_em.stock_bj_a_spot_em, "bj", "920992", 0),
    ],
)
def test_market_spot_interfaces_reuse_cold_and_warm_paths(
    monkeypatch, interface, market, code, market_id
):
    calls = []

    def handler(url, params):
        calls.append((url, params.copy()))
        row = _make_row(code, market_id)
        if url == stock_hist_em._ZH_A_SPOT_URL:
            assert params["fs"] == stock_hist_em._ZH_A_SPOT_MARKET_FS[market]
            return _FakeResponse({"data": {"total": 1, "diff": [row]}})
        assert url == stock_hist_em._ZH_A_SPOT_BATCH_URL
        assert params["secids"] == f"{market_id}.{code}"
        return _FakeResponse({"data": {"diff": [row]}})

    monkeypatch.setattr(
        stock_hist_em,
        "_create_stock_zh_a_spot_session",
        lambda: _FakeSession(handler),
    )

    cold_result = interface()
    warm_result = interface()

    assert cold_result["代码"].tolist() == [code]
    assert warm_result["代码"].tolist() == [code]
    assert list(cold_result.columns) == stock_hist_em._ZH_A_SPOT_COLUMNS
    assert [url for url, _params in calls] == [
        stock_hist_em._ZH_A_SPOT_URL,
        stock_hist_em._ZH_A_SPOT_BATCH_URL,
    ]


def test_stock_zh_a_spot_em_cold_path_reuses_one_session(monkeypatch):
    pages = {
        "1": [_make_row("000001", pct_chg=-1), _make_row("600000", 1, 2)],
        "2": [_make_row("000002", pct_chg=0.5)],
    }

    def handler(url, params):
        assert url == stock_hist_em._ZH_A_SPOT_URL
        return _FakeResponse({"data": {"total": 3, "diff": pages[params["pn"]]}})

    session = _FakeSession(handler)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    result = stock_hist_em.stock_zh_a_spot_em()

    assert session.closed
    assert len(session.calls) == 2
    assert list(result.columns) == stock_hist_em._ZH_A_SPOT_COLUMNS
    assert result["序号"].tolist() == [1, 2, 3]
    assert result["代码"].tolist() == ["600000", "000002", "000001"]
    assert result["涨跌幅"].tolist() == [2.0, 0.5, -1.0]
    for column in stock_hist_em._ZH_A_SPOT_NUMERIC_COLUMNS:
        assert pd.api.types.is_numeric_dtype(result[column])
    assert stock_hist_em._ZH_A_SPOT_CACHED_SECIDS["zh"] == (
        "0.000001",
        "1.600000",
        "0.000002",
    )


def test_stock_zh_a_spot_em_falls_back_and_keeps_working_host(monkeypatch):
    pages = {
        "1": [_make_row("000001")],
        "2": [_make_row("600000", 1)],
    }

    def handler(url, params):
        if url == stock_hist_em._ZH_A_SPOT_URL:
            raise requests.ConnectionError("connection reset")
        assert url == stock_hist_em._ZH_A_SPOT_URLS[1]
        return _FakeResponse({"data": {"total": 2, "diff": pages[params["pn"]]}})

    session = _FakeSession(handler)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    result = stock_hist_em.stock_zh_a_spot_em()

    assert result["代码"].tolist() == ["000001", "600000"]
    assert [call[0] for call in session.calls] == [
        stock_hist_em._ZH_A_SPOT_URL,
        stock_hist_em._ZH_A_SPOT_URLS[1],
        stock_hist_em._ZH_A_SPOT_URLS[1],
    ]


def test_stock_zh_a_spot_em_reaches_second_fallback_host(monkeypatch):
    def handler(url, _params):
        if url != stock_hist_em._ZH_A_SPOT_URLS[2]:
            raise requests.ConnectionError("connection reset")
        return _FakeResponse({"data": {"total": 1, "diff": [_make_row("000001")]}})

    session = _FakeSession(handler)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    result = stock_hist_em.stock_zh_a_spot_em()

    assert result["代码"].tolist() == ["000001"]
    assert [call[0] for call in session.calls] == list(stock_hist_em._ZH_A_SPOT_URLS)


def test_stock_zh_a_spot_em_warm_path_batches_500_secids(monkeypatch):
    rows_by_secid = {}
    for index in range(501):
        market = index % 2
        code = f"{index:06d}"
        rows_by_secid[f"{market}.{code}"] = _make_row(code, market, index)
    secids = tuple(rows_by_secid)
    _set_valid_cache(monkeypatch, secids)

    def handler(url, params):
        assert url == stock_hist_em._ZH_A_SPOT_BATCH_URL
        batch = params["secids"].split(",")
        return _FakeResponse(
            {"data": {"diff": [rows_by_secid[secid] for secid in batch]}}
        )

    session = _FakeSession(handler)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    result = stock_hist_em.stock_zh_a_spot_em()

    assert len(result) == 501
    assert [len(call[1]["secids"].split(",")) for call in session.calls] == [500, 1]
    assert all(call[0] == stock_hist_em._ZH_A_SPOT_BATCH_URL for call in session.calls)


def test_stock_zh_a_spot_em_refreshes_expired_cache(monkeypatch):
    monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHED_SECIDS, "zh", ("0.000001",))
    monkeypatch.setitem(
        stock_hist_em._ZH_A_SPOT_CACHE_EXPIRES_AT,
        "zh",
        time.monotonic() - 1,
    )
    monkeypatch.setitem(stock_hist_em._ZH_A_SPOT_CACHE_VERSION, "zh", 4)

    def handler(url, _params):
        assert url == stock_hist_em._ZH_A_SPOT_URL
        return _FakeResponse({"data": {"total": 1, "diff": [_make_row("600000", 1)]}})

    session = _FakeSession(handler)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    result = stock_hist_em.stock_zh_a_spot_em()

    assert result["代码"].tolist() == ["600000"]
    assert [call[0] for call in session.calls] == [stock_hist_em._ZH_A_SPOT_URL]
    assert stock_hist_em._ZH_A_SPOT_CACHED_SECIDS["zh"] == ("1.600000",)
    assert stock_hist_em._ZH_A_SPOT_CACHE_VERSION["zh"] == 5


def test_stock_zh_a_spot_em_refreshes_stale_code_cache(monkeypatch):
    _set_valid_cache(monkeypatch, ("0.000001", "1.600000"), version=3)

    def handler(url, _params):
        if url == stock_hist_em._ZH_A_SPOT_BATCH_URL:
            return _FakeResponse({"data": {"diff": [_make_row("000001")]}})
        return _FakeResponse({"data": {"total": 1, "diff": [_make_row("000002")]}})

    session = _FakeSession(handler)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    result = stock_hist_em.stock_zh_a_spot_em()

    assert result["代码"].tolist() == ["000002"]
    assert [call[0] for call in session.calls] == [
        stock_hist_em._ZH_A_SPOT_BATCH_URL,
        stock_hist_em._ZH_A_SPOT_URL,
    ]
    assert stock_hist_em._ZH_A_SPOT_CACHED_SECIDS["zh"] == ("0.000002",)


@pytest.mark.parametrize(
    "response",
    [
        _FakeResponse(error=requests.HTTPError("403 Client Error")),
        _FakeResponse(error=requests.HTTPError("429 Client Error")),
    ],
)
def test_stock_zh_a_spot_em_does_not_switch_hosts_on_access_errors(
    monkeypatch, response
):
    _set_valid_cache(monkeypatch, ("0.000001",))
    session = _FakeSession(lambda _url, _params: response)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    with pytest.raises((requests.RequestException, ValueError)):
        stock_hist_em.stock_zh_a_spot_em()

    assert len(session.calls) == 1
    assert session.calls[0][0] == stock_hist_em._ZH_A_SPOT_BATCH_URL


@pytest.mark.parametrize(
    "response",
    [
        _FakeResponse(error=requests.ConnectionError("connection reset")),
        _FakeResponse(payload=ValueError("invalid json")),
    ],
)
def test_stock_zh_a_spot_em_tries_all_hosts_on_transient_errors(monkeypatch, response):
    _set_valid_cache(monkeypatch, ("0.000001",))
    session = _FakeSession(lambda _url, _params: response)
    monkeypatch.setattr(
        stock_hist_em, "_create_stock_zh_a_spot_session", lambda: session
    )

    with pytest.raises((requests.RequestException, ValueError)):
        stock_hist_em.stock_zh_a_spot_em()

    assert [call[0] for call in session.calls] == list(
        stock_hist_em._ZH_A_SPOT_BATCH_URLS
    )


def test_stock_zh_a_spot_em_cold_refresh_is_singleflight(monkeypatch):
    calls = []
    calls_lock = threading.Lock()

    def handler(url, params):
        with calls_lock:
            calls.append((url, params.copy()))
        if url == stock_hist_em._ZH_A_SPOT_URL:
            return _FakeResponse({"data": {"total": 1, "diff": [_make_row("000001")]}})
        return _FakeResponse({"data": {"diff": [_make_row("000001")]}})

    monkeypatch.setattr(
        stock_hist_em,
        "_create_stock_zh_a_spot_session",
        lambda: _FakeSession(handler),
    )
    barrier = threading.Barrier(2)

    def fetch():
        barrier.wait()
        return stock_hist_em.stock_zh_a_spot_em()

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: fetch(), range(2)))

    assert all(result["代码"].tolist() == ["000001"] for result in results)
    assert sum(url == stock_hist_em._ZH_A_SPOT_URL for url, _params in calls) == 1
    assert sum(url == stock_hist_em._ZH_A_SPOT_BATCH_URL for url, _params in calls) == 1


def test_stock_zh_a_spot_session_has_bounded_get_retries():
    session = stock_hist_em._create_stock_zh_a_spot_session()
    retry = session.adapters["https://"].max_retries
    try:
        assert retry.total == 3
        assert retry.allowed_methods == frozenset({"GET"})
        assert retry.status_forcelist == (429, 500, 502, 503, 504)
        assert retry.respect_retry_after_header
    finally:
        session.close()
