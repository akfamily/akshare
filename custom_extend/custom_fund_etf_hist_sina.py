# -*- coding:utf-8 -*-
# 对fund_etf_hist_sina的扩展

import requests
import pandas as pd
import json
import re


def get_etf_history_sina(symbol: str, count: int = 100) -> pd.DataFrame:
    """
    新浪财经K线数据接口 - 通过数量参数控制数据量
    """
    # 确保有市场前缀
    if not symbol.startswith(('sh', 'sz')):
        if symbol.startswith(('50', '51', '58')):
            symbol = f"sh{symbol}"
        else:
            symbol = f"sz{symbol}"

    # 新浪K线数据接口
    url = "https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20x=/CN_MarketDataService.getKLineData"

    params = {
        "symbol": symbol,
        "scale": "240",  # 240分钟，即日线
        "datalen": str(count),  # 数据条数
        "ma": "no"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn/",
        "Host": "quotes.sina.cn"
    }

    try:
        print(f"请求 {symbol} 最近 {count} 条数据")

        response = requests.get(url, params=params, headers=headers, timeout=15)
        print(f"响应状态: {response.status_code}")

        if response.status_code != 200:
            return pd.DataFrame()

        content = response.text
        print(f"响应长度: {len(content)}")

        # 解析JSONP响应
        json_match = re.search(r'\((\[.*])\)', content)
        if json_match:
            json_str = json_match.group(1)
            data = json.loads(json_str)

            if data:
                df = pd.DataFrame(data)

                # 重命名列
                column_mapping = {
                    'day': 'date',
                    'open': 'open',
                    'high': 'high',
                    'low': 'low',
                    'close': 'close',
                    'volume': 'volume'
                }
                df = df.rename(columns=column_mapping)

                # 数据类型转换
                df['date'] = pd.to_datetime(df['date'])
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                print(f"成功获取 {len(df)} 条数据")
                return df

        return pd.DataFrame()

    except Exception as e:
        print(f"接口调用失败: {e}")
        return pd.DataFrame()


# 如果需要日期范围筛选，可以在获取后处理
def get_etf_history_by_date(symbol: str, start_date: str = None, end_date: str = None,
                            max_count: int = 1000) -> pd.DataFrame:
    """
    通过获取较多数据后进行日期筛选
    """
    # 先获取足够多的数据
    df = get_etf_history_sina(symbol, max_count)

    if df.empty:
        return df

    # 然后进行日期筛选
    if start_date:
        start_dt = pd.to_datetime(start_date)
        df = df[df['date'] >= start_dt]

    if end_date:
        end_dt = pd.to_datetime(end_date)
        df = df[df['date'] <= end_dt]

    return df.reset_index(drop=True)


# 测试代码
if __name__ == "__main__":
    # 测试获取最近100条数据
    df = get_etf_history_sina("510050", 100)
    if not df.empty:
        print("获取成功!")
        print(f"数据日期范围: {df['date'].min()} 到 {df['date'].max()}")
        print(f"数据条数: {len(df)}")
        print(df.head())

    print("\n" + "=" * 50)

    # 测试按日期范围获取（通过后筛选）
    df2 = get_etf_history_by_date("510050", "2024-01-01", "2024-01-31", 500)
    if not df2.empty:
        print("按日期筛选成功!")
        print(f"筛选后数据条数: {len(df2)}")
        print(df2.head())