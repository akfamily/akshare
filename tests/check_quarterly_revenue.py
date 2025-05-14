import akshare as ak
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

def get_revenue_decline(code, countQ=3):
    """检查最近countQ个季度的营收连续环比下滑且平均下滑超-10%"""
    try:
        # 获取利润表数据（仅取countQ+1个季度）
        df = get_quarterly_revenue(code,countQ)
        #df = ak.stock_financial_benefit_ths(symbol=code)
        df = df.head(countQ+1)
        
        if len(df) < countQ+1:  # 数据不足时跳过[7](@ref)
            raise ValueError("数据不足")

        recent_qoq = df['QoQ'].head(countQ).tolist()
        
        # 条件验证（网页7财务分析逻辑）
        if len(recent_qoq) <3: 
                raise ValueError("没有获取到3个季度的营收数据")
        return df
    except Exception as e:
        print(f"Error processing {code}: {str(e)}")
        return False

def check_revenue_decline(list, countQ=3, everyQ=0, decline=-10):
    count = min(len(list),countQ)
    list = list[0:count]
    print(f"QoQ: {list}")
    if all(x <everyQ for x in list):  # 连续3季下滑
            annual_decline = np.mean(list)  # 年均下滑率
            print(f"annual_decline: {annual_decline} compare to {decline}")
            return annual_decline <= decline
    else:
        print(f"QoQ have value > {everyQ}")
        return False
    return False


def get_quarterly_revenue(code, countQ=3):
    """优化后支持动态季度数计算的版本"""
    try:
        # 获取数据并按报告期倒序排列（网页3数据排序逻辑）
        df = ak.stock_financial_benefit_ths(symbol=code)
        df = df[['报告期', '*营业总收入']].sort_values('报告期', ascending=False).head(countQ+1)  # 关键优化点
        
        # 单位转换（网页3中文单位处理逻辑）
        df['营收数值'] = df['*营业总收入'].apply(
            lambda x: float(x.replace('亿', '')) * 1e8 if '亿' in str(x) else np.nan
        )
        
        # 生成跨年标记
        df = generate_cross_year_flag(df)
    
        #计算单季营收（修正逻辑）
        df['单季营收'] = np.where(
            df['跨年标记'], 
            df['营收数值'], 
            df['营收数值']-df['营收数值'].shift(-1).fillna(0)
        )
    
        # 计算环比（网页3的pct_change逻辑）
        df['QoQ'] = df['单季营收'].pct_change(periods=-1).round(4)*100
        return df[['报告期','*营业总收入','单季营收','跨年标记','QoQ']]
    
    except Exception as e:
        print(f"处理{code}时出错: {str(e)}")
        return pd.DataFrame()

# 修改后的跨年标记逻辑（网页6/7跨年日期计算原理）
def generate_cross_year_flag(df):
    """基于自然年度的财年边界识别"""
    # 按报告期排序并提取年份、季度
    df = df.sort_values('报告期', ascending=False)
    df['年份'] = df['报告期'].str[:4].astype(int)
    df['季度'] = df['报告期'].apply(lambda x: (pd.to_datetime(x).month-1)//3 + 1)
    
    # 生成跨年标记：当前行年份 > 下一行年份（即新财年Q1）
    df['跨年标记'] = (df['年份'] > df['年份'].shift(-1)) & (df['季度'] == 1)
    return df

# 数据清洗
def convert_revenue_unit(rev_str):
    if pd.isna(rev_str) or rev_str.strip() == '':
        return np.nan
    try:
        if '亿' in rev_str:
            return float(rev_str.replace('亿', '')) * 1e8  # 转换为元
        elif '万' in rev_str:
            return float(rev_str.replace('万', '')) * 1e4
        else:
            return float(rev_str)
    except:
        return np.nan


if __name__ == "__main__":
    df=get_quarterly_revenue("000001",5)
    print(df)
    recent_qoq=df['QoQ'].tolist()
    print(check_revenue_decline(recent_qoq,countQ=3, everyQ=2, decline=-5))
