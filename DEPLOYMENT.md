# Deployment Guide

## Overview
This application uses GitHub Actions for CI/CD and deploys as a Docker container to GitHub Container Registry (GHCR).



**Production URL:** https://todo-devops-app.onrender.com

The application is deployed and running live on Render.com cloud platform.

### Quick Access

- **Main Application:** https://todo-devops-app.onrender.com
- **API Documentation:** https://todo-devops-app.onrender.com/docs
- **Health Check:** https://todo-devops-app.onrender.com/health
- **Metrics:** https://todo-devops-app.onrender.com/metrics

**Note:** Free tier may take 30 seconds to wake up on first visit if the app has been idle.

---

## Cloud Deployment Details

### Platform: Render.com

**Why Render?**
- Free tier suitable for student projects
- Automatic deployment from GitHub
- Built-in HTTPS
- Docker support
- Easy configuration

**Deployment Configuration:**
- **Platform:** Render Web Service
- **Region:** EU Central (Frankfurt)
- **Runtime:** Docker
- **Instance:** Free tier (750 hours/month)
- **Auto-Deploy:** Enabled from main branch

### Deployment Process

1. **Code Push:** Developer pushes code to GitHub main branch
2. **CI Pipeline:** GitHub Actions runs tests and builds Docker image
3. **Webhook Trigger:** Render detects changes via GitHub webhook
4. **Container Build:** Render pulls code and rebuilds Docker container
5. **Deployment:** New version deployed automatically with zero downtime
6. **Health Check:** Render monitors /health endpoint

### First Deployment
- **Date:** November 18, 2025
- **Status:** ✅ Successfully deployed
- **Build Time:** ~5 minutes
- **Deployment Time:** ~30 seconds

---


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