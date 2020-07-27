# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/3/1 0:02
Desc: ownthink-knowledge graph
https://ownthink.com/
https://www.ownthink.com/docs/kg/
"""
import pandas as pd
import requests


def nlp_ownthink(word: str = "人工智能", indicator: str = "entity") -> pd.DataFrame:
    """
    Knowledge Graph interface for financial research
    https://ownthink.com/
    :param word: word in chinese
    :type word: str
    :param indicator: entity or desc or avp or tag
    :type indicator: str
    :return: indicator data
    :rtype: list or dict or pandas.DataFrame
    """
    url = "https://api.ownthink.com/kg/knowledge"
    payload = {
        "entity": word,
    }
    r = requests.post(url, data=payload)
    if not r.json()["data"]:
        print("Can not find the resource, please type into the correct word")
        return None
    if indicator == "entity":
        return r.json()["data"]["entity"]
    if indicator == "desc":
        return r.json()["data"]["desc"]
    if indicator == "avp":
        return pd.DataFrame(r.json()["data"]["avp"], columns=["字段", "值"])
    if indicator == "tag":
        return r.json()["data"]["tag"]


if __name__ == "__main__":
    nlp_ownthink_df = nlp_ownthink(word="人工智能", indicator="tag")
    print(nlp_ownthink_df)
