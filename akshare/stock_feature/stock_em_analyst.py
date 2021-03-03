# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/11/15 13:39
Desc: 东方财富网-数据中心-研究报告-东方财富分析师指数
http://data.eastmoney.com/invest/invest/list.html
"""
import pandas as pd
import requests


def stock_em_analyst_rank(year: str = '2021') -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行
    http://data.eastmoney.com/invest/invest/list.html
    :param year: 从 2015 年至今
    :type year: str
    :return: 东方财富分析师指数2020最新排行
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://data.eastmoney.com/dataapi/invest/data"
    params = {
        "st": "0" if year == "2021" else year,
        "sr": "1",
        "p": "1",
        "ps": "5000",
        "name": "",
        "type": "list",
        "industrycode": "all",
        "pageNo": "1",
        "pageNum": "1",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    data_df = pd.DataFrame(data_json['data'])
    del data_df['_id']
    data_df.reset_index(inplace=True)
    data_df['index'] = list(range(1, len(data_df)+1))
    data_df.columns = [
            "序号",
            "_",
            f"{year}年收益率",
            "_",
            "分析师名称",
            "分析师单位",
            "年度指数",
            "3个月收益率",
            "6个月收益率",
            "12个月收益率",
            f"{year}最新个股评级",
            "_",
            "_",
            "分析师ID",
            "_",
            "成分股个数",
            "_",
        ]
    data_df = data_df[[
        "序号",
        "分析师名称",
        "分析师单位",
        "年度指数",
        f"{year}年收益率",
        "3个月收益率",
        "6个月收益率",
        "12个月收益率",
        "成分股个数",
        f"{year}最新个股评级",
        '分析师ID',
    ]]
    return data_df


def stock_em_analyst_detail(
    analyst_id: str = "11000200926", indicator: str = "最新跟踪成分股"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行-分析师详情
    http://data.eastmoney.com/invest/invest/11000200926.html
    :param analyst_id: 分析师ID, 从 stock_em_analyst_rank 获取
    :type analyst_id: str
    :param indicator: ["最新跟踪成分股", "历史跟踪成分股", "历史指数"]
    :type indicator: str
    :return: 具体指标的数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://data.eastmoney.com/dataapi/invest/other"
    if indicator == "最新跟踪成分股":
        params = {
            'href': '/api/Zgfxzs/json/AnalysisIndexNew.aspx',
            'paramsstr': f'index=1&size=100&code={analyst_id}',
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        temp_df = pd.DataFrame(json_data['re'])
        temp_df.reset_index(inplace=True)
        temp_df['index'] = list(range(1, len(temp_df)+1))
        temp_df.columns = [
            '序号',
            '股票代码',
            '股票名称',
            '调入日期',
            '当前评级名称',
            '成交价格(前复权)',
            '最新价格',
            '最新评级日期',
            "_",
            '阶段涨跌幅',
        ]
        temp_df = temp_df[[
            '序号',
            '股票代码',
            '股票名称',
            '调入日期',
            '最新评级日期',
            '当前评级名称',
            '成交价格(前复权)',
            '最新价格',
            '阶段涨跌幅',
        ]]
        return temp_df
    elif indicator == "历史跟踪成分股":
        params = {
            'href': '/api/Zgfxzs/json/AnalysisIndexls.aspx',
            'paramsstr': f'index=1&size=100&code={analyst_id}',
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        temp_df = pd.DataFrame(json_data['re'])
        temp_df.reset_index(inplace=True)
        temp_df['index'] = list(range(1, len(temp_df) + 1))
        temp_df.columns = [
            '序号',
            '股票代码',
            '股票名称',
            '调入日期',
            '调出日期',
            '调入时评级名称',
            '调出原因',
            '_',
            '累计涨跌幅',
        ]
        temp_df = temp_df[[
            '序号',
            '股票代码',
            '股票名称',
            '调入日期',
            '调出日期',
            '调入时评级名称',
            '调出原因',
            '累计涨跌幅',
        ]]
        return temp_df
    elif indicator == "历史指数":
        params = {
            'href': '/DataCenter_V3/chart/AnalystsIndex.ashx',
            'paramsstr': f'code={analyst_id}&d=&isxml=True',
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        temp_df = pd.DataFrame(
            [json_data["X"].split(","), json_data["Y"][0].split(",")],
            index=["date", "value"],
        ).T
        return temp_df


if __name__ == "__main__":
    stock_em_analyst_rank_df = stock_em_analyst_rank(year='2021')
    print(stock_em_analyst_rank_df)
    stock_em_analyst_detail_current_stock_df = stock_em_analyst_detail(
        analyst_id="11000200926", indicator="最新跟踪成分股"
    )
    print(stock_em_analyst_detail_current_stock_df)
    stock_em_analyst_detail_history_stock_df = stock_em_analyst_detail(
        analyst_id="11000200926", indicator="历史跟踪成分股"
    )
    print(stock_em_analyst_detail_history_stock_df)
    stock_em_analyst_detail_index_df = stock_em_analyst_detail(
        analyst_id="11000200926", indicator="历史指数"
    )
    print(stock_em_analyst_detail_index_df)
