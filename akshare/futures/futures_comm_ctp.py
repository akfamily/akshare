#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/30 17:00
Desc: openctp 期货交易费用参照表
http://openctp.cn/fees.html
"""

import pandas as pd
import requests
from akshare.request_config_manager import get_headers_and_timeout
from io import BytesIO


def futures_fees_info() -> pd.DataFrame:
    """
    openctp 期货交易费用参照表
    http://openctp.cn/fees.html
    :return: 期货交易费用参照表
    :rtype: pandas.DataFrame
    """
    url = "http://openctp.cn/fees.html"
    headers, timeout = get_headers_and_timeout(locals().get('headers', {}), locals().get('timeout', None))
    res = requests.get(url, headers=headers, timeout=timeout)
    res.raise_for_status()
    temp_df = pd.read_html(BytesIO(res.content))[0]
    return temp_df


if __name__ == "__main__":
    futures_fees_info_df = futures_fees_info()
    print(futures_fees_info_df)
