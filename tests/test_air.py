# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/12 18:16
contact: jindaxiang@163.com
desc: To test intention, just write test code here!
"""
from akshare.air.aqi_study import air_hourly
from akshare.index.index_weibo import weibo_index
from akshare.fortune.fortune_500 import fortune_rank


# def test_air_hourly():
#     """
#     test air_hourly interface
#     :return:
#     """
#     df_hourly = air_hourly("成都", "2019-12-10")
#     assert len(df_hourly) >= 10


def test_weibo_index():
    """
    test air_hourly interface
    :return: assert
    :rtype:
    """
    weibo_index_df = weibo_index(word="python", time_type="3month")
    assert len(weibo_index_df) >= 10


def test_fortune():
    """
    test air_hourly interface
    :return:
    """
    fortune_df = fortune_rank(year=2011)  # 2010 不一样
    assert len(fortune_df) >= 10


if __name__ == "__main__":
    # test_air_hourly()
    test_weibo_index()
    test_fortune()
