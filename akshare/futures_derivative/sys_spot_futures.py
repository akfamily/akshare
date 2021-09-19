# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/5/9 17:25
Desc: 生意社-商品与期货-现期图: 图片和表格
http://www.100ppi.com/sf/792.html
"""
from io import BytesIO

import pandas as pd
import requests
from PIL import Image
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


def get_sys_spot_futures(symbol: str = "铜", plot: bool = True) -> pd.DataFrame:
    """
    生意社-商品与期货-现期图: 图和表格
    :param symbol: str 品种
    :param plot: Bool
    :return: pd.DataFrame or pic
    日期       现货价格 主力合约 最近合约
    07-30  594.25  586  595
    08-08  589.25  577  577
    08-17  578.25    -    -
    08-26  584.25  588  586
    09-04  581.25  588  571
    09-13  587.25    -    -
    09-22  588.25    -    -
    10-01  588.25    -    -
    10-10  586.25  565  581
    10-19  579.25    -    -
    10-27  572.25    -    -
    日期        基差率
    07-30   1.25%
    08-08   1.98%
    08-17       -
    08-26  -0.71%
    09-04  -1.26%
    09-13       -
    09-22       -
    10-01       -
    10-10   3.59%
    10-19       -
    10-27       -
    日期      主力基差
    07-30   7.45
    08-08  11.65
    08-17      -
    08-26  -4.15
    09-04  -7.35
    09-13      -
    09-22      -
    10-01      -
    10-10  21.05
    10-19      -
    10-27      -
    """
    name_url_dict = get_sys_spot_futures_dict()
    url = name_url_dict[symbol]
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    temp_item = [item.find("img")["src"] for item in soup.find("div", attrs={"class": "content_left fl"}).find_all("div", attrs={"class": "pic"})]
    table_df_one = pd.read_html(res.text, header=0, index_col=0)[1].T
    table_df_two = pd.read_html(res.text, header=0, index_col=0)[2].T
    table_df_three = pd.read_html(res.text, header=0, index_col=0)[3].T
    if plot:
        for item_url in temp_item:
            res = requests.get(item_url)
            f = Image.open(BytesIO(res.content))
            f.show()
        return table_df_one, table_df_two, table_df_three
    else:
        return table_df_one, table_df_two, table_df_three


if __name__ == "__main__":
    get_sys_spot_futures_dict_map = get_sys_spot_futures_dict()
    print(get_sys_spot_futures_dict_map)
    df_one, df_two, df_three = get_sys_spot_futures(symbol="白银", plot=False)
    print(df_one)
    print(df_two)
    print(df_three)
