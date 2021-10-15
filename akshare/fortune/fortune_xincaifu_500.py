# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/11/7 12:12
Desc: 新财富 500 人富豪榜
http://www.xcf.cn/zhuanti/ztzz/hdzt1/500frb/index.html
"""
import json

import pandas as pd
import requests


def xincaifu_rank(year: str = "2020") -> pd.DataFrame:
    """
    新财富 500 人富豪榜
    http://www.xcf.cn/zhuanti/ztzz/hdzt1/500frb/index.html
    :param year: 具体排名年份, 数据从 2003-至今
    :type year: str
    :return: 排行榜
    :rtype: pandas.DataFrame
    """
    url = "http://service.ikuyu.cn/XinCaiFu2/pcremoting/bdListAction.do"
    params = {
        "method": "getPage",
        "callback": "jsonpCallback",
        "sortBy": "",
        "order": "",
        "type": "4",
        "keyword": "",
        "pageSize": "1000",
        "year": year,
        "pageNo": "1",
        "from": "jsonp",
        "_": "1604722171732",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame(data_json["data"]["rows"])
    temp_df.columns = [
        "_",
        "财富",
        "性别",
        "排名",
        "年龄",
        "主要公司",
        "姓名",
        "公司总部",
        "年份",
        "_",
        "相关行业",
    ]
    temp_df = temp_df[
        [
            "排名",
            "财富",
            "姓名",
            "主要公司",
            "相关行业",
            "公司总部",
            "性别",
            "年龄",
            "年份",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    xincaifu_rank_df = xincaifu_rank(year="2020")
    print(xincaifu_rank_df)
