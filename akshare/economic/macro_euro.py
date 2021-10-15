# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2019/10/21 12:08
Desc: 金十数据中心-经济指标-欧元区
金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平
金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场
金十数据中心-经济指标-欧元区-贸易状况
金十数据中心-经济指标-欧元区-产业指标
金十数据中心-经济指标-欧元区-领先指标
"""
import json
import time

import pandas as pd
import requests


# 金十数据中心-经济指标-欧元区-国民经济运行状况
# 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
# 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况-欧元区季度GDP年率报告
def macro_euro_gdp_yoy():
    """
    欧元区季度GDP年率报告, 数据区间从20131114-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_gdp_yoy
    https://cdn.jin10.com/dc/reports/dc_eurozone_gdp_yoy_all.js?v=1578578160
    :return: 欧元区季度GDP年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_gdp_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区季度GDP年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "gdp_yoy"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI月率报告
def macro_euro_cpi_mom():
    """
    欧元区CPI月率报告, 数据区间从19900301-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_cpi_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_cpi_mom_all.js?v=1578578318
    :return: 欧元区CPI月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_cpi_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区CPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi_mom"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI年率报告
def macro_euro_cpi_yoy():
    """
    欧元区CPI年率报告, 数据区间从19910201-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_cpi_yoy
    https://cdn.jin10.com/dc/reports/dc_eurozone_cpi_yoy_all.js?v=1578578404
    :return: 欧元区CPI年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_cpi_yoy_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区CPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "cpi_yoy"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区PPI月率报告
def macro_euro_ppi_mom():
    """
    欧元区PPI月率报告, 数据区间从19810301-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_ppi_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_ppi_mom_all.js?v=1578578493
    :return: 欧元区PPI月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_ppi_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区PPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "ppi_mom"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区零售销售月率报告
def macro_euro_retail_sales_mom():
    """
    欧元区零售销售月率报告, 数据区间从20000301-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_retail_sales_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_retail_sales_mom_all.js?v=1578578576
    :return: 欧元区零售销售月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_retail_sales_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区零售销售月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "retail_sales_mom"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区季调后就业人数季率报告
def macro_euro_employment_change_qoq():
    """
    欧元区季调后就业人数季率报告, 数据区间从20083017-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_employment_change_qoq
    https://cdn.jin10.com/dc/reports/dc_eurozone_employment_change_qoq_all.js?v=1578578699
    :return: 欧元区季调后就业人数季率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_employment_change_qoq_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区季调后就业人数季率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "employment_change_qoq"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区失业率报告
def macro_euro_unemployment_rate_mom():
    """
    欧元区失业率报告, 数据区间从19980501-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_unemployment_rate_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_unemployment_rate_mom_all.js?v=1578578767
    :return: 欧元区失业率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_unemployment_rate_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区失业率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "unemployment_rate_mom"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-贸易状况-欧元区未季调贸易帐报告
def macro_euro_trade_balance():
    """
    欧元区未季调贸易帐报告, 数据区间从19990201-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_trade_balance_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_trade_balance_mom_all.js?v=1578577862
    :return: 欧元区未季调贸易帐报告-今值(亿欧元)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_trade_balance_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区未季调贸易帐报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿欧元)"]
    temp_df.name = "trade_balance"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-贸易状况-欧元区经常帐报告
def macro_euro_current_account_mom():
    """
    欧元区经常帐报告, 数据区间从20080221-至今, 前两个值需要去掉
    https://datacenter.jin10.com/reportType/dc_eurozone_current_account_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_current_account_mom_all.js?v=1578577976
    :return: 欧元区经常帐报告-今值(亿欧元)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_current_account_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区经常帐报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿欧元)"]
    temp_df.name = "current_account_mom"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-产业指标-欧元区工业产出月率报告
def macro_euro_industrial_production_mom():
    """
    欧元区工业产出月率报告, 数据区间从19910301-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_industrial_production_mom
    https://cdn.jin10.com/dc/reports/dc_eurozone_industrial_production_mom_all.js?v=1578577377
    :return: 欧元区工业产出月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_industrial_production_mom_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区工业产出月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "industrial_production_mom"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-欧元区-产业指标-欧元区制造业PMI初值报告
def macro_euro_manufacturing_pmi():
    """
    欧元区制造业PMI初值报告, 数据区间从20080222-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_manufacturing_pmi
    https://cdn.jin10.com/dc/reports/dc_eurozone_manufacturing_pmi_all.js?v=1578577537
    :return: 欧元区制造业PMI初值报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_manufacturing_pmi_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区制造业PMI初值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "manufacturing_pmi"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-产业指标-欧元区服务业PMI终值报告
def macro_euro_services_pmi():
    """
    欧元区服务业PMI终值报告, 数据区间从20080222-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_services_pmi
    https://cdn.jin10.com/dc/reports/dc_eurozone_services_pmi_all.js?v=1578577639
    :return:欧元区服务业PMI终值报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_services_pmi_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区服务业PMI终值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "services_pmi"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-领先指标-欧元区ZEW经济景气指数报告
def macro_euro_zew_economic_sentiment():
    """
    欧元区ZEW经济景气指数报告, 数据区间从20080212-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_zew_economic_sentiment
    https://cdn.jin10.com/dc/reports/dc_eurozone_zew_economic_sentiment_all.js?v=1578577013
    :return: 欧元区ZEW经济景气指数报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_zew_economic_sentiment_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区ZEW经济景气指数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "zew_economic_sentiment"
    temp_df = temp_df.astype(float)
    temp_df = temp_df[temp_df != 0]
    return temp_df


# 金十数据中心-经济指标-欧元区-领先指标-欧元区Sentix投资者信心指数报告
def macro_euro_sentix_investor_confidence():
    """
    欧元区Sentix投资者信心指数报告, 数据区间从20020801-至今
    https://datacenter.jin10.com/reportType/dc_eurozone_sentix_investor_confidence
    https://cdn.jin10.com/dc/reports/dc_eurozone_sentix_investor_confidence_all.js?v=1578577195
    :return: 欧元区Sentix投资者信心指数报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_eurozone_sentix_investor_confidence_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["欧元区Sentix投资者信心指数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    temp_df.name = "sentix_investor_confidence"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-伦敦金属交易所(LME)-持仓报告
def macro_euro_lme_holding():
    """
    伦敦金属交易所(LME)-持仓报告, 数据区间从 20151022-至今
    https://datacenter.jin10.com/reportType/dc_lme_traders_report
    https://cdn.jin10.com/data_center/reports/lme_position.json?_=1591533934658
    :return: 伦敦金属交易所(LME)-持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {
        "_": str(int(round(t * 1000)))
    }
    r = requests.get("https://cdn.jin10.com/data_center/reports/lme_position.json", params=params)
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.fillna(value="[0, 0, 0]", inplace=True)
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


# 金十数据中心-伦敦金属交易所(LME)-库存报告
def macro_euro_lme_stock():
    """
    伦敦金属交易所(LME)-库存报告, 数据区间从 20140702-至今
    https://datacenter.jin10.com/reportType/dc_lme_report
    https://cdn.jin10.com/data_center/reports/lme_stock.json?_=1591535304783
    :return: 伦敦金属交易所(LME)-库存报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {
        "_": str(int(round(t * 1000)))
    }
    r = requests.get("https://cdn.jin10.com/data_center/reports/lme_stock.json", params=params)
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


if __name__ == "__main__":
    # 金十数据中心-经济指标-欧元区-国民经济运行状况
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况-欧元区季度GDP年率报告
    macro_euro_gdp_yoy_df = macro_euro_gdp_yoy()
    print(macro_euro_gdp_yoy_df)

    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI月率报告
    macro_euro_cpi_mom_df = macro_euro_cpi_mom()
    print(macro_euro_cpi_mom_df)
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI年率报告
    macro_euro_cpi_yoy_df = macro_euro_cpi_yoy()
    print(macro_euro_cpi_yoy_df)
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区PPI月率报告
    macro_euro_ppi_mom_df = macro_euro_ppi_mom()
    print(macro_euro_ppi_mom_df)
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区零售销售月率报告
    macro_euro_retail_sales_mom_df = macro_euro_retail_sales_mom()
    print(macro_euro_retail_sales_mom_df)

    # 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区季调后就业人数季率报告
    macro_euro_employment_change_qoq_df = macro_euro_employment_change_qoq()
    print(macro_euro_employment_change_qoq_df)
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区失业率报告
    macro_euro_unemployment_rate_mom_df = macro_euro_unemployment_rate_mom()
    print(macro_euro_unemployment_rate_mom_df)
    # 金十数据中心-经济指标-欧元区-贸易状况
    # 金十数据中心-经济指标-欧元区-贸易状况-欧元区未季调贸易帐报告
    macro_euro_trade_balance_df = macro_euro_trade_balance()
    print(macro_euro_trade_balance_df)
    # 金十数据中心-经济指标-欧元区-贸易状况-欧元区经常帐报告
    macro_euro_current_account_mom_df = macro_euro_current_account_mom()
    print(macro_euro_current_account_mom_df)
    # 金十数据中心-经济指标-欧元区-产业指标
    # 金十数据中心-经济指标-欧元区-产业指标-欧元区工业产出月率报告
    macro_euro_industrial_production_mom_df = macro_euro_industrial_production_mom()
    print(macro_euro_industrial_production_mom_df)
    # 金十数据中心-经济指标-欧元区-产业指标-欧元区制造业PMI初值报告
    macro_euro_manufacturing_pmi_df = macro_euro_manufacturing_pmi()
    print(macro_euro_manufacturing_pmi_df)
    # 金十数据中心-经济指标-欧元区-产业指标-欧元区服务业PMI终值报告
    macro_euro_services_pmi_df = macro_euro_services_pmi()
    print(macro_euro_services_pmi_df)
    # 金十数据中心-经济指标-欧元区-领先指标
    # 金十数据中心-经济指标-欧元区-领先指标-欧元区ZEW经济景气指数报告
    macro_euro_zew_economic_sentiment_df = macro_euro_zew_economic_sentiment()
    print(macro_euro_zew_economic_sentiment_df)
    # 金十数据中心-经济指标-欧元区-领先指标-欧元区Sentix投资者信心指数报告
    macro_euro_sentix_investor_confidence_df = macro_euro_sentix_investor_confidence()
    print(macro_euro_sentix_investor_confidence_df)

    # 金十数据中心-伦敦金属交易所(LME)-持仓报告
    macro_euro_lme_holding_df = macro_euro_lme_holding()
    print(macro_euro_lme_holding_df)
    # 金十数据中心-伦敦金属交易所(LME)-库存报告
    macro_euro_lme_stock_df = macro_euro_lme_stock()
    print(macro_euro_lme_stock_df)
