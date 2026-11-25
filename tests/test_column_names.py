"""几个接口的列名瑕疵：尾随空格、重复连字符、没有列名的原始表格、多出的行号列。"""

import json
from types import SimpleNamespace

import pandas as pd

from akshare.futures import futures_foreign
from akshare.option import option_czce

# 2026-11-25 抓到的 RMOPTIONS2025.txt 开头几行：表头与单元格都用空格补齐到固定宽度
CZCE_TEXT = (
    "\t\t\t\t\t郑州商品交易所期权历史行情下载(2025RM)\n"
    "交易日期  |合约代码   |昨结算    |今开盘    |最高价    |最低价    |今收盘    "
    "|今结算    |涨跌1     |涨跌2     |成交量(手)|持仓量    |增减量    |成交额(万元)"
    "|DELTA     |隐含波动率|行权量\n"
    "2025-01-02|RM503C1925|301.50    |0.00      |0.00      |0.00      |0.00      "
    "|318.00    |16.50     |16.50     |0         |2         |0         |0.00        "
    "|0.9814    |22.64     |0                              \n"
    "2025-01-02|RM503C2150|110.00    |121.00    |134.00    |111.50    |111.50    "
    "|121.00    |1.50      |11.00     |152       |1,155     |-62       |18.33       "
    "|0.7236    |22.32     |0                              \n"
)


def test_option_hist_yearly_czce_strips_padding(monkeypatch):
    monkeypatch.setattr(
        option_czce.http, "get", lambda url, **kwargs: SimpleNamespace(text=CZCE_TEXT)
    )
    df = option_czce.option_hist_yearly_czce(symbol="RM", year="2025")
    assert list(df.columns) == [
        "交易日期",
        "合约代码",
        "昨结算",
        "今开盘",
        "最高价",
        "最低价",
        "今收盘",
        "今结算",
        "涨跌1",
        "涨跌2",
        "成交量(手)",
        "持仓量",
        "增减量",
        "成交额(万元)",
        "DELTA",
        "隐含波动率",
        "行权量",
    ]
    assert df["合约代码"].tolist() == ["RM503C1925", "RM503C2150"]
    # 带千分位的数量列仍是文本，但不再带补齐用的空格
    assert df["持仓量"].tolist() == ["2", "1,155"]


def _table(rows):
    cells = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return f"<table>{cells}</table>"


# 新浪外盘期货详情页的第 7 张表：每行三组“项目-内容”，没有表头，空内容是空单元格
FOREIGN_HTML = (
    "<html><body>"
    + _table([["x"]]) * 6
    + _table(
        [
            ["交易品种", "伦敦锌", "交易单位", "每手25吨", "报价单位", "美元/吨"],
            ["交易代码", "ZSD", "上市交易所", "伦敦金属交易所", "附加信息", ""],
        ]
    )
    + "</body></html>"
)


def test_futures_foreign_detail_sina_returns_item_value(monkeypatch):
    monkeypatch.setattr(
        futures_foreign.http,
        "get",
        lambda url, **kwargs: SimpleNamespace(text=FOREIGN_HTML, encoding="utf-8"),
    )
    df = futures_foreign.futures_foreign_detail_sina(symbol="ZSD")
    assert list(df.columns) == ["item", "value"]
    assert df["item"].tolist() == [
        "交易品种",
        "交易单位",
        "报价单位",
        "交易代码",
        "上市交易所",
        "附加信息",
    ]
    assert df["value"].tolist()[:5] == [
        "伦敦锌",
        "每手25吨",
        "美元/吨",
        "ZSD",
        "伦敦金属交易所",
    ]
    assert pd.isna(df["value"].iloc[5])


def test_futures_daily_shfe_has_no_leaked_index_column(monkeypatch):
    # 其余交易所的 futures_daily_* 都是 symbol 开头的 12 列；上期所这个函数过滤掉
    # efp 行以后 reset_index() 没有 drop，多带出一列不连续的原始行号
    from akshare.futures import cons, futures_daily_bar

    def row(month, product="cu_f", group="cu"):
        return {
            "PRODUCTID": product,
            "PRODUCTGROUPID": group,
            "DELIVERYMONTH": month,
            "OPENPRICE": 1,
            "HIGHESTPRICE": 2,
            "LOWESTPRICE": 1,
            "CLOSEPRICE": 2,
            "SETTLEMENTPRICE": 2,
            "PRESETTLEMENTPRICE": 1,
            "VOLUME": 10,
            "TURNOVER": 5,
            "OPENINTEREST": 7,
        }

    payload = {"o_curinstrument": [row("efp"), row("2612"), row("小计"), row("2701")]}

    class Response:
        text = json.dumps(payload, ensure_ascii=False)

        def raise_for_status(self):
            return None

    monkeypatch.setattr(futures_daily_bar, "calendar", ["20261113"])
    monkeypatch.setattr(
        futures_daily_bar, "requests_link", lambda url, **kwargs: Response()
    )
    df = futures_daily_bar.futures_daily_shfe(date="20261113")
    assert list(df.columns) == cons.OUTPUT_COLUMNS
    assert df["symbol"].tolist() == ["CU2612", "CU2701"]
    assert df.index.tolist() == [0, 1]


def test_futures_index_ccidx_selects_named_columns(monkeypatch):
    # 上游在原有字段之外又加了十多个字段，过去会原样带出英文字段名
    from akshare.futures import futures_index_ccidx as module

    record = {
        "tradeDate": "2026-11-24",
        "indexId": "100001.CCI",
        "closingPrice": 1500.5,
        "settlePrice": 1499.0,
        "dailyIncreaseAndDecrease": 3.2,
        "dailyIncreaseAndDecreasePercentage": 0.21,
        "openingPrice": 1498.0,
        "highPrice": 1503.0,
        "preSettlePrice": 1496.0,
        "oneYearAnnualizedReturnPercentage": 5.1,
    }
    payload = {"data": {"dateLineJson": [record, dict(record, tradeDate="2026-11-23")]}}
    monkeypatch.setattr(
        module.http, "get", lambda url, **kwargs: SimpleNamespace(json=lambda: payload)
    )
    df = module.futures_index_ccidx(symbol="中证商品期货指数")
    assert list(df.columns) == [
        "日期",
        "指数代码",
        "收盘点位",
        "结算点位",
        "涨跌",
        "涨跌幅",
    ]
    assert [str(x) for x in df["日期"]] == ["2026-11-23", "2026-11-24"]


def test_stock_register_db_returns_financial_columns(monkeypatch):
    # 2026-11-25 抓到的 RPT_KCB_IPO（三板达标企业）字段，节选
    from akshare.stock.issue import stock_register_em as module

    row = {
        "ORG_NAME": "自贡东新电碳股份有限公司",
        "SECURITY_CODE": "875295",
        "SECURITY_NAME_ABBR": "自贡东碳",
        "BUSINESS_SCOPE": "石墨及碳素制品制造",
        "YEAR_1Y": "2025",
        "OPERATE_INCOME_1Y": 112131990.87,
        "NETPROFIT_1Y": 24353700,
        "ACCUM_NETPROFIT_2Y": 25395500,
        "ACCUM_OPERATEINCOME_3Y": 203909089.11,
        "ACCUM_RESEARCH_3Y": None,
        "RESEARCH_RATIO_3Y": None,
        "ACCUM_CASHFLOW_3Y": -65335329.91,
        "ZSZ": 1063651008,
        "ORG_TYPE": "三板达标企业",
        "LISTED": "0",
    }
    payload = {"result": {"pages": 1, "data": [row, dict(row, ORG_NAME="乙公司")]}}
    monkeypatch.setattr(
        module.http, "get", lambda url, **kwargs: SimpleNamespace(json=lambda: payload)
    )
    df = module.stock_register_db()
    assert list(df.columns) == [
        "序号",
        "企业名称",
        "证券代码",
        "证券简称",
        "经营范围",
        "最近年度",
        "最近一年营业收入",
        "最近一年净利润",
        "最近两年累计净利润",
        "最近三年累计营业收入",
        "最近三年累计研发投入",
        "最近三年研发投入占比",
        "最近三年累计经营现金流",
        "总市值",
    ]
    assert df["序号"].tolist() == [1, 2]
    assert df["证券代码"].tolist() == ["875295", "875295"]
    assert df["最近一年营业收入"].iloc[0] == 112131990.87
    assert pd.isna(df["最近三年累计研发投入"].iloc[0])
