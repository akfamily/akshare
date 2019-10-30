# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/25 15:56
contact: jindaxiang@163.com
desc:
"""
# hk
hk_url = "http://stock.gtimg.cn/data/hk_rank.php"
hk_headers = {
    "Referer": "http://stockapp.finance.qq.com/mstats/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
hk_payload = {
    "board": "A_H",
    "metric": "price",
    "pageSize": "20",
    "reqPage": "1",
    "order": "decs",
    "var_name": "list_data"
}


# usa
url_usa_daily = "http://webusstock.hermes.hexun.com/usa/kline"
payload_usa_daily = {
    "code": "NASDAQNTES",
    "start": "20191026213000",
    "number": "-1000",
    "type": "5"
}

# usa
url_usa = "http://quote.hexun.com/usastock/data/getdjstock.aspx"

payload_usa = {
    "type": "1",
    "market": "3",
    "sorttype": "4",
    "updown": "up",
    "page": "1",
    'count': "200",
    "time": "203450"
}

headers_usa = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # "Cookie": "HexunTrack=SID=201910251553580135036359ad3f5469cb4c5aa519a77b7b6&CITY=51&TOWN=510100; hxck_webdev1_general=stocklist=000001_2; UM_distinctid=16e0201a7821b0-0defa996468efb-b363e65-1fa400-16e0201a78639b; vjuids=-6d38bb03a.16e0201f866.0.7f6ade3a98c3b; vjlast=1571991714.1572090393.13; __jsluid_h=f06894bb913a38443e8302eaf8f287bf; ADVC=37da16bec37a5e; ADVS=37da16bec37a5e; ASL=18195,0000z,7ca1088e; __utma=194262068.759691484.1571991693.1571991693.1572091609.2; __utmc=194262068; __utmz=194262068.1572091609.2.2.utmcsr=data.hexun.com|utmccn=(referral)|utmcmd=referral|utmcct=/stock/67.html; cn_1263247791_dplus=%7B%22distinct_id%22%3A%20%2216e0201a7821b0-0defa996468efb-b363e65-1fa400-16e0201a78639b%22%2C%22userFirstDate%22%3A%20%2220191025%22%2C%22userID%22%3A%20%22%22%2C%22userName%22%3A%20%22%22%2C%22userType%22%3A%20%22nologinuser%22%2C%22userLoginDate%22%3A%20%2220191026%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201572092448%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201572092448%7D; ADHOC_MEMBERSHIP_CLIENT_ID1.0=a96a4a14-9eba-335e-7acc-783d3d98c3be; __utmb=194262068.3.10.1572091609; CNZZDATA1262910142=2109501423-1572092999-http%253A%252F%252Fquote.hexun.com%252F%7C1572092999; hxwzkf=321748F31279DBBC688956DDB60B9099",
    "Host": "quote.hexun.com",
    "Pragma": "no-cache",
    "Referer": "http://quote.hexun.com/usastock/xqstock.aspx?market=3",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

# china
url = "http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "ADVC=371c0a2afd9a7b; UM_distinctid=16a24d29c4f142-0f969e46eea4c7-e323069-1fa400-16a24d29c50aa5; HexunTrack=SID=20190416142542146f54a3710276640a88fea687ad6a7bcb0&CITY=51&TOWN=510100; vjuids=11fcc219b5.16a820267e4.0.cc0391a93be56; vjlast=1556959357.1556959357.30; __utma=194262068.1423418741.1558975446.1558975446.1558975446.1; __utmz=194262068.1558975446.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ASL=18179,anzqo,7ca108c3ded485387ca108c27ca108b97ca108ef; cn_1263247791_dplus=%7B%22distinct_id%22%3A%20%2216a24d29c4f142-0f969e46eea4c7-e323069-1fa400-16a24d29c50aa5%22%2C%22userFirstDate%22%3A%20%2220190504%22%2C%22userID%22%3A%20%22%22%2C%22userName%22%3A%20%22%22%2C%22userType%22%3A%20%22nologinuser%22%2C%22userLoginDate%22%3A%20%2220191010%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201570727325%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201570727325%2C%22initial_view_time%22%3A%20%221556958609%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DJmHPP1QGABcJs0kzrvZREqHK_nobidR7d7YPCQF75loa5N33Au5q_xFu8y9VPlvl8O6I7b1LmRuhIiccTnFW-_%26wd%3D%26eqid%3Db55837ee0001a310000000025ccd4f55%22%2C%22initial_referrer_domain%22%3A%20%22www.baidu.com%22%2C%22%24recent_outside_referrer%22%3A%20%22www.baidu.com%22%7D; hxck_webdev1_general=bondjlvcookie_list=019124_11%e5%9b%bd%e5%80%ba24_1&npFutjlvcookie_list=czcers1409|WT1009; appToken=pc%2Cother%2Cchrome%2ChxAppSignId96253760252191461570688954189%2CHXGG20190415; __jsluid_h=08f65cba22ad34dc3fd095b5b986c8a4",
    "Host": "stockdata.stock.hexun.com",
    "Pragma": "no-cache",
    "Referer": "http://stockdata.stock.hexun.com/zrbg/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
params = {
    "date": "2018-12-31",
    "count": "20",
    "pname": "20",
    "titType": "null",
    "page": "8",
    "callback": "hxbase_json11571989979887",
}
