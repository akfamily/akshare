# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/25 15:56
contact: jindaxiang@163.com
desc: 
"""
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