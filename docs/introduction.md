# [AKShare](https://github.com/jindaxiang/akshare) 概览

**风险提示：[AKShare](https://github.com/jindaxiang/akshare) 项目所采集的数据皆来自公开的数据源，不涉及任何个人隐私数据和非公开数据。
同时本项目提供的数据接口及相关数据仅用于学术研究，任何个人、机构及团体使用本项目的数据接口及相关数据请注意商业风险。**

1. 本文档更新于 **2020-03-30**;

2. 如有库、文档及数据的相关问题, 请在 [AKShare Issues](https://github.com/jindaxiang/akshare/issues) 中提 Issues;

3. 您也可以加入QQ群: 512720929

<div align=center>
    <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=lW9uQSc9HkKBmfRg6I25YIMjco_ZzTuN&jump_from=webapi">
        <img border="0" src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/qr_code_512720929.png" alt="AKShare-官方" title="AKShare-官方" align="center">
    </a>
</div>
4. 欢迎关注 数据科学实战 微信公众号:

<div align=center>
    <img src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/ds.png">
</div>

## 引用

如果您想在文章或者项目中引用 [AKShare](https://github.com/jindaxiang/akshare), 请使用如下 **bibtex** 格式:

```
@misc{akshare2019,
    author = {Albert King},
    title = {AKShare},
    year = {2019},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/jindaxiang/akshare}},
}
```

## [AKShare](https://github.com/jindaxiang/akshare) 的介绍

首先要特别感谢 [FuShare](https://github.com/jindaxiang/fushare), [TuShare](https://github.com/waditu/tushare) 在代码和项目开发上对本项目提供的借鉴和学习的机会!

[AKShare](https://github.com/jindaxiang/akshare) 是基于 Python 的财经数据接口库, 目的是实现对股票、期货、期权、基金、外汇、债券、指数、加密货币等金融产品的基本面数据、实时和历史行情数据、衍生数据从数据采集、数据清洗到数据落地的一套工具, 主要用于学术研究目的. 

[AKShare](https://github.com/jindaxiang/akshare) 的特点是获取的是相对权威的财经数据网站公布的原始数据, 通过利用原始数据进行各数据源之间的交叉验证, 进而再加工, 从而得出科学的结论.

**[AKShare](https://github.com/jindaxiang/akshare) 后续会基于学术论文和金融工程研究报告来添加更多数据接口和衍生指标并提供相应的计算代码, 敬请关注.**

## [AKShare](https://github.com/jindaxiang/akshare) 的特色

[AKShare](https://github.com/jindaxiang/akshare) 主要改进如下:

1. 代码语法符合 [PEP8](https://www.python.org/dev/peps/pep-0008/) 规范, 数据接口的命名统一;
2. 最佳支持 Python 3.7.5 及其以上版本;
3. 提供最佳的文档支持, 每个数据接口提供详细的说明和示例, 只需要复制粘贴就可以下载数据;
4. 持续维护由于目标网页变化而导致的部分数据接口运行异常问题;
5. 持续更新财经数据接口, 同时优化源代码;
6. 目前进行数据采集的网站一览:

    6.1 增加[奇货可查网站](https://qhkch.com/)提供的奇货可查指数数据;
    
    6.2 增加[智道智科网站](https://www.ziasset.com/)提供的私募指数数据;
    
    6.3 增加[99期货网](http://www.99qh.com/)提供的大宗商品库存数据;
    
    6.4 增加[商品期权](https://github.com/jindaxiang/akshare)提供的商品期货数据;
    
    6.5 增加[英为财情网站-全球指数](https://github.com/jindaxiang/akshare)提供的全球股指与期货指数数据;
    
    6.6 增加[英为财情网站-全球债券](https://github.com/jindaxiang/akshare)提供的全球政府债券行情与收益率数据;
    
    6.7 增加[中国外汇交易中心暨全国银行间同业拆借中心网站](http://www.chinamoney.com.cn/chinese/)提供的中国银行间债券行情和外汇数据;

    6.8 增加[英为财情网站-商品](https://cn.investing.com/commodities/)提供的全球商品历史数据;
    
    6.9 增加[金十数据网站](https://www.jin10.com/)提供的全球宏观经济数据接口-中国宏观;
    
    6.10 增加[金十数据网站](https://www.jin10.com/)提供的全球宏观经济数据接口-美国宏观;
    
    6.11 增加[金十数据网站](https://www.jin10.com/)提供的全球宏观经济数据接口-欧洲、机构宏观;

    6.12 增加[交易法门网站](https://www.jiaoyifamen.com/)提供的交易法门-仓单有效期数据;

    6.13 增加[和讯网网站](http://www.hexun.com/)提供的股票-企业社会责任数据;
    
    6.14 增加[和讯网](http://www.hexun.com/)提供的美国-中概股行情及历史数据;
    
    6.15 增加[交易法门网站](https://www.jiaoyifamen.com/)提供的期货相关数据接口;
    
    6.16 增加[新浪财经-期货](https://finance.sina.com.cn/futuremarket/)提供的期货实时行情数据;

    6.17 增加[新浪财经-港股](http://finance.sina.com.cn/stock/hkstock/)提供的实时行情数据和历史行情数据(包括前复权和后复权因子);

    6.18 增加[新浪财经-美股](http://finance.sina.com.cn/stock/usstock/sector.shtml)提供的实时行情数据和历史行情数据(包括前复权因子);

    6.19 增加[上海证券交易所-期权](http://www.sse.com.cn/assortment/options/price/)提供的当日期权行情数据;
    
    6.20 增加[金十数据网站](http://www.sse.com.cn/assortment/options/price/)提供的加密货币行情数据;

    6.21 增加[腾讯财经网站](http://stockapp.finance.qq.com/mstats/#mod=list&id=hk_ah&module=HK&type=AH)提供的A+H股数据;

    6.22 增加[新浪财经-A股](http://vip.stock.finance.sina.com.cn/mkt/#hs_a)提供的A股数据;

    6.23 增加[新浪财经-科创板](http://vip.stock.finance.sina.com.cn/mkt/#cyb)提供的科创板数据;

    6.24 增加[银保监分局本级行政处罚](http://www.cbirc.gov.cn/cn/list/9103/910305/ybjfjcf/1.html)提供的银保监分局本级行政处罚;

    6.25 增加[Realized Library](https://realized.oxford-man.ox.ac.uk/)提供的Oxford-Man Institute of Quantitative Finance; https://dachxiu.chicagobooth.edu/

    6.26 增加[FF Factors](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)提供的多因子模型数据

    6.27 增加[腾讯财经](http://stockapp.finance.qq.com/mstats/#mod=list&id=ssa&module=SS&type=ranka)提供的历史分笔行情数据(近2年)
    
    6.28 增加[金十数据](https://datacenter.jin10.com/market)提供的多品种实时数据接口和基于 websocket 的数据接口(基础版本);

    6.29 增加[微信公众号: Python大咖谈](https://upload-images.jianshu.io/upload_images/3240514-61004f2c71be4a0b.png)提供的专题教程-Pandas专题-连载;

    6.30 增加[timeanddate网站](https://www.timeanddate.com/)提供的日出和日落数据接口;
    
    6.31 增加[河北省空气质量预报信息发布系统网站](http://110.249.223.67/publish/)提供的河北省空气质量数据接口;
    
    6.32 增加[南华期货网站](http://www.nanhua.net/nhzc/varietytrend.html)提供的商品指数历史走势-收益率指数、价格指数、波动率指数接口;
    
    6.33 增加[Economic Policy Uncertainty网站](http://www.nanhua.net/nhzc/varietytrend.html)提供的经济政策不确定性(EPU)指数数据接口;
    
    6.34 增加[新浪微博](https://data.weibo.com/index)提供的微博指数数据;
    
    6.35 增加[百度](https://www.baidu.com/)提供的百度指数数据;
    
    6.36 增加[谷歌](https://www.google.com/)提供的谷歌趋势数据;
    
    6.37 增加[申万指数](http://www.swsindex.com/IdxMain.aspx)提供的申万指数数据;
    
    6.38 增加[真气网](https://www.zq12369.com/)提供的空气质量数据;
    
    6.39 增加[财富网站](http://www.fortunechina.com/)提供的财富企业500强排行榜数据;
    
    6.40 增加[中国证券投资基金业协会](http://gs.amac.org.cn/)提供的私募基金数据;

    6.41 增加[微信公众号: Python大咖谈](https://upload-images.jianshu.io/upload_images/3240514-61004f2c71be4a0b.png)专题教程-Anaconda专题-连载;
    
    6.42 增加[猫眼电影](https://maoyan.com/board/1)提供的实时票房数据;
    
    6.43 增加[北京市碳排放权电子交易平台](https://www.bjets.com.cn/article/jyxx/)提供的碳排放行情数据;
    
    6.44 新增[Expatistan网站](https://www.expatistan.com/cost-of-living)提供的世界各大城市生活成本数据;
    
    6.45 新增[国家金融与发展实验室网站](http://www.nifd.cn/)提供的宏观杠杆率数据;
    
    6.46 新增[IT桔子网站](https://www.itjuzi.com/)提供的千里马、独角兽、倒闭公司数据;
    
    6.47 新增[东方财富网站](http://data.eastmoney.com/jgdy/)提供的机构调研数据;
    
    6.48 新增[东方财富网站](http://data.eastmoney.com/gpzy/)提供的股权质押数据;
    
    6.49 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的商誉专题数据;
    
    6.50 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的股票账户统计数据;
    
    6.51 新增[交易法门网站](https://www.jiaoyifamen.com/)提供的商品期货数据数据;
    
    6.52 新增[百度疫情网站](https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1)提供的新型冠状病毒-疫情数据;
    
    6.53 新增[丁香园网站](http://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579615030&enterid=1579615030&from=groupmessage&isappinstalled=0)提供的新型冠状病毒-疫情数据;
    
    6.54 新增[网易网站](https://news.163.com/special/epidemic/)提供的新型冠状病毒-疫情数据;
    
    6.55 新增[百度迁徙网站](https://news.163.com/special/epidemic/)提供的人口迁徙数据;
    
    6.56 新增[新浪网站](http://vip.stock.finance.sina.com.cn/mkt/#hs_z)提供的沪深债券数据;
    
    6.57 新增[新浪网站](http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z)提供的沪深可转债数据;
    
    6.58 新增[商业特许经营信息管理网站](http://txjy.syggs.mofcom.gov.cn/)提供的特许经营数据;
    
    6.59 新增[慈善中国网站](http://cishan.chinanpo.gov.cn/platform/login.html)提供的慈善数据;
    
    6.60 新增[Currencyscoop网站](https://currencyscoop.com/)提供的货币数据;
    
    6.61 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的公募基金数据;
    
    6.62 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的LPR历史数据;
    
    6.63 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的千股千评数据;
    
    6.64 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的沪深港通数据;
    
    6.65 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的两市停复牌数据;
    
    6.66 新增[新浪网站](http://sina.com/)提供的外盘期货历史行情数据;
    
    6.67 新增[金十数据网站](https://www.jin10.com/)提供的恐慌指数数据;
    
    6.68 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的中国油价数据;
    
    6.69 新增[东方财富网站](http://data.eastmoney.com/sy/)提供的现货与股票数据;
    
    6.70 新增[中国期货市场监控中心](http://index.cfmmc.com/index/views/index.html)提供的期货指数数据;
    
    6.71 新增[CSSE开源项目](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)提供的全球疫情数据;
    
    6.72 新增[宽客在线](https://www.quantinfo.com/Argus/)提供的阿尔戈斯全网监控数据;
    
    6.73 新增[百度地图慧眼](https://qianxi.baidu.com/)提供的城内出行强度数据;
    
    6.74 新增[东方财富网](http://data.eastmoney.com/xg/xg/dxsyl.html/)提供的打新收益率数据;
    
    6.75 新增[东方财富网](http://data.eastmoney.com/bbsj/202003/yjyg.html/)提供的年报季报数据;
    
    6.76 新增[FutureSharks](https://github.com/FutureSharks/financial-data/)提供的高频日内数据;

7. 提供完善的接口文档, 提高 [AKShare](https://github.com/jindaxiang/akshare) 的易用性.

![思维导图](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/mindmap/AKShare.svg)

## [AKShare](https://github.com/jindaxiang/akshare) 的初衷

[AKShare](https://github.com/jindaxiang/akshare) 主要是用于财经研究, 解决在财经研究中数据获取困难的问题。传统的 CTA 策略以趋势为主, 但是自从 2017 年以来, 无论是长线还是短线的趋势策略都受制于商品波动率的降低, 面临了多多少少的回撤, 
同时市场也逐渐趋于机构化理性化, 因此在传统 CTA 策略的基础上加入基本面的因素显得迫在眉睫. 近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号, 它们的表现都与趋势策略有着很低的甚至负的相关性, 这样通过多种不同类型的信号对冲得到的策略, 就有机会在市场上取得非常棒的夏普率和稳定的收益. 
