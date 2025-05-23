import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import xlsxwriter
from datetime import datetime


# 分块读取优化内存（网页10）
def fetch_data_chunks():
    engine = create_engine('mysql+pymysql://powerbi:longyu@localhost:3306/akshare')
    chunksize = 50000
    
    # 按股票代码分块读取
    stock_codes = pd.read_sql("SELECT DISTINCT stock_code FROM stock_pe_history", engine)['stock_code']
    for code_chunk in np.array_split(stock_codes, len(stock_codes)//100):
        query = f"""
            SELECT * 
            FROM stock_pe_history 
            WHERE stock_code IN ({','.join([f"'{c}'" for c in code_chunk])})
            AND pe_ttm IS NOT NULL
            ORDER BY stock_code, trade_date DESC
        """
        yield pd.read_sql(query, engine)

def calculate_percentiles(chunk):
    """基于完整历史数据计算百分位"""
    # 构建时间窗口
    chunk['trade_date'] = pd.to_datetime(chunk['trade_date'])
    
    # 计算滚动百分位（最近3年数据）
    result = []
    for code, group in chunk.groupby('stock_code'):
        # 按时间排序
        sorted_group = group.sort_values('trade_date', ascending=False)
        
        # 计算最新记录的百分位（使用全部历史数据）
        latest_record = sorted_group.iloc[0].copy()
        latest_record['time_percentile'] = (
            (sorted_group['pe_ttm'] >= latest_record['pe_ttm']).mean() * 100
        )
        result.append(latest_record)
    
    return pd.DataFrame(result)

# 并行处理数据块（网页11）
from multiprocessing import Pool

def parallel_processing():
    with Pool(4) as pool:  # 4个进程
        results = []
        for chunk in fetch_data_chunks():
            results.append(pool.apply_async(calculate_percentiles, (chunk,)))
        
        return pd.concat([res.get() for res in results])

def save_to_excel(df):
    """优化Excel写入（网页10）"""
    end_date = datetime.now().strftime("%Y%m%d")
    writer = pd.ExcelWriter(f'.\output\stock_percentiles_{end_date}.xlsx', engine='xlsxwriter')
    
    # 格式设置
    format_dict = {
        'pe_ttm': '0.00',
        'time_percentile': '0.00%'  # 百分比格式（网页6）
    }
    
    df.to_excel(writer, index=False, sheet_name='最新PE百分位')
    
    # 应用格式
    workbook = writer.book
    worksheet = writer.sheets['最新PE百分位']
    for col_num, (col_name, fmt) in enumerate(format_dict.items()):
        col_idx = df.columns.get_loc(col_name)
        fmt = workbook.add_format({'num_format': fmt})
        worksheet.set_column(col_num, col_num, 15, fmt)
    
    writer.close()

if __name__ == '__main__':

    # 步骤1：并行计算
    result_df = parallel_processing()
    
    # 步骤2：合并结果
    final_df = result_df.groupby('stock_code').last().reset_index()
    
    # 步骤3：存储优化
    save_to_excel(final_df)