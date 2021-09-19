# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/6/30 15:55
Desc: 获取 IT桔子 的死亡公司数据、千里马和独角兽
https://www.itjuzi.com/deathCompany
https://www.itjuzi.com/chollima
https://www.itjuzi.com/unicorn
"""
import pandas as pd
import requests
from tqdm import tqdm


def death_company() -> pd.DataFrame:
    """
    IT桔子-死亡公司名单
    https://www.itjuzi.com/deathCompany
    :return: 死亡公司名单
    :rtype: pandas.DataFrame
    """
    temp_df = pd.read_csv(
        "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_juzi/juzi.csv"
    )
    for page in tqdm(range(1, 3)):
        url = "https://www.itjuzi.com/api/closure"
        params = {"com_prov": "", "sort": "", "page": page, "keyword": "", "cat_id": ""}
        r = requests.get(
            url, params=params
        )  # 如果需要更新此数据，请增加请求头，请求头中必须包括 Authorization 字段
        data_json = r.json()
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
        temp_df.drop_duplicates(inplace=True, ignore_index=True)
    temp_df.reset_index(inplace=True, drop=True)
    temp_df.columns = [
        "公司简称",
        "成立时间",
        "关闭时间",
        "存活天数",
        "融资规模",
        "行业",
        "地点",
    ]
    return temp_df


def nicorn_company() -> pd.DataFrame:
    """
    此数据未更新
    IT桔子-独角兽公司
    https://www.itjuzi.com/unicorn
    :return: 独角兽公司
    :rtype: pandas.DataFrame
    """
    temp_df = pd.read_csv(
        "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_juzi/nicorn_company.csv",
        index_col=0,
    )
    for i in tqdm(range(1, 2)):
        url = f"https://www.itjuzi.com/api/maxima"
        params = {
            "page": i,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        data_df = data_json["data"]["data"]
        data_df = pd.DataFrame(data_df)
        temp_df = temp_df.append(data_df, ignore_index=True)
        temp_df.drop_duplicates(inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    del temp_df['com_id']
    del temp_df['com_logo_archive']
    del temp_df['com_city']
    del temp_df['invse_year']
    del temp_df['invse_month']
    del temp_df['invse_day']
    del temp_df['invse_guess_particulars']
    del temp_df['invse_detail_money']
    del temp_df['invse_currency_id']
    del temp_df['invse_similar_money_id']
    del temp_df['invse_round_id']
    del temp_df['money']
    del temp_df['invse_money']
    del temp_df['round']
    del temp_df['com_scope_id']
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "公司",
        "地区",
        "行业",
        "子行业",
    ]
    return temp_df


def maxima_company() -> pd.DataFrame:
    """
    此数据未更新
    IT桔子-千里马公司
    https://www.itjuzi.com/chollima
    :return: 千里马公司
    :rtype: pandas.DataFrame
    """
    temp_df = pd.read_csv(
        "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/data/data_juzi/maxima.csv",
        index_col=0,
    )
    for i in range(1, 2):
        url = f"https://www.itjuzi.com/api/maxima/"
        params = {
            "page": i,
            "com_prov": "",
            "cat_id": "",
            "order_id": "1",
            "com_name": "",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        data_df = data_json["data"]["data"]
        data_df = pd.DataFrame(data_df)
        temp_df = temp_df.append(data_df, ignore_index=True)
        temp_df.drop_duplicates(inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    del temp_df['com_id']
    del temp_df['com_logo_archive']
    del temp_df['com_scope_id']
    del temp_df['invse_year']
    del temp_df['invse_month']
    del temp_df['invse_day']
    del temp_df['invse_similar_money_id']
    del temp_df['invse_guess_particulars']
    del temp_df['invse_detail_money']
    del temp_df['invse_currency_id']
    del temp_df['invse_round_id']
    del temp_df['money']
    del temp_df['invse_money']
    del temp_df['round']
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "公司",
        "行业",
        "地区",
    ]
    return temp_df


if __name__ == "__main__":
    death_company_df = death_company()
    print(death_company_df)

    nicorn_company_df = nicorn_company()
    print(nicorn_company_df)

    maxima_company_df = maxima_company()
    print(maxima_company_df)
