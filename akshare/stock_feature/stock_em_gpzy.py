# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/8/20 18:02
Desc: 东方财富网-数据中心-特色数据-股权质押
东方财富网-数据中心-特色数据-股权质押-股权质押市场概况: http://data.eastmoney.com/gpzy/marketProfile.aspx
东方财富网-数据中心-特色数据-股权质押-上市公司质押比例: http://data.eastmoney.com/gpzy/pledgeRatio.aspx
东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细: http://data.eastmoney.com/gpzy/pledgeDetail.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司: http://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行: http://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-行业数据: http://data.eastmoney.com/gpzy/industryData.aspx
"""
import math

from akshare.utils import demjson
import pandas as pd
import requests
from tqdm import tqdm


def stock_em_gpzy_profile() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
    http://data.eastmoney.com/gpzy/marketProfile.aspx
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    temp_df = pd.DataFrame()
    params = {
        "type": "ZD_SUM",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "tdate",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var zvxnZOnT={pages:(tp),data:(x),font:(font)}",
        "rt": "52583914",
    }
    res = requests.get(url, params=params)
    data_text = res.text
    data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
    map_dict = dict(
        zip(
            pd.DataFrame(data_json["font"]["FontMapping"])["code"],
            pd.DataFrame(data_json["font"]["FontMapping"])["value"],
        )
    )
    for key, value in map_dict.items():
        data_text = data_text.replace(key, str(value))
    data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
    temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "交易日期",
        "sc_zsz",
        "平均质押比例(%)",
        "涨跌幅",
        "A股质押总比例(%)",
        "质押公司数量",
        "质押笔数",
        "质押总股数(股)",
        "质押总市值(元)",
        "沪深300指数",
    ]
    temp_df = temp_df[
        [
            "交易日期",
            "平均质押比例(%)",
            "涨跌幅",
            "A股质押总比例(%)",
            "质押公司数量",
            "质押笔数",
            "质押总股数(股)",
            "质押总市值(元)",
            "沪深300指数",
        ]
    ]
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    return temp_df


def stock_em_gpzy_pledge_ratio(trade_date: str = "2020-08-07") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
    http://data.eastmoney.com/gpzy/pledgeRatio.aspx
    :param trade_date: 指定交易日, 访问 http://data.eastmoney.com/gpzy/pledgeRatio.aspx 查询
    :type trade_date: str
    :return: 上市公司质押比例
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    temp_df = pd.DataFrame()
    params = {
        "type": "ZD_QL_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "amtshareratio",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var rlJqyOhv={pages:(tp),data:(x),font:(font)}",
        "filter": f"(tdate='{trade_date}')",
        "rt": "52584436",
    }
    res = requests.get(url, params=params)
    data_text = res.text
    data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
    map_dict = dict(
        zip(
            pd.DataFrame(data_json["font"]["FontMapping"])["code"],
            pd.DataFrame(data_json["font"]["FontMapping"])["value"],
        )
    )
    for key, value in map_dict.items():
        data_text = data_text.replace(key, str(value))
    data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
    temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "股票代码",
        "股票简称",
        "交易日期",
        "所属行业",
        "blfb",
        "质押比例(%)",
        "质押股数(股)",
        "质押市值(元)",
        "质押笔数",
        "无限售股质押数(股)",
        "限售股质押数(股)",
        "近一年涨跌幅(%)",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "交易日期",
            "所属行业",
            "质押比例(%)",
            "质押股数(股)",
            "质押市值(元)",
            "质押笔数",
            "无限售股质押数(股)",
            "限售股质押数(股)",
            "近一年涨跌幅(%)",
        ]
    ]
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    return temp_df


def _get_page_num_gpzy_market_pledge_ratio_detail() -> int:
    """
    东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    http://data.eastmoney.com/gpzy/pledgeDetail.aspx
    :return: int 获取 重要股东股权质押明细 的总页数
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'sortColumns': 'NOTICE_DATE',
        'sortTypes': '-1',
        'pageSize': '500',
        'pageNumber': '1',
        'reportName': 'RPTA_APP_ACCUMDETAILS',
        'columns': 'ALL',
        'quoteColumns': '',
        'source': 'WEB',
        'client': 'WEB',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = math.ceil(int(data_json['result']['count']) / 500)
    return total_page


def stock_em_gpzy_pledge_ratio_detail() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    http://data.eastmoney.com/gpzy/pledgeDetail.aspx
    :return: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    page_num = _get_page_num_gpzy_market_pledge_ratio_detail()
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params = {
            'sortColumns': 'NOTICE_DATE',
            'sortTypes': '-1',
            'pageSize': '500',
            'pageNumber': page,
            'reportName': 'RPTA_APP_ACCUMDETAILS',
            'columns': 'ALL',
            'quoteColumns': '',
            'source': 'WEB',
            'client': 'WEB',
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = temp_df.append(pd.DataFrame(data_json['result']["data"]), ignore_index=True)
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "股票简称",
        "_",
        "股票代码",
        "股东名称",
        "_",
        "_",
        "_",
        "公告日期",
        "质押机构",
        "质押股份数量",
        "占所持股份比例",
        "占总股本比例",
        "质押日收盘价",
        "质押开始日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "预估平仓线",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "最新价",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "股东名称",
            "质押股份数量",
            "占所持股份比例",
            "占总股本比例",
            "质押机构",
            "最新价",
            "质押日收盘价",
            "预估平仓线",
            "质押开始日期",
            "公告日期",
        ]
    ]
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
    temp_df["质押开始日期"] = pd.to_datetime(temp_df["质押开始日期"]).dt.date
    return temp_df


def _get_page_num_gpzy_distribute_statistics_company() -> int:
    """
    东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司
    http://data.eastmoney.com/gpzy/distributeStatistics.aspx
    :return: int 获取 质押机构分布统计-证券公司 的总页数
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "GDZY_ZYJG_SUM",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "scode_count",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var bLnpEFtJ={pages:(tp),data:(x),font:(font)}",
        "filter": "(hy_name='券商信托')",
        "rt": "52584592",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_gpzy_distribute_statistics_company() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司
    http://data.eastmoney.com/gpzy/distributeStatistics.aspx
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_gpzy_distribute_statistics_company()
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=True):
        params = {
            "type": "GDZY_ZYJG_SUM",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "cmd": "",
            "st": "scode_count",
            "sr": "-1",
            "p": str(page),
            "ps": "5000",
            "js": "var bLnpEFtJ={pages:(tp),data:(x),font:(font)}",
            "filter": "(hy_name='券商信托')",
            "rt": "52584592",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "质押公司股票代码",
        "_",
        "jg_yjx_type_1",
        "jg_yjx_type_2",
        "质押机构",
        "行业名称",
        "质押公司数量",
        "质押笔数",
        "质押数量(股)",
        "未达预警线比例(%)",
        "达到预警线未达平仓线比例(%)",
        "达到平仓线比例(%)",
    ]
    temp_df = temp_df[
        [
            "质押公司股票代码",
            "质押机构",
            "行业名称",
            "质押公司数量",
            "质押笔数",
            "质押数量(股)",
            "未达预警线比例(%)",
            "达到预警线未达平仓线比例(%)",
            "达到平仓线比例(%)",
        ]
    ]
    return temp_df


def _get_page_num_gpzy_distribute_statistics_bank() -> int:
    """
    东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
    http://data.eastmoney.com/gpzy/distributeStatistics.aspx
    :return: int 获取 质押机构分布统计-银行 的总页数
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "GDZY_ZYJG_SUM",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "scode_count",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var AQxIdDuK={pages:(tp),data:(x),font:(font)}",
        "filter": "(hy_name='银行')",
        "rt": "52584617",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_gpzy_distribute_statistics_bank() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
    http://data.eastmoney.com/gpzy/distributeStatistics.aspx
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_gpzy_distribute_statistics_company()
    temp_df = pd.DataFrame()
    for page in range(1, page_num + 1):
        print(f"一共{page_num}页, 正在下载第{page}页")
        params = {
            "type": "GDZY_ZYJG_SUM",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "cmd": "",
            "st": "scode_count",
            "sr": "-1",
            "p": str(page),
            "ps": "5000",
            "js": "var AQxIdDuK={pages:(tp),data:(x),font:(font)}",
            "filter": "(hy_name='银行')",
            "rt": "52584617",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "质押公司股票代码",
        "_",
        "jg_yjx_type_1",
        "jg_yjx_type_2",
        "质押机构",
        "行业名称",
        "质押公司数量",
        "质押笔数",
        "质押数量(股)",
        "未达预警线比例(%)",
        "达到预警线未达平仓线比例(%)",
        "达到平仓线比例(%)",
    ]
    temp_df = temp_df[
        [
            "质押公司股票代码",
            "质押机构",
            "行业名称",
            "质押公司数量",
            "质押笔数",
            "质押数量(股)",
            "未达预警线比例(%)",
            "达到预警线未达平仓线比例(%)",
            "达到平仓线比例(%)",
        ]
    ]
    return temp_df


def _get_page_num_gpzy_industry_data() -> int:
    """
    东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
    http://data.eastmoney.com/gpzy/industryData.aspx
    :return: int 获取 上市公司质押比例-行业数据 的总页数
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "ZD_HY_SUM",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "amtshareratio_pj",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var SIqThurI={pages:(tp),data:(x),font:(font)}",
        "rt": "52584617",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_gpzy_industry_data() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
    http://data.eastmoney.com/gpzy/industryData.aspx
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_gpzy_industry_data()
    temp_df = pd.DataFrame()
    for page in range(1, page_num + 1):
        print(f"一共{page_num}页, 正在下载第{page}页")
        params = {
            "type": "ZD_HY_SUM",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "cmd": "",
            "st": "amtshareratio_pj",
            "sr": "-1",
            "p": str(page),
            "ps": "5000",
            "js": "var SIqThurI={pages:(tp),data:(x),font:(font)}",
            "rt": "52584617",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "统计时间",
        "-",
        "行业",
        "平均质押比例(%)",
        "公司家数",
        "质押总笔数",
        "质押总股本",
        "最新质押市值",
    ]
    temp_df = temp_df[["统计时间", "行业", "平均质押比例(%)", "公司家数", "质押总笔数", "质押总股本", "最新质押市值"]]
    temp_df["统计时间"] = pd.to_datetime(temp_df["统计时间"])
    return temp_df


if __name__ == "__main__":
    stock_em_gpzy_profile_df = stock_em_gpzy_profile()
    print(stock_em_gpzy_profile_df)

    stock_em_gpzy_pledge_ratio_df = stock_em_gpzy_pledge_ratio(trade_date="2021-04-30")
    print(stock_em_gpzy_pledge_ratio_df)

    stock_em_gpzy_pledge_ratio_detail_df = stock_em_gpzy_pledge_ratio_detail()
    print(stock_em_gpzy_pledge_ratio_detail_df)

    stock_em_gpzy_distribute_statistics_company_df = (
        stock_em_gpzy_distribute_statistics_company()
    )
    print(stock_em_gpzy_distribute_statistics_company_df)

    stock_em_gpzy_distribute_statistics_bank_df = stock_em_gpzy_distribute_statistics_bank()
    print(stock_em_gpzy_distribute_statistics_bank_df)

    stock_em_gpzy_industry_data_df = stock_em_gpzy_industry_data()
    print(stock_em_gpzy_industry_data_df)
