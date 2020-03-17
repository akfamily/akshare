# 时间序列与日期用法

依托 NumPy 的 `datetime64`、`timedelta64` 等数据类型，Pandas 可以处理各种时间序列数据，还能调用 `scikits.timeseries` 等 Python 支持库的时间序列功能。

Pandas 支持以下操作：

解析 `时间字符串`、`np.datetime64`、`datetime.datetime` 等多种时间序列数据。

```python
In [1]: import datetime

In [2]: dti = pd.to_datetime(['1/1/2018', np.datetime64('2018-01-01'),
   ...:                       datetime.datetime(2018, 1, 1)])
   ...: 

In [3]: dti
Out[3]: DatetimeIndex(['2018-01-01', '2018-01-01', '2018-01-01'], dtype='datetime64[ns]', freq=None)
```

生成 ` DatetimeIndex `、`TimedeltaIndex `、` PeriodIndex ` 等定频日期与时间段序列。

```python
In [4]: dti = pd.date_range('2018-01-01', periods=3, freq='H')

In [5]: dti
Out[5]: 
DatetimeIndex(['2018-01-01 00:00:00', '2018-01-01 01:00:00',
               '2018-01-01 02:00:00'],
              dtype='datetime64[ns]', freq='H')
```

处理、转换带时区的日期时间数据。

```python
In [6]: dti = dti.tz_localize('UTC')

In [7]: dti
Out[7]: 
DatetimeIndex(['2018-01-01 00:00:00+00:00', '2018-01-01 01:00:00+00:00',
               '2018-01-01 02:00:00+00:00'],
              dtype='datetime64[ns, UTC]', freq='H')

In [8]: dti.tz_convert('US/Pacific')
Out[8]: 
DatetimeIndex(['2017-12-31 16:00:00-08:00', '2017-12-31 17:00:00-08:00',
               '2017-12-31 18:00:00-08:00'],
              dtype='datetime64[ns, US/Pacific]', freq='H')
```

按指定频率重采样，并转换为时间序列。

```python
In [9]: idx = pd.date_range('2018-01-01', periods=5, freq='H')

In [10]: ts = pd.Series(range(len(idx)), index=idx)

In [11]: ts
Out[11]: 
2018-01-01 00:00:00    0
2018-01-01 01:00:00    1
2018-01-01 02:00:00    2
2018-01-01 03:00:00    3
2018-01-01 04:00:00    4
Freq: H, dtype: int64

In [12]: ts.resample('2H').mean()
Out[12]: 
2018-01-01 00:00:00    0.5
2018-01-01 02:00:00    2.5
2018-01-01 04:00:00    4.0
Freq: 2H, dtype: float64
```

用绝对或相对时间差计算日期与时间。

```python
In [13]: friday = pd.Timestamp('2018-01-05')

In [14]: friday.day_name()
Out[14]: 'Friday'

# 添加 1 个日历日
In [15]: saturday = friday + pd.Timedelta('1 day')

In [16]: saturday.day_name()
Out[16]: 'Saturday'

# 添加 1 个工作日，从星期五跳到星期一
In [17]: monday = friday + pd.offsets.BDay()

In [18]: monday.day_name()
Out[18]: 'Monday'
```

Pandas 提供了一组精悍、实用的工具集以完成上述操作。

## 时间序列纵览

Pandas 支持 4 种常见时间概念：

1. 日期时间（Datetime）：带时区的日期时间，类似于标准库的 `datetime.datetime` 。

2. 时间差（Timedelta）：绝对时间周期，类似于标准库的 `datetime.timedelta`。

3. 时间段（Timespan）：在某一时点以指定频率定义的时间跨度。

4. 日期偏移（Dateoffset）：与日历运算对应的时间段，类似于 `dateutil` 的 `dateutil.relativedelta.relativedelta`。


|   时间概念   |    标量类    |      数组类      |             Pandas 数据类型             |            主要构建方法             |
| :----------: | :----------: | :--------------: | :-------------------------------------: | :---------------------------------: |
|  Date times  | `Timestamp`  | `DatetimeIndex`  | `datetime64[ns]` 或 `datetime64[ns,tz]` |    `to_datetime` 或 `date_range`    |
| Time deltas  | `Timedelta`  | `TimedeltaIndex` |            `timedelta64[ns]`            | `to_timedelta` 或 `timedelta_range` |
|  Time spans  |   `Period`   |  `PeriodIndex`   |             `period[freq]`              |     `Period` 或 `period_range`      |
| Date offsets | `DateOffset` |      `None`      |                 `None`                  |            `DateOffset`             |

一般情况下，时间序列主要是 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 或 [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame") 的时间型索引，可以用时间元素进行操控。

```python
In [19]: pd.Series(range(3), index=pd.date_range('2000', freq='D', periods=3))
Out[19]: 
2000-01-01    0
2000-01-02    1
2000-01-03    2
Freq: D, dtype: int64
```

当然，[`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 与 [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame") 也可以直接把时间序列当成数据。

```python
In [20]: pd.Series(pd.date_range('2000', freq='D', periods=3))
Out[20]: 
0   2000-01-01
1   2000-01-02
2   2000-01-03
dtype: datetime64[ns]
```

[`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 与 [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame") 提供了 `datetime`、`timedelta` 、`Period` 扩展类型与专有用法，不过，`Dateoffset` 则保存为 `object`。

```python
In [21]: pd.Series(pd.period_range('1/1/2011', freq='M', periods=3))
Out[21]: 
0    2011-01
1    2011-02
2    2011-03
dtype: period[M]

In [22]: pd.Series([pd.DateOffset(1), pd.DateOffset(2)])
Out[22]: 
0         <DateOffset>
1    <2 * DateOffsets>
dtype: object

In [23]: pd.Series(pd.date_range('1/1/2011', freq='M', periods=3))
Out[23]: 
0   2011-01-31
1   2011-02-28
2   2011-03-31
dtype: datetime64[ns]
```

Pandas 用 `NaT` 表示日期时间、时间差及时间段的空值，代表了缺失日期或空日期的值，类似于浮点数的 `np.nan`。

```python
In [24]: pd.Timestamp(pd.NaT)
Out[24]: NaT

In [25]: pd.Timedelta(pd.NaT)
Out[25]: NaT

In [26]: pd.Period(pd.NaT)
Out[26]: NaT

# 与 np.nan 一样，pd.NaT 不等于 pd.NaT 
In [27]: pd.NaT == pd.NaT
Out[27]: False
```

## 时间戳 vs. 时间段

时间戳是最基本的时间序列数据，用于把数值与时点关联在一起。Pandas 对象通过时间戳调用时点数据。

```python
In [28]: pd.Timestamp(datetime.datetime(2012, 5, 1))
Out[28]: Timestamp('2012-05-01 00:00:00')

In [29]: pd.Timestamp('2012-05-01')
Out[29]: Timestamp('2012-05-01 00:00:00')

In [30]: pd.Timestamp(2012, 5, 1)
Out[30]: Timestamp('2012-05-01 00:00:00')
```

不过，大多数情况下，用时间段改变变量更自然。`Period` 表示的时间段更直观，还可以用日期时间格式的字符串进行推断。

示例如下：

```python
In [31]: pd.Period('2011-01')
Out[31]: Period('2011-01', 'M')

In [32]: pd.Period('2012-05', freq='D')
Out[32]: Period('2012-05-01', 'D')
```

[`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 与 [`Period`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Period.html#pandas.Period "pandas.Period") 可以用作索引。作为索引的 `Timestamp` 与 `Period` 列表则被强制转换为对应的 [`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 与 [`PeriodIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.PeriodIndex.html#pandas.PeriodIndex "pandas.PeriodIndex")。

```python
In [33]: dates = [pd.Timestamp('2012-05-01'),
   ....:          pd.Timestamp('2012-05-02'),
   ....:          pd.Timestamp('2012-05-03')]
   ....: 

In [34]: ts = pd.Series(np.random.randn(3), dates)

In [35]: type(ts.index)
Out[35]: pandas.core.indexes.datetimes.DatetimeIndex

In [36]: ts.index
Out[36]: DatetimeIndex(['2012-05-01', '2012-05-02', '2012-05-03'], dtype='datetime64[ns]', freq=None)

In [37]: ts
Out[37]: 
2012-05-01    0.469112
2012-05-02   -0.282863
2012-05-03   -1.509059
dtype: float64

In [38]: periods = [pd.Period('2012-01'), pd.Period('2012-02'), pd.Period('2012-03')]

In [39]: ts = pd.Series(np.random.randn(3), periods)

In [40]: type(ts.index)
Out[40]: pandas.core.indexes.period.PeriodIndex

In [41]: ts.index
Out[41]: PeriodIndex(['2012-01', '2012-02', '2012-03'], dtype='period[M]', freq='M')

In [42]: ts
Out[42]: 
2012-01   -1.135632
2012-02    1.212112
2012-03   -0.173215
Freq: M, dtype: float64
```

Pandas 可以识别这两种表现形式，并在两者之间进行转化。Pandas 后台用 `Timestamp` 实例代表时间戳，用 `DatetimeIndex` 实例代表时间戳序列。Pandas 用 `Period` 对象表示符合规律的时间段标量值，用 `PeriodIndex` 表示时间段序列。未来版本会支持用任意起止时间实现不规律时间间隔。

## 转换时间戳

`to_datetime` 函数用于转换字符串、纪元式及混合的日期 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 或日期列表。转换 `Series`，返回具有相同索引的 `Series`，日期时间列表被转换为 `DatetimeIndex`：

```python
In [43]: pd.to_datetime(pd.Series(['Jul 31, 2009', '2010-01-10', None]))
Out[43]: 
0   2009-07-31
1   2010-01-10
2          NaT
dtype: datetime64[ns]

In [44]: pd.to_datetime(['2005/11/23', '2010.12.31'])
Out[44]: DatetimeIndex(['2005-11-23', '2010-12-31'], dtype='datetime64[ns]', freq=None)
```

解析欧式日期（日-月-年），要用 `dayfirst` 关键字参数：

```python
In [45]: pd.to_datetime(['04-01-2012 10:00'], dayfirst=True)
Out[45]: DatetimeIndex(['2012-01-04 10:00:00'], dtype='datetime64[ns]', freq=None)

In [46]: pd.to_datetime(['14-01-2012', '01-14-2012'], dayfirst=True)
Out[46]: DatetimeIndex(['2012-01-14', '2012-01-14'], dtype='datetime64[ns]', freq=None)
```

::: danger 警告

从上例可以看出，`dayfirst` 并不严苛，如果不能把第一个数解析为**日**，就会以 `dayfirst` 为 `False` 进行解析。

:::

`to_datetime` 转换单个字符串时，返回单个 `Timestamp`。`Timestamp` 仅支持字符串输入，不支持 `dayfirst`、`format` 等字符串解析选项，如果要使用这些选项，就要用 `to_datetime`。

```python
In [47]: pd.to_datetime('2010/11/12')
Out[47]: Timestamp('2010-11-12 00:00:00')

In [48]: pd.Timestamp('2010/11/12')
Out[48]: Timestamp('2010-11-12 00:00:00')
```

Pandas 还支持直接使用 `DatetimeIndex` 构建器：

```python
In [49]: pd.DatetimeIndex(['2018-01-01', '2018-01-03', '2018-01-05'])
Out[49]: DatetimeIndex(['2018-01-01', '2018-01-03', '2018-01-05'], dtype='datetime64[ns]', freq=None)
```

创建 `DatetimeIndex` 时，传递字符串 `infer` 可推断索引的频率。

```python
In [50]: pd.DatetimeIndex(['2018-01-01', '2018-01-03', '2018-01-05'], freq='infer')
Out[50]: DatetimeIndex(['2018-01-01', '2018-01-03', '2018-01-05'], dtype='datetime64[ns]', freq='2D')
```

### 提供格式参数

要实现精准转换，除了传递 `datetime` 字符串，还要指定 `format` 参数，指定此参数还可以加速转换速度。

```python
In [51]: pd.to_datetime('2010/11/12', format='%Y/%m/%d')
Out[51]: Timestamp('2010-11-12 00:00:00')

In [52]: pd.to_datetime('12-11-2010 00:00', format='%d-%m-%Y %H:%M')
Out[52]: Timestamp('2010-11-12 00:00:00')
```

要了解更多 `format` 选项，请参阅 Python [日期时间文档](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)。

### 用多列组合日期时间

*0.18.1 版新增。*

Pandas 还可以把 `DataFrame` 里的整数或字符串列组合成 `Timestamp Series`。

```python
In [53]: df = pd.DataFrame({'year': [2015, 2016],
   ....:                    'month': [2, 3],
   ....:                    'day': [4, 5],
   ....:                    'hour': [2, 3]})
   ....: 

In [54]: pd.to_datetime(df)
Out[54]: 
0   2015-02-04 02:00:00
1   2016-03-05 03:00:00
dtype: datetime64[ns]
```

只传递组合所需的列也可以。

```python
In [55]: pd.to_datetime(df[['year', 'month', 'day']])
Out[55]: 
0   2015-02-04
1   2016-03-05
dtype: datetime64[ns]
```

`pd.to_datetime` 查找列名里日期时间组件的标准名称，包括：

  * 必填：`year`、`month`、`day`
  * 可选：`hour`、`minute`、`second`、`millisecond`、`microsecond`、`nanosecond`

### 无效数据

不可解析时，默认值 `errors='raise'` 会触发错误：

```python
In [2]: pd.to_datetime(['2009/07/31', 'asd'], errors='raise')
ValueError: Unknown string format
```

`errors='ignore'` 返回原始输入：

```python
In [56]: pd.to_datetime(['2009/07/31', 'asd'], errors='ignore')
Out[56]: Index(['2009/07/31', 'asd'], dtype='object')
```

`errors='coerce'` 把无法解析的数据转换为 `NaT`，即不是时间（Not a Time）：

```python
In [57]: pd.to_datetime(['2009/07/31', 'asd'], errors='coerce')
Out[57]: DatetimeIndex(['2009-07-31', 'NaT'], dtype='datetime64[ns]', freq=None)
```

### 纪元时间戳

Pandas 支持把整数或浮点数纪元时间转换为 `Timestamp` 与 `DatetimeIndex`。鉴于 `Timestamp` 对象内部存储方式，这种转换的默认单位是纳秒。不过，一般都会用指定其它时间单位 `unit` 来存储纪元数据，纪元时间从 `origin` 参数指定的时点开始计算。

```python
In [58]: pd.to_datetime([1349720105, 1349806505, 1349892905,
   ....:                 1349979305, 1350065705], unit='s')
   ....: 
Out[58]: 
DatetimeIndex(['2012-10-08 18:15:05', '2012-10-09 18:15:05',
               '2012-10-10 18:15:05', '2012-10-11 18:15:05',
               '2012-10-12 18:15:05'],
              dtype='datetime64[ns]', freq=None)

In [59]: pd.to_datetime([1349720105100, 1349720105200, 1349720105300,
   ....:                 1349720105400, 1349720105500], unit='ms')
   ....: 
Out[59]: 
DatetimeIndex(['2012-10-08 18:15:05.100000', '2012-10-08 18:15:05.200000',
               '2012-10-08 18:15:05.300000', '2012-10-08 18:15:05.400000',
               '2012-10-08 18:15:05.500000'],
              dtype='datetime64[ns]', freq=None)
```

用带 `tz` 参数的纪元时间戳创建 [`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 或 [`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 时，要先把纪元时间戳转化为 UTC，然后再把结果转换为指定时区。不过这种操作方式现在已经[废弃](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.24.0.html#whatsnew-0240-deprecations-integer-tz)了，对于其它时区 Wall Time 里的纪元时间戳，建议先把纪元时间戳转换为无时区时间戳，再本地化时区。

```python
In [60]: pd.Timestamp(1262347200000000000).tz_localize('US/Pacific')
Out[60]: Timestamp('2010-01-01 12:00:00-0800', tz='US/Pacific')

In [61]: pd.DatetimeIndex([1262347200000000000]).tz_localize('US/Pacific')
Out[61]: DatetimeIndex(['2010-01-01 12:00:00-08:00'], dtype='datetime64[ns, US/Pacific]', freq=None)
```

::: tip 注意

纪元时间取整到最近的纳秒。

::: 

::: danger 警告

[Python 浮点数](https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues "(in Python v3.7)")只精确到 15 位小数，因此，转换浮点纪元时间可能会导致不精准或失控的结果。转换过程中，免不了对高精度 `Timestamp` 取整，只有用 `int64` 等定宽类型才有可能实现极其精准的效果。

```python
In [62]: pd.to_datetime([1490195805.433, 1490195805.433502912], unit='s')
Out[62]: DatetimeIndex(['2017-03-22 15:16:45.433000088', '2017-03-22 15:16:45.433502913'], dtype='datetime64[ns]', freq=None)

In [63]: pd.to_datetime(1490195805433502912, unit='ns')
Out[63]: Timestamp('2017-03-22 15:16:45.433502912')
```
:::

::: tip 参阅

[应用 `origin` 参数](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-origin)

:::

### 把时间戳转换为纪元

反转上述操作，把 `Timestamp` 转换为 `unix` 纪元：

```python
In [64]: stamps = pd.date_range('2012-10-08 18:15:05', periods=4, freq='D')

In [65]: stamps
Out[65]: 
DatetimeIndex(['2012-10-08 18:15:05', '2012-10-09 18:15:05',
               '2012-10-10 18:15:05', '2012-10-11 18:15:05'],
              dtype='datetime64[ns]', freq='D')
```

首先与纪元开始时点（1970 年 1 月 1 日午夜，UTC）相减，然后以 1 秒为时间单位（`unit='1s'`）取底整除。

```python
In [66]: (stamps - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
Out[66]: Int64Index([1349720105, 1349806505, 1349892905, 1349979305], dtype='int64')
```

### 应用 `origin` 参数

*0.20.0 版新增。*

`origin` 参数可以指定 `DatetimeIndex` 的备选开始时点。例如，把`1960-01-01` 作为开始日期：

```python
In [67]: pd.to_datetime([1, 2, 3], unit='D', origin=pd.Timestamp('1960-01-01'))
Out[67]: DatetimeIndex(['1960-01-02', '1960-01-03', '1960-01-04'], dtype='datetime64[ns]', freq=None)
```

默认值为 `origin='unix'`，即 `1970-01-01 00:00:00`，一般把这个时点称为 `unix 纪元` 或 `POSIX` 时间。

```python
In [68]: pd.to_datetime([1, 2, 3], unit='D')
Out[68]: DatetimeIndex(['1970-01-02', '1970-01-03', '1970-01-04'], dtype='datetime64[ns]', freq=None)
```

## 生成时间戳范围

`DatetimeIndex`、`Index` 构建器可以生成时间戳索引，此处要提供 `datetime` 对象列表。

```python
In [69]: dates = [datetime.datetime(2012, 5, 1),
   ....:          datetime.datetime(2012, 5, 2),
   ....:          datetime.datetime(2012, 5, 3)]
   ....: 

# 注意频率信息
In [70]: index = pd.DatetimeIndex(dates)

In [71]: index
Out[71]: DatetimeIndex(['2012-05-01', '2012-05-02', '2012-05-03'], dtype='datetime64[ns]', freq=None)

# 自动转换为 DatetimeIndex
In [72]: index = pd.Index(dates)

In [73]: index
Out[73]: DatetimeIndex(['2012-05-01', '2012-05-02', '2012-05-03'], dtype='datetime64[ns]', freq=None)
```

实际工作中，生成大量时间戳的超长索引时，一个个输入时间戳又枯燥，又低效。如果时间戳是定频的，用 [`date_range()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html#pandas.date_range "pandas.date_range") 与 [`bdate_range()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.bdate_range.html#pandas.bdate_range "pandas.bdate_range") 函数即可创建 `DatetimeIndex`。`date_range` 默认的频率是**日历日**，`bdate_range` 的默认频率是**工作日**：

```python
In [74]: start = datetime.datetime(2011, 1, 1)

In [75]: end = datetime.datetime(2012, 1, 1)

In [76]: index = pd.date_range(start, end)

In [77]: index
Out[77]: 
DatetimeIndex(['2011-01-01', '2011-01-02', '2011-01-03', '2011-01-04',
               '2011-01-05', '2011-01-06', '2011-01-07', '2011-01-08',
               '2011-01-09', '2011-01-10',
               ...
               '2011-12-23', '2011-12-24', '2011-12-25', '2011-12-26',
               '2011-12-27', '2011-12-28', '2011-12-29', '2011-12-30',
               '2011-12-31', '2012-01-01'],
              dtype='datetime64[ns]', length=366, freq='D')

In [78]: index = pd.bdate_range(start, end)

In [79]: index
Out[79]: 
DatetimeIndex(['2011-01-03', '2011-01-04', '2011-01-05', '2011-01-06',
               '2011-01-07', '2011-01-10', '2011-01-11', '2011-01-12',
               '2011-01-13', '2011-01-14',
               ...
               '2011-12-19', '2011-12-20', '2011-12-21', '2011-12-22',
               '2011-12-23', '2011-12-26', '2011-12-27', '2011-12-28',
               '2011-12-29', '2011-12-30'],
              dtype='datetime64[ns]', length=260, freq='B')
```

`date_range`、`bdate_range` 等便捷函数可以调用各种[频率别名](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases)：

```python
In [80]: pd.date_range(start, periods=1000, freq='M')
Out[80]: 
DatetimeIndex(['2011-01-31', '2011-02-28', '2011-03-31', '2011-04-30',
               '2011-05-31', '2011-06-30', '2011-07-31', '2011-08-31',
               '2011-09-30', '2011-10-31',
               ...
               '2093-07-31', '2093-08-31', '2093-09-30', '2093-10-31',
               '2093-11-30', '2093-12-31', '2094-01-31', '2094-02-28',
               '2094-03-31', '2094-04-30'],
              dtype='datetime64[ns]', length=1000, freq='M')

In [81]: pd.bdate_range(start, periods=250, freq='BQS')
Out[81]: 
DatetimeIndex(['2011-01-03', '2011-04-01', '2011-07-01', '2011-10-03',
               '2012-01-02', '2012-04-02', '2012-07-02', '2012-10-01',
               '2013-01-01', '2013-04-01',
               ...
               '2071-01-01', '2071-04-01', '2071-07-01', '2071-10-01',
               '2072-01-01', '2072-04-01', '2072-07-01', '2072-10-03',
               '2073-01-02', '2073-04-03'],
              dtype='datetime64[ns]', length=250, freq='BQS-JAN')
```

`date_range` 与 `bdate_range` 通过指定 `start`、`end`、`period` 与 `freq` 等参数，简化了生成日期范围这项工作。开始与结束日期是必填项，因此，不会生成指定范围之外的日期。

```python
In [82]: pd.date_range(start, end, freq='BM')
Out[82]: 
DatetimeIndex(['2011-01-31', '2011-02-28', '2011-03-31', '2011-04-29',
               '2011-05-31', '2011-06-30', '2011-07-29', '2011-08-31',
               '2011-09-30', '2011-10-31', '2011-11-30', '2011-12-30'],
              dtype='datetime64[ns]', freq='BM')

In [83]: pd.date_range(start, end, freq='W')
Out[83]: 
DatetimeIndex(['2011-01-02', '2011-01-09', '2011-01-16', '2011-01-23',
               '2011-01-30', '2011-02-06', '2011-02-13', '2011-02-20',
               '2011-02-27', '2011-03-06', '2011-03-13', '2011-03-20',
               '2011-03-27', '2011-04-03', '2011-04-10', '2011-04-17',
               '2011-04-24', '2011-05-01', '2011-05-08', '2011-05-15',
               '2011-05-22', '2011-05-29', '2011-06-05', '2011-06-12',
               '2011-06-19', '2011-06-26', '2011-07-03', '2011-07-10',
               '2011-07-17', '2011-07-24', '2011-07-31', '2011-08-07',
               '2011-08-14', '2011-08-21', '2011-08-28', '2011-09-04',
               '2011-09-11', '2011-09-18', '2011-09-25', '2011-10-02',
               '2011-10-09', '2011-10-16', '2011-10-23', '2011-10-30',
               '2011-11-06', '2011-11-13', '2011-11-20', '2011-11-27',
               '2011-12-04', '2011-12-11', '2011-12-18', '2011-12-25',
               '2012-01-01'],
              dtype='datetime64[ns]', freq='W-SUN')

In [84]: pd.bdate_range(end=end, periods=20)
Out[84]: 
DatetimeIndex(['2011-12-05', '2011-12-06', '2011-12-07', '2011-12-08',
               '2011-12-09', '2011-12-12', '2011-12-13', '2011-12-14',
               '2011-12-15', '2011-12-16', '2011-12-19', '2011-12-20',
               '2011-12-21', '2011-12-22', '2011-12-23', '2011-12-26',
               '2011-12-27', '2011-12-28', '2011-12-29', '2011-12-30'],
              dtype='datetime64[ns]', freq='B')

In [85]: pd.bdate_range(start=start, periods=20)
Out[85]: 
DatetimeIndex(['2011-01-03', '2011-01-04', '2011-01-05', '2011-01-06',
               '2011-01-07', '2011-01-10', '2011-01-11', '2011-01-12',
               '2011-01-13', '2011-01-14', '2011-01-17', '2011-01-18',
               '2011-01-19', '2011-01-20', '2011-01-21', '2011-01-24',
               '2011-01-25', '2011-01-26', '2011-01-27', '2011-01-28'],
              dtype='datetime64[ns]', freq='B')
```

*0.23.0 版新增。*

指定 `start`、`end`、`periods` 即可生成从 `start` 开始至 `end` 结束的等距日期范围，这个日期范围包含了 `start` 与 `end`，生成的 `DatetimeIndex` 里的元素数量为 `periods` 的值。

```python
In [86]: pd.date_range('2018-01-01', '2018-01-05', periods=5)
Out[86]: 
DatetimeIndex(['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04',
               '2018-01-05'],
              dtype='datetime64[ns]', freq=None)

In [87]: pd.date_range('2018-01-01', '2018-01-05', periods=10)
Out[87]: 
DatetimeIndex(['2018-01-01 00:00:00', '2018-01-01 10:40:00',
               '2018-01-01 21:20:00', '2018-01-02 08:00:00',
               '2018-01-02 18:40:00', '2018-01-03 05:20:00',
               '2018-01-03 16:00:00', '2018-01-04 02:40:00',
               '2018-01-04 13:20:00', '2018-01-05 00:00:00'],
              dtype='datetime64[ns]', freq=None)
```

### 自定义频率范围

设定 `weekmask` 与 `holidays` 参数，`bdate_range` 还可以生成自定义频率日期范围。这些参数只用于传递自定义字符串。

```python
In [88]: weekmask = 'Mon Wed Fri'

In [89]: holidays = [datetime.datetime(2011, 1, 5), datetime.datetime(2011, 3, 14)]

In [90]: pd.bdate_range(start, end, freq='C', weekmask=weekmask, holidays=holidays)
Out[90]: 
DatetimeIndex(['2011-01-03', '2011-01-07', '2011-01-10', '2011-01-12',
               '2011-01-14', '2011-01-17', '2011-01-19', '2011-01-21',
               '2011-01-24', '2011-01-26',
               ...
               '2011-12-09', '2011-12-12', '2011-12-14', '2011-12-16',
               '2011-12-19', '2011-12-21', '2011-12-23', '2011-12-26',
               '2011-12-28', '2011-12-30'],
              dtype='datetime64[ns]', length=154, freq='C')

In [91]: pd.bdate_range(start, end, freq='CBMS', weekmask=weekmask)
Out[91]: 
DatetimeIndex(['2011-01-03', '2011-02-02', '2011-03-02', '2011-04-01',
               '2011-05-02', '2011-06-01', '2011-07-01', '2011-08-01',
               '2011-09-02', '2011-10-03', '2011-11-02', '2011-12-02'],
              dtype='datetime64[ns]', freq='CBMS')
```

::: tip  参阅

[自定义工作日](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-custombusinessdays)

:::

## 时间戳的界限

Pandas 时间戳的最低单位为纳秒，64 位整数显示的时间跨度约为 584 年，这就是 `Timestamp` 的界限：

```python
In [92]: pd.Timestamp.min
Out[92]: Timestamp('1677-09-21 00:12:43.145225')

In [93]: pd.Timestamp.max
Out[93]: Timestamp('2262-04-11 23:47:16.854775807')
```

::: tip 参阅

 [时间段越界展示](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-oob)

:::

## 索引

`DatetimeIndex` 主要用于 Pandas 对象的索引，为时间序列做了很多优化：

* 预计算了各种偏移量的日期范围，并在后台缓存，让后台生成后续日期范围的速度非常快（仅需抓取切片）。

* 在 Pandas 对象上用 `shift` 与 `tshift` 方法进行快速偏移。

* 合并具有相同频率的重叠 `DatetimeIndex` 对象的速度非常快（这点对快速数据对齐非常重要）。

* 通过 `year`、`month` 等属性快速访问日期字段。

* `snap` 等正则函数与超快的 `asof` 逻辑。

`DatetimeIndex` 支持 `Index` 的所有基本用法，以及一些列简化频率处理的高级时间序列专有方法。

::: tip 参阅

[重置索引](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-reindexing)

:::

::: tip 注意

Pandas 不强制排序日期索引，但如果日期未排序，可能会引发失控或错误操作。

:::

`DatetimeIndex` 可以当作常规索引，支持选择、切片等方法。

```python
In [94]: rng = pd.date_range(start, end, freq='BM')

In [95]: ts = pd.Series(np.random.randn(len(rng)), index=rng)

In [96]: ts.index
Out[96]: 
DatetimeIndex(['2011-01-31', '2011-02-28', '2011-03-31', '2011-04-29',
               '2011-05-31', '2011-06-30', '2011-07-29', '2011-08-31',
               '2011-09-30', '2011-10-31', '2011-11-30', '2011-12-30'],
              dtype='datetime64[ns]', freq='BM')

In [97]: ts[:5].index
Out[97]: 
DatetimeIndex(['2011-01-31', '2011-02-28', '2011-03-31', '2011-04-29',
               '2011-05-31'],
              dtype='datetime64[ns]', freq='BM')

In [98]: ts[::2].index
Out[98]: 
DatetimeIndex(['2011-01-31', '2011-03-31', '2011-05-31', '2011-07-29',
               '2011-09-30', '2011-11-30'],
              dtype='datetime64[ns]', freq='2BM')
```

### 局部字符串索引

能解析为时间戳的日期与字符串可以作为索引的参数：

```python
In [99]: ts['1/31/2011']
Out[99]: 0.11920871129693428

In [100]: ts[datetime.datetime(2011, 12, 25):]
Out[100]: 
2011-12-30    0.56702
Freq: BM, dtype: float64

In [101]: ts['10/31/2011':'12/31/2011']
Out[101]: 
2011-10-31    0.271860
2011-11-30   -0.424972
2011-12-30    0.567020
Freq: BM, dtype: float64
```

Pandas 为访问较长的时间序列提供了便捷方法，**年**、**年月**字符串均可：

```python
In [102]: ts['2011']
Out[102]: 
2011-01-31    0.119209
2011-02-28   -1.044236
2011-03-31   -0.861849
2011-04-29   -2.104569
2011-05-31   -0.494929
2011-06-30    1.071804
2011-07-29    0.721555
2011-08-31   -0.706771
2011-09-30   -1.039575
2011-10-31    0.271860
2011-11-30   -0.424972
2011-12-30    0.567020
Freq: BM, dtype: float64

In [103]: ts['2011-6']
Out[103]: 
2011-06-30    1.071804
Freq: BM, dtype: float64
```

带 `DatetimeIndex` 的 `DateFrame` 也支持这种切片方式。局部字符串是标签切片的一种形式，这种切片也**包含**截止时点，即，与日期匹配的时间也会包含在内：

```python
In [104]: dft = pd.DataFrame(np.random.randn(100000, 1), columns=['A'],
   .....:                    index=pd.date_range('20130101', periods=100000, freq='T'))
   .....: 

In [105]: dft
Out[105]: 
                            A
2013-01-01 00:00:00  0.276232
2013-01-01 00:01:00 -1.087401
2013-01-01 00:02:00 -0.673690
2013-01-01 00:03:00  0.113648
2013-01-01 00:04:00 -1.478427
...                       ...
2013-03-11 10:35:00 -0.747967
2013-03-11 10:36:00 -0.034523
2013-03-11 10:37:00 -0.201754
2013-03-11 10:38:00 -1.509067
2013-03-11 10:39:00 -1.693043

[100000 rows x 1 columns]

In [106]: dft['2013']
Out[106]: 
                            A
2013-01-01 00:00:00  0.276232
2013-01-01 00:01:00 -1.087401
2013-01-01 00:02:00 -0.673690
2013-01-01 00:03:00  0.113648
2013-01-01 00:04:00 -1.478427
...                       ...
2013-03-11 10:35:00 -0.747967
2013-03-11 10:36:00 -0.034523
2013-03-11 10:37:00 -0.201754
2013-03-11 10:38:00 -1.509067
2013-03-11 10:39:00 -1.693043

[100000 rows x 1 columns]
```

下列代码截取了自 1 月 1 日凌晨起，至 2 月 28 日午夜的日期与时间。

```python
In [107]: dft['2013-1':'2013-2']
Out[107]: 
                            A
2013-01-01 00:00:00  0.276232
2013-01-01 00:01:00 -1.087401
2013-01-01 00:02:00 -0.673690
2013-01-01 00:03:00  0.113648
2013-01-01 00:04:00 -1.478427
...                       ...
2013-02-28 23:55:00  0.850929
2013-02-28 23:56:00  0.976712
2013-02-28 23:57:00 -2.693884
2013-02-28 23:58:00 -1.575535
2013-02-28 23:59:00 -1.573517

[84960 rows x 1 columns]
```

下列代码截取了**包含截止日期及其时间在内**的日期与时间。

```python
In [108]: dft['2013-1':'2013-2-28']
Out[108]: 
                            A
2013-01-01 00:00:00  0.276232
2013-01-01 00:01:00 -1.087401
2013-01-01 00:02:00 -0.673690
2013-01-01 00:03:00  0.113648
2013-01-01 00:04:00 -1.478427
...                       ...
2013-02-28 23:55:00  0.850929
2013-02-28 23:56:00  0.976712
2013-02-28 23:57:00 -2.693884
2013-02-28 23:58:00 -1.575535
2013-02-28 23:59:00 -1.573517

[84960 rows x 1 columns]
```

下列代码指定了精准的截止时间，注意此处的结果与上述截取结果的区别：

```python
In [109]: dft['2013-1':'2013-2-28 00:00:00']
Out[109]: 
                            A
2013-01-01 00:00:00  0.276232
2013-01-01 00:01:00 -1.087401
2013-01-01 00:02:00 -0.673690
2013-01-01 00:03:00  0.113648
2013-01-01 00:04:00 -1.478427
...                       ...
2013-02-27 23:56:00  1.197749
2013-02-27 23:57:00  0.720521
2013-02-27 23:58:00 -0.072718
2013-02-27 23:59:00 -0.681192
2013-02-28 00:00:00 -0.557501

[83521 rows x 1 columns]
```

截止时间是索引的一部分，包含在截取的内容之内：

```python
In [110]: dft['2013-1-15':'2013-1-15 12:30:00']
Out[110]: 
                            A
2013-01-15 00:00:00 -0.984810
2013-01-15 00:01:00  0.941451
2013-01-15 00:02:00  1.559365
2013-01-15 00:03:00  1.034374
2013-01-15 00:04:00 -1.480656
...                       ...
2013-01-15 12:26:00  0.371454
2013-01-15 12:27:00 -0.930806
2013-01-15 12:28:00 -0.069177
2013-01-15 12:29:00  0.066510
2013-01-15 12:30:00 -0.003945

[751 rows x 1 columns]
```

*0.18.0 版新增*。

`DatetimeIndex` 局部字符串索引还支持多层索引 `DataFrame`。

```python
In [111]: dft2 = pd.DataFrame(np.random.randn(20, 1),
   .....:                     columns=['A'],
   .....:                     index=pd.MultiIndex.from_product(
   .....:                         [pd.date_range('20130101', periods=10, freq='12H'),
   .....:                          ['a', 'b']]))
   .....: 

In [112]: dft2
Out[112]: 
                              A
2013-01-01 00:00:00 a -0.298694
                    b  0.823553
2013-01-01 12:00:00 a  0.943285
                    b -1.479399
2013-01-02 00:00:00 a -1.643342
...                         ...
2013-01-04 12:00:00 b  0.069036
2013-01-05 00:00:00 a  0.122297
                    b  1.422060
2013-01-05 12:00:00 a  0.370079
                    b  1.016331

[20 rows x 1 columns]

In [113]: dft2.loc['2013-01-05']
Out[113]: 
                              A
2013-01-05 00:00:00 a  0.122297
                    b  1.422060
2013-01-05 12:00:00 a  0.370079
                    b  1.016331

In [114]: idx = pd.IndexSlice

In [115]: dft2 = dft2.swaplevel(0, 1).sort_index()

In [116]: dft2.loc[idx[:, '2013-01-05'], :]
Out[116]: 
                              A
a 2013-01-05 00:00:00  0.122297
  2013-01-05 12:00:00  0.370079
b 2013-01-05 00:00:00  1.422060
  2013-01-05 12:00:00  1.016331
```

*0.25.0 版新增*。

字符串索引切片支持 UTC 偏移。

```python
In [117]: df = pd.DataFrame([0], index=pd.DatetimeIndex(['2019-01-01'], tz='US/Pacific'))

In [118]: df
Out[118]: 
                           0
2019-01-01 00:00:00-08:00  0

In [119]: df['2019-01-01 12:00:00+04:00':'2019-01-01 13:00:00+04:00']
Out[119]: 
                           0
2019-01-01 00:00:00-08:00  0
```

### 切片 vs. 精准匹配

*0.20.0 版新增。*

基于索引的精度，字符串既可用于切片，也可用于精准匹配。字符串精度比索引精度低，就是切片，比索引精度高，则是精准匹配。

```python
In [120]: series_minute = pd.Series([1, 2, 3],
   .....:                           pd.DatetimeIndex(['2011-12-31 23:59:00',
   .....:                                             '2012-01-01 00:00:00',
   .....:                                             '2012-01-01 00:02:00']))
   .....: 

In [121]: series_minute.index.resolution
Out[121]: 'minute'
```

下例中的时间戳字符串没有 `Series` 对象的精度高。`series_minute` 到`秒`，时间戳字符串只到`分`。

```python
In [122]: series_minute['2011-12-31 23']
Out[122]: 
2011-12-31 23:59:00    1
dtype: int64
```

精度为分钟（或更高精度）的时间戳字符串，给出的是标量，不会被当作切片。

```python
In [123]: series_minute['2011-12-31 23:59']
Out[123]: 1

In [124]: series_minute['2011-12-31 23:59:00']
Out[124]: 1
```

索引的精度为秒时，精度为分钟的时间戳返回的是 `Series`。

```python
In [125]: series_second = pd.Series([1, 2, 3],
   .....:                           pd.DatetimeIndex(['2011-12-31 23:59:59',
   .....:                                             '2012-01-01 00:00:00',
   .....:                                             '2012-01-01 00:00:01']))
   .....: 

In [126]: series_second.index.resolution
Out[126]: 'second'

In [127]: series_second['2011-12-31 23:59']
Out[127]: 
2011-12-31 23:59:59    1
dtype: int64
```

用时间戳字符串切片时，还可以用 `[]` 索引 `DataFrame`。

```python
In [128]: dft_minute = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]},
   .....:                           index=series_minute.index)
   .....: 

In [129]: dft_minute['2011-12-31 23']
Out[129]: 
                     a  b
2011-12-31 23:59:00  1  4
```

::: danger 警告

字符串执行精确匹配时，用 `[]` 按列，而不是按行截取 `DateFrame` ，参阅[索引基础](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-basics)。如，`dft_minute ['2011-12-31 23:59']` 会触发 `KeyError`，这是因为 `2012-12-31 23:59`与索引的精度一样，但没有叫这个名字的列。

为了实现精准切片，要用 `.loc` 对行进行切片或选择。

```python
In [130]: dft_minute.loc['2011-12-31 23:59']
Out[130]: 
a    1
b    4
Name: 2011-12-31 23:59:00, dtype: int64
```

:::

注意：`DatetimeIndex` 精度不能低于日。

```python
In [131]: series_monthly = pd.Series([1, 2, 3],
   .....:                            pd.DatetimeIndex(['2011-12', '2012-01', '2012-02']))
   .....: 

In [132]: series_monthly.index.resolution
Out[132]: 'day'

In [133]: series_monthly['2011-12']  # 返回的是 Series
Out[133]: 
2011-12-01    1
dtype: int64
```

### 精确索引

正如上节所述，局部字符串依靠时间段的**精度**索引 `DatetimeIndex`，即时间间隔与索引精度相关。反之，用 `Timestamp` 或 `datetime` 索引更精准，这些对象指定的时间更精确。注意，精确索引包含了起始时点。

就算没有显式指定，`Timestamp` 与`datetime` 也支持 `hours`、`minutes`、`seconds`，默认值为 0。

```python
In [134]: dft[datetime.datetime(2013, 1, 1):datetime.datetime(2013, 2, 28)]
Out[134]: 
                            A
2013-01-01 00:00:00  0.276232
2013-01-01 00:01:00 -1.087401
2013-01-01 00:02:00 -0.673690
2013-01-01 00:03:00  0.113648
2013-01-01 00:04:00 -1.478427
...                       ...
2013-02-27 23:56:00  1.197749
2013-02-27 23:57:00  0.720521
2013-02-27 23:58:00 -0.072718
2013-02-27 23:59:00 -0.681192
2013-02-28 00:00:00 -0.557501

[83521 rows x 1 columns]
```

不用默认值。

```python
In [135]: dft[datetime.datetime(2013, 1, 1, 10, 12, 0):
   .....:     datetime.datetime(2013, 2, 28, 10, 12, 0)]
   .....: 
Out[135]: 
                            A
2013-01-01 10:12:00  0.565375
2013-01-01 10:13:00  0.068184
2013-01-01 10:14:00  0.788871
2013-01-01 10:15:00 -0.280343
2013-01-01 10:16:00  0.931536
...                       ...
2013-02-28 10:08:00  0.148098
2013-02-28 10:09:00 -0.388138
2013-02-28 10:10:00  0.139348
2013-02-28 10:11:00  0.085288
2013-02-28 10:12:00  0.950146

[83521 rows x 1 columns]
```

### 截断与花式索引

[`truncate()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.truncate.html#pandas.DataFrame.truncate "pandas.DataFrame.truncate") 便捷函数与切片类似。注意，与切片返回的是部分匹配日期不同， `truncate` 假设 `DatetimeIndex` 里未标明时间组件的值为 0。

```python
In [136]: rng2 = pd.date_range('2011-01-01', '2012-01-01', freq='W')

In [137]: ts2 = pd.Series(np.random.randn(len(rng2)), index=rng2)

In [138]: ts2.truncate(before='2011-11', after='2011-12')
Out[138]: 
2011-11-06    0.437823
2011-11-13   -0.293083
2011-11-20   -0.059881
2011-11-27    1.252450
Freq: W-SUN, dtype: float64

In [139]: ts2['2011-11':'2011-12']
Out[139]: 
2011-11-06    0.437823
2011-11-13   -0.293083
2011-11-20   -0.059881
2011-11-27    1.252450
2011-12-04    0.046611
2011-12-11    0.059478
2011-12-18   -0.286539
2011-12-25    0.841669
Freq: W-SUN, dtype: float64
```

花式索引返回 `DatetimeIndex`， 但因为打乱了 `DatetimeIndex` 频率，丢弃了频率信息，见 `freq=None`：

```python
In [140]: ts2[[0, 2, 6]].index
Out[140]: DatetimeIndex(['2011-01-02', '2011-01-16', '2011-02-13'], dtype='datetime64[ns]', freq=None)
```

## 日期/时间组件

以下日期/时间属性可以访问 `Timestamp` 或 `DatetimeIndex`。

|       属性       |                    说明                     |
| :--------------: | :-----------------------------------------: |
|       year       |                datetime 的年                |
|      month       |                datetime 的月                |
|       day        |                datetime 的日                |
|       hour       |               datetime 的小时               |
|      minute      |               datetime 的分钟               |
|      second      |                datetime 的秒                |
|   microsecond    |               datetime 的微秒               |
|    nanosecond    |               datetime 的纳秒               |
|       date       |    返回 datetime.date（不包含时区信息）     |
|       time       |    返回 datetime.time（不包含时区信息）     |
|      timetz      |     返回带本地时区信息的 datetime.time      |
|    dayofyear     |               一年里的第几天                |
|    weekofyear    |               一年里的第几周                |
|       week       |               一年里的第几周                |
|    dayofweek     |     一周里的第几天，Monday=0, Sunday=6      |
|     weekday      |     一周里的第几天，Monday=0, Sunday=6      |
|   weekday_name   |        这一天是星期几 （如，Friday）        |
|     quarter      | 日期所处的季节：Jan-Mar = 1，Apr-Jun = 2 等 |
|  days_in_month   |            日期所在的月有多少天             |
|  is_month_start  |      逻辑判断是不是月初（由频率定义）       |
|   is_month_end   |      逻辑判断是不是月末（由频率定义）       |
| is_quarter_start |      逻辑判断是不是季初（由频率定义）       |
|  is_quarter_end  |      逻辑判断是不是季末（由频率定义）       |
|  is_year_start   |      逻辑判断是不是年初（由频率定义）       |
|   is_year_end    |      逻辑判断是不是年末（由频率定义）       |
|   is_leap_year   |     逻辑判断是不是日期所在年是不是闰年      |

参照 [.dt 访问器](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dt-accessors) 一节介绍的知识点，`Series` 的值为 `datetime` 时，还可以用 `.dt` 访问这些属性。

## DateOffset 对象

上例中，频率字符串（如，`D`）用于定义指定的频率：

* 用 [`date_range()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html#pandas.date_range "pandas.date_range") 按指定频率分隔 [`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 里的日期与时间

* [`Period`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Period.html#pandas.Period "pandas.Period") 或 [`PeriodIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.PeriodIndex.html#pandas.PeriodIndex "pandas.PeriodIndex") 的频率

频率字符串表示的是 `DateOffset` 对象及其子类。`DateOffset` 类似于时间差 [`Timedelta`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html#pandas.Timedelta "pandas.Timedelta") ，但遵循指定的日历日规则。例如，[`Timedelta`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html#pandas.Timedelta "pandas.Timedelta") 表示的每日时间差一直都是 24 小时，而 `DateOffset` 的每日偏移量则是与下一天相同的时间差，使用夏时制时，每日偏移时间有可能是 23 或 24 小时，甚至还有可能是 25 小时。不过，`DateOffset` 子类只能是等于或小于**小时**的时间单位（`Hour`、`Minute`、`Second`、`Milli`、`Micro`、`Nano`），操作类似于 [`Timedelta`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html#pandas.Timedelta "pandas.Timedelta") 及对应的绝对时间。

`DateOffset` 基础操作类似于 `dateutil.relativedelta`（[relativedelta 文档](https://dateutil.readthedocs.io/en/stable/relativedelta.html)），可按指定的日历日时间段偏移日期时间。可用算数运算符（+）或 `apply` 方法执行日期偏移操作。

```python
# 指定包含夏时制变迁的某天
In [141]: ts = pd.Timestamp('2016-10-30 00:00:00', tz='Europe/Helsinki')

# 对应的绝对时间
In [142]: ts + pd.Timedelta(days=1)
Out[142]: Timestamp('2016-10-30 23:00:00+0200', tz='Europe/Helsinki')

# 对应的日历时间
In [143]: ts + pd.DateOffset(days=1)
Out[143]: Timestamp('2016-10-31 00:00:00+0200', tz='Europe/Helsinki')

In [144]: friday = pd.Timestamp('2018-01-05')

In [145]: friday.day_name()
Out[145]: 'Friday'

# 与两个工作日相加（星期五 --> 星期二）
In [146]: two_business_days = 2 * pd.offsets.BDay()

In [147]: two_business_days.apply(friday)
Out[147]: Timestamp('2018-01-09 00:00:00')

In [148]: friday + two_business_days
Out[148]: Timestamp('2018-01-09 00:00:00')

In [149]: (friday + two_business_days).day_name()
Out[149]: 'Tuesday'
```

大多数 `DateOffset` 都支持频率字符串或偏移别名，可用作 `freq` 关键字参数。有效的日期偏移及频率字符串如下：

|                          日期偏移量                          |    频率字符串     |                    说明                    |
| :----------------------------------------------------------: | :---------------: | :----------------------------------------: |
| [`DateOffset`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.DateOffset.html#pandas.tseries.offsets.DateOffset) |        无         |        通用偏移类，默认为一个日历日        |
| [`BDay`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BDay.html#pandas.tseries.offsets.BDay) 或 [`BusinessDay`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BusinessDay.html#pandas.tseries.offsets.BusinessDay) |       `'B'`       |                   工作日                   |
| [`CDay`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CDay.html#pandas.tseries.offsets.CDay) 或 [`CustomBusinessDay`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CustomBusinessDay.html#pandas.tseries.offsets.CustomBusinessDay) |       `'C'`       |                自定义工作日                |
| [`Week`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Week.html#pandas.tseries.offsets.Week) |       `'W'`       |           一周，可选周内固定某日           |
| [`WeekOfMonth`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.WeekOfMonth.html#pandas.tseries.offsets.WeekOfMonth) |      `'WOM'`      |             每月第几周的第几天             |
| [`LastWeekOfMonth`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.LastWeekOfMonth.html#pandas.tseries.offsets.LastWeekOfMonth) |     `'LWOM'`      |            每月最后一周的第几天            |
| [`MonthEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.MonthEnd.html#pandas.tseries.offsets.MonthEnd) |       `'M'`       |                 日历日月末                 |
| [`MonthBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.MonthBegin.html#pandas.tseries.offsets.MonthBegin) |      `'MS'`       |                 日历日月初                 |
| [`BMonthEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BMonthEnd.html#pandas.tseries.offsets.BMonthEnd) 或 [`BusinessMonthEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BusinessMonthEnd.html#pandas.tseries.offsets.BusinessMonthEnd) |      `'BM'`       |                 工作日月末                 |
| [`BMonthBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BMonthBegin.html#pandas.tseries.offsets.BMonthBegin) 或 [`BusinessMonthBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BusinessMonthBegin.html#pandas.tseries.offsets.BusinessMonthBegin) |      `'BMS'`      |                 工作日月初                 |
| [`CBMonthEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CBMonthEnd.html#pandas.tseries.offsets.CBMonthEnd) 或 [`CustomBusinessMonthEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CustomBusinessMonthEnd.html#pandas.tseries.offsets.CustomBusinessMonthEnd) |      `'CBM'`      |              自定义工作日月末              |
| [`CBMonthBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CBMonthBegin.html#pandas.tseries.offsets.CBMonthBegin) 或 [`CustomBusinessMonthBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CustomBusinessMonthBegin.html#pandas.tseries.offsets.CustomBusinessMonthBegin) |     `'CBMS'`      |              自定义工作日月初              |
| [`SemiMonthEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.SemiMonthEnd.html#pandas.tseries.offsets.SemiMonthEnd) |      `'SM'`       | 某月第 15 天（或其它半数日期）与日历日月末 |
| [`SemiMonthBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.SemiMonthBegin.html#pandas.tseries.offsets.SemiMonthBegin) |      `'SMS'`      |   日历日月初与第 15 天（或其它半数日期）   |
| [`QuarterEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.QuarterEnd.html#pandas.tseries.offsets.QuarterEnd) |       `'Q'`       |                 日历日季末                 |
| [`QuarterBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.QuarterBegin.html#pandas.tseries.offsets.QuarterBegin) |      `'QS'`       |                 日历日季初                 |
| [`BQuarterEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BQuarterEnd.html#pandas.tseries.offsets.BQuarterEnd) |       `'BQ`       |                 工作日季末                 |
| [`BQuarterBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BQuarterBegin.html#pandas.tseries.offsets.BQuarterBegin) |      `'BQS'`      |                 工作日季初                 |
| [`FY5253Quarter`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.FY5253Quarter.html#pandas.tseries.offsets.FY5253Quarter) |      `'REQ'`      |           零售季，又名 52-53 周            |
| [`YearEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.YearEnd.html#pandas.tseries.offsets.YearEnd) |       `'A'`       |                 日历日年末                 |
| [`YearBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.YearBegin.html#pandas.tseries.offsets.YearBegin) | `'AS'` 或 `'BYS'` |                 日历日年初                 |
| [`BYearEnd`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BYearEnd.html#pandas.tseries.offsets.BYearEnd) |      `'BA'`       |                 工作日年末                 |
| [`BYearBegin`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BYearBegin.html#pandas.tseries.offsets.BYearBegin) |      `'BAS'`      |                 工作日年初                 |
| [`FY5253`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.FY5253.html#pandas.tseries.offsets.FY5253) |      `'RE'`       |          零售年（又名 52-53 周）           |
| [`Easter`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Easter.html#pandas.tseries.offsets.Easter) |        无         |                 复活节假日                 |
| [`BusinessHour`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BusinessHour.html#pandas.tseries.offsets.BusinessHour) |      `'BH'`       |                  工作小时                  |
| [`CustomBusinessHour`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.CustomBusinessHour.html#pandas.tseries.offsets.CustomBusinessHour) |      `'CBH'`      |               自定义工作小时               |
| [`Day`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Day.html#pandas.tseries.offsets.Day) |       `'D'`       |                    一天                    |
| [`Hour`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Hour.html#pandas.tseries.offsets.Hour) |       `'H'`       |                   一小时                   |
| [`Minute`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Minute.html#pandas.tseries.offsets.Minute) | `'T'` 或 `'min'`  |                   一分钟                   |
| [`Second`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Second.html#pandas.tseries.offsets.Second) |       `'S'`       |                    一秒                    |
| [`Milli`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Milli.html#pandas.tseries.offsets.Milli) |  `'L'` 或 `'ms'`  |                   一毫秒                   |
| [`Micro`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Micro.html#pandas.tseries.offsets.Micro) |  `'U'` 或 `'us'`  |                   一微秒                   |
| [`Nano`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.Nano.html#pandas.tseries.offsets.Nano) |       `'N'`       |                   一纳秒                   |

`DateOffset` 还支持 `rollforward()` 与 `rollback()` 方法，按偏移量把某一日期**向前**或**向后**移动至有效偏移日期。例如，工作日偏移滚动日期时会跳过周末（即，星期六与星期日），直接到星期一，因为工作日偏移针对的是工作日。

```python
In [150]: ts = pd.Timestamp('2018-01-06 00:00:00')

In [151]: ts.day_name()
Out[151]: 'Saturday'

# 工作时间的有效偏移日期为星期一至星期五
In [152]: offset = pd.offsets.BusinessHour(start='09:00')

# 向前偏移到最近的工作日，即星期一
In [153]: offset.rollforward(ts)
Out[153]: Timestamp('2018-01-08 09:00:00')

# 向前偏移至最近的工作日，同时，小时也相应增加了
In [154]: ts + offset
Out[154]: Timestamp('2018-01-08 10:00:00')
```

这些操作默认保存时间（小时、分钟等）信息。`normalize()` 可以把时间重置为午夜零点，是否应用此操作，取决于是否需要保留时间信息。

```python
In [155]: ts = pd.Timestamp('2014-01-01 09:00')

In [156]: day = pd.offsets.Day()

In [157]: day.apply(ts)
Out[157]: Timestamp('2014-01-02 09:00:00')

In [158]: day.apply(ts).normalize()
Out[158]: Timestamp('2014-01-02 00:00:00')

In [159]: ts = pd.Timestamp('2014-01-01 22:00')

In [160]: hour = pd.offsets.Hour()

In [161]: hour.apply(ts)
Out[161]: Timestamp('2014-01-01 23:00:00')

In [162]: hour.apply(ts).normalize()
Out[162]: Timestamp('2014-01-01 00:00:00')

In [163]: hour.apply(pd.Timestamp("2014-01-01 23:30")).normalize()
Out[163]: Timestamp('2014-01-02 00:00:00')
```

### 参数偏移

偏移量支持参数，可以让不同操作生成不同结果。例如，`Week` 偏移生成每周数据时支持 `weekday` 参数，生成日期始终位于一周中的指定日期。

```python
In [164]: d = datetime.datetime(2008, 8, 18, 9, 0)

In [165]: d
Out[165]: datetime.datetime(2008, 8, 18, 9, 0)

In [166]: d + pd.offsets.Week()
Out[166]: Timestamp('2008-08-25 09:00:00')

In [167]: d + pd.offsets.Week(weekday=4)
Out[167]: Timestamp('2008-08-22 09:00:00')

In [168]: (d + pd.offsets.Week(weekday=4)).weekday()
Out[168]: 4

In [169]: d - pd.offsets.Week()
Out[169]: Timestamp('2008-08-11 09:00:00')
```

加减法也支持 `normalize` 选项。

```python
In [170]: d + pd.offsets.Week(normalize=True)
Out[170]: Timestamp('2008-08-25 00:00:00')

In [171]: d - pd.offsets.Week(normalize=True)
Out[171]: Timestamp('2008-08-11 00:00:00')
```

`YearEnd` 也支持参数，如 `month` 参数，用于指定月份 。

```python
In [172]: d + pd.offsets.YearEnd()
Out[172]: Timestamp('2008-12-31 09:00:00')

In [173]: d + pd.offsets.YearEnd(month=6)
Out[173]: Timestamp('2009-06-30 09:00:00')
```

### `Series` 与 `DatetimeIndex` 偏移

可以为 `Series` 或 `DatetimeIndex` 里的每个元素应用偏移。

```python
In [174]: rng = pd.date_range('2012-01-01', '2012-01-03')

In [175]: s = pd.Series(rng)

In [176]: rng
Out[176]: DatetimeIndex(['2012-01-01', '2012-01-02', '2012-01-03'], dtype='datetime64[ns]', freq='D')

In [177]: rng + pd.DateOffset(months=2)
Out[177]: DatetimeIndex(['2012-03-01', '2012-03-02', '2012-03-03'], dtype='datetime64[ns]', freq='D')

In [178]: s + pd.DateOffset(months=2)
Out[178]: 
0   2012-03-01
1   2012-03-02
2   2012-03-03
dtype: datetime64[ns]

In [179]: s - pd.DateOffset(months=2)
Out[179]: 
0   2011-11-01
1   2011-11-02
2   2011-11-03
dtype: datetime64[ns]
```

如果偏移直接映射 `Timedelta` （`Day`、`Hour`、`Minute`、`Second`、`Micro`、`Milli`、`Nano`），则该偏移与 `Timedelta` 的使用方式完全一样。参阅[时间差 - Timedelta](https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html#timedeltas-operations)，查看更多示例。

```python
In [180]: s - pd.offsets.Day(2)
Out[180]: 
0   2011-12-30
1   2011-12-31
2   2012-01-01
dtype: datetime64[ns]

In [181]: td = s - pd.Series(pd.date_range('2011-12-29', '2011-12-31'))

In [182]: td
Out[182]: 
0   3 days
1   3 days
2   3 days
dtype: timedelta64[ns]

In [183]: td + pd.offsets.Minute(15)
Out[183]: 
0   3 days 00:15:00
1   3 days 00:15:00
2   3 days 00:15:00
dtype: timedelta64[ns]
```

注意，某些偏移量（如 `BQuarterEnd`）不支持矢量操作，即使可以执行运算，速度也非常慢，并可能显示 `PerformanceWaring`（性能警告）。

```python
In [184]: rng + pd.offsets.BQuarterEnd()
Out[184]: DatetimeIndex(['2012-03-30', '2012-03-30', '2012-03-30'], dtype='datetime64[ns]', freq='D')
```

### 自定义工作日

`Cday` 或 `CustomBusinessDay` 类可以参数化 `BusinessDay` 类，用于创建支持本地周末与传统节假日的自定义工作日历。

下面这个例子就很有意思，知道吗？埃及的周末是星期五与星期六。

```python
In [185]: weekmask_egypt = 'Sun Mon Tue Wed Thu'


# 下面是 2012 - 2014 年的五一劳动节
In [186]: holidays = ['2012-05-01',
   .....:             datetime.datetime(2013, 5, 1),
   .....:             np.datetime64('2014-05-01')]
   .....: 

In [187]: bday_egypt = pd.offsets.CustomBusinessDay(holidays=holidays,
   .....:                                           weekmask=weekmask_egypt)
   .....: 

In [188]: dt = datetime.datetime(2013, 4, 30)

In [189]: dt + 2 * bday_egypt
Out[189]: Timestamp('2013-05-05 00:00:00')
```

下列代码实现了日期与工作日之间的映射关系。

```python
In [190]: dts = pd.date_range(dt, periods=5, freq=bday_egypt)

In [191]: pd.Series(dts.weekday, dts).map(
   .....:     pd.Series('Mon Tue Wed Thu Fri Sat Sun'.split()))
   .....: 
Out[191]: 
2013-04-30    Tue
2013-05-02    Thu
2013-05-05    Sun
2013-05-06    Mon
2013-05-07    Tue
Freq: C, dtype: object
```

节日日历支持节假日列表。更多信息，请参阅[节日日历](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-holiday)文档。

```python
In [192]: from pandas.tseries.holiday import USFederalHolidayCalendar

In [193]: bday_us = pd.offsets.CustomBusinessDay(calendar=USFederalHolidayCalendar())

# 马丁路德金纪念日前的星期五
In [194]: dt = datetime.datetime(2014, 1, 17)

# 马丁路德金纪念日后的星期二，因为星期一放假，所以跳过了
In [195]: dt + bday_us
Out[195]: Timestamp('2014-01-21 00:00:00')
```

遵循节日日历规则的月偏移可以用正常方式定义。

```python
In [196]: bmth_us = pd.offsets.CustomBusinessMonthBegin(
   .....:     calendar=USFederalHolidayCalendar())
   .....: 

# 跳过新年
In [197]: dt = datetime.datetime(2013, 12, 17)

In [198]: dt + bmth_us
Out[198]: Timestamp('2014-01-02 00:00:00')

# 定义带自定义偏移的日期索引
In [199]: pd.date_range(start='20100101', end='20120101', freq=bmth_us)
Out[199]: 
DatetimeIndex(['2010-01-04', '2010-02-01', '2010-03-01', '2010-04-01',
               '2010-05-03', '2010-06-01', '2010-07-01', '2010-08-02',
               '2010-09-01', '2010-10-01', '2010-11-01', '2010-12-01',
               '2011-01-03', '2011-02-01', '2011-03-01', '2011-04-01',
               '2011-05-02', '2011-06-01', '2011-07-01', '2011-08-01',
               '2011-09-01', '2011-10-03', '2011-11-01', '2011-12-01'],
              dtype='datetime64[ns]', freq='CBMS')
```

::: tip 注意

频率字符串 'C' 验证 `CustomBusinessDay` 日期偏移 调用，注意，`CustomBusinessDay` 可实现参数化，`CustomBusinessDay` 实例会各不相同，且频率字符串 'C' 无法识别这个问题。用户应确保应用里调用的频率字符串 'C' 的一致性 。

### 工作时间

`BusinessHour` 表示 `BusinessDay` 基础上的工作时间，用于指定开始与结束工作时间。

`BusinessHour` 默认的工作时间是 9:00 - 17:00。`BusinessHour` 加法以小时频率增加 `Timestamp` 。如果目标 `Timestamp` 超出了一小时，则要先移动到下一个工作小时，再行增加。如果超过了当日工作时间的范围，剩下的时间则添加到下一个工作日。

```python
In [200]: bh = pd.offsets.BusinessHour()

In [201]: bh
Out[201]: <BusinessHour: BH=09:00-17:00>

# 2014 年 8 月 1 日是星期五
In [202]: pd.Timestamp('2014-08-01 10:00').weekday()
Out[202]: 4

In [203]: pd.Timestamp('2014-08-01 10:00') + bh
Out[203]: Timestamp('2014-08-01 11:00:00')

# 下例等同于： pd.Timestamp('2014-08-01 09:00') + bh
In [204]: pd.Timestamp('2014-08-01 08:00') + bh
Out[204]: Timestamp('2014-08-01 10:00:00')

# 如果计算结果为当日下班时间，则转移到下一个工作日的上班时间
In [205]: pd.Timestamp('2014-08-01 16:00') + bh
Out[205]: Timestamp('2014-08-04 09:00:00')

# 剩下的时间也会添加到下一天
In [206]: pd.Timestamp('2014-08-01 16:30') + bh
Out[206]: Timestamp('2014-08-04 09:30:00')

# 添加 2 个工作小时
In [207]: pd.Timestamp('2014-08-01 10:00') + pd.offsets.BusinessHour(2)
Out[207]: Timestamp('2014-08-01 12:00:00')

# 减掉 3 个工作小时
In [208]: pd.Timestamp('2014-08-01 10:00') + pd.offsets.BusinessHour(-3)
Out[208]: Timestamp('2014-07-31 15:00:00')
```

还可以用关键字指定 `start` 与 `end` 时间。参数必须是`hour:minute` 格式的字符串或 `datetime.time` 实例。把秒、微秒、纳秒设置为工作时间会导致 `ValueError`。

```python
In [209]: bh = pd.offsets.BusinessHour(start='11:00', end=datetime.time(20, 0))

In [210]: bh
Out[210]: <BusinessHour: BH=11:00-20:00>

In [211]: pd.Timestamp('2014-08-01 13:00') + bh
Out[211]: Timestamp('2014-08-01 14:00:00')

In [212]: pd.Timestamp('2014-08-01 09:00') + bh
Out[212]: Timestamp('2014-08-01 12:00:00')

In [213]: pd.Timestamp('2014-08-01 18:00') + bh
Out[213]: Timestamp('2014-08-01 19:00:00')
```

`start` 时间晚于 `end` 时间表示夜班工作时间。此时，工作时间将从午夜延至第二天。工作时间是否有效取决于该时间是否开始于有效的 `BusinessDay`。

```python
In [214]: bh = pd.offsets.BusinessHour(start='17:00', end='09:00')

In [215]: bh
Out[215]: <BusinessHour: BH=17:00-09:00>

In [216]: pd.Timestamp('2014-08-01 17:00') + bh
Out[216]: Timestamp('2014-08-01 18:00:00')

In [217]: pd.Timestamp('2014-08-01 23:00') + bh
Out[217]: Timestamp('2014-08-02 00:00:00')

# 虽然 2014 年 8 月 2 日是星期六，
# 但因为工作时间开始于星期五，因此，也是有效的
In [218]: pd.Timestamp('2014-08-02 04:00') + bh
Out[218]: Timestamp('2014-08-02 05:00:00')


# 虽然 2014 年 8 月 4 日是星期一，
# 但开始时间是星期日，因此，超出了工作时间
In [219]: pd.Timestamp('2014-08-04 04:00') + bh
Out[219]: Timestamp('2014-08-04 18:00:00')
```

`BusinessHour.rollforward` 与 `rollback` 操作将前滚至下一天的上班时间，或回滚至前一天的下班时间。与其它偏移量不同，`BusinessHour.rollforward` 输出与 `apply` 定义不同的结果。

这是因为一天工作时间的结束等同于第二天工作时间的开始。默认情况下，工作时间为 9:00 - 17:00，Pandas 认为 `2014-08-01 17:00` 与 `2014-08-04 09:00` 之间的时间间隔为 0 分钟。

```python
# 把时间戳回滚到前一天的下班时间
In [220]: pd.offsets.BusinessHour().rollback(pd.Timestamp('2014-08-02 15:00'))
Out[220]: Timestamp('2014-08-01 17:00:00')

# 把时间戳前滚到下一个工作日的上班时间
In [221]: pd.offsets.BusinessHour().rollforward(pd.Timestamp('2014-08-02 15:00'))
Out[221]: Timestamp('2014-08-04 09:00:00')

# 等同于：BusinessHour().apply(pd.Timestamp('2014-08-01 17:00'))
# 与 BusinessHour().apply(pd.Timestamp('2014-08-04 09:00'))
In [222]: pd.offsets.BusinessHour().apply(pd.Timestamp('2014-08-02 15:00'))
Out[222]: Timestamp('2014-08-04 10:00:00')

# 工作日的结果（仅供参考）
In [223]: pd.offsets.BusinessHour().rollforward(pd.Timestamp('2014-08-02'))
Out[223]: Timestamp('2014-08-04 09:00:00')

# 等同于 BusinessDay().apply(pd.Timestamp('2014-08-01'))
# 等同于 rollforward 因为工作日不会重叠
In [224]: pd.offsets.BusinessHour().apply(pd.Timestamp('2014-08-02'))
Out[224]: Timestamp('2014-08-04 10:00:00')
```

`BusinessHour` 把星期六与星期日当成假日。`CustomBusinessHour` 可以把节假日设为工作时间，详见下文。

### 自定义工作时间

*0.18.1 版新增*。

`CustomBusinessHour` 是 `BusinessHour` 和 `CustomBusinessDay` 的混合体，可以指定任意节假日。除了跳过自定义节假日之外，`CustomBusinessHour` 的运作方式与 `BusinessHour` 一样。

```python
In [225]: from pandas.tseries.holiday import USFederalHolidayCalendar

In [226]: bhour_us = pd.offsets.CustomBusinessHour(calendar=USFederalHolidayCalendar())

# 马丁路德金纪念日之前的星期五
In [227]: dt = datetime.datetime(2014, 1, 17, 15)

In [228]: dt + bhour_us
Out[228]: Timestamp('2014-01-17 16:00:00')

# 跳至马丁路德金纪念日之后的星期二，星期一过节，所以跳过了
In [229]: dt + bhour_us * 2
Out[229]: Timestamp('2014-01-21 09:00:00')
```

`BusinessHour` 支持与 `CustomBusinessDay` 一样的关键字参数。

```python
In [230]: bhour_mon = pd.offsets.CustomBusinessHour(start='10:00',
   .....:                                           weekmask='Tue Wed Thu Fri')
   .....: 

# 跳过了星期一，因为星期一过节，工作时间从 10 点开始
In [231]: dt + bhour_mon * 2
Out[231]: Timestamp('2014-01-21 10:00:00')
```

### 偏移量别名

时间序列频率的字符串别名在这里叫**偏移量别名**。

|   别名   | 说明                       |
| :------: | :------------------------- |
|    B     | 工作日频率                 |
|    C     | 自定义工作日频率           |
|    D     | 日历日频率                 |
|    W     | 周频率                     |
|    M     | 月末频率                   |
|    SM    | 半月末频率（15 号与月末）  |
|    BM    | 工作日月末频率             |
|   CBM    | 自定义工作日月末频率       |
|    MS    | 月初频率                   |
|   SMS    | 半月初频率（1 号与 15 号） |
|   BMS    | 工作日月初频率             |
|   CBMS   | 自定义工作日月初频率       |
|    Q     | 季末频率                   |
|    BQ    | 工作日季末频率             |
|    QS    | 季初频率                   |
|   BQS    | 工作日季初频率             |
|   A, Y   | 年末频率                   |
|  BA, BY  | 工作日年末频率             |
|  AS, YS  | 年初频率                   |
| BAS, BYS | 工作日年初频率             |
|    BH    | 工作时间频率               |
|    H     | 小时频率                   |
|  T, min  | 分钟频率                   |
|    S     | 秒频率                     |
|  L, ms   | 毫秒                       |
|  U, us   | 微秒                       |
|    N     | 纳秒                       |

### 别名组合

如前说述，别名与偏移量实例在绝大多数函数里可以互换：

```python
In [232]: pd.date_range(start, periods=5, freq='B')
Out[232]: 
DatetimeIndex(['2011-01-03', '2011-01-04', '2011-01-05', '2011-01-06',
               '2011-01-07'],
              dtype='datetime64[ns]', freq='B')

In [233]: pd.date_range(start, periods=5, freq=pd.offsets.BDay())
Out[233]: 
DatetimeIndex(['2011-01-03', '2011-01-04', '2011-01-05', '2011-01-06',
               '2011-01-07'],
              dtype='datetime64[ns]', freq='B')
```

可以组合日与当日偏移量。

```python
In [234]: pd.date_range(start, periods=10, freq='2h20min')
Out[234]: 
DatetimeIndex(['2011-01-01 00:00:00', '2011-01-01 02:20:00',
               '2011-01-01 04:40:00', '2011-01-01 07:00:00',
               '2011-01-01 09:20:00', '2011-01-01 11:40:00',
               '2011-01-01 14:00:00', '2011-01-01 16:20:00',
               '2011-01-01 18:40:00', '2011-01-01 21:00:00'],
              dtype='datetime64[ns]', freq='140T')

In [235]: pd.date_range(start, periods=10, freq='1D10U')
Out[235]: 
DatetimeIndex([       '2011-01-01 00:00:00', '2011-01-02 00:00:00.000010',
               '2011-01-03 00:00:00.000020', '2011-01-04 00:00:00.000030',
               '2011-01-05 00:00:00.000040', '2011-01-06 00:00:00.000050',
               '2011-01-07 00:00:00.000060', '2011-01-08 00:00:00.000070',
               '2011-01-09 00:00:00.000080', '2011-01-10 00:00:00.000090'],
              dtype='datetime64[ns]', freq='86400000010U')
```

### 锚定偏移量

可以指定某些频率的锚定后缀：

|    别名     | 说明                                  |
| :---------: | :------------------------------------ |
|    W-SUN    | 周频率（星期日），与 “W” 相同         |
|    W-MON    | 周频率（星期一）                      |
|    W-TUE    | 周频率（星期二）                      |
|    W-WED    | 周频率（星期三）                      |
|    W-THU    | 周频率（星期四）                      |
|    W-FRI    | 周频率（星期五）                      |
|    W-SAT    | 周频率（星期六）                      |
| (B)Q(S)-DEC | 季频率，该年结束于十二月，与 “Q” 相同 |
| (B)Q(S)-JAN | 季频率，该年结束于一月                |
| (B)Q(S)-FEB | 季频率，该年结束于二月                |
| (B)Q(S)-MAR | 季频率，该年结束于三月                |
| (B)Q(S)-APR | 季频率，该年结束于四月                |
| (B)Q(S)-MAY | 季频率，该年结束于五月                |
| (B)Q(S)-JUN | 季频率，该年结束于六月                |
| (B)Q(S)-JUL | 季频率，该年结束于七月                |
| (B)Q(S)-AUG | 季频率，该年结束于八月                |
| (B)Q(S)-SEP | 季频率，该年结束于九月                |
| (B)Q(S)-OCT | 季频率，该年结束于十月                |
| (B)Q(S)-NOV | 季频率，该年结束于十一月              |
| (B)A(S)-DEC | 年频率，锚定结束于十二月，与 “A” 相同 |
| (B)A(S)-JAN | 年频率，锚定结束于一月                |
| (B)A(S)-FEB | 年频率，锚定结束于二月                |
| (B)A(S)-MAR | 年频率，锚定结束于三月                |
| (B)A(S)-APR | 年频率，锚定结束于四月                |
| (B)A(S)-MAY | 年频率，锚定结束于五月                |
| (B)A(S)-JUN | 年频率，锚定结束于六月                |
| (B)A(S)-JUL | 年频率，锚定结束于七月                |
| (B)A(S)-AUG | 年频率，锚定结束于八月                |
| (B)A(S)-SEP | 年频率，锚定结束于九月                |
| (B)A(S)-OCT | 年频率，锚定结束于十月                |
| (B)A(S)-NOV | 年频率，锚定结束于十一月              |

这些别名可以用作 `date_range`、`bdate_range` 、`DatetimeIndex` 及其它时间序列函数的参数。

### 锚定偏移量的含义

对于偏移量锚定于开始或结束指定频率（`MonthEnd`、`MonthBegin`、`WeekEnd` 等）下列规则应用于前滚与后滚。

`n` 不为 0 时，如果给定日期不是锚定日期，将寻找下一个或上一个锚点，并向前或向后移动 `|n|-1 ` 步。

```python
In [236]: pd.Timestamp('2014-01-02') + pd.offsets.MonthBegin(n=1)
Out[236]: Timestamp('2014-02-01 00:00:00')

In [237]: pd.Timestamp('2014-01-02') + pd.offsets.MonthEnd(n=1)
Out[237]: Timestamp('2014-01-31 00:00:00')

In [238]: pd.Timestamp('2014-01-02') - pd.offsets.MonthBegin(n=1)
Out[238]: Timestamp('2014-01-01 00:00:00')

In [239]: pd.Timestamp('2014-01-02') - pd.offsets.MonthEnd(n=1)
Out[239]: Timestamp('2013-12-31 00:00:00')

In [240]: pd.Timestamp('2014-01-02') + pd.offsets.MonthBegin(n=4)
Out[240]: Timestamp('2014-05-01 00:00:00')

In [241]: pd.Timestamp('2014-01-02') - pd.offsets.MonthBegin(n=4)
Out[241]: Timestamp('2013-10-01 00:00:00')
```

如果给定日期是锚定日期，则向前（或向后）移动 `|n|` 个点。

```python
In [242]: pd.Timestamp('2014-01-01') + pd.offsets.MonthBegin(n=1)
Out[242]: Timestamp('2014-02-01 00:00:00')

In [243]: pd.Timestamp('2014-01-31') + pd.offsets.MonthEnd(n=1)
Out[243]: Timestamp('2014-02-28 00:00:00')

In [244]: pd.Timestamp('2014-01-01') - pd.offsets.MonthBegin(n=1)
Out[244]: Timestamp('2013-12-01 00:00:00')

In [245]: pd.Timestamp('2014-01-31') - pd.offsets.MonthEnd(n=1)
Out[245]: Timestamp('2013-12-31 00:00:00')

In [246]: pd.Timestamp('2014-01-01') + pd.offsets.MonthBegin(n=4)
Out[246]: Timestamp('2014-05-01 00:00:00')

In [247]: pd.Timestamp('2014-01-31') - pd.offsets.MonthBegin(n=4)
Out[247]: Timestamp('2013-10-01 00:00:00')
```

`n=0` 时，如果日期在锚点，则不移动，否则将前滚至下一个锚点。

```python
In [248]: pd.Timestamp('2014-01-02') + pd.offsets.MonthBegin(n=0)
Out[248]: Timestamp('2014-02-01 00:00:00')

In [249]: pd.Timestamp('2014-01-02') + pd.offsets.MonthEnd(n=0)
Out[249]: Timestamp('2014-01-31 00:00:00')

In [250]: pd.Timestamp('2014-01-01') + pd.offsets.MonthBegin(n=0)
Out[250]: Timestamp('2014-01-01 00:00:00')

In [251]: pd.Timestamp('2014-01-31') + pd.offsets.MonthEnd(n=0)
Out[251]: Timestamp('2014-01-31 00:00:00')
```

### 假日与节日日历

用假日与日历可以轻松定义 `CustomBusinessDay` 假日规则，或其它分析所需的预设假日。`AbstractHolidayCalendar` 类支持所有返回假日列表的方法，并且仅需在指定假日日历类里定义 `rules` 。`start_date` 与 `end_date` 类属性决定了假日的范围。该操作会覆盖 `AbstractHolidayCalendar` 类，适用于所有日历子类。`USFederalHolidayCalendar` 是仅有的假日日历，主要用作开发其它日历的示例。

固定日期的假日，如美国阵亡将士纪念日或美国国庆日（7 月 4 日），取决于该假日是否是在周末，可以使用以下规则：

|          规则          |                      说明                       |
| :--------------------: | :---------------------------------------------: |
|    nearest_workday     |      把星期六移至星期五，星期日移至星期一       |
|    sunday_to_monday    |               星期六紧接着星期一                |
| next_monday_or_tuesday | 把星期六移至星期一，并把星期日/星期一移至星期二 |
|    previous_friday     |        把星期六与星期日移至上一个星期五         |
|      next_monday       |        把星期六与星期日移至下一个星期一         |

下例展示如何定义假日与假日日历：

```python
In [252]: from pandas.tseries.holiday import Holiday, USMemorialDay,\
   .....:     AbstractHolidayCalendar, nearest_workday, MO
   .....: 

In [253]: class ExampleCalendar(AbstractHolidayCalendar):
   .....:     rules = [
   .....:         USMemorialDay,
   .....:         Holiday('July 4th', month=7, day=4, observance=nearest_workday),
   .....:         Holiday('Columbus Day', month=10, day=1,
   .....:                 offset=pd.DateOffset(weekday=MO(2)))]
   .....: 

In [254]: cal = ExampleCalendar()

In [255]: cal.holidays(datetime.datetime(2012, 1, 1), datetime.datetime(2012, 12, 31))
Out[255]: DatetimeIndex(['2012-05-28', '2012-07-04', '2012-10-08'], dtype='datetime64[ns]', freq=None)
```

::: tip 提示

`weekday=MO(2)` 与 `2 * Week(weekday=2)` 相同。

:::

用这个日历创建索引，或计算偏移量，将跳过周末与假日（如，纪念日与国庆节）。下列代码用 `ExampleCalendar` 设定自定义工作日偏移量。至于其它偏移量，可以用于创建 `DatetimeIndex` 或添加到 `datetime` 与 `Timestamp` 对象。

```python
In [256]: pd.date_range(start='7/1/2012', end='7/10/2012',
   .....:               freq=pd.offsets.CDay(calendar=cal)).to_pydatetime()
   .....: 
Out[256]: 
array([datetime.datetime(2012, 7, 2, 0, 0),
       datetime.datetime(2012, 7, 3, 0, 0),
       datetime.datetime(2012, 7, 5, 0, 0),
       datetime.datetime(2012, 7, 6, 0, 0),
       datetime.datetime(2012, 7, 9, 0, 0),
       datetime.datetime(2012, 7, 10, 0, 0)], dtype=object)

In [257]: offset = pd.offsets.CustomBusinessDay(calendar=cal)

In [258]: datetime.datetime(2012, 5, 25) + offset
Out[258]: Timestamp('2012-05-29 00:00:00')

In [259]: datetime.datetime(2012, 7, 3) + offset
Out[259]: Timestamp('2012-07-05 00:00:00')

In [260]: datetime.datetime(2012, 7, 3) + 2 * offset
Out[260]: Timestamp('2012-07-06 00:00:00')

In [261]: datetime.datetime(2012, 7, 6) + offset
Out[261]: Timestamp('2012-07-09 00:00:00')
```

`AbstractHolidayCalendar` 的类属性 `start_date` 与 `end_date` 定义日期范围。默认值如下：

```python
In [262]: AbstractHolidayCalendar.start_date
Out[262]: Timestamp('1970-01-01 00:00:00')

In [263]: AbstractHolidayCalendar.end_date
Out[263]: Timestamp('2030-12-31 00:00:00')
```

这两个日期可以用 `datetime`、`Timestamp`、`字符串` 修改。

```python
In [264]: AbstractHolidayCalendar.start_date = datetime.datetime(2012, 1, 1)

In [265]: AbstractHolidayCalendar.end_date = datetime.datetime(2012, 12, 31)

In [266]: cal.holidays()
Out[266]: DatetimeIndex(['2012-05-28', '2012-07-04', '2012-10-08'], dtype='datetime64[ns]', freq=None)
```

`get_calender` 函数通过日历名称访问日历，返回的是日历实例。任意导入的日历都自动适用于此函数。同时，`HolidayCalendarFactory` 还提供了一个创建日历组合或含附加规则日历的简易接口。

```python
In [267]: from pandas.tseries.holiday import get_calendar, HolidayCalendarFactory,\
   .....:     USLaborDay
   .....: 

In [268]: cal = get_calendar('ExampleCalendar')

In [269]: cal.rules
Out[269]: 
[Holiday: Memorial Day (month=5, day=31, offset=<DateOffset: weekday=MO(-1)>),
 Holiday: July 4th (month=7, day=4, observance=<function nearest_workday at 0x7f2460862c20>),
 Holiday: Columbus Day (month=10, day=1, offset=<DateOffset: weekday=MO(+2)>)]

In [270]: new_cal = HolidayCalendarFactory('NewExampleCalendar', cal, USLaborDay)

In [271]: new_cal.rules
Out[271]: 
[Holiday: Labor Day (month=9, day=1, offset=<DateOffset: weekday=MO(+1)>),
 Holiday: Memorial Day (month=5, day=31, offset=<DateOffset: weekday=MO(-1)>),
 Holiday: July 4th (month=7, day=4, observance=<function nearest_workday at 0x7f2460862c20>),
 Holiday: Columbus Day (month=10, day=1, offset=<DateOffset: weekday=MO(+2)>)]
```

## 时间序列实例方法

### 移位与延迟

有时，需要整体向前或向后移动时间序列里的值，这就是移位与延迟。实现这一操作的方法是 [`shift()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.shift.html#pandas.Series.shift "pandas.Series.shift")，该方法适用于所有 Pandas 对象。

```python
In [272]: ts = pd.Series(range(len(rng)), index=rng)

In [273]: ts = ts[:5]

In [274]: ts.shift(1)
Out[274]: 
2012-01-01    NaN
2012-01-02    0.0
2012-01-03    1.0
Freq: D, dtype: float64
```

`shift` 方法支持 `freq` 参数，可以把 `DateOffset`、`timedelta` 对象、[`偏移量别名`](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases) 作为参数值：

```python
In [275]: ts.shift(5, freq=pd.offsets.BDay())
Out[275]: 
2012-01-06    0
2012-01-09    1
2012-01-10    2
Freq: B, dtype: int64

In [276]: ts.shift(5, freq='BM')
Out[276]: 
2012-05-31    0
2012-05-31    1
2012-05-31    2
Freq: D, dtype: int64
```

除更改数据与索引的对齐方式外，`DataFrame` 与 `Series` 对象还提供了 [`tshift()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.tshift.html#pandas.Series.tshift "pandas.Series.tshift") 便捷方法，可以指定偏移量修改索引日期。

```python
In [277]: ts.tshift(5, freq='D')
Out[277]: 
2012-01-06    0
2012-01-07    1
2012-01-08    2
Freq: D, dtype: int64
```

注意，使用 `tshift()` 时，因为数据没有重对齐，` NaN ` 不会排在前面。

### 频率转换

改变频率的函数主要是 [`asfreq()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.asfreq.html#pandas.Series.asfreq "pandas.Series.asfreq")。对于 `DatetimeIndex`，这就是一个调用 [`reindex()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.reindex.html#pandas.Series.reindex "pandas.Series.reindex")，并生成 `date_range` 的便捷打包器。

```python
In [278]: dr = pd.date_range('1/1/2010', periods=3, freq=3 * pd.offsets.BDay())

In [279]: ts = pd.Series(np.random.randn(3), index=dr)

In [280]: ts
Out[280]: 
2010-01-01    1.494522
2010-01-06   -0.778425
2010-01-11   -0.253355
Freq: 3B, dtype: float64

In [281]: ts.asfreq(pd.offsets.BDay())
Out[281]: 
2010-01-01    1.494522
2010-01-04         NaN
2010-01-05         NaN
2010-01-06   -0.778425
2010-01-07         NaN
2010-01-08         NaN
2010-01-11   -0.253355
Freq: B, dtype: float64
```

`asfreq` 用起来很方便，可以为频率转化后出现的任意间隔指定插值方法。

```python
In [282]: ts.asfreq(pd.offsets.BDay(), method='pad')
Out[282]: 
2010-01-01    1.494522
2010-01-04    1.494522
2010-01-05    1.494522
2010-01-06   -0.778425
2010-01-07   -0.778425
2010-01-08   -0.778425
2010-01-11   -0.253355
Freq: B, dtype: float64
```

### 向前与向后填充

与 `asfreq` 与 `reindex` 相关的是 [`fillna()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.fillna.html#pandas.Series.fillna "pandas.Series.fillna")，有关文档请参阅[缺失值](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-fillna)。

### 转换 Python 日期与时间

用 `to_datetime` 方法可以把`DatetimeIndex` 转换为 Python 原生 [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.7)") 对象数组。

## 重采样

::: danger 警告

0.18.0 版修改了 `.resample` 接口，现在的 `.resample` 更灵活，更像 groupby。参阅[更新文档](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.18.0.html#whatsnew-0180-breaking-resample) ，对比新旧版本操作的区别。

:::

Pandas 有一个虽然简单，但却强大、高效的功能，可在频率转换时执行重采样，如，将秒数据转换为 5 分钟数据，这种操作在金融等领域里的应用非常广泛。

[`resample()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.resample.html#pandas.Series.resample "pandas.Series.resample") 是基于时间的分组操作，每个组都遵循归纳方法。参阅 [Cookbook 示例](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#cookbook-resample)了解高级应用。

从 0.18.0 版开始，`resample()` 可以直接用于 `DataFrameGroupBy` 对象，参阅 [groupby 文档](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-transform-window-resample)。

::: tip 注意

`.resample()` 类似于基于时间偏移量的 [`rolling()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rolling.html#pandas.Series.rolling "pandas.Series.rolling") 操作，请参阅[这里](https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#stats-moments-ts-versus-resampling)的讨论。

:::

### 基础知识

```python
In [283]: rng = pd.date_range('1/1/2012', periods=100, freq='S')

In [284]: ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)

In [285]: ts.resample('5Min').sum()
Out[285]: 
2012-01-01    25103
Freq: 5T, dtype: int64
```

`resample` 函数非常灵活，可以指定多种频率转换与重采样参数。

任何支持[派送（dispatch）](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-dispatch)的函数都可用于 `resample` 返回对象，包括 `sum`、`mean`、`std`、`sem`、`max`、`min`、`mid`、`median`、`first`、`last`、`ohlc`：

```python
In [286]: ts.resample('5Min').mean()
Out[286]: 
2012-01-01    251.03
Freq: 5T, dtype: float64

In [287]: ts.resample('5Min').ohlc()
Out[287]: 
            open  high  low  close
2012-01-01   308   460    9    205

In [288]: ts.resample('5Min').max()
Out[288]: 
2012-01-01    460
Freq: 5T, dtype: int64
```

对于下采样，`closed` 可以设置为`left` 或 `right`，用于指定关闭哪一端间隔：

```python
In [289]: ts.resample('5Min', closed='right').mean()
Out[289]: 
2011-12-31 23:55:00    308.000000
2012-01-01 00:00:00    250.454545
Freq: 5T, dtype: float64

In [290]: ts.resample('5Min', closed='left').mean()
Out[290]: 
2012-01-01    251.03
Freq: 5T, dtype: float64
```

`label`、`loffset` 等参数用于生成标签。`label` 指定生成的结果是否要为间隔标注起始时间。`loffset` 调整输出标签的时间。

```python
In [291]: ts.resample('5Min').mean()  # 默认为 label='left'
Out[291]: 
2012-01-01    251.03
Freq: 5T, dtype: float64

In [292]: ts.resample('5Min', label='left').mean()
Out[292]: 
2012-01-01    251.03
Freq: 5T, dtype: float64

In [293]: ts.resample('5Min', label='left', loffset='1s').mean()
Out[293]: 
2012-01-01 00:00:01    251.03
dtype: float64
```


::: danger 警告

除了 `M`、`A`、`Q`、`BM`、`BA`、`BQ`、`W` 的默认值是 `right` 外，其它频率偏移量的 `label` 与 `closed` 默认值都是 `left`。

这种操作可能会导致时间回溯，即后面的时间会被拉回到前面的时间，如下例的 [`BusinessDay`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.tseries.offsets.BusinessDay.html#pandas.tseries.offsets.BusinessDay "pandas.tseries.offsets.BusinessDay") 频率所示。

```python
In [294]: s = pd.date_range('2000-01-01', '2000-01-05').to_series()

In [295]: s.iloc[2] = pd.NaT

In [296]: s.dt.weekday_name
Out[296]: 
2000-01-01     Saturday
2000-01-02       Sunday
2000-01-03          NaN
2000-01-04      Tuesday
2000-01-05    Wednesday
Freq: D, dtype: object

# 默认为：label='left', closed='left'
In [297]: s.resample('B').last().dt.weekday_name
Out[297]: 
1999-12-31       Sunday
2000-01-03          NaN
2000-01-04      Tuesday
2000-01-05    Wednesday
Freq: B, dtype: object
```

看到了吗？星期日被拉回到了上一个星期五。要想把星期日移至星期一，改用以下代码：

```python
In [298]: s.resample('B', label='right', closed='right').last().dt.weekday_name
Out[298]: 
2000-01-03       Sunday
2000-01-04      Tuesday
2000-01-05    Wednesday
Freq: B, dtype: object
```
:::

`axis` 参数的值为 `0` 或 `1`，并可指定 `DataFrame` 重采样的轴。

`kind` 参数可以是 `timestamp` 或 `period`，转换为时间戳或时间段形式的索引。`resample` 默认保留输入的日期时间形式。

重采样 `period` 数据时（详情见下文），`convention` 可以设置为 `start` 或 `end`。指定低频时间段如何转换为高频时间段。

### 上采样

上采样可以指定上采样的方式及插入时间间隔的 `limit` 参数：

```python
# 从秒到每 250 毫秒
In [299]: ts[:2].resample('250L').asfreq()
Out[299]: 
2012-01-01 00:00:00.000    308.0
2012-01-01 00:00:00.250      NaN
2012-01-01 00:00:00.500      NaN
2012-01-01 00:00:00.750      NaN
2012-01-01 00:00:01.000    204.0
Freq: 250L, dtype: float64

In [300]: ts[:2].resample('250L').ffill()
Out[300]: 
2012-01-01 00:00:00.000    308
2012-01-01 00:00:00.250    308
2012-01-01 00:00:00.500    308
2012-01-01 00:00:00.750    308
2012-01-01 00:00:01.000    204
Freq: 250L, dtype: int64

In [301]: ts[:2].resample('250L').ffill(limit=2)
Out[301]: 
2012-01-01 00:00:00.000    308.0
2012-01-01 00:00:00.250    308.0
2012-01-01 00:00:00.500    308.0
2012-01-01 00:00:00.750      NaN
2012-01-01 00:00:01.000    204.0
Freq: 250L, dtype: float64
```

### 稀疏重采样

相对于时间点总量，稀疏时间序列重采样的点要少很多。单纯上采样稀疏系列可能会生成很多中间值。未指定填充值，即 `fill_method` 是 `None` 时，中间值将填充为 `NaN`。

鉴于 `resample` 是基于时间的分组，下列这种方法可以有效重采样，只是分组不是都为 `NaN`。

```python
In [302]: rng = pd.date_range('2014-1-1', periods=100, freq='D') + pd.Timedelta('1s')

In [303]: ts = pd.Series(range(100), index=rng)
```

对 `Series` 全范围重采样。

```python
In [304]: ts.resample('3T').sum()
Out[304]: 
2014-01-01 00:00:00     0
2014-01-01 00:03:00     0
2014-01-01 00:06:00     0
2014-01-01 00:09:00     0
2014-01-01 00:12:00     0
                       ..
2014-04-09 23:48:00     0
2014-04-09 23:51:00     0
2014-04-09 23:54:00     0
2014-04-09 23:57:00     0
2014-04-10 00:00:00    99
Freq: 3T, Length: 47521, dtype: int64
```

对以下包含点的分组重采样：

```python
In [305]: from functools import partial

In [306]: from pandas.tseries.frequencies import to_offset

In [307]: def round(t, freq):
   .....:     freq = to_offset(freq)
   .....:     return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)
   .....: 

In [308]: ts.groupby(partial(round, freq='3T')).sum()
Out[308]: 
2014-01-01     0
2014-01-02     1
2014-01-03     2
2014-01-04     3
2014-01-05     4
              ..
2014-04-06    95
2014-04-07    96
2014-04-08    97
2014-04-09    98
2014-04-10    99
Length: 100, dtype: int64
```

### 聚合

类似于[聚合 API](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-aggregate)，[Groupby API](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-aggregate) 及[窗口函数 API](https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#stats-aggregate)，`Resampler` 可以有选择地重采样。

`DataFrame` 重采样，默认用相同函数操作所有列。

```python
In [309]: df = pd.DataFrame(np.random.randn(1000, 3),
   .....:                   index=pd.date_range('1/1/2012', freq='S', periods=1000),
   .....:                   columns=['A', 'B', 'C'])
   .....: 

In [310]: r = df.resample('3T')

In [311]: r.mean()
Out[311]: 
                            A         B         C
2012-01-01 00:00:00 -0.033823 -0.121514 -0.081447
2012-01-01 00:03:00  0.056909  0.146731 -0.024320
2012-01-01 00:06:00 -0.058837  0.047046 -0.052021
2012-01-01 00:09:00  0.063123 -0.026158 -0.066533
2012-01-01 00:12:00  0.186340 -0.003144  0.074752
2012-01-01 00:15:00 -0.085954 -0.016287 -0.050046
```

标准 `getitem` 操作可以指定的一列或多列。



```python
In [312]: r['A'].mean()
Out[312]: 
2012-01-01 00:00:00   -0.033823
2012-01-01 00:03:00    0.056909
2012-01-01 00:06:00   -0.058837
2012-01-01 00:09:00    0.063123
2012-01-01 00:12:00    0.186340
2012-01-01 00:15:00   -0.085954
Freq: 3T, Name: A, dtype: float64

In [313]: r[['A', 'B']].mean()
Out[313]: 
                            A         B
2012-01-01 00:00:00 -0.033823 -0.121514
2012-01-01 00:03:00  0.056909  0.146731
2012-01-01 00:06:00 -0.058837  0.047046
2012-01-01 00:09:00  0.063123 -0.026158
2012-01-01 00:12:00  0.186340 -0.003144
2012-01-01 00:15:00 -0.085954 -0.016287
```

聚合还支持函数列表与字典，输出的是 `DataFrame`。

```python
In [314]: r['A'].agg([np.sum, np.mean, np.std])
Out[314]: 
                           sum      mean       std
2012-01-01 00:00:00  -6.088060 -0.033823  1.043263
2012-01-01 00:03:00  10.243678  0.056909  1.058534
2012-01-01 00:06:00 -10.590584 -0.058837  0.949264
2012-01-01 00:09:00  11.362228  0.063123  1.028096
2012-01-01 00:12:00  33.541257  0.186340  0.884586
2012-01-01 00:15:00  -8.595393 -0.085954  1.035476
```

重采样后的 `DataFrame`，可以为每列指定函数列表，生成结构化索引的聚合结果：

```python
In [315]: r.agg([np.sum, np.mean])
Out[315]: 
                             A                    B                    C          
                           sum      mean        sum      mean        sum      mean
2012-01-01 00:00:00  -6.088060 -0.033823 -21.872530 -0.121514 -14.660515 -0.081447
2012-01-01 00:03:00  10.243678  0.056909  26.411633  0.146731  -4.377642 -0.024320
2012-01-01 00:06:00 -10.590584 -0.058837   8.468289  0.047046  -9.363825 -0.052021
2012-01-01 00:09:00  11.362228  0.063123  -4.708526 -0.026158 -11.975895 -0.066533
2012-01-01 00:12:00  33.541257  0.186340  -0.565895 -0.003144  13.455299  0.074752
2012-01-01 00:15:00  -8.595393 -0.085954  -1.628689 -0.016287  -5.004580 -0.050046
```

把字典传递给 `aggregate`，可以为 `DataFrame` 里不同的列应用不同聚合函数。

```python
In [316]: r.agg({'A': np.sum,
   .....:        'B': lambda x: np.std(x, ddof=1)})
   .....: 
Out[316]: 
                             A         B
2012-01-01 00:00:00  -6.088060  1.001294
2012-01-01 00:03:00  10.243678  1.074597
2012-01-01 00:06:00 -10.590584  0.987309
2012-01-01 00:09:00  11.362228  0.944953
2012-01-01 00:12:00  33.541257  1.095025
2012-01-01 00:15:00  -8.595393  1.035312
```

还可以用字符串代替函数名。为了让字符串有效，必须在重采样对象上操作：

```python
In [317]: r.agg({'A': 'sum', 'B': 'std'})
Out[317]: 
                             A         B
2012-01-01 00:00:00  -6.088060  1.001294
2012-01-01 00:03:00  10.243678  1.074597
2012-01-01 00:06:00 -10.590584  0.987309
2012-01-01 00:09:00  11.362228  0.944953
2012-01-01 00:12:00  33.541257  1.095025
2012-01-01 00:15:00  -8.595393  1.035312
```

甚至还可以为每列单独多个聚合函数。

```python
In [318]: r.agg({'A': ['sum', 'std'], 'B': ['mean', 'std']})
Out[318]: 
                             A                   B          
                           sum       std      mean       std
2012-01-01 00:00:00  -6.088060  1.043263 -0.121514  1.001294
2012-01-01 00:03:00  10.243678  1.058534  0.146731  1.074597
2012-01-01 00:06:00 -10.590584  0.949264  0.047046  0.987309
2012-01-01 00:09:00  11.362228  1.028096 -0.026158  0.944953
2012-01-01 00:12:00  33.541257  0.884586 -0.003144  1.095025
2012-01-01 00:15:00  -8.595393  1.035476 -0.016287  1.035312
```

如果 `DataFrame` 用的不是 `datetime` 型索引，则可以基于 `datetime` 数据列重采样，用关键字 `on` 控制。

```python
In [319]: df = pd.DataFrame({'date': pd.date_range('2015-01-01', freq='W', periods=5),
   .....:                    'a': np.arange(5)},
   .....:                   index=pd.MultiIndex.from_arrays([
   .....:                       [1, 2, 3, 4, 5],
   .....:                       pd.date_range('2015-01-01', freq='W', periods=5)],
   .....:                       names=['v', 'd']))
   .....: 

In [320]: df
Out[320]: 
                   date  a
v d                       
1 2015-01-04 2015-01-04  0
2 2015-01-11 2015-01-11  1
3 2015-01-18 2015-01-18  2
4 2015-01-25 2015-01-25  3
5 2015-02-01 2015-02-01  4

In [321]: df.resample('M', on='date').sum()
Out[321]: 
            a
date         
2015-01-31  6
2015-02-28  4
```

同样，还可以对 `datetime MultiIndex` 重采样，通过关键字 `level` 传递名字与位置。

```python
In [322]: df.resample('M', level='d').sum()
Out[322]: 
            a
d            
2015-01-31  6
2015-02-28  4
```

### 分组迭代

`Resampler`对象迭代分组数据的操作非常自然，类似于  [`itertools.groupby()`](https://docs.python.org/3/library/itertools.html#itertools.groupby "(in Python v3.7)")：

```python
In [323]: small = pd.Series(
   .....:     range(6),
   .....:     index=pd.to_datetime(['2017-01-01T00:00:00',
   .....:                           '2017-01-01T00:30:00',
   .....:                           '2017-01-01T00:31:00',
   .....:                           '2017-01-01T01:00:00',
   .....:                           '2017-01-01T03:00:00',
   .....:                           '2017-01-01T03:05:00'])
   .....: )
   .....: 

In [324]: resampled = small.resample('H')

In [325]: for name, group in resampled:
   .....:     print("Group: ", name)
   .....:     print("-" * 27)
   .....:     print(group, end="\n\n")
   .....: 
Group:  2017-01-01 00:00:00
---------------------------
2017-01-01 00:00:00    0
2017-01-01 00:30:00    1
2017-01-01 00:31:00    2
dtype: int64

Group:  2017-01-01 01:00:00
---------------------------
2017-01-01 01:00:00    3
dtype: int64

Group:  2017-01-01 02:00:00
---------------------------
Series([], dtype: int64)

Group:  2017-01-01 03:00:00
---------------------------
2017-01-01 03:00:00    4
2017-01-01 03:05:00    5
dtype: int64
```

了解更多详情，请参阅[分组迭代](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-iterating-label)或 [`itertools.groupby()`](https://docs.python.org/3/library/itertools.html#itertools.groupby "(in Python v3.7)")。

## 时间跨度表示

规律时间间隔可以用 Pandas 的 `Peirod` 对象表示，`Period` 对象序列叫做 `PeriodIndex`，用便捷函数 `period_range` 创建。

### Period

`Period` 表示时间跨度，即时间段，如年、季、月、日等。关键字 `freq` 与频率别名可以指定时间段。`freq` 表示的是 `Period` 的时间跨度，不能为负，如，`-3D`。

```python
In [326]: pd.Period('2012', freq='A-DEC')
Out[326]: Period('2012', 'A-DEC')

In [327]: pd.Period('2012-1-1', freq='D')
Out[327]: Period('2012-01-01', 'D')

In [328]: pd.Period('2012-1-1 19:00', freq='H')
Out[328]: Period('2012-01-01 19:00', 'H')

In [329]: pd.Period('2012-1-1 19:00', freq='5H')
Out[329]: Period('2012-01-01 19:00', '5H')
```

时间段加减法按自身频率位移。 不同频率的时间段不可进行算术运算。

```python
In [330]: p = pd.Period('2012', freq='A-DEC')

In [331]: p + 1
Out[331]: Period('2013', 'A-DEC')

In [332]: p - 3
Out[332]: Period('2009', 'A-DEC')

In [333]: p = pd.Period('2012-01', freq='2M')

In [334]: p + 2
Out[334]: Period('2012-05', '2M')

In [335]: p - 1
Out[335]: Period('2011-11', '2M')

In [336]: p == pd.Period('2012-01', freq='3M')
---------------------------------------------------------------------------
IncompatibleFrequency                     Traceback (most recent call last)
<ipython-input-336-4b67dc0b596c> in <module>
----> 1 p == pd.Period('2012-01', freq='3M')

/pandas/pandas/_libs/tslibs/period.pyx in pandas._libs.tslibs.period._Period.__richcmp__()

IncompatibleFrequency: Input has different freq=3M from Period(freq=2M)
```

`freq` 的频率为日或更高频率时，如 `D`、`H`、`T`、`S`、`L`、`U`、`N`，`offsets` 与 `timedelta` 可以用相同频率实现加法。否则，会触发 `ValueError`。

```python
In [337]: p = pd.Period('2014-07-01 09:00', freq='H')

In [338]: p + pd.offsets.Hour(2)
Out[338]: Period('2014-07-01 11:00', 'H')

In [339]: p + datetime.timedelta(minutes=120)
Out[339]: Period('2014-07-01 11:00', 'H')

In [340]: p + np.timedelta64(7200, 's')
Out[340]: Period('2014-07-01 11:00', 'H')
In [1]: p + pd.offsets.Minute(5)
Traceback
   ...
ValueError: Input has different freq from Period(freq=H)
```

如果 `Period` 为其它频率，只有相同频率的 `offsets` 可以相加。否则，会触发 `ValueError`。

```python
In [341]: p = pd.Period('2014-07', freq='M')

In [342]: p + pd.offsets.MonthEnd(3)
Out[342]: Period('2014-10', 'M')
In [1]: p + pd.offsets.MonthBegin(3)
Traceback
   ...
ValueError: Input has different freq from Period(freq=M)
```

用相同频率计算不同时间段实例之间的区别，将返回这些实例之间的频率单元数量。

```python
In [343]: pd.Period('2012', freq='A-DEC') - pd.Period('2002', freq='A-DEC')
Out[343]: <10 * YearEnds: month=12>
```

### PeriodIndex 与 period_range

 `period_range` 便捷函数可以创建有规律的 `Period` 对象序列，即 `PeriodIndex`。

```python
In [344]: prng = pd.period_range('1/1/2011', '1/1/2012', freq='M')

In [345]: prng
Out[345]: 
PeriodIndex(['2011-01', '2011-02', '2011-03', '2011-04', '2011-05', '2011-06',
             '2011-07', '2011-08', '2011-09', '2011-10', '2011-11', '2011-12',
             '2012-01'],
            dtype='period[M]', freq='M')
```

也可以直接用 `PeriodIndex` 创建：

```python
In [346]: pd.PeriodIndex(['2011-1', '2011-2', '2011-3'], freq='M')
Out[346]: PeriodIndex(['2011-01', '2011-02', '2011-03'], dtype='period[M]', freq='M')
```

频率为复数时，输出的 `Period` 序列为复数时间段。

```python
In [347]: pd.period_range(start='2014-01', freq='3M', periods=4)
Out[347]: PeriodIndex(['2014-01', '2014-04', '2014-07', '2014-10'], dtype='period[3M]', freq='3M')
```

`Period` 对象的 `start` 或 `end` 会被当作 `PeriodIndex` 的锚定终点，其频率与 `PeriodIndex` 的频率一样。

```python
In [348]: pd.period_range(start=pd.Period('2017Q1', freq='Q'),
   .....:                 end=pd.Period('2017Q2', freq='Q'), freq='M')
   .....: 
Out[348]: PeriodIndex(['2017-03', '2017-04', '2017-05', '2017-06'], dtype='period[M]', freq='M')
```

和 `DatetimeIndex` 一样，`PeriodIndex` 也可以作为 Pandas 对象的索引。

```python
In [349]: ps = pd.Series(np.random.randn(len(prng)), prng)

In [350]: ps
Out[350]: 
2011-01   -2.916901
2011-02    0.514474
2011-03    1.346470
2011-04    0.816397
2011-05    2.258648
2011-06    0.494789
2011-07    0.301239
2011-08    0.464776
2011-09   -1.393581
2011-10    0.056780
2011-11    0.197035
2011-12    2.261385
2012-01   -0.329583
Freq: M, dtype: float64
```

`PeriodIndex` 的加减法与 `Period` 一样。

```python
In [351]: idx = pd.period_range('2014-07-01 09:00', periods=5, freq='H')

In [352]: idx
Out[352]: 
PeriodIndex(['2014-07-01 09:00', '2014-07-01 10:00', '2014-07-01 11:00',
             '2014-07-01 12:00', '2014-07-01 13:00'],
            dtype='period[H]', freq='H')

In [353]: idx + pd.offsets.Hour(2)
Out[353]: 
PeriodIndex(['2014-07-01 11:00', '2014-07-01 12:00', '2014-07-01 13:00',
             '2014-07-01 14:00', '2014-07-01 15:00'],
            dtype='period[H]', freq='H')

In [354]: idx = pd.period_range('2014-07', periods=5, freq='M')

In [355]: idx
Out[355]: PeriodIndex(['2014-07', '2014-08', '2014-09', '2014-10', '2014-11'], dtype='period[M]', freq='M')

In [356]: idx + pd.offsets.MonthEnd(3)
Out[356]: PeriodIndex(['2014-10', '2014-11', '2014-12', '2015-01', '2015-02'], dtype='period[M]', freq='M')
```

`PeriodIndex` 有自己的数据类型，即 `period`，请参阅 [Period 数据类型](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-period-dtype)。

### Period 数据类型

*0.19.0 版新增*。

`PeriodIndex` 的自定义数据类型是 `period`，是 Pandas 扩展数据类型，类似于[带时区信息的数据类型](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-timezone-series)（`datetime64[ns, tz]`）。

`Period` 数据类型支持 `freq` 属性，还可以用 `period[freq]` 表示，如，`period[D]` 或 `period[M]`，这里用的是[频率字符串](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases)。

```python
In [357]: pi = pd.period_range('2016-01-01', periods=3, freq='M')

In [358]: pi
Out[358]: PeriodIndex(['2016-01', '2016-02', '2016-03'], dtype='period[M]', freq='M')

In [359]: pi.dtype
Out[359]: period[M]
```

`period` 数据类型在 `.astype(...)` 里使用。允许改变 `PeriodIndex` 的 `freq`， 如 `.asfreq()`，并用 `to_period()` 把 `DatetimeIndex` 转化为 `PeriodIndex`：

```python
# 把月频改为日频
In [360]: pi.astype('period[D]')
Out[360]: PeriodIndex(['2016-01-31', '2016-02-29', '2016-03-31'], dtype='period[D]', freq='D')

# 转换为 DatetimeIndex
In [361]: pi.astype('datetime64[ns]')
Out[361]: DatetimeIndex(['2016-01-01', '2016-02-01', '2016-03-01'], dtype='datetime64[ns]', freq='MS')

# 转换为 PeriodIndex
In [362]: dti = pd.date_range('2011-01-01', freq='M', periods=3)

In [363]: dti
Out[363]: DatetimeIndex(['2011-01-31', '2011-02-28', '2011-03-31'], dtype='datetime64[ns]', freq='M')

In [364]: dti.astype('period[M]')
Out[364]: PeriodIndex(['2011-01', '2011-02', '2011-03'], dtype='period[M]', freq='M')
```

### PeriodIndex 局部字符串索引

与 `DatetimeIndex` 一样，`PeriodIndex` 可以把日期与字符串传递给 `Series` 与 `DataFrame`。详情请参阅 [DatetimeIndex 局部字符串索引](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-partialindexing)。

```python
In [365]: ps['2011-01']
Out[365]: -2.9169013294054507

In [366]: ps[datetime.datetime(2011, 12, 25):]
Out[366]: 
2011-12    2.261385
2012-01   -0.329583
Freq: M, dtype: float64

In [367]: ps['10/31/2011':'12/31/2011']
Out[367]: 
2011-10    0.056780
2011-11    0.197035
2011-12    2.261385
Freq: M, dtype: float64
```

传递比 `PeriodIndex` 更低频率的字符串会返回局部切片数据。

```python
In [368]: ps['2011']
Out[368]: 
2011-01   -2.916901
2011-02    0.514474
2011-03    1.346470
2011-04    0.816397
2011-05    2.258648
2011-06    0.494789
2011-07    0.301239
2011-08    0.464776
2011-09   -1.393581
2011-10    0.056780
2011-11    0.197035
2011-12    2.261385
Freq: M, dtype: float64

In [369]: dfp = pd.DataFrame(np.random.randn(600, 1),
   .....:                    columns=['A'],
   .....:                    index=pd.period_range('2013-01-01 9:00',
   .....:                                          periods=600,
   .....:                                          freq='T'))
   .....: 

In [370]: dfp
Out[370]: 
                         A
2013-01-01 09:00 -0.538468
2013-01-01 09:01 -1.365819
2013-01-01 09:02 -0.969051
2013-01-01 09:03 -0.331152
2013-01-01 09:04 -0.245334
...                    ...
2013-01-01 18:55  0.522460
2013-01-01 18:56  0.118710
2013-01-01 18:57  0.167517
2013-01-01 18:58  0.922883
2013-01-01 18:59  1.721104

[600 rows x 1 columns]

In [371]: dfp['2013-01-01 10H']
Out[371]: 
                         A
2013-01-01 10:00 -0.308975
2013-01-01 10:01  0.542520
2013-01-01 10:02  1.061068
2013-01-01 10:03  0.754005
2013-01-01 10:04  0.352933
...                    ...
2013-01-01 10:55 -0.865621
2013-01-01 10:56 -1.167818
2013-01-01 10:57 -2.081748
2013-01-01 10:58 -0.527146
2013-01-01 10:59  0.802298

[60 rows x 1 columns]
```

与 `DatetimeIndex` 一样，终点包含在结果范围之内。下例中的切片数据就是从 10:00 到 11:59。

```python
In [372]: dfp['2013-01-01 10H':'2013-01-01 11H']
Out[372]: 
                         A
2013-01-01 10:00 -0.308975
2013-01-01 10:01  0.542520
2013-01-01 10:02  1.061068
2013-01-01 10:03  0.754005
2013-01-01 10:04  0.352933
...                    ...
2013-01-01 11:55 -0.590204
2013-01-01 11:56  1.539990
2013-01-01 11:57 -1.224826
2013-01-01 11:58  0.578798
2013-01-01 11:59 -0.685496

[120 rows x 1 columns]
```

### 频率转换与 `PeriodIndex` 重采样

`Period` 与 `PeriodIndex` 的频率可以用 `asfreq` 转换。下列代码开始于 2011 财年，结束时间为十二月：

```python
In [373]: p = pd.Period('2011', freq='A-DEC')

In [374]: p
Out[374]: Period('2011', 'A-DEC')
```

可以把它转换为月频。使用 `how` 参数，指定是否返回开始或结束月份。

```python
In [375]: p.asfreq('M', how='start')
Out[375]: Period('2011-01', 'M')

In [376]: p.asfreq('M', how='end')
Out[376]: Period('2011-12', 'M')
```

简称 `s` 与 `e` 用起来更方便：

```python
In [377]: p.asfreq('M', 's')
Out[377]: Period('2011-01', 'M')

In [378]: p.asfreq('M', 'e')
Out[378]: Period('2011-12', 'M')
```

转换为“超级 period”，（如，年频就是季频的超级 period），自动返回包含输入时间段的超级 period：

```python
In [379]: p = pd.Period('2011-12', freq='M')

In [380]: p.asfreq('A-NOV')
Out[380]: Period('2012', 'A-NOV')
```

注意，因为转换年频是在十一月结束的，2011 年 12 月的月时间段实际上是 `2012 A-NOV` period。

用锚定频率转换时间段，对经济学、商业等领域里的各种季度数据特别有用。很多公司都依据其财年开始月与结束月定义季度。因此，2011 年第一个季度有可能 2010 年就开始了，也有可能 2011 年过了几个月才开始。通过锚定频率，Pandas 可以处理所有从 `Q-JAN` 至 `Q-DEC`的季度频率。

`Q-DEC` 定义的是常规日历季度：

```python
In [381]: p = pd.Period('2012Q1', freq='Q-DEC')

In [382]: p.asfreq('D', 's')
Out[382]: Period('2012-01-01', 'D')

In [383]: p.asfreq('D', 'e')
Out[383]: Period('2012-03-31', 'D')
```

`Q-MAR` 定义的是财年结束于三月：

```python
In [384]: p = pd.Period('2011Q4', freq='Q-MAR')

In [385]: p.asfreq('D', 's')
Out[385]: Period('2011-01-01', 'D')

In [386]: p.asfreq('D', 'e')
Out[386]: Period('2011-03-31', 'D')
```

### 不同表现形式之间的转换

`to_period` 把时间戳转换为 `PeriodIndex`，`to_timestamp` 则执行反向操作。

```python
In [387]: rng = pd.date_range('1/1/2012', periods=5, freq='M')

In [388]: ts = pd.Series(np.random.randn(len(rng)), index=rng)

In [389]: ts
Out[389]: 
2012-01-31    1.931253
2012-02-29   -0.184594
2012-03-31    0.249656
2012-04-30   -0.978151
2012-05-31   -0.873389
Freq: M, dtype: float64

In [390]: ps = ts.to_period()

In [391]: ps
Out[391]: 
2012-01    1.931253
2012-02   -0.184594
2012-03    0.249656
2012-04   -0.978151
2012-05   -0.873389
Freq: M, dtype: float64

In [392]: ps.to_timestamp()
Out[392]: 
2012-01-01    1.931253
2012-02-01   -0.184594
2012-03-01    0.249656
2012-04-01   -0.978151
2012-05-01   -0.873389
Freq: MS, dtype: float64
```

记住 `s` 与 `e` 返回 `period` 开始或结束的时间戳：

```python
In [393]: ps.to_timestamp('D', how='s')
Out[393]: 
2012-01-01    1.931253
2012-02-01   -0.184594
2012-03-01    0.249656
2012-04-01   -0.978151
2012-05-01   -0.873389
Freq: MS, dtype: float64
```

用便捷算数函数可以转换时间段与时间戳。下例中，把以 11 月年度结束的季频转换为以下一个季度月末上午 9 点：

```python
In [394]: prng = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV')

In [395]: ts = pd.Series(np.random.randn(len(prng)), prng)

In [396]: ts.index = (prng.asfreq('M', 'e') + 1).asfreq('H', 's') + 9

In [397]: ts.head()
Out[397]: 
1990-03-01 09:00   -0.109291
1990-06-01 09:00   -0.637235
1990-09-01 09:00   -1.735925
1990-12-01 09:00    2.096946
1991-03-01 09:00   -1.039926
Freq: H, dtype: float64
```

## 界外跨度表示

数据在 `Timestamp` 限定边界外时，参阅 [Timestamp 限制](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-timestamp-limits)，可以用 `PeriodIndex` 或 `Periods` 的 `Series` 执行计算。

```python
In [398]: span = pd.period_range('1215-01-01', '1381-01-01', freq='D')

In [399]: span
Out[399]: 
PeriodIndex(['1215-01-01', '1215-01-02', '1215-01-03', '1215-01-04',
             '1215-01-05', '1215-01-06', '1215-01-07', '1215-01-08',
             '1215-01-09', '1215-01-10',
             ...
             '1380-12-23', '1380-12-24', '1380-12-25', '1380-12-26',
             '1380-12-27', '1380-12-28', '1380-12-29', '1380-12-30',
             '1380-12-31', '1381-01-01'],
            dtype='period[D]', length=60632, freq='D')
```

从基于 `int64` 的 `YYYYMMDD` 表示形式转换。

```python
In [400]: s = pd.Series([20121231, 20141130, 99991231])

In [401]: s
Out[401]: 
0    20121231
1    20141130
2    99991231
dtype: int64

In [402]: def conv(x):
   .....:     return pd.Period(year=x // 10000, month=x // 100 % 100,
   .....:                      day=x % 100, freq='D')
   .....: 

In [403]: s.apply(conv)
Out[403]: 
0    2012-12-31
1    2014-11-30
2    9999-12-31
dtype: period[D]

In [404]: s.apply(conv)[2]
Out[404]: Period('9999-12-31', 'D')
```

轻轻松松就可以这些数据转换成 `PeriodIndex`：

```python
In [405]: span = pd.PeriodIndex(s.apply(conv))

In [406]: span
Out[406]: PeriodIndex(['2012-12-31', '2014-11-30', '9999-12-31'], dtype='period[D]', freq='D')
```

## 时区控制

利用 `pytz` 与 `datetuil` 或标准库 `datetime.timezone` 对象，Pandas 能以多种方式处理不同时区的时间戳。

### 处理时区

Pandas 对象默认不支持时区信息：

```python
In [407]: rng = pd.date_range('3/6/2012 00:00', periods=15, freq='D')

In [408]: rng.tz is None
Out[408]: True
```

用 [`date_range()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html#pandas.date_range "pandas.date_range")、[`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 、[`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 的 `tz_localize` 方法或 `tz` 关键字参数，可以为这些日期加上本地时区，即，把指定时区分配给不带时区的日期。还可以传递 `pytz` 、 `dateutil` 时区对象或奥尔森时区数据库字符串。奥尔森时区字符串默认返回 `pytz` 时区对象。要返回 `dateutil` 时区对象，在字符串前加上 `datetuil/`。

* 用 `from pytz import common_timezones, all_timezones` 在 `pytz` 里查找通用时区。

* `dateutil` 使用操作系统时区，没有固定的列表，其通用时区名与 `pytz` 相同。

```python
In [409]: import dateutil

# pytz
In [410]: rng_pytz = pd.date_range('3/6/2012 00:00', periods=3, freq='D',
   .....:                          tz='Europe/London')
   .....: 

In [411]: rng_pytz.tz
Out[411]: <DstTzInfo 'Europe/London' LMT-1 day, 23:59:00 STD>

# dateutil
In [412]: rng_dateutil = pd.date_range('3/6/2012 00:00', periods=3, freq='D')

In [413]: rng_dateutil = rng_dateutil.tz_localize('dateutil/Europe/London')

In [414]: rng_dateutil.tz
Out[414]: tzfile('/usr/share/zoneinfo/Europe/London')

# dateutil - utc special case
In [415]: rng_utc = pd.date_range('3/6/2012 00:00', periods=3, freq='D',
   .....:                         tz=dateutil.tz.tzutc())
   .....: 

In [416]: rng_utc.tz
Out[416]: tzutc()
```

*0.25.0 版新增。*

```python
# datetime.timezone
In [417]: rng_utc = pd.date_range('3/6/2012 00:00', periods=3, freq='D',
   .....:                         tz=datetime.timezone.utc)
   .....: 

In [418]: rng_utc.tz
Out[418]: datetime.timezone.utc
```

注意， `dateutil` 的 `UTC` 时区是个特例，要显式地创建 `dateutil.tz.tzutc` 实例。可以先创建其它时区对象。

```python
In [419]: import pytz

# pytz
In [420]: tz_pytz = pytz.timezone('Europe/London')

In [421]: rng_pytz = pd.date_range('3/6/2012 00:00', periods=3, freq='D')

In [422]: rng_pytz = rng_pytz.tz_localize(tz_pytz)

In [423]: rng_pytz.tz == tz_pytz
Out[423]: True

# dateutil
In [424]: tz_dateutil = dateutil.tz.gettz('Europe/London')

In [425]: rng_dateutil = pd.date_range('3/6/2012 00:00', periods=3, freq='D',
   .....:                              tz=tz_dateutil)
   .....: 

In [426]: rng_dateutil.tz == tz_dateutil
Out[426]: True
```

不同时区之间转换带时区的 Pandas 对象时，用 `tz_convert` 方法。

```python
In [427]: rng_pytz.tz_convert('US/Eastern')
Out[427]: 
DatetimeIndex(['2012-03-05 19:00:00-05:00', '2012-03-06 19:00:00-05:00',
               '2012-03-07 19:00:00-05:00'],
              dtype='datetime64[ns, US/Eastern]', freq='D')
```

::: tip 注意

使用 `pytz` 时区时，对于相同的输入时区，[`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 会构建一个与 [`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp")  不同的时区对象。[`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 具有一组 [`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 对象，UTC 偏移量也不同，不能用一个 `pytz` 时区实例简洁地表示，[`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 则可以用来指定 UTC 偏移量表示一个时点。

```python
In [428]: dti = pd.date_range('2019-01-01', periods=3, freq='D', tz='US/Pacific')

In [429]: dti.tz
Out[429]: <DstTzInfo 'US/Pacific' LMT-1 day, 16:07:00 STD>

In [430]: ts = pd.Timestamp('2019-01-01', tz='US/Pacific')

In [431]: ts.tz
Out[431]: <DstTzInfo 'US/Pacific' PST-1 day, 16:00:00 STD>
```

:::

::: danger 警告

注意不同支持库之间的转换。一些时区，`pytz` 与 `datetuil` 对时区的定义不一样。与 `US/Eastern` 等“标准”时区相比，那些更少见的时区的问题更严重。

:::

::: danger 警告

注意不同版本时区支持库对时区的定义并不一致。在处理本地存储数据时使用一种版本的支持库，在运算时使用另一种版本的支持库，可能会引起问题。参阅[本文](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-hdf5-notes)了解如何处理这种问题。

:::

::: danger 警告

对于 `pytz` 时区，直接把时区对象传递给 `datetime.datetime` 构建器是不对的，如，`datetime.datetime(2011, 1, 1, tz=pytz.timezone('US/Eastern'))`。反之，datetime 要在 `pytz` 时区对象上使用 `localize` 方法。

:::

在后台，所有 Timestamp 都存储为 UTC。含时区信息的 [`DatetimeIndex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html#pandas.DatetimeIndex "pandas.DatetimeIndex") 或 [`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 的值有其自己的本地化时区字段（日、小时、分钟等）。不过，对于不同时区时间戳，如果其 UTC 值相同，将被视作是相等的时间。

```python
In [432]: rng_eastern = rng_utc.tz_convert('US/Eastern')

In [433]: rng_berlin = rng_utc.tz_convert('Europe/Berlin')

In [434]: rng_eastern[2]
Out[434]: Timestamp('2012-03-07 19:00:00-0500', tz='US/Eastern', freq='D')

In [435]: rng_berlin[2]
Out[435]: Timestamp('2012-03-08 01:00:00+0100', tz='Europe/Berlin', freq='D')

In [436]: rng_eastern[2] == rng_berlin[2]
Out[436]: True
```

不同时区 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 之间的操作生成的是与 UTC 时间戳数据对齐的 UTC [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series")。

```python
In [437]: ts_utc = pd.Series(range(3), pd.date_range('20130101', periods=3, tz='UTC'))

In [438]: eastern = ts_utc.tz_convert('US/Eastern')

In [439]: berlin = ts_utc.tz_convert('Europe/Berlin')

In [440]: result = eastern + berlin

In [441]: result
Out[441]: 
2013-01-01 00:00:00+00:00    0
2013-01-02 00:00:00+00:00    2
2013-01-03 00:00:00+00:00    4
Freq: D, dtype: int64

In [442]: result.index
Out[442]: 
DatetimeIndex(['2013-01-01 00:00:00+00:00', '2013-01-02 00:00:00+00:00',
               '2013-01-03 00:00:00+00:00'],
              dtype='datetime64[ns, UTC]', freq='D')
```

用 `tz_localize(None)` 或 `tz_convert(None)` 去掉时区信息。`tz_localize(None)` 去掉带本地时间表示的时区信息。`tz_convert(None)`先把时间戳转为 UTC 时间，再去掉时区信息。

```python
In [443]: didx = pd.date_range(start='2014-08-01 09:00', freq='H',
   .....:                      periods=3, tz='US/Eastern')
   .....: 

In [444]: didx
Out[444]: 
DatetimeIndex(['2014-08-01 09:00:00-04:00', '2014-08-01 10:00:00-04:00',
               '2014-08-01 11:00:00-04:00'],
              dtype='datetime64[ns, US/Eastern]', freq='H')

In [445]: didx.tz_localize(None)
Out[445]: 
DatetimeIndex(['2014-08-01 09:00:00', '2014-08-01 10:00:00',
               '2014-08-01 11:00:00'],
              dtype='datetime64[ns]', freq='H')

In [446]: didx.tz_convert(None)
Out[446]: 
DatetimeIndex(['2014-08-01 13:00:00', '2014-08-01 14:00:00',
               '2014-08-01 15:00:00'],
              dtype='datetime64[ns]', freq='H')

# tz_convert(None) 等同于 tz_convert('UTC').tz_localize(None)
In [447]: didx.tz_convert('UTC').tz_localize(None)
Out[447]: 
DatetimeIndex(['2014-08-01 13:00:00', '2014-08-01 14:00:00',
               '2014-08-01 15:00:00'],
              dtype='datetime64[ns]', freq='H')
```

### 本地化导致的混淆时间

`tz_localize` 不能决定时间戳的 UTC偏移量，因为本地时区的夏时制（DST）会引起一些时间在一天内出现两次的问题（“时钟回调”）。下面的选项是有效的：

* `raise`：默认触发 `pytz.AmbiguousTimeError`
* `infer`：依据时间戳的单一性，尝试推断正确的偏移量
* `NaT`：用 `NaT` 替换混淆时间
* `bool`：`True` 代表夏时制（DST）时间，`False` 代表正常时间。数组型的 `bool` 值支持一组时间序列。

```python
In [448]: rng_hourly = pd.DatetimeIndex(['11/06/2011 00:00', '11/06/2011 01:00',
   .....:                                '11/06/2011 01:00', '11/06/2011 02:00'])
   .....: 
```

这种操作会引起混淆时间失败错误（ '11/06/2011 01:00'）。

```python
In [2]: rng_hourly.tz_localize('US/Eastern')
AmbiguousTimeError: Cannot infer dst time from Timestamp('2011-11-06 01:00:00'), try using the 'ambiguous' argument
```

用下列指定的关键字控制混淆时间。

```python
In [449]: rng_hourly.tz_localize('US/Eastern', ambiguous='infer')
Out[449]: 
DatetimeIndex(['2011-11-06 00:00:00-04:00', '2011-11-06 01:00:00-04:00',
               '2011-11-06 01:00:00-05:00', '2011-11-06 02:00:00-05:00'],
              dtype='datetime64[ns, US/Eastern]', freq=None)

In [450]: rng_hourly.tz_localize('US/Eastern', ambiguous='NaT')
Out[450]: 
DatetimeIndex(['2011-11-06 00:00:00-04:00', 'NaT', 'NaT',
               '2011-11-06 02:00:00-05:00'],
              dtype='datetime64[ns, US/Eastern]', freq=None)

In [451]: rng_hourly.tz_localize('US/Eastern', ambiguous=[True, True, False, False])
Out[451]: 
DatetimeIndex(['2011-11-06 00:00:00-04:00', '2011-11-06 01:00:00-04:00',
               '2011-11-06 01:00:00-05:00', '2011-11-06 02:00:00-05:00'],
              dtype='datetime64[ns, US/Eastern]', freq=None)
```

### 本地化时不存在的时间

夏时制转换会移位本地时间一个小时，这样会创建一个不存在的本地时间（“时钟春季前滚”）。这种本地化操作会导致时间序列出现不存在的时间，此问题可以用 `nonexistent` 参数解决。下列都是有效的选项：

* `raise`：默认触发 `pytz.NonExistentTimeError`
* `NaT`：用 `NaT` 替换不存在的时间
* `shift_forward`：把不存在的时间前移至最近的真实时间
* `shift_backward`：把不存在的时间后滚至最近的真实时间
* `Timedelta` 对象：用 `timedelta` 移位不存在的时间

```python
In [452]: dti = pd.date_range(start='2015-03-29 02:30:00', periods=3, freq='H')

# 2:30 是不存在的时间
```

对不存在的时间进行本地化操作默认会触发错误。

```python
In [2]: dti.tz_localize('Europe/Warsaw')
NonExistentTimeError: 2015-03-29 02:30:00
```

把不存在的时间转换为 `NaT` 或移位时间

```python
In [453]: dti
Out[453]: 
DatetimeIndex(['2015-03-29 02:30:00', '2015-03-29 03:30:00',
               '2015-03-29 04:30:00'],
              dtype='datetime64[ns]', freq='H')

In [454]: dti.tz_localize('Europe/Warsaw', nonexistent='shift_forward')
Out[454]: 
DatetimeIndex(['2015-03-29 03:00:00+02:00', '2015-03-29 03:30:00+02:00',
               '2015-03-29 04:30:00+02:00'],
              dtype='datetime64[ns, Europe/Warsaw]', freq='H')

In [455]: dti.tz_localize('Europe/Warsaw', nonexistent='shift_backward')
Out[455]: 
DatetimeIndex(['2015-03-29 01:59:59.999999999+01:00',
                         '2015-03-29 03:30:00+02:00',
                         '2015-03-29 04:30:00+02:00'],
              dtype='datetime64[ns, Europe/Warsaw]', freq='H')

In [456]: dti.tz_localize('Europe/Warsaw', nonexistent=pd.Timedelta(1, unit='H'))
Out[456]: 
DatetimeIndex(['2015-03-29 03:30:00+02:00', '2015-03-29 03:30:00+02:00',
               '2015-03-29 04:30:00+02:00'],
              dtype='datetime64[ns, Europe/Warsaw]', freq='H')

In [457]: dti.tz_localize('Europe/Warsaw', nonexistent='NaT')
Out[457]: 
DatetimeIndex(['NaT', '2015-03-29 03:30:00+02:00',
               '2015-03-29 04:30:00+02:00'],
              dtype='datetime64[ns, Europe/Warsaw]', freq='H')
```

### 时区序列操作

无时区 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series")  值的数据类型是 datetime64[ns]。

```python
In [458]: s_naive = pd.Series(pd.date_range('20130101', periods=3))

In [459]: s_naive
Out[459]: 
0   2013-01-01
1   2013-01-02
2   2013-01-03
dtype: datetime64[ns]
```

有时区 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 值的数据类型是 datetime64[ns, tz]，`tz` 指的是时区。

```python
In [460]: s_aware = pd.Series(pd.date_range('20130101', periods=3, tz='US/Eastern'))

In [461]: s_aware
Out[461]: 
0   2013-01-01 00:00:00-05:00
1   2013-01-02 00:00:00-05:00
2   2013-01-03 00:00:00-05:00
dtype: datetime64[ns, US/Eastern]
```

这两种 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series") 的时区信息都可以用 `.dt` 访问器操控，参阅 [dt 访问器](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dt-accessors)。

例如，本地化与把无时区时间戳转换为有时区时间戳。

```python
In [462]: s_naive.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
Out[462]: 
0   2012-12-31 19:00:00-05:00
1   2013-01-01 19:00:00-05:00
2   2013-01-02 19:00:00-05:00
dtype: datetime64[ns, US/Eastern]
```

时区信息还可以用 `astype` 操控。这种方法可以本地化并转换无时区时间戳或转换有时区时间戳。

```python
# 本地化，并把无时区转换为有时区
In [463]: s_naive.astype('datetime64[ns, US/Eastern]')
Out[463]: 
0   2012-12-31 19:00:00-05:00
1   2013-01-01 19:00:00-05:00
2   2013-01-02 19:00:00-05:00
dtype: datetime64[ns, US/Eastern]

# 把有时区变为无时区
In [464]: s_aware.astype('datetime64[ns]')
Out[464]: 
0   2013-01-01 05:00:00
1   2013-01-02 05:00:00
2   2013-01-03 05:00:00
dtype: datetime64[ns]

# 转换为新的时区
In [465]: s_aware.astype('datetime64[ns, CET]')
Out[465]: 
0   2013-01-01 06:00:00+01:00
1   2013-01-02 06:00:00+01:00
2   2013-01-03 06:00:00+01:00
dtype: datetime64[ns, CET]
```

::: tip 注意

在 `Series` 上应用 [`Series.to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_numpy.html#pandas.Series.to_numpy "pandas.Series.to_numpy")，返回数据的 NumPy 数组。虽然 NumPy 可以**输出**本地时区！但其实它当前并不支持时区，因此，有时区时间戳数据返回的是时间戳对象数组：

```python
In [466]: s_naive.to_numpy()
Out[466]: 
array(['2013-01-01T00:00:00.000000000', '2013-01-02T00:00:00.000000000',
       '2013-01-03T00:00:00.000000000'], dtype='datetime64[ns]')

In [467]: s_aware.to_numpy()
Out[467]: 
array([Timestamp('2013-01-01 00:00:00-0500', tz='US/Eastern', freq='D'),
       Timestamp('2013-01-02 00:00:00-0500', tz='US/Eastern', freq='D'),
       Timestamp('2013-01-03 00:00:00-0500', tz='US/Eastern', freq='D')],
      dtype=object)
```

通过转换时间戳数组，保留时区信息。例如，转换回 `Series` 时：

```python
In [468]: pd.Series(s_aware.to_numpy())
Out[468]: 
0   2013-01-01 00:00:00-05:00
1   2013-01-02 00:00:00-05:00
2   2013-01-03 00:00:00-05:00
dtype: datetime64[ns, US/Eastern]
```

如果需要 NumPy `datetime64[ns]` 数组（带已转为 UTC 的值）而不是对象数组，可以指定 `dtype` 参数：

```python
In [469]: s_aware.to_numpy(dtype='datetime64[ns]')
Out[469]: 
array(['2013-01-01T05:00:00.000000000', '2013-01-02T05:00:00.000000000',
       '2013-01-03T05:00:00.000000000'], dtype='datetime64[ns]')
```

:::