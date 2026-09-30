# [AKShare](https://github.com/akfamily/akshare) Anaconda 环境配置

推荐使用 uv 来配置 [AKShare](https://github.com/akfamily/akshare) 的运行环境，详见 [AKShare uv 环境配置](https://akshare.akfamily.xyz/uv.html)。本页适用于需要在 R 语言或 MATLAB 中调用 [AKShare](https://github.com/akfamily/akshare)，或者习惯使用 Anaconda 的用户。

## Anaconda 安装说明

Anaconda 是集成上千个常用库的 Python 发行版本，自带图形界面和 JupyterLab 等工具，可以简化环境管理工作。

注意：Anaconda 官方默认渠道（defaults）的服务条款要求 200 人及以上的企业、政府和非营利组织购买商业授权，在单位中使用前请先确认 [Anaconda 服务条款](https://www.anaconda.com/legal)；也可以改用社区维护的 [Miniforge](https://github.com/conda-forge/miniforge)，它默认使用免费的 conda-forge 渠道，本页中的 conda 命令同样适用。

作者建议根据您计算机的操作系统选择相应版本的安装包，国内用户可以点击链接访问 [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/) 来加速下载最新的 64 位安装包。
国外用户可以访问 [Anaconda 官网](https://www.anaconda.com/products/individual) 下载最新的 64 位安装包。

## Anaconda 安装演示

**以 64 位 Windows 版本 Anaconda3-2019.07 为例**

下图中红框为 64 位 Windows 选择的版本：

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_download.png)

下载完成后双击如下图标进行安装：

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_icon.png)

点击 Next:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_1.png)

点击 I Agree:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_2.png)

点击 Just me --> Next:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_3.png)

修改 Destination Folder 为如图所示：

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_4.png)

勾选下图红框选项（以便于把安装的环境加入系统路径） --> Install:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_5.png)

安装好后，找到 Anaconda Prompt 窗口：

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt.png)

输入 python，如果如下图所示，即已经在系统目录中安装好 anaconda3 的环境。

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_1.png)

创建虚拟环境命令，此处指定推荐的 Python 3.13 版本，AKShare 支持 Python 3.11 及以上版本：

```
conda create -n ak_test python=3.13
```

输入上述命令后出现确认，输入 y

```
Proceed 输入 y
```

显示出最后一个红框内容则创建虚拟环境成功。

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_2.png)

在虚拟环境中安装 [AKShare](https://github.com/akfamily/akshare). 输入如下内容，会在全新的环境中自动安装所需要的依赖包

激活已经创建好的 ak_test 虚拟环境

```
conda activate ak_test
```

在 ak_test 虚拟环境中安装并更新 [AKShare](https://github.com/akfamily/akshare)

```
pip install akshare --upgrade
```

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_3.png)

在安装完毕后，输入 `python` 进入虚拟环境中的 Python

```
python
```

在 ak_test 虚拟环境的 Python 环境里面输入：

```python
import akshare as ak

print(ak.__doc__)
```

显示出如下图则虚拟环境和 [AKShare](https://github.com/akfamily/akshare) 安装成功：

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_4.png)

还可以在 ak_test 虚拟环境的 Python 环境中输入如下代码可以显示 [AKShare](https://github.com/akfamily/akshare) 的版本信息

```python
import akshare as ak

print(ak.__version__)
```
