# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/17 12:33
Desc: 河北省空气质量预报信息发布系统
http://110.249.223.67/publish/
每日 17 时发布
等级划分
1. 空气污染指数为0－50，空气质量级别为一级，空气质量状况属于优。此时，空气质量令人满意，基本无空气污染，各类人群可正常活动。
2. 空气污染指数为51－100，空气质量级别为二级，空气质量状况属于良。此时空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响，建议极少数异常敏感人群应减少户外活动。
3. 空气污染指数为101－150，空气质量级别为三级，空气质量状况属于轻度污染。此时，易感人群症状有轻度加剧，健康人群出现刺激症状。建议儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼。
4. 空气污染指数为151－200，空气质量级别为四级，空气质量状况属于中度污染。此时，进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响，建议疾病患者避免长时间、高强度的户外锻练，一般人群适量减少户外运动。
5. 空气污染指数为201－300，空气质量级别为五级，空气质量状况属于重度污染。此时，心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状，建议儿童、老年人和心脏病、肺病患者应停留在室内，停止户外运动，一般人群减少户外运动。
6. 空气污染指数大于300，空气质量级别为六级，空气质量状况属于严重污染。此时，健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病，建议儿童、老年人和病人应当留在室内，避免体力消耗，一般人群应避免户外活动。
发布单位：河北省环境应急与重污染天气预警中心 技术支持：中国科学院大气物理研究所 中科三清科技有限公司
"""
from datetime import datetime

import pandas as pd
from tqdm import tqdm
import requests


def air_quality_hebei(city: str = "唐山市") -> pd.DataFrame:
    """
    河北省空气质量预报信息发布系统-空气质量预报, 未来 6 天
    http://110.249.223.67/publish/
    :param city: ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市', '辛集市', '定州市']
    :type city: str
    :return: city = "", 返回所有地区的数据; city="唐山市", 返回唐山市的数据
    :rtype: pandas.DataFrame
    """
    url = "http://110.249.223.67/publishNewServer/api/CityPublishInfo/GetProvinceAndCityPublishData"
    params = {"publishDate": f"{datetime.today().strftime('%Y-%m-%d')} 16:00:00"}
    r = requests.get(url, params=params)
    json_data = r.json()
    city_list = pd.DataFrame.from_dict(json_data["cityPublishDatas"], orient="columns")[
        "CityName"
    ].tolist()
    outer_df = pd.DataFrame()
    for i in tqdm(range(1, 7)):
        inner_df = pd.DataFrame(
            [item[f"Date{i}"] for item in json_data["cityPublishDatas"]],
            index=city_list,
        )
        outer_df = outer_df.append(inner_df)
    if city == "":
        return outer_df
    else:
        return outer_df[outer_df.index == city]


if __name__ == "__main__":
    air_quality_hebei_df = air_quality_hebei(city="石家庄市")
    print(air_quality_hebei_df)
