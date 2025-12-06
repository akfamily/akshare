import logging
import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

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


class BulkDataLoader:
    def __init__(self):
        self.engine = engine

    def load_bulk_data(self, codes):
        """一次性加载所有股票数据"""
        price_queries = []
        for code in codes:
            # 价格数据查询。前复权数据，早期数据涨跌幅列无意义
            price_query = f"""
            SELECT '{code}' as code, date, open, close, high, low, volume, turnover_rate 
            FROM stock_qfq_{code} 
            """
            price_queries.append(price_query)
        # 执行批量查询
        full_price_query = " UNION ALL ".join(price_queries)
        price_df = pd.read_sql(full_price_query, self.engine)

        return price_df


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)  # 设置行数为无限制
    pd.set_option('display.max_columns', None)  # 设置列数为无限制
    pd.set_option('display.width', 1000)  # 设置列宽
    pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左


    db_loader = BulkDataLoader()
    with open(file='data/index_stocks/399101_codes.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_stock_codes = content.split('\n')
        print(len(t_stock_codes))
    time0 = time.time()
    t_price_df = db_loader.load_bulk_data(t_stock_codes)
    time1 = time.time()
    run_time0 = time1 - time0
    print(f"获取df, 运行时间: {run_time0:.4f} 秒")
    print(t_price_df.shape[0])
    table_name = 'qfq_daily_stock_price_sz_main'
    with get_db_session() as session:
        try:
            # 使用session的connection
            t_price_df.to_sql(
                name=table_name,
                con=session.connection(),
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            # 不需要显式commit，上下文管理器会自动处理
            print(f"{table_name} 成功插入 {t_price_df.shape[0]} 条数据")
        except Exception as e:
            # 不需要显式rollback，上下文管理器会自动处理
            print(f"插入数据时出错: {e}")
            raise e  # 重新抛出异常，让外层捕获
    time2 = time.time()
    run_time1 = time2 - time1
    print(f"插入表, 运行时间: {run_time1:.4f} 秒")
