# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/11 13:58
Desc: AkShare's pypi info file
"""
import re
import ast

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_version_string():
    """
    get the akshare version number
    :return: version number
    :rtype: str, e.g. '0.3.24'
    """
    with open("akshare/__init__.py", "rb") as _f:
        version_line = re.search(
            r"__version__\s+=\s+(.*)", _f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


setuptools.setup(
    name="akshare",
    version=get_version_string(),
    author="Albert King",
    author_email="jindaxiang@163.com",
    license="MIT",
    description="A tool for downloading economic and financial data!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jindaxiang/akshare",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.1",
        "lxml>=4.2.1",
        "matplotlib>=3.1.1",
        "numpy>=1.15.4",
        "pandas>=0.25",
        "requests>=2.22.0",
        "demjson>=2.2.4",
        "pyexecjs>=1.5.1",
        "pillow>=6.2.0",
        "pypinyin>=0.35.0",
        "websocket-client>=0.56.0",
        "html5lib>=1.0.1",
        "scikit-learn>=0.22",
        "fonttools>=4.2.2",
        "xlrd>=1.2.0",
        "tqdm>=4.43.0",
        "openpyxl>=3.0.3",
        "jsonpath>=0.82",
        "tabulate>=0.8.6",
        "decorator>=4.4.2",
    ],
    package_data={"": ["*.py", "*.json", "*.pk", "*.woff", "*.js"]},
    keywords=[
        "stock",
        "option",
        "futures",
        "fund",
        "bond",
        "index",
        "air",
        "finance",
        "spider",
        "quant",
        "quantitative",
        "investment",
        "trading",
        "algotrading",
        "data",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
