"""
数据处理和计算的辅助函数
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Union, Tuple


class DataHelper:
    """数据处理辅助函数"""

    @staticmethod
    def remove_outliers(data: np.ndarray, method='MAD', n_sigma=3) -> np.ndarray:
        """
        去极值

        Args:
            data: 输入数据
            method: 方法 ('MAD' 或 '3sigma')
            n_sigma: 标准差倍数

        Returns:
            处理后的数据
        """
        if method == 'MAD':
            # 中位数绝对偏差法
            median = np.median(data)
            mad = np.median(np.abs(data - median))

            if mad == 0:
                return data

            # MAD标准化
            mad_scores = 0.6745 * (data - median) / mad

            # 超过3倍MAD的值用边界值替代
            upper = median + 3 * mad / 0.6745
            lower = median - 3 * mad / 0.6745

            return np.clip(data, lower, upper)

        elif method == '3sigma':
            # 3倍标准差法
            mean = np.mean(data)
            std = np.std(data)

            upper = mean + n_sigma * std
            lower = mean - n_sigma * std

            return np.clip(data, lower, upper)

        else:
            return data

    @staticmethod
    def standardize(data: np.ndarray, method='zscore') -> np.ndarray:
        """
        标准化

        Args:
            data: 输入数据
            method: 方法 ('zscore', 'minmax', 'rank')

        Returns:
            标准化后的数据
        """
        if method == 'zscore':
            mean = np.mean(data)
            std = np.std(data)

            if std == 0:
                return np.zeros_like(data)

            return (data - mean) / std

        elif method == 'minmax':
            min_val = np.min(data)
            max_val = np.max(data)

            if max_val == min_val:
                return np.zeros_like(data)

            return (data - min_val) / (max_val - min_val)

        elif method == 'rank':
            return pd.Series(data).rank(pct=True).values

        else:
            return data

    @staticmethod
    def calculate_percentile(value: float, historical_data: np.ndarray, window=252) -> float:
        """
        计算历史分位数

        Args:
            value: 当前值
            historical_data: 历史数据
            window: 窗口大小

        Returns:
            分位数 (0-100)
        """
        if len(historical_data) < window:
            recent_data = historical_data
        else:
            recent_data = historical_data[-window:]

        if len(recent_data) == 0:
            return 50.0

        return np.sum(recent_data <= value) / len(recent_data) * 100

    @staticmethod
    def neutralize(data: Dict[str, float], industry_mapping: Dict[str, str]) -> Dict[str, float]:
        """
        行业中性化

        Args:
            data: {stock_code: value}
            industry_mapping: {stock_code: industry}

        Returns:
            行业中性化后的数据
        """
        neutralized = {}

        # 按行业分组
        industry_groups = {}
        for stock, value in data.items():
            industry = industry_mapping.get(stock, 'Unknown')
            if industry not in industry_groups:
                industry_groups[industry] = []
            industry_groups[industry].append((stock, value))

        # 行业内标准化
        for industry, stocks in industry_groups.items():
            if len(stocks) < 2:
                for stock, value in stocks:
                    neutralized[stock] = 0
                continue

            values = np.array([v for _, v in stocks])
            mean = np.mean(values)
            std = np.std(values)

            if std == 0:
                for stock, value in stocks:
                    neutralized[stock] = 0
            else:
                for stock, value in stocks:
                    neutralized[stock] = (value - mean) / std

        return neutralized

    @staticmethod
    def calculate_return(prices: np.ndarray, periods=1) -> np.ndarray:
        """
        计算收益率

        Args:
            prices: 价格序列
            periods: 周期数

        Returns:
            收益率序列
        """
        if len(prices) <= periods:
            return np.array([])

        returns = np.zeros(len(prices) - periods)
        for i in range(len(returns)):
            returns[i] = (prices[i + periods] - prices[i]) / prices[i]

        return returns

    @staticmethod
    def calculate_rolling_mean(data: np.ndarray, window: int) -> np.ndarray:
        """计算滚动平均"""
        return pd.Series(data).rolling(window=window).mean().values

    @staticmethod
    def calculate_rolling_std(data: np.ndarray, window: int) -> np.ndarray:
        """计算滚动标准差"""
        return pd.Series(data).rolling(window=window).std().values


class DateHelper:
    """日期处理辅助函数"""

    @staticmethod
    def get_trading_days(start_date: str, end_date: str) -> List[str]:
        """
        获取交易日列表
        简化版本：排除周末

        Args:
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'

        Returns:
            交易日列表
        """
        dates = []
        current = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        while current <= end:
            if current.weekday() < 5:  # 周一到周五
                dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

        return dates

    @staticmethod
    def get_last_trading_day(date: str = None) -> str:
        """
        获取上一个交易日

        Args:
            date: 日期字符串，None表示今天

        Returns:
            上一交易日
        """
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, '%Y-%m-%d')

        # 简化实现：向前找到工作日
        while True:
            date -= timedelta(days=1)
            if date.weekday() < 5:
                return date.strftime('%Y-%m-%d')

    @staticmethod
    def get_month_end_dates(start_date: str, end_date: str) -> List[str]:
        """
        获取月末日期列表

        Args:
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            月末交易日列表
        """
        dates = DateHelper.get_trading_days(start_date, end_date)
        if not dates:
            return []

        month_ends = []

        for i, date in enumerate(dates[:-1]):
            current_month = datetime.strptime(date, '%Y-%m-%d').month
            next_month = datetime.strptime(dates[i + 1], '%Y-%m-%d').month

            if current_month != next_month:
                month_ends.append(date)

        # 添加最后一个日期
        month_ends.append(dates[-1])

        return month_ends

    @staticmethod
    def is_trading_time() -> bool:
        """判断当前是否为交易时间"""
        now = datetime.now()

        # 简化版：周一到周五，9:30-15:00
        if now.weekday() >= 5:  # 周末
            return False

        time_now = now.time()
        morning_start = datetime.strptime('09:30', '%H:%M').time()
        morning_end = datetime.strptime('11:30', '%H:%M').time()
        afternoon_start = datetime.strptime('13:00', '%H:%M').time()
        afternoon_end = datetime.strptime('15:00', '%H:%M').time()

        return (morning_start <= time_now <= morning_end) or \
               (afternoon_start <= time_now <= afternoon_end)


class PerformanceHelper:
    """绩效计算辅助函数"""

    @staticmethod
    def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate=0.03) -> float:
        """
        计算夏普比率

        Args:
            returns: 日收益率序列
            risk_free_rate: 无风险利率（年化）

        Returns:
            夏普比率
        """
        if len(returns) == 0:
            return 0.0

        excess_returns = returns - risk_free_rate / 252

        if np.std(excess_returns) == 0:
            return 0.0

        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

    @staticmethod
    def calculate_sortino_ratio(returns: np.ndarray, risk_free_rate=0.03) -> float:
        """
        计算索提诺比率（只考虑下行波动）

        Args:
            returns: 日收益率序列
            risk_free_rate: 无风险利率（年化）

        Returns:
            索提诺比率
        """
        if len(returns) == 0:
            return 0.0

        excess_returns = returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]

        if len(downside_returns) == 0 or np.std(downside_returns) == 0:
            return 0.0

        return np.mean(excess_returns) / np.std(downside_returns) * np.sqrt(252)

    @staticmethod
    def calculate_calmar_ratio(annual_return: float, max_drawdown: float) -> float:
        """
        计算卡玛比率

        Args:
            annual_return: 年化收益率
            max_drawdown: 最大回撤

        Returns:
            卡玛比率
        """
        if max_drawdown == 0:
            return 0.0

        return annual_return / abs(max_drawdown)

    @staticmethod
    def calculate_information_ratio(portfolio_returns: np.ndarray,
                                      benchmark_returns: np.ndarray) -> float:
        """
        计算信息比率

        Args:
            portfolio_returns: 组合收益率
            benchmark_returns: 基准收益率

        Returns:
            信息比率
        """
        if len(portfolio_returns) != len(benchmark_returns):
            return 0.0

        tracking_error = portfolio_returns - benchmark_returns

        if np.std(tracking_error) == 0:
            return 0.0

        return np.mean(tracking_error) / np.std(tracking_error) * np.sqrt(252)

    @staticmethod
    def calculate_max_drawdown(equity_curve: np.ndarray) -> Tuple[float, int, int]:
        """
        计算最大回撤

        Args:
            equity_curve: 净值曲线

        Returns:
            (最大回撤, 开始位置, 结束位置)
        """
        if len(equity_curve) == 0:
            return 0.0, 0, 0

        peak = equity_curve[0]
        max_dd = 0.0
        max_dd_start = 0
        max_dd_end = 0
        peak_idx = 0

        for i, value in enumerate(equity_curve):
            if value > peak:
                peak = value
                peak_idx = i

            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
                max_dd_start = peak_idx
                max_dd_end = i

        return max_dd, max_dd_start, max_dd_end


class FinancialHelper:
    """财务指标计算辅助函数"""

    @staticmethod
    def calculate_roe(net_profit: float, equity: float) -> float:
        """计算ROE"""
        if equity == 0:
            return 0.0
        return net_profit / equity

    @staticmethod
    def calculate_roa(net_profit: float, total_assets: float) -> float:
        """计算ROA"""
        if total_assets == 0:
            return 0.0
        return net_profit / total_assets

    @staticmethod
    def calculate_debt_ratio(total_debt: float, total_assets: float) -> float:
        """计算资产负债率"""
        if total_assets == 0:
            return 0.0
        return total_debt / total_assets

    @staticmethod
    def calculate_current_ratio(current_assets: float, current_liabilities: float) -> float:
        """计算流动比率"""
        if current_liabilities == 0:
            return 0.0
        return current_assets / current_liabilities

    @staticmethod
    def calculate_quick_ratio(current_assets: float, inventory: float,
                               current_liabilities: float) -> float:
        """计算速动比率"""
        if current_liabilities == 0:
            return 0.0
        return (current_assets - inventory) / current_liabilities

    @staticmethod
    def calculate_gross_margin(gross_profit: float, revenue: float) -> float:
        """计算毛利率"""
        if revenue == 0:
            return 0.0
        return gross_profit / revenue

    @staticmethod
    def calculate_net_margin(net_profit: float, revenue: float) -> float:
        """计算净利率"""
        if revenue == 0:
            return 0.0
        return net_profit / revenue
