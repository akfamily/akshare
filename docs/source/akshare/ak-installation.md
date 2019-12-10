# 安装指导

**目前 [AkShare](https://github.com/jindaxiang/akshare) 支持 Python 3.6 及以上版本**

## 安装 [AkShare](https://github.com/jindaxiang/akshare)

```
pip install akshare
```

## 安装 [Node.js](https://nodejs.org/dist/)

**体验 [AkShare](https://github.com/jindaxiang/akshare) 完整功能, 请安装 [Node.js](https://nodejs.org/dist/)**

### Windows 系统

[点击下载 Node.js for win 64](https://nodejs.org/dist/v12.13.0/node-v12.13.0-x64.msi), 按照界面提示完成安装！

### Ubuntu 系统
```
sudo apt-get install nodejs
```

## 升级 [AkShare](https://github.com/jindaxiang/akshare)

**由于目前版本更新迭代比较频繁, 请在使用 [AkShare](https://github.com/jindaxiang/akshare) 前先升级, 命令如下所示**

```
pip install akshare --upgrade
```

## 安装报错解决方案

### 1. 提示安装 lxml 库失败

- 安装 wheel, 在 CMD 中运行如下命令:

```
pip install wheel
```

- 在[这里下载](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml3)与您的 Python 版本对应的 **.whl** 文件, **注意别改文件名!**

以下提供 64 位电脑的版本, 所以下载对应的 64 位就可以, 点击如下链接也可以下载:

1. [lxml‑4.4.2‑cp36‑cp36m‑win_amd64.whl](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/software/lxml/lxml-4.4.2-cp36-cp36m-win_amd64.whl)
2. [lxml‑4.4.2‑cp37‑cp37m‑win_amd64.whl](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/software/lxml/lxml-4.4.2-cp37-cp37m-win_amd64.whl)

- 进入 **.whl** 所在的文件夹, 执行命令即可完成安装, 如下

```
pip install 带后缀的完整路径和文件名
```

### 2. 提示其他错误的

升级您的 Anaconda 或者 Python 到 **Python3.7.3** 及以上版本
