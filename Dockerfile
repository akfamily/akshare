# 使用精简镜像，镜像体积从 1.2G 下降为约 400M，提高启动效率，同时升级到 Python 3.12.x 提高 20% 以上性能
FROM python:3.12-slim-bullseye

# 升级 pip 到最新版
RUN pip install --upgrade pip

# 新增 gunicorn 安装，提升并发和并行能力
RUN pip install --no-cache-dir akshare fastapi uvicorn gunicorn -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN pip install --no-cache-dir aktools -i https://pypi.org/simple --upgrade

# 设置工作目录方便启动
ENV APP_HOME=/usr/local/lib/python3.11/site-packages/aktools
WORKDIR $APP_HOME

# 默认启动 gunicorn 服务
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app", "-k", "uvicorn.workers.UvicornWorker"]
