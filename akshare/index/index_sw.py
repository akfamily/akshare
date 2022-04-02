#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/1/26 13:10
Desc: 申万指数-申万一级、二级和三级
http://www.swsindex.com/IdxMain.aspx
https://legulegu.com/stockdata/index-composition?industryCode=851921.SI
"""
import time
import json

import pandas as pd
from akshare.utils import demjson
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import sw_headers, sw_payload, sw_url


def sw_index_representation_spot() -> pd.DataFrame:
    """
    申万-市场表征实时行情数据
    http://www.swsindex.com/idx0120.aspx?columnid=8831
    :return: 市场表征实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.swsindex.com/handler.aspx"
    params = {
        "tablename": "swzs",
        "key": "L1",
        "p": "1",
        "where": "L1 in('801001','801002','801003','801005','801300','801901','801903','801905','801250','801260','801270','801280','802613')",
        "orderby": "",
        "fieldlist": "L1,L2,L3,L4,L5,L6,L7,L8,L11",
        "pagecount": "9",
        "timed": "1632300641756",
    }
    r = requests.get(url, params=params)
    data_json = demjson.decode(r.text)
    temp_df = pd.DataFrame(data_json["root"])
    temp_df.columns = ["指数代码", "指数名称", "昨收盘", "今开盘", "成交额", "最高价", "最低价", "最新价", "成交量"]
    temp_df["昨收盘"] = pd.to_numeric(temp_df["昨收盘"])
    temp_df["今开盘"] = pd.to_numeric(temp_df["今开盘"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"])
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    return temp_df


def sw_index_spot() -> pd.DataFrame:
    """
    申万一级行业-实时行情数据
    http://www.swsindex.com/idx0120.aspx?columnid=8832
    :return: 申万一级行业实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.swsindex.com/handler.aspx"
    result = []
    for i in range(1, 3):
        payload = sw_payload.copy()
        payload.update({"p": i})
        payload.update({"timed": int(time.time() * 1000)})
        r = requests.post(url, headers=sw_headers, data=payload)
        data = r.content.decode()
        data = data.replace("'", '"')
        data = json.loads(data)
        result.extend(data["root"])
    temp_df = pd.DataFrame(result)
    temp_df["L2"] = temp_df["L2"].str.strip()
    temp_df.columns = ["指数代码", "指数名称", "昨收盘", "今开盘", "成交额", "最高价", "最低价", "最新价", "成交量"]
    temp_df["昨收盘"] = pd.to_numeric(temp_df["昨收盘"])
    temp_df["今开盘"] = pd.to_numeric(temp_df["今开盘"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"])
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    return temp_df


def sw_index_second_spot() -> pd.DataFrame:
    """
    申万二级行业-实时行情数据
    http://www.swsindex.com/idx0120.aspx?columnId=8833
    :return: 申万二级行业-实时行情数据
    :rtype: pandas.DataFrame
    """
    result = []
    for i in range(1, 6):
        payload = {
            "tablename": "swzs",
            "key": "L1",
            "p": "1",
            "where": "L1 in('801011','801012','801013','801014','801015','801016','801021','801022','801023','801032','801033','801034','801035','801036','801037','801041','801051','801072','801073','801074','801075','801081','801082','801083','801084','801092','801093','801094','801101','801102','801111','801112','801123','801131','801132','801141','801142','801143','801151','801152','801153','801154','801155','801156','801161','801162','801163','801164','801171','801172','801173','801174','801175','801176','801177','801178','801181','801182','801191','801192','801193','801194','801202','801211','801212','801213','801214','801222','801223','801053','801054','801055','801076','801203','801204','801205','801711','801712','801713','801721','801722','801723','801724','801725','801731','801732','801733','801734','801741','801742','801743','801744','801751','801752','801761','801881','801017','801018')",
            "orderby": "",
            "fieldlist": "L1,L2,L3,L4,L5,L6,L7,L8,L11",
            "pagecount": "98",
            "timed": "",
        }
        payload.update({"p": i})
        payload.update({"timed": int(time.time() * 1000)})
        r = requests.post(sw_url, headers=sw_headers, data=payload)
        data = r.content.decode()
        data = data.replace("'", '"')
        data = json.loads(data)
        result.extend(data["root"])
    temp_df = pd.DataFrame(result)
    temp_df["L2"] = temp_df["L2"].str.strip()
    temp_df.columns = ["指数代码", "指数名称", "昨收盘", "今开盘", "成交额", "最高价", "最低价", "最新价", "成交量"]
    temp_df["昨收盘"] = pd.to_numeric(temp_df["昨收盘"])
    temp_df["今开盘"] = pd.to_numeric(temp_df["今开盘"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"])
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    return temp_df


def sw_index_cons(symbol: str = "801011") -> pd.DataFrame:
    """
    申万指数成份信息-包括一级和二级行业都可以查询
    http://www.swsindex.com/idx0210.aspx?swindexcode=801010
    :param symbol: 指数代码
    :type symbol: str
    :return: 申万指数成份信息
    :rtype: pandas.DataFrame
    """
    url = f"http://www.swsindex.com/downfile.aspx?code={symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
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
    temp_df = pd.DataFrame(data)
    temp_df["start_date"] = pd.to_datetime(temp_df["start_date"]).dt.date
    temp_df["weight"] = pd.to_numeric(temp_df["weight"])
    return temp_df


def sw_index_daily(
    symbol: str = "801011",
    start_date: str = "20191201",
    end_date: str = "20201207",
) -> pd.DataFrame:
    """
    申万指数一级和二级日频率行情数据
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param symbol: 申万指数
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 申万指数日频率行情数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.swsindex.com/excel2.aspx"
    params = {
        "ctable": "swindexhistory",
        "where": f" swindexcode in ('{symbol}') and BargainDate >= '{start_date}' and BargainDate <= '{end_date}'",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 10:
            symbol = cols[0].text
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
                    "index_code": symbol.replace(",", ""),
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
    temp_df = pd.DataFrame(data)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"])
    temp_df["high"] = pd.to_numeric(temp_df["high"])
    temp_df["low"] = pd.to_numeric(temp_df["low"])
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["vol"] = pd.to_numeric(temp_df["vol"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"])
    temp_df["change_pct"] = pd.to_numeric(temp_df["change_pct"])
    return temp_df


def sw_index_daily_indicator(
    symbol: str = "801011",
    start_date: str = "20191201",
    end_date: str = "20210907",
    data_type: str = "Day",
) -> pd.DataFrame:
    """
    申万一级和二级行业历史行情指标
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param symbol: 申万指数
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :param data_type: choice of {"Day": 日报表, "Week": 周报表}
    :type data_type: str
    :return: 申万指数不同频率数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.swsindex.com/excel.aspx"
    params = {
        "ctable": "V_Report",
        "where": f" swindexcode in ('{symbol}') and BargainDate >= '{start_date}' and BargainDate <= '{end_date}' and type='{data_type}'",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 14:
            symbol = cols[0].text
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
                    "index_code": symbol,
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
    temp_df = pd.DataFrame(data)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["volume"] = temp_df["volume"].apply(lambda x: x.replace(",", ""))
    temp_df["volume"] = pd.to_numeric(temp_df["volume"])
    temp_df["chg_pct"] = pd.to_numeric(temp_df["chg_pct"])
    temp_df["turn_rate"] = pd.to_numeric(temp_df["turn_rate"])
    temp_df["pe"] = pd.to_numeric(temp_df["pe"])
    temp_df["pb"] = pd.to_numeric(temp_df["pb"])
    temp_df["vwap"] = pd.to_numeric(temp_df["vwap"])
    temp_df["float_mv"] = temp_df["float_mv"].apply(lambda x: x.replace(",", ""))
    temp_df["float_mv"] = pd.to_numeric(
        temp_df["float_mv"],
    )
    temp_df["avg_float_mv"] = temp_df["avg_float_mv"].apply(
        lambda x: x.replace(",", "")
    )
    temp_df["avg_float_mv"] = pd.to_numeric(temp_df["avg_float_mv"])
    temp_df["dividend_yield_ratio"] = pd.to_numeric(temp_df["dividend_yield_ratio"])
    temp_df["turnover_pct"] = pd.to_numeric(temp_df["turnover_pct"])
    return temp_df


def sw_index_third_info() -> pd.DataFrame:
    """
    乐咕乐股-申万三级-分类
    https://legulegu.com/stockdata/sw-industry-overview#level1
    :return: 分类
    :rtype: pandas.DataFrame
    """
    url = "https://legulegu.com/stockdata/sw-industry-overview"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    code_raw = soup.find("div", attrs={"id": "level3Items"}).find_all(
        "div", attrs={"class": "lg-industries-item-chinese-title"}
    )
    name_raw = soup.find("div", attrs={"id": "level3Items"}).find_all(
        "div", attrs={"class": "lg-industries-item-number"}
    )
    value_raw = soup.find("div", attrs={"id": "level3Items"}).find_all(
        "div", attrs={"class": "lg-sw-industries-item-value"}
    )
    code = [item.get_text() for item in code_raw]
    name = [item.get_text().split("(")[0] for item in name_raw]
    num = [item.get_text().split("(")[1].split(")")[0] for item in name_raw]
    num_1 = [
        item.find_all("span", attrs={"class": "value"})[0].get_text().strip()
        for item in value_raw
    ]
    num_2 = [
        item.find_all("span", attrs={"class": "value"})[1].get_text().strip()
        for item in value_raw
    ]
    num_3 = [
        item.find_all("span", attrs={"class": "value"})[2].get_text().strip()
        for item in value_raw
    ]
    num_4 = [
        item.find_all("span", attrs={"class": "value"})[3].get_text().strip()
        for item in value_raw
    ]
    temp_df = pd.DataFrame([code, name, num, num_1, num_2, num_3, num_4]).T
    temp_df.columns = [
        "行业代码",
        "行业名称",
        "成份个数",
        "静态市盈率",
        "TTM(滚动)市盈率",
        "市净率",
        "静态股息率",
    ]
    temp_df["成份个数"] = pd.to_numeric(temp_df["成份个数"])
    temp_df["静态市盈率"] = pd.to_numeric(temp_df["静态市盈率"])
    temp_df["TTM(滚动)市盈率"] = pd.to_numeric(temp_df["TTM(滚动)市盈率"])
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"])
    temp_df["静态股息率"] = pd.to_numeric(temp_df["静态股息率"])
    return temp_df


def sw_index_third_cons(symbol: str = "851921.SI") -> pd.DataFrame:
    """
    乐咕乐股-申万三级-行业成份
    https://legulegu.com/stockdata/index-composition?industryCode=851921.SI
    :param symbol: 三级行业的行业代码
    :type symbol: str
    :return: 行业成份
    :rtype: pandas.DataFrame
    """
    url = f"https://legulegu.com/stockdata/index-composition?industryCode={symbol}"
    temp_df = pd.read_html(url)[0]
    temp_df.columns = [
        "序号",
        "股票代码",
        "股票简称",
        "纳入时间",
        "申万1级",
        "申万2级",
        "申万3级",
        "价格",
        "市盈率",
        "市盈率ttm",
        "市净率",
        "股息率",
        "市值",
    ]
    temp_df["价格"] = pd.to_numeric(temp_df["价格"], errors="coerce")
    temp_df["市盈率"] = pd.to_numeric(temp_df["市盈率"], errors="coerce")
    temp_df["市盈率ttm"] = pd.to_numeric(temp_df["市盈率ttm"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["股息率"] = pd.to_numeric(temp_df["股息率"].str.strip("%"), errors="coerce")
    temp_df["市值"] = pd.to_numeric(temp_df["市值"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    sw_index_representation_spot_df = sw_index_representation_spot()
    print(sw_index_representation_spot_df)

    sw_index_spot_df = sw_index_spot()
    print(sw_index_spot_df)

    sw_index_second_spot_df = sw_index_second_spot()
    print(sw_index_second_spot_df)

    sw_index_cons_df = sw_index_cons(symbol="801011")
    print(sw_index_cons_df)

    sw_index_daily_df = sw_index_daily(
        symbol="801010", start_date="20191201", end_date="20191207"
    )
    print(sw_index_daily_df)

    sw_index_daily_indicator_df = sw_index_daily_indicator(
        symbol="801003",
        start_date="20191101",
        end_date="20191207",
        data_type="Week",
    )
    print(sw_index_daily_indicator_df)

    sw_index_third_info_df = sw_index_third_info()
    print(sw_index_third_info_df)

    sw_index_third_cons_df = sw_index_third_cons(symbol="851921.SI")
    print(sw_index_third_cons_df)
