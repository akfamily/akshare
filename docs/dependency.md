## [AKShare](https://github.com/jindaxiang/akshare) 依赖说明

### Python 依赖

1. [AKShare](https://github.com/jindaxiang/akshare) 文档的依赖说明部分主要是为了对 [AKShare](https://github.com/jindaxiang/akshare) 库的所有依赖库做一个描述
   方便小伙伴在对 [AKShare](https://github.com/jindaxiang/akshare) 进行二次封装进行参考；
2. 提供选择该库函数的部分原因说明；
2. 所有的依赖名称都跟 PYPI 提供的库名称统一。

#### py-mini-racer

1. [PYPI 地址](https://pypi.org/project/py-mini-racer/)
2. [GitHub 地址](https://github.com/sqreen/PyMiniRacer)
3. 选用原因如下
    1. 由于 [PyExecJS](https://pypi.org/project/PyExecJS/) 在 20180118 推出最后一个版本后，主要的开发者
    不再对该库进行升级维护，导致部分问题无法通过升级该库来修复，该库的 [GitHub 地址](https://github.com/doloopwhile/PyExecJS) 可以访问如下地址，所以未采用该库;
    2. [Js2Py](https://pypi.org/project/Js2Py/) 是目前比较使用量较大和维护较好的库，其 [GitHub 地址](https://github.com/PiotrDabkowski/Js2Py) 但是
    考虑到在测试中，对部分 Javascript 代码的运行不稳定，所以未采用该库。

