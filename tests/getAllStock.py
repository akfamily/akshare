import os
import pandas as pd
from pathlib import Path
import akshare as ak
import time
from datetime import datetime,timedelta
from tqdm import tqdm
from pandas.core.frame import DataFrame
import xlsxwriter

# 注意将列表excel以下列名字放在py文件相同目录下
SH_PATH=r"..\input\shanghailist.xlsx"
SZ_PATH=r"..\input\shenzhenlist.xlsx"
SELECT_PATH=r"..\input\selectlist.xlsx"
IPOTIMEFILTER="20220522"

def get_all_stocks(sh_path=SH_PATH, sz_path=SZ_PATH) -> pd.DataFrame:
    """
    读取沪深股票列表，返回标准化代码与简称
    :param sh_path: 上交所文件路径
    :param sz_path: 深交所文件路径
    :return: DataFrame(代码, 名称)
    """
    # 读取上海数据[1,3](@ref)
    sh_cols = {'A股代码':'代码', '证券简称':'名称','上市日期':'上市日期'}
    base_path = Path(__file__).parent
    sh_df = pd.read_excel(
        base_path / sh_path,
        usecols=list(sh_cols.keys()),
        dtype={'A股代码': str}
    ).rename(columns=sh_cols)
    sh_df = sh_df[sh_df['代码'].notna()]  # 过滤无A股代码的记录
    sh_df['上市日期']= pd.to_datetime(sh_df['上市日期'], format='%Y%m%d', errors='coerce')

    # 读取深圳数据[2,4](@ref)
    sz_cols = {'A股代码':'代码', 'A股简称':'名称','A股上市日期':'上市日期'}
    sz_df = pd.read_excel(
        base_path / sz_path,
        usecols=list(sz_cols.keys()),
        dtype={'A股代码': str}
    ).rename(columns=sz_cols)
    sz_df = sz_df[sz_df['代码'].notna()]
    sz_df['上市日期']= pd.to_datetime(sz_df['上市日期'], format='%Y-%m-%d', errors='coerce')


    # 合并数据集[1,3,5](@ref)
    merged_df = pd.concat([sh_df, sz_df], ignore_index=True)
    
    # 数据清洗
    merged_df.drop_duplicates(subset=['代码'], keep='first', inplace=True)
    merged_df.sort_values(by='代码', inplace=True)
    
    return merged_df[['代码', '名称','上市日期']]

def get_select_stocks(select_path=SELECT_PATH) -> pd.DataFrame:
    """
    读取特定选中股票列表，返回标准化代码与简称
    :param SELECT_PATH: 选中股票文件路径
    :return: DataFrame(代码, 名称)
    """
    # 读取上海数据[1,3](@ref)
    se_cols = {'A股代码':'代码', '证券简称':'名称'}
    base_path = Path(__file__).parent
    se_df = pd.read_excel(
        base_path / select_path,
        usecols=list(se_cols.keys()),
        dtype={'A股代码': str}
    ).rename(columns=se_cols)
    se_df = se_df[se_df['代码'].notna()]  # 过滤无A股代码的记录


    # 数据清洗
    se_df.drop_duplicates(subset=['代码'], keep='first', inplace=True)
    se_df.sort_values(by='代码', inplace=True)
    
    return se_df[['代码', '名称']]

def filter_stocks(df, start_date):
    """
    通过Akshare接口筛选在指定日期前上市且有历史股价的股票
    
    参数：
        df : DataFrame，包含股票代码列（列名为'symbol'或'code'）
        start_date : str，格式为'YYYYMMDD'，筛选起始日期
    
    返回：
        valid_stocks : 在原有df中增加"上市日期"符合条件的df
    """
    #1. 获取代码列表      
    if '代码' in df.columns:
        symbols = df['代码'].tolist()
    elif 'code' in df.columns:
        symbols = df['code'].tolist()
    else:
        raise ValueError("输入DataFrame需包含'代码'或'code'列")
    valid_stocks = []
    start_dt = datetime.strptime(start_date, "%Y%m%d")

    total_symbols = len(symbols)
            
    with tqdm(total=total_symbols, desc='获取上市时间', unit='标的') as pbar:
        # 2. 遍历股票代码，获取上市日期并验证历史数据
        for symbol in symbols:
            try:
                # 获取上市日期
                info_df = ak.stock_individual_info_em(symbol=symbol.split('.')[0])
                list_date = info_df[info_df['item'] == '上市时间']['value'].values[0]
                symbolname = info_df[info_df['item'] == '股票简称']['value'].values[0]
                list_date_str = str(list_date)
                list_dt = datetime.strptime(list_date_str, "%Y%m%d")
            
                # 判断是否在起始日期前上市
                if list_dt > start_dt:
                    continue
             
                valid_stocks.append([symbol,symbolname])
                pbar.update(1)
                time.sleep(0.5)

            except Exception as e:
                print(f"股票 {symbol} 数据处理失败: {str(e)}")
                continue
    return valid_stocks

def ipodatefilter_stocks(df, start_date):
    """
    通过列表中的信息筛选在指定日期前上市且有历史股价的股票
    
    参数：
        df : DataFrame，包含列名'代码'和'上市时间'）
        start_date : str，格式为'YYYYMMDD'，筛选起始日期
    
    返回：
        valid_stocks : 符合条件的df
    """
    # 1. 检查必需列是否存在（修复unhashable type错误）
    required_cols = ['代码','名称', '上市日期']
    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        raise ValueError(f"输入DataFrame缺少必需列: {missing}")

    # 2. 转换日期格式并筛选
    start_dt = pd.to_datetime(start_date, format="%Y%m%d")

    # 3. 将上市日期列转换为datetime类型[3,5,6](@ref)
    df['上市日期'] = pd.to_datetime(df['上市日期'], format="%Y%m%d", errors='coerce')
    
    # 4. 筛选符合条件的股票
    valid_stocks = df[df['上市日期']<start_dt].copy()
        
    return valid_stocks

# 使用示例
if __name__ == "__main__":
    df = get_all_stocks()
    filterlist = ipodatefilter_stocks(df,IPOTIMEFILTER)
    print(filterlist)
    #Excel写入
    end_date = datetime.now().strftime("%Y%m%d")
    writer = pd.ExcelWriter(f".\output\stocksfilter_{end_date}.xlsx", engine='xlsxwriter')
    filterlist.to_excel(writer, index=False, sheet_name=f'按{IPOTIMEFILTER}上市时间过滤')       
    writer.close()

    #print(df)
    #print(df1)