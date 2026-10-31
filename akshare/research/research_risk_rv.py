#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 修大成主页-Risk Lab-Realized Volatility
"""

import warnings

import pandas as pd
from bs4 import BeautifulSoup

from akshare.utils import http


def article_rlab_rv(symbol: str = "39693") -> pd.DataFrame:
    """
    修大成主页-Risk Lab-Realized Volatility
    :param symbol: str 股票代码
    :return: pandas.DataFrame
    1996-01-02    0.000000
    1996-01-04    0.000000
    1996-01-05    0.000000
    1996-01-09    0.000000
    1996-01-10    0.000000
                    ...
    2019-11-04    0.175107
    2019-11-05    0.185112
    2019-11-06    0.210373
    2019-11-07    0.240808
    2019-11-08    0.199549
    Name: RV, Length: 5810, dtype: float64

    Website
    https://dachxiu.chicagobooth.edu/

    Objective
    We provide up-to-date daily annualized realized volatilities for individual stocks, ETFs, and future contracts, which are estimated from high-frequency data. We are in the process of incorporating equities from global markets.

    Data
    We collect trades at their highest frequencies available (up to every millisecond for US equities after 2007), and clean them using the prevalent national best bid and offer (NBBO) that are available up to every second. The mid-quotes are calculated based on the NBBOs, so their highest sampling frequencies are also up to every second.

    Methodology
    We provide quasi-maximum likelihood estimates of volatility (QMLE) based on moving-average models MA(q), using non-zero returns of transaction prices (or mid-quotes if available) sampled up to their highest frequency available, for days with at least 12 observations. We select the best model (q) using Akaike Information Criterion (AIC). For comparison, we report realized volatility (RV) estimates using 5-minute and 15-minute subsampled returns.

    References
    1. “When Moving-Average Models Meet High-Frequency Data: Uniform Inference on Volatility”, by Rui Da and Dacheng Xiu. 2017.
    2. “Quasi-Maximum Likelihood Estimation of Volatility with High Frequency Data”, by Dacheng Xiu. Journal of Econometrics, 159 (2010), 235-250.
    3. “How Often to Sample A Continuous-time Process in the Presence of Market Microstructure Noise”, by Yacine Aït-Sahalia, Per Mykland, and Lan Zhang. Review of Financial Studies, 18 (2005), 351–416.
    4. “The Distribution of Exchange Rate Volatility”, by Torben Andersen, Tim Bollerslev, Francis X. Diebold, and Paul Labys. Journal of the American Statistical Association, 96 (2001), 42-55.
    5. “Econometric Analysis of Realized Volatility and Its Use in Estimating Stochastic Volatility Models”, by Ole E Barndorff‐Nielsen and Neil Shephard. Journal of the Royal Statistical Society: Series B, 64 (2002), 253-280.
    """
    warnings.warn("由于服务器在国外, 请稍后, 如果访问失败, 请使用代理工具")
    url = "https://dachxiu.chicagobooth.edu/data.php"
    payload = {"ticker": symbol}
    res = http.get(url, params=payload)
    soup = BeautifulSoup(res.text, "lxml")
    title_fore = (
        pd.DataFrame(soup.find("p").get_text().split(symbol)).iloc[0, 0].strip()
    )
    title_list = (
        pd.DataFrame(soup.find("p").get_text().split(symbol))
        .iloc[1, 0]
        .strip()
        .split("\n")
    )
    title_list.insert(0, title_fore)
    temp_df = pd.DataFrame(soup.find("p").get_text().split(symbol)).iloc[2:, :]
    temp_df = temp_df.iloc[:, 0].str.split(" ", expand=True)
    temp_df = temp_df.iloc[:, 1:]
    temp_df.iloc[:, -1] = temp_df.iloc[:, -1].str.replace(r"\n", "")
    temp_df = temp_df.reset_index()
    temp_df.index = pd.to_datetime(temp_df.iloc[:, 1], format="%Y%m%d", errors="coerce")
    temp_df = temp_df.iloc[:, 1:]
    data_se = temp_df.iloc[:, 1]
    data_se.name = "RV"
    temp_df = data_se.astype("float", errors="ignore")
    temp_df.index.name = "date"
    return temp_df


if __name__ == "__main__":
    article_rlab_rv_df = article_rlab_rv(symbol="39693")
    print(article_rlab_rv_df)
