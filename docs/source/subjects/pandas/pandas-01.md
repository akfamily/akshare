# Pandas 基础用法

本节介绍 Pandas 数据结构的基础用法。下列代码创建上一节用过的示例数据对象：

```
In [1]: index = pd.date_range('1/1/2000', periods=8)

In [2]: s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])

In [3]: df = pd.DataFrame(np.random.randn(8, 3), index=index,
   ...:                   columns=['A', 'B', 'C'])
   ...: 
```
## Head 与 Tail

[`head()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.head.html#pandas.DataFrame.head) 与 [`tail()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.tail.html#pandas.DataFrame.tail)  用于快速预览 Series 与 DataFrame，默认显示 5 条数据，也可以指定显示数据的数量。

```
In [4]: long_series = pd.Series(np.random.randn(1000))

In [5]: long_series.head()
Out[5]: 
0   -1.157892
1   -1.344312
2    0.844885
3    1.075770
4   -0.109050
dtype: float64

In [6]: long_series.tail(3)
Out[6]: 
997   -0.289388
998   -1.020544
999    0.589993
dtype: float64
```
## 属性与底层数据

Pandas 可以通过多个属性访问元数据：

- **shape**: 
    - 输出对象的轴维度，与 ndarray 一致

- **轴标签**

    - **Series**: *Index* (仅有此轴)
    - **DataFrame**: *Index* (行) 与*列*

注意： **为属性赋值是安全的**！

```
In [7]: df[:2]
Out[7]: 
                   A         B         C
2000-01-01 -0.173215  0.119209 -1.044236
2000-01-02 -0.861849 -2.104569 -0.494929

In [8]: df.columns = [x.lower() for x in df.columns]

In [9]: df
Out[9]: 
                   a         b         c
2000-01-01 -0.173215  0.119209 -1.044236
2000-01-02 -0.861849 -2.104569 -0.494929
2000-01-03  1.071804  0.721555 -0.706771
2000-01-04 -1.039575  0.271860 -0.424972
2000-01-05  0.567020  0.276232 -1.087401
2000-01-06 -0.673690  0.113648 -1.478427
2000-01-07  0.524988  0.404705  0.577046
2000-01-08 -1.715002 -1.039268 -0.370647
```

Pandas 对象（[`Index`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.html#pandas.Index "pandas.Index")， [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series")， [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame")）相当于数组的容器，用于存储数据、执行计算。大部分类型的底层数组都是 [`numpy.ndarray`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v1.16)")。不过，Pandas 与第三方支持库一般都会扩展 NumPy 类型系统，添加自定义数组（见[数据类型](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dtypes)）。

`.array` 属性用于提取  [`Index`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.html#pandas.Index "pandas.Index") 或 [`Series`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series "pandas.Series")  里的数据。

```
In [10]: s.array
Out[10]: 
<PandasArray>
[ 0.4691122999071863, -0.2828633443286633, -1.5090585031735124,
 -1.1356323710171934,  1.2121120250208506]
Length: 5, dtype: float64

In [11]: s.index.array
Out[11]: 
<PandasArray>
['a', 'b', 'c', 'd', 'e']
Length: 5, dtype: object
```
[`array`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.array.html#pandas.Series.array "pandas.Series.array") 一般指 [`ExtensionArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray "pandas.api.extensions.ExtensionArray")。至于什么是 [`ExtensionArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray "pandas.api.extensions.ExtensionArray") 及 Pandas 为什么要用 [`ExtensionArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray "pandas.api.extensions.ExtensionArray") 不是本节要说明的内容。更多信息请参阅[数据类型](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dtypes)。

提取 NumPy 数组，用 [`to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_numpy.html#pandas.Series.to_numpy "pandas.Series.to_numpy") 或 `numpy.asarray()`。

```
In [12]: s.to_numpy()
Out[12]: array([ 0.4691, -0.2829, -1.5091, -1.1356,  1.2121])

In [13]: np.asarray(s)
Out[13]: array([ 0.4691, -0.2829, -1.5091, -1.1356,  1.2121])
```

`Series` 与 `Index` 的类型是 [`ExtensionArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray "pandas.api.extensions.ExtensionArray") 时， [`to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_numpy.html#pandas.Series.to_numpy "pandas.Series.to_numpy") 会复制数据，并强制转换值。详情见[数据类型](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dtypes)。

[`to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_numpy.html#pandas.Series.to_numpy "pandas.Series.to_numpy") 可以控制 [`numpy.ndarray`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v1.16)") 生成的数据类型。以带时区的 datetime 为例，NumPy 未提供时区信息的 datetime 数据类型，Pandas 则提供了两种表现形式：

1. 一种是带 [`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp "pandas.Timestamp") 的 [`numpy.ndarray`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v1.16)")，提供了正确的 `tz` 信息。

2. 另一种是 `datetime64[ns]`，这也是一种 [`numpy.ndarray`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v1.16)")，值被转换为 UTC，但去掉了时区信息。

时区信息可以用 `dtype=object` 保存。

```
In [14]: ser = pd.Series(pd.date_range('2000', periods=2, tz="CET"))

In [15]: ser.to_numpy(dtype=object)
Out[15]: 
array([Timestamp('2000-01-01 00:00:00+0100', tz='CET', freq='D'),
       Timestamp('2000-01-02 00:00:00+0100', tz='CET', freq='D')],
      dtype=object)
```
或用 `dtype='datetime64[ns]'` 去除。

```
In [16]: ser.to_numpy(dtype="datetime64[ns]")
Out[16]: 
array(['1999-12-31T23:00:00.000000000', '2000-01-01T23:00:00.000000000'],
      dtype='datetime64[ns]')
```

提取 `DataFrame` 里的**原数据**稍微有点复杂。DataFrame 里所有列的数据类型都一样时，[`DataFrame.to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_numpy.html#pandas.DataFrame.to_numpy "pandas.DataFrame.to_numpy") 返回底层数据：

```
In [17]: df.to_numpy()
Out[17]: 
array([[-0.1732,  0.1192, -1.0442],
       [-0.8618, -2.1046, -0.4949],
       [ 1.0718,  0.7216, -0.7068],
       [-1.0396,  0.2719, -0.425 ],
       [ 0.567 ,  0.2762, -1.0874],
       [-0.6737,  0.1136, -1.4784],
       [ 0.525 ,  0.4047,  0.577 ],
       [-1.715 , -1.0393, -0.3706]])
```
DataFrame 为同构型数据时，Pandas 直接修改原始 `ndarray`，所做修改会直接反应在数据结构里。对于异质型数据，即 DataFrame 列的数据类型不一样时，就不是这种操作模式了。与轴标签不同，不能为值的属性赋值。

::: tip 注意

处理异质型数据时，输出结果 `ndarray` 的数据类型适用于涉及的各类数据。若 DataFrame 里包含字符串，输出结果的数据类型就是 `object`。要是只有浮点数或整数，则输出结果的数据类型是浮点数。

:::

以前，Pandas 推荐用 [`Series.values`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.values.html#pandas.Series.values "pandas.Series.values") 或 [`DataFrame.values`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.values.html#pandas.DataFrame.values "pandas.DataFrame.values") 从 Series 或 DataFrame 里提取数据。旧有代码库或在线教程里仍在用这种操作，但 Pandas 已改进了此功能，现在，推荐用 `.array` 或 `to_numpy` 提取数据，别再用 `.values` 了。`.values` 有以下几个缺点：

1. Series 含[扩展类型](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-extension-types)时，[Series.values](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.values.html#pandas.Series.values) 无法判断到底是该返回 NumPy `array`，还是返回 `ExtensionArray`。而 [`Series.array`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.array.html#pandas.Series.array "pandas.Series.array") 则只返回 [`ExtensionArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray "pandas.api.extensions.ExtensionArray")，且不会复制数据。[`Series.to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_numpy.html#pandas.Series.to_numpy "pandas.Series.to_numpy") 则返回 NumPy 数组，其代价是需要复制、并强制转换数据的值。

2. DataFrame 含多种数据类型时，[`DataFrame.values`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.values.html#pandas.DataFrame.values "pandas.DataFrame.values") 会复制数据，并将数据的值强制转换同一种数据类型，这是一种代价较高的操作。[`DataFrame.to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_numpy.html#pandas.DataFrame.to_numpy "pandas.DataFrame.to_numpy") 则返回 NumPy 数组，这种方式更清晰，也不会把 DataFrame 里的数据都当作一种类型。

## 加速操作

借助 `numexpr` 与 `bottleneck` 支持库，Pandas 可以加速特定类型的二进制数值与布尔操作。

处理大型数据集时，这两个支持库特别有用，加速效果也非常明显。 `numexpr` 使用智能分块、缓存与多核技术。`bottleneck` 是一组专属 cython 例程，处理含 `nans` 值的数组时，特别快。

请看下面这个例子（`DataFrame` 包含 100 列 X 10 万行数据）:

|    操作     | 0.11.0版 (ms) | 旧版 (ms) | 提升比率 |
| :---------: | :-----------: | :-------: | :------: |
| `df1 > df2` |     13.32     |  125.35   |  0.1063  |
| `df1 * df2` |     21.71     |   36.63   |  0.5928  |
| `df1 + df2` |     22.04     |   36.50   |  0.6039  |

强烈建议安装这两个支持库，更多信息，请参阅[推荐支持库](https://pandas.pydata.org/pandas-docs/stable/install.html#install-recommended-dependencies)。

这两个支持库默认为启用状态，可用以下选项设置：

*0.20.0 版新增。*

```
pd.set_option('compute.use_bottleneck', False)
pd.set_option('compute.use_numexpr', False)
```

## 二进制操作

Pandas 数据结构之间执行二进制操作，要注意下列两个关键点：

* 多维（DataFrame）与低维（Series）对象之间的广播机制；
* 计算中的缺失值处理。

这两个问题可以同时处理，但下面先介绍怎么分开处理。

### 匹配/广播机制

DataFrame 支持 [`add()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.add.html#pandas.DataFrame.add "pandas.DataFrame.add")、[`sub()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sub.html#pandas.DataFrame.sub "pandas.DataFrame.sub")、[`mul()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mul.html#pandas.DataFrame.mul "pandas.DataFrame.mul")、[`div()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.div.html#pandas.DataFrame.div "pandas.DataFrame.div") 及 [`radd()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.radd.html#pandas.DataFrame.radd "pandas.DataFrame.radd")、[`rsub()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rsub.html#pandas.DataFrame.rsub "pandas.DataFrame.rsub") 等方法执行二进制操作。广播机制重点关注输入的 Series。通过 `axis` 关键字，匹配 *index* 或 *columns* 即可调用这些函数。

```
In [18]: df = pd.DataFrame({
   ....:     'one': pd.Series(np.random.randn(3), index=['a', 'b', 'c']),
   ....:     'two': pd.Series(np.random.randn(4), index=['a', 'b', 'c', 'd']),
   ....:     'three': pd.Series(np.random.randn(3), index=['b', 'c', 'd'])})
   ....: 

In [19]: df
Out[19]: 
        one       two     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [20]: row = df.iloc[1]

In [21]: column = df['two']

In [22]: df.sub(row, axis='columns')
Out[22]: 
        one       two     three
a  1.051928 -0.139606       NaN
b  0.000000  0.000000  0.000000
c  0.352192 -0.433754  1.277825
d       NaN -1.632779 -0.562782

In [23]: df.sub(row, axis=1)
Out[23]: 
        one       two     three
a  1.051928 -0.139606       NaN
b  0.000000  0.000000  0.000000
c  0.352192 -0.433754  1.277825
d       NaN -1.632779 -0.562782

In [24]: df.sub(column, axis='index')
Out[24]: 
        one  two     three
a -0.377535  0.0       NaN
b -1.569069  0.0 -1.962513
c -0.783123  0.0 -0.250933
d       NaN  0.0 -0.892516

In [25]: df.sub(column, axis=0)
Out[25]: 
        one  two     three
a -0.377535  0.0       NaN
b -1.569069  0.0 -1.962513
c -0.783123  0.0 -0.250933
d       NaN  0.0 -0.892516
```
还可以用 Series 对齐多层索引 DataFrame 的某一层级。

```
In [26]: dfmi = df.copy()

In [27]: dfmi.index = pd.MultiIndex.from_tuples([(1, 'a'), (1, 'b'),
   ....:                                         (1, 'c'), (2, 'a')],
   ....:                                        names=['first', 'second'])
   ....: 

In [28]: dfmi.sub(column, axis=0, level='second')
Out[28]: 
                   one       two     three
first second                              
1     a      -0.377535  0.000000       NaN
      b      -1.569069  0.000000 -1.962513
      c      -0.783123  0.000000 -0.250933
2     a            NaN -1.493173 -2.385688
```

Series 与 Index 还支持 [`divmod()`](https://docs.python.org/3/library/functions.html#divmod "(in Python v3.7)") 内置函数，该函数同时执行向下取整除与模运算，返回两个与左侧类型相同的元组。示例如下：

```
In [29]: s = pd.Series(np.arange(10))

In [30]: s
Out[30]: 
0    0
1    1
2    2
3    3
4    4
5    5
6    6
7    7
8    8
9    9
dtype: int64

In [31]: div, rem = divmod(s, 3)

In [32]: div
Out[32]: 
0    0
1    0
2    0
3    1
4    1
5    1
6    2
7    2
8    2
9    3
dtype: int64

In [33]: rem
Out[33]: 
0    0
1    1
2    2
3    0
4    1
5    2
6    0
7    1
8    2
9    0
dtype: int64

In [34]: idx = pd.Index(np.arange(10))

In [35]: idx
Out[35]: Int64Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype='int64')

In [36]: div, rem = divmod(idx, 3)

In [37]: div
Out[37]: Int64Index([0, 0, 0, 1, 1, 1, 2, 2, 2, 3], dtype='int64')

In [38]: rem
Out[38]: Int64Index([0, 1, 2, 0, 1, 2, 0, 1, 2, 0], dtype='int64')
```
[`divmod()`](https://docs.python.org/3/library/functions.html#divmod "(in Python v3.7)") 还支持元素级运算：

```
In [39]: div, rem = divmod(s, [2, 2, 3, 3, 4, 4, 5, 5, 6, 6])

In [40]: div
Out[40]: 
0    0
1    0
2    0
3    1
4    1
5    1
6    1
7    1
8    1
9    1
dtype: int64

In [41]: rem
Out[41]: 
0    0
1    1
2    2
3    0
4    0
5    1
6    1
7    2
8    2
9    3
dtype: int64
```

### 缺失值与填充缺失值操作

Series 与 DataFrame 的算数函数支持 `fill_value` 选项，即用指定值替换某个位置的缺失值。比如，两个 DataFrame 相加，除非两个 DataFrame 里同一个位置都有缺失值，其相加的和仍为 `NaN`，如果只有一个 DataFrame 里存在缺失值，则可以用 `fill_value` 指定一个值来替代 `NaN`，当然，也可以用 `fillna` 把 `NaN` 替换为想要的值。

::: tip 注意

下面第 43 条代码里，Pandas 官档没有写 df2 是哪里来的，这里补上，与 df 类似。 ```
df2 = pd.DataFrame({
   ....:     'one': pd.Series(np.random.randn(3), index=['a', 'b', 'c']),
   ....:     'two': pd.Series(np.random.randn(4), index=['a', 'b', 'c', 'd']),
   ....:     'three': pd.Series(np.random.randn(3), index=['a', 'b', 'c', 'd'])})
   ....:
```
:::

​```
In [42]: df
Out[42]: 
        one       two     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [43]: df2
Out[43]: 
        one       two     three
a  1.394981  1.772517  1.000000
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [44]: df + df2
Out[44]: 
        one       two     three
a  2.789963  3.545034       NaN
b  0.686107  3.824246 -0.100780
c  1.390491  2.956737  2.454870
d       NaN  0.558688 -1.226343

In [45]: df.add(df2, fill_value=0)
Out[45]: 
        one       two     three
a  2.789963  3.545034  1.000000
b  0.686107  3.824246 -0.100780
c  1.390491  2.956737  2.454870
d       NaN  0.558688 -1.226343
```

### 比较操作

与上一小节的算数运算类似，Series 与 DataFrame 还支持 `eq`、`ne`、`lt`、`gt`、`le`、`ge` 等二进制比较操作的方法：

| 序号 | 缩写 |           英文           |   中文   |
| :--: | :--: | :----------------------: | :------: |
|  1   |  eq  |         equal to         |   等于   |
|  2   |  ne  |       not equal to       |  不等于  |
|  3   |  lt  |        less than         |   小于   |
|  4   |  gt  |       greater than       |   大于   |
|  5   |  le  |  less than or equal to   | 小于等于 |
|  6   |  ge  | greater than or equal to | 大于等于 |

```
In [46]: df.gt(df2)
Out[46]: 
     one    two  three
a  False  False  False
b  False  False  False
c  False  False  False
d  False  False  False

In [47]: df2.ne(df)
Out[47]: 
     one    two  three
a  False  False   True
b  False  False  False
c  False  False  False
d   True  False  False
```

这些操作生成一个与左侧输入对象类型相同的 Pandas 对象，即，dtype 为 `bool`。`boolean` 对象可用于索引操作，参阅[布尔索引](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-boolean)。

### 布尔简化

[`empty`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.empty.html#pandas.DataFrame.empty "pandas.DataFrame.empty")、[`any()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.any.html#pandas.DataFrame.any "pandas.DataFrame.any")、[`all()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.all.html#pandas.DataFrame.all "pandas.DataFrame.all")、[`bool()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.bool.html#pandas.DataFrame.bool "pandas.DataFrame.bool") 可以把数据汇总简化至单个布尔值。

```
In [48]: (df > 0).all()
Out[48]: 
one      False
two       True
three    False
dtype: bool

In [49]: (df > 0).any()
Out[49]: 
one      True
two      True
three    True
dtype: bool
```

还可以进一步把上面的结果简化为单个布尔值。

```
In [50]: (df > 0).any().any()
Out[50]: True
```

通过 [`empty`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.empty.html#pandas.DataFrame.empty "pandas.DataFrame.empty") 属性，可以验证 Pandas 对象是否为**空**。

```
In [51]: df.empty
Out[51]: False

In [52]: pd.DataFrame(columns=list('ABC')).empty
Out[52]: True
```

用 [`bool()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.bool.html#pandas.DataFrame.bool "pandas.DataFrame.bool") 方法验证单元素 pandas 对象的布尔值。

```
In [53]: pd.Series([True]).bool()
Out[53]: True

In [54]: pd.Series([False]).bool()
Out[54]: False

In [55]: pd.DataFrame([[True]]).bool()
Out[55]: True

In [56]: pd.DataFrame([[False]]).bool()
Out[56]: False
```
::: danger 警告

以下代码：
```
>>> if df:
...     pass
```

或

```
>>> df and df2
```

上述代码试图比对多个值，因此，这两种操作都会触发错误：

```
ValueError: The truth value of an array is ambiguous. Use a.empty, a.any() or a.all().
```

:::

了解详情，请参阅[各种坑](https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#gotchas-truth)小节的内容。

### 比较对象是否等效

一般情况下，多种方式都能得出相同的结果。以 `df + df` 与 `df * 2` 为例。应用上一小节学到的知识，测试这两种计算方式的结果是否一致，一般人都会用 `(df + df == df * 2).all()`，不过，这个表达式的结果是 `False`：

```
In [57]: df + df == df * 2
Out[57]: 
     one   two  three
a   True  True  False
b   True  True   True
c   True  True   True
d  False  True   True

In [58]: (df + df == df * 2).all()
Out[58]: 
one      False
two       True
three    False
dtype: bool
```

注意：布尔型 DataFrame `df + df == df * 2` 中有 `False` 值！这是因为两个 `NaN` 值的比较结果为**不等**：

```
In [59]: np.nan == np.nan
Out[59]: False
```

为了验证数据是否等效，Series 与 DataFrame 等 N 维框架提供了 [`equals()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.equals.html#pandas.DataFrame.equals "pandas.DataFrame.equals") 方法，用这个方法验证 `NaN` 值的结果为**相等**。

```
In [60]: (df + df).equals(df * 2)
Out[60]: True
```

注意：Series 与 DataFrame 索引的顺序必须一致，验证结果才能为 `True`：

```
In [61]: df1 = pd.DataFrame({'col': ['foo', 0, np.nan]})

In [62]: df2 = pd.DataFrame({'col': [np.nan, 0, 'foo']}, index=[2, 1, 0])

In [63]: df1.equals(df2)
Out[63]: False

In [64]: df1.equals(df2.sort_index())
Out[64]: True
```

### 比较 array 型对象

用标量值与 Pandas 数据结构对比数据元素非常简单：

```
In [65]: pd.Series(['foo', 'bar', 'baz']) == 'foo'
Out[65]: 
0     True
1    False
2    False
dtype: bool

In [66]: pd.Index(['foo', 'bar', 'baz']) == 'foo'
Out[66]: array([ True, False, False])
```

Pandas 还能对比两个等长 `array` 对象里的数据元素：

```
In [67]: pd.Series(['foo', 'bar', 'baz']) == pd.Index(['foo', 'bar', 'qux'])
Out[67]: 
0     True
1     True
2    False
dtype: bool

In [68]: pd.Series(['foo', 'bar', 'baz']) == np.array(['foo', 'bar', 'qux'])
Out[68]: 
0     True
1     True
2    False
dtype: bool
```

对比不等长的 `Index` 或 `Series` 对象会触发 `ValueError`：

```
In [55]: pd.Series(['foo', 'bar', 'baz']) == pd.Series(['foo', 'bar'])
ValueError: Series lengths must match to compare

In [56]: pd.Series(['foo', 'bar', 'baz']) == pd.Series(['foo'])
ValueError: Series lengths must match to compare
```

注意： 这里的操作与 NumPy 的广播机制不同：

```
In [69]: np.array([1, 2, 3]) == np.array([2])
Out[69]: array([False,  True, False])
```

NumPy 无法执行广播操作时，返回 `False`:

```
In [70]: np.array([1, 2, 3]) == np.array([1, 2])
Out[70]: False
```

### 合并重叠数据集

有时，要合并两个相似的数据集，两个数据集里的其中一个的数据比另一个多。比如，展示特定经济指标的两个数据序列，其中一个是“高质量”指标，另一个是“低质量”指标。一般来说，低质量序列可能包含更多的历史数据，或覆盖更广的数据。因此，要合并这两个 DataFrame 对象，其中一个 DataFrame 中的缺失值将按指定条件用另一个 DataFrame 里类似标签中的数据进行填充。要实现这一操作，请用下列代码中的 [`combine_first()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.combine_first.html#pandas.DataFrame.combine_first "pandas.DataFrame.combine_first") 函数。

```
In [71]: df1 = pd.DataFrame({'A': [1., np.nan, 3., 5., np.nan],
   ....:                     'B': [np.nan, 2., 3., np.nan, 6.]})
   ....: 

In [72]: df2 = pd.DataFrame({'A': [5., 2., 4., np.nan, 3., 7.],
   ....:                     'B': [np.nan, np.nan, 3., 4., 6., 8.]})
   ....: 

In [73]: df1
Out[73]: 
     A    B
0  1.0  NaN
1  NaN  2.0
2  3.0  3.0
3  5.0  NaN
4  NaN  6.0

In [74]: df2
Out[74]: 
     A    B
0  5.0  NaN
1  2.0  NaN
2  4.0  3.0
3  NaN  4.0
4  3.0  6.0
5  7.0  8.0

In [75]: df1.combine_first(df2)
Out[75]: 
     A    B
0  1.0  NaN
1  2.0  2.0
2  3.0  3.0
3  5.0  4.0
4  3.0  6.0
5  7.0  8.0
```

### DataFrame 通用合并方法

上述 [`combine_first()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.combine_first.html#pandas.DataFrame.combine_first "pandas.DataFrame.combine_first") 方法调用了更普适的 [`DataFrame.combine()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.combine.html#pandas.DataFrame.combine "pandas.DataFrame.combine") 方法。该方法提取另一个 DataFrame 及合并器函数，并将之与输入的 DataFrame 对齐，再传递与 Series 配对的合并器函数（比如，名称相同的列）。

下面的代码复现了上述的 [`combine_first()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.combine_first.html#pandas.DataFrame.combine_first "pandas.DataFrame.combine_first") 函数：

```
In [76]: def combiner(x, y):
   ....:     return np.where(pd.isna(x), y, x)
   ....: 
```

## 描述性统计

[Series](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#api-series-stats) 与 [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#api-dataframe-stats) 支持大量计算描述性统计的方法与操作。这些方法大部分都是  [`sum()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html#pandas.DataFrame.sum "pandas.DataFrame.sum")、[`mean()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mean.html#pandas.DataFrame.mean "pandas.DataFrame.mean")、[`quantile()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.quantile.html#pandas.DataFrame.quantile "pandas.DataFrame.quantile") 等聚合函数，其输出结果比原始数据集小；此外，还有输出结果与原始数据集同样大小的 [`cumsum()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cumsum.html#pandas.DataFrame.cumsum "pandas.DataFrame.cumsum") 、 [`cumprod()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cumprod.html#pandas.DataFrame.cumprod "pandas.DataFrame.cumprod") 等函数。这些方法都基本上都接受 `axis` 参数，如， `ndarray.{sum,std,…}`，但这里的 `axis` 可以用名称或整数指定：

* **Series**：无需 `axis` 参数
* **DataFrame**：
  * `index`，即 `axis=0`，默认值
  * `columns`, 即 `axis=1`

示例如下：

```
In [77]: df
Out[77]: 
        one       two     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [78]: df.mean(0)
Out[78]: 
one      0.811094
two      1.360588
three    0.187958
dtype: float64

In [79]: df.mean(1)
Out[79]: 
a    1.583749
b    0.734929
c    1.133683
d   -0.166914
dtype: float64
```

上述方法都支持 `skipna` 关键字，指定是否要排除缺失数据，默认值为 `True`。

```
In [80]: df.sum(0, skipna=False)
Out[80]: 
one           NaN
two      5.442353
three         NaN
dtype: float64

In [81]: df.sum(axis=1, skipna=True)
Out[81]: 
a    3.167498
b    2.204786
c    3.401050
d   -0.333828
dtype: float64
```

结合广播机制或算数操作，可以描述不同统计过程，比如标准化，即渲染数据零均值与标准差 1，这种操作非常简单：

```
In [82]: ts_stand = (df - df.mean()) / df.std()

In [83]: ts_stand.std()
Out[83]: 
one      1.0
two      1.0
three    1.0
dtype: float64

In [84]: xs_stand = df.sub(df.mean(1), axis=0).div(df.std(1), axis=0)

In [85]: xs_stand.std(1)
Out[85]: 
a    1.0
b    1.0
c    1.0
d    1.0
dtype: float64
```

注 ： [`cumsum()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cumsum.html#pandas.DataFrame.cumsum) 与 [`cumprod()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cumprod.html#pandas.DataFrame.cumprod) 等方法保留 `NaN`  值的位置。这与 [`expanding()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.expanding.html#pandas.DataFrame.expanding) 和 [`rolling()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html#pandas.DataFrame.rolling) 略显不同，详情请参阅[本文](https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#stats-moments-expanding-note)。

```
In [86]: df.cumsum()
Out[86]: 
        one       two     three
a  1.394981  1.772517       NaN
b  1.738035  3.684640 -0.050390
c  2.433281  5.163008  1.177045
d       NaN  5.442353  0.563873
```

下表为常用函数汇总表。每个函数都支持 `level` 参数，仅在数据对象为[结构化 Index](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-hierarchical) 时使用。

|    函数    |           描述           |
| :--------: | :----------------------: |
|  `count`   |      统计非空值数量      |
|   `sum`    |          汇总值          |
|   `mean`   |          平均值          |
|   `mad`    |       平均绝对偏差       |
|  `median`  |        算数中位数        |
|   `min`    |          最小值          |
|   `max`    |          最大值          |
|   `mode`   |           众数           |
|   `abs`    |          绝对值          |
|   `prod`   |           乘积           |
|   `std`    | 贝塞尔校正的样本标准偏差 |
|   `var`    |         无偏方差         |
|   `sem`    |     平均值的标准误差     |
|   `skew`   |    样本偏度 (第三阶)     |
|   `kurt`   |    样本峰度 (第四阶)     |
| `quantile` | 样本分位数 (不同 % 的值) |
|  `cumsum`  |           累加           |
| `cumprod`  |           累乘           |
|  `cummax`  |        累积最大值        |
|  `cummin`  |        累积最小值        |

注意：NumPy 的 `mean`、`std`、`sum` 等方法默认不统计 Series 里的空值。

```
In [87]: np.mean(df['one'])
Out[87]: 0.8110935116651192

In [88]: np.mean(df['one'].to_numpy())
Out[88]: nan
```

[`Series.nunique()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.nunique.html#pandas.Series.nunique) 返回 Series 里所有非空值的唯一值。

```
In [89]: series = pd.Series(np.random.randn(500))

In [90]: series[20:500] = np.nan

In [91]: series[10:20] = 5

In [92]: series.nunique()
Out[92]: 11
```

### 数据总结：`describe`

[`describe()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html#pandas.DataFrame.describe)  函数计算 Series 与 DataFrame 数据列的各种数据统计量，注意，这里排除了**空值**。

```
In [93]: series = pd.Series(np.random.randn(1000))

In [94]: series[::2] = np.nan

In [95]: series.describe()
Out[95]: 
count    500.000000
mean      -0.021292
std        1.015906
min       -2.683763
25%       -0.699070
50%       -0.069718
75%        0.714483
max        3.160915
dtype: float64

In [96]: frame = pd.DataFrame(np.random.randn(1000, 5),
   ....:                      columns=['a', 'b', 'c', 'd', 'e'])
   ....: 

In [97]: frame.iloc[::2] = np.nan

In [98]: frame.describe()
Out[98]: 
                a           b           c           d           e
count  500.000000  500.000000  500.000000  500.000000  500.000000
mean     0.033387    0.030045   -0.043719   -0.051686    0.005979
std      1.017152    0.978743    1.025270    1.015988    1.006695
min     -3.000951   -2.637901   -3.303099   -3.159200   -3.188821
25%     -0.647623   -0.576449   -0.712369   -0.691338   -0.691115
50%      0.047578   -0.021499   -0.023888   -0.032652   -0.025363
75%      0.729907    0.775880    0.618896    0.670047    0.649748
max      2.740139    2.752332    3.004229    2.728702    3.240991
```

此外，还可以指定输出结果包含的分位数：

```
In [99]: series.describe(percentiles=[.05, .25, .75, .95])
Out[99]: 
count    500.000000
mean      -0.021292
std        1.015906
min       -2.683763
5%        -1.645423
25%       -0.699070
50%       -0.069718
75%        0.714483
95%        1.711409
max        3.160915
dtype: float64
```

一般情况下，默认值包含**中位数**。

对于非数值型 Series 对象， [`describe()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.describe.html#pandas.Series.describe)  返回值的总数、唯一值数量、出现次数最多的值及出现的次数。

```
In [100]: s = pd.Series(['a', 'a', 'b', 'b', 'a', 'a', np.nan, 'c', 'd', 'a'])

In [101]: s.describe()
Out[101]: 
count     9
unique    4
top       a
freq      5
dtype: object
```

注意：对于混合型的 DataFrame 对象， [`describe()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.describe.html#pandas.Series.describe)  只返回数值列的汇总统计量，如果没有数值列，则只显示类别型的列。

```
In [102]: frame = pd.DataFrame({'a': ['Yes', 'Yes', 'No', 'No'], 'b': range(4)})

In [103]: frame.describe()
Out[103]: 
              b
count  4.000000
mean   1.500000
std    1.290994
min    0.000000
25%    0.750000
50%    1.500000
75%    2.250000
max    3.000000
```
`include/exclude` 参数的值为列表，用该参数可以控制包含或排除的数据类型。这里还有一个特殊值，`all`：

```
In [104]: frame.describe(include=['object'])
Out[104]: 
          a
count     4
unique    2
top     Yes
freq      2

In [105]: frame.describe(include=['number'])
Out[105]: 
              b
count  4.000000
mean   1.500000
std    1.290994
min    0.000000
25%    0.750000
50%    1.500000
75%    2.250000
max    3.000000

In [106]: frame.describe(include='all')
Out[106]: 
          a         b
count     4  4.000000
unique    2       NaN
top     Yes       NaN
freq      2       NaN
mean    NaN  1.500000
std     NaN  1.290994
min     NaN  0.000000
25%     NaN  0.750000
50%     NaN  1.500000
75%     NaN  2.250000
max     NaN  3.000000
```
本功能依托于 [`select_dtypes`](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-selectdtypes)，要了解该参数接受哪些输入内容请参阅[本文](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-selectdtypes)。

### 最大值与最小值对应的索引

Series 与 DataFrame 的 [`idxmax()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html#pandas.DataFrame.idxmax)  与 [`idxmin()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmin.html#pandas.DataFrame.idxmin) 函数计算最大值与最小值对应的索引。

```
In [107]: s1 = pd.Series(np.random.randn(5))

In [108]: s1
Out[108]: 
0    1.118076
1   -0.352051
2   -1.242883
3   -1.277155
4   -0.641184
dtype: float64

In [109]: s1.idxmin(), s1.idxmax()
Out[109]: (3, 0)

In [110]: df1 = pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])

In [111]: df1
Out[111]: 
          A         B         C
0 -0.327863 -0.946180 -0.137570
1 -0.186235 -0.257213 -0.486567
2 -0.507027 -0.871259 -0.111110
3  2.000339 -2.430505  0.089759
4 -0.321434 -0.033695  0.096271

In [112]: df1.idxmin(axis=0)
Out[112]: 
A    2
B    3
C    1
dtype: int64

In [113]: df1.idxmax(axis=1)
Out[113]: 
0    C
1    A
2    C
3    A
4    C
dtype: object
```

多行或多列中存在多个最大值或最小值时，[`idxmax()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html#pandas.DataFrame.idxmax) 与 [`idxmin()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmin.html#pandas.DataFrame.idxmin) 只返回匹配到的第一个值的 `Index`：

```
In [114]: df3 = pd.DataFrame([2, 1, 1, 3, np.nan], columns=['A'], index=list('edcba'))

In [115]: df3
Out[115]: 
     A
e  2.0
d  1.0
c  1.0
b  3.0
a  NaN

In [116]: df3['A'].idxmin()
Out[116]: 'd'
```
::: tip 注意

`idxmin` 与 `idxmax` 对应 NumPy 里的 `argmin` 与 `argmax`。

:::

### 值计数（直方图）与众数

Series 的 [`value_counts()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html#pandas.Series.value_counts) 方法及顶级函数计算一维数组中数据值的直方图，还可以用作常规数组的函数：

```
In [117]: data = np.random.randint(0, 7, size=50)

In [118]: data
Out[118]: 
array([6, 6, 2, 3, 5, 3, 2, 5, 4, 5, 4, 3, 4, 5, 0, 2, 0, 4, 2, 0, 3, 2,
       2, 5, 6, 5, 3, 4, 6, 4, 3, 5, 6, 4, 3, 6, 2, 6, 6, 2, 3, 4, 2, 1,
       6, 2, 6, 1, 5, 4])

In [119]: s = pd.Series(data)

In [120]: s.value_counts()
Out[120]: 
6    10
2    10
4     9
5     8
3     8
0     3
1     2
dtype: int64

In [121]: pd.value_counts(data)
Out[121]: 
6    10
2    10
4     9
5     8
3     8
0     3
1     2
dtype: int64
```

与上述操作类似，还可以统计 Series 或 DataFrame 的众数，即出现频率最高的值：

```
In [122]: s5 = pd.Series([1, 1, 3, 3, 3, 5, 5, 7, 7, 7])

In [123]: s5.mode()
Out[123]: 
0    3
1    7
dtype: int64

In [124]: df5 = pd.DataFrame({"A": np.random.randint(0, 7, size=50),
   .....:                     "B": np.random.randint(-10, 15, size=50)})
   .....: 

In [125]: df5.mode()
Out[125]: 
     A   B
0  1.0  -9
1  NaN  10
2  NaN  13
```

### 离散化与分位数

[`cut() 函数`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.cut.html#pandas.cut)（以值为依据实现分箱）及 [`qcut() 函数`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.qcut.html#pandas.qcut)（以样本分位数为依据实现分箱）用于连续值的离散化：

```
In [126]: arr = np.random.randn(20)

In [127]: factor = pd.cut(arr, 4)

In [128]: factor
Out[128]: 
[(-0.251, 0.464], (-0.968, -0.251], (0.464, 1.179], (-0.251, 0.464], (-0.968, -0.251], ..., (-0.251, 0.464], (-0.968, -0.251], (-0.968, -0.251], (-0.968, -0.251], (-0.968, -0.251]]
Length: 20
Categories (4, interval[float64]): [(-0.968, -0.251] < (-0.251, 0.464] < (0.464, 1.179] <
                                    (1.179, 1.893]]

In [129]: factor = pd.cut(arr, [-5, -1, 0, 1, 5])

In [130]: factor
Out[130]: 
[(0, 1], (-1, 0], (0, 1], (0, 1], (-1, 0], ..., (-1, 0], (-1, 0], (-1, 0], (-1, 0], (-1, 0]]
Length: 20
Categories (4, interval[int64]): [(-5, -1] < (-1, 0] < (0, 1] < (1, 5]]
```

[`qcut()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.qcut.html#pandas.qcut) 计算样本分位数。比如，下列代码按等距分位数分割正态分布的数据：

```
In [131]: arr = np.random.randn(30)

In [132]: factor = pd.qcut(arr, [0, .25, .5, .75, 1])

In [133]: factor
Out[133]: 
[(0.569, 1.184], (-2.278, -0.301], (-2.278, -0.301], (0.569, 1.184], (0.569, 1.184], ..., (-0.301, 0.569], (1.184, 2.346], (1.184, 2.346], (-0.301, 0.569], (-2.278, -0.301]]
Length: 30
Categories (4, interval[float64]): [(-2.278, -0.301] < (-0.301, 0.569] < (0.569, 1.184] <
                                    (1.184, 2.346]]

In [134]: pd.value_counts(factor)
Out[134]: 
(1.184, 2.346]      8
(-2.278, -0.301]    8
(0.569, 1.184]      7
(-0.301, 0.569]     7
dtype: int64
```

定义分箱时，还可以传递无穷值：

```
In [135]: arr = np.random.randn(20)

In [136]: factor = pd.cut(arr, [-np.inf, 0, np.inf])

In [137]: factor
Out[137]: 
[(-inf, 0.0], (0.0, inf], (0.0, inf], (-inf, 0.0], (-inf, 0.0], ..., (-inf, 0.0], (-inf, 0.0], (-inf, 0.0], (0.0, inf], (0.0, inf]]
Length: 20
Categories (2, interval[float64]): [(-inf, 0.0] < (0.0, inf]]
```

## 函数应用

不管是为 Pandas 对象应用自定义函数，还是应用第三方函数，都离不开以下三种方法。用哪种方法取决于操作的对象是 `DataFrame`，还是 `Series` ；是行、列，还是元素。

1. 表级函数应用：[`pipe()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html#pandas.DataFrame.pipe)
2. 行列级函数应用： [`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply)

3. 聚合 API： [`agg()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.agg.html#pandas.DataFrame.agg) 与 [`transform()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.transform.html#pandas.DataFrame.transform)
4. 元素级函数应用：[`applymap()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.applymap.html#pandas.DataFrame.applymap)

### 表级函数应用

虽然可以把 DataFrame 与 Series 传递给函数，不过链式调用函数时，最好使用 [`pipe()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html#pandas.DataFrame.pipe) 方法。对比以下两种方式：

```
# f、g、h 是提取、返回 `DataFrames` 的函数
>>> f(g(h(df), arg1=1), arg2=2, arg3=3)
```

下列代码与上述代码等效：

```
>>> (df.pipe(h)
...    .pipe(g, arg1=1)
...    .pipe(f, arg2=2, arg3=3))
```

Pandas 鼓励使用第二种方式，即链式方法。在链式方法中调用自定义函数或第三方支持库函数时，用 `pipe` 更容易，与用 Pandas 自身方法一样。

上例中，`f`、`g`  与 `h` 这几个函数都把 `DataFrame` 当作首位参数。要是想把数据作为第二个参数，该怎么办？本例中，`pipe` 为元组 （`callable,data_keyword`）形式。`.pipe` 把  `DataFrame`  作为元组里指定的参数。

下例用 statsmodels 拟合回归。该 API 先接收一个公式，`DataFrame` 是第二个参数，`data`。要传递函数，则要用`pipe` 接收关键词对 (`sm.ols,'data'`)。

```
In [138]: import statsmodels.formula.api as sm

In [139]: bb = pd.read_csv('data/baseball.csv', index_col='id')

In [140]: (bb.query('h > 0')
   .....:    .assign(ln_h=lambda df: np.log(df.h))
   .....:    .pipe((sm.ols, 'data'), 'hr ~ ln_h + year + g + C(lg)')
   .....:    .fit()
   .....:    .summary()
   .....:  )
   .....: 
Out[140]: 
<class 'statsmodels.iolib.summary.Summary'>
"""
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                     hr   R-squared:                       0.685
Model:                            OLS   Adj. R-squared:                  0.665
Method:                 Least Squares   F-statistic:                     34.28
Date:                Thu, 22 Aug 2019   Prob (F-statistic):           3.48e-15
Time:                        15:48:59   Log-Likelihood:                -205.92
No. Observations:                  68   AIC:                             421.8
Df Residuals:                      63   BIC:                             432.9
Df Model:                           4                                         
Covariance Type:            nonrobust                                         
===============================================================================
                  coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------
Intercept   -8484.7720   4664.146     -1.819      0.074   -1.78e+04     835.780
C(lg)[T.NL]    -2.2736      1.325     -1.716      0.091      -4.922       0.375
ln_h           -1.3542      0.875     -1.547      0.127      -3.103       0.395
year            4.2277      2.324      1.819      0.074      -0.417       8.872
g               0.1841      0.029      6.258      0.000       0.125       0.243
==============================================================================
Omnibus:                       10.875   Durbin-Watson:                   1.999
Prob(Omnibus):                  0.004   Jarque-Bera (JB):               17.298
Skew:                           0.537   Prob(JB):                     0.000175
Kurtosis:                       5.225   Cond. No.                     1.49e+07
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.49e+07. This might indicate that there are
strong multicollinearity or other numerical problems.
"""
```

unix 的 `pipe`  与后来出现的 [dplyr](https://github.com/hadley/dplyr) 及 [magrittr](https://github.com/smbache/magrittr) 启发了`pipe` 方法，在此，引入了 R 语言里用于读取 pipe 的操作符 (`%>%`)。`pipe` 的实现思路非常清晰，仿佛 Python 源生的一样。强烈建议大家阅读  [`pipe()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html#pandas.DataFrame.pipe)  的源代码。

### 行列级函数应用

[`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply) 方法沿着 DataFrame 的轴应用函数，比如，描述性统计方法，该方法支持  `axis` 参数。

```
In [141]: df.apply(np.mean)
Out[141]: 
one      0.811094
two      1.360588
three    0.187958
dtype: float64

In [142]: df.apply(np.mean, axis=1)
Out[142]: 
a    1.583749
b    0.734929
c    1.133683
d   -0.166914
dtype: float64

In [143]: df.apply(lambda x: x.max() - x.min())
Out[143]: 
one      1.051928
two      1.632779
three    1.840607
dtype: float64

In [144]: df.apply(np.cumsum)
Out[144]: 
        one       two     three
a  1.394981  1.772517       NaN
b  1.738035  3.684640 -0.050390
c  2.433281  5.163008  1.177045
d       NaN  5.442353  0.563873

In [145]: df.apply(np.exp)
Out[145]: 
        one       two     three
a  4.034899  5.885648       NaN
b  1.409244  6.767440  0.950858
c  2.004201  4.385785  3.412466
d       NaN  1.322262  0.541630
```

[`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply) 方法还支持通过函数名字符串调用函数。

```
In [146]: df.apply('mean')
Out[146]: 
one      0.811094
two      1.360588
three    0.187958
dtype: float64

In [147]: df.apply('mean', axis=1)
Out[147]: 
a    1.583749
b    0.734929
c    1.133683
d   -0.166914
dtype: float64
```

默认情况下，[`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply) 调用的函数返回的类型会影响 `DataFrame.apply` 输出结果的类型。

* 函数返回的是 `Series` 时，最终输出结果是 `DataFrame`。输出的列与函数返回的 `Series` 索引相匹配。

* 函数返回其它任意类型时，输出结果是 `Series`。

`result_type`  会覆盖默认行为，该参数有三个选项：`reduce`、`broadcast`、`expand`。这些选项决定了列表型返回值是否扩展为 `DataFrame`。

用好 [`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply "pandas.DataFrame.apply") 可以了解数据集的很多信息。比如可以提取每列的最大值对应的日期：

```
In [148]: tsdf = pd.DataFrame(np.random.randn(1000, 3), columns=['A', 'B', 'C'],
   .....:                     index=pd.date_range('1/1/2000', periods=1000))
   .....: 

In [149]: tsdf.apply(lambda x: x.idxmax())
Out[149]: 
A   2000-08-06
B   2001-01-18
C   2001-07-18
dtype: datetime64[ns]
```

还可以向 [`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply "pandas.DataFrame.apply") 方法传递额外的参数与关键字参数。比如下例中要应用的这个函数：

```
def subtract_and_divide(x, sub, divide=1):
    return (x - sub) / divide
```

可以用下列方式应用该函数：

```
df.apply(subtract_and_divide, args=(5,), divide=3)
```

为每行或每列执行 `Series` 方法的功能也很实用：

```
In [150]: tsdf
Out[150]: 
                   A         B         C
2000-01-01 -0.158131 -0.232466  0.321604
2000-01-02 -1.810340 -3.105758  0.433834
2000-01-03 -1.209847 -1.156793 -0.136794
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08 -0.653602  0.178875  1.008298
2000-01-09  1.007996  0.462824  0.254472
2000-01-10  0.307473  0.600337  1.643950

In [151]: tsdf.apply(pd.Series.interpolate)
Out[151]: 
                   A         B         C
2000-01-01 -0.158131 -0.232466  0.321604
2000-01-02 -1.810340 -3.105758  0.433834
2000-01-03 -1.209847 -1.156793 -0.136794
2000-01-04 -1.098598 -0.889659  0.092225
2000-01-05 -0.987349 -0.622526  0.321243
2000-01-06 -0.876100 -0.355392  0.550262
2000-01-07 -0.764851 -0.088259  0.779280
2000-01-08 -0.653602  0.178875  1.008298
2000-01-09  1.007996  0.462824  0.254472
2000-01-10  0.307473  0.600337  1.643950
```
[`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply "pandas.DataFrame.apply") 有一个参数 `raw`，默认值为 `False`，在应用函数前，使用该参数可以将每行或列转换为 `Series`。该参数为 `True` 时，传递的函数接收 ndarray 对象，若不需要索引功能，这种操作能显著提高性能。

### 聚合 API

*0.20.0 版新增*。

聚合 API 可以快速、简洁地执行多个聚合操作。Pandas 对象支持多个类似的 API，如 [groupby API](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-aggregate)、[window functions API](https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#stats-aggregate)、[resample API](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-aggregate)。聚合函数为[`DataFrame.aggregate()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.aggregate.html#pandas.DataFrame.aggregate "pandas.DataFrame.aggregate")，它的别名是 [`DataFrame.agg()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.agg.html#pandas.DataFrame.agg "pandas.DataFrame.agg")。

此处用与上例类似的 `DataFrame`：

```
In [152]: tsdf = pd.DataFrame(np.random.randn(10, 3), columns=['A', 'B', 'C'],
   .....:                     index=pd.date_range('1/1/2000', periods=10))
   .....: 

In [153]: tsdf.iloc[3:7] = np.nan

In [154]: tsdf
Out[154]: 
                   A         B         C
2000-01-01  1.257606  1.004194  0.167574
2000-01-02 -0.749892  0.288112 -0.757304
2000-01-03 -0.207550 -0.298599  0.116018
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.814347 -0.257623  0.869226
2000-01-09 -0.250663 -1.206601  0.896839
2000-01-10  2.169758 -1.333363  0.283157
```

应用单个函数时，该操作与 [`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply "pandas.DataFrame.apply") 等效，这里也可以用字符串表示聚合函数名。下面的聚合函数输出的结果为 `Series`：

```
In [155]: tsdf.agg(np.sum)
Out[155]: 
A    3.033606
B   -1.803879
C    1.575510
dtype: float64

In [156]: tsdf.agg('sum')
Out[156]: 
A    3.033606
B   -1.803879
C    1.575510
dtype: float64

# 因为应用的是单个函数，该操作与`.sum()` 是等效的
In [157]: tsdf.sum()
Out[157]: 
A    3.033606
B   -1.803879
C    1.575510
dtype: float64
```

`Series` 单个聚合操作返回标量值：

```
In [158]: tsdf.A.agg('sum')
Out[158]: 3.033606102414146
```

### 多函数聚合

还可以用列表形式传递多个聚合函数。每个函数在输出结果 `DataFrame` 里以行的形式显示，行名是每个聚合函数的函数名。

```
In [159]: tsdf.agg(['sum'])
Out[159]: 
            A         B        C
sum  3.033606 -1.803879  1.57551
```

多个函数输出多行：

```
In [160]: tsdf.agg(['sum', 'mean'])
Out[160]: 
             A         B         C
sum   3.033606 -1.803879  1.575510
mean  0.505601 -0.300647  0.262585
```

`Series` 聚合多函数返回结果还是 `Series`，索引为函数名：

```
In [161]: tsdf.A.agg(['sum', 'mean'])
Out[161]: 
sum     3.033606
mean    0.505601
Name: A, dtype: float64
```
传递 `lambda` 函数时，输出名为 `<lambda>` 的行：

```
In [162]: tsdf.A.agg(['sum', lambda x: x.mean()])
Out[162]: 
sum         3.033606
<lambda>    0.505601
Name: A, dtype: float64
```

应用自定义函数时，该函数名为输出结果的行名：

```
In [163]: def mymean(x):
   .....:     return x.mean()
   .....: 

In [164]: tsdf.A.agg(['sum', mymean])
Out[164]: 
sum       3.033606
mymean    0.505601
Name: A, dtype: float64
```

### 用字典实现聚合

指定为哪些列应用哪些聚合函数时，需要把包含列名与标量（或标量列表）的字典传递给 `DataFrame.agg`。

注意：这里输出结果的顺序不是固定的，要想让输出顺序与输入顺序一致，请使用 `OrderedDict`。

```
In [165]: tsdf.agg({'A': 'mean', 'B': 'sum'})
Out[165]: 
A    0.505601
B   -1.803879
dtype: float64
```
输入的参数是列表时，输出结果为  `DataFrame`，并以矩阵形式显示所有聚合函数的计算结果，且输出结果由所有唯一函数组成。未执行聚合操作的列输出结果为 `NaN` 值：

```
In [166]: tsdf.agg({'A': ['mean', 'min'], 'B': 'sum'})
Out[166]: 
             A         B
mean  0.505601       NaN
min  -0.749892       NaN
sum        NaN -1.803879
```

### 多种数据类型（Dtype）

与 `groupby` 的 `.agg` 操作类似，DataFrame 含不能执行聚合的数据类型时，`.agg` 只计算可聚合的列：

```
In [167]: mdf = pd.DataFrame({'A': [1, 2, 3],
   .....:                     'B': [1., 2., 3.],
   .....:                     'C': ['foo', 'bar', 'baz'],
   .....:                     'D': pd.date_range('20130101', periods=3)})
   .....: 

In [168]: mdf.dtypes
Out[168]: 
A             int64
B           float64
C            object
D    datetime64[ns]
dtype: object
```

```
In [169]: mdf.agg(['min', 'sum'])
Out[169]: 
     A    B          C          D
min  1  1.0        bar 2013-01-01
sum  6  6.0  foobarbaz        NaT
```

### 自定义 Describe

`.agg()` 可以创建类似于内置 [describe 函数](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-describe) 的自定义 describe 函数。

```
In [170]: from functools import partial

In [171]: q_25 = partial(pd.Series.quantile, q=0.25)

In [172]: q_25.__name__ = '25%'

In [173]: q_75 = partial(pd.Series.quantile, q=0.75)

In [174]: q_75.__name__ = '75%'

In [175]: tsdf.agg(['count', 'mean', 'std', 'min', q_25, 'median', q_75, 'max'])
Out[175]: 
               A         B         C
count   6.000000  6.000000  6.000000
mean    0.505601 -0.300647  0.262585
std     1.103362  0.887508  0.606860
min    -0.749892 -1.333363 -0.757304
25%    -0.239885 -0.979600  0.128907
median  0.303398 -0.278111  0.225365
75%     1.146791  0.151678  0.722709
max     2.169758  1.004194  0.896839
```
### Transform API

*0.20.0 版新增*。

[`transform()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.transform.html#pandas.DataFrame.transform "pandas.DataFrame.transform") 方法的返回结果与原始数据的索引相同，大小相同。与 `.agg` API 类似，该 API 支持同时处理多种操作，不用一个一个操作。

下面，先创建一个 DataFrame：

```
In [176]: tsdf = pd.DataFrame(np.random.randn(10, 3), columns=['A', 'B', 'C'],
   .....:                     index=pd.date_range('1/1/2000', periods=10))
   .....: 

In [177]: tsdf.iloc[3:7] = np.nan

In [178]: tsdf
Out[178]: 
                   A         B         C
2000-01-01 -0.428759 -0.864890 -0.675341
2000-01-02 -0.168731  1.338144 -1.279321
2000-01-03 -1.621034  0.438107  0.903794
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.254374 -1.240447 -0.201052
2000-01-09 -0.157795  0.791197 -1.144209
2000-01-10 -0.030876  0.371900  0.061932
```

这里转换的是整个 DataFrame。`.transform()` 支持 NumPy 函数、字符串函数及自定义函数。

```
In [179]: tsdf.transform(np.abs)
Out[179]: 
                   A         B         C
2000-01-01  0.428759  0.864890  0.675341
2000-01-02  0.168731  1.338144  1.279321
2000-01-03  1.621034  0.438107  0.903794
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.254374  1.240447  0.201052
2000-01-09  0.157795  0.791197  1.144209
2000-01-10  0.030876  0.371900  0.061932

In [180]: tsdf.transform('abs')
Out[180]: 
                   A         B         C
2000-01-01  0.428759  0.864890  0.675341
2000-01-02  0.168731  1.338144  1.279321
2000-01-03  1.621034  0.438107  0.903794
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.254374  1.240447  0.201052
2000-01-09  0.157795  0.791197  1.144209
2000-01-10  0.030876  0.371900  0.061932

In [181]: tsdf.transform(lambda x: x.abs())
Out[181]: 
                   A         B         C
2000-01-01  0.428759  0.864890  0.675341
2000-01-02  0.168731  1.338144  1.279321
2000-01-03  1.621034  0.438107  0.903794
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.254374  1.240447  0.201052
2000-01-09  0.157795  0.791197  1.144209
2000-01-10  0.030876  0.371900  0.061932
```
这里的 [`transform()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.transform.html#pandas.DataFrame.transform "pandas.DataFrame.transform") 接受单个函数；与 ufunc 等效。

```
In [182]: np.abs(tsdf)
Out[182]: 
                   A         B         C
2000-01-01  0.428759  0.864890  0.675341
2000-01-02  0.168731  1.338144  1.279321
2000-01-03  1.621034  0.438107  0.903794
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.254374  1.240447  0.201052
2000-01-09  0.157795  0.791197  1.144209
2000-01-10  0.030876  0.371900  0.061932
```

 `.transform()` 向 `Series` 传递单个函数时，返回的结果也是单个 `Series`。

```
In [183]: tsdf.A.transform(np.abs)
Out[183]: 
2000-01-01    0.428759
2000-01-02    0.168731
2000-01-03    1.621034
2000-01-04         NaN
2000-01-05         NaN
2000-01-06         NaN
2000-01-07         NaN
2000-01-08    0.254374
2000-01-09    0.157795
2000-01-10    0.030876
Freq: D, Name: A, dtype: float64
```

### 多函数 Transform

`transform()` 调用多个函数时，生成多层索引 DataFrame。第一层是原始数据集的列名；第二层是 `transform()` 调用的函数名。

```
In [184]: tsdf.transform([np.abs, lambda x: x + 1])
Out[184]: 
                   A                   B                   C          
            absolute  <lambda>  absolute  <lambda>  absolute  <lambda>
2000-01-01  0.428759  0.571241  0.864890  0.135110  0.675341  0.324659
2000-01-02  0.168731  0.831269  1.338144  2.338144  1.279321 -0.279321
2000-01-03  1.621034 -0.621034  0.438107  1.438107  0.903794  1.903794
2000-01-04       NaN       NaN       NaN       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN       NaN       NaN       NaN
2000-01-08  0.254374  1.254374  1.240447 -0.240447  0.201052  0.798948
2000-01-09  0.157795  0.842205  0.791197  1.791197  1.144209 -0.144209
2000-01-10  0.030876  0.969124  0.371900  1.371900  0.061932  1.061932
```

为 Series 应用多个函数时，输出结果是 DataFrame，列名是 `transform()` 调用的函数名。

```
In [185]: tsdf.A.transform([np.abs, lambda x: x + 1])
Out[185]: 
            absolute  <lambda>
2000-01-01  0.428759  0.571241
2000-01-02  0.168731  0.831269
2000-01-03  1.621034 -0.621034
2000-01-04       NaN       NaN
2000-01-05       NaN       NaN
2000-01-06       NaN       NaN
2000-01-07       NaN       NaN
2000-01-08  0.254374  1.254374
2000-01-09  0.157795  0.842205
2000-01-10  0.030876  0.969124
```

### 用字典执行 `transform` 操作

函数字典可以为每列执行指定 `transform()` 操作。  

```
In [186]: tsdf.transform({'A': np.abs, 'B': lambda x: x + 1})
Out[186]: 
                   A         B
2000-01-01  0.428759  0.135110
2000-01-02  0.168731  2.338144
2000-01-03  1.621034  1.438107
2000-01-04       NaN       NaN
2000-01-05       NaN       NaN
2000-01-06       NaN       NaN
2000-01-07       NaN       NaN
2000-01-08  0.254374 -0.240447
2000-01-09  0.157795  1.791197
2000-01-10  0.030876  1.371900
```

`transform()` 的参数是列表字典时，生成的是以 `transform()` 调用的函数为名的多层索引 DataFrame。

```
In [187]: tsdf.transform({'A': np.abs, 'B': [lambda x: x + 1, 'sqrt']})
Out[187]: 
                   A         B          
            absolute  <lambda>      sqrt
2000-01-01  0.428759  0.135110       NaN
2000-01-02  0.168731  2.338144  1.156782
2000-01-03  1.621034  1.438107  0.661897
2000-01-04       NaN       NaN       NaN
2000-01-05       NaN       NaN       NaN
2000-01-06       NaN       NaN       NaN
2000-01-07       NaN       NaN       NaN
2000-01-08  0.254374 -0.240447       NaN
2000-01-09  0.157795  1.791197  0.889493
2000-01-10  0.030876  1.371900  0.609836
```

### 元素级函数应用

并非所有函数都能矢量化，即接受 NumPy 数组，返回另一个数组或值，DataFrame 的 [`applymap()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.applymap.html#pandas.DataFrame.applymap "pandas.DataFrame.applymap") 及 Series 的 [`map()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.map.html#pandas.Series.map "pandas.Series.map") ，支持任何接收单个值并返回单个值的 Python 函数。

示例如下：

```
In [188]: df4
Out[188]: 
        one       two     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [189]: def f(x):
   .....:     return len(str(x))
   .....: 

In [190]: df4['one'].map(f)
Out[190]: 
a    18
b    19
c    18
d     3
Name: one, dtype: int64

In [191]: df4.applymap(f)
Out[191]: 
   one  two  three
a   18   17      3
b   19   18     20
c   18   18     16
d    3   19     19
```

[`Series.map()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.map.html#pandas.Series.map "pandas.Series.map") 还有个功能，可以“连接”或“映射”第二个 Series 定义的值。这与 [merging / joining 功能](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#merging)联系非常紧密：

```
In [192]: s = pd.Series(['six', 'seven', 'six', 'seven', 'six'],
   .....:               index=['a', 'b', 'c', 'd', 'e'])
   .....: 

In [193]: t = pd.Series({'six': 6., 'seven': 7.})

In [194]: s
Out[194]: 
a      six
b    seven
c      six
d    seven
e      six
dtype: object

In [195]: s.map(t)
Out[195]: 
a    6.0
b    7.0
c    6.0
d    7.0
e    6.0
dtype: float64
```

## 重置索引与更换标签

[`reindex()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.reindex.html#pandas.Series.reindex "pandas.Series.reindex") 是 Pandas 里实现数据对齐的基本方法，该方法执行几乎所有功能都要用到的标签对齐功能。 `reindex` 指的是沿着指定轴，让数据与给定的一组标签进行匹配。该功能完成以下几项操作：

* 让现有数据匹配一组新标签，并重新排序；
* 在无数据但有标签的位置插入缺失值（`NA`）标记；
* 如果指定，则按逻辑**填充**无标签的数据，该操作多见于时间序列数据。

示例如下：

```
In [196]: s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])

In [197]: s
Out[197]: 
a    1.695148
b    1.328614
c    1.234686
d   -0.385845
e   -1.326508
dtype: float64

In [198]: s.reindex(['e', 'b', 'f', 'd'])
Out[198]: 
e   -1.326508
b    1.328614
f         NaN
d   -0.385845
dtype: float64
```

本例中，原 Series 里没有标签 `f` ，因此，输出结果里 `f` 对应的值为 `NaN`。

DataFrame 支持同时 `reindex` 索引与列：

```
In [199]: df
Out[199]: 
        one       two     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [200]: df.reindex(index=['c', 'f', 'b'], columns=['three', 'two', 'one'])
Out[200]: 
      three       two       one
c  1.227435  1.478369  0.695246
f       NaN       NaN       NaN
b -0.050390  1.912123  0.343054
```

`reindex` 还支持 `axis` 关键字：

```
In [201]: df.reindex(['c', 'f', 'b'], axis='index')
Out[201]: 
        one       two     three
c  0.695246  1.478369  1.227435
f       NaN       NaN       NaN
b  0.343054  1.912123 -0.050390
```

注意：不同对象可以**共享** `Index` 包含的轴标签。比如，有一个 Series，还有一个 DataFrame，可以执行下列操作：

```
In [202]: rs = s.reindex(df.index)

In [203]: rs
Out[203]: 
a    1.695148
b    1.328614
c    1.234686
d   -0.385845
dtype: float64

In [204]: rs.index is df.index
Out[204]: True
```

这里指的是，重置后，Series 的索引与 DataFrame 的索引是同一个 Python 对象。

*0.21.0 版新增*。

[`DataFrame.reindex()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reindex.html#pandas.DataFrame.reindex "pandas.DataFrame.reindex") 还支持 “轴样式”调用习语，可以指定单个 `labels` 参数，并指定应用于哪个 `axis`。

```
In [205]: df.reindex(['c', 'f', 'b'], axis='index')
Out[205]: 
        one       two     three
c  0.695246  1.478369  1.227435
f       NaN       NaN       NaN
b  0.343054  1.912123 -0.050390

In [206]: df.reindex(['three', 'two', 'one'], axis='columns')
Out[206]: 
      three       two       one
a       NaN  1.772517  1.394981
b -0.050390  1.912123  0.343054
c  1.227435  1.478369  0.695246
d -0.613172  0.279344       NaN
```
::: tip 注意

[多层索引与高级索引](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced)介绍了怎样用更简洁的方式重置索引。

:::

::: tip 注意

编写注重性能的代码时，最好花些时间深入理解 `reindex`：**预对齐数据后，操作会更快**。两个未对齐的 DataFrame 相加，后台操作会执行 `reindex`。探索性分析时很难注意到这点有什么不同，这是因为 `reindex` 已经进行了高度优化，但需要注重 CPU 周期时，显式调用 `reindex` 还是有一些影响的。

:::

### 重置索引，并与其它对象对齐

提取一个对象，并用另一个具有相同标签的对象 `reindex` 该对象的轴。这种操作的语法虽然简单，但未免有些啰嗦。这时，最好用 [`reindex_like()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reindex_like.html#pandas.DataFrame.reindex_like "pandas.DataFrame.reindex_like") 方法，这是一种既有效，又简单的方式：

```
In [207]: df2
Out[207]: 
        one       two
a  1.394981  1.772517
b  0.343054  1.912123
c  0.695246  1.478369

In [208]: df3
Out[208]: 
        one       two
a  0.583888  0.051514
b -0.468040  0.191120
c -0.115848 -0.242634

In [209]: df.reindex_like(df2)
Out[209]: 
        one       two
a  1.394981  1.772517
b  0.343054  1.912123
c  0.695246  1.478369
```

### 用 `align` 对齐多个对象

[`align()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.align.html#pandas.Series.align "pandas.Series.align") 方法是对齐两个对象最快的方式，该方法支持 `join` 参数（请参阅 [joining 与 merging](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#merging)）：

* `join='outer'`：使用两个对象索引的合集，默认值
* `join='left'`：使用左侧调用对象的索引
* `join='right'`：使用右侧传递对象的索引
* `join='inner'`：使用两个对象索引的交集

该方法返回重置索引后的两个 Series 元组：

```
In [210]: s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])

In [211]: s1 = s[:4]

In [212]: s2 = s[1:]

In [213]: s1.align(s2)
Out[213]: 
(a   -0.186646
 b   -1.692424
 c   -0.303893
 d   -1.425662
 e         NaN
 dtype: float64, a         NaN
 b   -1.692424
 c   -0.303893
 d   -1.425662
 e    1.114285
 dtype: float64)

In [214]: s1.align(s2, join='inner')
Out[214]: 
(b   -1.692424
 c   -0.303893
 d   -1.425662
 dtype: float64, b   -1.692424
 c   -0.303893
 d   -1.425662
 dtype: float64)

In [215]: s1.align(s2, join='left')
Out[215]: 
(a   -0.186646
 b   -1.692424
 c   -0.303893
 d   -1.425662
 dtype: float64, a         NaN
 b   -1.692424
 c   -0.303893
 d   -1.425662
 dtype: float64)
```

默认条件下，  `join` 方法既应用于索引，也应用于列：

```
In [216]: df.align(df2, join='inner')
Out[216]: 
(        one       two
 a  1.394981  1.772517
 b  0.343054  1.912123
 c  0.695246  1.478369,         one       two
 a  1.394981  1.772517
 b  0.343054  1.912123
 c  0.695246  1.478369)
```

`align` 方法还支持 `axis` 选项，用来指定要对齐的轴：

```
In [217]: df.align(df2, join='inner', axis=0)
Out[217]: 
(        one       two     three
 a  1.394981  1.772517       NaN
 b  0.343054  1.912123 -0.050390
 c  0.695246  1.478369  1.227435,         one       two
 a  1.394981  1.772517
 b  0.343054  1.912123
 c  0.695246  1.478369)
```

如果把 Series 传递给 [`DataFrame.align()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.align.html#pandas.DataFrame.align "pandas.DataFrame.align")，可以用 `axis` 参数选择是在 DataFrame 的索引，还是列上对齐两个对象：


```
In [218]: df.align(df2.iloc[0], axis=1)
Out[218]: 
(        one     three       two
 a  1.394981       NaN  1.772517
 b  0.343054 -0.050390  1.912123
 c  0.695246  1.227435  1.478369
 d       NaN -0.613172  0.279344, one      1.394981
 three         NaN
 two      1.772517
 Name: a, dtype: float64)
```

| 方法             | 动作               |
| :--------------- | :----------------- |
| pad / ffill      | 先前填充           |
| bfill / backfill | 向后填充           |
| nearest          | 从最近的索引值填充 |

下面用一个简单的 Series 展示 `fill` 方法：

```
In [219]: rng = pd.date_range('1/3/2000', periods=8)

In [220]: ts = pd.Series(np.random.randn(8), index=rng)

In [221]: ts2 = ts[[0, 3, 6]]

In [222]: ts
Out[222]: 
2000-01-03    0.183051
2000-01-04    0.400528
2000-01-05   -0.015083
2000-01-06    2.395489
2000-01-07    1.414806
2000-01-08    0.118428
2000-01-09    0.733639
2000-01-10   -0.936077
Freq: D, dtype: float64

In [223]: ts2
Out[223]: 
2000-01-03    0.183051
2000-01-06    2.395489
2000-01-09    0.733639
dtype: float64

In [224]: ts2.reindex(ts.index)
Out[224]: 
2000-01-03    0.183051
2000-01-04         NaN
2000-01-05         NaN
2000-01-06    2.395489
2000-01-07         NaN
2000-01-08         NaN
2000-01-09    0.733639
2000-01-10         NaN
Freq: D, dtype: float64

In [225]: ts2.reindex(ts.index, method='ffill')
Out[225]: 
2000-01-03    0.183051
2000-01-04    0.183051
2000-01-05    0.183051
2000-01-06    2.395489
2000-01-07    2.395489
2000-01-08    2.395489
2000-01-09    0.733639
2000-01-10    0.733639
Freq: D, dtype: float64

In [226]: ts2.reindex(ts.index, method='bfill')
Out[226]: 
2000-01-03    0.183051
2000-01-04    2.395489
2000-01-05    2.395489
2000-01-06    2.395489
2000-01-07    0.733639
2000-01-08    0.733639
2000-01-09    0.733639
2000-01-10         NaN
Freq: D, dtype: float64

In [227]: ts2.reindex(ts.index, method='nearest')
Out[227]: 
2000-01-03    0.183051
2000-01-04    0.183051
2000-01-05    2.395489
2000-01-06    2.395489
2000-01-07    2.395489
2000-01-08    0.733639
2000-01-09    0.733639
2000-01-10    0.733639
Freq: D, dtype: float64
```

上述操作要求索引按递增或递减**排序**。

注意：除了 `method='nearest'`，用 [`fillna`](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-fillna) 或 [`interpolate`](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-interpolate) 也能实现同样的效果：

```
In [228]: ts2.reindex(ts.index).fillna(method='ffill')
Out[228]: 
2000-01-03    0.183051
2000-01-04    0.183051
2000-01-05    0.183051
2000-01-06    2.395489
2000-01-07    2.395489
2000-01-08    2.395489
2000-01-09    0.733639
2000-01-10    0.733639
Freq: D, dtype: float64
```

如果索引不是按递增或递减排序，[`reindex()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.reindex.html#pandas.Series.reindex "pandas.Series.reindex") 会触发 ValueError 错误。[`fillna()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.fillna.html#pandas.Series.fillna "pandas.Series.fillna") 与 [`interpolate()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.interpolate.html#pandas.Series.interpolate "pandas.Series.interpolate") 则不检查索引的排序。

### 重置索引填充的限制

`limit` 与 `tolerance` 参数可以控制 `reindex` 的填充操作。`limit` 限定了连续匹配的最大数量：

```
In [229]: ts2.reindex(ts.index, method='ffill', limit=1)
Out[229]: 
2000-01-03    0.183051
2000-01-04    0.183051
2000-01-05         NaN
2000-01-06    2.395489
2000-01-07    2.395489
2000-01-08         NaN
2000-01-09    0.733639
2000-01-10    0.733639
Freq: D, dtype: float64
```

反之，`tolerance` 限定了索引与索引器值之间的最大距离：

```
In [230]: ts2.reindex(ts.index, method='ffill', tolerance='1 day')
Out[230]: 
2000-01-03    0.183051
2000-01-04    0.183051
2000-01-05         NaN
2000-01-06    2.395489
2000-01-07    2.395489
2000-01-08         NaN
2000-01-09    0.733639
2000-01-10    0.733639
Freq: D, dtype: float64
```

注意：索引为 `DatetimeIndex`、`TimedeltaIndex` 或 `PeriodIndex` 时，`tolerance` 会尽可能将这些索引强制转换为 `Timedelta`，这里要求用户用恰当的字符串设定 `tolerance` 参数。

### 去掉轴上的标签

[`drop()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html#pandas.DataFrame.drop "pandas.DataFrame.drop") 函数与 `reindex` 经常配合使用，该函数用于删除轴上的一组标签：

```
In [231]: df
Out[231]: 
        one       two     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [232]: df.drop(['a', 'd'], axis=0)
Out[232]: 
        one       two     three
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435

In [233]: df.drop(['one'], axis=1)
Out[233]: 
        two     three
a  1.772517       NaN
b  1.912123 -0.050390
c  1.478369  1.227435
d  0.279344 -0.613172
```

注意：下面的代码可以运行，但不够清晰：

```
In [234]: df.reindex(df.index.difference(['a', 'd']))
Out[234]: 
        one       two     three
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
```

### 重命名或映射标签

[`rename()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html#pandas.DataFrame.rename "pandas.DataFrame.rename") 方法支持按不同的轴基于映射（字典或 Series）调整标签。

```
In [235]: s
Out[235]: 
a   -0.186646
b   -1.692424
c   -0.303893
d   -1.425662
e    1.114285
dtype: float64

In [236]: s.rename(str.upper)
Out[236]: 
A   -0.186646
B   -1.692424
C   -0.303893
D   -1.425662
E    1.114285
dtype: float64
```

如果调用的是函数，该函数在处理标签时，必须返回一个值，而且生成的必须是一组唯一值。此外，`rename()` 还可以调用字典或 Series。

```
In [237]: df.rename(columns={'one': 'foo', 'two': 'bar'},
   .....:           index={'a': 'apple', 'b': 'banana', 'd': 'durian'})
   .....: 
Out[237]: 
             foo       bar     three
apple   1.394981  1.772517       NaN
banana  0.343054  1.912123 -0.050390
c       0.695246  1.478369  1.227435
durian       NaN  0.279344 -0.613172
```

Pandas 不会重命名标签未包含在映射里的列或索引。注意，映射里多出的标签不会触发错误。

*0.21.0 版新增*。

[`DataFrame.rename()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html#pandas.DataFrame.rename "pandas.DataFrame.rename") 还支持“轴式”习语，用这种方式可以指定单个 `mapper`，及执行映射的 `axis`。

```
In [238]: df.rename({'one': 'foo', 'two': 'bar'}, axis='columns')
Out[238]: 
        foo       bar     three
a  1.394981  1.772517       NaN
b  0.343054  1.912123 -0.050390
c  0.695246  1.478369  1.227435
d       NaN  0.279344 -0.613172

In [239]: df.rename({'a': 'apple', 'b': 'banana', 'd': 'durian'}, axis='index')
Out[239]: 
             one       two     three
apple   1.394981  1.772517       NaN
banana  0.343054  1.912123 -0.050390
c       0.695246  1.478369  1.227435
durian       NaN  0.279344 -0.613172
```

[`rename()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rename.html#pandas.Series.rename "pandas.Series.rename") 方法还提供了 `inplace` 命名参数，默认为 `False`，并会复制底层数据。`inplace=True` 时，会直接在原数据上重命名。

*0.18.0 版新增*。

[`rename()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rename.html#pandas.Series.rename "pandas.Series.rename") 还支持用标量或列表更改 `Series.name` 属性。

```
In [240]: s.rename("scalar-name")
Out[240]: 
a   -0.186646
b   -1.692424
c   -0.303893
d   -1.425662
e    1.114285
Name: scalar-name, dtype: float64
```

*0.24.0 版新增*。

[`rename_axis()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rename_axis.html#pandas.Series.rename_axis "pandas.Series.rename_axis") 方法支持指定 `多层索引` 名称，与标签相对应。

```
In [241]: df = pd.DataFrame({'x': [1, 2, 3, 4, 5, 6],
   .....:                    'y': [10, 20, 30, 40, 50, 60]},
   .....:                   index=pd.MultiIndex.from_product([['a', 'b', 'c'], [1, 2]],
   .....:                   names=['let', 'num']))
   .....: 

In [242]: df
Out[242]: 
         x   y
let num       
a   1    1  10
    2    2  20
b   1    3  30
    2    4  40
c   1    5  50
    2    6  60

In [243]: df.rename_axis(index={'let': 'abc'})
Out[243]: 
         x   y
abc num       
a   1    1  10
    2    2  20
b   1    3  30
    2    4  40
c   1    5  50
    2    6  60

In [244]: df.rename_axis(index=str.upper)
Out[244]: 
         x   y
LET NUM       
a   1    1  10
    2    2  20
b   1    3  30
    2    4  40
c   1    5  50
    2    6  60
```

## 迭代

Pandas 对象基于类型进行迭代操作。Series 迭代时被视为数组，基础迭代生成值。DataFrame 则遵循字典式习语，用对象的 `key` 实现迭代操作。

简言之，基础迭代（`for i in object`）生成：

* **Series** ：值
* **DataFrame**：列标签

例如，DataFrame 迭代时输出列名：

```
In [245]: df = pd.DataFrame({'col1': np.random.randn(3),
   .....:                    'col2': np.random.randn(3)}, index=['a', 'b', 'c'])
   .....: 

In [246]: for col in df:
   .....:     print(col)
   .....: 
col1
col2
```

Pandas 对象还支持字典式的 [`items()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.items.html#pandas.DataFrame.items "pandas.DataFrame.items") 方法，通过键值对迭代。

用下列方法可以迭代 DataFrame 里的行：

* [`iterrows()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows "pandas.DataFrame.iterrows")：把 DataFrame 里的行当作 （index， Series）对进行迭代。该操作把行转为 Series，同时改变数据类型，并对性能有影响。

* [`itertuples()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html#pandas.DataFrame.itertuples "pandas.DataFrame.itertuples") 把 DataFrame 的行当作值的命名元组进行迭代。该操作比  [`iterrows()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows "pandas.DataFrame.iterrows") 快的多，建议尽量用这种方法迭代 DataFrame 的值。

::: danger 警告

Pandas 对象迭代的速度较慢。大部分情况下，没必要对行执行迭代操作，建议用以下几种替代方式：

* 矢量化：很多操作可以用内置方法或 NumPy 函数，布尔索引……
* 调用的函数不能在完整的 DataFrame / Series 上运行时，最好用 [`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply "pandas.DataFrame.apply")，不要对值进行迭代操作。请参阅[函数应用](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-apply)文档。
* 如果必须对值进行迭代，请务必注意代码的性能，建议在 cython 或 numba 环境下实现内循环。参阅[性能优化](https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html#enhancingperf)一节，查看这种操作方法的示例。

:::

::: danger 警告

**永远不要修改**迭代的内容，这种方式不能确保所有操作都能正常运作。基于数据类型，迭代器返回的是复制（copy）的结果，不是视图（view），这种写入可能不会生效！

下例中的赋值就不会生效：

```
In [247]: df = pd.DataFrame({'a': [1, 2, 3], 'b': ['a', 'b', 'c']})

In [248]: for index, row in df.iterrows():
.....:     row['a'] = 10
.....: 

In [249]: df
Out[249]: 
a  b
0  1  a
1  2  b
2  3  c
```

:::

### 项目（items）
与字典型接口类似，[`items()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.items.html#pandas.DataFrame.items "pandas.DataFrame.items") 通过键值对进行迭代：

* **Series**：（Index，标量值）对
* **DataFrame**：（列，Series）对

示例如下：

```
In [250]: for label, ser in df.items():
   .....:     print(label)
   .....:     print(ser)
   .....: 
a
0    1
1    2
2    3
Name: a, dtype: int64
b
0    a
1    b
2    c
Name: b, dtype: object
```
### iterrows

[`iterrows()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows "pandas.DataFrame.iterrows") 迭代 DataFrame 或 Series 里的每一行数据。这个操作返回一个迭代器，生成索引值及包含每行数据的 Series：

```
In [251]: for row_index, row in df.iterrows():
   .....:     print(row_index, row, sep='\n')
   .....: 
0
a    1
b    a
Name: 0, dtype: object
1
a    2
b    b
Name: 1, dtype: object
2
a    3
b    c
Name: 2, dtype: object
```
::: tip 注意

[`iterrows()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows "pandas.DataFrame.iterrows") 返回的是 Series 里的每一行数据，该操作**不**保留每行数据的数据类型，因为数据类型是通过 DataFrame 的列界定的。

示例如下：

```
In [252]: df_orig = pd.DataFrame([[1, 1.5]], columns=['int', 'float'])

In [253]: df_orig.dtypes
Out[253]: 
int        int64
float    float64
dtype: object

In [254]: row = next(df_orig.iterrows())[1]

In [255]: row
Out[255]: 
int      1.0
float    1.5
Name: 0, dtype: float64
```
`row` 里的值以 Series 形式返回，并被转换为浮点数，原始的整数值则在列 X：

```
In [256]: row['int'].dtype
Out[256]: dtype('float64')

In [257]: df_orig['int'].dtype
Out[257]: dtype('int64')
```
要想在行迭代时保存数据类型，最好用 [`itertuples()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html#pandas.DataFrame.itertuples "pandas.DataFrame.itertuples")，这个函数返回值的命名元组，总的来说，该操作比 [`iterrows()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows "pandas.DataFrame.iterrows") 速度更快。

:::

下例展示了怎样转置 DataFrame：

```
In [258]: df2 = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

In [259]: print(df2)
   x  y
0  1  4
1  2  5
2  3  6

In [260]: print(df2.T)
   0  1  2
x  1  2  3
y  4  5  6

In [261]: df2_t = pd.DataFrame({idx: values for idx, values in df2.iterrows()})

In [262]: print(df2_t)
   0  1  2
x  1  2  3
y  4  5  6
```

### itertuples

[`itertuples()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html#pandas.DataFrame.itertuples "pandas.DataFrame.itertuples") 方法返回为 DataFrame 里每行数据生成命名元组的迭代器。该元组的第一个元素是行的索引值，其余的值则是行的值。

示例如下：

```
In [263]: for row in df.itertuples():
   .....:     print(row)
   .....: 
Pandas(Index=0, a=1, b='a')
Pandas(Index=1, a=2, b='b')
Pandas(Index=2, a=3, b='c')
```

该方法不会把行转换为 Series，只是返回命名元组里的值。[`itertuples()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html#pandas.DataFrame.itertuples "pandas.DataFrame.itertuples") 保存值的数据类型，而且比 [`iterrows()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows "pandas.DataFrame.iterrows") 快。

::: tip 注意

包含无效 Python 识别符的列名、重复的列名及以下划线开头的列名，会被重命名为位置名称。如果列数较大，比如大于 255 列，则返回正则元组。

:::

## .dt 访问器

`Series` 提供一个可以简单、快捷地返回 `datetime` 属性值的访问器。这个访问器返回的也是 Series，索引与现有的 Series 一样。

```
# datetime
In [264]: s = pd.Series(pd.date_range('20130101 09:10:12', periods=4))

In [265]: s
Out[265]: 
0   2013-01-01 09:10:12
1   2013-01-02 09:10:12
2   2013-01-03 09:10:12
3   2013-01-04 09:10:12
dtype: datetime64[ns]

In [266]: s.dt.hour
Out[266]: 
0    9
1    9
2    9
3    9
dtype: int64

In [267]: s.dt.second
Out[267]: 
0    12
1    12
2    12
3    12
dtype: int64

In [268]: s.dt.day
Out[268]: 
0    1
1    2
2    3
3    4
dtype: int64
```

用下列表达式进行筛选非常方便：

```
In [269]: s[s.dt.day == 2]
Out[269]: 
1   2013-01-02 09:10:12
dtype: datetime64[ns]
```

时区转换也很轻松：

```
In [270]: stz = s.dt.tz_localize('US/Eastern')

In [271]: stz
Out[271]: 
0   2013-01-01 09:10:12-05:00
1   2013-01-02 09:10:12-05:00
2   2013-01-03 09:10:12-05:00
3   2013-01-04 09:10:12-05:00
dtype: datetime64[ns, US/Eastern]

In [272]: stz.dt.tz
Out[272]: <DstTzInfo 'US/Eastern' LMT-1 day, 19:04:00 STD>
```

可以把这些操作连在一起：

```
In [273]: s.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
Out[273]: 
0   2013-01-01 04:10:12-05:00
1   2013-01-02 04:10:12-05:00
2   2013-01-03 04:10:12-05:00
3   2013-01-04 04:10:12-05:00
dtype: datetime64[ns, US/Eastern]
```

还可以用 [`Series.dt.strftime()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.strftime.html#pandas.Series.dt.strftime "pandas.Series.dt.strftime") 把 `datetime` 的值当成字符串进行格式化，支持与标准 [`strftime()`](https://docs.python.org/3/library/datetime.html#datetime.datetime.strftime "(in Python v3.7)") 同样的格式。

```
# DatetimeIndex
In [274]: s = pd.Series(pd.date_range('20130101', periods=4))

In [275]: s
Out[275]: 
0   2013-01-01
1   2013-01-02
2   2013-01-03
3   2013-01-04
dtype: datetime64[ns]

In [276]: s.dt.strftime('%Y/%m/%d')
Out[276]: 
0    2013/01/01
1    2013/01/02
2    2013/01/03
3    2013/01/04
dtype: object
```

```
# PeriodIndex
In [277]: s = pd.Series(pd.period_range('20130101', periods=4))

In [278]: s
Out[278]: 
0    2013-01-01
1    2013-01-02
2    2013-01-03
3    2013-01-04
dtype: period[D]

In [279]: s.dt.strftime('%Y/%m/%d')
Out[279]: 
0    2013/01/01
1    2013/01/02
2    2013/01/03
3    2013/01/04
dtype: object
```

`.dt` 访问器还支持 `period` 与 `timedelta`。

```
# period
In [280]: s = pd.Series(pd.period_range('20130101', periods=4, freq='D'))

In [281]: s
Out[281]: 
0    2013-01-01
1    2013-01-02
2    2013-01-03
3    2013-01-04
dtype: period[D]

In [282]: s.dt.year
Out[282]: 
0    2013
1    2013
2    2013
3    2013
dtype: int64

In [283]: s.dt.day
Out[283]: 
0    1
1    2
2    3
3    4
dtype: int64
```

```
# timedelta
In [284]: s = pd.Series(pd.timedelta_range('1 day 00:00:05', periods=4, freq='s'))

In [285]: s
Out[285]: 
0   1 days 00:00:05
1   1 days 00:00:06
2   1 days 00:00:07
3   1 days 00:00:08
dtype: timedelta64[ns]

In [286]: s.dt.days
Out[286]: 
0    1
1    1
2    1
3    1
dtype: int64

In [287]: s.dt.seconds
Out[287]: 
0    5
1    6
2    7
3    8
dtype: int64

In [288]: s.dt.components
Out[288]: 
   days  hours  minutes  seconds  milliseconds  microseconds  nanoseconds
0     1      0        0        5             0             0            0
1     1      0        0        6             0             0            0
2     1      0        0        7             0             0            0
3     1      0        0        8             0             0            0
```

::: tip 注意

用这个访问器处理不是 `datetime` 类型的值时，`Series.dt` 会触发 `TypeError` 错误。

:::

## 矢量化字符串方法

Series 支持字符串处理方法，可以非常方便地操作数组里的每个元素。这些方法会自动排除缺失值与空值，这也许是其最重要的特性。这些方法通过 Series 的 `str` 属性访问，一般情况下，这些操作的名称与内置的字符串方法一致。示例如下：

```
In [289]: s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])

In [290]: s.str.lower()
Out[290]: 
0       a
1       b
2       c
3    aaba
4    baca
5     NaN
6    caba
7     dog
8     cat
dtype: object
```

这里还提供了强大的模式匹配方法，但工业注意，模式匹配方法默认使用[正则表达式](https://docs.python.org/3/library/re.html)。

参阅[矢量化字符串方法](https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html#text-string-methods)，了解完整内容。

## 排序

Pandas 支持三种排序方式，按索引标签排序，按列里的值排序，按两种方式混合排序。

### 按索引排序

[`Series.sort_index()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.sort_index.html#pandas.Series.sort_index "pandas.Series.sort_index") 与 [`DataFrame.sort_index()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_index.html#pandas.DataFrame.sort_index "pandas.DataFrame.sort_index") 方法用于按索引层级对 Pandas 对象排序。

```
In [291]: df = pd.DataFrame({
   .....:     'one': pd.Series(np.random.randn(3), index=['a', 'b', 'c']),
   .....:     'two': pd.Series(np.random.randn(4), index=['a', 'b', 'c', 'd']),
   .....:     'three': pd.Series(np.random.randn(3), index=['b', 'c', 'd'])})
   .....: 

In [292]: unsorted_df = df.reindex(index=['a', 'd', 'c', 'b'],
   .....:                          columns=['three', 'two', 'one'])
   .....: 

In [293]: unsorted_df
Out[293]: 
      three       two       one
a       NaN -1.152244  0.562973
d -0.252916 -0.109597       NaN
c  1.273388 -0.167123  0.640382
b -0.098217  0.009797 -1.299504

# DataFrame
In [294]: unsorted_df.sort_index()
Out[294]: 
      three       two       one
a       NaN -1.152244  0.562973
b -0.098217  0.009797 -1.299504
c  1.273388 -0.167123  0.640382
d -0.252916 -0.109597       NaN

In [295]: unsorted_df.sort_index(ascending=False)
Out[295]: 
      three       two       one
d -0.252916 -0.109597       NaN
c  1.273388 -0.167123  0.640382
b -0.098217  0.009797 -1.299504
a       NaN -1.152244  0.562973

In [296]: unsorted_df.sort_index(axis=1)
Out[296]: 
        one     three       two
a  0.562973       NaN -1.152244
d       NaN -0.252916 -0.109597
c  0.640382  1.273388 -0.167123
b -1.299504 -0.098217  0.009797

# Series
In [297]: unsorted_df['three'].sort_index()
Out[297]: 
a         NaN
b   -0.098217
c    1.273388
d   -0.252916
Name: three, dtype: float64
```

### 按值排序

[`Series.sort_values()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.sort_values.html#pandas.Series.sort_values "pandas.Series.sort_values") 方法用于按值对 Series 排序。[`DataFrame.sort_values()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html#pandas.DataFrame.sort_values "pandas.DataFrame.sort_values") 方法用于按行列的值对 DataFrame 排序。[`DataFrame.sort_values()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html#pandas.DataFrame.sort_values "pandas.DataFrame.sort_values") 的可选参数 `by` 用于指定按哪列排序，该参数的值可以是一列或多列数据。

```
In [298]: df1 = pd.DataFrame({'one': [2, 1, 1, 1],
   .....:                     'two': [1, 3, 2, 4],
   .....:                     'three': [5, 4, 3, 2]})
   .....: 

In [299]: df1.sort_values(by='two')
Out[299]: 
   one  two  three
0    2    1      5
2    1    2      3
1    1    3      4
3    1    4      2
```

参数 `by` 支持列名列表，示例如下：

```
In [300]: df1[['one', 'two', 'three']].sort_values(by=['one', 'two'])
Out[300]: 
   one  two  three
2    1    2      3
1    1    3      4
3    1    4      2
0    2    1      5
```

这些方法支持用 `na_position` 参数处理空值。

```
In [301]: s[2] = np.nan

In [302]: s.sort_values()
Out[302]: 
0       A
3    Aaba
1       B
4    Baca
6    CABA
8     cat
7     dog
2     NaN
5     NaN
dtype: object

In [303]: s.sort_values(na_position='first')
Out[303]: 
2     NaN
5     NaN
0       A
3    Aaba
1       B
4    Baca
6    CABA
8     cat
7     dog
dtype: object
```

### 按索引与值排序

*0.23.0 版新增*。

通过参数 `by` 传递给 [`DataFrame.sort_values()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html#pandas.DataFrame.sort_values "pandas.DataFrame.sort_values") 的字符串可以引用列或索引层名。

```
# 创建 MultiIndex
In [304]: idx = pd.MultiIndex.from_tuples([('a', 1), ('a', 2), ('a', 2),
   .....:                                 ('b', 2), ('b', 1), ('b', 1)])
   .....: 

In [305]: idx.names = ['first', 'second']

# 创建 DataFrame
In [306]: df_multi = pd.DataFrame({'A': np.arange(6, 0, -1)},
   .....:                         index=idx)
   .....: 

In [307]: df_multi
Out[307]: 
              A
first second   
a     1       6
      2       5
      2       4
b     2       3
      1       2
      1       1
```

按 `second`（索引）与 `A`（列）排序。 

```
In [308]: df_multi.sort_values(by=['second', 'A'])
Out[308]: 
              A
first second   
b     1       1
      1       2
a     1       6
b     2       3
a     2       4
      2       5
```

::: tip 注意

字符串、列名、索引层名重名时，会触发警告提示，并以列名为准。后期版本中，这种情况将会触发模糊错误。

:::

### 搜索排序

Series 支持 [`searchsorted()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.searchsorted.html#pandas.Series.searchsorted "pandas.Series.searchsorted") 方法，这与[`numpy.ndarray.searchsorted()`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.searchsorted.html#numpy.ndarray.searchsorted "(in NumPy v1.17)") 的操作方式类似。

```
In [309]: ser = pd.Series([1, 2, 3])

In [310]: ser.searchsorted([0, 3])
Out[310]: array([0, 2])

In [311]: ser.searchsorted([0, 4])
Out[311]: array([0, 3])

In [312]: ser.searchsorted([1, 3], side='right')
Out[312]: array([1, 3])

In [313]: ser.searchsorted([1, 3], side='left')
Out[313]: array([0, 2])

In [314]: ser = pd.Series([3, 1, 2])

In [315]: ser.searchsorted([0, 3], sorter=np.argsort(ser))
Out[315]: array([0, 2])
```

### 最大值与最小值

Series 支持 [`nsmallest()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.nsmallest.html#pandas.Series.nsmallest "pandas.Series.nsmallest") 与 [`nlargest()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.nlargest.html#pandas.Series.nlargest "pandas.Series.nlargest") 方法，本方法返回 N 个最大或最小的值。对于数据量大的 `Series` 来说，该方法比先为整个 Series 排序，再调用 `head(n)` 这种方式的速度要快得多。

```
In [316]: s = pd.Series(np.random.permutation(10))

In [317]: s
Out[317]: 
0    2
1    0
2    3
3    7
4    1
5    5
6    9
7    6
8    8
9    4
dtype: int64

In [318]: s.sort_values()
Out[318]: 
1    0
4    1
0    2
2    3
9    4
5    5
7    6
3    7
8    8
6    9
dtype: int64

In [319]: s.nsmallest(3)
Out[319]: 
1    0
4    1
0    2
dtype: int64

In [320]: s.nlargest(3)
Out[320]: 
6    9
8    8
3    7
dtype: int64
```

`DataFrame` 也支持 `nlargest` 与 `nsmallest` 方法。

```
In [321]: df = pd.DataFrame({'a': [-2, -1, 1, 10, 8, 11, -1],
   .....:                    'b': list('abdceff'),
   .....:                    'c': [1.0, 2.0, 4.0, 3.2, np.nan, 3.0, 4.0]})
   .....: 

In [322]: df.nlargest(3, 'a')
Out[322]: 
    a  b    c
5  11  f  3.0
3  10  c  3.2
4   8  e  NaN

In [323]: df.nlargest(5, ['a', 'c'])
Out[323]: 
    a  b    c
5  11  f  3.0
3  10  c  3.2
4   8  e  NaN
2   1  d  4.0
6  -1  f  4.0

In [324]: df.nsmallest(3, 'a')
Out[324]: 
   a  b    c
0 -2  a  1.0
1 -1  b  2.0
6 -1  f  4.0

In [325]: df.nsmallest(5, ['a', 'c'])
Out[325]: 
   a  b    c
0 -2  a  1.0
1 -1  b  2.0
6 -1  f  4.0
2  1  d  4.0
4  8  e  NaN
```

### 用多层索引的列排序

列为多层索引时，可以显式排序，用 `by` 指定所有层级。

```
In [326]: df1.columns = pd.MultiIndex.from_tuples([('a', 'one'),
   .....:                                          ('a', 'two'),
   .....:                                          ('b', 'three')])
   .....: 

In [327]: df1.sort_values(by=('a', 'two'))
Out[327]: 
    a         b
  one two three
0   2   1     5
2   1   2     3
1   1   3     4
3   1   4     2
```

## 复制

在 Pandas 对象上执行 [`copy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.copy.html#pandas.DataFrame.copy "pandas.DataFrame.copy") 方法，将复制底层数据（但不包括轴索引，因为轴索引不可变），并返回一个新的对象。注意，**复制对象这种操作一般来说不是必须的**。比如说，以下几种方式可以***就地（inplace）*** 改变 DataFrame：

* 插入、删除、修改列
* 为 `index` 或 `columns` 属性赋值
* 对于同质数据，用 `values` 属性或高级索引即可直接修改值

注意，用 Pandas 方法修改数据不会带来任何副作用，几乎所有方法都返回新的对象，不会修改原始数据对象。如果原始数据有所改动，唯一的可能就是用户显式指定了要修改原始数据。

## 数据类型

大多数情况下，Pandas 使用 NumPy 数组、Series 或 DataFrame 里某列的数据类型。NumPy 支持 `float`、`int`、`bool`、`timedelta[ns]`、`datetime64[ns]`，注意，NumPy 不支持带时区信息的 `datetime`。

Pandas 与第三方支持库扩充了 NumPy 类型系统，本节只介绍 Pandas 的内部扩展。如需了解如何编写与 Pandas 扩展类型，请参阅[扩展类型](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-extension-types)，参阅[扩展数据类型](https://pandas.pydata.org/pandas-docs/stable/ecosystem.html#ecosystem-extensions)了解第三方支持库提供的扩展类型。

下表列出了 Pandas 扩展类型，参阅列出的文档内容，查看每种类型的详细说明。

|      数据种类       |                           数据类型                           |                             标量                             |                             数组                             |                             文档                             |
| :-----------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|  tz-aware datetime  | [`DatetimeTZDtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeTZDtype.html#pandas.DatetimeTZDtype) | [`Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp) | [`arrays.DatetimeArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.arrays.DatetimeArray.html#pandas.arrays.DatetimeArray) | [Time zone handling](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-timezone) |
|     Categorical     | [`CategoricalDtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.CategoricalDtype.html#pandas.CategoricalDtype) |                             (无)                             | [`Categorical`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Categorical.html#pandas.Categorical) | [Categorical data](https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html#categorical) |
| period (time spans) | [`PeriodDtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.PeriodDtype.html#pandas.PeriodDtype) | [`Period`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Period.html#pandas.Period) | [`arrays.PeriodArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.arrays.PeriodArray.html#pandas.arrays.PeriodArray) | [Time span representation](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-periods) |
|       sparse        | [`SparseDtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.SparseDtype.html#pandas.SparseDtype) |                             (无)                             |                     `arrays.SparseArray`                     | [Sparse data structures](https://pandas.pydata.org/pandas-docs/stable/user_guide/sparse.html#sparse) |
|      intervals      | [`IntervalDtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.IntervalDtype.html#pandas.IntervalDtype) | [`Interval`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Interval.html#pandas.Interval) | [`arrays.IntervalArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.arrays.IntervalArray.html#pandas.arrays.IntervalArray) | [IntervalIndex](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-intervalindex) |
|  nullable integer   | [`Int64Dtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Int64Dtype.html#pandas.Int64Dtype), … |                             (无)                             | [`arrays.IntegerArray`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.arrays.IntegerArray.html#pandas.arrays.IntegerArray) | [Nullable integer data type](https://pandas.pydata.org/pandas-docs/stable/user_guide/integer_na.html#integer-na) |

Pandas 用 `object` 存储字符串。

虽然， `object` 数据类型能够存储任何对象，但应尽量避免这种操作，要了解与其它支持库与方法的性能与交互操作，参阅 [对象转换](https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-object-conversion)。

DataFrame 的 [`dtypes`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dtypes.html#pandas.DataFrame.dtypes "pandas.DataFrame.dtypes") 属性用起来很方便，以 Series 形式返回每列的数据类型。

```
In [328]: dft = pd.DataFrame({'A': np.random.rand(3),
   .....:                     'B': 1,
   .....:                     'C': 'foo',
   .....:                     'D': pd.Timestamp('20010102'),
   .....:                     'E': pd.Series([1.0] * 3).astype('float32'),
   .....:                     'F': False,
   .....:                     'G': pd.Series([1] * 3, dtype='int8')})
   .....: 

In [329]: dft
Out[329]: 
          A  B    C          D    E      F  G
0  0.035962  1  foo 2001-01-02  1.0  False  1
1  0.701379  1  foo 2001-01-02  1.0  False  1
2  0.281885  1  foo 2001-01-02  1.0  False  1

In [330]: dft.dtypes
Out[330]: 
A           float64
B             int64
C            object
D    datetime64[ns]
E           float32
F              bool
G              int8
dtype: object
```

要查看 `Series` 的数据类型，用 [`dtype`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dtype.html#pandas.Series.dtype "pandas.Series.dtype") 属性。

```
In [331]: dft['A'].dtype
Out[331]: dtype('float64')
```

Pandas 对象单列中含多种类型的数据时，该列的数据类型为可适配于各类数据的数据类型，通常为 `object`。

```
# 整数被强制转换为浮点数
In [332]: pd.Series([1, 2, 3, 4, 5, 6.])
Out[332]: 
0    1.0
1    2.0
2    3.0
3    4.0
4    5.0
5    6.0
dtype: float64

# 字符串数据决定了该 Series 的数据类型为 ``object``
In [333]: pd.Series([1, 2, 3, 6., 'foo'])
Out[333]: 
0      1
1      2
2      3
3      6
4    foo
dtype: object
```

`DataFrame.dtypes.value_counts()` 用于统计 DataFrame 里不同数据类型的列数。

```
In [334]: dft.dtypes.value_counts()
Out[334]: 
float32           1
object            1
bool              1
int8              1
float64           1
datetime64[ns]    1
int64             1
dtype: int64
```

多种数值型数据类型可以在 DataFrame 里共存。如果只传递一种数据类型，不论是通过 `dtype` 关键字直接传递，还是通过 `ndarray` 或 `Series` 传递，都会保存至 DataFrame 操作。此外，不同数值型数据类型**不会**合并。示例如下：

```
In [335]: df1 = pd.DataFrame(np.random.randn(8, 1), columns=['A'], dtype='float32')

In [336]: df1
Out[336]: 
          A
0  0.224364
1  1.890546
2  0.182879
3  0.787847
4 -0.188449
5  0.667715
6 -0.011736
7 -0.399073

In [337]: df1.dtypes
Out[337]: 
A    float32
dtype: object

In [338]: df2 = pd.DataFrame({'A': pd.Series(np.random.randn(8), dtype='float16'),
   .....:                     'B': pd.Series(np.random.randn(8)),
   .....:                     'C': pd.Series(np.array(np.random.randn(8),
   .....:                                             dtype='uint8'))})
   .....: 

In [339]: df2
Out[339]: 
          A         B    C
0  0.823242  0.256090    0
1  1.607422  1.426469    0
2 -0.333740 -0.416203  255
3 -0.063477  1.139976    0
4 -1.014648 -1.193477    0
5  0.678711  0.096706    0
6 -0.040863 -1.956850    1
7 -0.357422 -0.714337    0

In [340]: df2.dtypes
Out[340]: 
A    float16
B    float64
C      uint8
dtype: object
```

### 默认值

整数的默认类型为 `int64`，浮点数的默认类型为 `float64`，这里的默认值与系统平台无关，不管是 32 位系统，还是 64 位系统都是一样的。下列代码返回的结果都是 `int64`：

```
In [341]: pd.DataFrame([1, 2], columns=['a']).dtypes
Out[341]: 
a    int64
dtype: object

In [342]: pd.DataFrame({'a': [1, 2]}).dtypes
Out[342]: 
a    int64
dtype: object

In [343]: pd.DataFrame({'a': 1}, index=list(range(2))).dtypes
Out[343]: 
a    int64
dtype: object
```

注意，NumPy 创建数组时，会根据系统选择类型。下列代码在 32 位系统上**将**返回 `int32`。

```
In [344]: frame = pd.DataFrame(np.array([1, 2]))
```

### 向上转型

与其它类型合并时，用的是向上转型，指的是从现有类型转换为另一种类型，如`int` 变为 `float`。

```
In [345]: df3 = df1.reindex_like(df2).fillna(value=0.0) + df2

In [346]: df3
Out[346]: 
          A         B      C
0  1.047606  0.256090    0.0
1  3.497968  1.426469    0.0
2 -0.150862 -0.416203  255.0
3  0.724370  1.139976    0.0
4 -1.203098 -1.193477    0.0
5  1.346426  0.096706    0.0
6 -0.052599 -1.956850    1.0
7 -0.756495 -0.714337    0.0

In [347]: df3.dtypes
Out[347]: 
A    float32
B    float64
C    float64
dtype: object
```

[`DataFrame.to_numpy()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_numpy.html#pandas.DataFrame.to_numpy "pandas.DataFrame.to_numpy") 返回多个数据类型里**用得最多的数据类型**，这里指的是，输出结果的数据类型，适用于所有同构 NumPy 数组的数据类型。此处强制执行**向上转型**。

```
In [348]: df3.to_numpy().dtype
Out[348]: dtype('float64')
```

### astype

[`astype()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html#pandas.DataFrame.astype "pandas.DataFrame.astype") 方法显式地把一种数据类型转换为另一种，默认操作为复制数据，就算数据类型没有改变也会复制数据，`copy=False` 改变默认操作模式。此外，`astype` 无效时，会触发异常。

向上转型一般都遵循 **NumPy** 规则。操作中含有两种不同类型的数据时，返回更为通用的那种数据类型。

```
In [349]: df3
Out[349]: 
          A         B      C
0  1.047606  0.256090    0.0
1  3.497968  1.426469    0.0
2 -0.150862 -0.416203  255.0
3  0.724370  1.139976    0.0
4 -1.203098 -1.193477    0.0
5  1.346426  0.096706    0.0
6 -0.052599 -1.956850    1.0
7 -0.756495 -0.714337    0.0

In [350]: df3.dtypes
Out[350]: 
A    float32
B    float64
C    float64
dtype: object

# 转换数据类型
In [351]: df3.astype('float32').dtypes
Out[351]: 
A    float32
B    float32
C    float32
dtype: object
```

用 [`astype()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html#pandas.DataFrame.astype "pandas.DataFrame.astype") 把一列或多列转换为指定类型 。

```
In [352]: dft = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})

In [353]: dft[['a', 'b']] = dft[['a', 'b']].astype(np.uint8)

In [354]: dft
Out[354]: 
   a  b  c
0  1  4  7
1  2  5  8
2  3  6  9

In [355]: dft.dtypes
Out[355]: 
a    uint8
b    uint8
c    int64
dtype: object
```
*0.19.0 版新增。*

[`astype()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html#pandas.DataFrame.astype "pandas.DataFrame.astype") 通过字典指定哪些列转换为哪些类型。

```
In [356]: dft1 = pd.DataFrame({'a': [1, 0, 1], 'b': [4, 5, 6], 'c': [7, 8, 9]})

In [357]: dft1 = dft1.astype({'a': np.bool, 'c': np.float64})

In [358]: dft1
Out[358]: 
       a  b    c
0   True  4  7.0
1  False  5  8.0
2   True  6  9.0

In [359]: dft1.dtypes
Out[359]: 
a       bool
b      int64
c    float64
dtype: object
```

::: tip 注意

用 [`astype()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html#pandas.DataFrame.astype "pandas.DataFrame.astype") 与 [`loc()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html#pandas.DataFrame.loc "pandas.DataFrame.loc") 为部分列转换指定类型时，会发生向上转型。

[`loc()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html#pandas.DataFrame.loc "pandas.DataFrame.loc") 尝试分配当前的数据类型，而 `[]` 则会从右方获取数据类型并进行覆盖。因此，下列代码会产出意料之外的结果：

```
In [360]: dft = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})

In [361]: dft.loc[:, ['a', 'b']].astype(np.uint8).dtypes
Out[361]: 
a    uint8
b    uint8
dtype: object

In [362]: dft.loc[:, ['a', 'b']] = dft.loc[:, ['a', 'b']].astype(np.uint8)

In [363]: dft.dtypes
Out[363]: 
a    int64
b    int64
c    int64
dtype: object
```

:::

### 对象转换

Pandas 提供了多种函数可以把 `object` 从一种类型强制转为另一种类型。这是因为，数据有时存储的是正确类型，但在保存时却存成了 `object` 类型，此时，用 [`DataFrame.infer_objects()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.infer_objects.html#pandas.DataFrame.infer_objects "pandas.DataFrame.infer_objects") 与 [`Series.infer_objects()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.infer_objects.html#pandas.Series.infer_objects "pandas.Series.infer_objects") 方法即可把数据**软**转换为正确的类型。

```
In [364]: import datetime

In [365]: df = pd.DataFrame([[1, 2],
   .....:                    ['a', 'b'],
   .....:                    [datetime.datetime(2016, 3, 2),
   .....:                     datetime.datetime(2016, 3, 2)]])
   .....: 

In [366]: df = df.T

In [367]: df
Out[367]: 
   0  1          2
0  1  a 2016-03-02
1  2  b 2016-03-02

In [368]: df.dtypes
Out[368]: 
0            object
1            object
2    datetime64[ns]
dtype: object
```

因为数据被转置，所以把原始列的数据类型改成了 `object`，但使用 `infer_objects` 后就变正确了。

```
In [369]: df.infer_objects().dtypes
Out[369]: 
0             int64
1            object
2    datetime64[ns]
dtype: object
```

下列函数可以应用于一维数组与标量，执行硬转换，把对象转换为指定类型。

* [`to_numeric()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_numeric.html#pandas.to_numeric "pandas.to_numeric")，转换为数值型


```
In [370]: m = ['1.1', 2, 3]

In [371]: pd.to_numeric(m)
Out[371]: array([1.1, 2. , 3. ])
```
* [`to_datetime()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime "pandas.to_datetime")，转换为 `datetime` 对象

```
In [372]: import datetime

In [373]: m = ['2016-07-09', datetime.datetime(2016, 3, 2)]

In [374]: pd.to_datetime(m)
Out[374]: DatetimeIndex(['2016-07-09', '2016-03-02'], dtype='datetime64[ns]', freq=None)
```

* [`to_timedelta()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html#pandas.to_timedelta "pandas.to_timedelta")，转换为 `timedelta` 对象。


```
In [375]: m = ['5us', pd.Timedelta('1day')]

In [376]: pd.to_timedelta(m)
Out[376]: TimedeltaIndex(['0 days 00:00:00.000005', '1 days 00:00:00'], dtype='timedelta64[ns]', freq=None)
```

如需强制转换，则要加入 `error` 参数，指定 Pandas 怎样处理不能转换为成预期类型或对象的数据。`errors` 参数的默认值为 `False`，指的是在转换过程中，遇到任何问题都触发错误。设置为 `errors='coerce'` 时，pandas 会忽略错误，强制把问题数据转换为 `pd.NaT`（`datetime` 与 `timedelta`），或 `np.nan`（数值型）。读取数据时，如果大部分要转换的数据是数值型或 `datetime`，这种操作非常有用，但偶尔也会有非制式数据混合在一起，可能会导致展示数据缺失：
```
In [377]: import datetime

In [378]: m = ['apple', datetime.datetime(2016, 3, 2)]

In [379]: pd.to_datetime(m, errors='coerce')
Out[379]: DatetimeIndex(['NaT', '2016-03-02'], dtype='datetime64[ns]', freq=None)

In [380]: m = ['apple', 2, 3]

In [381]: pd.to_numeric(m, errors='coerce')
Out[381]: array([nan,  2.,  3.])

In [382]: m = ['apple', pd.Timedelta('1day')]

In [383]: pd.to_timedelta(m, errors='coerce')
Out[383]: TimedeltaIndex([NaT, '1 days'], dtype='timedelta64[ns]', freq=None)
```

`error` 参数还有第三个选项，`error='ignore'`。转换数据时会忽略错误，直接输出问题数据：

```
In [384]: import datetime

In [385]: m = ['apple', datetime.datetime(2016, 3, 2)]

In [386]: pd.to_datetime(m, errors='ignore')
Out[386]: Index(['apple', 2016-03-02 00:00:00], dtype='object')

In [387]: m = ['apple', 2, 3]

In [388]: pd.to_numeric(m, errors='ignore')
Out[388]: array(['apple', 2, 3], dtype=object)

In [389]: m = ['apple', pd.Timedelta('1day')]

In [390]: pd.to_timedelta(m, errors='ignore')
Out[390]: array(['apple', Timedelta('1 days 00:00:00')], dtype=object)
```

执行转换操作时，[`to_numeric()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_numeric.html#pandas.to_numeric "pandas.to_numeric") 还有一个参数，`downcast`，即向下转型，可以把数值型转换为减少内存占用的数据类型：

```
In [391]: m = ['1', 2, 3]

In [392]: pd.to_numeric(m, downcast='integer')   # smallest signed int dtype
Out[392]: array([1, 2, 3], dtype=int8)

In [393]: pd.to_numeric(m, downcast='signed')    # same as 'integer'
Out[393]: array([1, 2, 3], dtype=int8)

In [394]: pd.to_numeric(m, downcast='unsigned')  # smallest unsigned int dtype
Out[394]: array([1, 2, 3], dtype=uint8)

In [395]: pd.to_numeric(m, downcast='float')     # smallest float dtype
Out[395]: array([1., 2., 3.], dtype=float32)
```

上述方法仅能应用于一维数组、列表或标量；不能直接用于 DataFrame 等多维对象。不过，用 [`apply()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html#pandas.DataFrame.apply "pandas.DataFrame.apply")，可以快速为每列应用函数：

```
In [396]: import datetime

In [397]: df = pd.DataFrame([
   .....:     ['2016-07-09', datetime.datetime(2016, 3, 2)]] * 2, dtype='O')
   .....: 

In [398]: df
Out[398]: 
            0                    1
0  2016-07-09  2016-03-02 00:00:00
1  2016-07-09  2016-03-02 00:00:00

In [399]: df.apply(pd.to_datetime)
Out[399]: 
           0          1
0 2016-07-09 2016-03-02
1 2016-07-09 2016-03-02

In [400]: df = pd.DataFrame([['1.1', 2, 3]] * 2, dtype='O')

In [401]: df
Out[401]: 
     0  1  2
0  1.1  2  3
1  1.1  2  3

In [402]: df.apply(pd.to_numeric)
Out[402]: 
     0  1  2
0  1.1  2  3
1  1.1  2  3

In [403]: df = pd.DataFrame([['5us', pd.Timedelta('1day')]] * 2, dtype='O')

In [404]: df
Out[404]: 
     0                1
0  5us  1 days 00:00:00
1  5us  1 days 00:00:00

In [405]: df.apply(pd.to_timedelta)
Out[405]: 
                0      1
0 00:00:00.000005 1 days
1 00:00:00.000005 1 days
```

### 各种坑

对 `integer` 数据执行选择操作时，可以很轻而易举地把数据转换为 `floating` 。Pandas 会保存输入数据的数据类型，以防未引入 `nans` 的情况。参阅 [对整数 NA 空值的支持](https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#gotchas-intna)。

```
In [406]: dfi = df3.astype('int32')

In [407]: dfi['E'] = 1

In [408]: dfi
Out[408]: 
   A  B    C  E
0  1  0    0  1
1  3  1    0  1
2  0  0  255  1
3  0  1    0  1
4 -1 -1    0  1
5  1  0    0  1
6  0 -1    1  1
7  0  0    0  1

In [409]: dfi.dtypes
Out[409]: 
A    int32
B    int32
C    int32
E    int64
dtype: object

In [410]: casted = dfi[dfi > 0]

In [411]: casted
Out[411]: 
     A    B      C  E
0  1.0  NaN    NaN  1
1  3.0  1.0    NaN  1
2  NaN  NaN  255.0  1
3  NaN  1.0    NaN  1
4  NaN  NaN    NaN  1
5  1.0  NaN    NaN  1
6  NaN  NaN    1.0  1
7  NaN  NaN    NaN  1

In [412]: casted.dtypes
Out[412]: 
A    float64
B    float64
C    float64
E      int64
dtype: object
```

浮点数类型未改变。

```
In [413]: dfa = df3.copy()

In [414]: dfa['A'] = dfa['A'].astype('float32')

In [415]: dfa.dtypes
Out[415]: 
A    float32
B    float64
C    float64
dtype: object

In [416]: casted = dfa[df2 > 0]

In [417]: casted
Out[417]: 
          A         B      C
0  1.047606  0.256090    NaN
1  3.497968  1.426469    NaN
2       NaN       NaN  255.0
3       NaN  1.139976    NaN
4       NaN       NaN    NaN
5  1.346426  0.096706    NaN
6       NaN       NaN    1.0
7       NaN       NaN    NaN

In [418]: casted.dtypes
Out[418]: 
A    float32
B    float64
C    float64
dtype: object
```

## 基于 `dtype` 选择列

[`select_dtypes()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html#pandas.DataFrame.select_dtypes "pandas.DataFrame.select_dtypes") 方法基于 `dtype` 选择列。

首先，创建一个由多种数据类型组成的 DataFrame：


```
In [419]: df = pd.DataFrame({'string': list('abc'),
   .....:                    'int64': list(range(1, 4)),
   .....:                    'uint8': np.arange(3, 6).astype('u1'),
   .....:                    'float64': np.arange(4.0, 7.0),
   .....:                    'bool1': [True, False, True],
   .....:                    'bool2': [False, True, False],
   .....:                    'dates': pd.date_range('now', periods=3),
   .....:                    'category': pd.Series(list("ABC")).astype('category')})
   .....: 

In [420]: df['tdeltas'] = df.dates.diff()

In [421]: df['uint64'] = np.arange(3, 6).astype('u8')

In [422]: df['other_dates'] = pd.date_range('20130101', periods=3)

In [423]: df['tz_aware_dates'] = pd.date_range('20130101', periods=3, tz='US/Eastern')

In [424]: df
Out[424]: 
  string  int64  uint8  float64  bool1  bool2                      dates category tdeltas  uint64 other_dates            tz_aware_dates
0      a      1      3      4.0   True  False 2019-08-22 15:49:01.870038        A     NaT       3  2013-01-01 2013-01-01 00:00:00-05:00
1      b      2      4      5.0  False   True 2019-08-23 15:49:01.870038        B  1 days       4  2013-01-02 2013-01-02 00:00:00-05:00
2      c      3      5      6.0   True  False 2019-08-24 15:49:01.870038        C  1 days       5  2013-01-03 2013-01-03 00:00:00-05:00
```

该 DataFrame 的数据类型：

```
In [425]: df.dtypes
Out[425]: 
string                                object
int64                                  int64
uint8                                  uint8
float64                              float64
bool1                                   bool
bool2                                   bool
dates                         datetime64[ns]
category                            category
tdeltas                      timedelta64[ns]
uint64                                uint64
other_dates                   datetime64[ns]
tz_aware_dates    datetime64[ns, US/Eastern]
dtype: object
```

[`select_dtypes()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html#pandas.DataFrame.select_dtypes "pandas.DataFrame.select_dtypes") 有两个参数，`include` 与 `exclude`，用于实现“提取这些数据类型的列” （`include`）或 “提取不是这些数据类型的列”（`exclude`）。

选择 `bool` 型的列，示例如下：
```
In [426]: df.select_dtypes(include=[bool])
Out[426]: 
   bool1  bool2
0   True  False
1  False   True
2   True  False
```

该方法还支持输入 [NumPy 数据类型](https://docs.scipy.org/doc/numpy/reference/arrays.scalars.html)的名称：

```
In [427]: df.select_dtypes(include=['bool'])
Out[427]: 
   bool1  bool2
0   True  False
1  False   True
2   True  False
```
[`select_dtypes()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.select_dtypes.html#pandas.DataFrame.select_dtypes "pandas.DataFrame.select_dtypes") 还支持通用数据类型。

比如，选择所有数值型与布尔型的列，同时，排除无符号整数：

```
In [428]: df.select_dtypes(include=['number', 'bool'], exclude=['unsignedinteger'])
Out[428]: 
   int64  float64  bool1  bool2 tdeltas
0      1      4.0   True  False     NaT
1      2      5.0  False   True  1 days
2      3      6.0   True  False  1 days
```

选择字符串型的列必须要用 `object`：

```
In [429]: df.select_dtypes(include=['object'])
Out[429]: 
  string
0      a
1      b
2      c
```

要查看 `numpy.number` 等通用 `dtype` 的所有子类型，可以定义一个函数，返回子类型树：

```
In [430]: def subdtypes(dtype):
   .....:     subs = dtype.__subclasses__()
   .....:     if not subs:
   .....:         return dtype
   .....:     return [dtype, [subdtypes(dt) for dt in subs]]
   .....: 
```

所有 NumPy 数据类型都是 `numpy.generic` 的子类：

```
In [431]: subdtypes(np.generic)
Out[431]: 
[numpy.generic,
 [[numpy.number,
   [[numpy.integer,
     [[numpy.signedinteger,
       [numpy.int8,
        numpy.int16,
        numpy.int32,
        numpy.int64,
        numpy.int64,
        numpy.timedelta64]],
      [numpy.unsignedinteger,
       [numpy.uint8,
        numpy.uint16,
        numpy.uint32,
        numpy.uint64,
        numpy.uint64]]]],
    [numpy.inexact,
     [[numpy.floating,
       [numpy.float16, numpy.float32, numpy.float64, numpy.float128]],
      [numpy.complexfloating,
       [numpy.complex64, numpy.complex128, numpy.complex256]]]]]],
  [numpy.flexible,
   [[numpy.character, [numpy.bytes_, numpy.str_]],
    [numpy.void, [numpy.record]]]],
  numpy.bool_,
  numpy.datetime64,
  numpy.object_]]
```

**tip 注意: Pandas 支持 `category` 与 `datetime64[ns, tz]` 类型，但这两种类型未整合到 NumPy 架构，因此，上面的函数没有显示。**
