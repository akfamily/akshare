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

STARTDAY="20230519"


def save_pe_to_mysql(symbol='证监会行业分类'):
    """查询行业行业分类的历史PE数据，并存入本地数据主函数（批量插入优化）"""
    """执行前先执行query_industry_pe_sequential接口确认从什么时间点开始查询"""
    try:
        # 建立PyMySQL连接（网页4标准连接方式）
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ 连接成功 | MySQL版本:", conn.get_server_info())
        conn.autocommit(False)  # 禁用自动提交
        
        with conn.cursor() as cursor:
            trade_days = get_trade_days(STARTDAY)
            pbar = tqdm(trade_days, desc="Processing Days")

            batch_size = 500  # 网页6推荐的批次大小
            total_data = []
            
            for day in pbar:
                try:
                    date_str = day.replace("-", "")
                    
                    # 获取PE数据（网页2接口）
                    pe_df = ak.stock_industry_pe_ratio_cninfo(
                        symbol=symbol,
                        date=date_str
                    )
                    
                    # 数据清洗
                    filtered_df = pe_df[['行业编码', '静态市盈率-加权平均',
                                       '静态市盈率-中位数', '静态市盈率-算术平均']].copy()
                    filtered_df['trade_date'] =  pd.to_datetime(day, errors='coerce')  # 强制日期转换

                    # 清除无效数据（网页8处理方案）
                    valid_df = filtered_df.dropna(subset=['trade_date'])
                    if valid_df.empty:
                        print(f"⚠️ 无效日期数据 {day}")
                        return
                    
                    # 生成批量数据（网页3数据格式转换）
                    batch_data = [
                        (row['trade_date'], row['行业编码'],
                         None if pd.isna(row['静态市盈率-加权平均']) else float(row['静态市盈率-加权平均']),
                         None if pd.isna(row['静态市盈率-中位数']) else float(row['静态市盈率-中位数']),
                         None if pd.isna(row['静态市盈率-算术平均']) else float(row['静态市盈率-算术平均'])
                         )
                        for _, row in filtered_df.iterrows()
                    ]
                    total_data.extend(batch_data)
                    
                    # 分批次全量处理
                    while len(total_data) >= batch_size:  # ✅ 循环处理所有完整分片
                        _execute_batch_insert(cursor, total_data[:batch_size])
                        conn.commit()  # 每批次提交
                        total_data = total_data[batch_size:]  # 动态更新剩余数据

                    pbar.set_postfix_str(f"Day {day} cached")
                    
                except MySQLError as e:
                    print(f"\nError processing {day}: {str(e)}")
                    conn.rollback()
                    continue
            
            # 插入剩余数据（网页6剩余数据处理）
            if total_data:
                _execute_batch_insert(cursor, total_data)
                conn.commit()
                
    except MySQLError as err:
        print(f"Database error: {err.code} {err.msg}")
    finally:
        if conn and conn.open:
            conn.close()
    return "INSERT finished!"

def _execute_batch_insert(cursor, data):
    """执行批量插入（网页1的executemany优化）"""
    insert_sql = """
    INSERT IGNORE INTO industry_pe_history 
    (trade_date, industry_code, pe_weighted, pe_median, pe_mean)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_sql, data)
    except MySQLError as e:
        if e.args[0] in (1062, 1586):  # 忽略主键冲突错误
            pass
        else:
            raise

def get_trade_days(startday="20230519"):
    """获取指定起始日至今的交易日历"""
    # 转换日期格式（网页6/7/8时间类型处理方案）
    start_date = pd.to_datetime(startday, format='%Y%m%d')  # 标准化输入日期
    end_date = pd.to_datetime(datetime.now() - timedelta(days=1))  # 统一时区
    
    # 获取原始交易日数据（网页1接口说明）
    df = ak.tool_trade_date_hist_sina()
    
    # 强制转换日期列类型（网页6兼容性处理）
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    
    # 日期范围过滤（网页7最佳实践）
    mask = (df['trade_date'] >= start_date) & (df['trade_date'] <= end_date)
    filtered_df = df.loc[mask, 'trade_date']
    
    # 转换为YYYYMMDD格式字符串列表（网页3数据格式需求）
    return [d.strftime('%Y%m%d') for d in filtered_df.dt.date.tolist()]

def query_industry_pe_sequential(date_list, symbol="证监会行业分类"):
    """
    按日期顺序查询行业PE数据，返回首个有效结果
    :param date_list: 日期列表(倒序排列，从最新到最旧)
    :param symbol: 市场类型，默认为"证监会行业分类"
    :return: (有效日期, DataFrame)
    """
    for date_str in tqdm(sorted(date_list, reverse=False), desc="日期查询进度"):
        try:
            # 转换日期格式（网页4日期规范）
            formatted_date = pd.to_datetime(date_str).strftime('%Y%m%d')
            
            # 调用接口（网页9接口调用规范）
            pe_df = ak.stock_industry_pe_ratio_cninfo(
                symbol=symbol,
                date=formatted_date
            )

            return (date_str, pe_df)
            
        except KeyError as e:
            if "'records'" in str(e):
                print(f"日期 {date_str} 无有效数据")
                continue
            else:
                raise
        except Exception as e:
            print(f"日期 {date_str} 无有效数据")
            continue
    
    return (None, None)


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
    
    #df = ak.stock_industry_pe_ratio_cninfo("证监会行业分类","20230519")
    #df = query_industry_pe_sequential(get_trade_days("20230501")) #从20230519开始有数据
  
    df = save_pe_to_mysql("证监会行业分类")
    print(df)
    