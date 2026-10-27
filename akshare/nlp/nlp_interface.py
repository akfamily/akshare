#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/27
Desc: 思知-智能问答
https://ownthink.com/robot.html
"""

import requests


def nlp_answer(question: str = "人工智能") -> str:
    """
    思知-智能问答
    https://ownthink.com/robot.html
    :param question: 问题
    :type question: str
    :return: 回答
    :rtype: str
    """
    url = "https://api.ownthink.com/bot"
    params = {"spoken": question}
    r = requests.get(url, params=params)
    json_data = r.json()
    answer = json_data["data"]["info"]["text"]
    return answer


if __name__ == "__main__":
    nlp_answer_df = nlp_answer(question="姚明的身高")
    print(nlp_answer_df)
