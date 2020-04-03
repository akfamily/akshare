# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/3 14:24
Desc: 东方财富网-数据中心-现货与股票
http://data.eastmoney.com/ifdata/xhgp.html
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

# pd.set_option('display.expand_frame_repr', False)
# pd.set_option('display.max_columns', None)


def futures_spot_stock(indicator: str = "能源") -> pd.DataFrame:
    """
    东方财富网-数据中心-现货与股票
    :param indicator: choice of ['能源', '化工', '塑料', '纺织', '有色', '钢铁', '建材', '农副']:
    :type indicator: str
    :return: 现货与股票上下游对应数据
    :rtype: pandas.DataFrame
    """
    map_dict = {
        "能源": 0,
        "化工": 1,
        "塑料": 2,
        "纺织": 3,
        "有色": 4,
        "钢铁": 5,
        "建材": 6,
        "农副": 7,
    }
    url = "http://data.eastmoney.com/ifdata/xhgp.html"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[map_dict.get(indicator)]
    temp_columns = [item for item in temp_df.columns if not item.startswith("Un")]
    temp_df = temp_df.iloc[:, :10]
    temp_df.columns = temp_columns

    soup = BeautifulSoup(r.text, "lxml")
    temp_soup = soup.find(attrs={"id": f"tab{map_dict.get(indicator)}"}).find(attrs={"class": "tab1"}).find_all(attrs={"onmousemove": "this.className='over'"})
    [item.find_all(attrs={"onmouseout": "hideall(1);"}) for item in temp_soup]

    big_list = []
    for item in temp_soup:
        inner_item = item.find_all(attrs={"onmouseout": "hideall(1);"})
        for hidden_item in inner_item:
            hidden_a = hidden_item.find_all("a")
            temp_list = []
            for hidden_a_item in hidden_a:
                temp_list.append(hidden_a_item.text)
            big_list.append(temp_list)

    temp_df["生产商"] = [", ".join(item) for key, item in enumerate(big_list) if key in range(0, len(big_list), 2)]
    temp_df["下游用户"] = [", ".join(item) for key, item in enumerate(big_list) if key in range(1, len(big_list), 2)]
    return temp_df


if __name__ == '__main__':
    for sector in ['能源', '化工', '塑料', '纺织', '有色', '钢铁', '建材', '农副']:
        futures_spot_stock_df = futures_spot_stock(indicator=sector)
        print(futures_spot_stock_df)
