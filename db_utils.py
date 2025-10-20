#!/usr/bin/env python3
"""
db_utils.py

轻量 SQLite 工具：创建表、插入（insert or replace）日线数据。
使用标准库 sqlite3，避免必须依赖 SQLAlchemy，便于在各种环境中运行。
"""

import sqlite3
from typing import Iterable, List, Tuple


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS daily_ohlcv (
    ts_code TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    amount REAL,
    pre_close REAL,
    change_amount REAL,
    pct_chg REAL,
    turnover_rate REAL,
    PRIMARY KEY (ts_code, date)
);
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, isolation_level=None)  # autocommit mode
    conn.execute("PRAGMA journal_mode=WAL;")  # improve concurrency
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_TABLE_SQL)


def insert_rows(conn: sqlite3.Connection, rows: Iterable[Tuple]) -> None:
    """
    rows: iterable of tuples matching table columns:
    (ts_code, date, open, high, low, close, volume, amount, pre_close, change_amount, pct_chg, turnover_rate)
    Uses INSERT OR REPLACE to upsert.
    """
    sql = """
    INSERT OR REPLACE INTO daily_ohlcv
    (ts_code, date, open, high, low, close, volume, amount, pre_close, change_amount, pct_chg, turnover_rate)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur = conn.cursor()
    cur.executemany(sql, rows)
    cur.close()
