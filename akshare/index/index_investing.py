# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/17 0:50
Desc: 英为财情-股票指数-全球股指与期货指数数据接口
https://cn.investing.com/indices/volatility-s-p-500-historical-data
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers

pd.set_option("mode.chained_assignment", None)


def _get_global_country_name_url() -> dict:
    """
    获取可获得指数数据国家对应的 URL
    :return: dict
    {'中国': '/indices/china-indices',
    '丹麦': '/indices/denmark-indices',
    '乌克兰': '/indices/ukraine-indices',
    '乌干达': '/indices/uganda-indices',
    '以色列': '/indices/israeli-indices',
    '伊拉克': '/indices/iraq-indices',
    '俄罗斯': '/indices/russia-indices',
    '保加利亚': '/indices/bulgaria-indices',
    '克罗地亚': '/indices/croatia-indices',
    '冰岛': '/indices/iceland-indices',
    '加拿大': '/indices/canada-indices',
    '匈牙利': '/indices/hungary-indices',
    '南非': '/indices/south-africa-indices',
    '博茨瓦纳': '/indices/botswana-indices',
    '卡塔尔': '/indices/qatar-indices',
    '卢旺达': '/indices/rwanda-indices',
    '卢森堡': '/indices/luxembourg-indices',
    '印度': '/indices/india-indices',
    '印度尼西亚': '/indices/indonesia-indices',
    '厄瓜多尔': '/indices/ecuador-indices',
    '台湾': '/indices/taiwan-indices',
    '哈萨克斯坦': '/indices/kazakhstan-indices',
    '哥伦比亚': '/indices/colombia-indices',
    '哥斯达黎加': '/indices/costa-rica-indices',
    '土耳其': '/indices/turkey-indices',
    '坦桑尼亚': '/indices/tanzania-indices',
    '埃及': '/indices/egypt-indices',
    '塞尔维亚': '/indices/serbia-indices',
    '塞浦路斯': '/indices/cyprus-indices',
    '墨西哥': '/indices/mexico-indices',
    '奥地利': '/indices/austria-indices',
    '委内瑞拉': '/indices/venezuela-indices',
    '孟加拉国': '/indices/bangladesh-indices',
    '尼日利亚': '/indices/nigeria-indices',
    '巴勒斯坦领土': '/indices/palestine-indices',
    '巴基斯坦': '/indices/pakistan-indices',
    '巴林': '/indices/bahrain-indices',
    '巴西': '/indices/brazil-indices',
    '希腊': '/indices/greece-indices',
    '德国': '/indices/germany-indices',
    '意大利': '/indices/italy-indices',
    '拉脱维亚': '/indices/latvia-indices',
    '挪威': '/indices/norway-indices',
    '捷克': '/indices/czech-republic-indices',
    '摩洛哥': '/indices/morocco-indices',
    '斯洛伐克': '/indices/slovakia-indices',
    '斯洛文尼亚': '/indices/slovenia-indices',
    '斯里兰卡': '/indices/sri-lanka-indices',
    '新加坡': '/indices/singapore-indices',
    '新西兰': '/indices/new-zealand-indices',
    '日本': '/indices/japan-indices',
    '智利': '/indices/chile-indices',
    '比利时': '/indices/belgium-indices',
    '毛里求斯': '/indices/mauritius-indices',
    '沙特阿拉伯': '/indices/saudi-arabia-indices',
    '法国': '/indices/france-indices',
    '波兰': '/indices/poland-indices',
    '波黑': '/indices/bosnia-indices',
    '泰国': '/indices/thailand-indices',
    '津巴布韦': '/indices/zimbabwe-indices',
    '澳大利亚': '/indices/australia-indices',
    '爱尔兰': '/indices/ireland-indices',
    '爱沙尼亚': '/indices/estonia-indices',
    '牙买加': '/indices/jamaica-indices',
    '瑞典': '/indices/sweden-indices',
    '瑞士': '/indices/switzerland-indices',
    '科威特': '/indices/kuwaiti-indices',
    '科特迪亚': '/indices/ivory-coast-indices',
    '秘鲁': '/indices/peru-indices',
    '突尼斯': '/indices/tunisia-indices',
    '立陶宛': '/indices/lithuania-indices',
    '约旦': '/indices/jordan-indices',
    '纳米比亚': '/indices/namibia-indices',
    '罗马尼亚': '/indices/romania-indices',
    '美国': '/indices/usa-indices',
    '肯尼亚': '/indices/kenya-indices',
    '芬兰': '/indices/finland-indices',
    '英国': '/indices/uk-indices',
    '荷兰': '/indices/netherlands-indices',
    '菲律宾': '/indices/philippines-indices',
    '葡萄牙': '/indices/portugal-indices',
    '蒙古': '/indices/mongolia-indices',
    '西班牙': '/indices/spain-indices',
    '赞比亚': '/indices/zambia-indices',
    '越南': '/indices/vietnam-indices',
    '阿拉伯联合酋长国': '/indices/dubai-indices',
    '阿曼': '/indices/oman-indices',
    '阿根廷': '/indices/argentina-indices',
    '韩国': '/indices/south-korea-indices',
    '香港': '/indices/hong-kong-indices',
    '马尔他': '/indices/malta-indices',
    '马拉维': '/indices/malawi-indices',
    '马来西亚': '/indices/malaysia-indices',
    '黎巴嫩': '/indices/lebanon-indices',
    '黑山': '/indices/montenegro-indices'}
    """
    url = "https://cn.investing.com/indices/"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    name_url_option_list = soup.find("select", attrs={"name": "country"}).find_all(
        "option"
    )[
        1:
    ]  # 去掉-所有国家及地区
    url_list = [item["value"] for item in name_url_option_list]
    name_list = [item.get_text() for item in name_url_option_list]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def index_investing_global_country_name_url(country: str = "中国") -> dict:
    """
    参考网页: https://cn.investing.com/indices/
    获取选择国家对应的: 主要指数, 主要行业, 附加指数, 其他指数
    :param country: str 中文国家名称, 对应 get_global_country_name_url 函数返回的国家名称
    :return: dict
     {'上证指数': '/indices/shanghai-composite', '深证成指': '/indices/szse-component', '上证100': '/indices/sse-100',
     'A股指数': '/indices/shanghai-se-a-share', '中信标普300': '/indices/s-p-citic300', '中信标普50': '/indices/s-p-citic50',
     '富时中国A50指数': '/indices/ftse-china-a50', '上证消费': '/indices/sse-consumer-staples',
     '上证信息': '/indices/sse-information-technology', '上证公用': '/indices/sse-utilities',
     '上证医药': '/indices/sse-health-care', '上证材料': '/indices/sse-materials',
     '上证可选': '/indices/sse-consumer-discretionary', '上证商品': '/indices/sse-commodity-equity',
     '上证工业': '/indices/sse-industrials', '上证新兴': '/indices/sse-emerging-industries',
     '上证电信': '/indices/sse-telecommunication-services', '综合指数': '/indices/sse-misc-sub', '上证能源': '/indices/sse-energy',
     '上证资源': '/indices/sse-natural-resource', '上证金融': '/indices/sse-financials',
     '上证银行': '/indices/sse-banks-total-return', '餐饮指数': '/indices/szse-hotel---catering',
     'IT指数': '/indices/szse-information-technology', '创业板50': '/indices/szse-chinext-50',
     '制造指数': '/indices/szse-manufacturing', '商务指数': '/indices/szse-business-service',
     '富时中国A600一般零售商': '/indices/ftse-china-general-retailers',
     '富时中国A600产油设备 - 相关服务和分销': '/indices/ftse-china-oil-eq-ser.---dist.',
     '富时中国A600人寿保险': '/indices/ftse-china-life-insurance', '富时中国A600公用事业': '/indices/ftse-china-utilities',
     '富时中国A600天然气、水和多用途设施': '/indices/ftse-china-gas---water-utilities', '富时中国A600媒体': '/indices/ftse-china-media',
     '富时中国A600房地产投资与服务': '/indices/ftse-china-reit---services', '富时中国A600旅游和休闲': '/indices/ftse-china-travel---leisure',
     '富时中国A600电信服务': '/indices/ftse-china-telecommunications', '富时中国A600电力': '/indices/ftse-china-electricity',
     '富时中国A600科技': '/indices/ftse-china-technology', '富时中国A600科技硬件和设备': '/indices/ftse-china-tech-hardware---eq',
     '富时中国A600移动电信服务': '/indices/ftse-china-mobile', '富时中国A600软件和计算机服务': '/indices/ftse-china-soft.---com.-services',
     '富时中国A600金融': '/indices/ftse-china-financials', '富时中国A600银行': '/indices/ftse-china-banks',
     '富时中国蓝筹价值100': '/indices/ftse-china-blue-chip-value-100', '建筑指数': '/indices/szse-construction',
     '地产指数': '/indices/sse-property-sub', '批零指数': '/indices/szse-wholesale---retail', '文化指数': '/indices/szse-media',
     '新综指': '/indices/sse-new-comp', '深证上游': '/indices/szse-upstream-industry',
     '深证下游': '/indices/szse-downstream-industry', '深证中游': '/indices/szse-midstream-industry',
     '深证消费': '/indices/szse-consumer-staples', '深证信息': '/indices/szse-technology', '深证公用': '/indices/szse-utilities',
     '深证农业': '/indices/szse-agriculture', '深医药50': '/indices/szse-health-care-50', '深证医药': '/indices/szse-health-care',
     '深证材料': '/indices/szse-materials', '深证可选': '/indices/szse-consumer-discretionary',
     '深证大宗': '/indices/szse-commodities-producer', '深证央企': '/indices/szse-central-company',
     '深证工业': '/indices/szse-industrials', '深证文化': '/indices/szse-culture',
     '深证民营': '/indices/szse-individual-businesses-price', '深消费50': '/indices/szse-consumer-50',
     '深证环保': '/indices/szse-environmental-protection', '深证电信': '/indices/szse-telecom',
     '深证绩效': '/indices/szse-performance', '深证能源': '/indices/szse-energy', '深证时钟': '/indices/szse-investment-clock',
     '深证龙头': '/indices/szse-industry-top', '深证装备': '/indices/szse-equipment-manufacturing',
     '深证责任': '/indices/szse-responsibility-price', '深证金融': '/indices/szse-financials',
     '深防御50': '/indices/szse-defensive-50', '科研指数': '/indices/szse-research---development',
     '综企指数': '/indices/szse-conglomerates', '运输指数': '/indices/szse-transportation', '采矿指数': '/indices/szse-mining',
     '5年信用': '/indices/sse-5-year-credit-bond', '企债指数': '/indices/shanghai-se-corporate-bond',
     '沪企债30': '/indices/sse-cb-30', '信用100': '/indices/sse-credit-bond-100', '沪公司债': '/indices/sse-enterprise-bond',
     '上证转债': '/indices/sse-convertible-bond', '国债指数': '/indices/shanghai-se-treasury-bond',
     '治理指数': '/indices/sse-corporate-governance', '沪投资品': '/indices/sse-investment-commodity',
     '沪消费品': '/indices/sse-consumer-commodity', '富时中国A600一般工业行业指数': '/indices/ftse-china-600-general-industrials',
     '富时中国A600一般金融行业指数': '/indices/ftse-china-600-financial-services',
     '富时中国A600个人消费品行业指数': '/indices/ftse-china-a-600-personal-goods',
     '富时中国A600制药和生物科技行业指数': '/indices/ftse-china-600-pharma---biotech',
     '富时中国A600化工制品行业指数': '/indices/ftse-china-a-600-chemicals',
     '富时中国A600卫生保健行业指数': '/indices/ftse-china-a-600--health-care',
     '富时中国A600基础材料行业指数': '/indices/ftse-china-a-600-basic-materials',
     '富时中国A600家庭用品行业指数': '/indices/ft-china-600-hous.goods---textiles',
     '富时中国A600家庭用品及住宅建筑行业指数': '/indices/ftse-china-a-600-household-goods',
     '富时中国A600工业行业指数': '/indices/ftse-china-a-600-industrials',
     '富时中国A600工业工程行业指数': '/indices/ftse-china-600-ind.-engineering',
     '富时中国A600工业金属和矿业行业指数': '/indices/ftse-china-a-600-industrial-metal',
     '富时中国A600建筑和材料行业指数': '/indices/ft-china-600-cons.---materials',
     '富时中国A600替代能源行业指数': '/indices/ftse-china-a-600-altenative-energy',
     '富时中国A600林业和造纸行业指数': '/indices/ftse-china-a-600-forestry---paper',
     '富时中国A600汽车和零件行业指数': '/indices/ftse-china-600-automobile---parts',
     '富时中国A600消费服务行业指数': '/indices/ftse-china-a-600-consumer-services',
     '富时中国A600生活消费品行业指数': '/indices/ftse-china-a-600-consumer-goods',
     '富时中国A600电子和电器设备行业指数': '/indices/ftse-china-600-elec.---elec.eq',
     '富时中国A600石油和天然气行业指数': '/indices/ftse-china-a-600-oil---gas',
     '富时中国A600石油和天然气生产商行业指数': '/indices/ftse-china-600-oil---gas-producers',
     '富时中国A600航天航空和国航行业指数': '/indices/ftse-china-600-aerospace---defence',
     '富时中国A600辅助服务行业指数': '/indices/ftse-china-a-600-support-services',
     '富时中国A600运输行业指数': '/indices/ftse-china-a-600-industrial-trans.',
     '富时中国A600采矿行业指数': '/indices/ftse-china-a-600-mining',
     '富时中国A600食品和药物零售行业指数': '/indices/ftse-china-600-food---drug-ret.',
     '富时中国A600食品生产商行业指数': '/indices/ftse-china-a-600-food-producers',
     '富时中国A600饮料行业指数': '/indices/ftse-china-a-600-beverages', '上证150': '/indices/sse-150',
     '180运输': '/indices/sse-180-transportation', '180价值': '/indices/sse180-value', '180低贝': '/indices/sse-180-low-beta',
     '180治理': '/indices/sse-180-corporate-governance', '180动态': '/indices/sse-180-dynamic',
     '180基建': '/indices/sse-180-infrastructure', '180基本': '/indices/sse-180-fundamental-weighted',
     '180成长': '/indices/sse180-growth', '上证180': '/indices/shanghai-se-180',
     '180波动': '/indices/sse-180-volatility-weighted', '180R价值': '/indices/sse180-relative-value',
     '180R成长': '/indices/sse180-relative-growth', '180稳定': '/indices/sse-180-stability',
     '180等权': '/indices/sse-180-equal-weight', '180红利': '/indices/sse-180-dividend',
     '180资源': '/indices/sse-180-natural-resource', '180金融': '/indices/shanghai-se-180-financial',
     '180高贝': '/indices/sse-180-high-beta', '380消费': '/indices/sse-380-consumer-staples',
     '380价值': '/indices/sse-380-value', '380低贝': '/indices/sse-380-low-beta',
     '380信息': '/indices/sse-380-information-technology', '380公用': '/indices/sse-380-utilities',
     '380动态': '/indices/sse-380-dynamic', '380医药': '/indices/sse-380-health-care',
     '380材料': '/indices/sse-380-materials', '380可选': '/indices/sse-380-consumer-discretionary',
     '380基本': '/indices/sse-380-fundamental-weighted', '380工业': '/indices/sse-380-industrials',
     '380成长': '/indices/sse-380-growth', '上证380': '/indices/sse-380', '380波动': '/indices/sse-380-volatility-weighted',
     '380电信': '/indices/sse-380-telecommunication-services', '380R价值': '/indices/sse-380-relative-value',
     '380R成长': '/indices/sse-380-relative-growth', '380稳定': '/indices/sse-380-stability',
     '380等权': '/indices/sse-380-equal-weight', '380红利': '/indices/sse-380-dividend', '380能源': '/indices/sse-380-energy',
     '380金融': '/indices/sse-380-financials', '380高贝': '/indices/sse-380-high-beta',
     '50基本': '/indices/sse-50-fundamental-weighted', '上证50': '/indices/shanghai-se-50',
     '50等权': '/indices/sse-50-equal-weight', 'B股指数': '/indices/shanghai-se-b-share',
     '上证上游': '/indices/sse-upstream-industry', '上证下游': '/indices/sse-downstream-industry',
     '中型综指': '/indices/sse-medium-enterprise-composite', '上证央企': '/indices/sse-central-state-owned-enterprises',
     '上证中小': '/indices/sse-mid-small-cap', '上证中游': '/indices/sse-midstream-industry', '上证中盘': '/indices/sse-midcap',
     '消费等权': '/indices/sse-consumer-staples-equal-weight', '优势制造': '/indices/sse-select-manufacturing-industries',
     '优势消费': '/indices/sse-select-consumption-industries', '优势资源': '/indices/sse-select-resources-industries',
     '信息等权': '/indices/sse-information-technology-equal-we', '全指价值': '/indices/sse-large-mid-small-cap-value',
     '全指成长': '/indices/sse-large-mid-small-cap-growth', '全R价值': '/indices/sse-large-mid-small-cap-relative-va',
     '全R成长': '/indices/sse-large-mid-small-cap-relative-gr', '公用等权': '/indices/sse-utilities-equal-weight',
     '公用指数': '/indices/sse-utility-sub', '农业主题': '/indices/sse-agriculture-theme',
     '医药主题': '/indices/sse-health-care-theme', '医药等权': '/indices/sse-health-care-equal-weight',
     '材料等权': '/indices/sse-materials-equal-weight', '持续产业': '/indices/sse-sustainable-development-industr',
     '可选等权': '/indices/sse-consumer-discretionary-equal-we', '上证周期': '/indices/sse-cyclical-industry-50',
     '商业指数': '/indices/sse-commercial-sub', '上证国企': '/indices/sse-state-owned-enterprises-100',
     '上国红利': '/indices/sse-state-owned-enterprises-dividen', '上证地企': '/indices/sse-local-state-owned-enterprises-5',
     '上证F200': '/indices/ssef-200', '上证F300': '/indices/ssef-300', '上证F500': '/indices/ssef-500',
     '上证全指': '/indices/sse-large-mid-small-cap', '上证小盘': '/indices/sse-smallcap', '工业指数': '/indices/sse-industrial-sub',
     '工业等权': '/indices/sse-industrials-equal-weight', '市值百强': '/indices/sse-market-value-top-100',
     '上证民企': '/indices/sse-private-owned-enterprises-50', '上民红利': '/indices/sse-private-owned-enterprises-divid',
     '上证沪企': '/indices/sse-shanghai-enterprises', '上证流通': '/indices/sse-free-float',
     '上证海外': '/indices/sse-overseas-listing-a-share', '消费50': '/indices/sse-consumer-50',
     '消费80': '/indices/sse-consumer-80', '消费领先': '/indices/sse-leading-consumption-and-service',
     '上证环保': '/indices/sse-environmental-protection-indust', '电信等权': '/indices/sse-telecommunication-services-equa',
     '责任指数': '/indices/sse-social-responsibility', '红利指数': '/indices/sse-dividend',
     '能源等权': '/indices/sse-energy-equal-weight', '沪财中小': '/indices/sse-wealth-mid-small',
     '资源50': '/indices/sse-resource-50', '超大盘': '/indices/sse-mega-cap', '金融等权': '/indices/sse-financials-equal-weight',
     '非周期': '/indices/sse-non-cyclical-industry-100', '上证高新': '/indices/sse-high-and-new-technology-enterpr',
     '高端装备': '/indices/sse-high-end-equipment-manufacturin', '上证龙头': '/indices/sse-industry-top',
     '中信标普企业债指数': '/indices/citic-corp-bond', '中创EW': '/indices/szse-sme-chinext-100-equal-weighted',
     '中创低波': '/indices/szse-500-low-volatility', '中创高贝': '/indices/szse-500-high-beta',
     '中创高新': '/indices/szse-sme-chinext-hnte', '中小低波': '/indices/szse-sme-low-volatility',
     '中小高贝': '/indices/szse-sme-high-beta', '中创100': '/indices/sme-chinext-100-price',
     '中创100R': '/indices/sme-chinext-100-trn', '中创400': '/indices/sme-chinext-400',
     '中创500': '/indices/sme-chinext-500', '中小基础': '/indices/szse-sme-prime-market',
     '中小价值': '/indices/sme-300-value-price', '中小成长': '/indices/sme-300-growth-price',
     '中小300': '/indices/szse-sme-300-price', '中创价值': '/indices/sme-chinext-value',
     '中创成长': '/indices/sme-chinext-growth', 'SME创新': '/indices/szse-sme-price',
     '中小新兴': '/indices/szse-sme-strategic-emerging-industr', '中小板R': '/indices/szse-sme-return',
     '中小绩效': '/indices/szse-sme-performance-weighted', '中小治理': '/indices/szse-sme-corp-governance',
     '中小板EW': '/indices/szse-sme-equal-weight', '中小红利': '/indices/szse-sme-dividend',
     '中小板综': '/indices/szse-sme-composite', '中小责任': '/indices/szse-sme-csr', '创业300': '/indices/szse-chinext-300',
     '创业板V': '/indices/chinext-300-value', '创业板G': '/indices/chinext-300-growth',
     '创业基础': '/indices/szse-chinext-prime-market', '创业新兴': '/indices/szse-chinext-strategic-emerging-ind',
     '创业板指': '/indices/chinext-price', '创业板R': '/indices/chinext-return', '创业板EW': '/indices/szse-chinext-equal-weight',
     '创业板综': '/indices/chinext-composite', '科技100': '/indices/sme-chinext-tec-100-price',
     '富时Shariah中国指数': '/indices/ftse-shariah-china', '富时中国H股指数': '/indices/ftse-china-h-share',
     '富时中国指数': '/indices/ftse-china', '富时价值股份中国指数': '/indices/ftse-value-stocks-china',
     '富时大中华指数': '/indices/ftse-greater-china', '富时大中华指数全指': '/indices/ftse-greater-china-all-cap',
     '沪深300': '/indices/csi300', '深报指数': '/indices/szse-press', '深报综指': '/indices/szse-press-composite',
     '1000价值': '/indices/szse-1000-value', '1000成长': '/indices/szse-1000-growth', '深证1000': '/indices/szse-1000',
     '100低波': '/indices/szse-100-low-volatility', '深证100': '/indices/szse-100-price', '深证100R': '/indices/szse-100',
     '深100EW': '/indices/szse-100-equal-weight', '100绩效': '/indices/szse-100-performance-weighted',
     '深证200': '/indices/szse-200', '深证价值': '/indices/szse-300-value-price', '深证300': '/indices/szse-300-price',
     '深证低波': '/indices/szse-300-low-volatility', '深证成长': '/indices/szse-300-growth-price',
     '深证300R': '/indices/szse-300', '深300EW': '/indices/szse-300-equal-weight',
     '300绩效': '/indices/szse-300-performance-weighted', '深证高贝': '/indices/szse-300-high-beta',
     '700价值': '/indices/szse-700-value', '700成长': '/indices/szse-700-growth', '深证700': '/indices/szse-700',
     '深证A指': '/indices/szse-a-share', '深证B指': '/indices/szse-b-share', '深证GDP': '/indices/szse-gdp-100',
     '深证创新': '/indices/szse-innovation-price', '深周期50': '/indices/szse-cyclical-50', '深证F120': '/indices/szfi-120',
     '深证F200': '/indices/szfi-200', '深证F60': '/indices/szfi-60', '成份B指': '/indices/szse-b-share-sub',
     '深成指R': '/indices/szse-a-share-sub', '深成指EW': '/indices/szse-component-equal-weighted',
     '成长40': '/indices/szse-growth-price', '深证新兴': '/indices/szse-strategic-emerging-industries',
     '新指数': '/indices/szse-new', '深证治理': '/indices/szse-corp-governance-price', 'TMT50': '/indices/szse-tmt50-price',
     '深证红利': '/indices/szse-dividend-price', '深证综指': '/indices/szse-composite'}
    """
    name_url_dict = _get_global_country_name_url()
    url = f"https://cn.investing.com{name_url_dict[country]}?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    url_list = [
        item.find("a")["href"] for item in soup.find_all(attrs={"class": "plusIconTd"})
    ]
    name_list = [
        item.find("a").get_text()
        for item in soup.find_all(attrs={"class": "plusIconTd"})
    ]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def index_investing_global(
    country: str = "台湾",
    index_name: str = "台湾加权指数",
    period: str = "每日",
    start_date: str = "2000-01-01",
    end_date: str = "2019-10-17",
) -> pd.DataFrame:
    """
    获得具体国家的具体指数的从 start_date 到 end_date 期间的数据
    :param country: 对应函数中的国家名称
    :type country: str
    :param index_name: 对应函数中的指数名称
    :type index_name: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: '2000-01-01', 注意格式
    :type start_date: str
    :param end_date: '2019-10-17', 注意格式
    :type end_date: str
    :return: 指定参数的数据
    :rtype: pandas.DataFrame
    深证战略性新兴产业指数历史数据
    0              日期        收盘        开盘         高         低     交易量   百分比变化
    1     2019年10月16日  1,692.60  1,695.38  1,708.59  1,691.39   4.65B  -0.01%
    2     2019年10月15日  1,692.79  1,712.84  1,712.84  1,691.32   5.41B  -1.45%
    3     2019年10月14日  1,717.74  1,713.70  1,726.25  1,710.30   5.99B   1.30%
    4     2019年10月11日  1,695.62  1,695.28  1,703.79  1,680.60   5.15B   0.24%
    5     2019年10月10日  1,691.63  1,664.54  1,693.21  1,660.60   5.36B   1.68%
               ...       ...       ...       ...       ...     ...     ...
    1647    2013年1月7日    914.17    901.32    914.17    899.97  18.97K   1.45%
    1648    2013年1月4日    901.11    917.44    918.90    893.13  17.70K  -1.02%
    1649  2012年12月31日    910.43    902.72    910.43    900.62  15.90K   1.11%
    1650  2012年12月28日    900.42    892.72    900.42    888.62  13.82K   0.88%
    1651  2012年12月27日    892.59    901.97    905.57    891.83  17.55K  -0.76%
    """
    start_date = start_date.replace("-", "/")
    end_date = end_date.replace("-", "/")
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    name_code_dict = index_investing_global_country_name_url(country)
    temp_url = f"https://cn.investing.com/{name_code_dict[index_name]}-historical-data"
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find_all(text=re.compile("window.histDataExcessInfo"))[0].strip()
    para_data = re.findall(r"\d+", data)
    payload = {
        "curr_id": para_data[0],
        "smlID": para_data[1],
        "header": title,
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": period_map[period],
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    res = requests.post(url, data=payload, headers=long_headers)
    df_data = pd.read_html(res.text)[0]
    if period == "每月":
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月")
    else:
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    if any(df_data["交易量"].astype(str).str.contains("-")):
        df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][
            df_data["交易量"].str.contains("-")
        ].replace("-", 0)
    if any(df_data["交易量"].astype(str).str.contains("B")):
        df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)]
            .str.replace("B", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000000
        )
    if any(df_data["交易量"].astype(str).str.contains("M")):
        df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)]
            .str.replace("M", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000
        )
    if any(df_data["交易量"].astype(str).str.contains("K")):
        df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)]
            .str.replace("K", "")
            .str.replace(",", "")
            .astype(float)
            * 1000
        )
    df_data["交易量"] = df_data["交易量"].astype(float)
    df_data = df_data[["收盘", "开盘", "高", "低", "交易量"]]
    df_data = df_data.astype(float)
    return df_data


if __name__ == "__main__":
    index_investing_global_country_name_url_dict = index_investing_global_country_name_url("美国")
    index_investing_global_df = index_investing_global(
        country="美国",
        index_name="美元指数",
        period="每日",
        start_date="2005-01-01",
        end_date="2020-10-11",
    )
    print(index_investing_global_df)
