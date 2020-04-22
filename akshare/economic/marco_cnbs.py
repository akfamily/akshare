# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/21 15:22
Desc: 国家金融与发展实验室-中国宏观杠杆率数据
http://114.115.232.154:8080/
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 显示中文标签


def macro_cnbs() -> pd.DataFrame:
    """
    国家金融与发展实验室-中国宏观杠杆率数据
    http://114.115.232.154:8080/
    :return: 中国宏观杠杆率数据
    :rtype: pandas.DataFrame
         年份       居民部门     非金融企业部门  ...      实体经济部门    金融部门资产方    金融部门负债方
    0   1993-12   8.311222   91.658000  ...  107.791459   8.896441   7.128428
    1   1994-12   7.808230   82.411703  ...   98.354271   9.808787   6.796868
    2   1995-12   8.240004   80.950106  ...   97.850373  10.009081   7.006151
    3   1996-03   8.403456   81.711651  ...   99.241521  10.183896   7.186300
    4   1996-06   8.581114   82.051373  ...   99.679459  10.379730   7.380510
    ..      ...        ...         ...  ...         ...        ...        ...
    93  2018-09  52.575456  155.641011  ...  245.227043  61.350917  60.645733
    94  2018-12  53.198837  153.553140  ...  243.702122  60.638348  60.936158
    95  2019-03  54.277928  156.881879  ...  248.828108  60.542178  59.417322
    96  2019-06  55.304291  155.743313  ...  249.533412  58.736094  58.727086
    97  2019-09  56.314848  155.618498  ...  251.147265  55.820243  59.358625
    """
    url = "http://114.115.232.154:8080/handler/download.ashx"
    excel_data = pd.read_excel(url, sheet_name="Data", header=0, skiprows=1)
    excel_data["Period"] = pd.to_datetime(excel_data["Period"]).dt.strftime("%Y-%m")
    excel_data.columns = [
        "年份",
        "居民部门",
        "非金融企业部门",
        "政府部门",
        "中央政府",
        "地方政府",
        "实体经济部门",
        "金融部门资产方",
        "金融部门负债方",
    ]
    return excel_data


if __name__ == '__main__':
    macro_cnbs_df = macro_cnbs()
    print(macro_cnbs_df)
    macro_cnbs_df.index = pd.to_datetime(macro_cnbs_df["年份"])
    macro_cnbs_df["居民部门"].plot()
    plt.ylabel("居民部门杠杆率数据(百分比%)")
    plt.title("中国宏观杠杆率数据-居民部门")
    plt.show()
