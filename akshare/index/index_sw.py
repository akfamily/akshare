# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/11/29 13:34
Desc: 获取申万指数-申万一级
http://www.swsindex.com/IdxMain.aspx
"""
import time
import json
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import sw_headers, sw_payload, sw_url, sw_cons_headers


def sw_index_spot() -> pd.DataFrame:
    """
    申万一级行业实时行情数据
    http://www.swsindex.com/idx0120.aspx?columnid=8832
    :return: 申万一级行业实时行情数据
    :rtype: pandas.DataFrame
    """
    result = []
    for i in range(1, 3):
        payload = sw_payload.copy()
        payload.update({"p": i})
        payload.update({"timed": int(time.time() * 1000)})
        req = requests.post(sw_url, headers=sw_headers, data=payload)
        data = req.content.decode()
        data = data.replace("'", '"')
        data = json.loads(data)
        result.extend(data["root"])
    result = pd.DataFrame(result)
    result["L2"] = result["L2"].str.strip()
    result.columns = ["指数代码", "指数名称", "昨收盘", "今开盘", "成交额", "最高价", "最低价", "最新价", "成交量"]
    return result


def sw_index_cons(index_code: str = "801010") -> pd.DataFrame:
    """
    申万指数成份信息
    http://www.swsindex.com/idx0210.aspx?swindexcode=801010
    :param index_code: 指数代码
    :type index_code: str
    :return: 申万指数成份信息
    :rtype: pandas.DataFrame
    """
    url = f"http://www.swsindex.com/downfile.aspx?code={index_code}"
    res = requests.get(url)
    if res is not None:
        soup = BeautifulSoup(res.text, "html5lib")
        data = []
        table = soup.findAll("table")[0]
        rows = table.findAll("tr")
        for row in rows:
            cols = row.findAll("td")
            if len(cols) >= 4:
                stock_code = cols[0].text
                stock_name = cols[1].text
                weight = cols[2].text
                start_date = cols[3].text

                data.append(
                    {
                        "stock_code": stock_code,
                        "stock_name": stock_name,
                        "start_date": start_date,
                        "weight": weight,
                    }
                )
        df = pd.DataFrame(data)
        if len(df) > 0:
            df["start_date"] = df["start_date"].apply(
                lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S")
            )
        return df
    return "获取数据失败"


def sw_index_daily(
    index_code: str = "801010",
    start_date: str = "2019-12-01",
    end_date: str = "2019-12-07",
) -> pd.DataFrame:
    """
    申万指数日频率行情数据
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param index_code: 申万指数
    :type index_code: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 申万指数日频率行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.swsindex.com/excel2.aspx?ctable=swindexhistory&where=%s "
    where_cond = (
        " swindexcode in ('%s') and BargainDate >= '%s' and BargainDate <= '%s'"
        % (index_code, start_date, end_date)
    )
    url = url % where_cond
    # print(url)

    response = requests.get(url).text
    if response is None:
        return None, "获取数据失败"

    soup = BeautifulSoup(response, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 10:
            index_code = cols[0].text
            index_name = cols[1].text
            date = cols[2].text
            open_ = cols[3].text
            high = cols[4].text
            low = cols[5].text
            close = cols[6].text
            vol = cols[7].text
            amount = cols[8].text
            change_pct = cols[9].text

            data.append(
                {
                    "index_code": index_code.replace(",", ""),
                    "index_name": index_name.replace(",", ""),
                    "date": date.replace(",", ""),
                    "open": open_.replace(",", ""),
                    "high": high.replace(",", ""),
                    "low": low.replace(",", ""),
                    "close": close.replace(",", ""),
                    "vol": vol.replace(",", ""),
                    "amount": amount.replace(",", ""),
                    "change_pct": change_pct.replace(",", ""),
                }
            )

    df = pd.DataFrame(data)
    if len(df) > 0:
        df["date"] = df["date"].apply(
            lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S")
        )
    return df


def sw_index_daily_indicator(
    index_code: str = "801010",
    start_date: str = "2019-12-01",
    end_date: str = "2019-12-07",
    data_type: str = "Day",
) -> pd.DataFrame:
    """
    申万一级行业历史行情指标
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param index_code: 申万指数
    :type index_code: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :param data_type: 频率
    :type data_type: str
    :return: 申万指数不同频率数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.swsindex.com/excel.aspx?ctable=V_Report&where=%s"
    where_cond = (
        "swindexcode in ('%s') and BargainDate >= '%s' and BargainDate <= '%s' and type='%s'"
        % (index_code, start_date, end_date, data_type)
    )
    url = url % where_cond

    response = requests.get(url).text
    if response is None:
        return None, "获取数据失败"

    soup = BeautifulSoup(response, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 14:
            index_code = cols[0].text
            index_name = cols[1].text
            date = cols[2].text
            close = cols[3].text
            volume = cols[4].text
            chg_pct = cols[5].text
            turn_rate = cols[6].text
            pe = cols[7].text
            pb = cols[8].text
            v_wap = cols[9].text
            turnover_pct = cols[10].text
            float_mv = cols[11].text
            avg_float_mv = cols[12].text
            dividend_yield_ratio = cols[13].text

            data.append(
                {
                    "index_code": index_code,
                    "index_name": index_name,
                    "date": date,
                    "close": close,
                    "volume": volume,
                    "chg_pct": chg_pct,
                    "turn_rate": turn_rate,
                    "pe": pe,
                    "pb": pb,
                    "vwap": v_wap,
                    "float_mv": float_mv,
                    "avg_float_mv": avg_float_mv,
                    "dividend_yield_ratio": dividend_yield_ratio,
                    "turnover_pct": turnover_pct,
                }
            )

    df = pd.DataFrame(data)
    if len(df) > 0:
        df["date"] = df["date"].apply(
            lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S")
        )
    return df


if __name__ == "__main__":
    sw_index_df = sw_index_spot()
    print(sw_index_df)
    sw_index_df = sw_index_cons(index_code="801020")
    print(sw_index_df)
    sw_index_df = sw_index_daily(
        index_code="801010", start_date="2019-12-01", end_date="2019-12-07"
    )
    print(sw_index_df)
    sw_index_df = sw_index_daily_indicator(
        index_code="801010",
        start_date="2019-11-01",
        end_date="2019-12-07",
        data_type="Week",
    )
    print(sw_index_df)
