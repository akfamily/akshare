# -*- coding:utf-8 -*- 

"""
版本改动记录:
1.1.7：
郑商所的仓单数据有些输出的格式是文本，改成int型；
郑商所有一些时间段得到的仓单是仓单变化量，修正此bug  
1.1.8:
上期所网站丢失了两个交易日20100416、20130821的数据，在调取此数据时返回None
1.1.9:
基差数据、会员持仓数据、仓单数据，在爬取过早日期时，出现交易所/生意社网还未发布源数据时，跳过并提示用户数据起始日期；
修正了基差数据第二次爬取时，由于用LATEST网址格式，出现日期不匹配跳过的问题；
修改了郑商所会员持仓数据在2010年8月25日前爬取失败的问题
在爬取基差数据和会员持仓数据时，如果出现连续爬取失败超过限制，直接返回已爬过的数据
1.1.10:
增加了原油的中文名称
1.1.11:
上期所抓取合约日线价格时，排除了‘合计’项
1.1.12:
大商所拿到持仓排名的DataFrame的index有重复值，增加reset_index
1.1.13:
当非交易日时，fushare主动抛出Warning，并返回None，搜索多日的情况除外
1.1.14:
获取郑商所会员持仓排名时，改进脚本，避免抛出不必要的warning
1.1.15:
修复获取中金所的一个不必要warning
1.1.16:
获取基差数据时，改进脚本，避免抛出不必要的warning
1.1.17:
为了与行情统一修改会员持仓的品种字段'var' 为'variety'
取上期所的日线行情时，取成交量细节时避免了不必要的警告
增加了上期所的品种 纸浆sp
1.1.18:
修正1.1.17中的一个bug，纸浆品种后面少一个逗号
1.1.19:
在仓单日报里增加原油品种；
在仓单日报中增加字段：当日相比前日仓单增减量
1.1.20:
增加大商所乙二醇品种EG
1.1.21
修改展期收益率的bug，用的公式为:
ln(合约2价格/合约1价格)/（合约1交割年月 - 合约2交割年月）*12
增添展期收益中的近月合约名称、远月合约名称

减去新版日历中的交易日2018年12月31日
1.1.22
增加2019年的交易日历

1.2.1
增加脚本sendEmail，方便每日监控17:00爬取数据，以csv文件形式存本地，并发送给自己QQ邮件确认完成。
需要在配置文件setting.json填写本地存储地址和QQ邮箱账号密码。未开通SMTP服务需要在QQ邮箱开启，方法见github教程

修改展期收益率取var时的日期bug
，由变量start改为变量date

1.2.3
爬取日线行情时，自动生成指数合约。指数合约由持仓量加权得到。

1.2.4
发现一个小bug，在获取指数合约加权计算时候，应该筛掉持仓量为0的合约

1.2.5
同bug，在获取指数合约加权计算时候，当筛掉持仓量为0的合约后，没有合约了，就跳过

1.2.6
同bug，改成持仓量或成交量为0时都不进行加权

1.2.7
czce的rank_table中有的数值类型变成numpy.int，在_tableCut_cal函数末尾加了一句保证数据类型转换为int

1.2.8
pandas最新版0.24.0的pd.read_html函数在basis脚本中识别格式有区别，脚本中针对不同pandas版本识别不同

1.2.9
大商所的仓单数据网站格式变化

1.2.10
上期所成交量0时候有的为str格式的空白，解决该问题
20190502, 20190503，去掉该交易日
"""

__version__ = '0.1.4'
__author__ = 'Albert King'

"""
大宗商品现货价格及基差
"""
# from fushare.basis import (get_spotPrice_daily,
#                            get_spotPrice)

"""
期货持仓成交排名数据
"""
# from fushare.cot import (get_rank_sum_daily,
#                          get_rank_sum,
#                          get_shfe_rank_table,
#                          get_czce_rank_table,
#                          get_dce_rank_table,
#                          get_cffex_rank_table)

"""
大宗商品仓单数据
"""
from akshare.receipt import (get_receipt)

"""
大宗商品仓单数据
"""
# from fushare.rollYield import (get_rollYield_bar, get_rollYield)

"""
交易所行情数据日线
"""
# from fushare.dailyBar import (get_cffex_daily,
#                               get_czce_daily,
#                               get_shfe_vwap,
#                               get_shfe_daily,
#                               get_dce_daily,
#                               get_future_daily)

"""
发邮件模块
"""
# from fushare.sendEmail import sendEmail
