---
tocdepth: 2
---

# 更新日志

本页记录 1.20.x 的更新，按版本号倒序排列，每个版本有固定锚点，如 `changelog.html#v1-20-2`。更早的版本见{doc}`历史更新日志 <changelog_archive>`，锚点名不变，如 `changelog_archive.html#v1-18-95`。接口改名记录见文末的{ref}`接口更名一览表 <changelog-rename>`。

## 1.20.x

(v1-20-13)=
### 1.20.13 fix: accept text values for numeric and boolean parameters

1. 要求数字或布尔值的参数现在也接受文本，便于经 HTTP（如 AKTools）、MCP 或配置文件调用：涉及 stock_zh_a_hist、stock_zh_a_hist_tx、stock_individual_info_em、stock_individual_spot_xq、stock_individual_basic_info_xq、stock_individual_basic_info_us_xq、stock_individual_basic_info_hk_xq 与 6 个 fund_individual_*_xq 接口的 timeout，fund_fh_em、fund_cf_em、bank_fjcf_table_detail 的 page，bank_fjcf_table_detail 的 begin，以及 search 的 limit、documented_only。原先 timeout="5" 报 `Timeout value … must be an int, float or None`，page="-1" 被当作第 -1 页，documented_only="false" 被当作真；无法转换时抛出 InvalidParameterError
2. 上述接口的 timeout 未指定时，原先等于不设超时，ak.set_timeout 对它们不起作用；现在使用 ak.set_timeout 设置的全局超时，默认连接 10 秒、读取 60 秒

(v1-20-12)=
### 1.20.12 perf: reduce requests of sina macro interfaces

1. 新浪财经宏观数据接口由每页 31 条改为每页 1000 条：macro_china_insurance 一次调用的请求数由 307 次降到 10 次，耗时由约 83 秒降到约 4 秒；macro_china_retail_price_index、macro_china_supply_of_money、macro_china_society_electricity 等共 8 个接口同样受益，返回结果不变
2. macro_china_society_traffic_volume、macro_china_postal_telecommunicational 保持每页 31 条：其上游按“非累计”“累计”两组返回数据，按页切分的结果随页长变化，1000 条一页会漏掉 2021 年 1 月等月份
3. news_cctv 去掉标题中的“[视频]”与正文开头的“央视网消息（新闻联播）：”时，原先按字符集合删除两端字符，以“视频”结尾的标题会被截掉末尾两字，正文以“新”“央”等字开头时也会被误删；现在只删除前缀
4. 移除 get_rank_table_czce、stock_news_em、news_cctv 请求头中写死的过期 Cookie，去掉后返回结果不变；同时删除不再使用的请求头常量

(v1-20-11)=
### 1.20.11 fix: fix air_quality_hist interface and remove dead interfaces

1. 修复 air_quality_hist 接口：真气网更换了请求加密的顺序与密钥，并改为写在页面里，原先内置的加密代码已无法使用，接口报 `JSONDecodeError`；现在每次调用时从真气网首页读取当前密钥，并使用站点当前的加解密代码
2. air_quality_hist 的默认日期改为近期：上游只提供最近约一年的数据，更早的日期返回空表并给出警告；月度数据上游目前无论查询哪个城市都返回郑州 2021-08～2022-08 的数据，现在城市名不符时报错，而不是返回其他城市的数据
3. 更新 air_quality_watch_point 文档的示例日期：上游只提供近期的数据，原示例的日期返回空表
4. 移除盖世汽车销量排行接口 car_sale_rank_gasgoo：盖世汽车启用了腾讯人机验证码，程序无法完成验证，接口报 `JSONDecodeError`
5. 移除碳交易网行情接口 energy_carbon_domestic：其数据服务返回 HTTP 500 并要求登录，接口报 `JSONDecodeError`；北京、深圳、湖北、广州等交易所的碳排放接口不受影响

(v1-20-10)=
### 1.20.10 fix: fix get_receipt interface

1. 修复 get_receipt 接口：上期所仓单页面新增 `20号胶(仓库)`、`20号胶(厂库)` 两个品种，品种映射中没有这两个名称，所有包含上期所品种的调用都报 ValueError: list.index(x): x not in list；现已映射为 NR，此后遇到未识别的新品种时给出警告并跳过，不再整体报错
2. 期货接口使用的 requests_link、pandas_read_html_link 重试用尽后原先返回 None，用户只能看到 'NoneType' object has no attribute 'text'；现在抛出原始的网络异常，如 ConnectTimeout、ProxyError
3. get_shfe_daily、get_czce_daily 原先处理 404 的分支从不执行：前者把响应对象与整数比较，两者都没有检查状态码；现在 404 返回空表，其他错误状态码给出警告后返回空表

(v1-20-9)=
### 1.20.9 refactor: replace demjson with jsonish

1. 移除内嵌的 demjson 2.2.4（约 7000 行，2015 年后已停止维护），改用新增的 akshare.utils.jsonish 解析上游返回的 JavaScript 对象字面量，涉及新浪、天天基金、腾讯等数据源的 60 余个接口
2. 解析速度显著提升：fund_open_fund_daily_em 等需解析数 MB 数据的接口，解析耗时由约 10 秒降至 0.1 秒以内；以 817 份真实响应计，总耗时由 75.9 秒降至 2.9 秒，解析结果与 demjson 逐份一致
3. 数组中的空位（如 fund_new_found_em 的部分字段）由 demjson 的 undefined 对象改为 None，在 DataFrame 中表现为正常的空值
4. 无法解析时抛出 DataParsingError，并附上出错位置附近的原文

(v1-20-8)=
### 1.20.8 build: raise dependency floors and drop pandas inplace

1. 上调依赖下限：pandas>=2.2.2、lxml>=4.9.2、beautifulsoup4>=4.11.2、html5lib>=1.1、openpyxl>=3.1.0、xlrd>=2.0.1。原先的下限在 Python 3.11 上无法使用：lxml 4.2.1 没有预编译包且源码编译失败，pandas 2.0.0 不兼容 numpy 2，部分接口用到的 DataFrame.map 需要 pandas 2.1 及以上，xlrd 与 openpyxl 低于 pandas 自身要求的版本，在最低版本环境下 currency_boc_safe、stock_zh_index_value_csindex 等接口会报错
2. 962 处 pandas 的 inplace=True 写法改为使用返回值。pandas 3.1 已弃用 inplace 并计划在 pandas 4 中移除，原先每次调用会产生大量 Pandas4Warning，如 stock_financial_report_sina 单次调用 118 条
3. CI 新增 lowest-deps 检查，在 Python 3.11 上按声明的最低版本安装依赖并运行测试

(v1-20-7)=
### 1.20.7 fix: stop retrying when eastmoney push2 rate-limits

1. 东方财富 push2 行情服务器限流时直接断开连接，原先会被当作普通网络故障在几秒内连续重试，而被封期间的请求会延长限流；现在识别出来后立即抛出 RateLimitError 并说明原因与等待时间，不再重试。涉及实时行情、历史 K 线、板块、资金流等使用 push2 的接口，详见{ref}`常见问题 <faq-eastmoney-ratelimit>`
2. 原先各自实现的重试统一为 akshare.utils.http.request_with_retry：连接失败、超时与 429、5xx 状态码最多尝试 3 次，按指数退避等待；其他状态码不再重试
3. 期货的 get_shfe_rank_table、get_receipt、futures_spot_price、get_shfe_daily 等接口，链接失败时由固定等待 5 秒、最多重试 20 次改为上述策略，最坏情况下的等待由近 2 分钟缩短到数秒
4. get_dce_rank_table 获取合约列表时，原先遇到任何错误都会无限重试，上游故障或改版时接口一直不返回；现在用尽重试次数后抛出异常

(v1-20-6)=
### 1.20.6 fix: fix fx_c_swap_cm, fred_md and fred_qd interface

1. 修复 fx_c_swap_cm 接口：www.chinamoney.org.cn 已无法完成 TLS 握手，改用 www.chinamoney.com.cn
2. 修复 fred_md、fred_qd 接口：原 S3 地址已返回 403，改从 www.stlouisfed.org 获取；当年以前的各期从官方历史压缩包中读取，首次调用需下载约 20～40 MB，同一进程内不重复下载；没有对应一期时抛出 InvalidParameterError 并给出可选范围
3. 84 处裸 except 改为 except Exception，翻页等循环中按 Ctrl+C 可正常中断，不再被当作“没有下一页”而返回部分数据
4. 库代码中的提示信息由 print 改为 warnings.warn，可用 warnings.filterwarnings 统一屏蔽，同一处的相同提示只显示一次；match_main_contract、get_receipt、get_rank_sum_daily 中打印进度的回显已移除

(v1-20-5)=
### 1.20.5 fix: fix futures_comm_info and stock_us_valuation_baidu interface

1. 修复 futures_comm_info 接口：一次调用由 14 个请求减为 2 个，不再因自身请求过多被九期网限流；上游返回 429 时抛出 RateLimitError，其他错误状态码抛出 APIError，页面改版时抛出 DataParsingError，不再报出 No tables found 或 'NoneType' object has no attribute 'previous'
2. 修复 stock_us_valuation_baidu 接口：上游地址由 gushitong.baidu.com 迁至 finance.baidu.com，原实现不跟随 301 跳转而报 JSONDecodeError
3. ak.set_proxies、ak.set_timeout 扩展到经 curl_cffi、urllib3、http.client 取数的接口，包括 stock_news_em、stock_hk_valuation_baidu、news_economic_baidu、news_trade_notify_suspend_baidu、news_report_time_baidu、news_trade_notify_dividend_baidu、macro_china_nbs_nation、macro_china_nbs_region、macro_china_urban_unemployment 与 amac_person_bond_org_list
4. ak.set_proxies、ak.set_timeout 扩展到由 pandas 直接读取网址的接口，包括 index_option_50etf_qvix 等 18 个期权波动率指数接口、article_epu_index、fred_md、fred_qd、macro_cnbs、currency_boc_safe、hf_sp_500、futures_hist_daily_cffex、stock_zh_index_value_csindex、repo_rate_query 与 stock_szse_sector_summary；这类请求原先没有超时，上游无响应时会一直等待。至此全部接口均受这两项设置控制
5. 移除未被使用的依赖 decorator、jsonpath 与 tabulate

(v1-20-4)=
### 1.20.4 feat: add global timeout and proxy settings

1. 所有基于 requests 的接口默认连接超时 10 秒、读取超时 60 秒，上游无响应时抛出 ConnectTimeout 或 ReadTimeout，不再无限等待；可用 ak.set_timeout 调整，ak.set_timeout(None) 恢复不限时
2. 新增 ak.set_proxies、ak.get_proxies、ak.set_timeout、ak.get_timeout 与 ak.ProxyContext，全局代理与超时对上述接口全部生效；原 akshare.utils.context 中的同名函数未导出，且只对 3 个模块生效
3. 新增 akshare.utils.http 作为统一的请求入口，315 个模块改经它发请求，Ruff 启用 TID251 禁止直接调用 requests.get、requests.post 与 requests.Session
4. stock_news_em、百度股市通系列、国家统计局系列等约 10 个经 curl_cffi 或其他 HTTP 库取数的接口暂不受上述设置影响，详见{ref}`常见问题 <faq-proxy>`

(v1-20-3)=
### 1.20.3 fix: replace eval with ast.literal_eval

1. stock_zh_a_daily、stock_zh_b_daily、stock_zh_kcb_daily、stock_hk_daily、stock_us_daily、stock_zh_a_tick_tx_js、fund_etf_dividend_sina、fund_fh_em、fund_cf_em、fund_fh_rank_em、option_cffex_sz50_daily_sina、option_cffex_hs300_daily_sina、option_cffex_zz1000_daily_sina、macro_euro_lme_holding、macro_euro_lme_stock 及 4 个 macro_usa_cftc_* 接口解析上游响应时由 eval 改为 ast.literal_eval，避免执行响应中的任意代码；其中 stock_zh_a_tick_tx_js 经明文 HTTP 取数，原写法可被中间人利用；返回结果不变
2. Ruff 启用 S307、S501 规则，禁止新增 eval 与 verify=False

(v1-20-2)=
### 1.20.2 fix: fix stock_board_concept_name_em interface

1. stock_board_concept_name_em、stock_board_industry_name_em 新增“领涨股票-代码”字段，股票名称变更（如加去 ST）时可按代码关联
2. 两个接口改为按东方财富字段名映射列名，上游新增字段时不再报 Length mismatch

(v1-20-1)=
### 1.20.1 build: switch release to trusted publishing

1. 接口与代码无变化，可放心升级
2. PyPI 发布改用 Trusted Publishing，安装包附带 PEP 740 数字证明，可验证来自 akfamily/akshare 仓库
3. 发布 tag 由 release-vX.Y.Z 改为 vX.Y.Z，本版本对应 tag v1.20.1
4. 不再提供 Docker 镜像；需要 HTTP API 时请使用 `pip install aktools` 部署，详见 [HTTP API（AKTools）](https://akshare.akfamily.xyz/aktools.html)
5. 删除多余的 setup.py，打包配置统一由 pyproject.toml 提供

(v1-20-0)=
### 1.20.0 refactor!: reorganize subpackages by interface category

1. 重新整理 `akshare/` 目录，不兼容旧的模块路径：子包名与 `ak.search()` 的类目名一一对应，股票接口按数据字典的 9 个主题分到 `akshare/stock/` 下的子目录，文件名统一为“类目_主题_数据源.py”。`ak.接口名()` 与 `from akshare import 接口名` 的用法不受影响；按 `from akshare.子包.模块 import 接口名` 导入的代码需要按 [AKShare 1.20.0 模块路径迁移](https://akshare.akfamily.xyz/migration.html) 中的对照表修改
2. 拆分接口跨类目的 3 个模块：bond_china_money、macro_other、news_baidu
3. 删除从未对外导出的失效或未完成代码：futures_rule_em、stock_kcb_renewal、stock_kcb_detail_renewal，以及 3 个未被使用的常量文件
4. 新增 fortune_rank 接口：历年《财富》世界 500 强榜单（1996 年至今），各年份输出统一为固定的 9 列
5. `akshare/__init__.py` 不再保留版本历史（完整记录见本页），导入语句按类目分组，文件由 7077 行减为约 2500 行
6. 内置数据文件统一放到 `akshare/data/`，通过 `akshare/datasets.py` 加载

(changelog-rename)=
## 接口更名一览表

| AKShare 版本 | 旧接口名称                                  | 新接口名称                                  | 修改日期 |
| ------------ | ------------------------------------------- | ------------------------------------------- | -------- |
| 1.17.81      | get_czce_rank_table                         | get_rank_table_czce                         | 20251103 |
| 1.17.81      | futures_czce_warehouse_receipt              | futures_warehouse_receipt_czce              | 20251103 |
| 1.17.72      | futures_dce_warehouse_receipt               | futures_warehouse_receipt_dce               | 20251027 |
| 1.17.68      | option_gfex_vol_daily                       | option_vol_gfex                             | 20251017 |
| 1.17.68      | option_gfex_daily                           | option_hist_gfex                            | 20251017 |
| 1.17.68      | option_shfe_daily                           | option_hist_shfe                            | 20251017 |
| 1.17.68      | option_czce_daily                           | option_hist_czce                            | 20251017 |
| 1.17.68      | option_dce_daily                            | option_hist_dce                             | 20251017 |
| 1.17.68      | option_czce_hist                            | option_hist_yearly_czce                     | 20251017 |
| 1.16.29      | futures_global_em                           | futures_global_spot_em                      | 20250305 |
| 1.13.88      | index_cflp_volume                           | index_volume_cflp                           | 20240527 |
| 1.13.88      | index_cflp_price                            | index_price_cflp                            | 20240527 |
| 1.13.19      | car_gasgoo_sale_rank                        | car_sale_rank_gasgoo                        | 20240403 |
| 1.13.19      | car_energy_sale_cpca                        | car_market_fuel_cpca                        | 20240403 |
| 1.13.15      | car_market_cpca                             | car_market_total_cpca                       | 20240331 |
| 1.12.95      | futures_hog_rank                            | futures_hog_cost                            | 20240318 |
| 1.12.95      | futures_hog_info                            | futures_hog_core                            | 20240318 |
| 1.12.93      | get_bond_bank                               | bond_debt_nafmii                            | 20240316 |
| 1.12.91      | stock_telegraph_cls                         | stock_info_global_cls                       | 20240313 |
| 1.12.11      | stock_zh_index_spot                         | stock_zh_index_spot_sina                    | 20240104 |
| 1.11.64      | futures_sgx_daily                           | futures_settlement_price_sgx                | 20231108 |
| 1.11.61      | fund_manager                                | fund_manager_em                             | 20231105 |
| 1.11.41      | weibo_index                                 | index_weibo_sina                            | 20231020 |
| 1.11.39      | option_300etf_min_qvix                      | index_option_300etf_min_qvix                | 20231019 |
| 1.11.39      | option_300etf_qvix                          | index_option_300etf_qvix                    | 20231019 |
| 1.11.39      | option_50etf_min_qvix                       | index_option_50etf_min_qvix                 | 20231019 |
| 1.11.39      | option_50etf_qvix                           | index_option_50etf_qvix                     | 20231019 |
| 1.10.50      | car_cpca_energy_sale                        | car_energy_sale_cpca                        | 20230710 |
| 1.10.36      | stock_em_sy_hy_list                         | stock_sy_hy_em                              | 20230624 |
| 1.10.36      | stock_em_sy_list                            | stock_sy_em                                 | 20230624 |
| 1.10.36      | stock_em_sy_jz_list                         | stock_sy_jz_em                              | 20230624 |
| 1.10.36      | stock_em_sy_yq_list                         | stock_sy_yq_em                              | 20230624 |
| 1.10.36      | stock_em_sy_profile                         | stock_sy_profile_em                         | 20230624 |
| 1.10.8       | futures_nh_volatility_index                 | futures_volatility_index_nh                 | 20230606 |
| 1.9.37       | stock_hk_eniu_indicator                     | stock_hk_indicator_eniu                     | 20230404 |
| 1.9.27       | fund_em_hk_rank                             | fund_hk_rank_em                             | 20230330 |
| 1.9.27       | fund_em_lcx_rank                            | fund_lcx_rank_em                            | 20230330 |
| 1.9.27       | fund_em_money_rank                          | fund_money_rank_em                          | 20230330 |
| 1.9.27       | fund_em_exchange_rank                       | fund_exchange_rank_em                       | 20230330 |
| 1.9.7        | stock_profit_forecast                       | stock_profit_forecast_em                    | 20230330 |
| 1.8.38       | macro_cons_silver_amount                    | macro_cons_silver                           | 20221227 |
| 1.8.38       | macro_cons_silver_change                    | macro_cons_silver                           | 20221227 |
| 1.8.38       | macro_cons_silver_volume                    | macro_cons_silver                           | 20221227 |
| 1.8.38       | macro_cons_gold_amount                      | macro_cons_gold                             | 20221227 |
| 1.8.38       | macro_cons_gold_change                      | macro_cons_gold                             | 20221227 |
| 1.8.38       | macro_cons_gold_volume                      | macro_cons_gold                             | 20221227 |
| 1.8.23       | stock_restricted_shares                     | stock_restricted_release_queue_sina         | 20221122 |
| 1.8.3        | stock_em_qbzf                               | stock_qbzf_em                               | 20221122 |
| 1.8.3        | stock_em_pg                                 | stock_pg_em                                 | 20221122 |
| 1.7.99       | stock_sina_lhb_jgmx                         | stock_lhb_jgmx_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_jgzz                         | stock_lhb_jgzz_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_yytj                         | stock_lhb_yytj_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_ggtj                         | stock_lhb_ggtj_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_detail_daily                 | stock_lhb_detail_daily_sina                 | 20221119 |
| 1.7.82       | index_analysis_sw                           | index_analysis_daily_sw                     | 20220921 |
| 1.7.27       | stock_em_qsjy                               | stock_qsjy_em                               | 20220921 |
| 1.7.23       | futures_pig_info                            | futures_hog_info                            | 20220916 |
| 1.7.23       | futures_pig_rank                            | futures_hog_rank                            | 20220916 |
| 1.6.86       | stock_em_gpzy_distribute_statistics_company | stock_gpzy_distribute_statistics_company_em | 20220811 |
| 1.6.86       | stock_em_gpzy_distribute_statistics_bank    | stock_gpzy_distribute_statistics_bank_em    | 20220811 |
| 1.5.94       | bond_conv_adj_logs_jsl                      | bond_cb_adj_logs_jsl                        | 20220524 |
| 1.5.94       | bond_cov_jsl                                | bond_cb_jsl                                 | 20220524 |
| 1.5.53       | stock_em_xjll                               | stock_xjll_em                               | 20220501 |
| 1.5.53       | stock_em_lrb                                | stock_lrb_em                                | 20220501 |
| 1.5.53       | stock_em_zcfz                               | stock_zcfz_em                               | 20220501 |
| 1.5.52       | stock_em_ggcg                               | stock_ggcg_em                               | 20220501 |
| 1.5.48       | futures_nh_price_index                      | futures_price_index_nh                      | 20220428 |
| 1.5.48       | futures_nh_index_symbol_table               | futures_index_symbol_table_nh               | 20220428 |
| 1.5.48       | futures_nh_return_index                     | futures_return_index_nh                     | 20220428 |
| 1.5.46       | stock_em_yzxdr                              | stock_yzxdr_em                              | 20220427 |
| 1.5.34       | stock_em_gpzy_industry_data                 | stock_gpzy_industry_data_em                 | 20220420 |
| 1.5.26       | stock_em_comment                            | stock_comment_em                            | 20220415 |
| 1.5.25       | stock_em_analyst_detail                     | stock_analyst_detail_em                     | 20220415 |
| 1.5.25       | stock_em_analyst_rank                       | stock_analyst_rank_em                       | 20220415 |
| 1.5.18       | fund_em_open_fund_rank                      | fund_open_fund_rank_em                      | 20220414 |
| 1.5.12       | stock_em_gpzy_pledge_ratio_detail           | stock_gpzy_pledge_ratio_detail_em           | 20220410 |
| 1.5.10       | stock_em_gpzy_pledge_ratio                  | stock_gpzy_pledge_ratio_em                  | 20220410 |
| 1.5.10       | stock_em_gpzy_profile                       | stock_gpzy_profile_em                       | 20220410 |
| 1.4.88       | fund_em_new_found                           | fund_new_found_em                           | 20220323 |
| 1.4.86       | fund_em_aum_hist                            | fund_aum_hist_em                            | 20220322 |
| 1.4.86       | fund_em_aum_trend                           | fund_aum_trend_em                           | 20220322 |
| 1.4.86       | fund_em_aum                                 | fund_aum_em                                 | 20220322 |
