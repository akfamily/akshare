import os
import pandas as pd
from pathlib import Path

# 注意将列表excel以下列名字放在py文件相同目录下
SH_PATH=r"..\input\shanghailist.xlsx"
SZ_PATH=r"..\input\shenzhenlist.xlsx"
SELECT_PATH=r"..\input\selectlist.xlsx"

def get_all_stocks(sh_path=SH_PATH, sz_path=SZ_PATH) -> pd.DataFrame:
    """
    读取沪深股票列表，返回标准化代码与简称
    :param sh_path: 上交所文件路径
    :param sz_path: 深交所文件路径
    :return: DataFrame(代码, 名称)
    """
    # 读取上海数据[1,3](@ref)
    sh_cols = {'A股代码':'代码', '证券简称':'名称'}
    base_path = Path(__file__).parent
    sh_df = pd.read_excel(
        base_path / sh_path,
        usecols=list(sh_cols.keys()),
        dtype={'A股代码': str}
    ).rename(columns=sh_cols)
    sh_df = sh_df[sh_df['代码'].notna()]  # 过滤无A股代码的记录

    # 读取深圳数据[2,4](@ref)
    sz_cols = {'A股代码':'代码', 'A股简称':'名称'}
    sz_df = pd.read_excel(
        base_path / sz_path,
        usecols=list(sz_cols.keys()),
        dtype={'A股代码': str}
    ).rename(columns=sz_cols)
    sz_df = sz_df[sz_df['代码'].notna()]

    # 合并数据集[1,3,5](@ref)
    merged_df = pd.concat([sh_df, sz_df], ignore_index=True)
    
    # 数据清洗
    merged_df.drop_duplicates(subset=['代码'], keep='first', inplace=True)
    merged_df.sort_values(by='代码', inplace=True)
    
    return merged_df[['代码', '名称']]

def get_select_stocks(select_path=SELECT_PATH) -> pd.DataFrame:
    """
    读取特定选中股票列表，返回标准化代码与简称
    :param SELECT_PATH: 选中股票文件路径
    :return: DataFrame(代码, 名称)
    """
    # 读取上海数据[1,3](@ref)
    se_cols = {'A股代码':'代码', '证券简称':'名称'}
    base_path = Path(__file__).parent
    se_df = pd.read_excel(
        base_path / select_path,
        usecols=list(se_cols.keys()),
        dtype={'A股代码': str}
    ).rename(columns=se_cols)
    se_df = se_df[se_df['代码'].notna()]  # 过滤无A股代码的记录


    # 数据清洗
    se_df.drop_duplicates(subset=['代码'], keep='first', inplace=True)
    se_df.sort_values(by='代码', inplace=True)
    
    return se_df[['代码', '名称']]

# 使用示例
if __name__ == "__main__":
     try:
        df = get_select_stocks()
        print(df.head())
     except (FileNotFoundError, PermissionError) as e:
            print(f"🛑 关键错误: {e}")
            print("💡 请检查：文件路径是否包含空格/中文？是否被其他程序占用？")