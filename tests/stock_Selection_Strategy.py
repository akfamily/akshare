import akshare as ak
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

def check_revenue_decline(code):
    """检查季度收入连续3次环比下滑且年均下滑超-10%"""
    try:
        # 获取利润表数据（网页7接口）
        df = ak.stock_financial_benefit_ths(symbol=code)
        df = df[['报表日期', '营业收入']].sort_values('报表日期', ascending=False)
        
        # 计算季度环比增长率
        df['QoQ'] = df['营业收入'].pct_change(periods=-1) * 100  # 上季度的环比
        recent_qoq = df['QoQ'].head(3).tolist()
        
        # 条件验证（网页7财务分析逻辑）
        if len(recent_qoq) <3: return False
        if all(x <0 for x in recent_qoq):  # 连续3季下滑
            annual_decline = np.mean(recent_qoq)  # 年均下滑率
            return annual_decline <= -10
        return False
    except:
        return False

def check_pe_percentile(code):
    """检查当前PE处于5年历史20%分位以下"""
    try:
        # 获取历史PE数据（网页6方法）
        df = ak.stock_financial_analysis_indicator(symbol=code)
        df = df[['日期', '市盈率(PE)']].dropna()
        df['日期'] = pd.to_datetime(df['日期'])
        df = df[df['日期'] >= pd.Timestamp.now() - pd.DateOffset(years=5)]
        
        if len(df) < 4: return False  # 数据不足
        current_pe = df.iloc[0]['市盈率(PE)']
        percentile_20 = np.percentile(df['市盈率(PE)'].values, 20)
        return current_pe <= percentile_20
    except:
        return False

def get_industry_metrics(code):
    """获取行业3年PE/PB/PS/PC分位数"""
    try:
        # 获取行业分类（网页3申万行业）
        industry_df = ak.sw_index_spot()
        industry_code = industry_df[industry_df['成分股代码'].str.contains(code)]['指数代码'].values[0]
        
        # 获取行业成分股（网页3方法）
        industry_stocks = ak.sw_index_cons(index_code=industry_code)['成分股代码'].tolist()
        
        # 收集行业指标（网页9估值方法）
        metrics = []
        for stock in tqdm(industry_stocks, desc="行业数据采集"):
            try:
                # 获取PE/PB/PS/PC（市现率=市值/经营现金流）
                df = ak.stock_financial_analysis_indicator(symbol=stock)
                cash_flow = ak.stock_financial_cash_ths(symbol=stock)['经营活动产生的现金流量净额'].iloc[0]
                market_cap = ak.stock_zh_a_spot_em(symbol=stock)['总市值'].iloc[0]
                
                metrics.append({
                    'PE': df['市盈率(PE)'].iloc[0],
                    'PB': df['市净率(PB)'].iloc[0],
                    'PS': df['市销率(PS)'].iloc[0],
                    'PC': market_cap / cash_flow if cash_flow !=0 else np.nan
                })
            except: continue
        
        # 计算30%分位（网页10估值逻辑）
        df_metrics = pd.DataFrame(metrics).dropna()
        return df_metrics.quantile(0.3)
    except:
        return None

