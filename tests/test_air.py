# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/12 18:16
contact: jindaxiang@163.com
desc: To test intention, just write test code here!
"""
# from akshare.air.aqi_study import air_hourly
from akshare.index.index_weibo import weibo_index
from akshare.event.franchise import franchise_china
# from akshare.fortune.fortune_500 import fortune_rank


def test_franchise_china():
    franchise_china_df = franchise_china()
    assert franchise_china_df.shape[0] > 0


# def test_air_hourly():
#     """
#     test air_hourly interface
#     :return: air_hourly_df
#     :rtype: pandas.DataFrame
#     """
#     air_hourly_df = air_hourly("成都", "2019-12-10")
#     assert air_hourly_df.shape[0] > 0


def test_weibo_index():
    """
    test weibo_index interface
    :return: weibo_index_df
    :rtype: pandas.DataFrame
    """
    weibo_index_df = weibo_index(word="口罩", time_type="3month")
    assert weibo_index_df.shape[0] > 0


# def test_fortune():
#     """
#     test fortune_rank interface
#     :return: fortune_rank_df
#     :rtype: pandas.DataFrame
#     """
#     fortune_rank_df = fortune_rank(year=2011)  # 2010 不一样
#     assert fortune_rank_df.shape[0] > 0


if __name__ == "__main__":
    # test_air_hourly()
    test_weibo_index()
    # test_fortune()
