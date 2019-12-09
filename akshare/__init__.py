"""AkShare 是基于 Python 的开源金融数据接口库, 目的是实现对股票, 期货, 期权, 基金, 债券, 外汇等金融产品和另类数据从数据采集, 数据清洗到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于可信任数据源发布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 从而得出科学的结论."""
import datetime

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
0.1.82
新增全球宏观数据-美国宏观数据
美联储利率决议报告
美国非农就业人数报告
美国失业率报告
美国EIA原油库存报告
0.1.83
更新说明文档
0.1.84
新增全球宏观数据-美国宏观数据
美国初请失业金人数报告美国核心
PCE物价指数年率报告
美国CPI月率报告
美联储劳动力市场状况指数报告
美国ADP就业人数报告
美国国内生产总值(GDP)报告
美国原油产量报告
新增全球宏观数据-欧洲宏观数据
欧洲央行决议报告
新增全球宏观数据-机构宏观数据
全球最大黄金ETF—SPDR Gold Trust持仓报告
全球最大白银ETF--iShares Silver Trust持仓报告
欧佩克报告
0.1.85
新增期货-仓单有效期接口
0.1.86
更新说明文档
0.1.87
新增和讯财经-企业社会责任数据接口
0.1.88
更新说明文档
0.1.89
更新requirements.txt
0.1.90
更新setup.py
0.1.91
新增和讯财经-中国概念股行情及日频历史数据接口
0.1.92
更新说明文档
0.1.93
新增交易法门-套利工具-跨期价差(自由价差)数据接口
0.1.94
新增生意社-商品与期货-现期图数据接口
新增西本新干线-指数数据
0.1.95
新增新浪财经-期货-实时数据接口
0.1.96
修正新浪财经-期货-实时数据接口-返回 current_price 字段为实时数据
0.1.97
修正新浪财经-期货-实时数据接口-返回 current_price 和 ask_price 字段为实时数据
0.1.98
修正版本更新错误
0.1.99
增加自动安装 pillow
0.2.1
增加港股当日(时点)行情数据和历史数据(前复权和后复权因子)
0.2.2
增加美股当日(时点)行情数据和历史数据(前复权因子)
0.2.3
增加金融期权
0.2.4
增加数字货币行情接口
0.2.5
增加 AkShare 接口导图
0.2.6
更新港股数据接口和说明文档
0.2.7
更新 qhkc 接口注释和说明文档
0.2.8
更新说明文档
0.2.9
更新A+H股数据实时行情数据和历史行情数据(后复权)
0.2.10
更新说明文档
0.2.11
更新说明文档
0.2.12
增加A股实时行情数据和历史行情数据
0.2.13
统一股票接口命名
0.2.14
统一股票接口命名, 去除 get
0.2.15
增加科创板实时行情数据和历史行情数据
0.2.16
增加银保监分局本级行政处罚数据
0.2.17
更新说明文档
0.2.18
修正银保监分局本级行政处罚数据接口字段命名
0.2.19
增加 Nodejs 安装说明
0.2.20
增加 Realized Library 接口
0.2.21
更新说明文档
0.2.22
更新说明文档
0.2.23
修正银保监分局本级行政处罚数据接口反扒升级-修改完成
0.2.24
增加FF多因子模型数据接口
0.2.25
更新说明文档
0.2.26
修正期货-实时行情: 接口命名, 字段补充及限制访问速度
0.2.27
增加新浪-外盘期货实时行情数据接口
0.2.28
修正新浪-外盘期货实时行情数据引入
更新文档
0.2.29
更新文档
0.2.30
监管-银保监: 反扒措施在变化, 更新接口
修正期货-国内-实时行情接口订阅问题
0.2.31
修正期货-国内-金融期货实时行情接口订阅问题
0.2.32
更新说明文档
0.2.33
更新说明文档-期货-外盘
0.2.34
新增新浪-指数实时行情和历史行情接口
0.2.35
新增新浪-指数和A股实时行情列表获取问题
0.2.36
新增腾讯财经-A股分笔行情历史数据
0.2.37
新增金十数据-实时监控接口
0.2.38
更新说明文档
0.2.39
更新说明文档目录结构
增加专题教程-pandas专题-连载
0.2.40
更新专题板块
0.2.41
更新说明文件
0.2.42
更新mindmap
0.2.43
重构说明文档-模块化处理, 将 github 说明文档和 docs 在线文档分开处理
重构私募指数接口
0.2.44
增加日出和日落模块
0.2.45
增加河北空气指数数据
0.2.46
更新 requirements.txt
0.2.47
添加初始化文件
0.2.48
添加 websocket-client
0.2.49
南华期货-南华商品指数
0.2.50
修正英为财情-指数板块的成交量显示问题
0.2.51
消除部分警告信息
0.2.52
基差数据缺失错误提示修正
0.2.53
统一南华期货-商品指数历史走势-收益率指数
新增南华期货-商品指数历史走势-价格指数
新增南华期货-商品指数历史走势-波动率指数
0.2.54
添加 numpy 依赖
0.2.55
更新已实现波动率的说明文档
统一 ff_crr --> article_ff_crr
0.2.56
新增经济政策不确定性(EPU)数据接口
更新说明文档
修改示例说明
0.2.57
修改 air_hebei 接口, 默认返回全部城市
0.2.58
新增微博指数
0.2.59
增加西本新干线说明文档
0.2.60
新增百度指数
0.2.61
修正河北空气数据代码
0.2.62
新增百度搜索指数
新增百度资讯指数
新增百度媒体指数
0.2.63
更新指数-legend代码
0.2.64
fix pillow>=6.2.0
0.2.65
新增谷歌指数
0.2.66
修正南华指数URL硬编码问题
0.2.67
修正 get_futures_index 函数中上海期货交易所
CU 出现 cuefp 数据导致指数合成异常的问题
0.2.68
降低 Python 版本要求
0.2.69
降低python版本要求到 Python3.7.1
0.2.70
适配 VNPY 使用
0.2.71
交易法门数据接口
0.2.72
申万行业一级指数-实时
0.2.73
更新纯碱期货数据接口
0.2.74
新增AQI空气质量数据接口
0.2.75
新增申万一级指数接口
0.2.76
统一交易法门登录和数据获取接口
0.2.77
清除冗余函数
0.2.78
Python 降级
0.2.79
Python 降级
0.2.80
Python 3.6
0.2.81
html5lib
0.2.82
websockets-8.1
0.2.83
修复 weibo_index 函数日期格式问题
0.2.84
修复 baidu_index 接口
"""

__version__ = "0.2.84"
__author__ = "Albert King"

"""
AQI空气质量接口
"""
from akshare.weather.aqi_study import air_all_city, air_city_list, air_daily, air_hourly

"""
申万行业一级-实时
"""
from akshare.index.index_sw import (
    sw_index_spot,
    sw_index_cons,
    sw_index_daily,
    sw_index_daily_indicator,
)

"""
交易法门-数据-农产品
"""
from akshare.futures_derivative.jyfm_data_func import (
    jyfm_data_palm,  # 棕榈
    jyfm_data_soybean_meal,  # 豆粕
    jyfm_data_sugar,  # 白糖
    jyfm_data_usa_bean,  # 美豆
)

"""
交易法门-登录
"""
from akshare.futures_derivative.jyfm_login_func import jyfm_login

"""
谷歌指数
"""
from akshare.index.index_google import google_index

"""
百度指数
"""
from akshare.index.index_baidu import (
    baidu_search_index,
    baidu_info_index,
    baidu_media_index,
)

"""
微博指数
"""
from akshare.index.index_weibo import weibo_index

"""
经济政策不确定性指数
"""
from akshare.article.epu_index import article_epu_index

"""
南华期货-南华指数
"""
from akshare.futures_derivative.nh_index_return import nh_return_index
from akshare.futures_derivative.nh_index_price import nh_price_index
from akshare.futures_derivative.nh_index_volatility import nh_volatility_index

"""
空气-河北
"""
from akshare.weather.air_hebei import air_hebei

"""
timeanddate-日出和日落
"""
from akshare.weather.time_and_date import weather_daily, weather_monthly

"""
金十财经-实时监控
"""
from akshare.ws.jinshi import watch

"""
新浪-指数实时行情和历史行情
"""
from akshare.stock.zh_stock_a_tick_tx import stock_zh_a_tick

"""
新浪-指数实时行情和历史行情
"""
from akshare.index.zh_stock_index_sina import stock_zh_index_daily, stock_zh_index_spot

"""
外盘期货实时行情
"""
from akshare.futures.hf_futures_sina import (
    futures_hf_spot,
    hf_subscribe_exchange_symbol,
)

"""
FF多因子数据接口
"""
from akshare.article.ff_factor import article_ff_crr

"""
Realized Library 接口
"""
from akshare.article.risk_rv import (
    article_oman_rv,
    article_oman_rv_short,
    article_rlab_rv,
)

"""
银保监分局本级行政处罚数据
"""
if datetime.datetime.now().weekday() in [0, 1, 2, 3, 4]:
    from akshare.bank.bank_cbirc_20191114 import bank_fjcf
else:
    from akshare.bank.bank_cbirc_20191115 import bank_fjcf

"""
科创板股票
"""
from akshare.stock.zh_stock_kcb_sina import stock_zh_kcb_spot, stock_zh_kcb_daily

"""
A股
"""
from akshare.stock.zh_stock_a_sina import stock_zh_a_spot, stock_zh_a_daily

"""
A+H股
"""
from akshare.stock.zh_stock_ah_tx import (
    stock_zh_ah_spot,
    stock_zh_ah_daily,
    stock_zh_ah_name,
)

"""
数字货币
"""
from akshare.economic.macro_other import get_js_dc_current

"""
金融期权
"""
from akshare.option.daily_bar_finance import (
    get_finance_option,
    get_finance_option_current,
)

"""
新浪-美股实时行情数据和历史行情数据(前复权)
"""
from akshare.stock.us_stock_sina import stock_us_daily, stock_us_spot

"""
新浪-港股实时行情数据和历史数据(前复权和后复权因子)
"""
from akshare.stock.hk_stock_sina import stock_hk_daily, stock_hk_spot

"""
新浪-期货实时数据
"""
from akshare.futures.zh_futures_sina import futures_zh_spot, match_main_contract

"""
西本新干线-指数数据
"""
from akshare.futures_derivative.xgx_data import get_code_pic, xgx_data

"""
生意社-商品与期货-现期图数据
"""
from akshare.futures_derivative.sys_spot_futures import (
    get_sys_spot_futures,
    get_sys_spot_futures_dict,
)

"""
交易法门-套利工具-跨期价差(自由价差)
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_futures_ratio,
    jyfm_tools_futures_customize,
    jyfm_tools_futures_spread,
)

"""
和讯财经-行情及历史数据
"""
from akshare.stock.us_zh_stock_hx import stock_us_zh_spot, stock_us_zh_daily

"""
和讯财经-企业社会责任
"""
from akshare.stock.zh_stock_zrbg_hx import stock_zh_a_scr_report

"""
期货-仓单有效期
"""
from akshare.futures.receipt_period import get_receipt_date

"""
全球宏观-机构宏观
"""
from akshare.economic.macro_constitute import (
    get_cons_gold_amount,
    get_cons_gold_change,
    get_cons_gold_volume,
    get_cons_opec_month,
    get_cons_opec_near_change,
    get_cons_silver_amount,
    get_cons_silver_change,
    get_cons_silver_volume,
)

"""
全球宏观-欧洲宏观
"""
from akshare.economic.macro_euro import get_euro_interest_rate

"""
全球宏观-美国宏观
"""
from akshare.economic.macro_usa import (
    get_usa_eia_crude_rate,
    get_usa_interest_rate,
    get_usa_non_farm,
    get_usa_unemployment_rate,
    get_usa_adp_employment,
    get_usa_core_pce_price,
    get_usa_cpi_monthly,
    get_usa_crude_alaska,
    get_usa_crude_inner,
    get_usa_crude_state,
    get_usa_gdp_monthly,
    get_usa_initial_jobless,
    get_usa_lmci,
)

"""
全球宏观-中国宏观
"""
from akshare.economic.macro_china import (
    get_china_monthly_cpi,
    get_china_yearly_cpi,
    get_china_yearly_m2,
    get_china_yearly_fx_reserves,
    get_china_yearly_cx_pmi,
    get_china_yearly_pmi,
    get_china_daily_energy,
    get_china_non_man_pmi,
    get_china_rmb,
    get_china_yearly_gdp,
    get_china_yearly_ppi,
)

"""
全球期货
"""
from akshare.futures.international_futures import get_sector_futures

"""
外汇
"""
from akshare.fx.fx_quote import get_fx_pair_quote, get_fx_spot_quote, get_fx_swap_quote

"""
债券行情
"""
from akshare.bond.china_bond import get_bond_market_quote, get_bond_market_trade

"""
商品期权
"""
from akshare.option.daily_bar_commodity import (
    get_dce_option_daily,
    get_czce_option_daily,
    get_shfe_option_daily,
)

"""
英为财情-债券
"""
from akshare.bond.investing_bond import get_country_bond  # 债券-全球政府债券行情与收益率

"""
英为财情-指数
"""
from akshare.index.index_investing import get_country_index  # 股票指数-全球股指与期货指数数据接口

"""
99期货数据
"""
from akshare.futures.futures_inventory import get_inventory_data

"""
私募指数
"""
from akshare.fund.zdzk_fund import zdzk_fund_index

"""
中国银行间市场交易商协会
"""
from akshare.bond.bond_bank import get_bond_bank

"""
奇货可查-工具模块
"""
from akshare.qhkc.qhkc_tool import qhkc_tool_foreign, qhkc_tool_gdp

"""
奇货可查-指数模块
"""
from akshare.qhkc.qhkc_index import (
    get_qhkc_index,
    get_qhkc_index_trend,
    get_qhkc_index_profit_loss,
)

"""
奇货可查-资金模块
"""
from akshare.qhkc.qhkc_fund import (
    get_qhkc_fund_money_change,
    get_qhkc_fund_bs,
    get_qhkc_fund_position,
)

"""
大宗商品现货价格及基差
"""
from akshare.futures.basis import get_spot_price_daily, get_spot_price

"""
期货持仓成交排名数据
"""
from akshare.futures.cot import (
    get_rank_sum_daily,
    get_rank_sum,
    get_shfe_rank_table,
    get_czce_rank_table,
    get_dce_rank_table,
    get_cffex_rank_table,
)

"""
大宗商品仓单数据
"""
from akshare.futures.receipt import get_receipt

"""
大宗商品展期收益率数据
"""
from akshare.futures.roll_yield import get_roll_yield_bar, get_roll_yield

"""
交易所日线行情数据
"""
from akshare.futures.daily_bar import (
    get_cffex_daily,
    get_czce_daily,
    get_shfe_v_wap,
    get_shfe_daily,
    get_dce_daily,
    get_futures_daily,
)

"""
配置文件
"""
from akshare.futures import cons
from akshare.fund import cons

"""
发邮件模块
"""
from akshare.tool.send_email import send_email
