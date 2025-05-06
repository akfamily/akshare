# [AKShare](https://github.com/akfamily/akshare) 安装指导

## 重要提示

1. 目前 [AKShare](https://github.com/akfamily/akshare) 仅支持 64 位版本的操作系统安装和使用;
2. 目前 [AKShare](https://github.com/akfamily/akshare) 仅支持 [Python](https://www.python.org/) 3.8(64 位) 及以上版本, 这里推荐 [Python](https://www.python.org/) 3.11.x(64 位) 版本;
3. [AKShare](https://github.com/akfamily/akshare) 推荐安装最新版本的 [Anaconda (64 位)](https://www.anaconda.com/), 可以解决大部分环境配置问题;
4. 对于熟悉容器技术的小伙伴, 可以安装 Docker 使用, 指导教程如下: [AKShare Docker 部署](https://akshare.akfamily.xyz/akdocker/akdocker.html).

## 安装 [AKShare](https://github.com/akfamily/akshare)

### 通用安装

```
pip install akshare --upgrade
```

注意：程序运行时，文件名、文件夹名不能是：akshare

### 国内安装-Python

```
pip install akshare --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 国内安装-Anaconda

```
pip install akshare --upgrade --user -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 升级 [AKShare](https://github.com/akfamily/akshare)

P.S. **由于目前版本更新迭代频繁, 请在使用 [AKShare](https://github.com/akfamily/akshare) 前先升级, 命令如下所示**

```
pip install akshare --upgrade -i https://pypi.org/simple
```

## M 系列芯片支持

1. AKShare 目前已经默认适合苹果 M 系列芯片，直接通过 `pip install akshare --upgrade` 即可使用
2. 如果需要编译，请参考该文章：[Building V8 on an M1 MacBook](https://joyeecheung.github.io/blog/2021/08/27/binding-v8-on-an-m1-macbook/)

## 树莓派支持

目前 AKShare 已支持在树莓派 4B 上安装和使用，具体安装方法如下：

1. 安装 [Raspberry Pi OS (64-bit)](https://www.raspberrypi.com/software/operating-systems/) 操作系统，目前支持树莓派于 20231010 发布的 64 位版本
2. 通过 `sudo apt-get install python3-venv` 安装虚拟环境支持
3. 通过 `python3 -m venv myenv` 创建名为 `myenv` 的虚拟环境
4. 通过 `source myenv/bin/activate` 来激活创建好的虚拟环境
5. 通过 `pip install akshare --upgrade` 来安装和升级 AKShare 到最新版本

## R 语言调用支持

**推荐使用 [AKTools 项目](https://github.com/akfamily/aktools) 来部署 AKShare 的 HTTP API 使用，运行速度更快，更稳定，兼容各种编程语言，详情参考 [AKTools 文档](https://aktools.readthedocs.io/)**

### 安装 Anaconda

[下载 Windows 64 位 Python 3.8 的 Anaconda](https://repo.anaconda.com/archive/Anaconda3-2020.07-Windows-x86_64.exe)

[安装教程参见 AKShare 文档的环境配置专栏](https://akshare.akfamily.xyz/anaconda.html)

### 安装 R 语言

[下载 R](https://mirrors.tuna.tsinghua.edu.cn/CRAN/bin/windows/)

[下载 RStudio](https://download1.rstudio.org/desktop/windows/RStudio-1.3.959.exe)

先安装 R，再安装 RStudio，选择默认步骤安装即可。

### 升级 R 语言到最新版本

#### Windows

```
install.packages('installr')
library(installr)
updateR()
```

#### Mac

从 [CRAN website](https://cran.r-project.org/) 网站下载和安装最新的版本，覆盖升级即可。

### 在 R 语言中安装相应的包

[Reticulate](https://rstudio.github.io/reticulate/)

```
install.packages("reticulate")
```

在安装完成后通过运行

```
library(reticulate)
use_python("/usr/local/bin/python")  # 默认使用本地的 Python, 如果需要使用虚拟环境的 Pyhton, 请参考 reticulate 的提示
```

调用本地的 Python 程序，其中 usr 需要替换为本地计算机的用户名。

最后展示一段演示代码，此代码在 R 语言中通过 reticulate 包来调用 [AKShare](https://github.com/akfamily/akshare) 获取数据：

```
library(reticulate)  # 导入 reticulate 包
use_python("/king/local/bin/python")  # 其中的 king 为本地计算机用户名
# use_condaenv(condaenv="ak_test", required = TRUE)  # 也可以使用 conda 创建的虚拟环境，其中的 ak_test 为虚拟环境名称
ak <- import("akshare")  # 类似于 import akshare as ak
stock_df <- ak$stock_zh_a_hist()  # 类似于 ak.stock_zh_a_hist()
head(stock_df)  # 查看数据
```

```
        日期  开盘   收盘  最高   最低     成交量 成交额  振幅  涨跌幅 涨跌额 换手率
1 1991-04-03 49.00 49.00 49.00 49.00      1   5000    0  22.50   9.00  0
2 1991-04-04 48.76 48.76 48.76 48.76      3  15000    0  -0.49  -0.24  0
3 1991-04-05 48.52 48.52 48.52 48.52      2  10000    0  -0.49  -0.24  0
4 1991-04-06 48.28 48.28 48.28 48.28      7  34000    0  -0.49  -0.24  0
5 1991-04-08 48.04 48.04 48.04 48.04      2  10000    0  -0.50  -0.24  0
6 1991-04-09 47.80 47.80 47.80 47.80      4  19000    0  -0.50  -0.24  0
```

## MATLAB 调用支持

**推荐使用 [AKTools 项目](https://github.com/akfamily/aktools) 来部署 AKShare 的 HTTP API 使用，运行速度更快，更稳定，兼容各种编程语言，详情参考 [AKTools 文档](https://aktools.readthedocs.io/)**

### 安装 Anaconda

[下载 Windows 平台带 64 位 Python 的 Anaconda](https://repo.anaconda.com/archive/)，其需要符合
[Matlab 各版本对 Python 的支持](https://www.mathworks.com/support/requirements/python-compatibility.html?s_tid=srchtitle_site_search_1_python%20compatibility)
，比如 `Matlab R2023b` 目前支持 `Python` 的 `3.9, 3.10, 3.11` 版本。

[Anaconda 安装教程参见 AKShare 文档的环境配置专栏](https://akshare.akfamily.xyz/anaconda.html)

### 安装 MATLAB

通过 [下载 64 位 MATLAB R2023b](https://ww2.mathworks.cn/downloads/message/error_page/unlicensed?release=R2023b) 页面
来登录后下载激活。

通过官方安装文档 [安装 64 位 MATLAB](https://ww2.mathworks.cn/help/install/ug/install-products-on-client-machines.html) 来
进行安装配置。

### 配置环境

1. Matlab 官方文档：[配置您的系统使用 Python](https://ww2.mathworks.cn/help/matlab/matlab_external/install-supported-python-implementation.html)
2. 帮助社区解答：[Python virtual environments with MATLAB](https://www.mathworks.com/support/search.html/answers/1750425-python-virtual-environments-with-python-interface.html?fq%5B%5D=asset_type_name:answer&page=1)

如果使用虚拟环境，则 `pyenv(Version="C:\Users\albert\.conda\envs\matlab\python.exe");` 即可激活相关环境，
此处 `C:\Users\albert\.conda\envs\matlab\python.exe` 为本地虚拟环境的路径。

#### 测试环境配置

在 MATLAB 命令行窗口输入：

```
pyenv
```

如返回：

```
ans =

  PythonEnvironment - 属性:

          Version: "3.10"
       Executable: "C:\Users\albert\.conda\envs\matlab\python.EXE"
          Library: "C:\Users\albert\.conda\envs\matlab\python310.dll"
             Home: "C:\Users\albert\.conda\envs\matlab"
           Status: NotLoaded
    ExecutionMode: InProcess
```

则表示可以正常使用 `C:\Users\albert\.conda\envs\matlab\python` 虚拟环境中的 Python，
同时确保在该环境中已经安装最新版的 AKShare（可以在本地 conda 中名为 `matlab` 的虚拟环境中查看）。

#### 测试调用 AKShare 接口

在 MATLAB 命令行窗口输入：

```
py.akshare.stock_zh_a_hist
```

如返回：

```
ans =

  Python DataFrame - 属性:

          T: [1×1 py.pandas.core.frame.DataFrame]
         at: [1×1 py.pandas.core.indexing._AtIndexer]
      attrs: [1×1 py.dict]
       axes: [1×2 py.list]
    columns: [1×1 py.pandas.core.indexes.base.Index]
     dtypes: [1×1 py.pandas.core.series.Series]
      empty: 0
      flags: [1×1 py.pandas.core.flags.Flags]
        iat: [1×1 py.pandas.core.indexing._iAtIndexer]
       iloc: [1×1 py.pandas.core.indexing._iLocIndexer]
      index: [1×1 py.pandas.core.indexes.range.RangeIndex]
        loc: [1×1 py.pandas.core.indexing._LocIndexer]
       ndim: [1×1 py.int]
      shape: [1×2 py.tuple]
       size: [1×1 py.int]
     values: [1×1 py.numpy.ndarray]

                  日期     开盘     收盘     最高  ...    振幅    涨跌幅   涨跌额   换手率
    0     1991-04-03  49.00  49.00  49.00  ...  0.00  22.50  9.00  0.00
    1     1991-04-04  48.76  48.76  48.76  ...  0.00  -0.49 -0.24  0.00
    2     1991-04-05  48.52  48.52  48.52  ...  0.00  -0.49 -0.24  0.00
    3     1991-04-06  48.28  48.28  48.28  ...  0.00  -0.49 -0.24  0.00
    4     1991-04-08  48.04  48.04  48.04  ...  0.00  -0.50 -0.24  0.00
    ...          ...    ...    ...    ...  ...   ...    ...   ...   ...
    7867  2024-03-11  10.38  10.47  10.47  ...  1.25   0.87  0.09  0.62
    7868  2024-03-12  10.48  10.56  10.59  ...  1.72   0.86  0.09  0.85
    7869  2024-03-13  10.53  10.33  10.55  ...  2.37  -2.18 -0.23  0.91
    7870  2024-03-14  10.30  10.23  10.38  ...  1.74  -0.97 -0.10  0.73
    7871  2024-03-15  10.55  10.60  10.75  ...  2.44   3.62  0.37  1.93

    [7872 rows x 11 columns]
```

则表示可以在 MATLAB 中调用 AKShare 的数据接口。

### 调用 AKShare

#### 不带参数接口调用

在 MATLAB 命令行窗口输入：

```
py.akshare.macro_cnbs
```

如返回：

```
ans =

  Python DataFrame - 属性:

          T: [1×1 py.pandas.core.frame.DataFrame]
         at: [1×1 py.pandas.core.indexing._AtIndexer]
      attrs: [1×1 py.dict]
       axes: [1×2 py.list]
    columns: [1×1 py.pandas.core.indexes.base.Index]
     dtypes: [1×1 py.pandas.core.series.Series]
      empty: 0
        iat: [1×1 py.pandas.core.indexing._iAtIndexer]
       iloc: [1×1 py.pandas.core.indexing._iLocIndexer]
      index: [1×1 py.pandas.core.indexes.range.RangeIndex]
        loc: [1×1 py.pandas.core.indexing._LocIndexer]
       ndim: [1×1 py.int]
      shape: [1×2 py.tuple]
       size: [1×1 py.numpy.int32]
      style: [1×1 py.pandas.io.formats.style.Styler]
     values: [1×1 py.numpy.ndarray]

              年份       居民部门     非金融企业部门  ...      实体经济部门    金融部门资产方    金融部门负债方
    0    1993-12   8.311222   91.658000  ...  107.791459   8.896441   7.128428
    1    1994-12   7.808230   82.411703  ...   98.354271   9.808787   6.796868
    2    1995-12   8.200000   81.000000  ...   97.900000  10.000000   7.000000
    3    1996-03   8.400000   81.700000  ...   99.200000  10.200000   7.200000
    4    1996-06   8.600000   82.100000  ...   99.700000  10.400000   7.400000
    ..       ...        ...         ...  ...         ...        ...        ...
    101  2020-09  61.700000  164.600000  ...  271.200000  55.800000  62.400000
    102  2020-12  62.200000  162.300000  ...  270.100000  54.200000  62.700000
    103  2021-03  62.100000  161.400000  ...  267.800000  52.800000  62.300000
    104  2021-06  62.000000  158.800000  ...  265.400000  51.300000  61.700000
    105  2021-09  62.100000  157.200000  ...  264.800000  49.200000  61.900000

    [106 rows x 9 columns]
```

则表示可以在 MATLAB 中调用 AKShare 的不带参数的接口。

#### 带参数接口调用

在 MATLAB 命令行窗口输入：

```
% 注意其中的传参方式，从左到右，依次传递参数，形参（及其‘=’）都不需要，参数必须按顺序传递
py.akshare.stock_zh_a_hist("000001", "daily", "20170301", '20210907', "")
```

如返回：

```
ans =

  Python DataFrame - 属性:

          T: [1×1 py.pandas.core.frame.DataFrame]
         at: [1×1 py.pandas.core.indexing._AtIndexer]
      attrs: [1×1 py.dict]
       axes: [1×2 py.list]
    columns: [1×1 py.pandas.core.indexes.base.Index]
     dtypes: [1×1 py.pandas.core.series.Series]
      empty: 0
        iat: [1×1 py.pandas.core.indexing._iAtIndexer]
       iloc: [1×1 py.pandas.core.indexing._iLocIndexer]
      index: [1×1 py.pandas.core.indexes.range.RangeIndex]
        loc: [1×1 py.pandas.core.indexing._LocIndexer]
       ndim: [1×1 py.int]
      shape: [1×2 py.tuple]
       size: [1×1 py.numpy.int32]
      style: [1×1 py.pandas.io.formats.style.Styler]
     values: [1×1 py.numpy.ndarray]

                  日期     开盘     收盘     最高  ...    振幅   涨跌幅   涨跌额   换手率
    0     2017-03-01   9.49   9.49   9.55  ...  0.84  0.11  0.01  0.21
    1     2017-03-02   9.51   9.43   9.54  ...  1.26 -0.63 -0.06  0.24
    2     2017-03-03   9.41   9.40   9.43  ...  0.74 -0.32 -0.03  0.20
    3     2017-03-06   9.40   9.45   9.46  ...  0.74  0.53  0.05  0.24
    4     2017-03-07   9.44   9.45   9.46  ...  0.63  0.00  0.00  0.17
    ...          ...    ...    ...    ...  ...   ...   ...   ...   ...
    1100  2021-09-01  17.48  17.88  17.92  ...  5.11  0.45  0.08  1.19
    1101  2021-09-02  18.00  18.40  18.78  ...  5.48  2.91  0.52  1.25
    1102  2021-09-03  18.50  18.04  18.50  ...  4.35 -1.96 -0.36  0.72
    1103  2021-09-06  17.93  18.45  18.60  ...  4.55  2.27  0.41  0.78
    1104  2021-09-07  18.60  19.24  19.56  ...  6.56  4.28  0.79  0.84

    [1105 rows x 11 columns]
```

则表示可以在 MATLAB 中调用 AKShare 的带参数的接口。

### 转换数据格式

#### 演示

```
% 导入 AKShare 库
ak = py.importlib.import_module('akshare');
% 代用 AKShare 数据接口
temp_df = ak.stock_zh_a_hist();
% 转化数据格式
df = py2matlab(temp_df);
% 展示获取到本地的数据
disp(df)
```

## 安装报错解决方案

### 1. 安装超时的错误

1.大致报错如下, 出现关键词 **amt** :

```
Traceback (most recent call last):
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/requests/packages/urllib3/response.py", line 228, in _error_catcher
yield
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/requests/packages/urllib3/response.py", line 310, in read
data = self._fp.read(amt)
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/cachecontrol/filewrapper.py", line 49, in read
data = self.__fp.read(amt)
```

2.解决方案如下:

方法一

```
pip --default-timeout=100 install -U akshare
```

方法二

使用全局代理解决

### 2. 拒绝访问错误

1.大致报错如下, 出现关键词 **拒绝访问** :

```
Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/mac/Anaconda/anaconda3/lib/python3.7/site-packages/cv2/__init__.py'
Consider using the `--user` option or check the permissions.
```

2.解决方案如下:

方法一

```
pip install akshare --user
```

方法二

使用管理员权限(右键单击选择管理员权限)打开 Anaconda Prompt 进行安装

### 3. 提示其他的错误

- 方法一: 确认并升级您已安装 64 位的 **Python 3.9** 及以上版本
- 方法二: 使用 conda 的虚拟环境来安装, 详见 **[AKShare](https://github.com/akfamily/akshare) 环境配置** 板块的内容
