# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/2/2 11:27
Desc: 期货-期转现-交割
"""
import requests
import pandas as pd


def futures_to_spot_shfe(date: str = "202101") -> pd.DataFrame:
    """
    上海期货交易所-期转现
    http://www.shfe.com.cn/statements/dataview.html?paramid=kx
    1、铜、铜(BC)、铝、锌、铅、镍、锡、螺纹钢、线材、热轧卷板、天然橡胶、20号胶、低硫燃料油、燃料油、石油沥青、纸浆、不锈钢的数量单位为：吨；黄金的数量单位为：克；白银的数量单位为：千克；原油的数量单位为：桶。
    2、交割量、期转现量为单向计算。
    :param date: 年月
    :type date: str
    :return: 上海期货交易所期转现
    :rtype: pandas.DataFrame
    """
    url = f"http://www.shfe.com.cn/data/instrument/ExchangeDelivery{date}.dat"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["ExchangeDelivery"])
    temp_df.columns = [
        "_",
        "日期",
        "交割量",
        "_",
        "期转现量",
        "合约",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "日期",
            "合约",
            "交割量",
            "期转现量",
        ]
    ]
    return temp_df


def futures_delivery_dce(date: str = "202101") -> pd.DataFrame:
    """
    大连商品交易所-交割统计
    http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/jgsj/index.html
    :param date: 交割日期
    :type date: str
    :return: 大连商品交易所-交割统计
    :rtype: pandas.DataFrame
    """
    url = "http://www.dce.com.cn/publicweb/quotesdata/delivery.html"
    params = {
        "deliveryQuotes.variety": "all",
        "year": "",
        "month": "",
        "deliveryQuotes.begin_month": date,
        "deliveryQuotes.end_month": str(int(date) + 1),
    }
    r = requests.post(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    temp_df["交割日期"] = temp_df["交割日期"].astype(str).str.split(".", expand=True).iloc[:, 0]
    return temp_df


def futures_to_spot_dce(date: str = "202102") -> pd.DataFrame:
    """
    大连商品交易所-期转现
    http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/qzxcx/index.html
    :param date: 期转现日期
    :type date: str
    :return: 大连商品交易所-期转现
    :rtype: pandas.DataFrame
    """
    url = "http://www.dce.com.cn/publicweb/quotesdata/ftsDeal.html"
    params = {
        "ftsDealQuotes.variety": "all",
        "year": "",
        "month": "",
        "ftsDealQuotes.begin_month": date,
        "ftsDealQuotes.end_month": date,
    }
    r = requests.post(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    temp_df["期转现发生日期"] = temp_df["期转现发生日期"].astype(str).str.split(".", expand=True).iloc[:, 0]
    return temp_df


def futures_delivery_match_dce(symbol: str = "a") -> pd.DataFrame:
    """
    大连商品交易所-交割配对表
    http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/jgsj/index.html
    :param symbol: 交割品种
    :type symbol: str
    :return: 大连商品交易所-交割配对表
    :rtype: pandas.DataFrame
    """
    url = "http://www.dce.com.cn/publicweb/quotesdata/deliveryMatch.html"
    params = {
        "deliveryMatchQuotes.variety": symbol,
        "contract.contract_id": "all",
        "contract.variety_id": symbol,
    }
    r = requests.post(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    temp_df["配对日期"] = temp_df["配对日期"].astype(str).str.split(".", expand=True).iloc[:, 0]
    return temp_df


def futures_to_spot_czce(date: str = "20210201") -> pd.DataFrame:
    """
    郑州商品交易所-期转现统计
    http://www.czce.com.cn/cn/jysj/qzxtj/H770311index_1.htm
    :param date: 年月日
    :type date: str
    :return: 郑州商品交易所-期转现统计
    :rtype: pandas.DataFrame
    """
    url = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{date[:4]}/{date}/FutureDataTrdtrades.htm"
    r = requests.get(url)
    r.encoding = "utf-8"
    temp_df = pd.read_html(r.text)[0]
    temp_df.columns = [
        "合约代码",
        "合约数量",
    ]
    temp_df = temp_df[
        [
            "合约代码",
            "合约数量",
        ]
    ]
    return temp_df


def futures_delivery_match_czce(date: str = "20210106") -> pd.DataFrame:
    """
    郑州商品交易所-交割配对
    http://www.czce.com.cn/cn/jysj/jgpd/H770308index_1.htm
    :param date: 年月日
    :type date: str
    :return: 郑州商品交易所-交割配对
    :rtype: pandas.DataFrame
    """
    url = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{date[:4]}/{date}/FutureDataDelsettle.htm"
    r = requests.get(url)
    r.encoding = "utf-8"
    temp_df = pd.read_html(r.text)[0]
    index_flag = temp_df[temp_df.iloc[:, 0].str.contains("配对日期")].index.values
    big_df = pd.DataFrame()
    for i, item in enumerate(index_flag):
        try:
            temp_inner_df = temp_df[index_flag[i] + 1: index_flag[i + 1]]
        except:
            temp_inner_df = temp_df[index_flag[i] + 1:]
        temp_inner_df.columns = temp_inner_df.iloc[0, :]
        temp_inner_df = temp_inner_df.iloc[1:-1, :]
        temp_inner_df.reset_index(drop=True, inplace=True)
        date_contract_str = (
            temp_df[temp_df.iloc[:, 0].str.contains("配对日期")].iloc[:, 0].values[i]
        )
        inner_date = date_contract_str.split("：")[1].split(" ")[0]
        symbol = date_contract_str.split("：")[-1]
        temp_inner_df["配对日期"] = inner_date
        temp_inner_df["合约代码"] = symbol
        big_df = big_df.append(temp_inner_df, ignore_index=True)
    big_df.columns = [
        "卖方会员",
        "卖方会员-会员简称",
        "买方会员",
        "买方会员-会员简称",
        "交割量",
        "配对日期",
        "合约代码",
    ]
    return big_df


def futures_delivery_czce(date: str = "20210112") -> pd.DataFrame:
    """
    郑州商品交易所-月度交割查询
    http://www.czce.com.cn/cn/jysj/ydjgcx/H770316index_1.htm
    :param date: 年月日
    :type date: str
    :return: 郑州商品交易所-月度交割查询
    :rtype: pandas.DataFrame
    """
    url = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{date[:4]}/{date}/FutureDataSettlematched.htm"
    r = requests.get(url)
    r.encoding = "utf-8"
    temp_df = pd.read_html(r.text)[0].iloc[:-1, :]
    temp_df.columns = [
        "品种",
        "交割数量",
        "交割额",
    ]
    return temp_df


def futures_delivery_shfe(date: str = "202003") -> pd.DataFrame:
    """
    上海期货交易所-交割情况表
    http://www.shfe.com.cn/statements/dataview.html?paramid=kx
    注意: 日期 -> 月度统计 -> 下拉到交割情况表
    :param date: 年月日
    :type date: str
    :return: 上海期货交易所-交割情况表
    :rtype: pandas.DataFrame
    """
    url = f"http://www.shfe.com.cn/data/dailydata/{date}monthvarietystatistics.dat"
    r = requests.get(url)
    r.encoding = "utf-8"
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["o_curdelivery"])
    temp_df.columns = [
        "品种",
        "品种代码",
        "_",
        "交割量-本月",
        "交割量-比重",
        "交割量-本年累计",
        "交割量-累计同比",
    ]
    temp_df = temp_df[[
        "品种",
        "交割量-本月",
        "交割量-比重",
        "交割量-本年累计",
        "交割量-累计同比",
    ]]
    return temp_df


if __name__ == "__main__":
    futures_to_spot_dce_df = futures_to_spot_dce(date="202102")
    print(futures_to_spot_dce_df)

    futures_to_spot_shfe_df = futures_to_spot_shfe(date="202101")
    print(futures_to_spot_shfe_df)

    futures_to_spot_czce_df = futures_to_spot_czce(date="20210112")
    print(futures_to_spot_czce_df)

    futures_delivery_dce_df = futures_delivery_dce(date="202101")
    print(futures_delivery_dce_df)

    futures_delivery_monthly_czce_df = futures_delivery_czce(date="20210112")
    print(futures_delivery_monthly_czce_df)

    futures_delivery_shfe_df = futures_delivery_shfe(date="202003")
    print(futures_delivery_shfe_df)

    futures_delivery_match_dce_df = futures_delivery_match_dce(symbol="y")
    print(futures_delivery_match_dce_df)

    futures_delivery_match_czce_df = futures_delivery_match_czce(date="20210106")
    print(futures_delivery_match_czce_df)
