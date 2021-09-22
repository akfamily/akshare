# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/5/7 15:58
Desc: Drewry集装箱指数
https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry
https://infogram.com/world-container-index-1h17493095xl4zj
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from akshare.utils import demjson


def drewry_wci_index():
    """
    Drewry 集装箱指数
    https://infogram.com/world-container-index-1h17493095xl4zj
    :return: Drewry 集装箱指数
    :rtype: pandas.DataFrame
    """
    url = "https://infogram.com/world-container-index-1h17493095xl4zj"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find_all('script')[-5].string.strip("window.infographicData=")[:-1]
    data_json = demjson.decode(data_text)
    temp_df = pd.DataFrame(data_json['elements'][2]['data'][0])
    temp_df = temp_df.iloc[1:, :]
    temp_df.columns = ['date', 'wci']
    day = temp_df['date'].str.split("-", expand=True).iloc[:, 0].str.strip()
    month = temp_df['date'].str.split("-", expand=True).iloc[:, 1].str.strip()
    year = temp_df['date'].str.split("-", expand=True).iloc[:, 2].str.strip()
    temp_df['date'] = day + "-" + month + "-" + year
    temp_df['date'] = pd.to_datetime(temp_df['date']).dt.date
    temp_df['wci'] = pd.to_numeric(temp_df['wci'], errors="coerce")
    return temp_df


# def drewry_wci_index() -> pd.DataFrame:
#     """
#     Drewry 集装箱指数
#     https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry
#     :return: Drewry 集装箱指数
#     :rtype: pandas.DataFrame
#     """
#     url = "https://api.chartblocks.com/v1/chart/data/6083e35c3ba0f6256a0afae3"
#     r = requests.get(url)
#     data_json = r.json()
#     data_text = data_json["data"]["series"]["ds-0"]["raw"]
#     temp_df = pd.DataFrame(data_text)
#     temp_df.columns = ["wci", "date"]
#     temp_df = temp_df.applymap(
#         lambda x: x.replace(",", "").replace("$", "") if type(x) == str else x
#     )
#     temp_df = temp_df.astype({"wci": float})
#     temp_df["date"] = pd.to_datetime(temp_df["date"])
#     temp_df = temp_df[
#         [
#             "date",
#             "wci",
#         ]
#     ]
#     return temp_df


if __name__ == "__main__":
    drewry_wci_index_df = drewry_wci_index()
    print(drewry_wci_index_df)
