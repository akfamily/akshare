#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/6/11 21:30
Desc: 商品现货价格指数
http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
"""
import pandas as pd
import requests
from akshare.request_config_manager import get_headers_and_timeout


def spot_goods(symbol: str = "波罗的海干散货指数") -> pd.DataFrame:
    """
    新浪财经-商品现货价格指数
    http://finance.sina.com.cn/futuremarket/spotprice.shtml#titlePos_0
    :param symbol: choice of {"波罗的海干散货指数", "钢坯价格指数", "澳大利亚粉矿价格"}
    :type symbol: str
    :return: 商品现货价格指数
    :rtype: pandas.DataFrame
    """
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/GoodsIndexService.get_goods_index"
    symbol_url_dict = {
        "波罗的海干散货指数": "BDI",
        "钢坯价格指数": "GP",
        "澳大利亚粉矿价格": "PB",
    }
    params = {"symbol": symbol_url_dict[symbol], "table": "0"}
    headers, timeout = get_headers_and_timeout(locals().get('headers', {}), locals().get('timeout', None))
    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    r.encoding = "gbk"
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"]["data"])
    temp_df = temp_df[["opendate", "price", "zde", "zdf"]]
    temp_df.columns = ["日期", "指数", "涨跌额", "涨跌幅"]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], format="%Y-%m-%d", errors="coerce").dt.date
    temp_df["指数"] = pd.to_numeric(temp_df["指数"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    spot_goods_df = spot_goods(symbol="波罗的海干散货指数")
    print(spot_goods_df)
