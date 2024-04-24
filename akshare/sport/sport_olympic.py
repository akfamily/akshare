#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/8/2 16:47
Desc: 运动-奥运会
https://www.kaggle.com/marcogdepinto/let-s-discover-more-about-the-olympic-games
"""
import pandas as pd
import requests
from akshare.request_config_manager import get_headers_and_timeout
from io import BytesIO


def sport_olympic_hist() -> pd.DataFrame:
    """
    运动-奥运会-奖牌数据
    https://www.kaggle.com/marcogdepinto/let-s-discover-more-about-the-olympic-games
    :return: 奥运会-奖牌数据
    :rtype: pandas.DataFrame
    """
    url = "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_olympic/athlete_events.zip"
    headers, timeout = get_headers_and_timeout(locals().get('headers', {}), locals().get('timeout', None))
    res = requests.get(url, headers=headers, timeout=timeout)
    temp_df = pd.read_csv(BytesIO(res.content), compression='zip')
    columns_list = [item.lower() for item in temp_df.columns.tolist()]
    temp_df.columns = columns_list
    return temp_df


if __name__ == "__main__":
    sport_olympic_hist_df = sport_olympic_hist()
    print(sport_olympic_hist_df)
