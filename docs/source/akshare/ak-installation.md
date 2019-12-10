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

- 进入 **.whl** 所在的文件夹, 执行命令即可完成安装

```
pip install 带后缀的完整文件名
```

### 2. 提示其他错误的

升级您的 Anaconda 或者 Python 到 **Python3.7.3** 及以上版本
