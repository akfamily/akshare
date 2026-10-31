# AI 助手（MCP）

[AKTools](https://github.com/akfamily/aktools) 内置了 [MCP](https://modelcontextprotocol.io/)（Model Context Protocol，模型上下文协议）服务。接入后，可以直接在 Claude、Cursor 等 AI 助手中用自然语言获取 AKShare 的数据，例如“帮我查一下贵州茅台 2024 年 10 月 8 日到 11 日的日线行情”，助手会自己查找接口、填写参数并取回数据。

安装 AKTools 时已经包含 MCP 服务，不需要额外安装。AKTools 也已上架 [MCP 官方注册表](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.akfamily/aktools)，名称为 `io.github.akfamily/aktools`，支持从注册表安装的客户端可以直接搜索添加。

(mcp-examples)=
## 可以问什么

下面是在 Claude Code 中实际提问的过程（根据真实会话记录回放）：

![在 Claude Code 中提问，AI 助手通过 AKTools 的 MCP 工具查询贵州茅台的日线行情](https://aktools.akfamily.xyz/img/mcp-demo.gif)

更多示例：

- “帮我查一下贵州茅台 2024 年 10 月 8 日到 11 日的前复权日线行情”
- “AKShare 里有哪些和可转债相关的接口？”
- “stock_zh_a_hist 这个接口有哪些参数，复权方式怎么填？”

助手每次最多取回 1000 行数据（默认 100 行），适合查看具体某段时间、某只证券的数据。需要完整的大表格时，请让助手给出 CSV 下载地址（HTTP 方式），或改用 {doc}`HTTP API <aktools>` 下载。

(mcp-modes)=
## 两种接入方式

| 方式 | 怎么用 | 适合 |
| --- | --- | --- |
| stdio（推荐） | 由 AI 助手自动启动 `aktools-mcp` 命令，不需要先运行服务 | 个人在自己电脑上使用 |
| HTTP | 先运行 `python -m aktools`，助手连接 `http://127.0.0.1:8080/mcp` | 多人或多台电脑共用一个服务 |

两种方式提供的工具完全相同。

(mcp-stdio)=
## stdio 方式

推荐用 [uv](https://docs.astral.sh/uv/) 的 `uvx` 启动：它会自动下载并在独立环境中运行 AKTools，不需要事先用 pip 安装。请先按{doc}`uv 环境配置 <uv>`安装 uv。

`````{tab-set}

````{tab-item} Claude Desktop

打开设置中的“开发者 → 编辑配置”，在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "aktools": {
      "command": "uvx",
      "args": ["--from", "aktools", "aktools-mcp"]
    }
  }
}
```

保存后重启 Claude Desktop。
````

````{tab-item} Claude Code

在命令行中运行：

```shell
claude mcp add aktools -- uvx --from aktools aktools-mcp
```
````

````{tab-item} Cursor

点击按钮一键添加：

[![Add AKTools MCP server to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=aktools&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJha3Rvb2xzIiwiYWt0b29scy1tY3AiXX0%3D)

也可以在项目的 `.cursor/mcp.json`（或全局的 `~/.cursor/mcp.json`）中手动添加：

```json
{
  "mcpServers": {
    "aktools": {
      "command": "uvx",
      "args": ["--from", "aktools", "aktools-mcp"]
    }
  }
}
```
````

`````

```{tip}
第一次启动时，`uvx` 需要下载 AKShare 等依赖（约 150 MB），可能需要几分钟，客户端可能提示连接超时，下载完成后重启客户端即可。国内网络可以在配置中加上镜像源，例如在 `aktools` 下添加 `"env": {"UV_INDEX_URL": "https://mirrors.aliyun.com/pypi/simple/"}`；刚发版后镜像可能还没有同步新版本，详见 [AKTools 常见问题](https://aktools.akfamily.xyz/faq/#faq-mirror)。需要代理或调整超时时，同样在 `env` 中加上 `AKTOOLS_PROXY`、`AKTOOLS_TIMEOUT`，详见[代理与超时](https://aktools.akfamily.xyz/deploy/#network)。
```

`aktools mcp` 与 `aktools-mcp` 两个命令作用相同，MCP 官方注册表中登记的启动方式是 `uvx aktools mcp`。已经用 pip 安装了 AKTools 时，也可以把 `command` 设为 `aktools-mcp`、去掉 `args`。这要求客户端能在 PATH 中找到该命令；找不到时，请改用命令的完整路径（Windows 上可用 `where aktools-mcp` 查看，macOS 和 Linux 上用 `which aktools-mcp`）。

(mcp-http)=
## HTTP 方式

先启动服务：

```shell
python -m aktools
```

然后在支持 Streamable HTTP 的客户端中填写 `http://127.0.0.1:8080/mcp`，例如 Claude Code：

```shell
claude mcp add --transport http aktools http://127.0.0.1:8080/mcp
```

Cursor 则在 `mcp.json` 中使用 `"url": "http://127.0.0.1:8080/mcp"` 代替 `command` 与 `args`。使用过程中服务需要保持运行。

服务设置了[访问令牌](https://aktools.akfamily.xyz/deploy/#token)时，需要在客户端配置中加上请求头，例如 Claude Code：

```shell
claude mcp add --transport http aktools http://127.0.0.1:8080/mcp --header "Authorization: Bearer <令牌>"
```

Cursor 则在 `mcp.json` 的 `aktools` 下加上 `"headers": {"Authorization": "Bearer <令牌>"}`。`get_data` 返回的 CSV 下载地址不含令牌，下载时需要自行加上 `_token=<令牌>`。

(mcp-tools)=
## 提供的工具

AKShare 有一千多个接口，如果逐个注册成工具，会占满助手的上下文。因此 AKTools 只提供 3 个通用工具，由助手分步使用：

| 工具 | 作用 |
| --- | --- |
| `search_interfaces` | 按关键词搜索接口，返回接口名与中文标题，最多 50 个 |
| `describe_interface` | 查看接口的参数、默认值和说明 |
| `get_data` | 传入接口名和参数获取数据，默认最多返回 100 行，可用 `max_rows` 调整，最多 1000 行 |

数据超过返回行数时，`get_data` 会给出总行数。HTTP 方式下还会给出完整数据的 CSV 下载地址，例如 `/api/public/stock_zh_a_daily?symbol=sh600519&_format=csv`，在地址前加上服务地址即可下载；stdio 方式没有 HTTP 服务，因此不提供下载地址。

`get_data` 与 HTTP API 的 `/api/public` 使用同一套逻辑，同样经过[数据缓存](https://aktools.akfamily.xyz/guide/usage/#cache)，出错时的说明也相同。参数值一律按文本传给 AKShare，日期通常写成 `20240101` 的形式。

(mcp-lan)=
## 局域网访问

为了防止恶意网页通过浏览器访问本机服务（DNS 重绑定攻击），HTTP 方式下服务只监听本机时，MCP 只接受发往 `127.0.0.1`、`localhost` 的请求。需要让其他电脑上的 AI 助手访问时，指定监听地址启动：

```shell
python -m aktools --host 0.0.0.0
```

其他电脑使用 `http://<本机 IP>:8080/mcp` 连接。用 Gunicorn 部署时，请通过环境变量 `AKTOOLS_HOST` 告诉 AKTools 实际的监听地址，详见 [AKTools 部署文档](https://aktools.akfamily.xyz/deploy/#production)。

```{warning}
未设置[访问令牌](https://aktools.akfamily.xyz/deploy/#token)时，能访问到 `/mcp` 的人都可以通过它获取数据。多人共用或经公网访问时，请设置访问令牌。
```

## 更多详情

[参见 AKTools 文档中的 AI 助手（MCP）](https://aktools.akfamily.xyz/guide/mcp/)
