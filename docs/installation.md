# [AkShare](https://github.com/jindaxiang/akshare) 安装指导

## 重要提示

1. 首先请确认安装 [Python](https://www.python.org/) 3.6 及以上版本, 这里推荐 [Python](https://www.python.org/) 3.7.5 版本;
2. [AkShare](https://github.com/jindaxiang/akshare) 推荐安装最新版本的 [Anaconda](https://www.anaconda.com/), 可以解决大部分安装问题.

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

P.S. 体验 [AkShare](https://github.com/jindaxiang/akshare) 完整功能, 请安装 [Node.js](https://nodejs.org/dist/)

### Windows 系统

[点击下载 Node.js for win 64](https://nodejs.org/dist/v12.13.0/node-v12.13.0-x64.msi), 按照界面提示完成安装即可！

### Ubuntu 系统

```shell script
sudo apt-get install nodejs
```

### Node.js 介绍

Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行环境，它的存在使开发者可以在不依赖游览器的情况下编译和运行 JavaScript 代码。

### Node.js 相关链接

1. [Node.js 官网](https://nodejs.org)
2. [NVM 的 GitHub 仓库](https://github.com/nvm-sh/nvm)

### Node.js 详细安装

我们既可以从 [Node.js 官网](https://nodejs.org) 下载安装包，也可以通过它的版本管理工具 NVM 来安装它。使用 NVM 的好处是可以在计算机中
安装多个版本的 Node.js，并且安装过程也比较简单。

首先下载并安装 NVM，对应的命令如下：

```shell script
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
```

然后刷新环境变量，对应的命令如下：

```shell script
source ~/.bashrc
```

接着验证 NVM 是否安装成功。在终端执行以下命令：

```shell script
command -v nvm
```

此时终端会输出如下内容：

```shell script
nvm
```

这代表 NVM 已经成功安装，并且正常运行。接着就可以安装 Node.js 了，在终端执行以下命令：

```shell script
nvm install node
```

此时终端输出如下内容：

```shell script
Downloading and installing node v13.12.0...
Downloading https://nodejs.org/dist/v13.12.0/node-v13.12.0-linux-x64.tar.xz...
################################################################################################################################################################## 100.0%
Computing checksum with sha256sum
Checksums matched!
Now using node v13.12.0 (npm v6.14.4)
Creating default alias: default -> node (-> v13.12.0)
```

这代表 Node.js 最新版本已被下载并安装。

接下来验证 Node.js 是否已经安装成功。新建一个 nodev.js 的文件，并将以下内容写入文件：

```javascript
console.log("node 可用");
```

最后在同级目录下唤起终端，在终端执行以下命令：

```shell script
node nodev.js
```

如果此时终端输出如下内容：

```shell script
node 可用
```

代表 Node.js 已经成功安装，并且正常运行。


## 升级 [AkShare](https://github.com/jindaxiang/akshare)

P.S. **由于目前版本更新迭代频繁, 请在使用 [AkShare](https://github.com/jindaxiang/akshare) 前先升级, 命令如下所示**

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

使用管理员权限(右键单击选择管理员权限)打开 Anaconda Prompt 进行安装

### 4. 提示其他的错误

- 方法一: 升级您的 Anaconda 或者 Python 到 **Python3.7.5** 及以上版本
- 方法二: 使用 conda 的虚拟环境来安装, 详见 **AkShare 环境配置**板块的内容
