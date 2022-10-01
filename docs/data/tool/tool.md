## [AKShare](https://github.com/akfamily/akshare) 工具箱

### 交易日历

接口: tool_trade_date_hist_sina

目标地址: https://finance.sina.com.cn/realstock/company/klc_td_sh.txt

描述: 新浪财经的股票交易日历数据

限量: 单次返回从 1990-12-19 到 2022-12-30 之间的股票交易日历数据, 这里补充 1992-05-04 进入交易日

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型     | 描述                                                        |
|------------|--------|-----------------------------------------------------------|
| trade_date | object | 从 1990-12-19 至 2022-12-30 的股票交易日数据; 这里补充 1992-05-04 进入交易日 |

接口示例

```python
import akshare as ak

tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
print(tool_trade_date_hist_sina_df)
```

数据示例

```
      trade_date
0     1990-12-19
1     1990-12-20
2     1990-12-21
3     1990-12-24
4     1990-12-25
          ...
7823  2022-12-26
7824  2022-12-27
7825  2022-12-28
7826  2022-12-29
7827  2022-12-30
```
