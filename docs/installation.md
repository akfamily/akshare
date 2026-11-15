# 安装指导

## 重要提示

1. 目前 [AKShare](https://github.com/akfamily/akshare) 仅支持 64 位版本的操作系统安装和使用；
2. 目前 AKShare 仅支持 [Python](https://www.python.org/) 3.11.5(64 位) 及以上版本，这里推荐 [Python](https://www.python.org/) 3.13.x(64 位) 版本；
3. Linux 需要 glibc 2.27 及以上（如 Ubuntu 18.04、Debian 10、CentOS 8 及更新的版本），可用 `ldd --version` 查看；CentOS 7 等更早的系统无法安装 AKShare 1.20.25 及以后的版本；
4. AKShare 推荐使用 [uv](https://docs.astral.sh/uv/) 来安装 Python 和管理虚拟环境，详见 [AKShare uv 环境配置](uv.md)；如需在 R 语言或 MATLAB 中调用，请参考下文的“R 语言调用支持”和“MATLAB 调用支持”；
5. 需要通过 HTTP 调用 AKShare 时，请使用 [AKTools](aktools.md) 部署 HTTP API 服务；
6. 需要在 Claude、Cursor 等 AI 助手中使用 AKShare 数据时，不必安装 AKShare，按 [AI 助手（MCP）](mcp.md) 接入 AKTools 的 MCP 服务即可。

## 安装 AKShare

### 使用 uv 安装（推荐）

在已激活的 uv 虚拟环境中运行，安装 uv 和创建虚拟环境的完整步骤详见 [AKShare uv 环境配置](uv.md)：

```
uv pip install akshare --upgrade
```

国内用户可以使用镜像源加速：

```
uv pip install akshare --upgrade --default-index https://pypi.tuna.tsinghua.edu.cn/simple
```

### 使用 pip 安装

```
pip install akshare --upgrade
```

国内用户可以使用镜像源加速：

```
pip install akshare --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```{warning}
程序运行时，文件名、文件夹名不能是 akshare
```

## 升级 AKShare

P.S. **由于目前版本更新迭代频繁，请在使用 AKShare 前先升级，命令如下所示**

```
pip install akshare --upgrade -i https://pypi.org/simple
```

## 树莓派支持

目前 AKShare 已支持在树莓派 4B 上安装和使用（需要 64 位系统），具体安装方法如下：

1. 安装 [Raspberry Pi OS (64-bit)](https://www.raspberrypi.com/software/operating-systems/) 操作系统，目前支持树莓派于 20231010 发布的 64 位版本
2. 通过 `sudo apt-get install python3-venv` 安装虚拟环境支持
3. 通过 `python3 -m venv myenv` 创建名为 `myenv` 的虚拟环境
4. 通过 `source myenv/bin/activate` 来激活创建好的虚拟环境
5. 通过 `pip install akshare --upgrade` 来安装和升级 AKShare 到最新版本

(install-r)=
## R 语言调用支持

```{tip}
推荐使用 [AKTools 项目](https://github.com/akfamily/aktools) 部署 AKShare 的 HTTP API，运行速度更快、更稳定，兼容各种编程语言，详情参考 [AKTools 文档](https://aktools.akfamily.xyz/)。
```

### 配置 Python 环境

按 [AKShare uv 环境配置](uv.md) 中的“方式一：虚拟环境”，创建名为 `ak_test` 的工作目录和虚拟环境，并在其中安装 AKShare。Python 需为 3.11.5 及以上版本，推荐 3.13。

### 安装 R 语言

[下载 R](https://mirrors.tuna.tsinghua.edu.cn/CRAN/bin/windows/)

[下载 RStudio Desktop](https://posit.co/download/rstudio-desktop/)

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
use_virtualenv("~/ak_test/.venv", required = TRUE)  # 使用 uv 创建的虚拟环境
```

即可调用已安装 AKShare 的 Python 环境，其中 `~/ak_test/.venv` 为虚拟环境所在目录，请替换为实际路径。
也可以用 `use_python()` 直接指定 Python 解释器的完整路径，例如 Windows 上的 `use_python("C:/Users/用户名/ak_test/.venv/Scripts/python.exe")`，
macOS 上的 `use_python("/Users/用户名/ak_test/.venv/bin/python")`，其中“用户名”需要替换为本地计算机的用户名。

最后展示一段演示代码，此代码在 R 语言中通过 reticulate 包来调用 AKShare 获取数据：

```
library(reticulate)  # 导入 reticulate 包
use_virtualenv("~/ak_test/.venv", required = TRUE)  # 使用 uv 创建的虚拟环境
ak <- import("akshare")  # 类似于 import akshare as ak
stock_df <- ak$stock_zh_a_hist_sina(symbol = "sz000001")  # 类似于 ak.stock_zh_a_hist_sina(symbol="sz000001")
head(stock_df)  # 查看数据
```

```
         date   open   high    low  close  volume   amount  outstanding_share  turnover
1  1991-04-03  49.00  49.00  49.00  49.00   100.0   5000.0         37100000.0  0.000003
2  1991-04-04  48.76  48.76  48.76  48.76   300.0  15000.0         37100000.0  0.000008
3  1991-04-05  48.52  48.52  48.52  48.52   200.0  10000.0         37100000.0  0.000005
4  1991-04-08  48.04  48.04  48.04  48.04   200.0  10000.0         37100000.0  0.000005
5  1991-04-09  47.80  47.80  47.80  47.80   400.0  19000.0         37100000.0  0.000011
6  1991-04-10  47.56  47.56  47.56  47.56  1500.0  71000.0         37100000.0  0.000040
```

(install-matlab)=
## MATLAB 调用支持

```{tip}
推荐使用 [AKTools 项目](https://github.com/akfamily/aktools) 部署 AKShare 的 HTTP API，运行速度更快、更稳定，兼容各种编程语言，详情参考 [AKTools 文档](https://aktools.akfamily.xyz/)。
```

### 配置 Python 环境

按 [AKShare uv 环境配置](uv.md) 中的“方式一：虚拟环境”创建虚拟环境并安装 AKShare，其中 Python 的版本需要符合
[Matlab 各版本对 Python 的支持](https://www.mathworks.com/support/requirements/python-compatibility.html?s_tid=srchtitle_site_search_1_python%20compatibility)
，同时满足 AKShare 对 Python 3.11.5 及以上版本的要求。比如 `Matlab R2023b` 支持 `Python` 的 `3.9, 3.10, 3.11` 版本，只能选用 3.11；`Matlab R2024b` 至 `R2025b` 最高支持 3.12；`Matlab R2026a` 起支持推荐的 3.13。创建虚拟环境时用 `--python` 指定版本，例如 `uv venv --python 3.12`。

### 安装 MATLAB

通过 [MATLAB 下载页面](https://ww2.mathworks.cn/downloads/) 登录 MathWorks 账号后下载并激活 64 位 MATLAB；
由于下文的数据格式转换需要用到 R2024a 引入的功能，建议安装 R2024a 及以上版本。

通过官方安装文档 [安装 64 位 MATLAB](https://ww2.mathworks.cn/help/install/ug/install-products-on-client-machines.html) 来
进行安装配置。

### 配置环境

1. Matlab 官方文档：[配置您的系统使用 Python](https://ww2.mathworks.cn/help/matlab/matlab_external/install-supported-python-implementation.html)
2. 帮助社区解答：[Python virtual environments with MATLAB](https://www.mathworks.com/support/search.html/answers/1750425-python-virtual-environments-with-python-interface.html?fq%5B%5D=asset_type_name:answer&page=1)

如果使用虚拟环境，则 `pyenv(Version="C:\Users\用户名\ak_test\.venv\Scripts\python.exe");` 即可激活相关环境，
此处 `C:\Users\用户名\ak_test\.venv\Scripts\python.exe` 为本地虚拟环境中 Python 解释器的路径，“用户名”需要替换为本地计算机的用户名；macOS 和 Linux 上为虚拟环境目录下的 `.venv/bin/python`。

#### 测试环境配置

在 MATLAB 命令行窗口输入：

```
pyenv
```

如果返回结果中的 `Executable` 为上面指定的虚拟环境中的 Python 解释器路径，`Version` 为该环境的 Python 版本，则表示可以正常使用该虚拟环境中的 Python，
同时确保在该环境中已经安装最新版的 AKShare（可以在激活该虚拟环境后运行 `uv pip show akshare` 查看）。

#### 测试调用 AKShare 接口

在 MATLAB 命令行窗口输入：

```
py.akshare.stock_zh_a_hist_sina
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

                date   open   high  ...       amount  outstanding_share  turnover
    0     2016-09-05   6.04   7.24  ...     206832.0         99700000.0  0.000289
    1     2016-09-06   7.96   7.96  ...     102565.0         99700000.0  0.000129
    2     2016-09-07   8.76   8.76  ...     122640.0         99700000.0  0.000140
    3     2016-09-08   9.64   9.64  ...     122727.0         99700000.0  0.000128
    4     2016-09-09  10.60  10.60  ...     518340.0         99700000.0  0.000490
    ...          ...    ...    ...  ...          ...                ...       ...
    2346  2026-11-09   4.45   4.92  ...  130069565.0        699623237.0  0.040208
    2347  2026-11-10   4.86   5.32  ...   98656795.0        699623237.0  0.027986
    2348  2026-11-11   5.11   5.31  ...   92000327.0        699623237.0  0.025527
    2349  2026-11-12   5.01   5.12  ...   49234315.0        699623237.0  0.013961
    2350  2026-11-13   5.00   5.02  ...   58031900.0        699623237.0  0.017102

    [2351 rows x 9 columns]
```

则表示可以在 MATLAB 中调用 AKShare 的数据接口。

### 调用 AKShare

#### 不带参数接口调用

在 MATLAB 命令行窗口输入：

```
py.akshare.macro_china_leverage_nifd
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
py.akshare.stock_zh_a_hist_sina("sz000001", "daily", "20170301", '20210907', "")
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

                date   open   high  ...        amount  outstanding_share  turnover
    0     2017-03-01   9.49   9.55  ...  3.301580e+08       1.691799e+10  0.002051
    1     2017-03-02   9.51   9.54  ...  3.823959e+08       1.691799e+10  0.002386
    2     2017-03-03   9.41   9.43  ...  3.219525e+08       1.691799e+10  0.002025
    3     2017-03-06   9.40   9.46  ...  3.812123e+08       1.691799e+10  0.002391
    4     2017-03-07   9.44   9.46  ...  2.777474e+08       1.691799e+10  0.001742
    ...          ...    ...    ...  ...           ...                ...       ...
    1100  2021-09-01  17.48  17.92  ...  4.046284e+09       1.940575e+10  0.011939
    1101  2021-09-02  18.00  18.78  ...  4.454545e+09       1.940575e+10  0.012484
    1102  2021-09-03  18.50  18.50  ...  2.523273e+09       1.940575e+10  0.007188
    1103  2021-09-06  17.93  18.60  ...  2.780281e+09       1.940575e+10  0.007808
    1104  2021-09-07  18.60  19.56  ...  3.067366e+09       1.940575e+10  0.008360

    [1105 rows x 9 columns]
```

则表示可以在 MATLAB 中调用 AKShare 的带参数的接口。

### 转换数据格式

#### 演示

```
% 导入 AKShare 库
ak = py.importlib.import_module('akshare');
% 调用 AKShare 数据接口
temp_df = ak.stock_zh_a_hist_sina();
% 将 pandas.DataFrame 转换为 MATLAB 表格，需要 MATLAB R2024a 及以上版本
df = table(temp_df);
% 展示获取到本地的数据
disp(df)
```

## 安装报错解决方案

### 1. 安装超时的错误

1. 大致报错如下，出现关键词 **amt**：

```
Traceback (most recent call last):
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/requests/packages/urllib3/response.py", line 228, in _error_catcher
yield
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/requests/packages/urllib3/response.py", line 310, in read
data = self._fp.read(amt)
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/cachecontrol/filewrapper.py", line 49, in read
data = self.__fp.read(amt)
```

2. 解决方案如下：

方法一

```
pip --default-timeout=100 install -U akshare
```

方法二

使用全局代理解决

### 2. 拒绝访问错误

1. 大致报错如下，出现关键词 **拒绝访问**：

```
Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/mac/Anaconda/anaconda3/lib/python3.7/site-packages/cv2/__init__.py'
Consider using the `--user` option or check the permissions.
```

2. 解决方案如下：

方法一

在虚拟环境中安装，虚拟环境位于用户目录下，不需要管理员权限，详见 [AKShare uv 环境配置](uv.md)

方法二

使用管理员权限（右键单击选择管理员权限）打开命令提示符或 PowerShell 进行安装

### 3. 提示其他的错误

- 方法一：确认并升级您已安装 64 位的 **Python 3.11.5** 及以上版本
- 方法二：使用虚拟环境来安装，推荐使用 uv，详见 [AKShare uv 环境配置](uv.md)
