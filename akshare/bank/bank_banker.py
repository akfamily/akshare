# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/14 15:56
Desc: thebankerdatabase
https://www.thebankerdatabase.com/index.cfm/search/ranking
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def bank_rank_banker() -> pd.DataFrame:
    """
    全球银行排名前 25 家
    https://www.thebankerdatabase.com/index.cfm/search/ranking
    :return: 全球银行排名前 25 家
    :rtype: pandas.DataFrame
    """
    url = "https://www.thebankerdatabase.com/index.cfm/search/index.cfm"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-length": "5906",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "cookie": "CFID=4066679; CFTOKEN=757b91f9e32ccf96-DABAED1E-5056-81CB-AC16B7759B219C5F; __utmz=11608689.1610550237.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=11608689.|1=User%20Type=Anonymous=1; X-Mapping-mcmjnkih=105487F00B86D7352E95B0FD5E7117FE; JSESSIONID=AAFB1EFAC538A6591033D322503118E6.cfusion; LIVEPAGEHEIGHT=600; LIVEPAGEWIDTH=800; __utma=11608689.1485486898.1610550237.1610550237.1610609939.2; __utmc=11608689; __utmt=1; __utmb=11608689.1.10.1610609939; CFGLOBALS=urltoken%3DCFID%23%3D4066679%26CFTOKEN%23%3D757b91f9e32ccf96%2DDABAED1E%2D5056%2D81CB%2DAC16B7759B219C5F%26jsessionid%23%3DAAFB1EFAC538A6591033D322503118E6%2Ecfusion%23lastvisit%3D%7Bts%20%272021%2D01%2D14%2007%3A39%3A01%27%7D%23hitcount%3D44%23timecreated%3D%7Bts%20%272021%2D01%2D13%2015%3A03%3A42%27%7D%23cftoken%3D757b91f9e32ccf96%2DDABAED1E%2D5056%2D81CB%2DAC16B7759B219C5F%23cfid%3D4066679%23",
        "origin": "https://www.thebankerdatabase.com",
        "pragma": "no-cache",
        "referer": "https://www.thebankerdatabase.com/index.cfm/search/ranking",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    params = {
        "fuseaction": "search.search_results_json",
        "ajax": "1",
        "ranking": "1",
    }
    payload = {
        "draw": "4",
        "columns[0][data]": "bank_id",
        "columns[0][name]": "bank_id",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "false",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "primary_ranking",
        "columns[1][name]": "primary_ranking",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "1",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "previous_ranking",
        "columns[2][name]": "previous_ranking",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "1",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "current_name",
        "columns[3][name]": "current_name",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "1",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "columns[4][data]": "country_name",
        "columns[4][name]": "country_name",
        "columns[4][searchable]": "true",
        "columns[4][orderable]": "1",
        "columns[4][search][value]": "",
        "columns[4][search][regex]": "false",
        "columns[5][data]": "yearend_datetime",
        "columns[5][name]": "yearend_datetime",
        "columns[5][searchable]": "true",
        "columns[5][orderable]": "1",
        "columns[5][search][value]": "",
        "columns[5][search][regex]": "false",
        "columns[6][data]": "DP2",
        "columns[6][name]": "DP2",
        "columns[6][searchable]": "true",
        "columns[6][orderable]": "1",
        "columns[6][search][value]": "",
        "columns[6][search][regex]": "false",
        "columns[7][data]": "DP2_change",
        "columns[7][name]": "DP2_change",
        "columns[7][searchable]": "true",
        "columns[7][orderable]": "1",
        "columns[7][search][value]": "",
        "columns[7][search][regex]": "false",
        "columns[8][data]": "DP2_rank",
        "columns[8][name]": "DP2_rank",
        "columns[8][searchable]": "true",
        "columns[8][orderable]": "1",
        "columns[8][search][value]": "",
        "columns[8][search][regex]": "false",
        "columns[9][data]": "DP6",
        "columns[9][name]": "DP6",
        "columns[9][searchable]": "true",
        "columns[9][orderable]": "1",
        "columns[9][search][value]": "",
        "columns[9][search][regex]": "false",
        "columns[10][data]": "DP6_change",
        "columns[10][name]": "DP6_change",
        "columns[10][searchable]": "true",
        "columns[10][orderable]": "1",
        "columns[10][search][value]": "",
        "columns[10][search][regex]": "false",
        "columns[11][data]": "DP6_rank",
        "columns[11][name]": "DP6_rank",
        "columns[11][searchable]": "true",
        "columns[11][orderable]": "1",
        "columns[11][search][value]": "",
        "columns[11][search][regex]": "false",
        "columns[12][data]": "DP1",
        "columns[12][name]": "DP1",
        "columns[12][searchable]": "true",
        "columns[12][orderable]": "1",
        "columns[12][search][value]": "",
        "columns[12][search][regex]": "false",
        "columns[13][data]": "DP1_change",
        "columns[13][name]": "DP1_change",
        "columns[13][searchable]": "true",
        "columns[13][orderable]": "1",
        "columns[13][search][value]": "",
        "columns[13][search][regex]": "false",
        "columns[14][data]": "DP12",
        "columns[14][name]": "DP12",
        "columns[14][searchable]": "true",
        "columns[14][orderable]": "1",
        "columns[14][search][value]": "",
        "columns[14][search][regex]": "false",
        "columns[15][data]": "DP48",
        "columns[15][name]": "DP48",
        "columns[15][searchable]": "true",
        "columns[15][orderable]": "1",
        "columns[15][search][value]": "",
        "columns[15][search][regex]": "false",
        "columns[16][data]": "DP48_rank",
        "columns[16][name]": "DP48_rank",
        "columns[16][searchable]": "true",
        "columns[16][orderable]": "1",
        "columns[16][search][value]": "",
        "columns[16][search][regex]": "false",
        "columns[17][data]": "DP130",
        "columns[17][name]": "DP130",
        "columns[17][searchable]": "true",
        "columns[17][orderable]": "1",
        "columns[17][search][value]": "",
        "columns[17][search][regex]": "false",
        "columns[18][data]": "DP130_rank",
        "columns[18][name]": "DP130_rank",
        "columns[18][searchable]": "true",
        "columns[18][orderable]": "1",
        "columns[18][search][value]": "",
        "columns[18][search][regex]": "false",
        "columns[19][data]": "DP13",
        "columns[19][name]": "DP13",
        "columns[19][searchable]": "true",
        "columns[19][orderable]": "1",
        "columns[19][search][value]": "",
        "columns[19][search][regex]": "false",
        "columns[20][data]": "DP13_rank",
        "columns[20][name]": "DP13_rank",
        "columns[20][searchable]": "true",
        "columns[20][orderable]": "1",
        "columns[20][search][value]": "",
        "columns[20][search][regex]": "false",
        "columns[21][data]": "DP8",
        "columns[21][name]": "DP8",
        "columns[21][searchable]": "true",
        "columns[21][orderable]": "1",
        "columns[21][search][value]": "",
        "columns[21][search][regex]": "false",
        "columns[22][data]": "DP49",
        "columns[22][name]": "DP49",
        "columns[22][searchable]": "true",
        "columns[22][orderable]": "1",
        "columns[22][search][value]": "",
        "columns[22][search][regex]": "false",
        "columns[23][data]": "DP49_rank",
        "columns[23][name]": "DP49_rank",
        "columns[23][searchable]": "true",
        "columns[23][orderable]": "1",
        "columns[23][search][value]": "",
        "columns[23][search][regex]": "false",
        "columns[24][data]": "DP131",
        "columns[24][name]": "DP131",
        "columns[24][searchable]": "true",
        "columns[24][orderable]": "1",
        "columns[24][search][value]": "",
        "columns[24][search][regex]": "false",
        "columns[25][data]": "DP132",
        "columns[25][name]": "DP132",
        "columns[25][searchable]": "true",
        "columns[25][orderable]": "1",
        "columns[25][search][value]": "",
        "columns[25][search][regex]": "false",
        "order[0][column]": "0",
        "order[0][dir]": "asc",
        "start": "0",
        "length": "100",
        "search[value]": "",
        "search[regex]": "false",
    }
    r = requests.post(url, params=params, data=payload, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    del temp_df["columnlist"]
    del temp_df["bank_id"]
    bank_url_list = [
        "https://www.thebankerdatabase.com/"
        + BeautifulSoup(item, "lxml").find("a")["href"]
        for item in temp_df["current_name"]
    ]
    bank_name_list = []
    for item in tqdm(bank_url_list, leave=False):
        r = requests.get(item)
        soup = BeautifulSoup(r.text, "lxml")
        bank_name = soup.find("h1", attrs={"class": "bank"}).find("span").text
        bank_name_list.append(bank_name)
    temp_df["current_name"] = bank_name_list
    temp_df["yearend_datetime"] = pd.to_datetime(temp_df["yearend_datetime"])
    return temp_df


if __name__ == "__main__":
    bank_rank_banker_df = bank_rank_banker()
    print(bank_rank_banker_df)
