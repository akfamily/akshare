# -*- coding:utf-8 -*-

# Author: PeterWeyland
# CreateTime: 2024/9/8
# Description: simple introduction of the code

import logging
import logging.handlers
import os
import inspect
import sys
from datetime import datetime


def setup_logger(name='t_app'):
    """
    前缀尽量不加别的东西
    :param name:
    :return:
    """
    # 在调用者目录生成log目录
    # 调用者文件
    caller_file_path = inspect.stack()[1].filename
    caller_file_name = os.path.basename(caller_file_path)
    caller_file_name = caller_file_name.rsplit(".", 1)[0]
    caller_dir_path = os.path.dirname(caller_file_path)
    log_dir = os.path.join(caller_dir_path, "log", caller_file_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建日志器
    logger = logging.getLogger(name)

    # 关键修改1：检查logger是否已经配置过，如果配置过直接返回
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 阻止日志传播到根logger
    logger.propagate = False

    # 日志格式
    formatter = logging.Formatter(
        # '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件处理器 - 按天滚动
    log_file = os.path.join(log_dir, f'{name}.log')
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"

    # 添加处理器到日志器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def setup_logger_simple_msg(name='t_app', level=logging.INFO):
    """
    前缀尽量不加别的东西
    :param name:
    :param level:
    :return:
    """
    # 在调用者目录生成log目录
    # 调用者文件
    caller_file_path = inspect.stack()[1].filename
    caller_file_name = os.path.basename(caller_file_path)
    caller_file_name = caller_file_name.rsplit(".", 1)[0]
    caller_dir_path = os.path.dirname(caller_file_path)
    log_dir = os.path.join(caller_dir_path, "log", caller_file_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建日志器
    logger = logging.getLogger(name)

    # 关键修改1：检查logger是否已经配置过，如果配置过直接返回
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # 阻止日志传播到根logger
    logger.propagate = False

    # 日志格式
    formatter = logging.Formatter(
        '%(name)s - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件处理器 - 按天滚动
    log_file = os.path.join(log_dir, f'{name}.log')
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"

    # 添加处理器到日志器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


class LogUtils:
    @classmethod
    def log_print(cls, str, log_dir_name=None):
        caller_file_path = inspect.stack()[1].filename
        # print(caller_file_path)
        caller_file_name = os.path.basename(caller_file_path)
        # 去除后缀
        caller_file_name = caller_file_name.rsplit(".", 1)[0]
        # 调用者文件所在目录
        caller_dir_path = os.path.dirname(caller_file_path)
        # 调用者文件所在目录/log/文件名
        if log_dir_name is None:
            log_dir_name = os.path.join(caller_dir_path, "log", caller_file_name)
        if not os.path.exists(log_dir_name):
            os.makedirs(log_dir_name)
        current_date_str = datetime.now().strftime("%Y-%m-%d")
        log_filename = os.path.join(log_dir_name, f"{current_date_str}.log")

        # 配置日志
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,  # 设置日志级别
            format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
            datefmt='%Y-%m-%d %H:%M:%S',  # 时间格式
            encoding='utf-8'  # 设置日志文件编码为 UTF-8
        )

        logging.info(str)
        print(str)


if __name__ == '__main__':
    LogUtils.log_print("xxx")
