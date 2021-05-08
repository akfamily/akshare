# [AKShare](https://github.com/jindaxiang/akshare) Docker 部署

AKDocker is a dockerfile for AKShare's latest version

## Installation

### Install Docker

#### Windows

[安装教程](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

#### Mac

[Mac](https://docs.docker.com/docker-for-mac/install)

#### Ubuntu

[安装教程](https://docs.docker.com/engine/install/ubuntu)

#### CentOS

[安装教程](https://docs.docker.com/engine/install/centos)

### Command

#### Pull AKDocker

```
docker pull registry.cn-hangzhou.aliyuncs.com/akshare/akdocker
```

#### Run AKDocker

```
docker run -it registry.cn-hangzhou.aliyuncs.com/akshare/akdocker python
```

#### Test AKDocker

```python
import akshare as ak
ak.__version__
```

### JupyterLab

```
docker run -it -p 8888:8888 --name akdocker -v /c/home:/home registry.cn-hangzhou.aliyuncs.com/akshare/akdocker jupyter-lab --allow-root --no-browser --ip=0.0.0.0
```

1. 其中 Windows 系统的路径如: ```C:\home``` 需要改写为: ```/c/home``` 的形式;
2. 打开本地游览器输入地址: ```http://localhost:8888```;
3. 将 Terminal 显示出来的 Jupyterlab 路径中的 token 复制显示出来的 Jupyterlab 的界面后点击登录;
4. 其中的 token 为: ```http://127.0.0.1:8888/lab?token=f398812e277e8f09848eb04b2c9123a6206fbda6694da3cb``` 中的 ```f398812e277e8f09848eb04b2c9123a6206fbda6694da3cb```;
5. 在本地游览器中的 Jupyterlab 界面进入 ```home``` 文件夹, 该目录内容会与本地的 ```C:\home``` 保持同步, 可以在此编辑 notebook 文件
