FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (Cloud Run uses PORT env var, default 8080)
EXPOSE 8080

# Set default port
ENV PORT=8080

# Run with gunicorn using PORT env var
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 run:app
