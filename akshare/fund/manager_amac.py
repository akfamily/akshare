"""
Author: Guo Yangyang
date: 2019/12/14 19:54
contact: guoyangyang_1994@163.com
desc:
获取中国证券投资基金业协会-信息公示-私募基金管理人公示
http://gs.amac.org.cn
"""
from operator import itemgetter
import requests
import pandas as pd
import time


def get_data():
    """
    获取 中国证券投资基金业协会-信息公示-私募基金管理人公示 数据
    """
    manager_url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.1906342132667007&page=0&size=50000'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
    }
    res = requests.post(url=manager_url, json=payload, headers=headers)  # 请求数据
    res.encoding = "utf-8"
    json_df = res.json()
    return json_df


def amac_manager_info(update=False):
    """
    处理 中国证券投资基金业协会-信息公示-私募基金管理人公示 数据
    """
    if not update:
        return pd.read_csv("https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_amac/amac.csv", index_col=0)
    data = get_data()
    need_data = data["content"]

    keys_list = [
        'managerName',
        'artificialPersonName',
        'primaryInvestType',
        'registerProvince',
        'registerNo',
        'establishDate',
        'registerDate'
    ]  # 定义要取的 value 的 keys
    manager_data_out = pd.DataFrame()
    # 根据keys取出所有的data
    for i in range(len(need_data)):
        manager_data = itemgetter(*keys_list)(need_data[i])
        manager_data = pd.DataFrame(manager_data).T
        manager_data.columns = ['私募基金管理人名称',
                                '法定代表人/执行事务合伙人(委派代表)姓名',
                                '机构类型',
                                '注册地',
                                '登记编号',
                                '成立时间',
                                '登记时间']
        manager_data_out = manager_data_out.append(manager_data, ignore_index=True)

    # 将时间戳转换为"XXXX-XX-XX"形式
    manager_data_out['成立时间'] = list(map(lambda y: time.strftime("%Y-%m-%d", y),
                                        map(lambda x: time.localtime(x), manager_data_out['成立时间'] / 1000)))
    manager_data_out['登记时间'] = list(map(lambda y: time.strftime("%Y-%m-%d", y),
                                        map(lambda x: time.localtime(x), manager_data_out['登记时间'] / 1000)))
    return manager_data_out


if __name__ == "__main__":
    manager_df = amac_manager_info(update=False)
    print(manager_df.columns)
