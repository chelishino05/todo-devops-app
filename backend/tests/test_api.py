"""
Integration tests for FastAPI endpoints
Tests API routes and responses
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Setup test database before each test"""
    from database import TodoDatabase
    import main
    
    db_name = "test_api.db"
    main.db = TodoDatabase(db_name)
    
    yield
    
    # Cleanup
    if os.path.exists(db_name):
        os.remove(db_name)


def test_health_check():
    """Test health check endpoint"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'


def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/metrics")
    
    assert response.status_code == 200


def test_create_todo():
    """Test creating a todo via API"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "due_date": "2025-12-31"
    }
    
    response = client.post("/api/todos", json=todo_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == "Test Todo"


def test_get_all_todos():
    """Test getting all todos"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/api/todos")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_todo_by_id():
    """Test getting a specific todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo first
    create_response = client.post("/api/todos", json={"title": "Find Me"})
    todo_id = create_response.json()['id']
    
    # Get it by ID
    response = client.get(f"/api/todos/{todo_id}")
    
    assert response.status_code == 200
    assert response.json()['title'] == "Find Me"


def test_update_todo():
    """Test updating a todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Original"})
    todo_id = create_response.json()['id']
    
    # Update it
    response = client.put(f"/api/todos/{todo_id}", json={"title": "Updated"})
    
    assert response.status_code == 200
    assert response.json()['title'] == "Updated"


def test_delete_todo():
    """Test deleting a todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Delete Me"})
    todo_id = create_response.json()['id']
    
    # Delete it
    response = client.delete(f"/api/todos/{todo_id}")
    
    assert response.status_code == 200