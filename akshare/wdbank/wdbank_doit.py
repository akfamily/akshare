# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/3/17 20:57
contact: jindaxiang@163.com
desc: world bank interface test file
"""
from akshare import wdbank

wdbank.get_source()
wdbank.get_data("NY.GDP.PCAP.PP.CD", country=["CHN", "USA"])
