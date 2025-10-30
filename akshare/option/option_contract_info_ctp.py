#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/30 17:40
Desc: openctp-合约信息接口
http://openctp.cn/instruments.html
"""

import pandas as pd
import requests


def option_contract_info_ctp() -> pd.DataFrame:
    """
    openctp-合约信息接口-期权合约
    http://openctp.cn/instruments.html
    :return: 期权合约信息
    :rtype: pandas.DataFrame
    """
    url = "http://dict.openctp.cn/instruments?types=option"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data'])

    # 字段映射：英文字段名 -> 中文字段名
    column_mapping = {
        'ExchangeID': '交易所ID',
        'InstrumentID': '合约ID',
        'InstrumentName': '合约名称',
        'ProductClass': '商品类别',
        'ProductID': '品种ID',
        'VolumeMultiple': '合约乘数',
        'PriceTick': '最小变动价位',
        'LongMarginRatioByMoney': '做多保证金率',
        'ShortMarginRatioByMoney': '做空保证金率',
        'LongMarginRatioByVolume': '做多保证金/手',
        'ShortMarginRatioByVolume': '做空保证金/手',
        'OpenRatioByMoney': '开仓手续费率',
        'OpenRatioByVolume': '开仓手续费/手',
        'CloseRatioByMoney': '平仓手续费率',
        'CloseRatioByVolume': '平仓手续费/手',
        'CloseTodayRatioByMoney': '平今手续费率',
        'CloseTodayRatioByVolume': '平今手续费/手',
        'DeliveryYear': '交割年份',
        'DeliveryMonth': '交割月份',
        'OpenDate': '上市日期',
        'ExpireDate': '最后交易日',
        'DeliveryDate': '交割日',
        'UnderlyingInstrID': '标的合约ID',
        'UnderlyingMultiple': '标的合约乘数',
        'OptionsType': '期权类型',
        'StrikePrice': '行权价',
        'InstLifePhase': '合约状态'
    }
    # 重命名列为中文
    temp_df = temp_df.rename(columns=column_mapping)
    return temp_df


# 使用示例
if __name__ == "__main__":
    option_contract_info_ctp_df = option_contract_info_ctp()
    print(option_contract_info_ctp_df)
