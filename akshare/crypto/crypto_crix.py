#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/6/24 16:08
Desc: CRIX 和 VCRIX 指数
https://thecrix.de/
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def crypto_crix(symbol: str = "CRIX") -> pd.DataFrame:
    """
    CRIX 和 VCRIX 指数
    https://thecrix.de/
    :param symbol: choice of {"CRIX", "VCRIX"}
    :type symbol: str
    :return: CRIX 和 VCRIX 指数
    :rtype: pandas.DataFrame
    """
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    url: str = "https://thecrix.de/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find_all("script")[12].string
    if symbol == "CRIX":
        inner_text = data_text[data_text.find("series") : data_text.find("CRIX")]
        temp_df = pd.DataFrame(
            list(
                eval(
                    inner_text[
                        inner_text.find("data") + 5 : inner_text.find("name")
                    ].strip()
                )
            )[0]
        )
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms").dt.date
        return temp_df

    else:
        data_text = data_text[
            data_text.find("VCRIX IndeX") : data_text.find("2014-11-28")
        ]
        inner_text = data_text[data_text.find("series") : data_text.find('"VCRIX"')]
        temp_df = pd.DataFrame(
            list(
                eval(
                    inner_text[
                        inner_text.find("data") + 5 : inner_text.find("name")
                    ].strip()
                )
            )[0]
        )
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms").dt.date
        return temp_df


if __name__ == "__main__":
    crypto_crix_df = crypto_crix(symbol="CRIX")
    print(crypto_crix_df)
