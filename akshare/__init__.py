# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 初始化文件, 主要用于在导入 package 的时候导入需要运行的函数
"""

"""
版本改动记录:
0.1.13
更新所有基于 fushare 的接口

0.1.14
更新 requirements.txt 文件

0.1.15
自动安装所需要的 packages

0.1.16
修正部分函数命名

0.1.17
更新版本号自动管理

0.1.18
更新说明文档
"""

__version__ = '0.1.18'
__author__ = 'Albert King'

"""
奇货可查模块
"""
from akshare.qhkc import get_qhkc_data

"""
大宗商品现货价格及基差
"""
from akshare.basis import (get_spot_price_daily,
                           get_spot_price)

"""
期货持仓成交排名数据
"""
from akshare.cot import (get_rank_sum_daily,
                         get_rank_sum,
                         get_shfe_rank_table,
                         get_czce_rank_table,
                         get_dce_rank_table,
                         get_cffex_rank_table)

"""
大宗商品仓单数据
"""
from akshare.receipt import (get_receipt)

"""
大宗商品展期收益率数据
"""
from akshare.roll_yield import (get_roll_yield_bar, get_roll_yield)

"""
交易所行情数据日线
"""
from akshare.daily_bar import (get_cffex_daily,
                               get_czce_daily,
                               get_shfe_v_wap,
                               get_shfe_daily,
                               get_dce_daily,
                               get_futures_daily)

"""
发邮件模块
"""
from akshare.send_email import send_email

