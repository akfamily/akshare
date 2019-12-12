# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/12 15:08
contact: jindaxiang@163.com
desc: 
"""
import newspaper

sina_paper = newspaper.build('http://futures.hexun.com/domestic/', language='zh')
for article in sina_paper.articles:
    print(article)

sina_paper.size()
first_article = sina_paper.articles[5]
first_article.download()
first_article.parse()
print(first_article.title)
print(first_article.text)
