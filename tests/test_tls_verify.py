#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/1
Desc: 证书校验相关测试

除申万宏源研究外，所有请求都校验证书（verify=False 由 Ruff 的 S501 规则禁止）。
www.swsresearch.com 只发送站点证书、不发送中间证书，无法校验，1.20.19 起只对访问该站点的
会话关闭校验（session.verify = False，S501 检查不到这种写法）。这里确认该例外只限于这一个
会话，没有扩散到其他模块。全程不联网。
"""

import re
from pathlib import Path

from akshare.index.index_research_sw import _sw_session
from akshare.utils import http

ROOT = Path(__file__).resolve().parent.parent

_VERIFY_OFF = re.compile(r"verify\s*=\s*False")


def test_only_swsresearch_session_disables_verification():
    assert _sw_session().verify is False
    assert http.Session().verify is True


def test_verify_false_appears_only_in_swsresearch_module():
    hits = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "akshare").rglob("*.py")
        if _VERIFY_OFF.search(path.read_text(encoding="utf-8"))
    )
    assert hits == ["akshare/index/index_research_sw.py"]
