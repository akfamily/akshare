# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/11/16 21:12
Desc: 中国电竞价值排行榜
http://rank.uuu9.com/player/ranking
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def club_rank_game(symbol: str = "英雄联盟") -> pd.DataFrame:
    """
    中国电竞价值排行榜-俱乐部排名
    http://rank.uuu9.com/
    :param symbol: choice of {'英雄联盟', '绝地求生', '王者荣耀', 'DOTA2', '穿越火线', '和平精英'}
    :type symbol: str
    :return: 俱乐部排名
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "DOTA2": "1",
        "英雄联盟": "2",
        "绝地求生": "3",
        "王者荣耀": "4",
        "穿越火线": "5",
        "和平精英": "6",
    }
    url = "http://rank.uuu9.com/club/ranking"
    params = {"gameId": symbol_map[symbol], "type": "0"}
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("div", attrs={"class": "ec_data"}).text
    report_date = data_text.split("：")[-1]
    temp_df = pd.read_html(r.text)[0]
    if symbol in {"英雄联盟", "王者荣耀", "DOTA2"}:
        temp_df.columns = [
            "排名",
            "俱乐部名称",
            "人气指数",
            "舆论指数",
            "战绩指数",
            "综合指数",
            "排名变动",
            "-",
        ]
        temp_df = temp_df[
            [
                "排名",
                "俱乐部名称",
                "人气指数",
                "舆论指数",
                "战绩指数",
                "综合指数",
                "排名变动",
            ]
        ]
    else:
        temp_df.columns = [
            "排名",
            "俱乐部名称",
            "人气指数",
            "舆论指数",
            "综合指数",
            "排名变动",
            "-",
        ]
        temp_df = temp_df[
            [
                "排名",
                "俱乐部名称",
                "人气指数",
                "舆论指数",
                "综合指数",
                "排名变动",
            ]
        ]
    temp_df['更新时间'] = report_date
    return temp_df


def player_rank_game(symbol: str = "英雄联盟") -> pd.DataFrame:
    """
    中国电竞价值排行榜-选手排行榜
    http://rank.uuu9.com/player/ranking
    :param symbol: choice of {'英雄联盟', '绝地求生', '王者荣耀', 'DOTA2', '穿越火线', '和平精英'}
    :type symbol: str
    :return: 选手排行榜
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "DOTA2": "1",
        "英雄联盟": "2",
        "绝地求生": "3",
        "王者荣耀": "4",
        "穿越火线": "5",
        "和平精英": "6",
    }
    url = "http://rank.uuu9.com/player/ranking"
    params = {"gameId": symbol_map[symbol], "type": "0"}
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("div", attrs={"class": "ec_data"}).text
    report_date = data_text.split("：")[-1]
    temp_df = pd.read_html(r.text)[0]
    if symbol == "王者荣耀":
        temp_df.columns = [
            "排名",
            "选手ID",
            "所属战队",
            "人气指数",
            "舆论指数",
            "战绩指数",
            "综合指数",
            "排名变动",
            "-",
        ]
        temp_df = temp_df[
            [
                "排名",
                "选手ID",
                "所属战队",
                "人气指数",
                "舆论指数",
                "战绩指数",
                "综合指数",
                "排名变动",
            ]
        ]
        temp_df['更新时间'] = report_date
        return temp_df
    if symbol in {"英雄联盟", "DOTA2"}:
        temp_df.columns = [
            "排名",
            "选手ID",
            "所属战队",
            "人气指数",
            "舆论指数",
            "战绩指数",
            "综合指数",
            "身价",
            "排名变动",
            "-",
        ]
        temp_df = temp_df[
            [
                "排名",
                "选手ID",
                "所属战队",
                "人气指数",
                "舆论指数",
                "战绩指数",
                "综合指数",
                "身价",
                "排名变动",
            ]
        ]
    else:
        temp_df.columns = [
            "排名",
            "选手ID",
            "所属战队",
            "人气指数",
            "舆论指数",
            "综合指数",
            "身价",
            "排名变动",
            "-",
        ]
        temp_df = temp_df[
            [
                "排名",
                "选手ID",
                "所属战队",
                "人气指数",
                "舆论指数",
                "综合指数",
                "身价",
                "排名变动",
            ]
        ]
    temp_df['更新时间'] = report_date
    return temp_df


if __name__ == "__main__":
    club_rank_game_df = club_rank_game(symbol="英雄联盟")
    print(club_rank_game_df)

    player_rank_game_df = player_rank_game(symbol="英雄联盟")
    print(player_rank_game_df)

    for item in ["英雄联盟", "绝地求生", "王者荣耀", "DOTA2", "穿越火线", "和平精英"]:
        print(item)

        club_rank_game_df = club_rank_game(symbol=item)
        print(club_rank_game_df)

        player_rank_game_df = player_rank_game(symbol=item)
        print(player_rank_game_df)
