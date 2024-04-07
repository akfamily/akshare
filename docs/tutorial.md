# [AKShare](https://github.com/akfamily/akshare/) 快速入门

## 查看数据

具体函数使用详情, 请查看 [AKShare 文档](https://akshare.akfamily.xyz/) 每个接口的示例代码

[AKShare](https://github.com/akfamily/akshare/) 数据接口一览

```
 # 交易所期货数据
 "get_cffex_daily",  # 中国金融期货交易所每日交易数据
 "get_cffex_rank_table",  # 中国金融期货交易所前20会员持仓数据明细
 "get_czce_daily",  # 郑州商品交易所每日交易数据
 "get_czce_rank_table",  # 获取郑州商品交易所前20会员持仓数据明细
 "get_dce_daily",  # 获取大连商品交易所每日交易数据
 "get_gfex_daily",  # 获取广州期货交易所每日交易数据
 "get_ine_daily",  # 获取上海国际能源交易中心每日交易数据
 "futures_settlement_price_sgx",  # 新加坡交易所期货品种每日交易数据
 "get_dce_rank_table",  # 获取大连商品交易所前20会员持仓数据明细
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
 "futures_gfex_warehouse_receipt"  # 广州期货交易所-行情数据-仓单日报
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
 # 中国银行间市场交易商协会-非金融企业债务融资工具注册信息系统
 "bond_debt_nafmii"  # 中国银行间市场交易商协会-非金融企业债务融资工具注册信息系统
 # 提供英为财情数据接口
 "index_investing_global"  # 提供英为财情-股票指数-全球股指与期货指数数据
 "bond_investing_global"  # 提供英为财情-债券数据-全球政府债券行情与收益率数据
 # 交易所商品期权数据
 "option_dce_daily"  # 提供大连商品交易所商品期权数据
 "option_czce_daily"  # 提供郑州商品交易所商品期权数据
 "option_shfe_daily"  # 提供上海期货交易所商品期权数据
 "option_gfex_daily"  # 提供广州期货交易所商品期权数据
 "option_gfex_vol_daily"  # 提供广州期货交易所-合约隐含波动率数据
 # 中国银行间市场债券行情数据
 "get_bond_market_quote"  # 债券市场行情-现券市场成交行情数据
 "get_bond_market_trade"  # 债券市场行情-现券市场做市报价数据
 # 外汇
 "get_fx_spot_quote"  # 人民币外汇即期报价数据
 "get_fx_swap_quote"  # 人民币外汇远掉报价数据
 "get_fx_pair_quote"  # 外币对即期报价数据
 # 全球大宗商品
 "futures_global_commodity_hist"  # 全球大宗商品数据
 # 宏观-欧洲
 "macro_euro_interest_rate"  # 欧洲央行决议报告
 # 宏观-主要机构
 "macro_cons_gold"  # 全球最大黄金ETF—SPDR Gold Trust持仓报告
 "macro_cons_silver"  # 全球最大白银ETF--iShares Silver Trust持仓报告
 "macro_cons_opec_month"  # 欧佩克报告
 # 期货-仓单有效期
 "get_receipt_date"  # 期货仓单有效期数据
 # 新浪财经-期货
 "futures_zh_spot"  # 获取新浪-国内期货实时行情数据
 "futures_zh_realtime"  # 获取新浪-国内期货实时行情数据(品种)
 "futures_foreign_commodity_realtime"  # 获取新浪-外盘期货实时行情数据
 "futures_foreign_hist"  # 获取新浪-外盘期货历史行情数据
 "futures_foreign_detail"  # 获取新浪-外盘期货合约详情
 "futures_zh_minute_sina"  # 获取新浪-内盘分时数据
 # 交易所金融期权数据
 "get_finance_option"  # 提供上海证券交易所期权数据
 # 加密货币行情
 "crypto_js_spot"  # 提供主流加密货币行情数据接口
 # 新浪财经-港股
 "stock_hk_spot"  # 获取港股的历史行情数据(包括前后复权因子)
 "stock_hk_daily"  # 获取港股的实时行情数据(也可以用于获得所有港股代码)
 # 东方财富
 "stock_hk_spot_em"  # 港股实时行情
 "stock_hk_main_board_spot_em"  # 港股主板实时行情
 # 新浪财经-美股
 "get_us_stock_name"  # 获得美股的所有股票代码
 "stock_us_spot"  # 获取美股行情报价
 "stock_us_daily"  # 获取美股的历史数据(包括前复权因子)
 # A+H股实时行情数据和历史行情数据
 "stock_zh_ah_spot"  # 获取 A+H 股实时行情数据(延迟15分钟)
 "stock_zh_ah_daily"  # 获取 A+H 股历史行情数据(日频)
 "stock_zh_ah_name"  # 获取 A+H 股所有股票代码
 # A股实时行情数据和历史行情数据
 "stock_zh_a_spot"  # 新浪 A 股实时行情数据
 "stock_zh_a_spot_em"  # 东财 A 股实时行情数据
 "stock_sh_a_spot_em"  # 东财沪 A 股实时行情数据
 "stock_sz_a_spot_em"  # 东财深 A 股实时行情数据
 "stock_bj_a_spot_em"  # 东财京 A 股实时行情数据
 "stock_new_a_spot_em"  # 东财新股实时行情数据
 "stock_kc_a_spot_em"  # 东财科创板实时行情数据
 "stock_zh_b_spot_em"  # 东财 B 股实时行情数据
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
 "stock_zh_index_spot_sina"  # 股票指数实时行情数据-新浪
 "stock_zh_index_spot_em"  # 股票指数实时行情数据-东财
 # 股票分笔数据
 "stock_zh_a_tick_tx_js"  # A 股票分笔行情数据-腾讯-当日数据
 # 世界各地区日出和日落数据-日
 "weather_daily"  # 每日日出和日落数据
 # 世界各地区日出和日落数据-月
 "weather_monthly"  # 每月日出和日落数据
 # 河北空气质量数据(期货-钢铁)
 "air_quality_hebei"  # 河北空气质量数据
 # 南华期货-南华指数-波动率指数
 "futures_volatility_index_nh"  # 波动率指数
 # 南华期货-南华指数-价格指数
 "futures_price_index_nh"  # 价格指数
 # 南华期货-南华指数-收益率指数
 "futures_return_index_nh"  # 收益率指数
 # 经济政策不确定性(EPU)指数
 "article_epu_index"  # 主要国家和地区的经济政策不确定性(EPU)指数
 # 申万行业指数
 "sw_index_third_info"  # 申万三级信息
 "sw_index_third_cons"  # 申万三级信息成份
 # 空气质量
 "air_quality_hist"  # 空气质量历史数据
 "air_quality_rank"  # 空气质量排行
 "air_quality_watch_point"  # 空气质量观测点历史数据
 "air_city_table"  # 所有城市列表
 # 财富世界五百强公司
 "fortune_rank"  # 获取财富世界500强公司历年排名
 # 中国证券投资基金业协会-信息公示
 "amac_member_info" # 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
 "amac_person_fund_org_list" # 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
 "amac_person_bond_org_list" # 中国证券投资基金业协会-信息公示-从业人员信息-债券投资交易相关人员公示
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
 "energy_carbon_domestic"  # 碳排放权-国内
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
 "stock_jgdy_tj_em"  # 获取机构调研数据-统计
 "stock_jgdy_detail_em"  # 获取机构调研数据-详细
 # 股权质押数据
 "stock_gpzy_profile_em"  # 获取股权质押市场概况
 "stock_gpzy_pledge_ratio_em"  # 获取上市公司质押比例
 "stock_gpzy_pledge_ratio_detail_em"  # 获取重要股东股权质押明细
 "stock_gpzy_distribute_statistics_company_em"  # 获取质押机构分布统计-证券公司
 "stock_gpzy_distribute_statistics_bank_em"  # 获取质押机构分布统计-银行
 "stock_gpzy_industry_data_em"  # 获取上市公司质押比例-行业数据
 # 商誉专题数据
 "stock_sy_profile_em"  # A股商誉市场概况
 "stock_sy_yq_em"  # 商誉减值预期明细
 "stock_sy_jz_em"  # 个股商誉减值明细
 "stock_sy_em"  # 个股商誉明细
 "stock_sy_hy_em"  # 行业商誉
 # 股票账户统计数据
 "stock_account_statistics_em"  # 获取股票账户统计数据
 # 股票指数-成份股
 "index_stock_cons"  # 股票指数-成份股-最新成份股获取
 "index_stock_cons_csindex"  # 中证指数-成份股
 "index_stock_cons_weight_csindex"  # 中证指数成份股的权重
 "index_stock_info"  # 股票指数-成份股-所有可以获取的指数表
 "index_stock_info_sina"  # 股票指数-成份股-所有可以获取的指数表-新浪新接口
 # 义乌小商品指数
 "index_yw"  # 获取义乌小商品指数
 # 世界银行间拆借利率
 "rate_interbank"  #  银行间拆借利率
 # 主要央行利率
 "macro_bank_usa_interest_rate"  # 美联储利率决议报告
 "macro_bank_euro_interest_rate"  # 欧洲央行决议报告
 "macro_bank_newzealand_interest_rate"  # 新西兰联储决议报告
 "macro_bank_switzerland_interest_rate"  # 瑞士央行决议报告
 "macro_bank_english_interest_rate"  # 英国央行决议报告
 "macro_bank_australia_interest_rate"  # 澳洲联储决议报告
 "macro_bank_japan_interest_rate"  # 日本央行决议报告
 "macro_bank_russia_interest_rate"  # 俄罗斯央行决议报告
 "macro_bank_india_interest_rate"  # 印度央行决议报告
 "macro_bank_brazil_interest_rate"  # 巴西央行决议报告
 # 中国
 "macro_china_urban_unemployment"  # 城镇调查失业率
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
 "macro_china_lpr"  # 中国-利率-贷款报价利率
 "macro_china_new_house_price"  # 中国-新房价指数
 "macro_china_enterprise_boom_index"  # 中国-企业景气及企业家信心指数
 "macro_china_national_tax_receipts"  # 中国-全国税收收入
 "macro_china_bank_financing"  # 中国-银行理财产品发行数量
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
 "macro_china_bond_public"  # 中国-债券发行
 # 美国
 "macro_usa_gdp_monthly"  # 金十数据中心-经济指标-美国-经济状况-美国GDP
 "macro_usa_cpi_monthly"  # 金十数据中心-经济指标-美国-物价水平-美国CPI月率报告
 "macro_usa_cpi_yoy"  # 东方财富-经济数据一览-美国-CPI年率
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
 # 百度迁徙地图接口
 "migration_area_baidu"  # 百度迁徙地图-迁入/出地详情
 "migration_scale_baidu"  # 百度迁徙地图-迁徙规模
 # 债券-沪深债券
 "bond_zh_hs_daily"  # 债券-沪深债券-历史行情数据
 "bond_zh_hs_spot"  # 债券-沪深债券-实时行情数据
 # 债券-沪深可转债
 "bond_zh_hs_cov_daily"  # 债券-沪深可转债-历史行情数据
 "bond_zh_hs_cov_spot"  # 债券-沪深可转债-实时行情数据
 "bond_zh_cov"  # 债券-可转债数据一览表
 "bond_cov_comparison"  # 债券-可转债数据比价
 "bond_cb_jsl"  # 可转债实时数据-集思录
 "bond_cb_adj_logs_jsl"  # 可转债转股价变动-集思录
 "bond_cb_index_jsl"  # 可转债-集思录可转债等权指数
 "bond_cb_redeem_jsl"  # 可转债-集思录可转债-强赎
 # 金融期权-新浪
 "option_cffex_sz50_list_sina"  # 上证50期权列表
  "option_cffex_sz50_spot_sina"  # 沪深300期权实时行情
 "option_cffex_sz50_daily_sina"  # 沪深300期权历史行情-日频
 "option_cffex_hs300_list_sina"  # 沪深300期权列表
 "option_cffex_hs300_spot_sina"  # 沪深300期权实时行情
 "option_cffex_hs300_daily_sina"  # 沪深300期权历史行情-日频
 "option_cffex_zz1000_list_sina"  # 中证1000期权列表
 "option_cffex_zz1000_spot_sina"  # 中证1000期权实时行情
 "option_cffex_zz1000_daily_sina"  # 中证1000期权历史行情-日频
 "option_sse_list_sina"  # 上交所期权列表
 "option_sse_expire_day_sina"  # 上交所期权剩余到期日
 "option_sse_codes_sina"  # 上交所期权代码
 "option_sse_spot_price_sina"  # 上交所期权实时行情
 "option_sse_underlying_spot_price_sina"  # 上交所期权标的物实时行情
 "option_sse_greeks_sina"  # 上交所期权希腊字母
 "option_sse_minute_sina"  # 上交所期权分钟数据
 "option_sse_daily_sina"  # 上交所期权日频数据
 "option_finance_minute_sina"  # 金融股票期权分时数据
 "option_minute_em"  # 股票期权分时数据
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
 # 公募基金
 "fund_name_em",  # 基金基本信息
 "fund_info_index_em",  # 指数型基金-基本信息
 "fund_purchase_em",  # 基金申购状态
 "fund_open_fund_daily_em",  # 开放式基金-实时数据
 "fund_open_fund_info_em",  # 开放式基金-历史数据
 "fund_etf_fund_daily_em",  # 场内交易基金-实时数据
 "fund_etf_fund_info_em",  # 场内交易基金-历史数据
 "fund_financial_fund_daily_em",  # 理财型基金-实时数据
 "fund_financial_fund_info_em",  # 理财型基金-历史数据
 "fund_graded_fund_daily_em",  # 分级基金-实时数据
 "fund_graded_fund_info_em",  # 分级基金-历史数据
 "fund_money_fund_daily_em",  # 货币型基金-实时数据
 "fund_money_fund_info_em",  # 货币型基金-历史数据
 "fund_value_estimation_em",  # 基金估值
 # 分析师指数
 "stock_analyst_rank_em"  # 分析师排名
 "stock_analyst_detail_em"  # 分析师详情
 # 千股千评
 "stock_comment_em"  # 股市关注度
 "stock_comment_detail_zlkp_jgcyd_em"  # 机构参与度
 "stock_comment_detail_zhpj_lspf_em"  # 综合评价-历史评分
 "stock_comment_detail_scrd_focus_em"  # 市场热度-用户关注指数
 "stock_comment_detail_scrd_desire_em"  # 市场热度-市场参与意愿
 "stock_comment_detail_scrd_desire_daily_em"  # 市场热度-日度市场参与意愿
 "stock_comment_detail_scrd_cost_em"  # 市场热度-市场成本
 # 沪深港通
 "stock_hk_ggt_components_em"  # 港股通成份股
 "stock_hsgt_north_net_flow_in_em"  # 沪深港通北向-净流入
 "stock_hsgt_north_cash_em"  # 沪深港通北向-资金余额
 "stock_hsgt_north_acc_flow_in_em"  # 沪深港通北向-累计净流入
 "stock_hsgt_south_net_flow_in_em"  # 沪深港通南向-净流入
 "stock_hsgt_south_cash_em"  # 沪深港通南向-资金余额
 "stock_hsgt_south_acc_flow_in_em"  # 沪深港通南向-累计净流入
 "stock_hsgt_hold_stock_em"  # 沪深港通持股-个股排行
 "stock_hsgt_stock_statistics_em"  # 沪深港通持股-每日个股统计
 "stock_hsgt_institution_statistics_em"  # 沪深港通持股-每日机构统计
 "stock_hsgt_hist_em"  # 沪深港通历史数据
 "stock_hsgt_board_rank_em"  # 板块排行
 "stock_hsgt_fund_flow_summary_em"  # 沪深港通资金流向
 # 两市停复牌
 "stock_tfp_em"  # 两市停复牌数据
 # 中国油价
 "energy_oil_hist"  # 汽柴油历史调价信息
 "energy_oil_detail"  # 地区油价
 # 现货与股票
 "futures_spot_stock"  # 现货与股票接口
 # 中证商品指数
 "futures_index_ccidx"  # 中证商品指数
 "futures_index_min_ccidx"  # 中证商品指数-分时
 # 打新收益率
 "stock_dxsyl_em"  # 打新收益率
 "stock_xgsglb_em"  # 新股申购与中签查询
 # 年报季报
 "stock_yjyg_em"  # 上市公司业绩预告
 "stock_yysj_em"  # 上市公司预约披露时间
 # 高频数据-标普500指数
 "hf_sp_500"  # 获取标普500指数的分钟数据
 # 商品期货库存数据
 "futures_inventory_em"  # 库存数据-东方财富
 # 个股资金流
 "stock_individual_fund_flow"  # 个股资金流
 "stock_individual_fund_flow_rank"  # 个股资金流排名
 "stock_market_fund_flow"  # 大盘资金流
 "stock_sector_fund_flow_rank"  # 板块资金流排名
 "stock_sector_fund_flow_summary"  # xx行业个股资金流
 "stock_sector_fund_flow_hist"  # 行业历史资金流
 "stock_concept_fund_flow_hist"  # 概念历史资金流
 "stock_main_fund_flow"  # 主力净流入排名
 # 股票基本面数据
 "stock_financial_abstract"  # 财务摘要
 "stock_financial_report_sina"  # 三大财务报表
 "stock_financial_analysis_indicator"  # 财务指标
 "stock_add_stock"  # 股票增发
 "stock_ipo_info"  # 股票新股
 "stock_history_dividend_detail"  # 分红配股
 "stock_history_dividend"  # 历史分红
 "stock_dividend_cninfo"  # 个股历史分红
 "stock_restricted_release_queue_sina"  # 限售解禁-新浪
 "stock_restricted_release_summary_em"  # 东方财富网-数据中心-特色数据-限售股解禁
 "stock_restricted_release_detail_em"  # 东方财富网-数据中心-限售股解禁-解禁详情一览
 "stock_restricted_release_queue_em"  # 东方财富网-数据中心-个股限售解禁-解禁批次
 "stock_restricted_release_stockholder_em"  # 东方财富网-数据中心-个股限售解禁-解禁股东
 "stock_circulate_stock_holder"  # 流动股东
 "stock_fund_stock_holder"  # 基金持股
 "stock_main_stock_holder"  # 主要股东
 # 股票板块
 "stock_sector_spot"  # 板块行情
 "stock_sector_detail"  # 板块详情(具体股票)
 # 股票信息
 "stock_info_sz_name_code"  # 深证证券交易所股票代码和简称
 "stock_info_sh_name_code"  # 上海证券交易所股票代码和简称
 "stock_info_bj_name_code"  # 北京证券交易所股票代码和简称
 "stock_info_sh_delist"  # 上海证券交易所暂停和终止上市
 "stock_info_sz_delist"  # 深证证券交易所暂停和终止上市
 "stock_info_sz_change_name"  # 深证证券交易所名称变更
 "stock_info_change_name"  # A 股股票曾用名列表
 "stock_info_a_code_name"  # A 股股票代码和简称
 # 机构持股
 "stock_institute_hold"  # 机构持股一览表
 "stock_institute_hold_detail"  # 机构持股详情
 # 机构推荐股票
 "stock_institute_recommend"  # 机构推荐
 "stock_institute_recommend_detail"  # 股票评级记录
 # 股票市场总貌
 "stock_szse_summary"  # 深圳证券交易所-市场总貌-证券类别统计
 "stock_szse_area_summary"  # 深圳证券交易所-市场总貌-地区交易排序
  "stock_szse_sector_summary"  # 深圳证券交易所-统计资料-股票行业成交
 "stock_sse_summary"  # 上海证券交易所-股票数据总貌
 "stock_sse_deal_daily"  # 上海证券交易所-每日股票情况
 # 美股港股目标价
 "stock_price_js"  # 美股港股目标价
 # 券商业绩月报
 "stock_qsjy_em"  # 券商业绩月报
 # 彭博亿万富豪指数
 "index_bloomberg_billionaires"  # 彭博亿万富豪指数
 "index_bloomberg_billionaires_hist"  # 彭博亿万富豪历史指数
 # A 股市盈率和市净率
 "stock_market_pe_lg"  # 乐咕乐股-主板市盈率
 "stock_index_pe_lg"  # 乐咕乐股-指数市盈率
 "stock_market_pb_lg"  # 乐咕乐股-主板市净率
 "stock_index_pb_lg"  # 乐咕乐股-指数市净率
 "stock_a_indicator_lg"  # A 股个股市盈率、市净率和股息率指标
 "stock_hk_indicator_eniu"  # 港股股个股市盈率、市净率和股息率指标
 "stock_a_high_low_statistics"  # 创新高和新低的股票数量
 "stock_a_below_net_asset_statistics"  # 破净股统计
 # 交易日历
 "tool_trade_date_hist"  # 新浪财经-交易日历
 # 基金行情
 "fund_etf_category_sina"  # 基金实时行情-新浪
 "fund_etf_hist_sina"  # 基金行情-新浪
 "fund_etf_hist_em"  # 基金历史行情-东财
 "fund_etf_hist_min_em"  # 基金分时行情-东财
 "fund_etf_spot_em"  # 基金实时行情-东财
 # 股票财务报告-预约披露
 "stock_report_disclosure"  # 股票财务报告-预约披露时间
 # 基金持股
 "stock_report_fund_hold"  # 个股-基金持股
 "stock_report_fund_hold_detail"  # 个股-基金持股-明细
 # 中证指数
 "stock_zh_index_hist_csindex"  # 中证指数
 "stock_zh_index_value_csindex"  # 中证指数-指数估值
 # A股龙虎榜
 "stock_lhb_detail_daily_sina"  # 龙虎榜-每日详情
 "stock_lhb_ggtj_sina"  # 龙虎榜-个股上榜统计
 "stock_lhb_yytj_sina"  # 龙虎榜-营业上榜统计
 "stock_lhb_jgzz_sina"  # 龙虎榜-机构席位追踪
 "stock_lhb_jgmx_sina"  # 龙虎榜-机构席位成交明细
 # 注册制审核
 "stock_register_kcb"  # 注册制审核-科创板
 "stock_register_cyb"  # 注册制审核-创业板
 "stock_register_db"  # 注册制审核-达标企业
 # 次新股
 "stock_zh_a_new"  # 股票数据-次新股
 # 国债期货可交割券相关指标
 "bond_futures_deliverable_coupons"  # 国债期货可交割券相关指标
 # COMEX库存数据
 "futures_comex_inventory"  # COMEX库存数据
 # 消费者信心指数
 "macro_china_xfzxx"  # 消费者信心指数
 # 工业增加值增长
 "macro_china_gyzjz"  # 工业增加值增长
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
 "crypto_name_url_table"  # 加密货币货币名称
 # 基金排行
 "fund_open_fund_rank_em"  # 开放式基金排行
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
 "stock_zh_kcb_report_em"  # 科创板报告
 # 东方财富-期权
 "option_current_em"  # 东方财富-期权
 # 国证指数
 "index_all_cni"  # 国证指数-所有指数
 "index_hist_cni"  # 国证指数-指数行情
 "index_detail_cni"  # 国证指数-样本详情
 "index_detail_hist_cni"  # 国证指数-历史样本
 "index_detail_hist_adjust_cni"  # 国证指数-历史调样
 # 大宗交易
 "stock_dzjy_sctj"  # 大宗交易-市场统计
 "stock_dzjy_mrmx"  # 大宗交易-每日明细
 "stock_dzjy_mrtj"  # 大宗交易-每日统计
 "stock_dzjy_hygtj"  # 大宗交易-活跃 A 股统计
 "stock_dzjy_yybph"  # 大宗交易-营业部排行
 "stock_dzjy_hyyybtj"  # 大宗交易-活跃营业部统计
 "stock_dzjy_yybph"  # 大宗交易-营业部排行
 # 一致行动人
 "stock_yzxdr_em"  # 股票数据-一致行动人
 # 新闻-个股新闻
 "stock_news_em"  # 新闻-个股新闻
 # 债券概览
 "bond_cash_summary_sse"  # 上登债券信息网-债券现券市场概览
 "bond_deal_summary_sse"  # 上登债券信息网-债券成交概览
 # 中国货币供应量
 "macro_china_money_supply"  # 中国货币供应量
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
 "fund_manager_em"  # 基金经理-基金经理大全
 # 盈利预测
 "stock_profit_forecast_em"  # 盈利预测-东财
 "stock_profit_forecast_ths"  # 盈利预测-同花顺
 # 中美国债收益率
 "bond_zh_us_rate"  # 中美国债收益率
 # 分红配送
 "stock_fhps_em"  # 分红配送
 # 业绩快报
 "stock_yjkb_em"  # 业绩快报
 # 概念板块
 "stock_board_concept_cons_ths"  # 同花顺-概念板块-成份股
 "stock_board_concept_hist_ths"  # 同花顺-概念板块-指数日频数据
 "stock_board_cons_ths"  # 同花顺-成份股
 # 业绩报告
 "stock_yjbb_em"  # 业绩报告
 # 三大表报
 "stock_zcfz_em"  # 三大表报-资产负债表
 "stock_lrb_em"  # 三大表报-利润表
 "stock_xjll_em"  # 三大表报-现金流量表
 # 首发企业申报
 "stock_ipo_declare"  # 首发企业申报
 # 行业板块
 "stock_board_industry_cons_ths"  # 同花顺-行业板块-成份股
 "stock_board_industry_index_ths"  # 同花顺-行业板块-指数日频数据
 # 营业部
 "stock_lh_yyb_most"  # 营业部排名-上榜次数最多
 "stock_lh_yyb_capital"  # 营业部排名-资金实力最强
 "stock_lh_yyb_control"  # 营业部排名-抱团操作实力
 # 比特比持仓
 "crypto_bitcoin_hold_report"  # 比特比持仓
 # 同花顺-数据中心-资金流向
 "stock_fund_flow_individual"  # 同花顺-数据中心-资金流向-个股资金流
 "stock_fund_flow_industry"  # 同花顺-数据中心-资金流向-行业资金流
 "stock_fund_flow_concept"  # 同花顺-数据中心-资金流向-概念资金流
 "stock_fund_flow_big_deal"  # 同花顺-数据中心-资金流向-大单追踪
 # 高管持股
 "stock_ggcg_em"  # 高管持股
 # 新发基金
 "fund_new_found_em"  # 新发基金
 # 柯桥指数
 "index_kq_fz"  # 柯桥纺织指数
 "index_kq_fashion"  # 柯桥时尚指数
 # 问财-热门股票
 "stock_hot_rank_wc"  # 问财-热门股票
 # Drewry 集装箱指数
 "drewry_wci_index"  # Drewry 集装箱指数
 # 浙江省排污权交易指数
 "index_eri"  # 浙江省排污权交易指数
 # 赚钱效应分析
 "stock_market_activity_legu"  # 赚钱效应分析
 # 中国公路物流运价指数
 "index_cflp_price"  # 中国公路物流运价指数
 # 中国公路物流运量指数
 "index_cflp_volume"  # 中国公路物流运量指数
 # 汽车销量
 "car_sale_rank_gasgoo"  # 盖世汽车-汽车行业制造企业数据库-销量数据
 "car_market_total_cpca"  # 乘联会-统计数据-总体市场
 "car_market_man_rank_cpca"  # 乘联会-统计数据-厂商排名
 "car_market_cate_cpca"  # 乘联会-统计数据-车型大类
 "car_market_country_cpca"  # 乘联会-统计数据-国别细分市场
 "car_market_segment_cpca"  # 乘联会-统计数据-级别细分市场
 "car_market_fuel_cpca"  # 乘联会-统计数据-新能源细分市场
 # 增发
 "stock_qbzf_em"  # 增发
 # 配股
 "stock_pg_em"  # 配股
 # 中国-香港-宏观经济指标
 "macro_china_hk_cpi"  # 中国-香港-消费者物价指数
 "macro_china_hk_cpi_ratio"  # 中国-香港-消费者物价指数年率
 "macro_china_hk_rate_of_unemployment"  # 中国-香港-失业率
 "macro_china_hk_gbp"  # 中国-香港-香港 GDP
 "macro_china_hk_gbp_ratio"  # 中国-香港-香港 GDP 同比
 "macro_china_hk_building_volume"  # 中国-香港-香港楼宇买卖合约数量
 "macro_china_hk_building_amount"  # 中国-香港-香港楼宇买卖合约成交金额
 "macro_china_hk_trade_diff_ratio"  # 中国-香港-香港商品贸易差额年率
 "macro_china_hk_ppi"  # 中国-香港-香港制造业 PPI 年率
 # 涨停板行情
 "stock_zt_pool_em"  # 涨停板行情-涨停股池
 "stock_zt_pool_previous_em"  # 涨停板行情-昨日涨停股池
 "stock_zt_pool_strong_em"  # 涨停板行情-强势股池
 "stock_zt_pool_sub_new_em"  # 涨停板行情-次新股池
 "stock_zt_pool_zbgc_em"  # 涨停板行情-炸板股池
 "stock_zt_pool_dtgc_em"  # 涨停板行情-跌停股池
 # 两网及退市
 "stock_staq_net_stop"  # 两网及退市
 # 股东户数
 "stock_zh_a_gdhs"  # 股东户数
 "stock_zh_a_gdhs_detail_em"  # 股东户数详情
 # 中行人民币牌价历史数据查询
 "currency_boc_sina"  # 中行人民币牌价历史数据查询
 # A 股日频率数据-东方财富
 "stock_zh_a_hist"  # A 股日频率数据-东方财富
 # A 股日频率数据-腾讯
 "stock_zh_a_hist_tx"  # A 股日频率数据-腾讯
 # 盘口异动
 "stock_changes_em"  # 盘口异动
 "stock_board_change_em"  # 板块异动
 # CME 比特币成交量
 "crypto_bitcoin_cme"  # CME 比特币成交量
 # 基金规模和规模趋势
 "fund_aum_em"  # 基金公司规模排名列表
 "fund_aum_trend_em"  # 基金市场管理规模走势图
 "fund_aum_hist_em"  # 基金市场管理规模历史
 # 企业商品价格指数
 "macro_china_qyspjg"  # 企业商品价格指数
 "macro_china_fdi"  # 外商直接投资数据
 # 未决房屋销售月率
 "macro_usa_phs"  # 未决房屋销售月率
 # 德国经济指标
 "macro_germany_ifo"  # ifo商业景气指数
 "macro_germany_cpi_monthly"  # 消费者物价指数月率终值
 "macro_germany_cpi_yearly"  # 消费者物价指数年率终值
 "macro_germany_trade_adjusted"  # 贸易帐(季调后)
 "macro_germany_gdp"  # GDP
 "macro_germany_retail_sale_monthly"  # 实际零售销售月率
 "macro_germany_retail_sale_yearly"  # 实际零售销售年率
 "macro_germany_zew"  # ZEW经济景气指数
 # 东方财富-概念板块
 "stock_board_concept_name_em"  # 概念板块-名称
 "stock_board_concept_hist_em"  # 概念板块-历史行情
 "stock_board_concept_hist_min_em"  # 概念板块-分时历史行情
 "stock_board_concept_cons_em"  # 概念板块-板块成份
 # 瑞士-宏观
 "macro_swiss_svme"  # 瑞士-宏观-SVME采购经理人指数
 "macro_swiss_trade"  # 瑞士-宏观-贸易帐
 "macro_swiss_cpi_yearly"  # 瑞士-宏观-消费者物价指数年率
 "macro_swiss_gdp_quarterly"  # 瑞士-宏观-GDP季率
 "macro_swiss_gbd_yearly"  # 瑞士-宏观-GDP年率
 "macro_swiss_gbd_bank_rate"  # 瑞士-宏观-央行公布利率决议
 # 日本-宏观
 "macro_japan_bank_rate"  # 日本-央行公布利率决议
 "macro_japan_cpi_yearly"  # 日本-全国消费者物价指数年率
 "macro_japan_core_cpi_yearly"  # 日本-全国核心消费者物价指数年率
 "macro_japan_unemployment_rate"  # 日本-失业率
 "macro_japan_head_indicator"  # 日本-领先指标终值
 # 英国-宏观
 "macro_uk_halifax_monthly"  # 英国-Halifax 房价指数月率
 "macro_uk_halifax_yearly"  # 英国-Halifax 房价指数年率
 "macro_uk_trade"  # 英国-贸易帐
 "macro_uk_bank_rate"  # 英国-央行公布利率决议
 "macro_uk_core_cpi_yearly"  # 英国-核心消费者物价指数年率
 "macro_uk_core_cpi_monthly"  # 英国-核心消费者物价指数月率
 "macro_uk_cpi_yearly"  # 英国-消费者物价指数年率
 "macro_uk_cpi_monthly"  # 英国-消费者物价指数月率
 "macro_uk_retail_monthly"  # 英国-零售销售月率
 "macro_uk_retail_yearly"  # 英国-零售销售年率
 "macro_uk_rightmove_yearly"  # 英国-Rightmove 房价指数年率
 "macro_uk_rightmove_monthly"  # 英国-Rightmove 房价指数月率
 "macro_uk_gdp_quarterly"  # 英国-GDP 季率初值
 "macro_uk_gdp_yearly"  # 英国-GDP 年率初值
 "macro_uk_unemployment_rate"  # 英国-失业率
 # 融资融券-深圳
 "stock_margin_underlying_info_szse"  # 标的证券信息
 "stock_margin_detail_szse"  # 融资融券明细
 "stock_margin_szse"  # 融资融券汇总
 # 宏观-澳大利亚
 "macro_australia_bank_rate"  # 央行公布利率决议
 "macro_australia_unemployment_rate"  # 失业率
 "macro_australia_trade"  # 贸易帐
 "macro_australia_cpi_quarterly"  # 消费者物价指数季率
 "macro_australia_cpi_yearly"  # 消费者物价指数年率
 "macro_australia_ppi_quarterly"  # 生产者物价指数季率
 "macro_australia_retail_rate_monthly"  # 零售销售月率
 # 养猪数据中心
 "futures_hog_core"  # 生猪信息-核心数据
 "futures_hog_cost"  # 生猪信息-成本维度
 "futures_hog_supply"  # 生猪信息-供应维度
 # 宏观-加拿大
 "macro_canada_new_house_rate"  # 新屋开工
 "macro_canada_unemployment_rate"  # 失业率
 "macro_canada_trade"  # 贸易帐
 "macro_canada_retail_rate_monthly"  # 零售销售月率
 "macro_canada_bank_rate"  # 央行公布利率决议
 "macro_canada_core_cpi_yearly"  # 核心消费者物价指数年率
 "macro_canada_core_cpi_monthly"  # 核心消费者物价指数月率
 "macro_canada_cpi_yearly"  # 消费者物价指数年率
 "macro_canada_cpi_monthly"  # 消费者物价指数月率
 "macro_canada_gdp_monthly"  # GDP 月率
 # 奥运奖牌
 "sport_olympic_hist"  # 奥运奖牌
 # 港股财报
 "stock_financial_hk_report_em"  # 东方财富-港股-财务报表-三大报表
 "stock_financial_hk_analysis_indicator_em"  # 东方财富-港股-财务分析-主要指标
 # 全部 A 股-等权重市盈率、中位数市盈率
 "stock_a_ttm_lyr"  # 全部 A 股-等权重市盈率、中位数市盈率
 "stock_a_all_pb"  # 全部 A 股-等权重市净率、中位数市净率
 # REITs
 "reits_realtime_em"  #  REITs-行情
 # A 股分时数据
 "stock_zh_a_hist_min_em"  # 东财-股票分时
 "stock_zh_a_hist_pre_min_em"  # 东财-股票盘前分时
 # 港股分时数据
 "stock_hk_hist_min_em"  # 东财-港股分时数据
 # 美股分时数据
 "stock_us_hist_min_em"  # 东财-美股分时数据
 # 可转债详情
 "bond_zh_cov_info"  # 东财-可转债详情
 # 风险警示板
 "stock_zh_a_st_em"  # 风险警示板
 # 美股-粉单市场
 "stock_us_pink_spot_em"  # 美股-粉单市场
 # 美股-知名美股
 "stock_us_famous_spot_em"  # 美股-知名美股
 # 股票-投资评级
 "stock_rank_forecast_cninfo"  # 股票-投资评级
 # 股票-行业市盈率
 "stock_industry_pe_ratio_cninfo"  # 股票-行业市盈率
 # 新股-新股过会
 "stock_new_gh_cninfo"  # 新股-新股过会
 # 新股-IPO
 "stock_new_ipo_cninfo"  # 新股-IPO
 # 股东人数及持股集中度
 "stock_hold_num_cninfo"  # 股东人数及持股集中度
 # 实际控制人持股变动
 "stock_hold_control_cninfo"  # 实际控制人持股变动
 # 高管持股变动明细
 "stock_hold_management_detail_cninfo"  # 高管持股变动明细
 # 期货手续费
 "futures_comm_info"  # 期货手续费
 "futures_fees_info"  # 期货交易费用参照表
 # B 股实时行情数据和历史行情数据
 "stock_zh_b_spot"  # B 股实时行情数据
 "stock_zh_b_daily"  # B 股历史行情数据(日频)
 "stock_zh_b_minute"  # B 股分时历史行情数据(分钟)
 # 公司治理-对外担保
 "stock_cg_guarantee_cninfo"  # 公司治理-对外担保
 # 公司治理-公司诉讼
 "stock_cg_lawsuit_cninfo"  # 公司治理-公司诉讼
 # 公司治理-股权质押
 "stock_cg_equity_mortgage_cninfo"  # 公司治理-股权质押
 # 债券报表-债券发行-国债发行
 "bond_treasure_issue_cninfo"  # 债券报表-债券发行-国债发行
 # 债券报表-债券发行-地方债发行
 "bond_local_government_issue_cninfo"  # 债券报表-债券发行-地方债
 # 债券报表-债券发行-企业债发行
 "bond_corporate_issue_cninfo"  # 债券报表-债券发行-企业债
 # 债券报表-债券发行-可转债发行
 "bond_cov_issue_cninfo"  # 债券报表-债券发行-可转债发行
 # 债券报表-债券发行-可转债转股
 "bond_cov_stock_issue_cninfo"  # 债券报表-债券发行-可转债转股
 # 基金报表-基金重仓股
 "fund_report_stock_cninfo"  # 基金报表-基金重仓股
 # 公告大全-沪深 A 股公告
 "stock_notice_report"  # 公告大全-沪深 A 股公告
 # 基金报表-基金行业配置
 "fund_report_industry_allocation_cninfo"  # 基金报表-基金行业配置
 "fund_report_asset_allocation_cninfo"  # 基金报表-基金资产配置
 # 基金规模
 "fund_scale_open_sina"  # 基金规模-开放式基金
 "fund_scale_close_sina"  # 基金规模-封闭式基金
 "fund_scale_structured_sina"  # 基金规模-分级子基金
 # 指数估值
 "index_value_hist_funddb"  # 指数估值
 # 沪深港通持股
 "stock_hsgt_individual_em"  # 沪深港通持股-具体股票
 "stock_hsgt_individual_detail_em"  # 沪深港通持股-具体股票-详情
 # IPO 受益股
 "stock_ipo_benefit_ths"  # IPO 受益股
 # 同花顺-数据中心-技术选股-创新高
 "stock_rank_cxg_ths"  # 创新高
 "stock_rank_cxd_ths"  # 创新低
 "stock_rank_lxsz_ths"  # 连续上涨
 "stock_rank_lxxd_ths"  # 连续下跌
 "stock_rank_cxfl_ths"  # 持续放量
 "stock_rank_cxsl_ths"  # 持续缩量
 "stock_rank_xstp_ths"  # 向上突破
 "stock_rank_xxtp_ths"  # 向下突破
 "stock_rank_ljqs_ths"  # 量价齐升
 "stock_rank_ljqd_ths"  # 量价齐跌
 "stock_rank_xzjp_ths"  # 险资举牌
 # 可转债分时数据
 "bond_zh_hs_cov_min"  # 可转债分时数据
 "bond_zh_hs_cov_pre_min"  # 可转债分时数据-分时行情-盘前
 # 艺人
 "business_value_artist"  # 艺人商业价值
 "online_value_artist"  # 艺人流量价值
 # 视频
 "video_tv"  # 电视剧集
 "video_variety_show"  # 综艺节目
 # 基金数据-分红送配
 "fund_cf_em"  # 基金拆分
 "fund_fh_rank_em"  # 基金分红排行
 "fund_fh_em"  # 基金分红
 # 基金数据-规模变动
 "fund_scale_change_em"  # 规模变动
 "fund_hold_structure_em"  # 持有人结构
 # 行业板块
 "stock_board_industry_cons_em"  # 行业板块-板块成份
 "stock_board_industry_hist_em"  # 行业板块-历史行情
 "stock_board_industry_hist_min_em"  # 行业板块-分时历史行情
 "stock_board_industry_name_em"  # 行业板块-板块名称
 # 股票回购数据
 "stock_repurchase_em"  # 股票回购数据
 # 期货品种字典
 "futures_hq_subscribe_exchange_symbol"  # 期货品种字典
 # 上海黄金交易所
 "spot_hist_sge"  # 上海黄金交易所-历史行情走势
 "spot_golden_benchmark_sge"  # 上海金基准价
 "spot_silver_benchmark_sge"  # 上海银基准价
 # 个股信息查询
 "stock_individual_info_em"  # 个股信息查询
 # 中国食糖指数
 "index_sugar_msweet"  # 中国食糖指数
 # 配额内进口糖估算指数
 "index_inner_quote_sugar_msweet"  # 配额内进口糖估算指数
 # 配额外进口糖估算指数
 "index_outer_quote_sugar_msweet"  # 配额外进口糖估算指数
 # 东方财富网-数据中心-股东分析-股东持股分析
 "stock_gdfx_free_holding_analyse_em"  # 股东持股分析-十大流通股东
 "stock_gdfx_holding_analyse_em"  # 股东持股分析-十大股东
 "stock_gdfx_free_top_10_em"  # 东方财富网-个股-十大流通股东
 "stock_gdfx_top_10_em"  # 东方财富网-个股-十大股东
 "stock_gdfx_free_holding_detail_em"  # 股东持股明细-十大流通股东
 "stock_gdfx_holding_detail_em"  # 股东持股明细-十大股东
 "stock_gdfx_free_holding_change_em"  # 股东持股变动统计-十大流通股东
 "stock_gdfx_holding_change_em"  # 股东持股变动统计-十大股东
 "stock_gdfx_free_holding_statistics_em"  # 股东持股统计-十大流通股东
 "stock_gdfx_holding_statistics_em"  # 股东持股统计-十大股东
 "stock_gdfx_free_holding_teamwork_em"  # 股东协同-十大流通股东
 "stock_gdfx_holding_teamwork_em"  # 股东协同-十大股东
 # 期权龙虎榜
 "option_lhb_em"  # 期权龙虎榜
 "option_value_analysis_em"  # 期权价值分析
 "option_risk_analysis_em"  # 期权风险分析
 "option_premium_analysis_em"  # 期权折溢价分析
 # 财新指数
 "index_pmi_com_cx"  # 财新数据-指数报告-财新中国 PMI-综合 PMI
 "index_pmi_man_cx"  # 财新数据-指数报告-财新中国 PMI-制造业 PMI
 "index_pmi_ser_cx"  # 财新数据-指数报告-财新中国 PMI-服务业 PMI
 "index_dei_cx"  # 财新数据-指数报告-数字经济指数
 "index_ii_cx"  # 财新数据-指数报告-产业指数
 "index_si_cx"  # 财新数据-指数报告-溢出指数
 "index_fi_cx"  # 财新数据-指数报告-融合指数
 "index_bi_cx"  # 财新数据-指数报告-基础指数
 "index_nei_cx"  # 财新数据-指数报告-中国新经济指数
 "index_li_cx"  # 财新数据-指数报告-劳动力投入指数
 "index_ci_cx"  # 财新数据-指数报告-资本投入指数
 "index_ti_cx"  # 财新数据-指数报告-科技投入指数
 "index_neaw_cx"  # 财新数据-指数报告-新经济行业入职平均工资水平
 "index_awpr_cx"  # 财新数据-指数报告-新经济入职工资溢价水平
 "index_cci_cx"  # 财新数据-指数报告-大宗商品指数
 # 冬奥会
 "sport_olympic_winter_hist"  # 冬奥会-历届奖牌榜
 # 指数历史数据
 "index_zh_a_hist"  # 中国股票指数历史数据
 # 指数分时数据
 "index_zh_a_hist_min_em"  # 中国股票指数-指数分时数据
 # 东方财富-个股人气榜-A股
 "stock_hot_rank_em"  # 东方财富-个股人气榜-人气榜
 "stock_hot_up_em"  # 东方财富-个股人气榜-飙升榜
 "stock_hot_rank_detail_em"  # 东方财富-个股人气榜-历史趋势及粉丝特征
 "stock_hot_rank_detail_realtime_em"  # 东方财富-个股人气榜-实时变动
 "stock_hot_keyword_em"  # 东方财富-个股人气榜-关键词
 "stock_hot_rank_latest_em"  # 东方财富-个股人气榜-最新排名
 "stock_hot_rank_relate_em"  # 东方财富-个股人气榜-相关股票
 # 东方财富-个股人气榜-港股
 "stock_hk_hot_rank_em"  # 东方财富-个股人气榜-人气榜-港股
 "stock_hk_hot_rank_detail_em"  # 东方财富-个股人气榜-历史趋势-港股
 "stock_hk_hot_rank_detail_realtime_em"  # 东方财富-个股人气榜-实时变动-港股
 "stock_hk_hot_rank_latest_em"  # 东方财富-个股人气榜-最新排名-港股
 # 东方财富-股票数据-龙虎榜
 "stock_lhb_detail_em"  # 东方财富网-数据中心-龙虎榜单-龙虎榜详情
 "stock_lhb_stock_statistic_em"  # 东方财富网-数据中心-龙虎榜单-个股上榜统计
 "stock_lhb_stock_detail_em"  # 东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
 "stock_lhb_jgmmtj_em"  # 东方财富网-数据中心-龙虎榜单-机构买卖每日统计
 "stock_lhb_hyyyb_em"  # 东方财富网-数据中心-龙虎榜单-每日活跃营业部
 "stock_lhb_yybph_em"  # 东方财富网-数据中心-龙虎榜单-营业部排行
 "stock_lhb_jgstatistic_em"  # 东方财富网-数据中心-龙虎榜单-机构席位追踪
 "stock_lhb_traderstatistic_em"  # 东方财富网-数据中心-龙虎榜单-营业部统计
 # 投资组合-基金持仓
 "fund_portfolio_hold_em"  # 天天基金网-基金档案-投资组合-基金持仓
 "fund_portfolio_bond_hold_em"  # 天天基金网-基金档案-投资组合-债券持仓
 # 投资组合-重大变动
 "fund_portfolio_change_em"  # 天天基金网-基金档案-投资组合-重大变动
 "fund_portfolio_industry_allocation_em"  # 天天基金网-基金档案-投资组合-行业配置
 # 中国宏观
 "macro_china_insurance_income"  # 原保险保费收入
 "macro_china_mobile_number"  # 手机出货量
 "macro_china_vegetable_basket"  # 菜篮子产品批发价格指数
 "macro_china_agricultural_product"  # 农产品批发价格总指数
 "macro_china_agricultural_index"  # 农副指数
 "macro_china_energy_index"  # 能源指数
 "macro_china_commodity_price_index"  # 大宗商品价格
 "macro_global_sox_index"  # 费城半导体指数
 "macro_china_yw_electronic_index"  # 义乌小商品指数-电子元器件
 "macro_china_construction_index"  # 建材指数
 "macro_china_construction_price_index"  # 建材价格指数
 "macro_china_lpi_index"  # 物流景气指数
 "macro_china_bdti_index"  # 原油运输指数
 "macro_china_bsi_index"  # 超灵便型船运价指数
 # 可转债溢价率分析和可转债价值分析
 "bond_zh_cov_value_analysis"  # 可转债溢价率分析
 "bond_zh_cov_value_analysis"  # 可转债价值分析
 # 南华期货
 "futures_correlation_nh"  # 相关系数矩阵
 "futures_board_index_nh"  # 板块指数涨跌
 "futures_variety_index_nh"  # 品种指数涨跌
 # 股票热度-雪球
 "stock_hot_follow_xq"  # 雪球-沪深股市-热度排行榜-关注排行榜
 "stock_hot_tweet_xq"  # 雪球-沪深股市-热度排行榜-讨论排行榜
 "stock_hot_deal_xq"  # 雪球-沪深股市-热度排行榜-分享交易排行榜
 # 内部交易
 "stock_inner_trade_xq"  # 内部交易
 # 股票-三大报表
 "stock_balance_sheet_by_report_em"  # 东方财富-股票-财务分析-资产负债表-按报告期
 "stock_balance_sheet_by_yearly_em"  # 东方财富-股票-财务分析-资产负债表-按年度
 "stock_profit_sheet_by_report_em"  # 东方财富-股票-财务分析-利润表-报告期
 "stock_profit_sheet_by_yearly_em"  # 东方财富-股票-财务分析-利润表-按年度
 "stock_profit_sheet_by_quarterly_em"  # 东方财富-股票-财务分析-利润表-按单季度
 "stock_cash_flow_sheet_by_report_em"  # 东方财富-股票-财务分析-现金流量表-按报告期
 "stock_cash_flow_sheet_by_yearly_em"  # 东方财富-股票-财务分析-现金流量表-按年度
 "stock_cash_flow_sheet_by_quarterly_em"  # 东方财富-股票-财务分析-现金流量表-按单季度
 "stock_balance_sheet_by_report_delisted_em"  # 东方财富-股票-财务分析-资产负债表-已退市股票-按报告期
 "stock_profit_sheet_by_report_delisted_em"  # 东方财富-股票-财务分析-利润表-已退市股票-按报告期
 "stock_cash_flow_sheet_by_report_delisted_em"  # 东方财富-股票-财务分析-现金流量表-已退市股票-按报告期
 # 宏观-全球事件
 "news_economic_baidu"  # 宏观-全球事件
 # 停复牌
 "news_trade_notify_suspend_baidu"  # 停复牌
 # 财报发行
 "news_report_time_baidu"  # 财报发行
 # 金融期权
 "option_risk_indicator_sse"  # 上海证券交易所-产品-股票期权-期权风险指标
 # 人民币汇率中间价
 "currency_boc_safe"  # 人民币汇率中间价
 # 主营构成
 "stock_zygc_ym"  # 主营构成-益盟
 "stock_zygc_em"  # 主营构成-东财
 # 管理层讨论与分析
 "stock_mda_ym"  # 管理层讨论与分析
 # 行业分类数据
 "stock_industry_category_cninfo"  # 巨潮资讯-行业分类数据
 # 上市公司行业归属的变动情况
 "stock_industry_change_cninfo"  # 巨潮资讯-上市公司行业归属的变动情况
 # 公司股本变动
 "stock_share_change_cninfo"  # 巨潮资讯-公司股本变动
 # 上海金属网
 "futures_news_shmet"  # 上海金属网-快讯
 # 分红配股
 "news_trade_notify_dividend_baidu"  # 分红配股
 # 中国债券信息网-中债指数-中债指数族系-总指数-综合类指数
 "bond_new_composite_index_cbond"  # 中债-新综合指数
 "bond_composite_index_cbond"  # 中债-综合指数
 # 沪深港股通-参考汇率和结算汇率
 "stock_sgt_settlement_exchange_rate_szse"  # 深港通-港股通业务信息-结算汇率
 "stock_sgt_reference_exchange_rate_szse"  # 深港通-港股通业务信息-参考汇率
 "stock_sgt_reference_exchange_rate_sse"  # 沪港通-港股通信息披露-参考汇率
 "stock_sgt_settlement_exchange_rate_sse"  # 沪港通-港股通信息披露-结算汇兑
 # 配股实施方案-巨潮资讯
 "stock_allotment_cninfo"  # 配股实施方案-巨潮资讯
 # 巨潮资讯-个股-公司概况
 "stock_profile_cninfo"  # 巨潮资讯-个股-公司概况
  # 巨潮资讯-个股-上市相关
 "stock_ipo_summary_cninfo"  # 巨潮资讯-个股-上市相关
 # 百度股市通-港股-财务报表-估值数据
 "stock_hk_valuation_baidu"  # 百度股市通-港股-财务报表-估值数据
 # 百度股市通-A 股-财务报表-估值数据
 "stock_zh_valuation_baidu"  # 百度股市通-A 股-财务报表-估值数据
 # 百度股市通- A 股或指数-股评-投票
 "stock_zh_vote_baidu"  # 百度股市通- A 股或指数-股评-投票
 # 百度股市通-期货-新闻
 "futures_news_baidu"  # 百度股市通-期货-新闻
 # 百度股市通-热搜股票
 "stock_hot_search_baidu"  # 百度股市通-热搜股票
 # 乐估乐股-底部研究-巴菲特指标
 "stock_buffett_index_lg"  # 乐估乐股-底部研究-巴菲特指标
 # 百度股市通-外汇-行情榜单
 "fx_quote_baidu"  # 百度股市通-外汇-行情榜单
 # 50ETF 期权波动率指数
 "index_option_50etf_qvix"  # 50ETF 期权波动率指数
 # 50ETF 期权波动率指数 QVIX-分时
 "index_option_50etf_min_qvix"  # 50ETF 期权波动率指数 QVIX-分时
 # 300 ETF 期权波动率指数
 "index_option_300etf_qvix"  # 300 ETF 期权波动率指数
 # 300 ETF 期权波动率指数 QVIX-分时
 "index_option_300etf_min_qvix"  # 300 ETF 期权波动率指数 QVIX-分时
 # 申万指数实时行情
 "index_realtime_sw"  # 申万指数实时行情
 # 申万指数历史行情
 "index_hist_sw"  # 申万指数历史行情
 # 申万宏源研究-行业分类-全部行业分类
 "stock_industry_clf_hist_sw"  # 申万宏源研究-行业分类-全部行业分类
 # 申万指数分时行情
 "index_min_sw"  # 申万指数分时行情
 # 申万指数成分股
 "index_component_sw"  # 申万指数成分股
 # 申万宏源研究-指数分析
 "index_analysis_daily_sw"  # 申万宏源研究-指数分析-日报表
 "index_analysis_weekly_sw"  # 申万宏源研究-指数分析-周报表
 "index_analysis_monthly_sw"  # 申万宏源研究-指数分析-月报表
 "index_analysis_week_month_sw"  # 申万宏源研究-指数分析-周/月-日期序列
 "index_realtime_fund_sw"  # 申万宏源研究-申万指数-指数发布-基金指数-实时行情
 "index_hist_fund_sw"  # 申万宏源研究-申万指数-指数发布-基金指数-历史行情
 # 债券-信息查询结果
 "bond_info_cm"  # 中国外汇交易中心暨全国银行间同业拆借中心-债券-信息查询结果
 "bond_info_detail_cm"  # 中国外汇交易中心暨全国银行间同业拆借中心-债券-债券详情
 # 生猪市场价格指数
 "index_hog_spot_price"  # 生猪市场价格指数
 # 乐咕乐股-股息率-A 股股息率
 "stock_a_gxl_lg"  # 乐咕乐股-股息率-A 股股息率
 "stock_hk_gxl_lg"  # 乐咕乐股-股息率-恒生指数股息率
 # 乐咕乐股-大盘拥挤度
 "stock_a_congestion_lg"  # 乐咕乐股-大盘拥挤度
 # 乐咕乐股-基金仓位
 "fund_stock_position_lg"  # 乐咕乐股-基金仓位-股票型基金仓位
 "fund_balance_position_lg"  # 乐咕乐股-基金仓位-平衡混合型基金仓位
 "fund_linghuo_position_lg"  # 乐咕乐股-基金仓位-灵活配置型基金仓位
 "stock_zyjs_ths"  # 主营介绍
 # 东方财富-行情报价
 "stock_bid_ask_em"  # 东方财富-行情报价
 # 可转债
 "bond_zh_cov_info_ths"  # 同花顺-数据中心-可转债
 # 港股股票指数数据
 "stock_hk_index_spot_sina"  # 新浪财经-行情中心-港股指数
 "stock_hk_index_daily_sina"  # 新浪财经-港股指数-历史行情数据
 "stock_hk_index_spot_em"  # 东方财富网-行情中心-港股-指数实时行情
 "stock_hk_index_daily_em"  # 东方财富网-港股-股票指数数据
 # 同花顺-财务指标-主要指标
 "stock_financial_abstract_ths"  # 同花顺-财务指标-主要指标
 "stock_financial_debt_ths"  # 同花顺-财务指标-资产负债表
 "stock_financial_benefit_ths"  # 同花顺-财务指标-利润表
 "stock_financial_cash_ths"  # 同花顺-财务指标-现金流量表
 # LOF 行情
 "fund_lof_hist_em"  # 东方财富-LOF 行情
 "fund_lof_spot_em"  # 东方财富-LOF 实时行情
 "fund_lof_hist_min_em"  # 东方财富-LOF 分时行情
 # 新浪财经-ESG评级中心
 "stock_esg_msci_sina"  # 新浪财经-ESG评级中心-ESG评级-MSCI
 "stock_esg_rft_sina"  # 新浪财经-ESG评级中心-ESG评级-路孚特
 "stock_esg_rate_sina"  # 新浪财经-ESG评级中心-ESG评级-ESG评级数据
 "stock_esg_zd_sina"  # 新浪财经-ESG评级中心-ESG评级-秩鼎
 "stock_esg_hz_sina"  # 新浪财经-ESG评级中心-ESG评级-华证指数
 # 基金公告
 "fund_announcement_personnel_em"  # 东方财富网站-天天基金网-基金档案-基金公告-人事调整
 # 互动易
 "stock_irm_cninfo"  # 互动易-提问
 "stock_irm_ans_cninfo"  # 互动易-回答
 # 上证e互动
 "stock_sns_sseinfo"  # 上证e互动-提问与回答
 # 新浪财经-债券-可转债
 "bond_cb_profile_sina"  # 新浪财经-债券-可转债-详情资料
 "bond_cb_summary_sina"  # 新浪财经-债券-可转债-债券概况
 # 东方财富网-数据中心-特色数据-高管持股
 "stock_hold_management_detail_em"  # 东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细
 "stock_hold_management_person_em"  # 东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细
 # 股市日历
 "stock_gsrl_gsdt_em"  # 东方财富网-数据中心-股市日历-公司动态
 # 东方财富网-数据中心-股东大会
 "stock_gddh_em"  # 东方财富网-数据中心-股东大会
 # 东方财富网-数据中心-重大合同-重大合同明细
 "stock_zdhtmx_em"  # 重大合同明细
 # 东方财富网-数据中心-研究报告-个股研报
 "stock_research_report_em"  # 个股研报
 # 董监高及相关人员持股变动
 "stock_share_hold_change_sse"  # 董监高及相关人员持股变动-上海证券交易所
 "stock_share_hold_change_szse"  # 董监高及相关人员持股变动-深圳证券交易所
 "stock_share_hold_change_bse"  # 董监高及相关人员持股变动-北京证券交易所
 # 统计局接口
 "macro_china_nbs_nation"  # 国家统计局全国数据通用接口
 "macro_china_nbs_region"  # 国家统计局地区数据通用接口
 # 新浪财经-美股指数行情
 "index_us_stock_sina"  # 新浪财经-美股指数行情
 # 融资融券-标的证券名单及保证金比例查询
 "stock_margin_ratio_pa"  # 融资融券-标的证券名单及保证金比例查询
 # 东财财富-日内分时数据
 "stock_intraday_em"  # 东财财富-日内分时数据
 # 新浪财经-日内分时数据
 "stock_intraday_sina"  # 新浪财经-日内分时数据
 # 同花顺-板块-概念板块-概念图谱
 "stock_board_concept_graph_ths"  # 同花顺-板块-概念板块-概念图谱
 # 恐惧贪婪指数
 "index_fear_greed_funddb"  # 恐惧贪婪指数
 # 筹码分布
 "stock_cyq_em"  # 筹码分布
 # 雪球基金-基金详情
 "fund_individual_basic_info_xq"  # 雪球基金-基金详情
 "fund_individual_achievement_xq"  # 雪球基金-基金业绩
 "fund_individual_analysis_xq"  # 雪球基金-基金数据分析
 "fund_individual_profit_probability_xq"  # 雪球基金-盈利概率
 "fund_individual_detail_info_xq"  # 雪球基金-交易规则
 "fund_individual_detail_hold_xq"  # 雪球基金-持仓详情
 # 港股盈利预测
 "stock_hk_profit_forecast_et"  # 港股盈利预测
 # 雪球-行情中心-个股
 "stock_individual_spot_xq"  # 雪球-行情中心-个股
 # 东方财富网-行情中心-期货市场-国际期货
 "futures_global_em"  # 东方财富网-行情中心-期货市场-国际期货
 # 东方财富-数据中心-沪深港通-市场概括-分时数据
 "stock_hsgt_fund_min_em"  # 东方财富-数据中心-沪深港通-市场概括-分时数据
 # 新浪财经-商品期货-成交持仓
 "futures_hold_pos_sina"  # 新浪财经-商品期货-成交持仓
 # 生意社-商品与期货-现期图
 "futures_spot_sys"  # 生意社-商品与期货-现期图
 # 上海期货交易所指定交割仓库库存周报
 "futures_stock_shfe_js"  # 上海期货交易所指定交割仓库库存周报
 # 期货合约信息
 "futures_contract_info_shfe"  # 上海期货交易所-期货合约信息
 "futures_contract_info_ine"  # 上海国际能源交易中心-期货合约信息
 "futures_contract_info_dce"  # 大连商品交易所-期货合约信息
 "futures_contract_info_czce"  # 郑州商品交易所-期货合约信息
 "futures_contract_info_gfex"  # 广州期货交易所-期货合约信息
 "futures_contract_info_cffex"  # 中国金融期货交易所-期货合约信息
 # 资讯数据
 "stock_info_cjzc_em"  # 资讯数据-财经早餐-东方财富
 "stock_info_global_em"  # 资讯数据-东方财富
 "stock_info_global_sina"  # 资讯数据-新浪财经
 "stock_info_global_futu"  # 资讯数据-富途牛牛
 "stock_info_global_ths"  # 资讯数据-同花顺
 "stock_info_global_cls"  # 资讯数据-财联社
```

## 案例演示

### 期货展期收益率

示例代码

```python
import akshare as ak

get_roll_yield_bar_df = ak.get_roll_yield_bar(type_method="date", var="RB", start_day="20180618", end_day="20180718")
print(get_roll_yield_bar_df)
```

结果显示: 日期, 展期收益率, 最近合约, 下一期合约

```
              roll_yield  near_by deferred
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
