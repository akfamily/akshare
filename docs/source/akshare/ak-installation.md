# 安装指导

**目前 [AkShare](https://github.com/jindaxiang/akshare) 支持 Python 3.6 及以上版本**

## 安装 [AkShare](https://github.com/jindaxiang/akshare)

### 通用安装

```
pip install akshare  --upgrade
```

### 国内安装-Python

```
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
```

### 国内安装-Anaconda

```
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --user  --upgrade
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

### 1. 安装 lxml 库失败的错误

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

### 2. 安装超时的错误

1.大致报错如下, 出现关键词 **amt**:

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

### 3. 拒绝访问错误

1.大致报错如下, 出现关键词 **拒绝访问**:

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

使用管理员权限打开 Anaconda Prompt 进行安装

### 4. 提示其他的错误

- 方法一: 升级您的 Anaconda 或者 Python 到 **Python3.7.3** 及以上版本
- 方法二: 使用 conda 的虚拟环境来安装, 详见 **AkShare 环境配置**板块的内容
