## [AKShare](https://github.com/akfamily/akshare) 迁徙数据

### 迁徙数据-百度

#### 迁入与迁出地详情

接口: migration_area_baidu

目标地址: https://qianxi.baidu.com/?from=shoubai#city=0

描述: 百度-百度地图慧眼-百度迁徙-迁入/迁出地数据接口

限量: 单次返回前 100 个城市的数据

输入参数

| 名称        | 类型  | 描述                                                          |
|-----------|-----|-------------------------------------------------------------|
| area      | str | area="乌鲁木齐市", 输入需要查询的省份或者城市, 都需要用全称, 比如: "浙江省", "乌鲁木齐市"     |
| indicator | str | indicator="move_in", 返回迁入地详情, indicator="move_out", 返回迁出地详情 |
| date      | str | date="20230922", 需要滞后一天                                     |

输出参数

| 名称            | 类型      | 描述       |
|---------------|---------|----------|
| city_name     | object  | 城市名称     |
| province_name | object  | 所属省份     |
| value         | float64 | 迁徙规模, 比例 |

接口示例

```python
import akshare as ak

migration_area_baidu_df = ak.migration_area_baidu(area="重庆市", indicator="move_in", date="20230922")
print(migration_area_baidu_df)
```

数据示例

```
     city_name province_name  value
0          苏州市           江苏省  24.43
1          嘉兴市           浙江省   6.46
2          杭州市           浙江省   5.09
3          南通市           江苏省   4.94
4          无锡市           江苏省   3.90
..         ...           ...    ...
95         淄博市           山东省   0.10
96  恩施土家族苗族自治州           湖北省   0.10
97         惠州市           广东省   0.10
98         汕头市           广东省   0.10
99     大理白族自治州           云南省   0.10
[100 rows x 3 columns]
```

#### 迁徙规模

接口: migration_scale_baidu

目标地址: https://qianxi.baidu.com/?from=shoubai#city=0

描述: 百度-百度地图慧眼-百度迁徙-迁徙规模

- 迁徙规模指数：反映迁入或迁出人口规模，城市间可横向对比
- 城市迁徙边界采用该城市行政区划，包含该城市管辖的区、县、乡、村

限量: 单次返回所有迁徙规模数据

输入参数

| 名称        | 类型  | 描述                                                          |
|-----------|-----|-------------------------------------------------------------|
| area      | str | area="广州市", 输入需要查询的省份或者城市, 都需要用全称, 比如: "浙江省", "乌鲁木齐市"       |
| indicator | str | indicator="move_in", 返回迁入地详情, indicator="move_out", 返回迁出地详情 |

输出参数

| 名称     | 类型      | 描述     |
|--------|---------|--------|
| 日期     | object  | -      |
| 迁徙规模指数 | float64 | 定义参见百度 |

接口示例

```python
import akshare as ak

migration_scale_baidu_df = ak.migration_scale_baidu(area="广州市", indicator="move_in")
print(migration_scale_baidu_df)
```

数据示例

```
         日期     迁徙规模指数
0     2019-01-12   8.413535
1     2019-01-13   7.877218
2     2019-01-14   8.920660
3     2019-01-15   7.426858
4     2019-01-16   7.339183
          ...        ...
1100  2023-09-18  13.620539
1101  2023-09-19   9.761666
1102  2023-09-20   9.755867
1103  2023-09-21  10.397938
1104  2023-09-22  10.492319
[1105 rows x 2 columns]
```
