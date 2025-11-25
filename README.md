# 📝 Todo List Manager - DevOps Project

A production-ready todo list application demonstrating modern DevOps practices including automated testing, CI/CD pipelines, containerization, cloud deployment, and monitoring.

**Student:** Elias Nmeir  
**Course:** IE University - BCSAI - Software Development & DevOps  
**Assignment:** Individual Assignment 2

---

## 🌐 Live Demo

**Try the deployed application:** [https://todolist-eliasnmeir-2025.azurewebsites.net](https://todolist-eliasnmeir-2025.azurewebsites.net)

The application is deployed live on **Microsoft Azure** with automated CI/CD deployment from GitHub.

**Available Endpoints:**
- Main App: [https://todolist-eliasnmeir-2025.azurewebsites.net](https://todolist-eliasnmeir-2025.azurewebsites.net)
- API Docs: [https://todolist-eliasnmeir-2025.azurewebsites.net/docs](https://todolist-eliasnmeir-2025.azurewebsites.net/docs)
- Health Check: [https://todolist-eliasnmeir-2025.azurewebsites.net/health](https://todolist-eliasnmeir-2025.azurewebsites.net/health)
- Metrics: [https://todolist-eliasnmeir-2025.azurewebsites.net/metrics](https://todolist-eliasnmeir-2025.azurewebsites.net/metrics)

⚠️ *Note: Container startup may take 30-60 seconds on first visit.*

---

## 🎯 Project Overview

This project transforms a simple todo list web application into a production-ready system with:

- ✅ **87% Test Coverage** (exceeds 70% requirement)
- ✅ **Automated Azure CI/CD Pipeline** with GitHub Actions
- ✅ **Docker Containerization** with Azure Container Registry
- ✅ **Cloud Deployment** on Azure Web Apps
- ✅ **Prometheus Monitoring** with health checks
- ✅ **Secure Secret Management** with GitHub Secrets
- ✅ **Clean Code Architecture** following SOLID principles

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker Desktop (for local containerized deployment)
- Git
- Azure CLI (for manual deployment)

### Option 1: Run with Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/chelishino05/todo-devops-app.git
cd todo-devops-app

# Run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/chelishino05/todo-devops-app.git
cd todo-devops-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload

# Access the application
open http://localhost:8000
```

---

## 📁 Project Structure
```
todo-devops-app/
├── .github/
│   └── workflows/
│       └── azure-deploy.yml      # Azure CI/CD pipeline configuration
├── backend/
│   ├── tests/                    # Test suite
│   │   ├── test_api.py          # API integration tests
│   │   ├── test_database.py     # Database unit tests
│   │   └── test_models.py       # Model validation tests
│   ├── config.py                # Configuration management
│   ├── database.py              # Database layer
│   ├── main.py                  # FastAPI application
│   ├── models.py                # Pydantic models
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── index.html               # Main page
│   ├── script.js                # JavaScript logic
│   └── style.css                # Styling
├── .dockerignore                # Docker ignore rules
├── .gitignore                   # Git ignore rules (includes Azure credentials protection)
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker image definition
├── AZURE_DEPLOYMENT.md          # Azure deployment guide
├── REPORT.md                    # Comprehensive project report
└── README.md                    # This file
```

---

## 🧪 Testing

### Run All Tests
```bash
cd backend
pytest tests/ -v
```

### Run Tests with Coverage
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Test Results

- **Total Tests:** 29
- **Coverage:** 87%
- **Test Duration:** ~3 seconds
- **Coverage Threshold:** ≥70% (enforced in CI/CD)

---

## 🐳 Docker

### Build Image Locally
```bash
docker build -t todo-app:latest .
```

### Run Container
```bash
docker run -d -p 8000:8000 --name todo-app todo-app:latest
```

### Stop Container
```bash
docker stop todo-app
docker rm todo-app
```

### Azure Container Registry

The production Docker images are stored in Azure Container Registry:
- **Registry:** `todolisteliasnmeir2025acr.azurecr.io`
- **Image:** `todolist-app:latest`
- **Built automatically** via GitHub Actions on every push to main

---

## 🔄 CI/CD Pipeline

The project uses **GitHub Actions** for continuous integration and deployment to **Azure**.

### Pipeline Stages

1. **Test and Coverage** (2-3 min)
   - Installs Python dependencies
   - Runs pytest with coverage
   - Fails if coverage < 70%
   - Uploads coverage reports

2. **Code Linting** (1-2 min)
   - Runs Black formatter check
   - Runs Flake8 linter
   - Continues even with warnings

3. **Build Docker Image** (5-8 min)
   - Logs into Azure
   - Creates/uses Azure Container Registry
   - Builds Docker image using `az acr build`
   - Pushes to Azure Container Registry

4. **Deploy to Azure** (7-10 min)
   - Creates/uses App Service Plan
   - Creates/updates Azure Web App
   - Configures container settings
   - Restarts application

**Total Deployment Time:** 15-22 minutes (first deployment)

### Trigger Pipeline
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

View pipeline status: [GitHub Actions](https://github.com/chelishino05/todo-devops-app/actions)

### Security Features

- ✅ **GitHub Secrets** for all Azure credentials
- ✅ **No hardcoded secrets** in code or workflows
- ✅ **Credential masking** in logs
- ✅ **Protected .gitignore** prevents accidental commits

---

## ☁️ Azure Deployment

### Azure Resources Created

The CI/CD pipeline automatically creates and manages:

- **Resource Group:** `todolist-rg` (East US)
- **Container Registry:** `todolisteliasnmeir2025acr` (Basic SKU)
- **App Service Plan:** `todolist-plan` (Linux, B1 tier)
- **Web App:** `todolist-eliasnmeir-2025`

### Required GitHub Secrets

The following secrets must be configured in GitHub repository settings:

- `AZURE_CLIENT_ID` - Service Principal client ID
- `AZURE_CLIENT_SECRET` - Service Principal secret
- `AZURE_SUBSCRIPTION_ID` - Azure subscription ID
- `AZURE_TENANT_ID` - Azure Active Directory tenant ID
- `AZURE_WEBAPP_NAME` - Unique web app name (e.g., todolist-eliasnmeir-2025)

### Manual Deployment (if needed)

See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for detailed deployment instructions.

---

## 📊 Monitoring

### Health Check
```bash
curl https://todolist-eliasnmeir-2025.azurewebsites.net/health
```

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Todo List Manager",
  "version": "1.0.0",
  "database": "connected",
  "stats": {
    "total_todos": 0,
    "completed": 0,
    "pending": 0
  }
}
```

### Prometheus Metrics
```bash
curl https://todolist-eliasnmeir-2025.azurewebsites.net/metrics
```

**Metrics Available:**
- `http_requests_total` - Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds` - Request latency histogram
- `todo_operations_total` - Todo CRUD operations by operation and status

---

##  API Documentation

Interactive API documentation is available at:

- **Swagger UI:** https://todolist-eliasnmeir-2025.azurewebsites.net/docs
- **ReDoc:** https://todolist-eliasnmeir-2025.azurewebsites.net/redoc

### Main Endpoints

- `GET /` - Main application page
- `GET /health` - Health check endpoint with database status
- `GET /metrics` - Prometheus metrics endpoint
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo

---

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and settings management
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Pytest** - Testing framework
- **Prometheus Client** - Metrics collection

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **Vanilla JavaScript** - Interactivity

### DevOps & Cloud
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Azure Container Registry** - Docker image storage
- **Azure Web Apps** - Cloud hosting
- **Azure CLI** - Infrastructure management
- **Black & Flake8** - Code quality tools

---

##  Learning Outcomes

This project demonstrates:

- Clean code architecture with SOLID principles
- Comprehensive automated testing (unit + integration)
- Continuous Integration/Continuous Deployment
- Container orchestration with Docker
- Cloud deployment on Azure
- Secure secret management practices
- Application monitoring and health checks
- Infrastructure as Code principles
- Professional documentation practices

---

## Security Best Practices

- ✅ All sensitive credentials stored in GitHub Secrets
- ✅ Credentials never committed to Git repository
- ✅ `.gitignore` includes Azure credential patterns
- ✅ Secrets masked in GitHub Actions logs
- ✅ Service Principal with minimal required permissions
- ✅ HTTPS-only communication with Azure services

---

## 📖 Additional Documentation

- **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** - Azure deployment guide
- **[REPORT.md](REPORT.md)** - Comprehensive project report and learning journey
- **[SCREENSHOTS_GUIDE.md](SCREENSHOTS_GUIDE.md)** - Guide for documentation screenshots

---

## 🐛 Troubleshooting

### Application Not Loading
- Wait 30-60 seconds for container to start
- Check health endpoint: `/health`
- View Azure logs in Azure Portal → Web App → Log stream

### CI/CD Pipeline Failing
- Check GitHub Actions logs for specific error
- Verify all 5 GitHub Secrets are configured correctly
- Ensure Azure Service Principal has "Contributor" role


---

## 🤝 Contributing

This is an academic project, but feedback and suggestions are welcome!

---


## 👤 Author

**Elias Nmeir**  
Computer Science & AI Student  
IE University, Madrid

GitHub: [@chelishino05](https://github.com/chelishino05)

---

## Acknowledgments

- IE University DevOps Course
- FastAPI Documentation
- Docker Documentation  
- Microsoft Azure Documentation
- GitHub Actions Community

---

**Last Updated:** November 2025  
**Status:** ✅ Production Ready - Deployed on Azure