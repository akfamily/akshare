# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/16 20:44
Desc: 猫眼电影实时票房
感谢老铁: https://cloudcrawler.club/cong-mao-yan-zi-ti-fan-pa-fen-xi-tan-tan-zi-ti-fan-pa-de-qian-shi-jin-sheng.html
"""
import re
from io import BytesIO
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont

from akshare.movie.cons import _board_url, _headers
from akshare.movie.movie_maoyan_knn_font import Classify

_woff_path = Path(__file__).absolute().parent / "fonts" / "test.woff"

_classify = Classify()


def get_map(text: str) -> Dict[str, Any]:
    woff_url = re.findall(r"url\('(.*?\.woff)'\)", text)[0]
    font_url = f"http:{woff_url}"
    res = requests.get(font_url)
    font = TTFont(BytesIO(res.content))
    glyf_order = font.getGlyphOrder()[2:]
    info = []
    for g in glyf_order:
        coors = font["glyf"][g].coordinates
        coors = [_ for c in coors for _ in c]
        info.append(coors)
    map_li = map(lambda x: str(int(x)), _classify.knn_predict(info))
    uni_li = map(lambda x: x.lower().replace("uni", "&#x") + ";", glyf_order)
    return dict(zip(uni_li, map_li))


def box_office_spot():
    """
    猫眼电影-榜单-国内票房榜
    :return: 国内上映电影的实时票房数据
    :rtype: pandas.DataFrame
    """
    res = requests.get(url=_board_url, headers=_headers)
    res.encoding = "utf-8"
    text = res.text
    map_dict = get_map(text=text)
    for uni in map_dict.keys():
        text = text.replace(uni, map_dict[uni])
    soup = BeautifulSoup(text, "lxml")
    dd_li = soup.find("dl", attrs={"class": "board-wrapper"}).find_all("dd")
    title_temp = []
    star_temp = []
    release_time_temp = []
    realtime_stont_temp = []
    total_stont_temp = []
    for dd in dd_li:
        # dd = dd_li[0]
        p_li = (
            dd.find("div", attrs={"class": "board-item-main"})
            .find("div", attrs={"class": "movie-item-info"})
            .find_all("p")
        )
        title = p_li[0].get_text()
        star = p_li[1].get_text()
        release_time = p_li[2].get_text()
        p_li = (
            dd.find("div", attrs={"class": "board-item-main"})
            .find("div", attrs={"class": "movie-item-number"})
            .find_all("p")
        )
        realtime_stont = "".join(list(map(lambda x: x.strip(), p_li[0].get_text())))
        total_stont = "".join(list(map(lambda x: x.strip(), p_li[1].get_text())))
        title_temp.append(title)
        star_temp.append(star.split("：")[1])
        release_time_temp.append(release_time.split("：")[1])
        realtime_stont_temp.append(realtime_stont.split(":")[1])
        total_stont_temp.append(total_stont.split(":")[1])
    temp_df = pd.DataFrame(
        [
            title_temp,
            star_temp,
            release_time_temp,
            realtime_stont_temp,
            total_stont_temp,
        ],
        index=["电影名称", "主演", "上映时间", "实时票房", "总票房"],
    ).T

    return temp_df


if __name__ == "__main__":
    box_office_spot_df = box_office_spot()
    print(box_office_spot_df)
