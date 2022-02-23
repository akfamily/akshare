# https://github.com/nikolaik/docker-python-nodejs
FROM nikolaik/python-nodejs:python3.8-nodejs16

MAINTAINER AKFamily <akfamily.akshare@gmail.com>

RUN set -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install akshare jupyterlab -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir jupyterlab
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir scipy
RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir aktools
RUN pip install --no-cache-dir akshare --upgrade
