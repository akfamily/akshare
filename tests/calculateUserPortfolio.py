import akshare as ak
import pandas as pd
import time
import numpy as np
from datetime import datetime,timedelta
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
import xlsxwriter
from getAllStock import get_all_stocks, get_select_stocks

#对标指数基准
BENCHMARKS = [
#"000016",# "上证50":
#"000300",#"沪深300": 
#"000009",#"上证380": 
#"399673",#"创业板50": 
"000905",#"中证500": 
#"000010",#"上证180": 
#"399324",#"深证红利": 
#"399330",#"深证100": 
#"000852",#"中证1000":
#"000015",#"上证红利":
#"000903",#"中证100": 
#"000906"#"中证800": 
]


# 对标指数基准预定义样式库
BENCH_STYLES = {
    '000016': {'color': '#1f77b4', 'linestyle': '-', 'linewidth': 2},
    '000300': {'color': '#ff7f0e', 'linestyle': '--', 'dash_capstyle': 'round'},
    '399673': {'color': '#2ca02c', 'linestyle': '-.', 'alpha': 0.8},
    '000905': {'color': '#d62728', 'linestyle': ':', 'marker': 'o', 'markevery': 10}
    }

SELECT_PATH=r"..\input\selectlist.xlsx"

def fetch_data(user_portfolio, benchmarks, start_date='20240521', end_date='20250522'):
    """获取所选择的股票和对标指数基准的历史股价数据"""
    dfs = []
    total_symbols = len(user_portfolio) + len(benchmarks)
    
    with tqdm(total=total_symbols, desc='下载数据', unit='标的') as pbar:
        # 处理股票数据
        for s in user_portfolio:
            try:
                df = ak.stock_zh_a_hist(s, period="daily", 
                                      start_date=start_date, end_date=end_date,
                                      adjust="hfq")
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


def calculateSelectProtfolio(select_path=SELECT_PATH,benchmarks = BENCHMARKS,start_date='20240521', end_date='20250522') -> pd.DataFrame:
    """获取所选择的股票数据"""
    # 默认SELECT_PATH=r"..\input\selectlist.xlsx"
    df = get_select_stocks(select_path)
    user_portfolio = df['代码'].tolist()

    #获取所选择的股票和对标指数的历史股价数据
    data = fetch_data(user_portfolio,benchmarks, start_date, end_date)
    if isinstance(data.index, pd.PeriodIndex):
        data.index = data.index.to_timestamp()  # 转换为时间戳
    elif not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)  # 确保是 DatetimeIndex

    # 提取自建组合数据
    portfolio_data = data[user_portfolio].copy()

    #计算每支股票对组合收益的贡献度
    contribution_ratio = calculate_contribution(portfolio_data)
    save_to_excel(contribution_ratio)

    
    # 归一化处理
    # 通过价格计算
    # 1. 对每只股票按初始值归一化（等权处理）
    normalized_stocks = portfolio_data.div(portfolio_data.iloc[0])  # 每列除以各自的首行值
    # 2. 计算每日等权平均（所有归一化后的股票每日取平均）
    portfolio_nav = normalized_stocks.mean(axis=1)  # axis=1表示按行求平均


    print(portfolio_nav.iloc[-1])
    print(contribution_ratio)

    # 提取对标指数基准数据
    benchmark_data = data[benchmarks].copy()

    # 方法1：直接通过价格计算累计收益率
    benchmark_nav = benchmark_data / benchmark_data.iloc[0]  # 初始值归一化为1
    
    #方法2：通过收益率累乘
    #benchmark_cum = benchmark_data.pct_change().fillna(0)
    #benchmark_nav = (1 + benchmark_cum).cumprod()

    return portfolio_nav,benchmark_nav


def calculate_contribution(prices_df: pd.DataFrame, 
                           weights: pd.Series = None, 
                           baseline_return: float = 0) -> pd.DataFrame:
    """
    计算每支股票对组合收益的贡献度，返回两列 DataFrame
    
    参数：
        prices_df : DataFrame，各股票历史价格数据（索引为日期，列为股票代码）
        weights   : Series，各股票权重（默认等权。要求：索引与prices_df列名一致）
        baseline_return : float，基准收益率（默认0，可设为组合总收益率）
    
    返回：
        DataFrame，包含列 ['代码', '贡献度']，贡献度为百分比格式（保留2位小数）
    """
    # 1. 输入校验
    if prices_df.empty:
        raise ValueError("价格数据不能为空")
    
    # 校验数据是否包含至少两个时间点（防止计算收益出错）
    if len(prices_df.index) < 2:
        raise ValueError("价格数据需包含至少两个不同日期的数据")

    # 2. 权重处理
    stocks = prices_df.columns.tolist()
    if weights is None:
        weights = pd.Series(1/len(stocks), index=stocks, name='权重')
    else:
        if not weights.index.equals(pd.Index(stocks)):
            raise ValueError("权重索引必须与股票代码一致")
        if abs(weights.sum() - 1) > 1e-6:
            raise ValueError("权重总和必须为1 (允许误差<1e-6)")

    # 3. 计算期间收益率（基准日到结束日）
    start_date = prices_df.index.min()
    end_date = prices_df.index.max()
    
    # 计算收益率（允许 结束日=基准日+1 的特殊情况）
    start_prices = prices_df.loc[start_date]
    end_prices = prices_df.loc[end_date]
    returns = (end_prices - start_prices) / start_prices

    # 4. 计算贡献度
    excess_returns = returns - baseline_return
    weighted_contrib = weights * excess_returns
    total_contrib = weighted_contrib.sum()

    # 处理总贡献为0的情况（避免除零错误）
    if abs(total_contrib) < 1e-10:
        contribution_ratio = pd.Series(0.0, index=stocks)
    else:
        contribution_ratio = (weighted_contrib / total_contrib) * 100

    # 5. 构建格式化输出
    result_df = pd.DataFrame({
        '代码': contribution_ratio.index,
        '贡献度': contribution_ratio.round(2).values
    })

    return result_df

#def calculate_contribution(prices_df, weights=None, baseline_return=0):
#    """
#    计算每支股票对组合收益的贡献度
    
#    参数：
#        prices_df : DataFrame，各股票历史价格数据（索引为日期，列为股票代码）
#        weights   : dict/Series，各股票权重（默认等权）
#        baseline_return : float，基准收益率（默认0，可设为组合总收益率）
    
#    返回：
#        Series，各股票的贡献度（百分比）
#    """
#    # 1. 验证输入数据
#    assert not prices_df.empty, "价格数据不能为空"
#    if weights is None:
#        weights = pd.Series(1/len(prices_df.columns), index=prices_df.columns)  # 等权
#    else:
#        assert abs(weights.sum() - 1) < 1e-6, "权重总和必须为1"

#    # 2. 计算期间收益率（首末日期）
#    start_date = prices_df.index.min()
#    end_date = prices_df.index.max()
#    start_prices = prices_df.loc[start_date]
#    end_prices = prices_df.loc[end_date]
#    returns = (end_prices - start_prices) / start_prices  # 简单收益率
    
#    # 3. 计算贡献度
#    excess_returns = returns - baseline_return
#    weighted_contrib = weights * excess_returns
#    total_contrib = weighted_contrib.sum()
    
#    if total_contrib == 0:  # 避免除零错误
#        return pd.Series(0, index=prices_df.columns)
    
#    contribution_ratio = weighted_contrib / total_contrib * 100
    
#    return contribution_ratio.round(2)

def plotPortfolio(portfolio_nav,benchmark_nav):
    # 创建大图（必须在绘图前设置）
    plt.figure(figsize=(16, 8))  # 这行要放在所有绘图操作之前！
    # Windows 系统推荐配置
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体支持中文[1,3](@ref)
    plt.rcParams['axes.unicode_minus'] = False    # 修复负号显示问题[1](@ref)

    # 绘制组合净值曲线
    portfolio_nav.plot(
        linewidth=3,
        color='#9467bd',
        label='用户组合',
        zorder=10  # 置于顶层
    )

    # 绘制基准曲线（采用网页7推荐的循环方式）
    for b in BENCHMARKS:
        if b in BENCH_STYLES:
            #benchmark_nav[b].plot(color='#1f77b4', linestyle='-', linewidth=2,label=f'基准: {b}')
             benchmark_nav[b].plot(**BENCH_STYLES[b],label=f'基准: {b}')
        else:  # 兜底样式
            benchmark_nav[b].plot(
                linestyle='--',
                alpha=0.6,
                label=f'基准: {b}'
            )

     # 图表装饰
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.title('组合与基准收益对比 (2020-2025)', fontsize=14)
    plt.ylabel('累计收益率', fontsize=12)

    # 优化图例（只保留一个legend调用）
    plt.legend(
        loc='upper left',
        bbox_to_anchor=(1, 1),  # 右侧外置图例
        frameon=False,
        fontsize=10
    )

    plt.tight_layout()
    plt.grid(True)
    plt.show()
    plt.show()
    return "Plot ok!"

def save_to_excel(df):
    """优化Excel写入（网页10）"""
    end_date = datetime.now().strftime("%Y%m%d")
    writer = pd.ExcelWriter(f'.\output\selectProtfolio{end_date}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='组合累计收益率')
    
    
    writer.close()

# 使用示例
if __name__ == "__main__":
    df1,df2 = calculateSelectProtfolio(SELECT_PATH,BENCHMARKS,'20220522', '20250522')    
    #print(df1)
    #print(df2)
    #save_to_excel(df1)
    #plotPortfolio(df1,df2)
