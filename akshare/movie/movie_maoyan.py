# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/16 20:44
contact: jindaxiang@163.com
desc: 猫眼电影实时票房
感谢老铁: https://cloudcrawler.club/cong-mao-yan-zi-ti-fan-pa-fen-xi-tan-tan-zi-ti-fan-pa-de-qian-shi-jin-sheng.html
"""
from typing import Dict, Any
import re
from io import BytesIO
from pathlib import Path

import requests
import pandas as pd
from lxml import etree
from fontTools.ttLib import TTFont

from akshare.movie.movie_maoyan_knn_font import Classify

_woff_path = (
        Path(__file__).absolute().parent / "fonts" / "test.woff"
)
_board_url = "https://maoyan.com/board/1"
_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Host": "maoyan.com",
    "Pragma": "no-cache",
    # "Cookie": "_lxsdk_s=16f32be05ae-d46-b03-a58%7C%7C1",
    "Referer": "https://maoyan.com/board/1",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}
_classify = Classify()


def get_map(text: str) -> Dict[str, Any]:
    woff_url = re.findall(r"url\('(.*?\.woff)'\)", text)[0]
    font_url = f"http:{woff_url}"
    content = requests.get(font_url).content
    try:
        with open(_woff_path, "wb") as f:
            f.write(content)
    except:
        with open(r"C:\Users\king\PycharmProjects\akshare\akshare\movie\fonts\test.woff", "wb") as f:
            f.write(content)
    font = TTFont(BytesIO(content))
    glyf_order = font.getGlyphOrder()[2:]
    info = []
    for g in glyf_order:
        coors = font["glyf"][g].coordinates
        coors = [_ for c in coors for _ in c]
        info.append(coors)
    map_li = map(lambda x: str(int(x)), _classify.knn_predict(info))
    uni_li = map(lambda x: x.lower().replace("uni", "&#x") + ";", glyf_order)
    return dict(zip(uni_li, map_li))


def movie_board():
    res = requests.get(url=_board_url, headers=_headers)
    res.encoding = "utf-8"
    text = res.text
    map_dict = get_map(text=text)
    for uni in map_dict.keys():
        text = text.replace(uni, map_dict[uni])
    html = etree.HTML(text)
    dd_li = html.xpath('//dl[@class="board-wrapper"]/dd')
    title_temp = []
    star_temp = []
    releasetime_temp = []
    realtime_stont_temp = []
    total_stont_temp = []
    for dd in dd_li:
        p_li = dd.xpath(
            './div[@class="board-item-main"]//div[@class="movie-item-info"]/p'
        )
        title = p_li[0].xpath("./a/@title")[0]
        star = p_li[1].xpath("./text()")[0]
        releasetime = p_li[2].xpath("./text()")[0]
        p_li = dd.xpath(
            './div[@class="board-item-main"]//div[@class="movie-item-number boxoffice"]/p'
        )
        realtime_stont = "".join(
            list(map(lambda x: x.strip(), p_li[0].xpath(".//text()")))
        )
        total_stont = "".join(
            list(map(lambda x: x.strip(), p_li[1].xpath(".//text()")))
        )
        # print(title)
        title_temp.append(title)
        # print(star)
        star_temp.append(star)
        # print(releasetime)
        releasetime_temp.append(releasetime)
        # print(realtime_stont)
        realtime_stont_temp.append(realtime_stont)
        # print(total_stont)
        total_stont_temp.append(total_stont)
        # print("-" * 50)
    return pd.DataFrame(
        [
            title_temp,
            star_temp,
            releasetime_temp,
            realtime_stont_temp,
            total_stont_temp,
        ],
        index=["电影名称", "主演", "上映时间", "实时票房", "总票房"],
    ).T


if __name__ == "__main__":
    df = movie_board()
    print(df)
