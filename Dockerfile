FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone && \
    apt-get clean

RUN useradd -ms /bin/bash dev

WORKDIR /workspace
USER dev

# Copy source code and install Python deps
COPY --chown=dev:dev . /workspace

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt