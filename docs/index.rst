欢迎访问 AKShare 在线文档！
===========================================

AKShare 是基于 Python 的开源财经数据接口库，提供股票、期货、期权、基金、债券、外汇、宏观经济等 1000 余个数据接口，返回结果均为带中文列名的 pandas DataFrame。

.. code-block:: bash

   pip install akshare --upgrade

.. container:: ak-home

   .. grid:: 1 2 2 4
      :gutter: 3

      .. grid-item-card:: 快速入门
         :link: tutorial
         :link-type: doc

         五分钟完成安装和第一次数据获取

      .. grid-item-card:: 数据字典
         :link: data/index
         :link-type: doc

         按类目浏览全部接口的参数、输出与示例

      .. grid-item-card:: 接口检索
         :link: search
         :link-type: doc

         用 ak.search() 按关键词查找接口

      .. grid-item-card:: 常见问题
         :link: faq
         :link-type: doc

         安装失败、接口报错等问题的解决办法

推荐
----

.. container:: ak-home

   .. grid:: 1 1 3 3
      :gutter: 3

      .. grid-item-card:: AKQuant 量化投研框架
         :link: https://akquant.akfamily.xyz/
         :class-card: ak-promo-card

         高性能量化投研框架，与 AKShare 数据无缝衔接，``pip install akquant`` 一键安装

      .. grid-item-card:: 期魔方
         :link: https://qmfquant.com
         :class-card: ak-promo-card

         本地化期货量化分析工具，无需复杂部署，支持数据分析和机器学习，研究功能免费开放

      .. grid-item-card:: 实盘交易服务
         :link: trade
         :link-type: doc
         :class-card: ak-promo-card

         股票、期权、两融与期货的实盘 API 对接、费率优惠和量化定制服务

.. raw:: html

   <div class="ak-wechat-banner">
     <img src="_static/wechat_qrcode.jpg" alt="微信公众号【数据科学实战】二维码" width="104" height="104">
     <div>
       <p class="ak-wechat-banner-title">关注微信公众号【数据科学实战】</p>
       <p>获取更多财经数据与量化投研知识，微信扫码或搜索“数据科学实战”即可关注。</p>
     </div>
   </div>

.. 下面的目录不在首页显示，用于确定全站的页面结构；顶栏入口见 _templates/ak-navbar.html。

.. toctree::
   :hidden:
   :caption: 入门

   introduction
   installation
   uv
   tutorial
   search
   faq

.. toctree::
   :hidden:
   :caption: 数据字典

   data/index

.. toctree::
   :hidden:
   :caption: 进阶

   backtest
   indicator
   quant_platforms
   aktools
   docker
   articles

.. toctree::
   :hidden:
   :caption: 项目

   changelog
   migration
   contributing
   acknowledgements

.. toctree::
   :hidden:
   :caption: 实盘交易

   trade
