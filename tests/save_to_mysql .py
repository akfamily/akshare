import akshare as ak
import pandas as pd
import pymysql
from datetime import datetime,timedelta
from tqdm import tqdm
from pymysql import MySQLError




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
        # 生成批量数据（需要根据具体存储表来修改代码）
        batch_data = [
                        (row['指数代码'],row['指数名称'],row['日期'],row['指数'], 
                         None if pd.isna(row['等权静态市盈率']) else float(row['等权静态市盈率']),
                         None if pd.isna(row['静态市盈率']) else float(row['静态市盈率']),
                         None if pd.isna(row['静态市盈率中位数']) else float(row['静态市盈率中位数']),                         
                         None if pd.isna(row['等权滚动市盈率']) else float(row['等权滚动市盈率']),
                         None if pd.isna(row['滚动市盈率']) else float(row['滚动市盈率']),
                         None if pd.isna(row['滚动市盈率中位数']) else float(row['滚动市盈率中位数']))
                        for _, row in datapd.iterrows()
                    ]
        # 建立PyMySQL连接（网页4标准连接方式）
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ 连接成功 | MySQL版本:", conn.get_server_info())
        conn.autocommit(False)  # 禁用自动提交
        batch_size = 500  # 网页6推荐的批次大小

        with conn.cursor() as cursor:
            # 分批次全量处理
            while len(batch_data) >= batch_size:  # ✅ 循环处理所有完整分片
                        _execute_batch_insert(cursor, batch_data[:batch_size])
                        conn.commit()  # 每批次提交
                        batch_data = batch_data[batch_size:]  # 动态更新剩余数据
       
            # 插入剩余数据（网页6剩余数据处理）
            if batch_data:
                _execute_batch_insert(cursor, batch_data)
                conn.commit()
                
    except MySQLError as err:
        print(f"Database error: {err.code} {err.msg}")
    finally:
        if conn and conn.open:
            conn.close()

def _execute_batch_insert(cursor, data,insert_sql):
    """执行批量插入（需要根据具体存储表来修改代码）"""
    #insert_sql = """
    #INSERT INTO `index_valuation_history` 
    #(`index_code`, `index_name`, `trade_date`, `index_value`, 
    #`pe_equal_weight_static`, `pe_static`, `pe_static_median`,
    # `pe_equal_weight_ttm`, `pe_ttm`, `pe_ttm_median`)
    #VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #"""
    try:
        cursor.executemany(insert_sql, data)
    except MySQLError as e:
        if e.args[0] in (1062, 1586):  # 忽略主键冲突错误
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
    #df = insert_to_mysql(df)
    