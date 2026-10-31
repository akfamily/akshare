"""验证沪深清单解析、跨市场估值及完整证券篮子的占比。"""

from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring

import pandas as pd
import pytest
import requests

import akshare as ak
from akshare.exceptions import DataParsingError, InvalidParameterError
from akshare.fund import fund_etf_pcf as module


def xml_content(szse=False, components=None, encoding="utf-8"):
    root = Element("PCFFile" if szse else "SSEPortfolioCompositionFile")
    if szse:
        root.set("xmlns", "http://ts.szse.cn/Fund")
    metadata = {
        "SecurityID" if szse else "FundInstrumentID": "159502" if szse else "510300",
        "CreationRedemptionUnit": "900000",
        "NAVperCU": "3600000",
        "TradingDay": "20261029",
        "CashComponent" if szse else "PreCashComponent": "-1200",
        "EstimateCashComponent" if szse else "EstimatedCashComponent": "1000",
    }
    for tag, value in metadata.items():
        SubElement(root, tag).text = value
    parent = SubElement(root, "Components" if szse else "ComponentList")
    tags = (
        [
            "UnderlyingSecurityID",
            "UnderlyingSymbol",
            "UnderlyingSecurityIDSource",
            "ComponentShare",
            "SubstituteFlag",
            "CreationCashSubstitute",
        ]
        if szse
        else [
            "InstrumentID",
            "InstrumentName",
            "UnderlyingSecurityID",
            "Quantity",
            "SubstitutionFlag",
            "SubstitutionCashAmount",
        ]
    )
    for values in components or [("000001", "平安银行", "102", "100", "1", "1000")]:
        row = SubElement(parent, "Component")
        for tag, value in zip(tags, values):
            SubElement(row, tag).text = value
    # 实际文件可能以 GB18030 编码并声明 UTF-8。
    return (
        '<?xml version="1.0" encoding="UTF-8"?>' + tostring(root, encoding="unicode")
    ).encode(encoding)


def response(content):
    result = requests.Response()
    result.status_code = 200
    result._content = content
    return result


@pytest.mark.parametrize(
    "szse,encoding", [(False, "utf-8"), (False, "gb18030"), (True, "utf-8")]
)
def test_parse(szse, encoding):
    df = module._parse_pcf(
        xml_content(szse, encoding=encoding), "159502" if szse else "510300", szse
    )
    assert df.loc[0, "证券代码"] == "000001"
    assert df.loc[0, "证券简称"] == "平安银行"
    assert df.loc[0, "交易日期"] == date(2026, 10, 29)
    assert df.loc[0, "现金差额"] == -1200
    assert df.loc[0, "证券数量"] == 100
    assert pd.isna(df.loc[0, "申购溢价比例"])


def test_latest_szse_and_public_exports(monkeypatch):
    calls = []

    def get(url, **kwargs):
        calls.append((url, kwargs))
        if "ShowReport" in url:
            return response(
                b'[{"data":[{"jjdm":"pcf_159502_20261023"},{"jjdm":"pcf_159502_20261029"}]}]'
            )
        return response(xml_content(True))

    monkeypatch.setattr(module.http, "get", get)
    assert ak.fund_etf_pcf("159502").loc[0, "基金代码"] == "159502"
    assert calls[-1][0].endswith("pcf_159502_20261029.xml")
    assert callable(ak.fund_etf_holdings_tx)


@pytest.mark.parametrize("symbol", ["600519", "sh510300", "15950", "510300x"])
def test_invalid_symbol(symbol):
    with pytest.raises(InvalidParameterError):
        ak.fund_etf_pcf(symbol)


@pytest.mark.parametrize(
    "content",
    [
        b"<html>",
        b"<PCFFile/>",
        xml_content().replace(b">100<", b">NaN<"),
        xml_content().replace(b">100<", b">-1<"),
    ],
)
def test_invalid_pcf(content):
    with pytest.raises(DataParsingError):
        module._parse_pcf(content, "510300", False)


def basket(monkeypatch):
    content = xml_content(
        True,
        components=[
            ("159900", "申赎现金", "102", "0", "2", "999999"),
            ("600519", "贵州茅台", "101", "1", "1", "0"),
            ("700", "腾讯控股", "103", "2", "1", "0"),
            ("BRK.B", "伯克希尔", "9999", "1", "1", "0"),
            ("ZERO", "零数量", "9999", "0", "1", "0"),
            ("FIXED", "现金替代", "9999", "0", "2", "1000"),
        ],
    )
    df = module._parse_pcf(content, "159502", True)
    monkeypatch.setattr(module, "fund_etf_pcf", lambda symbol: df)
    return df


def quote_mock(monkeypatch, missing=None):
    prices = {
        "sh600519": 1600,
        "hk00700": 100,
        "usBRK_B": 200,
        "whUSDCNY": 7,
        "whHKDCNY": 0.9,
    }
    calls = []

    def get(url, **kwargs):
        symbols = url.split("q=")[1].split(",")
        calls.extend(symbols)
        return response(
            "\n".join(
                f'v_{symbol}="1~name~code~{prices[symbol]}";'
                for symbol in symbols
                if symbol in prices and symbol != missing
            ).encode()
        )

    monkeypatch.setattr(module.http, "get", get)
    return calls


def test_complete_basket_valuation(monkeypatch):
    basket(monkeypatch)
    calls = quote_mock(monkeypatch)
    df = ak.fund_etf_holdings_tx("159502")
    assert df["证券代码"].tolist() == ["600519", "BRK.B", "FIXED", "700", "ZERO"]
    assert df["市值"].tolist() == [1600, 1400, 1000, 180, 0]
    assert df["市值占比"].sum() == pytest.approx(100)
    assert df.loc[0, "市值占比"] == pytest.approx(1600 / 4180 * 100)
    assert df.loc[2, "估值方式"] == "现金替代"
    assert "usFIXED" not in calls
    assert "usZERO" not in calls


@pytest.mark.parametrize("missing", ["usBRK_B", "whUSDCNY", "whHKDCNY"])
def test_incomplete_valuation_raises(monkeypatch, missing):
    basket(monkeypatch)
    quote_mock(monkeypatch, missing)
    with pytest.raises(DataParsingError):
        ak.fund_etf_holdings_tx("159502")


def test_fixed_cash_uses_cny_without_fx(monkeypatch):
    df = basket(monkeypatch).iloc[[5]].copy()
    monkeypatch.setattr(module, "fund_etf_pcf", lambda symbol: df)
    calls = quote_mock(monkeypatch)
    result = ak.fund_etf_holdings_tx("159502")
    assert result.loc[0, "市值"] == 1000
    assert result.loc[0, "市值占比"] == 100
    assert calls == []


def test_quote_batching(monkeypatch):
    batches = []

    def get(url, **kwargs):
        batches.append(url.split("q=")[1].split(","))
        return response(b'v_sh000001="1~name~000001~10";')

    monkeypatch.setattr(module.http, "get", get)
    result = module._quote_prices(
        [f"sh{index:06}" for index in range(101)] + ["sh000001"]
    )
    assert list(map(len, batches)) == [50, 50, 1]
    assert result["sh000001"] == 10


def test_sse_request_and_cny_valuation(monkeypatch):
    calls = []

    def get(url, **kwargs):
        calls.append((url, kwargs))
        if "downloadETF" in url:
            return response(xml_content(encoding="gb18030"))
        return response(b'v_sz000001="1~name~000001~10";')

    monkeypatch.setattr(module.http, "get", get)
    result = ak.fund_etf_holdings_tx("510300")
    assert result.loc[0, "市值"] == 1000
    assert result.loc[0, "人民币汇率"] == 1
    assert len(calls) == 2
    assert calls[0][1]["params"] == {"fundCode": "510300"}


def test_missing_announcement_and_http_error(monkeypatch):
    monkeypatch.setattr(
        module.http, "get", lambda *args, **kwargs: response(b'[{"data": []}]')
    )
    with pytest.raises(DataParsingError):
        ak.fund_etf_pcf("159502")
    failed = response(b"error")
    failed.status_code = 503
    monkeypatch.setattr(module.http, "get", lambda *args, **kwargs: failed)
    with pytest.raises(requests.HTTPError):
        ak.fund_etf_pcf("510300")


@pytest.mark.parametrize(
    "column,value",
    [
        ("申购替代金额", float("nan")),
        ("申购替代金额", -1),
        ("申购替代金额", float("inf")),
        ("市场代码", "999"),
        ("证券代码", "1234"),
    ],
)
def test_invalid_basket_raises(monkeypatch, column, value):
    df = basket(monkeypatch)
    df.loc[5, column] = value
    quote_mock(monkeypatch)
    with pytest.raises(DataParsingError):
        ak.fund_etf_holdings_tx("159502")


def test_zero_total_raises(monkeypatch):
    df = basket(monkeypatch).iloc[[4]]
    monkeypatch.setattr(module, "fund_etf_pcf", lambda symbol: df)
    with pytest.raises(DataParsingError):
        ak.fund_etf_holdings_tx("159502")


@pytest.mark.parametrize("value", ["NaN", "inf", "-1", "0"])
def test_invalid_fx_raises(monkeypatch, value):
    basket(monkeypatch)

    def get(url, **kwargs):
        symbols = url.split("q=")[1].split(",")
        return response(
            "\n".join(
                f'v_{symbol}="1~name~code~{value if symbol.startswith("wh") else "100"}";'
                for symbol in symbols
            ).encode()
        )

    monkeypatch.setattr(module.http, "get", get)
    with pytest.raises(DataParsingError):
        ak.fund_etf_holdings_tx("159502")
