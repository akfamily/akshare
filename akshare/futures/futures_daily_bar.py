# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/4 15:58
Desc: 交易所网站获取期货日线行情
"""
import datetime
import json
import re
import warnings
import zipfile
from io import BytesIO, StringIO

import numpy as np
import pandas as pd
import requests

from akshare.futures import cons
from akshare.futures.requests_fun import requests_link

calendar = cons.get_calendar()


def get_cffex_daily(date: str = "20100401") -> pd.DataFrame:
    """
    中国金融期货交易所日交易数据
    http://www.cffex.com.cn/rtj/
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象; 为空时为当天
    :return: pandas.DataFrame
    中国金融期货交易所日:
    symbol        合约代码
    date          日期
    open          开盘价
    high          最高价
    low          最低价
    close         收盘价
    volume        成交量
    open_interest   持仓量
    turnover      成交额
    settle        结算价
    pre_settle    前结算价
    variety       合约类别
    或 None(给定日期没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    url = f"http://www.cffex.com.cn/sj/historysj/{date[:-2]}/zip/{date[:-2]}.zip"
    r = requests.get(url)
    try:
        with zipfile.ZipFile(BytesIO(r.content)) as file:
            with file.open(f"{date}_1.csv") as my_file:
                data = my_file.read().decode("gb2312")
                data_df = pd.read_csv(StringIO(data))
    except:
        return None
    data_df = data_df[data_df["合约代码"] != "小计"]
    data_df = data_df[data_df["合约代码"] != "合计"]
    data_df = data_df[~data_df["合约代码"].str.contains("IO")]
    data_df.reset_index(inplace=True, drop=True)
    data_df["合约代码"] = data_df["合约代码"].str.strip()
    symbol_list = data_df["合约代码"].to_list()
    variety_list = [re.compile(r"[a-zA-Z_]+").findall(item)[0] for item in symbol_list]
    if data_df.shape[1] == 15:
        data_df.columns = ["symbol", "open", "high", "low", "volume", "turnover",
                           "open_interest", "_", "close", "settle", "pre_settle", "_", "_", "_", "_"]
    else:
        data_df.columns = ["symbol", "open", "high", "low", "volume", "turnover",
                           "open_interest", "_", "close", "settle", "pre_settle", "_", "_", "_"]
    data_df["date"] = date
    data_df["variety"] = variety_list
    data_df = data_df[
        ["symbol", "date", "open", "high", "low", "close", "volume", "open_interest", "turnover", "settle",
         "pre_settle", "variety"]]
    return data_df


def get_ine_daily(date: str = "20210421") -> pd.DataFrame:
    """
    上海国际能源交易中心-日频率-量价数据
    上海国际能源交易中心: 原油期货(上市时间: 20180326); 20号胶期货(上市时间: 20190812)
    trade_price: http://www.ine.cn/statements/daily/?paramid=kx
    trade_note: http://www.ine.cn/data/datanote.dat
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 上海国际能源交易中心-日频率-量价数据
    :rtype: pandas.DataFrame or None
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn(f"{day.strftime('%Y%m%d')}非交易日")
        return None
    url = f"http://www.ine.cn/data/dailydata/kx/kx{day.strftime('%Y%m%d')}.dat"
    r = requests.get(url)
    result_df = pd.DataFrame()
    try:
        data_json = r.json()
    except:
        return None
    temp_df = pd.DataFrame(data_json["o_curinstrument"]).iloc[:-1, :]
    temp_df = temp_df[temp_df["DELIVERYMONTH"] != "小计"]
    temp_df = temp_df[~temp_df["PRODUCTNAME"].str.contains("总计")]
    result_df["symbol"] = temp_df["PRODUCTGROUPID"].str.upper().str.strip() + temp_df["DELIVERYMONTH"]
    result_df["date"] = day.strftime("%Y%m%d")
    result_df["open"] = temp_df["OPENPRICE"]
    result_df["high"] = temp_df["HIGHESTPRICE"]
    result_df["low"] = temp_df["LOWESTPRICE"]
    result_df["close"] = temp_df["CLOSEPRICE"]
    result_df["volume"] = temp_df["VOLUME"]
    result_df["open_interest"] = temp_df["OPENINTEREST"]
    result_df["turnover"] = 0
    result_df["settle"] = temp_df["SETTLEMENTPRICE"]
    result_df["pre_settle"] = temp_df["PRESETTLEMENTPRICE"]
    result_df["variety"] = temp_df["PRODUCTGROUPID"].str.upper().str.strip()
    result_df = result_df[result_df["symbol"] != "总计"]
    result_df = result_df[~result_df["symbol"].str.contains("efp")]
    return result_df


def get_czce_daily(date: str = "20050525") -> pd.DataFrame:
    """
    郑州商品交易所-日频率-量价数据
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日; 日期需要大于 20100824
    :type date: str or datetime.date
    :return: 郑州商品交易所-日频率-量价数据
    :rtype: pandas.DataFrame or None
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn(f"{day.strftime('%Y%m%d')}非交易日")
        return None
    if day > datetime.date(2010, 8, 24):
        if day > datetime.date(2015, 9, 19):
            u = cons.CZCE_DAILY_URL_3
            url = u % (day.strftime("%Y"), day.strftime("%Y%m%d"))
        elif day < datetime.date(2015, 9, 19):
            u = cons.CZCE_DAILY_URL_2
            url = u % (day.strftime("%Y"), day.strftime("%Y%m%d"))
        listed_columns = cons.CZCE_COLUMNS
        output_columns = cons.OUTPUT_COLUMNS
        try:
            r = requests.get(url)
            html = r.text
        except requests.exceptions.HTTPError as reason:
            if reason.response.status_code != 404:
                print(
                    cons.CZCE_DAILY_URL_3
                    % (day.strftime("%Y"), day.strftime("%Y%m%d")),
                    reason,
                )
            return
        if html.find("您的访问出错了") >= 0 or html.find("无期权每日行情交易记录") >= 0:
            return
        html = [
            i.replace(" ", "").split("|")
            for i in html.split("\n")[:-4]
            if i[0][0] != "小"
        ]

        if day > datetime.date(2015, 9, 19):
            if html[1][0] not in ["品种月份", "品种代码", "合约代码"]:
                return
            dict_data = list()
            day_const = int(day.strftime("%Y%m%d"))
            for row in html[2:]:
                m = cons.FUTURES_SYMBOL_PATTERN.match(row[0])
                if not m:
                    continue
                row_dict = {"date": day_const, "symbol": row[0], "variety": m.group(1)}
                for i, field in enumerate(listed_columns):
                    if row[i + 1] == "\r" or row[i + 1] == '':
                        row_dict[field] = 0.0
                    elif field in [
                        "volume",
                        "open_interest",
                        "oi_chg",
                        "exercise_volume",
                    ]:
                        row[i + 1] = row[i + 1].replace(",", "")
                        row_dict[field] = int(row[i + 1])
                    else:
                        row[i + 1] = row[i + 1].replace(",", "")
                        row_dict[field] = float(row[i + 1])
                dict_data.append(row_dict)

            return pd.DataFrame(dict_data)[output_columns]
        elif day < datetime.date(2015, 9, 19):
            dict_data = list()
            day_const = int(day.strftime("%Y%m%d"))
            for row in html[1:]:
                row = row[0].split(",")
                m = cons.FUTURES_SYMBOL_PATTERN.match(row[0])
                if not m:
                    continue
                row_dict = {"date": day_const, "symbol": row[0], "variety": m.group(1)}
                for i, field in enumerate(listed_columns):
                    if row[i + 1] == "\r":
                        row_dict[field] = 0.0
                    elif field in [
                        "volume",
                        "open_interest",
                        "oi_chg",
                        "exercise_volume",
                    ]:
                        row_dict[field] = int(float(row[i + 1]))
                    else:
                        row_dict[field] = float(row[i + 1])
                dict_data.append(row_dict)
            return pd.DataFrame(dict_data)[output_columns]

    if day <= datetime.date(2010, 8, 24):
        u = cons.CZCE_DAILY_URL_1
        url = u % day.strftime("%Y%m%d")
        listed_columns = cons.CZCE_COLUMNS_2
        output_columns = cons.OUTPUT_COLUMNS
        df = pd.read_html(url)[1].dropna(how="any")
        dict_data = list()
        day_const = int(day.strftime("%Y%m%d"))
        for row in df.to_dict(orient="records"):
            row = list(row.values())
            m = cons.FUTURES_SYMBOL_PATTERN.match(row[0])
            if not m:
                continue
            row_dict = {"date": day_const, "symbol": row[0], "variety": m.group(1)}
            for i, field in enumerate(listed_columns):
                if row[i + 1] == "\r":
                    row_dict[field] = 0.0
                elif field in ["volume", "open_interest", "oi_chg", "exercise_volume"]:
                    row_dict[field] = int(row[i + 1])
                else:
                    row_dict[field] = float(row[i + 1])
            dict_data.append(row_dict)
        return pd.DataFrame(dict_data)[output_columns]


def get_shfe_v_wap(date: str = "20131017") -> pd.DataFrame:
    """
    获取上期所日成交均价数据
    Parameters
    ------
    date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    Return
    -------
    DataFrame
        郑商所日交易数据(DataFrame):
            symbol        合约代码
            date          日期
            time_range    v_wap时段，分09:00-10:15和09:00-15:00两类
            v_wap          加权平均成交均价
    或 None(给定日期没有数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    try:
        json_data = json.loads(
            requests_link(
                cons.SHFE_V_WAP_URL % (day.strftime("%Y%m%d")),
                headers=cons.headers,
                encoding="utf-8",
            ).text
        )
    except:
        return None

    if len(json_data["o_currefprice"]) == 0:
        return None
    try:
        df = pd.DataFrame(json_data["o_currefprice"])
        df["INSTRUMENTID"] = df["INSTRUMENTID"].str.strip()
        df[":B1"].astype("int16")
        return df.rename(columns=cons.SHFE_V_WAP_COLUMNS)[
            list(cons.SHFE_V_WAP_COLUMNS.values())
        ]
    except:
        return None


def get_shfe_daily(date: str = "20160104") -> pd.DataFrame:
    """
    上海期货交易所-日频率-量价数据
    http://www.shfe.com.cn/statements/dataview.html?paramid=kx
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象, 默认为当前交易日
    :type date: str or datetime.date
    :return: 上海期货交易所-日频率-量价数据
    :rtype: pandas.DataFrame or None
    上期所日交易数据(DataFrame):
    symbol        合约代码
    date          日期
    open          开盘价
    high          最高价
    low           最低价
    close         收盘价
    volume        成交量
    open_interest 持仓量
    turnover      成交额
    settle        结算价
    pre_settle     前结算价
    variety       合约类别
    或 None(给定交易日没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    try:
        json_data = json.loads(
            requests_link(
                cons.SHFE_DAILY_URL % (day.strftime("%Y%m%d")),
                headers=cons.shfe_headers,
            ).text
        )
    except requests.HTTPError as reason:
        if reason.response != 404:
            print(cons.SHFE_DAILY_URL % (day.strftime("%Y%m%d")), reason)
        return

    if len(json_data["o_curinstrument"]) == 0:
        return

    df = pd.DataFrame(
        [
            row
            for row in json_data["o_curinstrument"]
            if row["DELIVERYMONTH"] not in ["小计", "合计"] and row["DELIVERYMONTH"] != ""
        ]
    )
    try:
        df["variety"] = df["PRODUCTGROUPID"].str.upper().str.strip()
    except KeyError as e:
        df["variety"] = df["PRODUCTID"].str.upper().str.split('_', expand=True).iloc[:, 0].str.strip()
    df["symbol"] = df["variety"] + df["DELIVERYMONTH"]
    df["date"] = day.strftime("%Y%m%d")
    v_wap_df = get_shfe_v_wap(day)
    if v_wap_df is not None:
        df = pd.merge(
            df,
            v_wap_df[v_wap_df.time_range == "9:00-15:00"],
            on=["date", "symbol"],
            how="left",
        )
        df["turnover"] = df.v_wap * df.VOLUME
    else:
        df["VOLUME"] = df["VOLUME"].apply(lambda x: 0 if x == "" else x)
        df["turnover"] = df["VOLUME"] * df["SETTLEMENTPRICE"]
    df.rename(columns=cons.SHFE_COLUMNS, inplace=True)
    df = df[~df["symbol"].str.contains("efp")]
    return df[cons.OUTPUT_COLUMNS]


def get_dce_daily(date: str = "20030115") -> pd.DataFrame:
    """
    大连商品交易所日交易数据
    http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html
    :param date: 交易日, e.g., 20200416
    :type date: str
    :return: 具体交易日的个品种行情数据
    :rtype: pandas.DataFrame
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    url = "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "86",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.dce.com.cn",
        "Origin": "http://www.dce.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    }
    params = {
        "dayQuotes.variety": "all",
        "dayQuotes.trade_type": "0",
        "year": date[:4],
        "month": str(int(date[4:6]) - 1),
        "day": date[6:],
        "exportFlag": "excel",
    }
    r = requests.post(url, data=params, headers=headers)
    data_df = pd.read_excel(BytesIO(r.content))
    data_df = data_df[~data_df["商品名称"].str.contains("小计")]
    data_df = data_df[~data_df["商品名称"].str.contains("总计")]
    data_df["variety"] = data_df["商品名称"].map(lambda x: cons.DCE_MAP[x])
    data_df["symbol"] = data_df["variety"] + data_df["交割月份"].astype(int).astype(str)
    del data_df["商品名称"]
    del data_df["交割月份"]
    data_df.columns = ["open", "high", "low", "close",
                       "pre_settle", "settle", "_", "_",
                       "volume", "open_interest", "_", "turnover", "variety", "symbol"]
    data_df["date"] = date
    data_df = data_df[
        ["symbol", "date", "open", "high", "low", "close", "volume", "open_interest", "turnover", "settle",
         "pre_settle", "variety"]]
    data_df = data_df.applymap(lambda x: x.replace(",", ""))
    data_df = data_df.astype({"open": "float",
                              "high": "float",
                              "low": "float",
                              "close": "float",
                              "volume": "float",
                              "open_interest": "float",
                              "turnover": "float",
                              "settle": "float",
                              "pre_settle": "float",
                              })
    return data_df


def get_futures_daily(start_date: str = "20210421", end_date: str = "20210426", market: str = "INE", index_bar: bool = False) -> pd.DataFrame:
    """
    交易所日交易数据
    :param start_date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :type start_date: str
    :param end_date: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :type end_date: str
    :param market: 'CFFEX' 中金所, 'CZCE' 郑商所,  'SHFE' 上期所, 'DCE' 大商所 之一, 'INE' 上海国际能源交易中心。默认为中金所
    :type market: str
    :param index_bar: 是否合成指数K线, 默认为 False 否则影响 roll_yield 的计算
    :type index_bar: bool
    :return: 交易所日交易数据
    :rtype: pandas.DataFrame
    """
    if market.upper() == "CFFEX":
        f = get_cffex_daily
    elif market.upper() == "CZCE":
        f = get_czce_daily
    elif market.upper() == "SHFE":
        f = get_shfe_daily
    elif market.upper() == "DCE":
        f = get_dce_daily
    elif market.upper() == "INE":
        f = get_ine_daily
    else:
        print("Invalid Market Symbol")
        return None

    start_date = (
        cons.convert_date(start_date) if start_date is not None else datetime.date.today()
    )
    end_date = (
        cons.convert_date(end_date)
        if end_date is not None
        else cons.convert_date(cons.get_latest_data_date(datetime.datetime.now()))
    )

    df_list = list()
    while start_date <= end_date:
        df = f(date=str(start_date).replace("-", ""))
        if df is not None:
            df_list.append(df)
            if index_bar:
                df_list.append(get_futures_index(df))
        start_date += datetime.timedelta(days=1)

    if len(df_list) > 0:
        temp_df = pd.concat(df_list).reset_index(drop=True)
        temp_df = temp_df[~temp_df['symbol'].str.contains("efp")]
        return temp_df


def get_futures_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    指数日交易数据, 指数合成
    :param df: 爬到的原始合约日线行情
    :type df: pandas.DataFrame
    :return: 持仓量加权指数日线行情
    :rtype: pandas.DataFrame
    """
    index_dfs = []
    for var in set(df["variety"]):
        df_cut = df[df["variety"] == var]
        df_cut = df_cut[df_cut["open_interest"] != 0]
        df_cut = df_cut[df_cut["close"] != np.nan]
        df_cut = df_cut[df_cut["volume"] != int(0)]
        if len(df_cut.index) > 0:
            index_df = pd.Series(index=df_cut.columns, dtype="object")
            index_df[["volume", "open_interest", "turnover"]] = df_cut[
                ["volume", "open_interest", "turnover"]
            ].sum()
            if "efp" in df_cut.iloc[-1, 0]:
                df_cut = df_cut.iloc[:-1, :]
            df_cut.replace("", 0, inplace=True)  # 20201026 部分数据开盘价空缺
            index_df[["open", "high", "low", "close", "settle", "pre_settle"]] = np.dot(
                np.array(
                    df_cut[["open", "high", "low", "close", "settle", "pre_settle"]]
                ).T,
                np.array((df_cut["open_interest"].astype(float))),
            ) / np.sum(df_cut["open_interest"].astype(float))
            index_df[["date", "variety"]] = df_cut[["date", "variety"]].iloc[0, :]
            index_df["symbol"] = index_df["variety"] + "99"
            index_dfs.append(index_df)
    return pd.concat(index_dfs, axis=1).T


if __name__ == "__main__":
    get_futures_daily_df = get_futures_daily(start_date='20160101', end_date='20160201', market="SHFE", index_bar=True)
    print(get_futures_daily_df)

    get_dce_daily_df = get_dce_daily(date="20210427")
    print(get_dce_daily_df)

    get_cffex_daily_df = get_cffex_daily(date="20101101")
    print(get_cffex_daily_df)

    get_ine_daily_df = get_ine_daily(date="20210426")
    print(get_ine_daily_df)

    get_czce_daily_df = get_czce_daily(date="20210416")
    print(get_czce_daily_df)

    get_shfe_daily_df = get_shfe_daily(date="20160104")
    print(get_shfe_daily_df)
