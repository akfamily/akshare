# -*- coding:utf-8 -*-
# Author: PeterWeyland
# CreateTime: 2025-09-09
# Description: simple introduction of the code


import concurrent.futures
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timedelta, date

import pandas as pd
import akshare as ak
import custom_extend.custom_fund_etf_em as cfee
import requests
from sqlalchemy import create_engine, func, text, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import logging

from utils.db_utils import get_db_url

# 指数数据到本地
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
metadata = MetaData()
# 创建Session工厂
SessionLocal = sessionmaker(
    autocommit=False,  # 不自动提交
    autoflush=False,  # 不自动flush
    bind=engine  # 绑定到引擎
)


@contextmanager
def get_db_session():
    """
    数据库会话的上下文管理器
    使用方式：
    with get_db_session() as session:
        # 在这里执行数据库操作
    """
    session = SessionLocal()  # 从工厂创建新的Session
    try:
        yield session  # 将session提供给代码块使用
        session.commit()  # 如果代码块没有异常，提交事务
    except Exception as e:
        session.rollback()  # 如果有异常，回滚事务
        logger.error(f"数据库操作失败: {e}")
        raise  # 重新抛出异常
    finally:
        session.close()  # 无论如何都关闭Session


def append_2_table(table_name, df):
    try:
        with get_db_session() as session:
            try:
                # 使用session的connection
                df.to_sql(
                    name=table_name,
                    con=session.connection(),
                    if_exists='append',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                # 不需要显式commit，上下文管理器会自动处理
                print(f"{table_name} 成功插入 {len(df)} 条数据")
                return True

            except Exception as e:
                # 不需要显式rollback，上下文管理器会自动处理
                print(f"插入数据时出错: {e}")
                raise e  # 重新抛出异常，让外层捕获

    except SQLAlchemyError as e:
        print(f"数据库错误: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        traceback.print_exc()
        return False


def update_single_index_data_2_database(code, prefix, max_retries=5, delay=0.1):
    """
    更新单个股票数据到数据库。如果最近1个月有数据，则不更新。保持一个月更新一次的频率
    :param code:
    :param max_retries:
    :param delay:
    :return:
    """
    # table_name = f"index_{code}"
    table_name = f"{prefix}{code}"
    try:
        # 高效读取最后一行
        last_date = get_last_date(table_name)
        if last_date:
            # 如果和今天相差20天内，则直接返回
            today = datetime.now().date()
            diff_days = (today - last_date).days
            if diff_days < 20:
                print("20天内有数据，暂不获取...")
                return True  # 有数据但不需更新，也算成功
            # 最后一条数据的日期+1
            start_date = (last_date + timedelta(days=1)).strftime('%Y%m%d')
            end_date = today.strftime('%Y%m%d')

            print(f"需要更新数据 {code}，从 {start_date} 到 {end_date}")
            df = None
            tdelay = delay
            for attempt in range(max_retries):
                try:
                    # df = ak.index_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date)
                    # df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date=start_date,
                    #                           end_date=end_date, adjust="qfq")
                    df = cfee.fund_etf_hist_em(symbol=code, period="daily", start_date=start_date,
                                             end_date=end_date, adjust="qfq")
                    # 成功则退出
                    break
                except requests.exceptions.ConnectionError as cre:
                    print(f"超时尝试 {attempt + 1}")
                    time.sleep(tdelay)
                    # 如果失败，让超时时间增加
                    tdelay += 0.1

            if df is None or df.shape[0] == 0:
                print(f"接口返回空数据 {code}")
                return True  # 空数据但不算失败

            if len(df) > 0:
                # 重命名列
                df = df.rename(columns={
                    '日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low',
                    '成交量': 'volume', '涨跌幅': 'pct_chg', '换手率': 'turnover_rate'
                })
                df.index = pd.to_datetime(df.date)
                df = df[['date', 'open', 'close', 'high', 'low', 'volume', 'pct_chg', 'turnover_rate']]

                df['open'] = pd.to_numeric(df['open'])
                df['close'] = pd.to_numeric(df['close'])
                df['high'] = pd.to_numeric(df['high'])
                df['low'] = pd.to_numeric(df['low'])
                df['volume'] = pd.to_numeric(df['volume'])
                df['pct_chg'] = pd.to_numeric(df['pct_chg'])
                df['turnover_rate'] = pd.to_numeric(df['turnover_rate'])

                success = append_2_table(table_name, df)
                if success:
                    print(f"数据已更新 {code}，新增 {len(df)} 条记录")
                    return True  # 成功返回True
                else:
                    return False  # 失败返回False
            else:
                print(f"接口返回空数据 {code}")
                return True
        else:
            print(f"表为空 {code}，重新获取所有数据")
            success = fetch_all_data(code, table_name)
            return success

    except Exception as e:
        print(f"更新数据发生异常 {code}: {e}")
        return False


def get_last_date(table_name):
    """
    获取table_name表记录最新日期
    :param table_name:
    :return:
    """
    try:
        with get_db_session() as session:
            # 使用 text() 执行原生 SQL 查询
            result = session.execute(text(f"SELECT MAX(date) FROM {table_name}"))
            max_date = result.scalar()
            if max_date:
                return max_date
            else:
                return None
    except Exception as e:
        print(f"获取最后日期时出错 {table_name}: {e}")
        return None

sina_symbol_dict = {
    '159819':'sz159819',
    '159915': 'sz159915',
    '159941': 'sz159941',
    '159949':'sz159949',
    '159985':'sz159985',
    '510180': 'sh510180',
    '518880': 'sh518880',
    '513100':'sh513100',
    '513500':'sh513500',
    '512050':'sh512050',
    '512100':'sh512100',
    '588000':'sh588000',
    '588100':'sh588100',
    '513330':'sh513330',
    '513090':'sh513090',
    '512480':'sh512480',
    '510150':'sh510150',
    '562500':'sh562500',
    '512930':'sh512930',
}

def fetch_all_data(code, table_name, max_retries=5, delay=0.1):
    """获取所有历史数据并保存到表中"""
    try:
        df = None
        tdelay = delay
        for attempt in range(max_retries):
            try:
                # df = cfee.fund_etf_hist_em(symbol=code, period="daily", adjust="qfq")
                sina_symbol = sina_symbol_dict.get(code)
                if sina_symbol is None:
                    s = f'{code}未维护别名'
                    raise ValueError(s)
                df = ak.fund_etf_hist_sina(symbol=sina_symbol)
                # 成功则退出
                break
            except requests.exceptions.ConnectionError as cre:
                print(f"超时尝试 {attempt + 1}")
                time.sleep(tdelay)
                # 如果失败，让超时时间增加
                tdelay += 0.1

        if df is None or df.shape[0] == 0:
            print(f"接口返回空数据 {code}")
            return False

        if len(df) > 0:
            df = df.rename(columns={
                '日期': 'date', '开盘': 'open', '最高': 'high', '最低': 'low',
                '收盘': 'close', '成交量': 'volume',
                # '涨跌幅': 'pct_chg', '换手率': 'turnover_rate'
            })
            df.index = pd.to_datetime(df.date)
            df = df[['date', 'open', 'high', 'low', 'close', 'volume',
                     # 'pct_chg', 'turnover_rate'
                     ]]
            df['open'] = pd.to_numeric(df['open'])
            df['high'] = pd.to_numeric(df['high'])
            df['low'] = pd.to_numeric(df['low'])
            df['close'] = pd.to_numeric(df['close'])
            df['volume'] = pd.to_numeric(df['volume'])
            # df['pct_chg'] = pd.to_numeric(df['pct_chg'])
            # df['turnover_rate'] = pd.to_numeric(df['turnover_rate'])

            success = append_2_table(table_name, df)
            if success:
                print(f"数据已保存 {code}，共 {len(df)} 条记录")
                return True  # 成功返回True
            else:
                return False  # 失败返回False
        else:
            print(f"接口返回空数据 {code}")
            return False

    except Exception as e:
        print(f"获取所有数据并保存时出错 {code}: {e}")
        return False


def get_single_table_count(code):
    """多线程中获取单个表的记录数"""
    try:
        with get_db_session() as session:
            table_name = f'index_{code}'
            count = session.execute(text(f"SELECT count(*) FROM {table_name}")).scalar()
            return code, count, None
    except Exception as e:
        print(f"表 {table_name} 查询失败: {e}")
        return code, 0, str(e)


def get_counts(stock_codes, max_workers=10):
    """使用 as_completed 先收集结果再统一打印"""
    start_time = time.time()
    results = {}
    errors = {}
    min_code = None
    min_count = sys.maxsize
    max_code = None
    # max_count = -sys.maxsize - 1
    # 这里只会是0或正整数
    max_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_code = {
            executor.submit(get_single_table_count, code): code
            for code in stock_codes
        }

        # 收集所有结果
        completed_count = 0
        for future in concurrent.futures.as_completed(future_to_code):
            completed_count += 1
            stock_code = future_to_code[future]
            try:
                stock_code, count, error = future.result()
                if error:
                    errors[stock_code] = error
                else:
                    results[stock_code] = count
                    if count < min_count:
                        min_code = stock_code
                        min_count = count
                    if count > max_count:
                        max_code = stock_code
                        max_count = count
            except Exception as e:
                errors[stock_code] = str(e)

        # 统一打印结果（按股票代码排序）
    print("\n=== 查询结果 ===")
    for stock_code in sorted(results.keys()):
        print(f"表 stock_qfq_{stock_code}: {results[stock_code]} 条记录")

    if errors:
        print("\n=== 错误信息 ===")
        for stock_code in sorted(errors.keys()):
            print(f"表 stock_qfq_{stock_code}: {errors[stock_code]}")

    print(f"\n=== 统计信息 ===")
    print(f"查询耗时: {time.time() - start_time:.2f} 秒")
    print(f"成功查询: {len(results)} 个表")
    print(f"查询失败: {len(errors)} 个表")
    print(f"总记录数: {sum(results.values())}")
    print(f"最少记录表: {min_code}, {min_count}")
    print(f"最多记录表: {max_code}, {max_count}")

    return results, errors


def update_data_2_database():
    # update_single_index_data_2_database(code='518880', prefix='etf_qfq_')
    # update_single_index_data_2_database(code='159941', prefix='etf_qfq_')
    # update_single_index_data_2_database(code='159915', prefix='etf_qfq_')
    # update_single_index_data_2_database(code='510180', prefix='etf_qfq_')

    # update_single_index_data_2_database(code='159985', prefix='sina_etf_')
    # update_single_index_data_2_database(code='518880', prefix='sina_etf_')
    # update_single_index_data_2_database(code='513100', prefix='sina_etf_')
    # update_single_index_data_2_database(code='513500', prefix='sina_etf_')
    # update_single_index_data_2_database(code='512050', prefix='sina_etf_')
    # update_single_index_data_2_database(code='159949', prefix='sina_etf_')
    # update_single_index_data_2_database(code='512100', prefix='sina_etf_')
    # update_single_index_data_2_database(code='588000', prefix='sina_etf_')
    # update_single_index_data_2_database(code='588100', prefix='sina_etf_')
    # update_single_index_data_2_database(code='159819', prefix='sina_etf_')
    # update_single_index_data_2_database(code='513330', prefix='sina_etf_')
    # update_single_index_data_2_database(code='513090', prefix='sina_etf_')
    # update_single_index_data_2_database(code='512480', prefix='sina_etf_')
    # update_single_index_data_2_database(code='510150', prefix='sina_etf_')
    # update_single_index_data_2_database(code='562500', prefix='sina_etf_')
    update_single_index_data_2_database(code='512930', prefix='sina_etf_')


if __name__ == '__main__':
    update_data_2_database()
