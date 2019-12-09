# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/23 19:19
contact: jindaxiang@163.com
desc: 获取金十数据-数据中心所有连接
"""
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_js_data_list():
    session = HTMLSession()
    r = session.get("https://datacenter.jin10.com/")
    r.html.render()
    soup = BeautifulSoup(r.html.html, "lxml")
    temp_soup = soup.find("div", attrs={"class": "chart-overview-list"}).find_all(
        "div", attrs={"class": "chart-overview-item"}
    )[2:]
    big_dict = {}
    for out_item in temp_soup:
        big_dict[
            out_item.find("h4", attrs={"style": "position: relative;"})
            .get_text()
            .strip()
        ] = {}
        for item in out_item.find_all("ul", attrs={"class": "chart-overview-sublist"}):
            for item_inner in item.find_all(
                "li", attrs={"class": "chart-overview-subItem"}
            ):
                big_dict[
                    out_item.find("h4", attrs={"style": "position: relative;"})
                    .get_text()
                    .strip()
                ][item_inner.find("a").get_text().strip()] = item_inner.find("a")[
                    "href"
                ]
    return big_dict


if __name__ == "__main__":
    df = get_js_data_list()
    print(df["其他"])
