#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/3/10 16:59
Desc: This is a tool for downloading github user email address.
query url: https://api.github.com/graphql
reference url: https://thedatapack.com/tools/find-github-user-email/
"""
from collections import Counter

import jsonpath
import requests


def tool_github_star_list(owner="jindaxiang", name="akshare"):
    url = "https://api.github.com/graphql"
    query1 = """
    query GetStars($name: String!, $owner: String!) {
      repository(name: $name, owner: $owner) {
        createdAt
        stargazers(first: 100){
          edges {
            node {
              id
              login
              name
              avatarUrl
              __typename
            }
            starredAt
            __typename
          }
          pageInfo {
            startCursor
            endCursor
            hasNextPage
            __typename
          }
          totalCount
          __typename
        }
        __typename
      }
    }
    """
    query2 = """
    query GetStars($name: String!, $owner: String!, $after: String) {
      repository(name: $name, owner: $owner) {
        createdAt
        stargazers(first: 100, after: $after){
          edges {
            node {
              id
              login
              name
              avatarUrl
              __typename
            }
            starredAt
            __typename
          }
          pageInfo {
            startCursor
            endCursor
            hasNextPage
            __typename
          }
          totalCount
          __typename
        }
        __typename
      }
    }
    """
    headers = {
        "Authorization": "Bearer a4d404b52802435f25903641b58aef482f2d3565",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }

    variables = {"owner": owner, "name": name}
    payload = {
        "operationName": "GetStars",
        "variables": variables,
        "query": query1
    }
    r = requests.post(url, json=payload, headers=headers)
    data_json = r.json()
    big_list = []
    name_list = jsonpath.jsonpath(data_json, '$..login')
    next_flag = jsonpath.jsonpath(data_json, '$..endCursor')
    has_next = jsonpath.jsonpath(data_json, '$..hasNextPage')[0]
    big_list.extend(name_list)
    while has_next:
        print(next_flag[0])
        variables.update({"after": next_flag[0]})
        payload.update({"query": query2})
        r = requests.post(url, json=payload, headers=headers)
        data_json = r.json()
        name_list = jsonpath.jsonpath(data_json, '$..login')
        next_flag = jsonpath.jsonpath(data_json, '$..endCursor')
        has_next = jsonpath.jsonpath(data_json, '$..hasNextPage')[0]
        big_list.extend(name_list)
    return big_list


def tool_github_email_address(username="lateautumn4lin"):
    params = {
        "per_page": "100"
    }
    r = requests.get(f"https://api.github.com/users/{username}/events", params=params)
    if r.status_code in (403, 443):
        return None
    if jsonpath.jsonpath(r.json(), '$..email'):
        res = jsonpath.jsonpath(r.json(), '$..email')
        word_counts = Counter(res)
        top_three = word_counts.most_common(1)
        if len(top_three) > 0:
            print(top_three[0][0])
            return top_three[0][0]
    return None


if __name__ == '__main__':
    temp_list = tool_github_star_list(owner="PiotrDabkowski", name="Js2Py")
    print(temp_list)
    tool_github_email_address_df = tool_github_email_address(username="lateautumn4lin")
    print(tool_github_email_address_df)
