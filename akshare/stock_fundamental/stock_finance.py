#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/1/6 15:35
Desc: 股票基本面数据
新浪财经-财务报表-财务摘要
https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/600004.phtml
新浪财经-财务分析-财务指标
https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/600004/displaytype/4.phtml
新浪财经-发行与分配
http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/600004.phtml
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from io import BytesIO


def stock_financial_report_sina(
    stock: str = "600004", symbol: str = "现金流量表"
) -> pd.DataFrame:
    """
    新浪财经-财务报表-三大报表
    https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600004/ctrl/part/displaytype/4.phtml
    :param stock: 股票代码
    :type stock: str
    :param symbol: choice of {"资产负债表", "利润表", "现金流量表"}
    :type symbol:
    :return: 新浪财经-财务报表-三大报表
    :rtype: pandas.DataFrame
    """
    if symbol == "资产负债表":
        url = f"http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{stock}/ctrl/all.phtml"  # 资产负债表
    elif symbol == "利润表":
        url = f"http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/{stock}/ctrl/all.phtml"  # 利润表
    elif symbol == "现金流量表":
        url = f"http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/{stock}/ctrl/all.phtml"  # 现金流量表
    r = requests.get(url)
    temp_df = pd.read_table(BytesIO(r.content), encoding="gb2312", header=None).iloc[
        :, :-2
    ]
    temp_df = temp_df.T
    temp_df.columns = temp_df.iloc[0, :]
    temp_df = temp_df.iloc[1:, :]
    temp_df.index.name = None
    temp_df.columns.name = None
    return temp_df


def stock_financial_abstract(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-财务报表-财务摘要
    https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-财务报表-财务摘要
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[13].iloc[:, :2]
    big_df = pd.DataFrame()
    for i in range(0, len(temp_df), 12):
        truncated_df = temp_df.iloc[i : i + 11, 1]
        big_df = pd.concat(
            [big_df, truncated_df.reset_index(drop=True)], axis=1, ignore_index=True
        )
    data_df = big_df.T
    data_df.columns = temp_df.iloc[:11, 0].tolist()
    return data_df


def stock_financial_analysis_indicator(symbol: str = "600004") -> pd.DataFrame:
    """
    新浪财经-财务分析-财务指标
    https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/600004/ctrl/2019/displaytype/4.phtml
    :param symbol: 股票代码
    :type symbol: str
    :return: 新浪财经-财务分析-财务指标
    :rtype: pandas.DataFrame
    """
    url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{symbol}/ctrl/2020/displaytype/4.phtml"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    year_context = soup.find(attrs={"id": "con02-1"}).find("table").find_all("a")
    year_list = [item.text for item in year_context]
    out_df = pd.DataFrame()
    for year_item in tqdm(year_list, leave=False):
        url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{symbol}/ctrl/{year_item}/displaytype/4.phtml"
        r = requests.get(url)
        temp_df = pd.read_html(r.text)[12].iloc[:, :-1]
        temp_df.columns = temp_df.iloc[0, :]
        temp_df = temp_df.iloc[1:, :]
        big_df = pd.DataFrame()
        indicator_list = ["每股指标", "盈利能力", "成长能力", "营运能力", "偿债及资本结构", "现金流量", "其他指标"]
        for i in range(len(indicator_list)):
            if i == 6:
                inner_df = temp_df[
                    temp_df.loc[
                        temp_df.iloc[:, 0].str.find(indicator_list[i]) == 0, :
                    ].index[0] :
                ].T
            else:
                inner_df = temp_df[
                    temp_df.loc[temp_df.iloc[:, 0].str.find(indicator_list[i]) == 0, :]
                    .index[0] : temp_df.loc[
                        temp_df.iloc[:, 0].str.find(indicator_list[i + 1]) == 0, :
                    ]
                    .index[0]
                    - 1
                ].T
            inner_df = inner_df.reset_index(drop=True)
            big_df = pd.concat([big_df, inner_df], axis=1)
        big_df.columns = big_df.iloc[0, :].tolist()
        big_df = big_df.iloc[1:, :]
        big_df.index = temp_df.columns.tolist()[1:]
        out_df = pd.concat([out_df, big_df])

    out_df.dropna(inplace=True)
    out_df.reset_index(inplace=True)
    out_df.rename(columns={'index': '日期'}, inplace=True)
    return out_df


def stock_history_dividend() -> pd.DataFrame:
    """
    新浪财经-发行与分配-历史分红
    http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml?p=1&num=5000
    :return: 所有股票的历史分红数据
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml"
    params = {"p": "1", "num": "5000"}
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    temp_df["代码"] = temp_df["代码"].astype(str).str.zfill(6)
    temp_df.columns = ["代码", "名称", "上市日期", "累计股息", "年均股息", "分红次数", "融资总额", "融资次数", "详细"]
    temp_df["上市日期"] = pd.to_datetime(temp_df["上市日期"]).dt.date
    temp_df["累计股息"] = pd.to_numeric(temp_df["累计股息"])
    temp_df["年均股息"] = pd.to_numeric(temp_df["年均股息"])
    temp_df["分红次数"] = pd.to_numeric(temp_df["分红次数"])
    temp_df["融资总额"] = pd.to_numeric(temp_df["融资总额"])
    temp_df["融资次数"] = pd.to_numeric(temp_df["融资次数"])
    del temp_df["详细"]
    return temp_df


def stock_history_dividend_detail(
    symbol: str = "000002", indicator: str = "分红", date: str = ""
) -> pd.DataFrame:
    """
    新浪财经-发行与分配-分红配股详情
    https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/300670.phtml
    :param indicator: choice of {"分红", "配股"}
    :type indicator: str
    :param symbol: 股票代码
    :type symbol: str
    :param date: 分红配股的具体日期, e.g., "1994-12-24"
    :type date: str
    :return: 指定 indicator, stock, date 的数据
    :rtype: pandas.DataFrame
    """
    if indicator == "分红":
        url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/{symbol}.phtml"
        r = requests.get(url)
        temp_df = pd.read_html(r.text)[12]
        temp_df.columns = [item[2] for item in temp_df.columns.tolist()]
        temp_df.columns = [
            "公告日期",
            "送股",
            "转增",
            "派息",
            "进度",
            "除权除息日",
            "股权登记日",
            "红股上市日",
            "查看详细",
        ]
        del temp_df["查看详细"]
        if temp_df.iloc[0, 0] == '暂时没有数据！':
            return pd.DataFrame()
        temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
        temp_df["送股"] = pd.to_numeric(temp_df["送股"])
        temp_df["转增"] = pd.to_numeric(temp_df["转增"])
        temp_df["派息"] = pd.to_numeric(temp_df["派息"])
        temp_df["除权除息日"] = pd.to_datetime(temp_df["除权除息日"], errors="coerce").dt.date
        temp_df["股权登记日"] = pd.to_datetime(temp_df["股权登记日"], errors="coerce").dt.date
        temp_df["红股上市日"] = pd.to_datetime(temp_df["红股上市日"], errors="coerce").dt.date
        if date:
            url = "https://vip.stock.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php"
            params = {
                "stockid": symbol,
                "type": "1",
                "end_date": date,
            }
            r = requests.get(url, params=params)
            temp_df = pd.read_html(r.text)[12]
            temp_df.columns = ["item", "value"]
            return temp_df
        else:
            return temp_df
    else:
        url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/{symbol}.phtml"
        r = requests.get(url)
        temp_df = pd.read_html(r.text)[13]
        temp_df.columns = [item[1] for item in temp_df.columns.tolist()]
        temp_df.columns = [
            "公告日期",
            "配股方案",
            "配股价格",
            "基准股本",
            "除权日",
            "股权登记日",
            "缴款起始日",
            "缴款终止日",
            "配股上市日",
            "募集资金合计",
            "查看详细",
        ]
        del temp_df["查看详细"]
        if temp_df.iloc[0, 0] == '暂时没有数据！':
            return pd.DataFrame()
        temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"]).dt.date
        temp_df["配股方案"] = pd.to_numeric(temp_df["配股方案"])
        temp_df["配股价格"] = pd.to_numeric(temp_df["配股价格"])
        temp_df["基准股本"] = pd.to_numeric(temp_df["基准股本"])
        temp_df["除权日"] = pd.to_datetime(temp_df["除权日"]).dt.date
        temp_df["股权登记日"] = pd.to_datetime(temp_df["股权登记日"]).dt.date
        temp_df["缴款起始日"] = pd.to_datetime(temp_df["缴款起始日"]).dt.date
        temp_df["缴款终止日"] = pd.to_datetime(temp_df["缴款终止日"]).dt.date
        temp_df["配股上市日"] = pd.to_datetime(temp_df["配股上市日"]).dt.date
        temp_df["募集资金合计"] = pd.to_numeric(temp_df["募集资金合计"])
        if date:
            url = "https://vip.stock.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php"
            params = {
                "stockid": symbol,
                "type": "1",
                "end_date": date,
            }
            r = requests.get(url, params=params)
            temp_df = pd.read_html(r.text)[12]
            temp_df.columns = ["item", "value"]
            return temp_df
        else:
            return temp_df


def stock_ipo_info(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-发行与分配-新股发行
    https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_NewStock/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 返回新股发行详情
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_NewStock/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[12]
    temp_df.columns = ["item", "value"]
    return temp_df


def stock_add_stock(stock: str = "688166") -> pd.DataFrame:
    """
    新浪财经-发行与分配-增发
    https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 返回增发详情
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[12]
    if temp_df.at[0, 0] == "对不起，暂时没有相关增发记录":
        return f"股票 {stock} 无增发记录"
    big_df = pd.DataFrame()
    for i in range(int(len(temp_df.at[0, 1]) / 10)):
        temp_df = pd.read_html(r.text)[13 + i].iloc[:, 1]
        big_df[temp_df.name.split(" ")[1].split("：")[1][:10]] = temp_df
    big_df = big_df.T
    big_df.columns = ["发行方式", "发行价格", "实际公司募集资金总额", "发行费用总额", "实际发行数量"]
    return big_df


def stock_restricted_release_queue_sina(symbol: str = "600000") -> pd.DataFrame:
    """
    新浪财经-发行分配-限售解禁
    https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml?symbol=sh600000
    :param symbol: 股票代码
    :type symbol: str
    :return: 返回限售解禁数据
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml?symbol={symbol}"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[0]
    temp_df.columns = ['代码', '名称', '解禁日期', '解禁数量', '解禁股流通市值', '上市批次', '公告日期']
    temp_df['解禁日期'] = pd.to_datetime(temp_df['解禁日期']).dt.date
    temp_df['公告日期'] = pd.to_datetime(temp_df['公告日期']).dt.date
    temp_df['解禁数量'] = pd.to_numeric(temp_df['解禁数量'], errors="coerce")
    temp_df['解禁股流通市值'] = pd.to_numeric(temp_df['解禁股流通市值'], errors="coerce")
    temp_df['上市批次'] = pd.to_numeric(temp_df['上市批次'], errors="coerce")
    temp_df['上市批次'] = pd.to_numeric(temp_df['上市批次'], errors="coerce")
    return temp_df


def stock_circulate_stock_holder(stock: str = "600000") -> pd.DataFrame:
    """
    新浪财经-股东股本-流通股东
    P.S. 特定股票特定时间只有前 5 个; e.g., 000002
    https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CirculateStockHolder/stockid/600000.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-股东股本-流通股东
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CirculateStockHolder/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[13].iloc[:, :5]
    temp_df.columns = [*range(5)]
    big_df = pd.DataFrame()
    need_range = temp_df[temp_df.iloc[:, 0].str.find("截止日期") == 0].index.tolist() + [
        len(temp_df)
    ]
    for i in range(len(need_range) - 1):
        truncated_df = temp_df.iloc[need_range[i] : need_range[i + 1], :]
        truncated_df = truncated_df.dropna(how="all")
        temp_truncated = truncated_df.iloc[2:, :]
        temp_truncated.reset_index(inplace=True, drop=True)
        concat_df = pd.concat(
            [temp_truncated, truncated_df.iloc[0, :], truncated_df.iloc[1, :]], axis=1
        )
        concat_df.columns = concat_df.iloc[0, :]
        concat_df = concat_df.iloc[1:, :]
        concat_df["截止日期"] = concat_df["截止日期"].fillna(method="ffill")
        concat_df["公告日期"] = concat_df["公告日期"].fillna(method="ffill")
        big_df = pd.concat([big_df, concat_df], axis=0, ignore_index=True)
    big_df = big_df[["截止日期", "公告日期", "编号", "股东名称", "持股数量(股)", "占流通股比例(%)", "股本性质"]]
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def stock_fund_stock_holder(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-股本股东-基金持股
    https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-股本股东-基金持股
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[13].iloc[:, :5]
    temp_df.columns = [*range(5)]
    big_df = pd.DataFrame()
    need_range = temp_df[temp_df.iloc[:, 0].str.find("截止日期") == 0].index.tolist() + [
        len(temp_df)
    ]
    for i in range(len(need_range) - 1):
        truncated_df = temp_df.iloc[need_range[i] : need_range[i + 1], :]
        truncated_df = truncated_df.dropna(how="all")
        temp_truncated = truncated_df.iloc[2:, :]
        temp_truncated.reset_index(inplace=True, drop=True)
        concat_df = pd.concat([temp_truncated, truncated_df.iloc[0, 1:]], axis=1)
        concat_df.columns = truncated_df.iloc[1, :].tolist() + ["截止日期"]
        concat_df["截止日期"] = concat_df["截止日期"].fillna(method="ffill")
        concat_df["截止日期"] = concat_df["截止日期"].fillna(method="bfill")
        big_df = pd.concat([big_df, concat_df], axis=0, ignore_index=True)
    big_df.dropna(inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def stock_main_stock_holder(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-股本股东-主要股东
    P.S. 特定股票特定时间只有前 5 个; e.g., 000002
    https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-股本股东-主要股东
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[13].iloc[:, :5]
    temp_df.columns = [*range(5)]
    big_df = pd.DataFrame()
    need_range = temp_df[temp_df.iloc[:, 0].str.find("截至日期") == 0].index.tolist() + [
        len(temp_df)
    ]
    for i in range(len(need_range) - 1):
        truncated_df = temp_df.iloc[need_range[i] : need_range[i + 1], :]
        truncated_df = truncated_df.dropna(how="all")
        temp_truncated = truncated_df.iloc[5:, :]
        temp_truncated.reset_index(inplace=True, drop=True)
        concat_df = pd.concat(
            [
                temp_truncated,
                truncated_df.iloc[0, :],
                truncated_df.iloc[1, :],
                truncated_df.iloc[2, :],
                truncated_df.iloc[3, :],
                truncated_df.iloc[4, :],
            ],
            axis=1,
        )
        concat_df.columns = concat_df.iloc[0, :]
        concat_df = concat_df.iloc[1:, :]
        concat_df["截至日期"] = concat_df["截至日期"].fillna(method="ffill")
        concat_df["公告日期"] = concat_df["公告日期"].fillna(method="ffill")
        concat_df["股东总数"] = concat_df["股东总数"].fillna(method="ffill")
        concat_df["平均持股数"] = concat_df["平均持股数"].fillna(method="ffill")
        concat_df["股东总数"] = concat_df["股东总数"].str.strip("查看变化趋势")
        concat_df["平均持股数"] = concat_df["平均持股数"].str.strip("(按总股本计算) 查看变化趋势")
        big_df = pd.concat([big_df, concat_df], axis=0, ignore_index=True)
    big_df.dropna(inplace=True, how="all")
    big_df.reset_index(inplace=True, drop=True)
    return big_df


if __name__ == "__main__":
    stock_financial_report_sina_df = stock_financial_report_sina(
        stock="600009", symbol="现金流量表"
    )
    print(stock_financial_report_sina_df)

    stock_financial_report_sina_df = stock_financial_report_sina(
        stock="600004", symbol="资产负债表"
    )
    print(stock_financial_report_sina_df)

    stock_financial_abstract_df = stock_financial_abstract(stock="000958")
    print(stock_financial_abstract_df)

    stock_financial_analysis_indicator_df = stock_financial_analysis_indicator(
        symbol="300168"
    )
    print(stock_financial_analysis_indicator_df)

    stock_history_dividend_df = stock_history_dividend()
    print(stock_history_dividend_df)

    stock_history_dividend_detail_df = stock_history_dividend_detail(
        symbol="600012", indicator="分红", date=""
    )
    print(stock_history_dividend_detail_df)

    stock_history_dividend_detail_df = stock_history_dividend_detail(
        symbol="600012", indicator="分红", date="2019-07-08"
    )
    print(stock_history_dividend_detail_df)

    stock_history_dividend_detail_df = stock_history_dividend_detail(
        symbol="000002", indicator="配股"
    )
    print(stock_history_dividend_detail_df)

    stock_history_dividend_detail_df = stock_history_dividend_detail(
        symbol="000002", indicator="配股", date="1999-12-22"
    )
    print(stock_history_dividend_detail_df)

    stock_ipo_info_df = stock_ipo_info(stock="600004")
    print(stock_ipo_info_df)

    stock_add_stock_df = stock_add_stock(stock="600004")
    print(stock_add_stock_df)

    stock_restricted_release_queue_sina_df = stock_restricted_release_queue_sina(symbol="600000")
    print(stock_restricted_release_queue_sina_df)

    stock_circulate_stock_holder_df = stock_circulate_stock_holder(stock="600000")
    print(stock_circulate_stock_holder_df)

    stock_fund_stock_holder_df = stock_fund_stock_holder(stock="601318")
    print(stock_fund_stock_holder_df)

    stock_main_stock_holder_df = stock_main_stock_holder(stock="600000")
    print(stock_main_stock_holder_df)
