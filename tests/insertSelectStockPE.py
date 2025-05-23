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
import insert2Mysql as ins

log = log4ak.LogManager(log_level=logging.INFO)
MAX_CONSECUTIVE_ERRORS = 3  # 最大允许连续错误次数
OUTTIME = 5  # 接口长时间无返回报错
SELECT_PATH=r"..\input\selectlist.xlsx"

INSERT_SQL ="""
    INSERT IGNORE INTO `stock_pe_history` 
    (`stock_code`,`stock_name`,`trade_date`, `pe`, `pe_ttm`, `pb`, `dv_ratio`, `dv_ttm`, `ps`, `ps_ttm`, `total_mv`)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

def insertSelectStockPE(path = SELECT_PATH):
    ## 存入所选的A股上市公司历史PE

    stock_zh_a_spot_df = get_select_stocks(path)
    log.info("获取到所选的 A 股上市公司列表")
    df_stock = stock_zh_a_spot_df[['代码','名称']]

    # 分块处理设置[2,3](@ref)
    total_rows = len(df_stock)
    chunk_num = 1
    chunk_indices = np.array_split(np.arange(total_rows), chunk_num)
    log.info(f"分块处理设置总记录数total_rows={total_rows}；块数chunk_num={chunk_num}，每块记录数chunk_indices={len(chunk_indices[0])}")
    df_result = pd.DataFrame(columns=['stock_code','stock_name','trade_date','pe','pe_ttm','pb', 'dv_ratio', 'dv_ttm', 'ps', 'ps_ttm', 'total_mv'])
        

    # 初始化错误计数器（放在循环体外层）
    error_count = 0  # 连续错误计数器    

    # 分批处理逻辑
    for file_num, chunk_idx in enumerate(chunk_indices):
        
        chunk_df = df_stock.iloc[chunk_idx]
        log.info(f"开始处理第{file_num+1}批数据，包含{len(chunk_df)}条记录")
        checkcount = 0
        
        # 处理单个数据块
        for row_index, row in tqdm(chunk_df.iterrows(), total=len(chunk_df), desc=f"处理第{file_num+1}批\n"):
            try:
                r_code = row['代码']
                r_name = row['名称']
                checkcount += 1
                log.info(f"处理第{file_num+1}批第{checkcount}条记录：{r_code}")

                # 获取股票历史PE
                dfpe=get_pe_condition(r_code)
                log.debug(f"获取到{r_code}历史PE，数据块:{dfpe}")

                # 使用assign实现向量化赋值
                dfpe = dfpe.assign(**{
                    'stock_code': r_code,
                    'stock_name': r_name
                    })

                #数据合并
                df_result = pd.concat([df_result, dfpe], ignore_index=True)
                log.info(f"df_result数据块合并后大小为:{len(df_result)}")

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

        log.info(f"第{file_num+1}批数据已获取，包含{len(df_result)}条记录")

    # 生成批量数据（需要根据具体存储表来修改代码）
    batch_data = [
                (row['stock_code'],row['stock_name'],row['trade_date'],
                    None if pd.isna(row['pe']) else float(row['pe']),
                    None if pd.isna(row['pe_ttm']) else float(row['pe_ttm']),
                    None if pd.isna(row['pb']) else float(row['pb']),                         
                    None if pd.isna(row['dv_ratio']) else float(row['dv_ratio']),
                    None if pd.isna(row['dv_ttm']) else float(row['dv_ttm']),
                    None if pd.isna(row['ps']) else float(row['ps']),
                    None if pd.isna(row['ps_ttm']) else float(row['ps_ttm']),
                    None if pd.isna(row['total_mv']) else float(row['total_mv']))
                for _, row in df_result.iterrows()
                ]
    log.info(f"所有数据已获取，并封装为{len(batch_data)}条记录")

    ins.insert_to_mysql(batch_data,INSERT_SQL)
    #ins.insert_to_mysql(dfpe,INSERT_SQL)
    return "所有分块处理完成"



def get_pe_condition(stock_code="601398"):
    # 获取历史PE信息
    try:
        log.info(f"{stock_code}获取有效市盈率数据")
        
        # 添加超时控制（网页[1][1](@ref)推荐方法）
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(ak.stock_a_indicator_lg, symbol=stock_code)
            df = future.result(timeout=OUTTIME)  # 设置5秒超时[1,8](@ref)
            return df
    
    except TimeoutError:
        log.error(f"接口调用超时：5秒未返回数据 | 股票代码：{stock_code}")
        return False
    except Exception as e:
        log.error(f"接口调用失败: {str(e)}")
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
    df = insertSelectStockPE(SELECT_PATH)
    #导出Excel并自动调整列宽[4](@ref)
    #with pd.ExcelWriter(".\output\output.xlsx") as writer:
    #    df.to_excel(writer, sheet_name="全量数据")
    #selectStock()