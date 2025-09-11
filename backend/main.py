"""
Todo List Manager - DevOps Class Project
FastAPI backend providing RESTful API for todo management
Features: CRUD operations, SQLite persistence, automatic API docs
Author: Elias Nmeir
Date: September 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
from models import TodoCreate, TodoUpdate, TodoResponse
from database import TodoDatabase

# Create FastAPI app instance
app = FastAPI(title="Todo List API", version="1.0.0")

# Enable CORS (Cross-Origin Resource Sharing) for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = TodoDatabase()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Serve the main page
@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("../frontend/index.html")

# API Routes for CRUD operations

@app.post("/api/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    try:
        new_todo = db.create_todo(todo)
        return TodoResponse(**new_todo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/todos", response_model=List[TodoResponse])
async def get_all_todos():
    """Get all todo items"""
    try:
        todos = db.get_all_todos()
        return [TodoResponse(**todo) for todo in todos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    """Get a specific todo item"""
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(**todo)

@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update a todo item"""
    updated_todo = db.update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(**updated_todo)

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo item"""
    deleted = db.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
