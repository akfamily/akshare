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
import requests
from sqlalchemy import create_engine, func, text, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import logging

from data_2_local.tdx_data import get_file_data
from utils.data_2_local.create_tables import obtain_middle_small_stock_codes
from utils.db_utils import get_db_url

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


def clear_error_table():
    """清空task_error_code表"""
    try:
        with get_db_session() as session:
            error_table = Table('task_error_code', metadata, autoload_with=engine)
            session.execute(error_table.delete())
            logger.info("已清空task_error_code表")
    except SQLAlchemyError as e:
        logger.error(f"清空错误表时发生异常: {e}")


def record_error_code(error_code):
    """将错误代码插入到task_error_code表"""
    try:
        with get_db_session() as session:
            error_table = Table('task_error_code', metadata, autoload_with=engine)
            current_time = datetime.now()
            # 插入错误记录
            stmt = error_table.insert().values(
                stock_code=error_code,
                error_time=current_time
            )
            session.execute(stmt)
            logger.info(f"已记录错误代码: {error_code}, 时间: {current_time}")

    except SQLAlchemyError as e:
        logger.error(f"记录错误代码时发生异常: {e}")


def stock_price_data_2_database(stock_codes):
    """
    中小板股票数据存到数据库。由于中小板已经和主板合并，列表已经确定，直接从表里拿就行了，不用再从重新获取
    :return:
    """
    # 清空task_error_code表
    clear_error_table()
    # 获取中小板代码列表
    total_count = len(stock_codes)
    print(f"开始处理，总共 {total_count} 个股票代码")
    successful_count = 0
    failed_count = 0
    # 线程池，max_workers控制线程数
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有任务
        future_to_code = {
            executor.submit(update_single_price_data_2_database, code): code
            for code in stock_codes
        }
        for future in concurrent.futures.as_completed(future_to_code):
            code = future_to_code[future]
            try:
                # 获取结果，如果有异常会在这里抛出
                success = future.result()
                if success:
                    successful_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                print(f"处理股票代码 {code} 时出错: {e}")
                failed_count += 1
    # 打印最终统计结果
    print("=" * 50)
    print("处理完成统计:")
    print(f"总处理条数: {total_count}")
    print(f"成功条数: {successful_count}")
    print(f"失败条数: {failed_count}")
    print(f"成功率: {(successful_count / total_count * 100):.2f}%")
    print("=" * 50)


def append_2_table(table_name, df, code):
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
        record_error_code(code)
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        traceback.print_exc()
        record_error_code(code)
        return False


def update_single_price_data_2_database(code, max_retries=5, delay=0.1):
    """
    更新单个股票数据到数据库。如果最近1个月有数据，则不更新。保持一个月更新一次的频率
    :param code:
    :param max_retries:
    :param delay:
    :return:
    """
    table_name = f"stock_qfq_{code}"
    try:
        # 高效读取最后一行
        last_date = get_last_date(table_name)
        if last_date:
            greater_date_ts = pd.Timestamp(last_date)
            fetch_data_tdx(code, table_name, greater_date_ts)
            # today = datetime.now().date()
            # # 最后一条数据的日期+1
            # start_date = (last_date + timedelta(days=1)).strftime('%Y%m%d')
            # end_date = today.strftime('%Y%m%d')
            # print(f"需要更新数据 {code}，从 {start_date} 到 {end_date}")
            # df = None
            # tdelay = delay
            # for attempt in range(max_retries):
            #     try:
            #         df = ak.stock_zh_a_hist(
            #             symbol=code,
            #             period="daily",
            #             start_date=start_date,
            #             end_date=end_date,
            #             adjust="qfq"
            #         )
            #         # 成功则退出
            #         break
            #     except requests.exceptions.ConnectionError as cre:
            #         print(f"超时尝试 {attempt + 1}")
            #         time.sleep(tdelay)
            #         # 如果失败，让超时时间增加
            #         tdelay += 0.1
            # if df is None or df.shape[0] == 0:
            #     print(f"接口返回空数据 {code}")
            #     return True  # 空数据但不算失败
            # if len(df) > 0:
            #     # 重命名列
            #     df = df.rename(columns={
            #         '日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low',
            #         '成交量': 'volume', '涨跌幅': 'pct_chg', '换手率': 'turnover_rate'
            #     })
            #     df.index = pd.to_datetime(df.date)
            #     df = df[['date', 'open', 'close', 'high', 'low', 'volume', 'pct_chg', 'turnover_rate']]
            #
            #     df['open'] = pd.to_numeric(df['open'])
            #     df['close'] = pd.to_numeric(df['close'])
            #     df['high'] = pd.to_numeric(df['high'])
            #     df['low'] = pd.to_numeric(df['low'])
            #     df['volume'] = pd.to_numeric(df['volume'])
            #     df['pct_chg'] = pd.to_numeric(df['pct_chg'])
            #     df['turnover_rate'] = pd.to_numeric(df['turnover_rate'])
            #
            #     success = append_2_table(table_name, df, code)
            #     if success:
            #         print(f"数据已更新 {code}，新增 {len(df)} 条记录")
            #         return True  # 成功返回True
            #     else:
            #         return False  # 失败返回False
            # else:
            #     print(f"接口返回空数据 {code}")
            #     return True
        else:
            print(f"表为空 {code}，重新获取所有数据")
            # success = fetch_all_data(code, table_name)
            fetch_data_tdx(code, table_name)
            return True

    except Exception as e:
        print(f"更新数据发生异常 {code}: {e}")
        record_error_code(code)
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


def fetch_all_data(stock_code, table_name, max_retries=5, delay=0.1):
    """获取所有历史数据并保存到表中"""
    try:
        df = None
        tdelay = delay
        for attempt in range(max_retries):
            try:
                df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")
                # df = ak.stock_zh_a_hist(
                #     symbol=stock_code,
                #     period="daily",
                #     start_date='20250101',
                #     end_date='20250201',
                #     adjust="qfq"
                # )
                # 成功则退出
                break
            except requests.exceptions.ConnectionError as cre:
                print(f"超时尝试 {attempt + 1}")
                time.sleep(tdelay)
                # 如果失败，让超时时间增加
                tdelay += 0.1

        if df is None or df.shape[0] == 0:
            print(f"接口返回空数据 {stock_code}")
            return False

        if len(df) > 0:
            df = df.rename(columns={
                '日期': 'date', '开盘': 'open', '最高': 'high', '最低': 'low',
                '收盘': 'close', '成交量': 'volume', '涨跌幅': 'pct_chg', '换手率': 'turnover_rate'
            })
            df.index = pd.to_datetime(df.date)
            df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'pct_chg', 'turnover_rate']]

            df['open'] = pd.to_numeric(df['open'])
            df['high'] = pd.to_numeric(df['high'])
            df['low'] = pd.to_numeric(df['low'])
            df['close'] = pd.to_numeric(df['close'])
            df['volume'] = pd.to_numeric(df['volume'])
            df['pct_chg'] = pd.to_numeric(df['pct_chg'])
            df['turnover_rate'] = pd.to_numeric(df['turnover_rate'])

            success = append_2_table(table_name, df, stock_code)
            if success:
                print(f"数据已保存 {stock_code}，共 {len(df)} 条记录")
                return True  # 成功返回True
            else:
                return False  # 失败返回False
        else:
            print(f"接口返回空数据 {stock_code}")
            return False

    except Exception as e:
        print(f"获取所有数据并保存时出错 {stock_code}: {e}")
        record_error_code(stock_code)
        return False


def fetch_data_tdx(code, table_name, greater_date_ts=None):
    df = get_file_data(code=code, greater_date_ts=greater_date_ts)
    if df is None or df.shape[0] == 0:
        print(f"未获取到数据 {code}")
        return False
    success = append_2_table(table_name, df, code)
    if success:
        print(f"数据已保存 {code}，共 {len(df)} 条记录")
        return True  # 成功返回True
    else:
        return False  # 失败返回False

def get_single_table_count(stock_code):
    """多线程中获取单个表的记录数"""
    try:
        with get_db_session() as session:
            table_name = f'stock_qfq_{stock_code}'
            count = session.execute(text(f"SELECT count(*) FROM {table_name}")).scalar()
            return (stock_code, count, None)
    except Exception as e:
        print(f"表 {table_name} 查询失败: {e}")
        return (stock_code, 0, str(e))


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

    print("按照count从大到小排序取前100个，打印最后10个")
    # 按照count从大到小排序取前100个
    sorted_items = sorted(results.items(), key=lambda x: x[1], reverse=True)
    top_100 = sorted_items[:100]
    # 打印最后10个
    for code in top_100[90:]:
        print(code)

    return results, errors


def get_399101_table_counts():
    # 成功查询: 946 个表
    # 查询失败: 0 个表
    # 总记录数: 3021662
    # 最少记录表: 003040, 1090
    # 最多记录表: 002028, 5087
    stock_codes = obtain_middle_small_stock_codes()
    get_counts(stock_codes)


if __name__ == '__main__':
    # update_single_price_data_2_database('003040')
    # clear_error_table()
    # middle_small_price_data_2_database()
    # get_399101_table_counts()
    with open(file='data/stock_price_data_2_local/stock_codes.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_stock_codes = content.split('\n')
        print(len(t_stock_codes))

    stock_price_data_2_database(t_stock_codes)