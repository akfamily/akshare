# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/9/30 13:58
Desc: 基金配置文件
"""
# 中国证券投资基金业协会-信息公示-会员信息
# 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
amac_member_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/pofMember?rand=0.29121896744980824&page=0&size=10000"
amac_member_info_payload = {}

# 中国证券投资基金业协会-信息公示-从业人员信息
# 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
amac_person_org_list_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/personOrg?rand=0.29990518236199226&page=0&size=30000"
amac_person_org_list_payload = {"page": "1"}

# 中国证券投资基金业协会-信息公示-私募基金管理人公示
# 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
amac_manager_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.1906342132667007&page=0&size=30000"
amac_manager_info_payload = {}

# 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
amac_manager_classify_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.15042461260592477&page=0&size=30000"
amac_manager_classify_info_payload = {}

# 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
member_sub_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/pofMember?rand=0.7268765057523581&page=0&size=1000"
member_sub_payload = {"primaryInvestType": ["证券公司私募基金子公司"]}

# 中国证券投资基金业协会-信息公示-基金产品
# 中国证券投资基金业协会-信息公示-基金产品-私募基金管理人基金产品
amac_fund_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.4453771335054344&page=0&size=150000"
amac_fund_info_payload = {}

# 中国证券投资基金业协会-信息公示-基金产品-证券公司集合资管产品公示
amac_securities_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/securities?rand=0.37635501241756697&page=0&size=10000"
amac_securities_info_payload = {}

# 中国证券投资基金业协会-信息公示-基金产品-证券公司直投基金
amac_aoin_info_url = "https://gs.amac.org.cn/amac-infodisc/api/aoin/product?rand=0.8658543297539962&page=0&size=2000"
amac_aoin_info_payload = {}

# 中国证券投资基金业协会-信息公示-基金产品-证券公司私募投资基金
amac_fund_sub_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/subfund?rand=0.8256678186283957&page=0&size=2000"
amac_fund_sub_info_payload = {}

# 中国证券投资基金业协会-信息公示-基金产品-基金公司及子公司集合资管产品公示
amac_fund_account_info_url = "https://gs.amac.org.cn/amac-infodisc/api/fund/account?rand=0.7087855351461467&page=0&size=50000"
amac_fund_account_info_payload = {}

# 中国证券投资基金业协会-信息公示-基金产品-资产支持专项计划
amac_fund_abs_url = "http://ba.amac.org.cn/pages/amacWeb/ab-special-plan!list.action"
amac_fund_abs_payload = {
    "filter_LIKES_ASPI_NAME": "",
    "filter_GES_AT_AUDIT_DATE": "",
    "filter_LES_AT_AUDIT_DATE": "",
    "page.searchFileName": "publicity_abs_web",
    "page.sqlKey": "PAGE_ABS_PUBLICITY_WEB",
    "page.sqlCKey": "SIZE_ABS_PUBLICITY_WEB",
    "_search": "false",
    "nd": "1579177295346",
    "page.pageSize": "5000",
    "page.pageNo": "1",
    "page.orderBy": "ASPI_ID",
    "page.order": "desc",
}

# 中国证券投资基金业协会-信息公示-基金产品-期货公司集合资管产品公示
amac_futures_info_url = "https://gs.amac.org.cn/amac-infodisc/api/pof/futures?rand=0.7131945361451304&page=0&size=10000"
amac_futures_info_payload = {}

# 中国证券投资基金业协会-信息公示-诚信信息公示-已注销私募基金管理人名单
amac_manager_cancelled_info_url = "https://gs.amac.org.cn/amac-infodisc/api/cancelled/manager?rand=0.5044834416392225&page=0&size=20000"
amac_manager_cancelled_info_payload = {}

# 智道智科
zdzk_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=DDA2557CBF1FADE7F285F4D0DDE75CAB",
    "Host": "www.ziasset.com",
    "Referer": "https://www.ziasset.com/DataServices",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
}

code_name_map_dict = {
    "1": "商品综合",
    "2": "中债新综合",
    "15": "沪深300",
    "28": "智道私募综合指数",
    "30": "智道股票策略指数",
    "32": "智道管理期货指数",
    "34": "智道固定收益指数",
    "36": "智道相对价值指数",
    "38": "智道复合策略指数",
    "40": "智道北京区域指数",
    "42": "智道上海区域指数",
    "44": "智道广州区域指数",
    "46": "智道深圳区域指数",
    "48": "智道浙江区域指数",
}
