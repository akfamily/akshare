# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/2/13 23:11
contact: jindaxiang@163.com
desc: 可用函数库 --> client.py --> DataApi
"""


class QhkcFunctions:

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
