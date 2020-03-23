"""AkShare 是基于 Python 的开源金融数据接口库, 目的是实现对股票, 期货, 期权, 基金, 债券, 外汇等金融产品和另类数据从数据采集, 数据清洗到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于可信任数据源发布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 从而得出科学的结论."""

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
更新 qhkc_web 接口注释和说明文档
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
0.2.85
临时修复 baidu_index 接口
0.2.86
lxml 降级
0.2.87
lxml 降级
更新安装时的错误处理
0.2.88
pypinyin 降级
0.2.89
全国空气质量数据数据格式规范为数值型
0.2.90
更新注册仓单的产品参数和异常错误
0.2.91
世界五百强公司排名接口
0.2.92
更新中国债券市场行情数据接口
0.2.93
增加自动测试模型
0.2.94
增加私募基金管理人信息公示接口
0.2.95
增加中国证券投资基金业协会-信息公示
0.2.96
修复交易法门登录验证码
由于交易法门-数据部分权限缘故, 需要注册后方可使用
0.2.97
更新说明文档
0.2.98
增加甲醇期权和PTA期权
0.2.99
更新外汇数据接口, 规范格式
0.3.0
猫眼电影实时票房
0.3.1
更新说明文档
0.3.2
更新说明文档
0.3.3
更新外盘期货行情订阅时, 统一字段名称与网页端一致
0.3.4
新增能源-碳排放权数据
0.3.5
新增世界各大城市生活成本数据
0.3.6
商品现货价格指数
0.3.7
修复百度指数日期问题
0.3.8
新增中国宏观数据接口和文档说明
0.3.9
新增中国宏观杠杆率数据
0.3.10
修改金融期权数据接口
0.3.11
修复实时票房数据接口
0.3.12
新增新浪主力连续接口
0.3.13
新增新浪主力连续列表
0.3.14
中国倒闭公司名单
0.3.15
中国独角兽名单
中国千里马名单
0.3.16
东方财富-机构调研
0.3.17
东方财富网-数据中心-特色数据-机构调研
机构调研统计
机构调研详细
0.3.18
修复自动测试接口
0.3.19
修复融资融券字段名匹配问题
增加东方财富网-数据中心-特色数据-股票质押
0.3.20
东方财富网-数据中心-特色数据-股权质押
东方财富网-数据中心-特色数据-股权质押-股权质押市场概况: http://data.eastmoney.com/gpzy/marketProfile.aspx
东方财富网-数据中心-特色数据-股权质押-上市公司质押比例: http://data.eastmoney.com/gpzy/pledgeRatio.aspx
东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细: http://data.eastmoney.com/gpzy/pledgeDetail.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司: http://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行: http://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-行业数据: http://data.eastmoney.com/gpzy/industryData.aspx
0.3.21
东方财富网-数据中心-特色数据-商誉
东方财富网-数据中心-特色数据-商誉-A股商誉市场概况: http://data.eastmoney.com/sy/scgk.html
东方财富网-数据中心-特色数据-商誉-商誉减值预期明细: http://data.eastmoney.com/sy/yqlist.html
东方财富网-数据中心-特色数据-商誉-个股商誉减值明细: http://data.eastmoney.com/sy/jzlist.html
东方财富网-数据中心-特色数据-商誉-个股商誉明细: http://data.eastmoney.com/sy/list.html
东方财富网-数据中心-特色数据-商誉-行业商誉: http://data.eastmoney.com/sy/hylist.html
0.3.22
期货规则-交易日历数据表
更新2020交易日历数据
0.3.23
东方财富网-数据中心-特色数据-股票账户统计: http://data.eastmoney.com/cjsj/gpkhsj.html
0.3.24
移除-交易法门系列老函数
因为交易法门网站需要会员登录后访问数据
0.3.25
增加-交易法门-工具-套利分析接口
增加-交易法门-工具-交易规则接口
0.3.26
增加-交易法门-数据-农产品-豆油
增加-交易法门-数据-黑色系-焦煤
增加-交易法门-工具-持仓分析-期货分析
增加-交易法门-工具-持仓分析-持仓分析
0.3.27
交易法门-说明文档
0.3.28
增加-股票指数-股票指数成份股接口
0.3.29
增加-股票指数-股票指数成份股接口-代码注释
0.3.30
增加-义乌小商品指数
0.3.31
修复-银保监分局本级行政处罚数据接口
接口重命名为: bank_fjcf_table_detail
0.3.32
新增-中国电煤价格指数
0.3.33
修复-银保监分局本级行政处罚数据接口-20200108新增字段后适应
0.3.34
增加-交易法门-工具-期限分析-基差日报
增加-交易法门-工具-期限分析-基差分析
增加-交易法门-工具-期限分析-期限结构
增加-交易法门-工具-期限分析-价格季节性
0.3.35
更新说明文档
0.3.36
# 交易法门-工具-仓单分析
增加-交易法门-工具-仓单分析-仓单日报
增加-交易法门-工具-仓单分析-仓单查询
增加-交易法门-工具-仓单分析-虚实盘比查询
# 交易法门-工具-资讯汇总
增加-交易法门-工具-资讯汇总-研报查询
增加-交易法门-工具-资讯汇总-交易日历
# 交易法门-工具-资金分析
增加-交易法门-工具-资金分析-资金流向
0.3.37
更新说明文档
0.3.38
修改-交易法门-工具-资金分析-资金流向函数的字段和说明文档
0.3.39
金十数据中心-经济指标-央行利率-主要央行利率
美联储利率决议报告
欧洲央行决议报告
新西兰联储决议报告
中国央行决议报告
瑞士央行决议报告
英国央行决议报告
澳洲联储决议报告
日本央行决议报告
俄罗斯央行决议报告
印度央行决议报告
巴西央行决议报告
macro_euro_gdp_yoy #  金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况-欧元区季度GDP年率报告
macro_euro_cpi_mom #  金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI月率报告
macro_euro_cpi_yoy #  金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI年率报告
macro_euro_ppi_mom #  金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区PPI月率报告
macro_euro_retail_sales_mom #  金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区零售销售月率报告
macro_euro_employment_change_qoq #  金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区季调后就业人数季率报告
macro_euro_unemployment_rate_mom #  金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区失业率报告
macro_euro_trade_balance #  金十数据中心-经济指标-欧元区-贸易状况-欧元区未季调贸易帐报告
macro_euro_current_account_mom #  金十数据中心-经济指标-欧元区-贸易状况-欧元区经常帐报告
macro_euro_industrial_production_mom #  金十数据中心-经济指标-欧元区-产业指标-欧元区工业产出月率报告
macro_euro_manufacturing_pmi #  金十数据中心-经济指标-欧元区-产业指标-欧元区制造业PMI初值报告
macro_euro_services_pmi #  金十数据中心-经济指标-欧元区-产业指标-欧元区服务业PMI终值报告
macro_euro_zew_economic_sentiment #  金十数据中心-经济指标-欧元区-领先指标-欧元区ZEW经济景气指数报告
macro_euro_sentix_investor_confidence #  金十数据中心-经济指标-欧元区-领先指标-欧元区Sentix投资者信心指数报告
0.3.40
修复-欧洲央行决议报告
0.3.41
增加-东方财富网-经济数据-银行间拆借利率
0.3.42
# 中国
macro_china_gdp_yearly  # 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
macro_china_cpi_yearly  # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
macro_china_cpi_monthly  # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI月率报告
macro_china_ppi_yearly  # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
macro_china_exports_yoy  # 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
macro_china_imports_yoy  # 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
macro_china_trade_balance  # 金十数据中心-经济指标-中国-贸易状况-以美元计算贸易帐(亿美元)
macro_china_industrial_production_yoy  # 金十数据中心-经济指标-中国-产业指标-规模以上工业增加值年率
macro_china_pmi_yearly  # 金十数据中心-经济指标-中国-产业指标-官方制造业PMI
macro_china_cx_pmi_yearly  # 金十数据中心-经济指标-中国-产业指标-财新制造业PMI终值
macro_china_cx_services_pmi_yearly  # 金十数据中心-经济指标-中国-产业指标-财新服务业PMI
macro_china_non_man_pmi  # 金十数据中心-经济指标-中国-产业指标-中国官方非制造业PMI
macro_china_fx_reserves_yearly  # 金十数据中心-经济指标-中国-金融指标-外汇储备(亿美元)
macro_china_m2_yearly  # 金十数据中心-经济指标-中国-金融指标-M2货币供应年率
macro_china_shibor_all  # 金十数据中心-经济指标-中国-金融指标-上海银行业同业拆借报告
macro_china_hk_market_info  # 金十数据中心-经济指标-中国-金融指标-人民币香港银行同业拆息
macro_china_daily_energy  # 金十数据中心-经济指标-中国-其他-中国日度沿海六大电库存数据
macro_china_rmb  # 金十数据中心-经济指标-中国-其他-中国人民币汇率中间价报告
macro_china_market_margin_sz  # 金十数据中心-经济指标-中国-其他-深圳融资融券报告
macro_china_market_margin_sh  # 金十数据中心-经济指标-中国-其他-上海融资融券报告
macro_china_au_report  # 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
macro_china_ctci  # 发改委-中国电煤价格指数-全国综合电煤价格指数
macro_china_ctci_detail  # 发改委-中国电煤价格指数-各价区电煤价格指数
macro_china_ctci_detail_hist  # 发改委-中国电煤价格指数-历史电煤价格指数
# 美国
macro_usa_gdp_monthly  # 金十数据中心-经济指标-美国-经济状况-美国GDP
macro_usa_cpi_monthly  # 金十数据中心-经济指标-美国-物价水平-美国CPI月率报告
macro_usa_core_cpi_monthly  # 金十数据中心-经济指标-美国-物价水平-美国核心CPI月率报告
macro_usa_personal_spending  # 金十数据中心-经济指标-美国-物价水平-美国个人支出月率报告
macro_usa_retail_sales  # 金十数据中心-经济指标-美国-物价水平-美国零售销售月率报告
macro_usa_import_price  # 金十数据中心-经济指标-美国-物价水平-美国进口物价指数报告
macro_usa_export_price  # 金十数据中心-经济指标-美国-物价水平-美国出口价格指数报告
macro_usa_lmci  # 金十数据中心-经济指标-美国-劳动力市场-LMCI
macro_usa_unemployment_rate  # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国失业率报告
macro_usa_job_cuts  # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国挑战者企业裁员人数报告
macro_usa_non_farm  # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国非农就业人数报告
macro_usa_adp_employment  # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国ADP就业人数报告
macro_usa_core_pce_price  # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国核心PCE物价指数年率报告
macro_usa_real_consumer_spending  # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国实际个人消费支出季率初值报告
macro_usa_trade_balance  # 金十数据中心-经济指标-美国-贸易状况-美国贸易帐报告
macro_usa_current_account  # 金十数据中心-经济指标-美国-贸易状况-美国经常帐报告
macro_usa_rig_count  # 金十数据中心-经济指标-美国-产业指标-制造业-贝克休斯钻井报告
# 金十数据中心-经济指标-美国-产业指标-制造业-美国个人支出月率报告
macro_usa_ppi  # 金十数据中心-经济指标-美国-产业指标-制造业-美国生产者物价指数(PPI)报告
macro_usa_core_ppi  # 金十数据中心-经济指标-美国-产业指标-制造业-美国核心生产者物价指数(PPI)报告
macro_usa_api_crude_stock  # 金十数据中心-经济指标-美国-产业指标-制造业-美国API原油库存报告
macro_usa_pmi  # 金十数据中心-经济指标-美国-产业指标-制造业-美国Markit制造业PMI初值报告
macro_usa_ism_pmi  # 金十数据中心-经济指标-美国-产业指标-制造业-美国ISM制造业PMI报告
macro_usa_nahb_house_market_index  # 金十数据中心-经济指标-美国-产业指标-房地产-美国NAHB房产市场指数报告
macro_usa_house_starts  # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋开工总数年化报告
macro_usa_new_home_sales  # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋销售总数年化报告
macro_usa_building_permits  # 金十数据中心-经济指标-美国-产业指标-房地产-美国营建许可总数报告
macro_usa_exist_home_sales  # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋销售总数年化报告
macro_usa_house_price_index  # 金十数据中心-经济指标-美国-产业指标-房地产-美国FHFA房价指数月率报告
macro_usa_spcs20 # 金十数据中心-经济指标-美国-产业指标-房地产-美国S&P/CS20座大城市房价指数年率报告
macro_usa_pending_home_sales  # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋签约销售指数月率报告
macro_usa_cb_consumer_confidence  # 金十数据中心-经济指标-美国-领先指标-美国谘商会消费者信心指数报告
macro_usa_nfib_small_business # 金十数据中心-经济指标-美国-领先指标-美国NFIB小型企业信心指数报告
macro_usa_michigan_consumer_sentiment # 金十数据中心-经济指标-美国-领先指标-美国密歇根大学消费者信心指数初值报告
macro_usa_eia_crude_rate  # 金十数据中心-经济指标-美国-其他-美国EIA原油库存报告
macro_usa_initial_jobless  # 金十数据中心-经济指标-美国-其他-美国初请失业金人数报告
macro_usa_crude_inner  # 金十数据中心-经济指标-美国-其他-美国原油产量报告
macro_usa_crude_state  # 金十数据中心-经济指标-美国-其他-美国本土48州原油产量
macro_usa_crude_alaska  # 金十数据中心-经济指标-美国-其他-美国阿拉斯加州原油产量
0.3.43
增加-交易法门-数据-黑色系-焦煤
0.3.44
更新宏观数据
macro_cons_gold_volume  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
macro_cons_gold_change  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
macro_cons_gold_amount  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
macro_cons_silver_volume  # 全球最大白银ETF--iShares Silver Trust持仓报告
macro_cons_silver_change  # 全球最大白银ETF--iShares Silver Trust持仓报告
macro_cons_silver_amount  # 全球最大白银ETF--iShares Silver Trust持仓报告
macro_cons_opec_near_change  # 欧佩克报告-变动
macro_cons_opec_month  # 欧佩克报告-月度
0.3.45
增加中国证券投资基金业协会-信息公示
# 中国证券投资基金业协会-信息公示-会员信息
amac_member_info # 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
# 中国证券投资基金业协会-信息公示-从业人员信息
amac_person_org_list # 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
amac_person_org_list_ext # 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册外部公示信息
# 中国证券投资基金业协会-信息公示-私募基金管理人公示
amac_manager_info # 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
amac_manager_classify_info # 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
amac_member_sub_info # 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
# 中国证券投资基金业协会-信息公示-基金产品
amac_fund_info # 中国证券投资基金业协会-信息公示-基金产品-私募基金管理人基金产品
amac_securities_info # 中国证券投资基金业协会-信息公示-基金产品-证券公司集合资管产品公示
amac_aoin_info # 中国证券投资基金业协会-信息公示-基金产品-证券公司直投基金
amac_fund_sub_info # 中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
amac_fund_account_info # 中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
amac_fund_abs # 中国证券投资基金业协会-信息公示-基金产品公示-资产支持专项计划
amac_futures_info # 中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
# 中国证券投资基金业协会-信息公示-诚信信息
amac_manager_xxgs_hmd # 中国证券投资基金业协会-信息公示-诚信信息-违反自律规则黑名单
amac_manager_xxgs_jlcf # 中国证券投资基金业协会-信息公示-诚信信息-纪律处分
amac_manager_xxgs_cxdj # 中国证券投资基金业协会-信息公示-诚信信息-撤销管理人登记的名单
amac_manager_cancelled_info # 中国证券投资基金业协会-信息公示-诚信信息-已注销私募基金管理人名单
0.3.46
更新-商品期权-菜籽粕期权接口
修复 get_sector_futures 字段名问题
0.3.47
增加-商品期权-郑州商品交易所-期权-历史数据
0.3.48
修复 macro_cons_opec_month 接口数据更新问题
0.3.49
新增-交易法门-工具-仓单分析-虚实盘比日报接口
0.3.50
更新-说明文档
0.3.51
修复 macro_cons_opec_month 接口数据更新问题, 统一数据接口跟网页端统一
修复-百度指数-由用户输入cookie来访问数据及说明文档
0.3.52
新增-英为财情-外汇-货币对历史数据
0.3.53
修复-macro_usa_rig_count-接口返回数据
修复-rate_interbank-文档注释
0.3.54
新增-事件接口
新增-事件接口新型冠状病毒-网易
新增-事件接口新型冠状病毒-丁香园
0.3.55
更新-事件接口新型冠状病毒
0.3.56
更新-事件接口新型冠状病毒-全国疫情趋势图
0.3.57
更新-事件接口新型冠状病毒-分省地区
一些细节修复
0.3.58
新增-财富排行榜(英文版)
0.3.59
新增-currency_name_code-接口
0.3.60
修复-财富排行榜(英文版)-索引乱序问题
0.3.61
修复-事件接口新型冠状病毒-hospital-接口
0.3.62
修复-20200203交易日问题
0.3.63
修复-事件接口新型冠状病毒-网易接口
0.3.64
修复-事件接口新型冠状病毒-丁香园接口
0.3.65
修复-calendar.json 问题, 感谢 fxt0706
0.3.66
修复-epu_index-加载问题
0.3.67
修复-option_commodity-json数据加载问题
0.3.68
更名函数 movie_board -> box_office_spot
0.3.69
新增-epidemic_baidu
百度-新型冠状病毒肺炎-疫情实时大数据报告
0.3.70
修复-epidemic_dxy-字段问题
0.3.71
修复-epidemic_dxy-具体省份字段问题
0.3.72
新增-百度迁徙地图接口
0.3.73
修复文字表述
0.3.74
修复-epidemic_163-数据更新问题
0.3.75
修复-epidemic_dxy-图片显示问题
0.3.76
新增-stock_zh_index_daily_tx-补充新浪指数的数据缺失问题
0.3.77
修复-epidemic_163-数据更新问题
0.3.78
新增-bond_china_yield-中国债券信息网-国债及其他债券收益率曲线
0.3.79
修改-bond_china_yield-参数
0.3.80
新增-基金数据接口
0.3.81
新增-基金数据接口-净值
0.3.82
新增-小区查询
新增-相同行程查询
0.3.83
新增-交易法门-工具-套利分析-FullCarry
修改-交易法门-工具-期限分析-基差分析
0.3.84
新增-货币对-投机情绪报告
0.3.85
修复-epidemic_area_detail-增加下载进度提示
0.3.86
修复-epidemic_dxy-完善图片获取
0.3.87
新增-债券质押式回购成交明细数据
新增-细化到地市的疫情历史数据20200123至今
0.3.88
新增-交易法门-工具-持仓分析-持仓季节性
修复-epidemic_163
0.3.89
新增-epidemic_163-数据说明接口
0.3.90
修复-epidemic_dxy
0.3.91
修复-get_receipt-MA数值问题
0.3.92
新增-奇货可查接口测试
0.3.93
新增-奇货可查接口测试-代码补全
0.3.94
修复-epidemic_dxy
0.3.95
新增-债券-沪深债券
新增-债券-沪深可转债
0.3.96
修复-baidu_search_index-异常
0.3.97
新增-特许经营数据
0.3.98
修复-get_receipt-MA数值问题条件判断
0.3.99
修复-air_hebei-代码格式
0.4.1
修复-pandas-版本降级
0.4.2
修复-epidemic_baidu
0.4.3
新增-慈善中国
0.4.4
新增-epidemic_history-疫情所有历史数据
0.4.5
完善-慈善中国-类型注解
0.4.6
修复-charity_china_report
0.4.7
新增-测试接口
0.4.8
修复-epidemic_hist_all
修复-epidemic_hist_city
修复-epidemic_hist_province
0.4.9
新增-option_sina_cffex_hs300_list
新增-option_sina_cffex_hs300_spot
新增-option_sina_cffex_hs300_daily
新增-option_sina_sse_list
新增-option_sina_sse_expire_day
新增-option_sina_sse_codes
新增-option_sina_sse_spot_price
新增-option_sina_sse_underlying_spot_price
新增-option_sina_sse_greeks
新增-option_sina_sse_minute
新增-option_sina_sse_daily
0.4.10
修复-金十数据websocket接口
0.4.11
新增-交易法门-工具-资金分析-资金流向
新增-交易法门-工具-资金分析-沉淀资金
新增-交易法门-工具-资金分析-资金季节性
新增-交易法门-工具-资金分析-成交排名
0.4.12
新增-微博舆情报告
0.4.13
新增-Python3.8.1支持
0.4.14
修复-get_receipt-CZCE问题
0.4.15
修复-hf_subscribe_exchange_symbol-在Linux Python 3.8.1 报错问题
0.4.16
修复-get_js_dc_current
0.4.17
新增-知识图谱
0.4.18: fix: use tqdm replace print hints
0.4.19: fix: use tqdm replace print hints in energy_carbon.py and charity_china.py
0.4.20: add: jyfm_tools_position_structure and jyfm_tools_symbol_handbook
0.4.21: fix: macro_cons_opec_month print hints
0.4.22: fix: add tqdm desc
0.4.23: fix: add tqdm stock_zh_a_spot desc
0.4.24: fix: add get_us_stock_name to get the u.s. stock name
0.4.25: fix: upload setup.py file and set automate release and deploy
0.4.26: fix: bond_spot_quote and docs
0.4.27: test: automate test
0.4.28: test: automate test
0.4.29: feats: add currency interface
0.4.30: fix: roll_yield.py/get_roll_yield: CUefp error
0.4.31: format: format currency.py
0.4.32: fix: china_bond.py
0.4.33: add: jyfm_tools_futures_arbitrage_matrix for jyfm futures
0.4.34: fix: get_czce_rank_table history-20171228 format
0.4.35: fix: get_czce_rank_table history-20071228 format
0.4.36: fix: macro_cons_opec_month
0.4.37: add: get_ine_daily to fetch SC and NR data
0.4.38: add: futures_sgx_daily to fetch futures data from sgx
0.4.39: refactor: covid.py/covid_19_163 interface
0.4.40: refactor: covid.py interface
0.4.41: fix: cot.py get_rank_sum_daily interface
0.4.42: add: wdbank.py test
0.4.43: add: wdbank.py dependencies
0.4.44: add: tool github
0.4.45: add: fund_public file and docs
0.4.46: add: macro_china_lpr
0.4.47: add: stock_em_analyst
0.4.48: add: stock_em_comment
"""

__version__ = "0.4.48"
__author__ = "Albert King"

"""
stock-em-comment
"""
from akshare.stock_feature.stock_em_comment import stock_em_comment

"""
stock-em-analyst
"""
from akshare.stock_feature.stock_em_analyst import stock_em_analyst_detail, stock_em_analyst_rank

"""
tool-github
"""
from akshare.tool.tool_github import tool_github_star_list, tool_github_email_address

"""
sgx futures data
"""
from akshare.futures.futures_sgx_daily import futures_sgx_daily

"""
currency interface
"""
from akshare.currency.currency import (
    currency_convert,
    currency_currencies,
    currency_history,
    currency_latest,
    currency_time_series,
)

"""
知识图谱
"""
from akshare.nlp.nlp_interface import nlp_ownthink

"""
微博舆情报告
"""
from akshare.stock.stock_weibo_nlp import stock_js_weibo_nlp_time, stock_js_weibo_report

"""
金融期权-新浪
"""
from akshare.option.option_finance_sina import (
    option_sina_cffex_hs300_list,
    option_sina_cffex_hs300_spot,
    option_sina_cffex_hs300_daily,
    option_sina_sse_list,
    option_sina_sse_expire_day,
    option_sina_sse_codes,
    option_sina_sse_spot_price,
    option_sina_sse_underlying_spot_price,
    option_sina_sse_greeks,
    option_sina_sse_minute,
    option_sina_sse_daily,
)

"""
中国-慈善
"""
from akshare.charity.charity_china import (
    charity_china_organization,
    charity_china_plan,
    charity_china_platform,
    charity_china_progress,
    charity_china_report,
    charity_china_trust,
)

"""
中国-特许经营数据
"""
from akshare.event.franchise import franchise_china

"""
债券-沪深债券
"""
from akshare.bond.zh_bond_sina import bond_zh_hs_daily, bond_zh_hs_spot
from akshare.bond.zh_bond_cov_sina import bond_zh_hs_cov_daily, bond_zh_hs_cov_spot

"""
for pro api
"""
from akshare.pro.data_pro import pro_api

"""
for pro api token set
"""
from akshare.utils.token_process import set_token

"""
债券质押式回购成交明细数据
"""
from akshare.bond.china_repo import bond_repo_zh_tick

"""
新型肺炎
"""
from akshare.event.covid import (
    covid_19_area_search,
    covid_19_area_all,
    covid_19_area_detail,
    covid_19_trip,
    covid_19_history,
)

"""
基金数据接口
"""
from akshare.fund.fund_em import fund_em_daily, fund_em_info

"""
百度迁徙地图接口
"""
from akshare.event.covid import migration_area_baidu, migration_scale_baidu

"""
新增-事件接口新型冠状病毒接口
"""
from akshare.event.covid import (
    covid_19_163,
    covid_19_dxy,
    covid_19_baidu,
    covid_19_hist_city,
    covid_19_hist_province,
)

"""
英为财情-外汇-货币对历史数据
"""
from akshare.fx.currency_investing import (
    currency_hist,
    currency_name_code,
)

"""
商品期权-郑州商品交易所-期权-历史数据
"""
from akshare.option.czce_option import option_czce_hist

"""
宏观-经济数据-银行间拆借利率
"""
from akshare.interest_rate.interbank_rate_em import rate_interbank

"""
东方财富网-经济数据-银行间拆借利率
"""
from akshare.interest_rate.interbank_rate_em import rate_interbank

"""
金十数据中心-外汇情绪
"""
from akshare.economic.macro_other import macro_fx_sentiment

"""
金十数据中心-经济指标-欧元区
"""
from akshare.economic.macro_euro import (
    macro_euro_gdp_yoy,
    macro_euro_cpi_mom,
    macro_euro_cpi_yoy,
    macro_euro_current_account_mom,
    macro_euro_employment_change_qoq,
    macro_euro_industrial_production_mom,
    macro_euro_manufacturing_pmi,
    macro_euro_ppi_mom,
    macro_euro_retail_sales_mom,
    macro_euro_sentix_investor_confidence,
    macro_euro_services_pmi,
    macro_euro_trade_balance,
    macro_euro_unemployment_rate_mom,
    macro_euro_zew_economic_sentiment,
)

"""
金十数据中心-经济指标-央行利率-主要央行利率
"""
from akshare.economic.macro_bank import (
    macro_bank_australia_interest_rate,
    macro_bank_brazil_interest_rate,
    macro_bank_china_interest_rate,
    macro_bank_brazil_interest_rate,
    macro_bank_english_interest_rate,
    macro_bank_euro_interest_rate,
    macro_bank_india_interest_rate,
    macro_bank_japan_interest_rate,
    macro_bank_newzealand_interest_rate,
    macro_bank_russia_interest_rate,
    macro_bank_switzerland_interest_rate,
    macro_bank_usa_interest_rate,
)

"""
交易法门-工具-席位分析
"""
from akshare.futures_derivative.jyfm_tools_func import jyfm_tools_position_structure

"""
交易法门-工具-套利分析
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_futures_spread,
    jyfm_tools_futures_ratio,
    jyfm_tools_futures_customize,
    jyfm_exchange_symbol_dict,
    jyfm_tools_futures_full_carry,
    jyfm_tools_futures_arbitrage_matrix,
)

"""
交易法门-工具-资讯汇总
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_research_query,
    jyfm_tools_trade_calendar,
)

"""
交易法门-工具-持仓分析
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_position_detail,
    jyfm_tools_position_seat,
    jyfm_tools_position_season,
)

"""
交易法门-工具-资金分析
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_position_fund_direction,
    jyfm_tools_position_fund_down,
    jyfm_tools_position_fund_season,
    jyfm_tools_position_fund_deal,
)

"""
交易法门-工具-仓单分析
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_warehouse_receipt_daily,
    jyfm_tools_warehouse_receipt_query,
    jyfm_tools_warehouse_virtual_fact_ratio,
    jyfm_tools_warehouse_virtual_fact_daily,
)

"""
交易法门-工具-期限分析
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_futures_basis_daily,
    jyfm_tools_futures_basis_daily_area,
    jyfm_tools_futures_basis_analysis,
    jyfm_tools_futures_basis_structure,
    jyfm_tools_futures_basis_rule,
)

"""
交易法门-工具-交易规则
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_receipt_expire_info,
    jyfm_tools_position_limit_info,
    jyfm_tools_symbol_handbook,
)

"""
义乌小商品指数
"""
from akshare.index.index_yw import index_yw

"""
股票指数-股票指数-成份股
"""
from akshare.index.index_cons import (
    index_stock_info,
    index_stock_cons,
)

"""
交易法门-工具-数据-黑色系
"""
from akshare.futures_derivative.jyfm_data_func import (
    jyfm_data_cocking_coal,
    jyfm_data_coke,
)

"""
东方财富-股票账户
"""
from akshare.stock_feature.stock_em_account import stock_em_account

"""
期货规则
"""
from akshare.futures.futures_rule import futures_rule

"""
东方财富-商誉专题
"""
from akshare.stock_feature.stock_em_sy import (
    stock_em_sy_profile,
    stock_em_sy_yq_list,
    stock_em_sy_jz_list,
    stock_em_sy_list,
    stock_em_sy_hy_list,
)

"""
东方财富-股票质押
"""
from akshare.stock_feature.stock_em_gpzy import (
    stock_em_gpzy_pledge_ratio,
    stock_em_gpzy_profile,
    stock_em_gpzy_distribute_statistics_bank,
    stock_em_gpzy_distribute_statistics_company,
    stock_em_gpzy_industry_data,
    stock_em_gpzy_pledge_ratio_detail,
)

"""
东方财富-机构调研
"""
from akshare.stock_feature.stock_em_jgdy import stock_em_jgdy_tj, stock_em_jgdy_detail

"""
新浪主力连续接口
"""
from akshare.fortune.it_juzi import death_company, maxima_company, nicorn_company

"""
新浪主力连续接口
"""
from akshare.futures_derivative.sina_futures_index import (
    futures_main_sina,
    futures_display_main_sina,
)

"""
中国宏观杠杆率数据
"""
from akshare.economic.marco_cnbs import macro_cnbs

"""
大宗商品-现货价格指数
"""
from akshare.index.index_spot import spot_goods

"""
成本-世界各大城市生活成本
"""
from akshare.cost.cost_living import cost_living

"""
能约-碳排放权
"""
from akshare.energy.energy_carbon import energy_carbon

"""
猫眼电影实时票房
"""
from akshare.movie.movie_maoyan import box_office_spot

"""
中国证券投资基金业协会-信息公示
"""
from akshare.fund.fund_amac import (
    amac_manager_info,
    amac_member_info,
    amac_member_sub_info,
    amac_aoin_info,
    amac_fund_account_info,
    amac_fund_info,
    amac_fund_sub_info,
    amac_futures_info,
    amac_manager_cancelled_info,
    amac_securities_info,
    amac_fund_abs,
    amac_manager_classify_info,
    amac_manager_xxgs_cxdj,
    amac_manager_xxgs_hmd,
    amac_manager_xxgs_jlcf,
    amac_person_org_list,
    amac_person_org_list_ext,
)

"""
世界五百强公司排名接口
"""
from akshare.fortune.fortune_500 import fortune_rank, fortune_rank_eng

"""
AQI空气质量接口
"""
from akshare.air.aqi_study import air_all_city, air_city_list, air_daily, air_hourly

"""
申万行业一级
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
    jyfm_data_soybean_oil,  # 豆油
)

"""
交易法门-工具
"""
from akshare.futures_derivative.jyfm_tools_func import (
    jyfm_tools_futures_customize,  # 棕榈
    jyfm_tools_futures_ratio,  # 豆粕
    jyfm_tools_futures_spread,  # 白糖
    jyfm_tools_receipt_expire_info,  # 美豆
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
from akshare.air.air_hebei import air_hebei

"""
timeanddate-日出和日落
"""
from akshare.air.time_and_date import weather_daily, weather_monthly

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
from akshare.index.zh_stock_index_sina import (
    stock_zh_index_daily,
    stock_zh_index_spot,
    stock_zh_index_daily_tx,
)

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
from akshare.bank.bank_cbirc_2020 import bank_fjcf_table_detail

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
from akshare.option.option_finance import (
    option_finance_board,
    option_finance_underlying,
)

"""
新浪-美股实时行情数据和历史行情数据(前复权)
"""
from akshare.stock.us_stock_sina import stock_us_daily, stock_us_spot, get_us_stock_name

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
    macro_cons_gold_amount,
    macro_cons_gold_change,
    macro_cons_gold_volume,
    macro_cons_opec_month,
    macro_cons_opec_near_change,
    macro_cons_silver_amount,
    macro_cons_silver_change,
    macro_cons_silver_volume,
)

"""
全球宏观-美国宏观
"""
from akshare.economic.macro_usa import (
    macro_usa_eia_crude_rate,
    macro_usa_non_farm,
    macro_usa_unemployment_rate,
    macro_usa_adp_employment,
    macro_usa_core_pce_price,
    macro_usa_cpi_monthly,
    macro_usa_crude_alaska,
    macro_usa_crude_inner,
    macro_usa_crude_state,
    macro_usa_gdp_monthly,
    macro_usa_initial_jobless,
    macro_usa_lmci,
    macro_usa_api_crude_stock,
    macro_usa_building_permits,
    macro_usa_business_inventories,
    macro_usa_cb_consumer_confidence,
    macro_usa_core_cpi_monthly,
    macro_usa_core_ppi,
    macro_usa_current_account,
    macro_usa_durable_goods_orders,
    macro_usa_trade_balance,
    macro_usa_spcs20,
    macro_usa_services_pmi,
    macro_usa_rig_count,
    macro_usa_retail_sales,
    macro_usa_real_consumer_spending,
    macro_usa_ppi,
    macro_usa_pmi,
    macro_usa_personal_spending,
    macro_usa_pending_home_sales,
    macro_usa_nfib_small_business,
    macro_usa_new_home_sales,
    macro_usa_nahb_house_market_index,
    macro_usa_michigan_consumer_sentiment,
    macro_usa_exist_home_sales,
    macro_usa_export_price,
    macro_usa_factory_orders,
    macro_usa_house_price_index,
    macro_usa_house_starts,
    macro_usa_import_price,
    macro_usa_industrial_production,
    macro_usa_ism_non_pmi,
    macro_usa_ism_pmi,
    macro_usa_job_cuts,
)

"""
全球宏观-中国宏观
"""
from akshare.economic.macro_china import (
    macro_china_cpi_monthly,
    macro_china_cpi_yearly,
    macro_china_m2_yearly,
    macro_china_fx_reserves_yearly,
    macro_china_cx_pmi_yearly,
    macro_china_pmi_yearly,
    macro_china_daily_energy,
    macro_china_non_man_pmi,
    macro_china_rmb,
    macro_china_gdp_yearly,
    macro_china_ppi_yearly,
    macro_china_cx_services_pmi_yearly,
    macro_china_market_margin_sh,
    macro_china_market_margin_sz,
    macro_china_au_report,
    macro_china_ctci_detail,
    macro_china_ctci_detail_hist,
    macro_china_ctci,
    macro_china_exports_yoy,
    macro_china_hk_market_info,
    macro_china_imports_yoy,
    macro_china_trade_balance,
    macro_china_shibor_all,
    macro_china_industrial_production_yoy,
    macro_china_lpr,
)

"""
全球期货
"""
from akshare.futures.international_futures import get_sector_futures

"""
外汇
"""
from akshare.fx.fx_quote import fx_pair_quote, fx_spot_quote, fx_swap_quote

"""
债券行情
"""
from akshare.bond.china_bond import bond_spot_quote, bond_spot_deal, bond_china_yield

"""
商品期权
"""
from akshare.option.option_commodity import (
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
from akshare.fund.fund_zdzk import zdzk_fund_index

"""
中国银行间市场交易商协会
"""
from akshare.bond.bond_bank import get_bond_bank

"""
奇货可查-工具模块
"""
from akshare.qhkc_web.qhkc_tool import qhkc_tool_foreign, qhkc_tool_gdp

"""
奇货可查-指数模块
"""
from akshare.qhkc_web.qhkc_index import (
    get_qhkc_index,
    get_qhkc_index_trend,
    get_qhkc_index_profit_loss,
)

"""
奇货可查-资金模块
"""
from akshare.qhkc_web.qhkc_fund import (
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
