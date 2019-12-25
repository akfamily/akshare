# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/25 13:55
contact: jindaxiang@163.com
desc: 
"""
import time
import random
import os

import requests
import pandas as pd

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}


def death_company():
    page_num_url = 'https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page=1'
    data_json = requests.get(url=page_num_url, headers=headers).json()
    num_page_int = data_json['data']['page']["total"]
    for i in range(191, num_page_int+1):
        print(i)
        json_url = f'https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page={i}'
        data_json = requests.get(url=json_url, headers=headers).json()
        data_df = data_json['data']['info']
        data_df = pd.DataFrame(data_df)
        data_df = data_df[['com_name', 'born', "com_change_close_date", 'live_time', 'total_money', 'cat_name', 'com_prov']]
        data_df.to_csv(os.path.join(r"C:\Users\king\Desktop\juzi", str(i)+".csv"))
        time.sleep(2)
    return data_df


if __name__ == '__main__':
    df = death_company()
    print(df)
