# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/02/20 13:58
contact: jindaxiang@163.com
desc: 从交易所网站获取日线行情
"""
import datetime
import json
import urllib
import warnings

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.futures import cons
from akshare.futures.requests_fun import requests_link

calendar = cons.get_calendar()


def get_cffex_daily(date=None):
    """
    中国金融期货交易所日交易数据
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
    try:
        html = requests_link(
            cons.CFFEX_DAILY_URL.format(
                day.strftime("%Y%m"), day.strftime("%d"), day.strftime("%Y%m%d")
            ),
            encoding="gbk",
            headers=cons.headers,
        ).text
    except requests.exceptions.HTTPError as reason:
        if reason.response != 404:
            print(
                cons.CFFEX_DAILY_URL
                % (day.strftime("%Y%m"), day.strftime("%d"), day.strftime("%Y%m%d")),
                reason,
            )
        return

    if html.find("网页错误") >= 0:
        return
    html = [
        i.replace(" ", "").split(",") for i in html.split("\n")[:-2] if i[0][0] != "小"
    ]

    if html[0][0] != "合约代码":
        return

    dict_data = list()
    day_const = day.strftime("%Y%m%d")
    for row in html[1:]:
        m = cons.FUTURES_SYMBOL_PATTERN.match(row[0])
        if not m:
            continue
        row_dict = {"date": day_const, "symbol": row[0], "variety": m.group(1)}

        for i, field in enumerate(cons.CFFEX_COLUMNS):
            if row[i + 1] == "":
                row_dict[field] = 0.0
            elif field in ["volume", "open_interest", "oi_chg"]:
                row_dict[field] = int(row[i + 1])
            else:
                try:
                    row_dict[field] = float(row[i + 1])
                except:
                    pass
        row_dict["pre_settle"] = row_dict["close"] - row_dict["change1"]
        dict_data.append(row_dict)

    return pd.DataFrame(dict_data)[cons.OUTPUT_COLUMNS]


def get_ine_daily(date="20200312"):
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
    temp_df = pd.DataFrame(r.json()["o_curinstrument"]).iloc[:-1, :]
    temp_df = temp_df[temp_df["DELIVERYMONTH"] != "小计"]
    result_df["symbol"] = temp_df["PRODUCTID"].str.upper().str.split("_", expand=True)[0] + temp_df["DELIVERYMONTH"]
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
    result_df["variety"] = temp_df["PRODUCTID"].str.upper().str.split("_", expand=True)[0]
    return result_df


def get_czce_daily(date=None):
    """
    郑州商品交易所-日频率-量价数据
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 郑州商品交易所-日频率-量价数据
    :rtype: pandas.DataFrame or None
    郑商所每日期货交易数据:
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
    pre_settle    前结算价
    variety       合约类别
    或
   郑商所每日期权交易数据
    symbol        合约代码
    date          日期
    open          开盘价
    high          最高价
    low           最低价
    close         收盘价
    pre_settle      前结算价
    settle         结算价
    delta          对冲值
    volume         成交量
    open_interest     持仓量
    oi_change       持仓变化
    turnover        成交额
    implied_volatility 隐含波动率
    exercise_volume   行权量
    variety        合约类别
    None(类型错误或给定日期没有交易数据)
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
            if i[0][0] != u"小"
        ]

        if day > datetime.date(2015, 9, 19):
            if html[1][0] not in ["品种月份", u"品种代码"]:
                return
            dict_data = list()
            day_const = int(day.strftime("%Y%m%d"))
            for row in html[2:]:
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

        for row in df.to_dict(orient="records")[1:]:
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


def get_shfe_v_wap(date=None):
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
    except requests.HTTPError as reason:
        if reason.response not in [404, 403]:
            print(cons.SHFE_DAILY_URL % (day.strftime("%Y%m%d")), reason)
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


def get_shfe_daily(date=None):
    """
    上海期货交易所-日频率-量价数据
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
    df["variety"] = df.PRODUCTID.str.slice(0, -6).str.upper()
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
    return df[cons.OUTPUT_COLUMNS]


def get_dce_daily(date=None, symbol_type="futures", retries=0):
    """
        获取大连商品交易所日交易数据
    Parameters
    ------
        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        symbol_type: 数据类型, 为'futures'期货 或 'option'期权二者之一
        retries: int, 当前重试次数，达到3次则获取数据失败
    Return
    -------
        DataFrame
            大商所日交易数据(DataFrame):
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                volume        成交量
                open_interest   持仓量
                turnover       成交额
                settle        结算价
                pre_settle    前结算价
                variety       合约类别
        或
        DataFrame
           郑商所每日期权交易数据
                symbol        合约代码
                date          日期
                open          开盘价
                high          最高价
                low           最低价
                close         收盘价
                pre_settle      前结算价
                settle         结算价
                delta          对冲值
                volume         成交量
                open_interest     持仓量
                oi_change       持仓变化
                turnover        成交额
                implied_volatility 隐含波动率
                exercise_volume   行权量
                variety        合约类别
        或 None(给定日期没有交易数据)
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    if day.strftime("%Y%m%d") not in calendar:
        warnings.warn("%s非交易日" % day.strftime("%Y%m%d"))
        return None
    if retries > 3:
        print("maximum retires for DCE market data: ", day.strftime("%Y%m%d"))
        return

    if symbol_type == "futures":
        url = (
            cons.DCE_DAILY_URL
            + "?"
            + urllib.parse.urlencode(
                {
                    "currDate": day.strftime("%Y%m%d"),
                    "year": day.strftime("%Y"),
                    "month": str(int(day.strftime("%m")) - 1),
                    "day": day.strftime("%d"),
                }
            )
        )
        listed_columns = cons.DCE_COLUMNS
        output_columns = cons.OUTPUT_COLUMNS
    elif symbol_type == "option":
        url = (
            cons.DCE_DAILY_URL
            + "?"
            + urllib.parse.urlencode(
                {
                    "currDate": day.strftime("%Y%m%d"),
                    "year": day.strftime("%Y"),
                    "month": str(int(day.strftime("%m")) - 1),
                    "day": day.strftime("%d"),
                    "dayQuotes.trade_type": "1",
                }
            )
        )
        listed_columns = cons.DCE_OPTION_COLUMNS
        output_columns = cons.OPTION_OUTPUT_COLUMNS
    else:
        print(
            "invalid symbol_type :"
            + symbol_type
            + ', should be one of "futures" or "option"'
        )
        return

    try:
        response = requests_link(url, method="post", headers=cons.headers).text
    except requests.exceptions.ContentDecodingError as reason:
        return get_dce_daily(day, retries=retries + 1)
    except requests.exceptions.HTTPError as reason:
        if reason.response == 504:
            return get_dce_daily(day, retries=retries + 1)
        elif reason.response != 404:
            print(cons.DCE_DAILY_URL, reason)
        return

    if "错误：您所请求的网址（URL）无法获取" in response:
        return get_dce_daily(day, retries=retries + 1)
    elif "暂无数据" in response:
        return

    data = BeautifulSoup(response, "html.parser").find_all("tr")
    if len(data) == 0:
        return

    dict_data = list()
    implied_data = list()
    for i_data in data[1:]:
        if "小计" in i_data.text or "总计" in i_data.text:
            continue
        x = i_data.find_all("td")
        if symbol_type == "futures":
            row_dict = {"variety": cons.DCE_MAP[x[0].text.strip()]}
            row_dict["symbol"] = row_dict["variety"] + x[1].text.strip()
            for i, field in enumerate(listed_columns):
                field_content = x[i + 2].text.strip()
                if "-" in field_content:
                    row_dict[field] = 0
                elif field in ["volume", "open_interest"]:
                    row_dict[field] = int(field_content.replace(",", ""))
                else:
                    row_dict[field] = float(field_content.replace(",", ""))
            dict_data.append(row_dict)
        elif len(x) == 16:
            m = cons.FUTURES_SYMBOL_PATTERN.match(x[1].text.strip())
            if not m:
                continue
            row_dict = {
                "symbol": x[1].text.strip(),
                "variety": m.group(1).upper(),
                "contract_id": m.group(0),
            }
            for i, field in enumerate(listed_columns):
                field_content = x[i + 2].text.strip()
                if "-" in field_content:
                    row_dict[field] = 0
                elif field in ["volume", "open_interest"]:
                    row_dict[field] = int(field_content.replace(",", ""))
                else:
                    row_dict[field] = float(field_content.replace(",", ""))
            dict_data.append(row_dict)
        elif len(x) == 2:
            implied_data.append(
                {
                    "contract_id": x[0].text.strip(),
                    "implied_volatility": float(x[1].text.strip()),
                }
            )
    df = pd.DataFrame(dict_data)
    df["date"] = day.strftime("%Y%m%d")
    if symbol_type == "futures":
        return df[output_columns]
    else:
        return pd.merge(
            df,
            pd.DataFrame(implied_data),
            on="contract_id",
            how="left",
            indicator=False,
        )[output_columns]


def get_futures_daily(start_day=None, end_day=None, market="CFFEX", index_bar=False):
    """
    交易所日交易数据
    Parameters
    ------
        start_day: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        end_day: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        market: 'CFFEX' 中金所, 'CZCE' 郑商所,  'SHFE' 上期所, 'DCE' 大商所 之一, 'INE' 上海国际能源交易中心。默认为中金所
        index_bar: bool  是否合成指数K线
    Return
    -------
        DataFrame
            中金所日交易数据(DataFrame):
                symbol      合约代码
                date       日期
                open       开盘价
                high       最高价
                low       最低价
                close      收盘价
                volume      成交量
                open_interest 持仓量
                turnover    成交额
                settle     结算价
                pre_settle   前结算价
                variety     合约类别
        或 None(给定日期没有交易数据)
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
        return

    start_day = (
        cons.convert_date(start_day) if start_day is not None else datetime.date.today()
    )
    end_day = (
        cons.convert_date(end_day)
        if end_day is not None
        else cons.convert_date(cons.get_latest_data_date(datetime.datetime.now()))
    )

    df_list = list()
    while start_day <= end_day:
        df = f(start_day)
        if df is not None:
            df_list.append(df)
            if index_bar:
                df_list.append(get_futures_index(df))
        start_day += datetime.timedelta(days=1)

    if len(df_list) > 0:
        return pd.concat(df_list).reset_index(drop=True)


def get_futures_index(df):
    """
    指数日交易数据
    :param df: 爬到的原始合约日线行情
    :type df: pandas.DataFrame
    :return: 持仓量加权指数日线行情
    :rtype: pandas.DataFrame
    中金所日交易数据(DataFrame):
    symbol      合约代码
    date       日期
    open       开盘价
    high       最高价
    low       最低价
    close      收盘价
    volume      成交量
    open_interest 持仓量
    turnover    成交额
    settle     结算价
    pre_settle   前结算价
    variety     合约类别
    """
    index_dfs = []
    for var in set(df["variety"]):
        df_cut = df[df["variety"] == var]
        df_cut = df_cut[df_cut["open_interest"] != 0]
        df_cut = df_cut[df_cut["close"] != ""]
        df_cut = df_cut[df_cut["volume"] != 0]
        if len(df_cut.index) > 0:
            index_df = pd.Series(index=df_cut.columns)
            index_df[["volume", "open_interest", "turnover"]] = df_cut[
                ["volume", "open_interest", "turnover"]
            ].sum()
            index_df[["open", "high", "low", "close", "settle", "pre_settle"]] = np.dot(
                np.array(
                    df_cut[["open", "high", "low", "close", "settle", "pre_settle"]]
                ).T,
                np.array((df_cut["open_interest"])),
            ) / np.sum(df_cut["open_interest"])
            index_df[["date", "variety"]] = df_cut[["date", "variety"]].iloc[0, :]
            index_df["symbol"] = index_df["variety"] + "99"
            index_dfs.append(index_df)
    return pd.concat(index_dfs, axis=1).T


if __name__ == "__main__":
    get_futures_daily_df = get_futures_daily(
        start_day="20200310", end_day="20200312", market="DCE", index_bar=True
    )
    print(get_futures_daily_df)
    get_dce_daily_df = get_dce_daily(date=None, symbol_type="futures", retries=0)
    print(get_dce_daily_df)

