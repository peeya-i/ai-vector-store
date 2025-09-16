FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python packages with specific versions
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "uvicorn[standard]" && \
    pip install --no-cache-dir --force-reinstall huggingface-hub==0.16.4

# Copy the rest of the application
COPY . .

# Create data directory for LanceDB
RUN mkdir -p data/lancedb

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]