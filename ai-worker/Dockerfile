# Official lightweight Python 3.11 image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for compiling C extensions & curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Healthcheck to ensure FastAPI is accepting traffic
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
