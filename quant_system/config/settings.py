"""
量化系统配置文件
包含系统级配置和默认参数
"""

DEFAULT_CONFIG = {
    # 系统配置
    'system': {
        'log_level': 'INFO',
        'data_storage': 'sqlite',  # sqlite or mysql
        'cache_enabled': True,
        'db_path': 'data/quant.db'
    },

    # 数据配置
    'data': {
        'update_time': '16:00',  # 每日更新时间
        'history_years': 5,       # 历史数据年限
        'data_sources': ['akshare']
    },

    # 周期配置
    'cycle': {
        'juglar_window': 120,     # 朱格拉周期观察窗口（月）
        'kitchin_window': 48,     # 基钦周期观察窗口（月）
        'sentiment_window': 60,   # 情绪指标观察窗口（日）
    },

    # 因子配置
    'factor': {
        'num_factors': 6,
        'base_weights': {
            'value': 0.20,
            'quality': 0.20,
            'growth': 0.25,
            'momentum': 0.20,
            'sentiment': 0.10,
            'technical': 0.05
        },
        'industry_neutral': True,
        'outlier_method': 'MAD',   # MAD or 3sigma
        'standardization': 'zscore'
    },

    # 选股配置
    'selection': {
        'num_stocks': 50,
        'min_market_cap': 50,      # 最小市值（亿元）
        'min_daily_volume': 10,    # 最小日成交额（百万元）
        'max_st_stocks': 0,
        'rebalance_frequency': 'monthly'  # daily, weekly, monthly, quarterly
    },

    # 资产配置
    'allocation': {
        'strategy': 'hybrid',      # all_weather, swensen, hybrid
        'all_weather_weight': 0.5,
        'swensen_weight': 0.5,
        'rebalance_threshold': 0.05,
        'rebalance_frequency': 'quarterly'
    },

    # 风险控制
    'risk': {
        'max_position_pct': 0.10,       # 单只股票最大仓位
        'max_sector_pct': 0.30,         # 单个行业最大仓位
        'max_drawdown_limit': 0.25,     # 最大回撤限制
        'stop_loss_pct': 0.10,          # 个股止损
        'portfolio_stop_loss': 0.15,    # 组合止损
        'max_beta': 1.5,
        'min_liquidity': 10_000_000     # 最小流动性
    },

    # 回测配置
    'backtest': {
        'initial_capital': 1_000_000,
        'commission_rate': 0.0003,
        'stamp_tax': 0.001,
        'slippage': 0.001,
        'benchmark': '000300.SH'        # 沪深300
    },

    # 交易配置
    'trading': {
        'account_type': 'paper',        # paper or live
        'trade_time': '14:30',          # 交易执行时间
        'max_order_value': 100_000,     # 单笔最大交易金额
        'order_split': True             # 是否拆单
    }
}


class Config:
    """配置管理类"""

    def __init__(self, custom_config=None):
        self.config = DEFAULT_CONFIG.copy()
        if custom_config:
            self._update_config(custom_config)

    def _update_config(self, custom_config):
        """递归更新配置"""
        for key, value in custom_config.items():
            if isinstance(value, dict) and key in self.config:
                self.config[key].update(value)
            else:
                self.config[key] = value

    def get(self, key_path, default=None):
        """
        获取配置值
        支持点号分隔的路径，如 'system.log_level'
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path, value):
        """设置配置值"""
        keys = key_path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def to_dict(self):
        """返回完整配置字典"""
        return self.config.copy()
