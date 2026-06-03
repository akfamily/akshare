#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd

from akshare.utils import func as utils_func


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def test_fetch_paginated_data_empty_result(monkeypatch):
    def fake_request_with_retry(url, params, timeout):
        return _Response({"data": {"diff": [], "total": 0}})

    monkeypatch.setattr(utils_func, "request_with_retry", fake_request_with_retry)

    result = utils_func.fetch_paginated_data("https://example.test/api", {"pn": 1})

    assert isinstance(result, pd.DataFrame)
    assert result.empty
