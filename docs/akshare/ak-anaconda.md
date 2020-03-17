# [AkShare](https://github.com/jindaxiang/akshare) 环境配置

## Anaconda 安装说明

Anaconda 是集成了上千个常用库的 Python 发行版本, 通过安装 Anaconda 能简化环境管理工作, 非常推荐使用. 
作者基于目前 Python2 即将停止更新, 且目前大部分使用者电脑系统基本都是 64 位, 所以建议选择 Python3.7.3 64 位版本
同时, 根据您电脑的操作系统选择相对应的版本: Windows 版, MacOS 或 Linux 版的 64 位安装包.

## Anaconda 安装演示

**以 64 位 windows 版本为例**

下图中红框为 64 位 Windows 选择的版本:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_download.png)

在这里, 作者建议下载 Anaconda3-2019.07, 点击下载 [最新版 Anaconda 官方下载链接](https://repo.anaconda.com/archive/Anaconda3-2019.07-Windows-x86_64.exe)

双击如下图标进行安装:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_icon.png)

点击 Next:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_1.png)

点击 I Agree:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_2.png)

点击 Just me --> Next:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_3.png)

修改 Destination Folder 为如图所示:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_4.png)

勾选下图红框选项(以便于把安装的环境加入系统路径) --> Install:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_5.png)

安装好后, 找到 Anaconda Prompt 窗口:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt.png)

输入 python, 如果如下图所示, 即已经在系统目录中安装好 anaconda3 的环境. 

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_1.png)

创建虚拟环境命令:

```
conda create -n ak_test python=3.7.3
```

输入上述命令后出现确认, 输入 y

```
Proceed 输入 y
```

显示出最后一个红框内容则创建虚拟环境成功.

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_2.png)

在虚拟环境中安装 [AkShare](https://github.com/jindaxiang/akshare). 输入如下内容, 会在全新的环境中自动安装所需要的依赖包

激活已经创建好的 ak_test 虚拟环境

```
conda activate ak_test
```

在 ak_test 虚拟环境中安装并更新 [AkShare](https://github.com/jindaxiang/akshare)

```
pip install akshare --upgrade
```

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_3.png)

在安装完毕后, 输入 **python** 进入虚拟环境中的 Python

```
python
```

在 ak_test 虚拟环境的 Python 环境里面输入:

```python
import akshare as ak
ak.__doc__
```

显示出如下图则虚拟环境和 [AkShare](https://github.com/jindaxiang/akshare) 安装成功:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_4.png)

还可以在 ak_test 虚拟环境的 Python 环境中输入如下代码可以显示 [AkShare](https://github.com/jindaxiang/akshare) 的版本

```python
import akshare as ak
ak.__version__
```