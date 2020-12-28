# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/28 16:01
Desc: 美国股市(S&P 500)的指数及其收益率，还有常用的14个经济指标
http://www.hec.unil.ch/agoyal/
http://www.hec.unil.ch/agoyal/docs/PredictorData2018.xlsx
"""
import pandas as pd


def agoyal_stock_return(indicator: str = "monthly"):
    """
    This data about will be updated every year at May
    :param indicator: monthly, quarterly or annual
    :type indicator: str
    :return: return data at specific indicator
    :rtype: pandas.DataFrame
    """
    url = "http://www.hec.unil.ch/agoyal/docs/PredictorData2018.xlsx"
    if indicator == "monthly":
        return pd.read_excel(url, sheet_name="Monthly", engine="openpyxl")
    if indicator == "quarterly":
        return pd.read_excel(url, sheet_name="Quarterly", engine="openpyxl")
    if indicator == "annual":
        return pd.read_excel(url, sheet_name="Annual", engine="openpyxl")


if __name__ == '__main__':
    agoyal_stock_return_df = agoyal_stock_return(indicator="monthly")
    print(agoyal_stock_return_df)
