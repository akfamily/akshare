import datetime

import pandas as pd

delisted_stock_codes = {'002336', '002750'}

def get_file_name(code):
    # 已退市股票。用当前页面数据导出的。已退市股票用高级导出是空的，没数据。
    if code in delisted_stock_codes:
        file_name = f'T{code}.txt'
    elif code.startswith(('50', '51', '56', '58')):
        file_name = f"SH#{code}.txt"
    else:
        file_name = f"SZ#{code}.txt"
    return file_name


def get_file_data(code, greater_date_ts=None):
    file_name = get_file_name(code)
    file_path = f'D:/new_tdx/T0002/export/{file_name}'

    dtype_dict = {
        'open': 'float64',
        'close': 'float64',
        'high': 'float64',
        'low': 'float64',
        # 'volume': 'int64',
    }
    # 退市股是特殊的少数几个，用当前页面导出的数据。两种格式不一样
    if code in delisted_stock_codes:
        skiprows = 4
        column_names = ['date', 'open', 'high', 'low', 'close', 'volume', 'MA.MA1', 'MA.MA2', 'MA.MA3', 'MA.MA4', 'MA.MA5', 'MA.MA6', 'MA.MA7', 'MA.MA8']
    else:
        skiprows = 2
        # turnover: 成交额
        column_names = ['date', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    df = pd.read_csv(file_path,
                     sep='\s+',
                     skiprows=skiprows,
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

    codes = ['002019', '002750']
    # codes = ['002750']
    # t_greater_date_ts = pd.Timestamp(datetime.date(2025, 10, 27))
    for tcode in codes:
        # tdf = get_file_data(tcode, t_greater_date_ts)
        tdf = get_file_data(tcode)
        print(tdf.head(10))
