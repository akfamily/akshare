import time

import pandas as pd
import akshare as ak

from data_2_local.common_data_2_local import df_append_2_local



def data_2_local():
    column_rename_dict = {
        '证券简称': 'security_abbr',
        '机构名称': 'institution_name',
        '境外法人持股': 'foreign_corp_share',
        '证券投资基金持股': 'fund_share',
        '国家持股-受限': 'state_share_restricted',
        '国有法人持股': 'state_owned_corp_share',
        '配售法人股': 'placement_corp_share',
        '发起人股份': 'founder_share',
        '未流通股份': 'non_tradable_share',
        '其中：境外自然人持股': 'foreign_individual_share',
        '其他流通受限股份': 'other_restricted_share',
        '其他流通股': 'other_tradable_share',
        '外资持股-受限': 'foreign_share_restricted',
        '内部职工股': 'employee_share',
        '境外上市外资股-H股': 'h_share',
        '其中：境内法人持股': 'domestic_corp_share',
        '自然人持股': 'individual_share',
        '人民币普通股': 'a_share',
        '国有法人持股-受限': 'state_owned_corp_share_restricted',
        '一般法人持股': 'general_corp_share',
        '控股股东、实际控制人': 'controlling_shareholder',
        '其中：限售H股': 'restricted_h_share',
        '变动原因': 'change_reason',
        '公告日期': 'announcement_date',
        '境内法人持股': 'domestic_corp_share_2',
        '证券代码': 'code',
        '变动日期': 'change_date',
        '战略投资者持股': 'strategic_investor_share',
        '国家持股': 'state_share',
        '其中：限售B股': 'restricted_b_share',
        '其他未流通股': 'other_non_tradable_share',
        '流通受限股份': 'restricted_tradable_share',
        '优先股': 'preferred_share',
        '高管股': 'executive_share',
        '总股本': 'total_shares',
        '其中：限售高管股': 'restricted_executive_share',
        '转配股': 'transferred_share',
        '境内上市外资股-B股': 'b_share',
        '其中：境外法人持股': 'foreign_corp_share_2',
        '募集法人股': 'fundraising_corp_share',
        '已流通股份': 'tradable_share',
        '其中：境内自然人持股': 'domestic_individual_share',
        '其他内资持股-受限': 'other_domestic_restricted',
        '变动原因编码': 'change_reason_code'
    }

    # with open(file='data/stock_share_change_cninfo_2_local/399101_codes.txt', mode='r', encoding='utf-8') as f:
    #     content = f.read()
    #     t_stock_codes = content.split('\n')
    #     print(len(t_stock_codes))
    # with open(file='data/stock_share_change_cninfo_2_local/complete_codes.txt', mode='r', encoding='utf-8') as f:
    #     content = f.read()
    #     t_complete_codes = content.split('\n')
    #     print(len(t_complete_codes) - 1)  # 减1是因为多个换行
    # t_complete_code_set = set(t_complete_codes)
    # unlisted_set = {'002336', '002750'}  # 退市的查不到数据，跳过
    # t_codes = []
    # for code in t_stock_codes:
    #     if code in t_complete_code_set:
    #         continue
    #     if code in unlisted_set:
    #         continue
    #     t_codes.append(code)
    # # t_codes = ['002336']
    # print(f'len_t_codes: {len(t_codes)}')

    t_codes = ['002334']
    for code in t_codes:
        df = ak.stock_share_change_cninfo(symbol=code, start_date="20000101", end_date="20251206")
        df = df.rename(columns=column_rename_dict)
        # print(df)
        df_append_2_local(table_name='stock_share_change_cninfo', df=df)
        # code完成，向complete_codes.txt追加一条数据
        # with open(file='data/stock_share_change_cninfo_2_local/complete_codes.txt', mode='a', encoding='utf-8') as f:
        #     f.write(f'{code}\n')
        # time.sleep(0.5)

def unlisted_data_2_local(code):
    file_path = f'data/stock_share_change_cninfo_2_local/{code}.txt'
    column_names = ['code', 'day', 'circulating_cap']
    dtype_dict = {
        'circulating_cap': 'float64',
    }
    df = pd.read_csv(file_path,
                     sep='\s+',
                     skiprows=1,
                     # comment='#',  # 跳过以#开头的行
                     skip_blank_lines=True,  # 跳过空行
                     names=column_names,
                     dtype=dtype_dict,
                     encoding='utf-8')
    column_rename_dict = {
        'day': 'change_date',
        'circulating_cap': 'a_share',
    }
    df = df.rename(columns=column_rename_dict)
    df['code'] = code
    df['change_date'] = pd.to_datetime(df['change_date'])
    df_append_2_local(table_name='stock_share_change_cninfo', df=df)

def special_data_2_local():
    codes = ['002336', '002750']
    for code in codes:
        unlisted_data_2_local(code)

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)  # 设置行数为无限制
    pd.set_option('display.max_columns', None)  # 设置列数为无限制
    pd.set_option('display.width', 1000)  # 设置列宽
    pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左
    special_data_2_local()



