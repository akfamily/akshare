# [AKShare](https://github.com/akfamily/akshare) Docker 部署

目前 [AKShare](https://github.com/akfamily/akshare) 数据接口是基于 Python 开发的，鉴于部分小伙伴难以在短时间部署
[AKShare](https://github.com/akfamily/akshare) 的 Python 使用环境，特此提供基于 Docker 容器技术的使用教程。

## 安装 Docker

### 官方安装指导

1. Windows 11: [安装教程](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
2. Mac: [安装教程](https://docs.docker.com/docker-for-mac/install)
3. Ubuntu: [安装教程](https://docs.docker.com/engine/install/ubuntu)
4. CentOS: [安装教程](https://docs.docker.com/engine/install/centos)

### 第三方安装指导

1. [Docker 安装教程](https://www.runoob.com/docker/docker-tutorial.html)
2. 建议 Windows 7 和 8 的用户升级到 Windows 10/11 系统进行安装
3. [Windows 镜像下载地址](https://msdn.itellyou.cn/)

### 配置国内镜像

1. [Docker 国内镜像加速教程](https://www.runoob.com/docker/docker-mirror-acceleration.html)
2. 请在国内使用的用户务必进行该项配置, 从而加速获取镜像的速度.

## AKDocker 镜像使用

### 拉取 AKDocker 镜像

此镜像会在每次 AKShare 更新版本时自动更新

```
docker pull registry.cn-shanghai.aliyuncs.com/akfamily/aktools:jupyter
```

### 运行 AKDocker 容器

```
docker run -it registry.cn-shanghai.aliyuncs.com/akfamily/aktools:jupyter
```

### 测试 AKDocker 容器

```python
import akshare as ak

print(ak.__version__)
```

## 使用案例

### 背景说明

本案例是基于 AKDocker 容器中已经安装的 JupyterLab 来演示的. 主要是利用 JupyterLab 的 Python 交互式的开发环境, 使用户可以在 Web 输入 AKShare
的 Python 示例代码, 仅需要修改一些简单的参数, 就可以获取需要的数据. 为了能把 JupyterLab 中下载的数据从容器映射到本地, 请在
容器的 ```/home``` 目录下编辑 ```.ipynb``` 文件, 如果需要下载相关的文件也请保存到该目录.

### 命令行

```
docker run -it -p 8888:8888 --name akdocker -v /c/home:/home registry.cn-shanghai.aliyuncs.com/akfamily/aktools:jupyter jupyter-lab --allow-root --no-browser --ip=0.0.0.0
```

### 注意事项

1. 其中 Windows 系统的路径如: ```C:\home``` 需要改写为: ```/c/home``` 的形式;
2. 在 Terminal 中运行上述指令后，会在 Terminal 中显示如下信息: ![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/akdocker/akdocker_terminal.png)
3. 打开本地游览器输入地址: ```http://127.0.0.1:8888/lab?token=bbe7c8633c098b67df913dce522b82e00828b311a6fc954d```;
4. 在本地游览器中的 JupyterLab 界面进入 ```home``` 文件夹, 该目录内容会与本地的 ```C:\home``` 保持同步, 可以在此编辑 notebook 文件和导入数据到该文件夹从而在本地的 ```C:\home``` 文件夹下获取数据;
5. 如果在 JupyterLab 中的 AKShare 版本不是最新版，有以下两种方法：
   1. 在 JupyterLab 中运行 `!pip install akshare --upgrade` 命令来升级 AKShare 到最新版
   2. 在容器中进行升级 AKShare 并保存为新的镜像文件后使用，参考：https://aktools.akfamily.xyz/aktools/ 中【升级镜像】部分
