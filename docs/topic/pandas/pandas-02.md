# Pandas 25 式

Kevin Markham，数据科学讲师，2002 年，毕业于范德堡大学，计算机工程学士，2014 年，创建了 Data School，在线教授 Python 数据科学课程，他的课程主要包括 Pandas、Scikit-learn、Kaggle 竞赛数据科学、机器学习、自然语言处理等内容，迄今为止，浏览量在油管上已经超过 500 万次。

![Kevin Markham](https://upload-images.jianshu.io/upload_images/3240514-af20f82be79a1e87.png)

Kevin 还是 PyCon 培训讲师，主要培训课程如下：

* PyCon 2016，用 Scikit-learn 机器学习技术处理文本
* PyCon 2018，如何用 Pandas 更好（或更糟）地实现数据科学
* PyCon 2019，Pandas 数据科学最佳实践

本文基于 Kevin 于 2019 年 7 月推出的最新视频教程，汇总了他 5 年来最喜欢的 25 个 pandas 操作技巧，希望大家喜欢。

![Data School](https://upload-images.jianshu.io/upload_images/3240514-c54dfa4e7530f806.png)

**目录**

 1.  查看 pandas 及其支持项的版本
 2.  创建 DataFrame
 3.  重命名列
 4.  反转行序
 5.  反转列序
 6.  按数据类型选择列
 7.  把字符串转换为数值
 8.  优化 DataFrame 大小
 9.  用多个文件建立 DataFrame ~ 按行
 10.  用多个文件建立 DataFrame ~ 按列
 11.  从剪贴板创建 DataFrame
 12.  把 DataFrame 分割为两个随机子集
 13.  根据多个类别筛选 DataFrame
 14.  根据最大的类别筛选 DataFrame
 15.  操控缺失值
 16.  把字符串分割为多列
 17.  把 Series 里的列表转换为 DataFrame
 18.  用多个函数聚合
 19.  用一个 DataFrame 合并聚合的输出结果
 20.  选择行与列
 21.  重塑多重索引 Series
 22.  创建透视表
 23.  把连续型数据转换为类别型数据
 24.  改变显示选项
 25.  设置 DataFrame 样式
 26.  彩蛋：预览 DataFrame

**文末有 Jupyter Notebook 下载**，正文先上图。

## 使用的数据集

原文的数据集是 bit.ly 短网址的，我这里在读取时出问题，不稳定，就帮大家下载下来，统一放到了 **data** 目录里。

```Python
drinks = pd.read_csv('data/drinks.csv')
movies = pd.read_csv('data/imdb_1000.csv')
orders = pd.read_csv('data/chipotle.tsv', sep='\t')
orders['item_price'] = orders.item_price.str.replace('$', '').astype('float')
stocks = pd.read_csv('data/stocks.csv', parse_dates=['Date'])
titanic = pd.read_csv('data/titanic_train.csv')
ufo = pd.read_csv('data/ufo.csv', parse_dates=['Time'])
```

本文中采用让数据集主要为常见的酒水饮料、IMDB 电影、泰坦尼克号、飞碟目击等数据集。

这里需要注意的是：

1） `pd.read_csv('data/chipotle.tsv', sep='\t')` 里的 chipotle.tsv，是用 **tab** 作为分隔符的，所以要增加参数 `sep=\t`；
2） `orders.item_price.str.replace('$', '').astype('float')`，**item_price** 列是带 **\$** 的文本，要用 `.str.replace('$', '').astype('float')` 去掉 **$**，再把该列数据类型改为 `float`；
3）`ufo.csv`里的 **Time** 列，要用 `parse_dates=['Time'])`，解析日期。

## 查看 pandas 及其支持项的版本

使用 `pd.__version__` 查看 pandas 的版本。

![](https://upload-images.jianshu.io/upload_images/3240514-c7aa827d938b1ff7.png)

查看所有 pandas 的支持项版本，使用 `show_versions` 函数。比如，查看 Python、pandas、Numpy、matplotlib 等支持项的版本。

![](https://upload-images.jianshu.io/upload_images/3240514-0ccf966df346093d.png)


## 创建 DataFrame

创建 DataFrame 的方式有很多，比如，可以把字典传递给 DataFrame 构建器，字典的 Key 是列名，字典的 Value 为列表，是 DataFrame 的列的值。

![](https://upload-images.jianshu.io/upload_images/3240514-e4851f53a9f96e7c.png)

如果 DataFrame 的数据较多，用字典的方式就不合适了，需要输入的东西太多。这时，可以用 Numpy 的 `random.rand()` 函数，设定行数与列数，然后把值传递给 DataFrame 构建器。

![](https://upload-images.jianshu.io/upload_images/3240514-2e4bcf49bae3e593.png)

这样就可以生成 DataFrame 了，但如果要用非数字形式的列名，需要强制把字符串转换为列表， 再把这个列表传给 `columns` 参数。

![](https://upload-images.jianshu.io/upload_images/3240514-eb8a9242d111a335.png)

这里要注意的是，字符串里的字符数量必须与 DataFrame 的列数一致。

## 重命名列

![](https://upload-images.jianshu.io/upload_images/3240514-68b189611799a36a.png)

用点（`.`）选择 pandas 里的列写起来比较容易，但列名里有空格，就没法这样操作了。

`rename()`方法改列名是最灵活的方式，它的参数是**字典**，字典的 Key 是**原列名**，值是**新列名**，还可以指定轴向（axis）。

![](https://upload-images.jianshu.io/upload_images/3240514-ef27d24ec8a2f26a.png)

这种方式的优点是可以重命名任意数量的列，一列、多列、所有列都可以。

还有一种简单的方式可以一次性重命名所有列，即，直接为列的属性赋值。

![](https://upload-images.jianshu.io/upload_images/3240514-5bc29d557a952b4f.png)

只想替换列名里的空格，还有更简单的操作，直接用 `str.replace` 方法，不必把所有的列名都敲一遍。

![](https://upload-images.jianshu.io/upload_images/3240514-7f727721f50b83e2.png)

以上这三种方式都可以更改列名。

用 `add_prefix` 与 `add_suffix` 函数可以为所有列名添加**前缀**或**后缀**。

![](https://upload-images.jianshu.io/upload_images/3240514-f0300b0c04aebc77.png)

![](https://upload-images.jianshu.io/upload_images/3240514-a962d3f6a021fde5.png)

## 反转列序

反转 `drinks` 表的顺序。

![](https://upload-images.jianshu.io/upload_images/3240514-50c4208dbd32f9f7.png)

这个数据集按国家列出了酒水平均消耗量，如果想反转列序该怎么办？

最直接的方式是把 `::-1` 传递给 `loc` 访问器，与 Python 里反转列表的切片法一样。

![](https://upload-images.jianshu.io/upload_images/3240514-805a0a371b550e52.png)

如果想让索引从 0 到 1，用 `reset_index()`方法，并用 `drop` 关键字去掉原有索引。 

![](https://upload-images.jianshu.io/upload_images/3240514-07bad1d76b3b4d4c.png)

这样，行序就已经反转过来了，索引也重置为默认索引。

## 反转列序

与反转行序类似，还可以用 `loc` 从左到右反转列序。

![](https://upload-images.jianshu.io/upload_images/3240514-05a59276595d6e24.png)

逗号前面的分号表示选择**所有行**，逗号后面的 `::-1` 表示**反转列**，这样一来，country 列就跑到最右边去了。

## 按数据类型选择列

首先，查看一下 **drinks** 的数据类型：

![](https://upload-images.jianshu.io/upload_images/3240514-f850c7b9d526addd.png)

选择所有**数值型**的列，用 `selec_dtypes()` 方法。

![](https://upload-images.jianshu.io/upload_images/3240514-4b04fa02df0b3708.png)

同样的方法，还可以选择所有字符型的列。

![](https://upload-images.jianshu.io/upload_images/3240514-7c8438563ffe3eb6.png)

同理，还可以用 `datetime` 选择日期型的列。

传递列表即可选择多种类型的列。

![](https://upload-images.jianshu.io/upload_images/3240514-b5efb8833da6b364.png)

还可以使用 `exclude` 关键字排除指定的数据类型。

![](https://upload-images.jianshu.io/upload_images/3240514-7aac62a17a77dc68.png)

## 把字符串转换为数值

再创建一个新的 DataFrame 示例。

![](https://upload-images.jianshu.io/upload_images/3240514-fc8d04a2da962936.png)

这个 DataFrame 里的数字其实是以字符串形式保存的，因此，列类型是 `object`。

![](https://upload-images.jianshu.io/upload_images/3240514-651b487a5b9b8ac8.png)

要想执行数学计算，要先把这些列的数据类型转换为数值型，下面的代码用 `astype()` 方法把前两列的数据类型转化为 `float`。 

![](https://upload-images.jianshu.io/upload_images/3240514-463d4859695b3ce9.png)

用这种方式转换第三列会出错，因为这列里包含一个代表 0 的下划线，pandas 无法自动判断这个下划线。

为了解决这个问题，可以使用 `to_numeric()` 函数来处理第三列，让 pandas 把任意无效输入转为 `NaN`。

![](https://upload-images.jianshu.io/upload_images/3240514-f31b8f2af4f7d975.png)

`NaN` 代表的是 0，可以用 `fillna()` 方法填充。

![](https://upload-images.jianshu.io/upload_images/3240514-2d3e51c034414b06.png)

一行代码就可以解决这个问题，现在所有列的值都转成 `float` 了。

![](https://upload-images.jianshu.io/upload_images/3240514-108da1d9cdd3335b.png)

## 优化 DataFrame 对内存的占用

pandas 的 DataFrame 设计的目标是把数据存到内存里，有时要缩减 DataFrame 的大小，减少对内存的占用。

下面显示了 **drinks** 占用的内存。 

![](https://upload-images.jianshu.io/upload_images/3240514-a6b5290d467c067f.png)

这里显示 **drinks** 使用了 30.5 KB 内存。

大型 DataFrame 会影响计算性能，甚至导致 DataFrame 读入内存失败，下面介绍简单几步，即可在读取 DataFrame 时减少内存占用。

第一步是只读取切实所需的列，这里需要指定 `usecols` 参数。

![](https://upload-images.jianshu.io/upload_images/3240514-de7536a2aa6ebcaf.png)

只选择两列以后，DataFrame 对内存的占用减少到 13.7 KB。

第二步是把包含类别型数据的 object 列转换为 Category 数据类型，通过指定 `dtype` 参数实现。

![](https://upload-images.jianshu.io/upload_images/3240514-f2985bbcc0dac727.png)

把 continent 列改为 category 数据类型后，DataFrame 对内存的占用进一步缩减到 2.4 KB。

注意：类别数量相对于行数较少时，category 数据类型对对内存占用的减少会比较有限。

## 用多个文件建立 DataFrame ~ 按行

本段介绍怎样把分散于多个文件的数据集读取为一个 DataFrame。

比如，有多个 **stock** 文件，每个 CSV 文件里只存储一天的数据。

下面是三天的股票数据：

![](https://upload-images.jianshu.io/upload_images/3240514-ea2ac35084da18f0.png)

把每个 CSV 文件读取成 DataFrame，合并后，再删除导入的原始 DataFrame，但这种方式占用内存太多，而且要写很多代码。

使用 Python 内置的 `glob` 更方便。

![](https://upload-images.jianshu.io/upload_images/3240514-f790c902e88bc81e.png)

把文件名规则传递给 `glob()`，这里包括**通配符**，即可返回包含所有合规文件名的列表。

本例里，`glob` 会查找 **data** 子目录里所有以 **stocks** 开头的 CSV 文件。

![](https://upload-images.jianshu.io/upload_images/3240514-a6d4355459764346.png)

`glob` 返回的是无序文件名，要用 Python 内置的 `sorted()` 函数排序列表。

调用 `read_csv()` 函数读取生成器表达式里的每个文件，把读取结果传递给 `concat()` 函数，然后合并为一个 DataFrame。 

注：原文里用的是 `stock_files = sorted(glob('data/stocks*.csv'))`，译文里没用 `stocks*`，用的是 `stocks?`，这是因为 **data** 目录里还有一个叫 **stocks.csv** 的文件，如果用 \*，会读取出 4 个文件，而不是原文中的 3 个文件。

![](https://upload-images.jianshu.io/upload_images/3240514-cf460be8da2cafc3.png)

生成的 DataFrame 索引有重复值，见 “0、1、2”。为避免这种情况，要在 `concat()` 函数里用忽略旧索引、重置新索引的参数，`ignore_index = True`。

![](https://upload-images.jianshu.io/upload_images/3240514-7ae69422a7fb20b8.png)

## 用多个文件建立 DataFrame ~ 按列

上个技巧按行合并数据集，但是如果多个文件包含不同的列，该怎么办？

本例将 **drinks** 数据集分为了两个 CSV 文件，每个文件都包含 3 列。

![](https://upload-images.jianshu.io/upload_images/3240514-46d95f424d32ef84.png)

与上例一样，还是使用 `glob()`。

![](https://upload-images.jianshu.io/upload_images/3240514-eb71f1dbeb151823.png)

这里要让 `concat()` 函数按列合并，`axis='columns`。

![](https://upload-images.jianshu.io/upload_images/3240514-aa1dc1b141e6e17e.png)

现在 **drinks** 有 6 列啦！

## 从剪贴板创建 DataFrame

想快速把 Excel 或别的表格软件里存储的数据读取为 DataFrame，用 `read_clipboard()` 函数。

![](https://upload-images.jianshu.io/upload_images/3240514-362e1c05cd7ae09b.png)

打开要复制的 Excel 文件，选取内容，复制。

![](https://upload-images.jianshu.io/upload_images/3240514-5ef62f76e5caccea.png)

与 `read_csv()` 函数类似，`read_clipboard()` 会自动检测列名与每列的数据类型。

![](https://upload-images.jianshu.io/upload_images/3240514-91f63833188fba31.png)

![](https://upload-images.jianshu.io/upload_images/3240514-31edc5ec7cb3be67.png)

真不错！ pandas 自动把第一列当设置成索引了。

![](https://upload-images.jianshu.io/upload_images/3240514-74c1265ff818cd68.png)

注意：因为不能复用、重现，不推荐在正式代码里使用 `read_clipboard()` 函数。

## 把 DataFrame 分割为两个随机子集

把 DataFrame 分为两个随机子集，一个占 75% 的数据量，另一个是剩下的 25%。

以 **Movies** 为例，该数据有 979 条记录。

![](https://upload-images.jianshu.io/upload_images/3240514-16887376d8e71193.png)

使用 `sample()`方法随机选择 75% 的记录，并将之赋值给 **moives_1**。

![](https://upload-images.jianshu.io/upload_images/3240514-b0a5b6d0bccf9abc.png)

使用 `drop()` 方法删掉 **movies** 里所有 **movies_1**，并将之赋值给 **movies_2**。 

![](https://upload-images.jianshu.io/upload_images/3240514-cba2cc542fdee1c3.png)

两个 DataFrame 的行数之和与 **movies** 一致。

![](https://upload-images.jianshu.io/upload_images/3240514-14c39b94c308f388.png)

**movies_1** 与 **movies_2** 里的每个索引值都来自于 **movies**，而且互不重复。

![](https://upload-images.jianshu.io/upload_images/3240514-11951d4ca3c8d42d.png)

注意：如果索引值有重复、不唯一，这种方式会失效。

## 根据多个类别筛选 DataFrame

预览 **movies**。

![](https://upload-images.jianshu.io/upload_images/3240514-41c3457d6cf1d2d9.png)

查看 genre（电影类型）列。

![](https://upload-images.jianshu.io/upload_images/3240514-e50bae1f4b66a411.png)

要是想筛选 Action（动作片）、Drama（剧情片）、Western（西部片），可以用 `or` 的操作符实现多条件筛选。

![](https://upload-images.jianshu.io/upload_images/3240514-d9b753dbc44aa8b5.png)

不过，用 `isin()` 方法筛选会更清晰，只要传递电影类型的列表就可以了。

![](https://upload-images.jianshu.io/upload_images/3240514-74bbf8fdcbb59cfa.png)

如果想反选，可在条件前添加一个波浪符（tilde ~）。

![](https://upload-images.jianshu.io/upload_images/3240514-b9f1ecb597a5102a.png)

## 根据最大的类别筛选 DataFrame

筛选电影类别里（genre）数量最多的三类电影。

先用 `value_counts()` 统计各类电影的数量，把统计结果赋值给 `counts`，这个结果是 **Series**。 

![](https://upload-images.jianshu.io/upload_images/3240514-5b522c2cc85b9d31.png)

使用 **Series** 的 `nlargest` 方法，可以轻松选出 **Series** 里最大的三个值。

![](https://upload-images.jianshu.io/upload_images/3240514-5c9eb30fbeb2b2e2.png)

这里所需的只是这个 Series 的 index。

![](https://upload-images.jianshu.io/upload_images/3240514-5c4a495661595a9b.png)

把这个 index 传递给 `isin()`。

![](https://upload-images.jianshu.io/upload_images/3240514-f5673d3da4d85ef6.png)

最终，这个 DataFrame 里就只剩下了剧情片、喜剧片与动作片。

## 处理缺失值

本例使用目击 **UFO** 数据集。

![](https://upload-images.jianshu.io/upload_images/3240514-ea9e3c0bf118d211.png)

可以看到，这个数据集里有缺失值。

要查看每列有多少缺失值，可以使用 `isna()` 方法，然后使用 `sum()`函数。

![](https://upload-images.jianshu.io/upload_images/3240514-e2cfc263d27f0165.png)

`isna()` 生成一个由 `True` 与 `False` 构成的 DataFrame，`sum()` 把 `True` 转换为 1， 把 `False ` 转换为 0。

还可以用 `mean()` 函数，计算**缺失值**占比。

![](https://upload-images.jianshu.io/upload_images/3240514-16f040a1a85e0eec.png)

用 `dropna()` 删除列里的所有缺失值。

![](https://upload-images.jianshu.io/upload_images/3240514-ae25d5fd29424d84.png)

只想删除列中缺失值高于 10% 的缺失值，可以设置 `dropna()` 里的阈值，即 `threshold`.

![](https://upload-images.jianshu.io/upload_images/3240514-a17af58b089b8945.png)

## 把字符串分割为多列

创建一个 DataFrame 示例。

![](https://upload-images.jianshu.io/upload_images/3240514-7ffb0b882c6e6078.png)

把姓名列分为姓与名两列，用 `str.split()` 方法，按空格分割，并用 `expand` 关键字，生成一个新的 DataFrame。

![](https://upload-images.jianshu.io/upload_images/3240514-bca3c935a589482c.png)

通过赋值语句，把这两列添加到原 DataFrame。

![](https://upload-images.jianshu.io/upload_images/3240514-2a8160fab8b15d22.png)

如果想分割字符串，但只想保留分割结果的一列，该怎么操作？

![](https://upload-images.jianshu.io/upload_images/3240514-a49771b010329777.png)

要是只想保留**城市**列，可以选择只把**城市**加到 DataFrame 里。

![](https://upload-images.jianshu.io/upload_images/3240514-413b47fcc61a4204.png)

## 把 Series 里的列表转换为 DataFrame

创建一个 DataFrame 示例。

![](https://upload-images.jianshu.io/upload_images/3240514-8771692423664dba.png)

这里包含了两列，第二列包含的是 Python 整数列表。

要把第二列转为 DataFrame，在第二列上使用 `apply()` 方法，并把结果传递给 Series 构建器。

![](https://upload-images.jianshu.io/upload_images/3240514-a261365a08884c7f.png)

用 `concat()` 函数，把原 DataFrame 与新 DataFrame 组合在一起。

![](https://upload-images.jianshu.io/upload_images/3240514-5075122b81744050.png)

## 用多个函数聚合

先看一下 **Chipotle** 连锁餐馆的 DataFrame。

![](https://upload-images.jianshu.io/upload_images/3240514-ef5e77008f72ad80.png)

每个订单都有订单号（order_id），每个订单有多行。要统计每个订单的金额，需要先根据每个 order_id 汇总每个订单里各个产品（item_price）的金额。下面的例子列出了订单号为 1 的总价。

![](https://upload-images.jianshu.io/upload_images/3240514-6ca7c9d1be909ef0.png)

计算每单的总价，要按 `order_id` 进行 `groupby()` 分组，再按 `item_price` 计算每组的总价。

![](https://upload-images.jianshu.io/upload_images/3240514-57507a36b331fc73.png)

有时，要用多个聚合函数，不一定只是 `sum()` 一个函数。这时，要用 `agg()` 方法，把多个聚合函数的列表作为该方法的参数。

![](https://upload-images.jianshu.io/upload_images/3240514-ca0c72bb4dd9a73b.png)

上列就算出了每个订单的总价与订单里的产品数量。

## 用一个 DataFrame 合并聚合的输出结果

本例用的还是 **orders**。

![](https://upload-images.jianshu.io/upload_images/3240514-5877e47211c5aaa7.png)

如果想新增一列，为每行列出订单的总价，要怎么操作？上面介绍过用 `sum()` 计算总价。

![](https://upload-images.jianshu.io/upload_images/3240514-cb787017e7cad469.png)

`sum()` 是聚合函数，该函数返回结果的行数（1834行）比原始数据的行数（4622行）少。

![](https://upload-images.jianshu.io/upload_images/3240514-84fb6a8919690e52.png)

要解决这个问题得用 `transform()` 方法，这个方法执行同样的计算，但返回与原始数据行数一样的输出结果，本例中为 4622 行。

![](https://upload-images.jianshu.io/upload_images/3240514-9c2fcdb3fccc9580.png)

接下来，为 DataFrame 新增一列，`total_price`。

![](https://upload-images.jianshu.io/upload_images/3240514-8eff8097c2c19098.png)

如上所示，每一行都列出了对应的订单总价。

这样一来，计算每行产品占订单总价的百分比就易如反掌了。

![](https://upload-images.jianshu.io/upload_images/3240514-1910a61444b3683c.png)

## 选择行与列

本例使用大家都看腻了的**泰坦尼克**数据集。

![](https://upload-images.jianshu.io/upload_images/3240514-14540ea6ed4e7651.png)

这个数据集包括了泰坦尼克乘客的基本信息以及是否逃生的数据。

用 `describe()` 方法，可以得到该数据集的基本统计数据。

![](https://upload-images.jianshu.io/upload_images/3240514-eabf1dda0ae24d8c.png)

这个结果集显示的数据很多，但不一定都是你需要的，可能只需要其中几行。

![](https://upload-images.jianshu.io/upload_images/3240514-185460bc277f93b8.png)

还可以只选择部分列。

![](https://upload-images.jianshu.io/upload_images/3240514-ae0a04c310b20bf0.png)

## 重塑多重索引 Series

泰坦尼克数据集里有一列标注了**幸存（Survived）**状态，值用 0、1 代表。计算该列的平均值可以计算整体幸存率。

![](https://upload-images.jianshu.io/upload_images/3240514-cfa7d7590c5da08f.png)

按**性别（Sex）**统计男女的幸存率，需要使用 `groupby()`。

![](https://upload-images.jianshu.io/upload_images/3240514-91f48c877a345b94.png)

要按**性别**与**舱型（Pclass）**统计幸存率，就要按性别与舱型进行 `groupby()`。

![](https://upload-images.jianshu.io/upload_images/3240514-a99db8111f215843.png)

上面显示了不同性别，不同舱型的幸存率，输出结果是一个多重索引的序列（Series），这种形式与实际数据相比多了多重索引。

这种表现形式不利于阅读，也不方便实现数据交互，用 `unstack()` 把多重索引转换为 DataFrame 更方便。

![](https://upload-images.jianshu.io/upload_images/3240514-b61b594fbc28366b.png)

这个 DataFrame 包含的数据与多重索引序列一模一样，只是可以用大家更熟悉的 DataFrame 方法进行操控。

## 创建透视表

经常输出类似上例的 DataFrame，`pivot_table()` 方法更方便。

![](https://upload-images.jianshu.io/upload_images/3240514-4a9bd1e533508c63.png)

使用透视表，可以直接指定索引、数据列、值与聚合函数。

设置 `margins=True`，即可为透视表添加行与列的汇总。

![](https://upload-images.jianshu.io/upload_images/3240514-f9d597c474c92c09.png)

此表显示了整体幸存率，及按性别与舱型划分的幸存率。

把聚合函数 `mean` 改为 `count`，就可以生成交叉表。

![](https://upload-images.jianshu.io/upload_images/3240514-85d364c642527566.png)

这里显示了每个类别的记录数。

## 把连续型数据转换为类型数据

下面看一下泰坦尼克数据集的年龄（Age）列。

![](https://upload-images.jianshu.io/upload_images/3240514-ec09ddfe622989ce.png)

这一列是连续型数据，如果想把它转换为类别型数据怎么办？

这里可以用 `cut` 函数把年龄划分为儿童、青年、成人三个年龄段。

![](https://upload-images.jianshu.io/upload_images/3240514-855d8b893e39f176.png)

这段代码为不同分箱提供了标签，年龄在 0-18 岁的为儿童，18-25 岁的为青年，25-99 岁的为成人。

注意：现在数据已经是类别型了，类别型数据会自动排序。

## 改变显示选项

接下来还是看泰坦尼克数据集。

![](https://upload-images.jianshu.io/upload_images/3240514-b020f0f2908ae961.png)

年龄列有 1 位小数，票价列有 4 位小数，如何将这两列显示的小数位数标准化？

用以下代码让这两列只显示 2 位小数。

![](https://upload-images.jianshu.io/upload_images/3240514-79378cf197bb62cb.png)

第一个参数是要设置的选项名称，第二个参数是 Python 的字符串格式。

![](https://upload-images.jianshu.io/upload_images/3240514-89a54eccc9597863.png)

现在年龄与票价列为 2 位小数了。

注意：这种操作不改变底层数据，只改变数据的显示形式。

还可以用以下代码重置数据显示选项。

`pd.reset_option('display.float_format')`

注意：使用同样的方式，还可以设置更多选项。

## 设置 DataFrame 样式

上面的技巧适用于调整整个 Jupyter Notebook 的显示内容。

不过，要想为某个 DataFrame 设定指定的样式，pandas 还提供了更灵活的方式。

下面看一下 **stocks**。

![](https://upload-images.jianshu.io/upload_images/3240514-0ea8c7bbfb74b292.png)

创建**样式字符字典**，指定每列使用的格式。

![](https://upload-images.jianshu.io/upload_images/3240514-79f74803416405da.png)

把这个字典传递给 DataFrame 的 `style.format()` 方法。

![](https://upload-images.jianshu.io/upload_images/3240514-55da17ae308ac23c.png)

注意：日期是**月-日-年**的格式，闭市价有美元符，交易量有千分号。

接下来用链式方法实现更多样式。

![](https://upload-images.jianshu.io/upload_images/3240514-c3029032b9310996.png)

可以看到，这个表隐藏了索引，闭市价最小值用红色显示，最大值用浅绿色显示。

再看一下背景色渐变的样式。

![](https://upload-images.jianshu.io/upload_images/3240514-6512cfa3ff784caf.png)

交易量（Volume）列现在按不同深浅的蓝色显示，一眼就能看出来数据的大小。

下面看最后一个例子。

![](https://upload-images.jianshu.io/upload_images/3240514-1964b4ed644ea68c.png)

本例的 DataFrame 加上了标题，交易量列使用了迷你条形图。

注意：Pandas 还支持更多 DataFrame 样式选项，详见 pandas 官方文档。

## 彩蛋：预览 DataFrame

假如刚拿到一个数据集，想快速了解该数据集，又不想费劲折腾怎么办？这里介绍一个独立的支持库，[pandas_profiling](https://github.com/pandas-profiling/pandas-profiling)，可以快速预览数据集。

第一步，安装， `pip install pandas-profiling`

第二步，导入，`import pandas_profiling`

![](https://upload-images.jianshu.io/upload_images/3240514-a7f12301b7b6b6c2.png)

本例简单介绍一下 `ProfileReport()` 函数，这个函数支持任意 DataFrame，并生成交互式 HTML 数据报告：
* 第一部分是纵览数据集，还会列出数据一些可能存在的问题；
* 第二部分汇总每列数据，点击 **toggle details** 查看更多信息；
* 第三部分显示列之间的关联热力图；
* 第四部分显示数据集的前几条数据。

![](https://upload-images.jianshu.io/upload_images/3240514-f8919837733f5a28.png)

![](https://upload-images.jianshu.io/upload_images/3240514-b49319ea5b265af6.png)

![](https://upload-images.jianshu.io/upload_images/3240514-393b722ae00c477b.png)

![](https://upload-images.jianshu.io/upload_images/3240514-92f7c8e1e8befb66.png)

![](https://upload-images.jianshu.io/upload_images/3240514-d5a3eb3df97171ac.png)

![](https://upload-images.jianshu.io/upload_images/3240514-7252ab7e26bd4979.png)

[英文版 Jupyter Notebook 链接](https://nbviewer.jupyter.org/github/justmarkham/pandas-videos/blob/master/top_25_pandas_tricks.ipynb)

[中文版 Jupyter Notebook 链接](https://github.com/jaystone776/pandas_answered/blob/master/25_Pandas_Tips_by_PyCon_Master.ipynb)

[数据集下载](https://github.com/jaystone776/pandas_answered/blob/master/data/25_Pandas_Tips_by_PyCon_Master_data.zip)

[Kevin Markham - My top 25 pandas tricks 英文版视频: 提取码：vqup ](https://pan.baidu.com/s/1HDgOfG5yd_FuQag-Wsr-Bw)
