"""
Todo List Manager - DevOps Class Project
FastAPI backend providing RESTful API for todo management
Features: CRUD operations, SQLite persistence, monitoring, health checks

Author: Elias Nmeir
Date: November 2025
"""

import logging
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time

from models import TodoCreate, TodoUpdate, TodoResponse
from database import TodoDatabase, DatabaseError
from config import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request latency', 
    ['method', 'endpoint']
)
TODO_OPERATIONS = Counter(
    'todo_operations_total',
    'Total todo operations',
    ['operation', 'status']
)

# Database instance
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global db
    logger.info("Starting up application...")
    db = TodoDatabase()
    yield
    logger.info("Shutting down application...")


# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)


# Middleware for request logging and metrics
@app.middleware("http")
async def log_and_measure_requests(request: Request, call_next):
    """Log all requests and measure latency"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate latency
    latency = time.time() - start_time
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed with status {response.status_code} in {latency:.3f}s"
    )
    
    # Record metrics
    if settings.enable_metrics:
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


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


# Root endpoint - serve main page
@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("../frontend/index.html")


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    Returns application status and database connectivity
    """
    try:
        # Check database connectivity
        stats = db.get_stats()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "app_name": settings.app_name,
                "version": settings.app_version,
                "database": "connected",
                "stats": stats
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
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


# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# API Routes for CRUD operations

@app.post("/api/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    try:
        new_todo = db.create_todo(todo)
        TODO_OPERATIONS.labels(operation='create', status='success').inc()
        return TodoResponse(**new_todo)
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation='create', status='error').inc()
        logger.error(f"Failed to create todo: {e}")
        raise HTTPException(status_code=500, detail="Failed to create todo")
    except Exception as e:
        TODO_OPERATIONS.labels(operation='create', status='error').inc()
        logger.error(f"Unexpected error creating todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/todos", response_model=List[TodoResponse])
async def get_all_todos():
    """Get all todo items"""
    try:
        todos = db.get_all_todos()
        TODO_OPERATIONS.labels(operation='read_all', status='success').inc()
        return [TodoResponse(**todo) for todo in todos]
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation='read_all', status='error').inc()
        logger.error(f"Failed to retrieve todos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todos")
    except Exception as e:
        TODO_OPERATIONS.labels(operation='read_all', status='error').inc()
        logger.error(f"Unexpected error retrieving todos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    """Get a specific todo item"""
    try:
        todo = db.get_todo_by_id(todo_id)
        if not todo:
            TODO_OPERATIONS.labels(operation='read', status='not_found').inc()
            raise HTTPException(status_code=404, detail="Todo not found")
        
        TODO_OPERATIONS.labels(operation='read', status='success').inc()
        return TodoResponse(**todo)
    except HTTPException:
        raise
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation='read', status='error').inc()
        logger.error(f"Failed to retrieve todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todo")
    except Exception as e:
        TODO_OPERATIONS.labels(operation='read', status='error').inc()
        logger.error(f"Unexpected error retrieving todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update a todo item"""
    try:
        updated_todo = db.update_todo(todo_id, todo_update)
        if not updated_todo:
            TODO_OPERATIONS.labels(operation='update', status='not_found').inc()
            raise HTTPException(status_code=404, detail="Todo not found")
        
        TODO_OPERATIONS.labels(operation='update', status='success').inc()
        return TodoResponse(**updated_todo)
    except HTTPException:
        raise
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation='update', status='error').inc()
        logger.error(f"Failed to update todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update todo")
    except Exception as e:
        TODO_OPERATIONS.labels(operation='update', status='error').inc()
        logger.error(f"Unexpected error updating todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo item"""
    try:
        deleted = db.delete_todo(todo_id)
        if not deleted:
            TODO_OPERATIONS.labels(operation='delete', status='not_found').inc()
            raise HTTPException(status_code=404, detail="Todo not found")
        
        TODO_OPERATIONS.labels(operation='delete', status='success').inc()
        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except DatabaseError as e:
        TODO_OPERATIONS.labels(operation='delete', status='error').inc()
        logger.error(f"Failed to delete todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete todo")
    except Exception as e:
        TODO_OPERATIONS.labels(operation='delete', status='error').inc()
        logger.error(f"Unexpected error deleting todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info"
    )