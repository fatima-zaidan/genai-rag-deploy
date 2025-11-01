# ===== Base image =====
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Preconfigure pip
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    CUDA_VISIBLE_DEVICES=""

# Copy only requirements first (to use Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install CPU-only torch + dependencies in one layer
# Upgrade pip
RUN pip install --upgrade pip

# Install torch from PyTorch index
RUN pip install --no-cache-dir torch==2.2.0+cpu --index-url https://download.pytorch.org/whl/cpu

# Install the rest of requirements from PyPI
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose your app port
EXPOSE 7860

# Default command
CMD ["python", "-m", "src.gradio_app"]
