#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 金十数据-上海银行间同业拆放利率与香港银行同业拆息报告
https://datacenter.jin10.com/market
"""

import time
import pandas as pd
from akshare.utils import http


def interest_rate_shibor_js() -> pd.DataFrame:
    """
    上海银行业同业拆借报告，数据区间从20170317-至今
    https://datacenter.jin10.com/reportType/dc_shibor
    https://cdn.jin10.com/dc/reports/dc_shibor_all.js?v=1578755058
    :return: 上海银行业同业拆借报告-今值(%)
    :rtype: pandas.DataFrame
    """
    import numpy as np

    t = time.time()
    params = {"_": t}
    res = http.get(
        url="https://cdn.jin10.com/data_center/reports/il_1.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df = temp_df.fillna(value="--")
    big_df["O/N-定价"] = temp_df["O/N"].apply(lambda x: x[0])
    big_df["O/N-涨跌幅"] = temp_df["O/N"].apply(lambda x: x[1])
    big_df["1W-定价"] = temp_df["1W"].apply(lambda x: x[0])
    big_df["1W-涨跌幅"] = temp_df["1W"].apply(lambda x: x[1])
    big_df["2W-定价"] = temp_df["2W"].apply(lambda x: x[0])
    big_df["2W-涨跌幅"] = temp_df["2W"].apply(lambda x: x[1])
    big_df["1M-定价"] = temp_df["1M"].apply(lambda x: x[0])
    big_df["1M-涨跌幅"] = temp_df["1M"].apply(lambda x: x[1])
    big_df["3M-定价"] = temp_df["3M"].apply(lambda x: x[0])
    big_df["3M-涨跌幅"] = temp_df["3M"].apply(lambda x: x[1])
    big_df["6M-定价"] = temp_df["6M"].apply(lambda x: x[0])
    big_df["6M-涨跌幅"] = temp_df["6M"].apply(lambda x: x[1])
    big_df["9M-定价"] = temp_df["9M"].apply(lambda x: x[0])
    big_df["9M-涨跌幅"] = temp_df["9M"].apply(lambda x: x[1])
    big_df["1Y-定价"] = temp_df["1Y"].apply(lambda x: x[0])
    big_df["1Y-涨跌幅"] = temp_df["1Y"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", np.nan))
    big_df = big_df.apply(lambda x: x.replace([None], np.nan))
    for item in big_df.columns:
        big_df[item] = pd.to_numeric(big_df[item], errors="coerce")
    big_df = big_df.sort_index()
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    return big_df


def interest_rate_hibor_js() -> pd.DataFrame:
    """
    香港同业拆借报告，数据区间从 20170320-至今
    https://datacenter.jin10.com/reportType/dc_hk_market_info
    https://cdn.jin10.com/dc/reports/dc_hk_market_info_all.js?v=1578755471
    :return: 香港同业拆借报告-今值(%)
    :rtype: pandas.DataFrame
    """
    import numpy as np

    t = time.time()
    params = {"_": t}
    res = http.get(
        url="https://cdn.jin10.com/data_center/reports/il_2.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df = temp_df.fillna(value="--")
    big_df["1W-定价"] = temp_df["1W"].apply(lambda x: x[0])
    big_df["1W-涨跌幅"] = temp_df["1W"].apply(lambda x: x[1])
    big_df["2W-定价"] = temp_df["2W"].apply(lambda x: x[0])
    big_df["2W-涨跌幅"] = temp_df["2W"].apply(lambda x: x[1])
    big_df["1M-定价"] = temp_df["1M"].apply(lambda x: x[0])
    big_df["1M-涨跌幅"] = temp_df["1M"].apply(lambda x: x[1])
    big_df["3M-定价"] = temp_df["3M"].apply(lambda x: x[0])
    big_df["3M-涨跌幅"] = temp_df["3M"].apply(lambda x: x[1])
    big_df["6M-定价"] = temp_df["6M"].apply(lambda x: x[0])
    big_df["6M-涨跌幅"] = temp_df["6M"].apply(lambda x: x[1])
    big_df["1Y-定价"] = temp_df["1Y"].apply(lambda x: x[0])
    big_df["1Y-涨跌幅"] = temp_df["1Y"].apply(lambda x: x[1])
    big_df["ON-定价"] = temp_df["ON"].apply(lambda x: x[0])
    big_df["ON-涨跌幅"] = temp_df["ON"].apply(lambda x: x[1])
    big_df["2M-定价"] = temp_df["2M"].apply(lambda x: x[0])
    big_df["2M-涨跌幅"] = temp_df["2M"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", np.nan))
    big_df = big_df.apply(lambda x: x.replace([None], np.nan))
    for item in big_df.columns:
        big_df[item] = pd.to_numeric(big_df[item], errors="coerce")
    big_df = big_df.sort_index()
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    return big_df


if __name__ == "__main__":
    interest_rate_shibor_js_df = interest_rate_shibor_js()
    print(interest_rate_shibor_js_df)

    interest_rate_hibor_js_df = interest_rate_hibor_js()
    print(interest_rate_hibor_js_df)
