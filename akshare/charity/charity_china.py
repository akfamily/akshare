# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/15 18:03
Desc: 慈善中国
http://cishan.chinanpo.gov.cn/platform/login.html
# 慈善中国-慈善组织查询
http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaindex.html
# 慈善中国-慈善信托查询
http://cishan.chinanpo.gov.cn/biz/ma/csmh/e/csmheindex.html
# 慈善中国-募捐方案备案
http://cishan.chinanpo.gov.cn/biz/ma/csmh/c/csmhcindex.html
# 慈善中国-慈善项目进展
http://cishan.chinanpo.gov.cn/biz/ma/csmh/b/csmhbindex.html
# 慈善中国-慈善组织年报
http://cishan.chinanpo.gov.cn/biz/ma/csmh/d/csmhdindex.html
# 慈善中国-募捐信息平台
http://cishan.chinanpo.gov.cn/biz/ma/csmh/h/csmhhindex.html

# TODO 移除
"""
import re
from typing import Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# 慈善中国-慈善组织查询
def _get_page_num_charity_china_organization() -> int:
    """
    慈善中国-慈善组织查询-总页数
    :return: 总页数
    :rtype: int
    """
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/a/csmhaDoSort.html"
    payload_params = {
        "aaee0102_03": "",
        "field": "aaex0131",
        "sort": "desc",
        "flag": "0",
    }
    payload_data = {"pageNo": "1"}
    r = requests.post(url, params=payload_params, data=payload_data)
    soup = BeautifulSoup(r.text, "lxml")
    page_text = soup.find(
        "font", attrs={"style": "margin-left: 10px; color: #000000; font-weight: bold;"}
    ).text.split("/")[1]
    page_num = re.findall(re.compile(r"\d+"), page_text)[0]
    return int(page_num)


def charity_china_organization() -> pd.DataFrame:
    """
    慈善中国-慈善组织查询
    https://cszg.mca.gov.cn/biz/ma/csmh/a/csmhaindex.html
    :return: 慈善中国-慈善组织查询
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num_charity_china_organization()
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/a/csmhaDoSort.html"
    payload_params = {
        "aaee0102_03": "",
        "field": "aaex0131",
        "sort": "desc",
        "flag": "0",
    }
    outer_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1), leave=False):
        payload_data = {"pageNo": str(page)}
        r = requests.post(url, params=payload_params, data=payload_data)
        inner_df = pd.read_html(r.text)[0]
        outer_df = outer_df.append(inner_df, ignore_index=True)
    return outer_df


# 慈善中国-慈善信托查询
def _get_page_num_charity_china_trust() -> int:
    """
    慈善中国-慈善信托查询-总页数
    :return: 总页数
    :rtype: int
    """
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/e/csmhedoSort.html"
    payload_params = {
        "aafx0103": "",
        "field": "aafx0104",
        "sort": "desc",
    }
    payload_data = {"pageNo": "1"}
    r = requests.post(url, params=payload_params, data=payload_data)
    soup = BeautifulSoup(r.text, "lxml")
    page_text = soup.find(
        "font", attrs={"style": "margin-left: 10px; color: #000000; font-weight: bold;"}
    ).text.split("/")[1]
    page_num = re.findall(re.compile(r"\d+"), page_text)[0]
    return int(page_num)


def charity_china_trust() -> pd.DataFrame:
    """
    慈善中国-慈善信托查询
    https://cszg.mca.gov.cn/biz/ma/csmh/e/csmheindex.html
    :return: 慈善中国-慈善信托查询
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num_charity_china_trust()
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/e/csmhedoSort.html"
    payload_params = {
        "aafx0103": "",
        "field": "aafx0104",
        "sort": "desc",
    }
    outer_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1), leave=False):
        payload_data = {"pageNo": str(page)}
        r = requests.post(url, params=payload_params, data=payload_data)
        inner_df = pd.read_html(r.text)[0]
        outer_df = outer_df.append(inner_df, ignore_index=True)
    return outer_df


# 慈善中国-募捐方案备案
def _get_page_num_charity_china_plan() -> int:
    """
    慈善中国-募捐方案备案-总页数
    :return: 总页数
    :rtype: int
    """
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/c/csmhcquerylist.html"
    payload_params = {
        "aaex9102_03": "",
        "aaex8104": "1",
    }
    payload_data = {"pageNo": "1"}
    r = requests.post(url, params=payload_params, data=payload_data)
    soup = BeautifulSoup(r.text, "lxml")
    page_text = soup.find(
        "font", attrs={"style": "margin-left: 10px; color: #000000; font-weight: bold;"}
    ).text.split("/")[1]
    page_num = re.findall(re.compile(r"\d+"), page_text.replace(",", ""))[0]
    return int(page_num)


def _get_charity_china_plan_detail(url: str = "") -> Tuple:
    """
    获取页面的详情, 需要进入二级页面访问获取, 需要增加字段可以在此函数中进行
    https://cszg.mca.gov.cn/biz/ma/csmh/c/csmhcdetail.html?id=ff8080816390694d0163f31aab60188e
    :param url: charity_china_plan 二级页面的网址
    :type url: str
    :return: 名词和备案号
    :rtype: tuple
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.find("div", attrs={"class": "gkmj-title"}).text
    number = soup.find("div", attrs={"class": "gkmj-number"}).text
    return title, number


def charity_china_plan() -> pd.DataFrame:
    """
    慈善中国-募捐方案备案
    https://cszg.mca.gov.cn/biz/ma/csmh/c/csmhcindex.html
    :return: 慈善中国-募捐方案备案
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num_charity_china_plan()
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/c/csmhcquerylist.html"
    payload_params = {
        "aaex9102_03": "",
        "aaex8104": "1",
    }
    outer_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1)):
        payload_data = {"pageNo": str(page)}
        r = requests.post(url, params=payload_params, data=payload_data)
        soup = BeautifulSoup(r.text, "lxml")
        org = [
            item.text.split("：")[1]
            for item in soup.find_all("div", attrs={"class": "gkmj-list-team"})
        ]
        status = [
            item.text.split("：")[1]
            for item in soup.find_all("div", attrs={"class": "gkmj-amount"})
        ]
        temp_list = [
            _get_charity_china_plan_detail(
                "https://cszg.mca.gov.cn" + item["href"]
            )
            for item in soup.find_all("a")
        ]
        title = [item[0] for item in temp_list]
        num = [item[1] for item in temp_list]
        inner_df = pd.DataFrame([org, status, title, num]).T
        outer_df = outer_df.append(inner_df, ignore_index=True)
    outer_df.columns = ["组织", "状态", "名称", "备案号"]
    return outer_df


# 慈善中国-慈善项目进展
def _get_page_num_charity_china_progress() -> int:
    """
    慈善中国-慈善项目进展-总页数
    :return: 总页数
    :rtype: int
    """
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/b/csmhbquerylist.html"
    payload_params = {
        "aaex8102_03": "",
        "aaex8104": "1",
    }
    payload_data = {"pageNo": "1"}
    r = requests.post(url, params=payload_params, data=payload_data)
    soup = BeautifulSoup(r.text, "lxml")
    page_text = soup.find(
        "font", attrs={"style": "margin-left: 10px; color: #000000; font-weight: bold;"}
    ).text.split("/")[1]
    page_num = re.findall(re.compile(r"\d+"), page_text.replace(",", ""))[0]
    return int(page_num)


def _get_charity_china_progress_detail(url: str = "") -> Tuple[str]:
    """
    https://cszg.mca.gov.cn/biz/ma/csmh/b/csmhbdetail.html?id=ff80808170367b4c01703a5a9158053e
    :param url:
    :type url:
    :return:
    :rtype:
    """
    # url = "https://cszg.mca.gov.cn/biz/ma/csmh/b/csmhbdetail.html?id=ff80808170367b4c01703a5a9158053e"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.find("div", attrs={"class": "csxm-title"}).text
    number = soup.find("div", attrs={"class": "csxm-number"}).text
    ori_org = soup.find("div", attrs={"class": "csxm-orgnize"}).text.split("】")[1]
    status = soup.find("div", attrs={"class": "csxm-comp"}).text.split("】")[1]
    return title, number, ori_org, status


def charity_china_progress() -> pd.DataFrame:
    """
    慈善中国-慈善项目进展
    https://cszg.mca.gov.cn/biz/ma/csmh/b/csmhbindex.html
    :return: 慈善中国-慈善项目进展
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num_charity_china_progress()
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/b/csmhbquerylist.html"
    payload_params = {
        "aaex8102_03": "",
        "aaex8104": "1",
    }
    outer_df = pd.DataFrame()
    for page in tqdm(range(1, page_num)):
        payload_data = {"pageNo": str(page)}
        r = requests.post(url, params=payload_params, data=payload_data)
        soup = BeautifulSoup(r.text, "lxml")
        org = [
            item.text.split("：")[1]
            for item in soup.find_all("div", attrs={"class": "csxm-list-comp"})
        ]
        temp_list = [
            _get_charity_china_progress_detail(
                "https://cszg.mca.gov.cn" + item["href"]
            )
            for item in soup.find_all("a")
        ]
        title = [item[0] for item in temp_list]
        num = [item[1] for item in temp_list]
        ori = [item[2] for item in temp_list]
        status = [item[3] for item in temp_list]
        inner_df = pd.DataFrame([org, title, num, ori, status]).T
        outer_df = outer_df.append(inner_df, ignore_index=True)
    outer_df.columns = ["组织", "名称", "项目编号", "发起慈善组织", "项目状态"]
    return outer_df


# 慈善中国-慈善组织年报
def _get_page_num_charity_china_report() -> int:
    """
    慈善中国-慈善组织年报-总页数
    :return: 总页数
    :rtype: int
    """
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/d/csmhddoSort.html"
    payload_params = {
        "search_condit": "",
        "field": "",
        "sort": "desc",
        "flag": "0",
    }
    payload_data = {"pageNo": "1"}
    r = requests.post(url, params=payload_params, data=payload_data)
    soup = BeautifulSoup(r.text, "lxml")
    page_text = soup.find(
        "font", attrs={"style": "margin-left: 10px; color: #000000; font-weight: bold;"}
    ).text.split("/")[1]
    page_num = re.findall(re.compile(r"\d+"), page_text)[0]
    return int(page_num)


def charity_china_report() -> pd.DataFrame:
    """
    慈善中国-慈善组织年报
    https://cszg.mca.gov.cn/biz/ma/csmh/d/csmhdindex.html
    :return: 慈善中国-慈善组织年报
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num_charity_china_report()
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/d/csmhddoSort.html"
    payload_params = {
        "search_condit": "",
        "field": "",
        "sort": "desc",
        "flag": "0",
    }
    outer_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1), desc="Please wait for a moment"):
        payload_data = {"pageNo": str(page)}
        r = requests.post(url, params=payload_params, data=payload_data)
        inner_df = pd.read_html(r.text)[0]
        inner_soup = BeautifulSoup(r.text, "lxml")
        inner_df["操作"] = [
            "https://cszg.mca.gov.cn/mz/upload/pub/load/resource_download.html?"
            + item["onclick"].strip("Download('").strip("')")
            for item in inner_soup.find_all("a", attrs={"style": "color: #0088DB;"})
        ]
        outer_df = outer_df.append(inner_df, ignore_index=True)
    return outer_df


# 慈善中国-募捐信息平台
def charity_china_platform() -> pd.DataFrame:
    """
    慈善中国-募捐信息平台
    https://cszg.mca.gov.cn/biz/ma/csmh/h/csmhhindex.html
    :return: 募捐信息平台
    :rtype: pandas.DataFrame
    """
    url = "https://cszg.mca.gov.cn/biz/ma/csmh/h/csmhhindex.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    info_url = [item["href"] for item in soup.find_all("a", attrs={"target": "_blank"})]
    info_org = [
        item.text for item in soup.find_all("div", attrs={"class": "fk_text_1"})
    ]
    info_title = [
        item.text for item in soup.find_all("div", attrs={"class": "fk_text_2"})
    ]
    info_contact = [
        item.text for item in soup.find_all("div", attrs={"class": "fk_text_3"})
    ]
    info_df = pd.DataFrame([info_url, info_org, info_title, info_contact]).T
    info_df.columns = ["网址", "组织", "名称", "联系方式"]
    return info_df


if __name__ == "__main__":
    # 慈善中国-慈善组织查询
    charity_organization_df = charity_china_organization()
    print(charity_organization_df)

    # 慈善中国-慈善信托查询
    charity_china_trust_df = charity_china_trust()
    print(charity_china_trust_df)

    # 慈善中国-募捐方案备案
    charity_china_plan_df = charity_china_plan()
    print(charity_china_plan_df)

    # 慈善中国-慈善项目进展
    charity_china_progress_df = charity_china_progress()
    print(charity_china_progress_df)

    # 慈善中国-慈善组织年报
    charity_china_report_df = charity_china_report()
    print(charity_china_report_df)

    # 慈善中国-募捐信息平台
    charity_china_platform_df = charity_china_platform()
    print(charity_china_platform_df)
