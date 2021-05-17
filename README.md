![](https://github.com/jindaxiang/akshare/blob/master/example/images/AKShare_logo.jpg)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/akshare.svg)](https://pypi.org/project/akshare/)
[![PyPI](https://img.shields.io/pypi/v/akshare.svg)](https://pypi.org/project/akshare/)
[![Downloads](https://pepy.tech/badge/akshare)](https://pepy.tech/project/akshare)
[![Documentation Status](https://readthedocs.org/projects/akshare/badge/?version=latest)](https://akshare.readthedocs.io/zh_CN/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/jindaxiang/akshare)
[![Actions Status](https://github.com/jindaxiang/akshare/workflows/build/badge.svg)](https://github.com/jindaxiang/akshare/actions)
[![MIT Licence](https://camo.githubusercontent.com/14a9abb7e83098f2949f26d2190e04fb1bd52c06/68747470733a2f2f626c61636b2e72656164746865646f63732e696f2f656e2f737461626c652f5f7374617469632f6c6963656e73652e737667)](https://github.com/jindaxiang/akshare/blob/master/LICENSE)
[![](https://img.shields.io/github/forks/jindaxiang/akshare)](https://github.com/jindaxiang/akshare)
[![](https://img.shields.io/github/stars/jindaxiang/akshare)](https://github.com/jindaxiang/akshare)
[![](https://img.shields.io/github/issues/jindaxiang/akshare)](https://github.com/jindaxiang/akshare)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Overview

[AKShare](https://github.com/jindaxiang/akshare) requires Python(64 bit) 3.7 or greater, aims to make fetch financial data as convenient as possible.

**Write less, get more!**

- Documentation: [中文文档](https://akshare.readthedocs.io/zh_CN/latest/)

# ![](https://github.com/jindaxiang/akshare/blob/master/example/images/AKShare.svg)

## Installation

### General

```
pip install akshare --upgrade
```

### China

```cmd
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
```

### PR

Please check out [documentation](https://www.akshare.xyz/zh_CN/latest/contributor.html) if you want to contribute to AKShare

### Docker

#### Pull images

```
docker pull registry.cn-hangzhou.aliyuncs.com/akshare/akdocker
```

#### Run AkDocker

```
docker run -it registry.cn-hangzhou.aliyuncs.com/akshare/akdocker python
```

#### Test AkDocker

```python
import akshare as ak
ak.__version__
```

## Usage

### Data

Code

```python
import akshare as ak
hist_df = ak.stock_us_daily(symbol="AMZN")  # Get U.S. stock Amazon's price info
print(hist_df)
```

Output

```
               open       high        low      close     volume
date                                                           
1997-05-15    29.25    30.0000    23.1300    23.5000  6013000.0
1997-05-16    23.63    23.7500    20.5000    20.7500  1225000.0
1997-05-19    21.13    21.2500    19.5000    20.5000   508900.0
1997-05-20    20.75    21.0000    19.6300    19.6300   455600.0
1997-05-21    19.63    19.7500    16.5000    17.1300  1571100.0
             ...        ...        ...        ...        ...
2021-01-04  3270.00  3272.0000  3144.0200  3186.6299  4205801.0
2021-01-05  3166.01  3223.3799  3165.0601  3218.5100  2467255.0
2021-01-06  3146.48  3197.5090  3131.1599  3138.3799  4065357.0
2021-01-07  3157.00  3208.5420  3155.0000  3162.1599  3320882.0
2021-01-08  3180.00  3190.6399  3142.2000  3182.7000  3410288.0
[5951 rows x 5 columns]
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

Pay attention to **数据科学家** Official Accounts to get more information about Quant, ML, DS and so on.

<div align=center>
    <img src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/data_scientist">
</div>

Pay attention to **数据科学实战** WeChat Official Accounts to get the [AKShare](https://github.com/jindaxiang/akshare) updated info:

<div align=center>
    <img src="https://github.com/jindaxiang/akshare/blob/master/example/images/ds.png">
</div>

[comment]: <> (Application to add **AKShare-官方** QQ group and talk about [AKShare]&#40;https://github.com/jindaxiang/akshare&#41; issues, QQ group number: 444233982)

[comment]: <> (<div align=center>)

[comment]: <> (    <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=M50z_7n-XXg8PHRz_482NysL2ihMBKyK&jump_from=webapi"><img border="0" src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/qr_code_444233982.png" alt="AKShare-官方" title="AKShare-官方"></a>)

[comment]: <> (</div>)

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

[AKShare](https://github.com/jindaxiang/akshare) is still under developing, feel free to open issues and pull requests:

- Report or fix bugs
- Require or publish interface
- Write or fix documentation
- Add test cases

> Notice: We use [Black](https://black.readthedocs.io/en/stable/) to format the code

## Statement

1. All data provided by [AKShare](https://github.com/jindaxiang/akshare) is just for academic research purpose;

2. The data provided by [AKShare](https://github.com/jindaxiang/akshare) is for reference only and does not constitute any investment proposal;

3. Any investor based on [AKShare](https://github.com/jindaxiang/akshare) research should pay more attention to data risk;

4. [AKShare](https://github.com/jindaxiang/akshare) will insist on providing open-source financial data;

5. Based on some uncontrollable factors, some data interfaces in [AKShare](https://github.com/jindaxiang/akshare) may be removed;

6. Please follow the relevant open-source protocol used by [AKShare](https://github.com/jindaxiang/akshare)

## Show your style

Use the badge in your project's README.md:

```markdown
[![Data: akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/jindaxiang/akshare)
```

Using the badge in README.rst:

```
.. image:: https://img.shields.io/badge/Data%20Science-AKShare-green
    :target: https://github.com/jindaxiang/akshare
```

Looks like this:

[![Data: akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/jindaxiang/akshare)

## Citation

Please use this **bibtex** if you want to cite this repository in your publications:

```
@misc{akshare,
    author = {Albert King},
    title = {AKShare},
    year = {2019},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/jindaxiang/akshare}},
}
```

## Acknowledgement

Special thanks [FuShare](https://github.com/LowinLi/fushare) for the opportunity of learning from the project;

Special thanks [TuShare](https://github.com/waditu/tushare) for the opportunity of learning from the project;

Thanks for the data provided by [生意社网站](http://www.100ppi.com/);

Thanks for the data provided by [奇货可查网站](https://qhkch.com/);

Thanks for the data provided by [智道智科网站](https://www.ziasset.com/);

Thanks for the data provided by [中国银行间市场交易商协会网站](http://www.nafmii.org.cn/);

Thanks for the data provided by [99期货网站](http://www.99qh.com/);

Thanks for the data provided by [英为财情网站](https://cn.investing.com/);

Thanks for the data provided by [中国外汇交易中心暨全国银行间同业拆借中心网站](http://www.chinamoney.com.cn/chinese/);

Thanks for the data provided by [金十数据网站](https://www.jin10.com/);

Thanks for the data provided by [交易法门网站](https://www.jiaoyifamen.com/);

Thanks for the data provided by [和讯财经网站](http://www.hexun.com/);

Thanks for the data provided by [新浪财经网站](https://finance.sina.com.cn/);

Thanks for the data provided by [Oxford-Man Institute 网站](https://realized.oxford-man.ox.ac.uk/);

Thanks for the data provided by [DACHENG-XIU 网站](https://dachxiu.chicagobooth.edu/);

Thanks for the data provided by [上海证券交易所网站](http://www.sse.com.cn/assortment/options/price/);

Thanks for the data provided by [深证证券交易所网站](http://www.szse.cn/);

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

Thanks for the data provided by [猫眼电影网站](https://maoyan.com/board/1);

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

Thanks for the data provided by [Currencyscoop网站](https://currencyscoop.com/);

Thanks for the data provided by [新加坡交易所网站](https://www.sgx.com/zh-hans/research-education/derivatives);

Thanks for the data provided by [中国期货市场监控中心](http://index.cfmmc.com/index/views/index.html);

Thanks for the data provided by [宽客在线](https://www.quantinfo.com/Argus/);

Thanks for the tutorials provided by [微信公众号: Python大咖谈](https://upload-images.jianshu.io/upload_images/3240514-61004f2c71be4a0b.png).

## Backer and Sponsor

<a href="https://www.jetbrains.com/?from=jindaxiang/akshare" target="_blank">
<img src="https://github.com/jindaxiang/akshare/blob/master/example/images/jetbrains.svg" width="100px" height="100px">
</a>
