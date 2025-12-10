import logging
import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from data_2_local.common_data_2_local import df_append_2_local
from utils.db_utils import get_db_url

# 数据库连接配置
DATABASE_URL = get_db_url()
# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 生产环境关闭SQL日志
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
    pool_timeout=30,  # 获取连接超时时间
    pool_recycle=1800,  # 连接回收时间（避免MySQL 8小时问题）
    pool_pre_ping=True  # 执行前检测连接有效性
)
# 创建Session工厂
SessionLocal = sessionmaker(
    autocommit=False,  # 不自动提交
    autoflush=False,  # 不自动flush
    bind=engine  # 绑定到引擎
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




def get_file_name(code, delisted_stock_code_set):
    # 已退市股票。用当前页面数据导出的。已退市股票用高级导出是空的，没数据。
    if code in delisted_stock_code_set:
        file_name = f'T{code}.txt'
    elif code.startswith('6'):
        file_name = f"bfq-SH#{code}.txt"
    elif code.startswith('0'):
        file_name = f"bfq-SZ#{code}.txt"
    else:
        file_name = ''
    return file_name


def get_file_data(code, greater_date_ts=None, delisted_stock_code_set=None):
    if delisted_stock_code_set is None:
        delisted_stock_code_set = {}
    file_name = get_file_name(code, delisted_stock_code_set)
    file_path = f'D:/new_tdx/T0002/export/bfq-399101/{file_name}'

    dtype_dict = {
        'open': 'float64',
        'close': 'float64',
        'high': 'float64',
        'low': 'float64',
        # 'volume': 'int64',
    }
    # 退市股是特殊的少数几个，用当前页面导出的数据。两种格式不一样
    if code in delisted_stock_code_set:
        skiprows = 4
        column_names = ['date', 'open', 'high', 'low', 'close', 'volume', 'MA.MA1', 'MA.MA2', 'MA.MA3', 'MA.MA4', 'MA.MA5', 'MA.MA6', 'MA.MA7', 'MA.MA8']
    else:
        skiprows = 2
        # turnover: 成交额
        column_names = ['date', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    df = pd.read_csv(file_path,
                     sep='\s+',
                     skiprows=skiprows,
                     comment='#',  # 跳过以#开头的行
                     skip_blank_lines=True,  # 跳过空行
                     names=column_names,
                     dtype=dtype_dict,
                     encoding='GBK')
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df['code'] = code
    df['date'] = pd.to_datetime(df['date'])
    if greater_date_ts is not None:
        df = df[df['date'] > greater_date_ts]
    return df


if __name__ == '__main__':
    with open(file='data/temp/delisted_middle_small.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_delisted_stock_code_list = content.split('\n')
        t_delisted_stock_code_set = set(t_delisted_stock_code_list[1:])

    with open(file='data/bfq_daily_stock_price_sz_main_2_local/399101_codes.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_stock_codes = content.split('\n')
        print(len(t_stock_codes))
    with open(file='data/bfq_daily_stock_price_sz_main_2_local/complete_codes.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_complete_codes = content.split('\n')
        print(len(t_complete_codes) - 1)
    t_complete_code_set = set(t_complete_codes)
    t_codes = []
    for code in t_stock_codes:
        if code in t_complete_code_set:
            continue
        t_codes.append(code)
    # t_codes = ['002003']
    print(f'len_t_codes: {len(t_codes)}')

    for code in t_codes:
        tdf = get_file_data(code, None, t_delisted_stock_code_set)
        df_append_2_local(table_name='bfq_daily_stock_price_sz_main', df=tdf)
        with open(file='data/bfq_daily_stock_price_sz_main_2_local/complete_codes.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{code}\n')