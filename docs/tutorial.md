# [AKShare](https://github.com/jindaxiang/akshare) 快速入门

## 查看数据

具体函数使用详情, 请查看 [AKShare 文档](https://akshare.readthedocs.io/) 每个接口的示例代码

[AKShare](https://github.com/jindaxiang/akshare) 数据接口一览表

```
 # 交易所期货数据
 "get_cffex_daily",  # 获取中国金融期货交易所每日交易数据
 "get_cffex_rank_table",  # 获取中国金融期货交易所前20会员持仓数据明细
 "get_czce_daily",  # 获取郑州商品交易所每日交易数据
 "get_czce_rank_table",  # 获取郑州商品交易所前20会员持仓数据明细
 "get_dce_daily",  # 获取大连商品交易所每日交易数据
 "get_ine_daily",  # 获取上海国际能源交易中心每日交易数据
 "futures_sgx_daily",  # 获取新加坡交易所每日交易数据
 "get_dce_rank_table",  #获取大连商品交易所前20会员持仓数据明细
 "get_futures_daily",  # 获取中国金融期货交易所每日基差数据
 "get_rank_sum",  # 获取四个期货交易所前5, 10, 15, 20会员持仓排名数据
 "get_rank_sum_daily",  # 获取每日四个期货交易所前5, 10, 15, 20会员持仓排名数据
 "futures_dce_position_rank",  # 大连商品交易所前 20 会员持仓排名数据
 "get_receipt",  # 获取大宗商品注册仓单数据
 "get_roll_yield",  # 获取某一天某品种(主力和次主力)或固定两个合约的展期收益率
 "get_roll_yield_bar",  # 获取展期收益率
 "get_shfe_daily",  # 获取上海期货交易所每日交易数据
 "get_shfe_rank_table",  # 获取上海期货交易所前20会员持仓数据明细
 "get_shfe_v_wap",  # 获取上海期货交易所日成交均价数据
 "futures_spot_price",  # 获取具体交易日大宗商品现货价格及相应基差数据
 "futures_spot_price_previous",  # 获取具体交易日大宗商品现货价格及相应基差数据-该接口补充历史数据
 "futures_spot_price_daily"  # 获取一段交易日大宗商品现货价格及相应基差数据
 "futures_czce_warehouse_receipt"  # 郑州商品交易所-交易数据-仓单日报
 "futures_shfe_warehouse_receipt"  # 上海期货交易所-交易数据-仓单日报
 "futures_dce_warehouse_receipt"  # 大连商品交易所-交易数据-仓单日报
 "futures_rule"  # 国泰君安-交易日历
 # 奇货可查数据
 "get_qhkc_index"  # 获取奇货可查-指数-数值数据
 "get_qhkc_index_profit_loss"  # 获取奇货可查-指数-累计盈亏数据
 "get_qhkc_index_trend"  # 获取奇货可查-指数-大资金动向数据
 "get_qhkc_fund_bs"  # 获取奇货可查-资金-净持仓分布数据
 "get_qhkc_fund_position"  # 获取奇货可查-资金-总持仓分布数据
 "get_qhkc_fund_position_change"  # 获取奇货可查-资金-净持仓变化分布数据
 "get_qhkc_tool_foreign"  # 获取奇货可查-工具-外盘比价数据
 "get_qhkc_tool_gdp"  # 获取奇货可查-工具-各地区经济数据
 # 中国银行间市场交易所数据
 "get_bond_bank"  # 获取中国银行间市场交易商协会-债券数据
 # 提供英为财情数据接口
 "index_investing_global"  # 提供英为财情-股票指数-全球股指与期货指数数据
 "bond_investing_global"  # 提供英为财情-债券数据-全球政府债券行情与收益率数据
 # 交易所商品期权数据
 "get_dce_option_daily"  # 提供大连商品交易所商品期权数据
 "get_czce_option_daily"  # 提供郑州商品交易所商品期权数据
 "get_shfe_option_daily"  # 提供上海期货交易所商品期权数据
 # 中国银行间市场债券行情数据
 "get_bond_market_quote"  # 债券市场行情-现券市场成交行情数据
 "get_bond_market_trade"  # 债券市场行情-现券市场做市报价数据
 # 外汇
 "get_fx_spot_quote"  # 人民币外汇即期报价数据
 "get_fx_swap_quote"  # 人民币外汇远掉报价数据
 "get_fx_pair_quote"  # 外币对即期报价数据
 # 商品
 "get_sector_futures"  # 全球商品数据数据
 # 宏观-欧洲
 "get_euro_interest_rate"  # 欧洲央行决议报告
 # 宏观-主要机构
 "get_cons_gold_amount"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告-总价值
 "get_cons_gold_change"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告-增持/减持
 "get_cons_gold_volume"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告-总库存
 "get_cons_opec_month"  # 欧佩克报告-差异
 "get_cons_opec_near_change"  # 欧佩克报告-月份
 "get_cons_silver_amount"  # 全球最大白银ETF--iShares Silver Trust持仓报告-总价值
 "get_cons_silver_change"  # 全球最大白银ETF--iShares Silver Trust持仓报告-增持/减持
 "get_cons_silver_volume"  # 全球最大白银ETF--iShares Silver Trust持仓报告-总库存
 # 期货-仓单有效期
 "get_receipt_date"  # 期货仓单有效期数据
 # 新浪财经-期货
 "futures_zh_spot"  # 获取新浪-国内期货实时行情数据
 "futures_hq_spot"  # 获取新浪-外盘期货实时行情数据
 "futures_foreign_hist"  # 获取新浪-外盘期货历史行情数据
 "futures_foreign_detail"  # 获取新浪-外盘期货合约详情
 "futures_zh_minute_sina"  # 获取新浪-内盘分时数据
 # 交易所金融期权数据
 "get_finance_option"  # 提供上海证券交易所期权数据
 # 加密货币行情
 "crypto_js_spot"  # 提供主流加密货币行情数据接口
 # 股票-企业社会责任
 "stock_zh_a_scr_report"  # 企业社会责任数据
 # 美股-中国概念股行情和历史数据
 "stock_us_zh_spot"  # 中国概念股行情
 "stock_us_zh_daily"  # 中国概念股历史数据
 # 新浪财经-港股
 "stock_hk_spot"  # 获取港股的历史行情数据(包括前后复权因子)
 "stock_hk_daily"  # 获取港股的实时行情数据(也可以用于获得所有港股代码)
 # 新浪财经-美股
 "get_us_stock_name"  # 获得美股的所有股票代码
 "stock_us_spot"  # 获取美股行情报价
 "stock_us_daily"  # 获取美股的历史数据(包括前复权因子)
 "stock_us_fundamental"  # 获取美股的基本面数据
 # A+H股实时行情数据和历史行情数据
 "stock_zh_ah_spot"  # 获取 A+H 股实时行情数据(延迟15分钟)
 "stock_zh_ah_daily"  # 获取 A+H 股历史行情数据(日频)
 "stock_zh_ah_name"  # 获取 A+H 股所有股票代码
 # A股实时行情数据和历史行情数据
 "stock_zh_a_spot"  # 获取 A 股实时行情数据
 "stock_zh_a_daily"  # 获取 A 股历史行情数据(日频)
 "stock_zh_a_minute"  # 获取 A 股分时历史行情数据(分钟)
 "stock_zh_a_cdr_daily"  # 获取 A 股 CDR 历史行情数据(日频)
 # 科创板实时行情数据和历史行情数据
 "stock_zh_kcb_spot"  # 获取科创板实时行情数据
 "stock_zh_kcb_daily"  # 获取科创板历史行情数据(日频)
 # 银保监分局本级行政处罚数据
 "bank_fjcf_table_detail"  # 获取银保监分局本级行政处罚-信息公开表
 # 已实现波动率数据
 "article_oman_rv"  # O-MAN已实现波动率
 "article_rlab_rv"  # Risk-Lab已实现波动率
 # FF多因子模型数据
 "ff_crr"  # FF当前因子
 # 指数实时行情和历史行情
 "stock_zh_index_daily"  # 股票指数历史行情数据
 "stock_zh_index_daily_tx"  # 股票指数历史行情数据-腾讯
 "stock_zh_index_daily_em"  # 股票指数历史行情数据-东方财富
 "stock_zh_index_spot"  # 股票指数实时行情数据
 # 股票分笔数据
 "stock_zh_a_tick_tx"  # A 股票分笔行情数据(近2年)-腾讯
 "stock_zh_a_tick_tx_js"  # A 股票分笔行情数据(近2年)-腾讯-当日数据
 "stock_zh_a_tick_163"  # A 股票分笔行情数据(近5个交易日)-163
 # Websocket 实时监控
 "watch_jinshi_fx"  # 外汇实时接口
 "watch_jinshi_quotes"  # 行情报价接口
 # 世界各地区日出和日落数据-日
 "weather_daily"  # 每日日出和日落数据
 # 世界各地区日出和日落数据-月
 "weather_monthly"  # 每月日出和日落数据
 # 河北空气质量数据(期货-钢铁)
 "air_quality_hebei"  # 河北空气质量数据
 # 南华期货-南华指数-波动率指数
 "nh_volatility_index"  # 波动率指数
 # 南华期货-南华指数-价格指数
 "nh_price_index"  # 价格指数
 # 南华期货-南华指数-收益率指数
 "nh_return_index"  # 收益率指数
 # 经济政策不确定性(EPU)指数
 "article_epu_index"  # 主要国家和地区的经济政策不确定性(EPU)指数
 # 微博指数
 "weibo_index"  # 获取3个月内的微博指数
 # 百度指数
 "baidu_search_index"  # 获取百度搜索指数
 "baidu_info_index"  # 获取百度资讯指数
 "baidu_media_index"  # 获取百度媒体指数
 # 谷歌指数
 "google_index"  # 获取谷歌趋势指数
 # 申万行业指数
 "sw_index_spot"  # 获取申万一级实时行情
 "sw_index_cons"  # 获取申万一级板块成份
 "sw_index_daily"  # 获取申万一级历史行情
 "sw_index_daily_indicator"  # 获取申万一级历史行情指标
 # 空气质量
 "air_quality_hist"  # 空气质量历史数据
 "air_quality_rank"  # 空气质量排行
 "air_quality_watch_point"  # 空气质量观测点历史数据
 "air_city_list"  # 所有城市列表
 # 财富世界五百强公司
 "fortune_rank"  # 获取财富世界500强公司历年排名
 # 中国证券投资基金业协会-信息公示
 "amac_member_info" # 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
 "amac_person_org_list" # 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
 "amac_manager_info" # 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
 "amac_manager_classify_info" # 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
 "amac_member_sub_info" # 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
 "amac_fund_info" # 中国证券投资基金业协会-信息公示-基金产品-私募基金管理人基金产品
 "amac_securities_info" # 中国证券投资基金业协会-信息公示-基金产品-证券公司集合资管产品公示
 "amac_aoin_info" # 中国证券投资基金业协会-信息公示-基金产品-证券公司直投基金
 "amac_fund_sub_info" # 中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
 "amac_fund_account_info" # 中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
 "amac_fund_abs" # 中国证券投资基金业协会-信息公示-基金产品公示-资产支持专项计划
 "amac_futures_info" # 中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
 "amac_manager_cancelled_info" # 中国证券投资基金业协会-信息公示-诚信信息-已注销私募基金管理人名单
 # 全国银行间同业拆借中心-市场数据-市场行情-外汇市场行情
 "fx_spot_quote"  # 市场行情-外汇市场行情-人民币外汇即期报价
 "fx_swap_quote"  # 市场行情-债券市场行情-人民币外汇远掉报价
 "fx_pair_quote"  # 市场行情-债券市场行情-外币对即期报价
 # 能源-碳排放权
 "energy_carbon_bj"  # 碳排放权-北京
 "energy_carbon_sz"  # 碳排放权-深圳
 "energy_carbon_eu"  # 碳排放权-国际
 "energy_carbon_hb"  # 碳排放权-湖北
 "energy_carbon_gz"  # 碳排放权-广州
 # 生活成本
 "cost_living"  # 获取世界各大城市生活成本数据
 # 商品现货价格指数
 "spot_goods"  # 获取商品现货价格指数
 # 中国宏观杠杆率
 "macro_cnbs"  # 获取中国宏观杠杆率数据
 # 金融期权
 "option_finance_board"  # 获取金融期权数据
 # 期货连续合约
 "futures_main_sina"  # 获取新浪期货连续合约的历史数据
 # 倒闭公司数据
 "death_company"  # 获取2014至今倒闭公司名单
 # 独角兽公司数据
 "nicorn_company"  # 获取独角兽公司名单
 # 千里马公司数据
 "maxima_company"  # 获取千里马公司名单
 # 机构调研数据
 "stock_em_jgdy_tj"  # 获取机构调研数据-统计
 "stock_em_jgdy_detail"  # 获取机构调研数据-详细
 # 股权质押数据
 "stock_em_gpzy_profile"  # 获取股权质押市场概况
 "stock_em_gpzy_pledge_ratio"  # 获取上市公司质押比例
 "stock_em_gpzy_pledge_ratio_detail"  # 获取重要股东股权质押明细
 "stock_em_gpzy_distribute_statistics_company"  # 获取质押机构分布统计-证券公司
 "stock_em_gpzy_distribute_statistics_bank"  # 获取质押机构分布统计-银行
 "stock_em_gpzy_industry_data"  # 获取上市公司质押比例-行业数据
 # 商誉专题数据
 "stock_em_sy_profile"  # 获取A股商誉市场概况
 "stock_em_sy_yq_list"  # 获取商誉减值预期明细
 "stock_em_sy_jz_list"  # 获取个股商誉减值明细
 "stock_em_sy_list"  # 获取个股商誉明细
 "stock_em_sy_hy_list"  # 获取行业商誉
 # 股票账户统计数据
 "stock_em_account"  # 获取股票账户统计数据
 # 交易法门-工具接口-套利分析
 "jyfm_tools_futures_spread"  # 交易法门-工具-套利分析-跨期价差(自由价差)
 "jyfm_tools_futures_ratio"  # 交易法门-工具-套利分析-自由价比
 "jyfm_tools_futures_customize"  # 交易法门-工具-套利分析-多腿组合
 "jyfm_exchange_symbol_dict"  # 交易法门-交易所-品种字典
 # 交易法门-工具接口-套利分析
 "jyfm_tools_position_detail"  # 交易法门-工具-持仓分析-期货分析
 "jyfm_tools_position_seat"  # 交易法门-工具-持仓分析-持仓分析
 "jyfm_tools_position_season"  # 交易法门-工具-持仓分析-季节性分析
 # 交易法门-工具接口-交易规则
 "jyfm_tools_receipt_expire_info"  # 交易法门-工具-交易规则-仓单有效期
 "jyfm_tools_position_limit_info"  # 交易法门-工具-交易规则-限仓规定
 "jyfm_tools_symbol_handbook"  # 交易法门-工具-交易规则-品种手册
 # 交易法门-数据接口-农产品
 "jyfm_data_cocking_coal"  # 交易法门-数据-黑色系-焦煤
 "jyfm_data_palm"  # 交易法门-数据-农产品-棕榈
 "jyfm_data_soybean_meal"  # 交易法门-数据-农产品-豆粕
 "jyfm_data_sugar"  # 交易法门-数据-农产品-白糖
 "jyfm_data_usa_bean"  # 交易法门-数据-农产品-美豆
 "jyfm_data_soybean_oil"  # 交易法门-数据-农产品-豆油
 # 股票指数-成份股
 "index_stock_cons"  # 股票指数-成份股-最新成份股获取
 "index_stock_info"  # 股票指数-成份股-所有可以获取的指数表
 "index_stock_info_sina"  # 股票指数-成份股-所有可以获取的指数表-新浪新接口
 "index_stock_hist"  # 股票指数-历史成份股
 # 义乌小商品指数
 "index_yw"  # 获取义乌小商品指数
 # 交易法门-工具-期限分析
 "jyfm_tools_futures_basis_daily"  # 交易法门-工具-期限分析-基差日报
 "jyfm_tools_futures_basis_analysis"  # 交易法门-工具-期限分析-基差分析
 "jyfm_tools_futures_basis_structure"  # 交易法门-工具-期限分析-期限结构
 "jyfm_tools_futures_basis_rule"  # 交易法门-工具-期限分析-价格季节性
 # 交易法门-工具-资讯汇总
 "jyfm_tools_research_query"  # 交易法门-工具-资讯汇总-研报查询
 "jyfm_tools_trade_calendar"  # 交易法门-工具-资讯汇总-交易日历
 # 交易法门-工具-资金分析
 "jyfm_tools_position_fund_direction"  # 交易法门-工具-资金分析-资金流向
 "jyfm_tools_position_fund_down"  # 交易法门-工具-资金分析-沉淀资金
 "jyfm_tools_position_fund_season"  # 交易法门-工具-资金分析-资金季节性
 "jyfm_tools_position_fund_deal"  # 交易法门-工具-资金分析-成交排名
 # 交易法门-工具-席位分析
 "jyfm_tools_position_structure"  # 交易法门-工具-席位分析-持仓结构
 # 交易法门-工具-仓单分析
 "jyfm_tools_warehouse_receipt_daily"  # 交易法门-工具-仓单分析-仓单日报
 "jyfm_tools_warehouse_receipt_query"  # 交易法门-工具-仓单分析-仓单查询
 "jyfm_tools_warehouse_receipt_ratio"  # 交易法门-工具-仓单分析-虚实盘比查询
 # 世界银行间拆借利率
 "rate_interbank"  #  银行间拆借利率
 # 主要央行利率
 "macro_bank_usa_interest_rate"  # 美联储利率决议报告
 "macro_bank_euro_interest_rate"  # 欧洲央行决议报告
 "macro_bank_newzealand_interest_rate"  # 新西兰联储决议报告
 "macro_bank_china_interest_rate"  # 中国央行决议报告
 "macro_bank_switzerland_interest_rate"  # 瑞士央行决议报告
 "macro_bank_english_interest_rate"  # 英国央行决议报告
 "macro_bank_australia_interest_rate"  # 澳洲联储决议报告
 "macro_bank_japan_interest_rate"  # 日本央行决议报告
 "macro_bank_russia_interest_rate"  # 俄罗斯央行决议报告
 "macro_bank_india_interest_rate"  # 印度央行决议报告
 "macro_bank_brazil_interest_rate"  # 巴西央行决议报告
 # 中国
 "macro_china_shrzgm"  # 社会融资规模增量统计
 "macro_china_gdp_yearly"  # 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
 "macro_china_cpi_yearly"  # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
 "macro_china_cpi_monthly"  # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI月率报告
 "macro_china_ppi_yearly"  # 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
 "macro_china_exports_yoy"  # 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
 "macro_china_imports_yoy"  # 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
 "macro_china_trade_balance"  # 金十数据中心-经济指标-中国-贸易状况-以美元计算贸易帐(亿美元)
 "macro_china_industrial_production_yoy"  # 金十数据中心-经济指标-中国-产业指标-规模以上工业增加值年率
 "macro_china_pmi_yearly"  # 金十数据中心-经济指标-中国-产业指标-官方制造业PMI
 "macro_china_cx_pmi_yearly"  # 金十数据中心-经济指标-中国-产业指标-财新制造业PMI终值
 "macro_china_cx_services_pmi_yearly"  # 金十数据中心-经济指标-中国-产业指标-财新服务业PMI
 "macro_china_non_man_pmi"  # 金十数据中心-经济指标-中国-产业指标-中国官方非制造业PMI
 "macro_china_fx_reserves_yearly"  # 金十数据中心-经济指标-中国-金融指标-外汇储备(亿美元)
 "macro_china_m2_yearly"  # 金十数据中心-经济指标-中国-金融指标-M2货币供应年率
 "macro_china_shibor_all"  # 金十数据中心-经济指标-中国-金融指标-上海银行业同业拆借报告
 "macro_china_hk_market_info"  # 金十数据中心-经济指标-中国-金融指标-人民币香港银行同业拆息
 "macro_china_daily_energy"  # 金十数据中心-经济指标-中国-其他-中国日度沿海六大电库存数据
 "macro_china_rmb"  # 金十数据中心-经济指标-中国-其他-中国人民币汇率中间价报告
 "macro_china_market_margin_sz"  # 金十数据中心-经济指标-中国-其他-深圳融资融券报告
 "macro_china_market_margin_sh"  # 金十数据中心-经济指标-中国-其他-上海融资融券报告
 "macro_china_au_report"  # 金十数据中心-经济指标-中国-其他-上海黄金交易所报告
 "macro_china_ctci"  # 发改委-中国电煤价格指数-全国综合电煤价格指数
 "macro_china_ctci_detail"  # 发改委-中国电煤价格指数-各价区电煤价格指数
 "macro_china_ctci_detail_hist"  # 发改委-中国电煤价格指数-历史电煤价格指数
 "macro_china_lpr"  # 中国-利率-贷款报价利率
 "macro_china_new_house_price"  # 中国-新房价指数
 "macro_china_enterprise_boom_index"  # 中国-企业景气及企业家信心指数
 "macro_china_national_tax_receipts"  # 中国-全国税收收入
 "macro_china_new_financial_credit"  # 中国-新增信贷数据
 "macro_china_fx_gold"  # 中国-外汇和黄金储备
 "macro_china_stock_market_cap"  # 中国-全国股票交易统计表
 "macro_china_cpi"  # 中国-居民消费价格指数
 "macro_china_gdp"  # 中国-国内生产总值
 "macro_china_ppi"  # 中国-工业品出厂价格指数
 "macro_china_pmi"  # 中国-采购经理人指数
 "macro_china_gdzctz"  # 中国-城镇固定资产投资
 "macro_china_hgjck"  # 中国-海关进出口增减情况一览表
 "macro_china_czsr"  # 中国-财政收入
 "macro_china_whxd"  # 中国-外汇贷款数据
 "macro_china_wbck"  # 中国-本外币存款
 "macro_china_hb"  # 中国-货币净投放与净回笼
 "macro_china_gksccz"  # 中国-央行公开市场操作
 "macro_china_bond_public"  # 中国-债券发行
 # 美国
 "macro_usa_gdp_monthly"  # 金十数据中心-经济指标-美国-经济状况-美国GDP
 "macro_usa_cpi_monthly"  # 金十数据中心-经济指标-美国-物价水平-美国CPI月率报告
 "macro_usa_core_cpi_monthly"  # 金十数据中心-经济指标-美国-物价水平-美国核心CPI月率报告
 "macro_usa_personal_spending"  # 金十数据中心-经济指标-美国-物价水平-美国个人支出月率报告
 "macro_usa_retail_sales"  # 金十数据中心-经济指标-美国-物价水平-美国零售销售月率报告
 "macro_usa_import_price"  # 金十数据中心-经济指标-美国-物价水平-美国进口物价指数报告
 "macro_usa_export_price"  # 金十数据中心-经济指标-美国-物价水平-美国出口价格指数报告
 "macro_usa_lmci"  # 金十数据中心-经济指标-美国-劳动力市场-LMCI
 "macro_usa_unemployment_rate"  # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国失业率报告
 "macro_usa_job_cuts"  # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国挑战者企业裁员人数报告
 "macro_usa_non_farm"  # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国非农就业人数报告
 "macro_usa_adp_employment"  # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国ADP就业人数报告
 "macro_usa_core_pce_price"  # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国核心PCE物价指数年率报告
 "macro_usa_real_consumer_spending"  # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国实际个人消费支出季率初值报告
 "macro_usa_trade_balance"  # 金十数据中心-经济指标-美国-贸易状况-美国贸易帐报告
 "macro_usa_current_account"  # 金十数据中心-经济指标-美国-贸易状况-美国经常帐报告
 "macro_usa_rig_count"  # 金十数据中心-经济指标-美国-产业指标-制造业-贝克休斯钻井报告
 # 金十数据中心-经济指标-美国-产业指标-制造业-美国个人支出月率报告
 "macro_usa_ppi"  # 金十数据中心-经济指标-美国-产业指标-制造业-美国生产者物价指数(PPI)报告
 "macro_usa_core_ppi"  # 金十数据中心-经济指标-美国-产业指标-制造业-美国核心生产者物价指数(PPI)报告
 "macro_usa_api_crude_stock"  # 金十数据中心-经济指标-美国-产业指标-制造业-美国API原油库存报告
 "macro_usa_pmi"  # 金十数据中心-经济指标-美国-产业指标-制造业-美国Markit制造业PMI初值报告
 "macro_usa_ism_pmi"  # 金十数据中心-经济指标-美国-产业指标-制造业-美国ISM制造业PMI报告
 "macro_usa_nahb_house_market_index"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国NAHB房产市场指数报告
 "macro_usa_house_starts"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋开工总数年化报告
 "macro_usa_new_home_sales"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋销售总数年化报告
 "macro_usa_building_permits"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国营建许可总数报告
 "macro_usa_exist_home_sales"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋销售总数年化报告
 "macro_usa_house_price_index"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国FHFA房价指数月率报告
 "macro_usa_spcs20" # 金十数据中心-经济指标-美国-产业指标-房地产-美国S&P/CS20座大城市房价指数年率报告
 "macro_usa_pending_home_sales"  # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋签约销售指数月率报告
 "macro_usa_cb_consumer_confidence"  # 金十数据中心-经济指标-美国-领先指标-美国谘商会消费者信心指数报告
 "macro_usa_nfib_small_business" # 金十数据中心-经济指标-美国-领先指标-美国NFIB小型企业信心指数报告
 "macro_usa_michigan_consumer_sentiment" # 金十数据中心-经济指标-美国-领先指标-美国密歇根大学消费者信心指数初值报告
 "macro_usa_eia_crude_rate"  # 金十数据中心-经济指标-美国-其他-美国EIA原油库存报告
 "macro_usa_initial_jobless"  # 金十数据中心-经济指标-美国-其他-美国初请失业金人数报告
 "macro_usa_crude_inner"  # 金十数据中心-经济指标-美国-其他-美国原油产量报告
 # 宏观数据
 "macro_cons_gold_volume"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
 "macro_cons_gold_change"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
 "macro_cons_gold_amount"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
 "macro_cons_silver_volume"  # 全球最大白银ETF--iShares Silver Trust持仓报告
 "macro_cons_silver_change"  # 全球最大白银ETF--iShares Silver Trust持仓报告
 "macro_cons_silver_amount"  # 全球最大白银ETF--iShares Silver Trust持仓报告
 "macro_cons_opec_month"  # 欧佩克报告-月度
 # 伦敦金属交易所(LME)
 "macro_euro_lme_holding"  # 伦敦金属交易所(LME)-持仓报告
 "macro_euro_lme_stock"  # 伦敦金属交易所(LME)-库存报告
 # 美国商品期货交易委员会
 "macro_usa_cftc_nc_holding"  # 外汇类非商业持仓报告
 "macro_usa_cftc_c_holding"  # 商品类非商业持仓报告
 "macro_usa_cftc_merchant_currency_holding"  # 外汇类商业持仓报告
 "macro_usa_cftc_merchant_goods_holding"  # 商品类商业持仓报告
 # 货币对-投机情绪报告
 "macro_fx_sentiment"  # 货币对-投机情绪报告
 # COVID-19数据接口
 "covid_19_163"  # COVID-19-网易
 "covid_19_dxy"  # COVID-19-丁香园
 "covid_19_baidu"  # COVID-19-百度
 "covid_19_csse_daily"  # COVID-19-CSSE每日数据
 "covid_19_csse_global_confirmed"  # COVID-19-CSSE-全球确诊
 "covid_19_csse_global_death"  # COVID-19-CSSE-全球死亡
 "covid_19_csse_global_recovered"  # COVID-19-CSSE-全球治愈
 "covid_19_csse_us_death"  # COVID-19-CSSE-美国死亡
 "covid_19_csse_us_confirmed"  # COVID-19-CSSE-美国确诊
 "covid_19_history"  # COVID-19-所有历史数据(中文)
 # 百度迁徙地图接口
 "migration_area_baidu"  # 百度迁徙地图-迁入/出地详情
 "migration_scale_baidu"  # 百度迁徙地图-迁徙规模
 "internal_flow_history"  # 百度迁徙地图-城内出行强度
 # 新型肺炎-小区查询
 "covid_19_area_search"  # 具体小区查询
 "covid_19_area_all"  # 提供可查询的省份-城市-区一览表
 "covid_19_area_detail"  # 全国所有小区详细数据
 # 新型肺炎-相同行程查询
 "covid_19_trip"  # 同程交通
 "covid_19_trace"  # 病患轨迹
 # 债券-沪深债券
 "bond_zh_hs_daily"  # 债券-沪深债券-历史行情数据
 "bond_zh_hs_spot"  # 债券-沪深债券-实时行情数据
 # 债券-沪深可转债
 "bond_zh_hs_cov_daily"  # 债券-沪深可转债-历史行情数据
 "bond_zh_hs_cov_spot"  # 债券-沪深可转债-实时行情数据
 "bond_zh_cov"  # 债券-可转债数据一览表
 "bond_cov_comparison"  # 债券-可转债数据比价
 "bond_cov_jsl"  # 可转债转股价变动
 # 中国-商业特许经营数据
 "franchise_china"  # 中国-商业特许经营数据
 # 慈善中国
 "charity_china_organization"  # 慈善中国-慈善组织查询
 "charity_china_trust"  # 慈善中国-慈善信托查询
 "charity_china_plan"  # 慈善中国-募捐方案备案
 "charity_china_progress"  # 慈善中国-慈善项目进展
 "charity_china_report"  # 慈善中国-慈善组织年报
 "charity_china_platform"  # 慈善中国-募捐信息平台
 # 金融期权-新浪
 "option_sina_cffex_hs300_list"  # 沪深300期权列表
 "option_sina_cffex_hs300_spot"  # 沪深300期权实时行情
 "option_sina_cffex_hs300_daily"  # 沪深300期权历史行情-日频
 "option_sina_sse_list"  # 上交所期权列表
 "option_sina_sse_expire_day"  # 上交所期权剩余到期日
 "option_sina_sse_codes"  # 上交所期权代码
 "option_sina_sse_spot_price"  # 上交所期权实时行情
 "option_sina_sse_underlying_spot_price"  # 上交所期权标的物实时行情
 "option_sina_sse_greeks"  # 上交所期权希腊字母
 "option_sina_sse_minute"  # 上交所期权分钟数据
 "option_sina_sse_daily"  # 上交所期权日频数据
 "option_sina_finance_minute"  # 股票期权分时数据
 # 商品期权-新浪
 "option_sina_option_commodity_dict"  # 商品期权合约字典查询
 "option_sina_option_commodity_contract_list"  # 商品期权合约查询
 "option_sina_option_commodity_hist"  # 商品期权行情历史数据
 # 微博舆情报告
 "stock_js_weibo_report"  # 微博舆情报告
 # 自然语言处理
 "nlp_ownthink"  # 知识图谱
 "nlp_answer"  # 智能问答
 # 货币
 "currency_latest"  # 最新货币报价
 "currency_history"  # 指定历史日期的所有货币报价
 "currency_time_series"  # 指定日期间的时间序列数据-需要权限
 "currency_currencies"  # 查询所支持的货币信息
 "currency_convert"  # 货币换算
 "currency_hist"  # 指定历史日期的货币对的历史报价
 "currency_pair_map"  # 指定货币的所有可获取货币对的数据
 "currency_name_code"  # 当前所有可兑换货币对
 # 工具-GitHub
 "tool_github_star_list"  # GitHub Star 的用户
 "tool_github_email_address"  # GitHub 用户的邮箱
 # 公募基金
 "fund_em_fund_name",  # 基金基本信息
 "fund_em_open_fund_daily",  # 开放式基金-实时数据
 "fund_em_open_fund_info",  # 开放式基金-历史数据
 "fund_em_etf_fund_daily",  # 场内交易基金-实时数据
 "fund_em_etf_fund_info",  # 场内交易基金-历史数据
 "fund_em_financial_fund_daily",  # 理财型基金-实时数据
 "fund_em_financial_fund_info",  # 理财型基金-历史数据
 "fund_em_graded_fund_daily",  # 分级基金-实时数据
 "fund_em_graded_fund_info",  # 分级基金-历史数据
 "fund_em_money_fund_daily",  # 货币型基金-实时数据
 "fund_em_money_fund_info",  # 货币型基金-历史数据
 "fund_em_value_estimation",  # 基金估值
 # 分析师指数
 "stock_em_analyst_rank"  # 分析师排名
 "stock_em_analyst_detail"  # 分析师详情
 # 千股千评
 "stock_em_comment"  # 股市关注度
 # 沪深港通
 "stock_em_hsgt_north_net_flow_in"  # 沪深港通北向-净流入
 "stock_em_hsgt_north_cash"  # 沪深港通北向-资金余额
 "stock_em_hsgt_north_acc_flow_in"  # 沪深港通北向-累计净流入
 "stock_em_hsgt_south_net_flow_in"  # 沪深港通南向-净流入
 "stock_em_hsgt_south_cash"  # 沪深港通南向-资金余额
 "stock_em_hsgt_south_acc_flow_in"  # 沪深港通南向-累计净流入
 "stock_em_hsgt_hold_stock"  # 沪深港通持股-个股排行
 "stock_em_hsgt_stock_statistics"  # 沪深港通持股-每日个股统计
 "stock_em_hsgt_institution_statistics"  # 沪深港通持股-每日机构统计
 "stock_em_hsgt_hist"  # 沪深港通历史数据
 "stock_em_hsgt_board_rank"  # 板块排行
 # 两市停复牌
 "stock_em_tfp"  # 两市停复牌数据
 # 恐慌指数
 "index_vix"  # 恐慌指数
 # 中国油价
 "energy_oil_hist"  # 汽柴油历史调价信息
 "energy_oil_detail"  # 地区油价
 # 现货与股票
 "futures_spot_stock"  # 现货与股票接口
 # 中国期货市场监控中心
 "futures_index_cfmmc"  # 中国期货市场监控中心-指数
 # 阿尔戈斯全网监控
 "watch_argus"  # 阿尔戈斯全网监控
 # 打新收益率
 "stock_em_dxsyl"  # 打新收益率
 "stock_em_xgsglb"  # 新股申购与中签查询
 # 年报季报
 "stock_em_yjyg"  # 上市公司业绩预告
 "stock_em_yysj"  # 上市公司预约披露时间
 # 西本新干线-指数数据
 "futures_xgx_index"  # 西本新干线-指数数据
 # 高频数据-标普500指数
 "hf_sp_500"  # 获取标普500指数的分钟数据
 # 商品期货库存数据
 "futures_inventory_em"  # 库存数据-东方财富
 "futures_inventory_99"  # 库存数据-99期货
 # 个股资金流
 "stock_individual_fund_flow"  # 个股资金流
 "stock_individual_fund_flow_rank"  # 个股资金流排名
 "stock_market_fund_flow"  # 大盘资金流
 "stock_sector_fund_flow_rank"  # 板块资金流排名
 # 股票基本面数据
 "stock_financial_abstract"  # 财务摘要
 "stock_financial_report_sina"  # 三大财务报表
 "stock_financial_analysis_indicator"  # 财务指标
 "stock_add_stock"  # 股票增发
 "stock_ipo_info"  # 股票新股
 "stock_history_dividend_detail"  # 分红配股
 "stock_history_dividend"  # 历史分红
 "stock_restricted_shares"  # 限售解禁
 "stock_circulate_stock_holder"  # 流动股东
 "stock_fund_stock_holder"  # 基金持股
 "stock_main_stock_holder"  # 主要股东
 # 股票板块
 "stock_sector_spot"  # 板块行情
 "stock_sector_detail"  # 板块详情(具体股票)
 # 股票信息
 "stock_info_sz_name_code"  # 深证证券交易所股票代码和简称
 "stock_info_sh_name_code"  # 上海证券交易所股票代码和简称
 "stock_info_sh_delist"  # 上海证券交易所暂停和终止上市
 "stock_info_sz_delist"  # 深证证券交易所暂停和终止上市
 "stock_info_sz_change_name"  # 深证证券交易所股票曾用名详情
 "stock_info_change_name"  # A 股股票曾用名列表
 "stock_info_a_code_name"  # A 股股票代码和简称
 # 机构持股
 "stock_institute_hold"  # 机构持股一览表
 "stock_institute_hold_detail"  # 机构持股详情
 # 机构推荐股票
 "stock_institute_recommend"  # 机构推荐
 "stock_institute_recommend_detail"  # 股票评级记录
 # 股票市场总貌
 "stock_szse_summary"  # 深圳证券交易所-市场总貌
 "stock_sse_summary"  # 上海证券交易所-股票数据总貌
 "stock_sse_deal_daily"  # 上海证券交易所-每日股票情况
 # 美股港股目标价
 "stock_js_price"  # 美股港股目标价
 # 券商业绩月报
 "stock_em_qsjy"  # 券商业绩月报
 # 彭博亿万富豪指数
 "index_bloomberg_billionaires"  # 彭博亿万富豪指数
 # A 股市盈率和市净率
 "stock_a_pb"  # A 股市净率
 "stock_a_pe"  # A 股市盈率
 "stock_a_lg_indicator"  # A 股个股市盈率、市净率和股息率指标
 "stock_hk_eniu_indicator"  # 港股股个股市盈率、市净率和股息率指标
 "stock_a_high_low_statistics"  # 创新高和新低的股票数量
 "stock_a_below_net_asset_statistics"  # 破净股统计
 # 交易日历
 "tool_trade_date_hist"  # 新浪财经-交易日历
 # 基金行情
 "fund_etf_category_sina"  # 基金列表
 "fund_etf_hist_sina"  # 基金行情
 # 股票财务报告-预约披露
 "stock_report_disclosure"  # 股票财务报告-预约披露时间
 # 基金持股
 "stock_report_fund_hold"  # 个股-基金持股
 "stock_report_fund_hold_detail"  # 个股-基金持股-明细
 # 中证指数
 "stock_zh_index_hist_csindex"  # 中证指数
 # A股龙虎榜
 "stock_sina_lhb_detail_daily"  # 龙虎榜-每日详情
 "stock_sina_lhb_ggtj"  # 龙虎榜-个股上榜统计
 "stock_sina_lhb_yytj"  # 龙虎榜-营业上榜统计
 "stock_sina_lhb_jgzz"  # 龙虎榜-机构席位追踪
 "stock_sina_lhb_jgmx"  # 龙虎榜-机构席位成交明细
 # 注册制审核
 "stock_register_kcb"  # 注册制审核-科创板
 "stock_register_cyb"  # 注册制审核-创业板
 # 次新股
 "stock_zh_a_new"  # 股票数据-次新股
 # 国债期货可交割券相关指标
 "bond_futures_deliverable_coupons"  # 国债期货可交割券相关指标
 # COMEX库存数据
 "futures_comex_inventory"  # COMEX库存数据
 # 消费者信心指数
 "macro_china_xfzxx"  # 消费者信心指数
 # 存款准备金率
 "macro_china_reserve_requirement_ratio"  # 存款准备金率
 # 社会消费品零售总额
 "macro_china_consumer_goods_retail"  # 社会消费品零售总额
 # 海关进出口增减情况
 "macro_china_hgjck"  # 海关进出口增减情况
 # 全社会用电分类情况表
 "macro_china_society_electricity"  # 全社会用电分类情况表
 # 全社会客货运输量
 "macro_china_society_traffic_volume"  # 全社会客货运输量
 # 邮电业务基本情况
 "macro_china_postal_telecommunicational"  # 邮电业务基本情况
 # 国际旅游外汇收入构成
 "macro_china_international_tourism_fx"  # 国际旅游外汇收入构成
 # 民航客座率及载运率
 "macro_china_passenger_load_factor"  # 民航客座率及载运率
 # 航贸运价指数
 "macro_china_freight_index"  # 航贸运价指数
 # 央行货币当局资产负债
 "macro_china_central_bank_balance"  # 央行货币当局资产负债
 # FR007利率互换曲线历史数据
 "macro_china_swap_rate"  # FR007利率互换曲线历史数据
 # 收盘收益率曲线历史数据
 "bond_china_close_return"  # 收盘收益率曲线历史数据
 # 保险业经营情况
 "macro_china_insurance"  # 保险业经营情况
 # 货币供应量
 "macro_china_supply_of_money"  # 货币供应量
 # 央行黄金和外汇储备
 "macro_china_foreign_exchange_gold"  # 央行黄金和外汇储备
 # 商品零售价格指数
 "macro_china_retail_price_index"  # 商品零售价格指数
 # 新闻联播文字稿
 "news_cctv"  # 新闻联播文字稿
 # 电影票房
 "movie_boxoffice_realtime"  # 电影实时票房
 "movie_boxoffice_daily"  # 电影单日票房
 "movie_boxoffice_weekly"  # 电影单周票房
 "movie_boxoffice_monthly"  # 电影单月票房
 "movie_boxoffice_yearly"  # 电影年度票房
 "movie_boxoffice_yearly_first_week"  # 电影年度首周票房
 "movie_boxoffice_cinema_daily"  # 电影院单日票房
 "movie_boxoffice_cinema_weekly"  # 电影院单周票房
 # 国房景气指数
 "macro_china_real_estate"  # 国房景气指数
 # 加密货币历史数据
 "crypto_hist"  # 加密货币历史数据
 "crypto_name_map"  # 加密货币货币名称
 # 基金排行
 "fund_em_open_fund_rank"  # 开放式基金排行
 "fund_em_exchange_rank"  # 场内交易基金排行
 "fund_em_money_rank"  # 货币型基金排行
 "fund_em_lcx_rank"  # 理财基金排行
 "fund_em_hk_rank"  # 香港基金排行
 # 回购定盘利率
 "repo_rate_hist"  # 回购定盘利率
 # 福布斯中国榜单
 "forbes_rank"  # 福布斯中国榜单
 # 新财富500富豪榜
 "xincaifu_rank"  # 新财富500富豪榜
 # 胡润排行榜
 "hurun_rank"  # 胡润排行榜
 # 期货合约详情
 "futures_contract_detail"  # 期货合约详情
 # 科创板报告
 "zh_stock_kcb_report"  # 科创板报告
 # 东方财富-期权
 "option_current_em"  # 东方财富-期权
 # 金十数据-新闻资讯
 "js_news"  # 金十数据-新闻资讯
 # 国证指数
 "index_cni_all"  # 国证指数-所有指数
 "index_cni_hist"  # 国证指数-指数行情
 "index_cni_detail"  # 国证指数-样本详情
 "index_cni_detail_hist"  # 国证指数-历史样本
 "index_cni_detail_hist_adjust"  # 国证指数-历史调样
 # 大宗交易
 "stock_dzjy_sctj"  # 大宗交易-市场统计
 "stock_dzjy_mrmx"  # 大宗交易-每日明细
 "stock_dzjy_mrtj"  # 大宗交易-每日统计
 "stock_dzjy_hygtj"  # 大宗交易-活跃 A 股统计
 "stock_dzjy_yybph"  # 大宗交易-营业部排行
 "stock_dzjy_hyyybtj"  # 大宗交易-活跃营业部统计
 "stock_dzjy_yybph"  # 大宗交易-营业部排行
 # 一致行动人
 "stock_em_yzxdr"  # 股票数据-一致行动人
 # 新闻-个股新闻
 "stock_news_em"  # 新闻-个股新闻
 # 债券概览
 "bond_cash_summary_sse"  # 上登债券信息网-债券现券市场概览
 "bond_deal_summary_sse"  # 上登债券信息网-债券成交概览
 # 中国货币供应量
 "macro_china_money_supply"  # 中国货币供应量
 # 银行排名
 "bank_rank_banker"  # 全球银行排名数据及各项指标
 # 期货交割和期转现
 "futures_to_spot_czce"  # 郑商所期转现
 "futures_to_spot_shfe"  # 上期所期转现
 "futures_to_spot_dce"  # 大商所期转现
 "futures_delivery_dce"  # 大商所交割统计
 "futures_delivery_czce"  # 郑商所交割统计
 "futures_delivery_shfe"  # 上期所交割统计
 "futures_delivery_match_dce"  # 大商所交割配对
 "futures_delivery_match_czce"  # 郑商所交割配对
 # 融资融券
 "stock_margin_sse"  # 上海证券交易所-融资融券汇总
 "stock_margin_detail_sse"  # 上海证券交易所-融资融券详情
 # 基金评级
 "fund_rating_all"  # 基金评级-基金评级总汇
 "fund_rating_sh"  # 基金评级-上海证券评级
 "fund_rating_zs"  # 基金评级-招商证券评级
 "fund_rating_ja"  # 基金评级-济安金信评级
 # 基金经理
 "fund_manager"  # 基金经理-基金经理大全
 # 盈利预测
 "stock_profit_forecast"  # 盈利预测
 # 中美国债收益率
 "bond_zh_us_rate"  # 中美国债收益率
 # 分红配送
 "stock_em_fhps"  # 分红配送
 # 业绩快报
 "stock_em_yjkb"  # 业绩快报
 # 概念板块
 "stock_board_concept_cons_ths"  # 同花顺
```

## 案例演示

### 获取展期收益率

示例代码

```python
import akshare as ak
get_roll_yield_bar_df = ak.get_roll_yield_bar(type_method="date", var="RB", start_day="20180618", end_day="20180718", plot=True)
print(get_roll_yield_bar_df)
```

结果显示: 日期, 展期收益率, 最近合约, 下一期合约

```
            roll_yield near_by deferred
2018-06-19    0.191289  RB1810   RB1901
2018-06-20    0.192123  RB1810   RB1901
2018-06-21    0.183304  RB1810   RB1901
2018-06-22    0.190642  RB1810   RB1901
2018-06-25    0.194838  RB1810   RB1901
2018-06-26    0.204314  RB1810   RB1901
2018-06-27    0.213667  RB1810   RB1901
2018-06-28    0.211701  RB1810   RB1901
2018-06-29    0.205892  RB1810   RB1901
2018-07-02    0.224809  RB1810   RB1901
2018-07-03    0.229198  RB1810   RB1901
2018-07-04    0.222853  RB1810   RB1901
2018-07-05    0.247187  RB1810   RB1901
2018-07-06    0.261259  RB1810   RB1901
2018-07-09    0.253283  RB1810   RB1901
2018-07-10    0.225832  RB1810   RB1901
2018-07-11    0.210659  RB1810   RB1901
2018-07-12    0.212805  RB1810   RB1901
2018-07-13    0.170282  RB1810   RB1901
2018-07-16    0.218066  RB1810   RB1901
2018-07-17    0.229768  RB1810   RB1901
2018-07-18    0.225529  RB1810   RB1901
```
