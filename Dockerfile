# Simple CLI Notes Application with YDB - Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application files will be mounted as volume
# No need to copy application files

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Set environment variables with defaults
ENV YDB_ENDPOINT=grpc://ydb:2136
ENV YDB_DATABASE=/local

# Set the entrypoint
ENTRYPOINT ["python", "notes.py"]

# Default command shows help
CMD ["--help"]
