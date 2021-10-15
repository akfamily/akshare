# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/10/15
Desc: 沪深A股公告
http://data.eastmoney.com/notices/
"""
import pandas as pd
import requests
import json

def stock_notices_em(f_node: int = 5, page_index: int = 1) -> pd.DataFrame:
    """
    沪深A股公告- 50 条公告
    http://np-anotice-stock.eastmoney.com/api/security/ann?cb=jQuery112307586546013774447_1634268259865&sr=-1&page_size=50&page_index=1&ann_type=A&client_source=web&f_node=7&s_node=0

    f_node = {"1": "财务报告",
              "2":"融资公告",
              "3":"风险提示",
              "4":"信息变更",
              "5":"重大事项",
              "6":"资产重组",
              "7":"持股变动",
    }
    
    :param f_node: 公告类型
    :param page_index: 页数
    :type f_node: int
    :type page_index: int
    :return: 沪深A股公告
    :rtype: pandas.DataFrame
    """
    url = "http://np-anotice-stock.eastmoney.com/api/security/ann"
    params = {
        "cb": "jQuery112307586546013774447_1634268259865",
        "sr": "-1",
        "page_size": "50",
        "page_index": page_index,
        "ann_type": "A",
        "client_source": "web",
        "f_node": f_node,
        "s_node":"0"
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "np-anotice-stock.eastmoney.com",
        "Pragma": "no-cache",
        "Referer": "http://data.eastmoney.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.40 Safari/537.36 Edg/95.0.1020.20",
    }


    r = requests.get(url, params=params, headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{") : -1])
    content_list = json_data["data"]["list"]
    
    result_list = []
    for cl in content_list:
        result_dict={}
        result_dict['代码'] = cl['codes'][0]['stock_code']
        result_dict['名称'] = cl['codes'][0]['short_name']
        result_dict['公告类型'] = cl['columns'][0]['column_name']
        result_dict['公告日期'] = cl['notice_date']
        result_dict['公告标题'] = cl['title']
        result_list.append(result_dict)
    
    temp_df = pd.DataFrame(result_list)

    return temp_df


if __name__ == "__main__":
    stock_notices_df = stock_notices_em(1,2)
    print(stock_notices_df.info())
