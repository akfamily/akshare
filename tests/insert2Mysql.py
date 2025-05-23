import akshare as ak
import pandas as pd
import pymysql
from pymysql import MySQLError
from datetime import datetime,timedelta
from tqdm import tqdm
import log4ak
import logging

log = log4ak.LogManager(log_level=logging.INFO)

# 数据库配置（适配PyMySQL参数）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'powerbi',
    'password': 'longyu',
    'database': 'akshare',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}



def insert_to_mysql(datapd, insertSqlStr):
    """存入本地数据主函数（批量插入优化）"""
    """需要根据具体存储表来修改代码"""
    try:

        # 建立PyMySQL连接（网页4标准连接方式）
        conn = pymysql.connect(**DB_CONFIG)
        log.debug(f"数据库相关信息：{DB_CONFIG}")
        #print("✅ 连接成功 | MySQL版本:", conn.get_server_info())
        log.info(f"✅ 连接成功 | MySQL版本:{conn.get_server_info()}")

        conn.autocommit(False)  # 禁用自动提交
        batch_size = 500  # 网页6推荐的批次大小
        log.debug(f"batch_size = {batch_size}")

        with conn.cursor() as cursor:
            # 分批次全量处理
            while len(datapd) >= batch_size:  # ✅ 循环处理所有完整分片
                        _execute_batch_insert(cursor, datapd[:batch_size],insertSqlStr)
                        conn.commit()  # 每批次提交
                        datapd = datapd[batch_size:]  # 动态更新剩余数据
       
            # 插入剩余数据（网页6剩余数据处理）
            if datapd:
                _execute_batch_insert(cursor, datapd,insertSqlStr)
                conn.commit()
            log.info("insert finished!")
            return "insert finished!"
                
    except MySQLError as err:
        log.error(f"Database error: {err.code} {err.msg}")
    finally:
        if conn and conn.open:
            conn.close()

def _execute_batch_insert(cursor, data,insert_sql):
    """执行批量插入（需要根据具体存储表来修改代码）"""
    #insert_sql = """
    #INSERT IGNORE INTO `index_valuation_history` 
    #(`index_code`, `index_name`, `trade_date`, `index_value`, 
    #`pe_equal_weight_static`, `pe_static`, `pe_static_median`,
    # `pe_equal_weight_ttm`, `pe_ttm`, `pe_ttm_median`)
    #VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    #"""
    try:
        log.debug(f"insert data：{data}")
        log.debug(f"insert Sql：{insert_sql}")
        cursor.executemany(insert_sql, data)
    except MySQLError as e:
        if e.args[0] in (1062, 1586):  # 忽略主键冲突错误
            log.debug(f"错误码({e.args[0]})，出现主键冲突，已忽略。{e}")
            pass
        else:
            raise




def insert_batch_insert(data):
    try:
        # 建立PyMySQL连接（网页4标准连接方式）
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ 连接成功 | MySQL版本:", conn.get_server_info())
        conn.autocommit(False)  # 禁用自动提交

        with conn.cursor() as cursor:
            _execute_batch_insert(cursor, data)
            conn.commit()
            print(f"✅ 插入成功 |{data} ")
    except MySQLError as e:
        if e.args[0] in (1062, 1586):  # 忽略主键冲突错误
            pass
        else:
            print(f"Database error: {err.code} {err.msg}")
            raise
    finally:
        if conn and conn.open:
            conn.close()

if __name__ == "__main__":
    df = ak.stock_index_pe_lg('中证1000')
    df["指数代码"]="000852.SH"
    df["指数名称"]="中证1000"
    print(df)
    #df = insert_to_mysql(df)
    