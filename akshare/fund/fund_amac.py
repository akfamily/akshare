"""
Date: 2020/01/16 19:54
Desc: 获取中国证券投资基金业协会-信息公示数据
中国证券投资基金业协会-新版: http://gs.amac.org.cn
中国证券投资基金业协会-旧版: http://www1.amac.org.cn/
目前的网络数据采集基于旧版接口, Guo Yangyang 正在更新新版接口数据
接口目录设计按照 http://gs.amac.org.cn/ 来设计, 已经整理完该页面所有接口
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.fund.cons import (
    amac_member_info_url,
    amac_member_info_payload,
    amac_person_org_list_url,
    amac_person_org_list_payload,
    amac_person_org_list_ext_url,
    amac_person_org_list_ext_payload,
    amac_manager_info_url,
    amac_manager_info_payload,
    amac_manager_classify_info_url,
    amac_manager_classify_info_payload,
    member_sub_url,
    member_sub_payload,
    amac_fund_info_url,
    amac_fund_info_payload,
    amac_securities_info_url,
    amac_securities_info_payload,
    amac_aoin_info_url,
    amac_aoin_info_payload,
    amac_fund_sub_info_url,
    amac_fund_sub_info_payload,
    amac_fund_account_info_url,
    amac_fund_account_info_payload,
    amac_fund_abs_url,
    amac_fund_abs_payload,
    amac_futures_info_url,
    amac_futures_info_payload,
    amac_manager_cancelled_info_url,
    amac_manager_cancelled_info_payload,
)


def _get_pages(url="", payload=""):
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示 页数
    暂时不使用本函数, 直接可以获取所有数据
    """
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.post(url=url, json=payload, headers=headers)  # 请求数据
    res.encoding = "utf-8"
    json_df = res.json()
    return json_df["totalPages"]


def get_data(url="", payload=""):
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示
    """
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.post(url=url, json=payload, headers=headers)  # 请求数据
    res.encoding = "utf-8"
    json_df = res.json()
    return json_df


# 中国证券投资基金业协会-信息公示-会员信息
# 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
def amac_member_info():
    """
    中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
    http://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html
    :return: 会员机构综合查询
    :rtype: pandas.DataFrame
    """
    data = get_data(url=amac_member_info_url, payload=amac_member_info_payload)
    need_data = data["content"]
    keys_list = [
        "managerName",
        "memberBehalf",
        "memberType",
        "memberCode",
        "memberDate",
        "primaryInvestType",
        "markStar",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "机构（会员）名称",
        "会员代表",
        "会员类型",
        "会员编号",
        "入会时间",
        "机构类型",
        "是否星标",
    ]
    manager_data_out["入会时间"] = pd.to_datetime(manager_data_out["入会时间"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-从业人员信息
# 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
def amac_person_org_list():
    """
    中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
    http://gs.amac.org.cn/amac-infodisc/res/pof/person/personOrgList.html
    :return:
    :rtype: pandas.DataFrame
    """
    data = get_data(url=amac_person_org_list_url, payload=amac_person_org_list_payload)
    need_data = data["content"]
    keys_list = [
        "orgName",
        "workerTotalNum",
        "operNum",
        "salesmanNum",
        "investmentManagerNum",
        "fundManagerNum",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "机构名称",
        "员工人数",
        "基金从业资格",
        "基金销售业务资格",
        "基金经理",
        "投资经理",
    ]
    return manager_data_out


# 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册外部公示信息
def amac_person_org_list_ext():
    """
    中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册外部公示信息
    http://gs.amac.org.cn/amac-infodisc/res/pof/extperson/extPersonOrgList.html
    :return:
    :rtype: pandas.DataFrame
    """
    data = get_data(url=amac_person_org_list_ext_url, payload=amac_person_org_list_ext_payload)
    need_data = data["content"]
    keys_list = [
        "orgName",
        "orgType",
        "extWorkerTotalNum",
        "extOperNum",
        "extSalesmanNum",
        "extInvestmentManagerNum",
        "extFundManagerNum",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "机构名称",
        "机构性质",
        "员工人数",
        "基金从业资格",
        "基金销售业务资格",
        "基金经理",
        "投资经理",
    ]
    return manager_data_out


# 中国证券投资基金业协会-信息公示-私募基金管理人公示
# 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
def amac_manager_info():
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
    http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("Please waiting for about 10 seconds")
    data = get_data(url=amac_manager_info_url, payload=amac_manager_info_payload)
    need_data = data["content"]
    keys_list = [
        "managerName",
        "artificialPersonName",
        "primaryInvestType",
        "registerProvince",
        "registerNo",
        "establishDate",
        "registerDate",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "私募基金管理人名称",
        "法定代表人/执行事务合伙人(委派代表)姓名",
        "机构类型",
        "注册地",
        "登记编号",
        "成立时间",
        "登记时间",
    ]
    manager_data_out["成立时间"] = pd.to_datetime(manager_data_out["成立时间"], unit="ms")
    manager_data_out["登记时间"] = pd.to_datetime(manager_data_out["登记时间"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
def amac_manager_classify_info():
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 10 秒")
    data = get_data(url=amac_manager_classify_info_url, payload=amac_manager_classify_info_payload)
    need_data = data["content"]
    keys_list = [
        "managerName",
        "artificialPersonName",
        "primaryInvestType",
        "registerProvince",
        "registerNo",
        "establishDate",
        "registerDate",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "私募基金管理人名称",
        "法定代表人/执行事务合伙人(委派代表)姓名",
        "机构类型",
        "注册地",
        "登记编号",
        "成立时间",
        "登记时间",
    ]
    manager_data_out["成立时间"] = pd.to_datetime(manager_data_out["成立时间"], unit="ms")
    manager_data_out["登记时间"] = pd.to_datetime(manager_data_out["登记时间"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
def amac_member_sub_info():
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html?primaryInvestType=private
    :return:
    :rtype: pandas.DataFrame
    """
    data = get_data(url=member_sub_url, payload=member_sub_payload)
    need_data = data["content"]
    keys_list = [
        "managerName",
        "memberBehalf",
        "memberType",
        "memberCode",
        "memberDate",
        "primaryInvestType",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "机构（会员）名称",
        "会员代表",
        "会员类型",
        "会员编号",
        "入会时间",
        "公司类型",
    ]
    manager_data_out["入会时间"] = pd.to_datetime(manager_data_out["入会时间"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品
# 中国证券投资基金业协会-信息公示-基金产品-私募基金管理人基金产品
def amac_fund_info():
    """
    中国证券投资基金业协会-信息公示-基金产品-私募基金管理人基金产品
    http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 20 秒")
    data = get_data(url=amac_fund_info_url, payload=amac_fund_info_payload)
    need_data = data["content"]
    keys_list = [
        "fundName",
        "managerName",
        "managerType",
        "workingState",
        "putOnRecordDate",
        "establishDate",
        "mandatorName",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "基金名称",
        "私募基金管理人名称",
        "私募基金管理人类型",
        "运行状态",
        "备案时间",
        "建立时间",
        "托管人名称",
    ]
    manager_data_out["建立时间"] = pd.to_datetime(manager_data_out["建立时间"], unit="ms")
    manager_data_out["备案时间"] = pd.to_datetime(manager_data_out["备案时间"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品-证券公司集合资管产品公示
def amac_securities_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-证券公司集合资管产品公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/securities/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=amac_securities_info_url, payload=amac_securities_info_payload)
    need_data = data["content"]
    keys_list = [
        "cpmc",
        "cpbm",
        "gljg",
        "slrq",
        "dqr",
        "tzlx",
        "sffj",
        "tgjg",
        "barq",
        "yzzt",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "产品名称",
        "产品编码",
        "管理人名称",
        "成立日期",
        "到期时间",
        "投资类型",
        "是否分级",
        "托管人名称",
        "备案日期",
        "运作状态",
    ]
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品-证券公司直投基金
def amac_aoin_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-证券公司直投基金
    http://gs.amac.org.cn/amac-infodisc/res/aoin/product/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    data = get_data(url=amac_aoin_info_url, payload=amac_aoin_info_payload)
    need_data = data["content"]
    keys_list = [
        "code",
        "name",
        "aoinName",
        "managerName",
        "createDate",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "产品编码",
        "产品名称",
        "直投子公司",
        "管理机构",
        "设立日期",
    ]
    manager_data_out["设立日期"] = pd.to_datetime(manager_data_out["设立日期"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
def amac_fund_sub_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
    http://gs.amac.org.cn/amac-infodisc/res/pof/subfund/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    data = get_data(url=amac_fund_sub_info_url, payload=amac_fund_sub_info_payload)
    need_data = data["content"]
    keys_list = [
        "productCode",
        "productName",
        "mgrName",
        "trustee",
        "foundDate",
        "registeredDate",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "产品编码",
        "产品名称",
        "私募基金管理人名称",
        "托管人名称",
        "成立日期",
        "备案日期",
    ]
    manager_data_out["备案日期"] = pd.to_datetime(manager_data_out["备案日期"], unit="ms")
    manager_data_out["成立日期"] = pd.to_datetime(manager_data_out["成立日期"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
def amac_fund_account_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
    http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=amac_fund_account_info_url, payload=amac_fund_account_info_payload)
    need_data = data["content"]
    keys_list = [
        "registerDate",
        "registerCode",
        "name",
        "manager",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "成立日期",
        "产品编码",
        "产品名称",
        "管理人名称",
    ]
    manager_data_out["成立日期"] = pd.to_datetime(manager_data_out["成立日期"], unit="ms")
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品公示-资产支持专项计划
def amac_fund_abs():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-资产支持专项计划
    http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = requests.post(url=amac_fund_abs_url, data=amac_fund_abs_payload)
    need_data = data.json()["result"]
    keys_list = [
        "ASPI_BA_NUMBER",
        "ASPI_NAME",
        "ASPI_GL_NAME",
        "AII_TGR",
        "AT_AUDIT_DATE",
        "ASPI_SURE_FILE_NAME",
        "ASPI_SURE_FILE_PATH",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "备案编号",
        "专项计划全称",
        "管理人",
        "托管人",
        "备案通过时间",
        "备案函名称",
        "备案函下载地址",
    ]
    manager_data_out["备案通过时间"] = pd.to_datetime(manager_data_out["备案通过时间"])
    return manager_data_out


# 中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
def amac_futures_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/futures/index.html
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=amac_futures_info_url, payload=amac_futures_info_payload)
    need_data = data["content"]
    keys_list = [
        "mpiName",
        "mpiProductCode",
        "aoiName",
        "mpiTrustee",
        "mpiCreateDate",
        "tzlx",
        "sfjgh",
        "registeredDate",
        "dueDate",
        "fundStatus",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "产品名称",
        "产品编码",
        "管理人名称",
        "托管人名称",
        "成立日期",
        "投资类型",
        "是否分级",
        "备案日期",
        "到期日",
        "运作状态",
    ]
    return manager_data_out


# 中国证券投资基金业协会-信息公示-诚信信息
# 中国证券投资基金业协会-信息公示-诚信信息-违反自律规则黑名单
def amac_manager_xxgs_hmd():
    """
    中国证券投资基金业协会-信息公示-诚信信息-违反自律规则黑名单
    http://www1.amac.org.cn/xxgs/hmd/
    :return:
    :rtype: pandas.DataFrame
    """
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.get("http://www1.amac.org.cn/xxgs/hmd/", headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    content_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("a")]
    date_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("div", attrs={"class": "newsDate"})]
    manager_data_out = pd.DataFrame([date_list, content_list]).T
    return manager_data_out.iloc[:-1, :]


# 中国证券投资基金业协会-信息公示-诚信信息-纪律处分
def amac_manager_xxgs_jlcf():
    """
    中国证券投资基金业协会-信息公示-诚信信息-纪律处分
    http://www1.amac.org.cn/xxgs/jlcf/
    :return:
    :rtype: pandas.DataFrame
    """
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.get("http://www1.amac.org.cn/xxgs/jlcf/index.shtml", headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    page_num = soup.find(attrs={"onclick": "_PageBar_1574932671465_Go()"}).parent.get_text().split("/")[-1].split('页')[0]
    content_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("a")]
    date_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("div", attrs={"class": "newsDate"})]
    manager_data_out = pd.DataFrame([date_list, content_list]).T
    manager_data_out = manager_data_out.iloc[:-4, :]
    for page in range(1, int(page_num)):
        res = requests.get(f"http://www1.amac.org.cn/xxgs/jlcf/index_{page}.shtml", headers=headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "lxml")
        content_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("a")]
        date_list = [item.get_text() for item in
                     soup.find("div", attrs={"class": "iRight"}).find_all("div", attrs={"class": "newsDate"})]
        inner_manager_data_out = pd.DataFrame([date_list, content_list]).T
        inner_manager_data_out = inner_manager_data_out.iloc[:-4, :]
        manager_data_out = manager_data_out.append(inner_manager_data_out, ignore_index=True)
    return manager_data_out


# 中国证券投资基金业协会-信息公示-诚信信息-撤销管理人登记的名单
def amac_manager_xxgs_cxdj():
    """
    中国证券投资基金业协会-信息公示-诚信信息-撤销管理人登记的名单
    http://www1.amac.org.cn/xxgs/cxdj/
    :return:
    :rtype: pandas.DataFrame
    """
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.get("http://www1.amac.org.cn/xxgs/cxdj/", headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    content_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("a")]
    date_list = [item.get_text() for item in soup.find("div", attrs={"class": "iRight"}).find_all("div", attrs={"class": "newsDate"})]
    manager_data_out = pd.DataFrame([date_list, content_list]).T
    manager_data_out = manager_data_out.iloc[:-1, :]
    return manager_data_out


# 中国证券投资基金业协会-信息公示-诚信信息-已注销私募基金管理人名单
def amac_manager_cancelled_info():
    """
    中国证券投资基金业协会-信息公示-诚信信息公示-已注销私募基金管理人名单
    http://gs.amac.org.cn/amac-infodisc/res/cancelled/manager/index.html
    主动注销: 100
    依公告注销: 200
    协会注销: 300
    :return:
    :rtype: pandas.DataFrame
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=amac_manager_cancelled_info_url, payload=amac_manager_cancelled_info_payload)
    need_data = data["content"]
    keys_list = [
        "orgName",
        "orgCode",
        "orgSignDate",
        "cancelDate",
        "status",
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame(need_data)
    manager_data_out = manager_data_out[keys_list]
    manager_data_out.columns = [
        "管理人名称",
        "统一社会信用代码",
        "登记时间",
        "注销时间",
        "注销类型",
    ]
    return manager_data_out


if __name__ == "__main__":
    # 中国证券投资基金业协会-信息公示-会员信息
    # 中国证券投资基金业协会-信息公示-会员信息-会员机构综合查询
    amac_member_info_df = amac_member_info()
    print(amac_member_info_df)

    # 中国证券投资基金业协会-信息公示-从业人员信息
    # 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册信息
    amac_person_org_list_df = amac_person_org_list()
    print(amac_person_org_list_df)
    # 中国证券投资基金业协会-信息公示-从业人员信息-基金从业人员资格注册外部公示信息
    amac_person_org_list_ext_df = amac_person_org_list_ext()
    print(amac_person_org_list_ext_df)

    # 中国证券投资基金业协会-信息公示-私募基金管理人公示
    # 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
    amac_manager_info_df = amac_manager_info()
    print(amac_manager_info_df)
    # 中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人分类公示
    amac_manager_classify_info_df = amac_manager_classify_info()
    print(amac_manager_classify_info_df)
    # 中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
    amac_member_sub_info_df = amac_member_sub_info()
    print(amac_member_sub_info_df)

    # 中国证券投资基金业协会-信息公示-基金产品
    # 中国证券投资基金业协会-信息公示-基金产品-私募基金管理人基金产品
    amac_fund_info_df = amac_fund_info()
    print(amac_fund_info_df)
    example_df = amac_fund_info_df[amac_fund_info_df["私募基金管理人名称"].str.contains("聚宽")]
    print(example_df)
    # 中国证券投资基金业协会-信息公示-基金产品-证券公司集合资管产品公示
    amac_securities_info_df = amac_securities_info()
    print(amac_securities_info_df)
    # 中国证券投资基金业协会-信息公示-基金产品-证券公司直投基金
    amac_aoin_info_df = amac_aoin_info()
    print(amac_aoin_info_df)
    # 中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
    amac_fund_sub_info_df = amac_fund_sub_info()
    print(amac_fund_sub_info_df)
    # 中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
    amac_fund_account_info_df = amac_fund_account_info()
    print(amac_fund_account_info_df)
    # 中国证券投资基金业协会-信息公示-基金产品公示-资产支持专项计划
    amac_fund_abs_df = amac_fund_abs()
    print(amac_fund_abs_df)
    # 中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
    amac_futures_info_df = amac_futures_info()
    print(amac_futures_info_df)

    # 中国证券投资基金业协会-信息公示-诚信信息
    # 中国证券投资基金业协会-信息公示-诚信信息-违反自律规则黑名单
    amac_manager_xxgs_hmd_df = amac_manager_xxgs_hmd()
    print(amac_manager_xxgs_hmd_df)
    # 中国证券投资基金业协会-信息公示-诚信信息-纪律处分
    amac_manager_xxgs_jlcf_df = amac_manager_xxgs_jlcf()
    print(amac_manager_xxgs_jlcf_df)
    # 中国证券投资基金业协会-信息公示-诚信信息-撤销管理人登记的名单
    amac_manager_xxgs_cxdj_df = amac_manager_xxgs_cxdj()
    print(amac_manager_xxgs_cxdj_df)
    # 中国证券投资基金业协会-信息公示-诚信信息-已注销私募基金管理人名单
    amac_manager_cancelled_info_df = amac_manager_cancelled_info()
    print(amac_manager_cancelled_info_df)
