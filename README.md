# 📝 Todo List Manager - DevOps Project (Render Deployment)

A production-ready todo list application demonstrating modern DevOps practices including automated testing, CI/CD pipelines, containerization, cloud deployment on **Render**, and monitoring.

**Student:** Elias Nmeir  
**Course:** IE University - BCSAI - Software Development & DevOps  
**Assignment:** Individual Assignment 2

---

## 🌐 Live Demo

**Try the deployed application on Render:**  
👉 https://todo-devops-app.onrender.com

**Available Endpoints:**
- Main App: https://todo-devops-app.onrender.com
- API Docs: https://todo-devops-app.onrender.com/docs
- ReDoc: https://todo-devops-app.onrender.com/redoc
- Health Check: https://todo-devops-app.onrender.com/health

⚠️ *Note: Render free tier sleeps after inactivity. The first request may take 20–40 seconds to cold-start.*

---

## 🎯 Project Overview

This project transforms a simple todo list web application into a production-ready system with:

- ✅ **87% Test Coverage** (exceeds 70% requirement)  
- ✅ **Automated CI/CD Pipeline** with GitHub Actions  
- ✅ **Docker Containerization**  
- ✅ **Cloud Deployment on Render Web Services**  
- ✅ **Health Checks & Basic Monitoring**  
- ✅ **Secure Secret Management** with GitHub Secrets  
- ✅ **Clean Code Architecture** following SOLID principles  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+  
- Docker Desktop  
- Git  
- Render account  

---

## ▶️ Option 1: Run with Docker (Recommended)

```bash
git clone https://github.com/chelishino05/todo-devops-app.git
cd todo-devops-app

docker build -t todo-app .
docker run -p 8000:8000 todo-app
```

Access locally at **http://localhost:8000**

---

## ▶️ Option 2: Run Locally Without Docker

```bash
git clone https://github.com/chelishino05/todo-devops-app.git
cd todo-devops-app

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

Access: **http://localhost:8000**

---

## 📁 Project Structure

```
todo-devops-app/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── __init__.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_models.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .github/workflows/
│   └── ci.yml
└── README.md
```

---

# ☁️ Render Deployment (Replaces Azure Section)

Your application is deployed using **Render Web Services** which automatically builds and deploys your Docker container.

### Render Deployment Steps

1. **Connect GitHub repository** to Render  
2. Click **"New Web Service"**  
3. Choose **"Build & Deploy from a Git repository"**  
4. Select your repo  
5. Select runtime: **Docker**  
6. Render auto-detects your Dockerfile  
7. It builds → deploys → runs your container  
8. Your app becomes live at:  
   **https://todo-devops-app.onrender.com**

### Render Build Process

Render executes the Dockerfile:

```
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables (Render Dashboard)
- `PYTHON_VERSION=3.10`  
- Any additional secrets added manually  

### Auto-Deploy
Render automatically redeploys on every push to `main`.

---

# 🔄 CI/CD Pipeline (Converted from Azure → Render Compatible)

The Azure stages have been removed and replaced with Render-compatible CI/CD:

### Pipeline Stages

1. **Test & Coverage**
2. **Linting**
3. **Build Docker Image**
4. **Render Auto-Deploy Trigger (optional)**

### Trigger Pipeline
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### GitHub Secrets (Render version)
Render does not require Azure-level secrets.

Optional:
- `RENDER_API_KEY` (only if using Render API deployments)

---

# 🧪 Testing

### Run all tests
```bash
pytest -v
```

### Run with coverage
```bash
pytest --cov=backend
```

### Test Results

- **Total Tests:** 29  
- **Coverage:** 87%  
- **CI Threshold:** 70%  

---

# 🐳 Docker

### Build
```bash
docker build -t todo-app .
```

### Run
```bash
docker run -p 8000:8000 todo-app
```

### Compose
```bash
docker-compose up --build
```

---

# 📊 Monitoring

Render does not support Prometheus scraping on free tier.

### Provided Endpoints:
- `/health` (JSON status)
- `/` (frontend)
- `/docs` (Swagger)
- Render log dashboard for observability  

---

# 📖 API Documentation

Available live at:

- Swagger: https://todo-devops-app.onrender.com/docs  
- ReDoc: https://todo-devops-app.onrender.com/redoc  

### Main Endpoints

- `GET /`
- `GET /health`
- `GET /todos`
- `POST /todos`
- `DELETE /todos/{id}`

---

# 🛠️ Technologies Used

### Backend
- FastAPI  
- SQLite  
- Pydantic  
- Uvicorn  

### DevOps
- Docker  
- GitHub Actions  
- Render  

### Testing
- Pytest  
- Coverage  

### Frontend
- HTML  
- CSS  
- JavaScript  

---

# 🎓 Learning Outcomes

This project demonstrates:

- Containerized cloud deployment  
- CI/CD with GitHub Actions  
- Test-driven development  
- Clean architecture following SOLID principles  
- Docker orchestration  
- Cloud deployment on Render  
- Secure secret management  
- Professional DevOps documentation  

---

# 🐛 Troubleshooting

### ❗ Render app takes long to load
→ Cold start on free tier  
→ Wait 20–40 seconds  

### ❗ Deployment failing
Check:
- Dockerfile paths  
- `backend.main:app`  
- Render logs  

### ❗ Database errors
Delete local `todos.db` and restart

---

# 👤 Author

**Elias Nmeir**  
IE University — BCSAI  
GitHub: https://github.com/chelishino05

---

# ✔ Last Updated
**November 2025 — Render Deployment Edition**
