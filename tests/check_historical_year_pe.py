import akshare as ak
import numpy as np
import pandas as pd
from datetime import datetime


def get_historical_year_pe(stock_code, start_year="2020"):
    """获取历史年度市盈率(单位：亿元)"""

    # 获取年度净利润[6](@ref)
    income_df = get_historical_year_income(stock_code, start_year);
    #print(income_df)

    # 获取年度总股本[6](@ref)
    balance_df = get_historical_year_shares(stock_code, start_year)
    #print(balance_df)

    # 获取最后交易日股价[6](@ref)
    #price_df = get_annual_lastday_prices(stock_code, start_year)
    #print(price_df)
    
    # 获取年日均股价[6](@ref)
    price_df = get_annual_price_stats(stock_code, start_year)[['年份','日均价']]
    #print(price_df)
    
    # ================== 数据合并 ==================
    # 合并数据集
    merged_df = pd.merge(income_df, balance_df, on='年份', how='outer')
    merged_df = pd.merge(merged_df, price_df, on='年份', how='outer')
    
    # ================== PE计算 ==================
    # 计算年度PE
    merged_df['总市值'] = merged_df['总股本'] * merged_df['日均价']
    merged_df['总市值'] = merged_df['总市值'].round().astype(int)
    merged_df['PE'] = np.where(merged_df['净利润'] > 0,
                              round(merged_df['总市值'] / merged_df['净利润'],2),
                              np.nan)
    
    # ================== 数据清洗 ==================
    return merged_df[['年份', '净利润', '总股本', '日均价', 'PE']].sort_values('年份').reset_index(drop=True)


def get_historical_year_income(stock_code, start_year="2020"):
    """获取指定年份及之后的年度净利润数据"""
    # ================== 1. 获取并清洗财务数据 ==================
    try:
        # 获取利润表数据（网页1、网页8方法）
        income_df = ak.stock_financial_report_sina(stock=stock_code, symbol="利润表")
        
        # 筛选年报数据并提取年份（网页1）
        income_df = income_df[income_df['报告日'].str.endswith('1231', na=False)].copy()
        income_df['年份'] = pd.to_datetime(income_df['报告日']).dt.year
        
        # 转换金额单位（网页1处理逻辑）
        #income_df['净利润'] = income_df['净利润'].str.replace('亿', '').astype(float)
        
        # 按年份筛选（新增核心逻辑）
        filtered_df = income_df[income_df['年份'] >= int(start_year)]
        filtered_df.loc[:, '净利润'] = filtered_df['净利润'].round().astype(int)
        
        return filtered_df[['年份', '净利润']].reset_index(drop=True)
    
    except Exception as e:
        print(f"数据利润获取失败: {str(e)}")
        return pd.DataFrame(columns=['年份', '净利润'])

def get_historical_year_shares(stock_code, start_year="2020"):
    """通过年报获取历史总股本数据"""
    try:
        # 获取资产负债表（网页7方法）
        balance_df = ak.stock_financial_report_sina(stock_code, symbol="资产负债表")
        
        # 筛选年报数据（网页1、网页7逻辑）
        balance_df = balance_df[balance_df['报告日'].str.contains('1231')].copy()
        balance_df['年份'] = pd.to_datetime(balance_df['报告日']).dt.year
        
        # 按年份筛选（新增核心逻辑）
        filtered_df = balance_df[balance_df['年份'] >= int(start_year)]
        filtered_df = filtered_df.rename(columns={
            '实收资本(或股本)': '总股本'
            })[['年份', '总股本']]
        filtered_df.loc[:, '总股本'] = filtered_df['总股本'].round().astype(int)

        return filtered_df[['年份', '总股本']].reset_index(drop=True)
    
    except Exception as e:
        print(f"数据利润获取失败: {str(e)}")
        return pd.DataFrame(columns=['年份', '净利润'])

def get_annual_lastday_prices(stock_code, start_year="2020", adjust="qfq"):
    """
    高效获取每年最后一个交易日收盘价
    :param stock_code: 股票代码，如 '600519'
    :param start_year: 起始年份，如 2010
    :param adjust: 复权方式，默认前复权(qfq)
    """
    current_year = datetime.now().year
    results = []
    
    for year in range(start_year, current_year + 1):
        # 构造每年最后一周的查询范围(网页6参数规范)
        end_date = f"{year}1231"
        start_date = f"{year}1225"  # 查询最后一周数据
        
        try:
            # 仅获取年末最后一周数据(网页7接口调用优化)
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )
            
            if not df.empty:
                # 直接取最后一条有效数据(网页5数据处理逻辑)
                last_row = df.iloc[-1]
                results.append({
                    '年份': year,
                    '收盘价': last_row['收盘'],
                    '最后交易日': last_row['日期']
                })
        except Exception as e:
            print(f"{year}年数据异常: {str(e)}")
    
    return pd.DataFrame(results)

def get_annual_price_stats(stock_code, start_year="2020", adjust="qfq"):
    """
    获取股票历史年度价格统计（最高价、最低价、日均价）
    :param stock_code: 股票代码，如 '600519'
    :param start_year: 起始年份，如 2010
    :param adjust: 复权方式，默认前复权(qfq)
    :return: DataFrame with columns ['年份', '最高价', '最低价', '日均价', '交易天数']
    """
    current_year = datetime.now().year
    results = []
    
    for year in range(int(start_year), current_year):
        # 构造全年查询范围
        start_date = f"{year}0101"
        end_date = f"{year}1231"
        
        try:
            # 获取全年日线数据（网页7接口调用优化）
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )
            
            if not df.empty:
                # 计算年度统计指标（网页5数据处理逻辑）
                results.append({
                    '年份': year,
                    '最高价': df['收盘'].max(),
                    '最低价': df['收盘'].min(),
                    '收盘价': df.iloc[-1]['收盘'],
                    '日均价': round(df['收盘'].mean(),2),                    
                    '交易天数': len(df),
                    '首交易日': df.iloc[0]['日期'],
                    '末交易日': df.iloc[-1]['日期']
                })
            else:
                print(f"{year}年无有效交易数据")
                
        except Exception as e:
            print(f"{year}年数据异常: {str(e)}")
            continue
    
    return pd.DataFrame(results).sort_values('年份', ascending=False)

def df_to_excel(df):
    # 导出CSV查看[3](@ref)
    df.to_csv("full_columns.csv", index=False)

    # 导出Excel并自动调整列宽[4](@ref)
    with pd.ExcelWriter("output.xlsx") as writer:
        df.to_excel(writer, sheet_name="全量数据")
        worksheet = writer.sheets["全量数据"]
        for idx, col in enumerate(df.columns):
            worksheet.set_column(idx, idx, 20)  # 设置列宽为20字符
    return 


if __name__ == "__main__":
    df_pe=get_historical_year_pe("002555","2020")
    print(df_pe)