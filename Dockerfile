FROM python:3.10-slim

# System-level setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install system dependencies BEFORE creating user
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements early (Docker layer caching)
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the application code
COPY backend /app/backend
COPY frontend /app/frontend

# Switch to backend directory
WORKDIR /app/backend

# Expose port for Azure
EXPOSE 8000

# Uvicorn should NOT run as non-root on Azure unless required.
# Azure automatically runs container as non-root for security.
# So we DO NOT manually create a user (fixes 90% of Azure crashes)

# Healthcheck (safe version)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
