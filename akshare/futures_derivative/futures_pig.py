# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/8/13 17:03
Desc: 养猪数据中心
https://zhujia.zhuwang.cc/
"""
import requests
import pandas as pd


def futures_pig_info(symbol: str = "猪肉批发价") -> pd.DataFrame:
    """
    养猪数据中心
    https://zhujia.zhuwang.cc/
    :param symbol: choice of {"猪肉批发价", "仔猪价格", "生猪期货指数", "二元母猪价格", "生猪产能数据", "饲料原料数据", "中央储备冻猪肉", "白条肉", "育肥猪配合饲料", "肉类价格指数", "猪粮比价", "猪企销售简报-销售量", "猪企销售简报-销售额", "猪企销售简报-销售均价"}
    :type symbol: str
    :return: 猪肉信息
    :rtype: pandas.DataFrame
    """
    if symbol == "猪肉批发价":
        url = "https://zhujia.zhuwang.cc/new_map/zhujiapork/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "item", "value"]
        del temp_df["item"]
        return temp_df
    elif symbol == "仔猪价格":
        url = "https://zt.zhuwang.cc/new_map/zhizhu/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "生猪期货指数":
        url = "https://zhujia.zhuwang.cc/new_map/shengzhuqihuo/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        need_list = temp_df.iloc[-1, [1, 3, 5, 7, 9, 11]].tolist()
        temp_df.columns = list("abcdefghijklm")
        temp_df = temp_df.drop(["b", "d", "f", "h", "j", "l"], axis="columns")
        temp_df.columns = ["日期"] + need_list
        return temp_df
    elif symbol == "二元母猪价格":
        url = "https://zt.zhuwang.cc/new_map/eryuanpig/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "生猪产能数据":
        url = "https://zt.zhuwang.cc/new_map/shengzhuchanneng/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["周期", "能繁母猪存栏", "猪肉产量", "生猪存栏", "生猪出栏"]
        temp_df["能繁母猪存栏"] = pd.to_numeric(temp_df["能繁母猪存栏"], errors="coerce")
        temp_df["猪肉产量"] = pd.to_numeric(temp_df["猪肉产量"], errors="coerce")
        temp_df["生猪存栏"] = pd.to_numeric(temp_df["生猪存栏"], errors="coerce")
        temp_df["生猪出栏"] = pd.to_numeric(temp_df["生猪出栏"], errors="coerce")
        return temp_df
    elif symbol == "饲料原料数据":
        url = "https://zt.zhuwang.cc/new_map/pigfeed/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["周期", "大豆进口金额", "大豆播种面积", "玉米进口金额", "玉米播种面积"]
        temp_df["周期"] = temp_df["周期"].astype(int).astype(str)
        temp_df["大豆进口金额"] = pd.to_numeric(temp_df["大豆进口金额"], errors="coerce")
        temp_df["大豆播种面积"] = pd.to_numeric(temp_df["大豆播种面积"], errors="coerce")
        temp_df["玉米进口金额"] = pd.to_numeric(temp_df["玉米进口金额"], errors="coerce")
        temp_df["玉米播种面积"] = pd.to_numeric(temp_df["玉米播种面积"], errors="coerce")
        return temp_df
    elif symbol == "中央储备冻猪肉":
        url = "https://zt.zhuwang.cc/new_map/chubeidongzhurou/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "白条肉":
        url = "https://zt.zhuwang.cc/new_map/baitiaozhurou/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["周期", "白条肉平均出厂价格", "环比", "同比"]
        temp_df["白条肉平均出厂价格"] = pd.to_numeric(temp_df["白条肉平均出厂价格"])
        temp_df["环比"] = pd.to_numeric(temp_df["环比"])
        temp_df["同比"] = pd.to_numeric(temp_df["同比"])
        return temp_df
    elif symbol == "育肥猪配合饲料":
        url = "https://zhujia.zhuwang.cc/new_map/yufeipig/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["周期", "发布日期", "_", "本周", "去年同期", "上一周", "_", "_", "_"]
        temp_df = temp_df[["发布日期", "周期", "本周", "去年同期", "上一周"]]
        temp_df["去年同期"] = pd.to_numeric(temp_df["去年同期"])
        temp_df["上一周"] = pd.to_numeric(temp_df["上一周"])
        return temp_df
    elif symbol == "肉类价格指数":
        url = "https://zhujia.zhuwang.cc/new_map/meatindex/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "_", "value"]
        temp_df = temp_df[["date", "value"]]
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "猪粮比价":
        url = "https://zt.zhuwang.cc/new_map/zhuliangbi/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "猪企销售简报-销售量":
        url = "https://zt.zhuwang.cc/new_map/zhuqixiaoshoujianbao/xiaoliang.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["周期", "温氏", "正邦", "新希望", "牧原"]
        temp_df["温氏"] = pd.to_numeric(temp_df["温氏"])
        temp_df["正邦"] = pd.to_numeric(temp_df["正邦"])
        temp_df["新希望"] = pd.to_numeric(temp_df["新希望"])
        temp_df["牧原"] = pd.to_numeric(temp_df["牧原"])
        return temp_df
    elif symbol == "猪企销售简报-销售额":
        url = "https://zt.zhuwang.cc/new_map/zhuqixiaoshoujianbao/xiaoshoue.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["周期", "温氏", "正邦", "新希望", "牧原"]
        temp_df["温氏"] = pd.to_numeric(temp_df["温氏"])
        temp_df["正邦"] = pd.to_numeric(temp_df["正邦"])
        temp_df["新希望"] = pd.to_numeric(temp_df["新希望"])
        temp_df["牧原"] = pd.to_numeric(temp_df["牧原"])
        return temp_df
    elif symbol == "猪企销售简报-销售均价":
        url = "https://zt.zhuwang.cc/new_map/zhuqixiaoshoujianbao/junjia.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["周期", "温氏", "正邦", "新希望", "牧原"]
        temp_df["温氏"] = pd.to_numeric(temp_df["温氏"])
        temp_df["正邦"] = pd.to_numeric(temp_df["正邦"])
        temp_df["新希望"] = pd.to_numeric(temp_df["新希望"])
        temp_df["牧原"] = pd.to_numeric(temp_df["牧原"])
        return temp_df


def futures_pig_rank(symbol: str = "外三元") -> pd.DataFrame:
    """
    价格排行榜
    https://zhujia.zhuwang.cc/lists.shtml
    :param symbol: choice of {"外三元", "内三元", "土杂猪", "玉米", "豆粕"}
    :type symbol: str
    :return: 价格排行榜
    :rtype: pandas.DataFrame
    """
    if symbol == "外三元":
        temp_df = pd.read_html("https://zhujia.zhuwang.cc/lists.shtml")[0]
        temp_df.columns = [
            '排名',
            '品种',
            '省份',
            '价格-公斤',
            '价格-斤',
        ]
        temp_df['价格-公斤'] = temp_df['价格-公斤'].str.strip("元")
        temp_df['价格-斤'] = temp_df['价格-斤'].str.strip("元")
        temp_df['价格-公斤'] = pd.to_numeric(temp_df['价格-公斤'])
        temp_df['价格-斤'] = pd.to_numeric(temp_df['价格-斤'])
        return temp_df
    elif symbol == "内三元":
        temp_df = pd.read_html("https://zhujia.zhuwang.cc/lists-1.shtml")[0]
        temp_df.columns = [
            '排名',
            '品种',
            '省份',
            '价格-公斤',
            '价格-斤',
        ]
        temp_df['价格-公斤'] = temp_df['价格-公斤'].str.strip("元")
        temp_df['价格-斤'] = temp_df['价格-斤'].str.strip("元")
        temp_df['价格-公斤'] = pd.to_numeric(temp_df['价格-公斤'])
        temp_df['价格-斤'] = pd.to_numeric(temp_df['价格-斤'])
        return temp_df
    elif symbol == "土杂猪":
        temp_df = pd.read_html("https://zhujia.zhuwang.cc/lists-2.shtml")[0]
        temp_df.columns = [
            '排名',
            '品种',
            '省份',
            '价格-公斤',
            '价格-斤',
        ]
        temp_df['价格-公斤'] = temp_df['价格-公斤'].str.strip("元")
        temp_df['价格-斤'] = temp_df['价格-斤'].str.strip("元")
        temp_df['价格-公斤'] = pd.to_numeric(temp_df['价格-公斤'])
        temp_df['价格-斤'] = pd.to_numeric(temp_df['价格-斤'])
        return temp_df
    elif symbol == "玉米":
        temp_df = pd.read_html("https://zhujia.zhuwang.cc/lists-3.shtml")[0]
        temp_df.columns = [
            '排名',
            '品种',
            '省份',
            '价格-公斤',
            '价格-斤',
        ]
        temp_df['价格-公斤'] = temp_df['价格-公斤'].str.strip("元")
        temp_df['价格-斤'] = temp_df['价格-斤'].str.strip("元")
        temp_df['价格-公斤'] = pd.to_numeric(temp_df['价格-公斤'])
        temp_df['价格-斤'] = pd.to_numeric(temp_df['价格-斤'])
        return temp_df
    elif symbol == "豆粕":
        temp_df = pd.read_html("https://zhujia.zhuwang.cc/lists-4.shtml")[0]
        temp_df.columns = [
            '排名',
            '品种',
            '省份',
            '价格-公斤',
            '价格-斤',
        ]
        temp_df['价格-公斤'] = temp_df['价格-公斤'].str.strip("元")
        temp_df['价格-斤'] = temp_df['价格-斤'].str.strip("元")
        temp_df['价格-公斤'] = pd.to_numeric(temp_df['价格-公斤'])
        temp_df['价格-斤'] = pd.to_numeric(temp_df['价格-斤'])
        return temp_df


if __name__ == "__main__":
    futures_pig_info_df = futures_pig_info(symbol="猪肉批发价")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="仔猪价格")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="生猪期货指数")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="二元母猪价格")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="生猪产能数据")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="饲料原料数据")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="中央储备冻猪肉")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="白条肉")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="育肥猪配合饲料")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="肉类价格指数")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="猪粮比价")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="猪企销售简报-销售量")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="猪企销售简报-销售额")
    print(futures_pig_info_df)

    futures_pig_info_df = futures_pig_info(symbol="猪企销售简报-销售均价")
    print(futures_pig_info_df)

    futures_pig_rank_df = futures_pig_rank(symbol="外三元")
    print(futures_pig_rank_df)

    futures_pig_rank_df = futures_pig_rank(symbol="内三元")
    print(futures_pig_rank_df)

    futures_pig_rank_df = futures_pig_rank(symbol="土杂猪")
    print(futures_pig_rank_df)

    futures_pig_rank_df = futures_pig_rank(symbol="玉米")
    print(futures_pig_rank_df)

    futures_pig_rank_df = futures_pig_rank(symbol="豆粕")
    print(futures_pig_rank_df)
