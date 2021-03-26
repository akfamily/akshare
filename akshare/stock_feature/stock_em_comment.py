# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/3/26 15:28
Desc: 东方财富网-数据中心-特色数据-千股千评
http://data.eastmoney.com/stockcomment/
"""
import demjson
import pandas as pd
import requests


def stock_em_comment() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-千股千评
    http://data.eastmoney.com/stockcomment/
    :return: 千股千评数据
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "QGQP_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "Code",
        "sr": "1",
        "p": "1",
        "ps": "10000",
        "js": "var fHdHpFHW={pages:(tp),data:(x),font:(font)}",
        "filter": "",
        "rt": "52831859",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") :])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "发布时间",
        "代码",
        "名称",
        "最新价",
        "涨跌幅",
        "市盈率",
        "换手率",
        "主力成本",
        "机构参与度",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "综合得分",
        "上升",
        "目前排名",
        "关注指数",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "换手率",
            "市盈率",
            "主力成本",
            "机构参与度",
            "综合得分",
            "上升",
            "目前排名",
            "关注指数",
            "发布时间",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_em_comment_df = stock_em_comment()
    print(stock_em_comment_df)
