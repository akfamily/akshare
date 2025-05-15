import akshare as ak
import pandas as pd
from tqdm import tqdm

def standardize_stock_code(code):
    """代码标准化函数（兼容更多格式）"""
    code = str(code).strip().upper()
    if code.startswith(('SH', 'SZ')):  # 已有前缀则直接返回
        return code
    elif code.startswith(('6', '9', '5')):  # 沪市/科创板
        return f"SH{code.lstrip('SH')}"
    elif code.startswith(('0', '3', '2')):  # 深市/创业板
        return f"SZ{code.lstrip('SZ')}"
    else:
        return code

def get_hs300_stocks():
    """获取300成分股获取（兼容接口变更）"""
    try:
        # 新版接口可能返回不同字段名
        hs300 = ak.index_stock_cons(symbol="000300")
        # 兼容新旧字段名（网页3提到的字段差异）
        code_col = '品种代码' if '品种代码' in hs300.columns else '股票代码'
        name_col = '品种名称' if '品种名称' in hs300.columns else '股票简称'
        return hs300[[code_col, name_col]].rename(columns={code_col: '代码', name_col: '名称'})
    except Exception as e:
        print(f"接口获取失败: {str(e)}，尝试本地备份...")
        return pd.read_csv("hs300_backup.csv")

def get_financial_data(report_time="20231231"):
    """获取提取财报快讯计算营收和利润（使用stock_yjbb_em接口）"""
    # 1. 报告期格式处理（网页6要求）
    if len(report_time) != 8 or report_time[4:] not in ('0331', '0630', '0930', '1231'):
        report_time = "20231231"
        print(f"已自动修正报告期为: {report_time}")
    
    # 2. 批量获取全市场数据（网页1特性）
    try:
        full_data = ak.stock_yjbb_em(date=report_time)
        # 字段标准化（兼容接口变更）
        full_data['股票代码'] = full_data['股票代码'].astype(str).str.zfill(6)
        full_data = full_data.rename(columns={
            '股票代码':'代码',
            '股票简称':'简称',
            '营业总收入-营业总收入': '营业收入',
            '净利润-净利润': '净利润'
        })
    except Exception as e:
        print(f"接口调用失败: {str(e)}")
        return pd.DataFrame()

    # 3. 获取成分股并标准化代码
    hs300_stocks = get_hs300_stocks()
    #hs300_stocks['标准代码'] = hs300_stocks['代码'].apply(standardize_stock_code)
    
    # 4. 数据合并与筛选
    merged_df = pd.merge(
        hs300_stocks,
        full_data,
        left_on='代码',
        right_on='代码',
        how='inner'
    )
    
    # 5. 数据加工（网页3提到的单位转换）
    result_df = merged_df[['代码', '简称', '营业收入', '净利润']].copy()
    result_df['营收(亿元)'] = result_df['营业收入'] / 1e8  # 单位转换（网页1说明）
    result_df['净利润(亿元)'] = result_df['净利润'] / 1e8
    result_df['报告期'] = report_time
    
    # 6. 保存结果
    output_path = f".\output\HS300_核心财务数据_{report_time[:4]}.xlsx"
    result_df[['代码', '简称', '营收(亿元)', '净利润(亿元)', '报告期']].to_excel(output_path, index=False)
    return result_df

if __name__ == "__main__":
    """对比不同报告期数据"""
    report_times=["20231231", "20241231"]
    results = []
    for rt in report_times:
        df = get_financial_data(rt)
        if not df.empty:
            revenue = df['营收(亿元)'].sum()
            profit = df['净利润(亿元)'].sum()
            results.append({
                '报告期': rt[:4] + "年",
                '营收(亿元)': revenue,
                '营收同比': (revenue - results[-1]['营收(亿元)'])/results[-1]['营收(亿元)'] if len(results)>0 else 0,
                '净利润(亿元)': profit,
                '利润同比': (profit - results[-1]['净利润(亿元)'])/results[-1]['净利润(亿元)'] if len(results)>0 else 0
            })   
    print(pd.DataFrame(results))