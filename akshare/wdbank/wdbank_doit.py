#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/3/17 20:57
Desc: world bank interface test file
"""
from akshare import wdbank

wdbank.get_source()
wdbank.get_data("NY.GDP.PCAP.PP.CD", country=["CHN", "USA"])
