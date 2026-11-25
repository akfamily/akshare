#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
date: 2026/11/25 20:02
desc: 东方财富网-数据中心-特色数据-机构调研
http://data.eastmoney.com/jgdy/
东方财富网-数据中心-特色数据-机构调研-机构调研统计：http://data.eastmoney.com/jgdy/tj.html
东方财富网-数据中心-特色数据-机构调研-机构调研详细：http://data.eastmoney.com/jgdy/xx.html
"""

import datetime

import pandas as pd
from tqdm import tqdm

from akshare.exceptions import APIError, InvalidParameterError
from akshare.utils import http

# datacenter-web 的业务状态码：查询条件下没有数据、服务器繁忙
_CODE_EMPTY = 9201
_CODE_BUSY = 9701
# 机构调研详细每页最多 50 条；一次查询超过这个页数就改为按调研日期逐天查询。
# 2026-11-25 实测：一次查询翻到约第 50 页以后上游时常返回“服务器繁忙”（68 页里
# 每次有 9～13 页被拒），按日期分段后 70 页全部成功
_SURVEY_MAX_PAGES = 40


def _today() -> datetime.date:
    """
    当前日期，单独成函数以便测试时替换
    :return: 当前日期
    :rtype: datetime.date
    """
    return datetime.date.today()


def _require_survey_result(data_json: dict, date: str) -> None:
    """
    机构调研报表没有返回数据时，区分“没有数据”与“服务器繁忙”给出明确的报错
    :param data_json: 上游返回的 JSON
    :type data_json: dict
    :param date: 查询的开始时间
    :type date: str
    """
    if data_json.get("result"):
        return
    code = data_json.get("code")
    message = data_json.get("message")
    if code == _CODE_EMPTY:
        # 2026-11-25 实测：只有 date 之后确实没有记录（如 date 是今天或未来）时
        # 上游才返回这个代码；date 很早时上游照常返回它保留的全部数据
        raise InvalidParameterError(
            f"东方财富没有 {date} 之后的机构调研数据（上游提示：{message}），"
            "请改用更早的日期"
        )
    if code == _CODE_BUSY:
        # 2026-11-25 实测：机构调研详细翻到约第 50 页以后，上游时常返回“服务器繁忙”，
        # 放慢请求或隔几秒重试同一页都不能避免；每页条数大于 50 时则每次都返回它
        raise APIError(
            f"东方财富数据中心没有返回 {date} 以来的机构调研数据（上游提示：{message}）。"
            "数据量较大、需要翻很多页时上游时常拒绝靠后的页，请改用更近的日期缩小范围，"
            "或稍后重试"
        )
    raise APIError(f"东方财富没有返回机构调研数据（上游提示：{message}，代码：{code}）")


def stock_jgdy_tj_em(date: str = "20261101") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研统计
    https://data.eastmoney.com/jgdy/tj.html
    :param date: 开始时间
    :type date: str
    :return: 机构调研统计
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE,SUM,RECEIVE_START_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1,-1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_ORG_SURVEYNEW",
        "columns": "ALL",
        "quoteColumns": "f2~01~SECURITY_CODE~CLOSE_PRICE,f3~01~SECURITY_CODE~CHANGE_RATE",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(NUMBERNEW="1")(IS_SOURCE="1")(NOTICE_DATE>'{"-".join([date[:4], date[4:6], date[6:]])}')""",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    _require_survey_result(data_json, date)
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = http.get(url, params=params)
        data_json = r.json()
        _require_survey_result(data_json, date)
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df])
    big_df = big_df.reset_index()
    big_df["index"] = list(range(1, len(big_df) + 1))
    big_df.columns = [
        "序号",
        "_",
        "代码",
        "名称",
        "_",
        "公告日期",
        "接待日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "接待地点",
        "_",
        "接待方式",
        "_",
        "接待人员",
        "_",
        "_",
        "_",
        "_",
        "_",
        "接待机构数量",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "最新价",
        "涨跌幅",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "接待机构数量",
            "接待方式",
            "接待人员",
            "接待地点",
            "接待日期",
            "公告日期",
        ]
    ]
    big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["接待机构数量"] = pd.to_numeric(big_df["接待机构数量"], errors="coerce")
    big_df["接待日期"] = pd.to_datetime(big_df["接待日期"], errors="coerce").dt.date
    big_df["公告日期"] = pd.to_datetime(big_df["公告日期"], errors="coerce").dt.date
    return big_df


def stock_jgdy_detail_em(date: str = "20261118") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研详细
    https://data.eastmoney.com/jgdy/xx.html
    :param date: 开始时间
    :type date: str
    :return: 机构调研详细
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE,RECEIVE_START_DATE,SECURITY_CODE,NUMBERNEW",
        "sortTypes": "-1,-1,1,-1",
        "pageSize": "50",
        "pageNumber": "1",
        "reportName": "RPT_ORG_SURVEY",
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,NOTICE_DATE,RECEIVE_START_DATE,"
        "RECEIVE_OBJECT,RECEIVE_PLACE,RECEIVE_WAY_EXPLAIN,INVESTIGATORS,RECEPTIONIST,ORG_TYPE",
        "quoteColumns": "f2~01~SECURITY_CODE~CLOSE_PRICE,f3~01~SECURITY_CODE~CHANGE_RATE",
        "quoteType": "0",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(IS_SOURCE="1")(RECEIVE_START_DATE>'{"-".join([date[:4], date[4:6], date[6:]])}')""",
    }
    start = datetime.datetime.strptime(date, "%Y%m%d").date()

    def fetch(first_json: dict, bar) -> list:
        """取完一次查询的所有页；first_json 是已经取到的第 1 页"""
        frames = [pd.DataFrame(first_json["result"]["data"])]
        bar.update()
        for page in range(2, first_json["result"]["pages"] + 1):
            params.update({"pageNumber": page})
            data_json = http.get(url, params=params).json()
            _require_survey_result(data_json, date)
            frames.append(pd.DataFrame(data_json["result"]["data"]))
            bar.update()
        return frames

    data_json = http.get(url, params=params).json()
    _require_survey_result(data_json, date)
    total_page = data_json["result"]["pages"]
    with tqdm(total=total_page, leave=False) as bar:
        if total_page <= _SURVEY_MAX_PAGES:
            frames = fetch(data_json, bar)
        else:
            # 页数太多时逐天查询，从最近的一天往前；最后一段不设上界，
            # 以免漏掉调研日期晚于今天的记录
            end = max(_today(), start)
            windows = [f"(RECEIVE_START_DATE>'{end.isoformat()}')"]
            for offset in range((end - start).days):
                day = end - datetime.timedelta(days=offset)
                previous = day - datetime.timedelta(days=1)
                windows.append(
                    f"(RECEIVE_START_DATE>'{previous.isoformat()}')"
                    f"(RECEIVE_START_DATE<='{day.isoformat()}')"
                )
            frames = []
            for window in windows:
                params.update({"filter": f'(IS_SOURCE="1"){window}', "pageNumber": 1})
                data_json = http.get(url, params=params).json()
                if data_json.get("code") == _CODE_EMPTY:
                    continue  # 这一天没有调研记录
                _require_survey_result(data_json, date)
                frames.extend(fetch(data_json, bar))
            if not frames:
                raise APIError(
                    f"东方财富按天查询 {date} 以来的机构调研数据时没有返回任何记录，请稍后重试"
                )
    big_df = pd.concat(frames, ignore_index=True)
    # 与上游一次查询的顺序保持一致：公告日期、调研日期从新到旧，再按代码
    big_df = big_df.sort_values(
        by=["NOTICE_DATE", "RECEIVE_START_DATE", "SECURITY_CODE"],
        ascending=[False, False, True],
        kind="stable",
    )
    big_df = big_df.reset_index(drop=True).reset_index()
    big_df["index"] = list(range(1, len(big_df) + 1))
    big_df.columns = [
        "序号",
        "_",
        "代码",
        "名称",
        "公告日期",
        "调研日期",
        "调研机构",
        "接待地点",
        "接待方式",
        "调研人员",
        "接待人员",
        "机构类型",
        "最新价",
        "涨跌幅",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "调研机构",
            "机构类型",
            "调研人员",
            "接待方式",
            "接待人员",
            "接待地点",
            "调研日期",
            "公告日期",
        ]
    ]
    big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["调研日期"] = pd.to_datetime(big_df["调研日期"], errors="coerce").dt.date
    big_df["公告日期"] = pd.to_datetime(big_df["公告日期"], errors="coerce").dt.date
    return big_df


if __name__ == "__main__":
    stock_jgdy_tj_em_df = stock_jgdy_tj_em(date="20261101")
    print(stock_jgdy_tj_em_df)

    stock_jgdy_detail_em_df = stock_jgdy_detail_em(date="20261118")
    print(stock_jgdy_detail_em_df)
