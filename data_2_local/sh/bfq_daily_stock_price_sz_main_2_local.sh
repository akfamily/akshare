#!/bin/bash

# 设置虚拟环境路径
VENV_PATH="/home/arrow/code/invest/takshare/.venv"

# 直接使用虚拟环境中的Python解释器
"$VENV_PATH/bin/python" /home/arrow/code/invest/takshare/data_2_local/bfq_daily_stock_price_sz_main_2_local.py
