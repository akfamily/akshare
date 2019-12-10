# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/10 21:55
contact: jindaxiang@163.com
desc: 历年世界500强榜单数据
http://www.fortunechina.com/fortune500/index.htm
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup

from akshare.fortune.cons import (
    url_1996,
    url_1997,
    url_1998,
    url_1999,
    url_2000,
    url_2001,
    url_2002,
    url_2003,
    url_2004,
    url_2005,
    url_2006,
    url_2007,
    url_2008,
    url_2009,
    url_2010,
    url_2011,
    url_2012,
    url_2013,
    url_2014,
    url_2015,
    url_2016,
    url_2017,
    url_2018,
    url_2019,
)


def fortune_rank(year="2015"):
    res = requests.get(eval("url_" + year))
    res.encoding = "utf-8"
    df = pd.read_html(res.text)[0]
    return df


if __name__ == '__main__':
    df = fortune_rank(year="2015")
    print(df)
