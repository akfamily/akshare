# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/8/27 15:59
Desc: REITs 行情及信息
http://quote.eastmoney.com/center/gridlist.html#fund_reits_all
https://www.jisilu.cn/data/cnreits/#CnReits
"""
import pandas as pd
import requests


def reits_realtime_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-REITs-沪深 REITs
    http://quote.eastmoney.com/center/gridlist.html#fund_reits_all
    :return: 沪深 REITs-实时行情
    :rtype: pandas.DataFrame
    """
    url = "http://95.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "20",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:1 t:9 e:97,m:0 t:10 e:97",
        "fields": "f2,f3,f4,f5,f6,f12,f14,f15,f16,f17,f18",
        "_": "1630048369992",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.rename(
        {
            "index": "序号",
            "f2": "最新价",
            "f3": "涨跌幅",
            "f4": "涨跌额",
            "f5": "成交量",
            "f6": "成交额",
            "f12": "代码",
            "f14": "名称",
            "f15": "最高价",
            "f16": "最低价",
            "f17": "开盘价",
            "f18": "昨收",
        },
        axis=1,
        inplace=True,
    )

    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "成交量",
            "成交额",
            "开盘价",
            "最高价",
            "最低价",
            "昨收",
        ]
    ]
    return temp_df


def reits_info_jsl() -> pd.DataFrame:
    """
    集思录-实时数据-REITs-A股 REITs
    https://www.jisilu.cn/data/cnreits/#CnReits
    :return: A股 REITs
    :rtype: pandas.DataFrame
    """
    url = "https://www.jisilu.cn/data/cnreits/list/"
    params = {"___jsl": "LST___t=1630052485199"}
    payload = {"rp": "50", "page": "1"}
    r = requests.get(url, params=params, json=payload)
    data_json = r.json()
    temp_df = pd.DataFrame([item["cell"] for item in data_json["rows"]])
    temp_df.rename(
        {
            "fund_id": "代码",
            "fund_nm": "简称",
            "full_nm": "全称",
            "project_type": "项目类型",
            "price": "现价",
            "increase_rt": "涨幅",
            "volume": "成交额",
            "nav": "净值",
            "nav_dt": "净值日期",
            "discount_rt": "折价率",
            "maturity_dt": "到期日",
            "fund_company": "基金公司",
            "urls": "链接地址",
            "last_dt": "更新日期",
            "last_time": "更新时间",
            "unit_total": "规模",
            "left_year": "剩余年限",
        },
        axis=1,
        inplace=True,
    )

    temp_df = temp_df[
        [
            "代码",
            "简称",
            "现价",
            "涨幅",
            "成交额",
            "净值",
            "净值日期",
            "折价率",
            "规模",
            "到期日",
            "剩余年限",
            "全称",
            "项目类型",
            "基金公司",
        ]
    ]
    temp_df['现价'] = pd.to_numeric(temp_df['现价'])
    temp_df['涨幅'] = pd.to_numeric(temp_df['涨幅'])
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'])
    temp_df['净值'] = pd.to_numeric(temp_df['净值'])
    temp_df['折价率'] = pd.to_numeric(temp_df['折价率'])
    temp_df['规模'] = pd.to_numeric(temp_df['规模'])
    temp_df['剩余年限'] = pd.to_numeric(temp_df['剩余年限'])
    return temp_df


if __name__ == "__main__":
    reits_realtime_em_df = reits_realtime_em()
    print(reits_realtime_em_df)

    reits_info_jsl_df = reits_info_jsl()
    print(reits_info_jsl_df)
