FROM python:3.10.1-buster

MAINTAINER AKFamily <aktools@akfamily.email.cn>

RUN pip install --no-cache-dir fastapi uvicorn
RUN pip install --no-cache-dir aktools akshare -i https://pypi.org/simple
