# [AKShare](https://github.com/akfamily/akshare) 贡献源码

## 贡献指南

### 克隆及提交代码

1. 请从 [akshare-dev 分支](https://github.com/akfamily/akshare/tree/dev) 克隆，dev 分支中包含 AKShare 最新的开发代码
2. 请提交修改后的代码到 [akshare-dev 分支](https://github.com/akfamily/akshare/tree/dev)

### 代码及接口设计规范

1. 代码需要符合 **PEP 8** 要求，请使用 [Ruff](https://github.com/astral-sh/ruff) 格式化代码
2. 请使用 [pre-commit](https://pre-commit.com/) 来规范 git 提交记录，可以参考 [AKShare](https://github.com/akfamily/akshare) 的格式
3. 函数接口的设计 **stock_zh_a_hist_sina** 结构，其中 **stock** 为金融产品，**zh** 为国家或地区，**a** 为市场或品种，**hist** 为 history 的缩写表示历史数据，**sina** 表示数据源为新浪
4. 接口函数需要增加注释，注释规则请参考 **stock_zh_a_hist_sina** 接口的源码
5. 需要在接口函数的注释中增加目标网站的地址（不是具体的数据接口地址，而是网页的地址）
6. 返回数据格式要求：
   1. 为了兼容 HTTP API 接口，所有返回的数据格式统一为 Pandas 中的 pandas.DataFrame 格式

### 文档撰写规范

1. 在新增或者修改接口后，需要修改相对应的接口文档，保持接口与文档的同步更新；
2. 具体的接口文档路径（以股票接口的文档为例）为：akshare->docs->data->stock->stock.md，其中 stock 表示股票文件夹，stock.md 为具体的 Markdown 文件，需要在 stock.md 中对相应的接口文档进行修改或新增；
3. 以股票分时数据接口文档为例：
   1. 主要包含以下部分内容：
      1. 接口：填写具体的接口名称
      2. 目标地址：填写具体数据获取网页的地址（不是数据接口地址）
      3. 描述：简单描述数据接口获取的数据
      4. 限量：返回数据的情况
      5. 输入参数：数据接口函数中需要输入的参数
      6. 输出参数：返回数据的字段，这里需要填写返回数据的字段和类型
      7. 接口示例：Python 调用该数据接口的代码
      8. 数据示例：利用 **接口示例** 代码获取的数据的接口，这里只需要复制前 **5** 行和后 **5** 行数据即刻即可。

   2. 示例如下：

    ```shell
      ##### 分时数据

      接口: stock_zh_a_minute

      目标地址: https://finance.sina.com.cn/realstock/company/sh600519/nc.shtml

      描述: 新浪财经获取分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率

      限量: 单次返回指定公司的指定频率的所有历史分时行情数据

      输入参数

      \```
      | 名称   | 类型 |  描述|
      | -------- | ---- |  --- |
      | symbol | str  | symbol='sh000300'; 同日频率数据接口|
      | period | str  | period='1'; 获取 1, 5, 15, 30, 60 分钟的数据频率|
      \```

      输出参数

      \```shell
      | 名称           | 类型        |  描述   |
      | ------------  | ------      |  -------- |
      | day           | object   |  -     |
      | open          | float64      |  -     |
      | high          | float64      |  -     |
      | low           | float64      |  -     |
      | close         | float64      |  -     |
      | volume        | float64      |  -     |
      | ma_price5     | float64      |  -     |
      | ma_volume5    | float64      |  -     |
      | ma_price10    | float64      |  -     |
      | ma_volume10   | float64      |  -     |
      | ma_price30    | float64      |  -     |
      | ma_volume30   | float64      |  -     |
      \```

      接口示例

      \```python
      import akshare as ak

      stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sz000876', period='1', adjust="qfq")
      print(stock_zh_a_minute_df)
      \```

      数据示例

      \```
                             day  open  high   low  close  volume
       0     2024-04-22 13:53:00  9.30  9.31  9.30   9.30   90000
       1     2024-04-22 13:54:00  9.30  9.31  9.29   9.30   96100
       2     2024-04-22 13:55:00  9.30  9.32  9.30   9.32   89200
       3     2024-04-22 13:56:00  9.32  9.32  9.31   9.31   46300
       4     2024-04-22 13:57:00  9.31  9.32  9.31   9.32   18000
       ...                   ...   ...   ...   ...    ...     ...
       1965  2024-05-07 14:54:00   NaN   NaN   NaN    NaN  129300
       1966  2024-05-07 14:55:00   NaN   NaN   NaN    NaN  116100
       1967  2024-05-07 14:56:00   NaN   NaN   NaN    NaN  111300
       1968  2024-05-07 14:57:00   NaN   NaN   NaN    NaN   74400
       1969  2024-05-07 15:00:00   NaN   NaN   NaN    NaN  305000
       [1970 rows x 6 columns]
      \```
    ```

## 声明

1. 所提交的代码如不符合上述规范，则可能会被拒绝合并；
2. 由于某些原因，您所提交的代码、数据接口和文档会被修改、删除或被第三方使用；
3. **输出参数**里面的字段类型必须为 Pandas 最新版本的 int64 类型，float64 类型，object 类型等三种类型之一，整数为 int64 类型，浮点数为 float64 类型，日期及字符串为 object 类型。
