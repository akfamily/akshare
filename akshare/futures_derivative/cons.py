# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/27 19:49
Desc: 期货衍生指标配置文件
交易法门-数据
西本新干线-指数数据
"""
# 交易法门-数据-农产品
# 交易法门-数据-农产品-美豆
jyfm_data_usa_bean_name_url_dict = {
    "美豆种植进度": "https://www.jiaoyifamen.com/data/usa-bean-grow/grow",
    "美豆出苗率": "https://www.jiaoyifamen.com/data/usa-bean-emergence/ratio",
    "美豆开花率": "https://www.jiaoyifamen.com/data/usa-bean-flower/ratio",
    "美豆优良率": "https://www.jiaoyifamen.com/data/usa-bean-good/ratio",
    "美豆收割进度": "https://www.jiaoyifamen.com/data/usa-bean-harvest/ratio",
    "美豆出口情况": "https://www.jiaoyifamen.com/data/usa-bean-export/ratio",
}

# 交易法门-数据-农产品-豆粕
jyfm_data_soybean_meal_name_url_dict = {
    "大豆月度进口": "https://www.jiaoyifamen.com/data/soybean-meal-month-import/import",
    "大豆原料库存": "https://www.jiaoyifamen.com/data/soybean-meal-ingredient-stock/stock",
    "压榨开工率": "https://www.jiaoyifamen.com/data/soybean-meal-operate-ratio/ratio",
    "企业压榨利润": "https://www.jiaoyifamen.com/data/soybean-meal-profit/profit",
    "豆粕月度产量": "https://www.jiaoyifamen.com/data/soybean-meal-month-product/product",
    "豆粕每日成交": "https://www.jiaoyifamen.com/data/soybean-meal-profit/profit",
    "豆粕周度库存": "https://www.jiaoyifamen.com/data/soybean-meal-week-stock/stock",
    "豆粕平衡表": "https://www.jiaoyifamen.com/data/soybean-meal-balance/balance",
}

# 交易法门-数据-农产品-豆油
jyfm_data_soybean_oil_name_url_dict = {
    "豆油年度产能": "https://www.jiaoyifamen.com/data/soybean-oil-year-produce/produce",
    "压榨装置开工率": "https://www.jiaoyifamen.com/data/soybean-oil-operate-ratio/ratio",
    "油厂周度产量": "https://www.jiaoyifamen.com/data/soybean-oil-week-produce/produce",
    "豆油现货成交": "https://www.jiaoyifamen.com/data/soybean-oil-day-deal/deal",
    "豆油商业库存": "https://www.jiaoyifamen.com/data/soybean-oil-week-stock/stock",
    "豆油毛利润": "https://www.jiaoyifamen.com/data/soybean-oil-gross-profit/profit",
    "豆油月度产量": "https://www.jiaoyifamen.com/data/soybean-oil-month-data/data",  # 获取相应数据
    "豆油月度进口": "https://www.jiaoyifamen.com/data/soybean-oil-month-data/data",  # 获取相应数据
    "豆油月度消费": "https://www.jiaoyifamen.com/data/soybean-oil-month-data/data",  # 获取相应数据
    "豆油月度出口": "https://www.jiaoyifamen.com/data/soybean-oil-month-data/data",  # 获取相应数据
    "豆油月度库存": "https://www.jiaoyifamen.com/data/soybean-oil-month-data/data",  # 获取相应数据
}

# 交易法门-数据-农产品-棕榈
jyfm_data_palm_name_url_dict = {
    "马棕种植面积": "https://www.jiaoyifamen.com/data/palm-grow-area/grow",
    "马棕FFB单产": "https://www.jiaoyifamen.com/data/palm-f-f-b-product/product",
    "马棕出油率": "https://www.jiaoyifamen.com/data/palm-yield/yield",
    "马棕月度产量": "https://www.jiaoyifamen.com/data/palm-month-product/product",
    "马棕月度库存": "https://www.jiaoyifamen.com/data/palm-month-stock/stock",
    "马棕月度出口": "https://www.jiaoyifamen.com/data/palm-month-export/export",
}

# 交易法门-数据-农产品-白糖
jyfm_data_sugar_name_url_dict = {
    "国内种植面积": "https://www.jiaoyifamen.com/data/sugar-year-grow-area/grow",
    "年度产糖率": "https://www.jiaoyifamen.com/data/sugar-year-yield/yield",
    "白糖年度产销": "https://www.jiaoyifamen.com/data/sugar-year-data/produce",
    "白糖进出口量": "https://www.jiaoyifamen.com/data/sugar-year-data/trade",
    "食糖产需缺口": "https://www.jiaoyifamen.com/data/sugar-year-data/gap",
    "白糖月度产量": "https://www.jiaoyifamen.com/data/sugar-month-data/produce?category=1",
    "白糖月度销量": "https://www.jiaoyifamen.com/data/sugar-month-data/produce?category=2",
    "白糖月度进口": "https://www.jiaoyifamen.com/data/sugar-month-trade/trade",
    "食糖工业库存": "https://www.jiaoyifamen.com/data/sugar-month-stock/stock",
    "白糖产区库存": "https://www.jiaoyifamen.com/data/sugar-year-stock/stock",
}

# 交易法门-数据-黑色系
# 交易法门-数据-黑色系-焦煤
jyfm_data_cocking_coal_url_dict = {
    "焦煤总库存": "https://www.jiaoyifamen.com/data/cocking-coal-total-stock/stock",
    "焦煤焦企库存-焦煤焦企库存100": "https://www.jiaoyifamen.com/data/cocking-coal100-cocking-stock/stock",
    "焦煤焦企库存-焦煤焦企库存230": "https://www.jiaoyifamen.com/data/cocking-coal230-cocking-stock/stock",
    "焦煤钢厂库存": "https://www.jiaoyifamen.com/data/cocking-coal-steel-stock/stock",
    "焦煤港口库存": "https://www.jiaoyifamen.com/data/cocking-coal-port-stock/stock",
}
# 交易法门-数据-黑色系-焦炭
jyfm_data_coke_url_dict = {
    "焦企产能利用率-100家独立焦企产能利用率": "https://www.jiaoyifamen.com/data/coke100-availability-ratio/ratio",
    "焦企产能利用率-230家独立焦企产能利用率": "https://www.jiaoyifamen.com/data/coke230-availability-ratio/ratio",
    "焦炭日均产量-100家独立焦企焦炭日均产量": "https://www.jiaoyifamen.com/data/coke100-day-produce/produce",
    "焦炭日均产量-230家独立焦企焦炭日均产量": "https://www.jiaoyifamen.com/data/coke230-day-produce/produce",
    "焦炭总库存": "https://www.jiaoyifamen.com/data/coke-total-stock/stock",
    "焦炭焦企库存-100家独立焦企焦炭库存": "https://www.jiaoyifamen.com/data/coke100-cocking-stock/stock",
    "焦炭焦企库存-230家独立焦企焦炭库存": "https://www.jiaoyifamen.com/data/coke230-cocking-stock/stock",
    "焦炭钢厂库存": "https://www.jiaoyifamen.com/data/coke-steel-stock/stock",
    "焦炭港口库存": "https://www.jiaoyifamen.com/data/coke-port-stock/stock",
    "焦企焦化利润": "https://www.jiaoyifamen.com/data/coke-coking-profit/profit",
}


# 交易法门-登录
jyfm_init_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept-Encoding": "gzip, deflate, br",
                     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                     "Host": "www.jiaoyifamen.com",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
                     }
jyfm_login_url = "https://www.jiaoyifamen.com/login"

# xgx
symbol_dict = {
    '钢材指数': '65',
    '铁矿指数': '61',
    '焦炭指数': '64',
    '煤炭指数': '1002',
    '水泥指数': '1003',
    'FTZ指数': '1100',
    '钢铁行业PMI指数': '118',
    '生产指数': '119',
    '新订单指数': '120',
    '新出口订单指数': '121',
    '产成品库存指数': '122',
    '原材料库存指数': '123',
    '沪市终端线螺每周采购量监控': '74',
    '沪螺纹钢社会库存': '72',
    '国内螺纹钢社会库存量': '67',
    '国内线材社会库存量': '68',
    '国内主要城市热轧卷板库存': '69',
    '国内主要城市冷轧卷板库存': '70',
    '国内主要城市中厚板库存': '73',
    '全国主要钢材品种库存总量': '117',
    '热轧价格走势': '108',
    '冷轧价格走势': '109',
    '中板价格走势': '110',
    '型材价格走势': '111',
    '沪二级螺纹钢价格走势': '127',
    '螺纹钢主力合约收盘价格': '179',
    '铁矿石主力合约收盘价格': '180',
    '热轧板卷主力合约收盘价格': '181',
    '焦煤主力合约收盘价格': '182',
    '焦炭主力合约收盘价格': '183',
    '存款基准利率': '52',
    '贷款基准利率': '53',
    '存款准备金率': '105',
    '人民币新增贷款（亿元）': '174',
    '广义货币供应量增速（M2，%）': '175',
    '狭义货币供应量增速（M1，%)': '176',
    '上海大额银行承兑汇票(Ⅰ)': '129',
    '上海大额银行承兑汇票(Ⅱ)': '130',
    '上海大额银行承兑汇票(Ⅲ)': '131',
    '上海大额商业承兑汇票(Ⅰ)': '132',
    '上海大额商业承兑汇票(II)': '133',
    '上海大额商业承兑汇票(III)': '134',
    '重点企业粗钢日均产量（旬报）': '99',
    '重点企业钢材库存量（旬报）': '124',
    '国内月度粗钢日均产量': '159',
    '国内月度粗钢产量': '35',
    '国内月度钢材产量': '88',
    '国内月度螺纹钢产量': '40',
    '国内月度线材产量': '41',
    '国内月度热轧板卷产量': '114',
    '国内月度冷轧板卷产量': '115',
    '国内月度中厚板产量': '116',
    '国内月度生铁产量': '177',
    '国内月度焦炭产量': '37',
    '国内月度铁矿石原矿产量': '36',
    '国内月度铁矿石进口量': '42',
    '国内月度钢材出口量': '38',
    '国内月度钢材进口量': '39',
    '国内铁矿石港口存量': '43',
    '唐山地区钢坯库存量': '161',
    '印度矿港口库存': '100',
    '波罗的海干散货指数（BDI）': '77',
    '废钢价格走势': '78',
    '钢坯价格走势': '79',
    '钢材成本指数': '178',
    '铁矿石进口月度均价': '93',
    '巴西图巴朗-北仑铁矿海运价': '94',
    '西澳-北仑铁矿海运价': '95',
    '澳大利亚粉矿价格（56.5%，日照港）': '1006',
    '澳大利亚粉矿价格(61.5%青岛港，元/吨）': '106',
    '巴西粉矿价格（ 65% 日照港，元/吨）': '107',
    '62%铁矿石指数': '125',
    '63.5%印度粉矿外盘报价': '126',
    '国民生产总值季度增速（GDP）': '166',
    '居民消费物价指数（CPI）': '30',
    '工业生产者出厂价格指数（PPI）': '165',
    '制造业采购经理指数（PMI）': '104',
    '月度建筑安装工程投资额': '91',
    '月度固定资产投资额': '32',
    '月度房地产建设投资额': '34',
    '城填固定资产投资增速（累计值，%）': '171',
    '房地产开发投资增速（累计值，%）': '167',
    '土地购置面积同比增速（累计值，%）': '168',
    '房屋新开工面积同比增速（累计值，%）': '169',
    '商品房销售面积同比增速（累计值，%）': '170',
    '钢铁业固定资产投资增速（累计值，%）': '172',
    'CRU全球': '80',
    'CRU长材': '81',
    'CRU扁平材': '82',
    'CRU北美': '83',
    'CRU欧洲': '84',
    'CRU亚洲': '85',
    '全球粗钢月度产量（万吨）': '162',
    '全球粗钢日均产量（万吨）': '163',
    '全球粗钢产能利用率（%）': '164'}

xgx_code_url = "http://www.96369.net/Other/ValidateCode.aspx"
xgx_main_url = "http://www.96369.net/indices/{}"
xgx_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "57",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "www.96369.net",
    "Origin": "http://www.96369.net",
    "Pragma": "no-cache",
    "Referer": "http://www.96369.net/indices/67",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
xgx_short_headers = {
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.96369.net",
    "Pragma": "no-cache",
    "Referer": "http://www.96369.net/indices/67",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
# csa
csa_params_url = "https://www.jiaoyifamen.com/tools/nav/spread"
csa_url_spread = "https://www.jiaoyifamen.com/tools/future/spread/free"
csa_url_ratio = "https://www.jiaoyifamen.com/tools/future/valence/free"
csa_url_customize = "https://www.jiaoyifamen.com/tools/future/customize"

csa_payload = {
    "type1": "RB",
    "code1": "01",
    "type2": "RB",
    "code2": "05"
}
