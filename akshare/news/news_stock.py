#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/11/20 120:15
Desc: 个股新闻数据
https://so.eastmoney.com/news/s?keyword=603777
"""

import json

import pandas as pd
import requests


def stock_news_em(symbol: str = "600325", page_size: int = 20) -> pd.DataFrame:
    """
    东方财富-个股新闻-获取个股新闻信息
    https://data.eastmoney.com/stockcomment/stock/{symbol}.html
    
    :param symbol: 股票代码，例如 "600325" (华发股份)
    :type symbol: str
    :param page_size: 每页返回的新闻数量，默认 20，最大 100
    :type page_size: int
    :return: 个股新闻数据，包含以下列：
        - 关键词: 股票代码
        - 新闻标题: 新闻标题
        - 新闻内容: 新闻摘要（从标题提取）
        - 发布时间: 新闻发布时间
        - 文章来源: 新闻来源
        - 新闻链接: 新闻详情链接
    :rtype: pandas.DataFrame
    :raises ValueError: 当股票代码格式不正确时
    :raises requests.RequestException: 当网络请求失败时
    """
    import time
    import uuid
    
    # 验证股票代码格式（6位数字）
    if not symbol or not symbol.isdigit() or len(symbol) != 6:
        raise ValueError(f"Invalid stock code: {symbol}. Stock code must be 6 digits.")
    
    # 验证页面大小
    if page_size < 1 or page_size > 100:
        raise ValueError(f"Invalid page_size: {page_size}. Must be between 1 and 100.")
    
    # 自动检测市场代码：1=上海证券交易所，0=深圳证券交易所
    # 上海股票代码范围：600000-609999, 688000-688999(科创板), 510000-519999(基金)
    # 深圳股票代码范围：000000-009999, 300000-309999(创业板), 159000-159999(基金)
    stock_code_int = int(symbol)
    if (600000 <= stock_code_int <= 609999 or 
        688000 <= stock_code_int <= 688999 or
        510000 <= stock_code_int <= 519999):
        market_code = 1  # 上海
    else:
        market_code = 0  # 深圳
    
    # 构造 API URL
    url = "https://np-listapi.eastmoney.com/comm/web/getListInfo"
    
    # 生成随机请求追踪ID（模拟真实请求）
    req_trace = uuid.uuid4().hex
    
    # 构造请求参数
    params = {
        "client": "web",
        "biz": "web_voice",
        "mTypeAndCode": f"{market_code}.{symbol}",
        "pageSize": str(page_size),
        "type": "1",
        "req_trace": req_trace
    }
    
    # 构造请求头（严格按照 curl 命令配置）
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Origin": "https://data.eastmoney.com",
        "Referer": f"https://data.eastmoney.com/stockcomment/stock/{symbol}.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    
    # 发送请求，带重试机制
    max_retries = 3
    retry_delay = 1  # 秒
    
    for attempt in range(max_retries):
        try:
            # 发送 GET 请求，设置超时时间为 10 秒
            response = requests.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=10
            )
            
            # 检查 HTTP 状态码
            response.raise_for_status()
            
            # 解析 JSON 响应
            data_json = response.json()
            
            # 检查 API 返回的状态码
            if data_json.get("code") != 1:
                error_msg = data_json.get("message", "Unknown error")
                raise ValueError(f"API returned error: {error_msg}")
            
            # 提取新闻列表数据
            news_list = data_json.get("data", {}).get("list", [])
            
            if not news_list:
                # 返回空 DataFrame，但保持列结构
                return pd.DataFrame(columns=[
                    "关键词", "新闻标题", "新闻内容", "发布时间", "文章来源", "新闻链接"
                ])
            
            # 转换为 DataFrame
            temp_df = pd.DataFrame(news_list)
            
            # 数据处理和字段映射
            # 提取文章来源（从标题中提取或设置默认值）
            temp_df["文章来源"] = "东方财富"
            
            # 新闻内容设置为空字符串（API 不提供摘要）
            temp_df["新闻内容"] = ""
            
            # 添加关键词列
            temp_df["关键词"] = symbol
            
            # 重命名列
            temp_df.rename(
                columns={
                    "Art_ShowTime": "发布时间",
                    "Art_Title": "新闻标题",
                    "Art_Url": "新闻链接"
                },
                inplace=True
            )
            
            # 选择并排序输出列
            result_df = temp_df[
                [
                    "关键词",
                    "新闻标题",
                    "新闻内容",
                    "发布时间",
                    "文章来源",
                    "新闻链接"
                ]
            ]
            
            # 重置索引
            result_df.reset_index(drop=True, inplace=True)
            
            return result_df
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                raise requests.RequestException(
                    f"Request timeout after {max_retries} attempts. "
                    f"Please check your network connection."
                )
        
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1 and e.response.status_code >= 500:
                # 服务器错误，重试
                time.sleep(retry_delay)
                continue
            else:
                raise requests.RequestException(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.reason}"
                )
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                raise requests.RequestException(
                    f"Network error occurred: {str(e)}"
                )
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(
                f"Failed to parse API response: {str(e)}"
            )


if __name__ == "__main__":
    # 测试华发股份（600325）
    stock_news_em_df = stock_news_em(symbol="600325", page_size=20)
    print(stock_news_em_df)
    print(f"\n数据形状: {stock_news_em_df.shape}")
    print(f"列名: {stock_news_em_df.columns.tolist()}")
    
    # 打印新闻链接的完整 URL
    print(f"\n新闻链接 (前5条):")
    print("=" * 80)
    for idx, url in enumerate(stock_news_em_df["新闻链接"].head(5), 1):
        print(f"{idx}. {url}")
