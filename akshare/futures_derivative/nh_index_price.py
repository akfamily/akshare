# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2019/11/26 18:52
Desc: 获取南华期货-商品指数历史走势-价格指数-数值-http://www.nanhua.net/nhzc/varietytrend.html
1000 点开始, 用收益率累计
目标地址: http://www.nanhua.net/ianalysis/varietyindex/price/A.json?t=1574932974280
"""
import time

import requests
import pandas as pd


def num_to_str_data(str_date: str) -> str:
    """
    transfer date format
    :param str_date:
    :type str_date: str
    :return: data format
    :rtype: str
    """
    str_date = str_date / 1000
    str_date = time.localtime(str_date)  # 生成一个元组的时间
    strp_time = time.strftime("%Y-%m-%d %H:%M:%S", str_date)  # 格式化元组
    return strp_time


def get_nh_list_table() -> pd.DataFrame:
    """
    获取南华期货-南华指数所有品种一览表
    :return: pandas.DataFrame
    | id | code  | exchange             | firstday   | category | name           |
    |----|-------|----------------------|------------|----------|----------------|
    | 7  | A     | 大连商品交易所       | 1994/9/19  | 品种     | 大豆           |
    | 8  | AL    | 上海期货交易所       | 1994/10/12 | 品种     | 铝             |
    | 9  | CU    | 上海期货交易所       | 1996/4/5   | 品种     | 铜             |
    | 10 | RU    | 上海期货交易所       | 1997/4/17  | 品种     | 橡胶           |
    | 11 | M     | 大连商品交易所       | 2000/7/19  | 品种     | 豆粕           |
    | 12 | CF    | 郑州商品交易所       | 2004/6/2   | 品种     | 棉花           |
    | 13 | FU    | 上海期货交易所       | 2004/8/26  | 品种     | 燃油           |
    | 14 | C     | 大连商品交易所       | 2004/9/23  | 品种     | 玉米           |
    | 15 | SR    | 郑州商品交易所       | 2006/1/9   | 品种     | 白糖           |
    | 16 | Y     | 大连商品交易所       | 2006/1/10  | 品种     | 豆油           |
    | 17 | TA    | 郑州商品交易所       | 2006/12/19 | 品种     | PTA            |
    | 18 | ZN    | 上海期货交易所       | 2007/3/26  | 品种     | 锌             |
    | 19 | L     | 大连商品交易所       | 2007/7/31  | 品种     | 塑料           |
    | 20 | P     | 大连商品交易所       | 2007/10/29 | 品种     | 棕榈油         |
    | 21 | AU    | 上海期货交易所       | 2008/1/9   | 品种     | 黄金           |
    | 22 | RB    | 上海期货交易所       | 2009/3/27  | 品种     | 螺纹钢         |
    | 23 | WR    | 上海期货交易所       | 2009/3/27  | 品种     | 线材           |
    | 24 | V     | 大连商品交易所       | 2009/5/25  | 品种     | PVC            |
    | 25 | IF    | 中国金融期货交易所   | 2010/4/16  | 品种     | 股指           |
    | 26 | PB    | 上海期货交易所       | 2011/3/24  | 品种     | 铅             |
    | 27 | J     | 大连商品交易所       | 2011/4/15  | 品种     | 焦炭           |
    | 28 | PM    | 郑州商品交易所       | 2012/1/17  | 品种     | 普麦           |
    | 29 | AG    | 上海期货交易所       | 2012/5/10  | 品种     | 白银           |
    | 30 | OI    | 郑州商品交易所       | 2012/7/16  | 品种     | 菜籽油         |
    | 31 | RI    | 郑州商品交易所       | 2012/7/24  | 品种     | 早籼稻         |
    | 32 | WH    | 郑州商品交易所       | 2012/7/24  | 品种     | 强麦           |
    | 33 | FG    | 郑州商品交易所       | 2012/12/3  | 品种     | 玻璃           |
    | 34 | RS    | 郑州商品交易所       | 2012/12/28 | 品种     | 油菜籽         |
    | 35 | RM    | 郑州商品交易所       | 2012/12/28 | 品种     | 菜籽粕         |
    | 36 | JM    | 大连商品交易所       | 2013/3/22  | 品种     | 焦煤           |
    | 37 | TF    | 中国金融期货交易所   | 2013/9/6   | 品种     | 五年国债       |
    | 38 | BU    | 上海期货交易所       | 2013/10/9  | 品种     | 沥青           |
    | 39 | I     | 大连商品交易所       | 2013/10/18 | 品种     | 铁矿石         |
    | 40 | JD    | 大连商品交易所       | 2013/11/8  | 品种     | 鸡蛋           |
    | 41 | JR    | 郑州商品交易所       | 2013/11/18 | 品种     | 粳稻           |
    | 42 | BB    | 大连商品交易所       | 2013/12/6  | 品种     | 胶合板         |
    | 43 | FB    | 大连商品交易所       | 2013/12/6  | 品种     | 纤维板         |
    | 44 | PP    | 大连商品交易所       | 2014/2/28  | 品种     | 聚丙烯         |
    | 45 | HC    | 上海期货交易所       | 2014/3/21  | 品种     | 热轧卷板       |
    | 46 | LR    | 郑州商品交易所       | 2014/7/8   | 品种     | 晚籼稻         |
    | 47 | SF    | 郑州商品交易所       | 2014/8/8   | 品种     | 硅铁           |
    | 48 | SM    | 郑州商品交易所       | 2014/8/8   | 品种     | 锰硅           |
    | 49 | CS    | 大连商品交易所       | 2014/12/19 | 品种     | 玉米淀粉       |
    | 50 | T     | 中国金融期货交易所   | 2015/3/20  | 品种     | 十年国债       |
    | 51 | NI    | 上海期货交易所       | 2015/3/27  | 品种     | 沪镍           |
    | 52 | SN    | 上海期货交易所       | 2015/3/27  | 品种     | 沪锡           |
    | 53 | MA    | 郑州商品交易所       | 2015/4/10  | 品种     | 甲醇           |
    | 54 | IH    | 中国金融期货交易所   | 2015/4/16  | 品种     | 上证50         |
    | 55 | IC    | 中国金融期货交易所   | 2015/4/16  | 品种     | 中证500        |
    | 56 | ZC    | 郑州商品交易所       | 2015/5/18  | 品种     | 动力煤         |
    | 57 | SC    | 上海国际能源交易中心 | 2017/3/23  | 品种     | 原油           |
    | 58 | CY    | 郑州商品交易所       | 2017/8/18  | 品种     | 棉纱           |
    """
    url_name = "http://www.nanhua.net/ianalysis/plate-variety.json"
    res = requests.get(url_name)
    futures_name = [item["name"] for item in res.json()]
    futures_code = [item["code"] for item in res.json()]
    futures_exchange = [item["exchange"] for item in res.json()]
    futures_first_day = [item["firstday"] for item in res.json()]
    futures_index_cat = [item["indexcategory"] for item in res.json()]
    futures_df = pd.DataFrame(
        [
            futures_code,
            futures_exchange,
            futures_first_day,
            futures_index_cat,
            futures_name,
        ]
    ).T
    futures_df.columns = ["code", "exchange", "start_date", "category", "name"]
    futures_df = futures_df[futures_df["category"] == "品种"]
    return futures_df


def nh_price_index(code: str = "A") -> pd.DataFrame:
    """
    获取南华期货-南华指数单品种所有历史数据
    :param code: str 通过 get_nh_list 提供
    :return: pandas.Series
                      value
    date
    2006-01-10     1000
    2006-01-11   998.82
    2006-01-12     1000
    2006-01-13   990.17
    2006-01-16   994.49
                 ...
    2019-11-20  796.433
    2019-11-21  794.932
    2019-11-22  792.682
    2019-11-25  793.331
    2019-11-26  779.346
    """
    if code in get_nh_list_table()["code"].tolist():
        t = time.time()
        base_url = f"http://www.nanhua.net/ianalysis/varietyindex/price/{code}.json?t={int(round(t * 1000))}"
        res = requests.get(base_url)
        date = [num_to_str_data(item[0]).split(" ")[0] for item in res.json()]
        data = [item[1] for item in res.json()]
        df_all = pd.DataFrame([date, data]).T
        df_all.columns = ["date", "value"]
        df_all.index = pd.to_datetime(df_all["date"])
        del df_all["date"]
        return df_all


if __name__ == "__main__":
    nh_price_index_df = nh_price_index(code="A")
    print(nh_price_index_df)
