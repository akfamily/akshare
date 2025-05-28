import time
import numpy as np
import akshare as ak
import pandas as pd
import datetime
import logging
import log4ak
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from getAllStock import get_all_stocks, get_select_stocks

log = log4ak.LogManager(log_level=logging.INFO)
MAX_CONSECUTIVE_ERRORS = 3  # 最大允许连续错误次数
OUTTIME = 5  # 接口长时间无返回报错


def selectStock():
    ## A 股上市公司列表
    stock_zh_a_spot_df = get_select_stocks()
    log.info("获取到 A 股上市公司列表")
    df_stock = stock_zh_a_spot_df[['代码','名称']]

    # 分块处理设置[2,3](@ref)
    total_rows = len(df_stock)
    chunk_num = 2
    chunk_indices = np.array_split(np.arange(total_rows), chunk_num)
    log.info(f"分块处理设置总记录数total_rows={total_rows}；块数chunk_num={chunk_num}，每块记录数chunk_indices={len(chunk_indices[0])}")

    # 初始化错误计数器（放在循环体外层）
    error_count = 0  # 连续错误计数器    

    # 分批处理逻辑
    for file_num, chunk_idx in enumerate(chunk_indices):
        
        chunk_df = df_stock.iloc[chunk_idx]
        df_result = pd.DataFrame(columns=['stock','name','指标1','指标2','指标3','指标4','综合评估'])
        log.info(f"开始处理第{file_num+1}批数据，包含{len(chunk_df)}条记录")
        checkcount = 0
        
        # 处理单个数据块
        for row_index, row in tqdm(chunk_df.iterrows(), total=len(chunk_df), desc=f"处理第{file_num+1}批\n"):
            try:
                r_code = row['代码']
                r_name = row['名称']
                checkcount += 1
                log.info(f"处理第{file_num+1}批第{checkcount}条记录：{r_code}")

                # 指标计算
                var1, var2, var3 = checkRoeCashEBIT(r_code, "2019")
                var4 = check_pe_condition(r_code)

                varAll = var1 and var2 and var3 and var4
                log.info(f"第{file_num+1}批第{checkcount}条记录处理结果varAll={varAll}")
                
                # 结果存储
                df_result.loc[row_index] = {
                    'stock': r_code,
                    'name': r_name,
                    '指标1': var1,
                    '指标2': var2,
                    '指标3': var3,
                    '指标4': var4,
                    '综合评估': varAll
                }
                error_count = 0  # 成功执行后重置计数器[6](@ref)
                log.info(f"功执行后重置计数器error_count={error_count}")
                time.sleep(2)
            except AttributeError as e:
                error_count += 1  # 捕获特定异常时计数[6](@ref)
                errormsg=f"股票{r_code}解析失败: {str(e)}。连续次数{error_count}"
                handle_error(r_code, e, errormsg, error_count)  # 封装错误处理
                if error_count >= MAX_CONSECUTIVE_ERRORS:
                    break  # 达到阈值终止循环                
            except ValueError as e:
                error_count += 1  # 捕获特定异常时计数[6](@ref)
                errormsg=f"股票{r_code}表格缺失: {str(e)}。连续次数{error_count}"
                handle_error(r_code, e, errormsg, error_count)  # 封装错误处理
                if error_count >= MAX_CONSECUTIVE_ERRORS:
                    break  # 达到阈值终止循环
            except Exception as e:
                error_count += 1  # 捕获特定异常时计数[6](@ref)
                errormsg=f"处理{row['代码']}时出错：{str(e)}。连续次数{error_count}"
                handle_error(r_code, e, errormsg, error_count)  # 封装错误处理
                if error_count >= MAX_CONSECUTIVE_ERRORS:
                    break  # 达到阈值终止循环
        
        # 分块存储[1,5](@ref)
        df_result.to_excel(f'.\output\stock_result_{file_num}.xlsx', index=False)
        log.info(f"第{file_num+1}批数据已存储，包含{len(df_result)}条记录")
    
    return "所有分块处理完成"

def checkRoeCashEBIT(r_code = "601398",startyear = "2019"):
    #财务指标数据 工行财报
    # 获取最新接口调用添加精确的超时控制
    try:
        log.info(f"{r_code}获取{startyear}至今财报数据")
        
        # 添加超时控制（网页[1][1](@ref)推荐方法）
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(ak.stock_financial_analysis_indicator, symbol=r_code, start_year=startyear)
            df = future.result(timeout=OUTTIME)  # 设置5秒超时[1,8](@ref)
    
    except TimeoutError:
        log.error(f"接口调用超时：5秒未返回数据 | 股票代码：{stock_code}")
        return False
    except Exception as e:
        log.error(f"接口调用失败: {str(e)}")
        return False
    log.debug(f"{r_code}获取到财报信息")
    clean_df = df.copy()

    # 数据清洗
    # 日期转换与格式校验
    clean_df['日期'] = pd.to_datetime(
        clean_df['日期'],
        errors='coerce'  # 无效日期转为NaT（网页[2]建议）
        )
    # 筛选有效年报
    year_end_mask = (
        (clean_df['日期'].dt.month == 12) & 
        (clean_df['日期'].dt.day == 31) & 
        (clean_df['日期'].notna())
        )
    clean_df = clean_df[year_end_mask]

    # 按年排序与截取
    clean_df = clean_df.sort_values('日期', ascending=False)
    
    clean_df = clean_df.set_index(clean_df['日期'])
    log.debug(f"{r_code}筛选后年报信息：\n {clean_df['日期']}")

    #指标1 - 过去5年来平均净资产收益率高于14%
    df1 = clean_df['净资产收益率(%)']
    df1_sum = df1.replace('--',0).astype(float).sum(axis = 0, skipna = True)
    df1_count = df1.count()
    var1 = (df1_sum / df1_count)>14
    log.debug(f"{r_code}获取var1={var1}")

    #指标2：经营现金流为正
    df2=clean_df['每股经营性现金流(元)']
    var2 = float( df2.iat[0] ) > 0
    log.debug(f"{r_code}获取var2={var2}")

    
    #指标3：新期的净利润大于前5年的净利润 取万元 
    clean_df['扣非净利润'] = (
        pd.to_numeric(clean_df['扣除非经常性损益后的净利润(元)'], errors='coerce')
        .div(10000)  # 元转万元
        .dropna()     # 过滤无效数据
    )
    df3=clean_df['扣非净利润']

    # 获取最新一期数据
    latest = df3.iloc[0]  # 索引0为最新数据

    # 获取前五年数据（索引1-5为前1至前5年）
    past_5years = df3.iloc[1:6]  # 含1不含6

    # 计算逻辑
    var3 = latest > past_5years.max()
    log.info(f"{r_code}获取var1,var2,var3={var1},{var2},{var3}")

    return var1,var2,var3

## 指标4- 市盈率低于20且大于0
def check_pe_condition(stock_code="601398", pastday=30):
    # 获取最新接口调用添加精确的超时控制
    try:
        log.info(f"{stock_code}获取{pastday}天内有效市盈率数据")
        
        # 添加超时控制（网页[1][1](@ref)推荐方法）
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(ak.stock_a_indicator_lg, symbol=stock_code)
            df = future.result(timeout=OUTTIME)  # 设置5秒超时[1,8](@ref)
    
    except TimeoutError:
        log.error(f"接口调用超时：5秒未返回数据 | 股票代码：{stock_code}")
        return False
    except Exception as e:
        log.error(f"接口调用失败: {str(e)}")
        return False
    
    # 日期处理优化（网页[3][3](@ref)数据格式）
    date_threshold = datetime.datetime.now() - datetime.timedelta(pastday)
    date_threshold = date_threshold.date()
    
    # 数据清洗与计算（网页[1][1](@ref)字段说明）
    try:
        valid_df = df[
            (pd.to_datetime(df['trade_date']).dt.date > date_threshold) 
            & (df['pe'].notna())
        ]
    except KeyError as ke:
        log.error(f"数据字段缺失：{str(ke)} | 请确认接口返回格式")
        return False
        
    if valid_df.empty:
        log.info(f"{stock_code}无近期有效市盈率数据")
        return "NAN"
    
    # 计算逻辑优化（网页[1][1](@ref)数据处理建议）
    try:
        pe_mean = valid_df['pe'].astype(float).mean()
        var4 = 0 < pe_mean < 20       
        log.info(f"{stock_code}获取var4={var4}")
        return var4
    except ValueError as ve:
        log.error(f"市盈率数据类型错误：{str(ve)}")
        return False


def handle_error(code: str, e: Exception, error_msg: str, counter: int):
    """统一处理错误日志和阈值判断"""
    log.error(error_msg)
    time.sleep(2)  # 错误后延迟防止高频请求[6](@ref)
    
    # 触发连续错误异常
    if counter >= MAX_CONSECUTIVE_ERRORS:
        raise ConsecutiveErrorException(
            error_code=5001,
            message=f"连续{counter}次接口异常，服务终止"
        )

class ConsecutiveErrorException(Exception):
    """连续异常超过阈值时触发"""
    def __init__(self, error_code: int, message: str):
        self.error_code = error_code  # 如 5001
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    #time.sleep(600)
    #df = selectStock()
    df=checkRoeCashEBIT("301459")
    print(df)
    #导出Excel并自动调整列宽[4](@ref)
    df.to_excel(f'.\output\output.xlsx', index=False)
    #selectStock()