#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/5/11 17:52
Desc: 加密货币
https://cn.investing.com/crypto/currencies
高频数据
https://bitcoincharts.com/about/markets-api/
"""
import math

import pandas as pd
import requests
from tqdm import tqdm

from akshare.datasets import get_crypto_info_csv


def crypto_name_url_table(symbol: str = "web") -> pd.DataFrame:
    """
    加密货币名称、代码和 ID，每次更新较慢
    https://cn.investing.com/crypto/ethereum/historical-data
    :param symbol: choice of {"web", "local"}; web 表示从网页获取最新，local 表示利用本地本文件
    :type symbol: str
    :return: 加密货币名称、代码和 ID
    :rtype: pandas.DataFrame
    """
    if symbol == "web":
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = "https://cn.investing.com/crypto/Service/LoadCryptoCurrencies"
        payload = {
            'draw': '14',
            'columns[0][data]': 'currencies_order',
            'columns[0][name]': 'currencies_order',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': 'function',
            'columns[1][name]': 'crypto_id',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'false',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': 'function',
            'columns[2][name]': 'name',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': 'symbol',
            'columns[3][name]': 'symbol',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': 'function',
            'columns[4][name]': 'price_usd',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'columns[5][data]': 'market_cap_formatted',
            'columns[5][name]': 'market_cap_usd',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'true',
            'columns[5][search][value]': '',
            'columns[5][search][regex]': 'false',
            'columns[6][data]': '24h_volume_formatted',
            'columns[6][name]': '24h_volume_usd',
            'columns[6][searchable]': 'true',
            'columns[6][orderable]': 'true',
            'columns[6][search][value]': '',
            'columns[6][search][regex]': 'false',
            'columns[7][data]': 'total_volume',
            'columns[7][name]': 'total_volume',
            'columns[7][searchable]': 'true',
            'columns[7][orderable]': 'true',
            'columns[7][search][value]': '',
            'columns[7][search][regex]': 'false',
            'columns[8][data]': 'change_percent_formatted',
            'columns[8][name]': 'change_percent',
            'columns[8][searchable]': 'true',
            'columns[8][orderable]': 'true',
            'columns[8][search][value]': '',
            'columns[8][search][regex]': 'false',
            'columns[9][data]': 'percent_change_7d_formatted',
            'columns[9][name]': 'percent_change_7d',
            'columns[9][searchable]': 'true',
            'columns[9][orderable]': 'true',
            'columns[9][search][value]': '',
            'columns[9][search][regex]': 'false',
            'order[0][column]': 'currencies_order',
            'order[0][dir]': 'asc',
            'start': '0',
            'length': '100',
            'search[value]': '',
            'search[regex]': 'false',
            'currencyId': '12',
        }
        r = requests.post(url, data=payload, headers=headers)
        data_json = r.json()
        total_page = math.ceil(int(data_json['recordsTotal']) / 100)
        big_df = pd.DataFrame()
        for page in tqdm(range(1, total_page+1), leave=False):
            payload.update({
                "start": (page-1)*100,
                'length': 100
            })
            r = requests.post(url, data=payload, headers=headers)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json['data'])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        big_df = big_df[[
            'symbol',
            'name',
            'name_trans',
            'sml_id',
            'related_pair_ID',
        ]]
        return big_df
    else:
        get_crypto_info_csv_path = get_crypto_info_csv()
        name_url_df = pd.read_csv(get_crypto_info_csv_path)
        return name_url_df


def crypto_hist(
    symbol: str = "BTC",
    period: str = "每日",
    start_date: str = "20191020",
    end_date: str = "20201020",
):
    """
    加密货币历史数据
    https://cn.investing.com/crypto/ethereum/historical-data
    :param symbol: 货币名称
    :type symbol: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: '20151020', 注意格式
    :type start_date: str
    :param end_date: '20201020', 注意格式
    :type end_date: str
    :return: 加密货币历史数据获取
    :rtype: pandas.DataFrame
    """
    import warnings
    warnings.filterwarnings('ignore')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    start_date = "/".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "/".join([end_date[:4], end_date[4:6], end_date[6:]])
    name_url_df = crypto_name_url_table(symbol='local')
    curr_id = name_url_df[name_url_df["symbol"] == symbol]["related_pair_ID"].values[0]
    sml_id = name_url_df[name_url_df["symbol"] == symbol]["sml_id"].values[0]
    url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    payload = {
        "curr_id": curr_id,
        "smlID": sml_id,
        "header": "null",
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": period_map[period],
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    r = requests.post(url, data=payload, headers=headers)

    temp_df = pd.read_html(r.text)[0]
    df_data = temp_df.copy()
    if period == "每月":
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月")
    else:
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    if any(df_data["交易量"].astype(str).str.contains("-")):
        df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][
            df_data["交易量"].str.contains("-")
        ].replace("-", 0)
    if any(df_data["交易量"].astype(str).str.contains("B")):
        df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)]
            .str.replace("B", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000000
        )
    if any(df_data["交易量"].astype(str).str.contains("M")):
        df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)]
            .str.replace("M", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000
        )
    if any(df_data["交易量"].astype(str).str.contains("K")):
        df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)]
            .str.replace("K", "")
            .str.replace(",", "")
            .astype(float)
            * 1000
        )
    df_data["交易量"] = df_data["交易量"].astype(float)
    df_data["涨跌幅"] = pd.DataFrame(
        round(
            df_data["涨跌幅"].str.replace(",", "").str.replace("%", "").astype(float)
            / 100,
            6,
        )
    )
    del df_data["日期"]
    df_data.reset_index(inplace=True)
    df_data = df_data[[
        "日期",
        "收盘",
        "开盘",
        "高",
        "低",
        "交易量",
        "涨跌幅",
    ]]
    df_data['日期'] = pd.to_datetime(df_data['日期']).dt.date
    df_data['收盘'] = pd.to_numeric(df_data['收盘'])
    df_data['开盘'] = pd.to_numeric(df_data['开盘'])
    df_data['高'] = pd.to_numeric(df_data['高'])
    df_data['低'] = pd.to_numeric(df_data['低'])
    df_data['交易量'] = pd.to_numeric(df_data['交易量'])
    df_data['涨跌幅'] = pd.to_numeric(df_data['涨跌幅'])
    df_data.sort_values('日期', inplace=True)
    df_data.reset_index(inplace=True, drop=True)
    return df_data


if __name__ == "__main__":
    crypto_name_url_table_df = crypto_name_url_table(symbol="local")
    print(crypto_name_url_table_df)

    crypto_hist_df = crypto_hist(
        symbol="BTC", period="每日", start_date="20151020", end_date="20220511"
    )
    print(crypto_hist_df)
