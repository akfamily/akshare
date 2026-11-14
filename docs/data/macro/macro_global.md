# 宏观数据-全球与重要机构

## 全球宏观

(macro_calendar_ws)=
### 宏观日历

接口：macro_calendar_ws

目标地址：https://wallstreetcn.com/calendar

描述：华尔街见闻-日历-宏观

限量：单次返回指定 date 的数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20240514" |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 时间  | str     | -  |
| 地区  | str     | -  |
| 事件  | str     | -  |
| 重要性 | int64   | -  |
| 今值  | float64 | -  |
| 预期  | float64 | -  |
| 前值  | float64 | -  |
| 链接  | str     | -  |

接口示例

```python
import akshare as ak

macro_calendar_ws_df = ak.macro_calendar_ws(date="20240514")
print(macro_calendar_ws_df)
```

数据示例

```
                     时间  ...                                                 链接
0   2024-05-14 01:00:00  ...
1   2024-05-14 07:50:00  ...  https://wallstreetcn.com/calendar/JP111746/ove...
2   2024-05-14 07:50:00  ...  https://wallstreetcn.com/calendar/JP111747/ove...
3   2024-05-14 10:00:00  ...
4   2024-05-14 12:02:00  ...
5   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121576/ove...
6   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121563/ove...
7   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121574/ove...
8   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121573/ove...
9   2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121578/ove...
10  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/UK121577/ove...
11  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112128/ove...
12  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112139/ove...
13  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112152/ove...
14  2024-05-14 14:00:00  ...  https://wallstreetcn.com/calendar/DE112151/ove...
15  2024-05-14 17:00:00  ...  https://wallstreetcn.com/calendar/EA152021/ove...
16  2024-05-14 17:00:00  ...  https://wallstreetcn.com/calendar/DE152230/ove...
17  2024-05-14 17:00:00  ...  https://wallstreetcn.com/calendar/DE152229/ove...
18  2024-05-14 18:00:00  ...  https://wallstreetcn.com/calendar/US151153/ove...
19  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111043/ove...
20  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111042/ove...
21  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111049/ove...
22  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/US111048/ove...
23  2024-05-14 20:30:00  ...  https://wallstreetcn.com/calendar/CA173202/ove...
24  2024-05-14 21:15:00  ...
25  2024-05-14 22:00:00  ...
26  2024-05-15 00:00:00  ...
27  2024-05-15 00:00:00  ...
[28 rows x 8 columns]
```

(macro_calendar_baidu)=
### 全球宏观事件

接口：macro_calendar_baidu

目标地址：https://gushitong.baidu.com/calendar

描述：全球宏观指标重大事件

限量：单次返回指定 date 的所有历史数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20241107" |
| cookie | str | cookie=None；百度股市通的 Cookie，默认自动获取 |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  | -       |
| 时间  | str     | -       |
| 地区  | str     | -       |
| 事件  | str     | -       |
| 公布  | float64 | -       |
| 预期  | float64 | -       |
| 前值  | float64 | -       |
| 重要性 | float64 | 数值越大越重要 |

接口示例

```python
import akshare as ak

macro_calendar_baidu_df = ak.macro_calendar_baidu(date="20241107")
print(macro_calendar_baidu_df)
```

数据示例

```
        日期     时间   地区  ...      预期       前值  重要性
0   2024-11-07  01:30   巴西  ...     NaN      -16.72    1
1   2024-11-07  02:00   巴西  ...   49.76       50.23    1
2   2024-11-07  05:30   巴西  ...   11.25       10.75    1
3   2024-11-07  06:30   美国  ...     NaN  3091171.16    1
4   2024-11-07  06:30   美国  ...     NaN     6004.39    1
..         ...    ...  ...  ...     ...         ...  ...
95  2024-11-07  20:00   英国  ...    4.75        5.00    2
96  2024-11-07  21:00  俄罗斯  ...     NaN     6285.00    1
97  2024-11-07  21:00   巴西  ...     NaN      -11.40    1
98  2024-11-07  21:00   巴西  ...     NaN       -0.40    1
99  2024-11-07  21:30   美国  ...  187.50      186.20    2
[100 rows x 8 columns]
```
