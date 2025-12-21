# -*- coding:utf-8 -*-
from typing import Set

# Author: PeterWeyland
# CreateTime: 2025-09-11
# Description: simple introduction of the code
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Date, DECIMAL, UniqueConstraint, text
from datetime import datetime
import concurrent.futures
import time

from sqlalchemy.orm import sessionmaker

from utils.db_utils import get_db_url

PREFIX_IDX = "idx_"

# 数据库连接配置
DATABASE_URL = get_db_url()
# 或者使用 pymysql:
# DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/stock_db"

# 创建数据库引擎，增加连接池大小以适应多线程
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=15,
    max_overflow=25,
    pool_timeout=30,
    pool_recycle=1800
)
metadata = MetaData()


def get_exist_table_code_set(prefix) -> Set[str]:
    """获取所有以 stock_cir_cap_ 开头的表名中的代码"""
    table_set = set()
    tlen = len(prefix)
    try:
        with engine.connect() as connection:
            # 查询所有以 stock_cir_cap_ 开头的表
            sql = text(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name LIKE '{prefix}%'
            ORDER BY table_name
            """)

            result = connection.execute(sql, {'prefix': 'stock_cir_cap_'})

            for row in result:
                table_set.add(row[0][tlen:])

            print(f"找到 {len(table_set)} 个以 {prefix} 开头的表")

    except Exception as e:
        print(f"查询表时出错: {e}")

    finally:
        engine.dispose()

    return table_set

def create_single_stock_table_0(stock_code, prefix):
    table_name = None
    try:
        table_name = f'{prefix}{stock_code}'
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `open` DECIMAL(8,4)    COMMENT '开盘' ,
            `close` DECIMAL(8,4)    COMMENT '收盘' ,
            `high` DECIMAL(8,4)    COMMENT '最高' ,
            `low` DECIMAL(8,4)    COMMENT '最低' ,
            `volume` BIGINT    COMMENT '成交量' ,
            `pct_chg` DECIMAL(6,3)    COMMENT '涨跌幅' ,
            `turnover_rate` DECIMAL(8,5)    COMMENT '换手率' ,
            PRIMARY KEY (id)
        )  COMMENT = '股票-前复权-{stock_code}';
        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))
        return stock_code, True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return stock_code, False

def create_single_etf_table_0(stock_code, prefix):
    table_name = None
    try:
        table_name = f'{prefix}{stock_code}'
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `open` DECIMAL(8,4)    COMMENT '开盘' ,
            `close` DECIMAL(8,4)    COMMENT '收盘' ,
            `high` DECIMAL(8,4)    COMMENT '最高' ,
            `low` DECIMAL(8,4)    COMMENT '最低' ,
            `volume` BIGINT    COMMENT '成交量' ,
            `pct_chg` DECIMAL(6,3)    COMMENT '涨跌幅' ,
            `turnover_rate` DECIMAL(8,5)    COMMENT '换手率' ,
            PRIMARY KEY (id)
        )  COMMENT = 'etf-前复权-{stock_code}';

        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(date);
        """

        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))

        return stock_code, True

    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return stock_code, False


def create_single_stock_table(stock_code, prefix):
    """优化版的单个表创建函数"""
    table_name = None
    try:
        table_name = f'{prefix}{stock_code}'
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `cir_cap` DECIMAL(20,2)    COMMENT '流通市值' ,
            PRIMARY KEY (id)
        )  COMMENT = '{stock_code}每日流通市值';
        
        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(date);
        """

        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))

        return stock_code, True

    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return stock_code, False

def create_single_stock_cir_table(stock_code):
    """
    废弃，不存市值了，改为存股本，实际获取数据时再去计算市值
    """
    table_name = None
    try:
        table_name = f'stock_cir_cap_{stock_code}'
        create_sql = f"""
            CREATE TABLE {table_name}(
                `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
                `date` DATE NOT NULL   COMMENT '日期' ,
                `cir_cap` DECIMAL(20,2)    COMMENT '流通市值' ,
                PRIMARY KEY (id)
            )  COMMENT = '{stock_code}每日流通市值';

            """
        idx_sql = f"""
            CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(date);
            """

        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))

        return stock_code, True

    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return stock_code, False

def create_qfq_daily_stock_price_sz_main_table():
    """
    日K中小板股票价格前复权数据，包含深市主板所有代码。注意：中小板已经合并进主板，现在只能根据399101确定中小板列表
    前复权数据，早期数据涨跌幅列无意义
    """
    table_name = 'qfq_daily_stock_price_sz_main'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `open` DECIMAL(8,4)    COMMENT '开盘' ,
            `close` DECIMAL(8,4)    COMMENT '收盘' ,
            `high` DECIMAL(8,4)    COMMENT '最高' ,
            `low` DECIMAL(8,4)    COMMENT '最低' ,
            `volume` BIGINT    COMMENT '成交量' ,
            `turnover_rate` DECIMAL(8,5)    COMMENT '换手率' ,
            PRIMARY KEY (id)
        )  COMMENT = '前复权-日K-股票价格数据-深市主板';
        """
        idx_0_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name}_0 ON {table_name}(code, date);
        """
        idx_1_sql = f"""
        CREATE INDEX {PREFIX_IDX}{table_name}_1 ON {table_name}(date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
            connection.execute(text(idx_1_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_bfq_daily_stock_price_sz_main_table():
    """
    日K中小板股票价格不复权数据，包含深市主板所有代码。注意：中小板已经合并进主板，现在只能根据399101确定中小板列表
    不复权数据
    """
    table_name = 'bfq_daily_stock_price_sz_main'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `open` DECIMAL(8,4)    COMMENT '开盘' ,
            `close` DECIMAL(8,4)    COMMENT '收盘' ,
            `high` DECIMAL(8,4)    COMMENT '最高' ,
            `low` DECIMAL(8,4)    COMMENT '最低' ,
            `pct_chg` DECIMAL(6,3)    COMMENT '涨跌幅' ,
            `volume` BIGINT    COMMENT '成交量' ,
            `turnover` DECIMAL(20,4)    COMMENT '成交额' ,
            PRIMARY KEY (id)
        )  COMMENT = '不复权-日K-股票价格数据-深市主板';
        """
        idx_0_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name}_0 ON {table_name}(code, date);
        """
        idx_1_sql = f"""
        CREATE INDEX {PREFIX_IDX}{table_name}_1 ON {table_name}(date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
            connection.execute(text(idx_1_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_bfq_daily_etf_price_table():
    """
    日K，etf价格不复权数据
    不复权数据
    """
    table_name = 'bfq_daily_etf_price'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `open` DECIMAL(8,4)    COMMENT '开盘' ,
            `close` DECIMAL(8,4)    COMMENT '收盘' ,
            `high` DECIMAL(8,4)    COMMENT '最高' ,
            `low` DECIMAL(8,4)    COMMENT '最低' ,
            `volume` BIGINT    COMMENT '成交量' ,
            `turnover` DECIMAL(20,4)    COMMENT '成交额' ,
            PRIMARY KEY (id)
        )  COMMENT = '不复权-日K-etf价格数据';
        """
        idx_0_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name}_0 ON {table_name}(code, date);
        """
        idx_1_sql = f"""
        CREATE INDEX {PREFIX_IDX}{table_name}_1 ON {table_name}(date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
            connection.execute(text(idx_1_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_daily_stock_cir_sz_main_table():
    """
    每日中小板股票市值数据，包含深市主板所有代码。注意：中小板已经合并进主板，现在只能根据399101确定中小板列表
    不复权数据
    """
    table_name = 'bfq_daily_stock_price_sz_main'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `date` DATE NOT NULL   COMMENT '日期' ,
            `open` DECIMAL(8,4)    COMMENT '开盘' ,
            `close` DECIMAL(8,4)    COMMENT '收盘' ,
            `high` DECIMAL(8,4)    COMMENT '最高' ,
            `low` DECIMAL(8,4)    COMMENT '最低' ,
            `pct_chg` DECIMAL(6,3)    COMMENT '涨跌幅' ,
            `volume` BIGINT    COMMENT '成交量' ,
            `turnover` DECIMAL(20,4)    COMMENT '成交额' ,
            PRIMARY KEY (id)
        )  COMMENT = '不复权-日K-股票价格数据-深市主板';
        """
        idx_0_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name}_0 ON {table_name}(code, date);
        """
        idx_1_sql = f"""
        CREATE INDEX {PREFIX_IDX}{table_name}_1 ON {table_name}(date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
            connection.execute(text(idx_1_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_shenwan_industry_2_table():
    """优化版的单个表创建函数"""
    table_name = 'shenwan_industry_2'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '二级行业代码' ,
            `name` VARCHAR(30) NOT NULL   COMMENT '二级行业名称' ,
            PRIMARY KEY (id)
        )  COMMENT = '申万二级行业';
        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(code);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False


def create_code_industry_2_change_table():
    """
    股票行业(申万二级行业)变化表
    """
    table_name = 'code_industry_2_change'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `start_date` DATE NOT NULL   COMMENT '起始日期' ,
            `industry_code_2` CHAR(6) NOT NULL   COMMENT '二级行业代码' ,
            `industry_name_2` VARCHAR(30) NOT NULL   COMMENT '二级行业名称' ,
            PRIMARY KEY (id)
        )  COMMENT = '股票行业(申万二级行业)变化表';

        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(code, start_date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))
        return True

    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False


def create_code_is_st_change_table():
    """
    股票曾用名变化表
    """
    table_name = 'code_is_st_change'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `start_date` DATE NOT NULL   COMMENT '起始日期' ,
            `is_st` BOOL NOT NULL   COMMENT '是否ST' ,
            PRIMARY KEY (id)
        )  COMMENT = '股票是否ST变化表';
        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(code, start_date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False


def create_code_name_change_table():
    """
    股票曾用名变化表
    """
    table_name = 'code_name_change'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            `start_date` DATE NOT NULL   COMMENT '起始日期' ,
            `name` VARCHAR(30) NOT NULL   COMMENT '二级行业代码' ,
            PRIMARY KEY (id)
        )  COMMENT = '股票曾用名变化表';
        """
        idx_sql = f"""
        CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(code, start_date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_index_stocks_399101_table():
    """
    股票曾用名变化表
    """
    table_name = 'index_stocks_399101'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            PRIMARY KEY (id)
        )  COMMENT = '指数成分股_399101';
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False


def create_adjust_factor_table():
    """
    复权因子。按照baostock数据格式。BaoStock的实现中，adjustFactor（本次复权因子）被设计为向后复权的累积因子，和想后复权因子值一样，这里不存
    """
    table_name = 'adjust_factor'
    try:
        create_sql = f"""
            CREATE TABLE {table_name}(
                `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
                `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
                `divid_operate_date` DATE NOT NULL   COMMENT '除权除息日期' ,
                `fore_adjust_factor` DECIMAL(30,20)    COMMENT '向前复权因子' ,
                `back_adjust_factor` DECIMAL(30,20)    COMMENT '向后复权因子' ,
                PRIMARY KEY (id)
            )  COMMENT = '复权因子';
            """
        idx_0_sql = f"""
            CREATE UNIQUE INDEX {PREFIX_IDX}{table_name}_0 ON {table_name}(code, divid_operate_date);
            """
        idx_1_sql = f"""
        CREATE INDEX {PREFIX_IDX}{table_name}_1 ON {table_name}(divid_operate_date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
            connection.execute(text(idx_1_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_stock_share_change_cninfo_table():
    """
    复权因子。按照baostock数据格式。BaoStock的实现中，adjustFactor（本次复权因子）被设计为向后复权的累积因子，和想后复权因子值一样，这里不存
    """
    table_name = 'stock_share_change_cninfo'
    try:
        create_sql = f"""
            CREATE TABLE {table_name} (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(20) NOT NULL COMMENT '证券代码',
                change_date DATE NOT NULL COMMENT '变动日期',
                security_abbr VARCHAR(20) COMMENT '证券简称',
                institution_name VARCHAR(100) COMMENT '机构名称',
                foreign_corp_share DECIMAL(20, 4) COMMENT '境外法人持股',
                fund_share DECIMAL(20, 4) COMMENT '证券投资基金持股',
                state_share_restricted DECIMAL(20, 4) COMMENT '国家持股-受限',
                state_owned_corp_share DECIMAL(20, 4) COMMENT '国有法人持股',
                placement_corp_share DECIMAL(20, 4) COMMENT '配售法人股',
                founder_share DECIMAL(20, 4) COMMENT '发起人股份',
                non_tradable_share DECIMAL(20, 4) COMMENT '未流通股份',
                foreign_individual_share DECIMAL(20, 4) COMMENT '其中：境外自然人持股',
                other_restricted_share DECIMAL(20, 4) COMMENT '其他流通受限股份',
                other_tradable_share DECIMAL(20, 4) COMMENT '其他流通股',
                foreign_share_restricted DECIMAL(20, 4) COMMENT '外资持股-受限',
                employee_share DECIMAL(20, 4) COMMENT '内部职工股',
                h_share DECIMAL(20, 4) COMMENT '境外上市外资股-H股',
                domestic_corp_share DECIMAL(20, 4) COMMENT '其中：境内法人持股',
                individual_share DECIMAL(20, 4) COMMENT '自然人持股',
                a_share DECIMAL(20, 4) COMMENT '人民币普通股',
                state_owned_corp_share_restricted DECIMAL(20, 4) COMMENT '国有法人持股-受限',
                general_corp_share DECIMAL(20, 4) COMMENT '一般法人持股',
                controlling_shareholder DECIMAL(20, 4) COMMENT '控股股东、实际控制人',
                restricted_h_share DECIMAL(20, 4) COMMENT '其中：限售H股',
                change_reason VARCHAR(100) COMMENT '变动原因',
                announcement_date DATE COMMENT '公告日期',
                domestic_corp_share_2 DECIMAL(20, 4) COMMENT '境内法人持股',
                strategic_investor_share DECIMAL(20, 4) COMMENT '战略投资者持股',
                state_share DECIMAL(20, 4) COMMENT '国家持股',
                restricted_b_share DECIMAL(20, 4) COMMENT '其中：限售B股',
                other_non_tradable_share DECIMAL(20, 4) COMMENT '其他未流通股',
                restricted_tradable_share DECIMAL(20, 4) COMMENT '流通受限股份',
                preferred_share DECIMAL(20, 4) COMMENT '优先股',
                executive_share DECIMAL(20, 4) COMMENT '高管股',
                total_shares DECIMAL(20, 4) COMMENT '总股本',
                restricted_executive_share DECIMAL(20, 4) COMMENT '其中：限售高管股',
                transferred_share DECIMAL(20, 4) COMMENT '转配股',
                b_share DECIMAL(20, 4) COMMENT '境内上市外资股-B股',
                foreign_corp_share_2 DECIMAL(20, 4) COMMENT '其中：境外法人持股',
                fundraising_corp_share DECIMAL(20, 4) COMMENT '募集法人股',
                tradable_share DECIMAL(20, 4) COMMENT '已流通股份',
                domestic_individual_share DECIMAL(20, 4) COMMENT '其中：境内自然人持股',
                other_domestic_restricted DECIMAL(20, 4) COMMENT '其他内资持股-受限',
                change_reason_code VARCHAR(50) COMMENT '变动原因编码',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) COMMENT='股东持股变动表';
            """
        idx_0_sql = f"""
            CREATE UNIQUE INDEX {PREFIX_IDX}{table_name}_0 ON {table_name}(code, change_date);
            """
        idx_1_sql = f"""
        CREATE INDEX {PREFIX_IDX}{table_name}_1 ON {table_name}(change_date);
        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
            connection.execute(text(idx_1_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_stock_listing_date_table():
    """
    复权因子。按照baostock数据格式。BaoStock的实现中，adjustFactor（本次复权因子）被设计为向后复权的累积因子，和想后复权因子值一样，这里不存
    """
    table_name = 'stock_listing_date'
    try:
        create_sql = f"""
            CREATE TABLE {table_name}(
                `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
                `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
                `listing_date` DATE NOT NULL   COMMENT '上市日期' ,
                PRIMARY KEY (id)
            )  COMMENT = '股票上市日期';
            """
        idx_0_sql = f"""
            CREATE UNIQUE INDEX {PREFIX_IDX}{table_name} ON {table_name}(code);
            """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
            connection.execute(text(idx_0_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False

def create_temp_table():
    """
    股票曾用名变化表
    """
    table_name = 'temp'
    try:
        create_sql = f"""
        CREATE TABLE {table_name}(
            `id` INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
            `code` CHAR(6) NOT NULL   COMMENT '股票代码' ,
            PRIMARY KEY (id)
        )  COMMENT = 'temp';

        """
        with engine.begin() as connection:
            connection.execute(text(create_sql))
        return True
    except Exception as e:
        print(f"创建表 {table_name} 时出错: {e}")
        return False


def obtain_middle_small_stock_codes():
    Session = sessionmaker(bind=engine)
    session = Session()
    sql_str = "SELECT code FROM index_stocks_399101"
    try:
        result = session.execute(text(sql_str))
        code_list = [row[0] for row in result]
        return code_list
    except Exception as e:
        print(f"查询出错: {e}")
        return []
    finally:
        session.close()
    # return ['003039', '003038']


def create_stock_tables_parallel(prefix):
    """使用多线程并行创建股票数据表"""
    start_time = time.time()

    stock_codes = obtain_middle_small_stock_codes()
    # 已经存在的表名对应的代码
    exist_table_code_set = get_exist_table_code_set(prefix)
    stock_codes = [code for code in stock_codes if code not in exist_table_code_set]
    total_tables = len(stock_codes)
    successful_tables = 0
    failed_tables = []

    print(f"开始创建 {total_tables} 个股票数据表...")

    # 使用线程池并行创建（根据数据库性能调整线程数）
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # 提交所有任务
        future_to_code = {executor.submit(create_single_stock_table, code, prefix): code for code in stock_codes}

        # 处理完成的任务
        for i, future in enumerate(concurrent.futures.as_completed(future_to_code), 1):
            code = future_to_code[future]
            try:
                result_code, success = future.result()
                if success:
                    successful_tables += 1
                else:
                    failed_tables.append(code)

                # 每完成100个表输出进度
                if i % 100 == 0:
                    print(f"进度: {i}/{total_tables}，成功: {successful_tables}，失败: {len(failed_tables)}")

            except Exception as e:
                print(f"处理股票代码 {code} 时发生异常: {e}")
                failed_tables.append(code)

    end_time = time.time()

    # 输出结果统计
    print("\n" + "=" * 50)
    print("创建完成！")
    print(f"总表数: {total_tables}")
    print(f"成功创建: {successful_tables}")
    print(f"创建失败: {len(failed_tables)}")
    print(f"总耗时: {end_time - start_time:.2f} 秒")
    print(f"平均每个表: {(end_time - start_time) / total_tables:.3f} 秒")

    if failed_tables:
        print(f"\n失败的股票代码（前10个）: {failed_tables[:10]}")
        # 可以选择将失败的代码保存到文件
        with open('failed_tables.txt', 'w') as f:
            for code in failed_tables:
                f.write(f"{code}\n")


def verify_table_creation(sample_codes):
    """验证表是否创建成功"""
    print("\n验证表创建情况...")
    with engine.connect() as connection:
        for code in sample_codes:
            table_name = f'stock_qfq_{code}'
            try:
                sql = text(f"SHOW TABLES LIKE :table_name")
                result = connection.execute(sql, {'table_name': table_name})
                if result.fetchone():
                    print(f"✓ {table_name} 创建成功")
                else:
                    print(f"✗ {table_name} 创建失败")
            except Exception as e:
                print(f"✗ 检查表 {table_name} 时出错: {e}")


if __name__ == '__main__':
    # tprefix = 'stock_cir_cap_'
    # create_stock_tables_parallel(tprefix)
    # tset = get_exist_table_code_set(tprefix)
    # print(tset)

    # tprefix = 'etf_qfq_'
    # create_single_etf_table_0('518880', tprefix)

    # tprefix = 'stock_qfq_'
    # # create_single_stock_table_0('002001', tprefix)
    #
    # with open(file='data/stock_price_data_2_local/stock_codes.txt', mode='r', encoding='utf-8') as f:
    #     content = f.read()
    #     t_stock_codes = content.split('\n')
    #     # print(len(t_stock_codes))
    #     for code in t_stock_codes:
    #         # create_single_stock_table_0(code, tprefix)
    #         create_single_stock_cir_table(code)

    # create_shenwan_industry_2_table()
    # create_code_industry_2_change_table()
    # create_code_is_st_change_table()
    # create_code_name_change_table()

    # create_index_stocks_399101_table()
    # create_temp_table()

    # create_qfq_daily_stock_price_sz_main_table()

    # create_adjust_factor_table()
    # create_stock_share_change_cninfo_table()

    # create_bfq_daily_stock_price_sz_main_table()

    # create_stock_listing_date_table()
    create_bfq_daily_etf_price_table()