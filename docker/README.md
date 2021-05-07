# AKDocker

AKDocker is a dockerfile for AKShare's latest version

# Installation

## Install Docker

## Windows

[安装教程](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

## Mac

[Mac](https://docs.docker.com/docker-for-mac/install)

## Ubuntu

[安装教程](https://docs.docker.com/engine/install/ubuntu)

## CentOS

[安装教程](https://docs.docker.com/engine/install/centos)

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
