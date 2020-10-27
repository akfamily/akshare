# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/18 21:27
Desc: 东方财富-数据中心-年报季报
东方财富-数据中心-年报季报-业绩预告
http://data.eastmoney.com/bbsj/202003/yjyg.html
东方财富-数据中心-年报季报-预约披露时间
http://data.eastmoney.com/bbsj/202003/yysj.html
"""
import demjson
import pandas as pd
import requests


def stock_em_yjyg(date: str = "2020-03-31") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩预告
    http://data.eastmoney.com/bbsj/202003/yjyg.html
    :param date: "2020-03-31", "2020-06-30", "2020-09-30", "2020-12-31"; 从 2008-12-31 开始
    :type date: str
    :return: 业绩预告
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "YJBB21_YJYG",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "ndate",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var FtDGPHpn={pages:(tp),data: (x),font:(font)}",
        "filter": f"(IsLatest='T')(enddate=^{date}^)",
        "rt": "52907209",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    font_df = pd.DataFrame(data_json["font"]["FontMapping"])
    data_dict = dict(zip(font_df["code"], font_df["value"]))
    for key, value in data_dict.items():
        data_text = data_text.replace(key, str(value))
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df


def stock_em_yysj(date: str = "2020-03-31") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-预约披露时间
    http://data.eastmoney.com/bbsj/202003/yysj.html
    :param date: "2019-03-31", "2019-06-30", "2019-09-30", "2019-12-31"; 从 2008-12-31 开始
    :type date: str
    :return: 指定时间的上市公司预约披露时间数据
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "YJBB21_YYPL",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "frdate",
        "sr": "1",
        "p": "1",
        "ps": "5000",
        "js": "var HXutCoUP={pages:(tp),data: (x),font:(font)}",
        "filter": f"(securitytypecode='058001001')(reportdate=^{date}^)",
        "rt": "52907209",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df


if __name__ == '__main__':
    stock_em_yjyg_df = stock_em_yjyg(date="2019-12-31")
    print(stock_em_yjyg_df)
    stock_em_yysj_df = stock_em_yysj(date="2019-12-31")
    print(stock_em_yysj_df)
