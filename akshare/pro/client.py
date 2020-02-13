# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/10 22:52
contact: jindaxiang@163.com
desc: 数据接口源代码
"""
from functools import partial
from urllib import parse

import pandas as pd
import requests


class DataApi:

    __token = ""
    __http_url = "https://api.qhkch.com"

    def __init__(self, token, timeout=10):
        """
        初始化函数
        :param token: API接口TOKEN，用于用户认证
        :type token: str
        :param timeout: 超时设置
        :type timeout: int
        """
        self.__token = token
        self.__timeout = timeout

    def query(self, api_name, fields="", **kwargs):
        """
        :param api_name: 需要调取的接口
        :type api_name: str
        :param fields: 想要获取的字段
        :type fields: str
        :param kwargs: 指定需要输入的参数
        :type kwargs: 键值对
        :return: 指定的数据
        :rtype: dict or pandas.DataFrame
        """
        headers = {
            "X-Token": self.__token,
        }

        url = parse.urljoin(self.__http_url, "/".join([api_name, *kwargs.values()]))
        res = requests.get(url, headers=headers, timeout=self.__timeout)
        if res.status_code != 200:
            raise Exception("连接异常, 请检查您的Token是否过期和输入的参数是否正确")
        data_json = res.json()
        if fields == "":
            try:
                return pd.DataFrame(data_json)
            except ValueError as e:
                return data_json
        else:
            return pd.DataFrame(data_json[fields])

    def __getattr__(self, name):
        return partial(self.query, name)

    @staticmethod
    def variety_positions(fields="shorts", code="rb1810", date="2018-08-08"):
        """
        奇货可查-商品-持仓数据接口
        :param fields: 需要返回的字段, shorts or longs
        :type fields: str
        :param code: 合约代号
        :type code: str
        :param date: 查询日期
        :type date: str
        :return: 商品-持仓数据
        :rtype: pandas.DataFrame
        broker	string	席位
        long	int	该席位多头持仓量
        long_chge	int	该席位多头持仓变化量
        short	int	该席位空头持仓量
        short_chge	int	该席位空头持仓变化量
        """
        pass

    @staticmethod
    def variety_net_positions(fields="", symbol="RB", broker="永安期货", date="2018-08-08"):
        """
        奇货可查-商品-商品净持仓数据接口
        :param fields: 需要返回的字段
        :type fields: str
        :param symbol: 查询品种编码
        :type symbol: str
        :param broker: 席位
        :type broker: str
        :param date: 查询日期
        :type date: str
        :return: 商品-商品净持仓数据
        :rtype: dict
        trans_date	date	查询日期
        net_position	int	净持仓数据
        """
        pass


if __name__ == '__main__':
    pass
