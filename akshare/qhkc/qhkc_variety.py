# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/2/14 21:23
contact: jindaxiang@163.com
desc: 奇货可查-商品
奇货可查-商品-持仓数据
奇货可查-商品-商品净持仓数据
奇货可查-商品-合约行情数据
奇货可查-商品-商品沉淀资金数据
奇货可查-商品-合约多空比数据
奇货可查-商品-合约净持仓保证金变化数据
奇货可查-商品-合约净持仓保证金数据
奇货可查-商品-合约总持仓保证金数据
奇货可查-商品-商品的席位盈亏数据
奇货可查-商品-自研指标数据
奇货可查-商品-龙虎比排行数据
奇货可查-商品-牛熊线排行数据
奇货可查-商品-商品相关研报数据
奇货可查-商品-商品列表数据
"""
from akshare.pro.data_pro import pro_api

pro = pro_api()  # 接口初始化

# 奇货可查-商品-持仓数据
variety_positions_df = pro.variety_positions(fields="shorts", code="rb1810", date="2018-08-08")
print(variety_positions_df)

# 奇货可查-商品-商品净持仓数据
variety_net_positions_df = pro.variety_net_positions(fields="", symbol="RB", broker="永安期货", date="2018-08-08")
print(variety_net_positions_df)

# 奇货可查-商品-合约行情数据
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