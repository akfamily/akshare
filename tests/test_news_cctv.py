#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: news_cctv 标题与正文清洗测试

原先用 str.strip("[视频]") 与 str.strip("央视网消息（新闻联播）：") 去前缀。strip 的参数
是字符集合而不是前缀：以“视频”结尾的标题会被截掉末尾两个字，正文若以“新”“央”等
属于该集合的字开头也会被误删。全程不联网。
"""

import pytest

from akshare.alternative.alternative_news_cctv import _clean_content, _clean_title


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("[视频]习近平会见外宾", "习近平会见外宾"),
        ("[视频]这是一段视频", "这是一段视频"),
        ("  [视频]标题\n换行  ", "标题 换行"),
        ("没有标记的标题", "没有标记的标题"),
    ],
)
def test_clean_title(raw, expected):
    assert _clean_title(raw) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("央视网消息（新闻联播）：新时代新征程", "新时代新征程"),
        ("央视网消息(新闻联播)：央视记者报道", "央视记者报道"),
        ("（新闻联播）：视察工作", "视察工作"),
        ("(新闻联播)：联合国会议", "联合国会议"),
        ("  正文没有前缀\n第二段  ", "正文没有前缀 第二段"),
    ],
)
def test_clean_content(raw, expected):
    assert _clean_content(raw) == expected
