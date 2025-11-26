FROM python:3.10-slim

# System-level setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements early (Docker layer caching)
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY backend /app/backend
COPY frontend /app/frontend

# Switch to backend directory
WORKDIR /app/backend

# Expose port 8000 (Azure will map this to 80)
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

# Start server - Azure provides PORT environment variable
# If PORT is not set, default to 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}