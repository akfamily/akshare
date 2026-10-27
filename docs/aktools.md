# HTTP API（AKTools）

## 说明

AKShare HTTP 版本的部署主要依赖 AKTools、AKShare、FastAPI、Uvicorn、Typer 等开源 Python 库，部署的核心程序在 AKTools 中。
非常感谢给 [AKTools 项目](https://github.com/akfamily/aktools) 点 Star，您的支持是我们持续开发最大的动力！

## 快速启动

### 安装库

```shell
pip install aktools
```

### 运行库

```shell
python -m aktools
```

默认只监听 `127.0.0.1`，仅本机可以访问。部署在服务器上供其他机器调用时，需要指定监听地址和端口：

```shell
python -m aktools --host 0.0.0.0 --port 8080
```

启动后访问 `http://服务器地址:8080/docs` 查看接口文档。

```{note}
AKShare 不再提供 Docker 镜像。需要容器化部署时，可以参考 [AKTools 项目](https://github.com/akfamily/aktools) 自行构建镜像，在镜像中执行 `pip install aktools` 并以上面的命令启动。
```

## 版本说明

1. 仅体验 HTTP API 功能则只需要安装：`pip install aktools==0.0.68` 版本；
2. 体验完整功能请安装最新版，支持用于认证、权限、可视化页面等更多功能。

## 更多详情

[参见 AKTools 项目文档](https://aktools.akfamily.xyz/)
