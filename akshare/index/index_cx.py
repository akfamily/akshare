#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/5 20:00
Desc: 财新数据-财新指数
https://yun.ccxe.com.cn/dataindices/indices
"""

import pandas as pd

from akshare.exceptions import APIError
from akshare.utils import http


def _cx_index_data(index: str, data: dict) -> dict:
    """
    财新数据-财新指数-图表数据
    https://yun.ccxe.com.cn/dataindices/indices
    :param index: 指数接口名，如 "pmi"、"nei"、"cci"
    :type index: str
    :param data: 请求参数；宏观经济指数传 type，可投资指数传 month（空字符串为全部）
    :type data: dict
    :return: 上游返回的 data 字段，含 month（日期）、data（指数值）等列表
    :rtype: dict
    """
    url = f"https://yun.ccxe.com.cn/dataindices/{index}"
    r = http.post(url, data=data)
    data_json = r.json()
    if data_json.get("code") != 0 or not data_json.get("data"):
        raise APIError(f"财新数据返回错误：{data_json.get('msg')}", r.status_code)
    return data_json["data"]


def _cx_macro_index(
    index: str, sub_id: str, name: str, change_field: str
) -> pd.DataFrame:
    """
    财新数据-财新指数-宏观经济指数（月度）
    https://yun.ccxe.com.cn/dataindices/indices
    :param index: 指数接口名，"pmi" 或 "nei"
    :type index: str
    :param sub_id: 子指数代码，如 "COM"、"NEI"、"NEAW"
    :type sub_id: str
    :param name: 指数值列的列名
    :type name: str
    :param change_field: 与上期差值所在的字段；pmi 为 change，nei 为 changeData（nei 的 change 为百分比）
    :type change_field: str
    :return: 日期、指数值、变化值（与上期的差值，首期为空）
    :rtype: pandas.DataFrame
    """
    data = _cx_index_data(index, {"type": sub_id})
    temp_df = pd.DataFrame(
        {"日期": data["month"], name: data["data"], "变化值": data[change_field]}
    )
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df[name] = pd.to_numeric(temp_df[name], errors="coerce")
    temp_df["变化值"] = pd.to_numeric(temp_df["变化值"], errors="coerce")
    return temp_df


def _cx_investment_index(index: str, name: str, change_name: str) -> pd.DataFrame:
    """
    财新数据-财新指数-可投资指数（日度）
    https://yun.ccxe.com.cn/dataindices/indices
    :param index: 指数接口名，如 "cci"、"qli"、"ind"
    :type index: str
    :param name: 指数值列的列名
    :type name: str
    :param change_name: 涨跌幅列的列名
    :type change_name: str
    :return: 日期、指数值、涨跌幅（相对上一交易日，单位为 %，首日为空）；上游只提供指数值，涨跌幅由指数值计算
    :rtype: pandas.DataFrame
    """
    data = _cx_index_data(index, {"month": ""})
    temp_df = pd.DataFrame({"日期": data["month"], name: data["data"]})
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df[name] = pd.to_numeric(temp_df[name], errors="coerce")
    temp_df[change_name] = temp_df[name].pct_change() * 100
    return temp_df


def index_pmi_com_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-标普中国 PMI（原财新中国 PMI）-综合 PMI
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 综合 PMI
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("pmi", "COM", "综合PMI", "change")


def index_pmi_man_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-标普中国 PMI（原财新中国 PMI）-制造业 PMI
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 制造业 PMI
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("pmi", "MAN", "制造业PMI", "change")


def index_pmi_ser_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-标普中国 PMI（原财新中国 PMI）-服务业 PMI
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 服务业 PMI
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("pmi", "SER", "服务业PMI", "change")


def index_nei_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-中国新经济指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 中国新经济指数
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("nei", "NEI", "中国新经济指数", "changeData")


def index_li_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-中国新经济指数-劳动力投入指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 劳动力投入指数
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("nei", "LI", "劳动力投入指数", "changeData")


def index_ci_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-中国新经济指数-资本投入指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 资本投入指数
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("nei", "CI", "资本投入指数", "changeData")


def index_ti_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-中国新经济指数-科技投入指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 科技投入指数
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("nei", "TI", "科技投入指数", "changeData")


def index_neaw_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-中国新经济指数-新经济行业入职平均工资水平
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 新经济行业入职平均工资水平
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("nei", "NEAW", "新经济行业入职平均工资水平", "changeData")


def index_awpr_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-中国新经济指数-新经济入职工资溢价水平
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 新经济入职工资溢价水平
    :rtype: pandas.DataFrame
    """
    return _cx_macro_index("nei", "AWPR", "新经济入职工资溢价水平", "changeData")


def index_cci_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-大宗商品指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 大宗商品指数
    :rtype: pandas.DataFrame
    """
    return _cx_investment_index("cci", "大宗商品指数", "变化值")


def index_qli_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-高质量因子指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 高质量因子指数
    :rtype: pandas.DataFrame
    """
    return _cx_investment_index("qli", "高质量因子指数", "变化幅度")


def index_ai_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-AI策略指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: AI策略指数
    :rtype: pandas.DataFrame
    """
    return _cx_investment_index("ai", "AI策略指数", "变化幅度")


def index_bei_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-基石经济指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 基石经济指数
    :rtype: pandas.DataFrame
    """
    return _cx_investment_index("ind", "基石经济指数", "变化幅度")


def index_neei_cx() -> pd.DataFrame:
    """
    财新数据-财新指数-新动能指数
    https://yun.ccxe.com.cn/dataindices/indices
    :return: 新动能指数
    :rtype: pandas.DataFrame
    """
    return _cx_investment_index("indTwo", "新动能指数", "变化幅度")


if __name__ == "__main__":
    index_pmi_com_cx_df = index_pmi_com_cx()
    print(index_pmi_com_cx_df)

    index_pmi_man_cx_df = index_pmi_man_cx()
    print(index_pmi_man_cx_df)

    index_pmi_ser_cx_df = index_pmi_ser_cx()
    print(index_pmi_ser_cx_df)

    index_nei_cx_df = index_nei_cx()
    print(index_nei_cx_df)

    index_li_cx_df = index_li_cx()
    print(index_li_cx_df)

    index_ci_cx_df = index_ci_cx()
    print(index_ci_cx_df)

    index_ti_cx_df = index_ti_cx()
    print(index_ti_cx_df)

    index_neaw_cx_df = index_neaw_cx()
    print(index_neaw_cx_df)

    index_awpr_cx_df = index_awpr_cx()
    print(index_awpr_cx_df)

    index_cci_cx_df = index_cci_cx()
    print(index_cci_cx_df)

    index_qli_cx_df = index_qli_cx()
    print(index_qli_cx_df)

    index_ai_cx_df = index_ai_cx()
    print(index_ai_cx_df)

    index_bei_cx_df = index_bei_cx()
    print(index_bei_cx_df)

    index_neei_cx_df = index_neei_cx()
    print(index_neei_cx_df)
