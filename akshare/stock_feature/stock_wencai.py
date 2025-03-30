#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/9/21 18:00
Desc: 问财-热门股票排名
https://www.iwencai.com/unifiedwap/home/index
"""

import pandas as pd
import requests

from akshare.utils.cons import headers
from akshare.utils.tqdm import get_tqdm


def stock_hot_rank_wc(date: str = "20240920") -> pd.DataFrame:
    """
    问财-热门股票排名
    https://www.iwencai.com/unifiedwap/result?w=%E7%83%AD%E9%97%A85000%E8%82%A1%E7%A5%A8&querytype=stock&issugs&sign=1620126514335
    :param date: 查询日期
    :type date: str
    :return: 热门股票排名
    :rtype: pandas.DataFrame
    """
    url = "https://www.iwencai.com/gateway/urp/v7/landing/getDataList"
    params = {
        "query": "热门5000股票",
        "urp_sort_way": "desc",
        "urp_sort_index": f"个股热度[{date}]",
        "page": "1",
        "perpage": "100",
        "addheaderindexes": "",
        "condition": '[{"chunkedResult":"热门5000股票","opName":"and","opProperty":"","uiText":'
        '"个股热度排名<=5000且个股热度从大到小排名","sonSize":3,"queryText":'
        '"个股热度排名<=5000且个股热度从大到小排名","relatedSize":3},'
        '{"reportType":"NATURAL_DAILY","dateType":"+区间","indexName":'
        '"个股热度排名","indexProperties":["nodate 1","交易日期 20230817",'
        '"<=5000"],"valueType":"_整型数值","domain":"abs_股票领域","sonSize"'
        ':0,"relatedSize":0,"source":"new_parser","tag":"个股热度排名","type"'
        ':"index","indexPropertiesMap":{"<=":"5000","交易日期":"20230817","nodate":"1"}},'
        '{"opName":"sort","opProperty":"从大到小排名","sonSize":1,"relatedSize":0},'
        '{"reportType":"NATURAL_DAILY","dateType":"+区间","indexName":"个股热度",'
        '"indexProperties":["nodate 1","起始交易日期 20230817","截止交易日期 20230817"],'
        '"valueType":"_浮点型数值","domain":"abs_股票领域","sonSize":0,"relatedSize":0,'
        '"source":"new_parser","tag":"个股热度","type":"index","indexPropertiesMap":'
        '{"起始交易日期":"20230817","截止交易日期":"20230817","nodate":"1"}}]'.replace(
            "20230817", date
        ),
        "codelist": "",
        "indexnamelimit": "",
        "ret": "json_all",
        "source": "Ths_iwencai_Xuangu",
        "date_range[0]": date,
        "date_range[1]": date,
        "urp_use_sort": "1",
        "uuids[0]": "24087",
        "query_type": "stock",
        "comp_id": "6836372",
        "business_cat": "soniu",
        "uuid": "24087",
    }
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, 51), leave=False):
        params.update(
            {
                "page": page,
            }
        )
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["answer"]["components"][0]["data"]["datas"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    try:
        rank_date_str = big_df.columns[1].split("[")[1].strip("]")
    except:  # noqa: E722
        try:
            rank_date_str = big_df.columns[2].split("[")[1].strip("]")
        except:  # noqa: E722
            rank_date_str = date
    big_df.rename(
        columns={
            "index": "序号",
            f"个股热度排名[{rank_date_str}]": "个股热度排名",
            f"个股热度[{rank_date_str}]": "个股热度",
            "code": "股票代码",
            "market_code": "_",
            "最新涨跌幅": "涨跌幅",
            "最新价": "现价",
            "股票代码": "_",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "现价",
            "涨跌幅",
            "个股热度",
            "个股热度排名",
        ]
    ]
    big_df["涨跌幅"] = big_df["涨跌幅"].astype(float).round(2)
    big_df["排名日期"] = rank_date_str
    big_df["现价"] = pd.to_numeric(big_df["现价"], errors="coerce")
    return big_df


if __name__ == "__main__":
    stock_hot_rank_wc_df = stock_hot_rank_wc(date="20240920")
    print(stock_hot_rank_wc_df)
