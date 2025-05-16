import pandas as pd
import akshare as ak
from save_to_mysql import insert_to_mysql
from tqdm import tqdm
import sys

# SQL语句
INSERT_SQL ="""
INSERT INTO `index_valuation_history` 
(`index_code`, `index_name`, `trade_date`, `index_value`, 
`pe_equal_weight_static`, `pe_static`, `pe_static_median`,
`pe_equal_weight_ttm`, `pe_ttm`, `pe_ttm_median`)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def insert_major_index_valuation():
    """获取三大指数估值数据"""
    indices = {
        "上证50": "000016.SH",
        "沪深300": "000300.SH",
        #"上证380": "000009.SH",
        #"创业板50": "399673.SZ",
        #"中证500": "000905.SH",
        #"上证180": "000010.SH",
        #"深证红利": "399324.SZ",
        #"深证100": "399330.SZ",
        #"中证1000": "000852.SH",
        #"上证红利": "000015.SH",
        #"中证100": "000903.SH",
        #"中证800": "000906.SH"
               }
    for name,code in tqdm(indices.items(),desc=f"获取{indices.items()}估值……"):
        try:
            # 获取基础估值数据[5,9](@ref)
            df = ak.stock_index_pe_lg(name)
            df["指数代码"]=code
            df["指数名称"]=name

            # 生成批量数据（需要根据具体存储表来修改代码）
            batch_data = [
                        (row['指数代码'],row['指数名称'],row['日期'],row['指数'], 
                         None if pd.isna(row['等权静态市盈率']) else float(row['等权静态市盈率']),
                         None if pd.isna(row['静态市盈率']) else float(row['静态市盈率']),
                         None if pd.isna(row['静态市盈率中位数']) else float(row['静态市盈率中位数']),                         
                         None if pd.isna(row['等权滚动市盈率']) else float(row['等权滚动市盈率']),
                         None if pd.isna(row['滚动市盈率']) else float(row['滚动市盈率']),
                         None if pd.isna(row['滚动市盈率中位数']) else float(row['滚动市盈率中位数']))
                        for _, row in df.iterrows()
                        ]
            save_to_mysql.insert_to_mysql(batch_data,INSERT_SQL)
        except Exception as e:
            print(f"{name} 数据存储失败: {str(e)}")
    
    return "INSERT finished!"


if __name__ == "__main__":
    # 使用示例
    
    print(sys.path)  
    #df = insert_major_index_valuation()
    #df = ak.stock_index_pe_lg('沪深300')
    #df = df.iloc[0:2]

    #print(df)
