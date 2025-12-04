import pandas as pd

from data_2_local.common_data_2_local import df_append_2_local


def data_2_local():
    file_path = f'data/shenwan_industry_2/shenwan_industry_2.txt'
    # 定义列名。turnover: 成交额
    column_names = ['code', 'name']
    dtype_dict = {
        'code': 'str',
        'name': 'str',
    }
    df = pd.read_csv(file_path,
                     sep=' ',
                     skiprows=1,
                     # comment='#',  # 跳过以#开头的行
                     skip_blank_lines=True,  # 跳过空行
                     names=column_names,
                     dtype=dtype_dict,
                     encoding='utf-8')
    df_append_2_local(table_name='shenwan_industry_2', df=df)


if __name__ == '__main__':
    data_2_local()
