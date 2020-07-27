# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/16 21:39
Desc: 用 knn 训练模型来拟合数字, 但是要看样本的数量, 目前主要是 5 个样本
这里需要引入 sklearn package
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier

from akshare.movie.movie_maoyan_font import get_font_data


class Classify:
    def __init__(self):
        self.len = None
        self.knn = self.get_knn()

    @staticmethod
    def process_data(data):
        imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
        return pd.DataFrame(imputer.fit_transform(pd.DataFrame(data)))

    def get_knn(self):
        data = Classify.process_data(get_font_data())
        x_train = data.drop([0], axis=1)
        y_train = data[0]
        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(x_train, y_train)
        self.len = x_train.shape[1]
        return knn

    def knn_predict(self, data):
        df = pd.DataFrame(data)
        data = pd.concat(
            [
                df,
                pd.DataFrame(
                    np.zeros((df.shape[0], self.len - df.shape[1])),
                    columns=range(df.shape[1], self.len),
                ),
            ]
        )
        data = self.process_data(data)
        y_predict = self.knn.predict(data)
        return y_predict
