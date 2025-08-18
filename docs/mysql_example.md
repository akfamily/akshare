# MySQL 数据库存储功能使用说明

## 简介

AKShare 现在支持将获取到的金融数据保存到 MySQL 数据库中，方便用户进行数据持久化和进一步分析。

## 安装依赖

在使用数据库功能前，请确保安装了相关依赖：

```bash
pip install akshare pymysql sqlalchemy
```

或者直接安装 AKShare（已包含依赖）：

```bash
pip install akshare --upgrade
```

## 使用示例

### 1. 保存数据到 MySQL

```python
import akshare as ak
from akshare.utils.db import save_to_mysql

# 获取股票数据
stock_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")

# 保存到 MySQL 数据库
success = save_to_mysql(
    df=stock_df,
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare"
)

if success:
    print("数据保存成功")
else:
    print("数据保存失败")
```

### 2. 从 MySQL 读取数据

```python
from akshare.utils.db import read_from_mysql

# 从 MySQL 数据库读取数据
df = read_from_mysql(
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare"
)

if df is not None:
    print(df.head())
else:
    print("数据读取失败")
```

### 3. 使用字段映射功能

当需要将数据库中的字段名映射回原始字段名时，可以使用 `column_mapping` 参数：

```python
import akshare as ak
from akshare.utils.db import save_to_mysql, read_from_mysql

# 获取股票数据
stock_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")

# 定义字段映射关系（原始字段名 -> 数据库字段名）
column_mapping = {
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount"
}

# 保存到 MySQL 数据库（使用字段映射）
success = save_to_mysql(
    df=stock_df,
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare",
    column_mapping=column_mapping
)

# 定义反向映射关系（数据库字段名 -> 原始字段名）
reverse_mapping = {v: k for k, v in column_mapping.items()}

# 从 MySQL 数据库读取数据（使用字段映射）
df = read_from_mysql(
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare",
    column_mapping=reverse_mapping  # 映射回原始字段名
)

if df is not None:
    print(df.head())
else:
    print("数据读取失败")
```

### 4. 使用字段备注功能

可以为数据库表的字段添加备注信息：

```python
import akshare as ak
from akshare.utils.db import save_to_mysql

# 获取股票数据
stock_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")

# 定义字段备注
column_comments = {
    "日期": "交易日期",
    "开盘": "开盘价格",
    "收盘": "收盘价格",
    "最高": "最高价格",
    "最低": "最低价格",
    "成交量": "成交数量",
    "成交额": "成交金额"
}

# 保存到 MySQL 数据库（使用字段备注）
success = save_to_mysql(
    df=stock_df,
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare",
    column_comments=column_comments
)

if success:
    print("数据保存成功，并添加了字段备注")
else:
    print("数据保存失败")
```

### 5. 获取字段备注

可以从数据库中获取已有的字段备注信息：

```python
from akshare.utils.db import get_column_comments

# 获取表的字段备注
comments = get_column_comments(
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare"
)

if comments:
    for column, comment in comments.items():
        print(f"{column}: {comment}")
else:
    print("未找到字段备注或获取失败")
```

### 6. 综合使用示例

结合字段映射和字段备注功能：

```python
import akshare as ak
from akshare.utils.db import save_to_mysql, read_from_mysql, get_column_comments

# 获取股票数据
stock_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")

# 定义字段映射关系（原始字段名 -> 数据库字段名）
column_mapping = {
    "日期": "trade_date",
    "开盘": "open_price",
    "收盘": "close_price",
    "最高": "high_price",
    "最低": "low_price",
    "成交量": "volume",
    "成交额": "amount"
}

# 定义字段备注
column_comments = {
    "trade_date": "交易日期",
    "open_price": "开盘价格",
    "close_price": "收盘价格",
    "high_price": "最高价格",
    "low_price": "最低价格",
    "volume": "成交数量",
    "amount": "成交金额"
}

# 保存到 MySQL 数据库（同时使用字段映射和字段备注）
success = save_to_mysql(
    df=stock_df,
    table_name="stock_000001_daily",
    host="localhost",
    port=3306,
    user="root",
    password="your_password",
    database="akshare",
    column_mapping=column_mapping,
    column_comments=column_comments
)

if success:
    print("数据保存成功，并添加了字段映射和备注")
    
    # 获取字段备注
    comments = get_column_comments(
        table_name="stock_000001_daily",
        host="localhost",
        port=3306,
        user="root",
        password="your_password",
        database="akshare"
    )
    
    if comments:
        print("\n字段备注信息：")
        for column, comment in comments.items():
            print(f"  {column}: {comment}")
else:
    print("数据保存失败")
```

## 参数说明

### save_to_mysql 参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| df | pd.DataFrame | - | 要保存的数据 |
| table_name | str | - | 数据库表名 |
| host | str | localhost | MySQL 主机地址 |
| port | int | 3306 | MySQL 端口号 |
| user | str | root | MySQL 用户名 |
| password | str | '' | MySQL 密码 |
| database | str | akshare | MySQL 数据库名 |
| if_exists | str | replace | 表存在时的处理方式 |
| column_mapping | dict | None | 列名映射字典，键为原始列名，值为数据库列名 |
| column_comments | dict | None | 列注释字典，键为列名，值为注释内容 |

`if_exists` 参数可选值：
- `fail`: 如果表存在则抛出异常
- `replace`: 如果表存在则替换
- `append`: 如果表存在则追加数据

### read_from_mysql 参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| table_name | str | - | 数据库表名 |
| host | str | localhost | MySQL 主机地址 |
| port | int | 3306 | MySQL 端口号 |
| user | str | root | MySQL 用户名 |
| password | str | '' | MySQL 密码 |
| database | str | akshare | MySQL 数据库名 |
| column_mapping | dict | None | 列名映射字典，键为数据库列名，值为原始列名 |

### get_column_comments 参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| table_name | str | - | 数据库表名 |
| host | str | localhost | MySQL 主机地址 |
| port | int | 3306 | MySQL 端口号 |
| user | str | root | MySQL 用户名 |
| password | str | '' | MySQL 密码 |
| database | str | akshare | MySQL 数据库名 |

## 注意事项

1. 请确保 MySQL 服务正在运行
2. 请确保数据库用户有足够的权限访问指定数据库
3. 如果数据库不存在，请先创建数据库
4. 表名会自动根据 `table_name` 参数创建或替换
5. 日期等特殊字段会自动转换为适合数据库存储的格式
6. 使用字段映射功能时，确保映射字典的键值对应正确
7. 字段备注功能需要数据库用户具有 ALTER 权限
8. 字段备注仅支持 MySQL 数据库

## 常见问题

### 1. 连接失败

请检查以下几点：
- MySQL 服务是否启动
- 主机地址、端口是否正确
- 用户名、密码是否正确
- 数据库是否允许远程连接（如果非本地连接）

### 2. 权限不足

请确保使用的数据库用户具有以下权限：
- 对目标数据库的读写权限
- 创建表的权限（如果表不存在）
- ALTER 权限（如果需要添加字段备注）

### 3. 数据类型问题

如果遇到数据类型转换问题，可以先对数据进行预处理：
```python
# 示例：转换数据类型
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
```