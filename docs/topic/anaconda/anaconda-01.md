# Anaconda 库管理

以下是本文要解答的问题：

1. Anaconda 导航器有哪些常用功能？
2. 如何在 Anaconda 里安装、升级、删除 Python 支持库？
3. 怎么安装 Anaconda 里没有的 Python 支持库？

## 1. Anaconda 导航器有哪些功能？

点击菜单里的第一个绿色图标，启动导航器。

![](https://upload-images.jianshu.io/upload_images/3240514-4d8d45bcf8fc4f20.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

先看左边导航条：

![](https://upload-images.jianshu.io/upload_images/3240514-fccc707fb1b069d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* **Home**，常用，列出了常用工具；
* **Environment**，常用，Python 支持库管理，安装、删除、升级都在这里操作；
* **Learning**，不常用，列出了各种学习资源，有 Python 的，Pandas 的，有文档，也有视频，不过都是英文的，视频是油管的；
* **Community**，不常用，各种社区，Anaconda 、NumPy 、Bokeh、Blaze、Stack Overflow 等等，英文好的可以去看。

### Home 界面

Home 界面比较常用，这里简单介绍下这里提供的几个软件工具：

![](https://upload-images.jianshu.io/upload_images/3240514-868ab3d81db63c63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* Jupyter Notebook，数据分析神器；
* Jupyter Lab，Jupyter Notebook 升级版，可以很方便的管理多个文件；
* Spyder，老牌 IDE；
* VSCode，微软推出的 IDE，现在很潮，插件很多，界面美观，一直在升级；
* GlueViz，多维数据可视化工具；
* Orange 3，交互式数据挖掘与可视化工具箱；
* RStudio，R 语言的 IDE。

![](https://upload-images.jianshu.io/upload_images/3240514-6787da5facc72571.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 点击 **Launch** 打开指定工具；
* 点击 **Install** 安装指定工具；
* 点击**齿轮**，也就是设置图标，可以安装（Install）、升级（Update）、删除（Remove）指定工具，还可以安装指定版本（Install specific version）。

![](https://upload-images.jianshu.io/upload_images/3240514-76a3883805618ef7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### Environment

![](https://upload-images.jianshu.io/upload_images/3240514-1b0d0de452790fbf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在这个菜单打开命令窗口（Terminal），注意这里的 base，指的就是 Anaconda 的基础环境，可以在这里安装 Anaconda 未内置的 Python 支持库；

![](https://upload-images.jianshu.io/upload_images/3240514-3e16b12498c67a87.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还可以打开 Python 编程环境，最原始的。。。那种；

![](https://upload-images.jianshu.io/upload_images/3240514-50cb6fe91d65b20d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还可以打开 IPython 和 Jupyter Notebook，就不截图了。

![](https://upload-images.jianshu.io/upload_images/3240514-3f1ffed36e483901.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

中间下方的这几个按钮是创建（Create）、克隆（Clone）、导入（Import）、删除（Remove）虚拟环境的，等小白阶段过了，就用的上了。自己没事，也可以尝试一下怎么创建虚拟环境，虚拟环境最大的好处是可以分版本管理支持库，而且可以去掉无用的支持库，在分享源代码时，可以生成编码环境文件，便于在不同电脑上配置适合你编写的代码的编程环境。

![](https://upload-images.jianshu.io/upload_images/3240514-a8dfbea6dae4a2e8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

界面右侧是 Python 支持库管理界面，这个菜单是分类查询安装过的（Installed）、没安装的（Not installed）、可升级的（Updatable）、选中的（Selected）、及全部 （All）Anaconda 预置的 Python 支持库。

**Channels** 是用来设置安装镜像服务器的，有的时候国外镜像安装慢，就需要添加国内镜像；

**Update index** 是更新下方 Python 支持库索引的，用命令窗口（Terminal）安装了 Python 支持库后，在这里刷新；

**Search Packages** 是用来搜索 Python 支持库的，试着搜索 Pandas、Numpy，就可以看到 Anaconda 已经预安装了；

红框里的数字是 Python 支持库的版本号。


## 2. 如何在 Anaconda 里安装、升级、删除 Python 支持库？

### 安装

![](https://upload-images.jianshu.io/upload_images/3240514-8420433c6fba4b4c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
方框里没有打钩的，代表没有安装过的支持库，点击方框，再点击界面右下角的 Apply 按钮，就可以安装了。

![绿色的下载标识](https://upload-images.jianshu.io/upload_images/3240514-c2de164e0b6245f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![点击 Apply 安装](https://upload-images.jianshu.io/upload_images/3240514-bd0bccf1bda58dce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 升级

![](https://upload-images.jianshu.io/upload_images/3240514-a9282faf3bb0be62.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

版本号为蓝色，且有上升箭头时，表示可以升级。也可以通过筛选可升级（Updatable）查看所有已安装，且可升级的支持库；

点击方框，选择 **Mark for update**，再点 Apply，即可升级选中支持库；

### 删除

点击方框，选择 **Mark for removal**（见上图红框下方的菜单项），再点 Apply，即可删除选中支持库；

## 3. 怎么安装 Anaconda 里没有的 Python 支持库？

### pip 安装

比如呆鸟想安装 **styleframe**， 但是 Anaconda 内置的库里没有，怎么办？
没问题，首先，在 Anaconda 里打开 Terminal；

![打开 Terminal](https://upload-images.jianshu.io/upload_images/3240514-3024bf6c4f42fd56.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

输入 `pip install styleframe`，回车，就可以安装了。

![](https://upload-images.jianshu.io/upload_images/3240514-9899df7689e66d96.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

不过，用 pip 安装有一个缺陷，就是没办法在 Anaconda 导航器的环境里看到安装过的支持库，只能用 pip 查看，不太方便。

### conda 安装

**那怎么才能安装完支持库以后，在导航器里也能看到呢？**

以 django 为例，12 月 2 日，django 3.0 已经推出了，昨天呆鸟还发文介绍了一下，详见[《紧急插播，Django 3.0 已发布》](https://mp.weixin.qq.com/s/ksClnUERnA_aY3ADHx4PRw)一文。但用 Anaconda 里显示的还是 2.25，我们想安装 3.0 怎么弄？

![](https://upload-images.jianshu.io/upload_images/3240514-e23cac3eb5415451.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还是进入 Terminal， 输入 `conda install -c conda-forge django`，就可以安装了。

> 这里简单介绍一下这个命令，conda 是一种类似 pip 的支持库管理系统，-c 是指定安装的渠道，conda-forge 则是一个很流行的 Python 支持库发布渠道，django 就是要安装的支持库。作为小白，目前知道这些就够了。

![](https://upload-images.jianshu.io/upload_images/3240514-4262493e496224e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装过程中会问你要不要继续，输入 `y`，回车就可以了。

![](https://upload-images.jianshu.io/upload_images/3240514-dbd16355a2a3c3be.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装完成以后，在导航器里点击 **Update index**  刷新，就可以看到了 Django 3.0 已经安装好了。

![](https://upload-images.jianshu.io/upload_images/3240514-000d263ca9d9f6f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)