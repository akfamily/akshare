# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/12 18:16
contact: jindaxiang@163.com
desc: 测试文件
"""
from akshare.weather.aqi_study import air_hourly


def test_air_hourly():
    df_hourly = air_hourly('成都', '2019-12-10')
    assert len(df_hourly) >= 10


if __name__ == "__main__":
    test_air_hourly()
