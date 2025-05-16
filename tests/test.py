import akshare as ak
import pandas as pd
import pymysql
from datetime import datetime,timedelta
from tqdm import tqdm
from pymysql import MySQLError

INDICES = {
        "上证50": "000016.SH",
        "沪深300": "000300.SH",
        "上证380": "000009.SH",
        "创业板50": "399673.SZ",
        #"中证500": "000905.SH",
        #"上证180": "000010.SH",
        #"深证红利": "399324.SZ",
        #"深证100": "399330.SZ",
        #"中证1000": "000852.SH",
        #"上证红利": "000015.SH",
        #"中证100": "000903.SH",
        #"中证800": "000906.SH"
               }

def insert_major_index_valuation():
    """获取三大指数估值数据"""
    
    for name,code in tqdm(indices.items(),desc=f"获取{indices.items()}估值……"):
        try:
            # 获取基础估值数据[5,9](@ref)
            df = ak.stock_index_pe_lg(name)
            df["指数代码"]=code
            df["指数名称"]=name

            # 生成批量数据（需要根据具体存储表来修改代码）
            batch_data = [
                        (row['指数代码'],row['指数名称'],row['日期'],row['指数'], 
                         None if pd.isna(row['等权静态市盈率']) else float(row['等权静态市盈率']),
                         None if pd.isna(row['静态市盈率']) else float(row['静态市盈率']),
                         None if pd.isna(row['静态市盈率中位数']) else float(row['静态市盈率中位数']),                         
                         None if pd.isna(row['等权滚动市盈率']) else float(row['等权滚动市盈率']),
                         None if pd.isna(row['滚动市盈率']) else float(row['滚动市盈率']),
                         None if pd.isna(row['滚动市盈率中位数']) else float(row['滚动市盈率中位数']))
                        for _, row in df.iterrows()
                        ]
            insert_to_mysql(batch_data,INSERT_SQL)
        except Exception as e:
            print(f"{name} 数据存储失败: {str(e)}")
    
    return "INSERT finished!"

def insert_to_mysql(batch_data, insertSqlStr):
    """存入本地数据主函数（批量插入优化）"""
    """需要根据具体存储表来修改代码"""
    try:
        # 建立PyMySQL连接（网页4标准连接方式）
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ 连接成功 | MySQL版本:", conn.get_server_info())
        conn.autocommit(False)  # 禁用自动提交
        batch_size = 500  # 网页6推荐的批次大小

        with conn.cursor() as cursor:
            # 分批次全量处理
            while len(batch_data) >= batch_size:  # ✅ 循环处理所有完整分片
                        _execute_batch_insert(cursor, batch_data[:batch_size],insertSqlStr)
                        conn.commit()  # 每批次提交
                        batch_data = batch_data[batch_size:]  # 动态更新剩余数据
       
            # 插入剩余数据（网页6剩余数据处理）
            if batch_data:
                _execute_batch_insert(cursor, batch_data,insertSqlStr)
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

if __name__ == "__main__":
    # 使用示例
    print(INDICES.kyes())