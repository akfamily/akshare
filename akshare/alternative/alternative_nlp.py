#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/27
Desc: 思知-智能问答
https://ownthink.com/robot.html
"""

import pandas as pd

from akshare.utils import http


def alternative_nlp_answer(question: str = "人工智能") -> pd.DataFrame:
    """
    思知-智能问答
    https://ownthink.com/robot.html
    :param question: 问题
    :type question: str
    :return: 问题与回答
    :rtype: pandas.DataFrame
    """
    url = "https://api.ownthink.com/bot"
    params = {"spoken": question}
    r = http.get(url, params=params)
    json_data = r.json()
    answer = json_data["data"]["info"]["text"]
    return pd.DataFrame({"问题": [question], "回答": [answer]})


if __name__ == "__main__":
    alternative_nlp_answer_df = alternative_nlp_answer(question="姚明的身高")
    print(alternative_nlp_answer_df)
