# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/7 14:06
contact: jindaxiang@163.com
desc: 不需要控制速度, 但是需要伪装游览器, 不然会被一次封 IP 地址
"""
import os

import requests
import pandas as pd
from bs4 import BeautifulSoup
import execjs
import time

from akshare.bank.cons import cbirc_headers_without_cookie


def get_page_list(all_page=15):
    """
    想要获取多少页的内容
    注意路径
    http://www.cbirc.gov.cn/cn/list/9103/910305/ybjfjcf/1.html
    :param all_page: int 输入从第1页到 all_page 页的内容
    :return: pd.DataFrame 另存为 csv 文件
    """
    big_url_list = []
    big_title_list = []
    flag = True
    cbirc_headers = cbirc_headers_without_cookie.copy()
    time.sleep(5)
    for page in range(1, all_page):
        # page = 1

        print(page)
        main_url = "http://www.cbirc.gov.cn/cn/list/9103/910305/ybjfjcf/{}.html".format(page)
        if flag:
            res = requests.get(main_url, headers=cbirc_headers)
            temp_cookie = res.headers["Set-Cookie"].split(";")[0]
            cbirc_headers.update({"Cookie": res.headers["Set-Cookie"].split(";")[0]})
            res = requests.get(main_url, headers=cbirc_headers)
            soup = BeautifulSoup(res.text, "lxml")
            if "fromCharCode" not in res.text:
                res_html = "function getClearance(){" + soup.find_all("script")[0].get_text() + "};"
                res_html = res_html.replace("</script>", "")
                res_html = res_html.replace("eval", "return")
                res_html = res_html.replace("<script>", "")
                ctx = execjs.compile(res_html)
                over_js = "function getClearance2(){ var a" + ctx.call("getClearance").split("document.cookie")[1].split("Path=/;'")[
                             0] + "Path=/;';return a;};"
                over_js = over_js.replace("window.headless", "''")
                over_js = over_js.replace("window['_p'+'hantom']", "''")
                over_js = over_js.replace("window['__p'+'hantom'+'as']", "''")
                ctx = execjs.compile(over_js)
                cookie_2 = ctx.call("getClearance2").split(";")[0]
                cbirc_headers.update({"Cookie": temp_cookie + ";" + cookie_2})
                res = requests.get(main_url, headers=cbirc_headers)
            else:
                res_html = "function getClearance(){" + soup.find_all("script")[0].get_text() + "};"
                res_html = res_html.replace("</script>", "")
                res_html = res_html.replace("eval", "return")
                res_html = res_html.replace("<script>", "")
                ctx = execjs.compile(res_html)
                over_js = "function getClearance2(){ var a" + \
                          ctx.call("getClearance").split("document.cookie")[1].split("Path=/;'")[
                              0] + "Path=/;';return a;};"
                over_js = over_js.replace("window.headless", "''")
                over_js = over_js.replace("window['_p'+'hantom']", "''")
                over_js = over_js.replace("window['__p'+'hantom'+'as']", "''")
                over_js = over_js.replace("window['callP'+'hantom']", "''")
                ctx = execjs.compile(over_js)
                cookie_2 = ctx.call("getClearance2").split(";")[0]
                cbirc_headers.update({"Cookie": temp_cookie + ";" + cookie_2})
                res = requests.get(main_url, headers=cbirc_headers)
                flag = 0
        # print(cbirc_headers)
        soup = BeautifulSoup(res.text, "lxml")
        url_list = [item.find("a")["href"] for item in soup.find_all(attrs={"class": "zwbg-2"})]
        title_list = [item.find("a").get_text() for item in soup.find_all(attrs={"class": "zwbg-2"})]
        big_url_list.extend(url_list)
        big_title_list.extend(title_list)
    temp_df = pd.DataFrame([big_title_list, big_url_list]).T
    return temp_df


def get_detail():
    """
    获取每个具体页面的表格内容
    注意路径
    :return: pandas.DataFrame 另存为 csv 文件
    """
    os.chdir(r"C:\Users\king\PycharmProjects\akshare\temp")
    temp_df = pd.read_csv(r"C:\Users\king\PycharmProjects\akshare\bank.csv", encoding="gb2312", header=0, index_col=0)
    for i in range(1, len(temp_df) + 1):
        print(i)
        try:
            res = requests.get("http://www.cbirc.gov.cn" + temp_df.iloc[:, 1][i], headers=cbirc_headers)
            table_list = pd.read_html(res.text)
            table_df = table_list[6].iloc[:, 2:]
            table_df.columns = ["字段", "内容"]
            table_df.to_csv(f"{temp_df.iloc[:, 0][i]}.csv", encoding="gb2312")
        except:
            print(i, "是文档")
            continue


def process_data():
    """
    处理采集下载的具体页面的内容
    注意路径
    :return: pandas.DataFrame 另存为 csv 文件
    """
    big_df = pd.DataFrame()
    file_name_list = os.listdir(r"C:\Users\king\PycharmProjects\akshare\temp")
    for file in file_name_list:
        print(file)
        file_df = pd.read_csv(file, encoding="gb2312", header=0, index_col=0)
        big_df = big_df.append(file_df.iloc[:, 1])
    for file in file_name_list:
        print(file)
        file_df = pd.read_csv(file, encoding="gb2312", header=0, index_col=0)
        break
    df = big_df.reset_index(drop=True)
    df = df.iloc[:, :-1]
    df.columns = file_df.iloc[:, 0].tolist()
    df.to_csv("result.csv", encoding="gb2312")


if __name__ == "__main__":
    df = get_page_list(all_page=15)
    print(df)


