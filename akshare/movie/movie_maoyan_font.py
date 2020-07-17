# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/16 21:40
Desc: 下载猫眼电影的字体文件到本地
如果更新, 请重新人工标注 get_font_data 里面的数字
"""
import re
from pathlib import Path
from typing import List

import requests
from fontTools.ttLib import TTFont

_fonts_path = Path(__file__).absolute().parent / "fonts"
_brand_url = "https://maoyan.com/board/1"
_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}


def get_font_content() -> bytes:
    """
    请求字体文件
    :return: woff file
    :rtype: bytes
    """
    res = requests.get(url=_brand_url, headers=_headers)
    woff_url = re.findall(r"url\('(.*?\.woff)'\)", res.text)[0]
    font_url = f"http:{woff_url}"
    return requests.get(font_url).content


def save_font() -> None:
    for i in range(5):
        font_content = get_font_content()
        with open(_fonts_path / f"{i+1}.woff", "wb") as f:
            f.write(font_content)


def get_coor_info(font, cli):
    glyf_order = font.getGlyphOrder()[2:]
    info = list()
    for i, g in enumerate(glyf_order):
        coors = font["glyf"][g].coordinates
        coors = [_ for c in coors for _ in c]
        coors.insert(0, cli[i])
        info.append(coors)
    return info


def get_font_data() -> List[List[List[int]]]:
    """
    人工标注
    """
    font_1 = TTFont(_fonts_path / "1.woff")
    cli_1 = [6, 7, 4, 9, 1, 2, 5, 0, 3, 8]
    coor_info_1 = get_coor_info(font_1, cli_1)

    font_2 = TTFont(_fonts_path / "2.woff")
    cli_2 = [1, 3, 2, 7, 6, 8, 9, 0, 4, 5]
    coor_info_2 = get_coor_info(font_2, cli_2)

    font_3 = TTFont(_fonts_path / "3.woff")
    cli_3 = [5, 8, 3, 0, 6, 7, 9, 1, 2, 4]
    coor_info_3 = get_coor_info(font_3, cli_3)

    font_4 = TTFont(_fonts_path / "4.woff")
    cli_4 = [9, 3, 4, 8, 7, 5, 2, 1, 6, 0]
    coor_info_4 = get_coor_info(font_4, cli_4)

    font_5 = TTFont(_fonts_path / "5.woff")
    cli_5 = [1, 5, 8, 0, 7, 9, 6, 3, 2, 4]
    coor_info_5 = get_coor_info(font_5, cli_5)

    infos = coor_info_1 + coor_info_2 + coor_info_3 + coor_info_4 + coor_info_5
    return infos


if __name__ == '__main__':
    print(get_font_data())
