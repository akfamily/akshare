# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/18 13:07
Desc: 新浪财经-交易日历
https://finance.sina.com.cn/realstock/company/klc_td_sh.txt
"""
import execjs
import pandas as pd
import requests

from akshare.stock.cons import hk_js_decode


def tool_trade_date_hist_sina() -> pd.DataFrame:
    """
    交易日历-历史数据
    https://finance.sina.com.cn/realstock/company/klc_td_sh.txt
    :return: 交易日历
    :rtype: pandas.DataFrame
    """
    url = "https://finance.sina.com.cn/realstock/company/klc_td_sh.txt"
    r = requests.get(url)
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call('d', r.text.split("=")[1].split(";")[0].replace('"', ""))  # 执行js解密代码
    temp_df = pd.DataFrame(dict_list)
    temp_df.columns = ["trade_date"]
    temp_df["trade_date"] = pd.to_datetime(temp_df["trade_date"]).dt.date
    temp_df = temp_df.astype(str)
    return temp_df


if __name__ == '__main__':
    tool_trade_date_hist_df = tool_trade_date_hist_sina()
    print(tool_trade_date_hist_df)
