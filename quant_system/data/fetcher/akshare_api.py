"""
AKShare数据接口封装
提供统一的数据获取接口
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 将akshare库添加到路径
akshare_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if akshare_root not in sys.path:
    sys.path.insert(0, akshare_root)

import akshare as ak
import pandas as pd
import numpy as np
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from utils.logger import logger


class AKShareAPI:
    """AKShare API封装类"""

    def __init__(self):
        self.logger = logger

    # ==================== 行情数据 ====================

    def get_stock_zh_a_spot(self) -> pd.DataFrame:
        """
        获取A股实时行情数据

        Returns:
            包含股票代码、名称、最新价、涨跌幅等信息的DataFrame
        """
        try:
            df = ak.stock_zh_a_spot_em()
            self.logger.info(f"获取A股实时行情成功，共{len(df)}只股票")
            return df
        except Exception as e:
            self.logger.error(f"获取A股实时行情失败: {str(e)}", exc_info=True)
            return pd.DataFrame()

    def get_stock_zh_a_hist(self, symbol: str, period='daily',
                             start_date: str = None, end_date: str = None,
                             adjust='qfq') -> pd.DataFrame:
        """
        获取个股历史行情数据

        Args:
            symbol: 股票代码，如 '000001'
            period: 周期 ('daily', 'weekly', 'monthly')
            start_date: 开始日期 'YYYYMMDD'
            end_date: 结束日期 'YYYYMMDD'
            adjust: 复权类型 ('qfq'-前复权, 'hfq'-后复权, ''-不复权)

        Returns:
            历史行情DataFrame
        """
        try:
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date or '20200101',
                end_date=end_date or datetime.now().strftime('%Y%m%d'),
                adjust=adjust
            )
            return df
        except Exception as e:
            self.logger.error(f"获取{symbol}历史行情失败: {str(e)}")
            return pd.DataFrame()

    def get_index_zh_a_hist(self, symbol: str, period='daily',
                            start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取指数历史行情

        Args:
            symbol: 指数代码，如 '000001' (上证指数)
            period: 周期
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            指数历史行情DataFrame
        """
        try:
            df = ak.stock_zh_index_daily(
                symbol=f'sh{symbol}' if symbol.startswith('0') else f'sz{symbol}'
            )
            return df
        except Exception as e:
            self.logger.error(f"获取指数{symbol}历史行情失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 财务数据 ====================

    def get_financial_indicator(self, symbol: str) -> pd.DataFrame:
        """
        获取财务指标数据

        Args:
            symbol: 股票代码

        Returns:
            财务指标DataFrame (包含ROE、毛利率等)
        """
        try:
            df = ak.stock_financial_analysis_indicator(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取{symbol}财务指标失败: {str(e)}")
            return pd.DataFrame()

    def get_balance_sheet(self, symbol: str) -> pd.DataFrame:
        """获取资产负债表"""
        try:
            df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取{symbol}资产负债表失败: {str(e)}")
            return pd.DataFrame()

    def get_income_statement(self, symbol: str) -> pd.DataFrame:
        """获取利润表"""
        try:
            df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取{symbol}利润表失败: {str(e)}")
            return pd.DataFrame()

    def get_cashflow_statement(self, symbol: str) -> pd.DataFrame:
        """获取现金流量表"""
        try:
            df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取{symbol}现金流量表失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 宏观数据 ====================

    def get_macro_china_gdp(self) -> pd.DataFrame:
        """获取中国GDP数据"""
        try:
            df = ak.macro_china_gdp()
            return df
        except Exception as e:
            self.logger.error(f"获取GDP数据失败: {str(e)}")
            return pd.DataFrame()

    def get_macro_china_cpi(self) -> pd.DataFrame:
        """获取CPI数据"""
        try:
            df = ak.macro_china_cpi()
            return df
        except Exception as e:
            self.logger.error(f"获取CPI数据失败: {str(e)}")
            return pd.DataFrame()

    def get_macro_china_ppi(self) -> pd.DataFrame:
        """获取PPI数据"""
        try:
            df = ak.macro_china_ppi()
            return df
        except Exception as e:
            self.logger.error(f"获取PPI数据失败: {str(e)}")
            return pd.DataFrame()

    def get_macro_china_pmi(self) -> pd.DataFrame:
        """获取PMI数据"""
        try:
            df = ak.macro_china_pmi()
            return df
        except Exception as e:
            self.logger.error(f"获取PMI数据失败: {str(e)}")
            return pd.DataFrame()

    def get_macro_china_m2(self) -> pd.DataFrame:
        """获取M2数据"""
        try:
            df = ak.macro_china_money_supply()
            return df
        except Exception as e:
            self.logger.error(f"获取M2数据失败: {str(e)}")
            return pd.DataFrame()

    def get_macro_china_social_financing(self) -> pd.DataFrame:
        """获取社融数据"""
        try:
            df = ak.macro_china_shrzgm()
            return df
        except Exception as e:
            self.logger.error(f"获取社融数据失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 资金数据 ====================

    def get_stock_individual_fund_flow(self, symbol: str, market='sh') -> pd.DataFrame:
        """
        获取个股资金流向

        Args:
            symbol: 股票代码
            market: 市场 ('sh', 'sz')

        Returns:
            资金流向DataFrame
        """
        try:
            df = ak.stock_individual_fund_flow(stock=symbol, market=market)
            return df
        except Exception as e:
            self.logger.error(f"获取{symbol}资金流向失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_fund_flow_industry(self, symbol: str = '全部') -> pd.DataFrame:
        """获取行业资金流向"""
        try:
            df = ak.stock_fund_flow_industry(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取行业资金流向失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_em_hsgt_north_net_flow_in(self) -> pd.DataFrame:
        """获取北向资金流向"""
        try:
            df = ak.stock_em_hsgt_north_net_flow_in(indicator='沪股通')
            return df
        except Exception as e:
            self.logger.error(f"获取北向资金流向失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 估值数据 ====================

    def get_stock_a_lg_indicator(self, symbol: str) -> pd.DataFrame:
        """获取A股龙虎榜数据"""
        try:
            df = ak.stock_lhb_detail_em(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取龙虎榜数据失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_margin_detail(self, date: str = None) -> pd.DataFrame:
        """获取融资融券数据"""
        try:
            date = date or datetime.now().strftime('%Y%m%d')
            df = ak.stock_margin_detail(date=date)
            return df
        except Exception as e:
            self.logger.error(f"获取融资融券数据失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 行业数据 ====================

    def get_stock_board_industry_name_em(self) -> pd.DataFrame:
        """获取行业分类"""
        try:
            df = ak.stock_board_industry_name_em()
            return df
        except Exception as e:
            self.logger.error(f"获取行业分类失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_board_industry_cons_em(self, symbol: str) -> pd.DataFrame:
        """获取行业成份股"""
        try:
            df = ak.stock_board_industry_cons_em(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取行业成份股失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 特色数据 ====================

    def get_stock_a_ttm_lyr(self) -> pd.DataFrame:
        """获取A股市盈率市净率数据"""
        try:
            df = ak.stock_a_ttm_lyr()
            return df
        except Exception as e:
            self.logger.error(f"获取市盈率市净率数据失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_zt_pool_em(self, date: str = None) -> pd.DataFrame:
        """获取涨停板数据"""
        try:
            date = date or datetime.now().strftime('%Y%m%d')
            df = ak.stock_zt_pool_em(date=date)
            return df
        except Exception as e:
            self.logger.error(f"获取涨停板数据失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_dt_pool_em(self, date: str = None) -> pd.DataFrame:
        """获取跌停板数据"""
        try:
            date = date or datetime.now().strftime('%Y%m%d')
            df = ak.stock_dt_pool_em(date=date)
            return df
        except Exception as e:
            self.logger.error(f"获取跌停板数据失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_zh_a_new(self) -> pd.DataFrame:
        """获取新股数据"""
        try:
            df = ak.stock_zh_a_new()
            return df
        except Exception as e:
            self.logger.error(f"获取新股数据失败: {str(e)}")
            return pd.DataFrame()

    # ==================== 指数数据 ====================

    def get_index_stock_cons(self, symbol: str = '000300') -> pd.DataFrame:
        """
        获取指数成份股

        Args:
            symbol: 指数代码 (如 '000300' 为沪深300)

        Returns:
            成份股DataFrame
        """
        try:
            df = ak.index_stock_cons(symbol=symbol)
            return df
        except Exception as e:
            self.logger.error(f"获取指数{symbol}成份股失败: {str(e)}")
            return pd.DataFrame()

    def get_index_stock_info(self) -> pd.DataFrame:
        """获取所有指数信息"""
        try:
            df = ak.stock_zh_index_spot()
            return df
        except Exception as e:
            self.logger.error(f"获取指数信息失败: {str(e)}")
            return pd.DataFrame()
