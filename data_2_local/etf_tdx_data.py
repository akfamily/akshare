import datetime

import pandas as pd


def get_file_name(code):
    if code.startswith(('50', '51', '56', '58')):
        file_name = f"SH#{code}.txt"
    else:
        file_name = f"SZ#{code}.txt"
    return file_name


def get_file_data(code, greater_date_ts=None):
    file_name = get_file_name(code)
    file_path = f'D:/new_tdx/T0002/export/{file_name}'
    # 定义列名。turnover: 成交额
    column_names = ['date', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    dtype_dict = {
        'open': 'float64',
        'close': 'float64',
        'high': 'float64',
        'low': 'float64',
        'volume': 'float64',
    }
    df = pd.read_csv(file_path,
                     sep='\t',
                     skiprows=2,
                     comment='#',  # 跳过以#开头的行
                     skip_blank_lines=True,  # 跳过空行
                     names=column_names,
                     dtype=dtype_dict,
                     encoding='GBK')
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df['date'] = pd.to_datetime(df['date'])
    if greater_date_ts is not None:
        df = df[df['date'] > greater_date_ts]
    return df


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)  # 设置行数为无限制
    pd.set_option('display.max_columns', None)  # 设置列数为无限制
    pd.set_option('display.width', 1000)  # 设置列宽
    pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左

    codes = ['159985']
    greater_date_ts = pd.Timestamp(datetime.date(2025, 10, 27))
    for tcode in codes:
        tdf = get_file_data(tcode, greater_date_ts)
        print(tdf.head(10))
