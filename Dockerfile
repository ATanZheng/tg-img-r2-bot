FROM python:3.11-slim

# 防止 Python 输出被缓冲，docker logs 能实时看到
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖（boto3 / https）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir \
    python-telegram-bot==20.7 \
    boto3

# 只拷贝程序文件（config.py 不进镜像）
COPY main.py ./

# 启动 Bot
CMD ["python", "main.py"]

