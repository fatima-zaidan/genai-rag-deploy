# ===== Base image =====
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Preconfigure pip and environment
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    CUDA_VISIBLE_DEVICES="" \
    PIP_DEFAULT_TIMEOUT=200

# Install essential build tools and system dependencies
# (Some Python libs like numpy, scipy, torch need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install CPU-only torch first (biggest dependency)
RUN pip install --no-cache-dir torch==2.2.0+cpu --index-url https://download.pytorch.org/whl/cpu

# Pre-install Gradio separately to avoid timeout/retry issues
RUN pip install --no-cache-dir gradio==4.44.0

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose your app port
EXPOSE 7860

# Default command
CMD ["python", "-m", "src.gradio_app"]
