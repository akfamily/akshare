# HTTP API（AKTools）

## 说明

AKShare HTTP 版本的部署主要依赖 AKTools、AKShare、FastAPI、Uvicorn、Typer 等开源 Python 库，部署的核心程序在 AKTools 中。
非常感谢给 [AKTools 项目](https://github.com/akfamily/aktools) 点 Star，您的支持是我们持续开发最大的动力！

AKTools 同时内置了 MCP 服务，可以在 Claude、Cursor 等 AI 助手中直接用自然语言获取数据，详见{doc}`AI 助手（MCP） <mcp>`。

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

请安装 AKTools 的最新版本，它包含以下功能：

1. HTTP API：通过 `/api/public/<接口名>` 获取数据，可返回 JSON、CSV 或 Excel
2. MCP 服务：供 AI 助手调用，见{doc}`AI 助手（MCP） <mcp>`
3. 可选的访问令牌（`--token`）、数据缓存、代理与超时设置

## 更多详情

[参见 AKTools 项目文档](https://aktools.akfamily.xyz/)
