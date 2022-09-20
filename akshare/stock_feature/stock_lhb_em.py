# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/3/15 17:32
Desc: 东方财富网-数据中心-龙虎榜单
https://data.eastmoney.com/stock/tradedetail.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_lhb_detail_em(
    start_date: str = "20220314", end_date: str = "20220315"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-龙虎榜详情
    https://data.eastmoney.com/stock/tradedetail.html
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 龙虎榜详情
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "SECURITY_CODE,TRADE_DATE",
        "sortTypes": "1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_DAILYBILLBOARD_DETAILS",
        "columns": "SECURITY_CODE,SECUCODE,SECURITY_NAME_ABBR,TRADE_DATE,EXPLAIN,CLOSE_PRICE,CHANGE_RATE,BILLBOARD_NET_AMT,BILLBOARD_BUY_AMT,BILLBOARD_SELL_AMT,BILLBOARD_DEAL_AMT,ACCUM_AMOUNT,DEAL_NET_RATIO,DEAL_AMOUNT_RATIO,TURNOVERRATE,FREE_MARKET_CAP,EXPLANATION,D1_CLOSE_ADJCHRATE,D2_CLOSE_ADJCHRATE,D5_CLOSE_ADJCHRATE,D10_CLOSE_ADJCHRATE",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(TRADE_DATE<='{end_date}')(TRADE_DATE>='{start_date}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "代码",
        "-",
        "名称",
        "-",
        "解读",
        "收盘价",
        "涨跌幅",
        "龙虎榜净买额",
        "龙虎榜买入额",
        "龙虎榜卖出额",
        "龙虎榜成交额",
        "市场总成交额",
        "净买额占总成交比",
        "成交额占总成交比",
        "换手率",
        "流通市值",
        "上榜原因",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "解读",
            "收盘价",
            "涨跌幅",
            "龙虎榜净买额",
            "龙虎榜买入额",
            "龙虎榜卖出额",
            "龙虎榜成交额",
            "市场总成交额",
            "净买额占总成交比",
            "成交额占总成交比",
            "换手率",
            "流通市值",
            "上榜原因",
        ]
    ]
    return temp_df


def stock_lhb_stock_statistic_em(symbol: str = "近一月") -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-个股上榜统计
    https://data.eastmoney.com/stock/tradedetail.html
    :param symbol: choice of {"近一月", "近三月", "近六月", "近一年"}
    :type symbol: str
    :return: 个股上榜统计
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "近一月": "01",
        "近三月": "02",
        "近六月": "03",
        "近一年": "04",
    }
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "BILLBOARD_TIMES,LATEST_TDATE,SECURITY_CODE",
        "sortTypes": "-1,-1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_BILLBOARD_TRADEALL",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f'(STATISTICS_CYCLE="{symbol_map[symbol]}")',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "-",
        "代码",
        "最近上榜日",
        "名称",
        "近1个月涨跌幅",
        "近3个月涨跌幅",
        "近6个月涨跌幅",
        "近1年涨跌幅",
        "涨跌幅",
        "收盘价",
        "-",
        "龙虎榜总成交额",
        "龙虎榜净买额",
        "-",
        "-",
        "机构买入净额",
        "上榜次数",
        "龙虎榜买入额",
        "龙虎榜卖出额",
        "机构买入总额",
        "机构卖出总额",
        "买方机构次数",
        "卖方机构次数",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最近上榜日",
            "收盘价",
            "涨跌幅",
            "上榜次数",
            "龙虎榜净买额",
            "龙虎榜买入额",
            "龙虎榜卖出额",
            "龙虎榜总成交额",
            "买方机构次数",
            "卖方机构次数",
            "机构买入净额",
            "机构买入总额",
            "机构卖出总额",
            "近1个月涨跌幅",
            "近3个月涨跌幅",
            "近6个月涨跌幅",
            "近1年涨跌幅",
        ]
    ]
    temp_df["最近上榜日"] = pd.to_datetime(temp_df["最近上榜日"]).dt.date
    return temp_df


def stock_lhb_jgmmtj_em(
    start_date: str = "20220906", end_date: str = "20220906"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-机构买卖每日统计
    https://data.eastmoney.com/stock/jgmmtj.html
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 机构买卖每日统计
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NET_BUY_AMT,TRADE_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1,1",
        "pageSize": "5000",
        "pageNumber": "1",
        "reportName": "RPT_ORGANIZATION_TRADE_DETAILS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(TRADE_DATE>='{start_date}')(TRADE_DATE<='{end_date}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "-",
        "名称",
        "代码",
        "上榜日期",
        "收盘价",
        "涨跌幅",
        "买方机构数",
        "卖方机构数",
        "机构买入总额",
        "机构卖出总额",
        "机构买入净额",
        "市场总成交额",
        "机构净买额占总成交额比",
        "换手率",
        "流通市值",
        "上榜原因",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "收盘价",
            "涨跌幅",
            "买方机构数",
            "卖方机构数",
            "机构买入总额",
            "机构卖出总额",
            "机构买入净额",
            "市场总成交额",
            "机构净买额占总成交额比",
            "换手率",
            "流通市值",
            "上榜原因",
            "上榜日期",
        ]
    ]
    temp_df["上榜日期"] = pd.to_datetime(temp_df["上榜日期"]).dt.date
    temp_df['收盘价'] = pd.to_numeric(temp_df['收盘价'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    temp_df['买方机构数'] = pd.to_numeric(temp_df['买方机构数'], errors="coerce")
    temp_df['卖方机构数'] = pd.to_numeric(temp_df['卖方机构数'], errors="coerce")
    temp_df['机构买入总额'] = pd.to_numeric(temp_df['机构买入总额'], errors="coerce")
    temp_df['机构卖出总额'] = pd.to_numeric(temp_df['机构卖出总额'], errors="coerce")
    temp_df['机构买入净额'] = pd.to_numeric(temp_df['机构买入净额'], errors="coerce")
    temp_df['市场总成交额'] = pd.to_numeric(temp_df['市场总成交额'], errors="coerce")
    temp_df['机构净买额占总成交额比'] = pd.to_numeric(temp_df['机构净买额占总成交额比'], errors="coerce")
    temp_df['换手率'] = pd.to_numeric(temp_df['换手率'], errors="coerce")
    temp_df['流通市值'] = pd.to_numeric(temp_df['流通市值'], errors="coerce")

    return temp_df


def stock_lhb_hyyyb_em(
    start_date: str = "20220324", end_date: str = "20220324"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-每日活跃营业部
    https://data.eastmoney.com/stock/jgmmtj.html
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日活跃营业部
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "TOTAL_NETAMT,ONLIST_DATE,OPERATEDEPT_CODE",
        "sortTypes": "-1,-1,1",
        "pageSize": "5000",
        "pageNumber": "1",
        "reportName": "RPT_OPERATEDEPT_ACTIVE",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(ONLIST_DATE>='{start_date}')(ONLIST_DATE<='{end_date}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]

    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "营业部名称",
        "上榜日",
        "买入个股数",
        "卖出个股数",
        "买入总金额",
        "卖出总金额",
        "总买卖净额",
        "-",
        "-",
        "买入股票",
        "-",
        "-",
    ]
    big_df = big_df[
        [
            "序号",
            "营业部名称",
            "上榜日",
            "买入个股数",
            "卖出个股数",
            "买入总金额",
            "卖出总金额",
            "总买卖净额",
            "买入股票",
        ]
    ]

    big_df["上榜日"] = pd.to_datetime(big_df["上榜日"]).dt.date
    big_df["买入个股数"] = pd.to_numeric(big_df["买入个股数"])
    big_df["卖出个股数"] = pd.to_numeric(big_df["卖出个股数"])
    big_df["买入总金额"] = pd.to_numeric(big_df["买入总金额"])
    big_df["卖出总金额"] = pd.to_numeric(big_df["卖出总金额"])
    big_df["总买卖净额"] = pd.to_numeric(big_df["总买卖净额"])

    return big_df


def stock_lhb_stock_detail_date_em(symbol: str = "600077") -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-个股龙虎榜详情-日期
    https://data.eastmoney.com/stock/tradedetail.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 个股龙虎榜详情-日期
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_LHB_BOARDDATE",
        "columns": "SECURITY_CODE,TRADE_DATE,TR_DATE",
        "filter": f'(SECURITY_CODE="{symbol}")',
        "pageNumber": "1",
        "pageSize": "1000",
        "sortTypes": "-1",
        "sortColumns": "TRADE_DATE",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "股票代码",
        "交易日",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "股票代码",
            "交易日",
        ]
    ]
    temp_df["交易日"] = pd.to_datetime(temp_df["交易日"]).dt.date
    return temp_df


def stock_lhb_stock_detail_em(
    symbol: str = "000788", date: str = "20220315", flag: str = "卖出"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
    https://data.eastmoney.com/stock/lhb/600077.html
    :param symbol: 股票代码
    :type symbol: str
    :param date: 查询日期; 需要通过 ak.stock_lhb_stock_detail_date_em(symbol="600077") 接口获取相应股票的有龙虎榜详情数据的日期
    :type date: str
    :param flag: choice of {"买入", "卖出"}
    :type flag: str
    :return: 个股龙虎榜详情
    :rtype: pandas.DataFrame
    """
    flag_map = {
        "买入": "BUY",
        "卖出": "SELL",
    }
    report_map = {
        "买入": "RPT_BILLBOARD_DAILYDETAILSBUY",
        "卖出": "RPT_BILLBOARD_DAILYDETAILSSELL",
    }
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": report_map[flag],
        "columns": "ALL",
        "filter": f"""(TRADE_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')(SECURITY_CODE="{symbol}")""",
        "pageNumber": "1",
        "pageSize": "500",
        "sortTypes": "-1",
        "sortColumns": flag_map[flag],
        "source": "WEB",
        "client": "WEB",
        "_": "1647338693644",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1

    if flag == "买入":
        temp_df.columns = [
            "序号",
            "-",
            "-",
            "-",
            "-",
            "交易营业部名称",
            "类型",
            "-",
            "-",
            "-",
            "-",
            "买入金额",
            "卖出金额",
            "净额",
            "-",
            "-",
            "-",
            "-",
            "买入金额-占总成交比例",
            "卖出金额-占总成交比例",
            "-",
        ]
        temp_df = temp_df[
            [
                "序号",
                "交易营业部名称",
                "买入金额",
                "买入金额-占总成交比例",
                "卖出金额",
                "卖出金额-占总成交比例",
                "净额",
                "类型",
            ]
        ]
        temp_df["买入金额"] = pd.to_numeric(temp_df["买入金额"])
        temp_df["买入金额-占总成交比例"] = pd.to_numeric(temp_df["买入金额-占总成交比例"])
        temp_df["卖出金额"] = pd.to_numeric(temp_df["卖出金额"])
        temp_df["卖出金额-占总成交比例"] = pd.to_numeric(temp_df["卖出金额-占总成交比例"])
        temp_df.sort_values("类型", inplace=True)
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["序号"] = range(1, len(temp_df["序号"]) + 1)
    else:
        temp_df.columns = [
            "序号",
            "-",
            "-",
            "-",
            "-",
            "交易营业部名称",
            "类型",
            "-",
            "-",
            "-",
            "-",
            "买入金额",
            "卖出金额",
            "净额",
            "-",
            "-",
            "-",
            "-",
            "买入金额-占总成交比例",
            "卖出金额-占总成交比例",
            "-",
        ]
        temp_df = temp_df[
            [
                "序号",
                "交易营业部名称",
                "买入金额",
                "买入金额-占总成交比例",
                "卖出金额",
                "卖出金额-占总成交比例",
                "净额",
                "类型",
            ]
        ]
        temp_df["买入金额"] = pd.to_numeric(temp_df["买入金额"])
        temp_df["买入金额-占总成交比例"] = pd.to_numeric(temp_df["买入金额-占总成交比例"])
        temp_df["卖出金额"] = pd.to_numeric(temp_df["卖出金额"])
        temp_df["卖出金额-占总成交比例"] = pd.to_numeric(temp_df["卖出金额-占总成交比例"])
        temp_df.sort_values("类型", inplace=True)
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["序号"] = range(1, len(temp_df["序号"]) + 1)
    return temp_df


if __name__ == "__main__":
    stock_lhb_detail_em_df = stock_lhb_detail_em(
        start_date="20220314", end_date="20220315"
    )
    print(stock_lhb_detail_em_df)

    stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近一月")
    print(stock_lhb_stock_statistic_em_df)

    stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近三月")
    print(stock_lhb_stock_statistic_em_df)

    stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近六月")
    print(stock_lhb_stock_statistic_em_df)

    stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近一年")
    print(stock_lhb_stock_statistic_em_df)

    stock_lhb_jgmmtj_em_df = stock_lhb_jgmmtj_em(
        start_date="20220904", end_date="20220906"
    )
    print(stock_lhb_jgmmtj_em_df)

    stock_lhb_hyyyb_em_df = stock_lhb_hyyyb_em(
        start_date="20220324", end_date="20220324"
    )
    print(stock_lhb_hyyyb_em_df)

    stock_lhb_stock_detail_date_em_df = stock_lhb_stock_detail_date_em(symbol="600077")
    print(stock_lhb_stock_detail_date_em_df)

    stock_lhb_stock_detail_em_df = stock_lhb_stock_detail_em(
        symbol="000788", date="20220315", flag="买入"
    )
    print(stock_lhb_stock_detail_em_df)

    stock_lhb_stock_detail_em_df = stock_lhb_stock_detail_em(
        symbol="600016", date="20220324", flag="买入"
    )
    print(stock_lhb_stock_detail_em_df)
