FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl sqlite3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY frontend/ ./frontend/

# Copy startup script
COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Ensure /tmp is writable
RUN chmod 777 /tmp

EXPOSE 8000

# Use startup script
CMD ["/app/startup.sh"]
```

6. **Save** (Cmd+S)

---

### **FILE 3: `.github/workflows/deploy.yml`**

**Location:** `.github/workflows/` folder (REPLACE existing file)

**Steps:**
1. In VS Code left sidebar, expand `.github` folder
2. Expand `workflows` folder inside it
3. **Click on `deploy.yml`**
4. **Select All** (Cmd+A)
5. **Delete** everything
6. **Paste** the workflow content (from the download or copy from my previous message)
7. **Save** (Cmd+S)

---

## 📊 **YOUR PROJECT STRUCTURE SHOULD LOOK LIKE THIS:**
```
todo-devops-app/
├── .github/
│   └── workflows/
│       └── deploy.yml          ← FILE 3 (modified)
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   └── ...
├── frontend/
│   ├── index.html
│   └── ...
├── Dockerfile                   ← FILE 2 (modified)
├── startup.sh                   ← FILE 1 (NEW - create this!)
├── README.md
├── docker-compose.yml
└── ...