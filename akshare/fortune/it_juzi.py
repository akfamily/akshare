# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/25 13:55
Desc: 获取 IT桔子 的死亡公司数据
https://www.itjuzi.com/deathCompany
死亡公司数据库网页声明：
一、本网页基于IT桔子投资数据库而打造的“死亡公司数据库”，致力于展现中国新经济领域近些年倒闭的创新创业公司；
二、“死亡公司数据库”的公司关闭时间是依据公开媒体报道及部分估算，可能会存在些许误差，但我们着力确保更高的可靠性；
三、IT桔子对所收录公司运营状况的判定来源如下：
1、公开媒体报道公司关闭、破产清算的；
2、公司自身在微信、微博等渠道宣布关闭、破产清算的；
3、公司明显经营异常：公司被注销；公司产品比如APP或微信持续6个月及以上没更新；公司因为监管被抓、无法经营……交叉比对后确认没有持续经营。
四、关于一切媒体采用“死亡公司数据库”撰写相关文章报道，媒体需要对使用该信息的结果承担可能的风险或损失，IT桔子不承诺承担连带责任。对于该部分信息，欢迎用户参与和我们一起完善，如果涉及到有真实、可靠、知识产权纠纷的，请与hello@itjuzi.com联系，我们会第一时间做信息的核对与处理；
五、“死亡公司数据库”的公司死亡原因是依据专业数据团队经由数据统计及市场情况综合分析得出；
六、某些关闭公司，可能由于信息收录时间有所延误而未被列入数据库，如有未收录情况请及时联系我们；
七、“死亡公司数据库”欢迎更多的人参与共建，如需对数据纠错或进行其他数据反馈，欢迎随时联系我们。
邮箱：hello@itjuzi.com 微信：itjuzi-radar
"""
import pandas as pd
import requests

from akshare.fortune.cons import it_headers, it_url


def death_company():
    """
    直接读取下载好的文件, 以免给对方服务器造成压力
    此数据更新频率不高！需要大量下载, 请注册会员
    https://www.itjuzi.com/deathCompany
    :return: pandas.DataFrame
    """
    temp_df = pd.read_csv(it_url, index_col=0)
    for i in range(1, 3):
        json_url = (
            f"https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page={i}"
        )
        data_json = requests.get(url=json_url, headers=it_headers).json()
        data_df = data_json["data"]["info"]
        data_df = pd.DataFrame(data_df)
        data_df = data_df[
            [
                "com_name",
                "born",
                "com_change_close_date",
                "live_time",
                "total_money",
                "cat_name",
                "com_prov",
            ]
        ]
        temp_df = temp_df.append(data_df, ignore_index=True)
        temp_df.drop_duplicates(inplace=True)
    return temp_df


def nicorn_company():
    """
    直接读取下载好的文件, 以免给对方服务器造成压力
    此数据更新频率不高！
    https://www.itjuzi.com/deathCompany
    :return: pandas.DataFrame
    """
    temp_df = pd.read_csv(
        "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_juzi/nicorn_company.csv",
        index_col=0,
    )
    for i in range(1, 2):
        json_url = f"https://www.itjuzi.com/api/nicorn?page={i}&com_prov=&cat_id=&order_id=1&com_name="
        data_json = requests.get(url=json_url, headers=it_headers).json()
        data_df = data_json["data"]["data"]
        data_df = pd.DataFrame(data_df)
        temp_df = temp_df.append(data_df, ignore_index=True)
        temp_df.drop_duplicates(inplace=True)
    return temp_df


def maxima_company():
    """
    直接读取下载好的文件, 以免给对方服务器造成压力
    此数据更新频率不高！
    death_df.to_csv("test.csv", encoding="utf-8-sig")  # 注意编码格式
    千里马俱乐部网页声明
    1. 本榜单是基于IT桔子投资数据库而打造的 “千里马俱乐部”，致力于展现中国新经济领域最具成长性和最具价值的未上市创新创业公司；
    2. “千里马俱乐部”上榜公司要求最新估值在10亿人民币-10亿美元之间；新一轮融资额绝大多数是在2000万美元或2亿元人民币以上；
    3. “千里马俱乐部”榜单上的融资估值数据均为估算值，可能会存在些许误差，但我们着力确保更高的可靠性；
    4. 某些估值在10亿人民币-10亿美元的公司，可能由于信息收录时间有所延误而未被列入榜单，如有上述情况请及时联系我们；
    5. “千里马俱乐部”欢迎更多的人参与共建，如需对数据纠错或进行其他数据反馈，欢迎随时联系我们 。
    邮箱：hello@itjuzi.com, 微信公众号：itjuzi521 。
    https://www.itjuzi.com/deathCompany
    :return: pandas.DataFrame
    """
    temp_df = pd.read_csv(
        "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_juzi/maxima.csv",
        index_col=0,
    )
    temp_df.head().append(temp_df.tail())
    for i in range(1, 2):
        json_url = f"https://www.itjuzi.com/api/maxima/?page={i}&com_prov=&cat_id=&order_id=1&com_name="
        data_json = requests.get(url=json_url, headers=it_headers).json()
        data_df = data_json["data"]["data"]
        data_df = pd.DataFrame(data_df)
        temp_df = temp_df.append(data_df, ignore_index=True)
        temp_df.drop_duplicates(inplace=True)
    return temp_df


def _death_company():
    """
    获取 IT桔子 的死亡公司数据
    https://www.itjuzi.com/deathCompany
    :return: pandas.DataFrame
    """
    page_num_url = (
        "https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page=1"
    )
    data_json = requests.get(url=page_num_url, headers=it_headers).json()
    num_page_int = data_json["data"]["page"]["total"]
    for i in range(1, int(num_page_int / 10) + 1):
        print(i)
        json_url = (
            f"https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page={i}"
        )
        data_json = requests.get(url=json_url, headers=it_headers).json()
        data_df = data_json["data"]["info"]
        data_df = pd.DataFrame(data_df)
        data_df = data_df[
            [
                "com_name",
                "born",
                "com_change_close_date",
                "live_time",
                "total_money",
                "cat_name",
                "com_prov",
            ]
        ]
        # data_df.to_csv(os.path.join(r"C:\Users\king\Desktop\juzi", str(i)+".csv"))
    return data_df


if __name__ == "__main__":
    death_company_df = death_company()
    print(death_company_df)
    nicorn_company_df = nicorn_company()
    print(nicorn_company_df)
    maxima_company_df = maxima_company()
    print(maxima_company_df)
