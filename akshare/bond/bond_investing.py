# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/17 0:50
Desc: 提供英为财情-利率国债-全球政府债券行情与收益率
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers


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
    url = "https://cn.investing.com/rates-bonds/"
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


def bond_investing_global_country_name_url(country: str = "美国") -> dict:
    """
    参考网页: https://cn.investing.com/rates-bonds/
    获取选择国家对应的: 主要指数, 主要行业, 附加指数, 其他指数
    :param country: str 中文国家名称, 对应 get_global_country_name_url 函数返回的国家名称
    :return: dict
    """
    name_url_dict = _get_global_country_name_url()
    url = f"https://cn.investing.com{name_url_dict[country]}"
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


def bond_investing_global(
    country: str = "中国",
    index_name: str = "中国1年期国债",
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
    """
    start_date = start_date.replace("-", "/")
    end_date = end_date.replace("-", "/")
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    name_code_dict = bond_investing_global_country_name_url(country)
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
    df_data = df_data[["收盘", "开盘", "高", "低", "涨跌幅"]]
    df_data["涨跌幅"] = df_data["涨跌幅"].str.replace("%", "")
    df_data = df_data.astype(float)
    return df_data


if __name__ == "__main__":
    bond_investing_global_country_name_url_dict = bond_investing_global_country_name_url(country="美国")
    print(bond_investing_global_country_name_url_dict)
    bond_investing_global_df = bond_investing_global(
        country="中国",
        index_name="中国1年期国债",
        period="每月",
        start_date="2000-01-01",
        end_date="2020-06-06",
    )
    print(bond_investing_global_df)
