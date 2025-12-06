import time

import pandas as pd
import baostock as bs

from data_2_local.common_data_2_local import df_append_2_local


def get_baostock_code(code):
    if code.startswith('6'):
        baostock_code = f"sh.{code}"
    elif code.startswith('0'):
        baostock_code = f"sz.{code}"
    else:
        baostock_code = code
    return baostock_code

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)  # 设置行数为无限制
    pd.set_option('display.max_columns', None)  # 设置列数为无限制
    pd.set_option('display.width', 1000)  # 设置列宽
    pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)


    # rs_factor = bs.query_adjust_factor(code="sh.600000", start_date="2008-04-24", end_date="2009-06-20")
    # rs_factor = bs.query_adjust_factor(code="sh.600000", start_date="2024-07-18", end_date="2025-07-16")


    with open(file='data/adjust_factor_2_local/399101_codes.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_stock_codes = content.split('\n')
        print(len(t_stock_codes))
    with open(file='data/adjust_factor_2_local/complete_codes.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        t_complete_codes = content.split('\n')
        print(len(t_complete_codes) - 1)
    t_complete_code_set = set(t_complete_codes)
    t_codes = []
    for code in t_stock_codes:
        if code in t_complete_code_set:
            continue
        t_codes.append(code)
    # t_codes = ['002003']
    print(f'len_t_codes: {len(t_codes)}')

    for code in t_codes:
        t_baostock_code = get_baostock_code(code)
        rs_factor = bs.query_adjust_factor(code=t_baostock_code, start_date="2000-01-01")
        rs_list = []
        while (rs_factor.error_code == '0') & rs_factor.next():
            rs_list.append(rs_factor.get_row_data())
        result_factor = pd.DataFrame(rs_list, columns=rs_factor.fields)
        result_factor = result_factor[['code', 'dividOperateDate', 'foreAdjustFactor', 'backAdjustFactor']]
        result_factor.rename(columns={
                'dividOperateDate': 'divid_operate_date',
                'foreAdjustFactor': 'fore_adjust_factor',
                'backAdjustFactor': 'back_adjust_factor',
            }, inplace=True)
        result_factor['code'] = code
        # print(result_factor)
        df_append_2_local(table_name='adjust_factor', df=result_factor)
        # code完成，向complete_codes.txt追加一条数据
        with open(file='data/adjust_factor_2_local/complete_codes.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{code}\n')
        time.sleep(0.5)

    # rs_factor = bs.query_adjust_factor(code="sh.600000", start_date="2000-01-01")
    # while (rs_factor.error_code == '0') & rs_factor.next():
    #     rs_list.append(rs_factor.get_row_data())
    # result_factor = pd.DataFrame(rs_list, columns=rs_factor.fields)
    # # 打印输出
    # print(result_factor)

    # 结果集输出到csv文件
    # result_factor.to_csv("D:\\adjust_factor_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()