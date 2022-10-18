**《AKShare-初阶使用教学》视频课程已经上线，本课程手把手讲解 AKShare 和 AKTools 的环境配置和安装使用，还包含了众多衍生知识，[详情点击链接](https://zmj.xet.tech/s/wck86)! Tips：加入 AKShare VIP 答疑群可以免费获取该视频课程。**

**《AKShare-源码解析》课程即将上线，本课程会系统的给大家手把手讲解 AKShare 数据接口的源码及财经数据的网络数据采集知识！[点击链接](https://mp.weixin.qq.com/s?__biz=MzI3MzYwODk2MQ==&mid=2247492193&idx=2&sn=a02b305b57a4b0756d5842494de96011&chksm=eb221a0fdc5593196168927217fc8b5486ab43e479f13cc643096069bb829e4a50067534a0b2&mpshare=1&scene=23&srcid=0316bvNDuCQ9P2E08BgK1Bnt&sharer_sharetime=1647406328931&sharer_shareid=2a5935b93d26c84266d2170040c3643c#rd) 查看课程信息。**

**本次发布 [AKTools](https://github.com/akfamily/aktools) 作为 AKShare 的 HTTP API 版本，突破 Python 语言的限制，欢迎各位小伙伴试用并提出更好的意见或建议！ 点击 [AKTools](https://github.com/akfamily/aktools) 查看使用指南。另外提供 [awesome-data](https://github.com/akfamily/awesome-data) 方便各位小伙伴查询各种数据源。**

![](https://github.com/akfamily/akshare/blob/master/example/images/AKShare_logo.jpg)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/akshare.svg)](https://pypi.org/project/akshare/)
[![PyPI](https://img.shields.io/pypi/v/akshare.svg)](https://pypi.org/project/akshare/)
[![Downloads](https://pepy.tech/badge/akshare)](https://pepy.tech/project/akshare)
[![Documentation Status](https://readthedocs.org/projects/akshare/badge/?version=latest)](https://akshare.readthedocs.io/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/akfamily/akshare)
[![Actions Status](https://github.com/akfamily/akshare/workflows/build/badge.svg)](https://github.com/akfamily/akshare/actions)
[![MIT Licence](https://camo.githubusercontent.com/14a9abb7e83098f2949f26d2190e04fb1bd52c06/68747470733a2f2f626c61636b2e72656164746865646f63732e696f2f656e2f737461626c652f5f7374617469632f6c6963656e73652e737667)](https://github.com/akfamily/akshare/blob/master/LICENSE)
[![](https://img.shields.io/github/forks/jindaxiang/akshare)](https://github.com/akfamily/akshare)
[![](https://img.shields.io/github/stars/jindaxiang/akshare)](https://github.com/akfamily/akshare)
[![](https://img.shields.io/github/issues/jindaxiang/akshare)](https://github.com/akfamily/akshare)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Overview

[AKShare](https://github.com/akfamily/akshare) requires Python(64 bit) 3.7 or greater, aims to make fetch financial data as convenient as possible.

**Write less, get more!**

- Documentation: [中文文档](https://www.akshare.xyz/)

# ![](https://github.com/akfamily/akshare/blob/master/example/images/AKShare.svg)

## Installation

### General

```shell
pip install akshare --upgrade
```

### China

```shell
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
```

### PR

Please check out [documentation](https://www.akshare.xyz/zh_CN/latest/contributor.html) if you want to contribute to AKShare

### Docker

#### Pull images

```shell
docker pull registry.cn-hangzhou.aliyuncs.com/akshare/akdocker
```

#### Run AKDocker

```shell
docker run -it registry.cn-hangzhou.aliyuncs.com/akshare/akdocker python
```

#### Test AKDocker

```python
import akshare as ak

ak.__version__
```

## Usage

### Data

Code

```python
import akshare as ak

stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907', adjust="")
print(stock_zh_a_hist_df)
```

Output

```
      日期          开盘   收盘    最高  ...  振幅   涨跌幅 涨跌额 换手率
0     2017-03-01   9.49   9.49   9.55  ...  0.84  0.11  0.01  0.21
1     2017-03-02   9.51   9.43   9.54  ...  1.26 -0.63 -0.06  0.24
2     2017-03-03   9.41   9.40   9.43  ...  0.74 -0.32 -0.03  0.20
3     2017-03-06   9.40   9.45   9.46  ...  0.74  0.53  0.05  0.24
4     2017-03-07   9.44   9.45   9.46  ...  0.63  0.00  0.00  0.17
          ...    ...    ...    ...  ...   ...   ...   ...   ...
1100  2021-09-01  17.48  17.88  17.92  ...  5.11  0.45  0.08  1.19
1101  2021-09-02  18.00  18.40  18.78  ...  5.48  2.91  0.52  1.25
1102  2021-09-03  18.50  18.04  18.50  ...  4.35 -1.96 -0.36  0.72
1103  2021-09-06  17.93  18.45  18.60  ...  4.55  2.27  0.41  0.78
1104  2021-09-07  18.60  19.24  19.56  ...  6.56  4.28  0.79  0.84
[1105 rows x 11 columns]
```

### Plot

Code

```python
import akshare as ak
import mplfinance as mpf  # Please install mplfinance as follows: pip install mplfinance

stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
stock_us_daily_df = stock_us_daily_df[["open", "high", "low", "close", "volume"]]
stock_us_daily_df.columns = ["Open", "High", "Low", "Close", "Volume"]
stock_us_daily_df.index.name = "Date"
stock_us_daily_df = stock_us_daily_df["2020-04-01": "2020-04-29"]
mpf.plot(stock_us_daily_df, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=False)
```

Output

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/home/AAPL_candle.png)

## Communication

Pay attention to **数据科学家** Official Accounts to get more information about Quant, ML, DS and so on, please visit [数据科学家](https://www.akshare.xyz/introduction.html) for more information:

<div>
    <img src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/data_scientist.png">
</div>

Pay attention to **数据科学实战** WeChat Official Accounts to get the [AKShare](https://github.com/akfamily/akshare) updated info:

<div>
    <img src="https://github.com/akfamily/akshare/blob/master/example/images/ds.png">
</div>

Application to add **AKShare-VIP QQ group** and talk about [AKShare](https://github.com/akfamily/akshare) issues, please contact **AKShare-小助手 QQ**: 1254836886
![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/qr_code_1254836886.jpg)

## Features

- **Easy of use**: Just one line code to fetch the data;
- **Extensible**: Easy to customize your own code with other application;
- **Powerful**: Python ecosystem.

## Tutorials

1. [Overview](https://akshare.readthedocs.io/zh_CN/latest/akshare/ak-introduction.html)
2. [Installation](https://akshare.readthedocs.io/zh_CN/latest/akshare/ak-installation.html)
3. [Tutorial](https://akshare.readthedocs.io/zh_CN/latest/akshare/ak-tutorial.html)
4. [Data Dict](https://akshare.readthedocs.io/zh_CN/latest/README.html)
5. [Subjects](https://akshare.readthedocs.io/zh_CN/latest/subjects/index.html)

## Contribution

[AKShare](https://github.com/akfamily/akshare) is still under developing, feel free to open issues and pull requests:

- Report or fix bugs
- Require or publish interface
- Write or fix documentation
- Add test cases

> Notice: We use [Black](https://black.readthedocs.io/en/stable/) to format the code

## Statement

1. All data provided by [AKShare](https://github.com/akfamily/akshare) is just for academic research purpose;
2. The data provided by [AKShare](https://github.com/akfamily/akshare) is for reference only and does not constitute any investment proposal;
3. Any investor based on [AKShare](https://github.com/akfamily/akshare) research should pay more attention to data risk;
4. [AKShare](https://github.com/akfamily/akshare) will insist on providing open-source financial data;
5. Based on some uncontrollable factors, some data interfaces in [AKShare](https://github.com/akfamily/akshare) may be removed;
6. Please follow the relevant open-source protocol used by [AKShare](https://github.com/akfamily/akshare);
7. Provide HTTP API for the person who uses other program language: [AKTools](https://aktools.readthedocs.io/).

## Show your style

Use the badge in your project's README.md:

```markdown
[![Data: akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/akfamily/akshare)
```

Using the badge in README.rst:

```
.. image:: https://img.shields.io/badge/Data%20Science-AKShare-green
    :target: https://github.com/akfamily/akshare
```

Looks like this:

[![Data: akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/akfamily/akshare)

## Citation

Please use this **bibtex** if you want to cite this repository in your publications:

```markdown
@misc{akshare,
    author = {Albert King},
    title = {AKShare},
    year = {2019},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/akfamily/akshare}},
}
```

## Acknowledgement

Special thanks [FuShare](https://github.com/LowinLi/fushare) for the opportunity of learning from the project;

Special thanks [TuShare](https://github.com/waditu/tushare) for the opportunity of learning from the project;

Thanks for the data provided by [生意社网站](http://www.100ppi.com/);

Thanks for the data provided by [奇货可查网站](https://qhkch.com/);

Thanks for the data provided by [中国银行间市场交易商协会网站](http://www.nafmii.org.cn/);

Thanks for the data provided by [99期货网站](http://www.99qh.com/);

Thanks for the data provided by [英为财情网站](https://cn.investing.com/);

Thanks for the data provided by [中国外汇交易中心暨全国银行间同业拆借中心网站](http://www.chinamoney.com.cn/chinese/);

Thanks for the data provided by [金十数据网站](https://www.jin10.com/);

Thanks for the data provided by [和讯财经网站](http://www.hexun.com/);

Thanks for the data provided by [新浪财经网站](https://finance.sina.com.cn/);

Thanks for the data provided by [Oxford-Man Institute 网站](https://realized.oxford-man.ox.ac.uk/);

Thanks for the data provided by [DACHENG-XIU 网站](https://dachxiu.chicagobooth.edu/);

Thanks for the data provided by [上海证券交易所网站](http://www.sse.com.cn/assortment/options/price/);

Thanks for the data provided by [深证证券交易所网站](http://www.szse.cn/);

Thanks for the data provided by [北京证券交易所网站](http://www.bse.cn/);

Thanks for the data provided by [中国金融期货交易所网站](http://www.cffex.com.cn/);

Thanks for the data provided by [上海期货交易所网站](http://www.shfe.com.cn/);

Thanks for the data provided by [大连商品交易所网站](http://www.dce.com.cn/);

Thanks for the data provided by [郑州商品交易所网站](http://www.czce.com.cn/);

Thanks for the data provided by [上海国际能源交易中心网站](http://www.ine.com.cn/);

Thanks for the data provided by [Timeanddate 网站](https://www.timeanddate.com/);

Thanks for the data provided by [河北省空气质量预报信息发布系统网站](http://110.249.223.67/publish/);

Thanks for the data provided by [南华期货网站](http://www.nanhua.net/nhzc/varietytrend.html);

Thanks for the data provided by [Economic Policy Uncertainty 网站](http://www.nanhua.net/nhzc/varietytrend.html);

Thanks for the data provided by [微博指数网站](https://data.weibo.com/index/newindex);

Thanks for the data provided by [百度指数网站](http://index.baidu.com/v2/main/index.html);

Thanks for the data provided by [谷歌指数网站](https://trends.google.com/trends/?geo=US);

Thanks for the data provided by [申万指数网站](http://www.swsindex.com/idx0120.aspx?columnid=8832);

Thanks for the data provided by [真气网网站](https://www.zq12369.com/);

Thanks for the data provided by [财富网站](http://www.fortunechina.com/);

Thanks for the data provided by [中国证券投资基金业协会网站](http://gs.amac.org.cn/);

Thanks for the data provided by [Expatistan 网站](https://www.expatistan.com/cost-of-living);

Thanks for the data provided by [北京市碳排放权电子交易平台网站](https://www.bjets.com.cn/article/jyxx/);

Thanks for the data provided by [国家金融与发展实验室网站](http://www.nifd.cn/);

Thanks for the data provided by [IT桔子网站](https://www.itjuzi.com);

Thanks for the data provided by [东方财富网站](http://data.eastmoney.com/jgdy/);

Thanks for the data provided by [义乌小商品指数网站](http://www.ywindex.com/Home/Product/index/);

Thanks for the data provided by [中国国家发展和改革委员会网站](http://jgjc.ndrc.gov.cn/dmzs.aspx?clmId=741);

Thanks for the data provided by [163网站](https://news.163.com/special/epidemic/);

Thanks for the data provided by [丁香园网站](http://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579615030&enterid=1579615030&from=groupmessage&isappinstalled=0);

Thanks for the data provided by [百度新型肺炎网站](https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1);

Thanks for the data provided by [百度迁徙网站](https://qianxi.baidu.com/?from=shoubai#city=0);

Thanks for the data provided by [新型肺炎-相同行程查询工具网站](https://rl.inews.qq.com/h5/trip?from=newsapp&ADTAG=tgi.wx.share.message);

Thanks for the data provided by [新型肺炎-小区查询网站](https://ncov.html5.qq.com/community?channelid=1&from=singlemessage&isappinstalled=0);

Thanks for the data provided by [商业特许经营信息管理网站](http://txjy.syggs.mofcom.gov.cn/);

Thanks for the data provided by [慈善中国网站](http://cishan.chinanpo.gov.cn/platform/login.html);

Thanks for the data provided by [思知网站](https://www.ownthink.com/);

Thanks for the data provided by [Currencyscoop 网站](https://currencyscoop.com/);

Thanks for the data provided by [新加坡交易所网站](https://www.sgx.com/zh-hans/research-education/derivatives);

Thanks for the tutorials provided by [微信公众号: Python大咖谈](https://upload-images.jianshu.io/upload_images/3240514-61004f2c71be4a0b.png).

## Backer and Sponsor

<a href="https://www.jetbrains.com/?from=jindaxiang/akshare" target="_blank">
<img src="https://github.com/akfamily/akshare/blob/master/example/images/jetbrains.svg" width="100px" height="100px">
</a>
