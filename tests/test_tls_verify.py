#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 证书校验相关测试

1.20.16 起不再关闭任何请求的证书校验（verify=False，由 Ruff 的 S501 规则禁止）。唯一证书
不完整的站点 www.swsresearch.com 只发送站点证书、不发送中间证书，改为随包附带该中间证书，
在 certifi 的根证书之外加载。这里确认该文件随包发布、能被 ssl 加载，且适配器只挂在该站点。
全程不联网。
"""

import ssl
import tomllib
from pathlib import Path

import certifi

from akshare.datasets import get_data_file
from akshare.index.index_research_sw import _IntermediateCAAdapter, _sw_session

ROOT = Path(__file__).resolve().parent.parent


def test_intermediate_certificate_is_bundled_and_loadable():
    path = Path(get_data_file("swsresearch_intermediate.pem"))
    text = path.read_text(encoding="ascii")
    assert text.count("-----BEGIN CERTIFICATE-----") == 1
    ctx = ssl.create_default_context(cafile=certifi.where())
    before = ctx.cert_store_stats()["x509_ca"]
    ctx.load_verify_locations(cafile=str(path))
    assert ctx.cert_store_stats()["x509_ca"] == before + 1


def test_pem_files_are_package_data():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "*.pem" in config["tool"]["setuptools"]["package-data"]["*"]


def test_adapter_is_mounted_only_for_swsresearch():
    session = _sw_session()
    assert isinstance(
        session.get_adapter("https://www.swsresearch.com/x"), _IntermediateCAAdapter
    )
    assert not isinstance(
        session.get_adapter("https://example.com/x"), _IntermediateCAAdapter
    )
