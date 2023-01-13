# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/1/13 21:12
Desc: 网易财经-行情首页-沪深 A 股-每日行情
https://quotes.money.163.com/old/#query=EQA&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0
"""
import pandas as pd
import requests


def stock_zh_a_hist_163(
    symbol: str = "sh601318",
    start_date: str = "10700101",
    end_date: str = "20500101",
) -> pd.DataFrame:
    """
    网易财经-行情首页-沪深 A 股-每日行情
    注意：该接口只返回未复权数据
    https://quotes.money.163.com/trade/lsjysj_601318.html?year=2022&season=2
    :param symbol: 带市场表示的股票代码
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    url = "http://quotes.money.163.com/service/chddata.html"
    params = {
        "code": "0601318",
        "start": start_date,
        "end": end_date,
        "fields": "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP",
    }
    if "sh" in symbol:
        params.update({"code": f"0{symbol[2:]}"})
    else:
        params.update({"code": f"1{symbol[2:]}"})
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "quotes.money.163.com",
        "Pragma": "no-cache",
        "Referer": "http://quotes.money.163.com/trade/lsjysj_300254.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    r.encoding = "gbk"
    data_text = r.text
    temp_df = pd.DataFrame(
        [item.split(",") for item in data_text.split("\r\n")[1:]]
    )
    temp_df.columns = [
        "日期",
        "股票代码",
        "名称",
        "收盘价",
        "最高价",
        "最低价",
        "开盘价",
        "前收盘",
        "涨跌额",
        "涨跌幅",
        "换手率",
        "成交量",
        "成交金额",
        "总市值",
        "流通市值",
    ]
    temp_df["股票代码"] = temp_df["股票代码"].str.strip("'").str.strip()
    temp_df["名称"] = temp_df["名称"].str.strip()
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["收盘价"] = pd.to_numeric(temp_df["收盘价"], errors="coerce")
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
    temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
    temp_df["前收盘"] = pd.to_numeric(temp_df["前收盘"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交金额"] = pd.to_numeric(temp_df["成交金额"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    temp_df.dropna(subset=["日期"], inplace=True)
    temp_df.sort_values("日期", inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    stock_zh_a_hist_163_df = stock_zh_a_hist_163(
        symbol="sh000001", start_date="20201029", end_date="20220517"
    )
    print(stock_zh_a_hist_163_df)

    stock_zh_a_hist_163_df = stock_zh_a_hist_163(symbol="sh600587")
    print(stock_zh_a_hist_163_df)
