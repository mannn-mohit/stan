FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone && \
    apt-get clean

WORKDIR /workspace
COPY . /workspace/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt