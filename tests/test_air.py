# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/12 18:16
contact: jindaxiang@163.com
desc: 用于自动测试的文件, 这里写相关的自动测试接口函数
"""
from akshare.air.aqi_study import air_hourly
from akshare.index.index_weibo import weibo_index


def test_air_hourly():
    df_hourly = air_hourly('成都', '2019-12-10')
    assert len(df_hourly) >= 10


def test_weibo_index():
    weibo_index_df = weibo_index(word="python", time_type="3month")
    assert len(weibo_index_df) >= 10


if __name__ == "__main__":
    test_air_hourly()
    test_weibo_index()
