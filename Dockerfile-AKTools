FROM python:3.10.1-buster

USER root
RUN pip install --no-cache-dir akshare fastapi uvicorn -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir aktools --upgrade -i https://pypi.org/simple
