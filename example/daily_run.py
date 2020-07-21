# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/4 9:07
Desc: test
"""

import datetime
import json
import warnings
from time import sleep

import akshare

calendar = akshare.cons.get_calendar()

setting_file_name = "setting.json"
setting_file_path = akshare.cons.get_json_path(setting_file_name, __file__)
s = json.load(open(setting_file_path, "r"))


def down_load(date):
    date = akshare.cons.convert_date(date) if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn("%s非交易日" % date.strftime("%Y%m%d"))
        return
    # ----------------------------------------------------------------------
    print("\n" + "-" * 80 + "\n展期")
    df = akshare.get_roll_yield_bar(type_method="var", date=date)
    df.to_csv(s["root"] + "展期%s.csv" % date)

    # ----------------------------------------------------------------------
    print("\n" + "-" * 80 + "\n基差")
    df = akshare.futures_spot_price(date)
    df.to_csv(s["root"] + "基差%s.csv" % date)

    # ----------------------------------------------------------------------
    print("\n" + "-" * 80 + "\n会员持仓排名之和")
    df = akshare.get_rank_sum_daily(start_day=date, end_day=date)
    df.to_csv(s["root"] + "会员持仓排名%s.csv" % date)

    # ----------------------------------------------------------------------
    print("\n" + "-" * 80 + "\n仓单")
    df = akshare.get_receipt(date)
    df.to_csv(s["root"] + "仓单%s.csv" % date)

    # ----------------------------------------------------------------------
    if s["qqEmail"] != "*":
        akshare.send_email("akshare", s["qqEmail"], s["secret"], s["qqEmail"], "smtp.qq.com", "465", ["展期%s.csv" % date, "基差%s.csv" % date, "会员持仓排名%s.csv" % date, "仓单%s.csv" % date], s["root"], True)


def monitor(catch_time="17:00"):
    while True:
        now = datetime.datetime.now()
        if now.strftime("%H:%M") == catch_time:
            down_load(now.strftime("%Y%m%d"))
        sleep(40)


if __name__ == "__main__":
    monitor()
