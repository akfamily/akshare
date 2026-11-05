---
tocdepth: 2
---

# 更新日志

本页记录 1.20.x 的更新，按版本号倒序排列，每个版本有固定锚点，如 `changelog.html#v1-20-2`。更早的版本见{doc}`历史更新日志 <changelog_archive>`，锚点名不变，如 `changelog_archive.html#v1-18-95`。接口改名记录见文末的{ref}`接口更名一览表 <changelog-rename>`。

## 1.20.x

(v1-20-35)=
### 1.20.35 fix: fix bond_info_cm and bond_info_detail_cm interface

1. 修复 bond_info_cm 只按债券简称或代码查询时、以及 bond_info_detail_cm 报 `KeyError: 'pageTotal'` 的问题：中国货币网要求查询债券信息时必须指定债券类型，否则返回“债券类型必选”。现在未传 bond_type 但传入 bond_name 或 bond_code 时，依次按各债券类型查询，查到即停（查不到时约需 20 秒）；什么条件都不传时抛出 APIError 说明原因。连续请求时上游偶发返回非 JSON 内容，现会重试。bond_info_detail_cm 的默认值与文档示例改为 24国开10，文档补充 bond_type 的说明
2. fx_china_bank_sina（1 处）、index_research_sw（申万指数，2 处）、stock_board_industry_ths（1 处）、stock_info（股票列表，4 处）由按位置命名改为按上游字段名或表头映射；逐一实测 29 个调用改动前后返回结果一致。此前用于前后对比的采集脚本会漏掉带 lru_cache 等装饰器的函数，这几个模块中被漏掉的调用这次一并补测
3. 按位置赋列名的写法降至 483 处

(v1-20-34)=
### 1.20.34 refactor: map columns by upstream field name in report, restricted, analyst, legu, fx and cni modules

1. stock_report_em（资产负债表、利润表、现金流量表，4 处）、stock_restricted_em（限售解禁，4 处）、stock_analyst_em（分析师指数，3 处）、stock_a_pe_and_pb（乐咕乐股市盈率，3 处）、fx_quote（人民币外汇报价，3 处）、index_cni（国证指数，2 处）、futures_basis（现货与基差，1 处）由按位置命名改为按上游字段名或表头映射；逐一实测改动前后返回结果一致，其中外汇报价为实时数据，确认货币对与列名一致、仅报价随行情变化
2. 模块 index_cni 的 `__main__` 中 index_detail_hist_cni 示例多传了不存在的 date 参数，运行即报 TypeError，现已去掉；接口本身与文档不受影响
3. stock_zh_ah_tx、stock_market_legu、fund_rating、stock_board_concept_ths 的上游返回无字段名的数组，保持按位置命名
4. 按位置赋列名的写法降至 491 处

(v1-20-33)=
### 1.20.33 fix: fix fund_hk_rank_em, futures_settle_gfex and stock_gpzy_distribute_statistics interfaces

1. 修复 fund_hk_rank_em 返回错列数据的问题：天天基金香港基金排行每条记录的字段顺序不固定，原代码按位置命名，“基金代码”列实为币种、“基金简称”列实为基金代码、“日期”列为 1970 年、“可购买”列实为基金全称，且不报错；现按 HKFCODE、FCODE、SHORTNAME、CURRENCY、JZRQ、NAV、W、M、Q、HY、Y、TWY、TRY、SY、SE、ISBUY 等字段名映射，并与 fund_hk_fund_hist_em 的净值交叉核对一致
2. 修复 fund_hk_fund_hist_em 查询已停止披露净值的基金时报 KeyError 的问题，现在返回带列名的空表
3. 修复 futures_settle_gfex 以及 futures_settle(market="GFEX") 报 `Length mismatch` 的问题：广州期货交易所不再返回自营与客户持仓限额两个字段；现按字段名映射，self_tot_buy_posi_quota、client_buy_posi_quota 两列保留并填空值
4. 修复 stock_gpzy_distribute_statistics_company_em、stock_gpzy_distribute_statistics_bank_em 报 `TypeError: 'NoneType' object is not subscriptable` 的问题：东方财富把质押机构类型由“证券”“银行”改为“证券Ⅱ”“银行Ⅱ”，按旧值筛选返回空；现改用新值，并按字段名映射列名
5. stock_gpzy_em（4 处）、futures_settle（4 处）、bond_cbond（2 处）、fund_rank_em（fund_money_rank_em 1 处）由按位置命名改为按上游字段名映射；前三个模块逐一实测改动前后返回结果一致，fund_money_rank_em 因上游数据在两次采集之间更新，未做前后对比
6. 按位置赋列名的写法降至 511 处

(v1-20-32)=
### 1.20.32 fix!: fix stock_ipo_benefit_ths, remove movie_boxoffice_weekly and movie_boxoffice_cinema_weekly

**不兼容的改动：移除艺恩周票房接口 movie_boxoffice_weekly、movie_boxoffice_cinema_weekly。** 2026-11-05 实测，艺恩的周榜对最近一周和历史周都返回“没有权限”，必须登录账号才能获取，匿名无法使用；这两个接口此前也不发请求、直接报错。调用这两个接口的代码请删除。

1. 艺恩日票房 movie_boxoffice_daily、影院日票房 movie_boxoffice_cinema_daily 只能匿名查询当天及前 2 天的数据，更早的日期需要登录。原先查询更早的日期只报“没有权限”，现在报错信息说明可查询的日期范围；date 参数的默认值由已无法查询的 "20240219" 改为空字符串，表示前一天，不传参数即可取得最新数据；文档的限量说明、参数说明、接口示例与数据示例改用可查询的日期
2. 修复 stock_ipo_benefit_ths 报 `AttributeError: 'NoneType' object has no attribute 'text'` 的问题：同花顺 IPO 受益股页面目前没有数据，表格为空且不显示分页信息，原代码找不到分页信息即报错；现在按 1 页处理，上游无数据时返回带有原列名的空表
3. stock_lhb_em（龙虎榜，5 处）、alternative_movie_yien（艺恩票房，4 处）、fund_xq（雪球基金，5 处）、stock_board_industry_ths（同花顺行业一览表，1 处）由按位置命名改为按上游字段名或网页表头映射；逐一实测 30 个调用改动前后返回结果一致。spot_sge（上海黄金交易所）上游返回无字段名的数组，保持按位置命名
4. 按位置赋列名的写法降至 526 处

(v1-20-31)=
### 1.20.31 fix!: rename get_ interfaces, raise a clear error for all dce interfaces

**不兼容的改动：17 个以 get_ 开头的数据接口按 `futures_<主题>_<交易所>` 的命名规则改名，旧名称不再保留，调用旧名称会报 AttributeError。** 改名对照见文末的{ref}`接口更名一览表 <changelog-rename>`：get_shfe_daily→futures_daily_shfe、get_dce_daily→futures_daily_dce、get_czce_daily→futures_daily_czce、get_cffex_daily→futures_daily_cffex、get_ine_daily→futures_daily_ine、get_gfex_daily→futures_daily_gfex、get_futures_daily→futures_daily、get_shfe_rank_table→futures_rank_table_shfe、get_dce_rank_table→futures_rank_table_dce、get_cffex_rank_table→futures_rank_table_cffex、get_rank_table_czce→futures_rank_table_czce、get_rank_sum→futures_rank_sum、get_rank_sum_daily→futures_rank_sum_daily、get_receipt→futures_receipt、get_roll_yield→futures_roll_yield、get_roll_yield_bar→futures_roll_yield_bar、get_us_stock_name→stock_us_name_sina。参数与返回结果均不变，请把代码中的旧名称替换为新名称。配置类函数 get_proxies、get_timeout、get_token 不受影响。

1. 大连商品交易所全站启用瑞数反爬虫验证，程序请求返回 HTTP 412；原先只有 futures_warehouse_receipt_dce 给出明确报错，其余 15 个接口报 `BadZipFile`、`JSONDecodeError`、`IndexError` 等难以理解的错误，futures_roll_yield_bar 甚至返回空表。现在在统一的 HTTP 入口识别大商所的 412，涉及大商所的 16 个接口（futures_dce_position_rank、futures_daily_dce、futures_daily(market="DCE")、option_hist_dce 等）统一抛出 DceBlockedError（APIError 的子类，status_code 为 412）并说明原因；大商所解除限制后无需改代码即可恢复。常见问题“大连商品交易所相关接口报错或返回空数据”一节同步更新，并补充用 futures_hold_pos_sina 按合约获取大商所成交持仓排名的替代方法
2. futures_zh_spot 传入无效或已到期的合约（如 V2405）时，原先报难以理解的 `Length mismatch`，现在抛出 InvalidParameterError 并提示检查合约代码；模块 `__main__` 中已到期的示例合约 V2405、V2409 改为 V2701、V2705
3. stock_dzjy_em（大宗交易，6 处）、stock_fund_flow（同花顺资金流向，6 处）、stock_summary（深交所市场总貌，1 处）、futures_zh_sina（新浪期货分钟与日线，2 处）由按位置命名改为按上游字段名或网页表头映射；逐一实测 38 个调用，改动前后返回结果一致
4. 表头含查询月份（stock_szse_sector_summary）或排序箭头（stock_fund_flow_big_deal 的“成交时间↓”）的表格，按表头名映射反而更脆弱，保持按位置命名
5. 修复 stock_us_name_sina、stock_us_spot 翻页途中报 `KeyError: 'data'` 的问题：新浪美股列表每页固定 20 条，取全部美股需翻 900 多页，连续翻页时新浪偶发以 200 状态码返回后端数据库错误（`MySQL server has gone away`），原先直接报错且已翻的页全部作废；现在同一页按指数退避重试，重试后仍失败时抛出带页码和新浪错误信息的 APIError。同时不再修改共享的请求参数字典，翻页时复用同一个 JS 引擎，并修正总页数在股票数为 20 的整数倍时多算一页的问题
6. http.request_with_retry 新增 retry_if 参数，用于上游以 200 状态码返回错误内容时重试
7. 按位置赋列名的写法降至 541 处

(v1-20-30)=
### 1.20.30 fix!: fix stock_rank_lxxd_ths and stock_gdfx_em interfaces

**不兼容的改动：stock_rank_lxxd_ths（连续下跌）的“连涨天数”列更名为“连跌天数”，数值不变。** 同花顺该页面的表头为“连跌天数”，原代码与文档沿用了连续上涨接口的列名；按旧列名取值的代码请改用新列名。

1. stock_technology_ths 模块中 11 个技术选股接口（stock_rank_cxg_ths、stock_rank_lxsz_ths、stock_rank_cxfl_ths、stock_rank_ljqs_ths、stock_rank_xzjp_ths 等）由按位置命名改为按网页表头映射列名，同花顺调整表头顺序或增加列时不再错列；除上述更名外，逐一实测 17 个调用改动前后返回结果一致
2. macro_canada（10 个接口）、macro_australia（7 个接口）与 macro_usa 中东方财富全球宏观数据的 2 处，由按位置命名改为按上游字段名映射（REPORT_DATE_CH→时间、PUBLISH_DATE→发布日期、VALUE→现值、PRE_VALUE→前值）；逐一实测 58 个调用改动前后返回结果一致
3. 修复 stock_gdfx_free_holding_statistics_em、stock_gdfx_holding_statistics_em、stock_gdfx_holding_change_em 报 `Length mismatch` 的问题：东方财富在这几个接口的返回中增加了 SEAB_JOIN_LIS 等字段，原代码按位置命名，列数对不上即报错；现按上游字段名映射，返回的列名与类型不变
4. stock_gdfx_em 模块其余 9 处改为按上游字段名映射。十大股东与十大流通股东的持股变动接口中，上游市值（HOLDER_MARKET_CAP）与收盘价（CLOSE_PRICE）两个字段的位置正好相反，按位置命名时上游再调整一次顺序，“流通市值统计”就会变成收盘价且不报错；改为按字段名后不再有此风险。逐一实测改动前后返回结果一致
5. 按位置赋列名的写法降至 556 处

(v1-20-29)=
### 1.20.29 fix!: fix option_finance_sse_underlying and option_finance_board interface

**不兼容的改动：option_finance_sse_underlying 的 `成交量(手)`、`成交额(万元)` 两列更名为 `成交量(份)`、`成交额(元)`，数值不变。** 原列名标注的单位有误：上交所返回的成交量单位为份、成交额单位为元，5 个品种的成交额除以成交量均与当前价一致（如华夏上证50ETF期权 1991302797÷681494179≈2.92，当前价 2.93）。按旧列名取值的代码请改用新列名。

1. 修复 option_finance_sse_underlying 报 `TypeError: Invalid value ... for dtype 'float64'` 的问题：原代码把更新时间写入数值列，pandas 3 不再允许；现按请求参数 select 的字段顺序命名各列，更新日期整列赋值。同时修正“代码”列：上游不返回代码，原代码把第一行写死为 510300，查询华夏上证50ETF期权等其他品种时代码也显示为 510300；现取请求地址中的标的代码，如 510050、588000
2. 修复 option_finance_board 在 symbol="嘉实沪深300ETF期权" 时返回其他标的合约的问题：深交所期权列表包含沪深300ETF、创业板ETF、中证500ETF、深证100ETF 全部 4 个标的的期权，原代码未按标的筛选，返回当月全部合约；现只保留标的为沪深300ETF 的合约，并改为按上游字段名映射列名。其余品种返回结果不变
3. 模块 `__main__` 中示例的到期月份由已过期的 2306 改为 2612

(v1-20-28)=
### 1.20.28 fix!: fix index_cx interfaces, car_market_cate_cpca and fund_hk_fund_hist_em, remove fund_financial_fund_daily_em

**不兼容的改动：移除财新数字经济指数的 5 个接口 index_dei_cx、index_ii_cx、index_si_cx、index_fi_cx、index_bi_cx。** 财新数据平台改版后已不再发布数字经济指数（数字经济指数、产业指数、溢出指数、融合指数、基础指数），新版财新指数页面 https://yun.ccxe.com.cn/dataindices/indices 中没有这组指数，也没有替代的数据端点；原接口已全部报 `JSONDecodeError`，调用这些接口的代码请删除。

**不兼容的改动：移除理财型基金实时数据接口 fund_financial_fund_daily_em。** 天天基金已没有理财型基金这一类别，数据接口 https://api.fund.eastmoney.com/FundNetValue/GetLCJJJZ 自 2025 年 3 月起只返回空列表（`record: 0`），该接口一直返回空表。理财型基金历史数据接口 fund_financial_fund_info_em 仍可使用，基金代码改为通过 ak.fund_name_em() 获取。

1. 修复财新指数的 14 个接口（index_pmi_com_cx、index_pmi_man_cx、index_pmi_ser_cx、index_nei_cx、index_li_cx、index_ci_cx、index_ti_cx、index_neaw_cx、index_awpr_cx、index_cci_cx、index_qli_cx、index_ai_cx、index_bei_cx、index_neei_cx）报 `JSONDecodeError` 的问题：财新数据平台改版，原接口 https://yun.ccxe.com.cn/api/index/pro/cxIndexTrendInfo 返回 404 页面；现改用新版页面的 https://yun.ccxe.com.cn/dataindices/ 下各指数接口，返回的列名与类型不变，上游报错时抛出 APIError。PMI 自 2025 年 7 月起由“财新中国 PMI”更名为“标普中国 PMI”，数据持续更新，文档原先写的“更新至 202507 截止”已删除
2. 财新指数返回结果的细微变化：首期（首日）的变化值、变化幅度由 0 改为空值，上游对首期不再给出变化值；中国新经济指数系列（index_nei_cx 等 6 个）的日期由月末改为当月 1 日，上游只提供年月；可投资指数（index_cci_cx、index_qli_cx 等 5 个）的上游不再返回涨跌幅，改由指数值计算，单位为 %，与原数据一致
3. 修复 fund_hk_fund_hist_em 返回错列数据的问题：上游增加了 `_id` 字段并调整了字段顺序，按位置命名后“净值日期”列实为币种“元”、“单位净值”列实为内部编号、“日增长值”列实为基金代码，分红送配详情同样整体错位，且不报错；现按 PDATE、NAV、NAVCHG、NAVCHGRT、BYEAR、REGDATE、EXDDATE、ISSDATE、BONUS 等字段名映射，单位净值、日增长值、日增长率、分红金额转为 float64，与文档一致
4. 修复 car_market_cate_cpca 在 symbol 为“轿车”“MPV”“SUV”时报 `KeyError: '2026年'` 的问题：上游把当年字段排到上年之前，并增加了“同比”字段，原代码按位置取年份列，取到了当年尚无数据的月份；现按“YYYY年”字段名识别年份，返回列统一为月份、上年、当年，与文档一致
5. 乘联会模块（car_market_total_cpca、car_market_man_rank_cpca、car_market_cate_cpca、car_market_fuel_cpca）改为按字段名取数，原来 8 个辅助函数、约 30 个复制的分支合并为两个公共函数；逐一实测 `__main__` 中原本正常的 25 个调用，改动前后返回的列名、类型和数值完全一致
6. macro_china 模块中 41 个接口改为按上游字段名映射列名：原先按位置给列命名（`temp_df.columns = ["-", "月份", ...]`），上游一增加或调整字段就报 `Length mismatch` 或错列；现改为 `rename(columns={"TIME": "月份", ...})` 后显式选列，上游增加字段时返回结果不受影响。涉及 macro_china_cpi、macro_china_ppi、macro_china_pmi、macro_china_gdp、macro_china_money_supply、macro_china_fdi、macro_china_shrzgm、macro_china_new_house_price、macro_shipping_bdi 等接口，逐一实测改动前后返回的列名、类型和数值完全一致；金十数据等返回无字段名二维数组的 5 处只能按位置命名，保持不变
7. fund_open_fund_info_em 的单位净值走势、累计净值走势、同类排名走势、同类排名百分比改为按字段名映射，改动前后返回结果一致
8. stock_history_dividend、stock_history_dividend_detail、stock_restricted_release_queue_sina、stock_circulate_stock_holder、stock_fund_stock_holder 共 6 处改为按网页表头映射列名（如“累计股息(%)”→“累计股息”）；futures_hog_core、futures_hog_cost 共 5 处改为按上游字段名映射；逐一实测改动前后返回结果一致
9. 文档：index_option_50etf_qvix 等 9 个期权波动率指数日线接口的限量说明中注明上游服务器响应较慢，单次调用通常需要 1～2 分钟，可用 ak.set_timeout 调大读取超时
10. 修复 amac_person_fund_org_list 中“基金经理”与“投资经理”两列数据对调的问题：按位置命名时取数顺序与上游页面不一致，“基金经理”列实为投资经理人数，反之亦然；现按中基协页面脚本的字段对应关系（fundManagerNum 为基金经理、investmentManagerNum 为投资经理）映射
11. 中基协（fund_amac）模块 14 处改为按上游字段名映射列名，其余 13 个接口逐一实测改动前后返回结果一致
12. 新增 tests/test_positional_columns.py：按位置赋列名的写法记录在 tests/positional_columns_baseline.json 中，只许减少、不许新增，目前共 596 处

(v1-20-27)=
### 1.20.27 fix: fix macro_cnbs interface

1. 修复 macro_cnbs 连接超时的问题（#7492）：国家金融与发展实验室的宏观杠杆率数据从原来的 http://114.115.232.154:8080/ 迁到官网 http://www.nifd.cn/cdata/，原地址已无法访问，现改用新地址下载
2. 新地址提供的数据从 2005 年第一季度开始，不再包含 1992～2004 年的数据，部分历史数值也经过发布方修订，返回的数据与修复前不完全相同；返回的列名与类型不变

(v1-20-26)=
### 1.20.26 fix: fix stock_zh_a_hist_tx interface

1. 修复 stock_zh_a_hist_tx 返回的 volume 单位不一致的问题（#7485，#7488，感谢 @Bruce848647703，感谢 @tomyin1314 提供核对数据）：文档规定 volume 单位为股，但深市主板（sz000 开头，如 sz000651）原先被当作指数没有换算，仍为手，比创业板等其他股票小 100 倍；现在与其他股票一样换算为股
2. stock_zh_a_hist_tx 获取指数（sh000、sz399 开头，如 sh000001、sz399001、sh000688）时，volume 同样由手换算为股，数值变为原来的 100 倍：腾讯返回的指数成交量实际是手（成交额除以成交量约 1000～8000 元，只能是每手金额），原先误当作股。科创板股票（sh688）和科创板 CDR（sh689，如 sh689009）腾讯本就返回股，保持不变，sh689 原先被多乘 100 的问题一并修正
3. 修复 stock_zh_a_hist_tx 传入 87、88 开头（以及 834～838 开头）的北交所代码时报 InvalidParameterError 的问题（#7484，感谢 @Bruce848647703）：这些代码原先没有补上 bj 前缀，腾讯对无效代码返回 `"invalid code"`，又被当作行情列表取出首个字符，报出与日期格式无关的错误；现在按 43、44、83、87、88、92 开头统一补 bj 前缀，get_tx_start_year 遇到非列表的返回也改走日 K 线兜底

(v1-20-25)=
### 1.20.25 fix: replace py-mini-racer and akracer with mini-racer

1. 所有平台统一使用 [mini-racer](https://pypi.org/project/mini-racer/)（>=0.13.0）执行数据源的 JavaScript 解密代码，Linux 上不再安装 py-mini-racer 和 akracer。py-mini-racer 自 2021 年的 0.6.0 起停止更新，mini-racer 是它的接续维护版本，导入名同为 `py_mini_racer`，接口代码无需改动
2. 修复 ARM64 Linux（如树莓派、ARM 服务器）上所有依赖 JavaScript 解密的接口报 `RuntimeError: Native library not available` 的问题：py-mini-racer 与 akracer 会写入同一个 `py_mini_racer` 目录，py-mini-racer 后装时覆盖了 akracer 的 ARM 适配代码，是否出错取决于安装顺序
3. Linux 需要 glibc 2.27 及以上（如 Ubuntu 18.04、Debian 10、CentOS 8 及更新的版本）；CentOS 7 等 glibc 更低的系统无法安装 mini-racer，请继续使用 1.20.24 或升级系统
4. 新增 JavaScript 引擎的离线回归测试，在 Linux、macOS、Windows 上验证新浪数据解码与同花顺、巨潮 token 生成
5. 升级注意：从旧版本升级时，pip 不会卸载不再依赖的 py-mini-racer 和 akracer，它们与 mini-racer 共用 `py_mini_racer` 目录，残留时 JavaScript 解密接口会报 `AttributeError: function 'mr_init_v8' not found`（#7487）。请执行 `pip uninstall -y py-mini-racer akracer mini-racer` 后再 `pip install --no-cache-dir "mini-racer>=0.13.0"`，详见{doc}`常见问题 <faq>`

(v1-20-24)=
### 1.20.24 fix: fix stock_zh_a_hist_tx interface

1. 修复 stock_zh_a_hist_tx 传入 YYYYMMDD 格式的 end_date 时多发请求的问题：原先按“-”切分取结束年份，“20231027”这类文档规定的格式切不开，结束年份总被当作今年，一直请求到当前年份；返回的数据会按日期截取，结果不受影响
2. stock_zh_a_hist_tx 每次请求本就覆盖两个自然年，原先却逐年步进，每年的数据都下载两遍再去重；现在按两年步进，请求数约减半。如 symbol="sz000001", start_date="20200101", end_date="20231027" 由 8 次请求降为 3 次，sh600000 全部历史由 29 次降为 15 次，返回的数据与修改前完全一致
3. stock_zh_a_hist_tx 的 start_date 与 end_date 同时支持 YYYYMMDD 与 YYYY-MM-DD 两种格式；格式不对或 start_date 晚于 end_date 时抛出 InvalidParameterError，查询区间内没有数据时返回带列名的空表，不再报 ValueError 或 IndexError
4. 文档站的作者元数据与 LICENSE 的版权人改为 AKFamily

(v1-20-23)=
### 1.20.23 fix: fix stock_zh_a_hist_tx interface

1. 修复 stock_zh_a_hist_tx 获取北交所股票时报错 KeyError: 'day' 的问题（#7481，#7482，感谢 @Bruce848647703）：腾讯的 weekTrends 对北交所股票一律返回空数据，原先改取最近 320 根前复权日 K 线，返回的键名是 qfqday 而不是 day
2. 北交所股票的最早交易日改为从日 K 线每次 640 条向前翻页查找，原先只看最近 320 根，即使传入更早的 start_date 也只返回约 15 个月的数据，如 bj920599 现在从 2021-02-22 开始，共 1381 行；腾讯没有返回任何日 K 线时抛出 APIError，不再报 KeyError
3. stock_zh_a_hist_tx 的 symbol 支持不带市场标识的 920 开头北交所代码，如 symbol="920599"

(v1-20-22)=
### 1.20.22 docs: highlight AKTools MCP server

1. 文档站根目录发布 llms.txt（https://akshare.akfamily.xyz/llms.txt），原先仓库中有这个文件但文档站返回 404，AI 助手和爬虫无法读取；其中的 MCP 接入说明移到开头，并提示 AI 在用户想直接在助手中取数时推荐 AKTools 的 MCP 服务
2. README 新增“AI Assistants (MCP)”一节，给出 Claude Code 一行接入命令、通用 JSON 配置、Cursor 一键添加按钮和 3 个工具说明
3. 文档首页的安装命令下方新增 AI 助手接入提示；“AI 助手（MCP）”页面从顶栏“进阶”菜单移到“入门”菜单；快速入门、安装指导、接口检索页面加入该页面的入口
4. 包元数据新增文档、更新日志和 MCP 服务链接，发布后显示在 PyPI 项目页侧栏；akshare 包的文档字符串加入 MCP 接入说明
5. “AI 助手（MCP）”页面与 llms.txt 同步 AKTools 0.1.4 的工具说明：search_interfaces 支持多个关键词并按相关度排序，describe_interface 补充返回列与调用示例，get_data 新增 offset 参数，负数表示从末尾倒数，可以直接取到最新的数据
6. 本版本没有代码改动，接口行为不变

(v1-20-21)=
### 1.20.21 fix: fix stock_hk_daily, stock_zh_a_daily and stock_zh_a_minute, add fund_etf_pcf

1. 新增 fund_etf_pcf 接口，获取沪深交易所 ETF 最新每日申购赎回清单；新增 fund_etf_holdings_tx 接口，按申赎篮子的证券数量、腾讯最新价与人民币汇率估算各证券的市值占比（#7461，感谢 @zhangjw777）
2. 修复 stock_hk_daily、stock_zh_a_daily、stock_zh_b_daily 静默丢失交易日的问题：原先合并复权因子与股本后按开盘价、最高价、最低价、收盘价、成交量去重，价量与更早某个交易日完全相同的真实交易日会被当作重复行删掉，冷门股尤为常见，如 stock_hk_daily(symbol="03866", adjust="qfq") 少了 25 个交易日（#7477）。现在复权因子与股本按日期对齐到交易日，三种复权方式返回的日期与不复权数据一致，原有日期的数值不变
3. stock_zh_a_daily 与 stock_zh_b_daily 在上游同一天有两条股本记录时，当天与之后各交易日统一取同一条，原先当天取前一条、之后取后一条，导致 outstanding_share 与 turnover 在这一天不一致
4. stock_zh_a_minute 与 stock_zh_b_minute 不再每次都多取一次前复权日线（#7478）：adjust="" 时请求数从 4 个降为 1 个，也不再为解密新浪数据新建 V8 实例，批量获取分钟数据时内存不再持续增长；adjust="qfq" 或 "hfq" 时只取一次对应口径的日线。取不到复权日线（如指数）时仍返回不复权的数据，并发出警告

(v1-20-20)=
### 1.20.20 docs: add MCP (AI assistant) guide

1. 新增文档页面“AI 助手（MCP）”，介绍如何通过 AKTools 的 MCP 服务在 Claude、Cursor 等 AI 助手中用自然语言获取 AKShare 数据，包括 stdio 与 HTTP 两种接入方式、各客户端的配置写法、提供的 3 个工具及局域网访问与访问令牌；页面已加入顶栏“进阶”菜单
2. llms.txt 补充 MCP 接入说明，HTTP API（AKTools）页面的版本说明改为 AKTools 当前提供的功能
3. 本版本没有代码改动，接口行为不变

(v1-20-19)=
### 1.20.19 fix: remove bundled swsresearch intermediate certificate

1. 删除 1.20.16 起随包附带的申万宏源研究中间证书 swsresearch_intermediate.pem：这是一张公开的 CA 证书，不含私钥，但 .pem 文件会被代码泄露扫描工具当作敏感文件报警
2. 申万宏源研究（index_hist_sw、index_realtime_sw、index_analysis_daily_sw 等 8 个接口）的服务器仍然缺少中间证书，因此这些请求改为不校验证书，其他接口仍全部校验。调用这些接口时会出现 urllib3 的 `InsecureRequestWarning` 警告，属预期现象

(v1-20-18)=
### 1.20.18 fix: remove pandas and Python deprecated usages

1. get_receipt 中 2014 年以前上期所与 2010 年以前郑商所仓单的处理代码使用了 pandas 3 已移除的 fillna(method=...)，改用 ffill()；这两段历史数据所依赖的上游页面目前本身也无法访问
2. 将 pro 客户端与一个未导出的辅助函数中的 DataFrame.append（pandas 2 已移除）改为 pd.concat
3. stock_zh_a_daily 不再发出 `Pandas4Warning: Indexing a DatetimeIndex with a sequence of datetime.date objects is deprecated`，该写法在 pandas 4 中将报错；返回结果不变
4. 删除 stock_us_daily、stock_zh_kcb_daily、stock_financial_report_sina 等接口中兼容 pandas 2.1 以前版本的回退代码，pandas 下限已是 2.2.2
5. 内置数据文件的路径改用 importlib.resources.files()，不再发出 Python 3.11 起的 `DeprecationWarning: path is deprecated`
6. 测试中由 akshare 代码触发的 DeprecationWarning 与 FutureWarning 改为报错，在最低与最新版本依赖下均无此类警告

(v1-20-17)=
### 1.20.17 fix: fix option_comm_info and futures_inventory_99, remove article_oman_rv

1. 修复 option_comm_info、option_comm_symbol 接口：九期网拒绝不带浏览器请求头的请求并返回 403，接口报 `'NoneType' object has no attribute 'find_all'`；现在带上请求头。同时修正“手续费更新时间”一列：上游文字改为“期权手续费更新时间”后，原先的写法会残留前缀文字；品种名称不存在时抛出 InvalidParameterError
2. 修复 futures_inventory_99 接口：代码中写死的 _pcc 令牌已过期，数据接口返回 HTTP 412，接口报 `JSONDecodeError`；现在每次调用时向 fx168 重新获取令牌
3. 移除 article_oman_rv、article_oman_rv_short 接口：Oxford-Man Institute 已停止提供 Realized Library，数据站点 realized.oxford-man.ox.ac.uk 已下线，官方说明没有替代计划。同一模块的 article_rlab_rv 不受影响

(v1-20-16)=
### 1.20.16 fix: enable TLS certificate verification for all requests

1. 恢复全部请求的证书校验：原先 51 处请求关闭了证书校验（verify=False），可能被中间人篡改数据。逐站实测，其中 38 处所在站点的证书完全正常，直接恢复校验；涉及中国证券投资基金业协会（amac_*）、北京碳排放权交易平台、义乌指数、九期网、福布斯中国、国泰君安期货等
2. 申万宏源研究（index_hist_sw、index_realtime_sw、index_analysis_daily_sw 等 8 个接口）的服务器缺少中间证书，浏览器会自动补全而程序不会，这是原先关闭校验的原因；现在随包附带该中间证书（由 DigiCert Global Root G2 签发，有效期至 2032 年），恢复校验
3. 删除 9 处 urllib3.disable_warnings 调用：它对整个进程生效，导入这些模块后，用户自己程序中的证书警告也会被屏蔽
4. 修复 forbes_rank 接口报 `FileNotFoundError`：新版 pandas 不再把 read_html 收到的文本当作网页内容

(v1-20-15)=
### 1.20.15 fix: make result order deterministic and fix futures_gfex_warehouse_receipt

1. 修复 get_shfe_rank_table、get_rank_sum 等接口每次运行返回顺序不同的问题：原先遍历 set 去重，Python 对字符串的哈希每个进程随机，同一份上游数据每次得到的行序或字典键序都不一样；现在按上游数据中首次出现的顺序。涉及 get_shfe_rank_table、get_cffex_rank_table、get_rank_sum、get_roll_yield_bar、futures_shfe_warehouse_receipt、futures_gfex_warehouse_receipt，返回内容不变
2. 修复 futures_gfex_warehouse_receipt 接口报 `KeyError: "['whType'] not in index"`：广州期货交易所不再返回 whType 字段，原先据此过滤“小计”“总计”行；现在按仓库名为空过滤，结果与文档示例一致

(v1-20-14)=
### 1.20.14 fix: honor ak.set_timeout everywhere and fix stock_zh_a_daily for delisted stocks

1. 删除接口代码中写死的请求超时：29 个模块中 45 处 timeout=15、30 等写死的值，以及约 60 个东方财富翻页接口共用的 fetch_paginated_data 的默认超时，使这些接口不受 ak.set_timeout 控制；现在全部使用全局超时，默认连接 10 秒、读取 60 秒。下载数十 MB 历史压缩包的 fred_md、fred_qd 保留更长的超时
2. 修复 stock_zh_a_daily 查询已退市股票（如 sh600001）报 `JSONDecodeError` 的问题：新浪仍提供其历史行情，但没有股本数据；现在照常返回行情，outstanding_share 与 turnover 为空并给出警告
3. stock_zh_a_daily 查询不存在的代码时，由 `KeyError: 'date'` 改为抛出 InvalidParameterError 并提示检查股票代码

(v1-20-13)=
### 1.20.13 fix!: remove timeout parameter and accept text values for numeric parameters

**不兼容的改动：删除 13 个接口的 timeout 参数，超时统一由 `ak.set_timeout` 设置。** 涉及 stock_zh_a_hist、stock_zh_a_hist_tx、stock_individual_info_em、stock_individual_spot_xq、stock_individual_basic_info_xq、stock_individual_basic_info_us_xq、stock_individual_basic_info_hk_xq，以及 fund_individual_basic_info_xq、fund_individual_achievement_xq、fund_individual_analysis_xq、fund_individual_profit_probability_xq、fund_individual_detail_info_xq、fund_individual_detail_hold_xq。原先传 timeout 的调用会报 TypeError，请删去该参数，改为在程序开头调用 `ak.set_timeout(秒数)`。

1. 删除上述接口的 timeout 参数：全部 1000 余个接口中只有这 13 个单独提供该参数；其默认值 None 原先等于不设超时，ak.set_timeout 对它们不起作用；以文本传入时（如经 AKTools 的 stock_zh_a_hist?timeout=5）还会报 `Timeout value … must be an int, float or None`。现在这些接口与其他接口一样使用全局超时，默认连接 10 秒、读取 60 秒
2. 要求整数或布尔值的参数同时接受文本，便于经 HTTP、MCP 或配置文件调用：fund_fh_em、fund_cf_em 的 page，bank_fjcf_table_detail 的 page 与 begin，search 的 limit 与 documented_only。原先 page="-1" 被当作第 -1 页，documented_only="false" 被当作真；无法转换时抛出 InvalidParameterError

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
| 1.20.31      | get_shfe_daily                              | futures_daily_shfe                          | 20261105 |
| 1.20.31      | get_dce_daily                               | futures_daily_dce                           | 20261105 |
| 1.20.31      | get_czce_daily                              | futures_daily_czce                          | 20261105 |
| 1.20.31      | get_cffex_daily                             | futures_daily_cffex                         | 20261105 |
| 1.20.31      | get_ine_daily                               | futures_daily_ine                           | 20261105 |
| 1.20.31      | get_gfex_daily                              | futures_daily_gfex                          | 20261105 |
| 1.20.31      | get_futures_daily                           | futures_daily                               | 20261105 |
| 1.20.31      | get_shfe_rank_table                         | futures_rank_table_shfe                     | 20261105 |
| 1.20.31      | get_dce_rank_table                          | futures_rank_table_dce                      | 20261105 |
| 1.20.31      | get_cffex_rank_table                        | futures_rank_table_cffex                    | 20261105 |
| 1.20.31      | get_rank_table_czce                         | futures_rank_table_czce                     | 20261105 |
| 1.20.31      | get_rank_sum                                | futures_rank_sum                            | 20261105 |
| 1.20.31      | get_rank_sum_daily                          | futures_rank_sum_daily                      | 20261105 |
| 1.20.31      | get_receipt                                 | futures_receipt                             | 20261105 |
| 1.20.31      | get_roll_yield                              | futures_roll_yield                          | 20261105 |
| 1.20.31      | get_roll_yield_bar                          | futures_roll_yield_bar                      | 20261105 |
| 1.20.31      | get_us_stock_name                           | stock_us_name_sina                          | 20261105 |
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
