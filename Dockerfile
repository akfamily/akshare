# https://hub.docker.com/layers/python/library/python/3.10.1-buster/images/sha256-d59f2d9d7f17d34ad8e0c4aff37e61b181018413078ab8f0a688319ebee65d30?context=explore
FROM python:3.10.1-buster

MAINTAINER AKFamily <akfamily.aktools@gmail.com>

# time-zone
RUN set -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir uvicorn
RUN pip install --no-cache-dir aktools
RUN pip install --no-cache-dir akshare --upgrade
