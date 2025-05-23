import akshare as ak
import vectorbt as vbt
import pandas as pd
import time
import numpy as np
from datetime import datetime,timedelta
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
from getAllStock import get_all_stocks, get_select_stocks


# Windows 系统推荐配置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体支持中文[1,3](@ref)
plt.rcParams['axes.unicode_minus'] = False    # 修复负号显示问题[1](@ref)
print("当前生效字体:", plt.rcParams['font.sans-serif'])

def fetch_data(user_portfolio, benchmarks, start_date='20230522', end_date='20250522'):
    dfs = []
    total_symbols = len(user_portfolio) + len(benchmarks)
    
    with tqdm(total=total_symbols, desc='下载数据', unit='标的') as pbar:
        # 处理股票数据
        for s in user_portfolio:
            try:
                df = ak.stock_zh_a_hist(s, period="daily", 
                                      start_date=start_date, end_date=end_date,
                                      adjust="qfq")
                df = df.set_index(pd.to_datetime(df['日期'])).drop('日期', axis=1)
                dfs.append(df['收盘'].rename(s))
                pbar.update(1)
                time.sleep(1)
            except Exception as e:
                print(f"\n错误：{s}获取失败，{str(e)}")
        
        # 处理指数数据 
        for s in benchmarks:
            try:
                df = ak.index_zh_a_hist(symbol=s, period="daily",
                                      start_date=start_date, end_date=end_date)
                df = df.set_index(pd.to_datetime(df['日期'])).drop('日期', axis=1)
                dfs.append(df['收盘'].rename(s))
                pbar.update(1)
                time.sleep(1)
            except Exception as e:
                print(f"\n错误：{s}获取失败，{str(e)}")
    
    # 合并与对齐
    combined = pd.concat(dfs, axis=1)
    full_dates = pd.date_range(start=pd.to_datetime(start_date), 
                              end=pd.to_datetime(end_date), freq='B')
    return combined.reindex(full_dates).sort_index().ffill()

# 创建等权组合（每日再平衡）
def create_equal_weight_portfolio(portfolio_data, init_cash=1e6):
    # 生成等权配置矩阵
    weight_matrix = np.full_like(portfolio_data, 1/len(portfolio_data.columns))
    
    # 构建投资组合
    return vbt.Portfolio.from_holding(
        close=portfolio_data,
        size=weight_matrix,
        init_cash=init_cash,
        fees=0.001,
        slippage=0.005,
        freq='D'
    )

# 使用示例
if __name__ == "__main__":
    # 获取全量数据
    df = get_select_stocks()
    user_portfolio = df['代码'].tolist()
    benchmarks = [
    #"000016",# "上证50":
    #"000300",#"沪深300": 
    #"000009",#"上证380": 
    "399673",#"创业板50": 
    #"000905",#"中证500": 
    #"000010",#"上证180": 
    #"399324",#"深证红利": 
    #"399330",#"深证100": 
    #"000852",#"中证1000":
    #"000015",#"上证红利":
    #"000903",#"中证100": 
    #"000906"#"中证800": 
    ]

    # 预定义样式库（扩展自网页6、网页8）
    bench_styles = {
        '000016': {'color': '#1f77b4', 'linestyle': '-', 'linewidth': 2},
        '000300': {'color': '#ff7f0e', 'linestyle': '--', 'dash_capstyle': 'round'},
        '399673': {'color': '#2ca02c', 'linestyle': '-.', 'alpha': 0.8},
        '000905': {'color': '#d62728', 'linestyle': ':', 'marker': 'o', 'markevery': 10}
        }

    data = fetch_data(user_portfolio,benchmarks)

    # 提取自建组合数据
    portfolio_data = data[user_portfolio]
    # 创建自建组合动态权重矩阵
    weights = pd.DataFrame(
        np.full(portfolio_data.shape, 1/len(user_portfolio)),  # 每日等权
        index=portfolio_data.index,
        columns=portfolio_data.columns
    )

    # 构建投资组合
    portfolio = vbt.Portfolio.from_orders(
        close=portfolio_data,        # 收盘价数据
        size=weights,               # 目标持仓比例
        size_type='targetpercent',  # 按百分比调仓
        init_cash=1e6,              # 初始资金
        fees=0.001,                 # 手续费0.1%
        slippage=0.005,             # 滑点0.5%
        freq='D'                    # 每日再平衡
    )
    
    # 归一化处理
    portfolio_nav = portfolio.value().sum(axis=1) / 1e6  

    # 提取基准数据
    benchmark_data = data[benchmarks]

    # 计算基准收益率
    benchmark_cum = benchmark_data.pct_change().fillna(0)
    # 计算累计收益率时初始化首日为1（网页1、网页6方法）
    benchmark_cum.iloc[0] = 1  # 强制设置首日为基准起点

    # 绘制组合净值曲线
    portfolio_nav.plot(
        linewidth=3,
        color='#9467bd',
        label='用户组合',
        zorder=10  # 置于顶层
    )

    # 绘制基准曲线（采用网页7推荐的循环方式）
    for b in benchmarks:
        #if b in bench_styles:
        #    (benchmark_cum[b]/benchmark_cum[b].iloc[0]).plot(color='#1f77b4', linestyle='-', linewidth=2,label=f'基准: {b}')
        #else:  # 兜底样式
            (benchmark_cum[b]/benchmark_cum[b].iloc[0]).plot(
                linestyle='--',
                alpha=0.6,
                label=f'基准: {b}'
            )

    # 增强图例可读性（网页6、网页8方法）
    plt.legend(
        loc='upper left',
        bbox_to_anchor=(1, 1),  # 右侧外置图例
        frameon=False,
        fontsize=10
    )

    # 添加辅助网格
    plt.figure(figsize=(16, 8))  # 扩大画布尺寸[8](@ref)
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.title('组合与基准收益对比 (2023-2025)', fontsize=14)
    plt.ylabel('累计收益率', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()