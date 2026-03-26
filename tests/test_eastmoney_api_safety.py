#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/3/26
Desc: Tests for eastmoney ETF/futures API safety improvements.
Covers request_with_retry, safe .get() access patterns, and
graceful empty-DataFrame returns when upstream data is missing.
"""

from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
import requests

from akshare.utils.request import request_with_retry
from akshare.fund.fund_etf_em import (
    fund_etf_hist_em,
    fund_etf_hist_min_em,
    get_market_id,
)


# ---------------------------------------------------------------------------
# Helper: build a mock Response whose .json() returns the given dict
# ---------------------------------------------------------------------------
def _mock_response(json_data, status_code=200):
    resp = MagicMock(spec=requests.Response)
    resp.json.return_value = json_data
    resp.status_code = status_code
    resp.raise_for_status.return_value = None
    return resp


# ===========================================================================
# 1. request_with_retry — retry logic, backoff, exception propagation
# ===========================================================================
class TestRequestWithRetry:
    """Verify retry logic, backoff, and final-exception propagation."""

    @patch("akshare.utils.request.time.sleep", return_value=None)
    @patch("akshare.utils.request.requests.Session")
    def test_success_on_first_attempt(self, mock_session_cls, _sleep):
        mock_resp = _mock_response({"ok": True})
        session_inst = MagicMock()
        session_inst.get.return_value = mock_resp
        session_inst.__enter__ = MagicMock(return_value=session_inst)
        session_inst.__exit__ = MagicMock(return_value=False)
        mock_session_cls.return_value = session_inst

        resp = request_with_retry("https://example.com", params={"a": "1"}, timeout=10)

        assert resp.json() == {"ok": True}
        _sleep.assert_not_called()

    @patch("akshare.utils.request.time.sleep", return_value=None)
    @patch("akshare.utils.request.requests.Session")
    def test_success_after_transient_failure(self, mock_session_cls, _sleep):
        """First call raises ConnectionError, second succeeds."""
        good_resp = _mock_response({"ok": True})
        call_count = {"n": 0}

        def _side_effect():
            call_count["n"] += 1
            session = MagicMock()
            if call_count["n"] == 1:
                session.get.side_effect = requests.ConnectionError("transient")
            else:
                session.get.return_value = good_resp
            session.__enter__ = MagicMock(return_value=session)
            session.__exit__ = MagicMock(return_value=False)
            return session

        mock_session_cls.side_effect = _side_effect

        resp = request_with_retry(
            "https://example.com",
            max_retries=3,
            base_delay=0.01,
            random_delay_range=(0.0, 0.0),
        )
        assert resp.json() == {"ok": True}
        assert _sleep.call_count == 1

    @patch("akshare.utils.request.time.sleep", return_value=None)
    @patch("akshare.utils.request.requests.Session")
    def test_all_retries_exhausted_raises(self, mock_session_cls, _sleep):
        """When every attempt fails, the last exception is raised."""
        session = MagicMock()
        session.get.side_effect = requests.ConnectionError("down")
        session.__enter__ = MagicMock(return_value=session)
        session.__exit__ = MagicMock(return_value=False)
        mock_session_cls.return_value = session

        with pytest.raises(requests.ConnectionError, match="down"):
            request_with_retry(
                "https://example.com",
                max_retries=2,
                base_delay=0.01,
                random_delay_range=(0.0, 0.0),
            )
        assert _sleep.call_count == 1

    @patch("akshare.utils.request.time.sleep", return_value=None)
    @patch("akshare.utils.request.requests.Session")
    def test_max_retries_one_no_sleep(self, mock_session_cls, _sleep):
        """With max_retries=1, a single failure raises immediately without sleep."""
        session = MagicMock()
        session.get.side_effect = requests.Timeout("timeout")
        session.__enter__ = MagicMock(return_value=session)
        session.__exit__ = MagicMock(return_value=False)
        mock_session_cls.return_value = session

        with pytest.raises(requests.Timeout):
            request_with_retry(
                "https://example.com",
                max_retries=1,
                base_delay=0.01,
                random_delay_range=(0.0, 0.0),
            )
        _sleep.assert_not_called()


# ===========================================================================
# 2. get_market_id — pure function, Shanghai/Shenzhen classification
# ===========================================================================
class TestGetMarketId:
    """Verify Shanghai/Shenzhen market classification."""

    @pytest.mark.parametrize(
        "symbol, expected",
        [
            ("510300", 1),   # starts with 5 -> Shanghai
            ("600000", 1),   # starts with 6 -> Shanghai
            ("159707", 0),   # starts with 1 -> Shenzhen
            ("000001", 0),   # starts with 0 -> Shenzhen
            ("300001", 0),   # starts with 3 -> Shenzhen
            ("200001", 0),   # starts with 2 -> Shenzhen
            ("899050", 1),   # starts with 8 -> default Shanghai
        ],
    )
    def test_market_id_classification(self, symbol, expected):
        assert get_market_id(symbol) == expected


# ===========================================================================
# 3. fund_etf_hist_em — safe .get() and empty-DataFrame returns
# ===========================================================================
class TestFundEtfHistEm:
    """Tests for the daily/weekly/monthly ETF history endpoint."""

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_normal_response_returns_dataframe(self, mock_req):
        """A well-formed response with klines produces a non-empty DataFrame."""
        mock_req.return_value = _mock_response(
            {
                "data": {
                    "klines": [
                        "2025-01-02,1.000,1.050,1.060,0.990,10000,100000,6.00,5.00,0.050,1.20",
                        "2025-01-03,1.050,1.080,1.090,1.040,12000,120000,4.76,2.86,0.030,1.44",
                    ]
                }
            }
        )
        df = fund_etf_hist_em(symbol="510300", period="daily")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) == 2
        assert "日期" in df.columns
        assert "收盘" in df.columns

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_data_is_none_returns_empty(self, mock_req):
        """When upstream returns data=null, we get an empty DataFrame (no KeyError)."""
        mock_req.return_value = _mock_response({"data": None})
        df = fund_etf_hist_em(symbol="510300", period="daily")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_data_missing_key_returns_empty(self, mock_req):
        """When upstream response has no 'data' key at all."""
        mock_req.return_value = _mock_response({"rc": 0})
        df = fund_etf_hist_em(symbol="510300", period="daily")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_klines_is_none_returns_empty(self, mock_req):
        """data exists but klines is null."""
        mock_req.return_value = _mock_response({"data": {"klines": None}})
        df = fund_etf_hist_em(symbol="510300", period="daily")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_klines_empty_list_returns_empty(self, mock_req):
        """data.klines is an empty list (falsy)."""
        mock_req.return_value = _mock_response({"data": {"klines": []}})
        df = fund_etf_hist_em(symbol="510300", period="daily")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_keyerror_fallback_data_none(self, mock_req):
        """
        When the try block raises KeyError (e.g. json parsing issue),
        the except branch tries market_id=1 then falls back to market_id=0.
        Both paths use .get() safely.
        """
        call_count = {"n": 0}

        def _side_effect(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                resp = MagicMock()
                resp.json.side_effect = KeyError("simulated")
                return resp
            else:
                return _mock_response({"data": None})

        mock_req.side_effect = _side_effect
        df = fund_etf_hist_em(symbol="510300", period="daily")
        assert isinstance(df, pd.DataFrame)
        assert df.empty


# ===========================================================================
# 4. fund_etf_hist_min_em — period="1" (trends) and period!="1" (klines)
# ===========================================================================
class TestFundEtfHistMinEm:
    """Tests for intraday ETF history (minute bars)."""

    # --- period="1" branch (trends) ---

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period1_normal_response(self, mock_req):
        """period='1' with valid trends returns a DataFrame."""
        mock_req.return_value = _mock_response(
            {
                "data": {
                    "trends": [
                        "2025-03-10 09:31,1.000,1.010,1.015,0.998,5000,50000,1.005",
                    ]
                }
            }
        )
        df = fund_etf_hist_min_em(symbol="510300", period="1")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "时间" in df.columns

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period1_data_none_returns_empty(self, mock_req):
        """period='1': data=null -> empty DataFrame, no KeyError."""
        mock_req.return_value = _mock_response({"data": None})
        df = fund_etf_hist_min_em(symbol="510300", period="1")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period1_trends_none_returns_empty(self, mock_req):
        """period='1': data exists but trends=null -> empty DataFrame."""
        mock_req.return_value = _mock_response({"data": {"trends": None}})
        df = fund_etf_hist_min_em(symbol="510300", period="1")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period1_no_data_key_returns_empty(self, mock_req):
        """period='1': response lacks 'data' key entirely."""
        mock_req.return_value = _mock_response({"rc": 0})
        df = fund_etf_hist_min_em(symbol="510300", period="1")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    # --- period="5" branch (klines) ---

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period5_normal_response(self, mock_req):
        """period='5' with valid klines returns a DataFrame."""
        mock_req.return_value = _mock_response(
            {
                "data": {
                    "klines": [
                        "2025-03-10 09:35,1.000,1.010,1.015,0.998,5000,50000,1.50,1.00,0.010,0.60",
                    ]
                }
            }
        )
        df = fund_etf_hist_min_em(symbol="510300", period="5")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period5_data_none_returns_empty(self, mock_req):
        """period='5': data=null -> empty DataFrame."""
        mock_req.return_value = _mock_response({"data": None})
        df = fund_etf_hist_min_em(symbol="510300", period="5")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period5_klines_none_returns_empty(self, mock_req):
        """period='5': data.klines=null -> empty DataFrame."""
        mock_req.return_value = _mock_response({"data": {"klines": None}})
        df = fund_etf_hist_min_em(symbol="510300", period="5")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("akshare.fund.fund_etf_em.request_with_retry")
    def test_period5_klines_empty_returns_empty(self, mock_req):
        """period='5': data.klines=[] -> empty DataFrame."""
        mock_req.return_value = _mock_response({"data": {"klines": []}})
        df = fund_etf_hist_min_em(symbol="510300", period="5")
        assert isinstance(df, pd.DataFrame)
        assert df.empty


# ===========================================================================
# 5. futures_hist_em — safe .get() and empty-DataFrame returns
#
# The double-underscore helpers (__fetch_exchange_symbol_raw_em,
# __get_exchange_symbol_map) are module-level functions — Python does NOT
# name-mangle them. They live in the module __dict__ with their literal
# names. We patch __fetch_exchange_symbol_raw_em so the lru_cached
# __get_exchange_symbol_map populates from controlled test data.
# ===========================================================================
class TestFuturesHistEm:
    """
    Verify futures_hist_em returns an empty DataFrame gracefully
    when upstream data/klines are missing or null.
    """

    FAKE_EXCHANGE_DATA = [
        {
            "name": "热卷主连",
            "code": "hcm",
            "mktid": 113,
            "vcode": "hc",
            "vname": "热卷",
            "mktname": "上期所",
        }
    ]

    def _patch_and_call(self, api_json, symbol="热卷主连"):
        """Patch network calls, invoke futures_hist_em, return result."""
        import akshare.futures.futures_hist_em as mod

        # Clear lru_caches so mocks take effect each test
        for key in list(mod.__dict__):
            fn = mod.__dict__[key]
            if callable(fn) and hasattr(fn, "cache_clear"):
                if "exchange_symbol" in key or "get_exchange_symbol_map" in key:
                    fn.cache_clear()

        # Locate the actual attribute name for __fetch_exchange_symbol_raw_em
        fetch_name = None
        for key in mod.__dict__:
            if "fetch_exchange_symbol_raw_em" in key:
                fetch_name = key
                break

        with patch.object(mod, fetch_name, return_value=self.FAKE_EXCHANGE_DATA):
            with patch("akshare.futures.futures_hist_em.request_with_retry") as mock_req:
                mock_req.return_value = _mock_response(api_json)
                from akshare.futures.futures_hist_em import futures_hist_em
                return futures_hist_em(symbol=symbol, period="daily")

    def test_normal_klines_returns_dataframe(self):
        kline_row = "2025-01-02,100.0,105.0,106.0,99.0,1000,100000,0,5.00,5.0,0,0,500,0"
        df = self._patch_and_call({"data": {"klines": [kline_row]}})
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "时间" in df.columns
        assert "收盘" in df.columns

    def test_data_none_returns_empty(self):
        df = self._patch_and_call({"data": None})
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_data_key_missing_returns_empty(self):
        df = self._patch_and_call({"rc": 0})
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_klines_none_returns_empty(self):
        df = self._patch_and_call({"data": {"klines": None}})
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_klines_empty_list_returns_empty(self):
        df = self._patch_and_call({"data": {"klines": []}})
        assert isinstance(df, pd.DataFrame)
        assert df.empty


# ===========================================================================
# 6. __fetch_exchange_symbol_raw_em — Session reuse + empty-page skip
# ===========================================================================
class TestFetchExchangeSymbolRawEm:
    """Verify session-based fetching skips empty page_data."""

    def _get_unwrapped_fetch_fn(self):
        """Return the unwrapped (non-cached) __fetch_exchange_symbol_raw_em."""
        import akshare.futures.futures_hist_em as mod

        for key in list(mod.__dict__):
            if "fetch_exchange_symbol_raw_em" in key:
                fn = mod.__dict__[key]
                if hasattr(fn, "cache_clear"):
                    fn.cache_clear()
                return fn.__wrapped__ if hasattr(fn, "__wrapped__") else fn
        raise RuntimeError("Could not locate __fetch_exchange_symbol_raw_em")

    def test_empty_page_data_is_skipped(self):
        """Empty page responses must not be appended to the result list."""
        mock_session = MagicMock()
        call_sequence = [
            _mock_response([{"mktid": 100}]),                          # gnweb
            _mock_response([{"dummy": 1}, {"dummy": 2}]),              # mktid=100 -> 2 pages
            _mock_response([{"name": "A", "code": "a", "mktid": 100,
                             "vcode": "a", "vname": "AA", "mktname": "X"}]),  # 100_1
            _mock_response([]),                                        # 100_2 (empty, skip)
        ]
        mock_session.get.side_effect = call_sequence
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)

        fn = self._get_unwrapped_fetch_fn()
        with patch("akshare.futures.futures_hist_em.requests.Session", return_value=mock_session):
            result = fn()

        assert len(result) == 1
        assert result[0]["name"] == "A"

    def test_multiple_exchanges_aggregated(self):
        """Data from multiple exchanges must be merged into a single list."""
        mock_session = MagicMock()
        call_sequence = [
            _mock_response([{"mktid": 100}, {"mktid": 200}]),  # gnweb: 2 exchanges
            _mock_response([{"x": 1}]),                         # mktid=100 -> 1 page
            _mock_response([{"name": "A", "code": "a"}]),       # 100_1
            _mock_response([{"x": 1}]),                         # mktid=200 -> 1 page
            _mock_response([{"name": "B", "code": "b"}]),       # 200_1
        ]
        mock_session.get.side_effect = call_sequence
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)

        fn = self._get_unwrapped_fetch_fn()
        with patch("akshare.futures.futures_hist_em.requests.Session", return_value=mock_session):
            result = fn()

        assert len(result) == 2
        assert result[0]["name"] == "A"
        assert result[1]["name"] == "B"

    def test_single_exchange_no_varieties(self):
        """An exchange with zero variety pages produces an empty result."""
        mock_session = MagicMock()
        call_sequence = [
            _mock_response([{"mktid": 100}]),   # gnweb: 1 exchange
            _mock_response([]),                   # mktid=100 -> 0 pages (len=0)
        ]
        mock_session.get.side_effect = call_sequence
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)

        fn = self._get_unwrapped_fetch_fn()
        with patch("akshare.futures.futures_hist_em.requests.Session", return_value=mock_session):
            result = fn()

        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
