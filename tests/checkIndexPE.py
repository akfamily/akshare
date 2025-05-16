import akshare as ak
import pandas as pd
from datetime import datetime,timedelta
from tqdm import tqdm
import matplotlib.pyplot as plt

"""获取重要指数"""

INDICES = [
        "上证50",
        "沪深300",
        "创业板50",
        "中证500",
        "深证红利",
        "中证1000", 
        "上证红利"
        ]

"""最早数据从2005年1月开始"""
STARTDAY=pd.to_datetime("2015-01-01")


def get_index_PE(symbol = "沪深300"):
    """获取指数估值数据"""
    # 获取沪深300指数的市盈率数据（默认返回全历史数据）
    pe_df = ak.stock_index_pe_lg(symbol)

    # 提取最新数据（按日期降序排序）
    latest_pe = pe_df["日期"==pe_df.sort_values('日期', ascending=False).iloc[0]]["静态市盈率中位数"]
       
    return latest_pe


def calculate_all_percentiles(clean_df):
    """多PE指标百分位计算"""
    # 定义计算列与结果容器
    pe_metrics = [
        ('等权静态市盈率', '静态'),
        ('静态市盈率', '静态'),
        ('静态市盈率中位数', '静态'),
        ('等权滚动市盈率', '滚动'),
        ('滚动市盈率', '滚动'), 
        ('滚动市盈率中位数', '滚动')
    ]
    
    results = []
    
    # 遍历每个PE指标
    for col, pe_type in pe_metrics:
        if col not in clean_df.columns:
            continue
            
        # 提取有效数据
        pe_series = clean_df[col].dropna()
        if len(pe_series) < 10:  # 数据量不足提示
            print(f"警告: {col} 有效数据不足10条")
            continue
            
        # 计算当前值和百分位
        latest_value = pe_series.iloc[-1]
        historical_data = pe_series[:-1]  # 排除最新数据
        
        # 计算时间百分位[8](@ref)
        time_percentile = (historical_data <= latest_value).mean()
        
        # 计算空间百分位（考虑极值）
        q1 = historical_data.quantile(0.25)
        q3 = historical_data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5*iqr
        upper_bound = q3 + 1.5*iqr
        valid_data = historical_data[(historical_data >= lower_bound) & (historical_data <= upper_bound)]
        space_percentile = (valid_data <= latest_value).mean()

        results.append({
             '最新值': latest_value,
            '时%': f"{time_percentile:.1%}",
            '空%': f"{space_percentile:.1%}",
            '市盈率指标类型': col,            
            '当前日期': pd.to_datetime(clean_df["日期"].iloc[-1]).strftime('%Y-%m-%d'),
            '起始日期': pd.to_datetime(clean_df["日期"].iloc[0]).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(results)

def preprocess_pe_data(df, startDay = STARTDAY):
    """数据清洗与格式转换"""
    # 转换日期格式并处理NaN
    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')  # 无效日期转为NaT[7](@ref)
    
    # 过滤无效日期记录
    valid_df = df[df['日期'].notna()].copy()
    valid_df = valid_df[valid_df['日期'] > startDay]      # 布尔索引筛选[2,5](@ref)
    
    # 定义需处理的PE列
    pe_columns = [
        '等权静态市盈率', '静态市盈率', '静态市盈率中位数',
        '等权滚动市盈率', '滚动市盈率', '滚动市盈率中位数'
    ]
    
    # 处理各PE列的NaN（前向填充+过滤全空列）
    for col in pe_columns:
        if col in valid_df.columns:
            valid_df[col] = valid_df[col].ffill().dropna()
        else:
            print(f"警告: 缺失必要列 {col}")
    
    return valid_df.sort_values('日期').drop_duplicates('日期')

import matplotlib.pyplot as plt

def plot_pe_percentiles(result_df):
    """可视化展示优化"""
    plt.figure(figsize=(14, 8))
    
    # 创建双坐标轴
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    # 绘制时间百分位
    bars = ax1.bar(result_df['市盈率指标类型'], 
                  result_df['时%'].str.rstrip('%').astype(float),
                  alpha=0.6,
                  color='steelblue',
                  label='时间百分位')
    
    # 绘制空间百分位
    line, = ax2.plot(result_df['市盈率指标类型'],
                    result_df['空%'].str.rstrip('%').astype(float),
                    'r-o',
                    linewidth=2,
                    markersize=8,
                    label='空间百分位')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', 
                ha='center', 
                va='bottom')
    
    # 设置坐标轴
    ax1.set_ylabel('时间百分位(%)', fontsize=12)
    ax2.set_ylabel('空间百分位(%)', fontsize=12, color='red')
    ax2.tick_params(axis='y', colors='red')
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans CJK JP']  # 优先选择系统已安装的字体[6,8](@ref)
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题[6,8](@ref)
    plt.title('多维度PE指标百分位对比', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend([bars, line], ['时间百分位', '空间百分位'], loc='upper left')
    plt.tight_layout()
    plt.show()
    return

def main_analysis(index_name):
    """完整分析流程"""
    try:
        # 获取原始数据
        raw_df = ak.stock_index_pe_lg(symbol=index_name)
        
        # 数据清洗
        clean_df = preprocess_pe_data(raw_df)
        
        # 计算百分位
        result_df = calculate_all_percentiles(clean_df)
        
        # 结果展示
        print(f"\n{index_name} PE指标分析报告")
        print(result_df.sort_values('时%', ascending=False))
        
        # 可视化
        plot_pe_percentiles(result_df)
        
        return result_df
    except Exception as e:
        print(f"分析失败: {str(e)}")
        return None

# 示例执行
if __name__ == "__main__":
    result = main_analysis('上证红利')

    
#INDICES = [
#        "上证50",
#        "沪深300",
#        "创业板50",
#        "中证500",
#        "中证1000", 
#        "深证红利",
#        "上证红利"
#        ]

    #print(STARTDAY)