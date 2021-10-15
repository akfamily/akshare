# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/5/27 20:19
Desc: 指数配置文件
"""
# weibo-user-agent
index_weibo_headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Referer": "http://data.weibo.com/index/newindex",
    "Accept": "application/json",
    "Origin": "https://data.weibo.com",
}

# sw-cons
sw_cons_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "34",
    "Content-Type": "text/plain; charset=UTF-8",
    # "Cookie": "ASP.NET_SessionId=i55eaz55142xdxfx0bkqp145",
    "Host": "www.swsindex.com",
    "Origin": "http://www.swsindex.com",
    "Referer": "http://www.swsindex.com/idx0210.aspx?swindexcode=801010",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "X-AjaxPro-Method": "ReturnContent",
}

# sw-url
sw_url = "http://www.swsindex.com/handler.aspx"

# sw-payload
sw_payload = {
    "tablename": "swzs",
    "key": "L1",
    "p": "1",
    "where": "L1 in('801010','801020','801030','801040','801050','801080','801110','801120','801130','801140','801150','801160','801170','801180','801200','801210','801230','801710','801720','801730','801740','801750','801760','801770','801780','801790','801880','801890')",
    "orderby": "",
    "fieldlist": "L1,L2,L3,L4,L5,L6,L7,L8,L11",
    "pagecount": "28",
    "timed": "",
}

# sw-headers
sw_headers = {
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'www.swsindex.com',
    'Origin': 'http://www.swsindex.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.swsindex.com/idx0120.aspx?columnid=8832',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# zh-sina-a
zh_sina_index_stock_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple"
zh_sina_index_stock_payload = {
    "page": "1",
    "num": "80",
    "sort": "symbol",
    "asc": "1",
    "node": "hs_s",
    "_s_r_a": "page"
}
zh_sina_index_stock_count_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCountSimple?node=hs_s"
zh_sina_index_stock_hist_url = "https://finance.sina.com.cn/realstock/company/{}/hisdata/klc_kl.js"

# investing
short_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}

long_headers = {
    'accept': 'text/plain, */*; q=0.01',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-length': '267',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://cn.investing.com',
    'referer': 'https://cn.investing.com/commodities/brent-oil-historical-data',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
