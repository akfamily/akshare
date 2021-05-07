# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/7 15:58
Desc: Drewry集装箱指数
https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry
"""
import pandas as pd
import requests


def drewry_wci_index() -> pd.DataFrame:
    """
    Drewry 集装箱指数
    https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry
    :return: Drewry集装箱指数
    :rtype: pandas.DataFrame
    """
    url = "https://api.chartblocks.com/v1/chart/data/6083e35c3ba0f6256a0afae3?t=733e658870e7bec"
    r = requests.get(url)
    data_json = r.json()
    data_text = data_json["data"]["series"]["ds-0"]["raw"]
    temp_df = pd.DataFrame(data_text)
    temp_df.columns = ["wci", "date"]
    temp_df = temp_df.applymap(
        lambda x: x.replace(",", "").replace("$", "") if type(x) == str else x
    )
    temp_df = temp_df.astype({"wci": float})
    temp_df["date"] = pd.to_datetime(temp_df["date"])
    temp_df = temp_df[
        [
            "date",
            "wci",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    drewry_wci_index_df = drewry_wci_index()
    print(drewry_wci_index_df)
