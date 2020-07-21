# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/19 12:19
Desc: 商品现货价格指数
http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
"""
import json

import requests
import pandas as pd

from akshare.index.cons import soy_url, bdi_url, gp_url, ps_url


def spot_goods(symbol="波罗的海干散货指数"):
    """
    获取商品现货价格指数
    http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
    """
    symbol_url_dict = {"进口大豆价格指数": soy_url, "波罗的海干散货指数": bdi_url, "钢坯价格指数": gp_url, "普氏62%铁矿石指数": ps_url}
    res = requests.get(symbol_url_dict[symbol])
    res.encoding = "gbk"
    res_text = res.text
    data_json = json.loads(res_text[res_text.find("{"):res_text.rfind(")")])
    data_df = pd.DataFrame(data_json["result"]["data"]["data"])
    temp_df = data_df[["opendate", "price", "zde", "zdf"]]
    temp_df.columns = ["日期", "指数", "涨跌额", "涨跌幅"]
    return temp_df


if __name__ == '__main__':
    spot_df = spot_goods(symbol="波罗的海干散货指数")
    print(spot_df)
