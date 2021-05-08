# [AKShare](https://github.com/jindaxiang/akshare) Docker 部署

目前 [AKShare](https://github.com/jindaxiang/akshare) 数据接口是基于 Python 开发的，鉴于部分其他语言的用户难以在短时间部署
[AKShare](https://github.com/jindaxiang/akshare) 的 Python 使用环境，特此提供基于虚拟化容器技术 Docker 的使用教程。

## 安装 Docker

### 官方安装指导

1. Windows 10: [安装教程](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
2. Mac: [安装教程](https://docs.docker.com/docker-for-mac/install)
3. Ubuntu: [安装教程](https://docs.docker.com/engine/install/ubuntu)
4. CentOS: [安装教程](https://docs.docker.com/engine/install/centos)

### 第三方安装指导

1. [Docker 安装教程](https://www.runoob.com/docker/docker-tutorial.html)
2. 建议 Windows 7 和 8 的用户升级到 Windows 10 系统进行安装
3. [Windows 镜像下载地址](https://msdn.itellyou.cn/)

### 配置国内镜像

1. [Docker 国内镜像加速教程](https://www.runoob.com/docker/docker-mirror-acceleration.html)
2. 请在国内使用的用户务必进行该项配置, 从而加速获取镜像的速度.

## AKDocker 镜像使用

### 拉取 AKDocker 镜像

```
docker pull registry.cn-hangzhou.aliyuncs.com/akshare/akdocker
```

### 运行 AKDocker 容器

```
docker run -it registry.cn-hangzhou.aliyuncs.com/akshare/akdocker python
```

### 测试 AKDocker 容器

```python
import akshare as ak
ak.__version__
```

## 使用 JupyterLab 环境

### 配置

```
docker run -it -p 8888:8888 --name akdocker -v /c/home:/home registry.cn-hangzhou.aliyuncs.com/akshare/akdocker jupyter-lab --allow-root --no-browser --ip=0.0.0.0
```

1. 其中 Windows 系统的路径如: ```C:\home``` 需要改写为: ```/c/home``` 的形式;
2. 打开本地游览器输入地址: ```http://localhost:8888```;
3. 将 Terminal 显示出来的 Jupyterlab 路径中的 token 复制显示出来的 Jupyterlab 的界面后点击登录;
4. 步骤 3 中的 token 为在 Terminal 显示出来: ```http://127.0.0.1:8888/lab?token=f398812e277e8f09848eb04b2c9123a6206fbda6694da3cb``` 中的 ```f398812e277e8f09848eb04b2c9123a6206fbda6694da3cb``` 部分;
5. 在本地游览器中的 JupyterLab 界面进入 ```home``` 文件夹, 该目录内容会与本地的 ```C:\home``` 保持同步, 可以在此编辑 notebook 文件和导入数据到该文件夹从而在本地的 ```C:\home``` 文件夹下获取数据;
