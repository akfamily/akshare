"""日出日落接口：上游返回 Cloudflare 质询页或城市名不对时应给出明确的报错。"""

from types import SimpleNamespace

import pytest

from akshare.alternative import alternative_sunrise_tad as module
from akshare.exceptions import APIError, InvalidParameterError

# 2026-11-25 实测 timeanddate.com 对程序访问返回的页面（节选）
CHALLENGE_HTML = (
    "<!DOCTYPE html><html lang=en><head><title>Just a moment&hellip;</title>"
    "</head><body></body></html>"
)

CITY_HTML = """
<table><tr><td>x</td></tr></table>
<table>
<tr><td>Beijing</td><td>-</td><td>-</td><td>Shanghai</td><td>-</td><td>-</td>
<td>Wuhan</td></tr>
</table>
<table>
<tr><td>Anshan</td><td>Baotou</td><td>Changchun</td><td>Dalian</td><td>Fuzhou</td></tr>
</table>
"""


def _response(text: str, status_code: int = 200):
    return SimpleNamespace(text=text, status_code=status_code)


@pytest.mark.parametrize(
    "func",
    [module.alternative_sunrise_daily_tad, module.alternative_sunrise_monthly_tad],
)
def test_cloudflare_challenge_raises_api_error(monkeypatch, func):
    monkeypatch.setattr(
        module.http, "get", lambda url, **kwargs: _response(CHALLENGE_HTML, 403)
    )
    with pytest.raises(APIError, match="timeanddate") as excinfo:
        func(date="20240428", city="beijing")
    assert excinfo.value.status_code == 403


@pytest.mark.parametrize(
    "func",
    [module.alternative_sunrise_daily_tad, module.alternative_sunrise_monthly_tad],
)
def test_unknown_city_raises_invalid_parameter(monkeypatch, func):
    monkeypatch.setattr(module.http, "get", lambda url, **kwargs: _response(CITY_HTML))
    with pytest.raises(InvalidParameterError, match="not_a_city"):
        func(date="20240428", city="not_a_city")
