"""AkShare 是实现对期货等衍生金融产品从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论."""

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
0.1.19
修正 cot.py 中请求错误
0.1.20
修正 __doc__
0.1.21
修复 __doc__
0.1.22
修复命名和绘图
0.1.23
修复错误机制
0.1.24
增加奇货可查所有指数数据获取接口
0.1.25
修复 qhck 接口
0.1.26
修复代码格式问题
0.1.27
修复说明格式问题
0.1.28
更新说明文档
0.1.29
规范说明文档格式
"""

__version__ = '0.1.28'
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
