import time
import numpy as np
import akshare as ak
import pandas as pd
import datetime
from tqdm import tqdm
from getAllStock import get_all_stocks


def selectStock():
    ## A 股上市公司列表
    stock_zh_a_spot_df = get_all_stocks()
    #print(stock_zh_a_spot_df)
    df_stock = stock_zh_a_spot_df[['代码','名称']]
     # 分块处理设置[2,3](@ref)
    total_rows = len(df_stock)
    chunk_num = 10
    chunk_indices = np.array_split(np.arange(total_rows), chunk_num)

    # 分批处理逻辑
    for file_num, chunk_idx in enumerate(chunk_indices):
        chunk_df = df_stock.iloc[chunk_idx]
        df_result = pd.DataFrame(columns=['stock','name','指标1','指标2','指标3','指标4','综合评估'])
        
        # 处理单个数据块
        for row_index, row in tqdm(chunk_df.iterrows(), total=len(chunk_df), desc=f"处理第{file_num+1}批"):
            try:
                r_code = row['代码']
                r_name = row['名称']
                
                # 指标计算
                var1, var2, var3 = checkRoeCashEBIT(r_code, "2019")
                var4 = check_pe_condition(r_code)
                varAll = var1 and var2 and var3 and var4
                
                # 结果存储
                df_result.loc[row_index] = {
                    'stock': r_code,
                    'name': r_name,
                    '指标1': var1,
                    '指标2': var2,
                    '指标3': var3,
                    '指标4': var4,
                    '综合评估': varAll
                }
                time.sleep(1.5)
                
            except Exception as e:
                print(f"处理{row['代码']}时出错：{str(e)}")
                continue
        
        # 分块存储[1,5](@ref)
        df_result.to_excel(f'.\output\stock_result_{file_num}.xlsx', index=False)
        print(f"第{file_num+1}批数据已存储，包含{len(df_result)}条记录")
    
    return "所有分块处理完成"

def checkRoeCashEBIT(r_code = "601398",startyear = "2019"):
    #财务指标数据 工行财报
    df = ak.stock_financial_analysis_indicator(r_code,startyear)
    # print(df.head())
    clean_df = df.copy()

    # 数据清洗
    # 日期转换与格式校验
    clean_df['日期'] = pd.to_datetime(
        clean_df['日期'],
        errors='coerce'  # 无效日期转为NaT（网页[2]建议）
        )
    # 筛选有效年报
    year_end_mask = (
        (clean_df['日期'].dt.month == 12) & 
        (clean_df['日期'].dt.day == 31) & 
        (clean_df['日期'].notna())
        )
    clean_df = clean_df[year_end_mask]

    # 按年排序与截取
    clean_df = clean_df.sort_values('日期', ascending=False)
    
    clean_df = clean_df.set_index(clean_df['日期'])

    #指标1 - 过去5年来平均净资产收益率高于14%
    df1 = clean_df['净资产收益率(%)']
    df1_sum = df1.replace('--',0).astype(float).sum(axis = 0, skipna = True)
    df1_count = df1.count()
    var1 = (df1_sum / df1_count)>14

    #指标2：经营现金流为正
    df2=clean_df['每股经营性现金流(元)']
    var2 = float( df2.iat[0] ) > 0

    
    #指标3：新期的净利润大于前5年的净利润 取万元 
    clean_df['扣非净利润'] = (
        pd.to_numeric(clean_df['扣除非经常性损益后的净利润(元)'], errors='coerce')
        .div(10000)  # 元转万元
        .dropna()     # 过滤无效数据
    )
    df3=clean_df['扣非净利润']

    # 获取最新一期数据
    latest = df3.iloc[0]  # 索引0为最新数据

    # 获取前五年数据（索引1-5为前1至前5年）
    past_5years = df3.iloc[1:6]  # 含1不含6

    # 计算逻辑
    var3 = latest > past_5years.max() 

    return var1,var2,var3

## 指标2- 市盈率低于30且大于0
def check_pe_condition(stock_code="601398", pastday = 30):
    # 获取最新接口数据（网页[2]接口变更）
    try:
        df = ak.stock_a_indicator_lg(symbol=stock_code)
    except Exception as e:
        print(f"接口调用失败: {str(e)}")
        return False
    
    # 日期处理优化（网页[3]数据格式）
    date_threshold = datetime.datetime.now() - datetime.timedelta(pastday)
    date_threshold = date_threshold.date()  # 转换为日期对象
    
    # 数据清洗与计算（网页[1]字段说明）
    valid_df = df[
        (pd.to_datetime(df['trade_date']).dt.date > date_threshold) 
        & (df['pe'].notna())
    ]
    
    if valid_df.empty:
        #print("无近期有效数据")
        return "NAN"
        
    pe_mean = valid_df['pe'].mean()
    var2 = 0 < pe_mean < 30
    return var2


if __name__ == "__main__":
    df = selectStock()
    #导出Excel并自动调整列宽[4](@ref)
    #with pd.ExcelWriter(".\output\output.xlsx") as writer:
    #    df.to_excel(writer, sheet_name="全量数据")
    #selectStock()