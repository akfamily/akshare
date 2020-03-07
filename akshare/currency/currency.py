# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/3/6 16:41
contact: jindaxiang@163.com
desc: https://currencyscoop.com/
https://currencyscoop.com/
"""
import pandas as pd
import requests


def currency_latest(
    base="USD", api_key=""
) -> pd.DataFrame:
    """
    Latest data from currencyscoop.com
    https://currencyscoop.com/api-documentation
    :param base: The base currency you would like to use for your rates
    :type base: str
    :param api_key: Account -> Account Details -> API KEY (use as password in external tools)
    :type api_key: str
    :return: Latest data of base currency
    :rtype: pandas.DataFrame
    """
    payload = {"base": base, "api_key": api_key}
    url = "https://api.currencyscoop.com/v1/latest"
    r = requests.get(url, params=payload)
    temp_df = pd.DataFrame.from_dict(r.json()["response"])
    temp_df["date"] = pd.to_datetime(temp_df["date"])
    return temp_df


def currency_history(
    base="USD", date="2020-02-03", api_key=""
) -> pd.DataFrame:
    """
    Latest data from currencyscoop.com
    https://currencyscoop.com/api-documentation
    :param base: The base currency you would like to use for your rates
    :type base: str
    :param date: Specific date, e.g., "2020-02-03"
    :type date: str
    :param api_key: Account -> Account Details -> API KEY (use as password in external tools)
    :type api_key: str
    :return: Latest data of base currency
    :rtype: pandas.DataFrame
    """
    payload = {"base": base, "date": date, "api_key": api_key}
    url = "https://api.currencyscoop.com/v1/historical"
    r = requests.get(url, params=payload)
    temp_df = pd.DataFrame.from_dict(r.json()["response"])
    temp_df["date"] = pd.to_datetime(temp_df["date"])
    return temp_df


def currency_time_series(
    base="USD",
    start_date="2020-02-03",
    end_date="2020-03-04",
    api_key="",
) -> pd.DataFrame:
    """
    Time-series data from currencyscoop.com
    P.S. need special authority
    https://currencyscoop.com/api-documentation
    :param base: The base currency you would like to use for your rates
    :type base: str
    :param start_date: Specific date, e.g., "2020-02-03"
    :type start_date: str
    :param end_date: Specific date, e.g., "2020-02-03"
    :type end_date: str
    :param api_key: Account -> Account Details -> API KEY (use as password in external tools)
    :type api_key: str
    :return: Latest data of base currency
    :rtype: pandas.DataFrame
    """
    payload = {
        "base": base,
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
    }
    url = "https://api.currencyscoop.com/v1/timeseries"
    r = requests.get(url, params=payload)
    temp_df = pd.DataFrame.from_dict(r.json()["response"])
    temp_df["date"] = pd.to_datetime(temp_df["date"])
    return temp_df


def currency_currencies(
    c_type="fiat", api_key=""
) -> pd.DataFrame:
    """
    currencies data from currencyscoop.com
    https://currencyscoop.com/api-documentation
    :param c_type: now only "fiat" can return data
    :type c_type: str
    :param api_key: Account -> Account Details -> API KEY (use as password in external tools)
    :type api_key: str
    :return: Latest data of base currency
    :rtype: pandas.DataFrame
    """
    payload = {"type": c_type, "api_key": api_key}
    url = "https://api.currencyscoop.com/v1/currencies"
    r = requests.get(url, params=payload)
    temp_df = pd.DataFrame.from_dict(r.json()["response"]["fiats"]).T
    return temp_df


def currency_convert(
    base="USD", to="CNY", amount="10000", api_key=""
) -> pd.DataFrame:
    """
    currencies data from currencyscoop.com
    https://currencyscoop.com/api-documentation
    :param base: The base currency you would like to use for your rates
    :type base: str
    :param to: The currency you would like to use for your rates
    :type to: str
    :param amount: The amount of base currency
    :type amount: str
    :param api_key: Account -> Account Details -> API KEY (use as password in external tools)
    :type api_key: str
    :return: Latest data of base currency
    :rtype: pandas.Series
    """
    payload = {
        "base": base,
        "to": to,
        "amount": amount,
        "api_key": api_key,
    }
    url = "https://api.currencyscoop.com/v1/convert"
    r = requests.get(url, params=payload)
    temp_se = pd.Series(r.json()["response"])
    temp_se["timestamp"] = pd.to_datetime(temp_se["timestamp"], unit="s")
    return temp_se


if __name__ == "__main__":
    currency_latest_df = currency_latest(
        base="USD", api_key="e2cd623e630613c89ba9cee546ae5108"
    )
    print(currency_latest_df)
    currency_history_df = currency_history(
        base="USD", date="2020-02-03", api_key="e2cd623e630613c89ba9cee546ae5108"
    )
    print(currency_history_df)
    # currency_time_series_df = currency_time_series(
    #     base="USD",
    #     start_date="2020-02-03",
    #     end_date="2020-03-04",
    #     api_key="e2cd623e630613c89ba9cee546ae5108",
    # )
    # print(currency_time_series_df)
    currency_currencies_df = currency_currencies(
        c_type="fiat", api_key="e2cd623e630613c89ba9cee546ae5108"
    )
    print(currency_currencies_df)
    currency_convert_df = currency_convert(
        base="USD", to="CNY", amount="10000", api_key="e2cd623e630613c89ba9cee546ae5108"
    )
    print(currency_convert_df)
