"""
Author: Albert King & Guo Yangyang
date: 2019/12/14 19:54
contact: jindaxiang@163.com
desc: 获取中国证券投资基金业协会-信息公示数据
http://gs.amac.org.cn
"""
import requests
import pandas as pd

from akshare.fund.cons import (
    manager_url,
    manager_payload,
    member_sub_url,
    member_sub_payload,
    fund_info_url,
    fund_info_payload,
    securities_url,
    securities_payload,
    manager_cancelled_url,
    manager_cancelled_payload,
    futures_url,
    futures_payload,
    fund_account_url,
    fund_account_payload,
    fund_sub_url,
    fund_sub_payload,
    aoin_url,
    aoin_payload,
    member_url,
    member_payload,
)


def _get_pages(url="", payload=""):
    """
    获取 中国证券投资基金业协会-信息公示-私募基金管理人公示 页数
    暂时不适用本函数, 直接可以获取所有数据
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
    获取 中国证券投资基金业协会-信息公示-私募基金管理人公示 数据
    """
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.post(url=url, json=payload, headers=headers)  # 请求数据
    res.encoding = "utf-8"
    json_df = res.json()
    return json_df


def amac_member_info():
    """
    中国证券投资基金业协会-信息公示-会员信息公示-会员机构综合查询
    http://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html
    """
    data = get_data(url=member_url, payload=member_payload)
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
        "特俗标注",
    ]
    manager_data_out["入会时间"] = pd.to_datetime(manager_data_out["入会时间"], unit="ms")
    return manager_data_out


def amac_manager_info():
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示-私募基金管理人综合查询
    http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html
    """
    print("正在下载, 由于数据量比较大, 请等待大约 10 秒")
    data = get_data(url=manager_url, payload=manager_payload)
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


def amac_member_sub_info():
    """
    中国证券投资基金业协会-信息公示-私募基金管理人公示-证券公司私募基金子公司管理人信息公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/member/index.html?primaryInvestType=private
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


def amac_fund_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-私募基金管理人基金产品
    http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html
    """
    print("正在下载, 由于数据量比较大, 请等待大约 20 秒")
    data = get_data(url=fund_info_url, payload=fund_info_payload)
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


def amac_securities_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-证券公司集合资管产品公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/securities/index.html
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=securities_url, payload=securities_payload)
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


def amac_aoin_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-证券公司直投基金
    http://gs.amac.org.cn/amac-infodisc/res/aoin/product/index.html
    """
    data = get_data(url=aoin_url, payload=aoin_payload)
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


def amac_fund_sub_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-证券公司私募投资基金
    http://gs.amac.org.cn/amac-infodisc/res/pof/subfund/index.html
    """
    data = get_data(url=fund_sub_url, payload=fund_sub_payload)
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


def amac_fund_account_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-基金公司及子公司集合资管产品公示
    http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=fund_account_url, payload=fund_account_payload)
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


def amac_futures_info():
    """
    中国证券投资基金业协会-信息公示-基金产品公示-期货公司集合资管产品公示
    http://gs.amac.org.cn/amac-infodisc/res/pof/futures/index.html
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=futures_url, payload=futures_payload)
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


def amac_manager_cancelled_info():
    """
    中国证券投资基金业协会-信息公示-诚信信息公示-已注销私募基金管理人名单
    http://gs.amac.org.cn/amac-infodisc/res/cancelled/manager/index.html
    主动注销: 100
    依公告注销: 200
    协会注销: 300
    """
    print("正在下载, 由于数据量比较大, 请等待大约 5 秒")
    data = get_data(url=manager_cancelled_url, payload=manager_cancelled_payload)
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
    manager_df = amac_manager_info()
    print(manager_df)
    member_df = amac_member_sub_info()
    print(member_df)
    fund_df = amac_fund_info()
    print(fund_df)
    securities_df = amac_securities_info()
    print(securities_df)
    manager_cancelled_df = amac_manager_cancelled_info()
    print(manager_cancelled_df)
    futures_df = amac_futures_info()
    print(futures_df)
    fund_account_info_df = amac_fund_account_info()
    print(fund_account_info_df)
    fund_sub_info_df = amac_fund_sub_info()
    print(fund_sub_info_df)
    aoin_info_df = amac_aoin_info()
    print(aoin_info_df)
    amac_member_info_df = amac_member_info()
    print(amac_member_info_df)
    # fund_df[fund_df["建立时间"] > "2019-12-01"].info()
    # fund_df.info()

