#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/2/8 17:14
Desc: 腾讯运动-冬奥会-历届奖牌榜
https://m.sports.qq.com/g/sv3/winter-oly22/winter-olympic-rank.htm?type=0
"""
import requests
import pandas as pd


def sport_olympic_winter_hist() -> pd.DataFrame:
    """
    腾讯运动-冬奥会-历届奖牌榜
    :return: 历届奖牌榜
    :rtype: pandas.DataFrame
    """
    url = "https://app.sports.qq.com/m/oly/historyMedal"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["list"])
    temp_df = temp_df.explode("list")
    temp_df["国家及地区"] = temp_df["list"].apply(lambda x: (x["noc"]))
    temp_df["金牌数"] = temp_df["list"].apply(lambda x: (int(x["gold"])))
    temp_df["总奖牌数"] = temp_df["list"].apply(lambda x: (int(x["total"])))
    temp_df["举办年份"] = temp_df["year"].astype("str")
    temp_df["届数"] = temp_df["no"].astype("str")
    temp_df["举办地点"] = temp_df["country"]
    temp_df = temp_df[["举办年份", "届数", "举办地点", "国家及地区", "金牌数", "总奖牌数"]]
    temp_df = temp_df.replace("俄罗斯奥委会", "俄罗斯")
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.rename(columns={"index": "序号"}, inplace=True)
    return temp_df


if __name__ == "__main__":
    sport_olympic_winter_hist_df = sport_olympic_winter_hist()
    print(sport_olympic_winter_hist_df)
