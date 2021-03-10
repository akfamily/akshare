# AKDocker

AKDocker is a dockerfile for AKShare's latest version

# Installation

## Install Docker

## Windows

[安装教程](https://www.cnblogs.com/skatesky/archive/2019/12/05/11987955.html)

## Ubuntu

[安装教程](https://www.jianshu.com/p/28d41eb592b0)

## Command

### Pull AKDocker

```
docker pull registry.cn-hangzhou.aliyuncs.com/akshare/akdocker
```

### Run AKDocker
```
docker run -it registry.cn-hangzhou.aliyuncs.com/akshare/akdocker python
```

### Test AKDocker

```python
import akshare as ak
ak.__version__
```
