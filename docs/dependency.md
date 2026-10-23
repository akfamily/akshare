# [AKShare](https://github.com/akfamily/akshare) 依赖说明

## Python 依赖

1. [AKShare](https://github.com/akfamily/akshare) 文档的依赖说明部分主要是为了对 [AKShare](https://github.com/akfamily/akshare) 库的所有依赖库做一个描述，
方便小伙伴在对 [AKShare](https://github.com/akfamily/akshare) 进行二次封装进行参考；
2. 提供选择该库函数的部分原因说明；
3. 所有的依赖名称都跟 PyPI 提供的库名称统一；
4. 打包的时候注意 mini-racer 库如报错，请重新编译。

### mini-racer

1. 版本 >=0.12.4，仅在 Windows 和 macOS 上安装；Linux 上改为安装 [py-mini-racer](https://pypi.org/project/py-mini-racer/)（>=0.6.0）和 [akracer](https://pypi.org/project/akracer/)（>=0.0.13），由 pip 按平台自动选择
2. 推荐使用最新版
3. [PyPI 地址](https://pypi.org/project/mini-racer/)
4. [GitHub 地址](https://github.com/bpcreech/PyMiniRacer)
5. 选用原因如下
    1. 由于 [PyExecJS](https://pypi.org/project/PyExecJS/) 在 20180118 推出最后一个版本后，
       主要的开发者不再对该库进行升级维护，导致部分问题无法通过升级该库来修复，
       该库的 [GitHub 地址](https://github.com/doloopwhile/PyExecJS) 可以访问如下地址，所以没有使用该库；
    2. [Js2Py](https://pypi.org/project/Js2Py/) 是目前比较使用量较大和维护较好的库，其 [GitHub 地址](https://github.com/PiotrDabkowski/Js2Py) 但是考虑到在测试中，
       对部分 Javascript 代码的运行不稳定，所以没有使用该库。

### pandas

1. 版本 >=2.0.0
2. 推荐使用最新版
3. [PyPI 地址](https://pypi.org/project/pandas/)
4. [GitHub 地址](https://github.com/pandas-dev/pandas/)
5. [文档地址](https://pandas.pydata.org/)
6. 选用原因如下
    1. 该库主要用于采集后的数据清洗，此处建议升级到最新版，[AKShare](https://github.com/akfamily/akshare/) 会优先支持最新的版本；
    2. 默认会安装 [NumPy](https://numpy.org/) 依赖。
