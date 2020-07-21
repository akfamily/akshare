# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/9/30 13:58
Desc: 常用变量
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir(r'C:\Users\king\Desktop\obor_rank\data')
file_name_list = os.listdir()
alternative_name = [item.split('--')[1] for item in file_name_list]
name_dict = dict(zip(file_name_list, alternative_name))
dict_list_name = list(name_dict.keys())
fit_list = []
for file_name in dict_list_name:
    # file_name = dict_list_name[0]
    file_df = pd.read_csv(file_name, encoding='gb2312', parse_dates=['日期'], index_col=['日期'])
    file_df.index = pd.to_datetime(file_df.index, format='%Y年%m月%d日')
    file_df = file_df.sort_index()
    if file_df.shape[0] > 4500:  # 10年长度设置
        print(file_name)
        fit_list.append(file_name)
len(fit_list)
sh_df = pd.read_csv(fit_list[4], encoding='gb2312', parse_dates=['日期'], index_col=['日期'])
sh_df.index = pd.to_datetime(sh_df.index, format='%Y年%m月%d日')
sh_df = sh_df.sort_index()['百分比变化']
sh_df = pd.DataFrame(sh_df)
type(sh_df)
sh_df.columns = [fit_list[4].split('--')[1].split('.')[0]]
for file_name in fit_list:
    # file_name = fit_list[4]
    file_df = pd.read_csv(file_name, encoding='gb2312', parse_dates=['日期'], index_col=['日期'])
    file_df.index = pd.to_datetime(file_df.index, format='%Y年%m月%d日')
    file_df = file_df.sort_index()
    df_use = file_df.truncate(before='2000-01-01')
    # round((df_use['百分比变化'].str.replace('%', '').astype(float)/100 + 1).cumprod() * 1000, 2).plot()
    # plt.show()
    df_use = pd.DataFrame(round(df_use['百分比变化'].str.replace('%', '').astype(float)/100, 6))
    df_use.columns = [file_name.split('--')[1].split('.')[0]]
    sh_df = sh_df.merge(df_use, left_index=True, right_index=True, how='left')

temp_df = sh_df.dropna(how='any')
temp_df = temp_df.iloc[:, 1:]
temp_df.plot()
plt.show()
temp_df.to_csv('obor.csv', encoding='gb2312')

