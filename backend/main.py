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
# Static files - FIXED PATH
# ---------------------------------------------------------

app.mount("/static", StaticFiles(directory="frontend"), name="static")


# ---------------------------------------------------------
# Root Route
# ---------------------------------------------------------

@app.get("/")
async def root():
    """Serve the frontend HTML"""
    return FileResponse("frontend/index.html")


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    """Health check endpoint with database status"""
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
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


# ---------------------------------------------------------
# Metrics Endpoint
# ---------------------------------------------------------

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# ---------------------------------------------------------
# Todo CRUD Endpoints
# ---------------------------------------------------------

@app.post("/api/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    try:
        new_todo = db.create_todo(todo)
        TODO_OPERATIONS.labels(operation="create", status="success").inc()
        logger.info(f"Created todo: {new_todo['id']}")
        return new_todo
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation="create", status="error").inc()
        logger.error(f"Failed to create todo: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        TODO_OPERATIONS.labels(operation="create", status="error").inc()
        logger.error(f"Unexpected error creating todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/todos", response_model=List[TodoResponse])
async def get_all_todos():
    """Get all todo items"""
    try:
        todos = db.get_all_todos()
        TODO_OPERATIONS.labels(operation="read_all", status="success").inc()
        return todos
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation="read_all", status="error").inc()
        logger.error(f"Failed to fetch todos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        TODO_OPERATIONS.labels(operation="read_all", status="error").inc()
        logger.error(f"Unexpected error fetching todos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    """Get a specific todo item"""
    try:
        todo = db.get_todo_by_id(todo_id)
        if not todo:
            TODO_OPERATIONS.labels(operation="read", status="not_found").inc()
            raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
        TODO_OPERATIONS.labels(operation="read", status="success").inc()
        return todo
    except HTTPException:
        raise
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation="read", status="error").inc()
        logger.error(f"Failed to fetch todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        TODO_OPERATIONS.labels(operation="read", status="error").inc()
        logger.error(f"Unexpected error fetching todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo: TodoUpdate):
    """Update a todo item"""
    try:
        updated = db.update_todo(todo_id, todo)
        if not updated:
            TODO_OPERATIONS.labels(operation="update", status="not_found").inc()
            raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
        TODO_OPERATIONS.labels(operation="update", status="success").inc()
        logger.info(f"Updated todo: {todo_id}")
        return updated
    except HTTPException:
        raise
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation="update", status="error").inc()
        logger.error(f"Failed to update todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        TODO_OPERATIONS.labels(operation="update", status="error").inc()
        logger.error(f"Unexpected error updating todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo item"""
    try:
        success = db.delete_todo(todo_id)
        if not success:
            TODO_OPERATIONS.labels(operation="delete", status="not_found").inc()
            raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
        TODO_OPERATIONS.labels(operation="delete", status="success").inc()
        logger.info(f"Deleted todo: {todo_id}")
        return {"message": f"Todo {todo_id} deleted successfully"}
    except HTTPException:
        raise
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation="delete", status="error").inc()
        logger.error(f"Failed to delete todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        TODO_OPERATIONS.labels(operation="delete", status="error").inc()
        logger.error(f"Unexpected error deleting todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")