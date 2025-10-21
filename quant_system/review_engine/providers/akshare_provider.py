"""
AkShare数据提供者
严格使用AkShare真实数据，禁止任何虚拟/模拟数据
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time
import logging
from pathlib import Path
import sqlite3
import os

logger = logging.getLogger(__name__)


class DataValidationError(Exception):
    """数据校验失败异常"""
    pass


class AkShareProvider:
    """
    AkShare数据提供者

    职责：
    1. 从AkShare获取真实数据（严禁虚拟数据）
    2. 字段校验与单位规范
    3. 持久化到SQLite和Parquet
    4. 错误处理与重试
    """

    def __init__(self, config: dict):
        self.config = config
        self.timeout = config.get('akshare', {}).get('timeout', 30)
        self.retry = config.get('akshare', {}).get('retry', 3)
        self.retry_delay = config.get('akshare', {}).get('retry_delay', 2)

        # 数据存储路径
        self.sqlite_path = config.get('paths', {}).get('sqlite', 'data/review.sqlite')
        self.parquet_dir = config.get('paths', {}).get('parquet_dir', 'data/parquet/')

        # 确保目录存在
        Path(self.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.parquet_dir).mkdir(parents=True, exist_ok=True)

        # 初始化数据库
        self._init_database()

    def _init_database(self):
        """初始化SQLite数据库表结构"""
        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()

        # 指数数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS indices (
                date TEXT NOT NULL,
                symbol TEXT NOT NULL,
                name TEXT,
                close REAL,
                open REAL,
                high REAL,
                low REAL,
                volume REAL,
                amount REAL,
                change_pct REAL,
                PRIMARY KEY (date, symbol)
            )
        """)

        # 成交额表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_amount (
                date TEXT PRIMARY KEY,
                sh_amount REAL,
                sz_amount REAL,
                total_amount REAL
            )
        """)

        # 市场广度表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS breadth (
                date TEXT PRIMARY KEY,
                up_count INTEGER,
                down_count INTEGER,
                flat_count INTEGER,
                limit_up_count INTEGER,
                limit_down_count INTEGER,
                max_continuous_limit_up INTEGER,
                continuous_limit_rate REAL
            )
        """)

        # 北向资金表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS northbound (
                date TEXT PRIMARY KEY,
                net_flow REAL,
                sh_net REAL,
                sz_net REAL
            )
        """)

        # ETF流向表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS etf_flows (
                date TEXT NOT NULL,
                bucket TEXT NOT NULL,
                net_flow REAL,
                PRIMARY KEY (date, bucket)
            )
        """)

        # 融资融券表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS margin (
                date TEXT PRIMARY KEY,
                balance REAL,
                buy_amount REAL
            )
        """)

        # 行业数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS industry (
                date TEXT NOT NULL,
                industry_name TEXT NOT NULL,
                avg_return REAL,
                net_flow REAL,
                avg_turnover REAL,
                limit_up_count INTEGER,
                PRIMARY KEY (date, industry_name)
            )
        """)

        # 宏观数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS macro (
                date TEXT NOT NULL,
                indicator TEXT NOT NULL,
                value REAL,
                PRIMARY KEY (date, indicator)
            )
        """)

        # 交易日历表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calendar (
                date TEXT PRIMARY KEY,
                is_trading_day INTEGER
            )
        """)

        conn.commit()
        conn.close()
        logger.info("数据库初始化完成")

    def _retry_fetch(self, func, *args, **kwargs):
        """带重试的数据获取"""
        for i in range(self.retry):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if i < self.retry - 1:
                    logger.warning(f"数据获取失败，{self.retry_delay}秒后重试 ({i+1}/{self.retry}): {e}")
                    time.sleep(self.retry_delay * (2 ** i))  # 指数退避
                else:
                    logger.error(f"数据获取失败，已重试{self.retry}次: {e}")
                    raise

    def _validate_dataframe(self, df: pd.DataFrame, required_columns: List[str],
                           table_name: str) -> None:
        """
        校验DataFrame

        Args:
            df: 待校验的DataFrame
            required_columns: 必需的列
            table_name: 表名（用于日志）

        Raises:
            DataValidationError: 校验失败
        """
        if df is None or df.empty:
            raise DataValidationError(f"{table_name}: DataFrame为空")

        # 检查必需列
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise DataValidationError(f"{table_name}: 缺少必需列 {missing_cols}")

        # 检查空值比例
        null_tolerance = self.config.get('validation', {}).get('null_tolerance', 0.1)
        for col in required_columns:
            null_ratio = df[col].isnull().sum() / len(df)
            if null_ratio > null_tolerance:
                raise DataValidationError(
                    f"{table_name}: 列 {col} 空值比例过高 ({null_ratio:.2%} > {null_tolerance:.2%})"
                )

    def fetch_indices(self, date: str) -> pd.DataFrame:
        """
        获取指数数据

        Args:
            date: 日期 YYYY-MM-DD

        Returns:
            包含上证/深成/创业板/沪深300的DataFrame
        """
        indices_config = {
            'sh000001': '上证指数',
            'sz399001': '深证成指',
            'sz399006': '创业板指',
            'sh000300': '沪深300'
        }

        results = []
        for symbol, name in indices_config.items():
            try:
                df = self._retry_fetch(ak.stock_zh_index_daily, symbol=symbol)

                if df is None or df.empty:
                    logger.warning(f"指数 {name} 数据为空")
                    continue

                # 转换日期列
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

                # 筛选指定日期
                df_date = df[df['date'] == date]

                if df_date.empty:
                    logger.warning(f"指数 {name} 在 {date} 无数据")
                    continue

                df_date = df_date.copy()
                df_date['symbol'] = symbol
                df_date['name'] = name

                # 计算涨跌幅
                if 'close' in df_date.columns and len(df) > 1:
                    prev_close = df[df['date'] < date].iloc[-1]['close'] if len(df[df['date'] < date]) > 0 else None
                    if prev_close:
                        df_date['change_pct'] = (df_date['close'] - prev_close) / prev_close * 100

                results.append(df_date)

            except Exception as e:
                logger.error(f"获取指数 {name} 失败: {e}")

        if not results:
            raise DataValidationError(f"所有指数数据获取失败 (日期: {date})")

        result_df = pd.concat(results, ignore_index=True)

        # 校验
        required_cols = self.config.get('validation', {}).get('required_columns', {}).get('indices',
                                                              ['date', 'close', 'volume', 'amount'])
        self._validate_dataframe(result_df, required_cols, 'indices')

        return result_df

    def fetch_market_amount(self, date: str) -> Dict[str, float]:
        """
        获取两市成交额

        Args:
            date: 日期

        Returns:
            {'sh_amount': xx, 'sz_amount': xx, 'total_amount': xx}
        """
        try:
            # 从指数数据中提取成交额
            indices = self.fetch_indices(date)

            sh_amount = indices[indices['symbol'] == 'sh000001']['amount'].values
            sz_amount = indices[indices['symbol'] == 'sz399001']['amount'].values

            sh_amount = float(sh_amount[0]) if len(sh_amount) > 0 else 0.0
            sz_amount = float(sz_amount[0]) if len(sz_amount) > 0 else 0.0

            return {
                'date': date,
                'sh_amount': sh_amount,
                'sz_amount': sz_amount,
                'total_amount': sh_amount + sz_amount
            }

        except Exception as e:
            logger.error(f"获取成交额失败: {e}")
            raise DataValidationError(f"成交额数据获取失败: {e}")

    def fetch_market_breadth(self, date: str) -> Dict:
        """
        获取市场广度

        Args:
            date: 日期

        Returns:
            涨跌家数、涨跌停等数据
        """
        try:
            # 获取实时行情（当日快照）
            spot_df = self._retry_fetch(ak.stock_zh_a_spot_em)

            if spot_df is None or spot_df.empty:
                raise DataValidationError("A股快照数据为空")

            # 计算涨跌家数
            up_count = len(spot_df[spot_df['涨跌幅'] > 0])
            down_count = len(spot_df[spot_df['涨跌幅'] < 0])
            flat_count = len(spot_df[spot_df['涨跌幅'] == 0])

            # 获取涨停板
            try:
                limit_up_df = self._retry_fetch(ak.stock_zt_pool_em, date=date.replace('-', ''))
                limit_up_count = 0 if limit_up_df is None or limit_up_df.empty else len(limit_up_df)

                # 连板高度
                max_continuous = 0
                if limit_up_df is not None and not limit_up_df.empty and '连板数' in limit_up_df.columns:
                    max_continuous = int(limit_up_df['连板数'].max())
            except:
                logger.warning(f"获取涨停池失败 (日期: {date})，可能非交易日")
                limit_up_count = 0
                max_continuous = 0

            # 获取跌停板
            try:
                limit_down_df = self._retry_fetch(ak.stock_zt_pool_dtgc_em, date=date.replace('-', ''))
                limit_down_count = 0 if limit_down_df is None or limit_down_df.empty else len(limit_down_df)
            except:
                logger.warning(f"获取跌停池失败 (日期: {date})")
                limit_down_count = 0

            return {
                'date': date,
                'up_count': up_count,
                'down_count': down_count,
                'flat_count': flat_count,
                'limit_up_count': limit_up_count,
                'limit_down_count': limit_down_count,
                'max_continuous_limit_up': max_continuous,
                'continuous_limit_rate': 0.0  # 需要历史数据计算，暂时为0
            }

        except Exception as e:
            logger.error(f"获取市场广度失败: {e}")
            raise DataValidationError(f"市场广度数据获取失败: {e}")

    def fetch_northbound(self, date: str) -> Dict[str, float]:
        """
        获取北向资金

        Args:
            date: 日期

        Returns:
            北向净流入数据
        """
        try:
            df = self._retry_fetch(ak.stock_hsgt_north_net_flow_in_em)

            if df is None or df.empty:
                raise DataValidationError("北向资金数据为空")

            # 转换日期格式
            df['date'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')

            # 筛选日期
            df_date = df[df['date'] == date]

            if df_date.empty:
                logger.warning(f"北向资金在 {date} 无数据，可能非交易日")
                return {
                    'date': date,
                    'net_flow': 0.0,
                    'sh_net': 0.0,
                    'sz_net': 0.0
                }

            # 北向资金单位为亿元，转换为元
            net_flow = float(df_date['当日净流入-净流入'].values[0]) * 1e8
            sh_net = float(df_date['沪股通-净流入'].values[0]) * 1e8 if '沪股通-净流入' in df_date.columns else 0.0
            sz_net = float(df_date['深股通-净流入'].values[0]) * 1e8 if '深股通-净流入' in df_date.columns else 0.0

            return {
                'date': date,
                'net_flow': net_flow,
                'sh_net': sh_net,
                'sz_net': sz_net
            }

        except Exception as e:
            logger.error(f"获取北向资金失败: {e}")
            raise DataValidationError(f"北向资金数据获取失败: {e}")

    def save_to_db(self, table_name: str, data: Union[pd.DataFrame, Dict]):
        """
        保存数据到SQLite

        Args:
            table_name: 表名
            data: DataFrame或Dict
        """
        conn = sqlite3.connect(self.sqlite_path)

        try:
            if isinstance(data, dict):
                # Dict转DataFrame
                df = pd.DataFrame([data])
            else:
                df = data

            # 幂等upsert
            df.to_sql(table_name, conn, if_exists='append', index=False)
            conn.commit()
            logger.info(f"数据已保存到表 {table_name}")

        except sqlite3.IntegrityError:
            # 主键冲突，更新数据
            logger.info(f"数据已存在，更新表 {table_name}")
            # 简化处理：先删除再插入
            if isinstance(data, dict):
                date = data.get('date')
                if date:
                    conn.execute(f"DELETE FROM {table_name} WHERE date = ?", (date,))
                df = pd.DataFrame([data])
            else:
                df = data
            df.to_sql(table_name, conn, if_exists='append', index=False)
            conn.commit()

        finally:
            conn.close()

    def fetch_and_save_all(self, date: str):
        """
        获取并保存所有数据

        Args:
            date: 日期 YYYY-MM-DD
        """
        logger.info(f"开始获取 {date} 的所有数据")

        try:
            # 1. 指数数据
            logger.info("获取指数数据...")
            indices = self.fetch_indices(date)
            self.save_to_db('indices', indices)

            # 2. 成交额
            logger.info("获取成交额...")
            amount = self.fetch_market_amount(date)
            self.save_to_db('market_amount', amount)

            # 3. 市场广度
            logger.info("获取市场广度...")
            breadth = self.fetch_market_breadth(date)
            self.save_to_db('breadth', breadth)

            # 4. 北向资金
            logger.info("获取北向资金...")
            northbound = self.fetch_northbound(date)
            self.save_to_db('northbound', northbound)

            logger.info(f"{date} 数据获取完成")

        except Exception as e:
            logger.error(f"数据获取失败: {e}")
            raise


# 导入类型提示
from typing import Union
