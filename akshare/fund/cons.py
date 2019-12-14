# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 基金配置文件
"""
# amac
manager_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.1906342132667007&page=0&size=30000"
manager_payload = {}

member_sub_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/pofMember?rand=0.7268765057523581&page=0&size=1000"
member_sub_payload = {"primaryInvestType": ["证券公司私募基金子公司"]}

fund_info_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.4453771335054344&page=0&size=150000"
fund_info_payload = {}

manager_cancelled_url = "http://gs.amac.org.cn/amac-infodisc/api/cancelled/manager?rand=0.5044834416392225&page=0&size=20000"
manager_cancelled_payload = {}

# 证券公司集合资管产品公示
securities_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/securities?rand=0.37635501241756697&page=0&size=10000"
securities_payload = {}

# 期货公司集合资管产品公示
futures_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/futures?rand=0.7131945361451304&page=0&size=10000"
futures_payload = {}

# 基金公司及子公司集合资管产品公示
fund_account_url = "http://gs.amac.org.cn/amac-infodisc/api/fund/account?rand=0.7087855351461467&page=0&size=50000"
fund_account_payload = {}

# 证券公司私募投资基金
fund_sub_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/subfund?rand=0.8256678186283957&page=0&size=2000"
fund_sub_payload = {}

# 证券公司直投基金
aoin_url = "http://gs.amac.org.cn/amac-infodisc/api/aoin/product?rand=0.8658543297539962&page=0&size=2000"
aoin_payload = {}

# 会员机构综合查询
member_url = "http://gs.amac.org.cn/amac-infodisc/api/pof/pofMember?rand=0.29121896744980824&page=0&size=10000"
member_payload = {}


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
