# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/17 17:06
Desc: 中国银行保险监督管理委员会-首页-政务信息-行政处罚-银保监分局本级-XXXX行政处罚信息公开表
http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=4115&itemUrl=ItemListRightList.html&itemName=%E9%93%B6%E4%BF%9D%E7%9B%91%E5%88%86%E5%B1%80%E6%9C%AC%E7%BA%A7&itemsubPId=931&itemsubPName=%E8%A1%8C%E6%94%BF%E5%A4%84%E7%BD%9A#2
提取 具体页面 html 页面的 json 接口
http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId=881446.json
2020新接口
"""
import requests
import numpy as np
import pandas as pd

from akshare.bank.cons import cbirc_headers_without_cookie_2020

item_id_list = {
    '机关': '4113',
    '本级': '4114',
    '分局本级': '4115',
}


def bank_fjcf_total_num(item: str = "分局本级") -> int:
    """
    首页-政务信息-行政处罚-银保监分局本级 总页数
    http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=4115&itemUrl=ItemListRightList.html&itemName=%E9%93%B6%E4%BF%9D%E7%9B%91%E5%88%86%E5%B1%80%E6%9C%AC%E7%BA%A7&itemsubPId=931
    :return: 总页数
    :rtype: int
    """
    cbirc_headers = cbirc_headers_without_cookie_2020.copy()
    main_url = "http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocByItemIdAndChild"
    params = {
        "itemId": item_id_list[item],
        "pageSize": "18",
        "pageIndex": "1",
    }
    res = requests.get(main_url, params=params, headers=cbirc_headers)
    return int(res.json()["data"]["total"])


def bank_fjcf_total_page(item: str = "分局本级", begin: int = 1) -> int:
    """
    获取  首页-政务信息-行政处罚-银保监分局本级 总页数
    http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=4115&itemUrl=ItemListRightList.html&itemName=%E9%93%B6%E4%BF%9D%E7%9B%91%E5%88%86%E5%B1%80%E6%9C%AC%E7%BA%A7&itemsubPId=931
    :return: 总页数
    :rtype: int
    """
    cbirc_headers = cbirc_headers_without_cookie_2020.copy()
    main_url = "http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocByItemIdAndChild"
    params = {
        "itemId": item_id_list[item],
        "pageSize": "18",
        "pageIndex": str(begin),
    }
    res = requests.get(main_url, params=params, headers=cbirc_headers)
    if res.json()["data"]["total"] / 18 > int(res.json()["data"]["total"] / 18):
        total_page = int(res.json()["data"]["total"] / 18) + 1
    return total_page


def bank_fjcf_page_url(page: int = 5, item: str = "分局本级", begin: int = 1) -> pd.DataFrame:
    """
    获取 首页-政务信息-行政处罚-银保监分局本级-每一页的 json 数据
    :param page: 需要获取前 page 页的内容, 总页数请通过 bank_fjcf_total_page() 获取
    :type page: int
    :return: 需要的字段
    :rtype: pandas.DataFrame
    """
    cbirc_headers = cbirc_headers_without_cookie_2020.copy()
    main_url = "http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocByItemIdAndChild"
    temp_df = pd.DataFrame()
    for i_page in range(begin, page+begin):
        print(i_page)
        params = {
            "itemId": item_id_list[item],
            "pageSize": "18",
            "pageIndex": str(i_page),
        }
        res = requests.get(main_url, params=params, headers=cbirc_headers)
        temp_df = temp_df.append(pd.DataFrame(res.json()["data"]["rows"]))
    return temp_df[["docId", "docSubtitle", "publishDate", "docFileUrl", "docTitle", "generaltype"]]


def bank_fjcf_table_detail(page: int = 5, item: str = "分局本级", begin: int = 1) -> pd.DataFrame:
    """
    获取 首页-政务信息-行政处罚-银保监分局本级-XXXX行政处罚信息公开表 数据
    :param page: 需要获取前 page 页的内容, 总页数请通过 bank_fjcf_total_page() 获取
    :type page: int
    :return: 返回所有行政处罚信息公开表的集合, 按第一页到最后一页的顺序排列
    :rtype: pandas.DataFrame
    """
    id_list = bank_fjcf_page_url(page=page, item=item, begin=begin)["docId"]
    big_df = pd.DataFrame()
    for item in id_list:
        print(item)
        url = f"http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId={item}.json"
        res = requests.get(url)
        # print(res.json()["data"]["docClob"])
        try:
            table_list = pd.read_html(res.json()["data"]["docClob"])[0]
            table_list = table_list.iloc[:, 3:].values.tolist()
            # 部分旧表缺少字段，所以填充
            if len(table_list) == 7:
                table_list.insert(2, np.nan)
                table_list.insert(3, np.nan)
                table_list.insert(4, np.nan)
            elif len(table_list) == 8:
                table_list.insert(1, np.nan)
                table_list.insert(2, np.nan)
            elif len(table_list) == 9:
                table_list.insert(2, np.nan)
            elif len(table_list) == 11:
                table_list = table_list[2:]
                table_list.insert(2, np.nan)
            # 部分会变成嵌套列表, 这里还原
            table_list = [item[0] if isinstance(
                item, list) else item for item in table_list]
            table_list.append(str(item))
            table_list.append(res.json()["data"]["publishDate"])
            table_df = pd.DataFrame(table_list)
            table_df.columns = ["内容"]
            big_df = big_df.append(table_df.T, ignore_index=True)
            # 解决有些页面缺少字段的问题, 都放到 try 里面
        except:
            print(f"{item} is not table, it will be skip")
            continue
    big_df.columns = [
        "行政处罚决定书文号",
        "姓名",
        "单位",  # 20200108新增
        "单位名称",
        "主要负责人姓名",
        "主要违法违规事实（案由）",
        "行政处罚依据",
        "行政处罚决定",
        "作出处罚决定的机关名称",
        "作出处罚决定的日期",
        "处罚ID",
        "处罚公布日期",
    ]
    return big_df


if __name__ == '__main__':
    bank_fjcf_table_detail_df = bank_fjcf_table_detail(page=2)
    print(bank_fjcf_table_detail_df)
