"""
Unit tests for database operations
Tests CRUD operations and error handling
"""

import pytest
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import TodoDatabase, DatabaseError
from models import TodoCreate, TodoUpdate


@pytest.fixture
def test_db():
    """Create a test database"""
    db = TodoDatabase("test_todos.db")
    yield db
    # Cleanup after tests
    if os.path.exists("test_todos.db"):
        os.remove("test_todos.db")


class TestTodoDatabase:
    """Test suite for TodoDatabase class"""
    
    def test_database_initialization(self, test_db):
        """Test database is initialized correctly"""
        assert test_db.db_name == "test_todos.db"
        assert os.path.exists("test_todos.db")
    
    def test_create_todo(self, test_db):
        """Test creating a new todo"""
        todo_data = TodoCreate(
            title="Test Todo",
            description="Test Description",
            due_date="2025-12-31"
        )
        
        result = test_db.create_todo(todo_data)
        
        assert result is not None
        assert result['id'] == 1
        assert result['title'] == "Test Todo"
        assert result['description'] == "Test Description"
        assert result['completed'] == 0  # SQLite stores False as 0
    
    def test_get_all_todos_empty(self, test_db):
        """Test getting todos from empty database"""
        todos = test_db.get_all_todos()
        assert todos == []
    
    def test_get_all_todos(self, test_db):
        """Test getting all todos"""
        # Create multiple todos
        todo1 = TodoCreate(title="Todo 1", description="First")
        todo2 = TodoCreate(title="Todo 2", description="Second")
        
        test_db.create_todo(todo1)
        test_db.create_todo(todo2)
        
        todos = test_db.get_all_todos()
        
        assert len(todos) == 2
        assert todos[0]['title'] == "Todo 2"  # Most recent first
        assert todos[1]['title'] == "Todo 1"
    
    def test_get_todo_by_id(self, test_db):
        """Test getting a specific todo by ID"""
        todo_data = TodoCreate(title="Find Me")
        created = test_db.create_todo(todo_data)
        
        result = test_db.get_todo_by_id(created['id'])
        
        assert result is not None
        assert result['id'] == created['id']
        assert result['title'] == "Find Me"
    
    def test_get_todo_by_id_not_found(self, test_db):
        """Test getting non-existent todo"""
        result = test_db.get_todo_by_id(999)
        assert result is None
    
    def test_update_todo(self, test_db):
        """Test updating a todo"""
        todo_data = TodoCreate(title="Original Title")
        created = test_db.create_todo(todo_data)
        
        update_data = TodoUpdate(
            title="Updated Title",
            completed=True
        )
        
        result = test_db.update_todo(created['id'], update_data)
        
        assert result is not None
        assert result['title'] == "Updated Title"
        assert result['completed'] == 1  # SQLite stores True as 1
    
    def test_update_todo_partial(self, test_db):
        """Test partial update of todo"""
        todo_data = TodoCreate(
            title="Original",
            description="Original Description"
        )
        created = test_db.create_todo(todo_data)
        
        update_data = TodoUpdate(completed=True)
        result = test_db.update_todo(created['id'], update_data)
        
        assert result['title'] == "Original"  # Unchanged
        assert result['description'] == "Original Description"  # Unchanged
        assert result['completed'] == 1  # SQLite stores True as 1
    
    def test_update_todo_not_found(self, test_db):
        """Test updating non-existent todo"""
        update_data = TodoUpdate(title="New Title")
        result = test_db.update_todo(999, update_data)
        assert result is None
    
    def test_delete_todo(self, test_db):
        """Test deleting a todo"""
        todo_data = TodoCreate(title="Delete Me")
        created = test_db.create_todo(todo_data)
        
        result = test_db.delete_todo(created['id'])
        
        assert result is True
        
        # Verify it's deleted
        found = test_db.get_todo_by_id(created['id'])
        assert found is None
    
    def test_delete_todo_not_found(self, test_db):
        """Test deleting non-existent todo"""
        result = test_db.delete_todo(999)
        assert result is False
    
    def test_get_stats_empty(self, test_db):
        """Test stats with empty database"""
        stats = test_db.get_stats()
        
        assert stats['total'] == 0
        assert stats['completed'] == 0
        assert stats['pending'] == 0
    
    def test_get_stats(self, test_db):
        """Test database statistics"""
        # Create some todos
        todo1 = TodoCreate(title="Todo 1")
        todo2 = TodoCreate(title="Todo 2")
        todo3 = TodoCreate(title="Todo 3")
        
        created1 = test_db.create_todo(todo1)
        test_db.create_todo(todo2)
        test_db.create_todo(todo3)
        
        # Mark one as completed
        test_db.update_todo(created1['id'], TodoUpdate(completed=True))
        
        stats = test_db.get_stats()
        
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['pending'] == 2