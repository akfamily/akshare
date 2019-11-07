# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/20 10:21
contact: jindaxiang@163.com
desc: 债券配置文件
"""
# headers
SHORT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}

# quote
MARKET_QUOTE_URL = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbMktMakQuot?flag=1&lang=cn&abdAssetEncdShrtDesc=&emaEntyEncdShrtDesc="
MARKET_QUOTE_PAYLOAD = {
    "flag": "1",
    "lang": "cn",
    "abdAssetEncdShrtDesc": "",
    "emaEntyEncdShrtDesc": "",
}

# trade
MARKET_TRADE_URL = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbtPri?lang=cn&flag=1&bondName="
MARKET_TRADE_PAYLOAD = {
    "lang": "cn",
    "flag": "1",
    "bondName": ""
}
