# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/17 1:19
contact: jindaxiang@163.com
desc: 指数配置文件
"""
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}

long_headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '143',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=gqemr8f6b5k3ln2sm2mot584c1; geoC=CN; adBlockerNewUserDomains=1505836027; StickySession=id.24390176506.946.cn.investing.com; __gads=ID=64a5550702122294:T=1505836033:S=ALNI_MarJZek4h5Tsuhfp_UlmdEui3sqvw; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7D%7D%7D%7D; travelDistance=4; billboardCounter_6=0; _ga=GA1.2.328544075.1505836032; _gid=GA1.2.1402998722.1505836033; Hm_lvt_a1e3d50107c2a0e021d734fe76f85914=1505836033; Hm_lpvt_a1e3d50107c2a0e021d734fe76f85914=1505837460; nyxDorf=NTI3ZmczZCY0Y2puYi8xMDZvN3IzNWFgMTA%3D',
    'Host': 'cn.investing.com',
    'Origin': 'https://cn.investing.com',
    'Referer': 'https://cn.investing.com/commodities/crude-oil-historical-data',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
