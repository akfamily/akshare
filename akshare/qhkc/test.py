# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/2/13 21:33
contact: jindaxiang@163.com
desc: 接口测试文件
"""
from akshare.pro.data_pro import pro_api

from akshare.utils.token_process import set_token

pro = pro_api(token="")

variety_positions_df = pro.variety_positions(fields="shorts", code="rb1810", date="2018-08-08")
print(variety_positions_df)

variety_net_positions_df = pro.variety_net_positions(fields="", symbol="RB", broker="永安期货", date="2018-08-08")
print(variety_net_positions_df)

variety_quotes_df = pro.variety_quotes(fields="", code="rb1810", date="2018-08-08")
print(variety_quotes_df)

variety_money_df = pro.variety_money(fields="", symbol="RB", date="2018-08-08")
print(variety_money_df)

variety_bbr_df = pro.variety_bbr(fields="", code="rb1810", date="2018-08-08")
print(variety_bbr_df)

variety_net_money_chge_df = pro.variety_net_money_chge(fields="", code="rb1810", date="2018-08-08")
print(variety_net_money_chge_df)

variety_net_money_df = pro.variety_net_money(fields="", code="rb1810", date="2018-08-08")
print(variety_net_money_df)

variety_total_money_df = pro.variety_total_money(fields="", code="rb1810", date="2018-08-08")
print(variety_total_money_df)

# 席位
broker_positions_df = pro.broker_positions(fields="", broker="永安期货", date="2018-08-08")
print(broker_positions_df)

# 指数
index_info_df = pro.index_info(fields="", index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959")
print(index_info_df)
