#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/11/27 14:02
Desc: ownthink-knowledge graph
https://ownthink.com/
https://www.ownthink.com/docs/kg/
"""
import pandas as pd
import requests
from akshare.request_config_manager import get_headers_and_timeout


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
    headers, timeout = get_headers_and_timeout(locals().get('headers', {}), locals().get('timeout', None))
    r = requests.post(url, data=payload, headers=headers, timeout=timeout)
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


def nlp_answer(question: str = "人工智能") -> str:
    """
    智能问答
    https://ownthink.com/robot.html
    :param question: word in chinese
    :type question: str
    :return: indicator data
    :rtype: list or dict or pandas.DataFrame
    """
    url = 'https://api.ownthink.com/bot'
    params = {
        'spoken': question
    }
    headers, timeout = get_headers_and_timeout(locals().get('headers', {}), locals().get('timeout', None))
    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    json_data = r.json()
    answer = json_data['data']['info']['text']
    return answer


if __name__ == "__main__":
    nlp_ownthink_df = nlp_ownthink(word="人工智能", indicator="tag")
    print(nlp_ownthink_df)

    nlp_answer_df = nlp_answer(question="姚明的身高")
    print(nlp_answer_df)
