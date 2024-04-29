#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/26 17:30
Desc: AKShare's PYPI info file
"""

import ast
import re

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_version_string() -> str:
    """
    get the version of akshare
    :return: version number
    :rtype: str, e.g. '0.6.24'
    """
    with open("akshare/__init__.py", "rb") as _f:
        version_line = re.search(
            pattern=r"__version__\s+=\s+(.*)", string=_f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


setuptools.setup(
    name="akshare",
    version=get_version_string(),
    author="AKFamily",
    author_email="albertandking@gmail.com",
    license="MIT",
    description="AKShare is an elegant and simple financial data interface library for Python, built for human beings!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akfamily/akshare",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.1",
        "lxml>=4.2.1",
        "pandas>=0.25",
        "requests>=2.22.0",
        "html5lib>=1.0.1",
        "xlrd>=1.2.0",
        "urllib3>=1.25.8",
        "tqdm>=4.43.0",
        "openpyxl>=3.0.3",
        "jsonpath>=0.82",
        "tabulate>=0.8.6",
        "decorator>=4.4.2",
        "py-mini-racer>=0.6.0",
        "akracer>=0.0.11",
    ],
    extras_require={
        # 这些是额外的依赖集合，可以通过 'pip install akshare[full]' 安装
        "full": [
            "akqmt",
        ],
        # 这些是额外的依赖集合，可以通过 'pip install akshare[qmt]' 安装
        "qmt": [
            "akqmt",
        ],
    },
    package_data={"": ["*.py", "*.json", "*.pk", "*.js", "*.zip"]},
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
