# 📝 Todo List Manager - DevOps Project

A production-ready todo list application demonstrating modern DevOps practices including automated testing, CI/CD pipelines, containerization, and monitoring.

**Student:** Elias Nmeir  
**Course:** IE University - BCSAI - Software Development & DevOps  
**Assignment:** Individual Assignment 2

---
## 🌐 Live Demo

**Try the deployed application:** [https://todo-devops-app.onrender.com](https://todo-devops-app.onrender.com)

The application is deployed live on Render.com cloud platform with automatic deployment from GitHub.

**Available Endpoints:**
- Main App: [https://todo-devops-app.onrender.com](https://todo-devops-app.onrender.com)
- API Docs: [https://todo-devops-app.onrender.com/docs](https://todo-devops-app.onrender.com/docs)
- Health Check: [https://todo-devops-app.onrender.com/health](https://todo-devops-app.onrender.com/health)
- Metrics: [https://todo-devops-app.onrender.com/metrics](https://todo-devops-app.onrender.com/metrics)

⚠️ *Note: Free tier may take 30 seconds to wake up on first visit.*

---

## 🎯 Project Overview

This project transforms a simple todo list web application into a production-ready system with:

- ✅ **87% Test Coverage** (exceeds 70% requirement)
- ✅ **Automated CI/CD Pipeline** with GitHub Actions
- ✅ **Docker Containerization** for consistent deployment
- ✅ **Prometheus Monitoring** with health checks
- ✅ **Clean Code Architecture** following SOLID principles

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker Desktop (for containerized deployment)
- Git

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
│       └── ci.yml              # CI/CD pipeline configuration
├── backend/
│   ├── tests/                  # Test suite
│   │   ├── test_api.py        # API integration tests
│   │   ├── test_database.py   # Database unit tests
│   │   └── test_models.py     # Model validation tests
│   ├── config.py              # Configuration management
│   ├── database.py            # Database layer
│   ├── main.py                # FastAPI application
│   ├── models.py              # Pydantic models
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Main page
│   ├── script.js              # JavaScript logic
│   └── style.css              # Styling
├── .dockerignore              # Docker ignore rules
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image definition
├── DEPLOYMENT.md              # Deployment guide
├── REPORT.md                  # Comprehensive project report
└── README.md                  # This file
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

---

## 🐳 Docker

### Build Image
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

---

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Stages

1. **Test** - Runs all tests and checks coverage (≥70%)
2. **Lint** - Code quality checks with Black and Flake8
3. **Build** - Builds Docker image and pushes to GitHub Container Registry
4. **Deploy** - Deployment notification and instructions

### Trigger Pipeline
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

View pipeline status: [GitHub Actions](https://github.com/chelishino05/todo-devops-app/actions)

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Todo List API",
  "version": "1.0.0",
  "database": "connected",
  "stats": {
    "total": 0,
    "completed": 0,
    "pending": 0
  }
}
```

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

**Metrics Available:**
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `todo_operations_total` - Todo CRUD operations

---

## 📚 API Documentation

Interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Main Endpoints

- `GET /` - Main application page
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo

---

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **SQLite** - Database
- **Uvicorn** - ASGI server
- **Pytest** - Testing framework
- **Prometheus Client** - Metrics collection

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **Vanilla JavaScript** - Interactivity

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **GitHub Container Registry** - Image storage
- **Black & Flake8** - Code quality

---

## 🎓 Learning Outcomes

This project demonstrates:

- Clean code architecture with SOLID principles
- Comprehensive automated testing (unit + integration)
- Continuous Integration/Continuous Deployment
- Container orchestration with Docker
- Application monitoring and health checks
- Professional documentation practices

---

## 📖 Additional Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment instructions
- **[REPORT.md](REPORT.md)** - Comprehensive project report and learning journey

---

## 🤝 Contributing

This is an academic project, but feedback and suggestions are welcome!

---

## 📝 License

This project is for educational purposes as part of IE University coursework.

---

## 👤 Author

**Elias Nmeir**  
Computer Science & AI Student  
IE University, Madrid

---

## 🙏 Acknowledgments

- IE University DevOps Course
- FastAPI Documentation
- Docker Documentation
- GitHub Actions Community
- AI assistance for learning and guidance
