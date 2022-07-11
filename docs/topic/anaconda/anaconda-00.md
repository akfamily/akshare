# Anaconda 安装

本文要解决的问题如下：

1. 为什么是 Anaconda 的 Jupyter Notebook ？
2. 在哪里下载 Anaconda，怎么选版本？
3. 怎么安装 Anaconda ？

## 1. 为什么是 Anaconda 的 Jupyter Notebook？

有关 Jupyter Notebook 的优点上一篇文章里已经说过了，再重复一下，就是**上手简单、结果直观，为数据分析工作进行过专门优化**。其他的就不细说了。

Jupyter Notebook 可以直接安装，微软的 VSCode 也内置支持 Jupyter Notebook，那为什么我要推荐安装 Anaconda？用 Anaconda 里面带着的 Jupyter Notebook 呢？原因如下：

* Anaconda 是专门为数据科学、数据分析优化过的 Python 数据开发平台；
* Anaconda 内置了数百个 Python 支持库，并预安装了大部分数据分析所需的 Python 支持库，无需自己安装，比如 Pandas、Numpy、Scikit-learn 这些都已经安装好了；
* Anaconda 提供了图形化界面，可以轻松安装、升级、卸载 Python 支持库，查看版本也十分方便；
* Anaconda 与 VSCode 与 Pycharm 实现无缝连接，这两个 IDE 是从小白到专家后最流行的两个 IDE，扩展性能好；
* Anaconda 还内置了很多知名的数据开发工具，除了 Jupyter Notebook 外，还有 Jupyter Lab 等。

## 2. 在哪里下载 Anaconda，怎么选版本？

* 下载地址
  [www.anaconda.com/distribution#download-section](https://www.anaconda.com/distribution/#download-section)
  ![](https://upload-images.jianshu.io/upload_images/3240514-bc20462b4e0db65e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 选择版本
  见上图，根据自己的操作系统、Python 版本、系统是 32 位，还是 64 位，这几个条件进行选择，不推荐用 Python 2.7 版，推荐用 Python 3.7 版。比如呆鸟用的就是 windows 版、Python 3.7 版、64 位系统的 Anaconda。安装文件见下图：

![](https://upload-images.jianshu.io/upload_images/3240514-25c7ad86364be7df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 下载方式
  国外地址下载较慢，推荐用百度网盘离线下载，多次亲测秒下，再从百度网盘下载到本机电脑，也可以用迅雷下载，不建议直接用浏览器下载，速度很慢。

## 3. 怎么安装 Anaconda ？

因条件有限，本文仅以 Windows 系统、Python 3.7 版、64 位系统的 Anaconda 安装为例，macOS，Linux 的用户如不会安装，请在网上搜索安装方法。

* 双击安装文件 **Anaconda3-2019.10-Windows-x86_64.exe**，进入安装界面，点击 **Next**。

![](https://upload-images.jianshu.io/upload_images/3240514-cc7242450311d1db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击 **I Agree**，同意 Anaconda 的协议。

![](https://upload-images.jianshu.io/upload_images/3240514-ac495e5b8303a230.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

呆鸟一般选择 **Just Me**，这也是建议安装选项，当然，选 **All Users**，为电脑上的所有用户安装也未尝不可。选好了以后点击 **Next** 继续。

![](https://upload-images.jianshu.io/upload_images/3240514-f6f92f4cbd05bb3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在下图显示的界面选择安装目录，如果以前安装过 Anaconda，且默认目录不为空，会提示不能使用该目录，要先删除旧版 Anaconda。Anaconda 占差不多 3G 的空间，随着安装 Python 支持库的增加，可能还会更多。点击 **Next** 继续。

![](https://upload-images.jianshu.io/upload_images/3240514-caee554edd421671.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下图显示的界面里，默认第一个勾选框是没有选中的，**需要自己点选**，这个选项说的是把 **Anaconda 添加为 PATH 环境参数**，意思是告诉 Windows 在哪里找到 Anaconda 的程序，虽然选中会有红字提示不建议选择此选项，有可能会引发问题，让自己去设置，但从呆鸟无数次安装 Anaconda 的经验来看，选中更好，当然前提是，你之前的安装目录是默认目录，否则，今天把 Anaconda 装一个目录下，明天装到另一个，后天又换，系统就懵圈了，自然会出现问题。

> 建议小白选择这个选项，不要自己去设置。

第二个选项是默认就有的，不要取消，该选项的目的是把 Anaconda 与 Python 3.7 版的文件相关联。

点击 **Install**，开始正式安装。

![](https://upload-images.jianshu.io/upload_images/3240514-ca548e0cf5f13825.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Anaconda 的安装与卸载时间都比较长，要耐心等待，文件太多了，根据电脑速度，五六分钟到十几二十分钟不等。**以呆鸟电脑的速度就需要四十分钟来卸载、安装，为了给大家写原创，呆鸟特地卸载重装了 Anaconda，不容易啊，能看到这里的朋友，给点个在看 / 喜欢吧，也不枉呆鸟辛苦一番**。

![](https://upload-images.jianshu.io/upload_images/3240514-c4d3fffa03197951.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

终于安装完啦！在这个界面你会看到 Anaconda 推荐 PyCharm，记住右下角写着 PC 图标，说不定就是以后常用的工具。点击 **Next** 继续。

![](https://upload-images.jianshu.io/upload_images/3240514-7068d1b70bb41f30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下图界面里有两个选项，一个是了解 Anaconda 云，另一个是上手 Anaconda 教程，呆鸟就不选了。

点击 **Finish** 完成安装。

![](https://upload-images.jianshu.io/upload_images/3240514-3f4475a6be0e8486.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

至此，Anaconda 的安装就完成了，在 Windows 程序菜单里，可以看到安装的内容。

![](https://upload-images.jianshu.io/upload_images/3240514-ce5ff4e5cff2f5b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

简单介绍一下这几个快捷方式：

* 第一个绿色图标是 Anaconda 的导航器（常用）；
* 第二、三个黑色图标是 PowerShell 的命令窗与 Anaconda 的命令窗口，这两个窗口适合有点基础的人，执行安装 Anaconda 自带导航器不支持的 Python 支持库等操作；
* 第三、四个橙色图标就是今后最常用的 Jupyter Notebook 了，第三个是我们要用的，不过呆鸟一般不从这里启动 Jupyter，那呆鸟从哪里启动呢?下篇告诉大家；
* 第四个白色图标是用来重置 Spyder IDE 设置的；
* 第五个花色图标就是 Spyder IDE，但呆鸟不是特别推荐，等过了小白阶段，完全可以用 VSCode 或 PyCharm 这两个更流行的 IDE。
