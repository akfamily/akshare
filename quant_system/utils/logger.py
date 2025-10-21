"""
日志管理模块
"""

import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    """日志管理器"""

    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self, log_level='INFO', log_dir='logs'):
        """
        设置日志器

        Args:
            log_level: 日志级别
            log_dir: 日志目录
        """
        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建logger
        self._logger = logging.getLogger('QuantSystem')
        self._logger.setLevel(getattr(logging, log_level))

        # 清除已有的handlers
        self._logger.handlers = []

        # 创建formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # 文件处理器 - 所有日志
        today = datetime.now().strftime('%Y%m%d')
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f'quant_system_{today}.log'),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        # 错误日志文件处理器
        error_handler = logging.FileHandler(
            os.path.join(log_dir, f'error_{today}.log'),
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self._logger.addHandler(error_handler)

    def get_logger(self):
        """获取logger实例"""
        return self._logger

    def info(self, message: str):
        """记录INFO级别日志"""
        self._logger.info(message)

    def debug(self, message: str):
        """记录DEBUG级别日志"""
        self._logger.debug(message)

    def warning(self, message: str):
        """记录WARNING级别日志"""
        self._logger.warning(message)

    def error(self, message: str, exc_info=False):
        """记录ERROR级别日志"""
        self._logger.error(message, exc_info=exc_info)

    def critical(self, message: str):
        """记录CRITICAL级别日志"""
        self._logger.critical(message)


# 全局logger实例
logger = Logger()


def get_logger():
    """获取全局logger"""
    return logger.get_logger()
