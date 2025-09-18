from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    """Model for creating a new todo item"""
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None

class TodoUpdate(BaseModel):
    """Model for updating an existing todo item"""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None



class TodoResponse(BaseModel):
    """Model for returning todo data to frontend"""
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[str]
    completed: bool
    created_at: str
    
    class Config:
        # This allows the model to work with database objects
        from_attributes = True
