"""
Tests for Pydantic models
Tests data validation and serialization
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import TodoCreate, TodoUpdate, TodoResponse
from pydantic import ValidationError


class TestTodoCreate:
    """Test TodoCreate model"""
    
    def test_create_with_all_fields(self):
        """Test creating todo with all fields"""
        todo = TodoCreate(
            title="Test Todo",
            description="Test Description",
            due_date="2025-12-31"
        )
        
        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.due_date == "2025-12-31"
    
    def test_create_with_required_only(self):
        """Test creating todo with only required fields"""
        todo = TodoCreate(title="Minimal Todo")
        
        assert todo.title == "Minimal Todo"
        assert todo.description is None
        assert todo.due_date is None
    
    def test_create_without_title(self):
        """Test that title is required"""
        with pytest.raises(ValidationError):
            TodoCreate()


class TestTodoUpdate:
    """Test TodoUpdate model"""
    
    def test_update_all_fields(self):
        """Test updating all fields"""
        update = TodoUpdate(
            title="New Title",
            description="New Description",
            due_date="2026-01-01",
            completed=True
        )
        
        assert update.title == "New Title"
        assert update.description == "New Description"
        assert update.due_date == "2026-01-01"
        assert update.completed is True
    
    def test_update_partial(self):
        """Test partial update"""
        update = TodoUpdate(completed=True)
        
        assert update.completed is True
        assert update.title is None
        assert update.description is None
    
    def test_update_empty(self):
        """Test update with no fields"""
        update = TodoUpdate()
        
        assert update.title is None
        assert update.description is None
        assert update.due_date is None
        assert update.completed is None


class TestTodoResponse:
    """Test TodoResponse model"""
    
    def test_response_model(self):
        """Test TodoResponse with all fields"""
        response = TodoResponse(
            id=1,
            title="Test",
            description="Description",
            due_date="2025-12-31",
            completed=False,
            created_at="2025-11-11T00:00:00"
        )
        
        assert response.id == 1
        assert response.title == "Test"
        assert response.completed is False