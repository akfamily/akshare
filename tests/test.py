import numpy as np
import pandas as pd
import xlsxwriter



#以下是对该代码的分步解释，结合相关技术文档进行说明：

#### 一、窗口周期定义
#```python
#rolling_window = n_years * 250  # 假设每年250个交易日
#```
#1. **参数含义**  
#   - `n_years`表示需要回溯的历史年份（如3年）
#   - `250`是金融市场中常用的年度交易日估算值（排除节假日）

#2. **计算逻辑**  
#   - 生成一个包含`n_years*250`个交易日的滚动窗口  
#   - 例如，当`n_years=3`时，窗口大小=750个交易日（约3年）

#---

#### 二、分位值计算
#```python
#hist_data['volume_quantile'] = hist_data['成交额'].rolling(rolling_window).apply(
#    lambda x: x.rank(pct=True).iloc[-1], raw=False)
#```

##### 1. 滚动窗口操作
#- `hist_data['成交额'].rolling(rolling_window)`  
#  创建一个`Rolling`对象，窗口大小为`rolling_window`，按时间顺序滑动窗口

##### 2. 百分比排名计算
#- `x.rank(pct=True)`  
#  对窗口内的每个数据点计算百分比排名：
#  - 当前成交额在窗口期内从小到大排序后的百分比位置
#  - 例如：0.05表示该成交额处于窗口期最低5%分位

##### 3. 获取当前时点分位
#- `.iloc[-1]`  
#  取窗口内最后一个元素（即当前交易日）的排名值，反映当前成交额在历史窗口中的相对位置

##### 4. 参数细节
#- `raw=False`  
#  保证向lambda函数传递的是`pandas.Series`对象，而非原始数组，便于使用`.rank()`方法

#---

#### 三、技术应用场景
##### 1. 地量检测逻辑
#- 当`volume_quantile < 0.05`时，表示当前成交额处于近n年最低5%分位  
#- 符合技术分析中"地量见地价"的判断标准（成交量萎缩至历史极低水平）

##### 2. 动态监测优势
#- 滚动窗口自动更新历史数据范围，避免使用固定日期导致的数据陈旧问题  
#- 相比Excel的静态分位计算（如`PERCENTRANK`函数），更适合处理实时变动的金融数据

#---

#### 四、扩展优化建议
#1. **窗口参数动态化**  
#   ```python
#   # 使用交易日历替代固定250天（需安装exchange_calendars库）
#   from exchange_calendars import get_calendar
#   cal = get_calendar("XSHG")  # 上交所日历
#   trading_days = cal.sessions_in_range(start_date, end_date)
#   rolling_window = len(trading_days)
#   ```

#2. **异常值处理**  
#   添加数据有效性校验，避免停牌日零成交量的干扰：
#   ```python
#   valid_data = hist_data[hist_data['成交额'] > 0]
#   ```

#3. **多维度验证**  
#   结合价格指标（如布林带）进行信号过滤：
#   ```python
#   price_ma = hist_data['收盘价'].rolling(20).mean()
#   in_lower_band = hist_data['收盘价'] < (price_ma - 2*price_ma.std())
#   valid_signal = low_volume_mask & in_lower_band
#   ```
hist_data = pd.DataFrame({"col1": np.random.randint(1, 501, size=1000)})
print(hist_data)
# 计算n年历史分位（参考网页5/7的地量判断逻辑）
rolling_window = 100  # 假设每年250个交易日
hist_data['volume_quantile'] = hist_data['col1'].rolling(rolling_window).apply(
    lambda x: x.rank(pct=True).iloc[-1], raw=False)

# 优化Excel写入（网页10）"""
excelName = "test"
writer = pd.ExcelWriter(f'.\output\{excelName}.xlsx',engine='xlsxwriter')
hist_data.to_excel(writer, index=True,  index_label="ID")  
writer.close()