import pandas as pd

from data_2_local.common_data_2_local import df_append_2_local


def data_2_local():
    file_path = f'data/listing_date/listing_date.txt'
    # 定义列名
    column_names = ['code', 'listing_date']
    dtype_dict = {
        'code': 'str',
    }
    df = pd.read_csv(file_path,
                     sep='\s+',
                     # skiprows=1,
                     # comment='#',  # 跳过以#开头的行
                     skip_blank_lines=True,  # 跳过空行
                     names=column_names,
                     dtype=dtype_dict,
                     encoding='utf-8')
    df['listing_date'] = pd.to_datetime(df['listing_date'])
    df_append_2_local(table_name='stock_listing_date', df=df)


if __name__ == '__main__':
    data_2_local()
