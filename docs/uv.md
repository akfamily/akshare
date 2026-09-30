# [AKShare](https://github.com/akfamily/akshare) uv 环境配置

## uv 简介

[uv](https://docs.astral.sh/uv/) 是 Astral 开发的 Python 包与项目管理工具，可以安装 Python、创建虚拟环境并安装依赖，速度快且不依赖其他工具，[AKShare](https://github.com/akfamily/akshare) 项目本身也使用 uv 进行开发。推荐使用 uv 来配置 [AKShare](https://github.com/akfamily/akshare) 的运行环境。

如果需要在 R 语言或 MATLAB 中调用 [AKShare](https://github.com/akfamily/akshare)，或者习惯使用 Anaconda，请参考 [AKShare Anaconda 环境配置](https://akshare.akfamily.xyz/anaconda.html)。

## 安装 uv

### Windows

在 PowerShell 中运行：

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS 和 Linux

在终端中运行：

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 通过 pip 安装

如果本机已经安装了 Python，也可以通过 pip 安装 uv，国内用户可以使用镜像源加速：

```
pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple
```

安装完成后重新打开终端，输入 `uv --version`，显示版本号即表示安装成功。

## 安装 Python

[AKShare](https://github.com/akfamily/akshare) 支持 Python 3.11 及以上版本，推荐使用 Python 3.13：

```
uv python install 3.13
```

如果本机已经安装了符合要求的 Python，可以跳过此步骤，uv 会自动使用本机已安装的版本。

## 方式一：虚拟环境

该方式与直接使用 pip 最接近，适合在命令行或 JupyterLab 中直接使用 [AKShare](https://github.com/akfamily/akshare)，推荐新手使用。

1. 创建并进入工作目录，在其中创建 Python 3.13 的虚拟环境：

```
mkdir ak_test
cd ak_test
uv venv --python 3.13
```

2. 激活虚拟环境。Windows 中运行：

```
.venv\Scripts\activate
```

macOS 和 Linux 中运行：

```
source .venv/bin/activate
```

3. 在虚拟环境中安装并更新 [AKShare](https://github.com/akfamily/akshare)：

```
uv pip install akshare --upgrade
```

国内用户可以使用镜像源加速：

```
uv pip install akshare --upgrade --default-index https://pypi.tuna.tsinghua.edu.cn/simple
```

4. 验证安装，显示版本号即表示安装成功：

```
python -c "import akshare as ak; print(ak.__version__)"
```

如需使用 JupyterLab，在已激活的虚拟环境中安装并启动：

```
uv pip install jupyterlab
jupyter lab
```

## 方式二：项目管理

该方式适合编写量化研究代码、需要固定依赖版本的场景。uv 会在 `pyproject.toml` 和 `uv.lock` 中记录依赖及其版本，便于在其他计算机上复现相同的环境。

1. 创建项目并添加 [AKShare](https://github.com/akfamily/akshare)：

```
uv init ak_project --python 3.13
cd ak_project
uv add akshare
```

国内用户可以使用镜像源加速，该命令会把镜像源写入项目的 `pyproject.toml`，之后在此项目中添加其他依赖也会使用该镜像源：

```
uv add akshare --default-index https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 运行代码，无需手动激活虚拟环境：

```
uv run python your_script.py
```

3. 升级 [AKShare](https://github.com/akfamily/akshare) 到最新版本：

```
uv add akshare --upgrade-package akshare
```

如需使用 JupyterLab，将其添加为开发依赖后启动：

```
uv add --dev jupyterlab
uv run jupyter lab
```

## 常见问题

### 下载 Python 速度慢

`uv python install` 默认从 GitHub 下载 Python，国内网络环境下可能较慢。可以通过 `--mirror` 参数指定镜像地址，也可以先从 [Python 官网](https://www.python.org/downloads/) 下载安装 Python 3.11 及以上版本，uv 会自动使用本机已安装的 Python。

### 每次都需要指定镜像源

可以设置环境变量 `UV_DEFAULT_INDEX`，之后 uv 会默认使用该镜像源。Windows 中运行：

```
setx UV_DEFAULT_INDEX "https://pypi.tuna.tsinghua.edu.cn/simple"
```

macOS 和 Linux 中，将如下内容添加到 `~/.bashrc` 或 `~/.zshrc`：

```
export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
```

设置完成后需要重新打开终端才能生效。

### 导入 AKShare 失败

运行代码时，文件名、文件夹名不能是 akshare，否则会与 [AKShare](https://github.com/akfamily/akshare) 本身冲突导致导入失败。
