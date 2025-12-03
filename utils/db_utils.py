# -*- coding:utf-8 -*-

# Author: PeterWeyland
# CreateTime: 2025-09-11
# Description: simple introduction of the code
import configparser
import os
from pathlib import Path


def load_db_config(config_file='db_config.ini'):
    """
    从配置文件加载数据库配置
    """
    # 获取配置文件路径
    current_dir = Path(__file__).parent.parent
    config_path = current_dir / 'config' / config_file

    if not config_path.exists():
        raise FileNotFoundError(f"配置文件 {config_path} 不存在")

    # 读取配置
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')

    # 获取数据库配置
    db_config = {
        'host': config.get('database', 'host', fallback='localhost'),
        'port': config.getint('database', 'port', fallback=3306),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database'),
        'charset': config.get('database', 'charset', fallback='utf8mb4'),
    }

    return db_config


def get_db_url():
    # 数据库连接配置
    db_config = load_db_config()
    db_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
    return db_url

# 测试函数
if __name__ == "__main__":
    try:
        config = load_db_config()
        print("数据库配置加载成功:")
        for key, value in config.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"加载配置失败: {e}")