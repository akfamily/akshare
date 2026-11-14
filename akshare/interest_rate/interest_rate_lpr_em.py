#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 东方财富-数据中心-经济数据-中国-LPR 品种数据
https://data.eastmoney.com/cjsj/globalRateLPR.html
"""

import pandas as pd
from akshare.utils import http
from akshare.utils.tqdm import get_tqdm


def interest_rate_lpr_em() -> pd.DataFrame:
    """
    LPR品种详细数据
    https://data.eastmoney.com/cjsj/globalRateLPR.html
    :return: LPR品种详细数据
    :rtype: pandas.DataFrame
    """
    import warnings

    warnings.filterwarnings(action="ignore", category=FutureWarning)

    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPTA_WEB_RATE",
        "columns": "ALL",
        "sortColumns": "TRADE_DATE",
        "sortTypes": "-1",
        "token": "894050c76af8597a853f5b408b759f5d",
        "pageNumber": "1",
        "pageSize": "500",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = http.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df["TRADE_DATE"] = pd.to_datetime(big_df["TRADE_DATE"], errors="coerce").dt.date
    big_df["LPR1Y"] = pd.to_numeric(big_df["LPR1Y"], errors="coerce")
    big_df["LPR5Y"] = pd.to_numeric(big_df["LPR5Y"], errors="coerce")
    big_df["RATE_1"] = pd.to_numeric(big_df["RATE_1"], errors="coerce")
    big_df["RATE_2"] = pd.to_numeric(big_df["RATE_2"], errors="coerce")
    big_df = big_df.sort_values(by=["TRADE_DATE"])
    big_df = big_df.reset_index(drop=True)
    return big_df


if __name__ == "__main__":
    interest_rate_lpr_em_df = interest_rate_lpr_em()
    print(interest_rate_lpr_em_df)
