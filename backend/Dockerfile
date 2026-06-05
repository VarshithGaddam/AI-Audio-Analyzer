FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Fortran compiler
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libsndfile1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .

# Install packages with verbose output
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
