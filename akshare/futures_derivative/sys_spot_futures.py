#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/5/9 17:25
Desc: 生意社-商品与期货-现期图: 图片和表格
http://www.100ppi.com/sf/792.html
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_sys_spot_futures_dict() -> dict:
    """
    生意社-商品与期货-现期图: 品种和网址字典
    http://www.100ppi.com/sf/792.html
    :return: dict
    {'铜': 'http://www.100ppi.com/sf/792.html', '铅': 'http://www.100ppi.com/sf/825.html', '锌': 'http://www.100ppi.com/sf/826.html', '铝': 'http://www.100ppi.com/sf/827.html', '螺纹钢': 'http://www.100ppi.com/sf/927.html', '线材': 'http://www.100ppi.com/sf/740.html', '燃料油': 'http://www.100ppi.com/sf/387.html', '焦炭': 'http://www.100ppi.com/sf/617.html', '天然橡胶': 'http://www.100ppi.com/sf/586.html', '聚氯乙烯': 'http://www.100ppi.com/sf/107.html', '聚乙烯': 'http://www.100ppi.com/sf/435.html', '甲醇': 'http://www.100ppi.com/sf/817.html', '菜籽油': 'http://www.100ppi.com/sf/810.html', '棕榈油': 'http://www.100ppi.com/sf/1084.html', '硬麦': 'http://www.100ppi.com/sf/349.html', '豆一': 'http://www.100ppi.com/sf/1080.html', '豆粕': 'http://www.100ppi.com/sf/312.html', '豆油': 'http://www.100ppi.com/sf/403.html', '玉米': 'http://www.100ppi.com/sf/274.html', '白糖': 'http://www.100ppi.com/sf/564.html', '棉花': 'http://www.100ppi.com/sf/344.html', 'PTA': 'http://www.100ppi.com/sf/356.html', '黄金': 'http://www.100ppi.com/sf/551.html', '白银': 'http://www.100ppi.com/sf/544.html', '玻璃': 'http://www.100ppi.com/sf/959.html', '焦煤': 'http://www.100ppi.com/sf/1121.html', '菜籽粕': 'http://www.100ppi.com/sf/1014.html', '油菜籽': 'http://www.100ppi.com/sf/1087.html', '动力煤': 'http://www.100ppi.com/sf/369.html', '石油沥青': 'http://www.100ppi.com/sf/1022.html', '铁矿石': 'http://www.100ppi.com/sf/961.html', '鸡蛋': 'http://www.100ppi.com/sf/1049.html', '锰硅': 'http://www.100ppi.com/sf/1155.html', '硅铁': 'http://www.100ppi.com/sf/1154.html', '热轧卷板': 'http://www.100ppi.com/sf/195.html', '细木工板': 'http://www.100ppi.com/sf/1158.html', '聚丙烯': 'http://www.100ppi.com/sf/718.html', '锡': 'http://www.100ppi.com/sf/1181.html', '镍': 'http://www.100ppi.com/sf/1182.html', '玉米淀粉': 'http://www.100ppi.com/sf/1209.html'}
    """
    url = "http://www.100ppi.com/sf/792.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    temp_item = soup.find("div", attrs={"class": "q8"}).find_all("li")
    name_url_dict = dict(zip([item.find("a").get_text().strip() for item in temp_item], [item.find("a")["href"] for item in temp_item]))
    return name_url_dict


def get_sys_spot_futures(symbol: str = "铜") -> pd.DataFrame:
    """
    生意社-商品与期货-现期图: 图和表格
    :param symbol: str 品种
    :return: pd.DataFrame or pic
    """
    name_url_dict = get_sys_spot_futures_dict()
    url = name_url_dict[symbol]
    res = requests.get(url)
    table_df_one = pd.read_html(res.text, header=0, index_col=0)[1].T
    table_df_two = pd.read_html(res.text, header=0, index_col=0)[2].T
    table_df_three = pd.read_html(res.text, header=0, index_col=0)[3].T
    return table_df_one, table_df_two, table_df_three


if __name__ == "__main__":
    get_sys_spot_futures_dict_map = get_sys_spot_futures_dict()
    print(get_sys_spot_futures_dict_map)

    df_one, df_two, df_three = get_sys_spot_futures(symbol="白银")
    print(df_one)
    print(df_two)
    print(df_three)
