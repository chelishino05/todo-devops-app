# Deployment Guide

## Overview
This application uses GitHub Actions for CI/CD and deploys as a Docker container to GitHub Container Registry (GHCR).

## Automated Deployment

### CI/CD Pipeline
The pipeline automatically runs on every push to `main`:

1. **Test Stage**: Runs all tests and checks coverage (≥70%)
2. **Lint Stage**: Checks code quality
3. **Build Stage**: Builds Docker image and pushes to GHCR
4. **Deploy Stage**: Notifies successful deployment

### Triggering Deployment
```bash
git push origin main
```

## Manual Deployment

### Pull the Latest Image
```bash
docker pull ghcr.io/chelishino05/todo-devops-app:latest
```

### Run the Container
```bash
docker run -d -p 8000:8000 --name todo-app ghcr.io/chelishino05/todo-devops-app:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

## Accessing the Application

- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

## Environment Variables

You can configure the application using environment variables:
```bash
docker run -d -p 8000:8000 \
  -e APP_NAME="My Todo App" \
  -e DEBUG_MODE=False \
  -e DATABASE_NAME=todos.db \
  ghcr.io/chelishino05/todo-devops-app:latest
```

## Monitoring

### Check Container Health
```bash
docker ps
docker logs todo-app
```

### View Metrics
Visit http://localhost:8000/metrics for Prometheus metrics

## Stopping the Application
```bash
docker stop todo-app
docker rm todo-app
```

Or with Docker Compose:
```bash
docker-compose down
```

## Troubleshooting

### Container won't start
```bash
docker logs todo-app
```

### Port already in use
```bash
# Use a different port
docker run -d -p 8080:8000 --name todo-app ghcr.io/chelishino05/todo-devops-app:latest
```

### Pull latest changes
```bash
docker pull ghcr.io/chelishino05/todo-devops-app:latest
docker stop todo-app
docker rm todo-app
docker run -d -p 8000:8000 --name todo-app ghcr.io/chelishino05/todo-devops-app:latest
```