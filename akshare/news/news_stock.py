#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/11/20 120:15
Desc: 个股新闻数据
https://so.eastmoney.com/news/s?keyword=603777
"""

import json
import re
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_news_content(url: str, size: Optional[int] = 250) -> str:
    """
    获取新闻内容，精准提取新闻主体内容
    
    :param url: 新闻链接
    :type url: str
    :param size: 截取长度，None表示不截取
    :type size: Optional[int]
    :return: 新闻内容（纯文本）
    :rtype: str
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 优先查找东方财富网特有的文章主体内容区域
        content = _extract_eastmoney_content(soup)
        if content.strip():
            return _process_content(content, size)
        
        # 如果上面的方法没有提取到内容，尝试其他方法
        # 查找文章主体注释标记
        article_comments = soup.find_all(string=re.compile(r'文章主体'))
        if article_comments:
            # 获取注释后的内容
            content = _extract_content_after_comment(article_comments[0])
            if content.strip():
                return _process_content(content, size)
        
        # 使用CSS选择器查找内容
        content = _extract_content_by_selectors(soup)
        return _process_content(content, size)
        
    except requests.RequestException as e:
        return f"网络请求错误: {str(e)}"
    except Exception as e:
        return f"内容提取错误: {str(e)}"


def _extract_eastmoney_content(soup: BeautifulSoup) -> str:
    """
    提取东方财富网特有格式的文章内容
    
    :param soup: BeautifulSoup对象
    :return: 提取的内容
    """
    # 查找文章主体注释
    article_comments = soup.find_all(string=lambda text: isinstance(text, str) and '文章主体' in text)
    if not article_comments:
        return ""
    
    # 获取第一个注释
    comment = article_comments[0]
    
    # 收集注释后的内容元素
    content_elements = []
    
    # 从注释的下一个兄弟节点开始遍历
    current = comment.next_sibling
    while current:
        # 遇到文章结尾区域时停止
        if hasattr(current, 'name') and current.name == 'div':
            # 检查是否有特定的类名标识文章结尾
            classes = current.get('class', [])
            if any(end_cls in classes for end_cls in ['zwothers', 'pinglunbox', 'sharebox', 'zwctrls']):
                break
        
        # 添加到内容元素列表
        content_elements.append(current)
        current = current.next_sibling
    
    # 提取文本内容
    texts = []
    for element in content_elements:
        if isinstance(element, str):
            text = element.strip()
            # 过滤掉注释和样式标签
            if (text and 
                not text.startswith('<!--') and 
                not text.startswith('<style') and 
                not text.startswith('<script') and
                'EM_StockImg_' not in text and
                'autoimg' not in text and
                '{' not in text):
                # 清理文本
                cleaned_text = re.sub(r'\s+', ' ', text).strip()
                if cleaned_text:
                    texts.append(cleaned_text)
        elif hasattr(element, 'get_text'):
            # 获取文本内容
            text = element.get_text(strip=False)
            if text and not text.isspace():
                # 清理文本
                cleaned_text = re.sub(r'\s+', ' ', text).strip()
                # 过滤掉免责声明和版权信息
                if (cleaned_text and 
                    '免责声明' not in cleaned_text and 
                    '版权所有' not in cleaned_text and
                    '沪ICP证' not in cleaned_text and
                    'EM_StockImg_' not in cleaned_text and
                    'autoimg' not in cleaned_text):
                    texts.append(cleaned_text)
    
    # 合并段落，保留段落间的换行
    content = '\n\n'.join(texts)
    
    # 进一步清理内容，移除HTML标签残留和CSS样式
    content = _clean_content(content)
    
    return content


def _extract_content_after_comment(comment) -> str:
    """
    提取注释后的内容
    
    :param comment: BeautifulSoup中的注释节点
    :return: 提取的文本内容
    """
    texts = []
    # 获取注释后的所有兄弟节点
    next_node = comment.next_sibling
    
    while next_node:
        # 遇到明显的结束标记时停止
        if hasattr(next_node, 'name'):
            # 遇到文章结尾区域时停止
            if next_node.name == 'div' and next_node.get('class'):
                classes = ' '.join(next_node.get('class', []))
                if any(cls in classes for cls in ['zwothers', 'pinglunbox', 'sharebox', 'zwctrls']):
                    break
        
        # 提取文本
        if isinstance(next_node, str):
            text = next_node.strip()
            if (text and 
                not text.startswith('<!--') and 
                not text.startswith('<style') and 
                not text.startswith('<script') and
                'EM_StockImg_' not in text and
                'autoimg' not in text and
                '{' not in text):
                # 清理文本
                cleaned_text = re.sub(r'\s+', ' ', text).strip()
                if cleaned_text:
                    texts.append(cleaned_text)
        elif hasattr(next_node, 'get_text'):
            text = next_node.get_text(strip=False)
            if text and not text.isspace():
                # 清理文本
                cleaned_text = re.sub(r'\s+', ' ', text).strip()
                # 过滤掉免责声明和版权信息
                if (cleaned_text and 
                    '免责声明' not in cleaned_text and 
                    '版权所有' not in cleaned_text and
                    '沪ICP证' not in cleaned_text and
                    'EM_StockImg_' not in cleaned_text and
                    'autoimg' not in cleaned_text):
                    texts.append(cleaned_text)
        
        next_node = next_node.next_sibling
    
    # 合并段落，保留段落间的换行
    content = '\n\n'.join(texts)
    
    # 进一步清理内容，移除HTML标签残留和CSS样式
    content = _clean_content(content)
    
    return content


def _extract_content_by_selectors(soup: BeautifulSoup) -> str:
    """
    使用CSS选择器提取内容的辅助函数
    
    :param soup: BeautifulSoup对象
    :return: 提取的内容
    """
    # 移除script和style标签及其内容
    for script in soup(["script", "style", "noscript", "iframe", "nav", "header", "footer", "aside"]):
        script.decompose()
    
    # 尝试定位新闻主体内容的常见标签和类名
    content_selectors = [
        '#ContentBody',
        '[class*="content"]',
        '[class*="article"]',
        '[class*="news"]',
        '[id*="content"]',
        '[id*="article"]',
        '[id*="news"]',
        '.post-content',
        '.article-content',
        '.entry-content',
        '.story-body',
        '.news-content',
        'article',
        '.main-content',
        '.post-body',
        '.article-body'
    ]
    
    content_element = None
    for selector in content_selectors:
        content_element = soup.select_one(selector)
        if content_element:
            break
    
    # 如果没找到特定内容区域，则尝试移除常见的无关元素后使用body
    if not content_element:
        # 移除常见的无关元素
        for element in soup(['nav', 'header', 'footer', 'aside', 'advertisement', 'ad', 
                           '[class*="ad"]', '[id*="ad"]', '[class*="nav"]', '[id*="nav"]',
                           '[class*="menu"]', '[id*="menu"]', '[class*="sidebar"]', 
                           '[id*="sidebar"]', '[class*="comment"]', '[id*="comment"]']):
            element.decompose()
        
        content_element = soup.find('body') or soup
    
    # 提取文本内容
    if content_element:
        # 获取所有文本内容
        texts = []
        for element in content_element.descendants:
            if element.name in ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = element.get_text(strip=False)
                if text and not text.isspace():
                    # 清理文本
                    cleaned_text = re.sub(r'\s+', ' ', text).strip()
                    # 过滤掉免责声明和版权信息
                    if (cleaned_text and 
                        '免责声明' not in cleaned_text and 
                        '版权所有' not in cleaned_text and
                        '沪ICP证' not in cleaned_text and
                        'EM_StockImg_' not in cleaned_text and
                        'autoimg' not in cleaned_text):
                        texts.append(cleaned_text)
        
        # 合并段落，保留段落间的换行
        content = '\n\n'.join(texts)
    else:
        # 最后的备选方案：直接获取所有文本
        content = soup.get_text()
        # 清理多余的空白字符
        content = re.sub(r'\s+', ' ', content).strip()
        # 过滤掉免责声明和版权信息
        disclaimer_keywords = ['免责声明', '版权所有', '沪ICP证', '网站备案号', '经营证券期货业务许可证']
        for keyword in disclaimer_keywords:
            if keyword in content:
                disclaimer_pos = content.find(keyword)
                content = content[:disclaimer_pos].strip()
    
    # 进一步清理内容，移除HTML标签残留和CSS样式
    content = _clean_content(content)
    
    return content


def _clean_content(content: str) -> str:
    """
    清理内容中的HTML标签、CSS样式和其他无关内容
    
    :param content: 原始内容
    :return: 清理后的内容
    """
    if not content:
        return ""
    
    # 移除HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    
    # 移除CSS样式块和规则（更全面的匹配）
    content = re.sub(r'[a-zA-Z0-9_\-\.:#\s]*\{[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 移除EM_开头的标记
    content = re.sub(r'EM_[A-Za-z_]+(?:_[A-Za-z0-9_]+)*', '', content)
    
    # 移除独立的CSS属性
    content = re.sub(r'[a-z\-]+:\s*[a-zA-Z0-9#%\s\-\(\)_]*[;}]?', '', content, flags=re.IGNORECASE)
    
    # 移除常见的CSS类名和ID相关的内容
    css_patterns = [
        r'autoimg\s*\{[^}]*\}',
        r'\.tbl\s*\{[^}]*\}',
        r'tbl\s*\{[^}]*\}',
        r'display\s*:\s*[a-z]+',
        r'border\s*:\s*[0-9a-z\s]+',
        r'margin\s*:\s*[0-9a-z\s]+',
        r'padding\s*:\s*[0-9a-z\s]+',
        r'width\s*:\s*[0-9a-z%]+',
        r'height\s*:\s*[0-9a-z%]+',
        r'color\s*:\s*[#0-9a-z]+',
        r'background\s*:\s*[#0-9a-z\s]+'
    ]
    
    for pattern in css_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 移除CSS样式定义中的各种属性值
    css_properties = [
        r'\bblock\b',
        r'\bnone\b',
        r'\binline\b',
        r'\bflex\b',
        r'\bgrid\b',
        r'\brelative\b',
        r'\babsolute\b',
        r'\bfixed\b',
        r'\bsticky\b',
        r'\bnormal\b',
        r'\bbold\b',
        r'\bleft\b',
        r'\bright\b',
        r'\bcenter\b'
    ]
    
    for prop in css_properties:
        content = re.sub(prop, '', content, flags=re.IGNORECASE)
    
    # 移除常见的CSS单位和数值
    content = re.sub(r'\b\d+[a-z%]*\b', '', content)
    
    # 移除多余的空白字符
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 移除开头和结尾的无关字符
    content = content.strip('{};:.,()[]|\\/!@#$%^&*+-=_~`"\'' )
    
    # 移除单独的标点符号行和过短的行
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()
        # 保留包含足够文字内容的行
        if len(stripped_line) > 3 and not re.match(r'^[{};:.,\-\s]+$', stripped_line):
            # 进一步清理行内的无关内容
            cleaned_line = re.sub(r'^[{};:.,\-\s]+', '', stripped_line)
            cleaned_line = re.sub(r'[{};:.,\-\s]+$', '', cleaned_line)
            if len(cleaned_line) > 3:
                cleaned_lines.append(cleaned_line)
    
    content = '\n'.join(cleaned_lines)
    
    # 最终清理多余的空白
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 确保内容中不包含明显的CSS或HTML残留
    suspicious_patterns = [
        r'\.autoimg',
        r'\.tbl',
        r'EM_StockImg_',
        r'EM_[A-Za-z]*',
        r'EM[A-Za-z]*',
        r'\{',
        r'\}',
        r';',
        r':',
        r'border\-',
        r'margin\-',
        r'padding\-',
        r'display\-',
        r'width\-',
        r'height\-',
        r'color\-',
        r'background\-',
        r'autoimg',
        r'\.tbl'
    ]
    
    for pattern in suspicious_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 最终清理
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 移除过短的行（再次检查）
    lines = content.split('\n')
    final_lines = []
    for line in lines:
        if len(line.strip()) > 3:
            final_lines.append(line)
    
    content = '\n'.join(final_lines)
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 最后一遍清理，确保没有残留的CSS或HTML内容
    content = re.sub(r'[a-zA-Z_\-]+:', '', content)
    content = re.sub(r'\d+px', '', content)
    content = re.sub(r'\d+%', '', content)
    content = re.sub(r'#?[a-fA-F0-9]{3,6}', '', content)
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 确保最终内容不包含明显的HTML/CSS残留
    final_clean_patterns = [
        r'EM_',
        r'\.autoimg',
        r'\.tbl',
        r'\{',
        r'\}',
        r';',
        r':',
        r'border',
        r'margin',
        r'padding',
        r'display',
        r'width',
        r'height',
        r'color',
        r'background'
    ]
    
    for pattern in final_clean_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 最终清理
    content = re.sub(r'\s+', ' ', content).strip()
    
    return content


def _process_content(content: str, size: Optional[int]) -> str:
    """
    处理内容，根据size参数截取
    
    :param content: 原始内容
    :param size: 截取长度
    :return: 处理后的内容
    """
    if not content:
        return "未能提取到新闻内容"
    
    # 清理内容
    content = _clean_content(content)
    
    # 如果指定了size，则按段落边界截取内容
    if size and len(content) > size:
        # 找到最接近size的段落边界
        truncated = content[:size]
        last_paragraph_end = truncated.rfind('\n\n')
        if last_paragraph_end != -1:
            content = truncated[:last_paragraph_end]
        else:
            # 如果没有找到段落边界，则在单词边界处截取
            last_space = truncated.rfind(' ')
            if last_space != -1:
                content = truncated[:last_space] + '...'
            else:
                content = truncated + '...'
    
    return content


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
            
            # 使用get_news_content函数获取新闻内容
            temp_df["新闻内容"] = temp_df["Art_Url"].apply(lambda url: get_news_content(url))
            
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
    
    # 打印新闻链接和摘要
    print(f"\n新闻摘要 (前5条):")
    print("=" * 80)
    for idx, (url, content) in enumerate(zip(stock_news_em_df["新闻链接"].head(5), stock_news_em_df["新闻内容"].head(5)), 1):
        print(f"{idx}. {url}")
        print(f"摘要: {content}")
