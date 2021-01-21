# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/20 11:02
Desc: 东方财富网-数据中心-特色数据-股权质押
东方财富网-数据中心-特色数据-股权质押-股权质押市场概况: http://data.eastmoney.com/gpzy/marketProfile.aspx
东方财富网-数据中心-特色数据-股权质押-上市公司质押比例: http://data.eastmoney.com/gpzy/pledgeRatio.aspx
东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细: http://data.eastmoney.com/gpzy/pledgeDetail.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司: http://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行: http://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-行业数据: http://data.eastmoney.com/gpzy/industryData.aspx
"""
import requests
import demjson
import pandas as pd
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
    data_json = demjson.decode(data_text[data_text.find("={") + 1:])
    map_dict = dict(
        zip(
            pd.DataFrame(data_json["font"]["FontMapping"])["code"],
            pd.DataFrame(data_json["font"]["FontMapping"])["value"],
        )
    )
    for key, value in map_dict.items():
        data_text = data_text.replace(key, str(value))
    data_json = demjson.decode(data_text[data_text.find("={") + 1:])
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
    data_json = demjson.decode(data_text[data_text.find("={") + 1:])
    map_dict = dict(
        zip(
            pd.DataFrame(data_json["font"]["FontMapping"])["code"],
            pd.DataFrame(data_json["font"]["FontMapping"])["value"],
        )
    )
    for key, value in map_dict.items():
        data_text = data_text.replace(key, str(value))
    data_json = demjson.decode(data_text[data_text.find("={") + 1:])
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
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "GDZY_LB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "ndate",
        "sr": "-1",
        "p": "2",
        "ps": "5000",
        "js": "var oiIxTSgC={pages:(tp),data:(x),font:(font)}",
        "filter": "(datatype=1)",
        "rt": "52584576",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
    return data_json["pages"]


def stock_em_gpzy_pledge_ratio_detail() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    http://data.eastmoney.com/gpzy/pledgeDetail.aspx
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_gpzy_market_pledge_ratio_detail()
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "GDZY_LB",
            "token": "70f12f2f4f091e459a279469fe49eca5",
            "cmd": "",
            "st": "ndate",
            "sr": "-1",
            "p": str(page),
            "ps": "5000",
            "js": "var oiIxTSgC={pages:(tp),data:(x),font:(font)}",
            "filter": "(datatype=1)",
            "rt": "52584576",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "股票代码",
        "股票简称",
        "eitime",
        "eutime",
        "eid",
        "ccode",
        "公告日期",
        "upd",
        "sharehdcode",
        "gdmc",
        "股东名称",
        "sharehdnum",
        "质押开始日期",
        "jysj",
        "enddate",
        "fcode",
        "质押机构",
        "jglx",
        "-",
        "-",
        "pledgepur",
        "frozenreason",
        "remark",
        "newprice",
        "instcode",
        "relinstcode",
        "jg_scode",
        "zyjg_ccode",
        "pname",
        "yjx_pcx_type",
        "syscbl",
        "syscsz",
        "gd_count",
        "jg_sname",
        "yjx_min",
        "yjx_max",
        "yjx_row",
        "pcx_min",
        "pcx_max",
        "pcx_row",
        "datatype",
        "质押股份数量(股)",
        "占所持股份比例(%)",
        "占总股本比例(%)",
        "最新价(元)",
        "质押日收盘价(元)",
        "预估平仓线(元)",
        "sz",
        "yjx",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "公告日期",
            "股东名称",
            "质押开始日期",
            "质押机构",
            "质押股份数量(股)",
            "占所持股份比例(%)",
            "占总股本比例(%)",
            "最新价(元)",
            "质押日收盘价(元)",
            "预估平仓线(元)",
        ]
    ]
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"])
    temp_df["质押开始日期"] = pd.to_datetime(temp_df["质押开始日期"])
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
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
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
    for page in tqdm(range(1, page_num + 1)):
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
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
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
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
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
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
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
    data_json = demjson.decode(res.text[res.text.find("={") + 1:])
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
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        map_dict = dict(
            zip(
                pd.DataFrame(data_json["font"]["FontMapping"])["code"],
                pd.DataFrame(data_json["font"]["FontMapping"])["value"],
            )
        )
        for key, value in map_dict.items():
            data_text = data_text.replace(key, str(value))
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
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

    stock_em_gpzy_pledge_ratio_df = stock_em_gpzy_pledge_ratio(trade_date="2021-01-15")
    print(stock_em_gpzy_pledge_ratio_df)

    stock_em_gpzy_pledge_ratio_detail_df = stock_em_gpzy_pledge_ratio_detail()
    print(stock_em_gpzy_pledge_ratio_detail_df)

    stock_em_gpzy_distribute_statistics_company_df = stock_em_gpzy_distribute_statistics_company()
    print(stock_em_gpzy_distribute_statistics_company_df)

    stock_em_gpzy_distribute_statistics_bank_df = stock_em_gpzy_distribute_statistics_bank()
    print(stock_em_gpzy_distribute_statistics_bank_df)

    stock_em_gpzy_industry_data_df = stock_em_gpzy_industry_data()
    print(stock_em_gpzy_industry_data_df)
