# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/25 13:55
contact: jindaxiang@163.com
desc: 
"""
import time
import json
import random

import requests
import pandas as pd

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}


def main():
    data = pd.DataFrame(
        columns=['com_name', 'born', 'close', 'live_time', 'total_money', 'cat_name', 'com_prov', 'closure_type'])
    for i in range(1, 100):  # 设置爬取N页
        url = 'https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page=' + str(i)
        html = requests.get(url=url, headers=headers).content
        doc = json.loads(html.decode('utf-8'))['data']['info']
        for j in range(10):  # 一页10个死亡公司
            data = data.append({'com_name': doc[j]['com_name'], 'born': doc[j]['born'], 'cat_name': doc[j]['cat_name'],
                                'closure_type': doc[j]['closure_type'], 'close': doc[j]['com_change_close_date'],
                                'com_prov': doc[j]['com_prov'],
                                'live_time': doc[j]['live_time'], 'total_money': doc[j]['total_money']},
                               ignore_index=True)
            time.sleep(random.random())
    return data
