import pandas as pd

from data_2_local.common_data_2_local import df_append_2_local


def parse_stock_data(file_path):
    """
    解析股票数据文件，转换成指定格式

    Args:
        file_path (str): 数据文件路径

    Returns:
        list: 格式为 [(code, list[(日期, 代码)])] 的嵌套列表
    """
    result = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 逐行读取文件
            for line in f:
                # 去除首尾空白字符（换行、空格等）
                line = line.strip()
                if not line:  # 跳过空行
                    continue

                # 分割股票代码和后面的列表部分
                # 格式示例：000001.XSHE: [('20160104', '801192'), ('20211213', '801783')]
                code_part, data_part = line.split(':', 1)

                # 清理股票代码（去除多余空格）
                stock_code = code_part.strip()[0:6]

                # 处理数据部分，使用eval安全解析元组列表
                # 注意：如果文件来源不可信，请勿使用eval，可以改用ast.literal_eval
                import ast
                data_list = ast.literal_eval(data_part.strip())

                # 转换为list并添加到结果中
                result.append((stock_code, list(data_list)))

    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
    except Exception as e:
        print(f"解析文件时出错：{e}")

    return result


def data_2_local():
    file_path = "data/code_industry_2_change/20160104_20251203/log.txt"
    parsed_data = parse_stock_data(file_path)

    # 打印解析结果
    codes = []
    start_date_strs = []
    industry_codes = []
    industry_names = []
    for item in parsed_data:
        code = item[0]
        change_list = item[1]
        for (start_date_str, industry_code, industry_name) in change_list:
            codes.append(code)
            start_date_strs.append(start_date_str)
            industry_codes.append(industry_code)
            industry_names.append(industry_name)

    t_dict = {
        'code': codes,
        'start_date': start_date_strs,
        'industry_code_2': industry_codes,
        'industry_name_2': industry_names
    }
    df = pd.DataFrame(t_dict)
    df['code'] = df['code'].astype(str)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['industry_code_2'] = df['industry_code_2'].astype(str)
    print(df.head())

    df_append_2_local(table_name='code_industry_2_change', df=df)



if __name__ == "__main__":
    data_2_local()