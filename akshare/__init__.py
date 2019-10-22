"""AkShare 是基于 Python 的开源数据接口库, 目的是实现对期货, 期权, 基金等衍生金融产品和另类数据从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论."""

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
0.1.30
规范说明文档格式
0.1.31
规范 cot.py 函数说明
0.1.32
update basis.py
0.1.33
增加奇货可查数据三个接口:
get_qhkc_index, get_qhkc_index_trend, get_qhkc_index_profit_loss
使用方法请 help(get_qhkc_index) 查看
0.1.34
增加奇货可查-资金数据三个接口:
get_qhkc_fund_position_change, get_qhkc_fund_bs, get_qhkc_fund_position
使用方法请 help(get_qhkc_fund_position_change) 查看
0.1.35
增加奇货可查-工具-外盘比价接口:
get_qhkc_tool_foreign
使用方法请 help(get_qhkc_tool_foreign) 查看
0.1.36
增加奇货可查-工具-各地区经济数据接口:
get_qhkc_tool_gdp
使用方法请 help(get_qhkc_tool_gdp) 查看
0.1.37
增加中国银行间市场交易商协会-债券接口
get_bond_bank
使用方法请 help(get_bond_bank) 查看
0.1.38
修正
0.1.39
模块化处理
0.1.40
统一接口函数参数 start --> start_day; end --> end_day
0.1.41
更新大连商品交易所-苯乙烯-EB品种
0.1.42
更新上海期货交易所-上海国际能源交易中心-20号胶-NR品种
更新上海期货交易所-不锈钢-SS品种
0.1.43
修复 example --> test.py 函数调用
0.1.44
修复 example --> daily_run.py 函数调用
0.1.45
修复 README.md 函数接口调用说明和感谢单位
0.1.46
修复 README.md 图片显示
0.1.47
修复 README.md 增加说明部分
0.1.48
更新大连商品交易所-粳米-RR品种
0.1.49
增加智道智科-私募指数数据接口
使用方法请 help(get_zdzk_fund_index) 查看
0.1.50
更新 README.md 文件
0.1.51
更新官方文档: https://akshare.readthedocs.io
0.1.52
增加量化策略和量化平台板块
0.1.53
增加期货品种列表和名词解释
0.1.54
修改 AkShare的初衷, 增加管理期货策略指数
0.1.55
新增 99期货(http://www.99qh.com/d/store.aspx) 库存数据接口
0.1.56
修复 99期货(http://www.99qh.com/d/store.aspx) 库存数据接口
0.1.57
更新 md 文件数据接口
0.1.58
更新 md 文件数据接口
0.1.59
更新 md 文件数据接口
0.1.60
更新 致谢部分, 申明借鉴和引用的 package
0.1.61
更新说明文档
0.1.62
提供英为财情-股票指数-全球股指与期货指数数据接口
https://cn.investing.com/indices/
0.1.63
更新说明文档-致谢英为财情
0.1.64
更新 get_country_index 返回格式为日期索引
0.1.65
更新 get_country_index 返回格式数据开盘, 收盘, 高, 低为浮点型
0.1.66
提供英为财情-股票指数-全球股指与期货指数数据接口
https://cn.investing.com/rates-bonds/
新增 get_country_bond 返回格式数据开盘, 收盘, 高, 低为浮点型
0.1.67
更新说明文档-私募指数数据说明
0.1.68
更新说明文档-私募指数数据说明-增加图片
0.1.69
更新说明文档-债券说明格式调整
0.1.70
更新大商所, 郑商所商品期权数据接口
0.1.71
更新大商所, 郑商所, 上期所商品期权数据接口
0.1.72
修改大商所, 郑商所, 上期所商品期权数据接口
增加函数说明
更新说明文档-期权部分
0.1.73
更新说明文档-期权部分
0.1.74
更新说明文档格式调整
0.1.75
新增外汇接口, 银行间债券市场行情数据接口
0.1.76
更新说明文档
0.1.77
新增全球期货历史数据查询接口
0.1.78
新增全球宏观数据-中国宏观数据
年度、月度CPI数据, 年度M2数据
0.1.79
更新说明文档
0.1.80
更新说明文档-刷新
0.1.81
新增全球宏观数据-中国宏观数据
中国年度PPI数据
中国年度PMI数据 
中国年度GDP数据
中国年度财新PMI数据
中国外汇储备数据
中国电力能源数据
中国年度非制造业PMI数据
人民币中间报价汇率
"""

__version__ = '0.1.81'
__author__ = 'Albert King'

"""
全球宏观-中国宏观
"""
from akshare.economic.macro_data_china import (get_china_monthly_cpi,
                                               get_china_yearly_cpi,
                                               get_china_yearly_m2,
                                               get_china_yearly_fx_reserves,
                                               get_china_yearly_cx_pmi,
                                               get_china_yearly_pmi,
                                               get_china_daily_energy,
                                               get_china_non_man_pmi,
                                               get_china_rmb,
                                               get_china_yearly_gdp,
                                               get_china_yearly_ppi)

"""
全球期货
"""
from akshare.futures.international_futures import (get_sector_futures)

"""
外汇
"""
from akshare.fx.fx_quote import (get_fx_pair_quote,
                                 get_fx_spot_quote,
                                 get_fx_swap_quote)

"""
债券行情
"""
from akshare.bond.china_bond import (get_bond_market_quote,
                                     get_bond_market_trade)

"""
商品期权
"""
from akshare.option.daily_bar import (get_dce_option_daily,
                                      get_czce_option_daily,
                                      get_shfe_option_daily)

"""
英为财情-债券
"""
from akshare.bond.investing_bond import (get_country_bond)  # 债券-全球政府债券行情与收益率

"""
英为财情-指数
"""
from akshare.index.investing_index import (get_country_index)  # 股票指数-全球股指与期货指数数据接口

"""
99期货数据
"""
from akshare.futures.futures_inventory import (get_inventory_data)

"""
私募指数
"""
from akshare.fund.zdzk_fund import (get_zdzk_fund_index)

"""
中国银行间市场交易商协会
"""
from akshare.bond.bond_bank import (get_bond_bank)

"""
奇货可查-工具模块
"""
from akshare.qhkc.qhkc_tool import (get_qhkc_tool_foreign,
                                    get_qhkc_tool_gdp)

"""
奇货可查-指数模块
"""
from akshare.qhkc.qhkc_index import (get_qhkc_index,
                                     get_qhkc_index_trend,
                                     get_qhkc_index_profit_loss)

"""
奇货可查-资金模块
"""
from akshare.qhkc.qhkc_fund import (get_qhkc_fund_position_change,
                                    get_qhkc_fund_bs,
                                    get_qhkc_fund_position)

"""
大宗商品现货价格及基差
"""
from akshare.futures.basis import (get_spot_price_daily,
                                   get_spot_price)

"""
期货持仓成交排名数据
"""
from akshare.futures.cot import (get_rank_sum_daily,
                                 get_rank_sum,
                                 get_shfe_rank_table,
                                 get_czce_rank_table,
                                 get_dce_rank_table,
                                 get_cffex_rank_table)

"""
大宗商品仓单数据
"""
from akshare.futures.receipt import (get_receipt)

"""
大宗商品展期收益率数据
"""
from akshare.futures.roll_yield import (get_roll_yield_bar,
                                        get_roll_yield)

"""
交易所行情数据日线
"""
from akshare.futures.daily_bar import (get_cffex_daily,
                                       get_czce_daily,
                                       get_shfe_v_wap,
                                       get_shfe_daily,
                                       get_dce_daily,
                                       get_futures_daily)

"""
配置文件
"""
from akshare.futures import (cons)
from akshare.fund import (cons)

"""
发邮件模块
"""
from akshare.tool.send_email import (send_email)
