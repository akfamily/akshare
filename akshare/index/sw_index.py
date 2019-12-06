# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/6 14:34
contact: jindaxiang@163.com
desc: 获取申万指数
http://www.swsindex.com/IdxMain.aspx
"""
import time

import pandas as pd
import requests
import json

from akshare.index.cons import sw_headers, sw_payload, sw_url


def sw_level_one_index_spot():
    result = []
    for i in range(1, 3):
        payload = sw_payload.copy()
        payload.update({"p": i})
        payload.update({"timed": int(time.time() * 1000)})
        req = requests.post(sw_url, headers=sw_headers, data=payload)
        data = req.content.decode()
        data = data.replace("'", '"')
        data = json.loads(data)
        result.extend(data["root"])
    result = pd.DataFrame(result)
    result["L2"] = result["L2"].str.strip()
    result.columns = ["指数代码", "指数名称", "昨收盘", "今开盘", "成交额", "最高价", "最低价", "最新价", "成交量"]
    return result


if __name__ == "__main__":
    sw_index_df = sw_level_one_index_spot()
    print(sw_index_df)
