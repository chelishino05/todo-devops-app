"""
Todo List Manager - FastAPI Backend
Fully corrected, test-compatible version
"""

import logging
import time
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from models import TodoCreate, TodoUpdate, TodoResponse
from database import TodoDatabase, DatabaseError
from config import settings

# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Prometheus Metrics
# ---------------------------------------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

TODO_OPERATIONS = Counter(
    "todo_operations_total",
    "Total todo operations",
    ["operation", "status"]
)

# Global database instance
db = None

# ---------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    logger.info("Starting application...")
    db = TodoDatabase()
    yield
    logger.info("Shutting down application...")


# ---------------------------------------------------------
# FastAPI App Instance
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)

    return response


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# ---------------------------------------------------------
# Root → serve index.html
# ---------------------------------------------------------

@app.get("/")
async def root():
    return FileResponse("../frontend/index.html")

# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    try:
        stats = db.get_stats()
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "database": "connected",
            "stats": stats
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "app_name": settings.app_name,
                "version": settings.app_version,
                "database": "disconnected",
                "error": str(e)
            }
        )

# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ---------------------------------------------------------
# CRUD Routes
# ---------------------------------------------------------

@app.post("/api/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    try:
        created = db.create_todo(todo)
        TODO_OPERATIONS.labels("create", "success").inc()
        return TodoResponse(**created)
    except Exception as e:
        TODO_OPERATIONS.labels("create", "error").inc()
        raise HTTPException(500, str(e))


@app.get("/api/todos", response_model=List[TodoResponse])
async def get_all():
    todos = db.get_all_todos()
    return [TodoResponse(**t) for t in todos]


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_one(todo_id: int):
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(404, "Todo not found")
    return TodoResponse(**todo)


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update(todo_id: int, update: TodoUpdate):
    updated = db.update_todo(todo_id, update)
    if not updated:
        raise HTTPException(404, "Todo not found")
    return TodoResponse(**updated)


@app.delete("/api/todos/{todo_id}")
async def delete(todo_id: int):
    deleted = db.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(404, "Todo not found")
    return {"message": "Todo deleted"}


# ---------------------------------------------------------
# Local Dev Entrypoint
# ---------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info"
    )
