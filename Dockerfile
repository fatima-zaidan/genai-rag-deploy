# ===== Stage 1: Builder (Installs dependencies and cleans up build tools) =====
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Preconfigure pip and environment
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=200

# Install build tools for compiling Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip, install dependencies, and clean pip cache
# PyTorch is installed automatically if listed in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# ===== Stage 2: Runtime (Minimal image for deployment) =====
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Runtime environment
ENV PYTHONUNBUFFERED=1 \
    CUDA_VISIBLE_DEVICES=""

# Expose Gradio port
EXPOSE 7860

# Default command
CMD ["python", "-m", "src.gradio_app"]