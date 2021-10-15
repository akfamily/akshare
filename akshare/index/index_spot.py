# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/5/27 12:19
Desc: 商品现货价格指数
http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
"""
import requests
import pandas as pd


def spot_goods(symbol: str = "波罗的海干散货指数") -> pd.DataFrame:
    """
    商品现货价格指数
    http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
    :param symbol: choice of {"进口大豆价格指数", "波罗的海干散货指数", "钢坯价格指数", "普氏62%铁矿石指数"}
    :type symbol: str
    :return: 商品现货价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/GoodsIndexService.get_goods_index"
    symbol_url_dict = {
        "进口大豆价格指数": "SOY",
        "波罗的海干散货指数": "BDI",
        "钢坯价格指数": "GP",
        "普氏62%铁矿石指数": "PS",
    }
    params = {"symbol": symbol_url_dict[symbol], "table": "0"}
    r = requests.get(url, params=params)
    r.encoding = "gbk"
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"]["data"])
    temp_df = temp_df[["opendate", "price", "zde", "zdf"]]
    temp_df.columns = ["日期", "指数", "涨跌额", "涨跌幅"]
    return temp_df


if __name__ == "__main__":
    spot_df = spot_goods(symbol="钢坯价格指数")
    print(spot_df)
