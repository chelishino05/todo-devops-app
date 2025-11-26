#!/bin/bash
# Azure startup script - forces uvicorn instead of gunicorn

echo "Starting Todo List API with uvicorn..."
cd /app
python -m uvicorn main:app --host 0.0.0.0 --port 8000