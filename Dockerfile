FROM python:3.11-slim

# Set timezone non-interactively and install deps in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata git && \
    ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user early
RUN useradd -ms /bin/bash dev

# Set working dir as root (for pip install)
WORKDIR /workspace

# Copy only requirements first to leverage cache
COPY requirements.txt .

# Install pip deps as root (common in devcontainers)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app code
COPY --chown=dev:dev . .

# Switch to non-root user for safety
USER dev
